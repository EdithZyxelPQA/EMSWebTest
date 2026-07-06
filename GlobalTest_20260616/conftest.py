import pytest, json, re, os, sys
from datetime import datetime
from types import SimpleNamespace

SESSION_TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def load_env_data():
    with open("environment_parameter.json", encoding='utf-8') as f:
        return json.load(f)


# ====================================================================
# 1. 新增命令列參數：讓外部程式可以透過 --cmdopt 傳入指定的 NODE
# ====================================================================
def pytest_addoption(parser):
    """註冊自訂的參數 --cmdopt"""
    parser.addoption("--cmdopt", action="store", default="NODE2", help="device node name")

# ====================================================================
# 2. 核心：維持你原本一模一樣的配置建立邏輯 
# ====================================================================
def build_config_object(node_name):
    """將你原本 test_config 裡建立 SimpleNamespace 的龐大邏輯打包（內容完全不變）"""
    data = load_env_data()
    exeNode = node_name
    dut_data = data["ZYXEL_DUT"][exeNode]
    
    config = {
        "reportTitle": data["EMS"]["report_title"],
        "waitTime": data["ELEMENT"]["wait_time"],
        "uploadPath": os.path.abspath(data["AUTO_SITE"]["upload_path"]),
        "downloadpath": os.path.abspath(data["AUTO_SITE"]["download_path"]),
        "browser": data["AUTO_SITE"]["browser"],
        "emsIp": data["EMS"]["ip"],
        "emsURL": data["EMS"]["url"],
        "emsVer": data["EMS"]["version"],
        "emsUsr": data["EMS"]["login_username"],
        "emsPwd": data["EMS"]["login_password"],
        "emsSrvUsr": data["EMS"]["server_username"],
        "emsSrvPwd": data["EMS"]["server_password"],
        "emsSuPwd": data["EMS"]["sudo_password"],
        "dbUsr": data["EMS"]["db_username"],
        "dbPwd": data["EMS"]["db_password"],
        "ftpUsr": data["EMS"]["ftp_username"],
        "ftpPwd": data["EMS"]["ftp_password"],
        "emsFirstAlarmList": data["EMS"]["first_alarm_list"],
        "emsClearAlarmList": data["EMS"]["clear_alarm_list"],        
        "node_name": exeNode,
        "dutName": dut_data["name"],
        "dutIp": dut_data["ip"],
        "dutNodeName": f"{dut_data['name']}({dut_data['ip']})",
        "dutDesc": dut_data["description"],
        "dutAdminName": dut_data["login_username"],
        "dutAdminPwd": dut_data["login_password"],
        "dutType": dut_data["type"],
        "dutSet": dut_data["set_community"],
        "dutGet": dut_data["get_community"],
        "dutSnmpVer": dut_data["snmp_ver"],
        "dutSnmp3Auth": dut_data["snmp3_auth"],
        "dutSnmp3Hash": dut_data["snmp3_hash"],
        "dutSnmp3Encrypt": dut_data["snmp3_encrypt"],
        "dutAddr": dut_data["geo_position"],
        "dutSlotCount": dut_data["slot_total"]
    }
    
    dutAllCardID, dutAllCardPortID, cardTypeName, cardPortTypeName, cardPortTypeSpeed, cardFwVersion, fwUploadName, fwUploadFileName = ([] for _ in range(8))
    ies52xxAllCard = ["MSC", "GLC1440X", "GLC1540X", "OLC3416-42A", "OLC3708", "OLC3416B", "OLC3816"]
    neoxAllCard = ["NXC", "NXP316", "NXA340"]
    if "IES" in config["dutType"]:
        target_cards = ies52xxAllCard
        fwUploadName = ["Image(Switch input image)","GLC1440X-55(A)","GLC1540X-55(A)","OLC3416-42(A)","OLC3708-43A","OLC3416B-IA","OLC3816-IA"]
        fwUploadFileName =["MSC","GLC1440X-55","GLC1540X-55","OLC3416-42","OLC3708-43A","OLC3416B-IA","OLC3816-IA"]        
    elif "NeoX" in config["dutType"]:
        target_cards = neoxAllCard
        fwUploadName = ["Image(Switch input image)","NXP316","NXA340"]
        fwUploadFileName =["NXC","NXP316","NXA340"]        
    else:
        target_cards = None
    if target_cards:
        for ind in target_cards:
            card_info = dut_data["CARDINFO"].get(ind)
            if card_info:
                dutAllCardID.append(dut_data["CARDINFO"][ind]["slot_id"])
                dutAllCardPortID.append(dut_data["CARDINFO"][ind]["port_id"])
                cardTypeName.append(dut_data["CARDINFO"][ind]["type"])
                cardPortTypeName.append(dut_data["CARDINFO"][ind]["port_type"])
                cardPortTypeSpeed.append(dut_data["CARDINFO"][ind]["port_speed"])
                cardFwVersion.append(dut_data["CARDINFO"][ind]["fw_version"])
    else:
        dutAllCardID = [dut_data["CARDINFO"]["OLT140x"]["slot_id"], dut_data["CARDINFO"]["OLT140x"]["slot_id"]]
        dutAllCardPortID = [dut_data["CARDINFO"]["OLT140x"]["eth_port_id"], dut_data["CARDINFO"]["OLT140x"]["port_id"]]
        cardTypeName = [dut_data["CARDINFO"]["OLT140x"]["type"]]
        cardPortTypeName = [dut_data["CARDINFO"]["OLT140x"]["eth_port_type"], dut_data["CARDINFO"]["OLT140x"]["port_type"]]
        cardPortTypeSpeed = [dut_data["CARDINFO"]["OLT140x"]["eth_port_speed"], dut_data["CARDINFO"]["OLT140x"]["port_speed"]]
        cardFwVersion = [dut_data["CARDINFO"]["OLT140x"]["fw_version"]]
        fwUploadName = ["Image1"]
        fwUploadFileName = ["Image"]
    config.update({
        "dutAllCardID": dutAllCardID, "dutAllCardPortID": dutAllCardPortID, "cardTypeName": cardTypeName,
        "cardPortTypeName": cardPortTypeName, "cardPortTypeSpeed": cardPortTypeSpeed, "cardFwVersion": cardFwVersion,
        "fwUploadName": fwUploadName, "fwUploadFileName": fwUploadFileName
    })         
    ontCount = dut_data["ONT"]["exe_ontCount"]
    ontSlotIDList, ontPortIDList, ontOntIDList, ontSNList, ontPWList, ontModelList, ontTypeList, ontFlagList = ([] for _ in range(8))
    for index in range(ontCount):
        ontIndex = "ONT" + str(index+1)
        ontSlotIDList.append(dut_data["ONT"][ontIndex]["slot_id"])
        ontPortIDList.append(dut_data["ONT"][ontIndex]["port_id"])
        ontOntIDList.append(dut_data["ONT"][ontIndex]["ont_id"])
        ontSNList.append(dut_data["ONT"][ontIndex]["sn_16"])
        ontPWList.append(dut_data["ONT"][ontIndex]["pw"])
        ontModelList.append(dut_data["ONT"][ontIndex]["model"])
        ontTypeList.append(dut_data["ONT"][ontIndex]["type"])
        ontFlagList.append(dut_data["ONT"][ontIndex]["flag"])

    geCount = dut_data["GE"]["exe_geCount"]
    geSlotIDList, gePortIDList, geTypeList, geLinkSpeedList = ([] for _ in range(4))
    for index in range(geCount):
        geIndex = "GE" + str(index+1)
        geSlotIDList.append(dut_data["GE"][geIndex]["slot_id"])
        gePortIDList.append(dut_data["GE"][geIndex]["port_id"])
        geTypeList.append(dut_data["GE"][geIndex]["type"])
        geLinkSpeedList.append(dut_data["GE"][geIndex]["linkspeed"])

    exeUpgradeONT = dut_data["ONT"]["exe_upgrade_ont"]
    upgradeOntFW = dut_data["ONT"][exeUpgradeONT]["fw_image"]
    upgradeOntFlag = dut_data["ONT"][exeUpgradeONT]["flag"]
    upgradeOntModel = dut_data["ONT"][exeUpgradeONT]["model"]
    upgradeOntSlotID = "--"
    if dut_data["ONT"][exeUpgradeONT]["slot_id"] != "0":
        upgradeOntSlotID = dut_data["ONT"][exeUpgradeONT]["slot_id"]
    upgradeOntPortID = dut_data["ONT"][exeUpgradeONT]["port_id"]
    upgradeOntOntID = dut_data["ONT"][exeUpgradeONT]["ont_id"]
    config.update({
        "ontCount": ontCount, "ontSlotIDList": ontSlotIDList, "ontPortIDList": ontPortIDList, "ontOntIDList": ontOntIDList,
        "ontSNList": ontSNList, "ontPWList": ontPWList, "ontModelList": ontModelList, "ontTypeList": ontTypeList, "ontFlagList": ontFlagList,
        "exeUpgradeONT": exeUpgradeONT, "upgradeOntFW": upgradeOntFW, "upgradeOntFlag": upgradeOntFlag, "upgradeOntModel": upgradeOntModel,
        "upgradeOntSlotID": upgradeOntSlotID, "upgradeOntPortID": upgradeOntPortID, "upgradeOntOntID": upgradeOntOntID,
        "geCount": geCount, "geSlotIDList": geSlotIDList, "gePortIDList": gePortIDList, "geTypeList":geTypeList, "geLinkSpeedList":geLinkSpeedList

    })
    serviceOntSN = serviceOntPW = serviceOntType = serviceOntFlag = ""
    ontInfo = []
    serviceGeType = serviceGeSpeed = ""
    geInfo = []
    exeServiceOnt = dut_data["ONT"]["exe_provision_ont"]
    if exeServiceOnt != "":
        serviceOntSN = dut_data["ONT"][exeServiceOnt]["sn_16"]
        serviceOntPW = dut_data["ONT"][exeServiceOnt]["pw"]
        serviceOntType = dut_data["ONT"][exeServiceOnt]["type"]
        serviceOntFlag = dut_data["ONT"][exeServiceOnt]["flag"]
        ontInfo = [dut_data["ONT"][exeServiceOnt]["slot_id"], dut_data["ONT"][exeServiceOnt]["port_id"], dut_data["ONT"][exeServiceOnt]["ont_id"]]
    exeServiceGe = dut_data["GE"]["exe_provision_ge"]
    if exeServiceGe != "":
        serviceGeType = dut_data["GE"][exeServiceGe]["type"]
        serviceGeSpeed = dut_data["GE"][exeServiceGe]["linkspeed"]
        geInfo = [dut_data["GE"][exeServiceGe]["slot_id"], dut_data["GE"][exeServiceGe]["port_id"]]
    config.update({
        "exeServiceOnt": exeServiceOnt, "serviceOntSN": serviceOntSN, "serviceOntPW": serviceOntPW, "serviceOntType": serviceOntType, "serviceOntFlag": serviceOntFlag,
        "ontInfo": ontInfo, "exeServiceGe": exeServiceGe, "serviceGeType": serviceGeType, "serviceGeSpeed": serviceGeSpeed, "geInfo": geInfo
    })
    deviceStatusCount, ontStatusCount, alarmStatusCount = 3, 7, 5
    alarmStatus = ["total","critical","major","minor","info"]
    emsLink = config["emsURL"].replace("netatlasems/index","?page=")
    dateFormat, timeZone = f"%Y-%m-%d %H:%M:%S", " (GMT+8)"
    config.update({
        "deviceStatusCount": deviceStatusCount, "ontStatusCount": ontStatusCount, "alarmStatusCount": alarmStatusCount,
        "alarmStatus": alarmStatus, "emsLink": emsLink, "dateFormat": dateFormat, "timeZone": timeZone,
    })
    
    return SimpleNamespace(**config)


