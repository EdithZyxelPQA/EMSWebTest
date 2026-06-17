from os import times
import time
from attr import field
from pyrsistent import s
import selenium_module as mod
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys
import web_share.EMS.ems_module as e_mod
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

# GE/GENNI VLAN Setup

# VLAN > VLAN Table #

def VLAN_Table_Add(driver):
    driver.find_element(By.ID,"vlan_vlantable_vlan_add").click()

def VLAN_Table_VLAN_ID(driver,value):
    input = driver.find_element(By.ID,"vlan_vlantable_vlan_dialog_vid")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def VLAN_Table_Egress_TPID(driver,text):    
    Select(driver.find_element(By.ID,"vlan_vlantable_vlan_dialog_tpid")).select_by_visible_text(text)

def VLAN_Table_Port_Registration_All(driver,text,request):    
    e_mod.Checkbox_EMS(driver,f"vlan_vlanTable_{text}_all",request)    

def VLAN_Table_Port_Tagging_All(driver,request):
    e_mod.Checkbox_EMS(driver,f"vlan_vlanTable_untagged_all",request)        

def VLAN_Table_Slot_Port_Registration(driver,slot,port,text,request):
    e_mod.Checkbox_EMS(driver,f"vlan_vlanTable_{text}_{slot}-{port}",request)           

def VLAN_Table_Port_Tagging(driver,slot,port,request):
    e_mod.Checkbox_EMS(driver,f"vlan_vlanTable_untagged_{slot}-{port}",request)           
    
def VLAN_Table_OK(driver):
    driver.find_element(By.ID,"popupCallBack").click()

def VLAN_Table_Select(driver,sel,request):
    e_mod.Checkbox_EMS(driver,f"vlan_vlantable_del_checkbox{sel}",request)              

def VLAN_Table_Modify(driver):
    driver.find_element(By.ID,"vlan_vlantable_vlan_modify").click()

def VLAN_Table_Cancle(driver):
    driver.find_element(By.ID,"popupCancel").click()

def VLAN_Table_Delete(driver):
    driver.find_element(By.ID,"vlan_vlantable_vlan_delete").click()



# VLAN > VLAN Untag and Copy-Cpbit #

def VLAN_Untag_And_Copy_Cpbit_Select_Slot(driver,text):
    Select(driver.find_element(By.ID,"vlan_vlanuntagcpbit_card_combobox")).select_by_value(text)

def VLAN_Untag_and_Copy_Cpbit_PVID_All(driver,value):
    input = driver.find_element(By.ID,"vlan_vlanuntagcpbit_pvid_text_all")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def VLAN_Untag_and_Copy_Cpbit_Pbit_All(driver,value):
    input = driver.find_element(By.ID,"vlan_vlanuntagcpbit_pbit_text_all")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def VLAN_Untag_and_Copy_Cpbit_Frame_Type_All(driver,text):
    Select(driver.find_element(By.ID,"vlan_vlanuntagcpbit_frametype_select_all")).select_by_visible_text(text)

def VLAN_Untag_and_Copy_Cpbit_Copy_Cpbit_Enable_All(driver,request):
    e_mod.Checkbox_EMS(driver,f"vlan_vlanuntagcpbit_copyenable_checkbox_all",request)              

def VLAN_Untag_and_Copy_Cpbit_Outer_TPID_Enable_All(driver,request):
    e_mod.Checkbox_EMS(driver,f"vlan_vlanuntagcpbit_tpidenable_checkbox_all",request)                  

def VLAN_Untag_and_Copy_Cpbit_Apply(driver):
    driver.find_element(By.ID,"vlan_vlanuntagcpbit_vlanapply_button").click()

def VLAN_Untag_and_Copy_Cpbit_Cancel(driver):
    driver.find_element(By.ID,"vlan_vlanuntagcpbit_vlancancel_button").click()

# # Port VLAN TLS

# def Port_VLAN_TLS_Delete(driver):
#     driver.find_element(By.NAME, "rpVlanTlsDelete").click()

# def Port_VLAN_TLS_SVID(driver,value):
#     input = driver.find_element(By.NAME, "rpVlanTls_svidSetup")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def Port_VLAN_TLS_Spbit(driver,value):
#     input = driver.find_element(By.NAME, "rpVlanTls_spbitSetup")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def Port_VLAN_TLS_Apply(driver):
#     driver.find_element(By.NAME, "rpVlanTlsApply").click()

# def Port_VLAN_TLS_Cancel(driver):
#     driver.find_element(By.NAME, "rpVlanTlsCancel").click()

