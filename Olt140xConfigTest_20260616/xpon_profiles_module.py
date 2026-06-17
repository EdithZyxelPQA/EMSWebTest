from os import times
import time
from attr import field
from pyrsistent import s
import selenium_module as mod
from selenium.webdriver.support.ui import Select
import pyautogui
from selenium.webdriver.common.by import By


# Template Profile

def Template_New(driver):
    driver.find_element(By.CLASS_NAME, "font-btn").click()

def Template_Delete(driver):
    driver.find_element(By.NAME, "rpXgponTemplate_TablebtnDelete").click()

def Template_Delete_All_Select(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponTemplate_chkDelall")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
###
# def Template_Delete_Select_1(driver):
#     check_box = driver.find_elements(By.NAME, "rpXGSponTemplate_chkDel")[0].click()

# def Template_Delete_Select_2(driver):
#     check_box = driver.find_elements(By.NAME, "rpXGSponTemplate_chkDel")[1].click()

def Template_Delete_Select(driver,index):
    driver.find_elements(By.NAME, "rpXGSponTemplate_chkDel")[index-1].click()

def Template_New_Name(driver,value):
    driver.find_element(By.ID, "rpXGSponTemplate_IptProfName").clear()
    driver.find_element(By.ID, "rpXGSponTemplate_IptProfName").send_keys(value)

def Template_New_Apply(driver):
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[0].click()

def Template_New_Delete(driver):
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()

def Template_New_fec(driver,request):
    check_box = driver.find_element(By.ID, f"rpXGSponTemplate_Fec")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

###
def Template_New_UNI_Profile(driver,text):
    Select(driver.find_element(By.ID, "rpXGSponTemplate_UniProf")).select_by_visible_text(text)

def Template_New_Security_Profile(driver,text):
    Select(driver.find_element(By.ID, "rpXGSponTemplate_SecuProf")).select_by_visible_text(text)

def Template_New_Alarm_Profile(driver,text):
    Select(driver.find_element(By.ID, "rpXGSponTemplate_AlarmProf")).select_by_visible_text(text)

def Template_New_Ont_Profile(driver,text):
    Select(driver.find_element(By.ID, "rpXGSponTemplate_OntProf")).select_by_visible_text(text)
###

def Template_New_Main_UNI_Profile(driver,text):
    Select(driver.find_element(By.ID, "rpXGSponTemplate_UniProf")).select_by_visible_text(text)

def Template_New_Main_Security_Profile(driver,text):
    Select(driver.find_element(By.ID, "rpXGSponTemplate_SecuProf")).select_by_visible_text(text)

def Template_New_Main_Alarm_Profile(driver,text):
    Select(driver.find_element(By.ID, "rpXGSponTemplate_AlarmProf")).select_by_visible_text(text)

def Template_New_Main_Ont_Profile(driver,text):
    Select(driver.find_element(By.ID, "rpXGSponTemplate_OntProf")).select_by_visible_text(text)



# Template Profile -> Service

def Template_New_Service_Profile_Active_all(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponTemplate_saServiceActive")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Template_New_Service_Profile_Active_Select(driver,index,request):
    check_box = driver.find_elements(By.ID, "rpXGSponTemplate_serviceActive")[index-1]
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Template_New_Service_Profile_all(driver,text):
    Select(driver.find_element(By.NAME, "rpXGSponTemplate_ServiceProf")).select_by_visible_text(text)
    # Select(driver.find_element(By.NAME, "rpXGSponTemplate_slt_saServiceProf")).select_by_visible_text(text)
    # unable use on website, it is in <!-- -->
def Template_New_Service_Profile_Select(driver,index,text):
    Select(driver.find_elements(By.ID, "rpXGSponTemplate_ServiceProf")[index-1]).select_by_visible_text(text)

def Template_New_Service_Shared_Priority_all(driver,text):
    Select(driver.find_element(By.NAME, "rpXGSponTemplate_slt_saServiceSharedPri")).select_by_visible_text(text)

def Template_New_Service_Shared_Priority_Select(driver,index,text):
    Select(driver.find_elements(By.ID, "rpXGSponTemplate_ServiceSharedPri")[index-1]).select_by_visible_text(text)

def Template_New_Service_US_Bandwidth_Profile_all(driver,text):
    Select(driver.find_element(By.NAME, "rpXGSponTemplate_slt_saServiceUSBWProf")).select_by_visible_text(text)

def Template_New_Service_US_Bandwidth_Profile_Select(driver,index,text):
    Select(driver.find_elements(By.ID, "rpXGSponTemplate_ServiceUSBWProf")[index-1]).select_by_visible_text(text)

def Template_New_Service_DS_Bandwidth_Profile_all(driver,text):
    Select(driver.find_element(By.NAME, "rpXGSponTemplate_slt_saServiceDSBWProf")).select_by_visible_text(text)

def Template_New_Service_DS_Bandwidth_Profile_Select(driver,index,text):
    Select(driver.find_elements(By.ID, "rpXGSponTemplate_ServiceDSBWProf")[index-1]).select_by_visible_text(text)

# Template Profile -> T-cont

def Template_New_Tcont_Service_List_Active_all(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponTemplate_saTcontActive")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Template_New_Tcont_Service_List_Active_Select(driver,index,request):
    check_box = driver.find_elements(By.ID, "rpXGSponTemplate_tcontActive")[index-1]
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Template_New_Tcont_Service_List_all(driver,text):
    Select(driver.find_element(By.NAME, "rpXGSponTemplate_TcontServices")).select_by_visible_text(text)

def Template_New_Tcont_Service_List_Select(driver,index,text):
    Select(driver.find_elements(By.ID, "rpXGSponTemplate_TcontServices")[index-1]).select_by_visible_text(text)

def Template_New_Tcont_US_Bandwidth_Profile_all(driver,text):
    Select(driver.find_element(By.NAME, "rpXGSponTemplate_slt_saTcontUSBWProf")).select_by_visible_text(text)

def Template_New_Tcont_US_Bandwidth_Profile_Select(driver,index,text):
    Select(driver.find_elements(By.ID, "rpXGSponTemplate_TcontUSBWProf")[index-1]).select_by_visible_text(text)

def Template_New_Tcont_DS_Bandwidth_Profile_all(driver,text):
    Select(driver.find_element(By.NAME, "rpXGSponTemplate_slt_saTcontDSBWProf")).select_by_visible_text(text)

def Template_New_Tcont_DS_Bandwidth_Profile_Select(driver,index,text):
    Select(driver.find_elements(By.ID, "rpXGSponTemplate_TcontDSBWProf")[index-1]).select_by_visible_text(text)

def Template_New_Tcont_Type_all(driver,text):
    Select(driver.find_element(By.NAME, "rpXGSponTemplate_slt_saTcontType")).select_by_visible_text(text)

def Template_New_Tcont_Type_Select(driver,index,text):
    Select(driver.find_elements(By.ID, "rpXGSponTemplate_TcontType")[index-1]).select_by_visible_text(text)

# Template Profile -> Multicast

def Template_New_Multicast_Profile_Active_all(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponTemplate_saMcastActive")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Template_New_Multicast_Profile_Active_Select(driver,index,request):
    check_box = driver.find_elements(By.ID, "rpXGSponTemplate_mcastActive")[index-1]
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Template_New_Multicast_Profile_all(driver,text):
    Select(driver.find_element(By.NAME, "rpXGSponTemplate_slt_saMcastProf")).select_by_visible_text(text)

def Template_New_Multicast_Profile_Select(driver,index,text):
    Select(driver.find_elements(By.ID, "rpXGSponTemplate_McastProf")[index-1]).select_by_visible_text(text)

# def Template_New_tcont_Active_all(driver,request):
#     check_box = driver.find_element(By.NAME, "rpXGSponTemplate_saTcontActive")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def Template_New_US_Bandwidth_Profile_all(driver,text):
#     Select(driver.find_element(By.NAME, "rpXGSponTemplate_slt_saTcontUSBWProf")).select_by_visible_text(text)

# def Template_New_DS_Bandwidth_Profile_all(driver,text):
#     Select(driver.find_element(By.NAME, "rpXGSponTemplate_slt_saTcontDSBWProf")).select_by_visible_text(text)

# def Template_New_Multicast_Profile_Active_all(driver,request):
#     check_box = driver.find_element(By.NAME, "rpXGSponTemplate_saMcastActive")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def Template_New_Multicast_Profile_all(driver,text):
#     Select(driver.find_element(By.NAME, "rpXGSponTemplate_slt_saMcastProf")).select_by_visible_text(text)

# Service Profile   

def Service_Profile_New(driver):
    driver.find_element(By.CLASS_NAME, "font-btn").click()

def Service_Profile_Delete(driver):
    driver.find_element(By.NAME, "rpXgponServiceProf_TablebtnDelete").click()

def Service_Profile_Delete_All_Select(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponSecuProf_chkDelall")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Service_Profile_Delete_Select(driver,index):
    driver.find_elements(By.NAME, "rpXGSponServiceProf_chkDel")[index-1].click()

def Service_Profile_New_Name(driver,value):
    driver.find_element(By.ID, "rpXGSponServiceProf_IptProfName").clear()
    driver.find_element(By.ID, "rpXGSponServiceProf_IptProfName").send_keys(value)

def Service_Profile_New_VLAN(driver,value):
    driver.find_element(By.ID, "rpXGSponServiceProf_vlan").clear()
    driver.find_element(By.ID, "rpXGSponServiceProf_vlan").send_keys(value)

def Service_Profile_New_Mapper_Pbits(driver,num,request):
    check_box = driver.find_element(By.NAME, f"rpXGSponServiceProf_chkUniPbit{num}")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Service_Profile_New_Lan_mode_veip(driver):
    driver.find_elements(By.ID, "rpXGSponServiceProf_mode")[0].click()

def Service_Profile_New_Lan_mode_bridge(driver):
    driver.find_elements(By.ID, "rpXGSponServiceProf_mode")[1].click()

def Service_Profile_New_Lan(driver,text):
    # driver.find_element(By.XPATH, f"//*[@id='rpXGSponServiceProf_sltlanport']/option[{sel}]").click()
    Select(driver.find_element(By.ID, "rpXGSponServiceProf_sltlanport")).select_by_visible_text(text)

def Service_Profile_New_Vlan_xc(driver,value):
    driver.find_element(By.ID, "rpXGSponServiceProf_vlanxc").clear()
    driver.find_element(By.ID, "rpXGSponServiceProf_vlanxc").send_keys(value)

def Service_Profile_New_Vlan_xc_mode_enable(driver):
    driver.find_elements(By.ID, "rpXGSponServiceProf_vlanxcmode")[0].click()

def Service_Profile_New_Vlan_xc_mode_disable(driver):
    driver.find_elements(By.ID, "rpXGSponServiceProf_vlanxcmode")[1].click()

def Service_Profile_New_Apply(driver):
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[0].click()

def Service_Profile_New_Delete(driver):
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()

    # try:
    #     driver.find_element(By.ID, "rpXGSponServiceProf_vlanxcmode")
    #     print("yes",file = open("Web_auto_Report.txt", '+a'))
    # except:
    #     print("no",file = open("Web_auto_Report.txt", '+a'))

# QoS Bandwidth Profile

def QoS_Bandwidth_Profile_New(driver):
    driver.find_element(By.CLASS_NAME, "font-btn").click()

def QoS_Bandwidth_Profile_Delete(driver):
    driver.find_element(By.NAME, "rpXgponqosbwprof_TablebtnDelete").click()

def QoS_Bandwidth_Profile_Delete_All_Select(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponQosBwProf_chkDelall")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def QoS_Bandwidth_Profile_New_Name(driver,value):
    driver.find_element(By.ID, "rpXGSponQosBwProf_IptProfName").clear()
    driver.find_element(By.ID, "rpXGSponQosBwProf_IptProfName").send_keys(value)

def QoS_Bandwidth_Profile_New_sir(driver,value):
    driver.find_element(By.ID, "rpXGSponQosBwProf_sir").clear()
    driver.find_element(By.ID, "rpXGSponQosBwProf_sir").send_keys(value)

def QoS_Bandwidth_Profile_New_air(driver,value):
    driver.find_element(By.ID, "rpXGSponQosBwProf_air").clear()
    driver.find_element(By.ID, "rpXGSponQosBwProf_air").send_keys(value)

def QoS_Bandwidth_Profile_New_pir(driver,value):
    driver.find_element(By.ID, "rpXGSponQosBwProf_pir").clear()
    driver.find_element(By.ID, "rpXGSponQosBwProf_pir").send_keys(value)

def QoS_Bandwidth_Profile_New_Apply(driver):
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[0].click()

def QoS_Bandwidth_Profile_New_Delete(driver):
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()

# Multicast Profile

def Multicast_Profile_New(driver):
    driver.find_element(By.CLASS_NAME, "font-btn").click()

def Multicast_Profile_Delete(driver):
    driver.find_element(By.NAME, "rpXgponMcastProf_TablebtnDelete").click()

def Multicast_Profile_Delete_All_Select(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponMcastProf_chkDelall")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Multicast_Profile_Delete_Select(driver,index):
    driver.find_elements(By.NAME, "rpXGSponMcastProf_chkDel")[index-1].click()

def Multicast_Profile_New_Name(driver,value):
    driver.find_element(By.ID, "rpXGSponMcastProf_IptProfName").clear()
    driver.find_element(By.ID, "rpXGSponMcastProf_IptProfName").send_keys(value)

def Multicast_Profile_New_UNI_VID(driver,value):
    driver.find_element(By.ID, "rpXGSponMcastProf_uniVid").clear()
    driver.find_element(By.ID, "rpXGSponMcastProf_uniVid").send_keys(value)
    
def Multicast_Profile_New_IGMP_Version(driver,text):
    Select(driver.find_element(By.ID, "rpXGSponMcastProf_igmpVersion")).select_by_visible_text(text)
    
def Multicast_Profile_New_Tx_Tag_Mode(driver,text):
    Select(driver.find_element(By.ID, "rpXGSponMcastProf_txTagMode")).select_by_visible_text(text)

def Multicast_Profile_New_Tx_Tag_VID(driver,value):
    driver.find_element(By.ID, "rpXGSponMcastProf_txTagVid").clear()
    driver.find_element(By.ID, "rpXGSponMcastProf_txTagVid").send_keys(value)
    
def Multicast_Profile_New_Tx_Tag_Pbit(driver,text):
    Select(driver.find_element(By.ID, "rpXGSponMcastProf_txTagPbit")).select_by_visible_text(text)
    
def Multicast_Profile_New_Group_Privilege_Profile(driver,text):
    Select(driver.find_element(By.ID, "rpXGSponMcastProf_privilegeProf")).select_by_visible_text(text)

def Multicast_Profile_New_Max_Group(driver,value):
    driver.find_element(By.ID, "rpXGSponMcastProf_maxGroup").clear()
    driver.find_element(By.ID, "rpXGSponMcastProf_maxGroup").send_keys(value)

def Multicast_Profile_New_Max_Message(driver,value):
    driver.find_element(By.ID, "rpXGSponMcastProf_maxMsg").clear()
    driver.find_element(By.ID, "rpXGSponMcastProf_maxMsg").send_keys(value)

def Multicast_Profile_New_Apply(driver):
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[0].click()

def Multicast_Profile_New_Delete(driver):
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()

# Uni Profile

def Uni_Profile_New(driver):
    driver.find_element(By.CLASS_NAME, "font-btn").click()

def Uni_Profile_Delete(driver):
    driver.find_element(By.NAME, "rpXgponSecuProf_TablebtnDelete").click() ###

def Uni_Profile_Delete_All_Select(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponUniProf_chkDelall") 
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Uni_Profile_Delete_Select(driver,index):
    driver.find_elements(By.NAME, "rpXGSponUniProf_chkDel")[index-1].click()

def Uni_Profile_New_Apply(driver):
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[0].click()

def Uni_Profile_New_Delete(driver):
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()

# Uni Profile -> Lan

def Uni_Profile_New_Name(driver,value):
    driver.find_element(By.ID, "rpXGSponUniProf_IptProfName").clear()
    driver.find_element(By.ID, "rpXGSponUniProf_IptProfName").send_keys(value)

def Uni_Profile_New_Lan_Vlan_Active(driver,num,request):
    check_box = driver.find_elements(By.ID, "rpXGSponUniProf_lantagoperActive")[num-1]  ###8
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Uni_Profile_New_Lan_Filter_ethertype(driver,num):
    # driver.find_elements(By.ID, "rpXGSponUniProf_lantagfilter")[3*(num-1)].click()
    driver.find_elements(By.ID, "rpXGSponUniProf_lantag_ethertype_filter")[num-1].click()

def Uni_Profile_New_Lan_Filter_ethertype_Value(driver,num,text):
# 第二種寫法 
# if(num == 0):
#     Select(driver.find_element(By.ID, "rpXGSponUniProf_lantagfilterether")).select_by_visible_text(text) #只能是第0個
# else:
#     Select(driver.find_elements(By.ID, "rpXGSponUniProf_lantagfilterether")[num-1]).select_by_visible_text(text)
# 第三種寫法 
# a = driver.find_elements(By.ID, "rpXGSponUniProf_lantagfilterether")[0]
# Select(a).select_by_visible_text("ipoe")
    Select(driver.find_elements(By.ID, "rpXGSponUniProf_lantagfilterether")[num-1]).select_by_visible_text(text)

def Uni_Profile_New_Lan_Filter_uniVlan(driver,num):
    # driver.find_elements(By.ID, "rpXGSponUniProf_lantagfilter")[3*(num-1)+1].click()
    driver.find_elements(By.ID, "rpXGSponUniProf_lantag_unvlan_filter")[num-1].click()
    

def Uni_Profile_New_Lan_Filter_uniVlan_Value(driver,num,value):
    driver.find_elements(By.ID, "rpXGSponUniProf_lantagfilteruni")[num-1].clear()
    driver.find_elements(By.ID, "rpXGSponUniProf_lantagfilteruni")[num-1].send_keys(value)

def Uni_Profile_New_Lan_Filter_untag(driver,num):
    # driver.find_elements(By.ID, "rpXGSponUniProf_lantagfilter")[3*(num-1)+2].click()
    driver.find_elements(By.ID, "rpXGSponUniProf_lantag_untag_filter")[num-1].click()

def Uni_Profile_New_Lan_UniportList(driver,num,value):
    driver.find_elements(By.ID, "rpXGSponUniProf_lantagporlist")[num-1].clear()
    driver.find_elements(By.ID, "rpXGSponUniProf_lantagporlist")[num-1].send_keys(value)

def Uni_Profile_New_Lan_Vlan(driver,num,value):
    driver.find_elements(By.ID, "rpXGSponUniProf_lantagvlan")[num-1].clear()
    driver.find_elements(By.ID, "rpXGSponUniProf_lantagvlan")[num-1].send_keys(value)   

def Uni_Profile_New_Lan_fdb_count_all(driver,value):
    driver.find_element(By.NAME, "rpXGSponUniProf_saLanMaxFdbCnt").clear()
    driver.find_element(By.NAME, "rpXGSponUniProf_saLanMaxFdbCnt").send_keys(value) 

def Uni_Profile_New_Lan_DS_rate_all(driver,value):
    driver.find_element(By.NAME, "rpXGSponUniProf_saLanDsPir").clear()
    driver.find_element(By.NAME, "rpXGSponUniProf_saLanDsPir").send_keys(value) 

def Uni_Profile_New_Lan_Storm_B_all(driver,value):
    driver.find_element(By.NAME, "rpXGSponUniProf_saLanStormBcast").clear()
    driver.find_element(By.NAME, "rpXGSponUniProf_saLanStormBcast").send_keys(value) 

def Uni_Profile_New_Lan_Storm_M_all(driver,value):
    driver.find_element(By.NAME, "rpXGSponUniProf_saLanStormMcast").clear()
    driver.find_element(By.NAME, "rpXGSponUniProf_saLanStormMcast").send_keys(value) 

def Uni_Profile_New_Lan_Storm_D_all(driver,value):
    driver.find_element(By.NAME, "rpXGSponUniProf_saLanStormDlf").clear()
    driver.find_element(By.NAME, "rpXGSponUniProf_saLanStormDlf").send_keys(value) 

# Uni Profile -> XLan

def Uni_Profile_New_XLan_Vlan_Active(driver,num,request):
    check_box = driver.find_elements(By.ID, "rpXGSponUniProf_xlantagoperActive")[num-1]  ###8
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Uni_Profile_New_XLan_Filter_ethertype(driver,num):
    # driver.find_elements(By.ID, "rpXGSponUniProf_xlantagfilter")[3*(num-1)].click()
    driver.find_elements(By.ID, "rpXGSponUniProf_xlantag_ethertype_filter")[num-1].click()

def Uni_Profile_New_XLan_Filter_ethertype_Value(driver,num,text):
    Select(driver.find_elements(By.ID, "rpXGSponUniProf_xlantagfilterether")[num-1]).select_by_visible_text(text)

def Uni_Profile_New_XLan_Filter_uniVlan(driver,num):
    # driver.find_elements(By.ID, "rpXGSponUniProf_xlantagfilter")[3*(num-1)+1].click()
    driver.find_elements(By.ID, "rpXGSponUniProf_xlantag_unvlan_filter")[num-1].click()

def Uni_Profile_New_XLan_Filter_uniVlan_Value(driver,num,value):
    driver.find_elements(By.ID, "rpXGSponUniProf_xlantagfilteruni")[num-1].clear()
    driver.find_elements(By.ID, "rpXGSponUniProf_xlantagfilteruni")[num-1].send_keys(value)

def Uni_Profile_New_XLan_Filter_untag(driver,num):
    # driver.find_elements(By.ID, "rpXGSponUniProf_xlantagfilter")[3*(num-1)+2].click()
    driver.find_elements(By.ID, "rpXGSponUniProf_xlantag_untag_filter")[num-1].click()

def Uni_Profile_New_XLan_UniportList(driver,num,value):
    driver.find_elements(By.ID, "rpXGSponUniProf_xlantagporlist")[num-1].clear()
    driver.find_elements(By.ID, "rpXGSponUniProf_xlantagporlist")[num-1].send_keys(value)

def Uni_Profile_New_XLan_Vlan(driver,num,value):
    driver.find_elements(By.ID, "rpXGSponUniProf_xlantagvlan")[num-1].clear()
    driver.find_elements(By.ID, "rpXGSponUniProf_xlantagvlan")[num-1].send_keys(value)   

def Uni_Profile_New_XLan_fdb_count_all(driver,value):
    driver.find_element(By.NAME, "rpXGSponUniProf_saXlanMaxFdbCnt").clear()
    driver.find_element(By.NAME, "rpXGSponUniProf_saXlanMaxFdbCnt").send_keys(value) 

def Uni_Profile_New_XLan_DS_rate_all(driver,value):
    driver.find_element(By.NAME, "rpXGSponUniProf_saXlanDsPir").clear()
    driver.find_element(By.NAME, "rpXGSponUniProf_saXlanDsPir").send_keys(value) 

def Uni_Profile_New_XLan_Storm_B_all(driver,value):
    driver.find_element(By.NAME, "rpXGSponUniProf_saXlanStormBcast").clear()
    driver.find_element(By.NAME, "rpXGSponUniProf_saXlanStormBcast").send_keys(value) 

def Uni_Profile_New_XLan_Storm_M_all(driver,value):
    driver.find_element(By.NAME, "rpXGSponUniProf_saXlanStormMcast").clear()
    driver.find_element(By.NAME, "rpXGSponUniProf_saXlanStormMcast").send_keys(value) 

def Uni_Profile_New_XLan_Storm_D_all(driver,value):
    driver.find_element(By.NAME, "rpXGSponUniProf_saXlanStormDlf").clear()
    driver.find_element(By.NAME, "rpXGSponUniProf_saXlanStormDlf").send_keys(value) 

# Uni Profile -> Veip

def Uni_Profile_New_Veip_Vlan_Active(driver,num,request):
    check_box = driver.find_elements(By.ID, "rpXGSponUniProf_veiptagoperActive")[num-1]  ###8
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Uni_Profile_New_Veip_Filter_ethertype(driver,num):
    # driver.find_elements(By.ID, "rpXGSponUniProf_veiptagfilter")[3*(num-1)].click()
    driver.find_elements(By.ID, "rpXGSponUniProf_veiptag_ethertype_filter")[num-1].click()

def Uni_Profile_New_Veip_Filter_ethertype_Value(driver,num,text):
    Select(driver.find_elements(By.ID, "rpXGSponUniProf_veiptagfilterether")[num-1]).select_by_visible_text(text)

def Uni_Profile_New_Veip_Filter_uniVlan(driver,num):
    # driver.find_elements(By.ID, "rpXGSponUniProf_veiptagfilter")[3*(num-1)+1].click()
    driver.find_elements(By.ID, "rpXGSponUniProf_veiptag_unvlan_filter")[num-1].click()

def Uni_Profile_New_Veip_Filter_uniVlan_Value(driver,num,value):
    driver.find_elements(By.ID, "rpXGSponUniProf_veiptagfilteruni")[num-1].clear()
    driver.find_elements(By.ID, "rpXGSponUniProf_veiptagfilteruni")[num-1].send_keys(value)

def Uni_Profile_New_Veip_Filter_untag(driver,num):
    # driver.find_elements(By.ID, "rpXGSponUniProf_veiptagfilter")[3*(num-1)+2].click()
    driver.find_elements(By.ID, "rpXGSponUniProf_veiptag_untag_filter")[num-1].click()

def Uni_Profile_New_Veip_UniportList(driver,num,value):
    driver.find_elements(By.ID, "rpXGSponUniProf_veiptagporlist")[num-1].clear()
    driver.find_elements(By.ID, "rpXGSponUniProf_veiptagporlist")[num-1].send_keys(value)

def Uni_Profile_New_Veip_Vlan(driver,num,value):
    driver.find_elements(By.ID, "rpXGSponUniProf_veiptagvlan")[num-1].clear()
    driver.find_elements(By.ID, "rpXGSponUniProf_veiptagvlan")[num-1].send_keys(value)   

def Uni_Profile_New_Veip_fdb_count(driver,num,value):
    driver.find_elements(By.ID, "rpXGSponUniProf_veipMaxFdbCnt")[num-1].clear()
    driver.find_elements(By.ID, "rpXGSponUniProf_veipMaxFdbCnt")[num-1].send_keys(value) 

def Uni_Profile_New_Veip_DS_rate(driver,num,value):
    driver.find_elements(By.ID, "rpXGSponUniProf_veipDsLimit")[num-1].clear()
    driver.find_elements(By.ID, "rpXGSponUniProf_veipDsLimit")[num-1].send_keys(value) 

def Uni_Profile_New_Veip_Storm_B(driver,num,value):
    driver.find_elements(By.ID, "rpXGSponUniProf_veipStormCtrlBcast")[num-1].clear()
    driver.find_elements(By.ID, "rpXGSponUniProf_veipStormCtrlBcast")[num-1].send_keys(value) 

def Uni_Profile_New_Veip_Storm_M(driver,num,value):
    driver.find_elements(By.ID, "rpXGSponUniProf_veipStormCtrlMcast")[num-1].clear()
    driver.find_elements(By.ID, "rpXGSponUniProf_veipStormCtrlMcast")[num-1].send_keys(value) 

def Uni_Profile_New_Veip_Storm_D(driver,num,value):
    driver.find_elements(By.ID, "rpXGSponUniProf_veipStormCtrlDlf")[num-1].clear()
    driver.find_elements(By.ID, "rpXGSponUniProf_veipStormCtrlDlf")[num-1].send_keys(value) 

# Uni Profile -> Lan port

def Uni_Profile_New_Lan_Port_Active(driver,num,request):
    check_box = driver.find_elements(By.ID, "rpXGSponUniProf_lantagoperActive")[num]  ###8
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Uni_Profile_New_Lan_Port_FDB(driver,value):
    driver.find_element(By.NAME, "rpXGSponUniProf_saLanMaxFdbCnt").clear()
    driver.find_element(By.NAME, "rpXGSponUniProf_saLanMaxFdbCnt").send_keys(value)

def Uni_Profile_New_Lan_Port_DS(driver,value):
    driver.find_element(By.NAME, "rpXGSponUniProf_saLanDsPir").clear()
    driver.find_element(By.NAME, "rpXGSponUniProf_saLanDsPir").send_keys(value)

def Uni_Profile_New_Lan_Port_Storm_B(driver,value):
    driver.find_element(By.NAME, "rpXGSponUniProf_saLanStormBcast").clear()
    driver.find_element(By.NAME, "rpXGSponUniProf_saLanStormBcast").send_keys(value)

def Uni_Profile_New_Lan_Port_Storm_M(driver,value):
    driver.find_element(By.NAME, "rpXGSponUniProf_saLanStormMcast").clear()
    driver.find_element(By.NAME, "rpXGSponUniProf_saLanStormMcast").send_keys(value)

def Uni_Profile_New_Lan_Port_Storm_D(driver,value):
    driver.find_element(By.NAME, "rpXGSponUniProf_saLanStormDlf").clear()
    driver.find_element(By.NAME, "rpXGSponUniProf_saLanStormDlf").send_keys(value)

# Uni Profile -> XLan port

def Uni_Profile_New_XLan_Port_Active(driver,num,request):
    check_box = driver.find_elements(By.ID, "rpXGSponUniProf_xlantagoperActive")[num]  ###8
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Uni_Profile_New_XLan_Port_FDB(driver,value):
    driver.find_element(By.NAME, "rpXGSponUniProf_saXlanMaxFdbCnt").clear()
    driver.find_element(By.NAME, "rpXGSponUniProf_saXlanMaxFdbCnt").send_keys(value)

def Uni_Profile_New_XLan_Port_DS(driver,value):
    driver.find_element(By.NAME, "rpXGSponUniProf_saXlanDsPir").clear()
    driver.find_element(By.NAME, "rpXGSponUniProf_saXlanDsPir").send_keys(value)

def Uni_Profile_New_XLan_Port_Storm_B(driver,value):
    driver.find_element(By.NAME, "rpXGSponUniProf_saXlanStormBcast").clear()
    driver.find_element(By.NAME, "rpXGSponUniProf_saXlanStormBcast").send_keys(value)

def Uni_Profile_New_XLan_Port_Storm_M(driver,value):
    driver.find_element(By.NAME, "rpXGSponUniProf_saXlanStormMcast").clear()
    driver.find_element(By.NAME, "rpXGSponUniProf_saXlanStormMcast").send_keys(value)

def Uni_Profile_New_XLan_Port_Storm_D(driver,value):
    driver.find_element(By.NAME, "rpXGSponUniProf_saXlanStormDlf").clear()
    driver.find_element(By.NAME, "rpXGSponUniProf_saXlanStormDlf").send_keys(value)

# Uni Profile -> Veip port

def Uni_Profile_New_Veip_Port_Active(driver,num,request):
    check_box = driver.find_elements(By.ID, "rpXGSponUniProf_xlantagoperActive")[num]  ###8
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Uni_Profile_New_Veip_Port_FDB(driver,value):
    driver.find_element(By.NAME, "rpXGSponUniProf_veipMaxFdbCnt").clear()
    driver.find_element(By.NAME, "rpXGSponUniProf_veipMaxFdbCnt").send_keys(value)

def Uni_Profile_New_Veip_Port_DS(driver,value):
    driver.find_element(By.NAME, "rpXGSponUniProf_veipDsPir").clear()
    driver.find_element(By.NAME, "rpXGSponUniProf_veipDsPir").send_keys(value)

def Uni_Profile_New_Veip_Port_Storm_B(driver,value):
    driver.find_element(By.NAME, "rpXGSponUniProf_veipStormCtrlBcast").clear()
    driver.find_element(By.NAME, "rpXGSponUniProf_veipStormCtrlBcast").send_keys(value)

def Uni_Profile_New_Veip_Port_Storm_M(driver,value):
    driver.find_element(By.NAME, "rpXGSponUniProf_veipStormMcast").clear()
    driver.find_element(By.NAME, "rpXGSponUniProf_veipStormMcast").send_keys(value)

def Uni_Profile_New_Veip_Port_Storm_D(driver,value):
    driver.find_element(By.NAME, "rpXGSponUniProf_veipStormDlf").clear()
    driver.find_element(By.NAME, "rpXGSponUniProf_veipStormDlf").send_keys(value)

# Security Profile


def Security_Profile_New(driver):
    driver.find_element(By.CLASS_NAME, "font-btn").click()

def Security_Profile_Delete(driver):
    driver.find_element(By.NAME, "rpXgponSecuProf_TablebtnDelete").click()

def Security_Profile_Delete_All_Select(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponMcastProf_chkDelall") ###
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Security_Profile_Delete_Select(driver,index):
    driver.find_elements(By.NAME, "rpXGSponSecuProf_chkDel")[index-1].click()

def Security_Profile_New_Name(driver,value):
    driver.find_element(By.ID, "rpXGSponSecuProf_IptProfName").clear()
    driver.find_element(By.ID, "rpXGSponSecuProf_IptProfName").send_keys(value)

def Security_Profile_New_anti(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponSecuProf_antiMacSpoofing")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Security_Profile_New_fdb(driver,value):
    driver.find_element(By.ID, "rpXGSponSecuProf_maxFdbCnt").clear()
    driver.find_element(By.ID, "rpXGSponSecuProf_maxFdbCnt").send_keys(value)

def Security_Profile_New_Apply(driver):
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[0].click()

def Security_Profile_New_Delete(driver):
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()

# Ont Profile

def Ont_Profile_New(driver):
    driver.find_element(By.CLASS_NAME, "font-btn").click()

def Ont_Profile_Delete(driver):
    driver.find_element(By.NAME, "rpXgponOntProf_TablebtnDelete").click()

def Ont_Profile_Delete_All_Select(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponMcastProf_chkDelall")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Ont_Profile_Delete_Select(driver,index):
    driver.find_elements(By.NAME, "rpXGSponOntProf_chkDel")[index-1].click()

def Ont_Profile_New_Apply(driver):
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[0].click()

def Ont_Profile_New_Delete(driver):
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()

# Ont Profile -> Service

def Ont_Profile_New_Name(driver,value):
    driver.find_element(By.ID, "rpXGSponOntProf_IptProfName").clear()
    driver.find_element(By.ID, "rpXGSponOntProf_IptProfName").send_keys(value)

def Ont_Profile_New_Service_Control(driver,request):
    check_box = driver.find_element(By.ID, f"rpXGSponOntProf_controlService")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Ont_Profile_New_Service_lcmp_enable(driver,text):
    Select(driver.find_element(By.ID, "rpXGSponOntProf_svc_icmpEnable")).select_by_visible_text(text)

def Ont_Profile_New_Service_ftp_enable(driver,text):
    Select(driver.find_element(By.ID, "rpXGSponOntProf_svc_ftpEnable")).select_by_visible_text(text)

def Ont_Profile_New_Service_Http_enable(driver,text):
    Select(driver.find_element(By.ID, "rpXGSponOntProf_svc_httpEnable")).select_by_visible_text(text)

def Ont_Profile_New_Service_Https_enable(driver,text):
    Select(driver.find_element(By.ID, "rpXGSponOntProf_svc_httpsEnable")).select_by_visible_text(text)

def Ont_Profile_New_Service_Snmp_enable(driver,text):
    Select(driver.find_element(By.ID, "rpXGSponOntProf_svc_snmpEnable")).select_by_visible_text(text)

def Ont_Profile_New_Service_Telnet_enable(driver,text):
    Select(driver.find_element(By.ID, "rpXGSponOntProf_svc_telnetEnable")).select_by_visible_text(text)

def Ont_Profile_New_Service_SSH_enable(driver,text):
    Select(driver.find_element(By.ID, "rpXGSponOntProf_svc_sshEnable")).select_by_visible_text(text)

def Ont_Profile_New_Service_Firewall_control(driver,request):
    check_box = driver.find_element(By.ID, f"rpXGSponOntProf_controlFirewall")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Ont_Profile_New_Service_Firewall_enable(driver,text):
    Select(driver.find_element(By.ID, "rpXGSponOntProf_firewallEnable")).select_by_visible_text(text)

def Ont_Profile_New_Service_Firewall_level(driver,text):
    Select(driver.find_element(By.ID, "rpXGSponOntProf_firewallLevel")).select_by_visible_text(text)

def Ont_Profile_New_Service_Dmz_control(driver,request):
    check_box = driver.find_element(By.ID, f"rpXGSponOntProf_controlDmz")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Ont_Profile_New_Service_Dmz_ip(driver,value):
    driver.find_element(By.ID, "rpXGSponOntProf_dmzIp").clear()
    driver.find_element(By.ID, "rpXGSponOntProf_dmzIp").send_keys(value)

def Ont_Profile_New_Service_PoE_control(driver,request):
    check_box = driver.find_element(By.ID, f"rpXGSponOntProf_controlPower")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Ont_Profile_New_Service_PoE_management(driver,text):
    Select(driver.find_element(By.ID, "rpXGSponOntProf_powerManagement")).select_by_visible_text(text)

def Ont_Profile_New_Service_PoE_mode(driver,text):
    Select(driver.find_element(By.ID, "rpXGSponOntProf_powerMode")).select_by_visible_text(text)

def Ont_Profile_New_Service_Upnp_control(driver,request):
    check_box = driver.find_element(By.ID, f"rpXGSponOntProf_controlUpnp")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Ont_Profile_New_Service_Upnp_enable(driver,request):
    check_box = driver.find_element(By.ID, f"rpXGSponOntProf_upnpEnable")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Ont_Profile_New_Service_Roaming_control(driver,request):
    check_box = driver.find_element(By.ID, f"rpXGSponOntProf_controlRoaming")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Ont_Profile_New_Service_Roaming(driver,value):
    driver.find_element(By.ID, "rpXGSponOntProf_roaming").clear()
    driver.find_element(By.ID, "rpXGSponOntProf_roaming").send_keys(value)

def Ont_Profile_New_Service_Acs_control(driver,request):
    check_box = driver.find_element(By.ID, f"rpXGSponOntProf_controlAcs")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Ont_Profile_New_Service_Acs_server(driver,request):
    check_box = driver.find_element(By.ID, f"rpXGSponOntProf_acsServerEnable")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Ont_Profile_New_Service_Acs_username(driver,value):
    driver.find_element(By.ID, "rpXGSponOntProf_acsUsername").clear()
    driver.find_element(By.ID, "rpXGSponOntProf_acsUsername").send_keys(value)

def Ont_Profile_New_Service_Acs_password(driver,value):
    driver.find_element(By.ID, "rpXGSponOntProf_acsPassword").clear()
    driver.find_element(By.ID, "rpXGSponOntProf_acsPassword").send_keys(value)

def Ont_Profile_New_Service_Acs_url(driver,value):
    driver.find_element(By.ID, "rpXGSponOntProf_acsUrl").clear()
    driver.find_element(By.ID, "rpXGSponOntProf_acsUrl").send_keys(value)

def Ont_Profile_New_Service_Acs_inform(driver,request):
    check_box = driver.find_element(By.ID, f"rpXGSponOntProf_acsInformEnable")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Ont_Profile_New_Service_Acs_interval(driver,value):
    driver.find_element(By.ID, "rpXGSponOntProf_acsInformInterval").clear()
    driver.find_element(By.ID, "rpXGSponOntProf_acsInformInterval").send_keys(value)

def Ont_Profile_New_Service_Loopguard_control(driver,request):
    check_box = driver.find_element(By.ID, f"rpXGSponOntProf_controlLoopguard")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Ont_Profile_New_Service_Loopguard_detected(driver,value):
    driver.find_element(By.ID, "rpXGSponOntProf_loopguardDetectedTime").clear()
    driver.find_element(By.ID, "rpXGSponOntProf_loopguardDetectedTime").send_keys(value)

def Ont_Profile_New_Service_Loopguard_enable(driver,request):
    check_box = driver.find_element(By.ID, f"rpXGSponOntProf_loopguardEnable")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Ont_Profile_New_Service_Loopguard_recovery(driver,value):
    driver.find_element(By.ID, "rpXGSponOntProf_loopguardRecoveryTime").clear()
    driver.find_element(By.ID, "rpXGSponOntProf_loopguardRecoveryTime").send_keys(value)

def Ont_Profile_New_Service_StormControl_control(driver,request):
    check_box = driver.find_element(By.ID, f"rpXGSponOntProf_controlStorm")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Ont_Profile_New_Service_StormControl_threshold(driver,value):
    driver.find_element(By.ID, "rpXGSponOntProf_stormThreshold").clear()
    driver.find_element(By.ID, "rpXGSponOntProf_stormThreshold").send_keys(value)

# Ont Profile -> Lan

def Ont_Profile_New_Lan_Active(driver,index,request):
    check_box = driver.find_elements(By.ID, f"rpXGSponOntProf_lan_active")[index]
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Ont_Profile_New_Lan_Static_Mode(driver,index,request):
    check_box = driver.find_elements(By.ID, f"rpXGSponOntProf_lan_staticMode")[index]
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Ont_Profile_New_Lan_IP(driver,index,value):
    driver.find_elements(By.ID, "rpXGSponOntProf_lan_ipAddr")[index].clear()
    driver.find_elements(By.ID, "rpXGSponOntProf_lan_ipAddr")[index].send_keys(value)

def Ont_Profile_New_Lan_Mask(driver,index,value):
    driver.find_elements(By.ID, "rpXGSponOntProf_lan_ipMask")[index].clear()
    driver.find_elements(By.ID, "rpXGSponOntProf_lan_ipMask")[index].send_keys(value)

def Ont_Profile_New_Lan_DHCP_Mode(driver,index,text):
    Select(driver.find_elements(By.ID, "rpXGSponOntProf_lan_dhcpServerMode")[index]).select_by_visible_text(text)

def Ont_Profile_New_Lan_PoolBegin(driver,index,value):
    driver.find_elements(By.ID, "rpXGSponOntProf_lan_dhcpIpPoolBegin")[index].clear()
    driver.find_elements(By.ID, "rpXGSponOntProf_lan_dhcpIpPoolBegin")[index].send_keys(value)

def Ont_Profile_New_Lan_PoolEnd(driver,index,value):
    driver.find_elements(By.ID, "rpXGSponOntProf_lan_dhcpIpPoolEnd")[index].clear()
    driver.find_elements(By.ID, "rpXGSponOntProf_lan_dhcpIpPoolEnd")[index].send_keys(value)

def Ont_Profile_New_Lan_RelayServerIp(driver,index,value):
    driver.find_elements(By.ID, "rpXGSponOntProf_lan_dhcpRelayServerIp")[index].clear()
    driver.find_elements(By.ID, "rpXGSponOntProf_lan_dhcpRelayServerIp")[index].send_keys(value)

def Ont_Profile_New_Lan_DnsType(driver,index,text):
    Select(driver.find_elements(By.ID, "rpXGSponOntProf_lan_dnsType")[index]).select_by_visible_text(text)

def Ont_Profile_New_Lan_priDns(driver,index,value):
    driver.find_elements(By.ID, "rpXGSponOntProf_lan_priDnsConfig")[index].clear()
    driver.find_elements(By.ID, "rpXGSponOntProf_lan_priDnsConfig")[index].send_keys(value)

def Ont_Profile_New_Lan_secDns(driver,index,value):
    driver.find_elements(By.ID, "rpXGSponOntProf_lan_secDnsConfig")[index].clear()
    driver.find_elements(By.ID, "rpXGSponOntProf_lan_secDnsConfig")[index].send_keys(value)

# Ont Profile -> Wan

def Ont_Profile_New_Wan_Active(driver,index,request):
    check_box = driver.find_elements(By.ID, f"rpXGSponOntProf_wan_active")[index-1]
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Ont_Profile_New_Wan_Default(driver,index,request):
    check_box = driver.find_elements(By.ID, f"rpXGSponOntProf_wan_default")[index-1]
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Ont_Profile_New_Wan_Enable(driver,index,request):
    check_box = driver.find_elements(By.ID, f"rpXGSponOntProf_wan_enable")[index-1]
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Ont_Profile_New_Wan_Nat(driver,index,request):
    check_box = driver.find_elements(By.ID, f"rpXGSponOntProf_wan_nat")[index-1]
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Ont_Profile_New_Wan_Mode(driver,index,text):
    Select(driver.find_elements(By.ID, "rpXGSponOntProf_wan_ipMode")[index-1]).select_by_visible_text(text)

def Ont_Profile_New_Wan_Address(driver,index,value):
    driver.find_elements(By.ID, "rpXGSponOntProf_wan_ipAddr")[index-1].clear()
    driver.find_elements(By.ID, "rpXGSponOntProf_wan_ipAddr")[index-1].send_keys(value)

def Ont_Profile_New_Wan_Mask(driver,index,value):
    driver.find_elements(By.ID, "rpXGSponOntProf_wan_ipMask")[index-1].clear()
    driver.find_elements(By.ID, "rpXGSponOntProf_wan_ipMask")[index-1].send_keys(value)

def Ont_Profile_New_Wan_Gateway(driver,index,value):
    driver.find_elements(By.ID, "rpXGSponOntProf_wan_ipGateway")[index-1].clear()
    driver.find_elements(By.ID, "rpXGSponOntProf_wan_ipGateway")[index-1].send_keys(value)

def Ont_Profile_New_Wan_priDns(driver,index,value):
    driver.find_elements(By.ID, "rpXGSponOntProf_wan_priDnsConfig")[index-1].clear()
    driver.find_elements(By.ID, "rpXGSponOntProf_wan_priDnsConfig")[index-1].send_keys(value)

def Ont_Profile_New_Wan_secDns(driver,index,value):
    driver.find_elements(By.ID, "rpXGSponOntProf_wan_secDnsConfig")[index-1].clear()
    driver.find_elements(By.ID, "rpXGSponOntProf_wan_secDnsConfig")[index-1].send_keys(value)

def Ont_Profile_New_Wan_type(driver,index,text):
    Select(driver.find_elements(By.ID, "rpXGSponOntProf_wan_connect")[index-1]).select_by_visible_text(text)

def Ont_Profile_New_Wan_username(driver,index,value):
    driver.find_elements(By.ID, "rpXGSponOntProf_wan_username")[index-1].clear()
    driver.find_elements(By.ID, "rpXGSponOntProf_wan_username")[index-1].send_keys(value)

def Ont_Profile_New_Wan_password(driver,index,value):
    driver.find_elements(By.ID, "rpXGSponOntProf_wan_password")[index-1].clear()
    driver.find_elements(By.ID, "rpXGSponOntProf_wan_password")[index-1].send_keys(value)

def Ont_Profile_New_Wan_port_list(driver,index,value):
    driver.find_elements(By.ID, "rpXGSponOntProf_wan_portbinding")[index-1].clear()
    driver.find_elements(By.ID, "rpXGSponOntProf_wan_portbinding")[index-1].send_keys(value)

def Ont_Profile_New_Wan_wifi_2_4_ssid(driver,index,value):
    driver.find_elements(By.ID, "rpXGSponOntProf_wan_wifibinding")[index-1].clear()
    driver.find_elements(By.ID, "rpXGSponOntProf_wan_wifibinding")[index-1].send_keys(value)

def Ont_Profile_New_Wan_wifi_5_ssid(driver,index,value):
    driver.find_elements(By.ID, "rpXGSponOntProf_wan_wifi5gbinding")[index-1].clear()
    driver.find_elements(By.ID, "rpXGSponOntProf_wan_wifi5gbinding")[index-1].send_keys(value)

def Ont_Profile_New_Wan_vlan(driver,index,value):
    driver.find_elements(By.ID, "rpXGSponOntProf_wan_vlan")[index-1].clear()
    driver.find_elements(By.ID, "rpXGSponOntProf_wan_vlan")[index-1].send_keys(value)

def Ont_Profile_New_Wan_priority(driver,index,text):
    Select(driver.find_elements(By.ID, "rpXGSponOntProf_wan_priority")[index-1]).select_by_visible_text(text)

def Ont_Profile_New_Wan_mvlan(driver,index,value):
    driver.find_elements(By.ID, "rpXGSponOntProf_wan_mvlan")[index-1].clear()
    driver.find_elements(By.ID, "rpXGSponOntProf_wan_mvlan")[index-1].send_keys(value)

def Ont_Profile_New_Wan_service(driver,index,value):
    driver.find_elements(By.ID, "rpXGSponOntProf_wan_service")[index-1].clear()
    driver.find_elements(By.ID, "rpXGSponOntProf_wan_service")[index-1].send_keys(value)

# Ont Profile -> WiFi 2.4g

def Ont_Profile_New_WiFi_2_4g_Active(driver,index,request):
    check_box = driver.find_elements(By.ID, f"rpXGSponOntProf_wifi2_active")[index-1]
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Ont_Profile_New_WiFi_2_4g_Enable(driver,index,request):
    check_box = driver.find_elements(By.ID, f"rpXGSponOntProf_wifi2_enable")[index-1]
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Ont_Profile_New_WiFi_2_4g_ssid(driver,index,value):
    driver.find_elements(By.ID, "rpXGSponOntProf_wifi2_ssid")[index-1].clear()
    driver.find_elements(By.ID, "rpXGSponOntProf_wifi2_ssid")[index-1].send_keys(value)

def Ont_Profile_New_WiFi_2_4g_password(driver,index,value):
    driver.find_elements(By.ID, "rpXGSponOntProf_wifi2_password")[index-1].clear()
    driver.find_elements(By.ID, "rpXGSponOntProf_wifi2_password")[index-1].send_keys(value)

def Ont_Profile_New_WiFi_2_4g_Channel(driver,index,text):
    Select(driver.find_elements(By.ID, "rpXGSponOntProf_wifi2_channel")[index-1]).select_by_visible_text(text)

def Ont_Profile_New_WiFi_2_4g_Bandwidth(driver,index,text):
    Select(driver.find_elements(By.ID, "rpXGSponOntProf_wifi2_bandwidth")[index-1]).select_by_visible_text(text)

def Ont_Profile_New_WiFi_2_4g_maxClients(driver,index,value):
    driver.find_elements(By.ID, "rpXGSponOntProf_wifi2_maxClients")[index-1].clear()
    driver.find_elements(By.ID, "rpXGSponOntProf_wifi2_maxClients")[index-1].send_keys(value)

def Ont_Profile_New_WiFi_2_4g_securityMode(driver,index,text):
    Select(driver.find_elements(By.ID, "rpXGSponOntProf_wifi2_securityMode")[index-1]).select_by_visible_text(text)

def Ont_Profile_New_WiFi_2_4g_txPower(driver,index,text):
    Select(driver.find_elements(By.ID, "rpXGSponOntProf_wifi2_txPower")[index-1]).select_by_visible_text(text)

# Ont Profile -> WiFi 5g

def Ont_Profile_New_WiFi_5g_Active(driver,index,request):
    check_box = driver.find_elements(By.ID, f"rpXGSponOntProf_wifi5_active")[index-1]
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Ont_Profile_New_WiFi_5g_Enable(driver,index,request):
    check_box = driver.find_elements(By.ID, f"rpXGSponOntProf_wifi5_enable")[index-1]
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Ont_Profile_New_WiFi_5g_ssid(driver,index,value):
    driver.find_elements(By.ID, "rpXGSponOntProf_wifi5_ssid")[index-1].clear()
    driver.find_elements(By.ID, "rpXGSponOntProf_wifi5_ssid")[index-1].send_keys(value)

def Ont_Profile_New_WiFi_5g_password(driver,index,value):
    driver.find_elements(By.ID, "rpXGSponOntProf_wifi5_password")[index-1].clear()
    driver.find_elements(By.ID, "rpXGSponOntProf_wifi5_password")[index-1].send_keys(value)

def Ont_Profile_New_WiFi_5g_Channel(driver,index,text):
    Select(driver.find_elements(By.ID, "rpXGSponOntProf_wifi5_channel")[index-1]).select_by_visible_text(text)

def Ont_Profile_New_WiFi_5g_Bandwidth(driver,index,text):
    Select(driver.find_elements(By.ID, "rpXGSponOntProf_wifi5_bandwidth")[index-1]).select_by_visible_text(text)

def Ont_Profile_New_WiFi_5g_maxClients(driver,index,value):
    driver.find_elements(By.ID, "rpXGSponOntProf_wifi5_maxClients")[index-1].clear()
    driver.find_elements(By.ID, "rpXGSponOntProf_wifi5_maxClients")[index-1].send_keys(value)

def Ont_Profile_New_WiFi_5g_securityMode(driver,index,text):
    Select(driver.find_elements(By.ID, "rpXGSponOntProf_wifi5_securityMode")[index-1]).select_by_visible_text(text)

def Ont_Profile_New_WiFi_5g_txPower(driver,index,text):
    Select(driver.find_elements(By.ID, "rpXGSponOntProf_wifi5_txPower")[index-1]).select_by_visible_text(text)

# Ont Profile -> Acl

def Ont_Profile_New_Acl_Active(driver,index,request):
    check_box = driver.find_elements(By.ID, f"rpXGSponOntProf_acl_active")[index-1]
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Ont_Profile_New_Acl_Name(driver,index,text):
    Select(driver.find_elements(By.ID, "rpXGSponOntProf_acl_name")[index-1]).select_by_visible_text(text)

# Ont Profile -> Voip

def Ont_Profile_New_Voip_Uniport(driver,index,text):
    Select(driver.find_elements(By.ID, f"rpXGSponVoipPortId")[index-1]).select_by_visible_text(text)

def Ont_Profile_New_Voip_Enable(driver,index,request):
    check_box = driver.find_elements(By.ID, f"rpXGSponVoipEnable")[index-1]
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Ont_Profile_New_Voip_Active(driver,index,request):    
    check_box = driver.find_elements(By.ID, f"rpXGSponVoipActive")[index-1]
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Ont_Profile_New_Voip_Vlan(driver,index,value): 
    driver.find_elements(By.ID, "rpXGSponVoipVlanId")[index-1].clear()
    driver.find_elements(By.ID, "rpXGSponVoipVlanId")[index-1].send_keys(value)
    # driver.find_element(By.XPATH, "//*[@id='rpXGSponVoipVlanId']").clear()
    # driver.find_element(By.XPATH, "//*[@id='rpXGSponVoipVlanId']").send_keys(value)
    # //*[@id="rpXGSponVoipVlanId"]

def Ont_Profile_New_Voip_Username(driver,index,value): 
    driver.find_elements(By.ID, "rpXGSponVoipUsername")[index-1].clear()
    driver.find_elements(By.ID, "rpXGSponVoipUsername")[index-1].send_keys(value)
    
def Ont_Profile_New_Voip_Password(driver,index,value):         
    driver.find_elements(By.ID, "rpXGSponVoipPassword")[index-1].clear()
    driver.find_elements(By.ID, "rpXGSponVoipPassword")[index-1].send_keys(value)
    
def Ont_Profile_New_Voip_User_Part_AOR(driver,index,value):
    driver.find_elements(By.ID, "rpXGSponVoipAor")[index-1].clear()
    driver.find_elements(By.ID, "rpXGSponVoipAor")[index-1].send_keys(value)
    
def Ont_Profile_New_Voip_Display_Name(driver,index,value):  
    driver.find_elements(By.ID, "rpXGSponVoipDispname")[index-1].clear()
    driver.find_elements(By.ID, "rpXGSponVoipDispname")[index-1].send_keys(value)

def Ont_Profile_New_Voip_Voicemail_Server_SIP_URI(driver,index,value): 
    driver.find_elements(By.ID, "rpXGSponVoipVmailUri")[index-1].clear()
    driver.find_elements(By.ID, "rpXGSponVoipVmailUri")[index-1].send_keys(value)

def Ont_Profile_New_Voip_Voicemail_Expiration_Time(driver,index,value): 
    driver.find_elements(By.ID, "rpXGSponVoipVmailExtimer")[index-1].clear()
    driver.find_elements(By.ID, "rpXGSponVoipVmailExtimer")[index-1].send_keys(value)

def Ont_Profile_New_Voip_Release_Timer(driver,index,value): 
    driver.find_elements(By.ID, "rpXGSponVoipRelTimer")[index-1].clear()
    driver.find_elements(By.ID, "rpXGSponVoipRelTimer")[index-1].send_keys(value)

def Ont_Profile_New_Voip_ROH_Timer(driver,index,value):
    driver.find_elements(By.ID, "rpXGSponVoipRohTimer")[index-1].clear()
    driver.find_elements(By.ID, "rpXGSponVoipRohTimer")[index-1].send_keys(value)

def Ont_Profile_New_Voip_VoIP_Comment_Profile(driver,index,text):
    Select(driver.find_elements(By.ID, "rpXGSponVoipComProf")[index-1]).select_by_visible_text(text)

def Ont_Profile_New_Voip_VoIP_Sip_Profile(driver,index,text):
    Select(driver.find_elements(By.ID, "rpXGSponVoipSipProf")[index-1]).select_by_visible_text(text) 

def Ont_Profile_New_Voip_VoIP_Dial_Plan_Profile(driver,index,text):
    Select(driver.find_elements(By.ID, "rpXGSponVoipDialPlanProf")[index-1]).select_by_visible_text(text) 

# Ont Profile -> Poe

def Ont_Profile_New_Poe_Active(driver,index,request):
    check_box = driver.find_elements(By.ID, f"rpXGSponOntProf_poe_active")[index-1]
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Ont_Profile_New_Poe_Enable(driver,index,request):
    check_box = driver.find_elements(By.ID, f"rpXGSponOntProf_poe_enable")[index-1]
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Ont_Profile_New_Poe_Priority(driver,index,text):
    Select(driver.find_elements(By.ID, "rpXGSponOntProf_poe_priority")[index-1]).select_by_visible_text(text) 

def Ont_Profile_New_Poe_Max(driver,index,text):
    Select(driver.find_elements(By.ID, "rpXGSponOntProf_poe_max")[index-1]).select_by_visible_text(text) 


# Sip Profile

def Sip_Profile_New(driver):
    driver.find_element(By.CLASS_NAME, "font-btn").click()

def Sip_Profile_Delete(driver):
    driver.find_element(By.NAME, "rpXgponSipProf_TablebtnDelete").click()

def Sip_Profile_Delete_All_Select(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponMcastProf_chkDelall")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Sip_Profile_New_Apply(driver):
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[0].click()

def Sip_Profile_New_Delete(driver):
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()

def Sip_Profile_New_Name(driver,name):
    input = driver.find_element(By.ID, "rpXGSponSipProf_IptProfName")
    input.clear()
    input.send_keys(name)

def Sip_Profile_New_PSA(driver,value):
    input = driver.find_element(By.ID, "rpXGSponVoipSip_proxyAddr")
    input.clear()
    input.send_keys(value)

def Sip_Profile_New_OPA(driver,value):
    input = driver.find_element(By.ID, "rpXGSponVoipSip_outbandAddr")
    input.clear()
    input.send_keys(value)

def Sip_Profile_New_PD(driver,value):
    input = driver.find_element(By.ID, "rpXGSponVoipSip_priDns")
    input.clear()
    input.send_keys(value)

def Sip_Profile_New_SD(driver,value):
    input = driver.find_element(By.ID, "rpXGSponVoipSip_secDns")
    input.clear()
    input.send_keys(value)

def Sip_Profile_New_RET(driver,value):
    input = driver.find_element(By.ID, "rpXGSponVoipSip_regExpTime")
    input.clear()
    input.send_keys(value)

def Sip_Profile_New_RHST(driver,value):
    input = driver.find_element(By.ID, "rpXGSponVoipSip_reregHeadStartTime")
    input.clear()
    input.send_keys(value)

def Sip_Profile_New_HPU(driver,value):
    input = driver.find_element(By.ID, "rpXGSponVoipSip_hostPartUri")
    input.clear()
    input.send_keys(value)

def Sip_Profile_New_SR(driver,value):
    input = driver.find_element(By.ID, "rpXGSponVoipSip_registrar")
    input.clear()
    input.send_keys(value)

def Sip_Profile_New_S(driver,value):
    input = driver.find_element(By.ID, "rpXGSponVoipSip_softswitch")
    input.clear()
    input.send_keys(value)
    
def Sip_Profile_New_CI_cal_num(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponVoipSip_calNum")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def Sip_Profile_New_CI_cal_nam(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponVoipSip_calNam")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def Sip_Profile_New_CI_cid_bio(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponVoipSip_cidBlo")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def Sip_Profile_New_CI_cid_num(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponVoipSip_cidNum")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def Sip_Profile_New_CI_cid_nam(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponVoipSip_cidNam")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def Sip_Profile_New_CI_ACR(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponVoipSip_acr")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def Sip_Profile_New_CW_cal_wai(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponVoipSip_calWai")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def Sip_Profile_New_CW_cid_ann(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponVoipSip_cidAnn")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def Sip_Profile_New_CPOT_3way(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponVoipSip_3way")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def Sip_Profile_New_CPOT_cal_tra(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponVoipSip_calTra")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def Sip_Profile_New_CPOT_cal_hol(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponVoipSip_calHol")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def Sip_Profile_New_CPOT_cal_par(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponVoipSip_calPar")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def Sip_Profile_New_CPOT_not_dis(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponVoipSip_notDis")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def Sip_Profile_New_CPOT_flash(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponVoipSip_flash")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def Sip_Profile_New_CPOT_origin(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponVoipSip_origin")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def Sip_Profile_New_CPOT_6way(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponVoipSip_6way")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def Sip_Profile_New_CP_spl_rin(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponVoipSip_splRin")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def Sip_Profile_New_CP_dia_ton(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponVoipSip_diaTon")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def Sip_Profile_New_CP_vis_ind(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponVoipSip_visInd")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def Sip_Profile_New_CP_cal_for(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponVoipSip_calFor")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def Sip_Profile_New_DC_enable(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponVoipSip_enable")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def Sip_Profile_New_DC_dia_opt(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponVoipSip_diaOpt")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Sip_Profile_New_DCU(driver,value):
    input = driver.find_element(By.ID, "rpXGSponVoipSip_dirConUri")
    input.clear()
    input.send_keys(value)

def Sip_Profile_New_BLAU(driver,value):
    input = driver.find_element(By.ID, "rpXGSponVoipSip_briLineAgentUri")
    input.clear()
    input.send_keys(value)

def Sip_Profile_New_CFU(driver,value):
    input = driver.find_element(By.ID, "rpXGSponVoipSip_conFactUri")
    input.clear()
    input.send_keys(value)

# Voip Common Profile

def Voip_Common_Profile_New(driver):
    driver.find_element(By.CLASS_NAME, "font-btn").click()

def Voip_Common_Profile_Delete(driver):
    driver.find_element(By.NAME, "rpXgponCommonProf_TablebtnDelete").click()

def Voip_Common_Profile_Delete_All_Select(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponMcastProf_chkDelall")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Voip_Common_Profile_New_Apply(driver):
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[0].click()

def Voip_Common_Profile_New_Delete(driver):
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()

def Voip_Common_Profile_New_Name(driver,name):
    input = driver.find_element(By.ID, "rpXGSponCommonProf_IptProfName")
    input.clear()
    input.send_keys(name)

def Voip_Common_Profile_New_min_Local_Port(driver,vlaue):
    input = driver.find_element(By.ID, "rpXGSponVoipCommon_minPort")
    input.clear()
    input.send_keys(vlaue)

def Voip_Common_Profile_New_max_Local_Port(driver,vlaue):
    input = driver.find_element(By.ID, "rpXGSponVoipCommon_maxPort")
    input.clear()
    input.send_keys(vlaue)

def Voip_Common_Profile_New_dscp_mark(driver,vlaue):
    input = driver.find_element(By.ID, "rpXGSponVoipCommon_dscpMark")
    input.clear()
    input.send_keys(vlaue)

def Voip_Common_Profile_New_piggyback(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponVoipCommon_piggyback")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Voip_Common_Profile_New_tone(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponVoipCommon_tone")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Voip_Common_Profile_New_dtmf(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponVoipCommon_dtmf")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Voip_Common_Profile_New_cas(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponVoipCommon_cas")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Voip_Common_Profile_New_jitter_target(driver,vlaue):
    input = driver.find_element(By.ID, "rpXGSponVoipCommon_jitterTarget")
    input.clear()
    input.send_keys(vlaue)

def Voip_Common_Profile_New_max_jitter_buffer(driver,vlaue):
    input = driver.find_element(By.ID, "rpXGSponVoipCommon_jitterBuf")
    input.clear()
    input.send_keys(vlaue)

def Voip_Common_Profile_New_ptsn_protocol(driver,vlaue):
    input = driver.find_element(By.ID, "rpXGSponVoipCommon_pstn")
    input.clear()
    input.send_keys(vlaue)

def Voip_Common_Profile_New_announce_type(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpXGSponVoipCommon_announce']/option[{sel}]")
    select.click()

def Voip_Common_Profile_New_echo_cancel(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponVoipCommon_echo")
    if(check_box.is_selected() == True):     
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Voip_Common_Profile_New_fax_mode(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpXGSponVoipCommon_fax']/option[{sel}]")
    select.click()

def Voip_Common_Profile_New_1st_codec(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpXGSponVoipCommon_1stCodec']/option[{sel}]")
    select.click()

def Voip_Common_Profile_New_2nd_codec(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpXGSponVoipCommon_2ndCodec']/option[{sel}]")
    select.click()

def Voip_Common_Profile_New_3rd_codec(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpXGSponVoipCommon_3rdCodec']/option[{sel}]")
    select.click()

def Voip_Common_Profile_New_4th_codec(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpXGSponVoipCommon_4thCodec']/option[{sel}]")
    select.click()

def Voip_Common_Profile_New_1st_packet_period(driver,vlaue):
    input = driver.find_element(By.ID, "rpXGSponVoipCommon_1stPktPeriod")
    input.clear()
    input.send_keys(vlaue)

def Voip_Common_Profile_New_2nd_packet_period(driver,vlaue):
    input = driver.find_element(By.ID, "rpXGSponVoipCommon_2ndPktPeriod")
    input.clear()
    input.send_keys(vlaue)

def Voip_Common_Profile_New_3rd_packet_period(driver,vlaue):
    input = driver.find_element(By.ID, "rpXGSponVoipCommon_3rdPktPeriod")
    input.clear()
    input.send_keys(vlaue)

def Voip_Common_Profile_New_4th_packet_period(driver,vlaue):
    input = driver.find_element(By.ID, "rpXGSponVoipCommon_4thPktPeriod")
    input.clear()
    input.send_keys(vlaue)

def Voip_Common_Profile_New_1st_silence(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponVoipCommon_1stSilence")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Voip_Common_Profile_New_2nd_silence(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponVoipCommon_2ndSilence")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Voip_Common_Profile_New_3rd_silence(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponVoipCommon_3rdSilence")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Voip_Common_Profile_New_4th_silence(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponVoipCommon_4thSilence")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Voip_Common_Profile_New_oob_dtmf(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponVoipCommon_oobDtmf")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Voip_Common_Profile_New_signal_code(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpXGSponVoipCommon_signalCode']/option[{sel}]")
    select.click()

# Dial Plan Profile

def Dial_Plan_Profile_New(driver):
    driver.find_element(By.CLASS_NAME, "font-btn").click()

def Dial_Plan_Profile_Delete(driver):
    driver.find_element(By.NAME, "rpXgponDialPlanProf_TablebtnDelete").click()

def Dial_Plan_Profile_Delete_All_Select(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponMcastProf_chkDelall")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Dial_Plan_Profile_New_Apply(driver):
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[0].click()

def Dial_Plan_Profile_New_Delete(driver):
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()

def Dial_Plan_Profile_New_Name(driver,name):
    input = driver.find_element(By.ID, "rpXGSponDialPlanProf_IptProfName")
    input.clear()
    input.send_keys(name)

def Dial_Plan_Profile_New_MS(driver,vlaue):
    input = driver.find_element(By.ID, "rpXGSponVoipDialPlan_maxSize")
    input.clear()
    input.send_keys(vlaue)

def Dial_Plan_Profile_New_CDT(driver,vlaue):
    input = driver.find_element(By.ID, "rpXGSponVoipDialPlan_criDialTimeout")
    input.clear()
    input.send_keys(vlaue)

def Dial_Plan_Profile_New_PDT(driver,vlaue):
    input = driver.find_element(By.ID, "rpXGSponVoipDialPlan_parDialTimeout")
    input.clear()
    input.send_keys(vlaue)
    
def Dial_Plan_Profile_New_format(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpXGSponVoipDialPlan_format']/option[{sel}]")
    select.click()

def Dial_Plan_Profile_New_CT(driver,vlaue):
    input = driver.find_element(By.ID, "rpXGSponVoipDialPlan_token1")
    input.clear()
    input.send_keys(vlaue)

# ACL Profile

def ACL_Profile_New(driver):
    driver.find_element(By.CLASS_NAME, "font-btn").click()

def ACL_Profile_Delete(driver):
    driver.find_element(By.NAME, "rpXgponOntProf_TablebtnDelete").click()

def ACL_Profile_Delete_All_Select(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponMcastProf_chkDelall")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_Profile_New_Apply(driver):
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[0].click()

def ACL_Profile_New_Delete(driver):
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()

def ACL_Profile_New_Name(driver,name):
    input = driver.find_element(By.ID, "rpXGSponOntAclProf_IptProfName")
    input.clear()                      
    input.send_keys(name)

def ACL_Profile_New_Enable(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponOntAclProf_enable")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_Profile_New_Count(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponOntAclProf_count")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_Profile_New_Log(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponOntAclProf_log")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ACL_Profile_New_Policy(driver,text):
    Select(driver.find_element(By.ID, "rpXGSponOntAclProf_policy")).select_by_visible_text(text)

def ACL_Profile_New_Interface(driver,text):
    Select(driver.find_element(By.ID, "rpXGSponOntAclProf_interface")).select_by_visible_text(text)

def ACL_Profile_New_Protocol(driver,value):
    driver.find_element(By.ID, "rpXGSponOntAclProf_protocol").clear()
    driver.find_element(By.ID, "rpXGSponOntAclProf_protocol").send_keys(value)

def ACL_Profile_New_Src_Port(driver,value):
    driver.find_element(By.ID, "rpXGSponOntAclProf_srcPort").clear()
    driver.find_element(By.ID, "rpXGSponOntAclProf_srcPort").send_keys(value)

def ACL_Profile_New_Dst_Port(driver,value):
    driver.find_element(By.ID, "rpXGSponOntAclProf_dstPort").clear()
    driver.find_element(By.ID, "rpXGSponOntAclProf_dstPort").send_keys(value)

def ACL_Profile_New_Src_ip(driver,value):
    driver.find_element(By.ID, "rpXGSponOntAclProf_srcIp").clear()
    driver.find_element(By.ID, "rpXGSponOntAclProf_srcIp").send_keys(value)

def ACL_Profile_New_Src_mask(driver,value):
    driver.find_element(By.ID, "rpXGSponOntAclProf_srcMask").clear()
    driver.find_element(By.ID, "rpXGSponOntAclProf_srcMask").send_keys(value)

def ACL_Profile_New_Dst_ip(driver,value):
    driver.find_element(By.ID, "rpXGSponOntAclProf_dstIp").clear()
    driver.find_element(By.ID, "rpXGSponOntAclProf_dstIp").send_keys(value)

def ACL_Profile_New_Dst_mask(driver,value):
    driver.find_element(By.ID, "rpXGSponOntAclProf_dstMask").clear()
    driver.find_element(By.ID, "rpXGSponOntAclProf_dstMask").send_keys(value)

def ACL_Profile_New_Src_mac(driver,value):
    driver.find_element(By.ID, "rpXGSponOntAclProf_srcMac").clear()
    driver.find_element(By.ID, "rpXGSponOntAclProf_srcMac").send_keys(value)

def ACL_Profile_New_Dst_mac(driver,value):
    driver.find_element(By.ID, "rpXGSponOntAclProf_dstMac").clear()
    driver.find_element(By.ID, "rpXGSponOntAclProf_dstMac").send_keys(value)

# ONT Alarm Profile

def Ont_Alarm_Profile_New(driver):
    driver.find_element(By.CLASS_NAME, "font-btn").click()

def Ont_Alarm_Profile_Delete(driver):
    driver.find_element(By.NAME, "rpXgponOntAlarmProf_TablebtnDelete").click()

def Ont_Alarm_Profile_Delete_All_Select(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponMcastProf_chkDelall")
    if(check_box.is_selected() == True):     
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Ont_Alarm_Profile_New_Apply(driver):
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[0].click()
                                      
def Ont_Alarm_Profile_New_Delete(driver):
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()

def Ont_Alarm_Profile_New_Name(driver,name):
    input = driver.find_element(By.ID, "rpXGSponOntAlarmProf_IptProfName")
    input.clear()                      
    input.send_keys(name)

def Ont_Alarm_New_Low_Current_Threshold(driver,value):
    driver.find_element(By.ID, "rpXGSponOntAlarmProf_currThreshLow").clear()
    driver.find_element(By.ID, "rpXGSponOntAlarmProf_currThreshLow").send_keys(value)

def Ont_Alarm_New_Up_Current_Threshold(driver,value):
    driver.find_element(By.ID, "rpXGSponOntAlarmProf_currThreshUp").clear()
    driver.find_element(By.ID, "rpXGSponOntAlarmProf_currThreshUp").send_keys(value)

def Ont_Alarm_New_Low_rxpower_thresh(driver,value):
    driver.find_element(By.ID, "rpXGSponOntAlarmProf_rxPowerThreshLow").clear()
    driver.find_element(By.ID, "rpXGSponOntAlarmProf_rxPowerThreshLow").send_keys(value)

def Ont_Alarm_New_Up_rxpower_thresh(driver,value):
    driver.find_element(By.ID, "rpXGSponOntAlarmProf_rxPowerThreshUp").clear()
    driver.find_element(By.ID, "rpXGSponOntAlarmProf_rxPowerThreshUp").send_keys(value)

def Ont_Alarm_New_Low_temp(driver,value):
    driver.find_element(By.ID, "rpXGSponOntAlarmProf_temperThreshLow").clear()
    driver.find_element(By.ID, "rpXGSponOntAlarmProf_temperThreshLow").send_keys(value)

def Ont_Alarm_New_Up_temp(driver,value):
    driver.find_element(By.ID, "rpXGSponOntAlarmProf_temperThreshUp").clear()
    driver.find_element(By.ID, "rpXGSponOntAlarmProf_temperThreshUp").send_keys(value)

def Ont_Alarm_New_Low_txpower_thresh(driver,value):
    driver.find_element(By.ID, "rpXGSponOntAlarmProf_txPowerThreshLow").clear()
    driver.find_element(By.ID, "rpXGSponOntAlarmProf_txPowerThreshLow").send_keys(value)

def Ont_Alarm_New_Up_txpower_thresh(driver,value):
    driver.find_element(By.ID, "rpXGSponOntAlarmProf_txPowerThreshUp").clear()
    driver.find_element(By.ID, "rpXGSponOntAlarmProf_txPowerThreshUp").send_keys(value)

def Ont_Alarm_New_Low_volt_thresh(driver,value):
    driver.find_element(By.ID, "rpXGSponOntAlarmProf_voltThreshLow").clear()
    driver.find_element(By.ID, "rpXGSponOntAlarmProf_voltThreshLow").send_keys(value)

def Ont_Alarm_New_Up_volt_thresh(driver,value):
    driver.find_element(By.ID, "rpXGSponOntAlarmProf_voltThreshUp").clear()
    driver.find_element(By.ID, "rpXGSponOntAlarmProf_voltThreshUp").send_keys(value)

# XPON > Statistics 

def Port_Statistics_Current_Statistics_Load(driver):
    driver.find_element(By.CLASS_NAME, "font-btn").click()

def Port_Statistics_Current_Statistics_Clear(driver):
    driver.find_element(By.CLASS_NAME, "font-btn").click()

#dont use xpath
def Slot_Port_Select_Statistics(driver,text):
    # retry = True
    # while(retry == True):
    #     try:
    #         driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlot']/option[{slot}]").click()
    #     except:
    #         time.sleep(1)
    #     try:
    #         if(driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlot']/option[{slot}]").is_selected() == True):
    #             retry = False
    #     except:
    #         time.sleep(1)

    Select(driver.find_element(By.ID, "xgponSelOltPort")).select_by_visible_text(text)
    # can i use this way ("Select")?

def OntPort_Select_Statistics(driver, text):    
    Select(driver.find_element(By.ID, "xgponSelOntPort")).select_by_visible_text(text)
    # can i use this way ("Select")?  

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


# XPON > Diagnostic > O7 state

def Diagnostic_Port(driver,text):    
                                      
    Select(driver.find_element(By.ID, "rpXgponDiagnostic_IptTableOltPort")).select_by_visible_text(text)
    # can i use this way ("Select")?

def Diagnostic_SN(driver, value):
    driver.find_element(By.ID, "rpXgponDiagnostic_TableSN").clear()
    driver.find_element(By.ID, "rpXgponDiagnostic_TableSN").send_keys(value)

# XPON > Diagnostic > Debug cmd

def Diagnostic_Debug_cmd_system(driver, text):
    Select(driver.find_element(By.ID, "rpXgponDiagnostic_IptTableSlot")).select_by_visible_text(text)

def Diagnostic_Debug_cmd_port(driver, text):
    Select(driver.find_element(By.ID, "rpXgponDiagnostic_IptTableOltPort")).select_by_visible_text(text)

def Diagnostic_Debug_cmd_ont1(driver, text):
    Select(driver.find_element(By.ID, "rpXgponDiagnostic_IptTableOntOltPort")).select_by_visible_text(text)

def Diagnostic_Debug_cmd_ont2(driver, text):
    Select(driver.find_element(By.ID, "rpXgponOntConfig_OLC3708IptTableOntPort")).select_by_visible_text(text)
                                    
def Maintenance_Config_Reset(driver):
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "Maintenance").click()
    driver.find_element(By.LINK_TEXT, "Config Reset").click()    
    driver.switch_to.frame(0)
    driver.find_element(By.NAME, "rpConfigReset").click()
    pyautogui.press("enter")
    time.sleep(60)


