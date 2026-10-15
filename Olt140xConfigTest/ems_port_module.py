from os import times
import time
from attr import field
from pyrsistent import s
import selenium_module as mod
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys
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

# # Copy

# def Copy_Destination_Slot_Select(driver,slot):
#     retry = True
#     while(retry == True):
#         try:                                    
#             driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlot_dst']/option[{slot}]").click()
#         except:
#             time.sleep(1)
#         try:
#             if(driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlot_dst']/option[{slot}]").is_selected() == True):
#                 retry = False
#         except:
#             time.sleep(1)

# def Copy_Destination_Port_List(driver,value):
#     input = driver.find_element(By.NAME, "rpportcopy_inputDestPort")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def Copy_Apply(driver):
#     driver.find_element(By.NAME, "rpportcopy_btnApply").click()

# # Default

# def Default_Port_List(driver,value):
#     input = driver.find_element(By.NAME, "rp_portlist")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def Default_Apply(driver):
#     driver.find_element(By.NAME, "rpportdefault_btnApply").click()

# DHCP #

def DHCP_Slot_Select(driver,text):
    Select(driver.find_element(By.ID,"port_dhcp_slot_combobox")).select_by_value(text)

def DHCP_Port_Select(driver,text):
    Select(driver.find_element(By.ID,"port_dhcp_port_combobox")).select_by_visible_text(text)

def DHCP_Option_82_Policy(driver,text):
    Select(driver.find_element(By.ID,"port_dhcp_option82_select")).select_by_visible_text(text)

def DHCP_Option_LDRA_Policy(driver,text):
    Select(driver.find_element(By.ID,"port_dhcp_optionldra_policy_select")).select_by_visible_text(text)

def DHCP_Option_LDRA_LinkLocal(driver,text):
    if(text=="Chk-all"):
        text = "Check all"
    elif(text == "Skip-all"):
        text = "Skip all"
    elif(text == "Skip-dst"):
        text = "Skip destination"
    elif(text == "Skip-scr"):
        text = "Skip source"
    

    Select(driver.find_element(By.ID,"port_dhcp_optionldra_linklocal_select")).select_by_visible_text(text)

def DHCP_Snooping_Setting_Max_Lease(driver,value):
    input = driver.find_element(By.ID,"port_dhcp_max_lease")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def DHCP_Snooping_Setting_Priority_VLAN(driver,value):
    input = driver.find_element(By.ID,"port_dhcp_priority_vlan")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def DHCP_Snooping_Setting_IP_MAC_Binding(driver,text):
    Select(driver.find_element(By.ID,"port_dhcp_ipmacbinding1_select")).select_by_visible_text(text) # port_dhcp_ipmacbinding_select

def DHCP_Snooping_Setting_DHCPv4_Trust_Untrust(driver,text):
    Select(driver.find_element(By.ID,"port_dhcp_ipv4_select")).select_by_visible_text(text)

def DHCP_Snooping_Setting_DHCPv6_Trust_Untrust(driver,text):
    Select(driver.find_element(By.ID,"port_dhcp_ipv6_select")).select_by_visible_text(text)

def DHCP_Static_IP_Fitter_Setting_Index(driver,text):
    Select(driver.find_element(By.ID,"port_dhcp_index_select")).select_by_visible_text(text)

