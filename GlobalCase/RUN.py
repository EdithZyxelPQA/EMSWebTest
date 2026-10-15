import json
import importlib.util
import subprocess
import os
import shutil
import sys
from concurrent.futures import ProcessPoolExecutor

CASE_TYPES = {
    "1": "Icat",
    "2": "Restful",
    "3": "Provision",
    "4": "Unicase",
    "5": "server",
}


def resolve_test_python():
    """選擇仍提供 telnetlib、可執行既有 EMS case 的 Python。"""
    configured = os.environ.get("EMSWEB_PYTHON", "").strip()
    candidates = [configured] if configured else []
    if sys.version_info < (3, 13) and importlib.util.find_spec("telnetlib"):
        candidates.append(sys.executable)

    launcher = shutil.which("py")
    if launcher:
        probe = subprocess.run(
            [launcher, "-3.11", "-c", "import sys; print(sys.executable)"],
            capture_output=True,
            text=True,
        )
        if probe.returncode == 0 and probe.stdout.strip():
            candidates.append(probe.stdout.strip().splitlines()[-1])

    local_app_data = os.environ.get("LOCALAPPDATA", "")
    if local_app_data:
        candidates.append(
            os.path.join(local_app_data, "Programs", "Python", "Python311", "python.exe")
        )

    checked = []
    for candidate in candidates:
        if not candidate or candidate in checked:
            continue
        checked.append(candidate)
        probe = subprocess.run(
            [candidate, "-c", "import telnetlib, pytest"],
            capture_output=True,
            text=True,
        )
        if probe.returncode == 0:
            return candidate
    raise RuntimeError(
        "找不到相容的 Python。EMSWeb 目前需要含 telnetlib 的 Python 3.11/3.12；"
        "可設定 EMSWEB_PYTHON 指向相容的 python.exe。"
    )


