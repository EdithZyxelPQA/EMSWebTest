from selenium.webdriver.common.by import By
from os import times
import time
from attr import field
from pyrsistent import s
import selenium_module as mod
from selenium.webdriver.support.ui import Select

def Slot_Select(driver,slot):
    retry = True
    while(retry == True):
        try:
            driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlot']/option[{slot}]").click()
        except:
            time.sleep(1)
        try:
            if(driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlot']/option[{slot}]").is_selected() == True):
                retry = False
        except:
            time.sleep(1)

def Port_Select(driver,port):
    retry = True
    while(retry == True):
        try:
            driver.find_element(By.XPATH, f"//*[@name='lctbl_selPort']/option[{port}]").click()
        except:
            time.sleep(1)
        try:
            if(driver.find_element(By.XPATH, f"//*[@name='lctbl_selPort']/option[{port}]").is_selected() == True):
                retry = False
        except:
            time.sleep(1)

def Load(driver):
    driver.find_element(By.NAME, "lctbl_selLoad").click()

# Mirror

def Mirror_Active(driver,request):
    check_box = driver.find_element(By.NAME, f"rpmirror_sltEnable")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Mirror_Destination(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpmirror_sltDestPort']/option[{sel}]").click()

def Mirror_Apply_1(driver):
    driver.find_elements(By.NAME, "rpmirror_btnApply")[0].click()

def Mirror_Mode(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpmirror_sltMonMode']/option[{sel}]").click()

def Mirror_Vlan_All(driver):
    driver.find_elements(By.NAME, "rpmirror_rdoVlan")[0].click()

def Mirror_Vlan_Untag(driver):
    driver.find_elements(By.NAME, "rpmirror_rdoVlan")[1].click()

def Mirror_Vlan_VID(driver):
    driver.find_elements(By.NAME, "rpmirror_rdoVlan")[2].click()

def Mirror_Vlan_VID_Input(driver,value):
    input = driver.find_element(By.NAME, "rpmirror_sltMonVlan")
    input.clear()
    input.send_keys(value)

def Mirror_Session_Vlan(driver, value):
    driver.find_element(By.NAME, "rpmirror_sessionVlan").clear
    driver.find_element(By.NAME, "rpmirror_sessionVlan").send_keys(value)

def Mirror_Apply_2(driver):
    driver.find_elements(By.NAME, "rpmirror_btnApply")[1].click()

def Mirror_Delete(driver):
    driver.find_element(By.NAME, "rpMirrorDelete").click()

# STP

def STP_Active(driver,request):
    check_box = driver.find_element(By.NAME, f"rpswstp_active")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def STP_Mode(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpswstp_mode']/option[{sel}]").click()

def STP_Apply(driver):
    driver.find_elements(By.NAME, "rpswrstp_button_apply")[0].click()

# STP > RSTP

def STP_RSTP_Active(driver,request):
    check_box = driver.find_element(By.NAME, f"rpswrstp_active")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def STP_RSTP_Priority(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpswrstp_priority']/option[{sel}]").click()

def STP_RSTP_Hello_Time(driver,value):
    input = driver.find_element(By.NAME, "rpswrstp_input_hello_time")
    input.clear()
    input.send_keys(value)

def STP_RSTP_Maximum_Age(driver,value):
    input = driver.find_element(By.NAME, "rpswrstp_input_maximum_age")
    input.clear()
    input.send_keys(value)

def STP_RSTP_Forwarding_Delay(driver,value):
    input = driver.find_element(By.NAME, "rpswrstp_input_fwdelay")
    input.clear()
    input.send_keys(value)

def STP_RSTP_Apply(driver):
    driver.find_elements(By.NAME, "rpswrstp_port_button_apply")[0].click()

def STP_RSTP_Cancel(driver):
    driver.find_element(By.NAME, "rpswrstp_port_button_cancel").click()

def STP_RSTP_Port_Active(driver,port,request):
    check_box = driver.find_element(By.NAME, f"rpswrstp_port_active{port}")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def STP_RSTP_Port_Priority(driver,port,value):
    input = driver.find_element(By.NAME, f"rpswrstp_port_priotity{port}")
    input.clear()
    input.send_keys(value)

def STP_RSTP_Port_Path_Cost(driver,port,value):
    input = driver.find_element(By.NAME, f"rpswrstp_port_pathcost{port}")
    input.clear()
    input.send_keys(value)

def STP_RSTP_Port_Apply(driver):
    driver.find_elements(By.NAME, "rpswrstp_port_button_apply")[1].click()

def STP_RSTP_Port_Cancel(driver):
    driver.find_element(By.NAME, "rpswrstp_port_button_cancel2").click()

# STP > MSTP

def STP_MSTP_Active(driver,request):
    check_box = driver.find_element(By.NAME, f"rpswmstp_active")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def STP_MSTP_Hello_Time(driver,value):
    input = driver.find_element(By.NAME, "rpswmstp_input_hello_time")
    input.clear()
    input.send_keys(value)

def STP_MSTP_Maximum_Age(driver,value):
    input = driver.find_element(By.NAME, "rpswmstp_input_maximum_age")
    input.clear()
    input.send_keys(value)

def STP_MSTP_Forwarding_Delay(driver,value):
    input = driver.find_element(By.NAME, "rpswmstp_input_fwdelay")
    input.clear()
    input.send_keys(value)

def STP_MSTP_MaxHops(driver,value):
    input = driver.find_element(By.NAME, "rpswmstp_input_maxhops")
    input.clear()
    input.send_keys(value)

def STP_MSTP_MST_Revision(driver,value):
    input = driver.find_element(By.NAME, "rpswmstp_input_revision")
    input.clear()
    input.send_keys(value)

def STP_MSTP_MST_Configuration_Name(driver,value):
    input = driver.find_element(By.NAME, "rpswmstp_input_configname")
    input.clear()
    input.send_keys(value)

def STP_MSTP_Apply(driver):
    driver.find_elements(By.NAME, "rpswmstp_port_button_apply")[0].click()

def STP_MSTP_Cancel(driver):
    driver.find_element(By.NAME, "rpswmstp_port_button_cancel").click()

def STP_MSTP_Port_Instance(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpswmstp__port_inst']/option[{sel}]").click()

def STP_MSTP_Port_Priority_Select(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpswmstp_port_priority']/option[{sel}]").click()

def STP_MSTP_Port_VLAN(driver,value):
    input = driver.find_element(By.NAME, "rpswmstp_port_Vlan")
    input.clear()
    input.send_keys(value)

def STP_MSTP_Port_Active(driver,port,request):
    check_box = driver.find_element(By.NAME, f"rpswmstp_port_active{port}")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def STP_MSTP_Port_Priority(driver,port,value):
    input = driver.find_element(By.NAME, f"rpswmstp_port_priority{port}")
    input.clear()
    input.send_keys(value)

def STP_MSTP_Port_Path_Cost(driver,port,value):
    input = driver.find_element(By.NAME, f"rpswmstp_port_pathcost{port}")
    input.clear()
    input.send_keys(value)

def STP_MSTP_Port_Apply(driver):
    driver.find_elements(By.NAME, "rpswmstp_port_button_apply")[1].click()

def STP_MSTP_Port_Cancel(driver):
    driver.find_element(By.NAME, "rpswmstp_port_button_cancel2").click()

def STP_MSTP_Port_Delete(driver):
    driver.find_element(By.NAME, "rpswmstp_port_button_delete").click()

# Switch Setup

# Switch Setup > General

def Switch_Setup_General_Priority(driver,priority,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpsw_setup_general_slt_queue_{priority}']/option[{sel}]").click()

def Switch_Setup_General_Apply_1(driver):
    driver.find_element(By.NAME, "rpsw_setup_general_button_apply").click()

def Switch_Setup_General_Cancel_1(driver):
    driver.find_element(By.NAME, "rpsw_setup_general_button_cancel").click()

def Switch_Setup_General_Aging_Time(driver,value):
    input = driver.find_element(By.NAME, f"rpsw_setup_general_ipt_aging_time")
    input.clear()
    input.send_keys(value)

def Switch_Setup_General_Apply_2(driver):
    driver.find_element(By.NAME, "rpsw_setup_general_button_apply2").click()

def Switch_Setup_General_Cancel_2(driver):
    driver.find_element(By.NAME, "rpsw_setup_general_button_cancel2").click()

# Switch Setup > Dot3ad

def Switch_Setup_Dot3ad_Group(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpsw_setup_dot3ad_slt_group']/option[{sel}]").click()

def Switch_Setup_Dot3ad_Mode(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpsw_setup_dot3ad_slt_mode']/option[{sel}]").click()

def Switch_Setup_Dot3ad_Member(driver,value):
    input = driver.find_element(By.NAME, f"rpsw_setup_dot3ad_slt_member")
    input.clear()
    input.send_keys(value)

def Switch_Setup_Dot3ad_Apply_1(driver):
    driver.find_element(By.NAME, "rpsw_setup_dot3ad_button_apply").click()

def Switch_Setup_Dot3ad_Cancel_1(driver):
    driver.find_element(By.NAME, "rpsw_setup_dot3ad_button_cancel").click()

def Switch_Setup_Dot3ad_LACP_Priority(driver,value):
    input = driver.find_element(By.NAME, f"rpsw_setup_dot3ad_ipt_lacp_priority")
    input.clear()
    input.send_keys(value)

def Switch_Setup_Dot3ad_LACP_Timeput(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpsw_setup_dot3ad_slt_lacp_timeout']/option[{sel}]").click()

def Switch_Setup_Dot3ad_Apply_2(driver):
    driver.find_element(By.NAME, "rpsw_setup_dot3ad_button_apply2").click()

def Switch_Setup_Dot3ad_Cancel_2(driver):
    driver.find_element(By.NAME, "rpsw_setup_dot3ad_button_cancel2").click()

# Switch Setup > Isolation

def Switch_Setup_Isolation_Enable(driver,request):
    check_box = driver.find_element(By.NAME, f"rpsw_setup_isolation_chk_enable")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Switch_Setup_Isolation_Apply(driver):
    driver.find_element(By.NAME, "rpswrstp_port_button_apply").click()

def Switch_Setup_Isolation_Cancel(driver):
    driver.find_element(By.NAME, "rpswrstp_port_button_cancel").click()

# Switch Setup > DSCP

def Switch_Setup_DSCP_Mapping(driver,Codepoint,Priority,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpsw_setup_dscp_slt_priority_{Codepoint+Priority}']/option[{sel}]").click()

def Switch_Setup_DSCP_Apply_1(driver):
    driver.find_element(By.NAME, "rpsw_setup_dscp_button_apply").click()

def Switch_Setup_DSCP_Cancel_1(driver):
    driver.find_element(By.NAME, "rpsw_setup_dscp_button_cancel").click()

def Switch_Setup_DSCP_Slot_Select(driver,slot):
    retry = True
    while(retry == True):
        try:
            driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlotjejeje']/option[{slot}]").click()
        except:
            time.sleep(1)
        try:
            if(driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlotjejeje']/option[{slot}]").is_selected() == True):
                retry = False
        except:
            time.sleep(1)

def Switch_Setup_DSCP_All(driver,request):
    check_box = driver.find_element(By.NAME, f"rpsw_setup_dscp_chk_port_all")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Switch_Setup_DSCP_Apply_2(driver):
    driver.find_element(By.NAME, "rpsw_setup_dscp_enable_button_apply").click()

def Switch_Setup_DSCP_Cancel_2(driver):
    driver.find_element(By.NAME, "rpsw_setup_dscp_enable_button_cancel").click()

# Switch Setup > Storm Control

def Switch_Setup_Storm_Control_Slot_Select(driver,slot):
    retry = True
    while(retry == True):
        try:
            driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlotjejeje']/option[{slot}]").click()
        except:
            time.sleep(1)
        try:
            if(driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlotjejeje']/option[{slot}]").is_selected() == True):
                retry = False
        except:
            time.sleep(1)

def Switch_Setup_Storm_Control_Broadcast_All(driver,value):
    input = driver.find_element(By.NAME, f"rpsw_setup_storm_control_ipt_broadcast")
    input.clear()
    input.send_keys(value)

def Switch_Setup_Storm_Control_DLF_All(driver,value):
    input = driver.find_element(By.NAME, f"rpsw_setup_storm_control_ipt_dlf")
    input.clear()
    input.send_keys(value)

def Switch_Setup_Storm_Control_Multicast_All(driver,value):
    input = driver.find_element(By.NAME, f"rpsw_setup_storm_control_ipt_multicast")
    input.clear()
    input.send_keys(value)

def Switch_Setup_Storm_Control_Broadcast(driver,port,value):
    input = driver.find_element(By.NAME, f"rpsw_setup_storm_control_ipt_broadcast{int(port)-1}")
    input.clear()
    input.send_keys(value)

def Switch_Setup_Storm_Control_DLF(driver,port,value):
    input = driver.find_element(By.NAME, f"rpsw_setup_storm_control_ipt_dlf{int(port)-1}")
    input.clear()
    input.send_keys(value)

def Switch_Setup_Storm_Control_Multicast(driver,port,value):
    input = driver.find_element(By.NAME, f"rpsw_setup_storm_control_ipt_multicast{int(port)-1}")
    input.clear()
    input.send_keys(value)

def Switch_Setup_Storm_Control_Apply(driver):
    driver.find_element(By.NAME, "rpsw_setup_storm_control_button_apply").click()

def Switch_Setup_Storm_Control_Cancel(driver):
    driver.find_element(By.NAME, "rpsw_setup_storm_control_button_cancel").click()

# Switch Setup > VCShaping

def Switch_Setup_VCShaping_Enable(driver,request):
    check_box = driver.find_element(By.NAME, f"rpsw_setup_shaping_chk_enable")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Switch_Setup_VCShaping_Apply(driver):
    driver.find_element(By.NAME, "rpswrstp_port_button_apply").click()

def Switch_Setup_VCShaping_Cancel(driver):
    driver.find_element(By.NAME, "rpswrstp_port_button_cancel").click()

# OAM

def OAM_Slot_Select(driver,slot):
    retry = True
    while(retry == True):
        try:
            driver.find_element(By.XPATH, f"//*[@name='rpswoam_slot']/option[{slot}]").click()
        except:
            time.sleep(1)
        try:
            if(driver.find_element(By.XPATH, f"//*[@name='rpswoam_slot']/option[{slot}]").is_selected() == True):
                retry = False
        except:
            time.sleep(1)

def OAM_Enable_All(driver,request):
    check_box = driver.find_element(By.NAME, f"rpswoam_enable_all")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def OAM_Mode_All(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpswoam_mode_all']/option[{sel}]").click()

def OAM_RemoteLoopback_All(driver,request):
    check_box = driver.find_element(By.NAME, f"rpswoam_rmtlbk_all")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def OAM_Apply(driver):
    driver.find_element(By.NAME, "rpswoam_btnApply").click()

def OAM_Cancel(driver):
    driver.find_element(By.NAME, "rpswoam_btnCancel").click()

# LLDP

# LLDP > Configuration

def LLDP_Configuration_Active(driver,request):
    check_box = driver.find_element(By.NAME, f"RpLLDPConfig_ChkActive")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def LLDP_Configuration_Transmit_Interval(driver,value):
    input = driver.find_element(By.NAME, f"RpLLDPConfig_IptTextTransmitInterval")
    input.clear()
    input.send_keys(value)

def LLDP_Configuration_Transmit_Hold(driver,value):
    input = driver.find_element(By.NAME, f"RpLLDPConfig_IptTextTransmitHold")
    input.clear()
    input.send_keys(value)

def LLDP_Configuration_Transmit_Delay(driver,value):
    input = driver.find_element(By.NAME, f"RpLLDPConfig_IptTextTransmitDelay")
    input.clear()
    input.send_keys(value)

def LLDP_Configuration_Transmit_Reinit(driver,value):
    input = driver.find_element(By.NAME, f"RpLLDPConfig_IptTextTransmitReinit")
    input.clear()
    input.send_keys(value)

def LLDP_Configuration_Admin_Status(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='RpLLDPConfig_saSltAdminStatus']/option[{sel}]").click()

def LLDP_Configuration_Notification(driver,request):
    check_box = driver.find_element(By.NAME, f"RpLLDPConfig_saChkNotification")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def LLDP_Configuration_Apply(driver):
    driver.find_element(By.NAME, "rplldp_btnApply").click()

def LLDP_Configuration_Cancel(driver):
    driver.find_element(By.NAME, "rplldp_btnCancel").click()

# LLDP > Basic TLV Setting

def LLDP_Basic_TLV_Setting_Management_Address(driver,request):
    check_box = driver.find_element(By.NAME, f"RpBasicTLVSetting_saChkManagementAddress")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def LLDP_Basic_TLV_Setting_Port_Description(driver,request):
    check_box = driver.find_element(By.NAME, f"RpBasicTLVSetting_saChkPortDescription")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def LLDP_Basic_TLV_Setting_System_Capabilities(driver,request):
    check_box = driver.find_element(By.NAME, f"RpBasicTLVSetting_saChkSystemCapabilities")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def LLDP_Basic_TLV_Setting_System_Description(driver,request):
    check_box = driver.find_element(By.NAME, f"RpBasicTLVSetting_saChkSystemDescription")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def LLDP_Basic_TLV_Setting_System_Name(driver,request):
    check_box = driver.find_element(By.NAME, f"RpBasicTLVSetting_saChkSystemName")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def LLDP_Basic_TLV_Setting_Apply(driver):
    driver.find_element(By.NAME, "RpBasicTLVSetting_BtnApply").click()

def LLDP_Basic_TLV_Setting_Cancel(driver):
    driver.find_element(By.NAME, "rplldp_btnCancel").click()

# LLDP > Orgspecific TLV Setting

def LLDP_Orgspecific_TLV_Setting_VLAN_ID(driver,request):
    check_box = driver.find_element(By.NAME, f"RpOrgTLVSetting_saChkPVLANID")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def LLDP_Orgspecific_TLV_Setting_Link_Aggregation(driver,request):
    check_box = driver.find_element(By.NAME, f"RpOrgTLVSetting_saChkLinkAggregation")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def LLDP_Orgspecific_TLV_Setting_MAC_PHY_Config(driver,request):
    check_box = driver.find_element(By.NAME, f"RpOrgTLVSetting_saChkMACPHY")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def LLDP_Orgspecific_TLV_Setting_Max_Frame_Size(driver,request):
    check_box = driver.find_element(By.NAME, f"RpOrgTLVSetting_saChkMaxFrameSize")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def LLDP_Orgspecific_TLV_Setting_Apply(driver):
    driver.find_element(By.NAME, "RpOrgTLVSetting_BtnApply").click()

def LLDP_Orgspecific_TLV_Setting_Cancel(driver):
    driver.find_element(By.NAME, "rplldp_btnCancel").click()

# Error Disable

# Error Disable > Configuration

def Error_Disable_Configuration_Delete_Active(driver,request):
    check_box = driver.find_element(By.NAME, f"RperrdisConfig_saChkDetectActive")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Error_Disable_Configuration_Mode(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='RperrdisConfig_saSltDetectMode']/option[{sel}]").click()

def Error_Disable_Configuration_Upper(driver,value):
    input = driver.find_element(By.NAME, f"RperrdisConfig_saTxtDetectUpper")
    input.clear()
    input.send_keys(value)

def Error_Disable_Configuration_Recovery_Active(driver,request):
    check_box = driver.find_element(By.NAME, f"RperrdisConfig_saChkRecoveryActive")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Error_Disable_Configuration_Interval(driver,value):
    input = driver.find_element(By.NAME, f"RperrdisConfig_saTxtRecoveryInterval")
    input.clear()
    input.send_keys(value)

def Error_Disable_Configuration_Apply(driver):
    driver.find_element(By.NAME, "rperrdis_btnApply").click()

def Error_Disable_Configuration_Cancel(driver):
    driver.find_element(By.NAME, "rperrdis_btnCancel").click()

# Error Disable > Port Setting

def Error_Disable_Port_Setting_IGMP_All(driver,value):
    input = driver.find_element(By.NAME, f"RperrdisConfig_saTxtThresh_1")
    input.clear()
    input.send_keys(value)

def Error_Disable_Port_Setting_LLDP_All(driver,value):
    input = driver.find_element(By.NAME, f"RperrdisConfig_saTxtThresh_2")
    input.clear()
    input.send_keys(value)

def Error_Disable_Port_Setting_Apply(driver):
    driver.find_element(By.NAME, "RpErrdisPortConfig_BtnApply").click()

def Error_Disable_Port_Setting_Cancel(driver):
    driver.find_element(By.NAME, "rperrdis_btnCancel").click()

# Protect Switch

def Protect_Switch_Group(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpsw_ps_slt_group']/option[{sel}]").click()

def Protect_Switch_Active_port(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpsw_ps_slt_active_port']/option[{sel}]").click()

def Protect_Switch_Backup_port(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpsw_ps_slt_backup_port']/option[{sel}]").click()

def Protect_Switch_Preemption_Mode(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpsw_ps_slt_mode']/option[{sel}]").click()

def Protect_Switch_Preemption_Delay(driver,value):
    input = driver.find_element(By.NAME, f"rpsw_ps_slt_delay")
    input.clear()
    input.send_keys(value)

def Protect_Switch_Apply(driver):
    driver.find_element(By.NAME, "rpsw_ps_button_apply").click()

def Protect_Switch_Cancel(driver):
    driver.find_element(By.NAME, "rpsw_ps_button_cancel").click()

def Protect_Switch_Modify(driver):
    driver.find_element(By.NAME, "rpsw_ps_button_modify").click()

def Protect_Switch_Delete(driver):
    driver.find_element(By.NAME, "rpsw_ps_button_delete").click()
