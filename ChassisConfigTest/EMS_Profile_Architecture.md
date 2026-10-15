# EMS Profile 自動化測試框架 — 架構交接文件

> 適用版本：Run_EMS_Profiles_1.py（單機版，可用 `--ems` 同時跑多台 EMS）、Run_EMS_Profiles_Retest.py  
> 最後更新：2026-10-07（新增 `--ems`、頁面就緒等待、重跑工具，見 2.2 / 4.4 / 6）

---

## 目錄

1. [核心架構與設計模式](#1-核心架構與設計模式)
2. [執行配置](#2-執行配置)
3. [Profile 測試清單與容量管理](#3-profile-測試清單與容量管理)
4. [容錯機制](#4-容錯機制)
5. [報表輸出](#5-報表輸出)
6. [重跑失敗 / 無結果的項目](#6-重跑失敗--無結果的項目)

---

## 1. 核心架構與設計模式

### 1.1 架構概覽

Profile 測試與 Config 測試共用相同的三層架構，差異在於執行層為**單執行緒腳本**，且只測試 EMS 端的 Provision > Profile 功能，**不涉及 FW Web 設定驗證**。

```
┌────────────────────────────────────────────────────────────┐
│  流程執行層  Run_EMS_Profiles_1.py                          │
│  · 從 variable_module 匯入所有環境變數                       │
│  · 固定單機、單 thread 執行                                  │
│  · 腳本頂層直接依序呼叫所有 profile 測試函式                  │
└───────────────────────────┬────────────────────────────────┘
                             │  呼叫 ems.XXX(driver, ems_url, ...)
┌───────────────────────────▼────────────────────────────────┐
│  腳本層  module/ems_test_module.py                          │
│  · ONT_*Profile、Rate_Limit_Profile、Shaping_Profile 等     │
│  · EMS_delete_profiles、Create_zzz_profile_for_Sort_test   │
└───────────────────────────┬────────────────────────────────┘
                             │  呼叫 e_pro.*, mod.*
┌───────────────────────────▼────────────────────────────────┐
│  頁面操作層  ems_profile_module.py + ems_module.py          │
│  · Profile_Path、New_Profile、Delete_Profile、              │
│    Profile_Name、If_Profile_Table_Full 等 UI helpers        │
└────────────────────────────────────────────────────────────┘
```

### 1.2 與 Config 測試的主要差異

| 項目 | Run_EMS_Config_all.py | Run_EMS_Profiles_1.py |
|------|----------------------|----------------------|
| 執行模式 | 多執行緒（每台設備一個 thread） | 單執行緒 |
| 環境讀取 | 各 thread 內直接解析 CLI 指定的 JSON | `from module.variable_module import *`（固定 `ENV/ENV_WEB.json`） |
| 驗證範圍 | EMS Set → EMS Check → **FW Check** | EMS Set → **EMS Check**（無 FW Check） |
| 測試目標 | EMS 各頁面功能＋卡片相關設定 | EMS > Provision > Profile 各類型 |
| 啟動前置 | 無 | Windows API 強制切換螢幕解析度至 1920×1080 |
| 測試前清理 | Config Reset（FW 恢復出廠） | `EMS_delete_profiles()`（刪除指定的 auto-test profiles） |

### 1.3 模組依賴樹

```
Run_EMS_Profiles_1.py                  # 完整測試（17 組 profile、119 個 case）
Run_EMS_Profiles_Retest.py             # 只重跑指定的測試函式（見第 6 節）
├── module/variable_module.py          # 環境變數載入（from ... import *）；處理 --ems
├── module/ems_test_module.py          # 所有 Profile 測試函式定義處
│   ├── module/ems_profile_module.py   # Profile 頁面 UI helper（Profile_Path 等）
│   ├── module/ems_module.py           # EMS 通用頁面操作
│   └── module/selenium_module.py     # 低層瀏覽器操作（Login_EMS, Page_Switch...）
├── module/ems_module.py               # （Run 腳本也直接 import，alias: e_mod）
├── module/customdriver.py             # 加強版 Chrome Driver
├── module/globals.py                  # 全域狀態（msc_card_type）
└── module/get_card.py                 # （import 但 Profile 測試中已全部 comment out）
```

### 1.4 典型 Profile 測試流程

```
1.  變更螢幕解析度至 1920×1080（Windows API，確保 EMS 頁面元素不被截切）
2.  from module.variable_module import * → 載入 ENV/ENV_WEB.json 所有變數
3.  CustomDriver 建立 Chrome session
4.  driver.get(ems_url) → 登入 EMS Web
5.  讀取 EMS 版本號 → 組合 file_name（Report 目錄）
6.  EMS_delete_profiles() → 刪除上次測試殘留的 auto-test profiles（確保乾淨起點）
7.  Create_zzz_profile_for_Sort_test() → 建立 "zzz" 前綴 profile 測試排序功能
8.  依序執行各 Profile 測試函式（每個函式皆自帶 @retry 裝飾器）
9. driver.quit() → 結束
```


---

## 2. 執行配置

### 2.1 環境變數來源

Profile 測試透過 `from module.variable_module import *` 一次匯入所有設定，固定讀取：

```
ENV/ENV_WEB.json   （非 ENV_WEB_{id}.json，無 CLI 參數）
```

`variable_module.py` 解析的主要欄位與 Config 測試相同（詳見 EMS_Config_Architecture.md 2.1 節），並將所有變數匯出至全域命名空間，腳本可直接使用 `url`, `username`, `ems_url`, `ems_password` 等變數。

> 若需切換受測設備，直接修改 `ENV/ENV_WEB.json` 或將目標 `ENV_WEB_{id}.json` 複製為 `ENV_WEB.json`。  
> 只換 EMS 時，用 `--ems <IP>` 即可（見 2.2），不必改檔。`ENV/ENV_WEB_EMS_128_8.json` 是 EMS 指向 128.8 的版本。

`variable_module.py` 另外匯出：

| 變數 | 說明 |
|------|------|
| `ems_ip` | 本次執行的 EMS IP（取自 `ems_url`） |
| `ems_tag` | EMS IP 最後兩段，例如 `EMS128_8`，用在報告檔名 |
| `ems_cli_ip` | 命令列 `--ems` 給的 IP；沒給為 `None` |

### 2.2 啟動語法

```bash
python Run_EMS_Profiles_1.py                          # EMS 取自 ENV/ENV_WEB.json
python Run_EMS_Profiles_1.py --ems 192.168.128.8      # 本次改測 128.8（也可寫 --ems=192.168.128.8）
```

- `--ems <IP>` 只換掉 `EMS.url` 的主機部分與 `EMS.ip`，port / 路徑沿用 `ENV_WEB.json`（→ `https://<IP>:9116/netatlasems/`）。
- EMS 帳號密碼仍取自 `ENV_WEB.json`；另一台 EMS 的 admin 密碼不同時要改檔。
- 必須在 `ChassisConfigTest` 目錄下執行（`ENV/`、`Report/` 為相對路徑）。
- 本機要用 `C:\Users\ZT02452\AppData\Local\Programs\Python\Python311\python.exe`（有 selenium 等套件）。該資料夾內有舊版 chromedriver.exe，跑之前先把它從 PATH 拿掉；CustomDriver 用的是 `drivers/chromedriver.exe`。

**同時跑多台 EMS**：在同一個資料夾開兩個終端機，各自給 `--ems`。報告檔名含 `ems_tag`，不會互相覆蓋；兩台 EMS 的 profile 各自獨立，不會互相影響。

```bash
python Run_EMS_Profiles_1.py --ems 192.168.128.100
python Run_EMS_Profiles_1.py --ems 192.168.128.8
```

注意：本機記憶體約 8 GB，同時開兩個 Chrome 會明顯變慢；失敗截圖是截整個螢幕，可能截到另一台的畫面（不影響結果）。

### 2.3 螢幕解析度前置設定

腳本頂部使用 Windows API（`ctypes.windll.user32.ChangeDisplaySettingsW`）強制切換解析度：

```python
TARGET_WIDTH  = 1920
TARGET_HEIGHT = 1080
change_resolution(TARGET_WIDTH, TARGET_HEIGHT)
```

原因：EMS 部分 Profile 頁面的元素位置或捲動行為受視窗大小影響，固定解析度可確保元素可見性與點擊準確度。

### 2.4 操作節奏控制

與 Config 測試相同，讀取 `ENV/time_sleep_before_find_element.txt`，傳入 `CustomDriver(time_sleep=0)`（Profile 腳本預設值直接寫 `0`，比 Config 測試更快）。

`time_sleep` 是每次找元素前的固定等待；EMS 載入慢時固定等待不夠，另有「頁面就緒等待」（預設開啟），見 4.4。

---

## 3. Profile 測試清單與容量管理


### 3.2 Profile 測試執行順序

`Run_EMS_Profiles_1.py` 依以下順序執行（對應 `ems_test_module.py` 的函式定義）：

| 順序 | 函式名稱 | 說明 |  
|-----|---------|------| 
| 前置 | `EMS_delete_profiles` | 刪除殘留的 auto-test profiles  
| 前置 | `Create_zzz_profile_for_Sort_test` | 建立排序測試用 "zzz" profiles  
| 1 | `ONT_QoS_Bandwidth_Profile` | QoS 頻寬設定 profile  
| 2 | `ONT_Security_Profile` | 安全性設定 profile  
| 3 | `Rate_Limit_Profile` | 速率限制 profile  
| 4 | `Shaping_Profile` | 流量整形 profile  
| 5 | `IGMP_Group_Privilege_Profile` | IGMP 群組權限 profile 
| 6 | `ONT_Service_Profile` | ONT 服務 profile 
| 7 | `ONT_Multicast_Profile` | ONT Multicast profile  
| 8 | `ONT_UNI_Profile` | ONT UNI 設定 profile  
| 9 | `ONT_ONT_Profile` | ONT 裝置 profile  
| 10 | `ONT_VoIP_SIP_Profile` | VoIP SIP profile  
| 11 | `ONT_VoIP_Common_Profile` | VoIP 公用設定 profile 
| 12 | `ONT_VoIP_Dial_Plan_Profile` | VoIP 撥號計畫 profile  
| 13 | `ONT_ACL_Profile` | ACL profile  
| 14 | `ONT_Alarm_Profile` | 告警 profile  
| 15 | `ONT_Template_Profile` | ONT Template（依賴多種 profile 已存在）  
| 16 | `Weight_Profile` | 權重 profile  
| 17 | `GE_Template` | GE Template（依賴其他 profile）  

> **注意：** `ONT_Template_Profile` 與 `GE_Template` 在測試中需要引用其他 profile 作為關聯，因此排在清單後段，須確保前面的 profile 均已建立完成。

### 3.3 Profile 測試函式典型操作模式

每個 Profile 測試函式的內部操作順序：

```
1. driver.get(ems_url) + Login_EMS()          ← 確保 session 有效
2. e_pro.Profile_Path(driver, "Profile Name") ← 導航至指定 profile 頁面
3. Delete_Profile_1() 刪除既有測試 profile    ← 乾淨起點
4. If_Profile_Table_Full() 檢查容量上限        ← 超過上限則 return 跳過
5. e_pro.New_Profile() 點擊 New               ← 建立新 profile
6. 填入各欄位值（輸入名稱、選擇選項等）
7. 儲存並驗證 EMS 畫面顯示是否正確             ← EMS Check
8. （無 FW Check）
```

### 3.4 測試 Profile 命名慣例

| 前綴 | 意義 |
|-----|------|
| `!!!Auto_DoNotDelete_` | 長期保留的基準 profile（EMS_delete_profiles 不會刪除） |
| `!!!Auto_____` | 測試用 profile，由 EMS_delete_profiles 在測試前清除 |
| `!!!AutoTest_DoNotDelete_` | 特定測試保留 profile |
| `______xpon_` | 單次測試使用的工作 profile |
| `zzz_` | Sort 排序測試用，由 Create_zzz_profile_for_Sort_test 建立 |

> `!!!` 前綴讓這些 profile 排列在清單最前方（依名稱排序），便於識別與管理。

---

## 4. 容錯機制

Profile 測試與 Config 測試共用相同的容錯基礎設施，以下為 Profile 情境下的重點說明。

### 4.1 @retry 裝飾器

所有 Profile 測試函式均有 `@retry()`（預設 `max_retries=2, delay=2`），行為與 Config 測試完全相同：

- 失敗自動重試一次，重試前執行 `window.stop()` + `driver.get("about:blank")`。
- 耗盡重試後截圖存至 `Report/{timestamp}_{funcname}_screenshot.png`，`return None` 繼續執行下一個 profile 測試。
- **整組跳過 = 該組 case 沒有結果**（不是 Fail）。log 會出現 `XXX failed after 2 attempts. Skipping...`，該函式還沒印出的 `[EMS1-xxxx] Result` 都不會有。統計結果時要用不重複的 case ID 數（完整一輪為 119），不能只數 `Result Fail`。
- 在外面再包一層 `retry(max_retries=3)(ems.XXX)` 沒有用：內層耗盡後是 `return None` 而非拋例外，外層看不到失敗，不會再試。

### 4.2 容量上限防護

`If_Profile_Table_Full(driver, outp_id, profile_type, file_name)` 在每個測試函式開頭執行：

```python
if If_Profile_Table_Full(driver, 'EMS1-5574', 'ONT Security Profile', file_name):
    return   # 跳過本 profile 測試，不繼續新增
```

EMS 系統對各 profile 類型有數量上限（見 3.1 節），若表格已滿則直接跳過，避免因 DOM 狀態異常導致後續測試失敗。

### 4.3 EMS Session 保活

每個 Profile 測試函式開頭都有：

```python
driver.get(ems_url)
time.sleep(5)
mod.Login_EMS(driver, username, password)
```

確保長時間測試過程中 EMS session 超時後仍能自動重新登入，不依賴外部 session 保活機制。

### 4.4 CustomDriver 容錯

- `CustomDriver.find_element()` / `find_elements()` 內建 3 次重試 + renderer recovery。
- `CustomDriver.__init__` 失敗時自動觸發 `update_my_chromedriver` 下載對應版本（需要 `requests` 套件；Python311 目前沒裝，自動更新會失敗，要手動換 `drivers/chromedriver.exe`，Selenium 快取 `C:\Users\ZT02452\.cache\selenium\chromedriver\win64\` 裡常有現成版本）。

**頁面就緒等待（2026-10-07 加入，預設開啟）**

每次 `find_element` / `find_elements` 前，先：
1. 等 EMS 載入遮罩消失（`loadind_1`、舊版 `configure_loader`），最多 `overlay_timeout` 秒；
2. 再等目標元素出現，最多 `element_timeout`（find_element）/ `elements_timeout`（find_elements）秒。

逾時不報錯，照原本流程繼續（原有的 3 次重試照舊）。等待時直接用 Selenium 原生 `WebDriver.find_elements`，不會遞迴呼叫自己（舊的 `Wait_Block` 在 find_element 內會遞迴，所以當年被註解掉）。

```python
CustomDriver(time_sleep=0, wait_page_ready=True, overlay_timeout=30, element_timeout=5, elements_timeout=3)
CustomDriver(time_sleep=0, wait_page_ready=False)   # 關閉，行為同舊版
```

背景：EMS 192.168.128.100 頁面載入較慢（例如 SIP profile 有 1,731 筆），沒有這個等待時常出現 `element click intercepted ... loadind_1`、`no such element: profile_name`、`stale element`，造成整組被 `@retry` 跳過。代價：用 `find_elements` 確認「元素不存在」的地方，每次最多多等 `elements_timeout` 秒。改動前的版本留在 `module/customdriver.py.bak_20261007`。

---

## 5. 報表輸出

### 5.1 Log 檔命名規則

```
Report\Web_EMS_Profiles_{EMS_version}_{ems_tag}_{日期時分}.txt
Report\Web_EMS_Profiles_Retest_{EMS_version}_{ems_tag}_{日期時分}.txt     # Run_EMS_Profiles_Retest.py
```

範例：`Report\Web_EMS_Profiles_03.00.11 (AAVV.221) b13_EMS128_8_2026-10-07 1600.txt`

- `ems_tag` 為 EMS IP 最後兩段（2026-10-07 起加入，讓多台 EMS 同時跑時檔名不衝突）；之前的報告沒有這段。
- 不包含 FW title（Profile 測試不綁定特定 FW）。
- 副檔名為 `.txt`（Config 測試為 `.log`）。
- 報告檔混有 UTF-8 與 cp950 位元組，用程式處理時以 latin-1 讀寫，避免破壞內容。

### 5.2 Log 結構

```
EMS Web Auto Report
{datetime}
EMS Web IP: {ems_url}   EMS Version: {emsversion}
  (find_element(), find_elements() will wait 0 sec)
========================
EMS Test
Test Start
EMS - Profile Test Start

             In ONT_QoS_Bandwidth_Profile .../ems_test_module.py:22780
  ...（測試輸出）
                                           [TIME 0:1:23]   2026-05-05 14:25:30.123456
             In ONT_Security_Profile .../ems_test_module.py:22154
  ...
EMS - Profile Test End

Profile Test   Total time: 0 hr 45 min 12 sec
[Page]
END   Test   Total time: 0 hr 45 min 12 sec
[Page]
```

### 5.3 時間記錄

每個測試函式由 `@retry` 裝飾器自動在 log 記錄：
- 開始時：函式名稱 + 原始碼位置（行號）
- 結束時：`[TIME H:M:S]` + 絕對時間戳記

腳本結尾另輸出兩行總計時：`Profile Test Total time` 與 `END Test Total time`（兩者數值相同，為設計習慣）。

---

## 6. 重跑失敗 / 無結果的項目

### 6.1 Run_EMS_Profiles_Retest.py

```bash
python Run_EMS_Profiles_Retest.py [--ems <IP>] <函式名稱> [<函式名稱> ...]
```

- 依序執行指定的函式，名稱可為 `ems_test_module` 的測試函式（如 `ONT_Template_Profile`、`GE_Template`、`Create_zzz_profile_for_Sort_test`），或本檔內的輔助函式。
- 不給函式名稱時，執行檔內預設的 `RETEST` 清單。
- 環境變數 `EMS_FIND_WAIT` 設定 `time_sleep`（預設 0）。
- 不會先跑 `EMS_delete_profiles`，需要清理時自己把清理函式排在前面。

本檔內的輔助函式：

| 函式 | 用途 |
|------|------|
| `Cleanup_Multicast_SIP` | 刪除 Multicast（`!!!AutoTest_DoNotDelete_mul_SFU/HGU`、zzz）、IGMP（`!!!AutoTest_DoNotDelete_xxxxxxx`）、SIP（`sip_profile_SFU/HGU`、zzz） |
| `Cleanup_Template_GE_Sec_Alarm_Rate_Shaping` | 刪除 ONT Template / GE Template / Security / Alarm / Rate Limit / Shaping 的測試 profile 與 zzz（Template 先刪，因為它引用其他 profile）；每筆刪除失敗會再試一次 |
| `Sort_Sec_Rate_Shaping` | 重建 Security / Rate Limit / Shaping 的 zzz，再只跑 EMS1-5650 / 5766 / 5777 |

範例：

```bash
python Run_EMS_Profiles_Retest.py --ems 192.168.128.100 Cleanup_Multicast_SIP Create_zzz_profile_for_Sort_test ONT_Multicast_Profile ONT_VoIP_SIP_Profile
```

### 6.2 重跑時要注意的相依

- **先刪相關 profile 再跑**：前一輪中斷時常留下半成品（例如 SFU 存在、HGU 不存在），會讓 New / Profile info / Delete 失敗。
- **Sort case 需要 zzz profile**：清理會刪掉 zzz，之後要先跑 `Create_zzz_profile_for_Sort_test`（或對應頁面自行建立）。這支函式本身也可能因頁面慢而中途失敗，要確認各頁 zzz 有建起來。
- **ONT Template Sort（EMS1-3636）找的是全形 `ＺＺＺ…`**（31 字），由 `Create_zzz_profile_for_Sort_test` 建立，不是半形 zzz。
- **zzz 長度依頁面不同**：VoIP（SIP / Common / Dial Plan）15 字、ACL 24 字、其他頁 30 字。
- **Delete 需要被刪的對象存在**：例如 EMS1-5666 要先有 `sip_profile_SFU/HGU`，EMS1-5626 要先有 Multicast SFU/HGU、EMS1-5740 要先有 3 個 `!!!GE_template_*`。
- **ONT Template / GE Template 前置步驟多**：會先建立約 10 種 profile，頁面慢時最容易在這段中斷。

### 6.3 把重跑結果寫回原報告

- 原報告先留 `_orig.txt` 備份。
- 用 Fail 的 case 區塊（上一個 `Result` 行之後到該 case 的 `Result` 行）換成重跑報告的同一區塊，並加一行 `(retest <時間> ...)` 標註。
- 原報告沒有結果的 case（整組被跳過），以新段落插在 `EMS - Profile Test End` 之前。
- 寫到暫存檔，確認 Pass/Fail 數、檔頭檔尾、case 清單與 `_orig.txt` 一致後才取代。

---

## 附錄：Profile 測試前置條件清單

| 項目 | 說明 |
|------|------|
| `ENV/ENV_WEB.json` | 確認 EMS url / 帳密填寫正確（或執行時用 `--ems` 指定 EMS） |
| EMS 連線可達 | Profile 測試不需要 FW 連線 |
| `Report/` 資料夾 | 不存在時腳本自動建立 |
| Chrome 與 ChromeDriver | 版本不符時自動更新 |
| 螢幕解析度 | 腳本啟動時自動設定為 1920×1080（Windows 環境） |

## 附錄：常見維護操作

| 情境 | 操作 |
|------|------|
| 切換受測 EMS | 執行時加 `--ems <IP>`；帳密不同時修改 `ENV/ENV_WEB.json` 的 `EMS` 區塊 |
| 同時測多台 EMS | 同一資料夾開多個終端機，各自加 `--ems`（見 2.2） |
| 只跑特定 profile | `python Run_EMS_Profiles_Retest.py <函式名稱>...`（見第 6 節） |
| 新增 Profile 類型 | 在 `ems_test_module.py` 新增 `@retry()` 函式，在 Run 腳本末段加入呼叫 |
| 查看哪個 profile 失敗 | 搜尋 log 中的 `failed after 2 attempts`（整組沒結果）與 `Result Fail`，或查看 `Report/*.png` 截圖 |
| 統計結果 | 以不重複的 `[EMS1-xxxx]` 計算（重試會讓同一 case 出現兩次），完整一輪應為 119 個 |
| Chrome 更新後無法啟動 | 錯誤 `This version of ChromeDriver only supports Chrome version N`：換 `drivers/chromedriver.exe` 為對應版本（見 4.4） |
| 關閉頁面就緒等待 | `CustomDriver(time_sleep=0, wait_page_ready=False)` |
