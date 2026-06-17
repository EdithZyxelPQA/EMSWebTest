from selenium.webdriver.common.by import By
from os import times
import time
from attr import field
from pyrsistent import s
import module.selenium_module as mod
from selenium.webdriver.support.ui import Select

def Slot_Select(driver,slot):
    retry = True
    while(retry == True):
        try:
            driver.find_element(By.XPATH, f"//*[@name='rpQosPort_slot']/option[{slot}]").click() # lctbl_selSlot
        except:
            time.sleep(1)
        try:
            if(driver.find_element(By.XPATH, f"//*[@name='rpQosPort_slot']/option[{slot}]").is_selected() == True):
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

# Copy

def Copy_Destination_Slot_Select(driver,slot):
    retry = True
    while(retry == True):
        try:                                    
            driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlot_dst']/option[{slot}]").click()
        except:
            time.sleep(1)
        try:
            if(driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlot_dst']/option[{slot}]").is_selected() == True):
                retry = False
        except:
            time.sleep(1)

def Copy_Destination_Port_List(driver,value):
    input = driver.find_element(By.NAME, "rpportcopy_inputDestPort")
    input.clear()
    input.send_keys(value)

def Copy_Apply(driver):
    driver.find_element(By.NAME, "rpportcopy_btnApply").click()

# Default

def Default_Port_List(driver,value):
    input = driver.find_element(By.NAME, "rp_portlist")
    input.clear()
    input.send_keys(value)

def Default_Apply(driver):
    driver.find_element(By.NAME, "rpportdefault_btnApply").click()

# DHCP

def DHCP_Slot_Select(driver,slot):
    retry = True
    # while(retry == True):
    for i in range(30):
        try:
            driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlot']/option[{slot}]").click() # lctbl_selSlot
        except:
            time.sleep(1)
        try:
            if(driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlot']/option[{slot}]").is_selected() == True):
                retry = False
                break
        except:
            time.sleep(1)

def DHCP_Option_82_Policy(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpportdhcp_opt82Policy']/option[{sel}]").click()

def DHCP_Option_LDRA_Policy(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpportdhcp_optLdraPolicy']/option[{sel}]").click()

def DHCP_Option_LDRA_LinkLocal(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpportdhcp_optLdraLinkLocal']/option[{sel}]").click()

def DHCP_Snooping_Setting_Max_Lease(driver,value):
    input = driver.find_element(By.NAME, "rpportdhcp_inputMaxlease")
    input.clear()
    input.send_keys(value)

def DHCP_Snooping_Setting_Priority_VLAN(driver,value):
    input = driver.find_element(By.NAME, "rpportdhcp_priorityVlan")
    input.clear()
    input.send_keys(value)

def DHCP_Snooping_Setting_IP_MAC_Binding(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpportdhcp_SnIpMacBinding']/option[{sel}]").click()

def DHCP_Static_IP_Fitter_Setting_Index(driver,value):
    input = driver.find_element(By.NAME, "rpportdhcp_stIpIdx")
    input.clear()
    input.send_keys(value)

def DHCP_Static_IP_Fitter_Setting_IP_Address(driver,value):
    input = driver.find_element(By.NAME, "rpportdhcp_inputStIp")
    input.clear()
    input.send_keys(value)

def DHCP_Static_IP_Fitter_Setting_IPv6_Prefix(driver,value):
    input = driver.find_element(By.NAME, "rpportdhcp_ipv6Prefix")
    input.clear()
    input.send_keys(value)

def DHCP_Static_IP_Fitter_Setting_IP_MAC_Binding(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpportdhcp_stIpMacBinding']/option[{sel}]").click()

def DHCP_Apply(driver):
    driver.find_element(By.NAME, "rpPortDhcpApply").click()

def DHCP_Delete(driver):
    driver.find_element(By.NAME, "rpportdhcp_data_button_delete").click()

# DSL

def DSL_Slot_Select(driver,slot):
    driver.find_elements(By.NAME, "rpdsl_rdoSlt")[int(slot)-1].click()

# GENNI

def GENNI_Slot_Select(driver,slot):
    driver.find_elements(By.NAME, "Lcmantableid")[int(slot)-1].click()

def GENNI_Slot_Up(driver):
    driver.find_element(By.NAME, "rpportGenni_btnUp").click()

def GENNI_Name_All(driver,value):
    input = driver.find_element(By.NAME, "rpportGenni_txtName_all")
    input.clear()
    input.send_keys(value)

def GENNI_Apply(driver):
    driver.find_element(By.NAME, "rpportGenni_btnApply").click()

def GENNI_Port_Select(driver,port):
    driver.find_elements(By.CLASS_NAME, "font-btn.radio_link")[int(port)-1].click()

def GENNI_Port_Up(driver):
    driver.find_element(By.NAME, "rpportGennidetail_btnUp").click()

# GE

def GE_Slot_Select(driver,slot):
    driver.find_elements(By.NAME, "Lcmantableid")[int(slot)-1].click()

def GE_Slot_Up(driver):
    driver.find_element(By.NAME, "rpportGe_btnUp").click()

def GE_Active_All(driver,request):
    check_box = driver.find_element(By.NAME, f"rpportGe_chkActive")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def GE_Active(driver,index,request):
    check_box = driver.find_element(By.NAME, f"rpportGe_chkActive_{index}")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def GE_Name_All(driver,value):
    input = driver.find_element(By.NAME, "rpportGe_txtNameA_all")
    input.clear()
    input.send_keys(value)

def GE_Auto_Nego_All(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpportGe_sltAutoNgtA_all']/option[{sel}]").click()

def GE_Flow_Ctrl_All(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpportGe_sltflowctrlA_all']/option[{sel}]").click()

def GE_Speed_All(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpportGe_SltSpeedA_all']/option[{sel}]").click()

def GE_Frame_Type_All(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpportGe_sltFrameTypeA_all']/option[{sel}]").click()

def GE_Apply(driver):
    driver.find_element(By.NAME, "rpportGe_btnApply").click()

def GE_Cancel(driver):
    driver.find_element(By.NAME, "rpportGe_btnCancel").click()

def GE_Port_Select(driver,port):
    driver.find_element(By.NAME, f"Lcmantableid_{port}").click()

def GE_Port_Up(driver):
    driver.find_element(By.NAME, "rpportGedetail_btnUp").click()

def GE_Port_MTU(driver,value):
    input = driver.find_element(By.NAME, "rpportge_mtu")
    input.clear()
    input.send_keys(value)

def GE_Port_TEL_NO(driver,value):
    input = driver.find_element(By.NAME, "rpportge_tel")
    input.clear()
    input.send_keys(value)

def GE_Port_Apply(driver):
    driver.find_element(By.NAME, "rpportGedetail_btnApply").click()

def GE_Port_Cancel(driver):
    driver.find_element(By.NAME, "rpportGedetail_btnCancel").click()

# FDB

def FDB_Static_MAC(driver,value):
    input = driver.find_element(By.NAME, "rpportfdb_txtMacAddr")
    input.clear()
    input.send_keys(value)

def FDB_VLAN(driver,value):
    input = driver.find_element(By.NAME, "rpportfdb_txtMacVid")
    input.clear()
    input.send_keys(value)

def FDB_Apply(driver):
    driver.find_element(By.NAME, "rpportfdb_btnApply").click()

def FDB_Delete(driver):
    driver.find_element(By.NAME, "rpportfdb_btnDelete").click()

# G.bond

def G_bond_Slot_Select(driver,slot):
    driver.find_elements(By.NAME, "rpdsl_rdoSlt")[int(slot)-1].click()

# PPPoE+

def PPPoE_Policy(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpportPppoe_opt82Policy']/option[{sel}]").click()

def PPPoE_Apply(driver):
    driver.find_element(By.NAME, "rpPortPppoeApply").click()

# PVC

def PVC_Slot_Select(driver,slot):
    driver.find_elements(By.NAME, "rpdsl_rdoSlt")[int(slot)-1].click()

# QoS

def Qos_Slot_Select(driver,slot):
    retry = True
    while(retry == True):
        try:
            driver.find_element(By.XPATH, f"//*[@name='rpQosPort_slot']/option[{slot}]").click()
        except:
            time.sleep(1)
        try:
            if(driver.find_element(By.XPATH, f"//*[@name='rpQosPort_slot']/option[{slot}]").is_selected() == True):
                retry = False
        except:
            time.sleep(1)

def Qos_Rate_Limit_Profile_All(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpPortQos_ratelimit_all']/option[{sel}]").click()

def Qos_Algorithm_All(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpPortQos_algorithm_all']/option[{sel}]").click()

def Qos_Shaping_Profile_All(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpPortQos_shapProf_all']/option[{sel}]").click()

def Qos_Weight_Profile_All(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpPortQos_weightProf_all']/option[{sel}]").click()

def Qos_Apply(driver):
    driver.find_element(By.NAME, "rpPortQos_btnApply").click()

# DDMI

def DDMI_Module_Temperature(driver,High_Limit,Low_Limit):
    input = driver.find_element(By.NAME, "rpportddmi_input_highalarm_moduleTemperature")
    input.clear()
    input.send_keys(High_Limit)
    input = driver.find_element(By.NAME, "rpportddmi_input_lowalarm_moduleTemperature")
    input.clear()
    input.send_keys(Low_Limit)

def DDMI_Supply_Voltage(driver,High_Limit,Low_Limit):
    input = driver.find_element(By.NAME, "rpportddmi_input_highalarm_supplyVoltageVcc")
    input.clear()
    input.send_keys(High_Limit)
    input = driver.find_element(By.NAME, "rpportddmi_input_lowalarm_supplyVoltageVcc")
    input.clear()
    input.send_keys(Low_Limit)

def DDMI_TX_Bias_Current(driver,High_Limit,Low_Limit):
    input = driver.find_element(By.NAME, "rpportddmi_input_highalarm_tXBias")
    input.clear()
    input.send_keys(High_Limit)
    input = driver.find_element(By.NAME, "rpportddmi_input_lowalarm_tXBias")
    input.clear()
    input.send_keys(Low_Limit)

def DDMI_TX_Output_Power(driver,High_Limit,Low_Limit):
    input = driver.find_element(By.NAME, "rpportddmi_input_highalarm_tXOutputPower")
    input.clear()
    input.send_keys(High_Limit)
    input = driver.find_element(By.NAME, "rpportddmi_input_lowalarm_tXOutputPower")
    input.clear()
    input.send_keys(Low_Limit)

def DDMI_RX_Input_Power(driver,High_Limit,Low_Limit):
    input = driver.find_element(By.NAME, "rpportddmi_input_highalarm_rXInputPower")
    input.clear()
    input.send_keys(High_Limit)
    input = driver.find_element(By.NAME, "rpportddmi_input_lowalarm_rXInputPower")
    input.clear()
    input.send_keys(Low_Limit)

def DDMI_Apply(driver):
    driver.find_element(By.NAME, "rpportddmi_btnapply").click()
