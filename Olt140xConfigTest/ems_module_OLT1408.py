from os import times
import time
from attr import field
from pyrsistent import s
import selenium_module as mod
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import web_share.EMS.ems_module as e_mod
import ems_profile_module as e_pro
SUCCESS_TEXT = "uccess"
#print(f"             [ACL - MAC Count] EMS New invalid input: apply msg:{msg}",file = open(file_name, '+a'))

def alert_accept_text(driver, timeout=10):  # 60
    # # try:
    # #     alert = WebDriverWait(driver, 10).until(EC.alert_is_present())    
    # #     msg = alert.text
    # #     alert.accept()    
    # #     return msg
    # # except:
    # #     return "get alert msg fail..."    

    #                                                          #* modify 20230718
    # # try:
    
    # # wait
    # Wait_Block(driver)
    
    # # WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="message_text" and @class="normal_text"]')))
    # try:
    #     WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.ID,"message_text")))                                          #* modify 20230802
    #     msg = get_ems_alert_msg(driver)
    #     alert_accept(driver)   
    # except:
    #     msg = f'timeout {timeout}s no msg'
    # # msg = driver.find_element(By.XPATH,'//*[@id="message_text" and @class="normal_text"]').text   
          
    # return (msg + ' ')
    # # except:
    #     # return "get alert msg fail..."
    return e_mod.alert_accept_text(driver,timeout) 

def Basic_General_Apply(driver,file_name):
    driver.find_element(By.ID, "basic_generalsetup_apply_button").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass

