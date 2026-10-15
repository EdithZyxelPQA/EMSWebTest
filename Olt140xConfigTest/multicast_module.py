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

# IGMP

# IGMP -> IGMP Setup

def IGMP_IGMP_Setup_Non_MVLAN_Mode(driver,num):
    #　Non MVLAN Mode
    select = driver.find_element(By.XPATH, f"//*[@name='rpmcigmp_sltMode']/option[{num}]")
    select.click()

def IGMP_IGMP_Setup_MVLAN_Mode(driver,num):
    #　MVLAN Mode
    select = driver.find_element(By.XPATH, f"//*[@name='rpmcigmp_sltMvlanMode']/option[{num}]")
    select.click()

def IGMP_IGMP_Setup_Version(driver,num):
    # Version
    select = driver.find_element(By.XPATH, f"//*[@name='rpmcigmp_sltVer']/option[{num}]")
    select.click()

def IGMP_IGMP_Setup_Leave_Mode(driver,num):
    # Leave-Mode
    select = driver.find_element(By.XPATH, f"//*[@name='rpmcigmp_sltLeave']/option[{num}]")
    select.click()

def IGMP_IGMP_Setup_Pbit(driver,num):
    # Pbit
    select = driver.find_element(By.XPATH, f"//*[@name='rpmcigmp_sltPbit']/option[{num}]")
    select.click()

def IGMP_IGMP_Setup_GQT_Interval(driver,key):
    # General-Query Timer -> Interval
    input = driver.find_element(By.NAME, "rpmcigmp_txtGqItv")
    input.clear()
    input.send_keys(key)

def IGMP_IGMP_Setup_GQT_Robustness(driver,key):
    # General-Query Timer -> Robustness
    input = driver.find_element(By.NAME, "rpmcigmp_txtGqRobust")
    input.clear()
    input.send_keys(key)

def IGMP_IGMP_Setup_GQT_Max_Response_Time(driver,key):
    # General-Query Timer -> Max-Response-Time
    input = driver.find_element(By.NAME, "rpmcigmp_txtRespTime")
    input.clear()
    input.send_keys(key)

def IGMP_IGMP_Setup_LMQT_Interval(driver,key):
    # Last-Member-Query Timer -> Interval
    input = driver.find_element(By.NAME, "rpmcigmp_txtLmqItv")
    input.clear()
    input.send_keys(key)

def IGMP_IGMP_Setup_LMQT_Robustness(driver,key):
    # Last-Member-Query Timer -> Robustness
    input = driver.find_element(By.NAME, "rpmcigmp_txtLmqRobust")
    input.clear()
    input.send_keys(key)

def IGMP_IGMP_Setup_Apply_Click(driver): 
    # Apply
    btn = driver.find_element(By.NAME, "rpmcigmp_btnApply")
    btn.click()
    
def IGMP_IGMP_Setup_Cancel_Click(driver): 
    # Cancel
    btn = driver.find_element(By.NAME, "rpmcigmp_btnCancel")
    btn.click()

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
    input.clear()
    input.send_keys(value)

def IGMP_Port_Setup_Max_Group(driver,value):
    input = driver.find_element(By.NAME, "rpmcigmpport_txtMg")
    input.clear()
    input.send_keys(value)

def IGMP_Port_Setup_Max_Message(driver,value):
    input = driver.find_element(By.NAME, "rpmcigmpport_txtMmeg")
    input.clear()
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
    input.clear()
    input.send_keys(value)

def IGMP_Port_MVLAN_Setup_Apply(driver):
    driver.find_element(By.NAME, "rpPortMvlanApply").click()

# IGMP -> Port Mode

def IGMP_Port_Mode_Static_querier(driver,sel):
    driver.find_element(By.XPATH, f"//*[@id='RpportMode_saSltStaticQuerier']/option[{sel}]").click()

def IGMP_Port_Mode_Apply(driver):
    driver.find_element(By.NAME, "rpportMode_btnApply").click()

# IGMP -> VLAN Mode

def IGMP_VLAN_Mode_mode(driver, text):
    Select(driver.find_element(By.NAME, "rpIgmpVlan_ipt_mode")).select_by_visible_text(text)    

def IGMP_VLAN_Mode_Apply(driver):
    driver.find_element(By.NAME, "rpVLANModeApply").click()

def IGMP_VLAN_Mode_VLAN(driver, value):
    driver.find_element(By.NAME, "rpIgmpVlan_ipt_vlan").clear()
    driver.find_element(By.NAME, "rpIgmpVlan_ipt_vlan").send_keys(value)

def IGMP_VLAN_Mode_Name(driver, value):
    driver.find_element(By.NAME, "rpIgmpVlan_ipt_name").clear()
    driver.find_element(By.NAME, "rpIgmpVlan_ipt_name").send_keys(value)

def IGMP_VLAN_Mode_VPN(driver, request):
    check_box = driver.find_element(By.NAME, "rpIgmpVlan_ipt_chkVpn")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def IGMP_VLAN_Mode_Add(driver):
    driver.find_element(By.NAME, "rpMvlanApply").click()

def IGMP_VLAN_Mode_Delete(driver):
    driver.find_element(By.NAME, "rpMvlanDelete").click()

def IGMP_VLAN_Mode_Cancle(driver):
    driver.find_element(By.NAME, "rpMvlanCancel").click()




