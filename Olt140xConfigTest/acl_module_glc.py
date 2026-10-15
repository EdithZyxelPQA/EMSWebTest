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

# Anti Macspoof

def Anti_Macspoof_Anti_Macspoof_Select_All(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpantispoof_sltAntiSpoof_all']/option[{sel}]").click()

# def Anti_Macspoof_Anti_Macspoof_Select(driver,sel,port):
#     driver.find_element(By.XPATH, f"//*[@name='rpantispoof_sltAntiSpoof']/option[{port}]/option[{sel}]").click()
    
def Anti_Macspoof_Spoof_Action_Select_All(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpantispoof_sltSpoofAction_all']/option[{sel}]").click()

# def Anti_Macspoof_Spoof_Action_Select(driver,sel,port): 
#     driver.find_element(By.XPATH, f"//*[@name='rpantispoof_sltSpoofAction']/option[{port}]/option[{sel}]").click()

def Anti_Macspoof_Apply(driver):
    driver.find_element(By.NAME, "rpalarm_def_dsl_button_apply").click()

# Arp Inspection

def Arp_Inspection_Port_Setting_Select_All(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rparpinspection_sltEnable_all']/option[{sel}]").click()

def Arp_Inspection_Port_Setting_Apply(driver):
    driver.find_element(By.NAME, "rpstatArpInspection_apply").click()

# DHCP

# DHCP -> DhcpL2Agent

def DHCP_L2Agent_Max_Lease_Overflow_Mode(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpdhcp_sltOverflowMode']/option[{sel}]").click()

def DHCP_L2Agent_Option_82_Check(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpdhcp_chkOpt82']/option[{sel}]").click()

def DHCP_L2Agent_Option_82_Policy_Mode(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpdhcp_opt82PolicyMode']/option[{sel}]").click()

def DHCP_L2Agent_Apply_1(driver):
    driver.find_element(By.NAME, "rpAclDhcpSysApply").click()

def DHCP_L2Agent_DHCP_L2_Agent_Forbidden(driver,value):
    input = driver.find_element(By.NAME, "rpdhcp_inputL2AgentForbidVid")
    input.clear()
    input.send_keys(value)

def DHCP_L2Agent_LDRA(driver,request):
    check_box = driver.find_element(By.NAME, "rpLDRAForbid_chkEnable")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def DHCP_L2Agent_Apply_2(driver):
    driver.find_element(By.NAME, "rpAclDHCPInterAgentForbidApply").click()

def DHCP_L2Agent_Delete_2(driver):
    driver.find_element(By.NAME, "rpAclDHCPInterAgentForbidDelete").click()

def DHCP_L2Agent_DHCP_L2_Agent_VID(driver,value):
    input = driver.find_element(By.NAME, "rpdhcp_inputL2AgentVid")
    input.clear()
    input.send_keys(value)

def DHCP_L2Agent_Apply_3(driver):
    driver.find_element(By.NAME, "rpAclDHCPInterAgentApply").click()

def DHCP_L2Agent_Select_Enable_LDRA(driver,request):
    check_box = driver.find_element(By.NAME, "rpdhcp_chkLdra")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def DHCP_L2Agent_Select_Option_18_Interface_Id(driver,value):
    input = driver.find_element(By.NAME, "opt18OptionInfo")
    input.clear()
    input.send_keys(value)

def DHCP_L2Agent_Select_Option_37_Remote_Id(driver,value):
    input = driver.find_element(By.NAME, "opt37OptionInfo")
    input.clear()
    input.send_keys(value)

def DHCP_L2Agent_Select_Option_82_Circuit_Id(driver,value):
    input = driver.find_element(By.NAME, "opt82CircuitOptionInfo")
    input.clear()
    input.send_keys(value)

def DHCP_L2Agent_Select_Option_82_Remote_Id(driver,value):
    input = driver.find_element(By.NAME, "opt82RemoteOptionInfo")
    input.clear()
    input.send_keys(value)

def DHCP_L2Agent_Select_Option_82_Policy(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpdhcp_opt82Policy']/option[{sel}]").click()

def DHCP_L2Agent_Select_Option_82_Linechar(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpdhcp_opt82Linechar']/option[{sel}]").click()

def DHCP_L2Agent_Select_Enable_DHCP_Relay(driver,request):
    check_box = driver.find_element(By.NAME, "rpdhcp_chkRelay")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def DHCP_L2Agent_Select_Primary_Relay_Server_IP(driver,value):
    input = driver.find_element(By.NAME, "rpdhcp_priRelaySvrIp")
    input.clear()
    input.send_keys(value)

def DHCP_L2Agent_Select_Secondary_Relay_Server_IP(driver,value):
    input = driver.find_element(By.NAME, "rpdhcp_sndRelaySvrIp")
    input.clear()
    input.send_keys(value)

def DHCP_L2Agent_Select_Active_Server(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpdhcp_activeRelaySvrIdx']/option[{sel}]").click()

def DHCP_L2Agent_Select_Relay_Mode(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpdhcp_relayMode']/option[{sel}]").click()

def DHCP_L2Agent_Select_Apply(driver):
    driver.find_element(By.NAME, "rpAclDHCPInterAgentModify").click()

def DHCP_L2Agent_Select_Delete(driver):
    driver.find_element(By.NAME, "rpAclDHCPInterAgentDelete").click()

# MAC Count

def MAC_Count_Limit_Input_All(driver,value):
    input = driver.find_element(By.NAME, "name_all")
    input.clear()
    input.send_keys(value)

def MAC_Count_Apply(driver):
    driver.find_element(By.ID, "rpmaccountlimit_btnApply").click()

def MAC_Count_Cancel(driver):
    driver.find_element(By.ID, "rpmaccountlimit_btnCancel").click()

def MAC_Count_Detail_Limit(driver,value):
    input = driver.find_element(By.NAME, "rpmacCount_sltMacLimit")
    input.clear()
    input.send_keys(value)

def MAC_Count_Detail_Limit_Apply(driver):
    driver.find_element(By.NAME, "rpAclMacCountApply").click()

def MAC_Count_Detail_Limit_Cancel(driver):
    driver.find_element(By.NAME, "rpAclMacCountCancel").click()

def MAC_Count_Detail_New_VLAN(driver,value):
    input = driver.find_element(By.NAME, "rpmacCount_sltVlanText")
    input.clear()
    input.send_keys(value)

def MAC_Count_Detail_New_Limit(driver,value):
    input = driver.find_element(By.NAME, "rpmacCount_sltLimitText")
    input.clear()
    input.send_keys(value)

def MAC_Count_Detail_New_Apply(driver):
    driver.find_element(By.NAME, "rpmacCount_btnApply").click()

def MAC_Count_Detail_New_Delete(driver):
    driver.find_element(By.NAME, "rpmacCount_btnDelete").click()

# MAC Filter

def MAC_Filter_Enable(driver,request):
    check_box = driver.find_element(By.NAME, "rpmacFilter_chkEnable")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def MAC_Filter_Mode(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpmacFilter_sltMode']/option[{sel}]").click()

def MAC_Filter_MAC(driver,value,mac):
    input = driver.find_element(By.NAME, f"rpmacFilter_sltFilterMac{mac}")
    input.clear()
    input.send_keys(value)

def MAC_Filter_Apply(driver):
    driver.find_element(By.NAME, "rpAclMacFilterApply").click()

def MAC_Filter_Cancel(driver):
    driver.find_element(By.NAME, "rpAclMacFilterCancel").click()

# OUI Filter

def OUI_Filter_Enable(driver,request):
    check_box = driver.find_element(By.NAME, "rpouiFilter_chkEnable")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def OUI_Filter_Mode(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpouiFilter_sltMode']/option[{sel}]").click()

def OUI_Filter_OUI(driver,value,mac):
    input = driver.find_element(By.NAME, f"rpouiFilter_sltFilterOui{mac}")
    input.clear()
    input.send_keys(value)

def OUI_Filter_Apply(driver):
    driver.find_element(By.NAME, "rpAclOuiFilterApply").click()

def OUI_Filter_Cancel(driver):
    driver.find_element(By.NAME, "rpAclOuiFilterCancel").click()

# 802.1x

# 802.1x -> General Setup

def x802_1x_General_Setup_Method(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpDot1x_authMethod']/option[{sel}]").click()

def x802_1x_General_Setup_Apply(driver):
    driver.find_element(By.NAME, "rpDot1xApply").click()

# 802.1x -> RADIUS Server

def x802_1x_RADIUS_Server_IP_Address(driver,value,index):
    input = driver.find_elements(By.NAME, "rpDot1xServer_ipAddress")[index]
    input.clear()
    input.send_keys(value)

def x802_1x_RADIUS_Server_Port(driver,value,index):
    input = driver.find_elements(By.NAME, "rpDot1xServer_port")[index]
    input.clear()
    input.send_keys(value)

def x802_1x_RADIUS_Server_Secret(driver,value,index):
    input = driver.find_elements(By.NAME, "rpDot1xServer_secret")[index]
    input.clear()
    input.send_keys(value)

def x802_1x_RADIUS_Server_Apply(driver):
    driver.find_element(By.NAME, "rpDot1xServerApply").click()

# 802.1x -> User Profile

def x802_1x_User_Profile_Name(driver,value):
    input = driver.find_element(By.NAME, "rpDot1xUserProf_nameSetup")
    input.clear()
    input.send_keys(value)

def x802_1x_User_Profile_Password(driver,value):
    input = driver.find_element(By.NAME, "rpDot1xUserProf_passwordSetup")
    input.clear()
    input.send_keys(value)

def x802_1x_User_Profile_Retype_Password(driver,value):
    input = driver.find_element(By.NAME, "rpDot1xUserProf_retypePasswordSetup")
    input.clear()
    input.send_keys(value)

def x802_1x_User_Profile_Apply(driver):
    driver.find_element(By.NAME, "rpDot1xUserProfApply").click()

def x802_1x_User_Profile_Delete(driver):
    driver.find_element(By.NAME, "rpDot1xUserProfDelete").click()

# 802.1x -> Port Setting

def x802_1x_Port_Setting_Enable_All(driver,request):
    check_box = driver.find_element(By.NAME, "rpdot1x_portcfg_chkAll_enable")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def x802_1x_Port_Setting_Control_All(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpdot1x_portcfg_sltAll_control']/option[{sel}]").click()

def x802_1x_Port_Setting_Server_Index_All(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpdot1x_portcfg_sltAll_server']/option[{sel}]").click()

def x802_1x_Port_Setting_Auth_Once_All(driver,request):
    check_box = driver.find_element(By.NAME, "rpdot1x_portcfg_chkAll_authonce")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def x802_1x_Port_Setting_Reauth_Period_All(driver,value):
    input = driver.find_element(By.NAME, "rpdot1x_portcfg_All_period")
    input.clear()
    input.send_keys(value)

def x802_1x_Port_Setting_Circuit_ID_All(driver,value):
    input = driver.find_element(By.NAME, "rpdot1x_portcfg_iptAll_circuid_id")
    input.clear()
    input.send_keys(value)

def x802_1x_Port_Setting_Apply(driver):
    driver.find_element(By.NAME, "rpalarm_def_dsl_button_apply").click()

# Loopguard

def Loopguard_LG_Enable_All(driver,request):
    check_box = driver.find_element(By.NAME, "rpacl_lg_iptALL_chk_enable")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Loopguard_Policy_All(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpacl_lg_sltAll_policy']/option[{sel}]").click()

def Loopguard_Recover_Time_All(driver,value):
    input = driver.find_element(By.NAME, "rpacl_lg_iptALL_recover_time")
    input.clear()
    input.send_keys(value)

def Loopguard_Apply(driver):
    driver.find_element(By.NAME, "rpalarm_def_dsl_button_apply").click()

# Packet Filter

def Packet_Filter_Type_All(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rppkfilterAcceptAll']/option[{sel}]").click()

def Packet_Filter_PPPoE_All(driver,request):
    check_box = driver.find_element(By.NAME, "rppkfilterREJECT_PPPoE")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Packet_Filter_IP_All(driver,request):
    check_box = driver.find_element(By.NAME, "rppkfilterREJECT_IP")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Packet_Filter_ARP_All(driver,request):
    check_box = driver.find_element(By.NAME, "rppkfilterREJECT_ARP")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Packet_Filter_NetBIOS_All(driver,request):
    check_box = driver.find_element(By.NAME, "rppkfilterREJECT_NETBIOS")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Packet_Filter_DHCP_All(driver,request):
    check_box = driver.find_element(By.NAME, "rppkfilterREJECT_DHCP")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Packet_Filter_EAPOL_All(driver,request):
    check_box = driver.find_element(By.NAME, "rppkfilterREJECT_EAPOL")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Packet_Filter_IGMP_All(driver,request):
    check_box = driver.find_element(By.NAME, "rppkfilterREJECT_IGMP")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Packet_Filter_Apply(driver):
    driver.find_element(By.NAME, "rppkfilterport_btnApply").click()

# PPPoE

def PPPoE_Option_Policy_Mode(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rppoe_inputOpt82PolicyMode']/option[{sel}]").click()

def PPPoE_Intermediate_Agent_VID(driver,value):
    input = driver.find_element(By.NAME, "rppoe_inputTransparentVID")
    input.clear()
    input.send_keys(value)

def PPPoE_Apply(driver):
    driver.find_elements(By.NAME, "rpAclPPPoETransparentApply")[0].click()

def PPPoE_Intermediate_Agent_Forbidden_VID(driver,value):
    input = driver.find_element(By.NAME, "rppoe_inputForbidenVID")
    input.clear()
    input.send_keys(value)

def PPPoE_Forbidden_Apply(driver):
    driver.find_elements(By.NAME, "rpAclPPPoETransparentApply")[1].click()

def PPPoE_Forbidden_Delete(driver):
    driver.find_element(By.NAME, "rpAclPPPoETransparentDelete").click()

def PPPoE_Select_Format_Circuit_ID_Option_Info(driver,value):
    input = driver.find_element(By.NAME, "rppoe_circuit_id_info")
    input.clear()
    input.send_keys(value)

def PPPoE_Select_Format_Remote_ID_Option_Info(driver,value):
    input = driver.find_element(By.NAME, "rppoe_remote_id_info")
    input.clear()
    input.send_keys(value)

def PPPoE_Select_Option_Policy(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rppoe_opt82_policy']/option[{sel}]").click()

def PPPoE_Select_Option_Linechar(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rppoe_opt82_linechar']/option[{sel}]").click()

def PPPoE_Select_Apply(driver):
    driver.find_element(By.NAME, "rpppoeApply").click()

def PPPoE_Select_Delete(driver):
    driver.find_element(By.NAME, "rpppoeDelete").click()

# ACL Rule

def ACL_Rule_ACL_Profile(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpaclrule_profilename']/option[{sel}]").click()

def ACL_Rule_Priority(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='lctbl_priority']/option[{sel}]").click()

def ACL_Rule_Apply(driver):
    driver.find_element(By.NAME, "rpAclRuleApply").click()

# ACL Egress Rule

# MACFF

# MACFF -> General Setup

def MACFF_New(driver):
    driver.find_element(By.CLASS_NAME, "font-btn").click()

def MACFF_New_Name(driver,value):
    input = driver.find_element(By.NAME, "rpmacff_txtName")
    input.clear()
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
        input.clear()
        input.send_keys(value)
    else:
        input = driver.find_element(By.NAME, f"rpmacff_txtVlan{index}")
        input.clear()
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
        input.clear()
        input.send_keys(value)
    else:
        input = driver.find_element(By.NAME, f"rpmacff_txtArIp{index}")
        input.clear()
        input.send_keys(value)

def MACFF_New_subnet_ip(driver,value,index):
    if(index < 10):
        input = driver.find_element(By.NAME, f"rpmacff_txtSrcIp0{index}")
        input.clear()
        input.send_keys(value)
    else:
        input = driver.find_element(By.NAME, f"rpmacff_txtSrcIp{index}")
        input.clear()
        input.send_keys(value)

def MACFF_New_netmask(driver,value,index):
    if(index < 10):
        input = driver.find_element(By.NAME, f"rpmacff_txtMask0{index}")
        input.clear()
        input.send_keys(value)
    else:
        input = driver.find_element(By.NAME, f"rpmacff_txtMask{index}")
        input.clear()
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

def Multicast_The_multicast_packets_from_upstream_direction_for_IPv4_IPv6(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpaclmc_sltupstream']/option[{sel}]").click()

def Multicast_The_unknown_multicast_packets_for_IPv4(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpaclmc_sltunsolicited']/option[{sel}]").click()

def Multicast_The_IPv6_passthrough(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpaclmc_sltipv6passthrough']/option[{sel}]").click()

def Multicast_The_reserve_multicast_for_IPv4(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpaclmc_sltreserve']/option[{sel}]").click()

def Multicast_Apply(driver):
    driver.find_element(By.NAME, "rpaclmc_btnApply").click()

# BPDU Ctrl

def BPDU_Ctrl_Mode_All(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpbpdu_mode_all']/option[{sel}]").click()

def BPDU_Ctrl_Apply(driver):
    driver.find_element(By.NAME, "rpbpdu_btnApply").click()

# Host Protection

def Host_Protection_ARP(driver,value):
    input = driver.find_element(By.NAME, "rpaclhostprotect_rateArp")
    input.clear()
    input.send_keys(value)

def Host_Protection_BPDU(driver,value):
    input = driver.find_element(By.NAME, "rpaclhostprotect_rateBpdu")
    input.clear()
    input.send_keys(value)

def Host_Protection_DHCP(driver,value):
    input = driver.find_element(By.NAME, "rpaclhostprotect_rateDhcp")
    input.clear()
    input.send_keys(value)

def Host_Protection_DHCPv6(driver,value):
    input = driver.find_element(By.NAME, "rpaclhostprotect_rateDhcpv6")
    input.clear()
    input.send_keys(value)

def Host_Protection_ICMPv6(driver,value):
    input = driver.find_element(By.NAME, "rpaclhostprotect_rateIcmpv6")
    input.clear()
    input.send_keys(value)

def Host_Protection_IGMP(driver,value):
    input = driver.find_element(By.NAME, "rpaclhostprotect_rateIgmp")
    input.clear()
    input.send_keys(value)

def Host_Protection_PPPoE(driver,value):
    input = driver.find_element(By.NAME, "rpaclhostprotect_ratePppoe")
    input.clear()
    input.send_keys(value)

def Host_Protection_Apply(driver):
    driver.find_element(By.NAME, "rpaclhostprotect_btnApply").click()

def Host_Protection_Cancel(driver):
    driver.find_element(By.NAME, "rpaclhostprotect_btnCancel").click()
