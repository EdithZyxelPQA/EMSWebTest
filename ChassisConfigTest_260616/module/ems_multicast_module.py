from os import times
import time
from attr import field
from pyrsistent import s
import module.selenium_module as mod
from selenium.webdriver.support.ui import Select

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys
import module.ems_module as e_mod
# .clear() -> .send_keys(Keys.CONTROL + 'a')

# Apply # 
def Apply(driver):
    driver.find_element(By.XPATH, '//*[@value="Apply"]').click()

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

# IGMP

# IGMP -> IGMP Setup

def IGMP_IGMP_Setup_Non_MVLAN_Mode(driver,text):
    #　Non MVLAN Mode    
    Select(driver.find_element(By.ID, "multicast_igmpSetup_igmpmode_combobox")).select_by_visible_text(text)

def IGMP_IGMP_Setup_MVLAN_Mode(driver,text):
    #　MVLAN Mode
    Select(driver.find_element(By.ID, "multicast_igmpSetup_mvlanmode_combobox")).select_by_visible_text(text)

def IGMP_IGMP_Setup_Version(driver,text):
    # Version
    Select(driver.find_element(By.ID, "multicast_igmpSetup_version_combobox")).select_by_visible_text(text)

def IGMP_IGMP_Setup_Leave_Mode(driver,text):
    # Leave-Mode
    Select(driver.find_element(By.ID, "multicast_igmpSetup_leavemode_combobox")).select_by_visible_text(text)    

def IGMP_IGMP_Setup_Pbit(driver,text):
    # Pbit
    Select(driver.find_element(By.ID, "multicast_igmpSetup_pbit_combobox")).select_by_visible_text(text)    

def IGMP_IGMP_Setup_GQT_Interval(driver,value):
    # General-Query Timer -> Interval
    driver.find_element(By.ID, "multicast_igmpSetup_general_interval_text").send_keys(Keys.CONTROL + 'a')
    try:
        WebDriverWait(driver, 10).until(EC.alert_is_present()).accept()    
    except:
        pass
    driver.find_element(By.ID, "multicast_igmpSetup_general_interval_text").send_keys(value)

def IGMP_IGMP_Setup_GQT_Robustness(driver,value):
    # General-Query Timer -> Robustness
    driver.find_element(By.ID, "multicast_igmpSetup_general_robustness_text").send_keys(Keys.CONTROL + 'a')
    try:
        WebDriverWait(driver, 10).until(EC.alert_is_present()).accept()
    except:
        pass
    driver.find_element(By.ID, "multicast_igmpSetup_general_robustness_text").send_keys(value)

def IGMP_IGMP_Setup_GQT_Max_Response_Time(driver,value):
    # General-Query Timer -> Max-Response-Time
    driver.find_element(By.ID, "multicast_igmpSetup_general_response_text").send_keys(Keys.CONTROL + 'a')
    try:
        WebDriverWait(driver, 10).until(EC.alert_is_present()).accept()
    except:
        pass
    driver.find_element(By.ID, "multicast_igmpSetup_general_response_text").send_keys(value)