# IGMP Privilege Profile

def IGMP_Privilege_Profile_Name(driver,value):
    input = driver.find_element(By.NAME, "rpigmpPriProf_ipt_profile_name")
    input.clear()
    input.send_keys(value)

def IGMP_Privilege_Profile_Index(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpigmpPriProf_slt_index']/option[{sel}]").click()

def IGMP_Privilege_Profile_Bandwidth(driver,value):
    input = driver.find_element(By.NAME, "rpigmpPriProf_ipt_bw")
    input.clear()
    input.send_keys(value)

def IGMP_Privilege_Profile_Start_Address(driver,value):
    input = driver.find_element(By.NAME, "rpigmpPriProf_ipt_st_add")
    input.clear()
    input.send_keys(value)

def IGMP_Privilege_Profile_End_Address(driver,value):
    input = driver.find_element(By.NAME, "rpigmpPriProf_ipt_end_add")
    input.clear()
    input.send_keys(value)

def IGMP_Privilege_Profile_Privilege(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpigmpPriProf_slt_privilege']/option[{sel}]").click()

def IGMP_Privilege_Profile_Length(driver,value):
    input = driver.find_element(By.NAME, "rpigmpPriProf_ipt_len")
    input.clear()
    input.send_keys(value)

def IGMP_Privilege_Profile_Interval(driver,value):
    input = driver.find_element(By.NAME, "rpigmpPriProf_ipt_interval")
    input.clear()
    input.send_keys(value)

def IGMP_Privilege_Profile_Count(driver,value):
    input = driver.find_element(By.NAME, "rpigmpPriProf_ipt_count")
    input.clear()
    input.send_keys(value)

def IGMP_Privilege_Profile_Reset(driver,value):
    input = driver.find_element(By.NAME, "rpigmpPriProf_ipt_reset")
    input.clear()
    input.send_keys(value)

def IGMP_Privilege_Profile_Apply_New(driver):
    driver.find_element(By.NAME, "rpigmpPriProf_config_button_apply").click()

def IGMP_Privilege_Profile_Delete_Entry(driver):
    driver.find_element(By.NAME, "rpigmpPriProf_config_button_cancel").click()

def IGMP_Privilege_Profile_Modify(driver):
    driver.find_element(By.NAME, "rpigmpPriProf_data_button_modify").click()

def IGMP_Privilege_Profile_Delete(driver):
    driver.find_element(By.NAME, "rpigmpPriProf_data_button_delete").click()

# MVLAN

# MVLAN -> MVLAN

def MVLAN_MVLAN_MVLAN(driver,value):
    input = driver.find_element(By.ID, "rpMvlan_mvlan")
    input.clear()
    input.send_keys(value)

def MVLAN_MVLAN_Pbit(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpMvlan_ipt_pbit']/option[{sel}]").click()

def MVLAN_MVLAN_Apply(driver):
    driver.find_element(By.NAME, "rpMvlanApply").click()

def MVLAN_MVLAN_Delete(driver):
    driver.find_element(By.NAME, "rpMvlanDelete").click()

# MVLAN -> MVLAN Table

def MVLAN_MVLAN_Table_Start_IP_Address(driver,index,value):
    input = driver.find_elements(By.NAME, "rpMvlanTbl_startIp")[index]
    input.clear()
    input.send_keys(value)

def MVLAN_MVLAN_Table_End_IP_Address(driver,index,value):
    input = driver.find_elements(By.NAME, "rpMvlanTbl_endIp")[index]
    input.clear()
    input.send_keys(value)

def MVLAN_MVLAN_Table_Apply(driver):
    driver.find_element(By.NAME, "rpMvlanTblApply").click()

def MVLAN_MVLAN_Table_Modify(driver):
    driver.find_element(By.NAME, "rpMvlanTblModify").click()

# Static Multicast

# Static Multicast -> Multicast MAC

def Static_Multicast_MAC_Address(driver,value):
    input = driver.find_element(By.NAME, "rpsmcastMac_txtMac")
    input.clear()
    input.send_keys(value)

def Static_Multicast_MAC_NNI_VLAN(driver,value):
    input = driver.find_element(By.NAME, "rpsmcastMac_txtVid")
    input.clear()
    input.send_keys(value)

def Static_Multicast_MAC_Apply(driver):
    driver.find_element(By.NAME, "rpsmcastMac_btnApply").click()

def Static_Multicast_MAC_Delete(driver):
    driver.find_element(By.NAME, "rpsmcastMac_btnDelete").click()

# Static Multicast -> Multicast IP

def Static_Multicast_IP_Address(driver,value):
    input = driver.find_element(By.NAME, "rpsmcastIp_txtIp")
    input.clear()
    input.send_keys(value)

def Static_Multicast_IP_NNI_VLAN(driver,value):
    input = driver.find_element(By.NAME, "rpsmcastIp_txtVid")
    input.clear()
    input.send_keys(value)

def Static_Multicast_IP_Role(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpsmcastIp_txtRole']/option[{sel}]").click()

def Static_Multicast_IP_Apply(driver):
    driver.find_element(By.NAME, "rpsmcastIp_btnApply").click()

def Static_Multicast_IP_Delete(driver):
    driver.find_element(By.NAME, "rpsmcastIp_btnDelete").click()
