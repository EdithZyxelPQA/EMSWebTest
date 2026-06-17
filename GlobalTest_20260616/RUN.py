import json
import subprocess
import os
import sys
from concurrent.futures import ProcessPoolExecutor

def load_channels():
    """從你的環境設定檔中撈出所有要執行的測試設備 (NODE)"""
    with open("environment_parameter.json", encoding="utf-8") as f:
        data = json.load(f)
    execute_nodes = data["EMS"]["executeNode"]
    if isinstance(execute_nodes, list):
        return execute_nodes
    else:
        return [execute_nodes]  # 如果只有單個字串，包成 list

def run_pytest_for_node(node_info):
    """
    將把 node_name 與 test_case 包成 tuple 傳進來
    """
    node_name, test_case, reruns_count = node_info
    print(f"\n================ [啟動] 開始執行設備: {node_name} ================")

    # 建立測試指令，其中的測試目標改為動態變數 test_case
    cmd = [
        "pytest",
        test_case,
        "-v",
        "-s",
        f"--html=report/report_{node_name}.html",
        f"--capture=sys",
        f"--cmdopt={node_name}"
    ]
    if reruns_count > 0:
        print(f"若測試失敗將自動重試 {reruns_count} 次")
        cmd.append(f"--reruns={reruns_count}")
    
    # 執行指令，各設備的變數互不干擾
    result = subprocess.run(cmd, capture_output=False, text=True)
    
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

    # 讓使用者輸入想要執行的 Pytest 項目
    print("\n" + "="*50)
    print("請輸入要執行的 Pytest 測試項目。範例：")
    print("  - 跑單一 Case : Icat.py::TestIcat::test_EMS1_5489_deviceStatus")
    print("  - 跑整份檔案 : Restful.py")
    print(" [提示] 直接按下 Enter 鍵不輸入，將自動執行預設的 Icat.py::TestIcat::test_EMS1_5489_deviceStatus")
    print("="*50)
    
    user_case = input("請輸入測試項目: ").strip()
    
    # 防呆預設值
    if not user_case:
        test_case = "Icat.py::TestIcat::test_EMS1_5489_deviceStatus"
    else:
        test_case = user_case

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
    print(f"目前指定測試項目 : {test_case}")
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

        tasks = [(node, test_case, reruns_count) for node in nodes]
        
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            results = executor.map(run_pytest_for_node, tasks)
            final_results = list(results)
            
    elif mode == "2":
        # 模式 2：依序執行
        print(f"\n 正在啟動 [依序執行] 測試，將會依序跑完各個設備...\n")
        
        for node in nodes:
            # 依序呼叫並傳入當前設備與測試項目
            res = run_pytest_for_node((node, test_case, reruns_count))
            final_results.append(res)
    else:
        print(" 輸入錯誤！請輸入 1 或 2。程式即將結束。")
        return

    # 收集並列印最終執行結果總結
    print("\n" + "="*40 + "\n總測試執行總結：")
    print(f"測試項目: {test_case}")
    print(f"重試次數: {reruns_count} 次")
    for node_name, returncode in final_results:
        status = "成功 (PASS)" if returncode == 0 else "失敗 (FAIL)"
        print(f"  - 設備 {node_name}: {status}")
    print("="*40)

if __name__ == "__main__":
    main()