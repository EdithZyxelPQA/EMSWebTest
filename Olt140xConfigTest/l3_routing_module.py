from selenium.webdriver.common.by import By
from os import times
import time
from attr import field
from pyrsistent import s
import selenium_module as mod
from selenium.webdriver.support.ui import Select

# Interface

# Interface > Interface

def Interface_Interface_VID_Select(driver,text):
    Select(driver.find_element(By.ID, "vid_select")).select_by_visible_text(text)

def Interface_Interface_Load(driver):
    driver.find_element(By.ID, "vid_Load").click()

def Interface_Interface_Delete(driver):
    driver.find_element(By.ID, "rprip_btnDelete").click()

def Interface_Interface_IP(driver,value):
    input = driver.find_element(By.ID, "rpinterface_ip")
    input.clear()
    input.send_keys(value)

def Interface_Interface_Mask(driver,value):
    input = driver.find_element(By.ID, "rpinterface_mask")
    input.clear()
    input.send_keys(value)

def Interface_Interface_Apply(driver):
    driver.find_element(By.ID, "rprip_btnApply").click()

# Interface > RIP

def Interface_RIP_VLAN_Select(driver,text):
    Select(driver.find_element(By.ID, "rpl3routing_ripSelvlan")).select_by_visible_text(text)

def Interface_RIP_Load(driver):
    driver.find_element(By.NAME, "rpl3routingRipRoad").click()

def Interface_RIP_Direction(driver,sel):
    driver.find_element(By.XPATH, f"//*[@id='rpl3routingRip_direction']/option[{sel}]").click()