def Basic_General_System(driver,value):
    driver.find_element(By.ID,"basic_generalsetup_hostname_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"basic_generalsetup_hostname_text").send_keys(value)


    
def Basic_General_Location(driver,value):
    driver.find_element(By.ID,"basic_generalsetup_location_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"basic_generalsetup_location_text").send_keys(value)
   
def Basic_General_Contact(driver,value):
    driver.find_element(By.ID,"basic_generalsetup_personname_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"basic_generalsetup_personname_text").send_keys(value)

    
def Basic_General_UseTime(driver,text):
     Select(driver.find_element(By.ID,"basic_generalsetup_timeservertype_select")).select_by_visible_text(text)
   
    
def Basic_General_TimeIP(driver,value):
    driver.find_element(By.ID,"basic_generalsetup_timeserveripaddress_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"basic_generalsetup_timeserveripaddress_text").send_keys(value)

    
def Basic_General_TimeZone(driver,text):
    Select(driver.find_element(By.ID,"basic_generalsetup_timezone_select")).select_by_visible_text(text)

def Basic_General_Daylight(driver,request):
    e_mod.Checkbox_EMS(driver,"basic_generalsetup_daylight_checkbox",request)
   
def Basic_General_StartDate_Week(driver,text):
    Select(driver.find_element(By.ID,"basic_generalsetup_startdate1_select")).select_by_visible_text(text)
   
def Basic_General_StartDate_Day(driver,text):
    Select(driver.find_element(By.ID,"basic_generalsetup_startdate2_select")).select_by_visible_text(text)
    
def Basic_General_StartDate_Month(driver,text):
    Select(driver.find_element(By.ID,"basic_generalsetup_startdate3_select")).select_by_visible_text(text)
    
def Basic_General_StartDate_Hour(driver,text):
    Select(driver.find_element(By.ID,"basic_generalsetup_startdate4_select")).select_by_visible_text(text)
    
def Basic_General_EndDate_Week(driver,text):
    Select(driver.find_element(By.ID,"basic_generalsetup_enddate1_select")).select_by_visible_text(text)
def Basic_General_EndDate_Day(driver,text):
    Select(driver.find_element(By.ID,"basic_generalsetup_enddate2_select")).select_by_visible_text(text)
   
def Basic_General_EndDate_Month(driver,text):
    Select(driver.find_element(By.ID,"basic_generalsetup_enddate3_select")).select_by_visible_text(text)
    
def Basic_General_EndDate_Hour(driver,text):
    Select(driver.find_element(By.ID,"basic_generalsetup_enddate4_select")).select_by_visible_text(text)






def Basic_Switch_Apply(driver,file_name):
    driver.find_element(By.ID,"basic_switch_apply_btn").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass


def Basic_Switch_WRED(driver,request):
    e_mod.Checkbox_EMS(driver,"basic_switch_wredactive_checkbox",request)

def Basic_Switch_Bridge(driver,request):
    e_mod.Checkbox_EMS(driver,"basic_switch_bridgeactive_checkbox",request)

def Basic_Switch_SmartIsolation(driver,request):
    e_mod.Checkbox_EMS(driver,"basic_switch_smartactive_checkbox",request)
    
def Basic_Switch_AgingTime(driver,value):
    driver.find_element(By.ID,"basic_switch_agingiime_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"basic_switch_agingiime_text").send_keys(value)

def Basic_Switch_Downstream_Macro(driver,text):
     Select(driver.find_element(By.ID,"basic_switch_downstreammacro_select")).select_by_visible_text(text)
def Basic_Switch_Downstream_Shaper(driver,text):
     Select(driver.find_element(By.ID,"basic_switch_downstreamshaper_select")).select_by_visible_text(text)
def Basic_Switch_Priority0(driver,text):
     Select(driver.find_element(By.ID,"basic_switch_priority0_select")).select_by_visible_text(text)
def Basic_Switch_Priority1(driver,text):
     Select(driver.find_element(By.ID,"basic_switch_priority1_select")).select_by_visible_text(text)
def Basic_Switch_Priority2(driver,text):
     Select(driver.find_element(By.ID,"basic_switch_priority2_select")).select_by_visible_text(text)
def Basic_Switch_Priority3(driver,text):
     Select(driver.find_element(By.ID,"basic_switch_priority3_select")).select_by_visible_text(text)
def Basic_Switch_Priority4(driver,text):
     Select(driver.find_element(By.ID,"basic_switch_priority4_select")).select_by_visible_text(text)
def Basic_Switch_Priority5(driver,text):
     Select(driver.find_element(By.ID,"basic_switch_priority5_select")).select_by_visible_text(text)
def Basic_Switch_Priority6(driver,text):
     Select(driver.find_element(By.ID,"basic_switch_priority6_select")).select_by_visible_text(text)
def Basic_Switch_Priority7(driver,text):
     Select(driver.find_element(By.ID,"basic_switch_priority7_select")).select_by_visible_text(text)

def Management_IP_Address(driver,IP_Address,IP_Subnet,Defualt,file_name):
    driver.find_element(By.ID,"basic_ip_ipaddress_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"basic_ip_ipaddress_text").send_keys(IP_Address)
    driver.find_element(By.ID,"basic_ip_ipmask_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"basic_ip_ipmask_text").send_keys(IP_Subnet)
    driver.find_element(By.ID,"basic_ip_ipdefaultgateway_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"basic_ip_ipdefaultgateway_text").send_keys(Defualt)
    driver.find_element(By.ID,'basic_ip_apply_btn').click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass


def Basic_IP_Interface(driver,IP_Address,IP_Mask,VID,file_name):
    driver.find_element(By.ID,"basic_ipinterface_ip_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"basic_ipinterface_ip_text").send_keys(IP_Address)
    driver.find_element(By.ID,"basic_ipinterface_mask_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"basic_ipinterface_mask_text").send_keys(IP_Mask)
    driver.find_element(By.ID,"basic_ipinterface_vid_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"basic_ipinterface_vid_text").send_keys(VID)
    time.sleep(2)
    driver.find_element(By.ID,"popupCallBack").click()
    time.sleep(2)
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass
    

#def Basic_IP_New_Management(driver,IP_Address,IP_Mask,Default_Gateway):

def IP_Static_Route(driver,Active,Name,Des_Add,IP_Subnet_Mask,Gateway_Address,Metric,file_name):
    e_mod.Checkbox_EMS(driver,"ip_iproute_active_checkbox",Active)
    driver.find_element(By.ID,"ip_iproute_name_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ip_iproute_name_text").send_keys(Name)
    driver.find_element(By.ID,"ip_iproute_destip_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ip_iproute_destip_text").send_keys(Des_Add)
    driver.find_element(By.ID,"ip_iproute_mask_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ip_iproute_mask_text").send_keys(IP_Subnet_Mask)
    driver.find_element(By.ID,"ip_iproute_gateway_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ip_iproute_gateway_text").send_keys(Gateway_Address)
    driver.find_element(By.ID,"ip_iproute_metric_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ip_iproute_metric_text").send_keys(Metric)
    time.sleep(1)
    driver.find_element(By.ID,"popupCallBack").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass



def Basic_Portset(driver,port,request,name,speed,priority,Control,set_modify_delete,file_name):

    Select(driver.find_element(By.ID,"basic_port_port_combobox")).select_by_visible_text(port)
    time.sleep(2)
    e_mod.Checkbox_EMS(driver,"basic_port_active_checkbox",request)
    time.sleep(2)
    driver.find_element(By.ID,"basic_port_name_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"basic_port_name_text").send_keys(name)
    Select(driver.find_element(By.ID,"basic_port_speed_combobox")).select_by_visible_text(speed)
    Select(driver.find_element(By.ID,"basic_port_priority_combobox")).select_by_visible_text(priority)
    Select(driver.find_element(By.ID,"basic_port_bpdu_combobox")).select_by_visible_text(Control)
    driver.find_element(By.ID,"basic_port_apply_btn").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass
    if_temp_error = False

    if(Select(driver.find_element(By.ID,"basic_port_port_combobox")).first_selected_option.get_attribute("text") == port ):
        print(f"             [EMS1-6448][Basic - Port Setup] EMS {set_modify_delete} {port} port Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6448][Basic - Port Setup] EMS {set_modify_delete} {port} port Fail",file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.ID,"basic_port_active_checkbox").is_selected() == request ):
        print(f"             [EMS1-6448][Basic - Port Setup] EMS {set_modify_delete} {port} Active pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6448][Basic - Port Setup] EMS {set_modify_delete} {port} Active fail",file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.ID,"basic_port_name_text").get_attribute("value") == name ):
        print(f"             [EMS1-6448][Basic - Port Setup] EMS {set_modify_delete} {port} Name pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6448][Basic - Port Setup] EMS {set_modify_delete} {port} Name fail",file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.ID,"basic_port_speed_combobox")).first_selected_option.get_attribute("text") == speed ):
        print(f"             [EMS1-6448][Basic - Port Setup] EMS {set_modify_delete} {port} speed Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6448][Basic - Port Setup] EMS {set_modify_delete} {port} speed Fail",file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.ID,"basic_port_priority_combobox")).first_selected_option.get_attribute("text") == priority ):
        print(f"             [EMS1-6448][Basic - Port Setup] EMS {set_modify_delete} {port} priority Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6448][Basic - Port Setup] EMS {set_modify_delete} {port} priority Fail",file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.ID,"basic_port_bpdu_combobox")).first_selected_option.get_attribute("text") == Control ):
        print(f"             [EMS1-6448][Basic - Port Setup] EMS {set_modify_delete} {port} Control Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6448][Basic - Port Setup] EMS {set_modify_delete} {port} Control Fail",file = open(file_name, '+a'))
        if_temp_error = True
    
    if(if_temp_error==False):
        print(f"             [EMS1-6448][Basic - Port Setup] EMS {set_modify_delete} {port} Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6448][Basic - Port Setup] EMS {set_modify_delete} {port} Result Fail",file = open(file_name, '+a'))

def DHCP_Relay(driver,Active,DHCP1,DHCP2,DHCP3,Relay_Agent,Format,Information,file_name):
    e_mod.Checkbox_EMS(driver,"ip_dhcp_relay_active_checkbox",Active)
    driver.find_element(By.ID,"ip_dhcp_relay_server1_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ip_dhcp_relay_server1_text").send_keys(DHCP1)
    driver.find_element(By.ID,"ip_dhcp_relay_server2_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ip_dhcp_relay_server2_text").send_keys(DHCP2)
    driver.find_element(By.ID,"ip_dhcp_relay_server3_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ip_dhcp_relay_server3_text").send_keys(DHCP3)
    e_mod.Checkbox_EMS(driver,"ip_dhcp_relay_agent_checkbox",Relay_Agent)
    e_mod.Checkbox_EMS(driver,"ip_dhcp_relay_format_checkbox",Format)
    e_mod.Checkbox_EMS(driver,"ip_dhcp_relay_info_checkbox",Information)
    driver.find_element(By.ID,"ip_dhcp_relay_apply_btn").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass
def DHCP_VLAN(driver,VID,DHCP_Status,Pool_Address_or_DHCP_Serner1,Pool_Size_or_DHCP_Server2,Subnet_Mask_or_DHCP_Server3,Default_Gateway_or_Relay_Agent,Primary_DNS_Server_or_Format,Secondary_DNS_Server_or_information,file_name):

    driver.find_element(By.ID,"ip_dhcp_vlan_vid_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ip_dhcp_vlan_vid_text").send_keys(VID)
    if(DHCP_Status=="Server"):
        e_mod.Checkbox_EMS(driver,"ip_dhcp_vlan_status_server_radio",True)
        driver.find_element(By.ID,"ip_dhcp_vlan_address_text").send_keys(Keys.CONTROL + 'a')
        driver.find_element(By.ID,"ip_dhcp_vlan_address_text").send_keys(Pool_Address_or_DHCP_Serner1)
        driver.find_element(By.ID,"ip_dhcp_vlan_pool_text").send_keys(Keys.CONTROL + 'a')
        driver.find_element(By.ID,"ip_dhcp_vlan_pool_text").send_keys(Pool_Size_or_DHCP_Server2)
        driver.find_element(By.ID,"ip_dhcp_vlan_mask_text").send_keys(Keys.CONTROL + 'a')
        driver.find_element(By.ID,"ip_dhcp_vlan_mask_text").send_keys(Subnet_Mask_or_DHCP_Server3)
        driver.find_element(By.ID,"ip_dhcp_vlan_gateway_text").send_keys(Keys.CONTROL + 'a')
        driver.find_element(By.ID,"ip_dhcp_vlan_gateway_text").send_keys(Default_Gateway_or_Relay_Agent)
        driver.find_element(By.ID,"ip_dhcp_vlan_primarydns_text").send_keys(Keys.CONTROL + 'a')
        driver.find_element(By.ID,"ip_dhcp_vlan_primarydns_text").send_keys(Primary_DNS_Server_or_Format)
        driver.find_element(By.ID,"ip_dhcp_vlan_secondarydns_text").send_keys(Keys.CONTROL + 'a')
        driver.find_element(By.ID,"ip_dhcp_vlan_secondarydns_text").send_keys(Secondary_DNS_Server_or_information)
        time.sleep(1)
        driver.find_element(By.ID,"popupCallBack").click()
        time.sleep(2)
        msg = alert_accept_text(driver)
        
        try:
            e_pro.Close(driver)
        except:
            pass
    if(DHCP_Status=="Relay"):
        e_mod.Checkbox_EMS(driver,"ip_dhcp_vlan_status_relay_radio",True)
        driver.find_element(By.ID,"ip_dhcp_vlan_dhcpserver1_text").send_keys(Keys.CONTROL + 'a')
        driver.find_element(By.ID,"ip_dhcp_vlan_dhcpserver1_text").send_keys(Pool_Address_or_DHCP_Serner1)
        driver.find_element(By.ID,"ip_dhcp_vlan_dhcpserver2_text").send_keys(Keys.CONTROL + 'a')
        driver.find_element(By.ID,"ip_dhcp_vlan_dhcpserver2_text").send_keys(Pool_Address_or_DHCP_Serner1)
        driver.find_element(By.ID,"ip_dhcp_vlan_dhcpserver3_text").send_keys(Keys.CONTROL + 'a')
        driver.find_element(By.ID,"ip_dhcp_vlan_dhcpserver3_text").send_keys(Pool_Address_or_DHCP_Serner1)
        e_mod.Checkbox_EMS(driver,"ip_dhcp_vlan_agent_active_checkbox",Default_Gateway_or_Relay_Agent)
        e_mod.Checkbox_EMS(driver,"ip_dhcp_vlan_format_active_checkbox",Primary_DNS_Server_or_Format)
        e_mod.Checkbox_EMS(driver,"ip_dhcp_vlan_information_active_checkbox",Secondary_DNS_Server_or_information)
        time.sleep(1)
        driver.find_element(By.ID,"popupCallBack").click()
        time.sleep(2)
        msg = alert_accept_text(driver)
        
        try:
            e_pro.Close(driver)
        except:
            pass

def DHCP_L2(driver,VID,Circuit_Id82,Remote_Id82,Interface_Id18,Remote_Id37,ENABLE):
    driver.find_element(By.ID,"ip_dhcp_agent_vid_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ip_dhcp_agent_vid_text").send_keys(VID)
    driver.find_element(By.ID,"ip_dhcp_agent_circuit_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ip_dhcp_agent_circuit_text").send_keys(Circuit_Id82)
    driver.find_element(By.ID,"ip_dhcp_agent_remote82_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ip_dhcp_agent_remote82_text").send_keys(Remote_Id82)
    driver.find_element(By.ID,"ip_dhcp_agent_interface_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ip_dhcp_agent_interface_text").send_keys(Interface_Id18)
    driver.find_element(By.ID,"ip_dhcp_agent_remote37_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"ip_dhcp_agent_remote37_text").send_keys(Remote_Id37)
    e_mod.Checkbox_EMS(driver,"ip_dhcp_agent_ldra_active_checkbox",ENABLE)
    time.sleep(2)
    driver.find_element(By.ID,"popupCallBack").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass

def VLAN_Port_isolation(driver,request,file_name):
    e_mod.Checkbox_EMS(driver,"advance_vlan_port_isolation_checkbox",request)
    driver.find_element(By.ID,"advance_vlan_sys_apply_btn").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass

def VLAN_Port_Setting(driver,Port,Ingress_Check,PVID,Frame_Type,VLAN_Trunking,file_name):
    Select(driver.find_element(By.ID,"advance_vlan_port_combobox")).select_by_visible_text(Port)
    time.sleep(2)
    e_mod.Checkbox_EMS(driver,"advance_vlan_port_ingress_checkbox",Ingress_Check)
    driver.find_element(By.ID,"advance_vlan_port_pvid_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_vlan_port_pvid_text").send_keys(PVID)
    Select(driver.find_element(By.ID,"advance_vlan_port_acceptable_combobox")).select_by_visible_text(Frame_Type)
    e_mod.Checkbox_EMS(driver,"advance_vlan_port_trunking_checkbox",VLAN_Trunking)
    driver.find_element(By.ID,"advance_vlan_port_apply_btn").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass

def VLAN_Subnet_Based_Apply(driver,Active,DHCP_VLAN_Override,file_name):
    e_mod.Checkbox_EMS(driver,"advance_vlan_subnet_checkbox",Active)
    time.sleep(2)
    e_mod.Checkbox_EMS(driver,"advance_vlan_override_checkbox",DHCP_VLAN_Override)
    time.sleep(2)
    driver.find_element(By.ID,"advance_vlan_subnet_apply_btn").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass

def VLAN_Subnet_Based(driver,Active,Name,IP,Mask_Bits,VID,Priority,file_name):
    time.sleep(2)
    e_mod.Checkbox_EMS(driver,"advance_vlan_subnet_active_checkbox",Active)
    driver.find_element(By.ID,"advance_vlan_subnet_name_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_vlan_subnet_name_text").send_keys(Name)
    driver.find_element(By.ID,"advance_vlan_subnet_ip_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_vlan_subnet_ip_text").send_keys(IP)
    driver.find_element(By.ID,"advance_vlan_subnet_mask_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_vlan_subnet_mask_text").send_keys(Mask_Bits)
    driver.find_element(By.ID,"advance_vlan_subnet_vid_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_vlan_subnet_vid_text").send_keys(VID)
    Select(driver.find_element(By.ID,"advance_vlan_subnet_priority_combobox")).select_by_visible_text(Priority)
    time.sleep(2)
    driver.find_element(By.ID,"popupCallBack").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass

def Protocol_Based_VLAN(driver,Active,Port,Name,first_second,Ethernet_type,VID,Priority,file_name):
    e_mod.Checkbox_EMS(driver,"advance_vlan_protocol_active_checkbox",Active)
    Select(driver.find_element(By.ID,"advance_vlan_protocol_port_combobox")).select_by_visible_text(Port)
    driver.find_element(By.ID,"advance_vlan_protocol_name_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_vlan_protocol_name_text").send_keys(Name)
    if(first_second == "first"):
        e_mod.Checkbox_EMS(driver,"advance_vlan_protocol_ethtype1_radio",True)
        Select(driver.find_element(By.ID,"advance_vlan_protocol_ethtype1_combobox")).select_by_visible_text(Ethernet_type)
    elif(first_second == "second"):
        e_mod.Checkbox_EMS(driver,"advance_vlan_protocol_ethtype2_radio",True)
        driver.find_element(By.ID,"advance_vlan_protocol_ethtype_text").send_keys(Keys.CONTROL + 'a')
        driver.find_element(By.ID,"advance_vlan_protocol_ethtype_text").send_keys(Ethernet_type)
    driver.find_element(By.ID,"advance_vlan_protocol_vid_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_vlan_protocol_vid_text").send_keys(VID)
    Select(driver.find_element(By.ID,"advance_vlan_protocol_priority_combobox")).select_by_visible_text(Priority)
    time.sleep(2)
    driver.find_element(By.XPATH,'//*[@id="popupCallBack"]').click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass

def VLAN_Static_VLAN(driver,Active,Name,VLAN_ID,Fixed_Forbidden,Tagging,file_name):
    e_mod.Checkbox_EMS(driver,"advance_vlan_static_active",Active)
    driver.find_element(By.ID,"advance_vlan_static_name").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_vlan_static_name").send_keys(Name)
    driver.find_element(By.ID,"advance_vlan_static_vid").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_vlan_static_vid").send_keys(VLAN_ID)
    if(Fixed_Forbidden=="Fixed"):
        e_mod.Checkbox_EMS(driver,"advance_vlan_static_fixed_all",True)
    else:
        e_mod.Checkbox_EMS(driver,"advance_vlan_static_forbidden_all",True)
    if(Tagging=="Tagging"):
        e_mod.Checkbox_EMS(driver,"advance_vlan_static_tagging_all",True)

    time.sleep(2)
    driver.find_element(By.ID,"popupCallBack").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass

def Advanced_Static_Multicast(driver,Active,MAC_Address,VID,Port):
    e_mod.Checkbox_EMS(driver,"advance_staticmulticastforward_active_checkbox",Active)
    driver.find_element(By.ID,"advance_staticmulticastforward_mac_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_staticmulticastforward_mac_text").send_keys(MAC_Address)
    driver.find_element(By.ID,"advance_staticmulticastforward_vid_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_staticmulticastforward_vid_text").send_keys(VID)
    driver.find_element(By.ID,"advance_staticmulticastforward_port_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_staticmulticastforward_port_text").send_keys(Port)
    time.sleep(2)
    driver.find_element(By.ID,"popupCallBack").click()
    time.sleep(2)

def Advanced_Filtering(driver,Active,Name,Action,MAC_Address,VID):
    e_mod.Checkbox_EMS(driver,"advance_filtering_active_checkbox",Active)
    driver.find_element(By.ID,"advance_filtering_name_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_filtering_name_text").send_keys(Name)
    if(Action == "Discard source"):
        e_mod.Checkbox_EMS(driver,"advance_filtering_action_source_checkbox",True)
    if(Action == "Discard destination"):
        e_mod.Checkbox_EMS(driver,"advance_filtering_action_destination_checkbox",True)
    if(Action == "Discard both"):
        e_mod.Checkbox_EMS(driver,"advance_filtering_action_source_checkbox",True)
        e_mod.Checkbox_EMS(driver,"advance_filtering_action_destination_checkbox",True)
    driver.find_element(By.ID,"advance_filtering_mac_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_filtering_mac_text").send_keys(MAC_Address)
    driver.find_element(By.ID,"advance_filtering_vid_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_filtering_vid_text").send_keys(VID)
    time.sleep(2)
    driver.find_element(By.ID,"popupCallBack").click()
    time.sleep(2)

def Advanced_Broadcast_Apply(driver,Active,file_name):
    e_mod.Checkbox_EMS(driver,"advance_broadcaststorm_active_checkbox",Active)
    driver.find_element(By.ID,"advance_broadcaststorm_sys_apply_btn").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass

def Advanced_Broadcast_port_Apply(driver,Port,Counter_Active,Logging_Active,Broadcast_Active,Broadcast,Multicast_Active,Multicast,DLF_Active,DLF,file_name):
    Select(driver.find_element(By.ID,"advance_broadcaststorm_port_combobox")).select_by_visible_text(Port)
    time.sleep(2)
    e_mod.Checkbox_EMS(driver,"advance_broadcaststorm_counteractive_checkbox",Counter_Active)
    time.sleep(2)
    e_mod.Checkbox_EMS(driver,"advance_broadcaststorm_loggingactive_checkbox",Logging_Active)
    time.sleep(2)
    e_mod.Checkbox_EMS(driver,"advance_broadcaststorm_broadcastactive_checkbox",Broadcast_Active)
    driver.find_element(By.ID,"advance_broadcaststorm_broadcast_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_broadcaststorm_broadcast_text").send_keys(Broadcast)
    time.sleep(2)
    e_mod.Checkbox_EMS(driver,"advance_broadcaststorm_multicastactive_checkbox",Multicast_Active)
    driver.find_element(By.ID,"advance_broadcaststorm_multicast_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_broadcaststorm_multicast_text").send_keys(Multicast)
    time.sleep(2)
    e_mod.Checkbox_EMS(driver,"advance_broadcaststorm_dlfactive_checkbox",DLF_Active)
    driver.find_element(By.ID,"advance_broadcaststorm_dlf_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_broadcaststorm_dlf_text").send_keys(DLF)
    driver.find_element(By.ID,"advance_broadcaststorm_apply_btn").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass

def Advanced_LinkAggregation_Apply(driver,LACP_Active,LACP_Ststem_Priority,file_name):
    e_mod.Checkbox_EMS(driver,"advance_link_lacpactive_checkbox",LACP_Active)
    driver.find_element(By.ID,"advance_link_lacpsystempriority_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_link_lacpsystempriority_text").send_keys(LACP_Ststem_Priority)
    driver.find_element(By.ID,"advance_link_sysapply_btn").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass
    time.sleep(2)


def Advanced_LinkAggregation_GroupApply(driver,Group_ID,Active,Criteria,LACP_Active,file_name):
    Select(driver.find_element(By.ID,"advance_link_groupid_combobox")).select_by_visible_text(Group_ID)
    time.sleep(2)
    e_mod.Checkbox_EMS(driver,"advance_link_groupactive_checkbox",Active)
    Select(driver.find_element(By.ID,"advance_link_groupcriteria_combobox")).select_by_visible_text(Criteria)
    e_mod.Checkbox_EMS(driver,"advance_link_grouplacpactive_checkbox",LACP_Active)
    driver.find_element(By.ID,"advance_link_groupapply_btn").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass
    time.sleep(2)

def Advanced_LinkAggregation_PortApply(driver,Port,Group,LACP_Timeout,file_name):
    Select(driver.find_element(By.ID,"advance_link_port_combobox")).select_by_visible_text(Port)
    time.sleep(2)
    Select(driver.find_element(By.ID,"advance_link_portgroup_combobox")).select_by_visible_text(Group)
    Select(driver.find_element(By.ID,"advance_link_portlacptimeout_combobox")).select_by_visible_text(LACP_Timeout)
    driver.find_element(By.ID,"advance_link_portapply_btn").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass
    time.sleep(2)

def Advanced_PortSecurity_Apply(driver,Port_Security,Anti_Mac_Spoof,file_name):
    e_mod.Checkbox_EMS(driver,"advance_security_security_checkbox",Port_Security)
    time.sleep(2)
    e_mod.Checkbox_EMS(driver,"advance_security_antispoof_checkbox",Anti_Mac_Spoof)
    driver.find_element(By.ID,"advance_security_sysapply_btn").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass
    time.sleep(2)

def Advanced_PortSecurity_PortApply(driver,Port,Port_Security_Active,Anti_Mac_Spoof,Address_Learning,Limited_Number_MACaddress,file_name):
    Select(driver.find_element(By.ID,"advance_security_port_combobox")).select_by_visible_text(Port)
    time.sleep(2)
    e_mod.Checkbox_EMS(driver,"advance_security_portactive_checkbox",Port_Security_Active)
    if(Port =="PON 1" or "PON 2" or "PON 3" or "PON 4"):
        e_mod.Checkbox_EMS(driver,"advance_security_portantispoof_checkbox",Anti_Mac_Spoof)
    e_mod.Checkbox_EMS(driver,"advance_security_portaddress_checkbox",Address_Learning)
    driver.find_element(By.ID,"advance_security_portmaclimit_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_security_portmaclimit_text").send_keys(Limited_Number_MACaddress)
    driver.find_element(By.ID,"advance_security_groupapply_btn").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass
    time.sleep(2)

def Advanced_Classifier(driver,Active,Name,Packet_Formet,VLAN,Priority,Ethernet_Type,Type_Number,Source_MAC,Source_Port,Destination_MAC,Destination_Port,DSCP,IP_Protocol,Establish_Dec,IP_Type,Source_IP,Source_Address,Source_Socket,Destination_IP,Destination_Address,Destination_Socket,file_name):
    e_mod.Checkbox_EMS(driver,"advance_classifier_active_checkbox",Active)
    driver.find_element(By.ID,"advance_classifier_name_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_classifier_name_text").send_keys(Name)
    Select(driver.find_element(By.ID,"advance_classifier_packet_combobox")).select_by_visible_text(Packet_Formet)
    if(VLAN == "Any"):
        e_mod.Checkbox_EMS(driver,"advance_classifier_vlan_any_radio",True)
    else:
        e_mod.Checkbox_EMS(driver,"advance_classifier_vlan_radio",True)
        driver.find_element(By.ID,"advance_classifier_vlan_vlan_text").send_keys(Keys.CONTROL + 'a')
        driver.find_element(By.ID,"advance_classifier_vlan_vlan_text").send_keys(VLAN)
    if(Priority == "Any"):
        e_mod.Checkbox_EMS(driver,"advance_classifier_priority_any_radio",True)
    else:
        e_mod.Checkbox_EMS(driver,"advance_classifier_priority_radio",True)
        Select(driver.find_element(By.ID,"advance_classifier_priority_combobox")).select_by_visible_text(Priority)
    if(Ethernet_Type == "Type"):
        e_mod.Checkbox_EMS(driver,"advance_classifier_ethernet_type_radio",True)
        Select(driver.find_element(By.ID,"advance_classifier_ethernet_combobox")).select_by_visible_text(Type_Number)
    else:
        e_mod.Checkbox_EMS(driver,"advance_classifier_ethernet_other_radio",True)
        driver.find_element(By.ID,"advance_classifier_ethernet_other_text").send_keys(Keys.CONTROL + 'a')
        driver.find_element(By.ID,"advance_classifier_ethernet_other_text").send_keys(Type_Number)
    if(Source_MAC == "Any"):
        e_mod.Checkbox_EMS(driver,"advance_classifier_source_mac_any_radio",True)
    else:
        e_mod.Checkbox_EMS(driver,"advance_classifier_source_mac_radio",True)
        driver.find_element(By.ID,"advance_classifier_source_mac_text").send_keys(Keys.CONTROL + 'a')
        driver.find_element(By.ID,"advance_classifier_source_mac_text").send_keys(Source_MAC)
    if(Source_Port == "Any"):
        e_mod.Checkbox_EMS(driver,"advance_classifier_source_port_any_radio",True)
    else:
        e_mod.Checkbox_EMS(driver,"advance_classifier_source_port_radio",True)
        driver.find_element(By.ID,"advance_classifier_source_port_text").send_keys(Keys.CONTROL + 'a')
        driver.find_element(By.ID,"advance_classifier_source_port_text").send_keys(Source_Port)
    if(Destination_MAC == "Any"):
        e_mod.Checkbox_EMS(driver,"advance_classifier_destination_mac_any_radio",True)
    else:
        e_mod.Checkbox_EMS(driver,"advance_classifier_destination_mac_radio",True)
        driver.find_element(By.ID,"advance_classifier_destination_mac_text").send_keys(Keys.CONTROL + 'a')
        driver.find_element(By.ID,"advance_classifier_destination_mac_text").send_keys(Destination_MAC)
    if(Destination_Port == "Any"):
        e_mod.Checkbox_EMS(driver,"advance_classifier_destination_port_any_radio",True)
    else:
        e_mod.Checkbox_EMS(driver,"advance_classifier_destination_port_radio",True)
        driver.find_element(By.ID,"advance_classifier_destination_port_text").send_keys(Keys.CONTROL + 'a')
        driver.find_element(By.ID,"advance_classifier_destination_port_text").send_keys(Destination_Port)
    if(DSCP == "Any"):
        e_mod.Checkbox_EMS(driver,"advance_classifier_dscp_any_radio",True)
    else:
        e_mod.Checkbox_EMS(driver,"advance_classifier_dscp_dscp_radio",True)
        driver.find_element(By.ID,"advance_classifier_dscp_dscp_text").send_keys(Keys.CONTROL + 'a')
        driver.find_element(By.ID,"advance_classifier_dscp_dscp_text").send_keys(DSCP)
    if(IP_Protocol == "Others"):
        e_mod.Checkbox_EMS(driver,"advance_classifier_protocol_other_radio",True)
        driver.find_element(By.ID,"advance_classifier_protocol_other_text").send_keys(Keys.CONTROL + 'a')
        driver.find_element(By.ID,"advance_classifier_protocol_other_text").send_keys(Establish_Dec)
    else:
        e_mod.Checkbox_EMS(driver,"advance_classifier_protocol_type_radio",True)
        Select(driver.find_element(By.ID,"advance_classifier_protocol_type_combobox")).select_by_visible_text(IP_Protocol)
        e_mod.Checkbox_EMS(driver,"advance_classifier_establish_checkbox",Establish_Dec)
    if(IP_Type == "IPv4"):
        e_mod.Checkbox_EMS(driver,"advance_classifier_iptype_ipv4_radio",True)
    else:
        e_mod.Checkbox_EMS(driver,"advance_classifier_iptype_ipv6_radio",True)
    
    driver.find_element(By.ID,"advance_classifier_source_ip_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_classifier_source_ip_text").send_keys(Source_IP)
    driver.find_element(By.ID,"advance_classifier_source_prefix_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_classifier_source_prefix_text").send_keys(Source_Address)
    if(Source_Socket == "Any"):
        e_mod.Checkbox_EMS(driver,"advance_classifier_source_socket_any_radio",True)
    else:
        e_mod.Checkbox_EMS(driver,"advance_classifier_source_socket_number_radio",True)
        driver.find_element(By.ID,"advance_classifier_source_socket_text").send_keys(Keys.CONTROL + 'a')
        driver.find_element(By.ID,"advance_classifier_source_socket_text").send_keys(Source_Socket)

    driver.find_element(By.ID,"advance_classifier_destination_ip_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_classifier_destination_ip_text").send_keys(Destination_IP)
    driver.find_element(By.ID,"advance_classifier_destination_prefix_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_classifier_destination_prefix_text").send_keys(Destination_Address)
    if(Destination_Socket == "Any"):
        e_mod.Checkbox_EMS(driver,"advance_classifier_destination_socket_any_radio",True)
    else:
        e_mod.Checkbox_EMS(driver,"advance_classifier_destination_socket_number_radio",True)
        driver.find_element(By.ID,"advance_classifier_destination_socket_text").send_keys(Keys.CONTROL + 'a')
        driver.find_element(By.ID,"advance_classifier_destination_socket_text").send_keys(Destination_Socket)
    time.sleep(2)
    driver.find_element(By.ID,"popupCallBack").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass
    time.sleep(2)

def Advanced_Policy(driver,Active,Name,Egress_port,Mirror_port,file_name):
    e_mod.Checkbox_EMS(driver,"advance_policy_active_checkbox",Active)
    driver.find_element(By.ID,"advance_policy_name_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_policy_name_text").send_keys(Name)
    for i in range(1,driver.find_elements(By.NAME,"advance_policy_classifier_checkbox").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/div[6]/div[1]/div[2]/div[1]/div/div[3]/div[2]/div/div[{i+1}]/div[1]").text
        if(ele == Name):
            driver.find_element(By.XPATH,f"/html/body/div[6]/div[1]/div[2]/div[1]/div/div[3]/div[2]/div/div[{i+1}]/div[2]/label").click()
            time.sleep(2)
    
    Select(driver.find_element(By.ID,"advance_policy_egressport_combobox")).select_by_visible_text(Egress_port)
    Select(driver.find_element(By.ID,"advance_policy_mirrorport_combobox")).select_by_visible_text(Mirror_port)
    e_mod.Checkbox_EMS(driver,"advance_policy_forward2_radio",True)
    driver.find_element(By.ID,"popupCallBack").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass
    time.sleep(2)

def Advanced_Queue(driver,Port,Method,Q0,Q1,Q2,Q3,Q4,Q5,Q6,Q7,Lowest_Queue,file_name):
    Select(driver.find_element(By.ID,"advance_queue_port_combobox")).select_by_visible_text(Port)
    time.sleep(2)
    if(Method == "SPQ"):
        e_mod.Checkbox_EMS(driver,"advance_queue_method_SPQ_radio",True)
    else:
        e_mod.Checkbox_EMS(driver,"advance_queue_method_WFQ_radio",True)
    driver.find_element(By.ID,"advance_queue_q0_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_queue_q0_text").send_keys(Q0)
    driver.find_element(By.ID,"advance_queue_q1_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_queue_q1_text").send_keys(Q1)
    driver.find_element(By.ID,"advance_queue_q2_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_queue_q2_text").send_keys(Q2)
    driver.find_element(By.ID,"advance_queue_q3_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_queue_q3_text").send_keys(Q3)
    driver.find_element(By.ID,"advance_queue_q4_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_queue_q4_text").send_keys(Q4)
    driver.find_element(By.ID,"advance_queue_q5_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_queue_q5_text").send_keys(Q5)
    driver.find_element(By.ID,"advance_queue_q6_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_queue_q6_text").send_keys(Q6)
    driver.find_element(By.ID,"advance_queue_q7_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_queue_q7_text").send_keys(Q7)
    Select(driver.find_element(By.ID,"advance_queue_lowestqueue_combobox")).select_by_visible_text(Lowest_Queue)
    driver.find_element(By.ID,"advance_queue_groupapply_btn").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass
    time.sleep(2)
    
def Advanced_VLAN_Stacking(driver,Port,Role,Tunnel,SPVID,Priority,file_name):
    Select(driver.find_element(By.ID,"advance_vlanstacking_port_combobox")).select_by_visible_text(Port)
    time.sleep(2)
    Select(driver.find_element(By.ID,"advance_vlanstacking_role_combobox")).select_by_visible_text(Role)
    driver.find_element(By.ID,"advance_vlanstacking_tpid_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_vlanstacking_tpid_text").send_keys(Tunnel)
    driver.find_element(By.ID,"advance_vlanstacking_spvid_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_vlanstacking_spvid_text").send_keys(SPVID)
    Select(driver.find_element(By.ID,"advance_vlanstacking_priority_combobox")).select_by_visible_text(Priority)
    driver.find_element(By.ID,"advance_vlanstacking_apply_btn").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass
    time.sleep(2)

def Advanced_Multicast_Port_Apply(driver,Port,Immed_Leave,IGMP,file_name):
    Select(driver.find_element(By.ID,"advance_multicast_port_combobox")).select_by_visible_text(Port)
    time.sleep(2)
    e_mod.Checkbox_EMS(driver,"advance_multicast_leave_checkbox",Immed_Leave)
    if(IGMP == "None"):
        driver.find_element(By.ID,"advance_multicast_portapply_btn").click()
        time.sleep(2)
        msg = alert_accept_text(driver)
    else:
        Select(driver.find_element(By.ID,"advance_multicast_igmpquerier_combobox")).select_by_visible_text(IGMP)
        print(f"            XXXXXXXXXXXXXXXXXX",file = open(file_name, '+a'))
        driver.find_element(By.ID,"advance_multicast_portapply_btn").click()
        time.sleep(2)
        msg = alert_accept_text(driver)
    try:
        e_pro.Close(driver)
    except:
        pass
        time.sleep(2)

def Advanced_Multicast_Mode_Apply(driver,Active,MLD,Host_Timeout,Leave_Timeout,Priority,Mode,Frame,Group,Report_Tag,Query_Tag,file_name):
    if(Active == "None"):
        e_mod.Checkbox_EMS(driver,"advance_multicast_active_none_radio",True)
    elif(Active == "Snooping"):
        e_mod.Checkbox_EMS(driver,"advance_multicast_active_snooping_radio",True)
    elif(Active == "Proxy"):
        e_mod.Checkbox_EMS(driver,"advance_multicast_active_proxy_radio",True)

    e_mod.Checkbox_EMS(driver,"advance_multicast_mld_checkbox",MLD)
    driver.find_element(By.ID,"advance_multicast_hosttimeout_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_multicast_hosttimeout_text").send_keys(Host_Timeout)
    driver.find_element(By.ID,"advance_multicast_leavetimeout_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_multicast_leavetimeout_text").send_keys(Leave_Timeout)
    Select(driver.find_element(By.ID,"advance_multicast_priority_combobox")).select_by_visible_text(Priority)
    e_mod.Checkbox_EMS(driver,"advance_multicast_mgmdv3_checkbox",Mode)
    if(Frame == "Flooding"):
        e_mod.Checkbox_EMS(driver,"advance_multicast_unknown_flooding_radio",True)
    elif(Frame == "Drop"):
        e_mod.Checkbox_EMS(driver,"advance_multicast_unknown_drop_radio",True)
    if(Group == "Flooding"):
        e_mod.Checkbox_EMS(driver,"advance_multicast_reserved_flooding_radio",True)
    elif(Frame == "Drop"):
        e_mod.Checkbox_EMS(driver,"advance_multicast_reserved_drop_radio",True)
    if(Report_Tag == "Mvlan"):
        e_mod.Checkbox_EMS(driver,"advance_multicast_report_mvlan_radio",True)
    elif(Report_Tag == "Ani vlan"):
        e_mod.Checkbox_EMS(driver,"advance_multicast_report_anivlan_radio",True)
    if(Query_Tag == "Mvlan"):
        e_mod.Checkbox_EMS(driver,"advance_multicast_query_mvlan_radio",True)
    elif(Query_Tag == "Ani vlan"):
        e_mod.Checkbox_EMS(driver,"advance_multicast_query_anivlan_radio",True)
    driver.find_element(By.ID,"advance_multicast_apply_btn").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass
    time.sleep(2)

def Advanced_Multicast_Channel(driver,Active,start_group_ip,end_group_ip,VLAN,pbit,src_ip,package_member,preview_duration,preview_count,preview_blackout,file_name):
    e_mod.Checkbox_EMS(driver,"advance_multicast_channel_active_checkbox",Active)
    driver.find_element(By.ID,"advance_multicast_channel_startgroupip_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_multicast_channel_startgroupip_text").send_keys(start_group_ip)
    driver.find_element(By.ID,"advance_multicast_channel_endgroupip_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_multicast_channel_endgroupip_text").send_keys(end_group_ip)
    driver.find_element(By.ID,"advance_multicast_channel_vlan_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_multicast_channel_vlan_text").send_keys(VLAN)
    Select(driver.find_element(By.ID,"advance_multicast_channel_pbit_combobox")).select_by_visible_text(pbit)
    driver.find_element(By.ID,"advance_multicast_channel_srcip_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_multicast_channel_srcip_text").send_keys(src_ip)
    driver.find_element(By.ID,"advance_multicast_channel_package_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_multicast_channel_package_text").send_keys(package_member)
    driver.find_element(By.ID,"advance_multicast_channel_duration_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_multicast_channel_duration_text").send_keys(preview_duration)
    driver.find_element(By.ID,"advance_multicast_channel_count_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_multicast_channel_count_text").send_keys(preview_count)
    driver.find_element(By.ID,"advance_multicast_channel_blackout_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_multicast_channel_blackout_text").send_keys(preview_blackout)
    time.sleep(2)
    driver.find_element(By.ID,"popupCallBack").click()
    time.sleep(2)
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass
    time.sleep(2)

def Advanced_IP_Source(driver,Active,DHCP,file_name):
    e_mod.Checkbox_EMS(driver,"advance_ipsg_snooping_active_checkbox",Active)
    if(DHCP == "Disable"):
        e_mod.Checkbox_EMS(driver,"advance_ipsg_snooping_dhcpvlan_disable_radio",True)
    else:
        e_mod.Checkbox_EMS(driver,"advance_ipsg_snooping_dhcpvlan_vlan_radio",True)
        driver.find_element(By.ID,"advance_ipsg_snooping_dhcpvlan_vlan_text").send_keys(Keys.CONTROL + 'a')
        driver.find_element(By.ID,"advance_ipsg_snooping_dhcpvlan_vlan_text").send_keys(DHCP)
        driver.find_element(By.ID,"advance_ipsg_snooping_apply_btn").click()
        time.sleep(2)
        msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass
        time.sleep(2)
    
def Advanced_DHCP_Snooping(driver,Port,Server_Trusted_state,Rate,file_name):
    Select(driver.find_element(By.ID,"advance_ipsg_snooping_port_combobox")).select_by_visible_text(Port)
    time.sleep(2)
    Select(driver.find_element(By.ID,"advance_ipsg_snooping_port_server_combobox")).select_by_visible_text(Server_Trusted_state)
    driver.find_element(By.ID,"advance_ipsg_snooping_port_rate_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_ipsg_snooping_port_rate_text").send_keys(Rate)
    driver.find_element(By.ID,"advance_ipsg_snooping_port_apply_btn").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass
    time.sleep(2)

def Advanced_Static_Binding(driver,MAC_Address,IP_Address,VLAN,Port,file_name):
    driver.find_element(By.ID,"advance_ipsg_static_mac_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_ipsg_static_mac_text").send_keys(MAC_Address)
    driver.find_element(By.ID,"advance_ipsg_static_address_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_ipsg_static_address_text").send_keys(IP_Address)
    driver.find_element(By.ID,"advance_ipsg_static_vlan_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_ipsg_static_vlan_text").send_keys(VLAN)
    if(Port == "Any"):
        e_mod.Checkbox_EMS(driver,"advance_ipsg_static_port_any_radio",True)
    else:
        e_mod.Checkbox_EMS(driver,"advance_ipsg_static_port_radio",True)
        driver.find_element(By.ID,"advance_ipsg_static_port_text").send_keys(Keys.CONTROL + 'a')
        driver.find_element(By.ID,"advance_ipsg_static_port_text").send_keys(Port)
    time.sleep(2)
    driver.find_element(By.ID,"popupCallBack").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass
    time.sleep(2)

def Advanced_VLAN_Configure(driver,Star_VLAN,End_VLAN):
    driver.find_element(By.ID,"advance_ipsg_vlan_startvid_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_ipsg_vlan_startvid_text").send_keys(Star_VLAN)
    driver.find_element(By.ID,"advance_ipsg_vlan_endvid_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_ipsg_vlan_endvid_text").send_keys(End_VLAN)
    driver.find_element(By.ID,"advance_ipsg_vlan_add_apply_btn").click()
    time.sleep(2)

def Advanced_VLAN_Configure_Table(driver,VLAN,Enabled,Option82,Information,file_name):
    Select(driver.find_element(By.ID,f"advance_ipsg_vlan_enabled_select_{VLAN}")).select_by_visible_text(Enabled)
    e_mod.Checkbox_EMS(driver,f"advance_ipsg_vlan_option82_checkbox_{VLAN}",Option82)
    e_mod.Checkbox_EMS(driver,f"advance_ipsg_vlan_information_checkbox_{VLAN}",Information)
    driver.find_element(By.ID,"advance_ipsg_vlan_apply_btn").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass
    time.sleep(2)

def Advanced_Loop_Guard_Apply(driver,Active,Detection,file_name):
    e_mod.Checkbox_EMS(driver,"advance_loopguard_state_checkbox",Active)
    driver.find_element(By.ID,"advance_loopguard_detection_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_loopguard_detection_text").send_keys(Detection)
    driver.find_element(By.ID,"advance_loopguard_sysapply_btn").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass
    time.sleep(2)

def Advanced_Loop_Guard_Port_Apply(driver,Port,Active,VID,file_name):
    Select(driver.find_element(By.ID,"advance_loopguard_port_combobox")).select_by_visible_text(Port)
    time.sleep(2)
    e_mod.Checkbox_EMS(driver,"advance_loopguard_portstate_checkbox",Active)
    driver.find_element(By.ID,"advance_loopguard_portvid_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_loopguard_portvid_text").send_keys(VID)
    driver.find_element(By.ID,"advance_loopguard_apply_btn").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass
    time.sleep(2)

def Advanced_PPPoE_IA_Apply(driver,Active,file_name):
    e_mod.Checkbox_EMS(driver,"advance_pppoe_pppoeia_active_checkbox",Active)
    driver.find_element(By.ID,"advance_pppoe_pppoeia_apply_btn").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass
    time.sleep(2)

def Advanced_PPPoE_IA_Option(driver,VID,Option_Circuit_Id,Option_Remote_Id,file_name):
    driver.find_element(By.ID,"advance_pppoe_option_vid_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_pppoe_option_vid_text").send_keys(VID)
    driver.find_element(By.ID,"advance_pppoe_option_circuit_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_pppoe_option_circuit_text").send_keys(Option_Circuit_Id)
    driver.find_element(By.ID,"advance_pppoe_option_remote_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_pppoe_option_remote_text").send_keys(Option_Remote_Id)
    time.sleep(2)
    driver.find_element(By.ID,"popupCallBack").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass
    time.sleep(2)

def Advanced_PPPoE_Port_Apply(driver,Port,Server_Trusted_State,file_name):
    Select(driver.find_element(By.ID,"advance_pppoe_port_combobox")).select_by_visible_text(Port)
    time.sleep(2)
    Select(driver.find_element(By.ID,"advance_pppoe_port_trust_combobox")).select_by_visible_text(Server_Trusted_State)
    driver.find_element(By.ID,"advance_pppoe_port_apply_btn").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass
    time.sleep(2)

def Advanced_PPPoE_VLAN(driver,Star_ID,End_ID,Enable,Circuit_id,Remote_id,file_name):
    driver.find_element(By.ID,"advance_pppoe_vlan_startvid_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_pppoe_vlan_startvid_text").send_keys(Star_ID)
    driver.find_element(By.ID,"advance_pppoe_vlan_endvid_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"advance_pppoe_vlan_endvid_text").send_keys(End_ID)
    Select(driver.find_element(By.ID,"advance_pppoe_vlan_enabled_combobox")).select_by_visible_text(Enable)
    e_mod.Checkbox_EMS(driver,"advance_pppoe_vlan_circuit_checkbox",Circuit_id)
    e_mod.Checkbox_EMS(driver,"advance_pppoe_vlan_remote_checkbox",Remote_id)
    time.sleep(2)
    driver.find_element(By.ID,"popupCallBack").click()
    time.sleep(2)
    
    

def Advanced_PPPoE_VLAN_Modify(driver,Enable,Circuit_id,Remote_id,file_name):
    Select(driver.find_element(By.ID,"advance_pppoe_vlan_modify_enabled_combobox")).select_by_visible_text(Enable)
    e_mod.Checkbox_EMS(driver,"advance_pppoe_vlan_modify_circuit_checkbox",Circuit_id)
    e_mod.Checkbox_EMS(driver,"advance_pppoe_vlan_modify_remote_checkbox",Remote_id)
    time.sleep(2)
    driver.find_element(By.ID,"popupCallBack").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass
    time.sleep(2)

def Advanced_PPPoE_ONTOption(driver,Port,ONT,Pass_through,Disable,file_name):
    Select(driver.find_element(By.ID,"advance_pppoe_ont_port_combobox")).select_by_visible_text(Port)
    time.sleep(2)
    Select(driver.find_element(By.ID,"advance_pppoe_ont_ont_combobox")).select_by_visible_text(ONT)
    time.sleep(2)
    e_mod.Checkbox_EMS(driver,"advance_pppoe_ont_pass_checkbox",Pass_through)
    e_mod.Checkbox_EMS(driver,"advance_pppoe_ont_disable_checkbox",Disable)
    driver.find_element(By.ID,"advance_pppoe_ont_apply_btn").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass
    time.sleep(2)
    

def GPON_OLT_Apply(driver,Port,Active,Register_Method,ONT_Template_Active,Template,Fec_Active,Ranging_Distance,file_name):
    Select(driver.find_element(By.ID,"gpon_oltregistration_port_combobox")).select_by_visible_text(Port)
    e_mod.Checkbox_EMS(driver,"gpon_oltregistration_active_checkbox",Active)
    Select(driver.find_element(By.ID,"gpon_oltregistration_method_combobox")).select_by_visible_text(Register_Method)
    e_mod.Checkbox_EMS(driver,"gpon_oltregistration_onttemplateactive_checkbox",ONT_Template_Active)
    Select(driver.find_element(By.ID,"gpon_oltregistration_template_combobox")).select_by_visible_text(Template)
    e_mod.Checkbox_EMS(driver,"gpon_oltregistration_fecactive_checkbox",Fec_Active)
    driver.find_element(By.ID,"gpon_oltregistration_distance_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"gpon_oltregistration_distance_text").send_keys(Ranging_Distance)
    driver.find_element(By.ID,"gpon_oltregistration_apply_btn").click()
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass
    time.sleep(2)

def Configure_Save(driver,file_name):
    driver.find_element(By.ID,"device_configure_save_btn_1").click()
    time.sleep(2)
    if(driver.find_element(By.ID,"message_text").text == 'Save Success'):
        print(f"             [EMS1-6525][Configure Save] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6525][Configure Save] Result Fail",file = open(file_name, '+a'))
    msg = alert_accept_text(driver)
    
    try:
        e_pro.Close(driver)
    except:
        pass















    



    

















    










    

    


    
