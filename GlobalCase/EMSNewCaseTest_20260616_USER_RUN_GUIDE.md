# EMSNewCaseTest_20260616 使用者執行指南

這份文件給需要手動執行 `EMSNewCaseTest_20260616` 自動化 case 的使用者參考。

## 1. 進入專案資料夾

請用 PowerShell 進入新 case 專案：

```powershell
cd D:\Auto\EMS\Agent\EMSWebTest\EMSNewCaseTest_20260616
```

## 2. 執行前確認環境參數

測試使用的 EMS URL、帳號密碼、設備 IP、ONT SN/PW、card/port 資訊都在：

```text
D:\Auto\EMS\Agent\EMSWebTest\EMSNewCaseTest_20260616\environment_parameter.json
```

執行前請確認這些欄位正確：

- `EMS.url`：EMS Web 登入 URL
- `EMS.ip`：EMS server IP
- `EMS.version`：目前測試的 EMS 版本
- `EMS.login_username` / `EMS.login_password`：EMS Web 帳號密碼
- `EMS.executeNode`：預設要執行的設備清單
- `ZYXEL_DUT`：設備資料，key 通常是設備 IP，例如 `192.168.168.85`
- `ZYXEL_DUT.<device>.CARDINFO`：card、slot、port 資訊
- `ZYXEL_DUT.<device>.ONT`：provision 測試用 ONT 資訊

目前 `--cmdopt` 要填 `environment_parameter.json` 裡 `ZYXEL_DUT` 的 key。  
例如目前設備 key 是 `192.168.168.85`。

## 3. 第一次執行前安裝套件

如果這台電腦尚未安裝必要 Python 套件，請先執行：

```powershell
pip install -r requirements.txt
```

如果已經可以正常執行 pytest，這一步可以略過。

## 4. 執行所有新專案 case

執行 `EMSNewCaseTest_20260616` 裡全部 case：

```powershell
pytest tests -v -s --cmdopt=192.168.168.85
```

## 5. 執行單一 case

建議用檔名執行單一 case。

### EMS1-6262 ontServiceSelectBySearch

```powershell
pytest tests\test_ems1_6262_ont_service_select_by_search.py -v -s --cmdopt=192.168.168.85
```

### EMS1-6207 ontServiceSelectBySearchRegistered

```powershell
pytest tests\test_ems1_6207_ont_service_select_by_search_registered.py -v -s --cmdopt=192.168.168.85
```

### EMS1-7212 ipNameServer

```powershell
pytest tests\test_ems1_7212_ip_name_server.py -v -s --cmdopt=192.168.168.85
```

### EMS1-4538 portSpeedSelection

```powershell
pytest tests\test_ems1_4538_port_speed_selection.py -v -s --cmdopt=192.168.168.85
```

### EMS1-7214 deviceStatusDown

```powershell
pytest tests\test_ems1_7214_device_status_down.py -v -s --cmdopt=192.168.168.85
```

### EMS1-4515 peformanceCurrentCreate

```powershell
pytest tests\test_ems1_4515_performance_current_create.py -v -s --cmdopt=192.168.168.85
```

### EMS1-6309 peformanceCurrentInterface

```powershell
pytest tests\test_ems1_6309_performance_current_interface.py -v -s --cmdopt=192.168.168.85
```

### EMS1-7215 ontServiceEditVlan

```powershell
pytest tests\test_ems1_7215_ont_service_edit_vlan.py -v -s --cmdopt=192.168.168.85
```

## 6. 執行環境檢查 case

用來確認 `environment_parameter.json` 是否能正確載入：

```powershell
pytest tests\test_environment.py -v -s --cmdopt=192.168.168.85
```

## 7. 使用 RUN.py 互動式執行

也可以使用新專案內的 `RUN.py` 執行。

```powershell
python RUN.py
```

執行後會詢問：

```text
Nodes [192.168.168.85]:
Pytest target [tests]:
Reruns [0]:
```

範例 1：直接按 Enter 執行預設 node 的全部 tests。

範例 2：只執行 EMS1-7212：

```text
Nodes [192.168.168.85]: 192.168.168.85
Pytest target [tests]: tests\test_ems1_7212_ip_name_server.py
Reruns [0]: 0
```

範例 3：失敗時自動重跑 1 次：

```text
Nodes [192.168.168.85]: 192.168.168.85
Pytest target [tests]: tests\test_ems1_4538_port_speed_selection.py
Reruns [0]: 1
```

## 8. 產生 pytest HTML 報告

如果需要 pytest HTML 報告，可以加上 `--html`：

```powershell
pytest tests\test_ems1_7212_ip_name_server.py -v -s --cmdopt=192.168.168.85 --html=reports\EMS1-7212.html --self-contained-html
```

注意：這是 pytest HTML 報告。  
如果使用者要求「產出報告」，應另外產生專案指定的 EMS txt 報告格式。

## 9. 常用 pytest 參數

- `-v`：顯示詳細測試名稱
- `-s`：顯示程式中的 `print()` 輸出
- `--cmdopt=<device key>`：指定要測試的設備
- `--env-file=<json path>`：指定其他環境參數檔
- `--reruns=1`：失敗時自動重跑 1 次
- `--tb=short`：失敗時顯示較短 traceback

範例：

```powershell
pytest tests\test_ems1_6262_ont_service_select_by_search.py -v -s --tb=short --cmdopt=192.168.168.85
```

## 10. 注意事項

- 執行 Selenium case 時會開啟 Chrome 視窗，測試期間不要手動操作該測試視窗。
- `EMS1-7214 deviceStatusDown` 會透過 console/設備指令讓設備狀態 Down/Up，執行前請確認設備可以被測試影響。
- `EMS1-7215 ontServiceEditVlan` 只支援 NeoX 設備的 `xont`。
- `EMS1-7212 ipNameServer` 只針對 NeoX 設備。
- Performance 相關 case 會建立與關閉 Performance/Current 圖表，執行前請確認 EMS probes 數量足夠。
- 如果測試中斷後留下 pytest、python 或 chromedriver 程序，下一次執行前應先確認並清掉本次測試殘留程序。

## 11. Case 文件位置

每個 case 的測試流程文件放在：

```text
D:\Auto\EMS\Agent\EMSWebTest\EMSNewCaseTest_20260616\docs
```

目前新專案 case list：

```text
D:\Auto\EMS\Agent\EMSWebTest\EMSNewCaseTest_20260616\Web_EMS_NewCase.list
```
