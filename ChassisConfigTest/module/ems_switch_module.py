from os import times
import time
from attr import field
from pyrsistent import s
import module.selenium_module as mod
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys
import module.ems_module as e_mod

# .clear() -> .send_keys(Keys.CONTROL + 'a')

# def Slot_Select(driver,slot):
#     retry = True
#     while(retry == True):
#         try:
#             driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlot']/option[{slot}]").click()
#         except:
#             time.sleep(1)
#         try:
#             if(driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlot']/option[{slot}]").is_selected() == True):
#                 retry = False
#         except:
#             time.sleep(1)

# def Port_Select(driver,port):
#     retry = True
#     while(retry == True):
#         try:
#             driver.find_element(By.XPATH, f"//*[@name='lctbl_selPort']/option[{port}]").click()
#         except:
#             time.sleep(1)
#         try:
#             if(driver.find_element(By.XPATH, f"//*[@name='lctbl_selPort']/option[{port}]").is_selected() == True):
#                 retry = False
#         except:
#             time.sleep(1)

# def Load(driver):
#     driver.find_element(By.NAME, "lctbl_selLoad").click()

# # Mirror

# def Mirror_Active(driver,request):
#     check_box = driver.find_element(By.NAME, f"rpmirror_sltEnable")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def Mirror_Destination(driver,sel):
#     driver.find_element(By.XPATH, f"//*[@name='rpmirror_sltDestPort']/option[{sel}]").click()

# def Mirror_Apply_1(driver):
#     driver.find_elements(By.NAME, "rpmirror_btnApply")[0].click()

# def Mirror_Mode(driver,sel):
#     driver.find_element(By.XPATH, f"//*[@name='rpmirror_sltMonMode']/option[{sel}]").click()

# def Mirror_Vlan_All(driver):
#     driver.find_elements(By.NAME, "rpmirror_rdoVlan")[0].click()

# def Mirror_Vlan_Untag(driver):
#     driver.find_elements(By.NAME, "rpmirror_rdoVlan")[1].click()

# def Mirror_Vlan_VID(driver):
#     driver.find_elements(By.NAME, "rpmirror_rdoVlan")[2].click()

# def Mirror_Vlan_VID_Input(driver,value):
#     input = driver.find_element(By.NAME, "rpmirror_sltMonVlan")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def Mirror_Session_Vlan(driver, value):
#     driver.find_element(By.NAME, "rpmirror_sessionVlan").clear
#     driver.find_element(By.NAME, "rpmirror_sessionVlan").send_keys(value)

# def Mirror_Apply_2(driver):
#     driver.find_elements(By.NAME, "rpmirror_btnApply")[1].click()

# def Mirror_Delete(driver):
#     driver.find_element(By.NAME, "rpMirrorDelete").click()

# # STP

# def STP_Active(driver,request):
#     check_box = driver.find_element(By.NAME, f"rpswstp_active")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def STP_Mode(driver,sel):
#     driver.find_element(By.XPATH, f"//*[@name='rpswstp_mode']/option[{sel}]").click()

# def STP_Apply(driver):
#     driver.find_elements(By.NAME, "rpswrstp_button_apply")[0].click()

# # STP > RSTP

# def STP_RSTP_Active(driver,request):
#     check_box = driver.find_element(By.NAME, f"rpswrstp_active")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def STP_RSTP_Priority(driver,sel):
#     driver.find_element(By.XPATH, f"//*[@name='rpswrstp_priority']/option[{sel}]").click()

# def STP_RSTP_Hello_Time(driver,value):
#     input = driver.find_element(By.NAME, "rpswrstp_input_hello_time")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def STP_RSTP_Maximum_Age(driver,value):
#     input = driver.find_element(By.NAME, "rpswrstp_input_maximum_age")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def STP_RSTP_Forwarding_Delay(driver,value):
#     input = driver.find_element(By.NAME, "rpswrstp_input_fwdelay")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def STP_RSTP_Apply(driver):
#     driver.find_elements(By.NAME, "rpswrstp_port_button_apply")[0].click()

# def STP_RSTP_Cancel(driver):
#     driver.find_element(By.NAME, "rpswrstp_port_button_cancel").click()

# def STP_RSTP_Port_Active(driver,port,request):
#     check_box = driver.find_element(By.NAME, f"rpswrstp_port_active{port}")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def STP_RSTP_Port_Priority(driver,port,value):
#     input = driver.find_element(By.NAME, f"rpswrstp_port_priotity{port}")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def STP_RSTP_Port_Path_Cost(driver,port,value):
#     input = driver.find_element(By.NAME, f"rpswrstp_port_pathcost{port}")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def STP_RSTP_Port_Apply(driver):
#     driver.find_elements(By.NAME, "rpswrstp_port_button_apply")[1].click()

