# GlobalTest_20260616 使用者執行指南

這份文件給需要手動執行 `GlobalTest_20260616` 舊有自動化 case 的使用者參考。

`GlobalTest_20260616` 是既有舊專案，未來只做基本維護。新的自動化 case 請新增到：

```text
D:\Auto\EMS\Agent\EMSWebTest\EMSNewCaseTest_20260616
```

## 1. 進入專案資料夾

請用 PowerShell 進入 GlobalTest 專案：

```powershell
cd D:\Auto\EMS\Agent\EMSWebTest\GlobalTest_20260616
```

## 2. 執行前確認環境參數

GlobalTest 會讀取此檔案：

```text
D:\Auto\EMS\Agent\EMSWebTest\GlobalTest_20260616\environment_parameter.json
```

執行前請確認這些欄位正確：

- `EMS.url`：EMS Web 登入 URL
- `EMS.ip`：EMS server SSH IP
- `EMS.version`：目前測試的 EMS 版本
- `EMS.login_username` / `EMS.login_password`：EMS Web 帳號密碼
- `EMS.executeNode`：預設要執行的設備清單
- `ZYXEL_DUT`：設備資料，key 通常是設備 IP，例如 `192.168.168.85`
- `ZYXEL_DUT.<device>.CARDINFO`：card、slot、port 資訊
- `ZYXEL_DUT.<device>.ONT`：ONT 測試資料
- `ZYXEL_DUT.<device>.GE`：GE port 測試資料

注意：如果使用者指定「現在測試某版本」，請先把 `EMS.version` 改成該版本，報告檔名與內容會使用這個版本字串。

## 3. 第一次執行前安裝套件

如果這台電腦尚未安裝必要 Python 套件，請先執行：

```powershell
pip install -r requirements.txt
```

如果 `pytest` 指令無法辨識，可以改用：

```powershell
python -m pytest
```

## 4. 建議執行方式：使用 RUN.py

GlobalTest 建議使用 `RUN.py` 執行，因為它會：

- 讀取 `environment_parameter.json` 的 `EMS.executeNode`
- 詢問要執行哪些 node
- 詢問要執行哪個 pytest target
- 詢問失敗 rerun 次數
- 詢問平行或逐台設備執行
- 自動產生 pytest HTML 報告到 `report\report_<node>.html`
- 透過 `conftest.py` 產生 EMS txt 報告

執行：

```powershell
python RUN.py
```

RUN.py 會互動式詢問：

```text
Nodes:
Pytest target:
Reruns:
Mode:
```

如果直接按 Enter，RUN.py 會使用預設值。預設 pytest target 是：

```text
Icat.py::TestIcat::test_EMS1_5489_deviceStatus
```

## 5. RUN.py 執行範例

### 執行 Unicase.py 全部 case

```text
Nodes: 192.168.168.85
Pytest target: Unicase.py
Reruns: 1
Mode: 2
```

### 執行 Restful.py 全部 case

```text
Nodes: 192.168.168.85
Pytest target: Restful.py
Reruns: 1
Mode: 2
```

### 執行 Provision.py 全部 case

```text
Nodes: 192.168.168.85
Pytest target: Provision.py
Reruns: 1
Mode: 2
```

### 執行 Icat.py 全部 case

```text
Nodes: 192.168.168.85
Pytest target: Icat.py
Reruns: 1
Mode: 2
```

### 執行單一 case

pytest target 可以指定到 class/method，例如：

```text
Nodes: 192.168.168.85
Pytest target: Icat.py::TestIcat::test_EMS1_5489_deviceStatus
Reruns: 1
Mode: 2
```

`Mode` 建議選 `2` 逐台執行，畫面與報告比較不容易混在一起。  
只有在很確定多台設備可以同時測試時，才使用 `1` 平行執行。

## 6. 直接使用 pytest 執行

也可以不用 `RUN.py`，直接用 pytest。

### 執行單一檔案

```powershell
pytest Unicase.py -vv -s --cmdopt=192.168.168.85
```

```powershell
pytest Restful.py -vv -s --cmdopt=192.168.168.85
```

```powershell
pytest Provision.py -vv -s --cmdopt=192.168.168.85
```

```powershell
pytest Icat.py -vv -s --cmdopt=192.168.168.85
```

### 執行單一測試方法

```powershell
pytest Icat.py::TestIcat::test_EMS1_5489_deviceStatus -vv -s --cmdopt=192.168.168.85
```

### 失敗自動 rerun

```powershell
pytest Provision.py -vv -s --cmdopt=192.168.168.85 --reruns=1
```

### 產生 pytest HTML 報告

```powershell
pytest Restful.py -vv -s --cmdopt=192.168.168.85 --html=report\report_192.168.168.85.html --capture=sys
```

## 7. 常用 pytest target

GlobalTest 常用測試檔：

- `Unicase.py`
- `Restful.py`
- `Provision.py`
- `Icat.py`

其他既有測試檔包含：

- `Configuration.py`
- `commonPrf.py`
- `e2e.py`
- `maxPm.py`
- `maxPrf.py`
- `maxUsr.py`
- `prfApply.py`
- `sessionTest.py`

## 8. Case list 檔案

GlobalTest 目前有下列 list 檔案可查 case id 與 case name：

```text
Web_EMS_Unicase.list
Web_EMS_Restful.list
Web_EMS_Provision.list
Web_EMS_ICAT.list
Web_EMS_Profile.list
```

例如：

```powershell
Get-Content Web_EMS_Unicase.list
```

```powershell
Get-Content Web_EMS_Restful.list
```

## 9. 報告位置與格式

GlobalTest 的 `conftest.py` 會在 pytest 執行時自動產生 EMS txt 報告到：

```text
D:\Auto\EMS\Agent\EMSWebTest\GlobalTest_20260616\report
```

檔名格式類似：

```text
EMS_Unicase_03.00.11(AAVV.221)b5_NeoX-06_NXC400_2026-06-16_11-44-52.txt
EMS_Restful_03.00.11(AAVV.221)b2_NeoX-06_NXC400_2026-05-22_23-40-16.txt
```

報告內容格式類似：

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

如果用 `RUN.py` 執行，也會另外產生 pytest HTML 報告：

```text
D:\Auto\EMS\Agent\EMSWebTest\GlobalTest_20260616\report\report_<node>.html
```

## 10. 常用參數說明

- `-vv`：顯示更詳細的測試名稱
- `-s`：顯示測試中的 print output
- `--cmdopt=<device key>`：指定要測試的設備，必須存在於 `environment_parameter.json` 的 `ZYXEL_DUT`
- `--reruns=1`：失敗時自動重跑 1 次
- `--html=<path>`：產生 pytest HTML 報告
- `--capture=sys`：讓 pytest HTML 報告保留輸出內容
- `--tb=short`：失敗時顯示較短 traceback

## 11. 執行注意事項

- 執行 Selenium case 時會開啟 Chrome 視窗，測試期間不要手動操作該測試視窗。
- 測試完成後應確認測試開啟的 Chrome / chromedriver / pytest / python 沒有殘留。
- 如果測試中途停止，下次執行前建議先確認沒有殘留程序。
- 舊專案內容只做基本維護，不要在這個資料夾新增新 case。
- 如果需要新增新自動化 case，請加到 `EMSNewCaseTest_20260616`。
- 如果需要參考舊專案內容，請複製一份到新專案，不要讓新舊專案共用檔案。
