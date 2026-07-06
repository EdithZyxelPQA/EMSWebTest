# EMSWebTest Project Memory

這份檔案用來保存使用者要求 Codex 記住的專案規則與工作習慣。之後在這個大專案內工作時，應先參考這份檔案。

## 專案結構

- 大專案路徑：`D:\Auto\EMS\Agent\EMSWebTest`
- 舊有三個專案只做基本維護：
  - `Olt140xConfigTest_20260616`
  - `GlobalTest_20260616`
  - `ChassisConfigTest_260616`
- 新增自動化 case 必須放在新專案：
  - `EMSNewCaseTest_20260616`
- 新專案資料夾必須和 `GlobalTest_20260616` 平行。
- 未來新的測試程式要獨立在 `EMSNewCaseTest_20260616`，不要加到舊資料夾。
- 舊資料夾內容必須保持獨立，只有使用者明確要求些微改動時才能動。
- 新專案需要參考舊資料夾內容時，直接複製一份到新專案，不共用舊檔案。

## 新增 Case 規則

- 每次新增新的自動化 test case 後，都要更新新專案內的 case list 檔案。
- 新專案已有 case list：
  - `EMSNewCaseTest_20260616\Web_EMS_NewCase.list`
- 新 case 以 pytest 架構撰寫，參考 `GlobalTest_20260616` 的結構與寫法：
  - `Unicase.py`
  - `conftest.py`
  - `environment_parameter.json`

## 測試執行原則

- 使用者要求執行 `GlobalTest_20260616` 裡的 `Restful.py`、`Unicase.py`、`Provision.py`、`Icat.py` 時，可以參考 `RUN.py` 的執行方式。
- 如果使用者說測試失敗的 case 要再跑一次，最多依使用者指示重跑失敗 case。
- 執行 Selenium 測試時，測試完應關閉測試開啟的瀏覽器，避免一直開新視窗造成錯亂。
- 若測試 fail，除非使用者特別要求畫面停住，否則程式要繼續往下跑，不要停住。
- 使用者要求停止測試時，要停止本次 pytest/python/chromedriver，不要任意停止使用者其他 Chrome。

## 前端操作原則

- 測試動作一定要從前端模擬使用者操作。
- 絕對不可以用後端處理任何測試動作。
- 關閉 Performance 圖表也必須從前端點圖表 X，不可用後端刪除資料。
- Performance 圖表關閉相關記憶：
  - 可先用 `//*[contains(@id,'pm_')]` 或更精準的 `//*[starts-with(@id,'pm_')]` 計算圖表數量。
  - 關閉時要點圖表內的 `class="icon exitBlock"`。
  - 要考慮滾軸以下的圖表，必要時先滾到底讓所有圖表載入後再計數。
  - 全部 create 完圖表後，再一起 refresh、等待至少 30 秒，再檢查 canvas 資料。
  - canvas 檢查要像人眼一樣確認有點和線，也要確認裡面有數值。

## EMS 與設備參數

- EMS URL 可能會變，應寫在 `environment_parameter.json`，不要寫死在 case 裡。
- 若使用者說「現在執行測試某版本的 xxx.py」，要一併更新 `environment_parameter.json` 裡的 `"version"`。
- 曾使用過的 EMS URL/IP：
  - `https://192.168.128.100:9116/netatlasems/index`
  - `https://192.168.128.50:9116/netatlasems/index`
- 預設測試設備曾指定：
  - `192.168.168.85`
- 常用帳號密碼：
  - EMS：admin / `Pqa1234!!`
  - 設備：admin / `Pqa1234!!`

## 報告格式

- 使用者說「產出報告」時，要產生類似舊報告格式的 txt。
- 報告檔名格式範例：
  - `EMS_Restful_03.00.11(AAVV.221)b2_NeoX-06_NXC400_2026-05-22_23-40-16.txt`
  - `EMS_Unicase_03.00.11(AAVV.221)b5_NeoX-06_NXC400_2026-06-16_11-44-52.txt`
- 報告內容格式範例：

```text
EMS_Unicase Report
2026-06-16_11-44-52
EMS URL   : https://192.168.128.100:9116/netatlasems/index
EMS Ver   : 03.00.11(AAVV.221)b5

Device Type : NeoX-06
Device Info :
NXC400 : V1.02(ACKG.1)
NXP316 : V1.02(ACKI.1)
NXA340 : V1.02(ACQE.1)

==================================================

[EMS1-6267][serviceExport] Result failed
[EMS1-6268][serviceExport] Result failed
```

- 使用者也需要簡短結果時，可以提供：
  - `EMS1-6262 ontServiceSelectBySearch: PASSED`
  - `EMS1-6207 ontServiceSelectBySearchRegistered: PASSED`

## GitHub

- GitHub repository：
  - `https://github.com/EdithZyxelPQA/EMSWebTest.git`
- 使用者已設定：
  - `git config --global --add safe.directory D:/Auto/EMS/Agent/EMSWebTest`
  - `git push -u origin main`
- 未來使用者叫 Codex 上傳 GitHub 時，直接幫忙 push。
- 如果 git push 回傳需要使用者認證，就回覆請使用者認證。

## 文件來源

- `NetAtlasEMS_UserGuide.pdf` 是 EMS 網管軟體操作手冊。
- `TestPlan_NetAtlasEMS-20260615.xlsx` 是 EMS 所有測試 case，但不是全部都已自動化。
- 長期目標是將所有 case 都自動化。