def IGMP_IGMP_Setup_GQT_V4_Query_Source_IP(driver,value):
    driver.find_element(By.ID, "multicast_igmpSetup_general_ipv4_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "multicast_igmpSetup_general_ipv4_text").send_keys(value)

def IGMP_IGMP_Setup_GQT_V6_Query_Source_IP(driver,value):
    driver.find_element(By.ID, "multicast_igmpSetup_general_ipv6_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "multicast_igmpSetup_general_ipv6_text").send_keys(value)

def IGMP_IGMP_Setup_LMQT_Interval(driver,value):
    # Last-Member-Query Timer -> Interval
    driver.find_element(By.ID, "multicast_igmpSetup_lastMember_interval_text").send_keys(Keys.CONTROL + 'a')
    try:
        WebDriverWait(driver, 10).until(EC.alert_is_present()).accept()
    except:
        pass
    driver.find_element(By.ID, "multicast_igmpSetup_lastMember_interval_text").send_keys(value)

def IGMP_IGMP_Setup_LMQT_Robustness(driver,value):
    # Last-Member-Query Timer -> Robustness
    driver.find_element(By.ID, "multicast_igmpSetup_lastMember_robustness_text").send_keys(Keys.CONTROL + 'a')
    try:
        WebDriverWait(driver, 10).until(EC.alert_is_present()).accept()
    except:
        pass
    driver.find_element(By.ID, "multicast_igmpSetup_lastMember_robustness_text").send_keys(value)

def IGMP_IGMP_Setup_Apply_Click(driver): 
    driver.find_element(By.CLASS_NAME, "button.button_green.mr-3").click()
    
def IGMP_IGMP_Setup_Cancel_Click(driver): 
    driver.find_element(By.CLASS_NAME, "button.button_green.button_check_pri").click()

def IGMP_IGMP_Setup(driver,select_1,select_2,select_3,select_4,select_5,key_6,key_7,key_8,key_9,key_10):
    # Setup IGMP Setup all input
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Multicast")
    mod.Switch_Frame(driver)
    IGMP_IGMP_Setup_Non_MVLAN_Mode(driver,select_1)
    IGMP_IGMP_Setup_MVLAN_Mode(driver,select_2)
    IGMP_IGMP_Setup_Version(driver,select_3)
    IGMP_IGMP_Setup_Leave_Mode(driver,select_4)
    IGMP_IGMP_Setup_Pbit(driver,select_5)
    IGMP_IGMP_Setup_GQT_Interval(driver,key_6)
    IGMP_IGMP_Setup_GQT_Robustness(driver,key_7)
    IGMP_IGMP_Setup_GQT_Max_Response_Time(driver,key_8)
    IGMP_IGMP_Setup_LMQT_Interval(driver,key_9)
    IGMP_IGMP_Setup_LMQT_Robustness(driver,key_10)
    IGMP_IGMP_Setup_Apply_Click(driver)

# IGMP -> Port Setup

def IGMP_Port_Setup_Bandwidth(driver,value):
    input = driver.find_element(By.NAME, "rpmcigmpport_txtBw")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def IGMP_Port_Setup_Max_Group(driver,value):
    input = driver.find_element(By.NAME, "rpmcigmpport_txtMg")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def IGMP_Port_Setup_Max_Message(driver,value):
    input = driver.find_element(By.NAME, "rpmcigmpport_txtMmeg")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def IGMP_Port_Setup_Group_Privilege(driver,request):
    check_box = driver.find_element(By.NAME, "rpmcigmpport_chkPriv")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def IGMP_Port_Setup_Group_Privilege_Profile_Apply(driver):
    driver.find_elements(By.CLASS_NAME, "font-btn")[1].click()

def IGMP_Port_Setup_Group_Privilege_Profile_Remove(driver):
    driver.find_elements(By.CLASS_NAME, "font-btn")[2].click()

def IGMP_Port_Setup_Apply(driver):
    driver.find_element(By.NAME, "rpmcigmpport_btnApply").click()

# IGMP -> Port MVLAN Setup

def IGMP_Port_MVLAN_Setup_Delete(driver):
    driver.find_element(By.NAME, "rpPortMvlanDelete").click()

def IGMP_Port_MVLAN_Setup_MVLAN(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpPortMvlan_mvlanList']/option[{sel}]").click()

def IGMP_Port_MVLAN_Setup_Type(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpPortMvlan_typeList']/option[{sel}]").click()

def IGMP_Port_MVLAN_Setup_Uni_VLAN(driver,value):
    input = driver.find_element(By.NAME, "rpPortMvlan_uniVlan")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def IGMP_Port_MVLAN_Setup_Apply(driver):
    driver.find_element(By.NAME, "rpPortMvlanApply").click()

# Port Mode #

def Port_Mode_Slot(driver,text):
    Select(driver.find_element(By.ID, "multicast_portmode_card_combobox")).select_by_value(text)

def Port_Mode_Load(driver):
    driver.find_element(By.XPATH, '//*[@value="Load"]').click()

# def Port_Mode_Apply(driver):
#     driver.find_element(By.XPATH, '//*[@value="Apply"]').click()

def Port_Mode_Cancle(driver):
    driver.find_element(By.XPATH, '//*[@value="Cancel"]').click()

def Port_Mode_Static_Querier(driver,text):
    Select(driver.find_element(By.ID, "multicast_portmode_querier_all")).select_by_visible_text(text)

# VLAN Mode #

def VLAN_Mode_Mode(driver,text):
    Select(driver.find_element(By.ID, "multicast_vlanmode_mode_combobox")).select_by_visible_text(text)

def VLAN_Mode_VLAN(driver,value):
    driver.find_element(By.ID, "multicast_vlanmode_vlan_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "multicast_vlanmode_vlan_text").send_keys(value)

def VLAN_Mode_Name(driver,value):
    driver.find_element(By.ID, "multicast_vlanmode_name_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "multicast_vlanmode_name_text").send_keys(value)

def VLAN_Mode_VPN(driver,request):
    e_mod.Checkbox_EMS(driver,"multicast_vlanmode_vpnenable_checkbox",request)    

def VLAN_Mode_Add(driver):
    # driver.find_element(By.ID, "multicast_vlanmode_vlan_add").click()  
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, "multicast_vlanmode_vlan_add"))).click()

def VLAN_Mode_Load(driver):
    driver.find_element(By.ID, "multicast_vlanmode_vlan_load").click()  
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, "multicast_vlanmode_vlan_load"))).click()

