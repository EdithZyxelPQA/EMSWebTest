# OLT140x EMS 自動化測試框架 — 架構交接文件

> 適用版本：EXE.py（OLT140x 專用執行層）  
> 專案目錄：web_auto_OLT1408_EMS_project_240319  
> 最後更新：2026-05-06

---

## 目錄

1. [專案定位與與 IES 專案的差異](#1-專案定位與與-ies-專案的差異)
2. [核心架構](#2-核心架構)
3. [執行配置與多執行緒](#3-執行配置與多執行緒)
4. [測試流程詳解](#4-測試流程詳解)
5. [OLT140x 機型差異處理](#5-olt140x-機型差異處理)
6. [報表輸出](#6-報表輸出)

---

## 1. 專案定位與與 IES 專案的差異

本專案針對 **OLT140x 系列**（OLT1404A-IA、OLT1404B-IA、OLT1408A-IA、OLT1408B-IA、OLT1408A-C）進行 EMS Web 自動化測試，與 IES/NeoX 的 `Run_EMS_Config_all.py` 共用相同的設計哲學，但針對 OLT 設備的特性有幾處重要差異：

| 面向 | IES/NeoX（Run_EMS_Config_all.py） | OLT140x（EXE.py） |
|------|----------------------------------|-------------------|
| 受測設備 | IES 系列（模組化機箱，多卡片） | OLT140x 系列（固定形式因素） |
| 測試前清理 | FW Web → Maintenance Config Reset | **Telnet** `er ru ext` 抹除 running config |
| FW Web 登入方式 | 表單輸入帳密 | URL 嵌入憑證 `http://user:pass@ip` |
| FW 頁面導覽 | `mod.Switch_Frame()` | `mod.Switch_Specific_Frame(n)`（指定 frame 編號 3/4/6） |
| 卡片偵測 | `get_card.get_card_case()` 動態掃描 | 無（OLT 無卡片概念，port 固定） |
| NeoX 動態分支 | 有（`if if_Neox:`） | 無 |
| Port 名稱計算 | 直接從 ENV 取得 | 依機型動態計算（見第 5 節） |
| 腳本層模組 | `ems_test_module.py`（alias: ems） | `ems_test_module_OLT1408.py`（alias: emss） |
| 頁面操作層 | `ems_*_module.py`（功能分類） | `ems_module_OLT1408.py`（統一單一模組） |
| 模組路徑 | `module/` 子目錄 | 專案根目錄（平坦結構） |
| 輸出資料夾 | `Report/` | `Output/` |
| max_workers 上限 | `len(env_list)`（無上限） | `min(4, len(env_list))`（上限 4） |
| 預設 env_id | `82` | `207` |

---

## 2. 核心架構

### 2.1 三層結構

```
┌────────────────────────────────────────────────────────────┐
│  流程執行層  EXE.py                                         │
│  · 讀取 ENV JSON、建立 driver、Telnet 前置清理              │
│  · 計算 OLT 機型相關的 Port 名稱                            │
│  · 依序呼叫所有 OLT 測試函式                                │
└───────────────────────────┬────────────────────────────────┘
                             │  呼叫 emss.XXX(driver, ...)
┌───────────────────────────▼────────────────────────────────┐
│  腳本層  ems_test_module_OLT1408.py (alias: emss)           │
│  · 定義所有 OLT140x 測試函式（Basic_*, IP_*, Advanced_*）   │
│  · @retry 裝飾器容錯機制                                    │
└───────────────────────────┬────────────────────────────────┘
                             │  呼叫 e_swi.*, e_mod.*, mod.*
┌───────────────────────────▼────────────────────────────────┐
│  頁面操作層  ems_module_OLT1408.py (alias: e_swi)           │
│  · 細粒度 UI helpers（Basic_General_Apply、                 │
│    Basic_Switch_WRED、Basic_Port_Speed 等）                 │
│  · web_share/EMS/ems_module.py — 共用 EMS 操作              │
└────────────────────────────────────────────────────────────┘
```

### 2.2 模組依賴樹

```
EXE.py
├── ems_test_module_OLT1408.py        # OLT 腳本層（alias: emss）
│   ├── ems_module_OLT1408.py         # OLT 頁面操作層（alias: e_swi）
│   ├── web_share/EMS/ems_module.py   # 共用 EMS 頁面操作（alias: e_mod）
│   ├── ems_profile_module.py         # Profile UI helpers（alias: e_pro）
│   └── selenium_module.py            # 低層頁面操作（alias: mod）
├── ems_test_module.py                # IES 共用腳本層（alias: ems，本專案未實際呼叫）
├── customdriver.py                   # 加強版 Chrome Driver
├── selenium_module.py                # 低層頁面操作（alias: mod）
└── module/update_my_chromedriver.py  # ChromeDriver 自動更新（CustomDriver 內部使用）
```

> `ems_test_module.py`（IES 版）雖有 import，但本專案測試函式全部透過 `emss`（OLT1408 版）呼叫，`ems` 在 EXE.py 中未被使用。

---

## 3. 執行配置與多執行緒

### 3.1 環境檔格式

與 IES 專案共用相同 JSON 結構，OLT140x 新增 `OLT140x` 卡片資訊欄位：

```json
{
  "ZYXEL_DUT": {
    "NODE1": {
      "url": "http://192.168.1.207/",
      "login_username": "admin",
      "login_password": "1234",
      "default_username": "admin",
      "default_password": "1234",
      "CARDINFO": {
        "MSC":      { "slot_id": "1", "port_id": "1" },
        "GLC1440X": { "slot_id": "3", "port_id": "1" },
        "OLT140x":  { "port_id": "1", "eth_port_id": "5" }
      },
      "ONTINFO": {
        "XPON": {
          "ONT1": { "slot_id": "...", "port_id": "...", "ont_id": "...", ... }
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

**OLT140x 特有欄位說明：**

| 欄位 | 說明 |
|------|------|
| `OLT140x.port_id` | PON 埠號（EMS 頁面顯示為 `PON {port_id}`） |
| `OLT140x.eth_port_id` | 上行 ETH 埠的原始編號，需依機型換算為 ETH 相對編號（見第 5 節） |

### 3.2 CLI 啟動語法

```bash
# 單台設備（預設 207）
python EXE.py

# 指定單台
python EXE.py 84

# 同時對多台設備平行執行（上限 4 個 worker）
python EXE.py 207 84 85
```

### 3.3 多執行緒機制

```python
max_workers = min(4, len(env_list))   # 上限 4，避免壓垮 EMS Server
with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="ENV") as executor:
    ...
```

與 IES 版相同的 thread-per-env 模式，但 max_workers 上限設為 4（IES 版無上限）。每個 thread 內各自建立 `CustomDriver` 實例，不共用瀏覽器 session。

失敗的 thread 將 traceback 寫入 `Report/error_{env_file}.log`，不中斷其他 thread。

---

## 4. 測試流程詳解

### 4.1 完整流程（單一 env_file）

```
1.  變更螢幕解析度至 1920×1080（Windows API，CDS_UPDATEREGISTRY）
2.  讀取 ENV JSON → 解析 FW/EMS 連線資訊、OLT port 資訊
3.  【Telnet 前置清理】telnet 登入 FW → 執行 "er ru ext" + "y" → 抹除 running config
4.  等待 10 秒（設備重置穩定）
5.  CustomDriver 建立 Chrome session
6.  登入 EMS Web → 讀取 EMS 版本號
7.  登入 FW Web（URL 嵌入憑證方式）→ 讀取機型名稱與韌體版本
8.  設定 FW Web logout timeout 為 255 分鐘（Management > Access Control）
9.  依機型計算 Pon_Name、Eth_Name、Pon_Name_L、Eth_Name_L（見第 5 節）
10. 建立 Output 目錄下的 log 檔，寫入版本資訊表頭
11. 重新登入 EMS → 依序呼叫所有 emss.XXX() 測試函式
12. 關閉 Telnet log 檔案（output_file_f.close()）
13. 記錄總耗時
```

### 4.2 Telnet 前置清理（步驟 3）

OLT140x 沒有 FW Web 的 Config Reset 功能，改以 Telnet 指令抹除設定：

```python
My_List = ['er ru ext', 'y']    # erase running extended, confirm
Telnet_func(url_ip, My_List, output_file, _type=1)
time.sleep(10)
```

`Telnet_func()` 內嵌於 `process_env()` 中（非獨立模組），處理邏輯包含：
- 等待 `User name:` 提示（`_type=1`）或 `login:` 提示（`_type=0`）
- 傳送指令後對 `# ` 或 `-- more --` 兩種提示符做 3 次重試等待
- 所有 Telnet 互動輸出寫入 `temp_erase_log.txt`

### 4.3 FW Web 登入方式

OLT140x FW 使用 URL 嵌入帳密的 Basic Auth 登入，不走表單：

```python
driver.get(f"http://{username}:{password}@{url_ip}")
```

FW 頁面為 frame-based 結構，導覽時需指定 frame 編號：

```python
mod.Switch_Specific_Frame(driver, 3)   # 左側選單 frame
driver.find_element(By.LINK_TEXT, "Basic Setting").click()
mod.Switch_Specific_Frame(driver, 4)   # 子選單 frame
driver.find_element(By.LINK_TEXT, "System Info").click()
mod.Switch_Specific_Frame(driver, 6)   # 內容 frame
```

### 4.4 測試函式呼叫序列

依 OLT140x EMS 頁面結構分為四大群組：

```
emss.Basic_General(...)         # Basic > General
emss.Basic_Switch(...)          # Basic > Switch
emss.Basic_IP(...)              # Basic > IP
emss.Basic_Port(...)            # Basic > Port（含 Pon/Eth 埠名稱）

emss.IP_Static(...)             # IP > Static Route
emss.IP_DHCP(...)               # IP > DHCP

emss.Advanced_VLAN(...)         # Advanced > VLAN
emss.Advanced_Static(...)       # Advanced > Static MAC
emss.Advanced_Filtering(...)    # Advanced > Filtering
emss.Advanced_Broadcast(...)    # Advanced > Broadcast Storm
emss.Advanced_Link(...)         # Advanced > Link Aggregation
emss.Advanced_Port(...)         # Advanced > Port
emss.Advanced_Classifier(...)   # Advanced > Classifier
emss.Advanced_Policy(...)       # Advanced > Policy
emss.Advanced_Queqe(...)        # Advanced > Queue（含 Pon/Eth 埠名稱）
emss.Advanced_VLANStacking(...) # Advanced > VLAN Stacking
emss.Advanced_Multicast(...)    # Advanced > Multicast
emss.Advanced_IP(...)           # Advanced > IP Source Guard
emss.Advanced_Loop(...)         # Advanced > Loop Guard
emss.Advanced_PPPoE(...)        # Advanced > PPPoE IA

emss.GPON_OLT(...)              # GPON > OLT
emss.Configure_Save(...)        # Configure Save（儲存設定）
```

> 帶有 `Pon_Name`、`Eth_Name`、`OLT_Port`、`OLT_Eth_Port` 參數的函式，是需要指定特定埠進行設定的測試。

---

## 5. OLT140x 機型差異處理

OLT140x 有多個子型號，ETH 上行埠的**相對編號**計算方式依 PON 埠數不同而異：

```python
if model_name == "OLT1404A-IA":    # 4 PON 埠
    a = int(OLT_Eth_Port) - 4
elif model_name == "OLT1404B-IA":
    a = int(OLT_Eth_Port) - 4
elif model_name == "OLT1408A-IA":  # 8 PON 埠
    a = int(OLT_Eth_Port) - 8
elif model_name == "OLT1408B-IA":
    a = int(OLT_Eth_Port) - 8
elif model_name == "OLT1408A-C":
    a = int(OLT_Eth_Port) - 8
```

換算後產生四個埠名稱變數，傳入需要指定埠的測試函式：

| 變數 | 格式 | 範例（port_id=1, eth_port_id=9, OLT1408A-IA） |
|------|------|----------------------------------------------|
| `Pon_Name` | `"PON {port_id}"` | `"PON 1"` |
| `Pon_Name_L` | `"pon-{port_id}"` | `"pon-1"` |
| `Eth_Name` | `"ETH {a}"` | `"ETH 1"`（9-8=1） |
| `Eth_Name_L` | `"eth-{a}"` | `"eth-1"` |

> `OLT_Eth_Port` 是從 ENV JSON 的 `OLT140x.eth_port_id` 取得的原始硬體埠號，EMS 顯示的是相對於 PON 埠數的偏移值。

---

## 6. 報表輸出

### 6.1 Log 檔命名規則

```
Output\Web_EMS_{model_name}_{EMS_version}_{日期時分}_{IP後3碼}.txt
```

範例：`Output\Web_EMS_OLT1408A-IA_V5.30_2026-05-06 1012_207.txt`

與 IES 版的差異：
- 輸出目錄為 `Output/`（IES 版為 `Report/`）
- 機型名稱取自 FW Web System Info 頁面（IES 版取 driver.title）
- 副檔名為 `.txt`

### 6.2 Log 表頭格式

```
Web Auto Report
{datetime}
EMS Web url: {ems_url}
EMS Web Version: {emsversion}
FW Web IP: {url}
FW Web model: {model_name}
FW Web version: {model_version}
EMS - Configuration for OLT140x Test Start
...
Total time: 0 hr 35 min 42 sec
```

### 6.3 Telnet 操作 Log

Telnet 前置清理的互動記錄另存為：

```
temp_erase_log.txt   （固定路徑，每次執行覆蓋）
```

> 注意：多 thread 執行時，多個 thread 同時寫入同一個 `temp_erase_log.txt` 會互相覆蓋，這是已知問題。

---

## 附錄：環境準備清單

| 項目 | 說明 |
|------|------|
| `ENV/ENV_WEB_{id}.json` | 每台 OLT 一份，注意 `OLT140x.port_id` 與 `eth_port_id` 的填寫 |
| `Output/` 資料夾 | 需預先手動建立（EXE.py 未自動建立，不同於 IES 版） |
| FW Telnet 可達 | 測試前置步驟會 telnet 到 FW，確保 Telnet 服務開啟 |
| Chrome 與 ChromeDriver | 版本不符時 CustomDriver 自動更新 |
| 螢幕解析度 | 啟動時自動切換為 1920×1080（永久寫入 registry） |

## 附錄：常見維護操作

| 情境 | 操作 |
|------|------|
| 新增受測 OLT140x | 複製任一 `ENV/ENV_WEB_*.json`，修改 IP / 帳密 / OLT140x port 資訊 |
| 新增機型（OLT140xC-xx 等） | 在 `process_env()` 的機型判斷 if-elif 區塊新增對應計算邏輯 |
| 跳過特定測試 | 在 EXE.py 的函式呼叫序列中 comment 掉對應行 |
| 查看失敗的測試 | 搜尋 `Output/*.txt` 中的 `failed after` 或查看 `Report/*.png` 截圖 |
| 多台同時測試（上限 4） | `python EXE.py 207 84 85 86` |