def Interface_RIP_Version(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpl3routingRip_version']/option[{sel}]").click()

def Interface_RIP_Apply(driver):
    driver.find_element(By.NAME, "rpl3routingRipApply").click()

# Interface > OSPF

def Interface_OSPF_VLAN_Select(driver,text):
    Select(driver.find_element(By.ID, "webOspf_vidSelect")).select_by_visible_text(text)

def Interface_OSPF_Load(driver):
    driver.find_element(By.ID, "webOspf_btnLoad").click()

def Interface_OSPF_Cost(driver,value):
    input = driver.find_element(By.ID, "webOspf_inputCost")
    input.clear()
    input.send_keys(value)

def Interface_OSPF_Priority(driver,value):
    input = driver.find_element(By.ID, "webOspf_inputPriority")
    input.clear()
    input.send_keys(value)

def Interface_OSPF_Passive(driver,request):
    check_box = driver.find_element(By.ID, "webOspf_checkPassive")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Interface_OSPF_Retransmit_Interval(driver,value):
    input = driver.find_element(By.ID, "webOspf_inputRetransmit")
    input.clear()
    input.send_keys(value)

def Interface_OSPF_Transmit_Delay(driver,value):
    input = driver.find_element(By.ID, "webOspf_inputTransmit")
    input.clear()
    input.send_keys(value)

def Interface_OSPF_Dead_Interval(driver,value):
    input = driver.find_element(By.ID, "webOspf_inputDead")
    input.clear()
    input.send_keys(value)

def Interface_OSPF_Hello_Interval(driver,value):
    input = driver.find_element(By.ID, "webOspf_inputHello")
    input.clear()
    input.send_keys(value)

def Interface_OSPF_Authentication(driver,sel):
    driver.find_element(By.XPATH, f"//*[@id='webOspf_selectAuth']/option[{sel}]").click()

def Interface_OSPF_Simple_Key(driver,value):
    input = driver.find_element(By.ID, "webOspf_inputSimple")
    input.clear()
    input.send_keys(value)

def Interface_OSPF_MD5_Key_ID(driver,value):
    input = driver.find_element(By.ID, "webOspf_inputMd5KeyId")
    input.clear()
    input.send_keys(value)

def Interface_OSPF_MD5_Key(driver,value):
    input = driver.find_element(By.ID, "webOspf_inputMd5Key")
    input.clear()
    input.send_keys(value)

def Interface_OSPF_Apply(driver):
    driver.find_element(By.ID, "webOspf_btnApply").click()

def Interface_OSPF_Default(driver):
    driver.find_element(By.ID, "webOspf_btnDefault").click()

# RIP

def RIP_Distance(driver,value):
    input = driver.find_element(By.ID, "rprip_input_distance")
    input.clear()
    input.send_keys(value)

def RIP_Apply(driver):
    driver.find_element(By.ID, "rprip_btnApply").click()

def RIP_Default(driver):
    driver.find_element(By.ID, "rprip_btnDefault").click()

# DHCP Server

# DHCP Server > Server

def DHCP_Serve_Server_VID(driver,text):
    Select(driver.find_element(By.ID, "webDhcpServer_vidSelect")).select_by_visible_text(text)

def DHCP_Serve_Server_Load(driver):
    driver.find_element(By.ID, "webDhcpServer_btnLoad").click()

def DHCP_Serve_Server_Start_IP(driver,value):
    input = driver.find_element(By.ID, "webDhcpServer_startAddr")
    input.clear()
    input.send_keys(value)

def DHCP_Serve_Server_End_IP(driver,value):
    input = driver.find_element(By.ID, "webDhcpServer_endAddr")
    input.clear()
    input.send_keys(value)

def DHCP_Serve_Server_Apply(driver):
    driver.find_element(By.ID, "webDhcpServer_btnApply").click()

def DHCP_Serve_Server_Select_Netmask(driver,value):
    input = driver.find_element(By.NAME, "webDhcpServer_netmask")
    input.clear()
    input.send_keys(value)

def DHCP_Serve_Server_Select_Gateway(driver,value):
    input = driver.find_element(By.NAME, "webDhcpServer_gateway")
    input.clear()
    input.send_keys(value)

def DHCP_Serve_Server_Select_Primary(driver,value):
    input = driver.find_element(By.NAME, "webDhcpServer_primaryDnsAddr")
    input.clear()
    input.send_keys(value)

def DHCP_Serve_Server_Select_Secondary(driver,value):
    input = driver.find_element(By.NAME, "webDhcpServer_secondaryDnsAddr")
    input.clear()
    input.send_keys(value)

def DHCP_Serve_Server_Select_Apply(driver):
    driver.find_element(By.NAME, "webDhcpServer_btnOpApply").click()

def DHCP_Serve_Server_Select_Delete(driver):
    driver.find_element(By.NAME, "webDhcpServer_btnDelete").click()

# DHCP Server > Lease

def DHCP_Serve_Lease_VID(driver,text):
    Select(driver.find_element(By.ID, "webDhcpServerLease_vidSelect")).select_by_visible_text(text)

def DHCP_Serve_Lease_ALIE(driver,request):
    check_box = driver.find_element(By.NAME, "webDhcpServerLease_expiredChk")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def DHCP_Serve_Lease_Load(driver):
    driver.find_element(By.ID, "webDhcpServerLease_btnLoad").click()

# OSPF

# OSPF > Configuration

def OSPF_Configuration_Active(driver,request):
    check_box = driver.find_element(By.ID, "webOspf_checkOspfActive")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def OSPF_Configuration_Router_ID(driver,value):
    input = driver.find_element(By.ID, "webOspf_inputRouterId")
    input.clear()
    input.send_keys(value)

def OSPF_Configuration_Distance(driver,value):
    input = driver.find_element(By.ID, "webOspf_inputDistance")
    input.clear()
    input.send_keys(value)

def OSPF_Configuration_RS_Active(driver,request):
    check_box = driver.find_element(By.ID, "webOspf_checkRedistributeStatic")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def OSPF_Configuration_RS_Metric_Type(driver,sel):
    driver.find_element(By.XPATH, f"//*[@id='webOspf_selectRedistributeStatic']/option[{sel}]").click()

def OSPF_Configuration_RS_Metric(driver,value):
    input = driver.find_element(By.ID, "webOspf_inputMetricStatic")
    input.clear()
    input.send_keys(value)

def OSPF_Configuration_RR_Active(driver,request):
    check_box = driver.find_element(By.ID, "webOspf_checkRedistributeRip")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def OSPF_Configuration_RR_Metric_Type(driver,sel):
    driver.find_element(By.XPATH, f"//*[@id='webOspf_selectRedistributeRip']/option[{sel}]").click()

def OSPF_Configuration_RR_Metric(driver,value):
    input = driver.find_element(By.ID, "webOspf_inputMetricRip")
    input.clear()
    input.send_keys(value)

def OSPF_Configuration_Apply_1(driver):
    driver.find_element(By.ID, "webOspf_btnApply").click()

def OSPF_Configuration_IP_Address(driver,value):
    input = driver.find_element(By.ID, "webOspf_inputIpAddr")
    input.clear()
    input.send_keys(value)

def OSPF_Configuration_Netmask(driver,value):
    input = driver.find_element(By.ID, "webOspf_inputMask")
    input.clear()
    input.send_keys(value)

def OSPF_Configuration_Area(driver,value):
    input = driver.find_element(By.ID, "webOspf_inputNetArea")
    input.clear()
    input.send_keys(value)

def OSPF_Configuration_Apply_2(driver):
    driver.find_element(By.ID, "webOspfNetwork_btnApply").click()

def OSPF_Configuration_Load(driver):
    driver.find_element(By.ID, "webOspf_btnLoad").click()

def OSPF_Configuration_Delete(driver):
    driver.find_element(By.ID, "webOspf_btnDelete").click()

def OSPF_Configuration_Remove_All(driver):
    driver.find_element(By.ID, "webOspf_btnRemoveAll").click()

# OSPF > Area

def OSPF_Area(driver,value):
    input = driver.find_element(By.ID, "webOspf_inputArea")
    input.clear()
    input.send_keys(value)

def OSPF_Area_Name(driver,value):
    input = driver.find_element(By.ID, "webOspf_inputName")
    input.clear()
    input.send_keys(value)

def OSPF_Area_Type(driver,sel):
    driver.find_element(By.XPATH, f"//*[@id='webOspf_selectAreaType']/option[{sel}]").click()

def OSPF_Area_Default_Cost(driver,value):
    input = driver.find_element(By.ID, "webOspf_inputDefaultCost")
    input.clear()
    input.send_keys(value)

def OSPF_Area_Authentication(driver,sel):
    driver.find_element(By.XPATH, f"//*[@id='webOspf_selectAreaAuth']/option[{sel}]").click()

def OSPF_Area_Apply(driver):
    driver.find_element(By.ID, "webOspf_btnApply").click()

def OSPF_Area_Load(driver):
    driver.find_element(By.ID, "webOspf_btnLoad").click()

def OSPF_Area_Delete(driver):
    driver.find_element(By.ID, "webOspf_btnDelete").click()

def OSPF_Area_Remove_All(driver):
    driver.find_element(By.ID, "webOspf_btnRemoveAll").click()