def plugin_available(python_executable, module_name):
    """確認實際執行 pytest 的 Python 是否已安裝指定 plugin。"""
    result = subprocess.run(
        [
            python_executable,
            "-c",
            "import importlib.util,sys; "
            "sys.exit(0 if importlib.util.find_spec(sys.argv[1]) else 1)",
            module_name,
        ],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0

def load_channels():
    """從你的環境設定檔中撈出所有要執行的測試設備 (NODE)"""
    with open("environment_parameter.json", encoding="utf-8") as f:
        data = json.load(f)
    execute_nodes = data["EMS"]["executeNode"]
    if isinstance(execute_nodes, list):
        return execute_nodes
    else:
        return [execute_nodes]  # 如果只有單個字串，包成 list

def parse_case_types(user_input):
    """解析編號或類型名稱；空白代表執行全部類型。"""
    if not user_input:
        return []

    name_lookup = {name.lower(): name for name in CASE_TYPES.values()}
    selected_types = []
    for item in user_input.split(","):
        value = item.strip()
        case_type = CASE_TYPES.get(value) or name_lookup.get(value.lower())
        if not case_type:
            valid_values = ", ".join(CASE_TYPES.values())
            raise ValueError(f"無效的 Case 類型：{value}（可選：{valid_values}）")
        if case_type not in selected_types:
            selected_types.append(case_type)
    return selected_types

def normalize_test_target(user_input):
    """建立 GlobalCase.py 的單一 Case node id；空白代表非單一 Case。"""
    if not user_input:
        return "GlobalCase.py"
    if user_input.startswith("GlobalCase.py::TestGlobalCase::test_EMS1_"):
        return user_input
    if user_input.startswith("TestGlobalCase::test_EMS1_"):
        return f"GlobalCase.py::{user_input}"
    if user_input.startswith("test_EMS1_"):
        return f"GlobalCase.py::TestGlobalCase::{user_input}"
    raise ValueError(
        "請輸入 test_EMS1_xxx；也可輸入完整的 "
        "GlobalCase.py::TestGlobalCase::test_EMS1_xxx"
    )

def run_pytest_for_node(node_info):
    """
    將 node_name、test_target、selected_types 與 reruns_count 包成 tuple 傳進來
    """
    node_name, test_target, selected_types, reruns_count = node_info
    print(f"\n================ [啟動] 開始執行設備: {node_name} ================")
    test_python = resolve_test_python()
    print(f"使用測試 Python：{test_python}")

    # GlobalCase.py 是固定測試目標；有選類型時以 marker 過濾。
    cmd = [
        test_python,
        "-m",
        "pytest",
        test_target,
        "-vv",
        "-s",
        f"--capture=sys",
        f"--cmdopt={node_name}"
    ]
    if plugin_available(test_python, "pytest_html"):
        cmd.append(f"--html=report/report_{node_name}.html")
    else:
        print(
            "[警告] 目前 Python 未安裝 pytest-html，將繼續執行測試，"
            "但不產生 HTML 報告。"
        )
    if selected_types and test_target == "GlobalCase.py":
        cmd.extend(["-m", " or ".join(selected_types)])
    if reruns_count > 0:
        if plugin_available(test_python, "pytest_rerunfailures"):
            print(f"若測試失敗將自動重試 {reruns_count} 次")
            cmd.append(f"--reruns={reruns_count}")
        else:
            print(
                "[警告] 目前 Python 未安裝 pytest-rerunfailures，"
                "本次不執行失敗重試。"
            )
    
    # pytest-html 可能寫入 EMS icon 的 Unicode 私用字元；強制使用 UTF-8，
    # 避免 Windows 預設 CP950 在 session finish 時讓報告產生失敗。
    child_env = os.environ.copy()
    child_env["PYTHONUTF8"] = "1"
    child_env["PYTHONIOENCODING"] = "utf-8"
    path_entries = child_env.get("PATH", "").split(os.pathsep)
    stale_driver_dirs = [
        entry
        for entry in path_entries
        if entry and os.path.isfile(os.path.join(entry, "chromedriver.exe"))
    ]
    if stale_driver_dirs:
        child_env["PATH"] = os.pathsep.join(
            entry for entry in path_entries if entry not in stale_driver_dirs
        )
        print(
            "[提示] 已從本次 pytest PATH 排除獨立 ChromeDriver 目錄，"
            "改由 Selenium Manager 選擇相容版本："
            + ", ".join(stale_driver_dirs)
        )

    # 執行指令，各設備的變數互不干擾
    result = subprocess.run(
        cmd,
        capture_output=False,
        text=True,
        env=child_env,
    )
    
    print(f"================ [結束] 設備 {node_name} 執行完畢 ================\n")
    return node_name, result.returncode

def main():
    # 取得 JSON 預設的所有節點
    default_nodes = load_channels()
    
    # 開放讓使用者輸入想要執行的設備
    print("\n" + "="*50)
    print(f"JSON 檔預設的設備清單為: {default_nodes}")
    print("請輸入本次要執行的設備名稱 (多個設備請用英文逗號 `,` 隔開)")
    print(" 範例: 192.168.168.85, 192.168.168.87")
    print(" [提示] 直接按下 Enter 鍵不輸入，將自動執行預設的所有設備")
    print("="*50)
    
    user_nodes = input("請輸入執行設備: ").strip()
    
    if not user_nodes:
        nodes = default_nodes
    else:
        # 將輸入的字串切開並去除空格，過濾空字串
        nodes = [node.strip() for node in user_nodes.split(",") if node.strip()]
        
    print(f"確認執行設備：{nodes}")
    
    # 確保報告資料夾存在
    os.makedirs("./report", exist_ok=True)

    # 選擇全部、Group 或單一 Case。
    print("\n" + "="*50)
    print("請選擇測試範圍：")
    print("1. 全部 Case [預設]")
    print("2. Group Case (Icat, Restful, Provision 或 Unicase)")
    print("3. 單一 Case (test_EMS1_xxx)")
    print(" [提示] 直接按下 Enter 鍵不輸入，將選擇 1. 全部 Case")
    print("="*50)

    while True:
        test_scope = input("請輸入選項 (1、2 或 3): ").strip() or "1"
        if test_scope in {"1", "2", "3"}:
            break
        print("⚠️ 輸入錯誤，請輸入 1、2 或 3。")

    test_target = "GlobalCase.py"
    selected_types = []
    case_type_summary = "全部 Case"

    if test_scope == "2":
        print("\n" + "="*50)
        print("請選擇 Group Case：")
        print("1. Icat")
        print("2. Restful")
        print("3. Provision")
        print("4. Unicase")
        print("5. server")
        print("可用英文逗號選擇多個 Group，例如：1,3 或 Icat,Provision")
        print("="*50)
        while True:
            user_case_types = input("請輸入 Group 編號或名稱: ").strip()
            try:
                selected_types = parse_case_types(user_case_types)
                if not selected_types:
                    raise ValueError("Group Case 不可留空")
                break
            except ValueError as error:
                print(f"⚠️ {error}")
        case_type_summary = "Group Case：" + ", ".join(selected_types)

    elif test_scope == "3":
        print("\n" + "="*50)
        print("請輸入單一 Case 名稱。範例：test_EMS1_5489_deviceStatus")
        print("="*50)
        while True:
            user_single_case = input("請輸入單一 Case: ").strip()
            try:
                if not user_single_case:
                    raise ValueError("單一 Case 不可留空")
                test_target = normalize_test_target(user_single_case)
                break
            except ValueError as error:
                print(f"⚠️ {error}")
        case_type_summary = "單一 Case"

    # 重試次數問答，並做防呆處理
    print("\n" + "="*40)
    print("請輸入失敗後的重試次數 (例如: 2 代表失敗會再跑兩次)")
    print(" [提示] 直接按下 Enter 鍵不輸入，預設為 [0] 次 (錯一次即判定失敗)")
    print("="*40)
    
    user_reruns = input("請輸入重試次數: ").strip()
    
    try:
        reruns_count = int(user_reruns) if user_reruns else 0
        if reruns_count < 0:
            reruns_count = 0
    except ValueError:
        print("⚠️ 輸入格式不正確，已自動設定為不重試 (0次)。")
        reruns_count = 0

    # 提供互動選單供使用者選擇執行模式
    print("\n" + "="*40)
    print(f"目前測試項目 : {test_target}")
    print(f"目前 Case 類型 : {case_type_summary}")
    print(f"目前設定重試次數 : {reruns_count} 次")
    print(f"請選擇測試執行模式：(請考慮測試項目內容是否交互影響)")
    print("1. [同時執行] 所有設備並行測試 (多進程)")
    print("2. [依序執行] 設備1測完，才換設備2 (單進程) [預設]")
    print(" [提示] 直接按下 Enter 鍵不輸入，將自動選擇 2. [依序執行]")
    print("="*40)
    
    user_mode = input("請輸入選項 (1 或 2): ").strip()
    if not user_mode:
        mode = "2"
    else:
        mode = user_mode
        
    # 用來存放最終結果的列表
    final_results = []
    
    if mode == "1":
        # 模式 1：同時執行
        max_workers = len(nodes)
        print(f"\n 正在啟動 [同時執行] 測試，最大平行數量: {max_workers}...\n")

        tasks = [(node, test_target, selected_types, reruns_count) for node in nodes]
        
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            results = executor.map(run_pytest_for_node, tasks)
            final_results = list(results)
            
    elif mode == "2":
        # 模式 2：依序執行
        print(f"\n 正在啟動 [依序執行] 測試，將會依序跑完各個設備...\n")
        
        for node in nodes:
            # 依序呼叫並傳入當前設備與測試項目
            res = run_pytest_for_node((node, test_target, selected_types, reruns_count))
            final_results.append(res)
    else:
        print(" 輸入錯誤！請輸入 1 或 2。程式即將結束。")
        return

    # 收集並列印最終執行結果總結
    print("\n" + "="*40 + "\n總測試執行總結：")
    print(f"測試項目: {test_target}")
    print(f"Case 類型: {case_type_summary}")
    print(f"重試次數: {reruns_count} 次")
    for node_name, returncode in final_results:
        status = "成功 (PASS)" if returncode == 0 else "失敗 (FAIL)"
        print(f"  - 設備 {node_name}: {status}")
    print("="*40)

if __name__ == "__main__":
    main()
