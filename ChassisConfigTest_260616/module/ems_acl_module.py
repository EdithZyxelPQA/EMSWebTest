from os import times
import time
from attr import field
from pyrsistent import s
import module.selenium_module as mod
from selenium.webdriver.support.ui import Select

from selenium.webdriver.common.keys import Keys
import module.ems_module as e_mod
from selenium.webdriver.common.by import By

# .clear() -> .send_keys(Keys.CONTROL + 'a')

def Select_Slot(driver,text):
    # Select(driver.find_element(By.ID, "sw_ouifilter_slot_combobox")).select_by_visible_text(text)
    Select(driver.find_element(By.ID, "sw_ouifilter_slot_combobox")).select_by_value(text)
                                      
def Select_Port(driver,text):
    # if_pass = False
    # count = 0
    # while(if_pass == False):
    #     try:
    #         Select(driver.find_element(By.ID, "sw_ouifilter_port_combobox")).select_by_visible_text(text)
    #         time.sleep(5)
    #         if_pass = True
    #     except:            
    #         count = count + 1
    #         if(count > 3):
    #             break
    #         time.sleep(5)

    Select(driver.find_element(By.ID, "sw_ouifilter_port_combobox")).select_by_visible_text(text)    
    try:
        driver.find_element(By.ID, "configure_loader")
        time.sleep(10)
    except:
        pass


def Save(driver):
    driver.find_element(By.CLASS_NAME, "button.button_center.button_green.button_check_pri").click()
                                    
def OK(driver):
    driver.find_element(By.ID, "popupCallBack").click()


def Load(driver):
    driver.find_element(By.NAME, "lctbl_selLoad").click()



# Anti Macspoof

def Anti_Macspoof_Anti_Macspoof_Select(driver,text):
    Select(driver.find_element(By.ID, "acl_antimacspoof_macspoof_select")).select_by_visible_text(text)

def Anti_Macspoof_Spoof_Action_Select(driver,text):
    Select(driver.find_element(By.ID, "acl_antimacspoof_spoof_select")).select_by_visible_text(text)

            
# ARP Inspection

def ARP_Inspection_Select(driver, text):
    Select(driver.find_element(By.ID, "acl_arp_inspection_select")).select_by_visible_text(text)

def ARP_Inspection_Apply(driver):
    driver.find_elements("class name","button.button_center.button_green.button_check_pri")[0].click()


def ARP_Inspection_VID(driver, value):
    driver.find_element(By.ID, "acl_arp_inspection_vid").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_arp_inspection_vid").send_keys(value)

def ARP_Inspection_VID_Add(driver):
    driver.find_elements("class name","button.button_center.button_green.button_check_pri")[1].click()

def ARP_Inspection_VID_Delete(driver):
    driver.find_elements("class name","button.button_center.button_green.button_check_pri")[2].click()

def ARP_Inspection_VID_Get(driver):
    driver.find_elements("class name","button.button_center.button_green.button_check_pri")[3].click()

# DHCP

# DHCP -> DhcpL2Agent                                 

def DHCP_L2Agent_Max_Lease_Overflow_Mode(driver,text):    
    Select(driver.find_element(By.ID, "acl_dhcpl2agent_overflowmodel_select")).select_by_visible_text(text)

def DHCP_L2Agent_Option_82_Check(driver,text):
    Select(driver.find_element(By.ID, "acl_dhcpl2agent_option82check_select")).select_by_visible_text(text)

def DHCP_L2Agent_Option_82_Policy_Mode(driver,text):
    Select(driver.find_element(By.ID, "acl_dhcpl2agent_option82policympde_select")).select_by_visible_text(text)

def DHCP_L2Agent_DHCP_L2_Agent_Forbidden_New(driver):
    driver.find_element(By.ID, "acl_dhcpl2agent_forbiddenvid_table_new_btn").click()

def DHCP_L2Agent_DHCP_L2_Agent_Forbidden_Select(driver,request,sel):
    e_mod.Checkbox_EMS(driver,f"acl_dhcpl2agent_ldra_checkbox{sel}",request)    

def DHCP_L2Agent_DHCP_L2_Agent_Forbidden_Select_All(driver,request):
    e_mod.Checkbox_EMS(driver,f"acl_dhcpl2agent_ldra_checkbox",request)    

def DHCP_L2Agent_DHCP_L2_Agent_Forbidden_Delete(driver):
    driver.find_element(By.ID, "acl_dhcpl2agent_forbiddenvid_table_del_btn").click()

def DHCP_L2Agent_DHCP_L2_Agent_Forbidden(driver,value):    
    driver.find_element(By.ID, "acl_dhcpl2agent_forbiddenvid_dialog_vid").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_dhcpl2agent_forbiddenvid_dialog_vid").send_keys(value)

def DHCP_L2Agent_DHCP_L2_Agent_Forbidden_LDRA(driver,request):
    e_mod.Checkbox_EMS(driver,f"acl_dhcpl2agent_forbiddenvid_dialog_ldar",request)        
                    
def DHCP_L2Agent_DHCP_L2_Agent_New(driver):
    driver.find_element(By.ID, "acl_dhcpl2agent_vid_table_new_btn").click()

def DHCP_L2Agent_DHCP_L2_Agent_Select(driver,request,sel):
    e_mod.Checkbox_EMS(driver,f"acl_dhcpl2agent_vid_table_checkbox{sel}",request)            

def DHCP_L2Agent_DHCP_L2_Agent_Select_All(driver,request):
    e_mod.Checkbox_EMS(driver,f"acl_dhcpl2agent_vid_table_checkbox",request)                

def DHCP_L2Agent_DHCP_L2_Agent_Delete(driver):
    driver.find_element(By.ID, "acl_dhcpl2agent_vid_table_del_btn").click()

def DHCP_L2Agent_DHCP_L2_Agent_VID(driver,value):    
    driver.find_element(By.ID, "acl_dhcpl2agent_vid_dialog_vid").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_dhcpl2agent_vid_dialog_vid").send_keys(value)