def VLAN_Mode_Delete(driver):
    # driver.find_element(By.ID, "multicast_vlanmode_vlan_delete").click()
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, "multicast_vlanmode_vlan_delete"))).click()

# def VLAN_Mode_Cancle(driver):
#     driver.find_element(By.ID, "").click()

def VLAN_Mode_Select(driver,sel):
    # driver.find_element(By.XPATH, f'//*[@for="multicast_vlanmode_vlan_radio{sel}"]').click()
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, f'//*[@for="multicast_vlanmode_vlan_radio{sel}"]'))).click()

# # IGMP Privilege Profile

# def IGMP_Privilege_Profile_Name(driver,value):
#     input = driver.find_element(By.NAME, "rpigmpPriProf_ipt_profile_name")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def IGMP_Privilege_Profile_Index(driver,sel):
#     driver.find_element(By.XPATH, f"//*[@name='rpigmpPriProf_slt_index']/option[{sel}]").click()

# def IGMP_Privilege_Profile_Bandwidth(driver,value):
#     input = driver.find_element(By.NAME, "rpigmpPriProf_ipt_bw")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def IGMP_Privilege_Profile_Start_Address(driver,value):
#     input = driver.find_element(By.NAME, "rpigmpPriProf_ipt_st_add")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def IGMP_Privilege_Profile_End_Address(driver,value):
#     input = driver.find_element(By.NAME, "rpigmpPriProf_ipt_end_add")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def IGMP_Privilege_Profile_Privilege(driver,sel):
#     driver.find_element(By.XPATH, f"//*[@name='rpigmpPriProf_slt_privilege']/option[{sel}]").click()

# def IGMP_Privilege_Profile_Length(driver,value):
#     input = driver.find_element(By.NAME, "rpigmpPriProf_ipt_len")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def IGMP_Privilege_Profile_Interval(driver,value):
#     input = driver.find_element(By.NAME, "rpigmpPriProf_ipt_interval")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def IGMP_Privilege_Profile_Count(driver,value):
#     input = driver.find_element(By.NAME, "rpigmpPriProf_ipt_count")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def IGMP_Privilege_Profile_Reset(driver,value):
#     input = driver.find_element(By.NAME, "rpigmpPriProf_ipt_reset")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# # def IGMP_Privilege_Profile_Apply_New(driver):
# #     driver.find_element(By.NAME, "rpigmpPriProf_config_button_apply").click()

# # def IGMP_Privilege_Profile_Delete_Entry(driver):
# #     driver.find_element(By.NAME, "rpigmpPriProf_config_button_cancel").click()

# # def IGMP_Privilege_Profile_Modify(driver):
# #     driver.find_element(By.NAME, "rpigmpPriProf_data_button_modify").click()

# # def IGMP_Privilege_Profile_Delete(driver):
# #     driver.find_element(By.NAME, "rpigmpPriProf_data_button_delete").click()

# MVLAN

# MVLAN -> MVLAN