# def Port_VLAN_TLS_Slot_Select(driver,slot):
#     driver.find_elements(By.CLASS_NAME, "lcman_href")[int(slot)-1].click()

# def Port_VLAN_TLS_Slot_Up(driver):
#     driver.find_element(By.NAME, "rpVlanTlsPort_back").click()

# def Port_VLAN_TLS_Slot_Select_All(driver,request):
#     check_box = driver.find_element(By.NAME, "rpVlanTlsPort_selectAll")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def Port_VLAN_TLS_Slot_Prev(driver):
#     driver.find_element(By.ID, "btnPrevPage").click()

# def Port_VLAN_TLS_Slot_Next(driver):
#     driver.find_element(By.ID, "btnNextPage").click()

# def Port_VLAN_TLS_Slot_Delete(driver):
#     driver.find_element(By.NAME, "rpVlanTlsPortDelete").click()

# # Port VLAN Trunk

# # Port VLAN Trunk > UNI-tag

# def Port_VLAN_Trunk_UNI_tag_Delete(driver):
#     driver.find_element(By.NAME, "rpVlanTrunkUniVlanDelete").click()

# def Port_VLAN_Trunk_UNI_tag_Uni_VID(driver,value):
#     input = driver.find_element(By.NAME, "rpVlanTrunkUniVlan_uniVidSetup")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def Port_VLAN_Trunk_UNI_tag_SVID(driver,value):
#     input = driver.find_element(By.NAME, "rpVlanTrunkUniVlan_svidSetup")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def Port_VLAN_Trunk_UNI_tag_Apply(driver):
#     driver.find_element(By.NAME, "rpVlanTrunkUniVlanApply").click()

# def Port_VLAN_Trunk_UNI_tag_Cancel(driver):
#     driver.find_element(By.NAME, "rpVlanTrunkUniVlanCancel").click()

# def Port_VLAN_Trunk_UNI_tag_Slot_Select(driver,slot):
#     driver.find_elements(By.CLASS_NAME, "lcman_href")[int(slot)-1].click()

# def Port_VLAN_Trunk_UNI_tag_Slot_Up(driver):
#     driver.find_element(By.NAME, "rpVlanTrunkUniVlanPort_back").click()

# def Port_VLAN_Trunk_UNI_tag_Slot_Select_All(driver,request):
#     check_box = driver.find_element(By.NAME, "rpVlanTrunkUniVlanPort_selectAll")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def Port_VLAN_Trunk_UNI_tag_Slot_Prev(driver):
#     driver.find_element(By.ID, "btnPrevPage").click()

# def Port_VLAN_Trunk_UNI_tag_Slot_Next(driver):
#     driver.find_element(By.ID, "btnNextPage").click()

# def Port_VLAN_Trunk_UNI_tag_Slot_Delete(driver):
#     driver.find_element(By.NAME, "rpVlanTrunkUniVlanPortDelete").click()

# # Port VLAN Trunk > UNI-untag

# def Port_VLAN_Trunk_UNI_untag_Delete(driver):
#     driver.find_element(By.NAME, "rpVlanTrunkUniUntagDelete").click()

# def Port_VLAN_Trunk_UNI_untag_Ether_Type(driver,request):
#     check_box = driver.find_element(By.NAME, "rpVlanTrunkUniUntag_checkEtherTypeSetup")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def Port_VLAN_Trunk_UNI_untag_Ether_Type_Input(driver,value):
#     input = driver.find_element(By.NAME, "rpVlanTrunkUniUntag_etherTypeSetup")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def Port_VLAN_Trunk_UNI_untag_Subnet_IP(driver,request):
#     check_box = driver.find_element(By.NAME, "rpVlanTrunkUniUntag_checkSubnetIpMaskSetup")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def Port_VLAN_Trunk_UNI_untag_Subnet(driver,value):
#     input = driver.find_element(By.NAME, "rpVlanTrunkUniUntag_SubnetIpMaskSetup")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def Port_VLAN_Trunk_UNI_untag_SVID(driver,value):
#     input = driver.find_element(By.NAME, "rpVlanTrunkUniUntag_svidSetup")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def Port_VLAN_Trunk_UNI_untag_Spbit(driver,value):
#     input = driver.find_element(By.NAME, "rpVlanTrunkUniUntag_spbitSetup")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def Port_VLAN_Trunk_UNI_untag_CVID(driver,value):
#     input = driver.find_element(By.NAME, "rpVlanTrunkUniUntag_cvidSetup")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def Port_VLAN_Trunk_UNI_untag_Apply(driver):
#     driver.find_element(By.NAME, "rpVlanTrunkUniUntagApply").click()

