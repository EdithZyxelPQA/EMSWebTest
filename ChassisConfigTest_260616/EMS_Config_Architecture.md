# EMS Config 自動化測試框架 — 架構交接文件

> 適用版本：Run_EMS_Config_all.py（多執行緒版）  
> 最後更新：2026-05-05

---

## 目錄

1. [核心架構與設計模式](#1-核心架構與設計模式)
2. [執行配置與併發測試](#2-執行配置與併發測試)
3. [容錯與動態適應機制](#3-容錯與動態適應機制)
4. [報表與後處理工具](#4-報表與後處理工具)

---

## 1. 核心架構與設計模式

### 1.1 三層架構

```
┌────────────────────────────────────────────────────────────┐
│  流程執行層  Run_EMS_Config_all.py                          │
│  · 讀取 ENV JSON、建立 driver、定義測試順序                  │
│  · 每個 thread 執行一個 process_env(env_file) 函式           │
└───────────────────────────┬────────────────────────────────┘
                             │  呼叫 ems.XXX(driver, ...)
┌───────────────────────────▼────────────────────────────────┐
│  腳本層  module/ems_test_module.py                          │
│  · 定義所有具名測試函式（EMS_ACL_*, Sys_*, Port_*, ...）     │
│  · 聚合所有 EMS / FW 功能子模組                             │
│  · 管理 thread-local 狀態（憑證、log 路徑）                 │
└───────────────────────────┬────────────────────────────────┘
                             │  呼叫 mod.*, e_mod.*, e_acl.*, ...
┌───────────────────────────▼────────────────────────────────┐
│  頁面操作層  ems_acl_module / ems_sys_module / ...          │
│  · 每個模組對應一個 EMS 或 FW 功能頁面群組                    │
│  · 底層網頁點擊或輸入文字等互動                               │
└────────────────────────────────────────────────────────────┘
```

### 1.2 模組依賴樹

```
Run_EMS_Config_all.py
├── module/ems_test_module.py          # 腳本層主體
│   ├── EMS 功能子模組
│   │   ├── ems_acl_module.py
│   │   ├── ems_sys_module.py
│   │   ├── ems_switch_module.py
│   │   ├── ems_port_module.py
│   │   ├── ems_vlan_module.py
│   │   ├── ems_multicast_module.py
│   │   ├── ems_profile_module.py
│   │   ├── ems_gpon_module.py
│   │   └── ems_xpon_module.py
│   ├── FW 功能子模組
│   │   ├── xpon_module.py / xpon_olt_config_module.py / ...
│   │   ├── port_module.py / sys_module.py / switch_module.py / vlan_module.py
│   │   └── multicast_module.py / statistics_module.py
│   └── 基礎工具
│       ├── selenium_module.py         # 低層頁面操作 (Login, Page_Switch, ...)
│       ├── ems_module.py              # EMS 頁面操作 (Login_EMS, Click, ...)
│       └── not_support.py            # Not-support 旗標常數
├── module/customdriver.py             # 加強版 Chrome Driver
├── module/globals.py                  # 全域狀態 (msc_card_type)
├── module/get_card.py                 # FW 卡片偵測
└── module/telnet_module.py            # 測試結尾 write memory
```

### 1.3 典型測試流程（單一 env_file）

```
1. 讀取 ENV JSON → 解析 FW/EMS 連線資訊、卡片資訊
2. CustomDriver 建立 Chrome session
3. 登入 FW Web → 讀取 MSC 型號與版本
4. 偵測 FW title 判斷是否為 NeoX（設定 if_Neox 旗標）
5. Maintenance Config Reset（恢復出廠，確保測試環境乾淨）
6. EMS_Set_Prepare（設定 SNMP 社群字串等前置條件）
7. get_card.get_card_case() → 掃描所有 active slot，依卡片類型分類為 list1
8. 登入 EMS Web → 讀取 EMS 版本號
9. 執行 No Card Test（System/ACL/Multicast/Switch/VLAN 等無卡片依賴的測試）
10. 迴圈 list1 → 依每張卡片執行 Card Test（ACL/Port/VLAN/GPON/XPON 等）
11. Config Reset + write memory（清理）
```

### 1.4 卡片分類邏輯（get_card.py）

`get_card_case()` 掃描 FW Home 頁面所有 active slot 後，依卡片名稱分為四類：

| Case | 卡片類型 | 說明 |
|------|---------|------|
| Case 1 | GLC1440X、GLC1540X、NXA | GE 線卡 |
| Case 2 | XPON 系列、NXP | XG-PON / XGSPON 線卡 |
| Case 3 | GPON 系列（OLC3416-42A 等） | GPON 線卡 |
| Case 4 | MSC、NXC | 主控卡 |

每個 list1 元素格式為 `"case,slot,port,cardtype"`，後續 Card Test 迴圈以此解包 slot/port/cardtype。

### 1.5 測試函式命名規範

腳本層函式皆依功能頁面命名，例：

- `EMS_ACL_*` — EMS > ACL 功能
- `Sys_*` — EMS > System 功能
- `Switch_*` — EMS > Switch 功能
- `Port_*` — EMS > Port 功能
- `VLAN_*` — EMS > VLAN 功能
- `Multicast_*` — EMS > Multicast 功能
- `ONT_*Profile` — EMS > Provision > Profile 功能
- `xPON_OLT_Config` / `GPON_OLT_Registration` — xPON/GPON 線卡測試

每個函式的典型操作順序：**Web EMS Set → EMS Check → FW Check**，即先透過 EMS 設定參數，再驗證 EMS 畫面顯示是否正確，最後連回 FW Web 確認設定同步。

---

## 2. 執行配置與併發測試

### 2.1 環境檔格式

環境設定以 JSON 管理，路徑慣例 `ENV/ENV_WEB_{IP後段}.json`。

```json
{
  "ZYXEL_DUT": {
    "NODE1": {
      "url": "http://192.168.1.82/",
      "login_username": "admin",
      "login_password": "1234",
      "default_username": "admin",
      "default_password": "1234",
      "name": "IES5206",
      "map_name": "...",
      "set_community": "...",
      "get_community": "...",
      "inband_vlan": "...",
      "CARDINFO": {
        "MSC":         { "slot_id": "1", "port_id": "1" },
        "GLC1440X":    { "slot_id": "3", "port_id": "1" },
        "OLC3416-42A": { "slot_id": "5", "port_id": "1" }
      },
      "ONTINFO": {
        "XPON": {
          "ONT1": {
            "slot_id": "4", "port_id": "1", "ont_id": "1",
            "sn_12": "...", "sn_16": "...", "pw": "...",
            "ont_user": "...", "ont_pw": "...", "service_mode": "..."
          }
        }
      }
    }
  },
  "EMS": {
    "url": "http://192.168.128.8:9116/netatlasems/",
    "login_username": "admin",
    "login_password": "Admin1234!"
  },
  "LOOP": { "count": 1 }
}
```

> 新增受測設備時，複製既有 JSON，修改 IP、帳密、卡片 slot/port 資訊即可。

### 2.2 CLI 啟動語法

```bash
# 單台設備（預設 82）
python Run_EMS_Config_all.py

# 指定單台
python Run_EMS_Config_all.py 206

# 同時對多台設備平行執行
python Run_EMS_Config_all.py 82 206 222 88
```

腳本以 `argparse` 接收 `env_ids`（`nargs='*'`，預設 `['82']`），再組成 `ENV/ENV_WEB_{id}.json` 路徑清單。

### 2.3 多執行緒機制

```python
max_workers = len(env_list)
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    future_map = {executor.submit(process_env, env_file): env_file
                  for env_file in env_list}
```

- 每個 env_file 對應一個 thread，thread 內各自建立 `CustomDriver` 實例，不共用瀏覽器 session。
- Thread-local 設計：
  - `_tls = threading.local()` — 各 thread 各自存放 log 檔路徑（`get_file_name()`）。
- 失敗的 thread 會將 traceback 寫入 `Report/error_{env_file}.log`，不影響其他 thread 繼續執行。

### 2.4 NeoX 動態分支

```python
if "Neox".lower() in driver.title.lower():
    if_Neox = True
ems.parameter_add("if_Neox", if_Neox)
```

偵測 FW web title 判斷機型。NeoX 專屬測試（Loopguard、BPDU Control）僅在 `if_Neox == True` 時執行：

```python
if if_Neox:
    ems.EMS_Neox_ACL_Loopguard(...)
    ems.EMS_Neox_ACL_BPDU_Ctrl(...)
```
這邊 Cecily 說可能以後不會再區分 NeoX 或非 NeoX 而執行不同的 test script，預期兩邊結果應該相同。但目前 script 仍有 if if_Neox: 分支存在

### 2.5 操作節奏控制

每次 `find_element` / `find_elements` 前的固定等待時間，從檔案讀取：

```
ENV/time_sleep_before_find_element.txt
→ time_sleep_before_find_element = '0.3'
```

若檔案不存在，腳本會自動建立並寫入預設值 `0.3`。此值傳入 `CustomDriver(time_sleep=...)` 後生效於所有元素查找。

---

## 3. 容錯與動態適應機制

### 3.1 @retry 裝飾器

**位置：** `module/ems_test_module.py:142`

所有測試函式均以 `@retry()` 裝飾（預設 `max_retries=2, delay=2`）。

**行為流程：**

```
執行 func()
├── 成功 → 記錄耗時到 log，return 結果
└── 例外
    ├── 寫入錯誤訊息與 traceback（PrintException）到 log
    ├── 若還有重試次數
    │   ├── driver.execute_script("window.stop()")  ← 中止卡住的頁面
    │   ├── driver.get("about:blank")               ← 釋放 renderer 資源
    │   ├── time.sleep(delay)
    │   └── 重新執行 func()
    └── 若已耗盡重試次數
        ├── 寫入 "failed after N attempts. Skipping..."
        ├── driver.save_screenshot("Report/{timestamp}_{funcname}_screenshot.png")
        └── return None（跳過此測試，不中斷整體流程）
```

**關鍵設計：** 失敗不拋出例外，改為 `return None`，確保後續測試項目仍可繼續執行。

### 3.2 CustomDriver 元素查找容錯

**位置：** `module/customdriver.py:67`

`find_element()` / `find_elements()` 均包含 3 次重試：

```python
for i in range(3):
    try:
        super().find_element(by, value)
        break
    except TimeoutException:
        # Renderer 超時：先 window.stop() + get("about:blank") 再等 3 秒
        _try_recover_renderer(self, wait_sec=3)
    except Exception:
        time.sleep(1)
return super().find_element(by, value)
```

此機制在 `@retry` 之前就先攔截元素查找失敗，是第一道防線。

### 3.3 ChromeDriver 自動更新

**位置：** `module/customdriver.py:53`

```python
try:
    super().__init__(service=ChromeService())
except:
    import module.update_my_chromedriver   # 自動下載對應版本
    super().__init__(service=ChromeService())
```

Chrome 瀏覽器升版後 driver 版本不符時，會自動觸發下載，無需手動介入。

### 3.4 EMS 登入防呆

**位置：** `Run_EMS_Config_all.py:179`、`module/selenium_module.py:35`

```python
try:
    driver.find_element('id', 'helpMenu').click()
except:
    mod.Login_EMS(driver, username, ems_password)  # session 失效則重新登入
    time.sleep(5)
    driver.find_element('id', 'helpMenu').click()
```

`Login_EMS()` 本身亦包含最多 3 次的登入重試迴圈。

### 3.5 Config Reset 完成等待

**位置：** `module/ems_test_module.py:211`

```python
while state_n != "idle":
    time.sleep(2)
    state_n = driver.find_element_by_class_name("state").text
```

Config Reset 後以輪詢方式等待 FW 狀態回到 `idle`，確保後續測試在設備完全就緒後才繼續。

### 3.6 測試結尾清理

1. `Maintenance_Config_Reset(driver)` — 恢復出廠設定，為下次測試清場。
2. `time.sleep(30)` — 等待 FW 重啟穩定。
3. Telnet `write memory` — 將 running config 寫入 startup config，確保設定持久化。

---

## 4. 報表與後處理工具

### 4.1 Log 檔命名規則

```
Report/Web_EMS_Config_Card_{FW_title}_{EMS_version}_{日期時分}_{IP後3碼}.log
```

範例：`Report/Web_EMS_Config_Card_IES5206_V5.30_2026-05-05 1423_082.log`

- 每個 thread（每台受測設備）產生各自獨立的 log 檔，不互相覆蓋。
- 錯誤時額外產生 `Report/error_{env_file}.log`。

### 4.2 Log 結構

```
EMS Web Auto Report
{datetime}
EMS Web IP: ...   EMS Version: ...
FW Web IP: ...    FW MSC: slot-port/cardtype/version
if_Neox: True/False
[card list]
========================
No Card Test (System?)
========================
  ...（No Card 測試結果）
  No Card Test  Total time: 0 hr 12 min 34 sec
[Page]
========================
Card Test
========================
>>> [ GLC1440X ] <<<
  Now in case:1, Slot-Port:3-1, GLC1440X  (1/3)
  ...（Card 測試結果）
[Page]
>>> [ OLC3416-42A ] <<<
  ...
```

`[Page]` 標記為 `split_report.py` 的切割依據之一。
`>>>>...[ CardType ]` 標記為各卡片段落的起點。

### 4.3 split_report.py — 報表切割工具

**用法：**

```bash
python split_report.py "Report/Web_EMS_Config_Card_IES5206_V5.30_2026-05-05 1423_082.log"
```

無參數執行時，會列出 `Report/` 目錄下所有可切割的 `.log` 檔供參考。

**切割邏輯：**

1. 掃描 log，找到 `No Card Test ... Total time` 行 → 定義 System 段落結尾。
2. 掃描 `>>>>...[CardType]` 標記 → 定義每張卡片的段落起點與終點。
3. 輸出：
   - `{原檔名}_System.log` — No Card Test 全段
   - `{原檔名}_{CardType前3碼}.log` — 每張卡片獨立報告（含 log 開頭的前 18 行版本資訊）
   - 同型卡多張時自動加後綴：`GLC`, `GLC_2`, `GLC_3`

**輸出範例（原檔 `..._082.log`）：**

```
..._082_System.log
..._082_GLC.log
..._082_OLC.log
..._082_MSC.log
```

### 4.4 @retry 內建計時紀錄

每個測試函式在 log 中自動記錄：

```
             In EMS_ACL_PPPoE /path/ems_test_module.py:916
...（測試輸出）
                                                           [TIME 0:3:21]   2026-05-05 14:26:07.123456
```

失敗時記錄：

```
Error in EMS_ACL_PPPoE: element not found...
{traceback}
-------------------------------------- Retry -----------------------------------------
...
EMS_ACL_PPPoE failed after 2 attempts. Skipping...
==============================================================================
                                                           [TIME 0:0:12]   2026-05-05 14:26:19.456789
```

截圖儲存於 `Report/{timestamp}_{funcname}_screenshot.png`。

---

## 附錄：環境準備清單

| 項目 | 說明 |
|------|------|
| Chrome 瀏覽器 | 安裝即可，ChromeDriver 由框架自動管理 |
| `ENV/ENV_WEB_{id}.json` | 每台受測設備一份，依 1.2 節格式填寫 |
| `ENV/time_sleep_before_find_element.txt` | 首次執行若不存在會自動建立（預設 0.3 秒） |
| `Report/` 資料夾 | 首次執行若不存在會自動建立 |
| Python 套件 | `selenium==4.1.5`, `pyautogui`, `attr`, `pyrsistent`, `pywin32` |

## 附錄：常見維護操作

| 情境 | 操作 |
|------|------|
| 新增受測設備 | 複製任一 `ENV/ENV_WEB_*.json`，修改 IP / 帳密 / 卡片資訊 |
| 調整操作速度 | 修改 `ENV/time_sleep_before_find_element.txt` 內的數值 |
| 新增 NeoX 專屬測試 | 在 Card Test 迴圈內加 `if if_Neox: ems.新函式(...)` |
| 切割已完成的報告 | `python split_report.py "Report/xxxxx.log"` |
| 單獨執行特定設備 | `python Run_EMS_Config_all.py {IP後段}` |