def DHCP_Static_IP_Fitter_Setting_IP_Address(driver,value):
    input = driver.find_element(By.ID,"port_dhcp_ipaddress_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def DHCP_Static_IP_Fitter_Setting_IPv6_Prefix(driver,value):
    input = driver.find_element(By.ID,"port_dhcp_ipv6prefix_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def DHCP_Static_IP_Fitter_Setting_IP_MAC_Binding(driver,text):
    Select(driver.find_element(By.ID,"port_dhcp_ipmacbinding2_select")).select_by_visible_text(text)

def DHCP_Apply(driver):
    driver.find_element(By.ID,"port_dhcp_apply").click()

def DHCP_Static_IP_Address(driver,value,sel):
    input = driver.find_element(By.ID,f"port_dhcp_staticip{sel}_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def DHCP_Static_IP_Select(driver,sel):
    driver.find_element(By.XPATH,f'//*[@for="port_dhcp_staticip{sel}"]').click()

def DHCP_Static_IP_Delete(driver):
    driver.find_element(By.ID,"port_dhcp_StaticIPAddress_delete").click()

# # DSL

# def DSL_Slot_Select(driver,slot):
#     driver.find_elements(By.NAME, "rpdsl_rdoSlt")[int(slot)-1].click()

# GENNI # 

def GENNI_Slot_Select(driver,text):
    Select(driver.find_element(By.ID,"port_genni_slot_combobox")).select_by_value(text)

def GENNI_Port_Select(driver,text):
    Select(driver.find_element(By.ID,"port_genni_port_combobox")).select_by_value(str(text))

def GENNI_Name(driver,value):
    input = driver.find_element(By.ID,"port_genni_name_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def GENNI_Active(driver,text):
    Select(driver.find_element(By.ID,"port_genni_active_combobox")).select_by_visible_text(text)    

def GENNI_Speed(driver,text):
    Select(driver.find_element(By.ID,"port_genni_speed_combobox")).select_by_visible_text(text)    

def GENNI_Auto_Nego(driver,text):
    Select(driver.find_element(By.ID,"port_genni_autonego_combobox")).select_by_visible_text(text)    

def GENNI_Flow_Ctrl(driver,text):
    Select(driver.find_element(By.ID,"port_genni_flowctrl_combobox")).select_by_visible_text(text)    

def GENNI_Mode(driver,text):
    Select(driver.find_element(By.ID,"port_genni_mode_combobox")).select_by_visible_text(text)    

def GENNI_VLAN_Trunk(driver,text):
    Select(driver.find_element(By.ID,"port_genni_vlantrunk_combobox")).select_by_visible_text(text)    

def GENNI_MTU(driver,value):
    input = driver.find_element(By.ID,"port_genni_mtu_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def GENNI_QinQ_TPID(driver,text):
    Select(driver.find_element(By.ID,"port_genni_qinqtpid_combobox")).select_by_visible_text(text)    

def GENNI_Default_TPID(driver,text):
    Select(driver.find_element(By.ID,"port_genni_defaulttpid_combobox")).select_by_visible_text(text)    

def GENNI_Apply(driver):
    driver.find_element(By.ID,"port_genni_apply_btn").click()



# GE # 

def GE_Slot_Select(driver,text):
    Select(driver.find_element(By.ID,"port_ge_slot_combobox")).select_by_value(text)    

def GE_Port_Select(driver,text):
    Select(driver.find_element(By.ID,"port_ge_port_combobox")).select_by_visible_text(str(text))    

def GE_Active(driver,text):
    Select(driver.find_element(By.ID,"port_ge_active_combobox")).select_by_visible_text(text)    

def GE_Name(driver,text):
    driver.find_element(By.ID,"port_ge_name_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID,"port_ge_name_text").send_keys(text)

def GE_Auto_Nego(driver,text):
    Select(driver.find_element(By.ID,"port_ge_autonego_combobox")).select_by_visible_text(text)    

def GE_Flow_Ctrl(driver,text):
    Select(driver.find_element(By.ID,"port_ge_flowctrl_combobox")).select_by_visible_text(text)    

def GE_Speed(driver,text):
    Select(driver.find_element(By.ID,"port_ge_speed_combobox")).select_by_visible_text(text)    

def GE_Frame_Type(driver,text):
    Select(driver.find_element(By.ID,"port_ge_frame_combobox")).select_by_visible_text(text)    

def GE_MTU(driver,text):
    input = driver.find_element(By.ID,"port_ge_mtu_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(text)

def GE_TEL_NO(driver,text):
    input = driver.find_element(By.ID,"port_ge_tel_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(text)

def GE_Apply(driver):
    driver.find_element(By.ID,"port_ge_apply_btn").click()


# # FDB

# def FDB_Static_MAC(driver,value):
#     input = driver.find_element(By.NAME, "rpportfdb_txtMacAddr")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def FDB_VLAN(driver,value):
#     input = driver.find_element(By.NAME, "rpportfdb_txtMacVid")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def FDB_Apply(driver):
#     driver.find_element(By.NAME, "rpportfdb_btnApply").click()

# def FDB_Delete(driver):
#     driver.find_element(By.NAME, "rpportfdb_btnDelete").click()

# # G.bond

# def G_bond_Slot_Select(driver,slot):
#     driver.find_elements(By.NAME, "rpdsl_rdoSlt")[int(slot)-1].click()

# # PPPoE+

# def PPPoE_Policy(driver,sel):
#     driver.find_element(By.XPATH, f"//*[@name='rpportPppoe_opt82Policy']/option[{sel}]").click()

# def PPPoE_Apply(driver):
#     driver.find_element(By.NAME, "rpPortPppoeApply").click()

# # PVC

# def PVC_Slot_Select(driver,slot):
#     driver.find_elements(By.NAME, "rpdsl_rdoSlt")[int(slot)-1].click()


# QoS #
 
def QoS_Slot_Select(driver,text):
    Select(driver.find_element(By.ID,"port_qos_slot_combobox")).select_by_value(text)    

def QoS_Port_Select(driver,text):
    Select(driver.find_element(By.ID,"port_qos_port_combobox")).select_by_visible_text(text)    

def QoS_Rate_Limit_Profile(driver,text):
    Select(driver.find_element(By.ID,"port_qos_rateprofile_combobox")).select_by_visible_text(text)    

def QoS_Algorithm_Olc(driver,text):
    Select(driver.find_element(By.ID,"port_qos_olcalgorithm1_combobox")).select_by_visible_text(text)    

def QoS_Algorithm_Olc_2(driver,text):
    Select(driver.find_element(By.ID,"port_qos_olcalgorithm2_combobox")).select_by_visible_text(text)    

def QoS_Algorithm(driver,text):
    Select(driver.find_element(By.ID,"port_qos_otheralgorithm_combobox")).select_by_visible_text(text)    

def QoS_Shaping_Profile(driver,text):
    Select(driver.find_element(By.ID,"port_qos_shapingprofile_combobox")).select_by_visible_text(text)    

def QoS_Weight_Profile(driver,text):
    Select(driver.find_element(By.ID,"port_qos_weightprofile_combobox")).select_by_visible_text(text)    

def QoS_Apply(driver):
    driver.find_element(By.ID,"port_qos_apply_button").click()

# def Qos_Slot_Select(driver,slot):
#     retry = True
#     while(retry == True):
#         try:
#             driver.find_element(By.XPATH, f"//*[@name='rpQosPort_slot']/option[{slot}]").click()
#         except:
#             time.sleep(1)
#         try:
#             if(driver.find_element(By.XPATH, f"//*[@name='rpQosPort_slot']/option[{slot}]").is_selected() == True):
#                 retry = False
#         except:
#             time.sleep(1)


# # DDMI

# def DDMI_Module_Temperature(driver,High_Limit,Low_Limit):
#     input = driver.find_element(By.NAME, "rpportddmi_input_highalarm_moduleTemperature")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(High_Limit)
#     input = driver.find_element(By.NAME, "rpportddmi_input_lowalarm_moduleTemperature")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(Low_Limit)

# def DDMI_Supply_Voltage(driver,High_Limit,Low_Limit):
#     input = driver.find_element(By.NAME, "rpportddmi_input_highalarm_supplyVoltageVcc")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(High_Limit)
#     input = driver.find_element(By.NAME, "rpportddmi_input_lowalarm_supplyVoltageVcc")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(Low_Limit)

# def DDMI_TX_Bias_Current(driver,High_Limit,Low_Limit):
#     input = driver.find_element(By.NAME, "rpportddmi_input_highalarm_tXBias")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(High_Limit)
#     input = driver.find_element(By.NAME, "rpportddmi_input_lowalarm_tXBias")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(Low_Limit)

# def DDMI_TX_Output_Power(driver,High_Limit,Low_Limit):
#     input = driver.find_element(By.NAME, "rpportddmi_input_highalarm_tXOutputPower")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(High_Limit)
#     input = driver.find_element(By.NAME, "rpportddmi_input_lowalarm_tXOutputPower")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(Low_Limit)

# def DDMI_RX_Input_Power(driver,High_Limit,Low_Limit):
#     input = driver.find_element(By.NAME, "rpportddmi_input_highalarm_rXInputPower")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(High_Limit)
#     input = driver.find_element(By.NAME, "rpportddmi_input_lowalarm_rXInputPower")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(Low_Limit)

# def DDMI_Apply(driver):
#     driver.find_element(By.NAME, "rpportddmi_btnapply").click()