def DHCP_L2Agent_DHCP_L2_Agent_LDRA(driver,request):
    e_mod.Checkbox_EMS(driver,f"acl_dhcpl2agent_vid_dialog_ldar",request)                   

def DHCP_L2Agent_DHCP_L2_Agent_Option_18_Interface_Id(driver,value):
    driver.find_element(By.ID, "acl_dhcpl2agent_vid_dialog_interface").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_dhcpl2agent_vid_dialog_interface").send_keys(value)

def DHCP_L2Agent_DHCP_L2_Agent_Option_37_Remote_Id(driver,value):
    driver.find_element(By.ID, "acl_dhcpl2agent_vid_dialog_remote37").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_dhcpl2agent_vid_dialog_remote37").send_keys(value)

def DHCP_L2Agent_DHCP_L2_Agent_Option_82_Circuit_Id(driver,value):
    driver.find_element(By.ID, "acl_dhcpl2agent_vid_dialog_circuit").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_dhcpl2agent_vid_dialog_circuit").send_keys(value)

def DHCP_L2Agent_DHCP_L2_Agent_Option_82_Remote_Id(driver,value):
    driver.find_element(By.ID, "acl_dhcpl2agent_vid_dialog_remote38").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_dhcpl2agent_vid_dialog_remote38").send_keys(value)

def DHCP_L2Agent_DHCP_L2_Agent_Option_82_Policy(driver,text):    
    Select(driver.find_element(By.ID, "acl_dhcpl2agent_vid_dialog_policy")).select_by_visible_text(text)

def DHCP_L2Agent_DHCP_L2_Agent_Option_82_Linechar(driver,text):
    Select(driver.find_element(By.ID, "acl_dhcpl2agent_vid_dialog_linechar")).select_by_visible_text(text)

def DHCP_L2Agent_DHCP_L2_Agent_Enable_DHCP_Relay(driver,request):
    e_mod.Checkbox_EMS(driver,f"acl_dhcpl2agent_vid_dialog_enablerealy",request)                       

def DHCP_L2Agent_DHCP_L2_Agent_Primary_Relay_Server_IP(driver,value):
    driver.find_element(By.ID, "acl_dhcpl2agent_vid_dialog_priip").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_dhcpl2agent_vid_dialog_priip").send_keys(value)

def DHCP_L2Agent_DHCP_L2_Agent_Secondary_Relay_Server_IP(driver,value):
    driver.find_element(By.ID, "acl_dhcpl2agent_vid_dialog_secip").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_dhcpl2agent_vid_dialog_secip").send_keys(value)

def DHCP_L2Agent_DHCP_L2_Agent_Active_Server(driver,text):    
    Select(driver.find_element(By.ID, "acl_dhcpl2agent_vid_dialog_activeserver")).select_by_visible_text(text)
    
def DHCP_L2Agent_DHCP_L2_Agent_Relay_Mode(driver,text):
    Select(driver.find_element(By.ID, "acl_dhcpl2agent_vid_dialog_relaymode")).select_by_visible_text(text)

# DHCP -> Remote Backup
def DHCP_Remote_Backup_Apply(driver):
    driver.find_element(By.ID, "acl_remotebackup_apply_btn").click()

def DHCP_Remote_Backup_Slot(driver, text):
    Select(driver.find_element(By.ID, "acl_remotebackup_slot_combobox")).select_by_value(text)    

def DHCP_Remote_Backup_Manual_Download(driver):
    driver.find_element(By.ID, "acl_remotebackup_download_btn").click()

def DHCP_Remote_Backup_FTP_IP(driver,value):
    driver.find_element(By.ID, "acl_remotebackup_ip_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_remotebackup_ip_text").send_keys(value)

def DHCP_Remote_Backup_Account(driver,value):
    driver.find_element(By.ID, "acl_remotebackup_account_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_remotebackup_account_text").send_keys(value)

def DHCP_Remote_Backup_Password(driver,value):
    driver.find_element(By.ID, "acl_remotebackup_password_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_remotebackup_password_text").send_keys(value)

def DHCP_Remote_Backup_Filepath(driver,value):
    driver.find_element(By.ID, "acl_remotebackup_path_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_remotebackup_path_text").send_keys(value)

# MAC Count

def MAC_Count_Limit_Input(driver,value):
    driver.find_element(By.ID, "acl_maccount_limit_num").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_maccount_limit_num").send_keys(value)

def MAC_Count_Limit_New(driver):
    driver.find_element(By.ID, "acl_maccount_table_new_btn").click()

def MAC_Count_Limit_New_Vlan(driver,value):
    driver.find_element(By.ID, "acl_maccount_vid_dialog_vid").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_maccount_vid_dialog_vid").send_keys(value)

def MAC_Count_Limit_New_Limit(driver,value):
    driver.find_element(By.ID, "acl_maccount_vid_dialog_limit").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_maccount_vid_dialog_limit").send_keys(value)

def MAC_Count_Limit_Delete(driver):
    driver.find_element(By.ID, "acl_maccount_table_del_btn").click()

def MAC_Count_Limit_Select(driver,request,sel):
    e_mod.Checkbox_EMS(driver,f"acl_maccount_table_checkbox{sel}",request)                           

def MAC_Count_Limit_Select_All(driver,request):
    MAC_Count_Limit_Select(driver,request,"")

# MAC Filter #

def MAC_Filter_Select_Slot(driver,text):
    Select(driver.find_element(By.ID, "sw_macfilter_slot_combobox")).select_by_value(text)

def MAC_Filter_Select_Port(driver,text):
    Select(driver.find_element(By.ID, "sw_macfilter_port_combobox")).select_by_visible_text(str(text))

def MAC_Filter_Enable(driver,request):    
    e_mod.Checkbox_EMS(driver,f"sw_macfilter_portenable_checkbox",request)                           

def MAC_Filter_Mode(driver,text):     
    Select(driver.find_element(By.ID, "sw_macfilter_portmode_combobox")).select_by_visible_text(text)

