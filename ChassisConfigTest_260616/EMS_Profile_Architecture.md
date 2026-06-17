# EMS Profile 自動化測試框架 — 架構交接文件

> 適用版本：Run_EMS_Profiles_1.py（單機版）  
> 最後更新：2026-05-05

---

## 目錄

1. [核心架構與設計模式](#1-核心架構與設計模式)
2. [執行配置](#2-執行配置)
3. [Profile 測試清單與容量管理](#3-profile-測試清單與容量管理)
4. [容錯機制](#4-容錯機制)
5. [報表輸出](#5-報表輸出)

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
Run_EMS_Profiles_1.py
├── module/variable_module.py          # 環境變數載入（from ... import *）
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

### 2.2 啟動語法

```bash
python Run_EMS_Profiles_1.py
```

無 CLI 參數，固定讀取 `ENV/ENV_WEB.json`。

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

### 4.4 CustomDriver 雙層容錯

與 Config 測試相同：
- `CustomDriver.find_element()` / `find_elements()` 內建 3 次重試 + renderer recovery。
- `CustomDriver.__init__` 失敗時自動觸發 `update_my_chromedriver` 下載對應版本。

---

## 5. 報表輸出

### 5.1 Log 檔命名規則

```
Report\Web_EMS_Profiles_{EMS_version}_{日期時分}.txt
```

範例：`Report\Web_EMS_Profiles_V5.30_2026-05-05 1423.txt`

與 Config 測試的差異：
- 不包含 FW title 或 IP 後綴（Profile 測試不綁定特定 FW）。
- 副檔名為 `.txt`（Config 測試為 `.log`）。

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

## 附錄：Profile 測試前置條件清單

| 項目 | 說明 |
|------|------|
| `ENV/ENV_WEB.json` | 確認 EMS url / 帳密填寫正確 |
| EMS 連線可達 | Profile 測試不需要 FW 連線 |
| `Report/` 資料夾 | 不存在時腳本自動建立 |
| Chrome 與 ChromeDriver | 版本不符時自動更新 |
| 螢幕解析度 | 腳本啟動時自動設定為 1920×1080（Windows 環境） |

## 附錄：常見維護操作

| 情境 | 操作 |
|------|------|
| 切換受測 EMS | 修改 `ENV/ENV_WEB.json` 的 `EMS.url` / 帳密 |
| 只跑特定 profile | 在 `Run_EMS_Profiles_1.py` 末段 comment 掉不需要的呼叫 |
| 新增 Profile 類型 | 在 `ems_test_module.py` 新增 `@retry()` 函式，在 Run 腳本末段加入呼叫 |
| 查看哪個 profile 失敗 | 搜尋 log 中的 `failed after 2 attempts` 或查看 `Report/*.png` 截圖 |
