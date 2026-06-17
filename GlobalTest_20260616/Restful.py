import pytest
import json
import re
import os
import time
import telnetlib
import paramiko
import ftplib
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pytest_assume.plugin import assume
from libs.func import *


class TestRestful():
    driver = None

    rData = None
    rBootfwversion = rFwimage1version = rFwimage2version = rMscmode = rLocation = rContact = rSlotInfo = rPortInfo = rOntInfo = None
    slotCount = cardTypeDic = cardOperstatusDic = cardAdminstateDic = cardAlarmstateDic = portStatusSimpleDic = None
    portCount = portTypeDic = portOperstatusDic = portAdminstateDic = None
    ontCount = ontStatusDetailDic = ontStatusDic = ontStatusSimpleDic = rOntrowstatusDic = rOntrowstatusSimpleDic = rBootversionDic = rBootversionSimpleDic = None
    xontCount = rXontInfo = None

    @pytest.fixture(autouse=True, scope="class")
    def _inject_config(self, request, test_config):
        cls = request.cls
        # conftest.py 的設備配置給 cls 類別物件
        for key, value in vars(test_config).items():
            setattr(cls, key, value)
            
        # 2. 執行你原本透過 Telnet/SSH/FTP 撈取設備 restful 資料的核心邏輯（完全維持你原本的）
        dutSnmpType = re.sub(r".*V", "", cls.dutSnmpVer, flags=re.DOTALL)
        dutSnmp3Level = ""
        match cls.dutSnmp3Auth:
            case "No authentication and no privacy":
                dutSnmp3Level = "noAuthNoPriv"
            case "Authentication and no privacy":
                dutSnmp3Level = "authNoPriv"
            case "Authentication and privacy":
                dutSnmp3Level = "authPriv"
                
        emsUploadDevPathDebug = cls.emsURL.replace(":9116/netatlasems/index", "/RESTfulServer/Server/DevicePollerDebug/")
        snmpSetDevDataCmdDebug = "snmpset -v " + dutSnmpType + " -c " + cls.dutSet + " -u " + cls.dutAdminName + " -l " + dutSnmp3Level + " -a "\
                                + cls.dutSnmp3Hash + " -A " + cls.dutAdminPwd + " -x " + cls.dutSnmp3Encrypt + " -X " + cls.dutAdminPwd + " "\
                                + cls.dutIp + " 1.3.6.1.4.1.890.1.5.13.13.16.21.2.0 s \"" + emsUploadDevPathDebug + "\""
        if "NeoX" in cls.dutType:
            snmpSetDevDataCmdDebug = "snmpset -v " + dutSnmpType + " -c " + cls.dutSet + " -u " + cls.dutAdminName + " -l " + dutSnmp3Level + " -a "\
                                    + cls.dutSnmp3Hash + " -A " + cls.dutAdminPwd + " -x " + cls.dutSnmp3Encrypt + " -X " + cls.dutAdminPwd + " "\
                                    + cls.dutIp + " 1.3.6.1.4.1.890.1.5.19.1.16.21.2.0 s \"" + emsUploadDevPathDebug + "\""
        snmpSetDevDataCmd = snmpSetDevDataCmdDebug.replace("/RESTfulServer/Server/DevicePollerDebug/", "/RESTfulServer/Server/DevicePoller/")


        tn = telnetlib.Telnet(cls.dutIp, port=23, timeout=50)
        tn.read_until(b" login:")
        tn.write(cls.dutAdminName.encode('ascii') + b"\n")
        tn.read_until(b"Password:")
        tn.write(cls.dutAdminPwd.encode('ascii') + b"\n")
        tn.read_until(b"#").decode('ascii')
        
        tn.write(b"linux supervisor" + b"\n")
        tn.write(snmpSetDevDataCmdDebug.encode('ascii') + b"\n")
        time.sleep(3)
        tn.read_until(b"#").decode('ascii')
        tn.write(snmpSetDevDataCmd.encode('ascii') + b"\n")
        time.sleep(3)
        tn.read_until(b"#").decode('ascii')
        tn.write(b"cd /tmp/emsUpload/" + b"\n")
        tn.write(b"cat dev_data" + b"\n")
        resultRaw = tn.read_until(b"}").decode('ascii')
        result = re.sub(r".*{", "{", resultRaw, flags=re.DOTALL)
        tn.close()
        time.sleep(60)
        
        jResult = json.loads(result)
        dutUUIDDev = jResult["uuid"]
        os.makedirs("./report", exist_ok=True)
        with open("./report/dutDevInfo_" + dutUUIDDev + ".json", "w") as f:
            json.dump(jResult, f, indent=4)
            
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(cls.emsIp, 22, cls.emsSrvUsr, cls.emsSrvPwd)
        commands = client.invoke_shell()
        command_list = ["sudo su", cls.emsSuPwd, "cd /opt/ELEMENTVIEW_MASTER/bin", "chmod 777 " + dutUUIDDev]
        for command in command_list:
            commands.send(f"{command}\n") 
            time.sleep(2)
            output = commands.recv(1000000)
            print(output.decode("utf-8", errors="ignore"))
        client.close()

        ftp = ftplib.FTP()
        ftp.set_pasv(True)
        ftp.connect(cls.emsIp, 21)
        ftp.login(cls.emsSrvUsr, cls.emsSrvPwd)
        ftp.cwd("/opt/ELEMENTVIEW_MASTER/bin/")
        with open("./report/dutDevDataInfo_" + dutUUIDDev + ".json", "wb") as jFile:
            ftp.retrbinary("RETR " + dutUUIDDev, jFile.write)
        ftp.close()

        with open("./report/dutDevDataInfo_" + dutUUIDDev + ".json", errors="ignore") as jGFile:
            cls.rData = json.load(jGFile)

        # 3. 填入各項全域變數（這些變數會直接進到當前進程的 globals()
        cls.rBootfwversion = cls.rData["bootfwversion"]
        cls.rFwimage1version = cls.rData["fwimage1version"]
        cls.rFwimage2version = cls.rData["fwimage2version"]
        cls.rMscmode = cls.rData["mscmode"]

        cls.rSlotInfo = cls.rData["slotinfo"]
        cls.slotCount = len(cls.rSlotInfo)
        
        cls.cardTypeDic = {
            0:"empty", 1:"unknown", 11:"MSC1240XA", 12:"MSC1240XB", 13:"MSC1240XC", 14:"MSC1280XA", 15:"MSC1240QA", 
            16:"MSC1280X", 17:"MSC1280XB", 18: "MSC1240QB", 21:"VEC1001X", 22:"VEC1002X", 23:"OUL3540X", 31:"VLC1448X-51", 32:"VLC1448X-53", 
            33:"VLC1448X-51S", 34:"VLC1448X-51D", 35:"VLC1448X-51F", 41:"OLC3416-22", 42:"OLC3416-42", 43:"OLC3416-42A", 
            44:"OLC3416-42A-C", 45:"OLC3708-43A", 46:"OLC3416B-IA", 47:"OLC3816-IA", 51:"GLC1440X-55", 52:"GLC1440X-55A",
            53:"GLC1540X-55A"
        }
        if "NeoX" in cls.dutType:
            cls.cardTypeDic = {0:"empty", 1:"unknown", 11:"NXC400", 21:"NXP316", 31:"NXA340"}
            
        cls.cardOperstatusDic = {0:"Empty", 1:"Inactive", 2:"Init", 3:"Active", 4:"Standby", 5:"Disable"}
        cls.cardAdminstateDic = {1:"Enable", 2:"Disable"}
        cls.cardAlarmstateDic = {1:"Alarmed", 2:"No Alarm"}
        
        cls.rPortInfo = cls.rData["portinfo"]
        cls.portCount = len(cls.rPortInfo)
        cls.portTypeDic = {104:"VoIP", 255:"Network", 117:"Network", 6:"Ethernet Access", 62:"Ethernet Access", 18:"E1T1", 250:"GPON", 2500:"xPON"}
        if "NeoX" in cls.dutType:
            cls.portTypeDic = {255:"Network", 6:"Ethernet Access", 250:"xPON"}
        cls.portStatusSimpleDic = {1:"1", 2:"2"}
        cls.portOperstatusDic = {0:"Down", 1:"Up", 2:"Down", 3:"Testing"}
        cls.portAdminstateDic = {1:"Enable", 2:"Disable", 3:"Testing"}
        
        cls.rOntInfo = cls.rData["ontinfo"]
        cls.ontCount = len(cls.rOntInfo)
        cls.ontStatusDetailDic = {0 :"Out Of Service", 1 :"In Service", 2 :"Out Of Service - The related line card is OOS", 3 :"Out Of Service - ONU is not registered", 4 :"Out Of Service - The OMCC is blocked", 5 :"Out Of Service - This entity is not ever provisioned", 6 :"Out Of Service - ONU replies error during provision", 7 :"Out Of Service - The entity is down administratively", 8 :"Out Of Service - ONU reports it can't perform its function", 9 :"Out Of Service - The related ONU is OOS", 10 :"Out Of Service - The actual type mismatches with config type", 11 :"Out Of Service - The related onu card is OOS", 12 :"Out Of Service - The related UNI is OOS", 13 :"Out Of Service - The related NNI is OOS", 14 :"Out Of Service - One or many of the related GEM ports are temporarily closed", 15 :"Out Of Service - One or many of the related GEM ports fails during creation", 16 :"Out Of Service - One or many of the related allocation ID fails during creation", 17 :"Out Of Service - The related VLAN service is OOS", 18 :"Out Of Service - ONU was ever registered, after that, it was deregistered due to loss of power", 19 :"Out Of Service - ONU was ever registered, after that, it was deregistered due to loss of signal", 20 :"Out Of Service - ONU is in standby mode in a protection groupDevice Not Responding"}
        cls.ontStatusDic = {0 :"OOS", 1 :"IS", 2 :"OOS", 3 :"OOS", 4 :"OOS", 5 :"OOS", 6 :"OOS", 7 :"OOS", 8 :"OOS", 9 :"OOS", 10 :"OOS", 11 :"OOS", 12 :"OOS", 13 :"OOS", 14 :"OOS", 15 :"OOS", 16 :"OOS", 17 :"OOS", 18 :"OOS", 19 :"OOS", 20 :"OOS"}
        cls.ontStatusSimpleDic = {1:"1", 2:"2", 3:"3", 4:"4", 5:"5", 19:"6", 18:"7"}
        cls.rOntrowstatusDic = {1: "Active", 2 :"Not In Service", 3: "Not Ready"}
        cls.rOntrowstatusSimpleDic = {1: "Active", 2 :"Inactive"}
        cls.rBootversionDic = {0: "None", 1: "Version 1", 2: "Version 2"}
        cls.rBootversionSimpleDic = {0: "--", 1: "1", 2: "2"}

        cls.rXontInfo = cls.rData["xontinfo"]
        cls.xontCount = len(cls.rXontInfo)

    @pytest.fixture(autouse=True, scope="class")
    def setup_browser(self, request, _inject_config):
        cls = request.cls
        print("\n正在啟動瀏覽器並登入 EMS...")
        match cls.browser:
            case "chrome":
                options = webdriver.ChromeOptions()
                options.add_argument('ignore-certificate-errors')
                cls.driver = webdriver.Chrome(options)
            case "edge":
                options = webdriver.EdgeOptions()
                options.add_argument('ignore-certificate-errors')
                cls.driver = webdriver.Edge(options)
            case "firefox":
                options = webdriver.FirefoxOptions()
                options.add_argument('-ignore-certificate-errors')
                cls.driver = webdriver.Firefox(options)   
        cls.driver.implicitly_wait(cls.waitTime)
        cls.driver.maximize_window()
        cls.driver.get(cls.emsURL)
        loginEMS(cls, cls.emsUsr, cls.emsPwd)
        time.sleep(3)
        yield
        if hasattr(cls, "driver"):
            print("\n所有測試執行完畢，關閉瀏覽器。")
            cls.driver.quit() 

    #Edith Inventory/ Device
    @pytest.mark.restful
    def test_EMS1_6686_devDeviceInfo(self):
        self.driver.find_element(By.LINK_TEXT, "Inventory").click()
        WebDriverWait(self.driver, 300).until(EC.visibility_of_element_located((By.LINK_TEXT, "Device")))
        time.sleep (3)
        entryPosition = getPositionByCol(self, "dev_inventory_div", "IPAddress", self.dutIp)
        rLocation = self.rData["location"] if self.rData["location"] != "" else "--"
        rContact = self.rData["contact"] if self.rData["contact"] != "" else "--"
        EMS_Location = getElementByPositionCol(self, "dev_inventory_div", entryPosition , "Location").text
        EMS_Contact = getElementByPositionCol(self, "dev_inventory_div", entryPosition , "Contact").text
        EMS_BootFwVersion = getElementByPositionCol(self, "dev_inventory_div", entryPosition , "BootFwVersion").text
        EMS_FwVersion1 = getElementByPositionCol(self, "dev_inventory_div", entryPosition , "FwVersion1").text 
        EMS_FwVersion2 = getElementByPositionCol(self, "dev_inventory_div", entryPosition , "FwVersion2").text
        with assume: assert EMS_Location == rLocation
        with assume: assert EMS_Contact == rContact
        with assume: assert EMS_BootFwVersion == self.rBootfwversion
        with assume: assert EMS_FwVersion1 == self.rFwimage1version
        with assume: assert EMS_FwVersion2 == self.rFwimage2version

    #Edith Dashboard/ Device Dashboard
    @pytest.mark.restful
    def test_EMS1_6687_devDeviceInfoDashboard(self):
        self.driver.find_element(By.LINK_TEXT, "Dashboard").click()
        WebDriverWait(self.driver, 300).until(EC.visibility_of_element_located((By.XPATH, "//div[@id=\'dashboard_net_title\']")))
        time.sleep(3)
        rLocation = self.rData["location"] if self.rData["location"] != "" else "--"
        rContact = self.rData["contact"] if self.rData["contact"] != "" else "--"
        self.driver.find_element(By.XPATH, "//div[@id=\'devStatus\']/div[1]/div[2]/a").click()
        entryPosition = getPositionByCol(self, "All_devStatusTable", "IPAddress", self.dutIp)
        with assume: assert getElementByPositionCol(self, "All_devStatusTable", entryPosition , "Contact").text == rContact
        with assume: assert getElementByPositionCol(self, "All_devStatusTable", entryPosition , "Location").text == rLocation
        with assume: assert getElementByPositionCol(self, "All_devStatusTable", entryPosition , "BootFwVersion").text == self.rBootfwversion
        with assume: assert getElementByPositionCol(self, "All_devStatusTable", entryPosition , "FwVersion1").text == self.rFwimage1version
        with assume: assert getElementByPositionCol(self, "All_devStatusTable", entryPosition , "FwVersion2").text == self.rFwimage2version
        
    #Edith Inventory/ Card
    @pytest.mark.restful
    def test_EMS1_6688_devSlotInfo(self):
        self.driver.find_element(By.LINK_TEXT, "Inventory").click()
        WebDriverWait(self.driver, 300).until(EC.visibility_of_element_located((By.LINK_TEXT, "Card")))
        time.sleep (3)
        self.driver.find_element(By.LINK_TEXT, "Card").click()
        self.driver.find_element(By.CSS_SELECTOR, "#i_action_filter > a").click()
        self.driver.find_element(By.ID, "inventory_slot_clear_btn").click()
        self.driver.find_element(By.ID, "ip2").send_keys(self.dutIp)
        self.driver.find_element(By.ID, "inventory_slot_btn").click()
        for slotIndex in range(self.slotCount):
            rSlot = self.rSlotInfo[slotIndex]["slot"]
            rType = self.rSlotInfo[slotIndex]["type"]
            rOperstatus = self.rSlotInfo[slotIndex]["operstatus"]
            rAdminstate = self.rSlotInfo[slotIndex]["adminstate"]
            rAlarmstate = self.rSlotInfo[slotIndex]["alarmstate"]
            rHwversion = self.rSlotInfo[slotIndex]["hwversion"] if self.rSlotInfo[slotIndex]["hwversion"] != "" else "--"
            rFwversion = self.rSlotInfo[slotIndex]["fwversion"] if self.rSlotInfo[slotIndex]["fwversion"] != "" else "--"
            rSerialnumber = self.rSlotInfo[slotIndex]["serialnumber"] if self.rSlotInfo[slotIndex]["serialnumber"] != "" else "--"
            entryPosition = getPositionByColNext(self, "card_inventory_div", "SlotID", str(rSlot))
            with assume: assert getElementByPositionCol(self, "card_inventory_div", entryPosition , "SlotID").text == str(rSlot), f"Slot {rSlot}"
            with assume: assert getElementByPositionCol(self, "card_inventory_div", entryPosition , "RealType").text == self.cardTypeDic[rType], f"Slot {rSlot}"
            with assume: assert getElementByPositionCol(self, "card_inventory_div", entryPosition , "OperationStatus").text == self.cardOperstatusDic[rOperstatus], f"Slot {rSlot}"
            with assume: assert getElementByPositionCol(self, "card_inventory_div", entryPosition , "AdminState").text == self.cardAdminstateDic[rAdminstate], f"Slot {rSlot}"
            with assume: assert getElementByPositionCol(self, "card_inventory_div", entryPosition , "AlarmStatus").text == self.cardAlarmstateDic[rAlarmstate], f"Slot {rSlot}"
            with assume: assert getElementByPositionCol(self, "card_inventory_div", entryPosition , "HwVersion").text == rHwversion, f"Slot {rSlot}"
            with assume: assert getElementByPositionCol(self, "card_inventory_div", entryPosition , "FwVersion").text == rFwversion, f"Slot {rSlot}"
            with assume: assert getElementByPositionCol(self, "card_inventory_div", entryPosition , "SerialNo").text == rSerialnumber, f"Slot {rSlot}"

    #Edith Inventory/ Port/ All Port
    @pytest.mark.restful
    def test_EMS1_6689_devPortInfoInventoryAllPort(self):
        self.driver.find_element(By.LINK_TEXT, "Inventory").click()
        WebDriverWait(self.driver, 300).until(EC.visibility_of_element_located((By.LINK_TEXT, "Port")))
        time.sleep (3)
        self.driver.find_element(By.LINK_TEXT, "Port").click()
        time.sleep (3)
        self.driver.find_element(By.ID, "AllPort").click()
        time.sleep (3)
        for portIndex in range(self.portCount):
            rSlot = self.rPortInfo[portIndex]["slot"]
            rPort = self.rPortInfo[portIndex]["port"]
            rType = self.rPortInfo[portIndex]["type"]
            if rPort == 0 or rPort == 99 or rPort == 999:
                continue
            if self.rMscmode == "1" and self.rSlotInfo[rSlot-1]["operstatus"] == 4:
                continue
            if self.rMscmode == "0" and self.rSlotInfo[rSlot-1]["operstatus"] == 3 and rPort > 6:
                continue
            if 45<= self.rSlotInfo[rSlot-1]["type"] <= 47:
                rType = 2500
            #if 11<= self.rSlotInfo[rSlot-1]["type"] <= 18 and ("NeoX" not in self.dutType):
            if 11<= self.rSlotInfo[rSlot-1]["type"] <= 18:
                rType = 255
            if rPort == 1:
                self.driver.find_element(By.CSS_SELECTOR, "#i_action_refresh > a").click()
                self.driver.find_element(By.CSS_SELECTOR, "#i_action_filter > a").click()
                self.driver.find_element(By.ID, "inventory_allport_clear_btn").click()
                self.driver.find_element(By.ID, "ip_all").send_keys(self.dutIp)
                self.driver.find_element(By.ID, "slot_all").send_keys(rSlot)
                self.driver.find_element(By.ID, "inventory_allport_btn").click()
            rName = self.rPortInfo[portIndex]["name"] if self.rPortInfo[portIndex]["name"] != "" else "--"
            rTel = self.rPortInfo[portIndex]["tel"]
            rOperstatus = self.rPortInfo[portIndex]["operstatus"]
            rAdminstate = self.rPortInfo[portIndex]["adminstate"]
            rLinetemplate = self.rPortInfo[portIndex]["linetemplate"]
            rAlarmtemplate = self.rPortInfo[portIndex]["alarmtemplate"]
            rUpstreamrate = self.rPortInfo[portIndex]["upstreamrate"]
            rDownstreamrate = self.rPortInfo[portIndex]["downstreamrate"]
            rRate = self.rPortInfo[portIndex]["rate"]
            rFiberstatus = self.rPortInfo[portIndex]["fiberstatus"]
            rLedstatus = self.rPortInfo[portIndex]["ledstatus"]
            entryPosition = getPositionByColNext(self, "port_inventory_div", "PortID", str(rPort))
            print( "slot id: " + str(rSlot) + "port id: " + str(rPort))
            with assume: assert getElementByPositionCol(self, "port_inventory_div", entryPosition , "SlotID").text == str(rSlot), f"Slot {rSlot}, Port {rPort}"
            with assume: assert getElementByPositionCol(self, "port_inventory_div", entryPosition , "PortID").text == str(rPort), f"Slot {rSlot}, Port {rPort}"
            with assume: assert getElementByPositionCol(self, "port_inventory_div", entryPosition , "PortType").text == self.portTypeDic.get(rType, "Unknown: "+ str(rType)), f"Slot {rSlot}, Port {rPort}"
            with assume: assert getElementByPositionCol(self, "port_inventory_div", entryPosition , "PortName").text == str(rName), f"Slot {rSlot}, Port {rPort}"
            with assume: assert getElementByPositionCol(self, "port_inventory_div", entryPosition , "portOperationStatus").text == self.portOperstatusDic[rOperstatus], f"Slot {rSlot}, Port {rPort}"
            with assume: assert getElementByPositionCol(self, "port_inventory_div", entryPosition , "portAdminState").text == self.portAdminstateDic[rAdminstate], f"Slot {rSlot}, Port {rPort}"
            #ddmi string type
            if  isinstance (self.rPortInfo[portIndex]["ddmitxpower"], str) and isinstance (self.rPortInfo[portIndex]["ddmirxpower"], str):
                rDdmitxpower = self.rPortInfo[portIndex]["ddmitxpower"] if self.rPortInfo[portIndex]["ddmitxpower"] != "" else "--"
                rDdmirxpower = self.rPortInfo[portIndex]["ddmirxpower"] if self.rPortInfo[portIndex]["ddmirxpower"] != "" else "--"
                if rDdmitxpower != "--" and rDdmitxpower != "N/A" and rDdmitxpower != "0.00":
                    rDdmitxpowerFloat = float(rDdmitxpower)
                    txRowerFloat = float(getElementByPositionCol(self, "port_inventory_div", entryPosition , "txPower").text)
                    with assume: assert rDdmitxpowerFloat-0.99 <= txRowerFloat <= rDdmitxpowerFloat+0.99
                else:
                    with assume: assert getElementByPositionCol(self, "port_inventory_div", entryPosition , "txPower").text == rDdmitxpower, f"Slot {rSlot}, Port {rPort}"
                if rDdmirxpower != "--" and rDdmirxpower != "N/A" and rDdmirxpower != "0.00":
                    rDdmirxpowerFloat = float(rDdmirxpower)
                    rxRowerFloat = float(getElementByPositionCol(self, "port_inventory_div", entryPosition , "rxPower").text)
                    with assume: assert rDdmirxpowerFloat-0.99 <= rxRowerFloat <= rDdmirxpowerFloat+0.99
                else:
                    with assume: assert getElementByPositionCol(self, "port_inventory_div", entryPosition , "rxPower").text == rDdmirxpower, f"Slot {rSlot}, Port {rPort}"
            #ddmi array type

    
    #Edith Inventory/ Differnt Type Port
    @pytest.mark.restful
    def test_EMS1_6690_devPortInfoInventoryTypePort(self):
        self.driver.find_element(By.LINK_TEXT, "Inventory").click()
        WebDriverWait(self.driver, 300).until(EC.visibility_of_element_located((By.LINK_TEXT, "Port")))
        time.sleep (3)
        self.driver.find_element(By.LINK_TEXT, "Port").click()
        for portIndex in range(self.portCount):
            checkTel = False
            rSlot = self.rPortInfo[portIndex]["slot"]
            rPort = self.rPortInfo[portIndex]["port"]
            rType = self.rPortInfo[portIndex]["type"]
            if rPort == 0 or rPort == 99 or rPort == 999:
                continue
            if self.rMscmode == "1" and self.rSlotInfo[rSlot-1]["operstatus"] == 4:
                continue
            if self.rMscmode == "0" and self.rSlotInfo[rSlot-1]["operstatus"] == 3 and rPort > 6:
                continue
            if 45<= self.rSlotInfo[rSlot-1]["type"] <= 47:
                rType = 2500
            #if 11<= self.rSlotInfo[rSlot-1]["type"] <= 18 and ("NeoX" not in self.dutType):
            if 11<= self.rSlotInfo[rSlot-1]["type"] <= 18:
                rType = 255
            if rPort == 1:
                self.driver.find_element(By.LINK_TEXT, self.portTypeDic[rType] + " Port").click()
                self.driver.find_element(By.CSS_SELECTOR, "#i_action_refresh > a").click()
                self.driver.find_element(By.CSS_SELECTOR, "#i_action_filter > a").click()
                match self.portTypeDic[rType]:
                    case "Network":
                        checkTel = True
                        self.driver.find_element(By.ID, "inventory_network_clear_btn").click()
                        self.driver.find_element(By.ID, "ip_network").send_keys(self.dutIp)
                        self.driver.find_element(By.ID, "slot_network").send_keys(rSlot)
                        self.driver.find_element(By.ID, "inventory_network_btn").click()
                    case "Ethernet Access":
                        checkTel = True
                        self.driver.find_element(By.ID, "inventory_ethernet_clear_btn").click()
                        self.driver.find_element(By.ID, "ip_ethernet").send_keys(self.dutIp)
                        self.driver.find_element(By.ID, "slot_ethernet").send_keys(rSlot)
                        self.driver.find_element(By.ID, "inventory_ethernet_btn").click()
                    case "GPON":
                        self.driver.find_element(By.ID, "inventory_pon_clear_btn").click()
                        self.driver.find_element(By.ID, "ip_pon").send_keys(self.dutIp)
                        self.driver.find_element(By.ID, "slot_pon").send_keys(rSlot)
                        self.driver.find_element(By.ID, "inventory_pon_btn").click()
                    case "xPON":
                        self.driver.find_element(By.ID, "inventory_xpon_clear_btn").click()
                        self.driver.find_element(By.ID, "ip_xpon").send_keys(self.dutIp)
                        self.driver.find_element(By.ID, "slot_xpon").send_keys(rSlot)
                        self.driver.find_element(By.ID, "inventory_xpon_btn").click()
            rName = self.rPortInfo[portIndex]["name"] if self.rPortInfo[portIndex]["name"] != "" else "--"
            rTel = self.rPortInfo[portIndex]["tel"] if self.rPortInfo[portIndex]["tel"] != "" else "--"
            rOperstatus = self.rPortInfo[portIndex]["operstatus"]
            rAdminstate = self.rPortInfo[portIndex]["adminstate"]
            rLinetemplate = self.rPortInfo[portIndex]["linetemplate"]
            rAlarmtemplate = self.rPortInfo[portIndex]["alarmtemplate"]
            rUpstreamrate = self.rPortInfo[portIndex]["upstreamrate"]
            rDownstreamrate = self.rPortInfo[portIndex]["downstreamrate"]
            rFiberstatus = self.rPortInfo[portIndex]["fiberstatus"]
            rLedstatus = self.rPortInfo[portIndex]["ledstatus"]
            rRate = ""
            match self.rPortInfo[portIndex]["rate"]:
                case 0: rRate = "None"
                case range(1,1000): rRate = str(self.rPortInfo[portIndex]["rate"]) + " M"
                case _ : 
                    if self.rPortInfo[portIndex]["rate"]%1000 == 0:
                        rRate = str(self.rPortInfo[portIndex]["rate"]//1000) + "G"
                    else:
                        rRate = str(self.rPortInfo[portIndex]["rate"]/1000) + "G"
            entryPosition = getPositionByColNext(self, "port_inventory_div", "PortID", str(rPort))
            with assume: assert getElementByPositionCol(self, "port_inventory_div", entryPosition , "SlotID").text == str(rSlot), f"Slot {rSlot}, Port {rPort}"
            with assume: assert getElementByPositionCol(self, "port_inventory_div", entryPosition , "PortID").text == str(rPort), f"Slot {rSlot}, Port {rPort}"
            with assume: assert getElementByPositionCol(self, "port_inventory_div", entryPosition , "PortName").text == str(rName), f"Slot {rSlot}, Port {rPort}"
            if checkTel:
                with assume: assert getElementByPositionCol(self, "port_inventory_div", entryPosition , "Tel").text == str(rTel), f"Slot {rSlot}, Port {rPort}"
            with assume: assert getElementByPositionCol(self, "port_inventory_div", entryPosition , "portOperationStatus").text == self.portOperstatusDic[rOperstatus], f"Slot {rSlot}, Port {rPort}"
            with assume: assert getElementByPositionCol(self, "port_inventory_div", entryPosition , "portAdminState").text == self.portAdminstateDic[rAdminstate], f"Slot {rSlot}, Port {rPort}"
            with assume: assert getElementByPositionCol(self, "port_inventory_div", entryPosition , "EnetPortLinkStatus").text == rRate, f"Slot {rSlot}, Port {rPort}"
            #ddmi string type
            if  isinstance (self.rPortInfo[portIndex]["ddmitxpower"], str) and isinstance (self.rPortInfo[portIndex]["ddmirxpower"], str):
                rDdmitxpower = self.rPortInfo[portIndex]["ddmitxpower"] if self.rPortInfo[portIndex]["ddmitxpower"] != "" else "--"
                rDdmirxpower = self.rPortInfo[portIndex]["ddmirxpower"] if self.rPortInfo[portIndex]["ddmirxpower"] != "" else "--"
                if rDdmitxpower != "--" and rDdmitxpower != "N/A" and rDdmitxpower != "0.00":
                    rDdmitxpowerFloat = float(rDdmitxpower)
                    txRowerFloat = float(getElementByPositionCol(self, "port_inventory_div", entryPosition , "txPower").text)
                    with assume: assert rDdmitxpowerFloat-0.99 <= txRowerFloat <= rDdmitxpowerFloat+0.99
                else:
                    with assume: assert getElementByPositionCol(self, "port_inventory_div", entryPosition , "txPower").text == rDdmitxpower, f"Slot {rSlot}, Port {rPort}"
                if rDdmirxpower != "--" and rDdmirxpower != "N/A" and rDdmirxpower != "0.00":
                    rDdmirxpowerFloat = float(rDdmirxpower)
                    rxRowerFloat = float(getElementByPositionCol(self, "port_inventory_div", entryPosition , "rxPower").text)
                    with assume: assert rDdmirxpowerFloat-0.99 <= rxRowerFloat <= rDdmirxpowerFloat+0.99
                else:
                    with assume: assert getElementByPositionCol(self, "port_inventory_div", entryPosition , "rxPower").text == rDdmirxpower, f"Slot {rSlot}, Port {rPort}"
            #ddmi array type



    #Edith Map/ Device/ Port status
    @pytest.mark.restful
    def test_EMS1_6691_devPortInfoMapPort(self):
        self.driver.find_element(By.LINK_TEXT, "Map").click()
        time.sleep (3)
        self.driver.find_element(By.ID, "navside_icon").click()
        time.sleep (3)
        for portIndex in range(self.portCount):
            rSlot = self.rPortInfo[portIndex]["slot"]
            rPort = self.rPortInfo[portIndex]["port"]
            rType = self.rPortInfo[portIndex]["type"]
            rName = self.rPortInfo[portIndex]["name"] if self.rPortInfo[portIndex]["name"] != "" else "--"
            rOperstatus = self.rPortInfo[portIndex]["operstatus"]
            if rPort == 0 or rPort == 99 or rPort == 999:
                continue
            if self.rMscmode == "1" and self.rSlotInfo[rSlot-1]["operstatus"] == 4:
                continue
            if self.rMscmode == "0" and self.rSlotInfo[rSlot-1]["operstatus"] == 3 and rPort > 6:
                continue
            if 45<= self.rSlotInfo[rSlot-1]["type"] <= 47:
                rType = 2500
            #if 11<= self.rSlotInfo[rSlot-1]["type"] <= 18 and ("NeoX" not in self.dutType):
            if 11<= self.rSlotInfo[rSlot-1]["type"] <= 18:
                rType = 255
            if rPort == 1:
                expandElement = self.driver.find_element(By.XPATH, "//*[@id=\'navMenuTree\']/ul/li[contains(.,\'" + self.dutNodeName + "\')]/span[contains(@class,\'expand-icon\')]")
                expandStatus = expandElement.get_attribute("class")
                if expandStatus == "icon expand-icon oi oi-plus":
                    expandElement.click()
                dutNodeId = int(self.driver.find_element(By.XPATH, "//*[@id=\'navMenuTree\']/ul/li[contains(.,\'" + self.dutNodeName + "\')]").get_attribute("data-nodeid"))
                cardNodeId = dutNodeId + rSlot
                self.driver.find_element(By.XPATH, "//*[@id=\'navMenuTree\']/ul/li[contains(@data-nodeid,\'" + str(cardNodeId) + "\')]").click()
                time.sleep (3)
            with assume: assert getElementByPositionColNoPage(self, "Slot_portStatusTable", rPort , "PortName").text == rName, f"Slot {rSlot}, Port {rPort}"
            with assume: assert getElementByPositionColNoPage(self, "Slot_portStatusTable", rPort , "portOperationStatus").text == self.portOperstatusDic[rOperstatus], f"Slot {rSlot}, Port {rPort}"
            with assume: assert getElementByPositionColNoPage(self, "Slot_portStatusTable", rPort , "PortType").text == self.portTypeDic.get(rType, "Unknown: "+ str(rType)), f"Slot {rSlot}, Port {rPort}"

    #Edith Inventory/ Ont/ All ONT
    @pytest.mark.restful
    def test_EMS1_6692_devOntInfoInventoryAllOnt(self):
        self.driver.find_element(By.LINK_TEXT, "Inventory").click()
        WebDriverWait(self.driver, 300).until(EC.visibility_of_element_located((By.LINK_TEXT, "ONT")))
        time.sleep (3)
        self.driver.find_element(By.LINK_TEXT, "ONT").click()
        self.driver.find_element(By.CSS_SELECTOR, "#i_action_refresh > a").click()
        rPortOld = 0
        rSlotOld = 0
        for ontIndex in range(self.ontCount):
            rSlot = self.rOntInfo[ontIndex]["slot"]
            rPort = self.rOntInfo[ontIndex]["port"]
            rOntid = ""
            rSn = self.rOntInfo[ontIndex]["sn"] if self.rOntInfo[ontIndex]["sn"] != "" else "--"
            rPassword = self.rOntInfo[ontIndex]["password"] if self.rOntInfo[ontIndex]["password"] != "" else "--"
            rOntstate = self.rOntInfo[ontIndex]["ontstate"]
            if rPortOld != rPort or rSlotOld != rSlot:
                self.driver.find_element(By.CSS_SELECTOR, "#i_action_filter > a").click()
                self.driver.find_element(By.ID, "inventory_allont_clear_btn").click()
                self.driver.find_element(By.ID, "ip_Allont").send_keys(self.dutIp)
                self.driver.find_element(By.ID, "slot_Allont").send_keys(rSlot)
                self.driver.find_element(By.ID, "port_Allont").send_keys(rPort)
                self.driver.find_element(By.ID, "inventory_allont_btn").click()
                time.sleep (3)
            rPortOld = rPort
            rSlotOld = rSlot
            if 124 < self.rOntInfo[ontIndex]["ontid"] < 129:
                continue
            elif self.rOntInfo[ontIndex]["ontid"] > 1000:
                rOntid = "Unregistered"
                entryPosition = getPositionByColNext(self, "ont_inventory_div", "sn", rSn)
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "Slot").text == str(rSlot), f"Slot {rSlot}, Port {rPort}, SN {rSn}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "Port").text == str(rPort), f"Slot {rSlot}, Port {rPort}, SN {rSn}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "ONT").text == rOntid, f"Slot {rSlot}, Port {rPort}, SN {rSn}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "sn").text == rSn, f"Slot {rSlot}, Port {rPort}, SN {rSn}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "password").text == rPassword, f"Slot {rSlot}, Port {rPort}, SN {rSn}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "OntOperationStatus").text == "Unknown", f"Slot {rSlot}, Port {rPort}, SN {rSn}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "model").text == "--", f"Slot {rSlot}, Port {rPort}, SN {rSn}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "activeVersion").text == "--", f"Slot {rSlot}, Port {rPort}, SN {rSn}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "versionA").text == "--", f"Slot {rSlot}, Port {rPort}, SN {rSn}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "versionB").text == "--", f"Slot {rSlot}, Port {rPort}, SN {rSn}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "ontDistance").text == "0", f"Slot {rSlot}, Port {rPort}, SN {rSn}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "description").text == "--", f"Slot {rSlot}, Port {rPort}, SN {rSn}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "OntAdminState").text == "Unknown", f"Slot {rSlot}, Port {rPort}, SN {rSn}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "templateName").text == "--", f"Slot {rSlot}, Port {rPort}, SN {rSn}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "txPower").text == "--", f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "rxPower").text == "--", f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "ONTType").text == "--", f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
            else:
                rOntid = str(self.rOntInfo[ontIndex]["ontid"])
                entryPosition = getPositionByColNext(self, "ont_inventory_div", "ONT", rOntid)
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "Slot").text == str(rSlot), f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "Port").text == str(rPort), f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "ONT").text == rOntid, f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                rModel = self.rOntInfo[ontIndex]["model"] if self.rOntInfo[ontIndex]["model"] != "" else "--"
                rBootversion = self.rOntInfo[ontIndex]["bootversion"]
                rFwversiona = self.rOntInfo[ontIndex]["fwversiona"] if self.rOntInfo[ontIndex]["fwversiona"] != "" else "--"
                rFwversionb = self.rOntInfo[ontIndex]["fwversionb"] if self.rOntInfo[ontIndex]["fwversionb"] != "" else "--"
                rDistance = self.rOntInfo[ontIndex]["distance"]
                rDescription = self.rOntInfo[ontIndex]["description"] if self.rOntInfo[ontIndex]["description"] != "" else "--"
                rPppoestate = self.rOntInfo[ontIndex]["pppoestate"]
                rWanip = self.rOntInfo[ontIndex]["wanip"]
                rOntrowstatus = self.rOntInfo[ontIndex]["ontrowstatus"]
                rTemplatename = self.rOntInfo[ontIndex]["templatename"]if self.rOntInfo[ontIndex]["templatename"] != "" else "--"
                rActuralsn = self.rOntInfo[ontIndex]["acturalsn"]
                rActuralpassword = self.rOntInfo[ontIndex]["acturalpassword"]
                rTxpower = self.rOntInfo[ontIndex]["txpower"]if self.rOntInfo[ontIndex]["txpower"] != "" else "--"
                rRxpower = self.rOntInfo[ontIndex]["rxpower"]if self.rOntInfo[ontIndex]["rxpower"] != "" else "--"
                rWaninfo = self.rOntInfo[ontIndex]["waninfo"]
                if self.ontStatusDetailDic[rOntstate] == "In Service":
                    with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "sn").text == rActuralsn, f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                    with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "password").text == rActuralpassword, f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                    if rTxpower != "--" and rTxpower != "N/A" and rTxpower != "0.00":
                        rTxpowerFloat = float(rTxpower)
                        txRowerFloat = float(getElementByPositionCol(self, "ont_inventory_div", entryPosition , "txPower").text)
                        with assume: assert rTxpowerFloat-0.99 <= txRowerFloat <= rTxpowerFloat+0.99
                    else:
                        with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "txPower").text == rTxpower, f"Slot {rSlot}, Port {rPort}"
                    if rRxpower != "--" and rRxpower != "N/A" and rRxpower != "0.00":
                        rRxpowerFloat = float(rRxpower)
                        rxRowerFloat = float(getElementByPositionCol(self, "ont_inventory_div", entryPosition , "rxPower").text)
                        with assume: assert rRxpowerFloat-0.99 <= rxRowerFloat <= rRxpowerFloat+0.99
                    else:
                        with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "rxPower").text == rRxpower, f"Slot {rSlot}, Port {rPort}"
                else:
                    with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "sn").text == rSn, f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                    with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "password").text == rPassword, f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                    with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "txPower").text == "--", f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                    with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "rxPower").text == "--", f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "OntOperationStatus").text == self.ontStatusDetailDic.get(rOntstate, "Unknow"), f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "model").text == rModel, f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "OntAdminState").text == self.rOntrowstatusDic.get(rOntrowstatus, "Unknow"), f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "activeVersion").text == self.rBootversionDic.get(rBootversion, "--"), f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "versionA").text == rFwversiona, f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "versionB").text == rFwversionb, f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "ontDistance").text == str(rDistance), f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "description").text == rDescription, f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "templateName").text == rTemplatename, f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "ONTType").text == "GPON", f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"

    #Edith Map/ Device/ Ont Status
    @pytest.mark.restful
    def test_EMS1_6693_devOntInfoMapDevice(self):
        self.driver.find_element(By.LINK_TEXT, "Map").click()
        WebDriverWait(self.driver, 300).until(EC.visibility_of_element_located((By.ID, "navside_icon")))
        time.sleep (3)
        self.driver.find_element(By.ID, "navside_icon").click()
        self.driver.find_element(By.XPATH, "//li[contains(.,\'" + self.dutNodeName + "\')]").click()
        time.sleep (3)
        self.driver.find_element(By.ID, "navside_icon").click()
        for ontIndex in range(self.ontCount):
            rSlot = str(self.rOntInfo[ontIndex]["slot"])
            rPort = str(self.rOntInfo[ontIndex]["port"])
            rOntid = str(self.rOntInfo[ontIndex]["ontid"])
            if self.rOntInfo[ontIndex]["ontid"] < 125:
                rSn = self.rOntInfo[ontIndex]["sn"] if self.rOntInfo[ontIndex]["sn"] != "" else "--"
                rPassword = self.rOntInfo[ontIndex]["password"] if self.rOntInfo[ontIndex]["password"] != "" else "--"
                rActuralsn = self.rOntInfo[ontIndex]["acturalsn"]
                rActuralpassword = self.rOntInfo[ontIndex]["acturalpassword"]
                rModel = self.rOntInfo[ontIndex]["model"] if self.rOntInfo[ontIndex]["model"] != "" else "--"
                rOntrowstatus = self.rOntInfo[ontIndex]["ontrowstatus"]
                rOntstate = self.rOntInfo[ontIndex]["ontstate"]
                rDescription = self.rOntInfo[ontIndex]["description"] if self.rOntInfo[ontIndex]["description"] != "" else "--"
                rTemplatename = self.rOntInfo[ontIndex]["templatename"] if self.rOntInfo[ontIndex]["templatename"] != "" else "--"
                ontStatus = self.ontStatusSimpleDic[rOntstate]
                if "dashboard-underborder-green" not in self.driver.find_element(By.XPATH, "//div[@id=\'ontStatus\']/div[" + ontStatus + "]/div[2]").get_attribute("className"):
                    self.driver.find_element(By.XPATH, "//div[@id=\'ontStatus\']/div[" + ontStatus + "]/div[2]/a").click()
                entryPosition = getPositionByColsNext(self, "Dev_ontStatusTable", {"Slot": rSlot, "Port": rPort, "ONT": rOntid})
                if self.ontStatusDetailDic[rOntstate] == "In Service":
                    with assume: assert getElementByPositionCol(self, "Dev_ontStatusTable", entryPosition , "sn").text == rActuralsn, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "Dev_ontStatusTable", entryPosition , "password").text == rActuralpassword, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                else:
                    with assume: assert getElementByPositionCol(self, "Dev_ontStatusTable", entryPosition , "sn").text == rSn, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "Dev_ontStatusTable", entryPosition , "password").text == rPassword, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "Dev_ontStatusTable", entryPosition , "model").text == rModel, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "Dev_ontStatusTable", entryPosition , "OntAdminState").text == self.rOntrowstatusDic.get(rOntrowstatus, "Unknow"), f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "Dev_ontStatusTable", entryPosition , "OntOperationStatus").text == self.ontStatusDetailDic.get(rOntstate, "Unknow"), f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "Dev_ontStatusTable", entryPosition , "description").text == rDescription, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "Dev_ontStatusTable", entryPosition , "templateName").text == rTemplatename, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
            else:
                continue

    #Edith Map/ Device/ Ont Status/ Ont Dashboard
    @pytest.mark.restful
    def test_EMS1_6694_devOntInfoMapDeviceOntDashboard(self):
        self.driver.find_element(By.LINK_TEXT, "Map").click()
        WebDriverWait(self.driver, 300).until(EC.visibility_of_element_located((By.ID, "navside_icon")))
        time.sleep (3)
        self.driver.find_element(By.ID, "navside_icon").click()
        self.driver.find_element(By.XPATH, "//li[contains(.,\'" + self.dutNodeName + "\')]").click()
        time.sleep (3)
        self.driver.find_element(By.ID, "navside_icon").click()
        for ontIndex in range(self.ontCount):
            rSlot = str(self.rOntInfo[ontIndex]["slot"])
            rPort = str(self.rOntInfo[ontIndex]["port"])
            rOntid = str(self.rOntInfo[ontIndex]["ontid"])
            if self.rOntInfo[ontIndex]["ontid"] < 125:
                rSn = str(self.rOntInfo[ontIndex]["sn"])
                rPassword = str(self.rOntInfo[ontIndex]["password"])
                rActuralsn = str(self.rOntInfo[ontIndex]["acturalsn"])
                rActuralpassword = str(self.rOntInfo[ontIndex]["acturalpassword"])
                rOntstate = self.rOntInfo[ontIndex]["ontstate"]
                rModel = str(self.rOntInfo[ontIndex]["model"])
                rBootversion = self.rOntInfo[ontIndex]["bootversion"]
                rFwversiona = str(self.rOntInfo[ontIndex]["fwversiona"])
                rFwversionb = str(self.rOntInfo[ontIndex]["fwversionb"])
                rDistance = str(self.rOntInfo[ontIndex]["distance"])
                rDescription = str(self.rOntInfo[ontIndex]["description"])
                rPppoestate = self.rOntInfo[ontIndex]["pppoestate"]
                rWanip = self.rOntInfo[ontIndex]["wanip"]
                rOntrowstatus = self.rOntInfo[ontIndex]["ontrowstatus"]
                rTemplatename = str(self.rOntInfo[ontIndex]["templatename"])
                rActuralsn = str(self.rOntInfo[ontIndex]["acturalsn"])
                rActuralpassword = str(self.rOntInfo[ontIndex]["acturalpassword"])
                rWaninfo = self.rOntInfo[ontIndex]["waninfo"]
                rLaninfo = self.rOntInfo[ontIndex]["laninfo"]
                ontStatusSimple = self.ontStatusSimpleDic[rOntstate]
                ontStatus = self.ontStatusDic[rOntstate]
                if "dashboard-underborder-green" not in self.driver.find_element(By.XPATH, "//div[@id=\'ontStatus\']/div[" + ontStatusSimple + "]/div[2]").get_attribute("className"):
                    self.driver.find_element(By.XPATH, "//div[@id=\'ontStatus\']/div[" + ontStatusSimple + "]/div[2]/a").click()
                    time.sleep(3)
                getPositionByColsAndClickNext(self, "Dev_ontStatusTable", {"Slot": rSlot, "Port": rPort, "ONT": rOntid})
                p= self.driver.window_handles[0]
                c = self.driver.window_handles[1]
                self.driver.switch_to.window(c)
                if (ontIndex % 10) == 0:self.driver.refresh()
                time.sleep(3)
                with assume: assert self.driver.find_element(By.ID, "dashboard_ont_title_dev").text == self.dutName + " (" + self.dutIp + ")", f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert self.driver.find_element(By.ID, "dashboard_ont_title_slotid").text == "Slot: " + rSlot, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert self.driver.find_element(By.ID, "dashboard_ont_title_portid").text == "Port: " + rPort, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert self.driver.find_element(By.ID, "dashboard_ont_title_ontid").text == "ONT: " + rOntid, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Active Version") == self.rBootversionSimpleDic[rBootversion], f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Admin Status") == self.rOntrowstatusSimpleDic.get(rOntrowstatus, "Unknow"), f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Description") == rDescription, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Distance") == rDistance, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Model") == rModel, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Operation Status") == ontStatus, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                if ontStatus == "IS":
                    with assume: assert getAttributeValue (self, "ontStatusTable", "Password") == rActuralpassword, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getAttributeValue (self, "ontStatusTable", "SN") == rActuralsn, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                else:
                    with assume: assert getAttributeValue (self, "ontStatusTable", "Password") == rPassword, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getAttributeValue (self, "ontStatusTable", "SN") == rSn, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Template Name") == rTemplatename, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Type") == "GPON", f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Version 1") == rFwversiona, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Version 2") == rFwversionb, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                for wanIndex in range(len(rWaninfo)):
                    wanIndexStr = "WAN IP "+str(wanIndex+1)
                    with assume: assert getAttributeValue (self, "ontStatusTable", wanIndexStr) == rWaninfo[wanIndex]["ip"], f"Slot {rSlot}, Port {rPort}, Ont {rOntid}, WanIP {wanIndexStr}"
                for lanIndex in range(len(rLaninfo)):
                    if rLaninfo[lanIndex]["status"] == "link up" or rLaninfo[lanIndex]["status"] == "link down":
                        lanIndexStr = "LAN "+str(lanIndex+1)
                        rLanStatus = rLaninfo[lanIndex]["status"].upper()
                        rLanSpeed = rLaninfo[lanIndex]["speedduplex"].upper().replace("-", " ") 
                        rLanState = rLanStatus + " (" + rLanSpeed + ")" if rLanStatus != "LINK DOWN" else rLanStatus
                        with assume: assert getAttributeValue (self, "ontStatusTable", lanIndexStr).upper() == rLanState, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}, Lan {lanIndexStr}"
                self.driver.close()
                self.driver.switch_to.window(p)
            else:
                continue

    #Edith Map/ Device card/ Ont Status/ Ont Dashboard
    @pytest.mark.restful
    def test_EMS1_6695_devOntInfoMapCardOntDashboard(self):
        self.driver.find_element(By.LINK_TEXT, "Map").click()
        WebDriverWait(self.driver, 300).until(EC.visibility_of_element_located((By.ID, "navside_icon")))
        time.sleep (3)
        self.driver.find_element(By.ID, "navside_icon").click()
        self.driver.find_element(By.XPATH, "//li[contains(.,\'" + self.dutNodeName + "\')]").click()
        time.sleep (3)
        for ontIndex in range(self.ontCount):
            rSlot = self.rOntInfo[ontIndex]["slot"]
            rPort = str(self.rOntInfo[ontIndex]["port"])
            rOntid = str(self.rOntInfo[ontIndex]["ontid"])
            if self.rOntInfo[ontIndex]["ontid"] < 125:
                expandElement = self.driver.find_element(By.XPATH, "//*[@id=\'navMenuTree\']/ul/li[contains(.,\'" + self.dutNodeName + "\')]/span[contains(@class,\'expand-icon\')]")
                expandStatus = expandElement.get_attribute("class")
                if expandStatus == "icon expand-icon oi oi-plus":
                    expandElement.click()
                dutNodeId = int(self.driver.find_element(By.XPATH, "//*[@id=\'navMenuTree\']/ul/li[contains(.,\'" + self.dutNodeName + "\')]").get_attribute("data-nodeid"))
                cardNodeId = dutNodeId + rSlot
                self.driver.find_element(By.XPATH, "//*[@id=\'navMenuTree\']/ul/li[contains(@data-nodeid,\'" + str(cardNodeId) + "\')]").click()
                time.sleep (3)
                rSn = str(self.rOntInfo[ontIndex]["sn"])
                rPassword = str(self.rOntInfo[ontIndex]["password"])
                rActuralsn = str(self.rOntInfo[ontIndex]["acturalsn"])
                rActuralpassword = str(self.rOntInfo[ontIndex]["acturalpassword"])
                rOntstate = self.rOntInfo[ontIndex]["ontstate"]
                rModel = str(self.rOntInfo[ontIndex]["model"])
                rBootversion = self.rOntInfo[ontIndex]["bootversion"]
                rFwversiona = str(self.rOntInfo[ontIndex]["fwversiona"])
                rFwversionb = str(self.rOntInfo[ontIndex]["fwversionb"])
                rDistance = str(self.rOntInfo[ontIndex]["distance"])
                rDescription = str(self.rOntInfo[ontIndex]["description"])
                rPppoestate = self.rOntInfo[ontIndex]["pppoestate"]
                rWanip = self.rOntInfo[ontIndex]["wanip"]
                rOntrowstatus = self.rOntInfo[ontIndex]["ontrowstatus"]
                rTemplatename = str(self.rOntInfo[ontIndex]["templatename"])
                rActuralsn = str(self.rOntInfo[ontIndex]["acturalsn"])
                rActuralpassword = str(self.rOntInfo[ontIndex]["acturalpassword"])
                rWaninfo = self.rOntInfo[ontIndex]["waninfo"]
                rLaninfo = self.rOntInfo[ontIndex]["laninfo"]
                ontStatusSimple = self.ontStatusSimpleDic[rOntstate]
                ontStatus = self.ontStatusDic[rOntstate]
                if "dashboard-underborder-green" not in self.driver.find_element(By.XPATH, "//div[@id=\'ontStatus\']/div[" + ontStatusSimple + "]/div[2]").get_attribute("className"):
                    self.driver.find_element(By.XPATH, "//div[@id=\'ontStatus\']/div[" + ontStatusSimple + "]/div[2]/a").click()
                    time.sleep(3)
                getPositionByColsAndClickNext(self, "Slot_ontStatusTable", {"Port": rPort, "ONT": rOntid})
                p= self.driver.window_handles[0]
                c = self.driver.window_handles[1]
                self.driver.switch_to.window(c)
                if (ontIndex % 10) == 0:self.driver.refresh()
                time.sleep(3)
                with assume: assert self.driver.find_element(By.ID, "dashboard_ont_title_dev").text == self.dutName + " (" + self.dutIp + ")", f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert self.driver.find_element(By.ID, "dashboard_ont_title_slotid").text == "Slot: " + str(rSlot), f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert self.driver.find_element(By.ID, "dashboard_ont_title_portid").text == "Port: " + rPort, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert self.driver.find_element(By.ID, "dashboard_ont_title_ontid").text == "ONT: " + rOntid, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Active Version") == self.rBootversionSimpleDic[rBootversion], f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Admin Status") == self.rOntrowstatusSimpleDic.get(rOntrowstatus, "Unknow"), f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Description") == rDescription, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Distance") == rDistance, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Model") == rModel, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Operation Status") == ontStatus, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                if ontStatus == "IS":
                    with assume: assert getAttributeValue (self, "ontStatusTable", "Password") == rActuralpassword, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getAttributeValue (self, "ontStatusTable", "SN") == rActuralsn, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                else:
                    with assume: assert getAttributeValue (self, "ontStatusTable", "Password") == rPassword, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getAttributeValue (self, "ontStatusTable", "SN") == rSn, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Template Name") == rTemplatename, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Type") == "GPON", f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Version 1") == rFwversiona, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Version 2") == rFwversionb, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                for wanIndex in range(len(rWaninfo)):
                    wanIndexStr = "WAN IP "+str(wanIndex+1)
                    with assume: assert getAttributeValue (self, "ontStatusTable", wanIndexStr) == rWaninfo[wanIndex]["ip"], f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                for lanIndex in range(len(rLaninfo)):
                    if rLaninfo[lanIndex]["status"] == "link up" or rLaninfo[lanIndex]["status"] == "link down":
                        lanIndexStr = "LAN "+str(lanIndex+1)
                        rLanSpeed = rLaninfo[lanIndex]["speedduplex"].upper().replace("-", " ")
                        rLanStatus = rLaninfo[lanIndex]["status"].upper()
                        rLanState = rLanStatus + " (" + rLanSpeed + ")" if rLanStatus != "LINK DOWN" else rLanStatus
                        with assume: assert getAttributeValue (self, "ontStatusTable", lanIndexStr).upper() == rLanState, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}, Lan {lanIndexStr}"
                self.driver.close()
                self.driver.switch_to.window(p)
            else:
                continue

    #Edith Map/ Device card/ Ont Status
    @pytest.mark.restful
    def test_EMS1_6696_devOntInfoMapCard(self):
        self.driver.find_element(By.LINK_TEXT, "Map").click()
        WebDriverWait(self.driver, 300).until(EC.visibility_of_element_located((By.ID, "navside_icon")))
        time.sleep (3)
        self.driver.find_element(By.ID, "navside_icon").click()
        self.driver.find_element(By.XPATH, "//li[contains(.,\'" + self.dutNodeName + "\')]").click()
        time.sleep (3)
        for ontIndex in range(self.ontCount):
            rSlot = self.rOntInfo[ontIndex]["slot"]
            rPort = str(self.rOntInfo[ontIndex]["port"])
            rOntid = str(self.rOntInfo[ontIndex]["ontid"])
            if self.rOntInfo[ontIndex]["ontid"] < 125:
                expandElement = self.driver.find_element(By.XPATH, "//*[@id=\'navMenuTree\']/ul/li[contains(.,\'" + self.dutNodeName + "\')]/span[contains(@class,\'expand-icon\')]")
                expandStatus = expandElement.get_attribute("class")
                if expandStatus == "icon expand-icon oi oi-plus":
                    expandElement.click()
                dutNodeId = int(self.driver.find_element(By.XPATH, "//*[@id=\'navMenuTree\']/ul/li[contains(.,\'" + self.dutNodeName + "\')]").get_attribute("data-nodeid"))
                cardNodeId = dutNodeId + rSlot
                self.driver.find_element(By.XPATH, "//*[@id=\'navMenuTree\']/ul/li[contains(@data-nodeid,\'" + str(cardNodeId) + "\')]").click()
                time.sleep (3)
                rSn = self.rOntInfo[ontIndex]["sn"] if self.rOntInfo[ontIndex]["sn"] != "" else "--"
                rPassword = self.rOntInfo[ontIndex]["password"] if self.rOntInfo[ontIndex]["password"] != "" else "--"
                rActuralsn = self.rOntInfo[ontIndex]["acturalsn"]
                rActuralpassword = self.rOntInfo[ontIndex]["acturalpassword"]
                rModel = self.rOntInfo[ontIndex]["model"] if self.rOntInfo[ontIndex]["model"] != "" else "--"
                rOntrowstatus = self.rOntInfo[ontIndex]["ontrowstatus"]
                rOntstate = self.rOntInfo[ontIndex]["ontstate"]
                rDescription = self.rOntInfo[ontIndex]["description"] if self.rOntInfo[ontIndex]["description"] != "" else "--"
                rTemplatename = self.rOntInfo[ontIndex]["templatename"] if self.rOntInfo[ontIndex]["templatename"] != "" else "--"
                ontStatus = self.ontStatusSimpleDic[rOntstate]
                if "dashboard-underborder-green" not in self.driver.find_element(By.XPATH, "//div[@id=\'ontStatus\']/div[" + ontStatus + "]/div[2]").get_attribute("className"):
                    self.driver.find_element(By.XPATH, "//div[@id=\'ontStatus\']/div[" + ontStatus + "]/div[2]/a").click()
                entryPosition = getPositionByColsNext(self, "Slot_ontStatusTable", {"Port": rPort, "ONT": rOntid})
                if self.ontStatusDetailDic[rOntstate] == "In Service":
                    with assume: assert getElementByPositionCol(self, "Slot_ontStatusTable", entryPosition , "sn").text == rActuralsn, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "Slot_ontStatusTable", entryPosition , "password").text == rActuralpassword, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                else:
                    with assume: assert getElementByPositionCol(self, "Slot_ontStatusTable", entryPosition , "sn").text == rSn, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "Slot_ontStatusTable", entryPosition , "password").text == rPassword, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "Slot_ontStatusTable", entryPosition , "model").text == rModel, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "Slot_ontStatusTable", entryPosition , "OntAdminState").text == self.rOntrowstatusDic.get(rOntrowstatus, "Unknow"), f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "Slot_ontStatusTable", entryPosition , "OntOperationStatus").text == self.ontStatusDetailDic.get(rOntstate, "Unknow"), f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "Slot_ontStatusTable", entryPosition , "description").text == rDescription, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "Slot_ontStatusTable", entryPosition , "templateName").text == rTemplatename, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
            else:
                continue

    #Edith Dashboard/ Ont Status
    @pytest.mark.restful
    def test_EMS1_6697_devOntInfoDashboard(self):
        self.driver.find_element(By.LINK_TEXT, "Dashboard").click()
        WebDriverWait(self.driver, 300).until(EC.visibility_of_element_located((By.XPATH, "//div[@id=\'dashboard_net_title\']")))
        time.sleep (3)
        self.driver.find_element(By.XPATH, "//div[@id=\'ontStatus\']/div[1]/div[2]/a").click()
        self.driver.find_element(By.CSS_SELECTOR, ".comboTreeArrowBtnImg").click()
        time.sleep (3)
        self.driver.find_element(By.XPATH, "//label[contains(.,\'" + self.dutNodeName + "\')]/parent::li").click()
        time.sleep (3)
        for ontIndex in range(self.ontCount):
            rSlot = str(self.rOntInfo[ontIndex]["slot"])
            rPort = str(self.rOntInfo[ontIndex]["port"])
            rOntid = str(self.rOntInfo[ontIndex]["ontid"])
            if self.rOntInfo[ontIndex]["ontid"] < 125:
                rSn = self.rOntInfo[ontIndex]["sn"] if self.rOntInfo[ontIndex]["sn"] != "" else "--"
                rPassword = self.rOntInfo[ontIndex]["password"] if self.rOntInfo[ontIndex]["password"] != "" else "--"
                rActuralsn = self.rOntInfo[ontIndex]["acturalsn"]
                rActuralpassword = self.rOntInfo[ontIndex]["acturalpassword"]
                rModel = self.rOntInfo[ontIndex]["model"] if self.rOntInfo[ontIndex]["model"] != "" else "--"
                rOntrowstatus = self.rOntInfo[ontIndex]["ontrowstatus"]
                rOntstate = self.rOntInfo[ontIndex]["ontstate"]
                rDescription = self.rOntInfo[ontIndex]["description"] if self.rOntInfo[ontIndex]["description"] != "" else "--"
                rTemplatename = self.rOntInfo[ontIndex]["templatename"] if self.rOntInfo[ontIndex]["templatename"] != "" else "--"
                ontStatus = self.ontStatusSimpleDic[rOntstate]
                if "dashboard-underborder-green" not in self.driver.find_element(By.XPATH, "//div[@id=\'ontStatus\']/div[" + ontStatus + "]/div[2]").get_attribute("className"):
                    self.driver.find_element(By.XPATH, "//div[@id=\'ontStatus\']/div[" + ontStatus + "]/div[2]/a").click()
                    self.driver.find_element(By.CSS_SELECTOR, ".comboTreeArrowBtnImg").click()
                    time.sleep (3)
                    self.driver.find_element(By.XPATH, "//label[contains(.,\'" + self.dutNodeName + "\')]/parent::li").click()
                    time.sleep (3)
                entryPosition = getPositionByColsNext(self, "All_ontStatusTable", {"Slot": rSlot, "Port": rPort, "ONT": rOntid})
                if self.ontStatusDetailDic[rOntstate] == "In Service":
                    with assume: assert getElementByPositionCol(self, "All_ontStatusTable", entryPosition , "sn").text == rActuralsn, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "All_ontStatusTable", entryPosition , "password").text == rActuralpassword, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                else:
                    with assume: assert getElementByPositionCol(self, "All_ontStatusTable", entryPosition , "sn").text == rSn, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "All_ontStatusTable", entryPosition , "password").text == rPassword, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "All_ontStatusTable", entryPosition , "model").text == rModel, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "All_ontStatusTable", entryPosition , "OntAdminState").text == self.rOntrowstatusDic.get(rOntrowstatus, "Unknow"), f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "All_ontStatusTable", entryPosition , "OntOperationStatus").text == self.ontStatusDetailDic.get(rOntstate, "Unknow"), f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "All_ontStatusTable", entryPosition , "description").text == rDescription, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "All_ontStatusTable", entryPosition , "templateName").text == rTemplatename, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
            else:
                continue

    #Edith Dashboard/ Ont Status/ Ont Dashboard
    @pytest.mark.restful
    def test_EMS1_6698_devOntInfoDashboardOntDashboard(self):
        self.driver.find_element(By.LINK_TEXT, "Dashboard").click()
        WebDriverWait(self.driver, 300).until(EC.visibility_of_element_located((By.XPATH, "//div[@id=\'dashboard_net_title\']")))
        time.sleep (3)
        self.driver.find_element(By.XPATH, "//div[@id=\'ontStatus\']/div[1]/div[2]/a").click()
        self.driver.find_element(By.CSS_SELECTOR, ".comboTreeArrowBtnImg").click()
        time.sleep (3)
        self.driver.find_element(By.XPATH, "//label[contains(.,\'" + self.dutNodeName + "\')]/parent::li").click()
        time.sleep (3)
        for ontIndex in range(self.ontCount):
            rSlot = str(self.rOntInfo[ontIndex]["slot"])
            rPort = str(self.rOntInfo[ontIndex]["port"])
            rOntid = str(self.rOntInfo[ontIndex]["ontid"])
            if self.rOntInfo[ontIndex]["ontid"] < 125:
                rSn = str(self.rOntInfo[ontIndex]["sn"])
                rPassword = str(self.rOntInfo[ontIndex]["password"])
                rActuralsn = str(self.rOntInfo[ontIndex]["acturalsn"])
                rActuralpassword = str(self.rOntInfo[ontIndex]["acturalpassword"])
                rOntstate = self.rOntInfo[ontIndex]["ontstate"]
                rModel = str(self.rOntInfo[ontIndex]["model"])
                rBootversion = self.rOntInfo[ontIndex]["bootversion"]
                rFwversiona = str(self.rOntInfo[ontIndex]["fwversiona"])
                rFwversionb = str(self.rOntInfo[ontIndex]["fwversionb"])
                rDistance = str(self.rOntInfo[ontIndex]["distance"])
                rDescription = str(self.rOntInfo[ontIndex]["description"])
                rPppoestate = self.rOntInfo[ontIndex]["pppoestate"]
                rWanip = self.rOntInfo[ontIndex]["wanip"]
                rOntrowstatus = self.rOntInfo[ontIndex]["ontrowstatus"]
                rTemplatename = str(self.rOntInfo[ontIndex]["templatename"])
                rActuralsn = str(self.rOntInfo[ontIndex]["acturalsn"])
                rActuralpassword = str(self.rOntInfo[ontIndex]["acturalpassword"])
                rWaninfo = self.rOntInfo[ontIndex]["waninfo"]
                rLaninfo = self.rOntInfo[ontIndex]["laninfo"]
                ontStatusSimple = self.ontStatusSimpleDic[rOntstate]
                ontStatus = self.ontStatusDic[rOntstate]
                if "dashboard-underborder-green" not in self.driver.find_element(By.XPATH, "//div[@id=\'ontStatus\']/div[" + ontStatusSimple + "]/div[2]").get_attribute("className"):
                    self.driver.find_element(By.XPATH, "//div[@id=\'ontStatus\']/div[" + ontStatusSimple + "]/div[2]/a").click()
                    self.driver.find_element(By.CSS_SELECTOR, ".comboTreeArrowBtnImg").click()
                    time.sleep(3)
                    self.driver.find_element(By.XPATH, "//label[contains(.,\'" + self.dutNodeName + "\')]/parent::li").click()
                    time.sleep(3)
                getPositionByColsAndClickNext(self, "All_ontStatusTable", {"Slot": rSlot, "Port": rPort, "ONT": rOntid})
                p= self.driver.window_handles[0]
                c = self.driver.window_handles[1]
                self.driver.switch_to.window(c)
                if (ontIndex % 10) == 0: self.driver.refresh()
                time.sleep(3)
                with assume: assert self.driver.find_element(By.ID, "dashboard_ont_title_dev").text == self.dutName + " (" + self.dutIp + ")", f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert self.driver.find_element(By.ID, "dashboard_ont_title_slotid").text == "Slot: " + str(rSlot), f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert self.driver.find_element(By.ID, "dashboard_ont_title_portid").text == "Port: " + rPort, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert self.driver.find_element(By.ID, "dashboard_ont_title_ontid").text == "ONT: " + rOntid, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Active Version") == self.rBootversionSimpleDic[rBootversion], f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Admin Status") == self.rOntrowstatusSimpleDic.get(rOntrowstatus, "Unknow"), f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Description") == rDescription, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Distance") == rDistance, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Model") == rModel, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Operation Status") == ontStatus, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                if ontStatus == "IS":
                    with assume: assert getAttributeValue (self, "ontStatusTable", "Password") == rActuralpassword, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getAttributeValue (self, "ontStatusTable", "SN") == rActuralsn, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                else:
                    with assume: assert getAttributeValue (self, "ontStatusTable", "Password") == rPassword, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getAttributeValue (self, "ontStatusTable", "SN") == rSn, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Template Name") == rTemplatename, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Type") == "GPON", f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Version 1") == rFwversiona, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Version 2") == rFwversionb, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                for wanIndex in range(len(rWaninfo)):
                    wanIndexStr = "WAN IP "+str(wanIndex+1)
                    with assume: assert getAttributeValue (self, "ontStatusTable", wanIndexStr) == rWaninfo[wanIndex]["ip"], f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                for lanIndex in range(len(rLaninfo)):
                    if rLaninfo[lanIndex]["status"] == "link up" or rLaninfo[lanIndex]["status"] == "link down":
                        lanIndexStr = "LAN "+str(lanIndex+1)
                        rLanSpeed = rLaninfo[lanIndex]["speedduplex"].upper().replace("-", " ")
                        rLanStatus = rLaninfo[lanIndex]["status"].upper()
                        rLanState = rLanStatus + " (" + rLanSpeed + ")" if rLaninfo[lanIndex]["status"] != "link down" else rLanStatus
                        with assume: assert getAttributeValue (self, "ontStatusTable", lanIndexStr).upper() == rLanState, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}, Lan {lanIndexStr}"
                self.driver.close()
                self.driver.switch_to.window(p)
            else:
                continue

    #Edith Inventory/ Ont/ All Ont
    @pytest.mark.restful
    def test_EMS1_6699_devXontInfoInventoryAllOnt(self):
        self.driver.find_element(By.LINK_TEXT, "Inventory").click()
        WebDriverWait(self.driver, 300).until(EC.visibility_of_element_located((By.LINK_TEXT, "ONT")))
        time.sleep (3)
        self.driver.find_element(By.LINK_TEXT, "ONT").click()
        self.driver.find_element(By.CSS_SELECTOR, "#i_action_refresh > a").click()
        rPortOld = 0
        rSlotOld = 0
        for ontIndex in range(self.xontCount):
            rSlot = self.rXontInfo[ontIndex]["slot"]
            rPort = self.rXontInfo[ontIndex]["port"]
            rOntid = ""
            rSn = self.rXontInfo[ontIndex]["sn"] if self.rXontInfo[ontIndex]["sn"] != "" else "--"
            rPassword = self.rXontInfo[ontIndex]["password"] if self.rXontInfo[ontIndex]["password"] != "" else "--"
            rOntstate = self.rXontInfo[ontIndex]["ontstate"]
            if rPortOld != rPort or rSlotOld != rSlot:
                self.driver.find_element(By.CSS_SELECTOR, "#i_action_filter > a").click()
                self.driver.find_element(By.ID, "inventory_allont_clear_btn").click()
                self.driver.find_element(By.ID, "ip_Allont").send_keys(self.dutIp)
                self.driver.find_element(By.ID, "slot_Allont").send_keys(rSlot)
                self.driver.find_element(By.ID, "port_Allont").send_keys(rPort)
                self.driver.find_element(By.ID, "inventory_allont_btn").click()
                time.sleep (3)
            rPortOld = rPort
            rSlotOld = rSlot
            if self.rXontInfo[ontIndex]["ontid"] > 1000:
                rOntid = "Unregistered"
                entryPosition = getPositionByColsAndClickNext(self, "ont_inventory_div", {"sn": rSn})
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "Slot").text == str(rSlot), f"Slot {rSlot}, Port {rPort}, SN {rSn}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "Port").text == str(rPort), f"Slot {rSlot}, Port {rPort}, SN {rSn}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "ONT").text == rOntid, f"Slot {rSlot}, Port {rPort}, SN {rSn}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "sn").text == rSn, f"Slot {rSlot}, Port {rPort}, SN {rSn}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "password").text == rPassword, f"Slot {rSlot}, Port {rPort}, SN {rSn}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "OntOperationStatus").text == "Unknown", f"Slot {rSlot}, Port {rPort}, SN {rSn}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "model").text == "", f"Slot {rSlot}, Port {rPort}, SN {rSn}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "activeVersion").text == "--", f"Slot {rSlot}, Port {rPort}, SN {rSn}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "versionA").text == "", f"Slot {rSlot}, Port {rPort}, SN {rSn}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "versionB").text == "", f"Slot {rSlot}, Port {rPort}, SN {rSn}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "ontDistance").text == "0", f"Slot {rSlot}, Port {rPort}, SN {rSn}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "description").text == "", f"Slot {rSlot}, Port {rPort}, SN {rSn}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "OntAdminState").text == "Unknown", f"Slot {rSlot}, Port {rPort}, SN {rSn}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "templateName").text == "", f"Slot {rSlot}, Port {rPort}, SN {rSn}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "txPower").text == "--", f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "rxPower").text == "--", f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "ONTType").text == "--", f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
            else:
                rOntid = str(self.rXontInfo[ontIndex]["ontid"])
                entryPosition = getPositionByColNext(self, "ont_inventory_div", "ONT", rOntid)
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "Slot").text == str(rSlot), f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "Port").text == str(rPort), f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "ONT").text == rOntid, f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                rOnttype = self.rXontInfo[ontIndex]["onttype"]
                rVendorid = self.rXontInfo[ontIndex]["vendorid"]
                rVendorversion = self.rXontInfo[ontIndex]["vendorversion"] if self.rXontInfo[ontIndex]["vendorversion"] != "" else "--"
                rBootversion = self.rXontInfo[ontIndex]["bootversion"]
                rFwversiona = self.rXontInfo[ontIndex]["fwversiona"] if self.rXontInfo[ontIndex]["fwversiona"] != "" else "--"
                rFwversionb = self.rXontInfo[ontIndex]["fwversionb"] if self.rXontInfo[ontIndex]["fwversionb"] != "" else "--"
                rDistance = self.rXontInfo[ontIndex]["distance"]
                rOntrowstatus = self.rXontInfo[ontIndex]["ontrowstatus"]
                rTemplatename = self.rXontInfo[ontIndex]["templatename"]if self.rXontInfo[ontIndex]["templatename"] != "" else "--"
                rActuralsn = self.rXontInfo[ontIndex]["acturalsn"]
                rActuralpassword = self.rXontInfo[ontIndex]["acturalpassword"]
                rDescription = self.rXontInfo[ontIndex]["description"] if self.rXontInfo[ontIndex]["description"] != "" else "--"
                rTxpower = self.rXontInfo[ontIndex]["txpower"] if self.rXontInfo[ontIndex]["txpower"] != "" else "--"
                rRxpower = self.rXontInfo[ontIndex]["rxpower"] if self.rXontInfo[ontIndex]["rxpower"] != "" else "--"
                rWaninfo = self.rXontInfo[ontIndex]["waninfo"]
                if self.ontStatusDetailDic[rOntstate] == "In Service":
                    with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "sn").text == rActuralsn, f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                    with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "password").text == rActuralpassword, f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                    if rTxpower != "--" or rTxpower != "N/A" or rTxpower != "0.00":
                        rTxpowerFloat = float(rTxpower)
                        txRowerFloat = float(getElementByPositionCol(self, "ont_inventory_div", entryPosition , "txPower").text)
                        with assume: assert rTxpowerFloat-0.99 <= txRowerFloat <= rTxpowerFloat+0.99
                    else:
                        with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "txPower").text == rTxpower, f"Slot {rSlot}, Port {rPort}"
                    if rRxpower != "--" or rRxpower != "N/A" or rRxpower != "0.00":
                        rRxpowerFloat = float(rRxpower)
                        rxRowerFloat = float(getElementByPositionCol(self, "ont_inventory_div", entryPosition , "rxPower").text)
                        with assume: assert rRxpowerFloat-0.99 <= rxRowerFloat <= rRxpowerFloat+0.99
                    else:
                        with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "rxPower").text == rRxpower, f"Slot {rSlot}, Port {rPort}"
                else:
                    with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "sn").text == rSn, f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                    with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "password").text == rPassword, f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                    #with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "txPower").text == "--", f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                    with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "txPower").text == rTxpower, f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                    #with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "rxPower").text == "--", f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"                
                    with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "rxPower").text == rRxpower, f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"                
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "OntOperationStatus").text == self.ontStatusDetailDic.get(rOntstate, "Unknow"), f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "model").text == rVendorversion, f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "OntAdminState").text == self.rOntrowstatusDic.get(rOntrowstatus, "Unknow"), f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "activeVersion").text == self.rBootversionDic.get(rBootversion, "--"), f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "versionA").text == rFwversiona, f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "versionB").text == rFwversionb, f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "ontDistance").text == str(rDistance), f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "description").text == rDescription, f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "templateName").text == rTemplatename, f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"
                with assume: assert getElementByPositionCol(self, "ont_inventory_div", entryPosition , "ONTType").text == rOnttype.upper(), f"Slot {rSlot}, Port {rPort}, ONT {rOntid}"

    #Edith Map/ Device/ Ont Status
    @pytest.mark.restful
    def test_EMS1_6700_devXontInfoMapDevice(self):
        self.driver.find_element(By.LINK_TEXT, "Map").click()
        WebDriverWait(self.driver, 300).until(EC.visibility_of_element_located((By.ID, "navside_icon")))
        time.sleep (3)
        self.driver.find_element(By.ID, "navside_icon").click()
        self.driver.find_element(By.XPATH, "//li[contains(.,\'" + self.dutNodeName + "\')]").click()
        time.sleep (3)
        self.driver.find_element(By.ID, "navside_icon").click()
        for ontIndex in range(self.xontCount):
            rSlot = self.rXontInfo[ontIndex]["slot"]
            rPort = self.rXontInfo[ontIndex]["port"]
            rOntid = self.rXontInfo[ontIndex]["ontid"]
            if rOntid> 1000:
                continue
            else:
                rSn = self.rXontInfo[ontIndex]["sn"] if self.rXontInfo[ontIndex]["sn"] != "" else "--"
                print("rSn = " + rSn )
                rPassword = self.rXontInfo[ontIndex]["password"] if self.rXontInfo[ontIndex]["password"] != "" else "--"
                rActuralsn = self.rXontInfo[ontIndex]["acturalsn"]
                rActuralpassword = self.rXontInfo[ontIndex]["acturalpassword"]
                rVendorversion = self.rXontInfo[ontIndex]["vendorversion"] if self.rXontInfo[ontIndex]["vendorversion"] != "" else "--"
                rOntrowstatus = self.rXontInfo[ontIndex]["ontrowstatus"]
                rOntstate = self.rXontInfo[ontIndex]["ontstate"]
                rDescription = self.rXontInfo[ontIndex]["description"] if self.rXontInfo[ontIndex]["description"] != "" else "--"
                rTemplatename = self.rXontInfo[ontIndex]["templatename"] if self.rXontInfo[ontIndex]["templatename"] != "" else "--"
                ontStatus = self.ontStatusSimpleDic[rOntstate]
                if "dashboard-underborder-green" not in self.driver.find_element(By.XPATH, "//div[@id=\'ontStatus\']/div[" + ontStatus + "]/div[2]").get_attribute("className"):
                    self.driver.find_element(By.XPATH, "//div[@id=\'ontStatus\']/div[" + ontStatus + "]/div[2]/a").click()
                entryPosition = getPositionByColsNext(self, "Dev_ontStatusTable", {"Slot": str(rSlot), "Port": str(rPort), "ONT": str(rOntid)})
                if self.ontStatusDetailDic[rOntstate] == "In Service":
                    with assume: assert getElementByPositionCol(self, "Dev_ontStatusTable", entryPosition , "sn").text == rActuralsn, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "Dev_ontStatusTable", entryPosition , "password").text == rActuralpassword, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                else:
                    with assume: assert getElementByPositionCol(self, "Dev_ontStatusTable", entryPosition , "sn").text == rSn, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "Dev_ontStatusTable", entryPosition , "password").text == rPassword, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "Dev_ontStatusTable", entryPosition , "model").text == rVendorversion, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "Dev_ontStatusTable", entryPosition , "OntAdminState").text == self.rOntrowstatusDic.get(rOntrowstatus, "Unknow"), f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "Dev_ontStatusTable", entryPosition , "OntOperationStatus").text == self.ontStatusDetailDic.get(rOntstate, "Unknow"), f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "Dev_ontStatusTable", entryPosition , "description").text == rDescription, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "Dev_ontStatusTable", entryPosition , "templateName").text == rTemplatename, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"

    #Edith Map/ Device/ Ont Status/ Ont Dashboard
    @pytest.mark.restful
    def test_EMS1_6701_devXontInfoMapDeviceOntDashboard(self):
        self.driver.find_element(By.LINK_TEXT, "Map").click()
        WebDriverWait(self.driver, 300).until(EC.visibility_of_element_located((By.ID, "navside_icon")))
        time.sleep (3)
        self.driver.find_element(By.ID, "navside_icon").click()
        self.driver.find_element(By.XPATH, "//li[contains(.,\'" + self.dutNodeName + "\')]").click()
        time.sleep (3)
        self.driver.find_element(By.ID, "navside_icon").click()
        for ontIndex in range(self.xontCount):
            rSlot = str(self.rXontInfo[ontIndex]["slot"])
            rPort = str(self.rXontInfo[ontIndex]["port"])
            rOntid = self.rXontInfo[ontIndex]["ontid"]
            if rOntid> 1000:
                continue
            else:
                rOnttype = self.rXontInfo[ontIndex]["onttype"]
                rSn = str(self.rXontInfo[ontIndex]["sn"])
                rPassword = str(self.rXontInfo[ontIndex]["password"])
                rActuralsn = str(self.rXontInfo[ontIndex]["acturalsn"])
                rActuralpassword = str(self.rXontInfo[ontIndex]["acturalpassword"])
                rOntstate = self.rXontInfo[ontIndex]["ontstate"]
                rVendorversion = str(self.rXontInfo[ontIndex]["vendorversion"])
                rBootversion = self.rXontInfo[ontIndex]["bootversion"]
                rFwversiona = str(self.rXontInfo[ontIndex]["fwversiona"])
                rFwversionb = str(self.rXontInfo[ontIndex]["fwversionb"])
                rDistance = str(self.rXontInfo[ontIndex]["distance"])
                rDescription = str(self.rXontInfo[ontIndex]["description"])
                rOntrowstatus = self.rXontInfo[ontIndex]["ontrowstatus"]
                rTemplatename = str(self.rXontInfo[ontIndex]["templatename"])
                rActuralsn = str(self.rXontInfo[ontIndex]["acturalsn"])
                rActuralpassword = str(self.rXontInfo[ontIndex]["acturalpassword"])
                rWaninfo = self.rXontInfo[ontIndex]["waninfo"]
                rLaninfo = self.rXontInfo[ontIndex]["laninfo"]
                rXLaninfo = self.rXontInfo[ontIndex]["xlaninfo"]
                ontStatusSimple = self.ontStatusSimpleDic[rOntstate]
                ontStatus = self.ontStatusDic[rOntstate]
                if "dashboard-underborder-green" not in self.driver.find_element(By.XPATH, "//div[@id=\'ontStatus\']/div[" + ontStatusSimple + "]/div[2]").get_attribute("className"):
                    self.driver.find_element(By.XPATH, "//div[@id=\'ontStatus\']/div[" + ontStatusSimple + "]/div[2]/a").click()
                    time.sleep(3)
                getPositionByColsAndClickNext(self, "Dev_ontStatusTable", {"Slot": rSlot, "Port": rPort, "ONT": str(rOntid)})
                p= self.driver.window_handles[0]
                c = self.driver.window_handles[1]
                self.driver.switch_to.window(c)
                if (ontIndex % 10) == 0: self.driver.refresh()
                time.sleep(3)
                with assume: assert self.driver.find_element(By.ID, "dashboard_ont_title_dev").text == self.dutName + " (" + self.dutIp + ")", f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert self.driver.find_element(By.ID, "dashboard_ont_title_slotid").text == "Slot: " + rSlot, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert self.driver.find_element(By.ID, "dashboard_ont_title_portid").text == "Port: " + rPort, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert self.driver.find_element(By.ID, "dashboard_ont_title_ontid").text == "ONT: " + str(rOntid), f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Active Version") == self.rBootversionSimpleDic[rBootversion], f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Admin Status") == self.rOntrowstatusSimpleDic.get(rOntrowstatus, "Unknow"), f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Description") == rDescription, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Distance") == rDistance, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Model") == rVendorversion, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Operation Status") == ontStatus, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                if ontStatus == "IS":
                    with assume: assert getAttributeValue (self, "ontStatusTable", "Password") == rActuralpassword, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getAttributeValue (self, "ontStatusTable", "SN") == rActuralsn, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                else:
                    with assume: assert getAttributeValue (self, "ontStatusTable", "Password") == rPassword, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getAttributeValue (self, "ontStatusTable", "SN") == rSn, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Template Name") == rTemplatename, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Type") == rOnttype.upper(), f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Version 1") == rFwversiona, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Version 2") == rFwversionb, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                for wanIndex in range(len(rWaninfo)):
                    wanIndexStr = "WAN IP "+str(wanIndex+1)
                    with assume: assert getAttributeValue (self, "ontStatusTable", wanIndexStr) == rWaninfo[wanIndex]["ip"], f"Slot {rSlot}, Port {rPort}, Ont {rOntid}, {wanIndexStr}"
                for lanIndex in range(len(rLaninfo)):
                    if rLaninfo[lanIndex]["status"] == "link up" or rLaninfo[lanIndex]["status"] == "link down":
                        lanIndexStr = "LAN "+str(lanIndex+1)
                        rLanSpeed = rLaninfo[lanIndex]["speedduplex"].upper().replace("-", " ")
                        rLanStatus = rLaninfo[lanIndex]["status"].upper()
                        rLanState = rLanStatus + " (" + rLanSpeed + ")" if rLaninfo[lanIndex]["status"] != "link down" else rLanStatus
                        with assume: assert getAttributeValue (self, "ontStatusTable", lanIndexStr).upper() == rLanState, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}, Lan {lanIndexStr}"
                for lanIndex in range(len(rXLaninfo)):
                    if rXLaninfo[lanIndex]["status"] == "link up" or rXLaninfo[lanIndex]["status"] == "link down":
                        lanIndexStr = "XLAN "+str(lanIndex+1)
                        rLanSpeed = rXLaninfo[lanIndex]["speedduplex"].upper().replace("-", " ")
                        rLanStatus = rXLaninfo[lanIndex]["status"].upper()
                        rLanState = rLanStatus + " (" + rLanSpeed + ")" if rXLaninfo[lanIndex]["status"] != "link down" else rLanStatus
                        with assume: assert getAttributeValue (self, "ontStatusTable", lanIndexStr).upper() == rLanState, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}, Lan {lanIndexStr}"                
                self.driver.close()
                self.driver.switch_to.window(p)


    #Edith Map/ Device card/ Ont Status/ Ont Dashboard
    @pytest.mark.restful
    def test_EMS1_6702_devXontInfoMapCardOntDashboard(self):
        self.driver.find_element(By.LINK_TEXT, "Map").click()
        WebDriverWait(self.driver, 300).until(EC.visibility_of_element_located((By.ID, "navside_icon")))
        time.sleep (3)
        self.driver.find_element(By.ID, "navside_icon").click()
        self.driver.find_element(By.XPATH, "//li[contains(.,\'" + self.dutNodeName + "\')]").click()
        time.sleep (3)
        for ontIndex in range(self.xontCount):
            rSlot = self.rXontInfo[ontIndex]["slot"]
            rPort = str(self.rXontInfo[ontIndex]["port"])
            rOntid = self.rXontInfo[ontIndex]["ontid"]
            expandElement = self.driver.find_element(By.XPATH, "//*[@id=\'navMenuTree\']/ul/li[contains(.,\'" + self.dutNodeName + "\')]/span[contains(@class,\'expand-icon\')]")
            expandStatus = expandElement.get_attribute("class")
            if expandStatus == "icon expand-icon oi oi-plus":
                expandElement.click()
            dutNodeId = int(self.driver.find_element(By.XPATH, "//*[@id=\'navMenuTree\']/ul/li[contains(.,\'" + self.dutNodeName + "\')]").get_attribute("data-nodeid"))
            cardNodeId = dutNodeId + rSlot
            self.driver.find_element(By.XPATH, "//*[@id=\'navMenuTree\']/ul/li[contains(@data-nodeid,\'" + str(cardNodeId) + "\')]").click()
            time.sleep (3)
            if rOntid> 1000:
                continue
            else:
                rOnttype = self.rXontInfo[ontIndex]["onttype"]
                rSn = str(self.rXontInfo[ontIndex]["sn"])
                rPassword = str(self.rXontInfo[ontIndex]["password"])
                rActuralsn = str(self.rXontInfo[ontIndex]["acturalsn"])
                rActuralpassword = str(self.rXontInfo[ontIndex]["acturalpassword"])
                rOntstate = self.rXontInfo[ontIndex]["ontstate"]
                rVendorversion = str(self.rXontInfo[ontIndex]["vendorversion"])
                rBootversion = self.rXontInfo[ontIndex]["bootversion"]
                rFwversiona = str(self.rXontInfo[ontIndex]["fwversiona"])
                rFwversionb = str(self.rXontInfo[ontIndex]["fwversionb"])
                rDistance = str(self.rXontInfo[ontIndex]["distance"])
                rDescription = str(self.rXontInfo[ontIndex]["description"])
                rOntrowstatus = self.rXontInfo[ontIndex]["ontrowstatus"]
                rTemplatename = str(self.rXontInfo[ontIndex]["templatename"])
                rOnttype = self.rXontInfo[ontIndex]["onttype"]
                rActuralsn = str(self.rXontInfo[ontIndex]["acturalsn"])
                rActuralpassword = str(self.rXontInfo[ontIndex]["acturalpassword"])
                rWaninfo = self.rXontInfo[ontIndex]["waninfo"]
                rLaninfo = self.rXontInfo[ontIndex]["laninfo"]
                rXLaninfo = self.rXontInfo[ontIndex]["xlaninfo"]
                ontStatusSimple = self.ontStatusSimpleDic[rOntstate]
                ontStatus = self.ontStatusDic[rOntstate]
                if "dashboard-underborder-green" not in self.driver.find_element(By.XPATH, "//div[@id=\'ontStatus\']/div[" + ontStatusSimple + "]/div[2]").get_attribute("className"):
                    self.driver.find_element(By.XPATH, "//div[@id=\'ontStatus\']/div[" + ontStatusSimple + "]/div[2]/a").click()
                    time.sleep(3)
                getPositionByColsAndClickNext(self, "Slot_ontStatusTable", {"Port": rPort, "ONT": str(rOntid)})
                p= self.driver.window_handles[0]
                c = self.driver.window_handles[1]
                self.driver.switch_to.window(c)
                if (ontIndex % 10) == 0: self.driver.refresh()
                time.sleep(3)
                with assume: assert self.driver.find_element(By.ID, "dashboard_ont_title_dev").text == self.dutName + " (" + self.dutIp + ")", f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert self.driver.find_element(By.ID, "dashboard_ont_title_slotid").text == "Slot: " + str(rSlot), f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert self.driver.find_element(By.ID, "dashboard_ont_title_portid").text == "Port: " + rPort, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert self.driver.find_element(By.ID, "dashboard_ont_title_ontid").text == "ONT: " + str(rOntid), f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Active Version") == self.rBootversionSimpleDic[rBootversion], f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Admin Status") == self.rOntrowstatusSimpleDic.get(rOntrowstatus, "Unknow"), f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Description") == rDescription, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Distance") == rDistance, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Model") == rVendorversion, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Operation Status") == ontStatus, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                if ontStatus == "IS":
                    with assume: assert getAttributeValue (self, "ontStatusTable", "Password") == rActuralpassword, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getAttributeValue (self, "ontStatusTable", "SN") == rActuralsn, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                else:
                    with assume: assert getAttributeValue (self, "ontStatusTable", "Password") == rPassword, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getAttributeValue (self, "ontStatusTable", "SN") == rSn, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Template Name") == rTemplatename, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Type") == rOnttype.upper(), f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Version 1") == rFwversiona, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Version 2") == rFwversionb, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                for wanIndex in range(len(rWaninfo)):
                    wanIndexStr = "WAN IP "+str(wanIndex+1)
                    with assume: assert getAttributeValue (self, "ontStatusTable", wanIndexStr) == rWaninfo[wanIndex]["ip"], f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                for lanIndex in range(len(rLaninfo)):
                    if rLaninfo[lanIndex]["status"] == "link up" or rLaninfo[lanIndex]["status"] == "link down":
                        lanIndexStr = "LAN "+str(lanIndex+1)
                        rLanSpeed = rLaninfo[lanIndex]["speedduplex"].upper().replace("-", " ")
                        rLanStatus = rLaninfo[lanIndex]["status"].upper()
                        rLanState = rLanStatus + " (" + rLanSpeed + ")" if rLaninfo[lanIndex]["status"] != "link down" else rLanStatus
                        with assume: assert getAttributeValue (self, "ontStatusTable", lanIndexStr).upper() == rLanState, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}, Lan {lanIndexStr}"
                for lanIndex in range(len(rXLaninfo)):
                    if rXLaninfo[lanIndex]["status"] == "link up" or rXLaninfo[lanIndex]["status"] == "link down":
                        lanIndexStr = "XLAN "+str(lanIndex+1)
                        rLanSpeed = rXLaninfo[lanIndex]["speedduplex"].upper().replace("-", " ")
                        rLanStatus = rXLaninfo[lanIndex]["status"].upper()
                        rLanState = rLanStatus + " (" + rLanSpeed + ")" if rXLaninfo[lanIndex]["status"] != "link down" else rLanStatus
                        with assume: assert getAttributeValue (self, "ontStatusTable", lanIndexStr).upper() == rLanState, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}, Lan {lanIndexStr}"  
                self.driver.close()
                self.driver.switch_to.window(p)

    #Edith Map/ Device/ Ont Status
    @pytest.mark.restful
    def test_EMS1_6703_devXontInfoMapCard(self):
        self.driver.find_element(By.LINK_TEXT, "Map").click()
        WebDriverWait(self.driver, 300).until(EC.visibility_of_element_located((By.ID, "navside_icon")))
        time.sleep (3)
        self.driver.find_element(By.ID, "navside_icon").click()
        self.driver.find_element(By.XPATH, "//li[contains(.,\'" + self.dutNodeName + "\')]").click()
        time.sleep (3)
        for ontIndex in range(self.xontCount):
            rSlot = self.rXontInfo[ontIndex]["slot"]
            rPort = str(self.rXontInfo[ontIndex]["port"])
            rOntid = self.rXontInfo[ontIndex]["ontid"]
            expandElement = self.driver.find_element(By.XPATH, "//*[@id=\'navMenuTree\']/ul/li[contains(.,\'" + self.dutNodeName + "\')]/span[contains(@class,\'expand-icon\')]")
            expandStatus = expandElement.get_attribute("class")
            if expandStatus == "icon expand-icon oi oi-plus":
                expandElement.click()
            dutNodeId = int(self.driver.find_element(By.XPATH, "//*[@id=\'navMenuTree\']/ul/li[contains(.,\'" + self.dutNodeName + "\')]").get_attribute("data-nodeid"))
            cardNodeId = dutNodeId + rSlot
            self.driver.find_element(By.XPATH, "//*[@id=\'navMenuTree\']/ul/li[contains(@data-nodeid,\'" + str(cardNodeId) + "\')]").click()
            time.sleep (3)
            if rOntid> 1000:
                continue
            else:
                rSn = self.rXontInfo[ontIndex]["sn"] if self.rXontInfo[ontIndex]["sn"] != "" else "--"
                rPassword = self.rXontInfo[ontIndex]["password"] if self.rXontInfo[ontIndex]["password"] != "" else "--"
                rActuralsn = self.rXontInfo[ontIndex]["acturalsn"]
                rActuralpassword = self.rXontInfo[ontIndex]["acturalpassword"]
                rVendorversion = self.rXontInfo[ontIndex]["vendorversion"] if self.rXontInfo[ontIndex]["vendorversion"] != "" else "--"
                rOntrowstatus = self.rXontInfo[ontIndex]["ontrowstatus"]
                rOntstate = self.rXontInfo[ontIndex]["ontstate"]
                rDescription = self.rXontInfo[ontIndex]["description"] if self.rXontInfo[ontIndex]["description"] != "" else "--"
                rTemplatename = self.rXontInfo[ontIndex]["templatename"] if self.rXontInfo[ontIndex]["templatename"] != "" else "--"
                ontStatus = self.ontStatusSimpleDic[rOntstate]
                if "dashboard-underborder-green" not in self.driver.find_element(By.XPATH, "//div[@id=\'ontStatus\']/div[" + ontStatus + "]/div[2]").get_attribute("className"):
                    self.driver.find_element(By.XPATH, "//div[@id=\'ontStatus\']/div[" + ontStatus + "]/div[2]/a").click()
                entryPosition = getPositionByColsNext(self, "Slot_ontStatusTable", {"Port": rPort, "ONT": str(rOntid)})
                if self.ontStatusDetailDic[rOntstate] == "In Service":
                    with assume: assert getElementByPositionCol(self, "Slot_ontStatusTable", entryPosition , "sn").text == rActuralsn, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "Slot_ontStatusTable", entryPosition , "password").text == rActuralpassword, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                else:
                    with assume: assert getElementByPositionCol(self, "Slot_ontStatusTable", entryPosition , "sn").text == rSn, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "Slot_ontStatusTable", entryPosition , "password").text == rPassword, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "Slot_ontStatusTable", entryPosition , "model").text == rVendorversion, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "Slot_ontStatusTable", entryPosition , "OntAdminState").text == self.rOntrowstatusDic.get(rOntrowstatus, "Unknow"), f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "Slot_ontStatusTable", entryPosition , "OntOperationStatus").text == self.ontStatusDetailDic.get(rOntstate, "Unknow"), f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "Slot_ontStatusTable", entryPosition , "description").text == rDescription, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "Slot_ontStatusTable", entryPosition , "templateName").text == rTemplatename, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"

    #Edith Dashboard/ Ont Status
    @pytest.mark.restful
    def test_EMS1_6704_devXontInfoDashboard(self):
        self.driver.find_element(By.LINK_TEXT, "Dashboard").click()
        WebDriverWait(self.driver, 300).until(EC.visibility_of_element_located((By.XPATH, "//div[@id=\'dashboard_net_title\']")))
        time.sleep (3)
        self.driver.find_element(By.XPATH, "//div[@id=\'ontStatus\']/div[1]/div[2]/a").click()
        self.driver.find_element(By.CSS_SELECTOR, ".comboTreeArrowBtnImg").click()
        time.sleep (3)
        self.driver.find_element(By.XPATH, "//label[contains(.,\'" + self.dutNodeName + "\')]/parent::li").click()
        time.sleep (3)
        for ontIndex in range(self.xontCount):
            rSlot = str(self.rXontInfo[ontIndex]["slot"])
            rPort = str(self.rXontInfo[ontIndex]["port"])
            rOntid = self.rXontInfo[ontIndex]["ontid"]
            if rOntid> 1000:
                continue
            else:
                rSn = self.rXontInfo[ontIndex]["sn"] if self.rXontInfo[ontIndex]["sn"] != "" else "--"
                rPassword = self.rXontInfo[ontIndex]["password"] if self.rXontInfo[ontIndex]["password"] != "" else "--"
                rActuralsn = self.rXontInfo[ontIndex]["acturalsn"]
                rActuralpassword = self.rXontInfo[ontIndex]["acturalpassword"]
                rVendorversion = self.rXontInfo[ontIndex]["vendorversion"] if self.rXontInfo[ontIndex]["vendorversion"] != "" else "--"
                rOntrowstatus = self.rXontInfo[ontIndex]["ontrowstatus"]
                rOntstate = self.rXontInfo[ontIndex]["ontstate"]
                rDescription = self.rXontInfo[ontIndex]["description"] if self.rXontInfo[ontIndex]["description"] != "" else "--"
                rTemplatename = self.rXontInfo[ontIndex]["templatename"] if self.rXontInfo[ontIndex]["templatename"] != "" else "--"
                ontStatus = self.ontStatusSimpleDic[rOntstate]
                if "dashboard-underborder-green" not in self.driver.find_element(By.XPATH, "//div[@id=\'ontStatus\']/div[" + ontStatus + "]/div[2]").get_attribute("className"):
                    self.driver.find_element(By.XPATH, "//div[@id=\'ontStatus\']/div[" + ontStatus + "]/div[2]/a").click()
                    self.driver.find_element(By.CSS_SELECTOR, ".comboTreeArrowBtnImg").click()
                    time.sleep (3)
                    self.driver.find_element(By.XPATH, "//label[contains(.,\'" + self.dutNodeName + "\')]/parent::li").click()
                    time.sleep (3)
                entryPosition = getPositionByColsNext(self, "All_ontStatusTable", {"Slot": rSlot, "Port": rPort, "ONT": str(rOntid)})
                if self.ontStatusDetailDic[rOntstate] == "In Service":
                    with assume: assert getElementByPositionCol(self, "All_ontStatusTable", entryPosition , "sn").text == rActuralsn, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "All_ontStatusTable", entryPosition , "password").text == rActuralpassword, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                else:
                    with assume: assert getElementByPositionCol(self, "All_ontStatusTable", entryPosition , "sn").text == rSn, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "All_ontStatusTable", entryPosition , "password").text == rPassword, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "All_ontStatusTable", entryPosition , "model").text == rVendorversion, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "All_ontStatusTable", entryPosition , "OntAdminState").text == self.rOntrowstatusDic.get(rOntrowstatus, "Unknow"), f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "All_ontStatusTable", entryPosition , "OntOperationStatus").text == self.ontStatusDetailDic.get(rOntstate, "Unknow"), f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "All_ontStatusTable", entryPosition , "description").text == rDescription, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getElementByPositionCol(self, "All_ontStatusTable", entryPosition , "templateName").text == rTemplatename, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"

    #Edith Dashboard/ Ont Status/ Ont Dashboard
    @pytest.mark.restful
    def test_EMS1_6705_devXontInfoDashboardOntDashboard(self):
        self.driver.find_element(By.LINK_TEXT, "Dashboard").click()
        WebDriverWait(self.driver, 300).until(EC.visibility_of_element_located((By.XPATH, "//div[@id=\'dashboard_net_title\']")))
        time.sleep (3)
        self.driver.find_element(By.XPATH, "//div[@id=\'ontStatus\']/div[1]/div[2]/a").click()
        self.driver.find_element(By.CSS_SELECTOR, ".comboTreeArrowBtnImg").click()
        time.sleep (3)
        self.driver.find_element(By.XPATH, "//label[contains(.,\'" + self.dutNodeName + "\')]/parent::li").click()
        time.sleep (3)
        for ontIndex in range(self.xontCount):
            rSlot = str(self.rXontInfo[ontIndex]["slot"])
            rPort = str(self.rXontInfo[ontIndex]["port"])
            rOntid = self.rXontInfo[ontIndex]["ontid"]
            if rOntid> 1000:
                continue
            else:
                rOnttype = self.rXontInfo[ontIndex]["onttype"]
                rSn = str(self.rXontInfo[ontIndex]["sn"])
                rPassword = str(self.rXontInfo[ontIndex]["password"])
                rActuralsn = str(self.rXontInfo[ontIndex]["acturalsn"])
                rActuralpassword = str(self.rXontInfo[ontIndex]["acturalpassword"])
                rOntstate = self.rXontInfo[ontIndex]["ontstate"]
                rVendorversion = str(self.rXontInfo[ontIndex]["vendorversion"])
                rBootversion = self.rXontInfo[ontIndex]["bootversion"]
                rFwversiona = str(self.rXontInfo[ontIndex]["fwversiona"])
                rFwversionb = str(self.rXontInfo[ontIndex]["fwversionb"])
                rDistance = str(self.rXontInfo[ontIndex]["distance"])
                rDescription = str(self.rXontInfo[ontIndex]["description"])
                rOntrowstatus = self.rXontInfo[ontIndex]["ontrowstatus"]
                rTemplatename = str(self.rXontInfo[ontIndex]["templatename"])
                rActuralsn = str(self.rXontInfo[ontIndex]["acturalsn"])
                rActuralpassword = str(self.rXontInfo[ontIndex]["acturalpassword"])
                rWaninfo = self.rXontInfo[ontIndex]["waninfo"]
                rLaninfo = self.rXontInfo[ontIndex]["laninfo"]
                rXLaninfo = self.rXontInfo[ontIndex]["xlaninfo"]
                ontStatusSimple = self.ontStatusSimpleDic[rOntstate]
                ontStatus = self.ontStatusDic[rOntstate]
                if "dashboard-underborder-green" not in self.driver.find_element(By.XPATH, "//div[@id=\'ontStatus\']/div[" + ontStatusSimple + "]/div[2]").get_attribute("className"):
                    self.driver.find_element(By.XPATH, "//div[@id=\'ontStatus\']/div[" + ontStatusSimple + "]/div[2]/a").click()
                    self.driver.find_element(By.CSS_SELECTOR, ".comboTreeArrowBtnImg").click()
                    time.sleep(3)
                    self.driver.find_element(By.XPATH, "//label[contains(.,\'" + self.dutNodeName + "\')]/parent::li").click()
                    time.sleep(3)
                getPositionByColsAndClickNext(self, "All_ontStatusTable", {"Slot": rSlot, "Port": rPort, "ONT": str(rOntid)})
                p = self.driver.window_handles[0]
                c = self.driver.window_handles[1]
                self.driver.switch_to.window(c)
                if (ontIndex % 10) == 0:self.driver.refresh()
                time.sleep(3)
                with assume: assert self.driver.find_element(By.ID, "dashboard_ont_title_dev").text == self.dutName + " (" + self.dutIp + ")", f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert self.driver.find_element(By.ID, "dashboard_ont_title_slotid").text == "Slot: " + str(rSlot), f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert self.driver.find_element(By.ID, "dashboard_ont_title_portid").text == "Port: " + rPort, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert self.driver.find_element(By.ID, "dashboard_ont_title_ontid").text == "ONT: " + str(rOntid), f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Active Version") == self.rBootversionSimpleDic[rBootversion], f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Admin Status") == self.rOntrowstatusSimpleDic.get(rOntrowstatus, "Unknow"), f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Description") == rDescription, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Distance") == rDistance, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Model") == rVendorversion, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Operation Status") == ontStatus, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                if ontStatus == "IS":
                    with assume: assert getAttributeValue (self, "ontStatusTable", "Password") == rActuralpassword, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getAttributeValue (self, "ontStatusTable", "SN") == rActuralsn, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                else:
                    with assume: assert getAttributeValue (self, "ontStatusTable", "Password") == rPassword, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                    with assume: assert getAttributeValue (self, "ontStatusTable", "SN") == rSn, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Template Name") == rTemplatename, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Type") == rOnttype.upper(), f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Version 1") == rFwversiona, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                with assume: assert getAttributeValue (self, "ontStatusTable", "Version 2") == rFwversionb, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                for wanIndex in range(len(rWaninfo)):
                    wanIndexStr = "WAN IP "+str(wanIndex+1)
                    with assume: assert getAttributeValue (self, "ontStatusTable", wanIndexStr) == rWaninfo[wanIndex]["ip"], f"Slot {rSlot}, Port {rPort}, Ont {rOntid}"
                for lanIndex in range(len(rLaninfo)):
                    if rLaninfo[lanIndex]["status"] == "link up" or rLaninfo[lanIndex]["status"] == "link down":
                        lanIndexStr = "LAN "+str(lanIndex+1)
                        rLanSpeed = rLaninfo[lanIndex]["speedduplex"].upper().replace("-", " ")
                        rLanStatus = rLaninfo[lanIndex]["status"].upper()
                        rLanState = rLanStatus + " (" + rLanSpeed + ")" if rLaninfo[lanIndex]["status"] != "link down" else rLanStatus
                        with assume: assert getAttributeValue (self, "ontStatusTable", lanIndexStr).upper() == rLanState, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}, Lan {lanIndexStr}"
                for lanIndex in range(len(rXLaninfo)):
                    if rXLaninfo[lanIndex]["status"] == "link up" or rXLaninfo[lanIndex]["status"] == "link down":
                        lanIndexStr = "XLAN "+str(lanIndex+1)
                        rLanSpeed = rXLaninfo[lanIndex]["speedduplex"].upper().replace("-", " ")
                        rLanStatus = rXLaninfo[lanIndex]["status"].upper()
                        rLanState = rLanStatus + " (" + rLanSpeed + ")" if rXLaninfo[lanIndex]["status"] != "link down" else rLanStatus
                        with assume: assert getAttributeValue (self, "ontStatusTable", lanIndexStr).upper() == rLanState, f"Slot {rSlot}, Port {rPort}, Ont {rOntid}, Lan {lanIndexStr}"              
                self.driver.close()
                self.driver.switch_to.window(p)

    #Edith Inventory/ Transceiver
    @pytest.mark.restful
    def test_EMS1_7080_devPortInfoInventoryTransceiver(self):
        self.driver.find_element(By.LINK_TEXT, "Inventory").click()
        WebDriverWait(self.driver, 300).until(EC.visibility_of_element_located((By.LINK_TEXT, "Transceiver")))
        time.sleep (3)
        self.driver.find_element(By.LINK_TEXT, "Transceiver").click()
        time.sleep (3)
        for portIndex in range(self.portCount):
            rSlot = self.rPortInfo[portIndex]["slot"]
            rPort = self.rPortInfo[portIndex]["port"]
            if rPort == 0 or rPort == 99 or rPort == 999:
                continue
            if self.rMscmode == "1" and self.rSlotInfo[rSlot-1]["operstatus"] == 4:
                continue
            if self.rMscmode == "0" and self.rSlotInfo[rSlot-1]["operstatus"] == 3 and rPort > 6:
                continue
            if rPort == 1:
                self.driver.find_element(By.CSS_SELECTOR, "#i_action_refresh > a").click()
                self.driver.find_element(By.CSS_SELECTOR, "#i_action_filter > a").click()
                self.driver.find_element(By.ID, "inventory_transceiver_clear_btn").click()
                self.driver.find_element(By.ID, "ip_transceiver").send_keys(self.dutIp)
                self.driver.find_element(By.ID, "slot_transceiver").send_keys(rSlot)
                self.driver.find_element(By.ID, "inventory_transceiver_btn").click()
            rVendorname = self.rPortInfo[portIndex]["vendorname"]
            rVendorpn = self.rPortInfo[portIndex]["vendorpn"]
            rVendorrevision = self.rPortInfo[portIndex]["vendorrevision"]
            rVendorsn = self.rPortInfo[portIndex]["vendorsn"]
            if rVendorpn != "":
                entryPosition = getPositionByColNext(self, "transceiver_inventory_div", "PortID", str(rPort))
                with assume: assert getElementByPositionCol(self, "transceiver_inventory_div", entryPosition , "SlotID").text == str(rSlot), f"Slot {rSlot}, Port {rPort}"
                with assume: assert getElementByPositionCol(self, "transceiver_inventory_div", entryPosition , "PortID").text == str(rPort), f"Slot {rSlot}, Port {rPort}"
                with assume: assert getElementByPositionCol(self, "transceiver_inventory_div", entryPosition , "VendorName").text == rVendorname.strip(), f"Slot {rSlot}, Port {rPort}"
                with assume: assert getElementByPositionCol(self, "transceiver_inventory_div", entryPosition , "VendorPN").text == rVendorpn.strip(), f"Slot {rSlot}, Port {rPort}"
                with assume: assert getElementByPositionCol(self, "transceiver_inventory_div", entryPosition , "VendorRevision").text == rVendorrevision.strip(), f"Slot {rSlot}, Port {rPort}"
                with assume: assert getElementByPositionCol(self, "transceiver_inventory_div", entryPosition , "VendorSN").text == rVendorsn.strip(), f"Slot {rSlot}, Port {rPort}"
                if "NeoX" in self.dutType:
                    rVendordc = self.rPortInfo[portIndex]["vendordc"] if self.rPortInfo[portIndex]["vendordc"] != "" else "--"
                    rTransceiver = self.rPortInfo[portIndex]["transceiver"] if self.rPortInfo[portIndex]["transceiver"] != "" else "--"
                    rCalibration = self.rPortInfo[portIndex]["calibration"] if self.rPortInfo[portIndex]["calibration"] != "" else "--"
                    with assume: assert getElementByPositionCol(self, "transceiver_inventory_div", entryPosition , "VendorDc").text == rVendordc.strip(), f"Slot {rSlot}, Port {rPort}"
                    with assume: assert getElementByPositionCol(self, "transceiver_inventory_div", entryPosition , "ModuleTypeName").text == rTransceiver.strip(), f"Slot {rSlot}, Port {rPort}"
                    with assume: assert getElementByPositionCol(self, "transceiver_inventory_div", entryPosition , "ModuleTypeCalibration").text == rCalibration.strip(), f"Slot {rSlot}, Port {rPort}"
                else:
                    with assume: assert getElementByPositionCol(self, "transceiver_inventory_div", entryPosition , "VendorDc").text == "null", f"Slot {rSlot}, Port {rPort}"
                    with assume: assert getElementByPositionCol(self, "transceiver_inventory_div", entryPosition , "ModuleTypeName").text == "null", f"Slot {rSlot}, Port {rPort}"
                    with assume: assert getElementByPositionCol(self, "transceiver_inventory_div", entryPosition , "ModuleTypeCalibration").text == "null", f"Slot {rSlot}, Port {rPort}"

    #Edith Dashboard/ Ethernet Access Port Status
    @pytest.mark.restful
    def test_EMS1_7091_devGePortInfoDashboard(self):
        self.driver.find_element(By.LINK_TEXT, "Dashboard").click()
        WebDriverWait(self.driver, 300).until(EC.visibility_of_element_located((By.XPATH, "//div[@id=\'dashboard_net_title\']")))
        time.sleep (3)
        for portIndex in range(self.portCount):
            rSlot = self.rPortInfo[portIndex]["slot"]
            rPort = self.rPortInfo[portIndex]["port"]
            rSlotType = self.rSlotInfo[rSlot-1]["type"]
            if rPort == 0 or rPort == 99 or rPort == 999: continue
            if ("IES" in self.dutType) and (rSlotType not in {51,52,53}) : continue
            elif ("NeoX" in self.dutType) and (rSlotType not in {31}) : continue
            else:
                rType = self.rPortInfo[portIndex]["type"]
                rOperstatus = self.rPortInfo[portIndex]["operstatus"]
                portStatus = self.portStatusSimpleDic[rOperstatus]
                if "dashboard-underborder-green" not in self.driver.find_element(By.XPATH, "//div[@id=\'gePortStatusList\']/div[" + portStatus + "]/div[2]").get_attribute("className"):
                    self.driver.find_element(By.XPATH, "//div[@id=\'gePortStatusList\']/div[" + portStatus + "]/div[2]/a").click()
                rName = self.rPortInfo[portIndex]["name"] if self.rPortInfo[portIndex]["name"] != "" else "--"
                rTel = self.rPortInfo[portIndex]["tel"] if self.rPortInfo[portIndex]["tel"] != "" else "--"
                rOperstatus = self.rPortInfo[portIndex]["operstatus"]
                rAdminstate = self.rPortInfo[portIndex]["adminstate"]
                rRate = ""
                match self.rPortInfo[portIndex]["rate"]:
                    case 0: rRate = "None"
                    case range(1,1000): rRate = str(self.rPortInfo[portIndex]["rate"]) + " M"
                    case _ : 
                        if self.rPortInfo[portIndex]["rate"]%1000 == 0:
                            rRate = str(self.rPortInfo[portIndex]["rate"]//1000) + "G"
                        else:
                            rRate = str(self.rPortInfo[portIndex]["rate"]/1000) + "G"
                entryPosition = getPositionByColsNext(self, "All_gePortStatusTable", {"DevName":self.dutName, "SlotID": str(rSlot), "PortID": str(rPort)})
                print("SlotID : " + str(rSlot) + ", PortID : " + str(rPort))
                with assume: assert getElementByPositionCol(self, "All_gePortStatusTable", entryPosition , "PortName").text == rName, f"Slot {rSlot}, Port {rPort}"
                with assume: assert getElementByPositionCol(self, "All_gePortStatusTable", entryPosition , "Tel").text == rTel, f"Slot {rSlot}, Port {rPort}"
                with assume: assert getElementByPositionCol(self, "All_gePortStatusTable", entryPosition , "portOperationStatus").text == self.portOperstatusDic[rOperstatus], f"Slot {rSlot}, Port {rPort}"
                with assume: assert getElementByPositionCol(self, "All_gePortStatusTable", entryPosition , "portAdminState").text == self.portAdminstateDic[rAdminstate], f"Slot {rSlot}, Port {rPort}"
                with assume: assert getElementByPositionCol(self, "All_gePortStatusTable", entryPosition , "EnetPortLinkStatus").text == rRate, f"Slot {rSlot}, Port {rPort}"
                #ddmi string type
                if  isinstance (self.rPortInfo[portIndex]["ddmitxpower"], str) and isinstance (self.rPortInfo[portIndex]["ddmirxpower"], str):
                    rDdmitxpower = self.rPortInfo[portIndex]["ddmitxpower"] if self.rPortInfo[portIndex]["ddmitxpower"] != "" else "--"
                    rDdmirxpower = self.rPortInfo[portIndex]["ddmirxpower"] if self.rPortInfo[portIndex]["ddmirxpower"] != "" else "--"
                    if rDdmitxpower != "--" and rDdmitxpower != "N/A" and rDdmitxpower != "0.00":
                        rDdmitxpowerFloat = float(rDdmitxpower)
                        txRowerFloat = float(getElementByPositionCol(self, "All_gePortStatusTable", entryPosition , "txPower").text)
                        with assume: assert rDdmitxpowerFloat-0.99 <= txRowerFloat <= rDdmitxpowerFloat+0.99
                    else:
                        with assume: assert getElementByPositionCol(self, "All_gePortStatusTable", entryPosition , "txPower").text == rDdmitxpower, f"Slot {rSlot}, Port {rPort}"
                    if rDdmirxpower != "--" and rDdmirxpower != "N/A" and rDdmirxpower != "0.00":
                        rDdmirxpowerFloat = float(rDdmirxpower)
                        rxRowerFloat = float(getElementByPositionCol(self, "All_gePortStatusTable", entryPosition , "rxPower").text)
                        with assume: assert rDdmirxpowerFloat-0.99 <= rxRowerFloat <= rDdmirxpowerFloat+0.99
                    else:
                        with assume: assert getElementByPositionCol(self, "All_gePortStatusTable", entryPosition , "rxPower").text == rDdmirxpower, f"Slot {rSlot}, Port {rPort}"
   

    #Edith Map/ Device/ Ethernet Access Port Status
    @pytest.mark.restful
    def test_EMS1_7092_devGePortInfoMapDevice(self):
        self.driver.find_element(By.LINK_TEXT, "Map").click()
        WebDriverWait(self.driver, 300).until(EC.visibility_of_element_located((By.ID, "navside_icon")))
        time.sleep (3)
        self.driver.find_element(By.ID, "navside_icon").click()
        self.driver.find_element(By.XPATH, "//li[contains(.,\'" + self.dutNodeName + "\')]").click()
        time.sleep (3)
        self.driver.find_element(By.ID, "navside_icon").click()
        for portIndex in range(self.portCount):
            rSlot = self.rPortInfo[portIndex]["slot"]
            rPort = self.rPortInfo[portIndex]["port"]
            rSlotType = self.rSlotInfo[rSlot-1]["type"]
            if rPort == 0 or rPort == 99 or rPort == 999: continue
            if ("IES" in self.dutType) and (rSlotType not in {51,52,53}) : continue
            elif ("NeoX" in self.dutType) and (rSlotType not in {31}) : continue
            else:
                rType = self.rPortInfo[portIndex]["type"]
                rOperstatus = self.rPortInfo[portIndex]["operstatus"]
                portStatus = self.portStatusSimpleDic[rOperstatus]
                if "dashboard-underborder-green" not in self.driver.find_element(By.XPATH, "//div[@id=\'gePortStatusList\']/div[" + portStatus + "]/div[2]").get_attribute("className"):
                    self.driver.find_element(By.XPATH, "//div[@id=\'gePortStatusList\']/div[" + portStatus + "]/div[2]/a").click()
                rName = self.rPortInfo[portIndex]["name"] if self.rPortInfo[portIndex]["name"] != "" else "--"
                rTel = self.rPortInfo[portIndex]["tel"] if self.rPortInfo[portIndex]["tel"] != "" else "--"
                rOperstatus = self.rPortInfo[portIndex]["operstatus"]
                rAdminstate = self.rPortInfo[portIndex]["adminstate"]
                rRate = ""
                match self.rPortInfo[portIndex]["rate"]:
                    case 0: rRate = "None"
                    case range(1,1000): rRate = str(self.rPortInfo[portIndex]["rate"]) + " M"
                    case _ : 
                        if self.rPortInfo[portIndex]["rate"]%1000 == 0:
                            rRate = str(self.rPortInfo[portIndex]["rate"]//1000) + "G"
                        else:
                            rRate = str(self.rPortInfo[portIndex]["rate"]/1000) + "G"
                entryPosition = getPositionByColsNext(self, "Dev_gePortStatusTable", {"SlotID": str(rSlot), "PortID": str(rPort)})
                with assume: assert getElementByPositionCol(self, "Dev_gePortStatusTable", entryPosition , "PortName").text == str(rName), f"Slot {rSlot}, Port {rPort}"
                with assume: assert getElementByPositionCol(self, "Dev_gePortStatusTable", entryPosition , "Tel").text == str(rTel), f"Slot {rSlot}, Port {rPort}"
                with assume: assert getElementByPositionCol(self, "Dev_gePortStatusTable", entryPosition , "portOperationStatus").text == self.portOperstatusDic[rOperstatus], f"Slot {rSlot}, Port {rPort}"
                with assume: assert getElementByPositionCol(self, "Dev_gePortStatusTable", entryPosition , "portAdminState").text == self.portAdminstateDic[rAdminstate], f"Slot {rSlot}, Port {rPort}"
                with assume: assert getElementByPositionCol(self, "Dev_gePortStatusTable", entryPosition , "EnetPortLinkStatus").text == rRate, f"Slot {rSlot}, Port {rPort}"
                #ddmi string type
                if  isinstance (self.rPortInfo[portIndex]["ddmitxpower"], str) and isinstance (self.rPortInfo[portIndex]["ddmirxpower"], str):
                    rDdmitxpower = self.rPortInfo[portIndex]["ddmitxpower"] if self.rPortInfo[portIndex]["ddmitxpower"] != "" else "--"
                    rDdmirxpower = self.rPortInfo[portIndex]["ddmirxpower"] if self.rPortInfo[portIndex]["ddmirxpower"] != "" else "--"
                    if rDdmitxpower != "--" and rDdmitxpower != "N/A" and rDdmitxpower != "0.00":
                        rDdmitxpowerFloat = float(rDdmitxpower)
                        txRowerFloat = float(getElementByPositionCol(self, "Dev_gePortStatusTable", entryPosition , "txPower").text)
                        with assume: assert rDdmitxpowerFloat-0.99 <= txRowerFloat <= rDdmitxpowerFloat+0.99
                    else:
                        with assume: assert getElementByPositionCol(self, "Dev_gePortStatusTable", entryPosition , "txPower").text == rDdmitxpower, f"Slot {rSlot}, Port {rPort}"
                    if rDdmirxpower != "--" and rDdmirxpower != "N/A" and rDdmirxpower != "0.00":
                        rDdmirxpowerFloat = float(rDdmirxpower)
                        rxRowerFloat = float(getElementByPositionCol(self, "Dev_gePortStatusTable", entryPosition , "rxPower").text)
                        with assume: assert rDdmirxpowerFloat-0.99 <= rxRowerFloat <= rDdmirxpowerFloat+0.99
                    else:
                        with assume: assert getElementByPositionCol(self, "Dev_gePortStatusTable", entryPosition , "rxPower").text == rDdmirxpower, f"Slot {rSlot}, Port {rPort}"