# ====================================================================
# 3. 簡化後的關鍵 Fixture：根據傳入的參數決定生產哪台設備的 config
# ====================================================================
@pytest.fixture(scope="session")
def test_config(request):
    node_name = request.config.getoption("--cmdopt")
    obj = build_config_object(node_name)
    return obj

def pytest_itemcollected(item):
    node_name = None
    for arg in sys.argv:
        if arg.startswith("--cmdopt="):
            node_name = arg.split("=")[1]
            break
            
    if node_name:
        item.name = f"{item.name}[{node_name}]"
        item._nodeid = f"{item.nodeid}[{node_name}]"

# ====================================================================
# 4. 測試報告生成
# ====================================================================
def pytest_runtest_logreport(report):
    if "PYTEST_XDIST_TESTRUNUID" in os.environ:
        return
    if report.when == "call":
        node_name = None
        report_name = None
        try:
            match = re.search(r"(.*?)\.py", report.nodeid)
            report_name = match.group(1) if match else None
            report_name = f"EMS_{report_name}"

            match = re.search(r"\[(.+)\]", report.nodeid)
            node_name = match.group(1) if match else None
            
            if not node_name:
                import sys
                for arg in sys.argv:
                    if arg.startswith("--cmdopt="):
                        node_name = arg.split("=")[1]
                        break
            if not node_name:
                node_name = "UNKNOWN_NODE"
            cfg = build_config_object(node_name)
        except Exception:
            cfg = None
        if cfg:
            os.makedirs("./report", exist_ok=True)
            if "OLT" in cfg.dutType:
                report_file_name = f"./report/{report_name}_{cfg.emsVer}_{cfg.cardTypeName[0]}_{SESSION_TIMESTAMP}.txt"
            else:
                report_file_name = f"./report/{report_name}_{cfg.emsVer}_{cfg.dutType}_{cfg.cardTypeName[0]}_{SESSION_TIMESTAMP}.txt"
            file_is_new = not os.path.exists(report_file_name)
            with open(report_file_name, 'a', encoding='utf-8') as f:
                if file_is_new:
                    f.write(f"{report_name} Report\n")
                    f.write(f"{SESSION_TIMESTAMP}\n")
                    f.write(f"EMS URL   : {cfg.emsURL}\n")
                    f.write(f"EMS Ver   : {cfg.emsVer}\n\n")
                    if "OLT" not in cfg.dutType:
                        f.write(f"Device Type : {cfg.dutType}\n")
                    f.write(f"Device Info : \n")
                    for ind, cardType in enumerate(cfg.cardTypeName):
                        if cfg.dutAllCardID[ind] == "0":
                            continue
                        f.write(f"{cardType} : {cfg.cardFwVersion[ind]}\n")
                    f.write("\n" + "=" * 50 + "\n\n")
                
                # 清理 nodeid 字串，寫入 case 結果
                caseStr = re.sub(r"^.*::test_|\s*\[.*\]$", "", report.nodeid, flags=re.DOTALL)
                caseCount = caseStr.count("_") - 1
                caseStrList = caseStr.split("_")
                
                for caseStrInd in range(caseCount):
                    if report.outcome == "rerun":
                        continue
                    caseTitle = f"[{caseStrList[0]}-{caseStrList[caseStrInd+1]}][{caseStrList[-1]}]"
                    f.write(f"{caseTitle} Result {report.outcome}\n")
                
                if report.failed:
                    f.write(f"Details:\n{report.longrepr}\n")
                f.write("-"*50 + "\n")

