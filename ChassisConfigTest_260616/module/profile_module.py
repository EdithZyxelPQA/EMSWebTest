from selenium.webdriver.common.by import By
from os import times
import time
from attr import field
from pyrsistent import s
import module.selenium_module as mod
from selenium.webdriver.support.ui import Select

# ACL

def ACL_Profile_Mode(driver,port):
    driver.find_element(By.XPATH, f"//*[@name='rpaclprof_aclProfileMode']/option[{port}]").click()

def ACL_Apply(driver):
    driver.find_elements(By.CLASS_NAME, "font-btn")[0].click()

def ACL_New(driver):
    driver.find_elements(By.CLASS_NAME, "font-btn")[1].click()


def ACL_New_Name(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtName")
    input.clear()
    input.send_keys(value)

def ACL_New_Source_MAC_OUI(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkSrcMac")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_New_Source_MAC_OUI_Input(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtSrcMac")
    input.clear()
    input.send_keys(value)

def ACL_New_Dest_MAC_OUI(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkDstMac")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_New_Dest_MAC_OUI_Input(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtDstMac")
    input.clear()
    input.send_keys(value)

def ACL_New_Source_IP(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkSrcIp")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_New_Source_IP_Input(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtSrcIp")
    input.clear()
    input.send_keys(value)

def ACL_New_Destination_IP(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkDstIp")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_New_Destination_IP_Input(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtDstIp")
    input.clear()
    input.send_keys(value)

def ACL_New_IP_Precedence(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkPrec")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_New_IP_Precedence_Input(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpaclprof_sltPrec']/option[{sel}]").click()

def ACL_New_DSCP(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkDscp")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_New_DSCP_Input(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtDscp")
    input.clear()
    input.send_keys(value)

def ACL_New_Traffic_Class(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkTc")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_New_Traffic_Class_Input(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtTc")
    input.clear()
    input.send_keys(value)

def ACL_New_Next_Header(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkNh")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_New_Next_Header_Input(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtNh")
    input.clear()
    input.send_keys(value)

def ACL_New_Source_L4_Port(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkSrcPort")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_New_Source_L4_Port_Input_1(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtSrcPortBegin")
    input.clear()
    input.send_keys(value)

def ACL_New_Source_L4_Port_Input_2(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtSrcPortEnd")
    input.clear()
    input.send_keys(value)

def ACL_New_Destination_L4_Port(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkDstPort")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_New_Destination_L4_Port_Input_1(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtDstPortBegin")
    input.clear()
    input.send_keys(value)

def ACL_New_Destination_L4_Port_Input_2(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtDstPortEnd")
    input.clear()
    input.send_keys(value)

def ACL_New_Ethertype(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkEther")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_New_Ethertype_Input(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtEther")
    input.clear()
    input.send_keys(value)

def ACL_New_Inner_VID(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkInVlan")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_New_Inner_VID_Input(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtInVlan")
    input.clear()
    input.send_keys(value)

def ACL_New_Inner_Pbit(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkInPbit")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_New_Inner_Pbit_Input(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpaclprof_sltInPbit']/option[{sel}]").click()

def ACL_New_Outer_VID(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkOutVlan")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_New_Outer_VID_Input(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtOutVlan")
    input.clear()
    input.send_keys(value)

def ACL_New_Outer_Pbit(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkOutPbit")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_New_Outer_Pbit_Input(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpaclprof_sltOutPbit']/option[{sel}]").click()

def ACL_New_Protocol(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkPtc")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_New_Protocol_Input(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtPtc")
    input.clear()
    input.send_keys(value)


def ACL_New_Drop(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkDrop")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_New_Permit(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkPermit")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_New_Change_DSCP(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkChangeDscp")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_New_Change_DSCP_Input(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtChangeDscp")
    input.clear()
    input.send_keys(value)

def ACL_New_Change_Outer_Pbit(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkChangeOutPbit")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_New_Change_Outer_Pbit_Input(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpaclprof_sltChangeOutPbit']/option[{sel}]").click()

def ACL_New_Change_QoS_Level(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkChangeQos")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_New_Change_QoS_Level_Input(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpaclprof_sltChangeQos']/option[{sel}]").click()

def ACL_New_Rate_Limit(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkRate")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_New_Rate_Limit_Input_CIR(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtRateCir")
    input.clear()
    input.send_keys(value)

def ACL_New_Rate_Limit_Input_CBS(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtRateCbs")
    input.clear()
    input.send_keys(value)

def ACL_New_Rate_Limit_Input_EIR(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtRateEir")
    input.clear()
    input.send_keys(value)

def ACL_New_Rate_Limit_Input_EBS(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtRateEbs")
    input.clear()
    input.send_keys(value)


def ACL_New_Profile_Priority(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkUdfPriority")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_New_Profile_Priority_Input(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtUdfPriority")
    input.clear()
    input.send_keys(value)


def ACL_New_Apply(driver):
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[0].click()

def ACL_New_Delete(driver):
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()

# ACL Egress

def ACL_Egress_New(driver):
    driver.find_elements(By.CLASS_NAME, "font-btn")[0].click()

def ACL_Egress_New_Name(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtName")
    input.clear()
    input.send_keys(value)

def ACL_Egress_New_Source_MAC_OUI(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkSrcMac")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_Egress_New_Source_MAC_OUI_Input(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtSrcMac")
    input.clear()
    input.send_keys(value)

def ACL_Egress_New_Dest_MAC_OUI(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkDstMac")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_Egress_New_Dest_MAC_OUI_Input(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtDstMac")
    input.clear()
    input.send_keys(value)

def ACL_Egress_New_Source_IP(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkSrcIp")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_Egress_New_Source_IP_Input(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtSrcIp")
    input.clear()
    input.send_keys(value)

def ACL_Egress_New_Destination_IP(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkDstIp")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_Egress_New_Destination_IP_Input(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtDstIp")
    input.clear()
    input.send_keys(value)

def ACL_Egress_New_IP_Precedence(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkPrec")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_Egress_New_IP_Precedence_Input(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpaclprof_sltPrec']/option[{sel}]").click()

def ACL_Egress_New_DSCP(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkDscp")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_Egress_New_DSCP_Input(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtDscp")
    input.clear()
    input.send_keys(value)

def ACL_Egress_New_Traffic_Class(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkTc")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_Egress_New_Traffic_Class_Input(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtTc")
    input.clear()
    input.send_keys(value)

def ACL_Egress_New_Next_Header(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkNh")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_Egress_New_Next_Header_Input(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtNh")
    input.clear()
    input.send_keys(value)

def ACL_Egress_New_Source_L4_Port(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkSrcPort")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_Egress_New_Source_L4_Port_Input_1(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtSrcPortBegin")
    input.clear()
    input.send_keys(value)

def ACL_Egress_New_Source_L4_Port_Input_2(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtSrcPortEnd")
    input.clear()
    input.send_keys(value)

def ACL_Egress_New_Destination_L4_Port(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkDstPort")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_Egress_New_Destination_L4_Port_Input_1(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtDstPortBegin")
    input.clear()
    input.send_keys(value)

def ACL_Egress_New_Destination_L4_Port_Input_2(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtDstPortEnd")
    input.clear()
    input.send_keys(value)

def ACL_Egress_New_Ethertype(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkEther")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_Egress_New_Ethertype_Input(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtEther")
    input.clear()
    input.send_keys(value)

def ACL_Egress_New_Uni_VID(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkInVlan")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_Egress_New_Uni_VID_Input(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtInVlan")
    input.clear()
    input.send_keys(value)

def ACL_Egress_New_Uni_Pbit(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkInPbit")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_Egress_New_Uni_Pbit_Input(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpaclprof_sltInPbit']/option[{sel}]").click()

def ACL_Egress_New_Protocol(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkPtc")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_Egress_New_Protocol_Input(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtPtc")
    input.clear()
    input.send_keys(value)


def ACL_Egress_New_Drop(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkDrop")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_Egress_New_Permit(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkPermit")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_Egress_New_Change_DSCP(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkChangeDscp")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_Egress_New_Change_DSCP_Input(driver,value):
    input = driver.find_element(By.NAME, "rpaclprof_txtChangeDscp")
    input.clear()
    input.send_keys(value)

def ACL_Egress_New_Change_Uni_Pbit(driver,request):
    check_box = driver.find_element(By.NAME, "rpaclprof_chkChangeInPbit")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_Egress_New_Change_Uni_Pbit_Input(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpaclprof_sltChangeInPbit']/option[{sel}]").click()


def ACL_Egress_New_Apply(driver):
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[0].click()

def ACL_Egress_New_Delete(driver):
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()

# DSL

# DSL Alarm

# G.band

# QoS

# QoS > VC-Shaping

def QoS_VC_Shaping_Profile_Name(driver,value):
    input = driver.find_element(By.NAME, "rpprofqosvcshape_txtName")
    input.clear()
    input.send_keys(value)

def QoS_VC_Shaping_Depth(driver,value):
    input = driver.find_element(By.NAME, "rpprofqosvcshape_txtDepth")
    input.clear()
    input.send_keys(value)

def QoS_VC_Shaping_Max_Rate(driver,value):
    input = driver.find_element(By.NAME, "rpprofqosvcshape_txtRate")
    input.clear()
    input.send_keys(value)

def QoS_VC_Shaping_Apply(driver):
    driver.find_element(By.NAME, "rpprofqosvcshape_btnApply").click()

def QoS_VC_Shaping_Delete(driver):
    driver.find_element(By.NAME, "rpprofqosvcshape_btnDelete").click()

# QoS > Shaping

def QoS_Shaping_Profile_Name(driver,value):
    input = driver.find_element(By.NAME, "rpprofqosshape_txtName")
    input.clear()
    input.send_keys(value)

def QoS_Shaping_Max_Rate_Queue(driver,Queue,value):
    input = driver.find_element(By.NAME, f"rpprofqosshape_txtRateQ{Queue}")
    input.clear()
    input.send_keys(value)

def QoS_Shaping_Apply(driver):
    driver.find_element(By.NAME, "rpprofqosshape_btnApply").click()

def QoS_Shaping_Delete(driver):
    driver.find_element(By.NAME, "rpprofqosshape_btnDelete").click()

# QoS > Weight

def QoS_Weight_Profile_Name(driver,value):
    input = driver.find_element(By.NAME, "rpprofqoswrr_txtName")
    input.clear()
    input.send_keys(value)

def QoS_Weight_Weight_Queue(driver,Queue,value):
    input = driver.find_element(By.NAME, f"rpprofqoswrr_txtWeightQ{Queue}")
    input.clear()
    input.send_keys(value)

def QoS_Weight_Apply(driver):
    driver.find_element(By.NAME, "rpprofqoswrr_btnApply").click()

def QoS_Weight_Delete(driver):
    driver.find_element(By.NAME, "rpprofqoswrr_btnDelete").click()

# QoS > RateLimit

def QoS_RateLimit_Profile_Name(driver,value):
    input = driver.find_element(By.NAME, "rpprofqosrlp_txtName")
    input.clear()
    input.send_keys(value)

def QoS_RateLimit_Ingress(driver,request,CIR,CBS,EIR,EBS):
    check_box = driver.find_element(By.NAME, "rpprofqosrlp_chk_ingress")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    input = driver.find_element(By.NAME, f"rpprofqosrlp_ipt_cir")
    input.clear()
    input.send_keys(CIR)
    input = driver.find_element(By.NAME, f"rpprofqosrlp_ipt_cbs")
    input.clear()
    input.send_keys(CBS)
    input = driver.find_element(By.NAME, f"rpprofqosrlp_ipt_pir")
    input.clear()
    input.send_keys(EIR)
    input = driver.find_element(By.NAME, f"rpprofqosrlp_ipt_pbs")
    input.clear()
    input.send_keys(EBS)

def QoS_RateLimit_Egress(driver,request,Rate,Burst):
    check_box = driver.find_element(By.NAME, "rpprofqosrlp_chk_egress")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    input = driver.find_element(By.NAME, f"rpprofqosrlp_ipt_rate")
    input.clear()
    input.send_keys(Rate)
    input = driver.find_element(By.NAME, f"rpprofqosrlp_ipt_burst")
    input.clear()
    input.send_keys(Burst)

def QoS_RateLimit_Apply(driver):
    driver.find_element(By.NAME, "rpprofqosqlp_btnApply").click()

def QoS_RateLimit_Delete(driver):
    driver.find_element(By.NAME, "rpprofqosrlp_btnDelete").click()