# def STP_RSTP_Port_Cancel(driver):
#     driver.find_element(By.NAME, "rpswrstp_port_button_cancel2").click()

# # STP > MSTP

# def STP_MSTP_Active(driver,request):
#     check_box = driver.find_element(By.NAME, f"rpswmstp_active")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def STP_MSTP_Hello_Time(driver,value):
#     input = driver.find_element(By.NAME, "rpswmstp_input_hello_time")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def STP_MSTP_Maximum_Age(driver,value):
#     input = driver.find_element(By.NAME, "rpswmstp_input_maximum_age")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def STP_MSTP_Forwarding_Delay(driver,value):
#     input = driver.find_element(By.NAME, "rpswmstp_input_fwdelay")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def STP_MSTP_MaxHops(driver,value):
#     input = driver.find_element(By.NAME, "rpswmstp_input_maxhops")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def STP_MSTP_MST_Revision(driver,value):
#     input = driver.find_element(By.NAME, "rpswmstp_input_revision")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def STP_MSTP_MST_Configuration_Name(driver,value):
#     input = driver.find_element(By.NAME, "rpswmstp_input_configname")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def STP_MSTP_Apply(driver):
#     driver.find_elements(By.NAME, "rpswmstp_port_button_apply")[0].click()

# def STP_MSTP_Cancel(driver):
#     driver.find_element(By.NAME, "rpswmstp_port_button_cancel").click()

# def STP_MSTP_Port_Instance(driver,sel):
#     driver.find_element(By.XPATH, f"//*[@name='rpswmstp__port_inst']/option[{sel}]").click()

# def STP_MSTP_Port_Priority_Select(driver,sel):
#     driver.find_element(By.XPATH, f"//*[@name='rpswmstp_port_priority']/option[{sel}]").click()

# def STP_MSTP_Port_VLAN(driver,value):
#     input = driver.find_element(By.NAME, "rpswmstp_port_Vlan")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def STP_MSTP_Port_Active(driver,port,request):
#     check_box = driver.find_element(By.NAME, f"rpswmstp_port_active{port}")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def STP_MSTP_Port_Priority(driver,port,value):
#     input = driver.find_element(By.NAME, f"rpswmstp_port_priority{port}")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def STP_MSTP_Port_Path_Cost(driver,port,value):
#     input = driver.find_element(By.NAME, f"rpswmstp_port_pathcost{port}")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def STP_MSTP_Port_Apply(driver):
#     driver.find_elements(By.NAME, "rpswmstp_port_button_apply")[1].click()

# def STP_MSTP_Port_Cancel(driver):
#     driver.find_element(By.NAME, "rpswmstp_port_button_cancel2").click()

# def STP_MSTP_Port_Delete(driver):
#     driver.find_element(By.NAME, "rpswmstp_port_button_delete").click()

# Switch 

# Switch > General

def Switch_General_Priority(driver, priority, sel):
    driver.find_element(By.XPATH, f'//*[@id="sw_general_queue{priority}"]/option[{sel}]').click()

def Switch_General_Apply_1(driver):
    driver.find_element(By.ID, "sw_general_queue_apply_btn").click()