def MAC_Filter_MAC(driver,value,mac):
    driver.find_element(By.ID, f"sw_macfilter_portmacip{mac}_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, f"sw_macfilter_portmacip{mac}_text").send_keys(value)

def MAC_Filter_Save(driver):
    driver.find_element(By.ID, "sw_macfilter_port_save_btn").click()

# OUI Filter #

def OUI_Filter_Select_Slot(driver,text):
    Select(driver.find_element(By.ID, "sw_ouifilter_slot_combobox")).select_by_value(text)

def OUI_Filter_Select_Port(driver,text):
    Select(driver.find_element(By.ID, "sw_ouifilter_port_combobox")).select_by_visible_text(str(text))
def OUI_Filter_Enable(driver,request):
    e_mod.Checkbox_EMS(driver,f"sw_ouifilter_enable_checkbox",request)                           

def OUI_Filter_Mode(driver,text):
    Select(driver.find_element(By.ID, "sw_ouifilter_mode_combobox")).select_by_visible_text(text)

def OUI_Filter_OUI(driver,value,sel):
    input = driver.find_element(By.ID, f"sw_ouifilter_oui{sel}_text")
    # input.send_keys(Keys.CONTROL + 'a')
    input.clear()
    input.send_keys(value)

def OUI_Filter_Save(driver):
    driver.find_element(By.ID, "sw_ouifilter_save_btn").click()

# Packet Filter

def Packet_Filter_Type(driver,text):
    Select(driver.find_element(By.ID, "acl_packet_filter_filtertype_select")).select_by_visible_text(text)

def Packet_Filter_PPPoE_Reject(driver,text):
    Select(driver.find_element(By.ID, "acl_packet_filter_pppoe_select")).select_by_visible_text(text)

def Packet_Filter_IP_Reject(driver,text):
    Select(driver.find_element(By.ID, "acl_packet_filter_ip_select")).select_by_visible_text(text)

def Packet_Filter_ARP_Reject(driver,text):
    Select(driver.find_element(By.ID, "acl_packet_filter_arp_select")).select_by_visible_text(text)

def Packet_Filter_NetBIOS_Reject(driver,text):
    Select(driver.find_element(By.ID, "acl_packet_filter_netbios_select")).select_by_visible_text(text)

def Packet_Filter_DHCP_Reject(driver,text):
    Select(driver.find_element(By.ID, "acl_packet_filter_dhcp_select")).select_by_visible_text(text)

def Packet_Filter_EAPOL_Reject(driver,text):
    Select(driver.find_element(By.ID, "acl_packet_filter_eapol_select")).select_by_visible_text(text)

def Packet_Filter_IGMP_Reject(driver,text):
    Select(driver.find_element(By.ID, "acl_packet_filter_igmp_select")).select_by_visible_text(text)

# 802.1x

# 802.1x -> General Setup

def x802_1x_General_Setup_Method(driver,text):
    Select(driver.find_element(By.ID, "acl_8021x_general_authentication_method_select")).select_by_visible_text(text)

def x802_1x_General_Setup_Apply(driver):
    driver.find_element(By.ID, "acl_8021x_general_authentication_method_btn").click()

# 802.1x -> RADIUS Server

def x802_1x_RADIUS_Server_IP_Address(driver,value,index):
    input = driver.find_element(By.ID,f"acl_8021x_server_ip_{index}") 
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def x802_1x_RADIUS_Server_Port(driver,value,index):
    input = driver.find_element(By.ID,f"acl_8021x_server_port_{index}") 
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def x802_1x_RADIUS_Server_Secret(driver,value,index):
    input = driver.find_element(By.ID,f"acl_8021x_server_secret_{index}") 
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def x802_1x_RADIUS_Server_Apply(driver):
    driver.find_element(By.ID,"sw_ouifilter_save_btn").click()

# 802.1x -> User Profile

def x802_1x_User_Profile_New(driver):
    driver.find_element(By.ID,"acl_8021x_userprofile_new_btn").click()

def x802_1x_User_Profile_Name(driver,value):
    input = driver.find_element(By.ID,"acl_8021x_userprofile_dialog_name_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def x802_1x_User_Profile_Password(driver,value):
    input = driver.find_element(By.ID,"acl_8021x_userprofile_dialog_password_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

# def x802_1x_User_Profile_Retype_Password(driver,value):
#     input = driver.find_element(By.NAME, "rpDot1xUserProf_retypePasswordSetup")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

def x802_1x_User_Profile_Apply(driver):
    driver.find_element(By.ID,"popupCallBack").click()

# def x802_1x_User_Profile_Delete(driver):
#     driver.find_element(By.NAME, "rpDot1xUserProfDelete").click()

# 802.1x -> Port Setting

def x802_1x_Port_Setting_Control(driver,text):
    Select(driver.find_element(By.ID,"acl_8021x_contr_combobox")).select_by_visible_text(text)

def x802_1x_Port_Setting_Enable_CircuitID(driver,request):
    e_mod.Checkbox_EMS(driver,"acl_8021x_portenable_checkbox",request)

def x802_1x_Port_Setting_Control(driver,text):
    Select(driver.find_element(By.ID,"acl_8021x_contr_combobox")).select_by_visible_text(text)

def x802_1x_Port_Setting_Server_Index(driver,text):
    Select(driver.find_element(By.ID,"acl_8021x_server_combobox")).select_by_visible_text(text)    

def x802_1x_Port_Setting_Auth_Once(driver,request):
    e_mod.Checkbox_EMS(driver,"acl_8021x_auth_once_checkbox",request)

def x802_1x_Port_Setting_Reauth_Period(driver,value):
    input = driver.find_element(By.ID,"acl_8021x_reauthperiod_number")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def x802_1x_Port_Setting_Info(driver,value):
    input = driver.find_element(By.ID,"acl_8021x_info_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def x802_1x_Port_Setting_Apply(driver):
    driver.find_element(By.ID,"acl_8021_port_save").click()


# def x802_1x_Port_Setting_Enable_All(driver,request):
#     check_box = driver.find_element(By.NAME, "rpdot1x_portcfg_chkAll_enable")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def x802_1x_Port_Setting_Control_All(driver,sel):
#     driver.find_element(By.XPATH, f"//*[@name='rpdot1x_portcfg_sltAll_control']/option[{sel}]").click()

# def x802_1x_Port_Setting_Server_Index_All(driver,sel):
#     driver.find_element(By.XPATH, f"//*[@name='rpdot1x_portcfg_sltAll_server']/option[{sel}]").click()

# def x802_1x_Port_Setting_Auth_Once_All(driver,request):
#     check_box = driver.find_element(By.NAME, "rpdot1x_portcfg_chkAll_authonce")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def x802_1x_Port_Setting_Reauth_Period_All(driver,value):
#     input = driver.find_element(By.NAME, "rpdot1x_portcfg_All_period")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def x802_1x_Port_Setting_Circuit_ID_All(driver,value):
#     input = driver.find_element(By.NAME, "rpdot1x_portcfg_iptAll_circuid_id")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def x802_1x_Port_Setting_Apply(driver):
#     driver.find_element(By.NAME, "rpalarm_def_dsl_button_apply").click()

# Loopguard
def Loopguard_LG_Enable(driver,text):
    Select(driver.find_element(By.ID,"acl_loopguard_lg_enable_select")).select_by_visible_text(str(text))

def Loopguard_Policy(driver,text):
    Select(driver.find_element(By.ID,"acl_loopguard_policy_select")).select_by_visible_text(str(text))

def Loopguard_Recover_Time(driver,value):
    driver.find_element(By.ID,"acl_loopguard_recover_time_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"acl_loopguard_recover_time_text").send_keys(value)    

def Loopguard_Apply(driver):
    driver.find_element(By.CLASS_NAME,"button.button_center.button_green.button_check_pri").click()

# def Loopguard_LG_Enable_All(driver,request):
#     check_box = driver.find_element(By.NAME, "rpacl_lg_iptALL_chk_enable")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def Loopguard_Policy_All(driver,sel):
#     driver.find_element(By.XPATH, f"//*[@name='rpacl_lg_sltAll_policy']/option[{sel}]").click()

# def Loopguard_Recover_Time_All(driver,value):
#     input = driver.find_element(By.NAME, "rpacl_lg_iptALL_recover_time")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def Loopguard_Apply(driver):
#     driver.find_element(By.NAME, "rpalarm_def_dsl_button_apply").click()

# # Packet Filter

# def Packet_Filter_Type_All(driver,sel):
#     driver.find_element(By.XPATH, f"//*[@name='rppkfilterAcceptAll']/option[{sel}]").click()

# def Packet_Filter_PPPoE_All(driver,request):
#     check_box = driver.find_element(By.NAME, "rppkfilterREJECT_PPPoE")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def Packet_Filter_IP_All(driver,request):
#     check_box = driver.find_element(By.NAME, "rppkfilterREJECT_IP")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def Packet_Filter_ARP_All(driver,request):
#     check_box = driver.find_element(By.NAME, "rppkfilterREJECT_ARP")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def Packet_Filter_NetBIOS_All(driver,request):
#     check_box = driver.find_element(By.NAME, "rppkfilterREJECT_NETBIOS")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def Packet_Filter_DHCP_All(driver,request):
#     check_box = driver.find_element(By.NAME, "rppkfilterREJECT_DHCP")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def Packet_Filter_EAPOL_All(driver,request):
#     check_box = driver.find_element(By.NAME, "rppkfilterREJECT_EAPOL")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def Packet_Filter_IGMP_All(driver,request):
#     check_box = driver.find_element(By.NAME, "rppkfilterREJECT_IGMP")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def Packet_Filter_Apply(driver):
#     driver.find_element(By.NAME, "rppkfilterport_btnApply").click()

# PPPoE

def PPPoE_New(driver):
    driver.find_element(By.ID, "acl_pppoe_vid_table_new_btn").click()

def PPPoE_Modify(driver):
    driver.find_element(By.ID, "acl_pppoe_vid_table_mod_btn").click()

def PPPoE_Delete(driver):
    driver.find_element(By.ID, "acl_pppoe_vid_table_del_btn").click()

def PPPoE_Option_82_Policy_Mode(driver,text):
    Select(driver.find_element(By.ID, "acl_pppoe_policymode")).select_by_visible_text(text)

def PPPoE_Option_82_Policy_Mode_Apply(driver):
    driver.find_element("class name","button.button_center.button_green.button_check_pri").click()

def PPPoE_New_Intermediate_Agent_VID(driver,value):
    driver.find_element(By.ID, "acl_pppoe_vid_dialog_vid").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_pppoe_vid_dialog_vid").send_keys(value)

def PPPoE_New_Circuit_ID_Option_Info(driver,value):
    driver.find_element(By.ID, "acl_pppoe_vid_dialog_circuit").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_pppoe_vid_dialog_circuit").send_keys(value)

def PPPoE_New_Remote_ID_Option_Info(driver,value):
    driver.find_element(By.ID, "acl_pppoe_vid_dialog_remoit").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_pppoe_vid_dialog_remoit").send_keys(value)

def PPPoE_New_Option_Policy(driver,text):
    Select(driver.find_element(By.ID, "acl_pppoe_vid_dialog_policy")).select_by_visible_text(text)

def PPPoE_New_Option_Linechar(driver,text):
    Select(driver.find_element(By.ID, "acl_pppoe_vid_dialog_linechar")).select_by_visible_text(text)

def PPPoE_Select(driver,request,sel):
    e_mod.Checkbox_EMS(driver,f"acl_pppoe_vid_table_checkbox{sel}",request)    

def PPPoE_Select_All(driver,request):
    PPPoE_Select(driver,request,"")

def PPPoE_Forbidden_New(driver):
    driver.find_element(By.ID, "acl_pppoe_forbidden_vid_table_new_btn").click()

def PPPoE_Forbidden_Delete(driver):
    driver.find_element(By.ID, "acl_pppoe_forbidden_vid_table_del_btn").click()

def PPPoE_Forbidden_New_Intermediate_Agent_Forbidden_VID(driver, value):
    driver.find_element(By.ID, "acl_dhcpl2agent_forbiddenvid_dialog_vid").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_dhcpl2agent_forbiddenvid_dialog_vid").send_keys(value)

def PPPoE_Forbidden_Select(driver,request,sel):
    e_mod.Checkbox_EMS(driver,f"acl_pppoe_forbidden_vid_table_checkbox{sel}",request)        

def PPPoE_Forbidden_Select_All(driver,request):
    PPPoE_Forbidden_Select(driver,request,"")


# ACL Rule

def ACL_Rule_Slot(driver,text):
    Select(driver.find_element(By.ID, "sw_aclrule_slot_combobox")).select_by_value(text)

def ACL_Rule_Port(driver,text):
    Select(driver.find_element(By.ID, "sw_aclrule_port_combobox")).select_by_visible_text(str(text))

def ACL_Rule_ACL_Profile(driver,text):
    Select(driver.find_element(By.ID, "acl_aclrule_aclprofile_combobox")).select_by_visible_text(str(text))

def ACL_Rule_ACL_Priority(driver,text):
    Select(driver.find_element(By.ID, "acl_aclrule_priority_combobox")).select_by_visible_text(str(text))

def ACL_Rule_Apply(driver):
    e_mod.Click(driver,'id','acl_aclrule_save_btn')

def ACL_Rule_Select(driver,index=''):
    e_mod.Checkbox_EMS(driver,f"acl_aclprofile_table_checkbox{index}",True)

def ACL_Rule_Delete(driver):
    e_mod.Click(driver,'id','acl_aclrule_table_delete_btn')


# ACL Profile

def ACL_Profile_Mode(driver,text):
    Select(driver.find_element(By.ID, "acl_AclProfile_mode")).select_by_visible_text(text)

def ACL_Profile_Mode_Apply(driver):
    e_mod.Click(driver,'class name','button.button_center.button_green.button_check_pri')

def ACL_Profile_New(driver):
    e_mod.Click(driver,'id','acl_AclProfile_table_new_btn')

def ACL_Profile_New_Name(driver,value):
    driver.find_element(By.ID, "acl_aclprofile_name_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclprofile_name_text").send_keys(value)

def ACL_Profile_New_Source_MAC_OUI(driver,value):
    e_mod.Checkbox_EMS(driver,"acl_aclprofile_sourmac_checkbox",True)
    driver.find_element(By.ID, "acl_aclprofile_sourmac_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclprofile_sourmac_text").send_keys(value)

def ACL_Profile_New_Dest_MAC_OUI(driver,value):
    e_mod.Checkbox_EMS(driver,"acl_aclprofile_destmac_checkbox",True)
    driver.find_element(By.ID, "acl_aclprofile_destmac_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclprofile_destmac_text").send_keys(value)

def ACL_Profile_New_Source_IP(driver,value):
    e_mod.Checkbox_EMS(driver,"acl_aclprofile_sourip_checkbox",True)
    driver.find_element(By.ID, "acl_aclprofile_sourip_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclprofile_sourip_text").send_keys(value)

def ACL_Profile_New_Dest_IP(driver,value):
    e_mod.Checkbox_EMS(driver,"acl_aclprofile_destip_checkbox",True)
    driver.find_element(By.ID, "acl_aclprofile_destip_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclprofile_destip_text").send_keys(value)

def ACL_Profile_New_IP_Precedence(driver,text):
    e_mod.Checkbox_EMS(driver,"acl_aclprofile_ipp_checkbox",True)
    Select(driver.find_element(By.ID, "acl_aclprofile_ipp_combobox")).select_by_visible_text(text)

def ACL_Profile_New_DSCP(driver,value):
    e_mod.Checkbox_EMS(driver,"acl_aclprofile_dscp_checkbox",True)
    driver.find_element(By.ID, "acl_aclprofile_dscp_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclprofile_dscp_text").send_keys(value)

def ACL_Profile_New_Traffic_Class(driver,value):
    e_mod.Checkbox_EMS(driver,"acl_aclprofile_tc_checkbox",True)
    driver.find_element(By.ID, "acl_aclprofile_tc_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclprofile_tc_text").send_keys(value)

def ACL_Profile_New_Next_Header(driver,value):
    e_mod.Checkbox_EMS(driver,"acl_aclprofile_nh_checkbox",True)
    driver.find_element(By.ID, "acl_aclprofile_nh_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclprofile_nh_text").send_keys(value)

def ACL_Profile_New_Source_L4_Port(driver,value1,value2):
    e_mod.Checkbox_EMS(driver,"acl_aclprofile_sl4p_checkbox",True)
    driver.find_element(By.ID, "acl_aclprofile_sl4p_text1").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclprofile_sl4p_text1").send_keys(value1)
    driver.find_element(By.ID, "acl_aclprofile_sl4p_text2").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclprofile_sl4p_text2").send_keys(value2)

def ACL_Profile_New_Dest_L4_Port(driver,value1,value2):
    e_mod.Checkbox_EMS(driver,"acl_aclprofile_dl4p_checkbox",True)
    driver.find_element(By.ID, "acl_aclprofile_dl4p_text1").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclprofile_dl4p_text1").send_keys(value1)
    driver.find_element(By.ID, "acl_aclprofile_dl4p_text2").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclprofile_dl4p_text2").send_keys(value2)

def ACL_Profile_New_Ethertype(driver,value):
    e_mod.Checkbox_EMS(driver,"acl_aclprofile_etype_checkbox",True)
    driver.find_element(By.ID, "acl_aclprofile_etype_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclprofile_etype_text").send_keys(value)

def ACL_Profile_New_Inner_VID(driver,value):
    e_mod.Checkbox_EMS(driver,"acl_aclprofile_invid_checkbox",True)
    driver.find_element(By.ID, "acl_aclprofile_invid_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclprofile_invid_text").send_keys(value)

def ACL_Profile_New_Inner_Pbit(driver,text):
    e_mod.Checkbox_EMS(driver,"acl_aclprofile_inpbit_checkbox",True)
    Select(driver.find_element(By.ID, "acl_aclprofile_inpbit_combobox")).select_by_visible_text(text)

def ACL_Profile_New_Outer_VID(driver,value):
    e_mod.Checkbox_EMS(driver,"acl_aclprofile_outvid_checkbox",True)
    driver.find_element(By.ID, "acl_aclprofile_outvid_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclprofile_outvid_text").send_keys(value)

def ACL_Profile_New_Outer_Pbit(driver,text):
    e_mod.Checkbox_EMS(driver,"acl_aclprofile_outpbit_checkbox",True)
    Select(driver.find_element(By.ID, "acl_aclprofile_outpbit_combobox")).select_by_visible_text(text)

def ACL_Profile_New_Protocol(driver,value):
    e_mod.Checkbox_EMS(driver,"acl_aclprofile_pro_checkbox",True)
    driver.find_element(By.ID, "acl_aclprofile_pro_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclprofile_pro_text").send_keys(value)
#
def ACL_Profile_New_Drop(driver):
    e_mod.Checkbox_EMS(driver,"acl_aclprofile_drop_checkbox",True)

def ACL_Profile_New_Permit(driver):
    e_mod.Checkbox_EMS(driver,"acl_aclprofile_permit_checkbox",True)

def ACL_Profile_New_Change_DSCP(driver,value):
    e_mod.Checkbox_EMS(driver,"acl_aclprofile_cdscp_text",True)
    driver.find_element(By.ID, "acl_aclprofile_cdscp_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclprofile_cdscp_text").send_keys(value)

def ACL_Profile_New_Change_Outer_Pbit(driver,text):
    e_mod.Checkbox_EMS(driver,"acl_aclprofile_coutpbit_checkbox",True)
    Select(driver.find_element(By.ID, "acl_aclprofile_coutpbit_combobox")).select_by_visible_text(text)

def ACL_Profile_New_Change_QoS_Level(driver,text):
    e_mod.Checkbox_EMS(driver,"acl_aclprofile_cql_checkbox",True)
    Select(driver.find_element(By.ID, "acl_aclprofile_cql_combobox")).select_by_visible_text(text)

def ACL_Profile_New_Rate_Limit(driver,CIR,CBS,EIR,EBS):
    e_mod.Checkbox_EMS(driver,"acl_aclprofile_rl_checkbox",True)
    driver.find_element(By.ID, "acl_aclprofile_rlcir_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclprofile_rlcir_text").send_keys(CIR)
    driver.find_element(By.ID, "acl_aclprofile_rlcbs_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclprofile_rlcbs_text").send_keys(CBS)
    driver.find_element(By.ID, "acl_aclprofile_rleir_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclprofile_rleir_text").send_keys(EIR)
    driver.find_element(By.ID, "acl_aclprofile_rlebs_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclprofile_rlebs_text").send_keys(EBS)
#
def ACL_Profile_New_Profile_Priority(driver,value):
    if value == False:
        e_mod.Checkbox_EMS(driver,"acl_aclprofile_pp_checkbox",False)
    else:
        e_mod.Checkbox_EMS(driver,"acl_aclprofile_pp_checkbox",True)
        driver.find_element(By.ID, "acl_aclprofile_pp_text").send_keys(Keys.CONTROL + 'a')
        driver.find_element(By.ID, "acl_aclprofile_pp_text").send_keys(value)    
#   
def ACL_Profile_Select(driver,index=''):
    e_mod.Checkbox_EMS(driver,f"acl_AclProfile_table_checkbox{index}",True)

def ACL_Profile_Modify(driver):
    e_mod.Click(driver,'id','acl_AclProfile_table_mod_btn')

def ACL_Profile_Delete(driver):
    e_mod.Click(driver,'id','acl_AclProfile_table_del_btn')

# ACL Egress Rule

def ACL_Egress_Rule_Slot(driver,text):
    Select(driver.find_element(By.ID, "sw_aclrule_slot_combobox")).select_by_value(text)

def ACL_Egress_Rule_Port(driver,text):
    Select(driver.find_element(By.ID, "sw_aclrule_port_combobox")).select_by_visible_text(str(text))

def ACL_Egress_Rule_ACL_Profile(driver,text):
    Select(driver.find_element(By.ID, "acl_aclegressrule_rgressprofile_combobox")).select_by_visible_text(str(text))

def ACL_Egress_Rule_ACL_Priority(driver,text):
    Select(driver.find_element(By.ID, "acl_aclegressrule_priority_combobox")).select_by_visible_text(str(text))

def ACL_Egress_Rule_Apply(driver):
    e_mod.Click(driver,'id','acl_acegressrule_save_btn')

def ACL_Egress_Rule_Select(driver,index=''):
    e_mod.Checkbox_EMS(driver,f"acl_aclegressprofile_table_checkbox{index}",True)

def ACL_Egress_Rule_Delete(driver):
    e_mod.Click(driver,'id','acl_aclegressprofile_table_delete_btn')

# ACL Egress Profile

# def ACL_Egress_Profile_Mode(driver,text):
#     Select(driver.find_element(By.ID, "acl_AclProfile_mode")).select_by_visible_text(text)

# def ACL_Egress_Profile_Mode_Apply(driver):
#     e_mod.Click(driver,'class name','button.button_center.button_green.button_check_pri')

def ACL_Egress_Profile_New(driver):
    e_mod.Click(driver,'id','acl_AclEgressProfile_table_new_btn')

def ACL_Egress_Profile_New_Name(driver,value):
    driver.find_element(By.ID, "acl_aclegressprofile_name_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclegressprofile_name_text").send_keys(value)

def ACL_Egress_Profile_New_Source_MAC_OUI(driver,value):
    e_mod.Checkbox_EMS(driver,"acl_aclegressprofile_sourmac_checkbox",True)
    driver.find_element(By.ID, "acl_aclegressprofile_sourmac_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclegressprofile_sourmac_text").send_keys(value)

def ACL_Egress_Profile_New_Dest_MAC_OUI(driver,value):
    e_mod.Checkbox_EMS(driver,"acl_aclegressprofile_destmac_checkbox",True)
    driver.find_element(By.ID, "acl_aclegressprofile_destmac_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclegressprofile_destmac_text").send_keys(value)

def ACL_Egress_Profile_New_Source_IP(driver,value):
    e_mod.Checkbox_EMS(driver,"acl_aclegressprofile_sourip_checkbox",True)
    driver.find_element(By.ID, "acl_aclegressprofile_sourip_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclegressprofile_sourip_text").send_keys(value)

def ACL_Egress_Profile_New_Dest_IP(driver,value):
    e_mod.Checkbox_EMS(driver,"acl_aclegressprofile_destip_checkbox",True)
    driver.find_element(By.ID, "acl_aclegressprofile_destip_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclegressprofile_destip_text").send_keys(value)

def ACL_Egress_Profile_New_IP_Precedence(driver,text):
    e_mod.Checkbox_EMS(driver,"acl_aclegressprofile_ipp_checkbox",True)
    Select(driver.find_element(By.ID, "acl_aclegressprofile_ipp_combobox")).select_by_visible_text(text)

def ACL_Egress_Profile_New_DSCP(driver,value):
    e_mod.Checkbox_EMS(driver,"acl_aclegressprofile_dscp_checkbox",True)
    driver.find_element(By.ID, "acl_aclegressprofile_dscp_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclegressprofile_dscp_text").send_keys(value)

def ACL_Egress_Profile_New_Traffic_Class(driver,value):
    e_mod.Checkbox_EMS(driver,"acl_aclegressprofile_tc_checkbox",True)
    driver.find_element(By.ID, "acl_aclegressprofile_tc_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclegressprofile_tc_text").send_keys(value)

def ACL_Egress_Profile_New_Next_Header(driver,value):
    e_mod.Checkbox_EMS(driver,"acl_aclegressprofile_nh_checkbox",True)
    driver.find_element(By.ID, "acl_aclegressprofile_nh_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclegressprofile_nh_text").send_keys(value)

def ACL_Egress_Profile_New_Source_L4_Port(driver,value1,value2):
    e_mod.Checkbox_EMS(driver,"acl_aclegressprofile_sl4p_checkbox",True)
    driver.find_element(By.ID, "acl_aclegressprofile_sl4p_text1").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclegressprofile_sl4p_text1").send_keys(value1)
    driver.find_element(By.ID, "acl_aclegressprofile_sl4p_text2").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclegressprofile_sl4p_text2").send_keys(value2)

def ACL_Egress_Profile_New_Dest_L4_Port(driver,value1,value2):
    e_mod.Checkbox_EMS(driver,"acl_aclegressprofile_dl4p_checkbox",True)
    driver.find_element(By.ID, "acl_aclegressprofile_dl4p_text1").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclegressprofile_dl4p_text1").send_keys(value1)
    driver.find_element(By.ID, "acl_aclegressprofile_dl4p_text2").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclegressprofile_dl4p_text2").send_keys(value2)

def ACL_Egress_Profile_New_Ethertype(driver,value):
    e_mod.Checkbox_EMS(driver,"acl_aclegressprofile_etype_checkbox",True)
    driver.find_element(By.ID, "acl_aclegressprofile_etype_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclegressprofile_etype_text").send_keys(value)

def ACL_Egress_Profile_New_Uni_VID(driver,value):
    e_mod.Checkbox_EMS(driver,"acl_aclegressprofile_univid_checkbox",True)
    driver.find_element(By.ID, "acl_aclegressprofile_univid_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclegressprofile_univid_text").send_keys(value)

def ACL_Egress_Profile_New_Uni_Pbit(driver,text):
    e_mod.Checkbox_EMS(driver,"acl_aclegressprofile_unipbit_checkbox",True)
    Select(driver.find_element(By.ID, "acl_aclegressprofile_unipbit_combobox")).select_by_visible_text(text)

def ACL_Egress_Profile_New_Protocol(driver,value):
    e_mod.Checkbox_EMS(driver,"acl_aclegressprofile_pro_checkbox",True)
    driver.find_element(By.ID, "acl_aclegressprofile_pro_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclegressprofile_pro_text").send_keys(value)
#
def ACL_Egress_Profile_New_Drop(driver):
    e_mod.Checkbox_EMS(driver,"acl_aclegressprofile_drop_checkbox",True)

def ACL_Egress_Profile_New_Permit(driver):
    e_mod.Checkbox_EMS(driver,"acl_aclegressprofile_permit_checkbox",True)

def ACL_Egress_Profile_New_Change_DSCP(driver,value):
    e_mod.Checkbox_EMS(driver,"acl_aclegressprofile_cdscp_checkbox",True)
    driver.find_element(By.ID, "acl_aclegressprofile_cdscp_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "acl_aclegressprofile_cdscp_text").send_keys(value)

def ACL_Egress_Profile_New_Change_Uni_Pbit(driver,text):
    e_mod.Checkbox_EMS(driver,"acl_aclegressprofile_cunipbit_checkbox",True)
    Select(driver.find_element(By.ID, "acl_aclegressprofile_cunipbit_combobox")).select_by_visible_text(text)
#   
def ACL_Egress_Profile_Select(driver,index=''):
    e_mod.Checkbox_EMS(driver,f"acl_AclEgressProfile_table_checkbox{index}",True)

def ACL_Egress_Profile_Modify(driver):
    e_mod.Click(driver,'id','acl_AclEgressProfile_table_mod_btn')

def ACL_Egress_Profile_Delete(driver):
    e_mod.Click(driver,'id','acl_AclEgressProfile_table_del_btn')


# MACFF

# MACFF -> General Setup

def MACFF_New(driver):
    driver.find_element(By.CLASS_NAME, "font-btn").click()

def MACFF_New_Name(driver,value):
    input = driver.find_element(By.NAME, "rpmacff_txtName")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def MACFF_New_Enable(driver,request,index):
    if(index < 10):
        check_box = driver.find_element(By.NAME, f"rpmacff_chkIndex0{index}")
        if(check_box.is_selected() == True):
            if(request == False):
                check_box.click()
        else:
            if(request == True):
                check_box.click()
    else:
        check_box = driver.find_element(By.NAME, f"rpmacff_chkIndex{index}")
        if(check_box.is_selected() == True):
            if(request == False):
                check_box.click()
        else:
            if(request == True):
                check_box.click()

def MACFF_New_Vlan(driver,value,index):
    if(index < 10):
        input = driver.find_element(By.NAME, f"rpmacff_txtVlan0{index}")
        input.send_keys(Keys.CONTROL + 'a')
        input.send_keys(value)
    else:
        input = driver.find_element(By.NAME, f"rpmacff_txtVlan{index}")
        input.send_keys(Keys.CONTROL + 'a')
        input.send_keys(value)

def MACFF_New_Static(driver,request,index):
    if(index < 10):
        check_box = driver.find_element(By.NAME, f"rpmacff_chkStatic0{index}")
        if(check_box.is_selected() == True):
            if(request == False):
                check_box.click()
        else:
            if(request == True):
                check_box.click()
    else:
        check_box = driver.find_element(By.NAME, f"rpmacff_chkStatic{index}")
        if(check_box.is_selected() == True):
            if(request == False):
                check_box.click()
        else:
            if(request == True):
                check_box.click()

def MACFF_New_ar_as_ip(driver,value,index):
    if(index < 10):
        input = driver.find_element(By.NAME, f"rpmacff_txtArIp0{index}")
        input.send_keys(Keys.CONTROL + 'a')
        input.send_keys(value)
    else:
        input = driver.find_element(By.NAME, f"rpmacff_txtArIp{index}")
        input.send_keys(Keys.CONTROL + 'a')
        input.send_keys(value)

def MACFF_New_subnet_ip(driver,value,index):
    if(index < 10):
        input = driver.find_element(By.NAME, f"rpmacff_txtSrcIp0{index}")
        input.send_keys(Keys.CONTROL + 'a')
        input.send_keys(value)
    else:
        input = driver.find_element(By.NAME, f"rpmacff_txtSrcIp{index}")
        input.send_keys(Keys.CONTROL + 'a')
        input.send_keys(value)

def MACFF_New_netmask(driver,value,index):
    if(index < 10):
        input = driver.find_element(By.NAME, f"rpmacff_txtMask0{index}")
        input.send_keys(Keys.CONTROL + 'a')
        input.send_keys(value)
    else:
        input = driver.find_element(By.NAME, f"rpmacff_txtMask{index}")
        input.send_keys(Keys.CONTROL + 'a')
        input.send_keys(value)

def MACFF_New_Apply(driver):
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[0].click()

def MACFF_New_Delete(driver):
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()

# MACFF -> Apply Table

def MACFF_Apply_Table_Apply_Profile(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpmacff_txtProfileName']/option[{sel}]").click()

def MACFF_Apply_Table_Apply(driver):
    driver.find_element(By.NAME, "rpmacff_Apply").click()

def MACFF_Apply_Table_Delete(driver):
    driver.find_element(By.NAME, "rpAclMacCountPerVlanDelete").click()

# Multicast

def Multicast_The_multicast_packets_from_upstream_direction_for_IPv4_IPv6(driver,text):    
    Select(driver.find_element(By.ID, "acl_multicast_upstream_select")).select_by_visible_text(text)

def Multicast_The_unknown_multicast_packets_for_IPv4(driver,text):
    Select(driver.find_element(By.ID, "acl_multicast_unknow_select")).select_by_visible_text(text)

def Multicast_The_IPv6_passthrough(driver,text):
    Select(driver.find_element(By.ID, "acl_multicast_ipv6pass_select")).select_by_visible_text(text)

def Multicast_The_reserve_multicast_for_IPv4(driver,text):
    Select(driver.find_element(By.ID, "acl_multicast_reserve_select")).select_by_visible_text(text)

# def Multicast_Apply(driver):
#     driver.find_element(By.NAME, "rpaclmc_btnApply").click()

# BPDU Ctrl
def BPDU_Ctrl_Mode(driver,text):
    Select(driver.find_element(By.ID,"acl_bptu_mode_select")).select_by_visible_text(text)

def BPDU_Ctrl_Apply(driver):
    driver.find_element(By.CLASS_NAME,"button.button_center.button_green.button_check_pri").click()

# Host Protection
def Host_Protection_Rate_Limit_Setting(driver,arp,bpdu,dhcp,dhcpv6,icmpv6,igmp,pppoe):
    driver.find_element(By.ID,"acl_hostprotection_arp_input").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"acl_hostprotection_arp_input").send_keys(arp)
    driver.find_element(By.ID,"acl_hostprotection_bpdu_input").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"acl_hostprotection_bpdu_input").send_keys(bpdu)
    driver.find_element(By.ID,"acl_hostprotection_dhcp_input").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"acl_hostprotection_dhcp_input").send_keys(dhcp)
    driver.find_element(By.ID,"acl_hostprotection_dhcpipv6_input").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"acl_hostprotection_dhcpipv6_input").send_keys(dhcpv6)
    driver.find_element(By.ID,"acl_hostprotection_icmpv6_input").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"acl_hostprotection_icmpv6_input").send_keys(icmpv6)
    driver.find_element(By.ID,"acl_hostprotection_igmp_input").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"acl_hostprotection_igmp_input").send_keys(igmp)
    driver.find_element(By.ID,"acl_hostprotection_pppoe_input").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"acl_hostprotection_pppoe_input").send_keys(pppoe)

def Host_Protection_Apply(driver):
    driver.find_element(By.ID,"acl_hostprotection_save_btn").click()

# 
