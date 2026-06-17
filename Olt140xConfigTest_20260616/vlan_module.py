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

# GE/GENNI VLAN Setup

# GE/GENNI VLAN Setup > VLAN Table

def GE_GENNI_VLAN_Setup_VLAN_Table_VLAN_ID(driver,value):
    input = driver.find_element(By.NAME, "rpvlantable_IptVID")
    input.clear()
    input.send_keys(value)

def GE_GENNI_VLAN_Setup_VLAN_Table_Egress_TPID(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpvlantable_sltEgrTpid']/option[{sel}]").click()

def GE_GENNI_VLAN_Setup_VLAN_Table_Port_Registration_All(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpvlantable_saSltRegStatus']/option[{sel}]").click()

def GE_GENNI_VLAN_Setup_VLAN_Table_Port_Tagging_All(driver,request):
    check_box = driver.find_element(By.NAME, "rpvlantable_saChkTag")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def GE_GENNI_VLAN_Setup_VLAN_Table_Port_Registration(driver,port,sel):
    driver.find_element(By.XPATH, f"/html/body/form/div[6]/span[{port}]/div[2]/select/option[{sel}]").click()

def GE_GENNI_VLAN_Setup_VLAN_Table_Port_Tagging(driver,port,request):
    check_box = driver.find_elements(By.NAME, "rpvlantable_ChkTag")[int(port)-1]
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def GE_GENNI_VLAN_Setup_VLAN_Table_Apply(driver):
    driver.find_element(By.NAME, "rpVlanEnetApply").click()

def GE_GENNI_VLAN_Setup_VLAN_Table_Cancel(driver):
    driver.find_element(By.NAME, "rpVlanEnetCancel").click()

def GE_GENNI_VLAN_Setup_VLAN_Table_Modify(driver):
    driver.find_element(By.NAME, "rpvlantable_btn_modify").click()

def GE_GENNI_VLAN_Setup_VLAN_Table_Delete(driver):
    driver.find_element(By.NAME, "rpvlantable_btn_delete").click()

# GE/GENNI VLAN Setup > VLAN Untag and Copy-Cpbit

def GE_GENNI_VLAN_Setup_VLAN_Untag_and_Copy_Cpbit_PVID(driver,value):
    input = driver.find_element(By.NAME, "rpvlanport_saIptPVID")
    input.clear()
    input.send_keys(value)

def GE_GENNI_VLAN_Setup_VLAN_Untag_and_Copy_Cpbit_Pbit(driver,value):
    input = driver.find_element(By.NAME, "rpvlanport_saIptPbit")
    input.clear()
    input.send_keys(value)

def GE_GENNI_VLAN_Setup_VLAN_Untag_and_Copy_Cpbit_Frame_Type(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpvlanport_slt_saRXTag']/option[{sel}]").click()

def GE_GENNI_VLAN_Setup_VLAN_Untag_and_Copy_Cpbit_Copy_Cpbit_Enable(driver,request):
    check_box = driver.find_element(By.NAME, "rpvlanport_saChkVlanCopyCpbit")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def GE_GENNI_VLAN_Setup_VLAN_Untag_and_Copy_Cpbit_Outer_TPID_Enable(driver,request):
    check_box = driver.find_element(By.NAME, "rpvlanport_saChkVlanOuterTpid")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def GE_GENNI_VLAN_Setup_VLAN_Untag_and_Copy_Cpbit_Apply(driver):
    driver.find_element(By.NAME, "rpVlanEnetApply").click()

def GE_GENNI_VLAN_Setup_VLAN_Untag_and_Copy_Cpbit_Cancel(driver):
    driver.find_element(By.NAME, "rpVlanEnetCancel").click()

# Port VLAN TLS

def Port_VLAN_TLS_Delete(driver):
    driver.find_element(By.NAME, "rpVlanTlsDelete").click()

def Port_VLAN_TLS_SVID(driver,value):
    input = driver.find_element(By.NAME, "rpVlanTls_svidSetup")
    input.clear()
    input.send_keys(value)

def Port_VLAN_TLS_Spbit(driver,value):
    input = driver.find_element(By.NAME, "rpVlanTls_spbitSetup")
    input.clear()
    input.send_keys(value)

def Port_VLAN_TLS_Apply(driver):
    driver.find_element(By.NAME, "rpVlanTlsApply").click()

def Port_VLAN_TLS_Cancel(driver):
    driver.find_element(By.NAME, "rpVlanTlsCancel").click()

def Port_VLAN_TLS_Slot_Select(driver,slot):
    driver.find_elements(By.CLASS_NAME, "lcman_href")[int(slot)-1].click()

def Port_VLAN_TLS_Slot_Up(driver):
    driver.find_element(By.NAME, "rpVlanTlsPort_back").click()

def Port_VLAN_TLS_Slot_Select_All(driver,request):
    check_box = driver.find_element(By.NAME, "rpVlanTlsPort_selectAll")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Port_VLAN_TLS_Slot_Prev(driver):
    driver.find_element(By.ID, "btnPrevPage").click()

def Port_VLAN_TLS_Slot_Next(driver):
    driver.find_element(By.ID, "btnNextPage").click()

def Port_VLAN_TLS_Slot_Delete(driver):
    driver.find_element(By.NAME, "rpVlanTlsPortDelete").click()

# Port VLAN Trunk

# Port VLAN Trunk > UNI-tag

def Port_VLAN_Trunk_UNI_tag_Delete(driver):
    driver.find_element(By.NAME, "rpVlanTrunkUniVlanDelete").click()

def Port_VLAN_Trunk_UNI_tag_Uni_VID(driver,value):
    input = driver.find_element(By.NAME, "rpVlanTrunkUniVlan_uniVidSetup")
    input.clear()
    input.send_keys(value)

def Port_VLAN_Trunk_UNI_tag_SVID(driver,value):
    input = driver.find_element(By.NAME, "rpVlanTrunkUniVlan_svidSetup")
    input.clear()
    input.send_keys(value)

def Port_VLAN_Trunk_UNI_tag_Apply(driver):
    driver.find_element(By.NAME, "rpVlanTrunkUniVlanApply").click()

def Port_VLAN_Trunk_UNI_tag_Cancel(driver):
    driver.find_element(By.NAME, "rpVlanTrunkUniVlanCancel").click()

def Port_VLAN_Trunk_UNI_tag_Slot_Select(driver,slot):
    driver.find_elements(By.CLASS_NAME, "lcman_href")[int(slot)-1].click()

def Port_VLAN_Trunk_UNI_tag_Slot_Up(driver):
    driver.find_element(By.NAME, "rpVlanTrunkUniVlanPort_back").click()

def Port_VLAN_Trunk_UNI_tag_Slot_Select_All(driver,request):
    check_box = driver.find_element(By.NAME, "rpVlanTrunkUniVlanPort_selectAll")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Port_VLAN_Trunk_UNI_tag_Slot_Prev(driver):
    driver.find_element(By.ID, "btnPrevPage").click()

def Port_VLAN_Trunk_UNI_tag_Slot_Next(driver):
    driver.find_element(By.ID, "btnNextPage").click()

def Port_VLAN_Trunk_UNI_tag_Slot_Delete(driver):
    driver.find_element(By.NAME, "rpVlanTrunkUniVlanPortDelete").click()

# Port VLAN Trunk > UNI-untag

def Port_VLAN_Trunk_UNI_untag_Delete(driver):
    driver.find_element(By.NAME, "rpVlanTrunkUniUntagDelete").click()

def Port_VLAN_Trunk_UNI_untag_Ether_Type(driver,request):
    check_box = driver.find_element(By.NAME, "rpVlanTrunkUniUntag_checkEtherTypeSetup")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Port_VLAN_Trunk_UNI_untag_Ether_Type_Input(driver,value):
    input = driver.find_element(By.NAME, "rpVlanTrunkUniUntag_etherTypeSetup")
    input.clear()
    input.send_keys(value)

def Port_VLAN_Trunk_UNI_untag_Subnet_IP(driver,request):
    check_box = driver.find_element(By.NAME, "rpVlanTrunkUniUntag_checkSubnetIpMaskSetup")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Port_VLAN_Trunk_UNI_untag_Subnet(driver,value):
    input = driver.find_element(By.NAME, "rpVlanTrunkUniUntag_SubnetIpMaskSetup")
    input.clear()
    input.send_keys(value)

def Port_VLAN_Trunk_UNI_untag_SVID(driver,value):
    input = driver.find_element(By.NAME, "rpVlanTrunkUniUntag_svidSetup")
    input.clear()
    input.send_keys(value)

def Port_VLAN_Trunk_UNI_untag_Spbit(driver,value):
    input = driver.find_element(By.NAME, "rpVlanTrunkUniUntag_spbitSetup")
    input.clear()
    input.send_keys(value)

def Port_VLAN_Trunk_UNI_untag_CVID(driver,value):
    input = driver.find_element(By.NAME, "rpVlanTrunkUniUntag_cvidSetup")
    input.clear()
    input.send_keys(value)

def Port_VLAN_Trunk_UNI_untag_Apply(driver):
    driver.find_element(By.NAME, "rpVlanTrunkUniUntagApply").click()

def Port_VLAN_Trunk_UNI_untag_Cancel(driver):
    driver.find_element(By.NAME, "rpVlanTrunkUniUntagCancel").click()

def Port_VLAN_Trunk_UNI_untag_Slot_Select(driver,slot):
    driver.find_elements(By.CLASS_NAME, "lcman_href")[int(slot)-1].click()

def Port_VLAN_Trunk_UNI_untag_Slot_Up(driver):
    driver.find_element(By.NAME, "rpVlanTrunkUniUntagPort_back").click()

def Port_VLAN_Trunk_UNI_untag_Slot_Select_All(driver,request):
    check_box = driver.find_element(By.NAME, "rpVlanTrunkUniUntagPort_selectAll")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Port_VLAN_Trunk_UNI_untag_Slot_Prev(driver):
    driver.find_element(By.ID, "btnPrevPage").click()

def Port_VLAN_Trunk_UNI_untag_Slot_Next(driver):
    driver.find_element(By.ID, "btnNextPage").click()

def Port_VLAN_Trunk_UNI_untag_Slot_Delete(driver):
    driver.find_element(By.NAME, "rpVlanTrunkUniUntagPortDelete").click()

# Port VLAN Translation

def Port_VLAN_Translation_Delete(driver):
    driver.find_element(By.NAME, "rpVlanTranslationDelete").click()

def Port_VLAN_Translation_Mode(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpVlanTranslation_sltTransMode']/option[{sel}]").click()

def Port_VLAN_Translation_Uni_VID(driver,value):
    input = driver.find_element(By.NAME, "rpVlanTranslation_uniVidSetup")
    input.clear()
    input.send_keys(value)

def Port_VLAN_Translation_SVID(driver,value):
    input = driver.find_element(By.NAME, "rpVlanTranslation_svidSetup")
    input.clear()
    input.send_keys(value)

def Port_VLAN_Translation_Spbit(driver,value):
    input = driver.find_element(By.NAME, "rpVlanTranslation_spbitSetup")
    input.clear()
    input.send_keys(value)

def Port_VLAN_Translation_C_tag_Add(driver,request):
    check_box = driver.find_element(By.NAME, "rpVlanTranslation_checkCvidSetup")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Port_VLAN_Translation_CVID(driver,value):
    input = driver.find_element(By.NAME, "rpVlanTranslation_cvidSetup")
    input.clear()
    input.send_keys(value)

def Port_VLAN_Translation_Apply(driver):
    driver.find_element(By.NAME, "rpVlanTranslationApply").click()

def Port_VLAN_Translation_Cancel(driver):
    driver.find_element(By.NAME, "rpVlanTranslationCancel").click()

def Port_VLAN_Translation_Slot_Select(driver,slot):
    driver.find_elements(By.CLASS_NAME, "lcman_href")[int(slot)-1].click()

def Port_VLAN_Translation_Slot_Up(driver):
    driver.find_element(By.NAME, "rpVlanTranslationPort_back").click()

def Port_VLAN_Translation_Slot_Select_All(driver,request):
    check_box = driver.find_element(By.NAME, "rpVlanTranslationPort_selectAll")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Port_VLAN_Translation_Slot_Prev(driver):
    driver.find_element(By.ID, "btnPrevPage").click()

def Port_VLAN_Translation_Slot_Next(driver):
    driver.find_element(By.ID, "btnNextPage").click()

def Port_VLAN_Translation_Slot_Delete(driver):
    driver.find_element(By.NAME, "rpVlanTranslationPortDelete").click()

# VLAN Tag Mode Setup

def VLAN_Tag_Mode_Setup_Tag_Mode(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpVlanSingleTag_sltStagMode']/option[{sel}]").click()

def VLAN_Tag_Mode_Setup_STPID(driver,value):
    input = driver.find_element(By.NAME, "rpVlanSingleTag_stpidSetup")
    input.clear()
    input.send_keys(value)

def VLAN_Tag_Mode_Setup_CTPID(driver,value):
    input = driver.find_element(By.NAME, "rpVlanSingleTag_ctpidSetup")
    input.clear()
    input.send_keys(value)

def VLAN_Tag_Mode_Setup_QinQ_TPID(driver,value):
    input = driver.find_element(By.NAME, "rpVlanSingleTag_qinqtpidSetup")
    input.clear()
    input.send_keys(value)

def VLAN_Tag_Mode_Setup_Apply(driver):
    driver.find_element(By.NAME, "rpVlanSingleTagApply").click()

def VLAN_Tag_Mode_Setup_Cancel(driver):
    driver.find_element(By.NAME, "rpVlanSingleTagCancel").click()
