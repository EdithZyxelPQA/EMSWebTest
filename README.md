# EMSWebTest

NetAtlas EMS Web 自動化測試資產（來源：`D:\Auto\EMS\Agent\EMSWeb`，快照日期 2026-10-15）。

2026-06-16 的舊快照（`GlobalTest_20260616`、`EMSNewCaseTest_20260616`、`ChassisConfigTest_260616`、`Olt140xConfigTest_20260616`）已由目前架構取代；需要時可從 git 歷史（commit `3247148`）取回。

## 目錄架構

```text
EMSWebTest/
├── GlobalCase/              # 主要 EMS Web 測試專案（pytest）
├── ChassisConfigTest/       # Chassis 設備 EMS 設定測試
├── Olt140xConfigTest/       # OLT140x EMS 設定測試
├── tools/                   # 建置 / 維護 GlobalCase 的工具腳本
├── local/testlink_audit/    # TestLink 上傳紀錄（逐筆 execution）
├── .qa-artifacts/           # TestLink 上傳前的 preview 檔
├── .qa-audits/              # TestLink 上傳 workflow 紀錄
├── qa_normalized_*.txt      # 已正規化、用於上傳 TestLink 的測試結果
├── NetAtlasEMS_UserGuide.pdf
├── TestPlan_NetAtlasEMS-20260615.xlsx
└── PROJECT_MEMORY.md
```

## GlobalCase

由舊的 `GlobalTest_20260616` 與 `EMSNewCaseTest_20260616` 整併而成，所有 case 集中在 `GlobalCase.py`。

| 檔案 / 資料夾 | 說明 |
| --- | --- |
| `RUN.py` | 互動式執行入口：選擇設備 node、Group（Icat / Restful / Provision / Unicase / server）、單一 case、重試次數與平行 / 依序模式 |
| `GlobalCase.py` | 全部測試 case |
| `conftest.py`、`pytest.ini` | pytest 設定與 fixture |
| `libs/` | 共用函式庫（瀏覽器、設備 CLI、EMS 頁面操作、報告等） |
| `docs/` | 個別 case（`EMS1-xxxx`）的說明文件 |
| `environment_parameter.json` | EMS URL / 帳密 / 版本、DUT 與 ONT 等測試環境參數 |
| `*.list` | 各 Group 的 case 清單（`Web_EMS_ICAT.list`、`Web_EMS_Unicase.list` …） |
| `ForUpload/` | 韌體升級等 case 使用的上傳檔（以 Git LFS 儲存） |
| `Run_Elevated.ps1`、`Setup_ElevatedTask.ps1`、`Start_Elevated.ps1` | 以系統管理員權限執行（例如需寫入 LocalMachine 憑證的 case） |
| `USER_RUN_GUIDE.md` | 使用者執行指南 |

### 執行

需使用仍提供 `telnetlib` 的 Python（3.11；可用環境變數 `EMSWEB_PYTHON` 指定），並確認 chromedriver 在 PATH 中。

```powershell
cd GlobalCase
pip install -r requirements.txt
python RUN.py
```

執行前請先確認 `environment_parameter.json` 的 `EMS.url`、`EMS.version`、`EMS.executeNode` 與 `ZYXEL_DUT` 設定。HTML 報告輸出到 `GlobalCase/report/`（不納入版控）。

## ChassisConfigTest

Chassis 設備的 EMS 設定 / Profile 測試。

- `RunSelect.py`：tkinter 介面，勾選要執行的 `Run_EMS_*.py`
- `Run_EMS_Config_*.py`、`Run_EMS_Profiles_*.py`、`Run_EMS_*_Retest.py`：各類設定與重測腳本
- `module/`：共用模組；`ENV/`：各台 DUT / EMS 的環境設定（`ENV_WEB_<ip>.json`）
- 架構說明：`EMS_Config_Architecture.md`、`EMS_Profile_Architecture.md`

## Olt140xConfigTest

OLT140x 系列的 EMS 設定測試。

- `EXE.py`（及打包好的 `Run_EMS_Config_OLT140x.exe`）：執行入口
- `ems_*_module.py`、`*_module.py`：各功能模組
- `Telnet_Check_project/`：Telnet CLI 檢查
- 架構說明：`EXE_Architecture.md`

## tools

- `build_global_case.ps1`：由舊的 GlobalTest / EMSNewCaseTest 來源合併產生 `GlobalCase`（來源資料夾已不在此 repo，需要時從 git 歷史取回）
- `generate_global_case_test_names.py`、`merge_global_case_lists.py`：產生 / 合併 case 清單
- `normalize_python_imports.py`、`inspect_map_power_supply.py`：維護用工具

## 版控說明

- `GlobalCase/ForUpload/**` 使用 Git LFS，clone 前請先安裝 `git lfs`。
- 不納入版控：`download/`、`report/`、`Report/`、`Output/`、`*.log`、`__pycache__/`、`.pytest_cache/`、`debug_artifacts/`。
- 環境設定檔含設備 / EMS 登入資訊與內網 IP，本 repo 為公開 repo，請留意。