def MVLAN_MVLAN_MVLAN(driver,value):
    input = driver.find_element(By.ID, "rpMvlan_mvlan")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def MVLAN_MVLAN_Pbit(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpMvlan_ipt_pbit']/option[{sel}]").click()

def MVLAN_MVLAN_Apply(driver):
    driver.find_element(By.NAME, "rpMvlanApply").click()

def MVLAN_MVLAN_Delete(driver):
    driver.find_element(By.NAME, "rpMvlanDelete").click()

# MVLAN #

def MVLAN_MVLAN(driver,value):
    driver.find_element(By.ID, "multicast_mvlan_mvlan_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "multicast_mvlan_mvlan_text").send_keys(value)

def MVLAN_Pbit(driver,value):
    driver.find_element(By.ID, "multicast_mvlan_pbit_combobox").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, "multicast_mvlan_pbit_combobox").send_keys(value)

def MVLAN_Select(driver,sel):
    driver.find_element(By.XPATH, f'//*[@for="multicast_mvlan_mvlan_radio{sel}"]').click()

def MVLAN_Add(driver):
    driver.find_element(By.ID, "multicast_mvlan_mvlan_add").click()

def MVLAN_Delete(driver):
    driver.find_element(By.ID, "multicast_mvlan_mvlan_delete").click()

def MVLAN_Cancle(driver):
    driver.find_element(By.ID, "multicast_mvlan_mvlan_cancel").click()

# MVLAN Table #

def MVLAN_Table_Start_IP_Address(driver,value,sel):
    input = driver.find_element(By.ID, f"multicast_mvlantable_startIP_text_{sel}")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def MVLAN_Table_End_IP_Address(driver,value,sel):
    input = driver.find_element(By.ID, f"multicast_mvlantable_endIP_text_{sel}")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def MVLAN_Table_Add(driver):
    driver.find_element(By.ID, "multicast_mvlantable_apply").click()

def MVLAN_Table_Select(driver,sel):
    sel = str(sel)
    e_mod.Checkbox_EMS(driver,f"multicast_mvlantable_radio{sel}",True)

def MVLAN_Table_Modify(driver):
    driver.find_element(By.ID, "multicast_mvlantable_modify").click()

def MVLAN_Table_Clear(driver):
    driver.find_element(By.ID, "multicast_mvlantable_cancel").click()

# Multicast -> Multicast MAC # 

def Multicast_MAC_Select_Slot(driver,text):
    Select(driver.find_element(By.ID, "multcast_mcastmac_card_combobox")).select_by_value(text)
                                      
def Multicast_MAC_Select_Port(driver,text):
    Select(driver.find_element(By.ID, "multcast_mcastmac_port_combobox")).select_by_value(text)

def Multicast_MAC_Load(driver):
    driver.find_element(By.ID, "multcast_mcastmac_card_btn").click()

def Multicast_MAC_Address(driver,value):
    input = driver.find_element(By.ID, "multicast_mcastmac_mac_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def Multicast_MAC_NNI_VLAN(driver,value):
    input = driver.find_element(By.ID, "multicast_mcastmac_nnivlan_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def Multicast_MAC_Add(driver):
    driver.find_element(By.ID, "multicast_mcastmac_mac_add").click()

def Multicast_MAC_Delete(driver):
    driver.find_element(By.ID, "multicast_mcastmac_mac_delete").click()

def Multicast_MAC_Select(driver,index):
    e_mod.Radio(driver,"multicast_mcastmac_del_radio",str(index))

# Multicast -> Multicast IP #

def Multicast_IP_Select_Slot(driver,text):
    Select(driver.find_element(By.ID, "multcast_mcastip_card_combobox")).select_by_value(text)

def Multicast_IP_Select_Port(driver,text):
    Select(driver.find_element(By.ID, "multcast_mcastip_port_combobox")).select_by_visible_text(text)

def Multicast_IP_Load(driver):
    driver.find_element(By.ID, "multcast_mcastip_card_btn").click()

def Multicast_IP_Address(driver,value):
    input = driver.find_element(By.ID, "multicast_mcastip_ip_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def Multicast_IP_NNI_VLAN(driver,value):
    input = driver.find_element(By.ID, "multicast_mcastip_nnivlan_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def Multicast_IP_Role(driver,text):    
    Select(driver.find_element(By.ID, "multicast_mcastip_role_combobox")).select_by_visible_text(text)

def Multicast_IP_Add(driver):
    driver.find_element(By.ID, "multicast_mcastip_ip_add").click()

def Multicast_IP_Delete(driver):
    driver.find_element(By.ID, "multicast_mcastip_ip_delete").click()

def Multicast_IP_Select(driver,index):
    e_mod.Radio(driver,f"multicast_mcastip_del_radio{index}")