# def Port_VLAN_Trunk_UNI_untag_Cancel(driver):
#     driver.find_element(By.NAME, "rpVlanTrunkUniUntagCancel").click()

# def Port_VLAN_Trunk_UNI_untag_Slot_Select(driver,slot):
#     driver.find_elements(By.CLASS_NAME, "lcman_href")[int(slot)-1].click()

# def Port_VLAN_Trunk_UNI_untag_Slot_Up(driver):
#     driver.find_element(By.NAME, "rpVlanTrunkUniUntagPort_back").click()

# def Port_VLAN_Trunk_UNI_untag_Slot_Select_All(driver,request):
#     check_box = driver.find_element(By.NAME, "rpVlanTrunkUniUntagPort_selectAll")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def Port_VLAN_Trunk_UNI_untag_Slot_Prev(driver):
#     driver.find_element(By.ID, "btnPrevPage").click()

# def Port_VLAN_Trunk_UNI_untag_Slot_Next(driver):
#     driver.find_element(By.ID, "btnNextPage").click()

# def Port_VLAN_Trunk_UNI_untag_Slot_Delete(driver):
#     driver.find_element(By.NAME, "rpVlanTrunkUniUntagPortDelete").click()

# # Port VLAN Translation

# def Port_VLAN_Translation_Delete(driver):
#     driver.find_element(By.NAME, "rpVlanTranslationDelete").click()

# def Port_VLAN_Translation_Mode(driver,sel):
#     driver.find_element(By.XPATH, f"//*[@name='rpVlanTranslation_sltTransMode']/option[{sel}]").click()

# def Port_VLAN_Translation_Uni_VID(driver,value):
#     input = driver.find_element(By.NAME, "rpVlanTranslation_uniVidSetup")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def Port_VLAN_Translation_SVID(driver,value):
#     input = driver.find_element(By.NAME, "rpVlanTranslation_svidSetup")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def Port_VLAN_Translation_Spbit(driver,value):
#     input = driver.find_element(By.NAME, "rpVlanTranslation_spbitSetup")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def Port_VLAN_Translation_C_tag_Add(driver,request):
#     check_box = driver.find_element(By.NAME, "rpVlanTranslation_checkCvidSetup")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def Port_VLAN_Translation_CVID(driver,value):
#     input = driver.find_element(By.NAME, "rpVlanTranslation_cvidSetup")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

# def Port_VLAN_Translation_Apply(driver):
#     driver.find_element(By.NAME, "rpVlanTranslationApply").click()

# def Port_VLAN_Translation_Cancel(driver):
#     driver.find_element(By.NAME, "rpVlanTranslationCancel").click()

# def Port_VLAN_Translation_Slot_Select(driver,slot):
#     driver.find_elements(By.CLASS_NAME, "lcman_href")[int(slot)-1].click()

# def Port_VLAN_Translation_Slot_Up(driver):
#     driver.find_element(By.NAME, "rpVlanTranslationPort_back").click()

# def Port_VLAN_Translation_Slot_Select_All(driver,request):
#     check_box = driver.find_element(By.NAME, "rpVlanTranslationPort_selectAll")
#     if(check_box.is_selected() == True):
#         if(request == False):
#             check_box.click()
#     else:
#         if(request == True):
#             check_box.click()

# def Port_VLAN_Translation_Slot_Prev(driver):
#     driver.find_element(By.ID, "btnPrevPage").click()

# def Port_VLAN_Translation_Slot_Next(driver):
#     driver.find_element(By.ID, "btnNextPage").click()

# def Port_VLAN_Translation_Slot_Delete(driver):
#     driver.find_element(By.NAME, "rpVlanTranslationPortDelete").click()

# VLAN Tag Mode Setup #

def VLAN_Tag_Mode_Setup_Tag_Mode(driver,text):
    Select(driver.find_element(By.ID,"vlan_vlantagmode_mode_combobox")).select_by_visible_text(text)

def VLAN_Tag_Mode_Setup_STPID(driver,value):
    input = driver.find_element(By.ID,"vlan_vlantagmode_stpid_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def VLAN_Tag_Mode_Setup_CTPID(driver,value):
    input = driver.find_element(By.ID,"vlan_vlantagmode_ctpid_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def VLAN_Tag_Mode_Setup_QinQ_TPID(driver,value):
    input = driver.find_element(By.ID,"vlan_vlantagmode_qtpid_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def VLAN_Tag_Mode_Setup_Apply(driver):
    driver.find_element(By.CLASS_NAME,"button.button_green.mr-3").click()