def Switch_Setup_General_Aging_Time(driver,value):
    input = driver.find_element(By.ID, f"sw_general_agingiime_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def Switch_General_Apply_2(driver):
    driver.find_element(By.ID, "sw_general_agingiime_apply_btn").click()


# Switch > Dot3ad #

def Switch_Dot3ad_Group(driver,text):    
    Select(driver.find_element(By.ID, "sw_dot3ad_group_select")).select_by_visible_text(text)

def Switch_Dot3ad_Mode(driver,text):
    Select(driver.find_element(By.ID, "sw_dot3ad_mode_select")).select_by_visible_text(text)

def Switch_Dot3ad_Member(driver,value):
    input = driver.find_element(By.ID, f"sw_dot3ad_member_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def Switch_Dot3ad_Apply_1(driver):
    driver.find_element(By.ID, "sw_dot3ad_group_apply_btn").click()

def Switch_Dot3ad_LACP_Priority(driver,value):
    input = driver.find_element(By.ID, f"sw_dot3ad_lacp_pri_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def Switch_Setup_Dot3ad_LACP_Timeput(driver,text):
    Select(driver.find_element(By.ID, "sw_dot3ad_lacp_timeout_select")).select_by_visible_text(text)

def Switch_Dot3ad_Apply_2(driver):
    driver.find_element(By.ID, "sw_dot3ad_lacp_apply_btn").click()


# Switch > Isolation #

def Switch_Isolation_Enable(driver,request):    
    e_mod.Checkbox_EMS(driver,"sw_general_isolation_enable_checkbox",request)

def Switch_Isolation_Apply(driver):
    driver.find_element(By.ID, "sw_general_isolation_apply_btn").click()

def Switch_Isolation_VLAN(driver,value):
    input = driver.find_element(By.ID, f"sw_isolation_vlan_table_vid_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def Switch_Isolation_VLAN_Add(driver):
    driver.find_element(By.ID, "sw_isolation_vlan_table_add_btn").click()

def Switch_Isolation_VLAN_Select(driver,index=''):
    e_mod.Checkbox_EMS(driver,f"sw_isolation_vlan_table_checkbox{index}",True)

def Switch_Isolation_VLAN_Select_All(driver):
    e_mod.Checkbox_EMS(driver,f"sw_isolation_vlan_table_checkbox",True)

def Switch_Isolation_VLAN_Delete(driver):
    driver.find_element(By.ID, "sw_isolation_vlan_table_del_btn").click()


# Switch > DSCP #

def Switch_DSCP_Mapping(driver,index,sel):
    # driver.find_element(By.XPATH, f'//*[@id="sw_dscp_dscppm{Codepoint+Priority}_combobox"]/option[{sel}]').click()    
    Select(driver.find_element("name",f"sw_dscp_{index}")).select_by_visible_text(sel) 

def Switch_DSCP_Slot_Select(driver,text):
    Select(driver.find_element(By.ID, "sw_dscp_slot_combobox")).select_by_value(text)

def Switch_DSCP_Port_Select(driver,text):
    text = str(text)
    Select(driver.find_element(By.ID, "sw_dscp_port_combobox")).select_by_value(text)

def Switch_DSCP_Port_Enable(driver,request):
    e_mod.Checkbox_EMS(driver,"sw_dscp_enable_checkbox",request)  

def Switch_DSCP_Port_Enable_Select(driver,text,sel='all'):      
    Select(driver.find_element(By.ID, f"switch_dscp_dscpport_{sel}")).select_by_visible_text(text)

def Switch_DSCP_Apply_1(driver):
    driver.find_element(By.ID, "sw_dscp_priority_table_save").click()

def Switch_DSCP_Apply_2(driver):
    # driver.find_element(By.ID, "sw_dscp_port_apply").click()
    driver.find_element(By.CLASS_NAME,"button.button_green.mr-3").click()

def Switch_DSCP_Load(driver):
    driver.find_element(By.XPATH,'//*[@value="Load"]').click()

# def Switch_Setup_DSCP_Slot_Select(driver,slot):
#     retry = True
#     while(retry == True):
#         try:
#             driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlotjejeje']/option[{slot}]").click()
#         except:
#             time.sleep(1)
#         try:
#             if(driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlotjejeje']/option[{slot}]").is_selected() == True):
#                 retry = False
#         except:
#             time.sleep(1)

# def Switch_Setup_DSCP_All(driver,request):
#     check_box = driver.find_element(By.NAME, f"rpsw_setup_dscp_chk_port_all")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()


# Switch Setup > Storm Control #

def Switch_Storm_Control_Slot_Select(driver,text):
    Select(driver.find_element(By.ID, "sw_ouifilter_slot_combobox")).select_by_value(text)

def Switch_Storm_Control_Port_Select(driver,text):
    text = str(text)
    Select(driver.find_element(By.ID, "sw_ouifilter_port_combobox")).select_by_value(text)

def Switch_Storm_Control_Broadcast(driver,value):
    input = driver.find_element(By.ID, f"sw_stormctrl_broadcast_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def Switch_Storm_Control_DLF(driver,value):
    input = driver.find_element(By.ID,f"sw_stormctrl_def_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def Switch_Storm_Control_Multicast(driver,value):
    input = driver.find_element(By.ID,f"sw_stormctrl_multi_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def Switch_Setup_Storm_Control_Save(driver):
    driver.find_element(By.CLASS_NAME,"button.button_center.button_green.button_check_pri").click()


# def Switch_Setup_Storm_Control_Slot_Select(driver,slot):
#     retry = True
#     while(retry == True):
#         try:
#             driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlotjejeje']/option[{slot}]").click()
#         except:
#             time.sleep(1)
#         try:
#             if(driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlotjejeje']/option[{slot}]").is_selected() == True):
#                 retry = False
#         except:
#             time.sleep(1)



# # Switch Setup > VCShaping

# def Switch_Setup_VCShaping_Enable(driver,request):
#     check_box = driver.find_element(By.NAME, f"rpsw_setup_shaping_chk_enable")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def Switch_Setup_VCShaping_Apply(driver):
#     driver.find_element(By.NAME, "rpswrstp_port_button_apply").click()

# def Switch_Setup_VCShaping_Cancel(driver):
#     driver.find_element(By.NAME, "rpswrstp_port_button_cancel").click()

# # OAM

# def OAM_Slot_Select(driver,slot):
#     retry = True
#     while(retry == True):
#         try:
#             driver.find_element(By.XPATH, f"//*[@name='rpswoam_slot']/option[{slot}]").click()
#         except:
#             time.sleep(1)
#         try:
#             if(driver.find_element(By.XPATH, f"//*[@name='rpswoam_slot']/option[{slot}]").is_selected() == True):
#                 retry = False
#         except:
#             time.sleep(1)

# def OAM_Enable_All(driver,request):
#     check_box = driver.find_element(By.NAME, f"rpswoam_enable_all")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def OAM_Mode_All(driver,sel):
#     driver.find_element(By.XPATH, f"//*[@name='rpswoam_mode_all']/option[{sel}]").click()

# def OAM_RemoteLoopback_All(driver,request):
#     check_box = driver.find_element(By.NAME, f"rpswoam_rmtlbk_all")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def OAM_Apply(driver):
#     driver.find_element(By.NAME, "rpswoam_btnApply").click()

# def OAM_Cancel(driver):
#     driver.find_element(By.NAME, "rpswoam_btnCancel").click()

# # LLDP

# # LLDP > Configuration

# def LLDP_Configuration_Active(driver,request):
#     check_box = driver.find_element(By.NAME, f"RpLLDPConfig_ChkActive")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def LLDP_Configuration_Transmit_Interval(driver,value):
#     input = driver.find_element(By.NAME, f"RpLLDPConfig_IptTextTransmitInterval")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def LLDP_Configuration_Transmit_Hold(driver,value):
#     input = driver.find_element(By.NAME, f"RpLLDPConfig_IptTextTransmitHold")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def LLDP_Configuration_Transmit_Delay(driver,value):
#     input = driver.find_element(By.NAME, f"RpLLDPConfig_IptTextTransmitDelay")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def LLDP_Configuration_Transmit_Reinit(driver,value):
#     input = driver.find_element(By.NAME, f"RpLLDPConfig_IptTextTransmitReinit")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def LLDP_Configuration_Admin_Status(driver,sel):
#     driver.find_element(By.XPATH, f"//*[@name='RpLLDPConfig_saSltAdminStatus']/option[{sel}]").click()

# def LLDP_Configuration_Notification(driver,request):
#     check_box = driver.find_element(By.NAME, f"RpLLDPConfig_saChkNotification")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def LLDP_Configuration_Apply(driver):
#     driver.find_element(By.NAME, "rplldp_btnApply").click()

# def LLDP_Configuration_Cancel(driver):
#     driver.find_element(By.NAME, "rplldp_btnCancel").click()

# # LLDP > Basic TLV Setting

# def LLDP_Basic_TLV_Setting_Management_Address(driver,request):
#     check_box = driver.find_element(By.NAME, f"RpBasicTLVSetting_saChkManagementAddress")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def LLDP_Basic_TLV_Setting_Port_Description(driver,request):
#     check_box = driver.find_element(By.NAME, f"RpBasicTLVSetting_saChkPortDescription")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def LLDP_Basic_TLV_Setting_System_Capabilities(driver,request):
#     check_box = driver.find_element(By.NAME, f"RpBasicTLVSetting_saChkSystemCapabilities")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def LLDP_Basic_TLV_Setting_System_Description(driver,request):
#     check_box = driver.find_element(By.NAME, f"RpBasicTLVSetting_saChkSystemDescription")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def LLDP_Basic_TLV_Setting_System_Name(driver,request):
#     check_box = driver.find_element(By.NAME, f"RpBasicTLVSetting_saChkSystemName")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def LLDP_Basic_TLV_Setting_Apply(driver):
#     driver.find_element(By.NAME, "RpBasicTLVSetting_BtnApply").click()

# def LLDP_Basic_TLV_Setting_Cancel(driver):
#     driver.find_element(By.NAME, "rplldp_btnCancel").click()

# # LLDP > Orgspecific TLV Setting

# def LLDP_Orgspecific_TLV_Setting_VLAN_ID(driver,request):
#     check_box = driver.find_element(By.NAME, f"RpOrgTLVSetting_saChkPVLANID")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def LLDP_Orgspecific_TLV_Setting_Link_Aggregation(driver,request):
#     check_box = driver.find_element(By.NAME, f"RpOrgTLVSetting_saChkLinkAggregation")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def LLDP_Orgspecific_TLV_Setting_MAC_PHY_Config(driver,request):
#     check_box = driver.find_element(By.NAME, f"RpOrgTLVSetting_saChkMACPHY")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def LLDP_Orgspecific_TLV_Setting_Max_Frame_Size(driver,request):
#     check_box = driver.find_element(By.NAME, f"RpOrgTLVSetting_saChkMaxFrameSize")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def LLDP_Orgspecific_TLV_Setting_Apply(driver):
#     driver.find_element(By.NAME, "RpOrgTLVSetting_BtnApply").click()

# def LLDP_Orgspecific_TLV_Setting_Cancel(driver):
#     driver.find_element(By.NAME, "rplldp_btnCancel").click()

# # Error Disable

# # Error Disable > Configuration

# def Error_Disable_Configuration_Delete_Active(driver,request):
#     check_box = driver.find_element(By.NAME, f"RperrdisConfig_saChkDetectActive")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def Error_Disable_Configuration_Mode(driver,sel):
#     driver.find_element(By.XPATH, f"//*[@name='RperrdisConfig_saSltDetectMode']/option[{sel}]").click()

# def Error_Disable_Configuration_Upper(driver,value):
#     input = driver.find_element(By.NAME, f"RperrdisConfig_saTxtDetectUpper")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def Error_Disable_Configuration_Recovery_Active(driver,request):
#     check_box = driver.find_element(By.NAME, f"RperrdisConfig_saChkRecoveryActive")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def Error_Disable_Configuration_Interval(driver,value):
#     input = driver.find_element(By.NAME, f"RperrdisConfig_saTxtRecoveryInterval")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def Error_Disable_Configuration_Apply(driver):
#     driver.find_element(By.NAME, "rperrdis_btnApply").click()

# def Error_Disable_Configuration_Cancel(driver):
#     driver.find_element(By.NAME, "rperrdis_btnCancel").click()

# # Error Disable > Port Setting

# def Error_Disable_Port_Setting_IGMP_All(driver,value):
#     input = driver.find_element(By.NAME, f"RperrdisConfig_saTxtThresh_1")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def Error_Disable_Port_Setting_LLDP_All(driver,value):
#     input = driver.find_element(By.NAME, f"RperrdisConfig_saTxtThresh_2")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def Error_Disable_Port_Setting_Apply(driver):
#     driver.find_element(By.NAME, "RpErrdisPortConfig_BtnApply").click()

# def Error_Disable_Port_Setting_Cancel(driver):
#     driver.find_element(By.NAME, "rperrdis_btnCancel").click()

# # Protect Switch

# def Protect_Switch_Group(driver,sel):
#     driver.find_element(By.XPATH, f"//*[@name='rpsw_ps_slt_group']/option[{sel}]").click()

# def Protect_Switch_Active_port(driver,sel):
#     driver.find_element(By.XPATH, f"//*[@name='rpsw_ps_slt_active_port']/option[{sel}]").click()

# def Protect_Switch_Backup_port(driver,sel):
#     driver.find_element(By.XPATH, f"//*[@name='rpsw_ps_slt_backup_port']/option[{sel}]").click()

# def Protect_Switch_Preemption_Mode(driver,sel):
#     driver.find_element(By.XPATH, f"//*[@name='rpsw_ps_slt_mode']/option[{sel}]").click()

# def Protect_Switch_Preemption_Delay(driver,value):
#     input = driver.find_element(By.NAME, f"rpsw_ps_slt_delay")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def Protect_Switch_Apply(driver):
#     driver.find_element(By.NAME, "rpsw_ps_button_apply").click()

# def Protect_Switch_Cancel(driver):
#     driver.find_element(By.NAME, "rpsw_ps_button_cancel").click()

# def Protect_Switch_Modify(driver):
#     driver.find_element(By.NAME, "rpsw_ps_button_modify").click()

# def Protect_Switch_Delete(driver):
#     driver.find_element(By.NAME, "rpsw_ps_button_delete").click()
