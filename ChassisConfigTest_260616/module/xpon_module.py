from selenium.webdriver.common.by import By
from os import times
import time
import datetime
from attr import field
# from pyrsistent import s
import module.selenium_module as mod
import module.xpon_olt_status_module as olts
import module.xpon_olt_config_module as oltc
import module.xpon_batch_ont_config_module as bat
import module.xpon_ont_config_module as ontc
import module.xpon_profiles_module as pro
import module.multicast_module as mul
import module.xpon_profiles_config_module as procf
from selenium.webdriver.support.ui import Select
import pyautogui

# from robot.api import TestSuite
# from robot.api import ResultWriter
# from robot.libraries.BuiltIn import BuiltIn
from selenium import webdriver
# from robot.libraries.BuiltIn import RobotNotRunningError
# from robot.api import logger

#import win32com.client as win32
# from docx import Document
# from docx.shared import Inches

import module.acl_module_glc as acl
import module.ems_acl_module as e_acl

template_capacity = 1024
service_profile_capacity = 4094
qos_bandwidth_profile_capacity = 1024
multicast_profile_capacity = 1024
uni_profile_capacity = 1024
security_profile_capacity = 128
ont_profile_capacity = 512
sip_profile_capacity = 64
voip_common_profile_capacity = 64
dial_plan_profile_capacity = 64
ACL_profile_capacity = 256
Ont_Alarm_profile_capacity = 256
# 剩下
# uni test
# security test

def Maintenance_Config_Reset(driver,file_name):
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Maintenance")
    mod.SubPage_Switch(driver,"Config Reset")
    mod.Switch_Frame(driver)
    driver.find_element(By.NAME, "rpConfigReset").click()
    pyautogui.press("enter")
    time.sleep(60)

def System_Summary_Test(driver,slot_x_1_aid,msc_card_type,olc_card_type,file_name):
    print(f"XPON System Summary Test\nTest Start",file = open(file_name, '+a'))
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "System Summary").click()
    driver.switch_to.frame(0)
    if_error = False
    time.sleep(1)
    xpon_control_card = driver.find_element(By.ID, "rpcontrol_card").get_attribute("textContent")
    xpon_control_card = xpon_control_card.split(" ")[2]
    if(msc_card_type == xpon_control_card):
        print("             [XPON - System Summary] MSC Cardtype Test Pass",file = open(file_name, '+a'))
    else:
        print("             [XPON - System Summary] MSC Cardtype Test Fail",file = open(file_name, '+a'))
        if_error = True
    olc_model_name = ""
    for index in range(driver.find_elements(By.NAME, "rpSysSum_slotPortStr").__len__()):
        if(driver.find_elements(By.NAME, "rpSysSum_slotPortStr")[index].get_attribute("textContent") == slot_x_1_aid):
            olc_model_name = driver.find_elements(By.NAME, "rpSysSum_model")[index].get_attribute("textContent")
    if(olc_card_type == olc_model_name):
        print("             [XPON - System Summary] XPON Cardtype Test Pass",file = open(file_name, '+a'))
    else:
        print("             [XPON - System Summary] XPON Cardtype Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(if_error == False):
        print("[MSAN1-12144][XPON - System Summary] Result Pass",file = open(file_name, '+a'))
    else:
        print("[MSAN1-12144][XPON - System Summary] Result Fail",file = open(file_name, '+a'))
    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def OLT_brief_Test(driver,slot_x_1_aid,pon_x_1_aid,file_name):
    print(f"XPON OLT brief Test\nTest Start",file = open(file_name, '+a'))
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "OLT Config").click()
    time.sleep(5)
    driver.switch_to.frame(0)    
    if_find = False
    for index in range(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOltConfig_TableOltPort").__len__()):
        if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOltConfig_TableOltPort")[index].get_attribute("textContent") == f"{slot_x_1_aid}-{pon_x_1_aid}"):
            if_find = True
            driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOltConfig_TableOltPort")[index].click()
            oltc.Active(driver,True)
            oltc.Apply(driver)
            time.sleep(5)
            break
    if(if_find != True):
        print(f"             [XPON - OLT Config] ONT {slot_x_1_aid}-{pon_x_1_aid} Not Found Active Setup Fail",file = open(file_name, '+a'))
        if_error = True
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "OLT brief").click()
    driver.switch_to.frame(0)
    if_find = False
    for index in range(driver.find_elements(By.NAME, "rpOltBrief_slotPortStr").__len__()):
        if(driver.find_elements(By.NAME, "rpOltBrief_slotPortStr")[index].get_attribute("textContent") == f"{slot_x_1_aid}-{pon_x_1_aid}\n"):
            if_find = True
            if(driver.find_element(By.XPATH, f"(.//*[normalize-space(text()) and normalize-space(.)='Config'])[{index}]/following::a[2]").get_attribute("style") == ""):
                print("             [XPON - OLT Brief] status Working Test Pass",file = open(file_name, '+a')) 
                print("[MSAN1-12145][XPON - OLT Brief] Result Pass",file = open(file_name, '+a'))
            else:
                print("             [XPON - OLT Brief] status Working Test Fail(#175087)",file = open(file_name, '+a')) 
                print("[MSAN1-12145][XPON - OLT Brief] Result Fail",file = open(file_name, '+a'))  
            break
    if(if_find == False):
        print(f"             [XPON - OLT Brief] Port {slot_x_1_aid}-{pon_x_1_aid} Not Found Test Fail",file = open(file_name, '+a')) 
        print("[MSAN1-12145][XPON - OLT Brief] Result Fail",file = open(file_name, '+a'))  #找不到xpon port
    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def OLT_Status_Test(driver,slot_x_1_aid,pon_x_1_aid,file_name):
    print(f"XPON OLT Status Test\nTest Start",file = open(file_name, '+a'))
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "OLT Status").click()
    driver.switch_to.frame(0)
    olts.Port_Select(driver,slot_x_1_aid,pon_x_1_aid)
    olts.Refresh(driver)
    if_error = False
    if(driver.find_element(By.CLASS_NAME, "xgspon-table-td-content.rpXgponOltStatus_linkStatus").get_attribute("textContent") == "Active"):
        print("             [XPON - OLT Status] Link Status Active Test Pass",file = open(file_name, '+a'))
    else:
        print("             [XPON - OLT Status] Link Status Active Test Fail",file = open(file_name, '+a'))
        if_error = True

    if(driver.find_element(By.CLASS_NAME, "xgspon-table-td-content.rpXgponOltStatus_keyExchangeInterval").get_attribute("textContent") == "60000"):
        print("             [XPON - OLT Status] Key Exchange Interval check Pass",file = open(file_name, '+a'))
    else:
        print("             [XPON - OLT Status] Key Exchange Interval check Fail",file = open(file_name, '+a'))
        if_error = True

    if(driver.find_element(By.CLASS_NAME, "xgspon-table-td-content.rpXgponOltStatus_snAcqInterval").get_attribute("textContent") == "8000"):
        print("             [XPON - OLT Status] SN Acq Interval check Pass",file = open(file_name, '+a'))
    else:
        print("             [XPON - OLT Status] SN Acq Interval check Fail",file = open(file_name, '+a'))
        if_error = True
    
    if(driver.find_element(By.CLASS_NAME, "xgspon-table-td-content.rpXgponOltStatus_keyExchageStatus").get_attribute("textContent") == "Enable"):
        print("             [XPON - OLT Status] Key Exchage Status check Pass",file = open(file_name, '+a'))
    else:
        print("             [XPON - OLT Status] Key Exchage Status check Fail",file = open(file_name, '+a'))
        if_error = True

    if(driver.find_element(By.CLASS_NAME, "xgspon-table-td-content.rpXgponOltStatus_snAcqState").get_attribute("textContent") == "Enable"):
        print("             [XPON - OLT Status] SN Acq Status check Pass",file = open(file_name, '+a'))
    else:
        print("             [XPON - OLT Status] SN Acq Status check Fail",file = open(file_name, '+a'))
        if_error = True

    if(driver.find_element(By.CLASS_NAME, "xgspon-table-td-content.rpXgponOltStatus_losStatus").get_attribute("textContent") == "Off"):
        print("             [XPON - OLT Status] LOS Status check Pass",file = open(file_name, '+a'))
    else:
        print("             [XPON - OLT Status] LOS Status check Fail",file = open(file_name, '+a'))
        if_error = True
    
    if(driver.find_element(By.CLASS_NAME, "xgspon-table-td-content.rpXgponOltStatus_txPower").get_attribute("textContent") == "Enable"):
        print("             [XPON - OLT Status] Tx Power check Pass",file = open(file_name, '+a'))
    else:
        print("             [XPON - OLT Status] Tx Power check Fail",file = open(file_name, '+a'))
        if_error = True
    
    if(driver.find_element(By.CLASS_NAME, "xgspon-table-td-content.rpXgponOltStatus_xontLinkStatus").get_attribute("textContent") == "Connected"):
        print("             [XPON - OLT Status] xontLinkStatus check Pass",file = open(file_name, '+a'))
    else:
        print("             [XPON - OLT Status] xontLinkStatus check Fail",file = open(file_name, '+a'))
        if_error = True
        

    if(if_error == True):
        print("[MSAN1-12147][XPON - OLT Status] Result Fail",file = open(file_name, '+a'))
    else:
        print("[MSAN1-12147][XPON - OLT Status] Result Pass",file = open(file_name, '+a'))
    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def XPON_Register_Test(driver,slot_x_1_aid,pon_x_1_aid,ont_x_1_1_sn,username,password,service_mode_x_1,file_name):# 還沒跑過
    print(f"XPON Register Test\nTest Start",file = open(file_name, '+a'))
    
    template_name = ["______________xpon_template_SFU","______________xpon_template_HGU"]
    create_name = ["SFU","HGU"]
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    time.sleep(5)
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Service").click()
    time.sleep(5)
    if_delete = False
    if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__() > service_profile_capacity-2):
        if_delete = True
    for check_time in range(2):
        if_find = False
        for index in range(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponServiceProf_name").__len__()):
            try:
                driver.switch_to.default_content()
                driver.find_element(By.ID, "userContinue").click()
                driver.switch_to.frame(0)
            except:
                try:
                    driver.switch_to.default_content()
                    driver.find_element(By.CLASS_NAME, "ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-front.ui-draggable")
                    driver.find_element(By.ID, "lg_user").send_keys(username)
                    driver.find_element(By.ID, "lg_pass").send_keys(password)
                    driver.find_element(By.ID, "userLogin").click()
                    driver.switch_to.frame(0)
                except:
                    driver.switch_to.frame(0)
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponServiceProf_name")[-(index+1)].get_attribute("textContent") == f"_______xpon_service_profile_{create_name[check_time]}"):
                if_find = True
                break
        if(if_find == False):
            if(if_delete == True):
                driver.find_elements(By.NAME, "rpXGSponServiceProf_chkDel")[-1].click()
                driver.find_elements(By.NAME, "rpXGSponServiceProf_chkDel")[-2].click()
                pro.Service_Profile_Delete(driver)
                if_delete = False
            pro.Service_Profile_New(driver)
            pro.Service_Profile_New_Name(driver,f"_______xpon_service_profile_{create_name[check_time]}")
            pro.Service_Profile_New_VLAN(driver,"4094")
            pro.Service_Profile_New_Mapper_Pbits(driver,0,True)
            pro.Service_Profile_New_Mapper_Pbits(driver,1,True)
            pro.Service_Profile_New_Mapper_Pbits(driver,2,True)
            pro.Service_Profile_New_Mapper_Pbits(driver,3,True)
            pro.Service_Profile_New_Mapper_Pbits(driver,4,True)
            pro.Service_Profile_New_Mapper_Pbits(driver,5,True)
            pro.Service_Profile_New_Mapper_Pbits(driver,6,True)
            pro.Service_Profile_New_Mapper_Pbits(driver,7,True)
            pro.Service_Profile_New_Lan_mode_veip(driver)
            pro.Service_Profile_New_Lan_mode_bridge(driver)
            pro.Service_Profile_New_Lan(driver,"Lan 8")
            pro.Service_Profile_New_Vlan_xc(driver,"4094")
            pro.Service_Profile_New_Vlan_xc_mode_enable(driver)
            pro.Service_Profile_New_Vlan_xc_mode_disable(driver)
            pro.Service_Profile_New_Apply(driver)

    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    time.sleep(5)
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "QoS Bandwidth").click()
    time.sleep(5)
    if_delete = False
    if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__() > qos_bandwidth_profile_capacity-1):
        if_delete = True
    for check_time in range(2):
        if_find = False
        for index in range(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponQosBwProf_name").__len__()):
            try:
                driver.switch_to.default_content()
                driver.find_element(By.ID, "userContinue").click()
                driver.switch_to.frame(0)
            except:
                try:
                    driver.switch_to.default_content()
                    driver.find_element(By.CLASS_NAME, "ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-front.ui-draggable")
                    driver.find_element(By.ID, "lg_user").send_keys(username)
                    driver.find_element(By.ID, "lg_pass").send_keys(password)
                    driver.find_element(By.ID, "userLogin").click()
                    driver.switch_to.frame(0)
                except:
                    driver.switch_to.frame(0)
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponQosBwProf_name")[-(index+1)].get_attribute("textContent") == "______________100M"):
                if_find = True
                break
        if(if_find == False):
            if(if_delete == True):
                driver.find_elements(By.NAME, "rpXGSponQosBwProf_chkDel")[-1].click()
                pro.QoS_Bandwidth_Profile_Delete(driver)
                if_delete = False
            pro.QoS_Bandwidth_Profile_New(driver)
            pro.QoS_Bandwidth_Profile_New_Name(driver,"______________100M")
            pro.QoS_Bandwidth_Profile_New_sir(driver,"500000")
            pro.QoS_Bandwidth_Profile_New_air(driver,"500000")
            pro.QoS_Bandwidth_Profile_New_pir(driver,"10000000")
            pro.QoS_Bandwidth_Profile_New_Apply(driver)

    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    time.sleep(5)
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Template").click()
    time.sleep(5)
    if_delete = False
    if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__() > template_capacity-2):
        if_delete = True
    for check_time in range(2):
        if_find = False
        for index in range(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponTemplate_name").__len__()):
            try:
                driver.switch_to.default_content()
                driver.find_element(By.ID, "userContinue").click()
                driver.switch_to.frame(0)
            except:
                try:
                    driver.switch_to.default_content()
                    driver.find_element(By.CLASS_NAME, "ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-front.ui-draggable")
                    driver.find_element(By.ID, "lg_user").send_keys(username)
                    driver.find_element(By.ID, "lg_pass").send_keys(password)
                    driver.find_element(By.ID, "userLogin").click()
                    driver.switch_to.frame(0)
                except:
                    driver.switch_to.frame(0)
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponTemplate_name")[-(index+1)].get_attribute("textContent") == f"______________xpon_template_{create_name[check_time]}"):
                if_find = True
                break
        if(if_find == False):
            if(if_delete == True):
                driver.find_elements(By.NAME, "rpXGSponTemplate_chkDel")[-1].click()
                driver.find_elements(By.NAME, "rpXGSponTemplate_chkDel")[-2].click()
                pro.Template_Delete(driver)
                if_delete = False
            pro.Template_New(driver)
            pro.Template_New_Name(driver,f"______________xpon_template_{create_name[check_time]}")
            driver.find_element(By.ID, "tab_service").click()
            pro.Template_New_Service_Profile_Active_Select(driver,8,True)
            pro.Template_New_Service_Profile_all(driver,f"_______xpon_service_profile_{create_name[check_time]}")
            pro.Template_New_Service_Shared_Priority_Select(driver,8,"7")
            pro.Template_New_Service_US_Bandwidth_Profile_Select(driver,8,"______________100M")
            pro.Template_New_Service_DS_Bandwidth_Profile_Select(driver,8,"______________100M")
            driver.find_element(By.LINK_TEXT, "T-Cont").click()
            pro.Template_New_Tcont_Service_List_Active_Select(driver,8,True)
            pro.Template_New_Tcont_Service_List_Select(driver,8,"8")
            pro.Template_New_Tcont_US_Bandwidth_Profile_Select(driver,8,"______________100M")
            pro.Template_New_Tcont_DS_Bandwidth_Profile_Select(driver,8,"______________100M")
            pro.Template_New_Tcont_Type_Select(driver,8,"best-effort")
            pro.Template_New_Apply(driver)
    ### Pre-config finish

    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "OLT Config").click()
    time.sleep(5)
    driver.switch_to.frame(0)
    if_error = False
    if_find = False
    for index in range(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOltConfig_TableOltPort").__len__()):
        olt_config_port = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOltConfig_TableOltPort")[index].get_attribute("textContent")
        if(olt_config_port.split("-")[0] == slot_x_1_aid):
            if_find = True
            driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOltConfig_TableOltPort")[index].click()
            oltc.Active(driver,True)
            oltc.Name(driver,"12345678901234567890123456789012")
            oltc.Tel(driver,"12345678901234567890123456789012")
            oltc.Register_Method(driver,"E")
            oltc.Ranging_distance(driver,"61")
            if(mod.IsAlert(driver) != True):
                print(f"             [XPON - OLT Config] {olt_config_port} Ranging distance:61 No Alert Test Fail(#175089)",file = open(file_name, '+a'))
                if_error = True
            oltc.Ranging_distance(driver,"60")
            oltc.ONT_Template(driver,template_name[0])
            oltc.Apply(driver)
            time.sleep(5)
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOltConfig_TableActive")[index].get_attribute("textContent") != "Y"):
                print(f"             [XPON - OLT Config] {olt_config_port} Active Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOltConfig_TableName")[index].get_attribute("textContent") != "12345678901234567890123456789012"):
                print(f"             [XPON - OLT Config] {olt_config_port} Name Test Fail(#175088)",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOltConfig_TableTel")[index].get_attribute("textContent") != "12345678901234567890123456789012"):
                print(f"             [XPON - OLT Config] {olt_config_port} Tel Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOltConfig_TableRegisterMethod")[index].get_attribute("textContent") != "E"):
                print(f"             [XPON - OLT Config] {olt_config_port} RegisterMethod Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOltConfig_TableRangingDistance")[index].get_attribute("textContent") != "60"):
                print(f"             [XPON - OLT Config] {olt_config_port} RangingDistance Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOltConfig_TableOntTemplate")[index].get_attribute("textContent") != template_name[0]):
                print(f"             [XPON - OLT Config] {olt_config_port} ONT-Template Test Fail",file = open(file_name, '+a'))
                if_error = True
            driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOltConfig_TableOltPort")[index].click()
            oltc.Active(driver,False)
            oltc.Name(driver,"")
            oltc.Tel(driver,"")
            oltc.Register_Method(driver,"A")
            oltc.Ranging_distance(driver,"20")
            oltc.ONT_Template(driver," ")
            oltc.Apply(driver)
            time.sleep(5)
    if(if_find != True):
        print(f"             [XPON - OLT Config] ONT Slot={slot_x_1_aid} Not Found Apply Fail",file = open(file_name, '+a'))
    if_find = False
    for index in range(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOltConfig_TableOltPort").__len__()):
        if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOltConfig_TableOltPort")[index].get_attribute("textContent") == f"{slot_x_1_aid}-{pon_x_1_aid}"):
            if_find = True
            driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOltConfig_TableOltPort")[index].click()
            oltc.Active(driver,True)
            oltc.Name(driver,"12345678901234567890123456789012")
            oltc.Tel(driver,"12345678901234567890123456789012")
            oltc.Register_Method(driver,"A")
            oltc.Ranging_distance(driver,"20")
            oltc.ONT_Template(driver,template_name[0])
            oltc.Apply(driver)
            time.sleep(5)
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOltConfig_TableActive")[index].get_attribute("textContent") != "Y"):
                print(f"             [XPON - OLT Config] {slot_x_1_aid}-{pon_x_1_aid} Active Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOltConfig_TableName")[index].get_attribute("textContent") != "12345678901234567890123456789012"):
                print(f"             [XPON - OLT Config] {slot_x_1_aid}-{pon_x_1_aid}(variable) Name Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOltConfig_TableTel")[index].get_attribute("textContent") != "12345678901234567890123456789012"):
                print(f"             [XPON - OLT Config] {slot_x_1_aid}-{pon_x_1_aid} Tel Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOltConfig_TableRegisterMethod")[index].get_attribute("textContent") != "A"):
                print(f"             [XPON - OLT Config] {slot_x_1_aid}-{pon_x_1_aid} RegisterMethod Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOltConfig_TableRangingDistance")[index].get_attribute("textContent") != "20"):
                print(f"             [XPON - OLT Config] {slot_x_1_aid}-{pon_x_1_aid} RangingDistance Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOltConfig_TableOntTemplate")[index].get_attribute("textContent") != template_name[0]):
                print(f"             [XPON - OLT Config] {slot_x_1_aid}-{pon_x_1_aid} ONT-Template Test Fail",file = open(file_name, '+a'))
                if_error = True
            break
    if(if_find != True):
        print(f"             [XPON - OLT Config] ONT {slot_x_1_aid}-{pon_x_1_aid} Not Found Setup Apply Fail",file = open(file_name, '+a'))
        if_error = True
   ### Add OLT Config page result
            
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "ONT Config").click()
    time.sleep(5)
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Main").click()
    time.sleep(5)
    ontc.Main_Delete_Select_All(driver,True)
    ontc.Main_Delete(driver)
    time.sleep(60)

    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Batch ONT Config").click()
    time.sleep(5)
    driver.switch_to.frame(0)
    if_find = False
    for index in range(driver.find_elements(By.NAME, "rpxontmgmt_port").__len__()):
        if(driver.find_elements(By.NAME, "rpxontmgmt_serial_numberStr")[index].get_attribute("textContent") == f"{service_mode_x_1}"):
            if_find = True
            if(driver.find_elements(By.NAME, "rpxontmgmt_status")[index].get_attribute("textContent") != "Unregistered"):
                print(f"             [XPON - Batch ONT Config] SN {service_mode_x_1} Status: Unregistered Test Fail",file = open(file_name, '+a'))
                if_error = True
            driver.find_elements(By.NAME, "rpxont_chk")[index].click()
            break
    if(if_find == False):
        print(f"             [XPON - Batch ONT Config]  SN {service_mode_x_1} Edit Not Found Test Fail",file = open(file_name, '+a'))
        if_error = True
    else:
        bat.Action(driver,"create config")
        bat.Create_config_with_default_template_profile(driver,"______________xpon_template_SFU")
        bat.ONT_description(driver,"123456789012345601")
        bat.Apply(driver)
    if_find = False
    for index in range(driver.find_elements(By.NAME, "rpxontmgmt_port").__len__()):
        if(driver.find_elements(By.NAME, "rpxontmgmt_serial_numberStr")[index].get_attribute("textContent") == f"{service_mode_x_1}"):
            if_find = True
            if(driver.find_elements(By.NAME, "rpxontmgmt_status")[index].get_attribute("textContent") != "Configured"):
                print(f"             [XPON - Batch ONT Config] SN {service_mode_x_1} Status:Configured Test Fail(#175095)",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.NAME, "rpxont_description")[index].get_attribute("textContent") != "123456789012345601"):
                print(f"             [XPON - Batch ONT Config] SN {service_mode_x_1} Description Test Fail(#175091)",file = open(file_name, '+a'))
                if_error = True
            break
    if(if_find == False):
        print(f"             [XPON - Batch ONT Config] SN {service_mode_x_1} Check Not Found Test Fail",file = open(file_name, '+a'))
        if_error = True

    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "ONT Config").click()
    time.sleep(5)
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Main").click()
    time.sleep(5)
    if_find = False
    for index in range(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOntConfig_TableSN").__len__()):
        ont_config_ont = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOntConfig_TableSN")[index].get_attribute("textContent")
        if(ont_config_ont.split("-")[0] == slot_x_1_aid and ont_config_ont.split("-")[1] == pon_x_1_aid ):
            if_find = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOntConfig_TableOntTemplate")[index].get_attribute("textContent") != "______________xpon_template_SFU"):
                print(f"             [XPON - ONT Config] ONT {ont_config_ont} ONT Template:SFU Test Fail",file = open(file_name, '+a'))
                if_error = True
    if(if_find == False):
        print(f"             [XPON - ONT Config] ONT {slot_x_1_aid}-{pon_x_1_aid} Check Not Found Test Fail",file = open(file_name, '+a'))
        if_error = True

    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Batch ONT Config").click()
    time.sleep(5)
    driver.switch_to.frame(0)
    if_find = False
    for index in range(driver.find_elements(By.NAME, "rpxontmgmt_port").__len__()):
        if(driver.find_elements(By.NAME, "rpxontmgmt_port")[index].get_attribute("textContent") == f"{slot_x_1_aid}-{pon_x_1_aid}"):
            if_find = True
            driver.find_elements(By.NAME, "rpxont_chk")[index].click()
    if(if_find == False):
        print(f"             [XPON - Batch ONT Config] {slot_x_1_aid}-{pon_x_1_aid} Edit Not Found Test Fail",file = open(file_name, '+a'))
        if_error = True
    else:
        bat.Action(driver,"create config")
        bat.Create_config_with_default_template_profile(driver,"______________xpon_template_HGU")
        bat.ONT_description(driver,"123456789012345602")
        bat.Apply(driver)
    for loop in range(3):
        driver.switch_to.default_content()
        driver.find_element(By.LINK_TEXT, "XPON").click()
        driver.find_element(By.LINK_TEXT, "Batch ONT Config").click()
        time.sleep(5)
        driver.switch_to.frame(0)
        if_find = False
        time.sleep(10)
        for index in range(driver.find_elements(By.NAME, "rpxontmgmt_port").__len__()):
            if(driver.find_elements(By.NAME, "rpxontmgmt_port")[index].get_attribute("textContent") == f"{slot_x_1_aid}-{pon_x_1_aid}"):
                if(driver.find_elements(By.NAME, "rpxontmgmt_status")[index].get_attribute("textContent") == "Unregistered"):
                    if_find = True
                    driver.find_elements(By.NAME, "rpxont_chk")[index].click()
        if(if_find == True):
            bat.Action(driver,"create config")
            bat.Create_config_with_default_template_profile(driver,"______________xpon_template_HGU")
            bat.ONT_description(driver,"123456789012345602")
            bat.Apply(driver)
    if_find = False
    for index in range(driver.find_elements(By.NAME, "rpxontmgmt_port").__len__()):
        if(driver.find_elements(By.NAME, "rpxontmgmt_port")[index].get_attribute("textContent") == f"{slot_x_1_aid}-{pon_x_1_aid}"):
            if_find = True
            if(driver.find_elements(By.NAME, "rpxontmgmt_status")[index].get_attribute("textContent") != "Configured"):
                print(f"             [XPON - Batch ONT Config] {slot_x_1_aid}-{pon_x_1_aid} Status:Configured Test Fail(#175095)",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.NAME, "rpxont_description")[index].get_attribute("textContent") != "123456789012345602"):
                print(f"             [XPON - Batch ONT Config] {slot_x_1_aid}-{pon_x_1_aid} Description Test Fail(#175091)",file = open(file_name, '+a'))
                if_error = True
            break
    if(if_find == False):
        print(f"             [XPON - Batch ONT Config] {slot_x_1_aid}-{pon_x_1_aid} Check Not Found Test Fail",file = open(file_name, '+a'))
        if_error = True
        
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "ONT Config").click()
    time.sleep(5)
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Main").click()
    time.sleep(5)
    ont_config_test_ont = "undefined"
    if_find = False
    for index in range(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOntConfig_TableOntPort").__len__()):
        ont_config_ont = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOntConfig_TableOntPort")[index].get_attribute("textContent")
        if(ont_config_ont.split("-")[0] == slot_x_1_aid and ont_config_ont.split("-")[1] == pon_x_1_aid ):
            if_find = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOntConfig_TableOntTemplate")[index].get_attribute("textContent") != "______________xpon_template_HGU"):
                print(f"             [XPON - ONT Config - Main] ONT {ont_config_ont} ONT Template:HGU Test Fail",file = open(file_name, '+a'))
                if_error = True
    if(if_find == False):
        print(f"             [XPON - ONT Config - Main] ONT {slot_x_1_aid}-{pon_x_1_aid} Check Not Found Test Fail",file = open(file_name, '+a'))
        if_error = True
    if_find = False
    for index in range(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOntConfig_TableSN").__len__()):
        if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOntConfig_TableSN")[index].get_attribute("textContent") == {ont_x_1_1_sn}):
            if_find = True
            ont_config_test_ont = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOntConfig_TableOntPort")[index].get_attribute("textContent")
            driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOntConfig_TableSN")[index].click()
            ontc.Main_Select_ONT_Template(driver,"______________xpon_template_SFU")
            ontc.Main_Select_Apply(driver)
    if(if_find == False):
        print(f"             [XPON - ONT Config - Main] SN {ont_x_1_1_sn} Not Found Edit Test Fail",file = open(file_name, '+a'))
        if_error = True
    else:
        if_find = False
        for index in range(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOntConfig_TableOntPort").__len__()):
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOntConfig_TableOntPort")[index].get_attribute("textContent") == ont_config_test_ont):
                if_find = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOntConfig_TableOntTemplate")[index].get_attribute("textContent") != "______________xpon_template_SFU"):
                    print(f"             [XPON - ONT Config - Main] ONT {ont_config_test_ont} ONT Template:SFU Test Fail",file = open(file_name, '+a'))
                    if_error = True
        if(if_find == False):
            print(f"             [XPON - ONT Config - Main] ONT {ont_config_test_ont} Check Not Found Test Fail",file = open(file_name, '+a'))
            if_error = True
          
    if(if_error == False):
        print(f"[MSAN1-12154][XPON - ONT Config - Main] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-12154][XPON - ONT Config - Main] Result Fail",file = open(file_name, '+a'))

    if(ont_config_test_ont != "undefined"):

        if_error = False
       
        driver.switch_to.default_content()
        driver.find_element(By.LINK_TEXT, "XPON").click()
        driver.find_element(By.LINK_TEXT, "ONT Config").click()
        time.sleep(5)
        driver.switch_to.frame(0)
        driver.find_element(By.LINK_TEXT, "QoS").click()
        time.sleep(5)
        if_find = False
        ontc.QoS_New(driver)
        try:
            ontc.QoS_New_ONT(driver,f"{ont_config_test_ont}")
            ontc.QoS_New_Tcont_Server(driver,"tcont8")
            ontc.QoS_New_US_Bandwidth_Profile(driver,"______________100M")
            ontc.QoS_New_DS_Bandwidth_Profile(driver,"______________100M")
            ontc.QoS_New_Apply(driver)
            ontc.QoS_New(driver)
            ontc.QoS_New_ONT(driver,f"{ont_config_test_ont}")
            ontc.QoS_New_Tcont_Server(driver,"service8")
            ontc.QoS_New_US_Bandwidth_Profile(driver,"______________100M")
            ontc.QoS_New_DS_Bandwidth_Profile(driver,"______________100M")
            ontc.QoS_New_Apply(driver)
            if_find == False
            for index in range(driver.find_elements(By.ID, "xgponOntQosLoadCfgTblList").__len__()):
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOntConfigQoSLoad_TableOntPort")[index].get_attribute("textContent") == f"{ont_config_test_ont}" and driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOntConfigQoSLoad_TableQosIdt")[index].get_attribute("textContent") == "tcont8"):
                    if_find = True
                    if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOntConfigQoSLoad_TableUsBwProfile")[index].get_attribute("textContent") != "______________100M"):
                        print(f"             [XPON - ONT Config - QoS] ONT {ont_config_test_ont} tcont8 US PW Profile Test Fail",file = open(file_name, '+a'))
                    if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOntConfigQoSLoad_TableDsBwProfile")[index].get_attribute("textContent") != "______________100M"):
                        print(f"             [XPON - ONT Config - QoS] ONT {ont_config_test_ont} tcont8 DS PW Profile Test Fail",file = open(file_name, '+a'))
            if(if_find == False):
                print(f"             [XPON - ONT Config - QoS] ONT {ont_config_test_ont} tcont8 Not Found Test Fail",file = open(file_name, '+a'))
            if_find == False
            for index in range(driver.find_elements(By.ID, "xgponOntQosLoadCfgTblList").__len__()):
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOntConfigQoSLoad_TableOntPort")[index].get_attribute("textContent") == f"{ont_config_test_ont}" and driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOntConfigQoSLoad_TableQosIdt")[index].get_attribute("textContent") == "service8"):
                    if_find = True
                    if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOntConfigQoSLoad_TableUsBwProfile")[index].get_attribute("textContent") != "______________100M"):
                        print(f"             [XPON - ONT Config - QoS] ONT {ont_config_test_ont} service8 US PW Profile Test Fail",file = open(file_name, '+a'))
                    if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOntConfigQoSLoad_TableDsBwProfile")[index].get_attribute("textContent") != "______________100M"):
                        print(f"             [XPON - ONT Config] ONT {ont_config_test_ont} service8 DS PW Profile Test Fail",file = open(file_name, '+a'))
            if(if_find == False):
                print(f"             [XPON - ONT Config - QoS] ONT {ont_config_test_ont} service8 Not Found Test Fail",file = open(file_name, '+a'))
        except:
            print(f"             [XPON - ONT Config - QoS] ONT {ont_config_test_ont} Not Found Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(if_error == False):
            print(f"[MSAN1-12155][XPON - ONT Config - QoS] Result Pass",file = open(file_name, '+a'))
        else:
            print(f"[MSAN1-12155][XPON - ONT Config - QoS] Result Fail",file = open(file_name, '+a'))

        if_error = False
            
        driver.switch_to.default_content()
        driver.find_element(By.LINK_TEXT, "XPON").click()
        driver.find_element(By.LINK_TEXT, "ONT Config").click()
        time.sleep(5)
        driver.switch_to.frame(0)
        driver.find_element(By.LINK_TEXT, "FDB").click()
        time.sleep(5)
        if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__() != 0):
            ontc.FDB_Delete_All_Select(driver,True)
            ontc.FDB_Delete(driver)
        if_ont_exist = True
        try:
            ontc.FDB_New(driver)
            ontc.FDB_New_ONT(driver,f"{ont_config_test_ont}")
            ontc.FDB_New_VLAN(driver,"4000")
            ontc.FDB_New_MAC(driver,f"10:10:10:10:10:01")
            ontc.FDB_New_Apply(driver)
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOntConfigFdb_TableOntPort")[index].get_attribute("textContent") != f"{ont_config_test_ont}"):
                print(f"             [XPON - ONT Config - FDB] ONT {ont_config_test_ont} Test Fail",file = open(file_name, '+a'))
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOntConfigFdb_TableVLAN")[index].get_attribute("textContent") != "4000"):
                print(f"             [XPON - ONT Config - FDB] VLAN 4000 Test Fail",file = open(file_name, '+a'))
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOntConfigFdb_TableMac")[index].get_attribute("textContent") != "10:10:10:10:10:01"):
                print(f"             [XPON - ONT Config - FDB] MAC 10:10:10:10:10:01 Test Fail",file = open(file_name, '+a'))
        except:
            print(f"             [XPON - ONT Config - FDB] ONT {ont_config_test_ont} Not Found Test Fail",file = open(file_name, '+a'))
            if_error = True
            if_ont_exist = False
        if(if_ont_exist == True):
            for mac in range(1025):
                mac = mac+1
                ontc.FDB_New(driver)
                ontc.FDB_New_ONT(driver,f"{ont_config_test_ont}")
                ontc.FDB_New_VLAN(driver,"4000")
                if(mac < 10):
                    ontc.FDB_New_MAC(driver,f"10:10:10:10:00:0{mac}")
                elif(mac < 100):
                    ontc.FDB_New_MAC(driver,f"10:10:10:10:00:{mac}")
                elif(mac < 110):
                    ontc.FDB_New_MAC(driver,f"10:10:10:10:01:0{mac-100}")
                elif(mac < 200):
                    ontc.FDB_New_MAC(driver,f"10:10:10:10:01:{mac-100}")
                elif(mac < 210):
                    ontc.FDB_New_MAC(driver,f"10:10:10:10:02:0{mac-200}")
                elif(mac < 300):
                    ontc.FDB_New_MAC(driver,f"10:10:10:10:02:{mac-200}")
                elif(mac < 310):
                    ontc.FDB_New_MAC(driver,f"10:10:10:10:03:0{mac-300}")
                elif(mac < 400):
                    ontc.FDB_New_MAC(driver,f"10:10:10:10:03:{mac-300}")
                elif(mac < 410):
                    ontc.FDB_New_MAC(driver,f"10:10:10:10:04:0{mac-400}")
                elif(mac < 500):
                    ontc.FDB_New_MAC(driver,f"10:10:10:10:04:{mac-400}")
                elif(mac < 510):
                    ontc.FDB_New_MAC(driver,f"10:10:10:10:05:0{mac-500}")
                elif(mac < 600):
                    ontc.FDB_New_MAC(driver,f"10:10:10:10:05:{mac-500}")
                elif(mac < 610):
                    ontc.FDB_New_MAC(driver,f"10:10:10:10:06:0{mac-600}")
                elif(mac < 700):
                    ontc.FDB_New_MAC(driver,f"10:10:10:10:06:{mac-600}")
                elif(mac < 710):
                    ontc.FDB_New_MAC(driver,f"10:10:10:10:07:0{mac-700}")
                elif(mac < 800):
                    ontc.FDB_New_MAC(driver,f"10:10:10:10:07:{mac-700}")
                elif(mac < 810):
                    ontc.FDB_New_MAC(driver,f"10:10:10:10:08:0{mac-800}")
                elif(mac < 900):
                    ontc.FDB_New_MAC(driver,f"10:10:10:10:08:{mac-800}")
                elif(mac < 910):
                    ontc.FDB_New_MAC(driver,f"10:10:10:10:09:0{mac-900}")
                elif(mac < 1000):
                    ontc.FDB_New_MAC(driver,f"10:10:10:10:09:{mac-900}")
                elif(mac < 1010):
                    ontc.FDB_New_MAC(driver,f"10:10:10:10:10:0{mac-1000}")
                elif(mac < 1025):
                    ontc.FDB_New_MAC(driver,f"10:10:10:10:10:{mac-1000}")
                else:
                    ontc.FDB_New_MAC(driver,f"10:10:10:10:10:{mac-1000}")
                ontc.FDB_New_Apply(driver)
                if(mac == 1025):
                    try:
                        driver.find_element(By.NAME, "rperror_btnBack").click()
                    except:
                        print(f"             [XPON - ONT Config - FDB] 1025 Apply Full No Alert Test Fail",file = open(file_name, '+a'))
            max_cap = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__()
            print(f"             [XPON - ONT Config - FDB] Max Capacity(1024) = {max_cap}",file = open(file_name, '+a'))
            
        if(if_error == False):
            print(f"[MSAN1-12156][XPON - ONT Config - FDB] Result Pass",file = open(file_name, '+a'))
        else:
            print(f"[MSAN1-12156][XPON - ONT Config - FDB] Result Fail",file = open(file_name, '+a'))

        ### Delete
        ontc.FDB_Delete_All_Select(driver,True)
        ontc.FDB_Delete(driver)
            
        driver.switch_to.default_content()
        driver.find_element(By.LINK_TEXT, "XPON").click()
        driver.find_element(By.LINK_TEXT, "ONT Config").click()
        time.sleep(5)
        driver.switch_to.frame(0)
        driver.find_element(By.LINK_TEXT, "QoS").click()
        time.sleep(5)
        ontc.QoS_Delete_All_Select(driver,True)
        ontc.QoS_Delete(driver)
            
        driver.switch_to.default_content()
        driver.find_element(By.LINK_TEXT, "XPON").click()
        driver.find_element(By.LINK_TEXT, "ONT Config").click()
        time.sleep(5)
        driver.switch_to.frame(0)
        driver.find_element(By.LINK_TEXT, "Main").click()
        time.sleep(5)
        ontc.Main_Delete_Select_All(driver,True)
        ontc.Main_Delete(driver)

    else:
        print(f"             [XPON - ONT Config - QoS] Main SN {ont_x_1_1_sn} Not Found Test Fail",file = open(file_name, '+a'))
        print(f"[MSAN1-12155][XPON - ONT Config - QoS] Result Pass",file = open(file_name, '+a'))
        print(f"             [XPON - ONT Config - FDB] Main SN {ont_x_1_1_sn} Not Found Test Fail",file = open(file_name, '+a'))
        print(f"[MSAN1-12156][XPON - ONT Config - FDB] Result Fail",file = open(file_name, '+a'))

    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "OLT Config").click()
    time.sleep(5)
    driver.switch_to.frame(0)
    if_find = False
    for index in range(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOltConfig_TableOltPort").__len__()):
        if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOltConfig_TableOltPort")[index].get_attribute("textContent") == f"{slot_x_1_aid}-{pon_x_1_aid}"):
            if_find = True
            driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOltConfig_TableOltPort")[index].click()
            oltc.Active(driver,False)
            oltc.Name(driver,"")
            oltc.Tel(driver,"")
            oltc.Register_Method(driver,"A")
            oltc.Ranging_distance(driver,"20")
            oltc.ONT_Template(driver," ")
            oltc.Apply(driver)
            time.sleep(5)
            break
    if(if_find == False):
        print(f"             [XPON - OLT Config] Delete Not Found",file = open(file_name, '+a'))

    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def ONT_brief_Test(driver,slot_x_1_aid,pon_x_1_aid,file_name):
    print(f"XPON ONT brief Test\nTest Start",file = open(file_name, '+a'))
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "OLT Config").click()
    time.sleep(5)
    driver.switch_to.frame(0)
    if_find = False
    for index in range(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOltConfig_TableOltPort").__len__()):
        if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOltConfig_TableOltPort")[index].get_attribute("textContent") == f"{slot_x_1_aid}-{pon_x_1_aid}"):
            if_find = True
            driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXgponOltConfig_TableOltPort")[index].click()
            oltc.Active(driver,True)
            oltc.Register_Method(driver,"A")
            oltc.Ranging_distance(driver,"20")
            oltc.Apply(driver)
            time.sleep(5)
            break
    if(if_find == False):
        print(f"             [XPON - OLT Config] Not Found xpon port",file = open(file_name, '+a'))
    time.sleep(60)
    
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "ONT brief").click()
    driver.switch_to.frame(0)
    if_find = False
    for index in range(driver.find_elements(By.NAME, "rpOntBrief_aidStr").__len__()):
        if(driver.find_elements(By.NAME, "rpOntBrief_aidStr")[index].get_attribute("textContent") == f"{slot_x_1_aid}-{pon_x_1_aid}-1"):
            if_find = True
            ONT_brief_ONT_Status = driver.find_elements(By.NAME, f"rpOntBrief_mainStatStr")[index].get_attribute("textContent")
            print(f"             [XPON - ONT Brief] Status: {ONT_brief_ONT_Status}",file = open(file_name, '+a')) 
            break
    if(if_find == False):
        print(f"             [XPON - ONT Brief] Port {slot_x_1_aid}-{pon_x_1_aid}-1 Not Found Test Fail",file = open(file_name, '+a')) 
        print("[MSAN1-12146][XPON - ONT Brief] Result Fail",file = open(file_name, '+a'))
    else:
        print("[MSAN1-12146][XPON - ONT Brief] Result Pass",file = open(file_name, '+a'))
    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def ONT_Status_Test(driver,slot_x_1_aid,pon_x_1_aid,ont_x_1_1_sn,file_name):
    print(f"XPON ONT Status Test\nTest Start",file = open(file_name, '+a'))
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "ONT Status").click()
    driver.switch_to.frame(0)
    olts.ONT_Select_1(driver,slot_x_1_aid,pon_x_1_aid)
    olts.Refresh(driver)
    if_error = False
    if(driver.find_element(By.CLASS_NAME, "xgspon-table-td-content.rpXgponOntStatus_SN").get_attribute("textContent") == ont_x_1_1_sn):
        print("             [XPON - ONT Status] SN match, Pass",file = open(file_name, '+a'))
    else:
        print("             [XPON - ONT Status] SN not match, Fail",file = open(file_name, '+a'))
        if_error = True

    if(driver.find_element(By.CLASS_NAME, "xgspon-table-td-content.rpXgponOntStatus_linkStatus").get_attribute("textContent") == "IS"):
        print("             [XPON - ONT Status] Status: IS",file = open(file_name, '+a'))
    else:
        ont_status_Status = driver.find_element(By.CLASS_NAME, "xgspon-table-td-content.rpXgponOntStatus_linkStatus").get_attribute("textContent")
        print(f"             [XPON - ONT Status] Status: {ont_status_Status}",file = open(file_name, '+a'))
    

    

    if(if_error == True):
        print("[MSAN1-12148][XPON - ONT Status] Result Fail",file = open(file_name, '+a'))
    else:
        print("[MSAN1-12148][XPON - ONT Status] Result Pass",file = open(file_name, '+a'))
    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))


# =======================================================================================
# Xpon profile max capacity test

def Template_Max_Test(driver,file_name):
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Template").click()
    profile_name = 0
    if_full = False
    while(if_full == False):
        profile_name = profile_name+1
        pro.Template_New(driver)
        pro.Template_New_Name(driver,1234567890123456789012345670000+profile_name)
        pro.Template_New_Apply(driver)
        try:
            driver.find_element(By.NAME, "rperror_btnBack").click()
            if_full = True
        except:
            pass
    print(f"[MSAN1-12279][XPON - Profiles - Template] Max Capacity({template_capacity}) = {profile_name-1}",file = open(file_name, '+a'))
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "Config Save").click()
    driver.switch_to.frame(0)
    driver.find_element(By.NAME, "rpConfigSave").click()

def Service_Profile_Max_Test(driver,file_name):
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Service").click()
    profile_name = 0
    if_full = False
    while(if_full == False):
        profile_name = profile_name+1
        pro.Service_Profile_New(driver)
        pro.Service_Profile_New_Name(driver,1234567890123456789012345670000+profile_name)
        pro.Service_Profile_New_VLAN(driver,"4094")
        pro.Service_Profile_New_Apply(driver)
        try:
            driver.find_element(By.NAME, "rperror_btnBack").click()
            if_full = True
        except:
            pass
    print(f"[MSAN1-12280][XPON - Profiles - Service Profile] Max Capacity({service_profile_capacity}) = {profile_name-1}",file = open(file_name, '+a'))
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "Config Save").click()
    driver.switch_to.frame(0)
    driver.find_element(By.NAME, "rpConfigSave").click()

def QoS_Bandwidth_Profile_Max_Test(driver,file_name):
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "QoS Bandwidth").click()
    profile_name = 0
    if_full = False
    while(if_full == False):
        profile_name = profile_name+1
        pro.QoS_Bandwidth_Profile_New(driver)
        pro.QoS_Bandwidth_Profile_New_Name(driver,12345678901230000+profile_name)
        pro.QoS_Bandwidth_Profile_New_Apply(driver)
        try:
            driver.find_element(By.NAME, "rperror_btnBack").click()
            if_full = True
        except:
            pass
    print(f"[MSAN1-12281][XPON - Profiles - QoS Bandwidth Profile] Max Capacity({qos_bandwidth_profile_capacity}) = {profile_name-1}",file = open(file_name, '+a'))
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "Config Save").click()
    driver.switch_to.frame(0)
    driver.find_element(By.NAME, "rpConfigSave").click()

def Multicast_Profile_Max_Test(driver,file_name):
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "Multicast").click()
    driver.find_element(By.LINK_TEXT, "IGMP Privilege Profile").click()
    driver.switch_to.frame(0)
    mul.IGMP_Privilege_Profile_Name(driver,f"1234567890123456789012345678901")
    mul.IGMP_Privilege_Profile_Bandwidth(driver,"100")
    mul.IGMP_Privilege_Profile_Start_Address(driver,f"224.0.0.0")
    mul.IGMP_Privilege_Profile_End_Address(driver,f"239.255.255.255")
    mul.IGMP_Privilege_Profile_Privilege(driver,3)
    mul.IGMP_Privilege_Profile_Length(driver,"300")
    mul.IGMP_Privilege_Profile_Interval(driver,"300")
    mul.IGMP_Privilege_Profile_Count(driver,"10")
    mul.IGMP_Privilege_Profile_Reset(driver,"86400")
    mul.IGMP_Privilege_Profile_Apply_New(driver)
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Multicast").click()
    mul_pro_name = 0
    if_full = False
    while(if_full == False):
        mul_pro_name = mul_pro_name+1
        pro.Multicast_Profile_New(driver)
        pro.Multicast_Profile_New_Name(driver,1234567890123456789012345670000+mul_pro_name)
        pro.Multicast_Profile_New_Apply(driver)
        try:
            driver.find_element(By.NAME, "rperror_btnBack").click()
            if_full = True
        except:
            pass
    print(f"[MSAN1-12282][XPON - Profiles - Multicast Profile] Max Capacity({multicast_profile_capacity}) = {mul_pro_name-1}",file = open(file_name, '+a'))
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "Config Save").click()
    driver.switch_to.frame(0)
    driver.find_element(By.NAME, "rpConfigSave").click()

def Uni_Profile_Max_Test(driver,file_name):
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "UNI").click()
    profile_name = 0
    if_full = False
    while(if_full == False):
        profile_name = profile_name+1
        pro.Uni_Profile_New(driver)
        pro.Uni_Profile_New_Name(driver,1234567890123456789012345670000+profile_name)
        pro.Uni_Profile_New_Lan_Vlan_Active(driver,7,True)
        pro.Uni_Profile_New_Apply(driver)
        try:
            driver.find_element(By.NAME, "rperror_btnBack").click()
            if_full = True
        except:
            pass
    print(f"[MSAN1-12283][XPON - Profiles - UNI Profile] Max Capacity({uni_profile_capacity}) = {profile_name-1}",file = open(file_name, '+a'))
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "Config Save").click()
    driver.switch_to.frame(0)
    driver.find_element(By.NAME, "rpConfigSave").click()

def Security_Profile_Max_Test(driver,file_name):
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Security").click()
    profile_name = 0
    if_full = False
    while(if_full == False):
        profile_name = profile_name+1
        pro.Security_Profile_New(driver)
        pro.Security_Profile_New_Name(driver,1234567890123456789012345670000+profile_name)
        pro.Security_Profile_New_Apply(driver)
        try:
            driver.find_element(By.NAME, "rperror_btnBack").click()
            if_full = True
        except:
            pass
    print(f"[MSAN1-12284][XPON - Profiles - Security Profile] Max Capacity({security_profile_capacity}) = {profile_name-1}",file = open(file_name, '+a'))
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "Config Save").click()
    driver.switch_to.frame(0)
    driver.find_element(By.NAME, "rpConfigSave").click()

def Ont_Profile_Max_Test(driver,file_name):
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "ONT").click()
    profile_name = 0
    if_full = False
    while(if_full == False):
        profile_name = profile_name+1
        pro.Ont_Profile_New(driver)
        pro.Ont_Profile_New_Name(driver,1234567890123456789012345670000+profile_name)
        pro.Ont_Profile_New_Apply(driver)
        try:
            driver.find_element(By.NAME, "rperror_btnBack").click()
            if_full = True
        except:
            pass
    print(f"[MSAN1-12285][XPON - Profiles - Ont Profile] Max Capacity({ont_profile_capacity}) = {profile_name-1}",file = open(file_name, '+a'))
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "Config Save").click()
    driver.switch_to.frame(0)
    driver.find_element(By.NAME, "rpConfigSave").click()

def Sip_Profile_Max_Test(driver,file_name):
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Voip Sip").click()
    time.sleep(5)
    profile_name = 0
    if_full = False
    while(if_full == False):
        profile_name = profile_name+1
        pro.Sip_Profile_New(driver)
        pro.Sip_Profile_New_Name(driver,123456789012000+profile_name)
        pro.Sip_Profile_New_Apply(driver)
        try:
            driver.find_element(By.NAME, "rperror_btnBack").click()
            if_full = True
        except:
            pass
    print(f"[MSAN1-12286][XPON - Profiles - Sip Profile] Max Capacity({sip_profile_capacity}) = {profile_name-1}",file = open(file_name, '+a'))
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "Config Save").click()
    driver.switch_to.frame(0)
    driver.find_element(By.NAME, "rpConfigSave").click()

def Voip_Common_Profile_Max_Test(driver,file_name):
    if_error = False
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Voip Common").click()
    time.sleep(5)
    profile_name = 0
    if_full = False
    while(if_full == False):
        profile_name = profile_name+1
        pro.Voip_Common_Profile_New(driver)
        pro.Voip_Common_Profile_New_Name(driver,123456789012000+profile_name)
        pro.Voip_Common_Profile_New_Apply(driver)
        try:
            driver.find_element(By.NAME, "rperror_btnBack").click()
            if_full = True
        except:
            pass
    print(f"[MSAN1-12287][XPON - Profiles - Voip Common Profile] Max Capacity({voip_common_profile_capacity}) = {profile_name-1}",file = open(file_name, '+a'))
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "Config Save").click()
    driver.switch_to.frame(0)
    driver.find_element(By.NAME, "rpConfigSave").click()

def Dial_Plan_Profile_Max_Test(driver,file_name):
    if_error = False
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Voip Dial Plan").click()
    time.sleep(5)
    profile_name = 0
    if_full = False
    while(if_full == False):
        profile_name = profile_name+1
        pro.Dial_Plan_Profile_New(driver)
        pro.Dial_Plan_Profile_New_Name(driver,123456789012000+profile_name)
        pro.Dial_Plan_Profile_New_Apply(driver)
        try:
            driver.find_element(By.NAME, "rperror_btnBack").click()
            if_full = True
        except:
            pass
    print(f"[MSAN1-12288][XPON - Profiles - Dial Plan Profile] Max Capacity({dial_plan_profile_capacity}) = {profile_name-1}",file = open(file_name, '+a'))
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "Config Save").click()
    driver.switch_to.frame(0)
    driver.find_element(By.NAME, "rpConfigSave").click()

def ACL_Profile_Max_Test(driver,file_name):
    if_error = False
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "ACL").click()
    time.sleep(5)
    profile_name = 0
    if_full = False
    while(if_full == False):
        profile_name = profile_name+1
        pro.ACL_Profile_New(driver)
        pro.ACL_Profile_New_Name(driver,123456789012000+profile_name)
        pro.ACL_Profile_New_Apply(driver)
        try:
            driver.find_element(By.NAME, "rperror_btnBack").click()
            if_full = True
        except:
            pass
    max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__()
    print(f"[MSAN1-00000][XPON - Profiles - ACL Profile] Max Capacity({ACL_profile_capacity}) = {max_count}",file = open(file_name, '+a'))
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "Config Save").click()
    driver.switch_to.frame(0)
    driver.find_element(By.NAME, "rpConfigSave").click()

# Xpon profile max capacity test
# =======================================================================================

# =======================================================================================
# Xpon profile delete all
#OK

def ONT_Config_Main_Delete(driver,file_name):
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "ONT Config").click()
    time.sleep(5)
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Main").click()
    time.sleep(5)
    ontc.Main_Delete_Select_All(driver,True)
    ontc.Main_Delete(driver)

def Template_Delete(driver,file_name):
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Template").click()
    pro.Template_Delete_All_Select(driver,True)
    pro.Template_Delete(driver)
    max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__()
    if(max_count == 0):
        print(f"             [XPON - Profiles - Template] Delete Pass. Entry = {max_count}",file = open(file_name, '+a'))
        print(f"[MSAN1-12157][XPON - Profiles - Template] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [XPON - Profiles - Template] Delete Fail. Entry = {max_count}",file = open(file_name, '+a'))
        print(f"[MSAN1-12157][XPON - Profiles - Template] Result Fail",file = open(file_name, '+a'))
   
def Service_Profile_Delete(driver,file_name):
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Service").click()
    pro.Service_Profile_Delete_All_Select(driver,True)
    pro.Service_Profile_Delete(driver)
    max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__()
    if(max_count == 0):
        print(f"             [XPON - Profiles - Service Profile] Delete Pass. Entry = {max_count}",file = open(file_name, '+a'))
        print(f"[MSAN1-12158][XPON - Profiles - Service Profile] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [XPON - Profiles - Service Profile] Delete Fail. Entry = {max_count}",file = open(file_name, '+a'))
        print(f"[MSAN1-12158][XPON - Profiles - Service Profile] Result Fail",file = open(file_name, '+a'))

def QoS_Bandwidth_Profile_Delete(driver,file_name):
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "QoS Bandwidth").click()
    pro.QoS_Bandwidth_Profile_Delete_All_Select(driver,True)
    pro.QoS_Bandwidth_Profile_Delete(driver)
    max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__()
    if(max_count == 0):
        print(f"             [XPON - Profiles - QoS Bandwidth Profile] Delete Pass. Entry = {max_count}",file = open(file_name, '+a'))
        print(f"[MSAN1-12159][XPON - Profiles - QoS Bandwidth Profile] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [XPON - Profiles - QoS Bandwidth Profile] Delete Fail. Entry = {max_count}",file = open(file_name, '+a'))
        print(f"[MSAN1-12159][XPON - Profiles - QoS Bandwidth Profile] Result Fail",file = open(file_name, '+a'))

def Multicast_Profile_Delete(driver,file_name):
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Multicast").click()
    pro.Multicast_Profile_Delete_All_Select(driver,True)
    pro.Multicast_Profile_Delete(driver)
    max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__()
    if(max_count == 0):
        print(f"             [XPON - Profiles - Multicast Profile] Delete Pass. Entry = {max_count}",file = open(file_name, '+a'))
        print(f"[MSAN1-12160][XPON - Profiles - Multicast Profile] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [XPON - Profiles - Multicast Profile] Delete Fail. Entry = {max_count}",file = open(file_name, '+a'))
        print(f"[MSAN1-12160][XPON - Profiles - Multicast Profile] Result Fail",file = open(file_name, '+a'))

def Uni_Profile_Delete(driver,file_name):
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "UNI").click()
    pro.Uni_Profile_Delete_All_Select(driver,True)
    pro.Uni_Profile_Delete(driver)   
    max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__()
    if(max_count == 0):
        print(f"             [XPON - Profiles - UNI Profile] Delete Pass. Entry = {max_count}",file = open(file_name, '+a'))
        print(f"[MSAN1-12161][XPON - Profiles - UNI Profile] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [XPON - Profiles - UNI Profile] Delete Fail. Entry = {max_count}",file = open(file_name, '+a'))
        print(f"[MSAN1-12161][XPON - Profiles - UNI Profile] Result Fail",file = open(file_name, '+a'))

def Security_Profile_Delete(driver,file_name):
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Security").click()
    pro.Security_Profile_Delete_All_Select(driver,True)
    pro.Security_Profile_Delete(driver)
    max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__()
    if(max_count == 0):
        print(f"             [XPON - Profiles - Security Profile] Delete Pass. Entry = {max_count}",file = open(file_name, '+a'))
        print(f"[MSAN1-12162][XPON - Profiles - Security Profile] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [XPON - Profiles - Security Profile] Delete Fail. Entry = {max_count}",file = open(file_name, '+a'))
        print(f"[MSAN1-12162][XPON - Profiles - Security Profile] Result Fail",file = open(file_name, '+a'))

def Ont_Profile_Delete(driver,file_name):
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "ONT").click()
    pro.Ont_Profile_Delete_All_Select(driver,True)
    pro.Ont_Profile_Delete(driver) 
    max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__()
    if(max_count == 0):
        print(f"             [XPON - Profiles - Ont Profile] Delete Pass. Entry = {max_count}",file = open(file_name, '+a'))
        print(f"[MSAN1-12163][XPON - Profiles - Ont Profile] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [XPON - Profiles - Ont Profile] Delete Fail. Entry = {max_count}",file = open(file_name, '+a'))
        print(f"[MSAN1-12163][XPON - Profiles - Ont Profile] Result Fail",file = open(file_name, '+a'))

def Sip_Profile_Delete(driver,file_name):
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Voip Sip").click()
    pro.Sip_Profile_Delete_All_Select(driver,True)
    pro.Sip_Profile_Delete(driver) 
    max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__()
    if(max_count == 0):
        print(f"             [XPON - Profiles - Sip Profile] Delete Pass. Entry = {max_count}",file = open(file_name, '+a'))
        print(f"[MSAN1-12164][XPON - Profiles - Sip Profile] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [XPON - Profiles - Sip Profile] Delete Fail. Entry = {max_count}",file = open(file_name, '+a'))
        print(f"[MSAN1-12164][XPON - Profiles - Sip Profile] Result Fail",file = open(file_name, '+a'))

def Voip_Common_Profile_Delete(driver,file_name):
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Voip Common").click()
    pro.Voip_Common_Profile_Delete_All_Select(driver,True)
    pro.Voip_Common_Profile_Delete(driver) 
    max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__()
    if(max_count == 0):
        print(f"             [XPON - Profiles - Voip Common Profile] Delete Pass. Entry = {max_count}",file = open(file_name, '+a'))
        print(f"[MSAN1-12165][XPON - Profiles - Voip Common Profile] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [XPON - Profiles - Voip Common Profile] Delete Fail. Entry = {max_count}",file = open(file_name, '+a'))
        print(f"[MSAN1-12165][XPON - Profiles - Voip Common Profile] Result Fail",file = open(file_name, '+a'))

def Dial_Plan_Profile_Delete(driver,file_name):
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Voip Dial Plan").click()
    pro.Dial_Plan_Profile_Delete_All_Select(driver,True)
    pro.Dial_Plan_Profile_Delete(driver) 
    max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__()
    if(max_count == 0):
        print(f"             [XPON - Profiles - Dial Plan Profile] Delete Pass. Entry = {max_count}",file = open(file_name, '+a'))
        print(f"[MSAN1-12166][XPON - Profiles - Dial Plan Profile] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [XPON - Profiles - Dial Plan Profile] Delete Fail. Entry = {max_count}",file = open(file_name, '+a'))
        print(f"[MSAN1-12166][XPON - Profiles - Dial Plan Profile] Result Fail",file = open(file_name, '+a'))

def ACL_Profile_Delete(driver,file_name):
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "ACL").click()
    pro.ACL_Profile_Delete_All_Select(driver,True)
    pro.ACL_Profile_Delete(driver) 
    max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__()
    if(max_count == 0):
        print(f"            [XPON - Profiles - ACL Profile] Delete Pass. Entry = {max_count}",file = open(file_name, '+a'))
        print(f"[MSAN1-00000[XPON - Profiles - ACL Profile] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [XPON - Profiles - ACL Profile] Delete Fail. Entry = {max_count}",file = open(file_name, '+a'))
        print(f"[MSAN1-00000][XPON - Profiles - ACL Profile] Result Fail(#175875)",file = open(file_name, '+a'))

# Xpon profile delete all
# =======================================================================================

# =======================================================================================
# Xpon profile count test

def Template_Count_Test(driver,file_name):
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Template").click()
    pro.Template_New(driver)
    pro.Template_New_Name(driver,"ifmaxtest")
    pro.Template_New_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
        time.sleep(2)
        # max = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1")[-1].get_attribute("textContent")
        max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__()
        if(max_count == template_capacity):  #Template_Profile_MaxTable
            print(f"[MSAN1-12279][XPON - Profiles - Template] Max Table Pass({template_capacity}) = {max_count}",file = open(file_name, '+a'))
        else:
            print(f"[MSAN1-12279][XPON - Profiles - Template] Max Table Fail({template_capacity}) = {max_count}",file = open(file_name, '+a'))
    except:
        max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__()
        print(f"             [XPON - Profiles - Template] Max Table Not full = {max_count}-1 = {max_count-1}",file = open(file_name, '+a'))
        print(f"[MSAN1-12279][XPON - Profiles - Template] Max Table Fail({template_capacity}) = {max_count}",file = open(file_name, '+a'))

def Service_Profile_Count_Test(driver,file_name):
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Service").click()
    pro.Service_Profile_New(driver)
    pro.Service_Profile_New_Name(driver,"ifmaxtest")
    pro.Service_Profile_New_VLAN(driver,"4094")
    pro.Service_Profile_New_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
        time.sleep(2)
        # max = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1")[-1].get_attribute("textContent")
        max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__()
        if(max_count == service_profile_capacity):  #Service_Profile_MaxTable
            print(f"[MSAN1-12280][XPON - Profiles - Service Profile] Max Table Pass({service_profile_capacity}) = {max_count}",file = open(file_name, '+a'))
        else:
            print(f"[MSAN1-12280][XPON - Profiles - Service Profile] Max Table Fail({service_profile_capacity}) = {max_count}",file = open(file_name, '+a'))
    except:
        max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__()
        print(f"             [XPON - Profiles - Service Profile] Max Table Not full = {max_count}-1 = {max_count-1}",file = open(file_name, '+a'))
        print(f"[MSAN1-12280][XPON - Profiles - Service Profile] Max Table Fail({service_profile_capacity}) = {max_count}",file = open(file_name, '+a'))

def QoS_Bandwidth_Profile_Count_Test(driver,file_name):
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "QoS Bandwidth").click()
    pro.QoS_Bandwidth_Profile_New(driver)
    pro.QoS_Bandwidth_Profile_New_Name(driver,"ifmaxtest")
    pro.QoS_Bandwidth_Profile_New_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
        time.sleep(2)
        # max = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1")[-1].get_attribute("textContent")
        max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__()
        if(max_count == qos_bandwidth_profile_capacity):  #QoS_Bandwidth_Profile_MaxTable
            print(f"[MSAN1-12281][XPON - Profiles - QoS Bandwidth Profile] Max Table Pass({qos_bandwidth_profile_capacity}) = {max_count}",file = open(file_name, '+a'))
        else:
            print(f"[MSAN1-12281][XPON - Profiles - QoS Bandwidth Profile] Max Table Fail({qos_bandwidth_profile_capacity}) = {max_count}",file = open(file_name, '+a'))
    except:
        max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__()
        print(f"             [XPON - Profiles - QoS Bandwidth Profile] Max Table Not full = {max_count}-1 = {max_count-1}",file = open(file_name, '+a'))
        print(f"[MSAN1-12281][XPON - Profiles - QoS Bandwidth Profile] Max Table Fail({qos_bandwidth_profile_capacity}) = {max_count}",file = open(file_name, '+a'))

def Multicast_Profile_Count_Test(driver,file_name):
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Multicast").click()
    pro.Multicast_Profile_New(driver)
    pro.Multicast_Profile_New_Name(driver,"ifmaxtest")
    pro.Multicast_Profile_New_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
        time.sleep(2)
        # max = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1")[-1].get_attribute("textContent")
        max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__()
        if(max_count == multicast_profile_capacity):  #Multicast_Profile_MaxTable
            print(f"[MSAN1-12282][XPON - Profiles - Multicast Profile] Max Table Pass({multicast_profile_capacity}) = {max_count}",file = open(file_name, '+a'))
        else:
            print(f"[MSAN1-12282][XPON - Profiles - Multicast Profile] Max Table Fail({multicast_profile_capacity}) = {max_count}",file = open(file_name, '+a'))
    except:
        max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__()
        print(f"             [XPON - Profiles - Multicast Profile] Max Table Not full = {max_count}-1 = {max_count-1}",file = open(file_name, '+a'))
        print(f"[MSAN1-12282][XPON - Profiles - Multicast Profile] Max Table Fail({multicast_profile_capacity}) = {max_count}",file = open(file_name, '+a'))

def Uni_Profile_Count_Test(driver,file_name):
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "UNI").click()
    pro.Uni_Profile_New(driver)
    pro.Uni_Profile_New_Name(driver,"ifmaxtest")
    pro.Uni_Profile_New_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
        time.sleep(5)
        # max = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.i1")[-1].get_attribute("textContent")
        max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.i1").__len__()
        if(max_count == uni_profile_capacity):  #UNI_Profile_MaxTable
            print(f"[MSAN1-12283][XPON - Profiles - UNI Profile] Max Table Pass({uni_profile_capacity}) = {max_count}",file = open(file_name, '+a'))
        else:
            print(f"[MSAN1-12283][XPON - Profiles - UNI Profile] Max Table Fail({uni_profile_capacity}) = {max_count}",file = open(file_name, '+a'))
    except:
        max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.i1").__len__()
        print(f"             [XPON - Profiles - UNI Profile] Max Table Not full = {max_count}-1 = {max_count-1}",file = open(file_name, '+a'))
        print(f"[MSAN1-12283][XPON - Profiles - UNI Profile] Max Table Fail({uni_profile_capacity}) = {max_count}",file = open(file_name, '+a'))

def Security_Profile_Count_Test(driver,file_name):
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Security").click()
    pro.Security_Profile_New(driver)
    pro.Security_Profile_New_Name(driver,"ifmaxtest")
    pro.Security_Profile_New_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
        time.sleep(2)
        # max = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1")[-1].get_attribute("textContent")
        max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__()
        if(max_count == security_profile_capacity):  #Security_Profile_MaxTable
            print(f"[MSAN1-12284][XPON - Profiles - Security Profile] Max Table Pass({security_profile_capacity}) = {max_count}",file = open(file_name, '+a'))
        else:
            print(f"[MSAN1-12284][XPON - Profiles - Security Profile] Max Table Fail({security_profile_capacity}) = {max_count}",file = open(file_name, '+a'))
    except:
        max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__()
        print(f"             [XPON - Profiles - Security Profile] Max Table Not full = {max_count}-1 = {max_count-1}",file = open(file_name, '+a'))
        print(f"[MSAN1-12284][XPON - Profiles - Security Profile] Max Table Fail({security_profile_capacity}) = {max_count}",file = open(file_name, '+a'))

def Ont_Profile_Count_Test(driver,file_name):
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "ONT").click()
    pro.Ont_Profile_New(driver)
    pro.Ont_Profile_New_Name(driver,"ifmaxtest")
    pro.Ont_Profile_New_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
        time.sleep(2)
        # max = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1")[-1].get_attribute("textContent")
        max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__()
        if(max_count == ont_profile_capacity):  #Ont_Profile_MaxTable
            print(f"[MSAN1-12285][XPON - Profiles - Ont Profile] Max Table Pass({ont_profile_capacity}) = {max_count}",file = open(file_name, '+a'))
        else:
            print(f"[MSAN1-12285][XPON - Profiles - Ont Profile] Max Table Fail({ont_profile_capacity}) = {max_count}",file = open(file_name, '+a'))
    except:
        max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__()
        print(f"             [XPON - Profiles - Ont Profile] Max Table Not full = {max_count}-1 = {max_count-1}",file = open(file_name, '+a'))
        print(f"[MSAN1-12285][XPON - Profiles - Ont Profile] Max Table Fail({ont_profile_capacity}) = {max_count}",file = open(file_name, '+a'))

def Sip_Profile_Count_Test(driver,file_name):
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Voip Sip").click()
    pro.Sip_Profile_New(driver)
    pro.Sip_Profile_New_Name(driver,"ifmaxtest")
    pro.Sip_Profile_New_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
        time.sleep(2)
        # max = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1")[-1].get_attribute("textContent")
        max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__()
        if(max_count == sip_profile_capacity):  #Sip_Profile_MaxTable
            print(f"[MSAN1-12286][XPON - Profiles - Sip Profile] Max Table Pass({sip_profile_capacity}) = {max_count}",file = open(file_name, '+a'))
        else:
            print(f"[MSAN1-12286][XPON - Profiles - Sip Profile] Max Table Fail({sip_profile_capacity}) = {max_count}",file = open(file_name, '+a'))
    except:
        max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__()
        print(f"             [XPON - Profiles - Sip Profile] Max Table Not full = {max_count}-1 = {max_count-1}",file = open(file_name, '+a'))
        print(f"[MSAN1-12286][XPON - Profiles - Sip Profile] Max Table Fail({sip_profile_capacity}) = {max_count}",file = open(file_name, '+a'))

def Voip_Common_Profile_Count_Test(driver,file_name):
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Voip Common").click()
    pro.Voip_Common_Profile_New(driver)
    pro.Voip_Common_Profile_New_Name(driver,"ifmaxtest")
    pro.Voip_Common_Profile_New_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
        time.sleep(2)
        # max = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1")[-1].get_attribute("textContent")
        max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__()
        if(max_count == voip_common_profile_capacity):  #Voip_Common_Profile_MaxTable
            print(f"[MSAN1-12287][XPON - Profiles - Voip Common Profile] Max Table Pass({voip_common_profile_capacity}) = {max_count}",file = open(file_name, '+a'))
        else:
            print(f"[MSAN1-12287][XPON - Profiles - Voip Common Profile] Max Table Fail({voip_common_profile_capacity}) = {max_count}",file = open(file_name, '+a'))
    except:
        max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__()
        print(f"             [XPON - Profiles - Voip Common Profile] Max Table Not full = {max_count}-1 = {max_count-1}",file = open(file_name, '+a'))
        print(f"[MSAN1-12287][XPON - Profiles - Voip Common Profile] Max Table Fail({voip_common_profile_capacity}) = {max_count}",file = open(file_name, '+a'))

def Dial_Plan_Profile_Count_Test(driver,file_name):
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Voip Dial Plan").click()
    pro.Dial_Plan_Profile_New(driver)
    pro.Dial_Plan_Profile_New_Name(driver,"ifmaxtest")
    pro.Dial_Plan_Profile_New_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
        time.sleep(2)
        # max = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1")[-1].get_attribute("textContent")
        max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__()
        if(max_count == dial_plan_profile_capacity):  #Dial_Plan_Profile_MaxTable
            print(f"[MSAN1-12288][XPON - Profiles - Dial Plan Profile] Max Table Pass({dial_plan_profile_capacity}) = {max_count}",file = open(file_name, '+a'))
        else:
            print(f"[MSAN1-12288][XPON - Profiles - Dial Plan Profile] Max Table Fail({dial_plan_profile_capacity}) = {max_count}",file = open(file_name, '+a'))
    except:
        max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__()
        print(f"             [XPON - Profiles - Dial Plan Profile] Max Table Not full = {max_count}-1 = {max_count-1}",file = open(file_name, '+a'))
        print(f"[MSAN1-12288][XPON - Profiles - Dial Plan Profile] Max Table Fail({dial_plan_profile_capacity}) = {max_count}",file = open(file_name, '+a'))

def ACL_Profile_Count_Test(driver,file_name):
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "ACL").click()
    pro.ACL_Profile_New(driver)
    pro.ACL_Profile_New_Name(driver,"ifmaxtest")
    pro.ACL_Profile_New_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
        time.sleep(2)
        # max = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1")[-1].get_attribute("textContent")
        max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__()
        if(max_count == ACL_profile_capacity):  #Dial_Plan_Profile_MaxTable
            print(f"[MSAN1-00000][XPON - Profiles - ACL Profile] Max Table Pass({ACL_profile_capacity}) = {max_count}",file = open(file_name, '+a'))
        else:
            print(f"[MSAN1-00000][XPON - Profiles - ACL Profile] Max Table Fail({ACL_profile_capacity}) = {max_count}",file = open(file_name, '+a'))
    except:
        max_count = driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__()
        print(f"             [XPON - Profiles - ACL Profile] Max Table Not full = {max_count}-1 = {max_count-1}",file = open(file_name, '+a'))
        print(f"[MSAN1-00000][XPON - Profiles - ACL Profile] Max Table Fail({ACL_profile_capacity}) = {max_count}",file = open(file_name, '+a'))

# Xpon profile count test
# =======================================================================================

# =======================================================================================
# Xpon profile test

def Service_Profile_Test(driver,username,password,file_name):
    if_error = False
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    time.sleep(5)
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Service").click()
    time.sleep(5)
    if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__() > service_profile_capacity-2):
        driver.find_elements(By.NAME, "rpXGSponServiceProf_chkDel")[-1].click()
        driver.find_elements(By.NAME, "rpXGSponServiceProf_chkDel")[-2].click()
        pro.Service_Profile_Delete(driver)
    pro.Service_Profile_New(driver)
    pro.Service_Profile_New_Name(driver,"_______xpon_service_profile_SFU")
    pro.Service_Profile_New_VLAN(driver,"4094")
    pro.Service_Profile_New_Mapper_Pbits(driver,0,False)
    pro.Service_Profile_New_Mapper_Pbits(driver,1,False)
    pro.Service_Profile_New_Mapper_Pbits(driver,2,False)
    pro.Service_Profile_New_Mapper_Pbits(driver,3,False)
    pro.Service_Profile_New_Mapper_Pbits(driver,4,False)
    pro.Service_Profile_New_Mapper_Pbits(driver,5,False)
    pro.Service_Profile_New_Mapper_Pbits(driver,6,False)
    pro.Service_Profile_New_Mapper_Pbits(driver,7,False)
    pro.Service_Profile_New_Lan_mode_veip(driver)
    pro.Service_Profile_New_Lan_mode_bridge(driver)
    pro.Service_Profile_New_Lan(driver,"Lan 8")
    # pro.Service_Profile_New_Vlan_xc(driver,"4094")
    # pro.Service_Profile_New_Vlan_xc_mode_enable(driver)
    # pro.Service_Profile_New_Vlan_xc_mode_disable(driver)
    pro.Service_Profile_New_Apply(driver)
    if(mod.IsAlert(driver) == True):
        print(f"             [XPON - Profiles - Service Profile] SFU Valid Value Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
        print(f"             [XPON - Profiles - Service Profile] SFU Apply Fail",file = open(file_name, '+a'))
        if_error = True
    except:
        pass
    if_find = False
    for index in range(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponServiceProf_name").__len__()):
        try:
            driver.switch_to.default_content()
            driver.find_element(By.ID, "userContinue").click()
            driver.switch_to.frame(0)
        except:
            try:
                driver.switch_to.default_content()
                driver.find_element(By.CLASS_NAME, "ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-front.ui-draggable")
                driver.find_element(By.ID, "lg_user").send_keys(username)
                driver.find_element(By.ID, "lg_pass").send_keys(password)
                driver.find_element(By.ID, "userLogin").click()
                driver.switch_to.frame(0)
            except:
                driver.switch_to.frame(0)
        if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponServiceProf_name")[-(index+1)].get_attribute("textContent") == "_______xpon_service_profile_SFU"):
            if_find = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponServiceProf_vlan")[-(index+1)].get_attribute("textContent") != "4094"):
                print(f"             [XPON - Profiles - Service Profile] SFU VLAN:4094 Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponServiceProf_uniPbit")[-(index+1)].get_attribute("textContent") != ""):
                print(f"             [XPON - Profiles - Service Profile] SFU Mapper pbits Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponServiceProf_mode")[-(index+1)].get_attribute("textContent") != "bridge"):
                print(f"             [XPON - Profiles - Service Profile] SFU Mode:bridge Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponServiceProf_port")[-(index+1)].get_attribute("textContent") != "Lan 8"):
                print(f"             [XPON - Profiles - Service Profile] SFU Port:Lan 8 Test Fail",file = open(file_name, '+a'))
                if_error = True
            # if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponServiceProf_dsfoward")[-(index+1)].get_attribute("textContent") != "vid+mac"):
            #     print(f"             [XPON - Profiles - Service Profile] SFU Ds forward mode:vid+mac Test Fail",file = open(file_name, '+a'))
            #     if_error = True
            # if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponServiceProf_vlan1_1")[-(index+1)].get_attribute("textContent") != "N"):
            #     print(f"             [XPON - Profiles - Service Profile] SFU 1:1-VLAN:N Test Fail",file = open(file_name, '+a'))
            #     if_error = True
            # if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponServiceProf_vlanxc")[-(index+1)].get_attribute("textContent") != "4094"):
            #     print(f"             [XPON - Profiles - Service Profile] SFU VLAN-xc:4094 Test Fail",file = open(file_name, '+a'))
            #     if_error = True
            # if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponServiceProf_vlanxcmode")[-(index+1)].get_attribute("textContent") != "disable"):
            #     print(f"             [XPON - Profiles - Service Profile] SFU VLAN-xc mode:disable Test Fail",file = open(file_name, '+a'))
            #     if_error = True
            break
    if(if_find == False):
        print(f"             [XPON - Profiles - Service Profile] SFU Apply Not Found Test Fail",file = open(file_name, '+a'))
        if_error = True
    pro.Service_Profile_New(driver)
    pro.Service_Profile_New_Name(driver,"_______xpon_service_profile_HGU")
    pro.Service_Profile_New_VLAN(driver,"4094")
    pro.Service_Profile_New_Mapper_Pbits(driver,0,False)
    pro.Service_Profile_New_Mapper_Pbits(driver,1,False)
    pro.Service_Profile_New_Mapper_Pbits(driver,2,False)
    pro.Service_Profile_New_Mapper_Pbits(driver,3,False)
    pro.Service_Profile_New_Mapper_Pbits(driver,4,False)
    pro.Service_Profile_New_Mapper_Pbits(driver,5,False)
    pro.Service_Profile_New_Mapper_Pbits(driver,6,False)
    pro.Service_Profile_New_Mapper_Pbits(driver,7,False)
    pro.Service_Profile_New_Lan_mode_bridge(driver)
    pro.Service_Profile_New_Lan_mode_veip(driver)
    pro.Service_Profile_New_Lan(driver,"Lan 8")
    # pro.Service_Profile_New_Vlan_xc(driver,"4094")
    # pro.Service_Profile_New_Vlan_xc_mode_enable(driver)
    # pro.Service_Profile_New_Vlan_xc_mode_disable(driver)
    pro.Service_Profile_New_Apply(driver)
    if(mod.IsAlert(driver) == True):
        print(f"             [XPON - Profiles - Service Profile] HGU Valid Input Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
        print(f"             [XPON - Profiles - Service Profile] HGU Apply Fail",file = open(file_name, '+a'))
        if_error = True
    except:
        pass
    if_find = False
    for index in range(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponServiceProf_name").__len__()):
        try:
            driver.switch_to.default_content()
            driver.find_element(By.ID, "userContinue").click()
            driver.switch_to.frame(0)
        except:
            try:
                driver.switch_to.default_content()
                driver.find_element(By.CLASS_NAME, "ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-front.ui-draggable")
                driver.find_element(By.ID, "lg_user").send_keys(username)
                driver.find_element(By.ID, "lg_pass").send_keys(password)
                driver.find_element(By.ID, "userLogin").click()
                driver.switch_to.frame(0)
            except:
                driver.switch_to.frame(0)
        if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponServiceProf_name")[-(index+1)].get_attribute("textContent") == "_______xpon_service_profile_HGU"):
            if_find = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponServiceProf_vlan")[-(index+1)].get_attribute("textContent") != "4094"):
                print(f"             [XPON - Profiles - Service Profile] HGU VLAN:4094 Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponServiceProf_uniPbit")[-(index+1)].get_attribute("textContent") != ""):
                print(f"             [XPON - Profiles - Service Profile] HGU Mapper pbits Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponServiceProf_mode")[-(index+1)].get_attribute("textContent") != "veip"):
                print(f"             [XPON - Profiles - Service Profile] HGU Mode:veip Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponServiceProf_port")[-(index+1)].get_attribute("textContent") != "Lan 8"):
                print(f"             [XPON - Profiles - Service Profile] HGU Port:Lan 8 Test Fail",file = open(file_name, '+a'))
                if_error = True
            # if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponServiceProf_dsfoward")[-(index+1)].get_attribute("textContent") != "vid+mac"):
            #     print(f"             [XPON - Profiles - Service Profile] HGU Ds forward mode:vid+mac Test Fail",file = open(file_name, '+a'))
            #     if_error = True
            # if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponServiceProf_vlan1_1")[-(index+1)].get_attribute("textContent") != "N"):
            #     print(f"             [XPON - Profiles - Service Profile] HGU 1:1-VLAN:N Test Fail",file = open(file_name, '+a'))
            #     if_error = True
            # if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponServiceProf_vlanxc")[-(index+1)].get_attribute("textContent") != "4094"):
            #     print(f"             [XPON - Profiles - Service Profile] HGU VLAN-xc:4094 Test Fail",file = open(file_name, '+a'))
            #     if_error = True
            # if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponServiceProf_vlanxcmode")[-(index+1)].get_attribute("textContent") != "disable"):
            #     print(f"             [XPON - Profiles - Service Profile] HGU VLAN-xc mode:disable Test Fail",file = open(file_name, '+a'))
            #     if_error = True
            break
    if(if_find == False):
        print(f"             [XPON - Profiles - Service Profile] HGU Apply Not Found Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(if_error == False):
        print(f"[MSAN1-12158][XPON - Profiles - Service Profile] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-12158][XPON - Profiles - Service Profile] 9Fail",file = open(file_name, '+a'))
    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def QoS_Bandwidth_Profile_Test(driver,username,password,file_name):
    if_error = False
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    time.sleep(5)
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "QoS Bandwidth").click()
    time.sleep(5)
    if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__() > qos_bandwidth_profile_capacity-1):
        driver.find_elements(By.NAME, "rpXGSponQosBwProf_chkDel")[-1].click()
        pro.QoS_Bandwidth_Profile_Delete(driver)
    pro.QoS_Bandwidth_Profile_New(driver)
    pro.QoS_Bandwidth_Profile_New_Name(driver,"______________100M")
    pro.QoS_Bandwidth_Profile_New_sir(driver,"8509953")
    pro.QoS_Bandwidth_Profile_New_Apply(driver)
    if(mod.IsAlert(driver) == False):
        print("             [XPON - Profiles - QoS Bandwidth Profile] sir No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    pro.QoS_Bandwidth_Profile_New_sir(driver,"500000")
    pro.QoS_Bandwidth_Profile_New_air(driver,"8509953")
    if(mod.IsAlert(driver) == False):
        print("             [XPON - Profiles - QoS Bandwidth Profile] air No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    pro.QoS_Bandwidth_Profile_New_air(driver,"500000")
    pro.QoS_Bandwidth_Profile_New_pir(driver,"10000001")
    if(mod.IsAlert(driver) == False):
        print("             [XPON - Profiles - QoS Bandwidth Profile] pir No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    pro.QoS_Bandwidth_Profile_New_pir(driver,"10000000")
    pro.QoS_Bandwidth_Profile_New_Apply(driver)
    if(mod.IsAlert(driver) == True):
        print(f"             [XPON - Profiles - QoS Bandwidth Profile] Valid Input Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
        print(f"             [XPON - Profiles - QoS Bandwidth Profile] Apply Fail",file = open(file_name, '+a'))
        if_error = True
    except:
        pass
    if_find = False
    for index in range(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponQosBwProf_name").__len__()):
        try:
            driver.switch_to.default_content()
            driver.find_element(By.ID, "userContinue").click()
            driver.switch_to.frame(0)
        except:
            try:
                driver.switch_to.default_content()
                driver.find_element(By.CLASS_NAME, "ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-front.ui-draggable")
                driver.find_element(By.ID, "lg_user").send_keys(username)
                driver.find_element(By.ID, "lg_pass").send_keys(password)
                driver.find_element(By.ID, "userLogin").click()
                driver.switch_to.frame(0)
            except:
                driver.switch_to.frame(0)
        if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponQosBwProf_name")[-(index+1)].get_attribute("textContent") == "______________100M"):
            if_find = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponQosBwProf_sir")[-(index+1)].get_attribute("textContent") != "500000"):
                print(f"             [XPON - Profiles - QoS Bandwidth Profile] SIR:500000 Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponQosBwProf_air")[-(index+1)].get_attribute("textContent") != "500000"):
                print(f"             [XPON - Profiles - QoS Bandwidth Profile] AIR:500000 Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponQosBwProf_pir")[-(index+1)].get_attribute("textContent") != "10000000"):
                print(f"             [XPON - Profiles - QoS Bandwidth Profile] PIR:10000000 Test Fail",file = open(file_name, '+a'))
                if_error = True
            break
    if(if_find == False):
        print(f"             [XPON - Profiles - QoS Bandwidth Profile] Apply Not Found Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(if_error == False):
        print(f"[MSAN1-12159][XPON - Profiles - QoS Bandwidth Profile] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-12159][XPON - Profiles - QoS Bandwidth Profile] Result Fail",file = open(file_name, '+a'))
    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def Multicast_Profile_Test(driver,username,password,file_name):
    if_error = False
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "Multicast").click()
    driver.find_element(By.LINK_TEXT, "IGMP Privilege Profile").click()
    time.sleep(5)
    driver.switch_to.frame(0)
    mul.IGMP_Privilege_Profile_Name(driver,f"1234567890123456789012345678901")
    mul.IGMP_Privilege_Profile_Bandwidth(driver,"100")
    mul.IGMP_Privilege_Profile_Start_Address(driver,f"224.0.0.0")
    mul.IGMP_Privilege_Profile_End_Address(driver,f"239.255.255.255")
    mul.IGMP_Privilege_Profile_Privilege(driver,3)
    mul.IGMP_Privilege_Profile_Length(driver,"300")
    mul.IGMP_Privilege_Profile_Interval(driver,"300")
    mul.IGMP_Privilege_Profile_Count(driver,"10")
    mul.IGMP_Privilege_Profile_Reset(driver,"86400")
    mul.IGMP_Privilege_Profile_Apply_New(driver)
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    time.sleep(5)
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Multicast").click()
    time.sleep(5)
    if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__() > multicast_profile_capacity-2):
        driver.find_elements(By.NAME, "rpXGSponMcastProf_chkDel")[-1].click()
        driver.find_elements(By.NAME, "rpXGSponMcastProf_chkDel")[-2].click()
        pro.Multicast_Profile_Delete(driver)
    pro.Multicast_Profile_New(driver)
    pro.Multicast_Profile_New_Name(driver,"_____xpon_multicast_profile_SFU")
    pro.Multicast_Profile_New_UNI_VID(driver,"0")
    pro.Multicast_Profile_New_Apply(driver)
    if(mod.IsAlert(driver) == False):
        print("             [XPON - Profiles - Multicast Profile] UNI VID:0 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    pro.Multicast_Profile_New_UNI_VID(driver,"4095")
    pro.Multicast_Profile_New_Apply(driver)
    if(mod.IsAlert(driver) == False):
        print("             [XPON - Profiles - Multicast Profile] UNI VID:4095 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    pro.Multicast_Profile_New_UNI_VID(driver,"@")
    pro.Multicast_Profile_New_Apply(driver)
    if(mod.IsAlert(driver) == False):
        print("             [XPON - Profiles - Multicast Profile] UNI VID:@ No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    pro.Multicast_Profile_New_UNI_VID(driver,"4094")
    pro.Multicast_Profile_New_Tx_Tag_VID(driver,"0")
    pro.Multicast_Profile_New_Apply(driver)
    if(mod.IsAlert(driver) == False):
        print("             [XPON - Profiles - Multicast Profile] Tx Tag VID:0 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    pro.Multicast_Profile_New_Tx_Tag_VID(driver,"4095")
    pro.Multicast_Profile_New_Apply(driver)
    if(mod.IsAlert(driver) == False):
        print("             [XPON - Profiles - Multicast Profile] Tx Tag VID:4095 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    pro.Multicast_Profile_New_Tx_Tag_VID(driver,"@")
    pro.Multicast_Profile_New_Apply(driver)
    if(mod.IsAlert(driver) == False):
        print("             [XPON - Profiles - Multicast Profile] Tx Tag VID:@ No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    pro.Multicast_Profile_New_Tx_Tag_VID(driver,"")
    pro.Multicast_Profile_New_Max_Group(driver,"0")
    pro.Multicast_Profile_New_Apply(driver)
    if(mod.IsAlert(driver) == False):
        print("             [XPON - Profiles - Multicast Profile] Max Group:0 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    pro.Multicast_Profile_New_Max_Group(driver,"513")
    pro.Multicast_Profile_New_Apply(driver)
    if(mod.IsAlert(driver) == False):
        print("             [XPON - Profiles - Multicast Profile] Max Group:513 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    pro.Multicast_Profile_New_Max_Group(driver,"@")
    pro.Multicast_Profile_New_Apply(driver)
    if(mod.IsAlert(driver) == False):
        print("             [XPON - Profiles - Multicast Profile] Max Group:@ No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    pro.Multicast_Profile_New_Max_Group(driver,"512")
    pro.Multicast_Profile_New_Max_Message(driver,"0")
    pro.Multicast_Profile_New_Apply(driver)
    if(mod.IsAlert(driver) == False):
        print("             [XPON - Profiles - Multicast Profile] Max Message:0 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    pro.Multicast_Profile_New_Max_Message(driver,"65")
    pro.Multicast_Profile_New_Apply(driver)
    if(mod.IsAlert(driver) == False):
        print("             [XPON - Profiles - Multicast Profile] Max Message:65 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    pro.Multicast_Profile_New_Max_Message(driver,"@")
    pro.Multicast_Profile_New_Apply(driver)
    if(mod.IsAlert(driver) == False):
        print("             [XPON - Profiles - Multicast Profile] Max Message:@ No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(3)
    pro.Multicast_Profile_New_Max_Message(driver,"64")
    pro.Multicast_Profile_New_IGMP_Version(driver,"IGMPv2")
    pro.Multicast_Profile_New_Tx_Tag_Mode(driver,"untag")
    pro.Multicast_Profile_New_Tx_Tag_Pbit(driver,"0")
    pro.Multicast_Profile_New_Group_Privilege_Profile(driver,"1234567890123456789012345678901")
    pro.Multicast_Profile_New_Apply(driver)
    if(mod.IsAlert(driver) == True):
        print("             [XPON - Profiles - Multicast Profile] SFU Valid Input Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
        print(f"             [XPON - Profiles - Multicast Profile] SFU Apply Fail",file = open(file_name, '+a'))
        if_error = True
    except:
        pass
    if_find = False
    for index in range(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponMcastProf_name").__len__()):
        try:
            driver.switch_to.default_content()
            driver.find_element(By.ID, "userContinue").click()
            driver.switch_to.frame(0)
        except:
            try:
                driver.switch_to.default_content()
                driver.find_element(By.CLASS_NAME, "ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-front.ui-draggable")
                driver.find_element(By.ID, "lg_user").send_keys(username)
                driver.find_element(By.ID, "lg_pass").send_keys(password)
                driver.find_element(By.ID, "userLogin").click()
                driver.switch_to.frame(0)
            except:
                driver.switch_to.frame(0)
        if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponMcastProf_name")[-(index+1)].get_attribute("textContent") == "_____xpon_multicast_profile_SFU"):
            if_find = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponMcastProf_uniVid")[-(index+1)].get_attribute("textContent") != "4094"):
                print(f"             [XPON - Profiles - Multicast Profile] SFU UNI VID:4094 Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponMcastProf_igmpVersion")[-(index+1)].get_attribute("textContent") != "IGMPv2"):
                print(f"             [XPON - Profiles - Multicast Profile] SFU Version:IGMPv2 Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponMcastProf_txTagMode")[-(index+1)].get_attribute("textContent") != "untag"):
                print(f"             [XPON - Profiles - Multicast Profile] SFU Tx Tag:untag Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponMcastProf_txTagVid")[-(index+1)].get_attribute("textContent") != ""):
                print(f"             [XPON - Profiles - Multicast Profile] SFU Tx Tag VID:null Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponMcastProf_txTagPbit")[-(index+1)].get_attribute("textContent") != ""):
                print(f"             [XPON - Profiles - Multicast Profile] SFU Tx Tag Pbit:0 Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponMcastProf_privilegeProf")[-(index+1)].get_attribute("textContent") != "1234567890123456789012345678901"):
                print(f"             [XPON - Profiles - Multicast Profile] SFU Group Privilege Profile Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponMcastProf_maxGroup")[-(index+1)].get_attribute("textContent") != "512"):
                print(f"             [XPON - Profiles - Multicast Profile] SFU Max Group:512 Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponMcastProf_maxMsg")[-(index+1)].get_attribute("textContent") != "64"):
                print(f"             [XPON - Profiles - Multicast Profile] SFU Max Message:64 Test Fail",file = open(file_name, '+a'))
                if_error = True
            break
    if(if_find == False):
        print(f"             [XPON - Profiles - Multicast Profile] SFU Apply Not Found Test Fail",file = open(file_name, '+a'))
        if_error = True
    pro.Multicast_Profile_New(driver)
    pro.Multicast_Profile_New_Name(driver,"_____xpon_multicast_profile_HGU")
    pro.Multicast_Profile_New_UNI_VID(driver,"4094")
    pro.Multicast_Profile_New_IGMP_Version(driver,"IGMPv3")
    pro.Multicast_Profile_New_Tx_Tag_Mode(driver,"replace")
    pro.Multicast_Profile_New_Tx_Tag_VID(driver,"4094")
    pro.Multicast_Profile_New_Tx_Tag_Pbit(driver,"7")
    pro.Multicast_Profile_New_Group_Privilege_Profile(driver,"1234567890123456789012345678901")
    pro.Multicast_Profile_New_Max_Group(driver,"512")
    pro.Multicast_Profile_New_Max_Message(driver,"64")
    pro.Multicast_Profile_New_Apply(driver)
    if(mod.IsAlert(driver) == True):
        print("             [XPON - Profiles - Multicast Profile] HGU Valid Input Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
        print(f"             [XPON - Profiles - Multicast Profile] HGU Apply Fail",file = open(file_name, '+a'))
        if_error = True
    except:
        pass
    if_find = False
    for index in range(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponMcastProf_name").__len__()):
        try:
            driver.switch_to.default_content()
            driver.find_element(By.ID, "userContinue").click()
            driver.switch_to.frame(0)
        except:
            try:
                driver.switch_to.default_content()
                driver.find_element(By.CLASS_NAME, "ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-front.ui-draggable")
                driver.find_element(By.ID, "lg_user").send_keys(username)
                driver.find_element(By.ID, "lg_pass").send_keys(password)
                driver.find_element(By.ID, "userLogin").click()
                driver.switch_to.frame(0)
            except:
                driver.switch_to.frame(0)
        if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponMcastProf_name")[-(index+1)].get_attribute("textContent") == "_____xpon_multicast_profile_HGU"):
            if_find = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponMcastProf_uniVid")[-(index+1)].get_attribute("textContent") != "4094"):
                print(f"             [XPON - Profiles - Multicast Profile] HGU UNI VID:4094 Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponMcastProf_igmpVersion")[-(index+1)].get_attribute("textContent") != "IGMPv3"):
                print(f"             [XPON - Profiles - Multicast Profile] HGU Version:IGMPv3 Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponMcastProf_txTagMode")[-(index+1)].get_attribute("textContent") != "replace"):
                print(f"             [XPON - Profiles - Multicast Profile] HGU Tx Tag:replace Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponMcastProf_txTagVid")[-(index+1)].get_attribute("textContent") != "4094"):
                print(f"             [XPON - Profiles - Multicast Profile] HGU Tx Tag VID:4094 Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponMcastProf_txTagPbit")[-(index+1)].get_attribute("textContent") != "7"):
                print(f"             [XPON - Profiles - Multicast Profile] HGU Tx Tag Pbit:7 Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponMcastProf_privilegeProf")[-(index+1)].get_attribute("textContent") != "1234567890123456789012345678901"):
                print(f"             [XPON - Profiles - Multicast Profile] HGU Group Privilege Profile Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponMcastProf_maxGroup")[-(index+1)].get_attribute("textContent") != "512"):
                print(f"             [XPON - Profiles - Multicast Profile] HGU Max Group:512 Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponMcastProf_maxMsg")[-(index+1)].get_attribute("textContent") != "64"):
                print(f"             [XPON - Profiles - Multicast Profile] HGU Max Message:64 Test Fail",file = open(file_name, '+a'))
                if_error = True
            break
    if(if_find == False):
        print(f"             [XPON - Profiles - Multicast Profile] HGU Apply Not Found Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(if_error == False):
        print(f"[MSAN1-12160][XPON - Profiles - Multicast Profile] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-12160][XPON - Profiles - Multicast Profile] Result Fail",file = open(file_name, '+a'))
    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def Uni_Profile_Test(driver,username,password,file_name):# 正在寫
    if_error = False
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "UNI").click()
    pro.Uni_Profile_New(driver)
    pro.Uni_Profile_New_Name(driver,"___________xpon_uni_profile_SFU")
    
    pro.Uni_Profile_New_Lan_Vlan_Active(driver,1,True)
    pro.Uni_Profile_New_Lan_Filter_ethertype(driver,1)
    pro.Uni_Profile_New_Lan_Filter_ethertype_Value(driver,1,"ipoe")
    pro.Uni_Profile_New_Lan_UniportList(driver,1,4)
    pro.Uni_Profile_New_Lan_Vlan(driver,1,"4094/7")
    
    pro.Uni_Profile_New_Lan_Vlan_Active(driver,2,True)
    pro.Uni_Profile_New_Lan_Filter_ethertype(driver,2)
    pro.Uni_Profile_New_Lan_Filter_ethertype_Value(driver,2,"arp")
    pro.Uni_Profile_New_Lan_UniportList(driver,2,4)
    pro.Uni_Profile_New_Lan_Vlan(driver,2,"4094/7")
    
    pro.Uni_Profile_New_Lan_Vlan_Active(driver,3,True)
    pro.Uni_Profile_New_Lan_Filter_ethertype(driver,3)
    pro.Uni_Profile_New_Lan_Filter_ethertype_Value(driver,3,"pppoe")
    pro.Uni_Profile_New_Lan_UniportList(driver,3,"4") 
    pro.Uni_Profile_New_Lan_Vlan(driver,3,"4094/7")

    pro.Uni_Profile_New_Lan_Vlan_Active(driver,4,True)
    pro.Uni_Profile_New_Lan_Filter_ethertype(driver,4)
    pro.Uni_Profile_New_Lan_Filter_ethertype_Value(driver,4,"ipv6")
    pro.Uni_Profile_New_Lan_UniportList(driver,4,4)
    pro.Uni_Profile_New_Lan_Vlan(driver,4,"4094/7")

    pro.Uni_Profile_New_Lan_Vlan_Active(driver,5,True)
    pro.Uni_Profile_New_Lan_Filter_uniVlan(driver,5)
    pro.Uni_Profile_New_Lan_Filter_uniVlan_Value(driver,5,4094)
    pro.Uni_Profile_New_Lan_UniportList(driver,5,4)
    pro.Uni_Profile_New_Lan_Vlan(driver,5,"4094")
    
    pro.Uni_Profile_New_Lan_Vlan_Active(driver,6,True)
    pro.Uni_Profile_New_Lan_Filter_untag(driver,6)
    pro.Uni_Profile_New_Lan_UniportList(driver,6,4)
    pro.Uni_Profile_New_Lan_Vlan(driver,6,"4094/4")

    pro.Uni_Profile_New_Lan_Vlan_Active(driver,7,True)
    pro.Uni_Profile_New_Lan_Filter_untag(driver,7)
    pro.Uni_Profile_New_Lan_UniportList(driver,7,4)
    pro.Uni_Profile_New_Lan_Vlan(driver,7,"4094/7")

    pro.Uni_Profile_New_Lan_Vlan_Active(driver,8,True)
    pro.Uni_Profile_New_Lan_Filter_uniVlan(driver,8)
    pro.Uni_Profile_New_Lan_Filter_uniVlan_Value(driver,8,1)
    pro.Uni_Profile_New_Lan_UniportList(driver,8,4)
    pro.Uni_Profile_New_Lan_Vlan(driver,8,"4094")

    #XLan
    driver.find_element(By.LINK_TEXT, "Xlan Port Vlan").click()
    pro.Uni_Profile_New_XLan_Vlan_Active(driver,1,True)
    pro.Uni_Profile_New_XLan_Filter_ethertype(driver,1)
    pro.Uni_Profile_New_XLan_Filter_ethertype_Value(driver,1,"ipoe")
    pro.Uni_Profile_New_XLan_UniportList(driver,1,4)
    pro.Uni_Profile_New_XLan_Vlan(driver,1,"4094/7")
    
    pro.Uni_Profile_New_XLan_Vlan_Active(driver,2,True)
    pro.Uni_Profile_New_XLan_Filter_ethertype(driver,2)
    pro.Uni_Profile_New_XLan_Filter_ethertype_Value(driver,2,"arp")
    pro.Uni_Profile_New_XLan_UniportList(driver,2,4)
    pro.Uni_Profile_New_XLan_Vlan(driver,2,"4094/7")
    
    pro.Uni_Profile_New_XLan_Vlan_Active(driver,3,True)
    pro.Uni_Profile_New_XLan_Filter_ethertype(driver,3)
    pro.Uni_Profile_New_XLan_Filter_ethertype_Value(driver,3,"pppoe")
    pro.Uni_Profile_New_XLan_UniportList(driver,3,"4") 
    pro.Uni_Profile_New_XLan_Vlan(driver,3,"4094/7")

    pro.Uni_Profile_New_XLan_Vlan_Active(driver,4,True)
    pro.Uni_Profile_New_XLan_Filter_ethertype(driver,4)
    pro.Uni_Profile_New_XLan_Filter_ethertype_Value(driver,4,"ipv6")
    pro.Uni_Profile_New_XLan_UniportList(driver,4,4)
    pro.Uni_Profile_New_XLan_Vlan(driver,4,"4094/7")

    pro.Uni_Profile_New_XLan_Vlan_Active(driver,5,True)
    pro.Uni_Profile_New_XLan_Filter_uniVlan(driver,5)
    pro.Uni_Profile_New_XLan_Filter_uniVlan_Value(driver,5,4094)
    pro.Uni_Profile_New_XLan_UniportList(driver,5,4)
    pro.Uni_Profile_New_XLan_Vlan(driver,5,"4094")
    
    pro.Uni_Profile_New_XLan_Vlan_Active(driver,6,True)
    pro.Uni_Profile_New_XLan_Filter_untag(driver,6)
    pro.Uni_Profile_New_XLan_UniportList(driver,6,4)
    pro.Uni_Profile_New_XLan_Vlan(driver,6,"4094/4")

    pro.Uni_Profile_New_XLan_Vlan_Active(driver,7,True)
    pro.Uni_Profile_New_XLan_Filter_untag(driver,7)
    pro.Uni_Profile_New_XLan_UniportList(driver,7,4)
    pro.Uni_Profile_New_XLan_Vlan(driver,7,"4094/7")

    pro.Uni_Profile_New_XLan_Vlan_Active(driver,8,True)
    pro.Uni_Profile_New_XLan_Filter_uniVlan(driver,8)
    pro.Uni_Profile_New_XLan_Filter_uniVlan_Value(driver,8,1)
    pro.Uni_Profile_New_XLan_UniportList(driver,8,4)
    pro.Uni_Profile_New_XLan_Vlan(driver,8,"4094")

    #Veip
    driver.find_element(By.LINK_TEXT, "Veip Port Vlan").click()
    pro.Uni_Profile_New_Veip_Vlan_Active(driver,1,True)
    pro.Uni_Profile_New_Veip_Filter_ethertype(driver,1)
    pro.Uni_Profile_New_Veip_Filter_ethertype_Value(driver,1,"ipoe")
    pro.Uni_Profile_New_Veip_UniportList(driver,1,1)
    pro.Uni_Profile_New_Veip_Vlan(driver,1,"4094/7")
    
    pro.Uni_Profile_New_Veip_Vlan_Active(driver,2,True)
    pro.Uni_Profile_New_Veip_Filter_ethertype(driver,2)
    pro.Uni_Profile_New_Veip_Filter_ethertype_Value(driver,2,"arp")
    pro.Uni_Profile_New_Veip_UniportList(driver,2,1)
    pro.Uni_Profile_New_Veip_Vlan(driver,2,"4094/7")
    
    pro.Uni_Profile_New_Veip_Vlan_Active(driver,3,True)
    pro.Uni_Profile_New_Veip_Filter_ethertype(driver,3)
    pro.Uni_Profile_New_Veip_Filter_ethertype_Value(driver,3,"pppoe")
    pro.Uni_Profile_New_Veip_UniportList(driver,3,1)
    pro.Uni_Profile_New_Veip_Vlan(driver,3,"4094/7")

    pro.Uni_Profile_New_Veip_Vlan_Active(driver,4,True)
    pro.Uni_Profile_New_Veip_Filter_ethertype(driver,4)
    pro.Uni_Profile_New_Veip_Filter_ethertype_Value(driver,4,"ipv6")
    pro.Uni_Profile_New_Veip_UniportList(driver,4,1)
    pro.Uni_Profile_New_Veip_Vlan(driver,4,"4094/7")

    pro.Uni_Profile_New_Veip_Vlan_Active(driver,5,True)
    pro.Uni_Profile_New_Veip_Filter_uniVlan(driver,5)
    pro.Uni_Profile_New_Veip_Filter_uniVlan_Value(driver,5,4094)
    pro.Uni_Profile_New_Veip_UniportList(driver,5,1)
    pro.Uni_Profile_New_Veip_Vlan(driver,5,"4094")
    
    pro.Uni_Profile_New_Veip_Vlan_Active(driver,6,True)
    pro.Uni_Profile_New_Veip_Filter_untag(driver,6)
    pro.Uni_Profile_New_Veip_UniportList(driver,6,1)
    pro.Uni_Profile_New_Veip_Vlan(driver,6,"4094/4")

    pro.Uni_Profile_New_Veip_Vlan_Active(driver,7,True)
    pro.Uni_Profile_New_Veip_Filter_untag(driver,7)
    pro.Uni_Profile_New_Veip_UniportList(driver,7,1)
    pro.Uni_Profile_New_Veip_Vlan(driver,7,"4094/7")

    pro.Uni_Profile_New_Veip_Vlan_Active(driver,8,True)
    pro.Uni_Profile_New_Veip_Filter_uniVlan(driver,8)
    pro.Uni_Profile_New_Veip_Filter_uniVlan_Value(driver,8,1)
    pro.Uni_Profile_New_Veip_UniportList(driver,8,1)
    pro.Uni_Profile_New_Veip_Vlan(driver,8,"4094")

    driver.find_element(By.LINK_TEXT, "Lan Port").click()
    pro.Uni_Profile_New_Lan_fdb_count_all(driver,255)
    pro.Uni_Profile_New_Lan_DS_rate_all(driver,1000000)
    pro.Uni_Profile_New_Lan_Storm_B_all(driver,1000000)
    pro.Uni_Profile_New_Lan_Storm_M_all(driver,1000000)
    pro.Uni_Profile_New_Lan_Storm_D_all(driver,1000000)

    driver.find_element(By.LINK_TEXT, "XLan Port").click()
    pro.Uni_Profile_New_XLan_fdb_count_all(driver,255)
    pro.Uni_Profile_New_XLan_DS_rate_all(driver,10000000)
    pro.Uni_Profile_New_XLan_Storm_B_all(driver,10000000)
    pro.Uni_Profile_New_XLan_Storm_M_all(driver,10000000)
    pro.Uni_Profile_New_XLan_Storm_D_all(driver,10000000)

    driver.find_element(By.LINK_TEXT, "Veip Port").click()
    pro.Uni_Profile_New_Veip_fdb_count(driver,1,255)
    pro.Uni_Profile_New_Veip_DS_rate(driver,1,10000000)
    pro.Uni_Profile_New_Veip_Storm_B(driver,1,10000000)
    pro.Uni_Profile_New_Veip_Storm_M(driver,1,10000000)
    pro.Uni_Profile_New_Veip_Storm_D(driver,1,10000000)

    pro.Uni_Profile_New_Apply(driver)
### Add check

    #Lan port vlan
    
    # pro.Uni_Profile_New_Lan_UniportList(driver,1,4)    
    # pro.Uni_Profile_New_Lan_Vlan(driver,1,"4094/7")


    if(mod.IsAlert(driver) == True):
        print(f"             [XPON - Profiles - UNI Profile] ___________xpon_uni_profile_SFU Valid Value Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
        print(f"             [XPON - Profiles - UNI Profile] ___________xpon_uni_profile_SFU Apply Fail",file = open(file_name, '+a'))
        if_error = True
    except:
        pass
    time.sleep(5)
    uni_profile_name = ["___________xpon_uni_profile_SFU"]

###
    for check_time in range(1):
        if_find = False                                       #td-table-content-xgspon.td-table-extend-text-left.rpXGSponUniProf_name
        for index in range(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.rpXGSponUniProf_name").__len__()):            
            try:
                driver.switch_to.default_content()
                driver.find_element(By.ID, "userContinue").click()
                driver.switch_to.frame(0)
            except:
                try:
                    driver.switch_to.default_content()
                    driver.find_element(By.CLASS_NAME, "ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-front.ui-draggable")
                    driver.find_element(By.ID, "lg_user").send_keys(username)
                    driver.find_element(By.ID, "lg_pass").send_keys(password)
                    driver.find_element(By.ID, "userLogin").click()
                    driver.switch_to.frame(0)
                except:
                    driver.switch_to.frame(0)                                                                                               
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.rpXGSponUniProf_name")[-(index+1)].get_attribute("textContent") == uni_profile_name[check_time]):
                if_find = True                                                   
                if(driver.find_element(By.CLASS_NAME, "td-table-content-xgspon.rpXGSponUniProf_lanActiveload").get_attribute("textContent") != "Y"):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} Active lan Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.CLASS_NAME, "td-table-content-xgspon.rpXGSponUniProf_xlanActiveload").get_attribute("textContent") != "Y"):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} Active xlan Test Fail",file = open(file_name, '+a'))
                    if_error = True
                #Max FDB Count
                if(driver.find_element(By.CLASS_NAME, "td-table-content-xgspon.rpXGSponUniProf_lanMaxFdbCntload").get_attribute("textContent") != "255"):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} Max FDB Count lan Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.CLASS_NAME, "td-table-content-xgspon.rpXGSponUniProf_xlanMaxFdbCntload").get_attribute("textContent") != "255"):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} Max FDB Count xlan Test Fail",file = open(file_name, '+a'))
                    if_error = True
                #DS RateLimit
                if(driver.find_element(By.CLASS_NAME, "td-table-content-xgspon.rpXGSponUniProf_lanDsLimitload").get_attribute("textContent") != "1000000"):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} DS RateLimit lan Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.CLASS_NAME, "td-table-content-xgspon.rpXGSponUniProf_xlanDsLimitload").get_attribute("textContent") != "10000000"):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} DS RateLimit xlan Test Fail",file = open(file_name, '+a'))
                    if_error = True
                #Storm Control
                if(driver.find_element(By.CLASS_NAME, "td-table-content-xgspon.rpXGSponUniProf_lanStormCtrlBcastload").get_attribute("textContent") != "1000000"):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} Storm Control Broadcast lan Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.CLASS_NAME, "td-table-content-xgspon.rpXGSponUniProf_lanStormCtrlMcastload").get_attribute("textContent") != "1000000"):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} Storm Control Multicast lan Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.CLASS_NAME, "td-table-content-xgspon.rpXGSponUniProf_lanStormCtrlDlfload").get_attribute("textContent") != "1000000"):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} Storm Control DLF lan Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.CLASS_NAME, "td-table-content-xgspon.rpXGSponUniProf_xlanStormCtrlBcastload").get_attribute("textContent") != "10000000"):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} Storm Control Broadcast xlan Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.CLASS_NAME, "td-table-content-xgspon.rpXGSponUniProf_xlanStormCtrlMcastload").get_attribute("textContent") != "10000000"):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} Storm Control Multicast xlan Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.CLASS_NAME, "td-table-content-xgspon.rpXGSponUniProf_xlanStormCtrlDlfload").get_attribute("textContent") != "10000000"):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} Storm Control DLF xlan Test Fail",file = open(file_name, '+a'))
                    if_error = True
                #lan tag operation                   
                if(driver.find_element(By.CLASS_NAME, "rpXGSponUniprof_lantagoperid1").get_attribute("textContent") != "Id #1: type: \"ethertype ipoe\", port-list : \"4\" ,vlan \"4094/7\""):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} lan tag operation1 Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.CLASS_NAME, "rpXGSponUniprof_lantagoperid2").get_attribute("textContent") != "Id #2: type: \"ethertype arp\", port-list : \"4\" ,vlan \"4094/7\""):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} lan tag operation2 Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.CLASS_NAME, "rpXGSponUniprof_lantagoperid3").get_attribute("textContent") != "Id #3: type: \"ethertype pppoe\", port-list : \"4\" ,vlan \"4094/7\""):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} lan tag operation3 Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.CLASS_NAME, "rpXGSponUniprof_lantagoperid4").get_attribute("textContent") != "Id #4: type: \"ethertype ipv6\", port-list : \"4\" ,vlan \"4094/7\""):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} lan tag operation4 Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.CLASS_NAME, "rpXGSponUniprof_lantagoperid5").get_attribute("textContent") != "Id #5: type: \"4094\", port-list : \"4\" ,vlan \"4094\""):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} lan tag operation5 Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.CLASS_NAME, "rpXGSponUniprof_lantagoperid6").get_attribute("textContent") != "Id #6: type: \"untag\", port-list : \"4\" ,vlan \"4094/4\""):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} lan tag operation6 Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.CLASS_NAME, "rpXGSponUniprof_lantagoperid7").get_attribute("textContent") != "Id #7: type: \"untag\", port-list : \"4\" ,vlan \"4094/7\""):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} lan tag operation7 Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.CLASS_NAME, "rpXGSponUniprof_lantagoperid8").get_attribute("textContent") != "Id #8: type: \"1\", port-list : \"4\" ,vlan \"4094\""):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} lan tag operation8 Test Fail",file = open(file_name, '+a'))
                    if_error = True
                #xlan tag operation
                if(driver.find_element(By.CLASS_NAME, "rpXGSponUniprof_xlantagoperid1").get_attribute("textContent") != "Id #1: type: \"ethertype ipoe\", port-list : \"4\" ,vlan \"4094/7\""):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} xlan tag operation1 Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.CLASS_NAME, "rpXGSponUniprof_xlantagoperid2").get_attribute("textContent") != "Id #2: type: \"ethertype arp\", port-list : \"4\" ,vlan \"4094/7\""):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} xlan tag operation2 Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.CLASS_NAME, "rpXGSponUniprof_xlantagoperid3").get_attribute("textContent") != "Id #3: type: \"ethertype pppoe\", port-list : \"4\" ,vlan \"4094/7\""):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} xlan tag operation3 Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.CLASS_NAME, "rpXGSponUniprof_xlantagoperid4").get_attribute("textContent") != "Id #4: type: \"ethertype ipv6\", port-list : \"4\" ,vlan \"4094/7\""):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} xlan tag operation4 Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.CLASS_NAME, "rpXGSponUniprof_xlantagoperid5").get_attribute("textContent") != "Id #5: type: \"4094\", port-list : \"4\" ,vlan \"4094\""):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} xlan tag operation5 Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.CLASS_NAME, "rpXGSponUniprof_xlantagoperid6").get_attribute("textContent") != "Id #6: type: \"untag\", port-list : \"4\" ,vlan \"4094/4\""):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} xlan tag operation6 Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.CLASS_NAME, "rpXGSponUniprof_xlantagoperid7").get_attribute("textContent") != "Id #7: type: \"untag\", port-list : \"4\" ,vlan \"4094/7\""):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} xlan tag operation7 Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.CLASS_NAME, "rpXGSponUniprof_xlantagoperid8").get_attribute("textContent") != "Id #8: type: \"1\", port-list : \"4\" ,vlan \"4094\""):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} xlan tag operation8 Test Fail",file = open(file_name, '+a'))
                    if_error = True
                #veip tag operation
                if(driver.find_element(By.CLASS_NAME, "rpXGSponUniprof_veiptagoperid1").get_attribute("textContent") != "Id #1: type: \"ethertype ipoe\", port-list : \"1\" ,vlan \"4094/7\""):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} veip tag operation1 Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.CLASS_NAME, "rpXGSponUniprof_veiptagoperid2").get_attribute("textContent") != "Id #2: type: \"ethertype arp\", port-list : \"1\" ,vlan \"4094/7\""):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} veip tag operation2 Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.CLASS_NAME, "rpXGSponUniprof_veiptagoperid3").get_attribute("textContent") != "Id #3: type: \"ethertype pppoe\", port-list : \"1\" ,vlan \"4094/7\""):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} veip tag operation3 Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.CLASS_NAME, "rpXGSponUniprof_veiptagoperid4").get_attribute("textContent") != "Id #4: type: \"ethertype ipv6\", port-list : \"1\" ,vlan \"4094/7\""):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} veip tag operation4 Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.CLASS_NAME, "rpXGSponUniprof_veiptagoperid5").get_attribute("textContent") != "Id #5: type: \"4094\", port-list : \"1\" ,vlan \"4094\""):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} veip tag operation5 Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.CLASS_NAME, "rpXGSponUniprof_veiptagoperid6").get_attribute("textContent") != "Id #6: type: \"untag\", port-list : \"1\" ,vlan \"4094/4\""):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} veip tag operation6 Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.CLASS_NAME, "rpXGSponUniprof_veiptagoperid7").get_attribute("textContent") != "Id #7: type: \"untag\", port-list : \"1\" ,vlan \"4094/7\""):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} veip tag operation7 Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.CLASS_NAME, "rpXGSponUniprof_veiptagoperid8").get_attribute("textContent") != "Id #8: type: \"1\", port-list : \"1\" ,vlan \"4094\""):
                    print(f"             [XPON - Profiles - UNI Profile] {uni_profile_name[check_time]} veip tag operation8 Test Fail",file = open(file_name, '+a'))
                    if_error = True


                break
        if(if_find == False):
            print(f"             [XPON - Profiles - UNI Profile] SFU Apply Not Found Test Fail",file = open(file_name, '+a'))
            if_error = True
        
        pass###




    if(if_error == False):
        print(f"[MSAN1-12161][XPON - Profiles - UNI Profile]UNI Profile Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-12161][XPON - Profiles - UNI Profile]UNI Profile Result Fail",file = open(file_name, '+a'))
    
    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def Security_Profile_Test(driver,file_name):# 正在改
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Security").click()
    if_full = False
    pro.Security_Profile_New(driver)
    pro.Security_Profile_New_Name(driver,"______xpon_security_profile_SFU")
    pro.Security_Profile_New_fdb(driver,"1024")
    pro.Security_Profile_New_Apply(driver)
    if_error = False
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [XPON - Profiles - Security Profile]Security Profile fdb Fail => 1024",file = open(file_name, '+a'))
        if_error = True
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Security").click()
    pro.Security_Profile_New(driver)
    pro.Security_Profile_New_Name(driver,"______xpon_security_profile_SFU")
    pro.Security_Profile_New_fdb(driver,"@")
    pro.Security_Profile_New_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [XPON - Profiles - Security Profile]Security Profile fdb Fail => @(#175096)",file = open(file_name, '+a'))
        if_error = True
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Security").click()
    pro.Security_Profile_New(driver)
    pro.Security_Profile_New_Name(driver,"______xpon_security_profile_SFU")
    pro.Security_Profile_New_anti(driver,True)
    pro.Security_Profile_New_fdb(driver,"1023")
    pro.Security_Profile_New_Apply(driver)
    if(mod.IsAlert(driver) == True):
        if_full = True
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
        if_full = True
    except:
        pass
    
    if(if_error == True):
        print(f"[MSAN1-12162][XPON - Profiles - Security Profile]Security Profile Config Test Fail",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-12162][XPON - Profiles - Security Profile]Security Profile Config Test Pass",file = open(file_name, '+a'))
    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def Ont_Profile_Test(driver,username,password,file_name):
    if_error = False
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    driver.switch_to.frame(0)

    # need to create name in [VoIP Common Profile], [Sip Profile], [Dial Plan Profile] pages first,
    # Ont > VoIP page need them, create them before create ONT Profile page
    # #[VoIP Common Profile]
    # driver.find_element(By.LINK_TEXT, "Voip Common").click()
    # time.sleep(5)
    # if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__() > voip_common_profile_capacity-2):
    #     driver.find_elements(By.NAME, "rpXGSponCommonProf_chkDel")[-1].click()
    #     driver.find_elements(By.NAME, "rpXGSponCommonProf_chkDel")[-2].click()
    #     pro.Voip_Common_Profile_Delete(driver) 
    # pro.Voip_Common_Profile_New(driver)      
    # pro.Voip_Common_Profile_New_Name(driver,"voip_common_SFU")
    # pro.Voip_Common_Profile_New_Apply(driver)
    # # #[Sip Profile]
    # driver.find_element(By.LINK_TEXT, "Voip Sip").click()
    # time.sleep(5)
    # if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__() > sip_profile_capacity-2):
    #     driver.find_elements(By.NAME, "rpXGSponSipProf_chkDel")[-1].click()
    #     driver.find_elements(By.NAME, "rpXGSponSipProf_chkDel")[-2].click()
    #     pro.Sip_Profile_Delete(driver)
    # pro.Sip_Profile_New(driver)
    # pro.Sip_Profile_New_Name(driver,"sip_profile_SFU") 
    # pro.Sip_Profile_New_Apply(driver)
    # # #[Dial Plan Profile]
    # driver.find_element(By.LINK_TEXT, "Voip Dial Plan").click()
    # time.sleep(5)
    # if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__() > dial_plan_profile_capacity-2):
    #     driver.find_elements(By.NAME, "rpXGSponDialPlanProf_chkDel")[-1].click()
    #     driver.find_elements(By.NAME, "rpXGSponDialPlanProf_chkDel")[-2].click()
    #     pro.Dial_Plan_Profile_Delete(driver)
    # pro.Dial_Plan_Profile_New(driver)
    # pro.Dial_Plan_Profile_New_Name(driver,"__dial_plan_SFU")        
    # pro.Dial_Plan_Profile_New_Apply(driver)


    driver.find_element(By.LINK_TEXT, "ONT").click()
    time.sleep(5)
    if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__() > ont_profile_capacity-2):
        driver.find_elements(By.NAME, "rpXGSponOntProf_chkDel")[-1].click()
        driver.find_elements(By.NAME, "rpXGSponOntProf_chkDel")[-2].click()
        pro.Ont_Profile_Delete(driver)
    ont_profile_name = ["___________xpon_ont_profile_SFU","___________xpon_ont_profile_HGU"]
    ont_profile_print_name = ["SFU","HGU"]
    for create_time in range(2):
        pro.Ont_Profile_New(driver)
        pro.Ont_Profile_New_Name(driver,ont_profile_name[create_time])
        pro.Ont_Profile_New_Service_Control(driver,True)
        pro.Ont_Profile_New_Service_lcmp_enable(driver,"L&W")
        pro.Ont_Profile_New_Service_ftp_enable(driver,"L&W")
        pro.Ont_Profile_New_Service_Http_enable(driver,"L&W")
        pro.Ont_Profile_New_Service_Https_enable(driver,"L&W")
        pro.Ont_Profile_New_Service_Snmp_enable(driver,"L&W")
        pro.Ont_Profile_New_Service_Telnet_enable(driver,"L&W")
        pro.Ont_Profile_New_Service_SSH_enable(driver,"L&W")
        pro.Ont_Profile_New_Service_Firewall_control(driver,True)
        pro.Ont_Profile_New_Service_Firewall_enable(driver,"ALL")
        pro.Ont_Profile_New_Service_Firewall_level(driver,"high")
        pro.Ont_Profile_New_Service_Dmz_control(driver,True)
        pro.Ont_Profile_New_Service_Dmz_ip(driver,"10.10.10.254")
        pro.Ont_Profile_New_Service_PoE_control(driver,True)
        pro.Ont_Profile_New_Service_PoE_management(driver,"consumption")
        pro.Ont_Profile_New_Service_PoE_mode(driver,"auto")
        pro.Ont_Profile_New_Service_Upnp_control(driver,True)
        pro.Ont_Profile_New_Service_Upnp_enable(driver,True)
        pro.Ont_Profile_New_Service_Roaming_control(driver,True)
        pro.Ont_Profile_New_Service_Roaming(driver,"90")
        pro.Ont_Profile_New_Service_Acs_control(driver,True)
        pro.Ont_Profile_New_Service_Acs_server(driver,True)
        pro.Ont_Profile_New_Service_Acs_username(driver,"12345678901234567890123456789012345678901234567")
        pro.Ont_Profile_New_Service_Acs_password(driver,"12345678901234567890123456789012345678901234567")
        pro.Ont_Profile_New_Service_Acs_url(driver,"http://12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123sssssss4567890123456789012345678901.io:10301/")
        pro.Ont_Profile_New_Service_Acs_inform(driver,True)
        pro.Ont_Profile_New_Service_Acs_interval(driver,"1000000")
        pro.Ont_Profile_New_Service_Loopguard_control(driver,True)
        pro.Ont_Profile_New_Service_Loopguard_detected(driver,"60")
        pro.Ont_Profile_New_Service_Loopguard_enable(driver,True)
        pro.Ont_Profile_New_Service_Loopguard_recovery(driver,"3600")
        pro.Ont_Profile_New_Service_StormControl_control(driver,True)
        pro.Ont_Profile_New_Service_StormControl_threshold(driver,"65535")
        driver.find_element(By.LINK_TEXT, "Lan").click()
        index = 0
        pro.Ont_Profile_New_Lan_Active(driver,index,True)
        pro.Ont_Profile_New_Lan_Static_Mode(driver,index,True)
        pro.Ont_Profile_New_Lan_IP(driver,index,f"192.168.{index}.100")
        pro.Ont_Profile_New_Lan_Mask(driver,index,"255.255.255.0")
        pro.Ont_Profile_New_Lan_DHCP_Mode(driver,index,"server")
        pro.Ont_Profile_New_Lan_PoolBegin(driver,index,"192.168.0.200")
        pro.Ont_Profile_New_Lan_PoolEnd(driver,index,"192.168.0.201")
        pro.Ont_Profile_New_Lan_DnsType(driver,index,"static")
        pro.Ont_Profile_New_Lan_priDns(driver,index,"192.168.0.1")
        pro.Ont_Profile_New_Lan_secDns(driver,index,"192.168.0.2")
        index = 1
        pro.Ont_Profile_New_Lan_Active(driver,index,True)
        pro.Ont_Profile_New_Lan_Static_Mode(driver,index,True)
        pro.Ont_Profile_New_Lan_IP(driver,index,f"192.168.{index}.100")
        pro.Ont_Profile_New_Lan_Mask(driver,index,"255.255.255.0")
        pro.Ont_Profile_New_Lan_DHCP_Mode(driver,index,"relay")
        pro.Ont_Profile_New_Lan_RelayServerIp(driver,index,"192.168.1.201")
        for index in range(7):
            pro.Ont_Profile_New_Lan_Active(driver,index+2,True)
            pro.Ont_Profile_New_Lan_Static_Mode(driver,index+2,True)
            pro.Ont_Profile_New_Lan_IP(driver,index+2,f"192.168.{index+2}.100")
            pro.Ont_Profile_New_Lan_Mask(driver,index+2,"255.255.255.0")
            pro.Ont_Profile_New_Lan_DHCP_Mode(driver,index+2,"disable")
        driver.find_element(By.LINK_TEXT, "Wan").click()
        index = 1
        pro.Ont_Profile_New_Wan_Active(driver,index,True)
        pro.Ont_Profile_New_Wan_Default(driver,index,True)
        pro.Ont_Profile_New_Wan_Enable(driver,index,True)
        pro.Ont_Profile_New_Wan_Nat(driver,index,True)
        pro.Ont_Profile_New_Wan_Mode(driver,index,"static")
        pro.Ont_Profile_New_Wan_Address(driver,index,"100.100.100.1")
        pro.Ont_Profile_New_Wan_Mask(driver,index,"255.255.255.0")
        pro.Ont_Profile_New_Wan_Gateway(driver,index,"100.100.100.254")
        pro.Ont_Profile_New_Wan_priDns(driver,index,"100.100.100.1")
        pro.Ont_Profile_New_Wan_secDns(driver,index,"100.100.100.2")
        pro.Ont_Profile_New_Wan_type(driver,index,"pppoe")
        pro.Ont_Profile_New_Wan_username(driver,index,"123456789012345")
        pro.Ont_Profile_New_Wan_password(driver,index,"123456789012345")
        pro.Ont_Profile_New_Wan_port_list(driver,index,index)
        pro.Ont_Profile_New_Wan_wifi_2_4_ssid(driver,index,index)
        pro.Ont_Profile_New_Wan_wifi_5_ssid(driver,index,index)
        pro.Ont_Profile_New_Wan_vlan(driver,index,"4094")
        pro.Ont_Profile_New_Wan_priority(driver,index,"7")
        pro.Ont_Profile_New_Wan_mvlan(driver,index,"4000")
        pro.Ont_Profile_New_Wan_service(driver,index,"data")
        index = 2
        pro.Ont_Profile_New_Wan_Active(driver,index,True)
        pro.Ont_Profile_New_Wan_Default(driver,index,False)
        pro.Ont_Profile_New_Wan_Enable(driver,index,True)
        pro.Ont_Profile_New_Wan_Nat(driver,index,True)
        pro.Ont_Profile_New_Wan_Mode(driver,index,"dynamic")
        pro.Ont_Profile_New_Wan_priDns(driver,index,"100.100.100.1")
        pro.Ont_Profile_New_Wan_secDns(driver,index,"100.100.100.2")
        pro.Ont_Profile_New_Wan_type(driver,index,"ipoe")
        pro.Ont_Profile_New_Wan_port_list(driver,index,index)
        pro.Ont_Profile_New_Wan_wifi_2_4_ssid(driver,index,index)
        pro.Ont_Profile_New_Wan_wifi_5_ssid(driver,index,index)
        pro.Ont_Profile_New_Wan_vlan(driver,index,"4094")
        pro.Ont_Profile_New_Wan_priority(driver,index,"7")
        pro.Ont_Profile_New_Wan_mvlan(driver,index,"4000")
        pro.Ont_Profile_New_Wan_service(driver,index,"data")
        for index in range(2):
            pro.Ont_Profile_New_Wan_Active(driver,index+3,True)
            pro.Ont_Profile_New_Wan_Default(driver,index+3,False)
            pro.Ont_Profile_New_Wan_Enable(driver,index+3,True)
            pro.Ont_Profile_New_Wan_Nat(driver,index+3,True)
            pro.Ont_Profile_New_Wan_Mode(driver,index+3,"dynamic")
            pro.Ont_Profile_New_Wan_priDns(driver,index+3,"100.100.100.1")
            pro.Ont_Profile_New_Wan_secDns(driver,index+3,"100.100.100.2")
            pro.Ont_Profile_New_Wan_type(driver,index+3,"bridge")
            pro.Ont_Profile_New_Wan_port_list(driver,index+3,index+3)
            pro.Ont_Profile_New_Wan_wifi_2_4_ssid(driver,index+3,index+3)
            pro.Ont_Profile_New_Wan_wifi_5_ssid(driver,index+3,index+3)
            pro.Ont_Profile_New_Wan_vlan(driver,index+3,"4094")
            pro.Ont_Profile_New_Wan_priority(driver,index+3,"7")
            pro.Ont_Profile_New_Wan_mvlan(driver,index+3,"4000")
            pro.Ont_Profile_New_Wan_service(driver,index+3,"data")
        for index in range(4):
            pro.Ont_Profile_New_Wan_Active(driver,index+5,True)
            pro.Ont_Profile_New_Wan_Default(driver,index+5,False)
            pro.Ont_Profile_New_Wan_Enable(driver,index+5,True)
            pro.Ont_Profile_New_Wan_Nat(driver,index+5,True)
            pro.Ont_Profile_New_Wan_Mode(driver,index+5,"dynamic")
            pro.Ont_Profile_New_Wan_priDns(driver,index+5,"100.100.100.1")
            pro.Ont_Profile_New_Wan_secDns(driver,index+5,"100.100.100.2")
            pro.Ont_Profile_New_Wan_type(driver,index+5,"bridge")
            pro.Ont_Profile_New_Wan_vlan(driver,index+5,"4094")
            pro.Ont_Profile_New_Wan_priority(driver,index+5,"7")
            pro.Ont_Profile_New_Wan_mvlan(driver,index+5,"4000")
            pro.Ont_Profile_New_Wan_service(driver,index+5,"data")
        driver.find_element(By.LINK_TEXT, "Wifi 2.4g").click()
        index = 1
        pro.Ont_Profile_New_WiFi_2_4g_Active(driver,index,True)
        pro.Ont_Profile_New_WiFi_2_4g_Enable(driver,index,True)
        pro.Ont_Profile_New_WiFi_2_4g_ssid(driver,index,f"123456789012345678901234567890{index}")
        pro.Ont_Profile_New_WiFi_2_4g_password(driver,index,f"123456789012345678901234567890{index}")
        pro.Ont_Profile_New_WiFi_2_4g_Channel(driver,index,"13") #*ori: auto
        pro.Ont_Profile_New_WiFi_2_4g_Bandwidth(driver,index,"20/40MHz") #*ori: 20MHz
        pro.Ont_Profile_New_WiFi_2_4g_maxClients(driver,index,"32")
        pro.Ont_Profile_New_WiFi_2_4g_securityMode(driver,index,"None")
        pro.Ont_Profile_New_WiFi_2_4g_txPower(driver,index,"100%") #*ori: 20%
        index = 2
        pro.Ont_Profile_New_WiFi_2_4g_Active(driver,index,True)
        pro.Ont_Profile_New_WiFi_2_4g_Enable(driver,index,True)
        pro.Ont_Profile_New_WiFi_2_4g_ssid(driver,index,f"123456789012345678901234567890{index}")
        pro.Ont_Profile_New_WiFi_2_4g_password(driver,index,f"123456789012345678901234567890{index}")
        pro.Ont_Profile_New_WiFi_2_4g_securityMode(driver,index,"WPA2-PSK")
        # 之後要刪掉
        # pro.Ont_Profile_New_WiFi_2_4g_Channel(driver,index,"auto")
        # pro.Ont_Profile_New_WiFi_2_4g_Bandwidth(driver,index,"20/40MHz")
        # pro.Ont_Profile_New_WiFi_2_4g_maxClients(driver,index,"32")
        # pro.Ont_Profile_New_WiFi_2_4g_txPower(driver,index,"100%")
        for index in range(2):
            pro.Ont_Profile_New_WiFi_2_4g_Active(driver,index+3,True)
            pro.Ont_Profile_New_WiFi_2_4g_Enable(driver,index+3,True)
            pro.Ont_Profile_New_WiFi_2_4g_ssid(driver,index+3,f"123456789012345678901234567890{index+3}")
            pro.Ont_Profile_New_WiFi_2_4g_password(driver,index+3,f"123456789012345678901234567890{index+3}")
            pro.Ont_Profile_New_WiFi_2_4g_securityMode(driver,index+3,"WEP")
            # 之後要刪掉
            # pro.Ont_Profile_New_WiFi_2_4g_Channel(driver,index+3,"auto")
            # pro.Ont_Profile_New_WiFi_2_4g_Bandwidth(driver,index+3,"20/40MHz")
            # pro.Ont_Profile_New_WiFi_2_4g_maxClients(driver,index+3,"32")
            # pro.Ont_Profile_New_WiFi_2_4g_txPower(driver,index+3,"100%")
        driver.find_element(By.LINK_TEXT, "Wifi 5g").click()
        index = 1
        pro.Ont_Profile_New_WiFi_5g_Active(driver,index,True)
        pro.Ont_Profile_New_WiFi_5g_Enable(driver,index,True)
        pro.Ont_Profile_New_WiFi_5g_ssid(driver,index,f"123456789012345678901234567890{index}")
        pro.Ont_Profile_New_WiFi_5g_password(driver,index,f"123456789012345678901234567890{index}")
        pro.Ont_Profile_New_WiFi_5g_Channel(driver,index,"128") #* ori: auto
        pro.Ont_Profile_New_WiFi_5g_Bandwidth(driver,index,"20/40/80MHz") #* ori: 20MHz
        pro.Ont_Profile_New_WiFi_5g_maxClients(driver,index,"32")
        pro.Ont_Profile_New_WiFi_5g_securityMode(driver,index,"None")
        pro.Ont_Profile_New_WiFi_5g_txPower(driver,index,"100%") #* ori: 20%
        index = 2
        pro.Ont_Profile_New_WiFi_5g_Active(driver,index,True)
        pro.Ont_Profile_New_WiFi_5g_Enable(driver,index,True)
        pro.Ont_Profile_New_WiFi_5g_ssid(driver,index,f"123456789012345678901234567890{index}")
        pro.Ont_Profile_New_WiFi_5g_password(driver,index,f"123456789012345678901234567890{index}")
        pro.Ont_Profile_New_WiFi_5g_securityMode(driver,index,"WPA2-PSK")
        # 之後要刪掉
        # pro.Ont_Profile_New_WiFi_5g_Channel(driver,index,"auto")
        # pro.Ont_Profile_New_WiFi_5g_Bandwidth(driver,index,"20/40/80MHz")
        # pro.Ont_Profile_New_WiFi_5g_maxClients(driver,index,"32")
        # pro.Ont_Profile_New_WiFi_5g_txPower(driver,index,"100%")
        for index in range(2):
            pro.Ont_Profile_New_WiFi_5g_Active(driver,index+3,True)
            pro.Ont_Profile_New_WiFi_5g_Enable(driver,index+3,True)
            pro.Ont_Profile_New_WiFi_5g_ssid(driver,index+3,f"123456789012345678901234567890{index+3}")
            pro.Ont_Profile_New_WiFi_5g_password(driver,index+3,f"123456789012345678901234567890{index+3}")
            pro.Ont_Profile_New_WiFi_5g_securityMode(driver,index+3,"WEP")
            # 之後要刪掉
            # pro.Ont_Profile_New_WiFi_5g_Channel(driver,index+3,"auto")
            # pro.Ont_Profile_New_WiFi_5g_Bandwidth(driver,index+3,"20/40/80MHz")
            # pro.Ont_Profile_New_WiFi_5g_maxClients(driver,index+3,"32")
            # pro.Ont_Profile_New_WiFi_5g_txPower(driver,index+3,"100%")
        driver.find_element(By.LINK_TEXT, "Acl").click()
        for index in range(16):
            pro.Ont_Profile_New_Acl_Active(driver,index+1,True)
            pro.Ont_Profile_New_Acl_Name(driver,index+1,"DEFVAL")
        
        # voip page             
                                                                          
        driver.find_element(By.LINK_TEXT, "Voip").click()
        index = 1
        pro.Ont_Profile_New_Voip_Uniport(driver,index,"1")
        pro.Ont_Profile_New_Voip_Vlan(driver,index,"4094")
        #* those three will show "not a valid number" 
        pro.Ont_Profile_New_Voip_Voicemail_Expiration_Time(driver,index,"3600")
        pro.Ont_Profile_New_Voip_Release_Timer(driver,index,"30")
        pro.Ont_Profile_New_Voip_ROH_Timer(driver,index,"30")
        for index in range(1,3):            
            pro.Ont_Profile_New_Voip_Enable(driver,index,True)
            pro.Ont_Profile_New_Voip_Active(driver,index,True)            
            pro.Ont_Profile_New_Voip_Username(driver,index,"1234567890123456789012345678901234567890123456789")#49
            pro.Ont_Profile_New_Voip_Password(driver,index,"1234567890123456789012345")#25
            pro.Ont_Profile_New_Voip_User_Part_AOR(driver,index,"123456789012345678901234567890123456789012345678901234567890123")#63
            pro.Ont_Profile_New_Voip_Display_Name(driver,index,"123456789012345678901234567890123456789012345678901234567890123")#63
            pro.Ont_Profile_New_Voip_Voicemail_Server_SIP_URI(driver,index,"123456789012345678901234567890123456789012345678901234567890123")#63            
            time.sleep(2)
            #*
            pro.Ont_Profile_New_Voip_VoIP_Comment_Profile(driver,index,"voip_common_SFU")#{rpXGSponVoipComProfs}
            pro.Ont_Profile_New_Voip_VoIP_Sip_Profile(driver,index,"sip_profile_SFU")#{rpXGSponVoipSipProfs}
            pro.Ont_Profile_New_Voip_VoIP_Dial_Plan_Profile(driver,index,"__dial_plan_SFU")#{rpXGSponVoipDialPlanProfs}
        index = 2
        pro.Ont_Profile_New_Voip_Uniport(driver,index,"4") 
        pro.Ont_Profile_New_Voip_Vlan(driver,index,"4000")
        #* those three will show "not a valid number" 
        pro.Ont_Profile_New_Voip_Voicemail_Expiration_Time(driver,index,"0")
        pro.Ont_Profile_New_Voip_Release_Timer(driver,index,"0")
        pro.Ont_Profile_New_Voip_ROH_Timer(driver,index,"0")
        time.sleep(2)

        # poe page
        driver.find_element(By.LINK_TEXT, "Poe").click()
        for index in range (1,5):
            pro.Ont_Profile_New_Poe_Active(driver,index,True)
            pro.Ont_Profile_New_Poe_Enable(driver,index,True)            
        pro.Ont_Profile_New_Poe_Priority(driver,1,"critical")
        pro.Ont_Profile_New_Poe_Max(driver,1,"class 1")
        pro.Ont_Profile_New_Poe_Priority(driver,2,"high")
        pro.Ont_Profile_New_Poe_Max(driver,2,"class 2")
        pro.Ont_Profile_New_Poe_Priority(driver,3,"low")
        pro.Ont_Profile_New_Poe_Max(driver,3,"class 3")
        pro.Ont_Profile_New_Poe_Priority(driver,4,"critical")
        pro.Ont_Profile_New_Poe_Max(driver,4,"class 4")

        pro.Ont_Profile_New_Apply(driver)
        if(mod.IsAlert(driver) == True):
            print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[create_time]} Valid Value Alert Test Fail",file = open(file_name, '+a'))
            if_error = True
        try:            
            time.sleep(20)
            driver.find_element(By.NAME, "rperror_btnBack").click()
            print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[create_time]} Apply Fail",file = open(file_name, '+a'))
            if_error = True
        except:
            pass
        time.sleep(5)
    for check_time in range(2):
        if_find = False
        for index in range(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntProf_name").__len__()):
            try:
                driver.switch_to.default_content()
                driver.find_element(By.ID, "userContinue").click()
                driver.switch_to.frame(0)
            except:
                try:
                    driver.switch_to.default_content()
                    driver.find_element(By.CLASS_NAME, "ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-front.ui-draggable")
                    driver.find_element(By.ID, "lg_user").send_keys(username)
                    driver.find_element(By.ID, "lg_pass").send_keys(password)
                    driver.find_element(By.ID, "userLogin").click()
                    driver.switch_to.frame(0)
                except:
                    driver.switch_to.frame(0)
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntProf_name")[-(index+1)].get_attribute("textContent") == ont_profile_name[check_time]):
                if_find = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntProf_controlFirewall")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} Firewall control Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntProf_firewallEnable")[-(index+1)].get_attribute("textContent") != "ALL"):
                    print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} Firewall enable Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntProf_firewallLevel")[-(index+1)].get_attribute("textContent") != "high"):
                    print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} Firewall level Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntProf_controlDmz")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} Dmz control Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntProf_dmzIp")[-(index+1)].get_attribute("textContent") != "10.10.10.254"):
                    print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} Dmz ip Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntProf_controlPower")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} POE control Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntProf_powerManagement")[-(index+1)].get_attribute("textContent") != "consumption"):
                    print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} POE management Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntProf_powerMode")[-(index+1)].get_attribute("textContent") != "auto"):
                    print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} POE mode Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntProf_controlUpnp")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} Upnp control Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntProf_upnpEnable")[-(index+1)].get_attribute("textContent") != "enable"):
                    print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} Upnp enable Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntProf_controlRoaming")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} Roaming control Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntProf_roaming")[-(index+1)].get_attribute("textContent") != "90"):
                    print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} Roaming value Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntProf_controlLoopguard")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} Loopguard control Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntProf_loopguardEnable")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} Loopguard enablie Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntProf_loopguardDetectedTime")[-(index+1)].get_attribute("textContent") != "60"):
                    print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} Loopguard detected time Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntProf_loopguardRecoveryTime")[-(index+1)].get_attribute("textContent") != "3600"):
                    print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} Loopguard recovery time Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntProf_controlStorm")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} Stormcontrol control Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntProf_stormThreshold")[-(index+1)].get_attribute("textContent") != "65535"):
                    print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} Stormcontrol control threshold Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "rpXGSponOntProf_lan_0")[-(index+1)].get_attribute("textContent") != 'Lan #0: ip "192.168.0.100", mask "255.255.255.0", dhcpMode: Server, begin "192.168.0.200", end "192.168.0.201", dns: static, priDns "192.168.0.1", secDns "192.168.0.2"'):
                    print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} Lan0 Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "rpXGSponOntProf_lan_1")[-(index+1)].get_attribute("textContent") != 'Lan #1: ip "192.168.1.100", mask "255.255.255.0", dhcpMode: Relay, relay ip "192.168.1.201", dns: proxy'):
                    print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} Lan1 Test Fail",file = open(file_name, '+a'))
                    if_error = True
                for lan in range(7):
                    if(driver.find_elements(By.CLASS_NAME, f"rpXGSponOntProf_lan_{lan+2}")[-(index+1)].get_attribute("textContent") != f'Lan #{lan+2}: ip "192.168.{lan+2}.100", mask "255.255.255.0", dns: proxy'):
                        print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} Lan{lan+2} Test Fail",file = open(file_name, '+a'))
                        if_error = True
                if(driver.find_elements(By.CLASS_NAME, "rpXGSponOntProf_wan_1")[-(index+1)].get_attribute("textContent") != 'Wan #1: enable, default, nat, static ip "100.100.100.1", mask "255.255.255.0", gateway "100.100.100.254", priDns "100.100.100.1", secDns "100.100.100.2", connect type: pppoe, user "123456789012345", password "123456789012345", portbinding: "1", wifibinding: "1", wifi5gbinding: "1", vlan: 4094, priority: 7, mvlan: 4000, service: "data"'):
                    print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} Wan1 Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "rpXGSponOntProf_wan_2")[-(index+1)].get_attribute("textContent") != 'Wan #2: enable, nat, dynamic priDns "100.100.100.1", secDns "100.100.100.2", connect type: ipoe, portbinding: "2", wifibinding: "2", wifi5gbinding: "2", vlan: 4094, priority: 7, mvlan: 4000, service: "data"'):
                    print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} Wan2 Test Fail",file = open(file_name, '+a'))
                    if_error = True
                for wan in range(2):
                    if(driver.find_elements(By.CLASS_NAME, f"rpXGSponOntProf_wan_{wan+3}")[-(index+1)].get_attribute("textContent") != f'Wan #{wan+3}: enable, nat, dynamic priDns "100.100.100.1", secDns "100.100.100.2", connect type: bridge, portbinding: "{wan+3}", wifibinding: "{wan+3}", wifi5gbinding: "{wan+3}", vlan: 4094, priority: 7, mvlan: 4000, service: "data"'):
                        print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} Wan{wan+3} Test Fail",file = open(file_name, '+a'))
                        if_error = True
                for wan in range(4):
                    if(driver.find_elements(By.CLASS_NAME, f"rpXGSponOntProf_wan_{wan+5}")[-(index+1)].get_attribute("textContent") != f'Wan #{wan+5}: enable, nat, dynamic priDns "100.100.100.1", secDns "100.100.100.2", connect type: bridge, vlan: 4094, priority: 7, mvlan: 4000, service: "data"'):
                        print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} Wan{wan+5} Test Fail",file = open(file_name, '+a'))
                        if_error = True
                # Wifi全部待確認                                                                                        #* ori: Wifi 2.4 #1: enable and broadcast ssid, bandwidth: 20MHz, maxClients: 32, securityMode: None, txPower: 20, SSID: 1234567890123456789012345678901, password: 1234567890123456789012345678901
                if(driver.find_elements(By.CLASS_NAME, "rpXGSponOntProf_wifi2_1")[-(index+1)].get_attribute("textContent") != 'Wifi 2.4 #1: enable and broadcast ssid, channel: 13, bandwidth: 20/40MHz, maxClients: 32, securityMode: None, txPower: 100, SSID: 1234567890123456789012345678901, password: 1234567890123456789012345678901'):
                    print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} WiFi 2.4g 1 Test Fail(#175106)",file = open(file_name, '+a'))
                    if_error = True                                                                                    #* ori Wifi 2.4 #2: enable and broadcast ssid, bandwidth: 20/40MHz, maxClients: 32, securityMode: WPA2-PSK, txPower: 100, SSID: 1234567890123456789012345678902, password: 1234567890123456789012345678902
                if(driver.find_elements(By.CLASS_NAME, "rpXGSponOntProf_wifi2_2")[-(index+1)].get_attribute("textContent") != 'Wifi 2.4 #2: enable and broadcast ssid, bandwidth: 20/40MHz, maxClients: 32, securityMode: WPA2-PSK, txPower: 100, SSID: 1234567890123456789012345678902, password: 1234567890123456789012345678902'):
                    print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} WiFi 2.4g 2 Test Fail(#175106)",file = open(file_name, '+a'))
                    if_error = True
                for wifi in range(2):                                                                                                     #Wifi 2.4 #4: enable and broadcast ssid, bandwidth: 20/40MHz, maxClients: 32, securityMode: WEP, txPower: 100, SSID: 1234567890123456789012345678904, password: 1234567890123456789012345678904
                    if(driver.find_elements(By.CLASS_NAME, f"rpXGSponOntProf_wifi2_{wifi+3}")[-(index+1)].get_attribute("textContent") != f'Wifi 2.4 #{wifi+3}: enable and broadcast ssid, bandwidth: 20/40MHz, maxClients: 32, securityMode: WEP, txPower: 100, SSID: 123456789012345678901234567890{wifi+3}, password: 123456789012345678901234567890{wifi+3}'):
                        print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} WiFi 2.4g {wifi+3} Test Fail(#175106)",file = open(file_name, '+a'))
                        if_error = True                                                                                  #* ori: Wan #1: enable and broadcast ssid, bandwidth: 20MHz, maxClients: 32, securityMode: None, txPower: 20, SSID: 1234567890123456789012345678901, password: 1234567890123456789012345678901
                if(driver.find_elements(By.CLASS_NAME, "rpXGSponOntProf_wifi5_1")[-(index+1)].get_attribute("textContent") != 'Wifi 5 #1: enable and broadcast ssid, channel: 128, bandwidth: 20/40/80MHz, maxClients: 32, securityMode: None, txPower: 100, SSID: 1234567890123456789012345678901, password: 1234567890123456789012345678901'):
                    print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} WiFi 5g 1 Test Fail(#175106)",file = open(file_name, '+a'))
                    if_error = True                                                                                      #* ori: Wan #2: enable and broadcast ssid, channel: 36, bandwidth: 20/40MHz, maxClients: 32, securityMode: WPA2-PSK, txPower: 40, SSID: 1234567890123456789012345678902, password: 1234567890123456789012345678902
                if(driver.find_elements(By.CLASS_NAME, "rpXGSponOntProf_wifi5_2")[-(index+1)].get_attribute("textContent") != 'Wifi 5 #2: enable and broadcast ssid, bandwidth: 20/40/80MHz, maxClients: 32, securityMode: WPA2-PSK, txPower: 100, SSID: 1234567890123456789012345678902, password: 1234567890123456789012345678902'):
                    print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} WiFi 5g 2 Test Fail(#175106)",file = open(file_name, '+a'))
                    if_error = True
                for wifi in range(2):
                    if(driver.find_elements(By.CLASS_NAME, f"rpXGSponOntProf_wifi5_{wifi+3}")[-(index+1)].get_attribute("textContent") != f'Wifi 5 #{wifi+3}: enable and broadcast ssid, bandwidth: 20/40/80MHz, maxClients: 32, securityMode: WEP, txPower: 100, SSID: 123456789012345678901234567890{wifi+3}, password: 123456789012345678901234567890{wifi+3}'):
                        print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} WiFi 5g {wifi+3} Test Fail(#175106)",file = open(file_name, '+a'))
                        if_error = True
                for acl in range(16):
                    if(driver.find_elements(By.CLASS_NAME, f"rpXGSponOntProf_acl_{acl+1}")[-(index+1)].get_attribute("textContent") != f'Acl #{acl+1}: profile DEFVAL'):
                        print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} Acl{acl+1} Test Fail",file = open(file_name, '+a'))
                        if_error = True
                if(driver.find_elements(By.CLASS_NAME, "rpXGSponOntProf_svc_longInfo")[-(index+1)].get_attribute("textContent") != 'ftp: l&w 21, http: l&w 80, https: l&w 443, snmp: l&w 161, telnet: l&w 23, ssh: l&w 22, icmp: l&w'):
                    print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} Ont service Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "rpXGSponOntProf_acs_longInfo")[-(index+1)].get_attribute("textContent") != 'server: enable username 12345678901234567890123456789012345678901234567 password 12345678901234567890123456789012345678901234567 url http://12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123sssssss4567890123456789012345678901.io:10301/, inform: enable interval 1000000'):
                    print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} Acs Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "rpXGSponvoipProf_1")[-(index+1)].get_attribute("textContent") != "idx:1 portId:1 active:ON VmailExtimer:3600 VlanId:4094 RelTimer:30 RohTimer:30 comProf:voip_common_SFU sipProf:sip_profile_SFU dialplanProf:__dial_plan_SFU Aor:123456789012345678901234567890123456789012345678901234567890123 Dispname:123456789012345678901234567890123456789012345678901234567890123 Username:1234567890123456789012345678901234567890123456789 Password:1234567890123456789012345 VmailUri:123456789012345678901234567890123456789012345678901234567890123"):
                    print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} VoIP 1 Test Fail",file = open(file_name, '+a'))
                    if_error = True                    
                if(driver.find_elements(By.CLASS_NAME, "rpXGSponvoipProf_2")[-(index+1)].get_attribute("textContent") != "idx:2 portId:4 active:ON VmailExtimer:0 VlanId:4000 RelTimer:0 RohTimer:0 comProf:voip_common_SFU sipProf:sip_profile_SFU dialplanProf:__dial_plan_SFU Aor:123456789012345678901234567890123456789012345678901234567890123 Dispname:123456789012345678901234567890123456789012345678901234567890123 Username:1234567890123456789012345678901234567890123456789 Password:1234567890123456789012345 VmailUri:123456789012345678901234567890123456789012345678901234567890123"):
                    print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} VoIP 2 Test Fail",file = open(file_name, '+a'))
                    if_error = True                   
                poe_array = ['critical','high','low','critical']    
                for poe_num in range(1,5):
                    if(driver.find_elements(By.CLASS_NAME, f"rpXGSponOntProf_poe_{poe_num}")[-(index+1)].get_attribute("textContent") != f"Poe #1_{poe_num}: enable, priority: {poe_array[poe_num-1]}, max: class {poe_num}"):
                        print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} Poe {poe_num} Test Fail",file = open(file_name, '+a'))
                        if_error = True                     
                
                break
        if(if_find == False):
            print(f"             [XPON - Profiles - Ont Profile] {ont_profile_print_name[check_time]} Not Found Test Fail",file = open(file_name, '+a'))
            if_error = True
    if(if_error == False):
        print(f"[MSAN1-12163][XPON - Profiles - Ont Profile] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-12163][XPON - Profiles - Ont Profile] Result Fail",file = open(file_name, '+a'))
    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def Sip_Profile_Test(driver,file_name):
    if_error = False
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    time.sleep(5)
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Voip Sip").click()
    time.sleep(5)
    if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__() > sip_profile_capacity-2):
        driver.find_elements(By.NAME, "rpXGSponSipProf_chkDel")[-1].click()
        driver.find_elements(By.NAME, "rpXGSponSipProf_chkDel")[-2].click()
        pro.Sip_Profile_Delete(driver)
    sip_profile_name = ["sip_profile_SFU","sip_profile_HGU"]
    sip_profile_print_name = ["SFU","HGU"]
    for create_time in range(2):
        pro.Sip_Profile_New(driver)
        pro.Sip_Profile_New_Name(driver,sip_profile_name[create_time])
        pro.Sip_Profile_New_PSA(driver,"123456789012345678901234567890123456789012345678901234567890123")
        pro.Sip_Profile_New_OPA(driver,"123456789012345678901234567890123456789012345678901234567890123")
        pro.Sip_Profile_New_PD(driver,"1.1.1.254")
        pro.Sip_Profile_New_SD(driver,"2.2.2.254")
        pro.Sip_Profile_New_RET(driver,"25200")
        pro.Sip_Profile_New_RHST(driver,"360")
        pro.Sip_Profile_New_HPU(driver,"123456789012345678901234567890123456789012345678901234567890123")
        pro.Sip_Profile_New_SR(driver,"123456789012345678901234567890123456789012345678901234567890123")
        pro.Sip_Profile_New_S(driver,"1234")
        # time.sleep(3)
        pro.Sip_Profile_New_CI_cal_num(driver,True)
        # time.sleep(1)
        pro.Sip_Profile_New_CI_cal_nam(driver,True)
        # time.sleep(1)
        pro.Sip_Profile_New_CI_cid_bio(driver,True)
        # time.sleep(1)
        pro.Sip_Profile_New_CI_cid_num(driver,True)
        # time.sleep(1)
        pro.Sip_Profile_New_CI_cid_nam(driver,True)
        # time.sleep(1)
        pro.Sip_Profile_New_CI_ACR(driver,True)
        # time.sleep(1)
        pro.Sip_Profile_New_CW_cal_wai(driver,True)
        # time.sleep(1)
        pro.Sip_Profile_New_CW_cid_ann(driver,True)
        # time.sleep(1)
        pro.Sip_Profile_New_CPOT_3way(driver,True)
        # time.sleep(1)
        pro.Sip_Profile_New_CPOT_cal_tra(driver,True)
        # time.sleep(1)
        pro.Sip_Profile_New_CPOT_cal_hol(driver,True)
        # time.sleep(1)
        pro.Sip_Profile_New_CPOT_cal_par(driver,True)
        # time.sleep(1)
        pro.Sip_Profile_New_CPOT_not_dis(driver,True)
        # time.sleep(1)
        pro.Sip_Profile_New_CPOT_flash(driver,True)
        # time.sleep(1)
        pro.Sip_Profile_New_CPOT_origin(driver,True)
        # time.sleep(1)
        pro.Sip_Profile_New_CPOT_6way(driver,True)
        # time.sleep(1)
        pro.Sip_Profile_New_CP_spl_rin(driver,True)
        # time.sleep(1)
        pro.Sip_Profile_New_CP_dia_ton(driver,True)
        # time.sleep(1)
        pro.Sip_Profile_New_CP_vis_ind(driver,True)
        # time.sleep(1)
        pro.Sip_Profile_New_CP_cal_for(driver,True)
        # time.sleep(1)
        pro.Sip_Profile_New_DC_enable(driver,True)
        # time.sleep(1)
        pro.Sip_Profile_New_DC_dia_opt(driver,True)
        # time.sleep(1)
        pro.Sip_Profile_New_DCU(driver,"123456789012345678901234567890123456789012345678901234567890123")
        pro.Sip_Profile_New_BLAU(driver,"123456789012345678901234567890123456789012345678901234567890123")
        pro.Sip_Profile_New_CFU(driver,"123456789012345678901234567890123456789012345678901234567890123")
        pro.Sip_Profile_New_Apply(driver)
        if(mod.IsAlert(driver) == True):
            print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[create_time]} Valid Value Alert Test Fail",file = open(file_name, '+a'))
            if_error = True
        try:
            driver.find_element(By.NAME, "rperror_btnBack").click()
            print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[create_time]} Apply Fail",file = open(file_name, '+a'))
            if_error = True
        except:
            pass
        time.sleep(5)
    for check_time in range(2):
        if_find = False
        for index in range(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponSipProf_name").__len__()):
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponSipProf_name")[-(index+1)].get_attribute("textContent") == sip_profile_name[check_time]):
                if_find = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_proxyAddr")[-(index+1)].get_attribute("textContent") != "123456789012345678901234567890123456789012345678901234567890123"):
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} proxy service address Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_outbandAddr")[-(index+1)].get_attribute("textContent") != "123456789012345678901234567890123456789012345678901234567890123"):
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} outbound proxy address Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_priDns")[-(index+1)].get_attribute("textContent") != "1.1.1.254"):
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} primary dns Test Fail(#175098)",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_secDns")[-(index+1)].get_attribute("textContent") != "2.2.2.254"):
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} secondary dns Test Fail(#175098)",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_regExpTime")[-(index+1)].get_attribute("textContent") != "25200"):
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} registration expiration time Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_reregHeadStartTime")[-(index+1)].get_attribute("textContent") != "360"):
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} re-registration head start time Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_hostPartUri")[-(index+1)].get_attribute("textContent") != "123456789012345678901234567890123456789012345678901234567890123"):
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} host part uri Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_registrar")[-(index+1)].get_attribute("textContent") != "123456789012345678901234567890123456789012345678901234567890123"):
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} sip registrar Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_softswitch")[-(index+1)].get_attribute("textContent") != "1234"):
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} softswitch Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_calNum")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} caller id cal-num Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_calNam")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} caller id cal-nam Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_cidBlo")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} caller id cid-blo Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_cidNum")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} caller id cid-num Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_cidNam")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} caller id cid-nam Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_acr")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} caller id ACR Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_calWai")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} call waiting cal-wai Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_cidAnn")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} call waiting cid-ann Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_3way")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} call progress or transfer 3way Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_calTra")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} call progress or transfer cal-tra Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_calHol")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} call progress or transfer cal-hol Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_calPar")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} call progress or transfer cal-par Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_notDis")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} call progress or transfer not-dis Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_flash")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} call progress or transfer flash Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_origin")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} call progress or transfer origin Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_6way")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} call progress or transfer 6way Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_splRin")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} call presentation spl-rin Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_diaTon")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Sip Profile]ip Profile {sip_profile_print_name[check_time]} call presentation dia-ton Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_visInd")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} call presentation vis-ind Test Fail(#175100)",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_calFor")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} call presentation cal-for Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_enable")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} direction connect enable Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_diaOpt")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} direction connect dia-opt Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_dirConUri")[-(index+1)].get_attribute("textContent") != "123456789012345678901234567890123456789012345678901234567890123"):
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} direction connect uri Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_briLineAgentUri")[-(index+1)].get_attribute("textContent") != "123456789012345678901234567890123456789012345678901234567890123"):
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} bridged line agent uri Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_conFactUri")[-(index+1)].get_attribute("textContent") != "123456789012345678901234567890123456789012345678901234567890123"):
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} conference factory uri Test Fail",file = open(file_name, '+a'))
                    if_error = True
                break
        if(if_find == False):
            print(f"             Sip Profile {sip_profile_print_name[check_time]} Not Found Test Fail",file = open(file_name, '+a'))
            if_error = True
    
    for check_time in range(2):### re-registration head start time:720 Test
        if_find = False
        for index in range(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponSipProf_name").__len__()):
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponSipProf_name")[-(index+1)].get_attribute("textContent") == sip_profile_name[check_time]):
                if_find = True
                driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponSipProf_name")[-(index+1)].click()
                pro.Sip_Profile_New_RHST(driver,"720")
                pro.Sip_Profile_New_Apply(driver)                
                try:
                    driver.find_element(By.NAME, "rperror_btnBack").click()
                    print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} re-registration head start time:720 Apply Fail(#175102)",file = open(file_name, '+a'))
                    if_error = True
                except:                                   
                    if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipSip_reregHeadStartTime")[-(index+1)].get_attribute("textContent") != "720"):                       
                        print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} re-registration head start time:720 Test Fail",file = open(file_name, '+a'))
                    
                break
        if(if_find == False):
            print(f"             [XPON - Profiles - Sip Profile] {sip_profile_print_name[check_time]} Not Found Test Fail",file = open(file_name, '+a'))
            if_error = True
    if(if_error == False):
        print(f"[MSAN1-12164][XPON - Profiles - Sip Profile] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-12164][XPON - Profiles - Sip Profile] Result Fail",file = open(file_name, '+a'))
    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def Voip_Common_Profile_Test(driver,file_name):
    if_error = False
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    time.sleep(5)
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Voip Common").click()
    time.sleep(5)
    if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__() > voip_common_profile_capacity-2):
        driver.find_elements(By.NAME, "rpXGSponCommonProf_chkDel")[-1].click()
        driver.find_elements(By.NAME, "rpXGSponCommonProf_chkDel")[-2].click()
        pro.Voip_Common_Profile_Delete(driver)
    voip_common_profile_name = ["voip_common_SFU","voip_common_HGU"]
    voip_common_profile_print_name = ["SFU","HGU"]
    for create_time in range(2):
        pro.Voip_Common_Profile_New(driver)
        pro.Voip_Common_Profile_New_Name(driver,voip_common_profile_name[create_time])
        pro.Voip_Common_Profile_New_min_Local_Port(driver,"65535")
        pro.Voip_Common_Profile_New_max_Local_Port(driver,"65535")
        pro.Voip_Common_Profile_New_dscp_mark(driver,"63")
        time.sleep(3)
        pro.Voip_Common_Profile_New_piggyback(driver,True)
        time.sleep(1)
        pro.Voip_Common_Profile_New_tone(driver,True)
        time.sleep(2)
        pro.Voip_Common_Profile_New_dtmf(driver,True)
        time.sleep(1)
        pro.Voip_Common_Profile_New_cas(driver,True)
        time.sleep(1)
        pro.Voip_Common_Profile_New_jitter_target(driver,"5000")
        pro.Voip_Common_Profile_New_max_jitter_buffer(driver,"500")             
        pro.Voip_Common_Profile_New_ptsn_protocol(driver,"999")           
        pro.Voip_Common_Profile_New_announce_type(driver,4)
        time.sleep(2)
        pro.Voip_Common_Profile_New_echo_cancel(driver,True)
        time.sleep(1)
        pro.Voip_Common_Profile_New_fax_mode(driver,2)
        pro.Voip_Common_Profile_New_1st_codec(driver,17)
        pro.Voip_Common_Profile_New_2nd_codec(driver,17)
        pro.Voip_Common_Profile_New_3rd_codec(driver,17)
        pro.Voip_Common_Profile_New_4th_codec(driver,17)
        pro.Voip_Common_Profile_New_1st_packet_period(driver,"30")
        pro.Voip_Common_Profile_New_2nd_packet_period(driver,"30")
        pro.Voip_Common_Profile_New_3rd_packet_period(driver,"30")
        pro.Voip_Common_Profile_New_4th_packet_period(driver,"30")
        time.sleep(3)
        pro.Voip_Common_Profile_New_1st_silence(driver,True)
        time.sleep(1)
        pro.Voip_Common_Profile_New_2nd_silence(driver,True)
        time.sleep(1)
        pro.Voip_Common_Profile_New_3rd_silence(driver,True)
        time.sleep(1)
        pro.Voip_Common_Profile_New_4th_silence(driver,True)
        time.sleep(1)
        pro.Voip_Common_Profile_New_oob_dtmf(driver,True)
        time.sleep(1)
        pro.Voip_Common_Profile_New_signal_code(driver,6)
        time.sleep(1)

        # re check invalid value "@"
        # "@" > it should false > toast error message / wait for Apply and go to error page which need to click btnback
        # pro.Voip_Common_Profile_New_ptsn_protocol(driver,"@")
        # if(mod.IsAlert(driver) == False):
        #     print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[create_time]} Invalid Value Test Fail. ptsn protocol:@",file = open(file_name, '+a'))
        #     if_error = True
        # try:
        #     driver.find_element(By.NAME, "rperror_btnBack").click()
        #     print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[create_time]} Apply Fail",file = open(file_name, '+a'))
        #     if_error = True
        # except:
        #     pass
        # pro.Voip_Common_Profile_New_ptsn_protocol(driver,"999")   
        # time.sleep(2)
        # pro.Voip_Common_Profile_New_dscp_mark(driver,"@") 
        # if(mod.IsAlert(driver) == False):
        #     print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[create_time]} Invalid Value Test Fail. dscp mark:@",file = open(file_name, '+a'))
        #     if_error = True
        # try:
        #     driver.find_element(By.NAME, "rperror_btnBack").click()
        #     print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[create_time]} Apply Fail",file = open(file_name, '+a'))
        #     if_error = True
        # except:
        #     pass
        # pro.Voip_Common_Profile_New_dscp_mark(driver,"63")
        # time.sleep(2)
        # pro.Voip_Common_Profile_New_jitter_target(driver,"@")
        # if(mod.IsAlert(driver) == False):
        #     print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[create_time]} Invalid Value Test Fail. jiter target:@",file = open(file_name, '+a'))
        #     if_error = True
        # try:
        #     driver.find_element(By.NAME, "rperror_btnBack").click()
        #     print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[create_time]} Apply Fail",file = open(file_name, '+a'))
        #     if_error = True
        # except:
        #     pass
        # pro.Voip_Common_Profile_New_jitter_target(driver,"5000")
        # time.sleep(2)
        # pro.Voip_Common_Profile_New_max_jitter_buffer(driver,"@")
        # if(mod.IsAlert(driver) == False):
        #     print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[create_time]} Invalid Value Test Fail. max jitter buffer:@",file = open(file_name, '+a'))
        #     if_error = True
        # try:
        #     driver.find_element(By.NAME, "rperror_btnBack").click()
        #     print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[create_time]} Apply Fail",file = open(file_name, '+a'))
        #     if_error = True
        # except:
        #     pass
        # pro.Voip_Common_Profile_New_max_jitter_buffer(driver,"500")
        # pro.Voip_Common_Profile_New_min_Local_Port(driver,"@")
        # if(mod.IsAlert(driver) == False):
        #     print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[create_time]} Invalid Value Test Fail. mini local port:@",file = open(file_name, '+a'))
        #     if_error = True
        # try:
        #     driver.find_element(By.NAME, "rperror_btnBack").click()
        #     print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[create_time]} Apply Fail",file = open(file_name, '+a'))
        #     if_error = True
        # except:
        #     pass
        # pro.Voip_Common_Profile_New_min_Local_Port(driver,"65535")
        
        time.sleep(3)
        pro.Voip_Common_Profile_New_ptsn_protocol(driver,"@")
        pro.Voip_Common_Profile_New_Apply(driver)
        try:
            driver.find_element(By.NAME, "rperror_btnBack").click()
        except:
            print(f"             [XPON - Profiles - Voip Common Profile] ptsn protocol Fail => @",file = open(file_name, '+a'))
            if_error = True


        pro.Voip_Common_Profile_New_Apply(driver)        
        if(mod.IsAlert(driver) == True):
            print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[create_time]} Valid Value Alert Test Fail",file = open(file_name, '+a'))
            if_error = True
        try:
            driver.find_element(By.NAME, "rperror_btnBack").click()
            print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[create_time]} Apply Fail",file = open(file_name, '+a'))
            if_error = True
        except:
            pass
        time.sleep(5)
    for check_time in range(2):
        if_find = False
        for index in range(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponCommonProf_name").__len__()):
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponCommonProf_name")[-(index+1)].get_attribute("textContent") == voip_common_profile_name[check_time]):
                if_find = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipCommon_minPort")[-(index+1)].get_attribute("textContent") != "65535"):
                    print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} min local port Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipCommon_maxPort")[-(index+1)].get_attribute("textContent") != "65535"):
                    print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} max local port Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipCommon_dscpMark")[-(index+1)].get_attribute("textContent") != "63"):
                    print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} dscp mark Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipCommon_piggyback")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} piggyback Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipCommon_tone")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} tone Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipCommon_dtmf")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} dtmf Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipCommon_cas")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} cas Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipCommon_jitterTarget")[-(index+1)].get_attribute("textContent") != "5000"):
                    print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} jitter target Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipCommon_jitterBuf")[-(index+1)].get_attribute("textContent") != "500"):
                    print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} max jitter buffer Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipCommon_pstn")[-(index+1)].get_attribute("textContent") != "500"):
                    print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} pstn protocol Test Fail, 0-500 -> 0-999",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipCommon_announce")[-(index+1)].get_attribute("textContent") != "voi-ann"):
                    print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} announce type Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipCommon_echo")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} echo cancel Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipCommon_fax")[-(index+1)].get_attribute("textContent") != "T38"):
                    print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} fax mode Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipCommon_1stCodec")[-(index+1)].get_attribute("textContent") != "G729"):
                    print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} 1st codec Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipCommon_2ndCodec")[-(index+1)].get_attribute("textContent") != "G729"):
                    print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} 2nd codec Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipCommon_3rdCodec")[-(index+1)].get_attribute("textContent") != "G729"):
                    print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} 3rd codec Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipCommon_4thCodec")[-(index+1)].get_attribute("textContent") != "G729"):
                    print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} 4th codec Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipCommon_1stPktPeriod")[-(index+1)].get_attribute("textContent") != "30"):
                    print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} 1st packet period Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipCommon_2ndPktPeriod")[-(index+1)].get_attribute("textContent") != "30"):
                    print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} 2nd packet period Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipCommon_3rdPktPeriod")[-(index+1)].get_attribute("textContent") != "30"):
                    print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} 3rd packet period Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipCommon_4thPktPeriod")[-(index+1)].get_attribute("textContent") != "30"):
                    print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} 4th packet period Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipCommon_1stSilence")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} 1st silence Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipCommon_2ndSilence")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} 2nd silence Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipCommon_3rdSilence")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} 3rd silence Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipCommon_4thSilence")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} 4th silence Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipCommon_oobDtmf")[-(index+1)].get_attribute("textContent") != "ON"):
                    print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} oob dtmf Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipCommon_signalCode")[-(index+1)].get_attribute("textContent") != "mul-par"):
                    print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} single code Test Fail",file = open(file_name, '+a'))
                    if_error = True
                break
        if(if_find == False):
            print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} Not Found Test Fail",file = open(file_name, '+a'))
            if_error = True
    
    # start check ptsn protocol
    #click already created data, edit value, check value
    for check_time in range(2):
        if_find = False
        for index in range(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponCommonProf_name").__len__()):
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponCommonProf_name")[-(index+1)].get_attribute("textContent") == voip_common_profile_name[check_time]):
                if_find = True
                driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponCommonProf_name")[-(index+1)].click()
                pro.Voip_Common_Profile_New_ptsn_protocol(driver,"@")
                pro.Voip_Common_Profile_New_Apply(driver)                
                try:
                    driver.find_element(By.NAME, "rperror_btnBack").click()
                    print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} ptsn protocol:@ Apply Fail",file = open(file_name, '+a'))
                    
                except:                                   
                    if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipCommon_pstn")[-(index+1)].get_attribute("textContent") != "@"):                       
                        print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} ptsn protocol:@ Test Fail",file = open(file_name, '+a'))
                        if_error = True
                driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponCommonProf_name")[-(index+1)].click()
                pro.Voip_Common_Profile_New_dscp_mark(driver,"@")            
                pro.Voip_Common_Profile_New_Apply(driver)                
                try:
                    driver.find_element(By.NAME, "rperror_btnBack").click()
                    print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} dscp mark:@ Apply Fail",file = open(file_name, '+a'))
                    
                except:                                   
                    if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipCommon_dscpMark")[-(index+1)].get_attribute("textContent") != "@"):                       
                        print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} dscp mark:@ Test Fail",file = open(file_name, '+a'))
                        if_error = True
                driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponCommonProf_name")[-(index+1)].click()
                pro.Voip_Common_Profile_New_jitter_target(driver,"@")            
                pro.Voip_Common_Profile_New_Apply(driver)                
                try:
                    driver.find_element(By.NAME, "rperror_btnBack").click()
                    print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} jitter target:@ Apply Fail",file = open(file_name, '+a'))
                    
                except:                                   
                    if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipCommon_jitterTarget")[-(index+1)].get_attribute("textContent") != "@"):                       
                        print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} jitter target:@ Test Fail",file = open(file_name, '+a'))
                        if_error = True
                driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponCommonProf_name")[-(index+1)].click()
                pro.Voip_Common_Profile_New_max_jitter_buffer(driver,"@")
                pro.Voip_Common_Profile_New_Apply(driver)                
                try:
                    driver.find_element(By.NAME, "rperror_btnBack").click()
                    print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} max jitter buffer:@ Apply Fail",file = open(file_name, '+a'))
                    
                except:                                   
                    if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipCommon_jitterBuf")[-(index+1)].get_attribute("textContent") != "@"):                       
                        print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} max jitter buffer:@ Test Fail",file = open(file_name, '+a'))
                        if_error = True
                
                break
        if(if_find == False):
            print(f"             [XPON - Profiles - Voip Common Profile] {voip_common_profile_print_name[check_time]} Not Found Test Fail",file = open(file_name, '+a'))
            if_error = True
    # edit value to original
    driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponCommonProf_name")[-(index+1)].click()
    pro.Voip_Common_Profile_New_ptsn_protocol(driver,"999")
    pro.Voip_Common_Profile_New_dscp_mark(driver,"63")
    pro.Voip_Common_Profile_New_jitter_target(driver,"5000")
    pro.Voip_Common_Profile_New_max_jitter_buffer(driver,"500")
    pro.Voip_Common_Profile_New_Apply(driver)                

    # end check 

    if(if_error == False):
        print(f"[MSAN1-12165][XPON - Profiles - Voip Common Profile] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-12165][XPON - Profiles - Voip Common Profile] Result Fail",file = open(file_name, '+a'))
    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def Dial_Plan_Profile_Test(driver,file_name):
    if_error = False
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    time.sleep(5)
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Voip Dial Plan").click()
    time.sleep(5)
    if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__() > dial_plan_profile_capacity-2):
        driver.find_elements(By.NAME, "rpXGSponDialPlanProf_chkDel")[-1].click()
        driver.find_elements(By.NAME, "rpXGSponDialPlanProf_chkDel")[-2].click()
        pro.Dial_Plan_Profile_Delete(driver)
    dial_plan_profile_name = ["__dial_plan_SFU","__dial_plan_HGU"]
    dial_plan_profile_print_name = ["SFU","HGU"]
    for create_time in range(2):
        pro.Dial_Plan_Profile_New(driver)
        pro.Dial_Plan_Profile_New_Name(driver,dial_plan_profile_name[create_time])
        pro.Dial_Plan_Profile_New_MS(driver,"256")
        pro.Dial_Plan_Profile_New_CDT(driver,"8000")
        pro.Dial_Plan_Profile_New_PDT(driver,"32000")
        pro.Dial_Plan_Profile_New_format(driver,2) #* 4
        pro.Dial_Plan_Profile_New_CT(driver,"0123456789012345678901234567")### content-table token Test
        pro.Dial_Plan_Profile_New_Apply(driver)
        if(mod.IsAlert(driver) == True):
            print(f"             [XPON - Profiles - Dial Plan Profile] {dial_plan_profile_print_name[create_time]} Valid Value Alert Test Fail",file = open(file_name, '+a'))
            if_error = True
        try:
            driver.find_element(By.NAME, "rperror_btnBack").click()
            print(f"             [XPON - Profiles - Dial Plan Profile] {dial_plan_profile_print_name[create_time]} Apply Fail",file = open(file_name, '+a'))
            if_error = True
        except:
            pass
        time.sleep(5)
    driver.find_element(By.LINK_TEXT, "Voip Dial Plan").click()###
    for check_time in range(2):
        if_find = False
        for index in range(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponDialPlanProf_name").__len__()):
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponDialPlanProf_name")[-(index+1)].get_attribute("textContent") == dial_plan_profile_name[check_time]):
                if_find = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipDialPlan_maxSize")[-(index+1)].get_attribute("textContent") != "256"):
                    print(f"             [XPON - Profiles - Dial Plan Profile] {dial_plan_profile_print_name[check_time]} common set max-size Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipDialPlan_criDialTimeout")[-(index+1)].get_attribute("textContent") != "8000"):
                    print(f"             [XPON - Profiles - Dial Plan Profile] {dial_plan_profile_print_name[check_time]} common set critical-dial-timeout Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipDialPlan_parDialTimeout")[-(index+1)].get_attribute("textContent") != "32000"):
                    print(f"             [XPON - Profiles - Dial Plan Profile] {dial_plan_profile_print_name[check_time]} common set partial-dial-timeout Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipDialPlan_format")[-(index+1)].get_attribute("textContent") != "h248"):
                    print(f"             [XPON - Profiles - Dial Plan Profile] {dial_plan_profile_print_name[check_time]} common set format Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponVoipDialPlan_token1")[-(index+1)].get_attribute("textContent") != "0123456789012345678901234567"):### content-table token Test
                    print(f"             [XPON - Profiles - Dial Plan Profile] {dial_plan_profile_print_name[check_time]} content-table token Test Fail",file = open(file_name, '+a'))
                    if_error = True
                break
        if(if_find == False):
            print(f"             [XPON - Profiles - Dial Plan Profile] {dial_plan_profile_print_name[check_time]} Not Found Test Fail",file = open(file_name, '+a'))
            if_error = True
    if(if_error == False):
        print(f"[MSAN1-12166][XPON - Profiles - Dial Plan Profile] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-12166][XPON - Profiles - Dial Plan Profile] Result Fail",file = open(file_name, '+a'))
    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def Template_Test(driver,username,password,file_name):
    if_error = False
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    time.sleep(5)
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Template").click()
    time.sleep(5)
    if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__() > template_capacity-2):
        driver.find_elements(By.NAME, "rpXGSponDialPlanProf_chkDel")[-1].click()
        driver.find_elements(By.NAME, "rpXGSponDialPlanProf_chkDel")[-2].click()
        pro.Dial_Plan_Profile_Delete(driver)

    if_break = False
    create_name = ["SFU","HGU"]
    for create_time in range(2):
        pro.Template_New(driver)
        pro.Template_New_Name(driver,f"______________xpon_template_{create_name[create_time]}")
        try:
            pro.Template_New_Main_UNI_Profile(driver,f"___________xpon_uni_profile_{create_name[create_time]}")
        except:
            print(f"             [XPON - Profiles - Template] UNI Profile {create_name[create_time]} Select Fail",file = open(file_name, '+a'))
            if_break = True
        try:
            pro.Template_New_Main_Security_Profile(driver,f"______xpon_security_profile_{create_name[create_time]}")
        except:
            print(f"             [XPON - Profiles - Template] Security Profile {create_name[create_time]} Select Fail",file = open(file_name, '+a'))
            if_break = True
        pro.Template_New_Main_Alarm_Profile(driver,"DEFVAL")
        try:                                         
            pro.Template_New_Main_Ont_Profile(driver,f"___________xpon_ont_profile_{create_name[create_time]}")
        except:
            print(f"             [XPON - Profiles - Template] Ont Profile {create_name[create_time]} Select Fail",file = open(file_name, '+a'))
            if_break = True

        time.sleep(3)

       # driver.find_element(By.LINK_TEXT, "tab_Service").click()
        driver.find_element(By.ID, "tab_service").click()         
        pro.Template_New_Service_Profile_Active_Select(driver,8,True)
        try:                                            # _______xpon_service_profile_HGU
            pro.Template_New_Service_Profile_all(driver,f"_______xpon_service_profile_{create_name[create_time]}")
            print(f"")
        except:
            print(f"             [XPON - Profiles - Template] Service Profile {create_name[create_time]} Select Fail",file = open(file_name, '+a'))
            if_break = True
        pro.Template_New_Service_Shared_Priority_Select(driver,8,"7")
        try:
            pro.Template_New_Service_US_Bandwidth_Profile_Select(driver,8,"______________100M")
            pro.Template_New_Service_DS_Bandwidth_Profile_Select(driver,8,"______________100M")
        except:
            print(f"             [XPON - Profiles - Template] QoS Bandwidth Profile Select Fail",file = open(file_name, '+a'))
            if_break = True
        time.sleep(10)
        driver.find_element(By.LINK_TEXT, "T-Cont").click()
        pro.Template_New_Tcont_Service_List_Active_Select(driver,8,True)
        pro.Template_New_Tcont_Service_List_Select(driver,8,"8")
        try:
            pro.Template_New_Tcont_US_Bandwidth_Profile_Select(driver,8,"______________100M")
            pro.Template_New_Tcont_DS_Bandwidth_Profile_Select(driver,8,"______________100M")
        except:
            print(f"             [XPON - Profiles - Template] QoS Bandwidth Profile Select Fail",file = open(file_name, '+a'))
            if_break = True
        pro.Template_New_Tcont_Type_Select(driver,8,"best-effort")
        
        #driver.find_element(By.LINK_TEXT, "Multicast").click()
        driver.find_element(By.ID, "tab_mcast").click()         
        pro.Template_New_Multicast_Profile_Active_Select(driver,4,True)
        try:
            pro.Template_New_Multicast_Profile_Select(driver,4,f"_____xpon_multicast_profile_{create_name[create_time]}")
        except:
            print(f"             [XPON - Profiles - Template] Multicast Profile {create_name[create_time]} Select Fail",file = open(file_name, '+a'))
            if_break = True
    if(if_break == True):
        print(f"[MSAN1-12157][XPON - Profiles - Template] Result Fail",file = open(file_name, '+a'))
    else:        
        pro.Template_New_Apply(driver)

        if(mod.IsAlert(driver) == True):
            print(f"             [XPON - Profiles - Template] {create_name[create_time]} Valid Value Alert Test Fail",file = open(file_name, '+a'))
            if_error = True
        try:
            driver.find_element(By.NAME, "rperror_btnBack").click()
            print(f"             [XPON - Profiles - Template] {create_name[create_time]} Apply Fail",file = open(file_name, '+a'))
            if_error = True
        except:
            pass
        for check_time in range(2):
            if_find = False
            for index in range(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponTemplate_name").__len__()):
                try:
                    driver.switch_to.default_content()
                    driver.find_element(By.ID, "userContinue").click()
                    driver.switch_to.frame(0)
                except:
                    try:
                        driver.switch_to.default_content()
                        driver.find_element(By.CLASS_NAME, "ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-front.ui-draggable")
                        driver.find_element(By.ID, "lg_user").send_keys(username)
                        driver.find_element(By.ID, "lg_pass").send_keys(password)
                        driver.find_element(By.ID, "userLogin").click()
                        driver.switch_to.frame(0)
                    except:
                        driver.switch_to.frame(0)
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponTemplate_name")[-(index+1)].get_attribute("textContent") == f"______________xpon_template_{create_name[check_time]}"):
                    if_find = True
                    if(driver.find_elements(By.CLASS_NAME, "rpXGSponTemplate_ServiceProf1")[-(index+1)].get_attribute("textContent") != ''):
                        print(f"             [XPON - Profiles - Template] {create_name[check_time]} Service & T-cont Service Profile 1 Test Fail",file = open(file_name, '+a'))
                        if_error = True
                    if(driver.find_elements(By.CLASS_NAME, "rpXGSponTemplate_ServiceProf2")[-(index+1)].get_attribute("textContent") != ''):
                        print(f"             [XPON - Profiles - Template] {create_name[check_time]} Service & T-cont Service Profile 2 Test Fail",file = open(file_name, '+a'))
                        if_error = True
                    if(driver.find_elements(By.CLASS_NAME, "rpXGSponTemplate_ServiceProf3")[-(index+1)].get_attribute("textContent") != ''):
                        print(f"             [XPON - Profiles - Template] {create_name[check_time]} Service & T-cont Service Profile 3 Test Fail",file = open(file_name, '+a'))
                        if_error = True
                    if(driver.find_elements(By.CLASS_NAME, "rpXGSponTemplate_ServiceProf4")[-(index+1)].get_attribute("textContent") != ''):
                        print(f"             [XPON - Profiles - Template] {create_name[check_time]} Service & T-cont Service Profile 4 Test Fail",file = open(file_name, '+a'))
                        if_error = True
                    if(driver.find_elements(By.CLASS_NAME, "rpXGSponTemplate_ServiceProf5")[-(index+1)].get_attribute("textContent") != ''):
                        print(f"             [XPON - Profiles - Template] {create_name[check_time]} Service & T-cont Service Profile 5 Test Fail",file = open(file_name, '+a'))
                        if_error = True
                    if(driver.find_elements(By.CLASS_NAME, "rpXGSponTemplate_ServiceProf6")[-(index+1)].get_attribute("textContent") != ''):
                        print(f"             [XPON - Profiles - Template] {create_name[check_time]} Service & T-cont Service Profile 6 Test Fail",file = open(file_name, '+a'))
                        if_error = True
                    if(driver.find_elements(By.CLASS_NAME, "rpXGSponTemplate_ServiceProf7")[-(index+1)].get_attribute("textContent") != ''):
                        print(f"             [XPON - Profiles - Template] {create_name[check_time]} Service & T-cont Service Profile 7 Test Fail",file = open(file_name, '+a'))
                        if_error = True
                    if(driver.find_elements(By.CLASS_NAME, "rpXGSponTemplate_ServiceProf8")[-(index+1)].get_attribute("textContent") != f'Service Profile #8: Name "_______xpon_service_profile_{create_name[check_time]}",  Shared priority: 7, US bwprof "______________100M", DS bwprof "______________100M" , Tcont : Type: best-effort, US bwprof "______________100M", DS bwprof "______________100M"'):
                        print(f"             [XPON - Profiles - Template] {create_name[check_time]} Service & T-cont Service Profile 8 Test Fail",file = open(file_name, '+a'))
                        if_error = True
                    if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponTemplate_Mcast")[-(index+1)].get_attribute("textContent") != f'_____xpon_multicast_profile_{create_name[check_time]}'):
                        print(f"             [XPON - Profiles - Template] {create_name[check_time]} Multicast Test Fail",file = open(file_name, '+a'))
                        if_error = True
                    if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponTemplate_UniProf")[-(index+1)].get_attribute("textContent") != f'___________xpon_uni_profile_{create_name[check_time]}'):
                        print(f"             [XPON - Profiles - Template] {create_name[check_time]} UNI Profile Test Fail",file = open(file_name, '+a'))
                        if_error = True
                    if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponTemplate_SecuProf")[-(index+1)].get_attribute("textContent") != f'______xpon_security_profile_{create_name[check_time]}'):
                        print(f"             [XPON - Profiles - Template] {create_name[check_time]} Security Profile Test Fail",file = open(file_name, '+a'))
                        if_error = True
                    if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponTemplate_AlarmProf")[-(index+1)].get_attribute("textContent") != 'DEFVAL'):
                        print(f"             [XPON - Profiles - Template] {create_name[check_time]} Alarm Profile Test Fail",file = open(file_name, '+a'))
                        if_error = True
                    if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponTemplate_OntProf")[-(index+1)].get_attribute("textContent") != f'___________xpon_ont_profile_{create_name[check_time]}'):
                        print(f"             [XPON - Profiles - Template] {create_name[check_time]} Ont Prof Test Fail",file = open(file_name, '+a'))
                        if_error = True
                    break
            if(if_find == False):
                print(f"             [XPON - Profiles - Template] {create_name[check_time]} Not Found Test Fail",file = open(file_name, '+a'))
                if_error = True
        if(if_error == False):
            print(f"[MSAN1-12157][XPON - Profiles - Template] Result Pass",file = open(file_name, '+a'))
        else:
            print(f"[MSAN1-12157][XPON - Profiles - Template] Result Fail",file = open(file_name, '+a'))
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "Config Save").click()
    driver.switch_to.frame(0)
    driver.find_element(By.NAME, "rpConfigSave").click()
    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def ACL_Profile_Test(driver,username,password,file_name):
    acl_pname = ['____xpon_ACL_profile_SFU','____xpon_ACL_profile_HGU']
    if_error = False
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    time.sleep(5)
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "ACL").click()
    time.sleep(5)   
    if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__() > ACL_profile_capacity-2):
        driver.find_elements(By.NAME, "rpXGSponOntAclProf_chkDel")[-1].click()
        driver.find_elements(By.NAME, "rpXGSponOntAclProf_chkDel")[-2].click()
        pro.ACL_Profile_Delete(driver)
    for check_time in range(2):
        pro.ACL_Profile_New(driver)
        pro.ACL_Profile_New_Name(driver,acl_pname[check_time])
        pro.ACL_Profile_New_Enable(driver,True)
        pro.ACL_Profile_New_Policy(driver,"trust")
        pro.ACL_Profile_New_Interface(driver,"both")
        pro.ACL_Profile_New_Count(driver,True)
        pro.ACL_Profile_New_Log(driver,True)
        pro.ACL_Profile_New_Protocol(driver,"255")
        pro.ACL_Profile_New_Src_Port(driver,"65535")
        pro.ACL_Profile_New_Dst_Port(driver,"65535")
        pro.ACL_Profile_New_Src_ip(driver,"10.10.10.1")
        pro.ACL_Profile_New_Src_mask(driver,"32")
        pro.ACL_Profile_New_Dst_ip(driver,"10.10.10.2")
        pro.ACL_Profile_New_Dst_mask(driver,"32")
        pro.ACL_Profile_New_Src_mac(driver,"10:10:10:10:10:01")
        pro.ACL_Profile_New_Dst_mac(driver,"10:10:10:10:10:02")
        pro.ACL_Profile_New_Apply(driver)
        if(mod.IsAlert(driver) == True):
            print(f"             [XPON - Profiles - ACL Profile] {acl_pname[check_time]} Valid Value Alert Test Fail",file = open(file_name, '+a'))
            if_error = True
        try:
            driver.find_element(By.NAME, "rperror_btnBack").click()
            print(f"             [XPON - Profiles - ACL Profile] {acl_pname[check_time]} Apply Fail",file = open(file_name, '+a'))
            if_error = True
        except:
            pass
        if_find = False                                       
        for index in range(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAclProf_name").__len__()):            
            try:
                driver.switch_to.default_content()
                driver.find_element(By.ID, "userContinue").click()
                driver.switch_to.frame(0)
            except:
                try:
                    driver.switch_to.default_content()
                    driver.find_element(By.CLASS_NAME, "ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-front.ui-draggable")
                    driver.find_element(By.ID, "lg_user").send_keys(username)
                    driver.find_element(By.ID, "lg_pass").send_keys(password)
                    driver.find_element(By.ID, "userLogin").click()
                    driver.switch_to.frame(0)
                except:
                    driver.switch_to.frame(0)       
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAclProf_name")[-(index+1)].get_attribute("textContent") == acl_pname[check_time]):                
                if_find = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAclProf_enable")[-(index+1)].get_attribute("textContent") != "on"):
                    print(f"             [XPON - Profiles - ACL Profile] {acl_pname[check_time]} Enable:on Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAclProf_policy")[-(index+1)].get_attribute("textContent") != "trust"):
                    print(f"             [XPON - Profiles - ACL Profile] {acl_pname[check_time]} Policy:trust Test Fail",file = open(file_name, '+a'))
                    if_error = True    
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAclProf_interface")[-(index+1)].get_attribute("textContent") != "both"):
                    print(f"             [XPON - Profiles - ACL Profile] {acl_pname[check_time]} Interface:both Test Fail",file = open(file_name, '+a'))
                    if_error = True    
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAclProf_count")[-(index+1)].get_attribute("textContent") != "enable"):
                    print(f"             [XPON - Profiles - ACL Profile] {acl_pname[check_time]} Count:enable Test Fail",file = open(file_name, '+a'))
                    if_error = True    
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAclProf_log")[-(index+1)].get_attribute("textContent") != "enable"):
                    print(f"             [XPON - Profiles - ACL Profile] {acl_pname[check_time]} Log:enable Test Fail",file = open(file_name, '+a'))
                    if_error = True   
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAclProf_protocol")[-(index+1)].get_attribute("textContent") != "255"):
                    print(f"             [XPON - Profiles - ACL Profile] {acl_pname[check_time]} Protocol:255 Test Fail",file = open(file_name, '+a'))
                    if_error = True   
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAclProf_srcPort")[-(index+1)].get_attribute("textContent") != "65535"):
                    print(f"             [XPON - Profiles - ACL Profile] {acl_pname[check_time]} Src port:65535 Test Fail",file = open(file_name, '+a'))
                    if_error = True   
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAclProf_dstPort")[-(index+1)].get_attribute("textContent") != "65535"):
                    print(f"             [XPON - Profiles - ACL Profile] {acl_pname[check_time]} Dst port:65535 Test Fail",file = open(file_name, '+a'))
                    if_error = True   
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAclProf_srcIp")[-(index+1)].get_attribute("textContent") != "10.10.10.1"):
                    print(f"             [XPON - Profiles - ACL Profile] {acl_pname[check_time]} Src ip:10.10.10.1 Test Fail",file = open(file_name, '+a'))
                    if_error = True   
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAclProf_srcMask")[-(index+1)].get_attribute("textContent") != "32"):
                    print(f"             [XPON - Profiles - ACL Profile] {acl_pname[check_time]} Src mask:32 Test Fail",file = open(file_name, '+a'))
                    if_error = True   
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAclProf_dstIp")[-(index+1)].get_attribute("textContent") != "10.10.10.2"):
                    print(f"             [XPON - Profiles - ACL Profile] {acl_pname[check_time]} Dst ip:10.10.10.2 Test Fail",file = open(file_name, '+a'))
                    if_error = True   
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAclProf_dstMask")[-(index+1)].get_attribute("textContent") != "32"):
                    print(f"             [XPON - Profiles - ACL Profile] {acl_pname[check_time]} Dst mask:32 Test Fail",file = open(file_name, '+a'))
                    if_error = True   
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAclProf_srcMac")[-(index+1)].get_attribute("textContent") != "10:10:10:10:10:01"):
                    print(f"             [XPON - Profiles - ACL Profile] {acl_pname[check_time]} Src mac:10:10:10:10:10:01 Test Fail",file = open(file_name, '+a'))
                    if_error = True   
                if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAclProf_dstMac")[-(index+1)].get_attribute("textContent") != "10:10:10:10:10:02"):
                    print(f"             [XPON - Profiles - ACL Profile] {acl_pname[check_time]} Dst mac:10:10:10:10:10:02 Test Fail",file = open(file_name, '+a'))
                    if_error = True                
                
                driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAclProf_name")[-(index+1)].click()
                pro.ACL_Profile_New_Protocol(driver,"@")
                pro.ACL_Profile_New_Apply(driver)                
                try:
                    driver.find_element(By.NAME, "rperror_btnBack").click()
                    print(f"             [XPON - Profiles - ACL Profile] {acl_pname[check_time]} protocol:@ Apply Fail(#175102)",file = open(file_name, '+a'))
                    
                except:                                   
                    if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAclProf_protocol")[-(index+1)].get_attribute("textContent") != "@"):                       
                        print(f"             [XPON - Profiles - ACL Profile] {acl_pname[check_time]} protocol:@ Test Fail",file = open(file_name, '+a'))
                        if_error = True
                driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAclProf_name")[-(index+1)].click()
                pro.ACL_Profile_New_Src_Port(driver,"@")
                pro.ACL_Profile_New_Apply(driver)                
                try:
                    driver.find_element(By.NAME, "rperror_btnBack").click()
                    print(f"             [XPON - Profiles - ACL Profile] {acl_pname[check_time]} Src port:@ Apply Fail(#175102)",file = open(file_name, '+a'))                    
                except:                                   
                    if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAclProf_srcPort")[-(index+1)].get_attribute("textContent") != "@"):                       
                        print(f"             [XPON - Profiles - ACL Profile] {acl_pname[check_time]} Src port:@ Test Fail",file = open(file_name, '+a'))
                        if_error = True
                driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAclProf_name")[-(index+1)].click()
                pro.ACL_Profile_New_Dst_Port(driver,"@")
                pro.ACL_Profile_New_Apply(driver)                
                try:
                    driver.find_element(By.NAME, "rperror_btnBack").click()
                    print(f"             [XPON - Profiles - ACL Profile] {acl_pname[check_time]} Dst port:@ Apply Fail(#175102)",file = open(file_name, '+a'))                   
                except:                                   
                    if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAclProf_dstPort")[-(index+1)].get_attribute("textContent") != "@"):                       
                        print(f"             [XPON - Profiles - ACL Profile] {acl_pname[check_time]} Dst port:@ Test Fail",file = open(file_name, '+a'))
                        if_error = True
                
                break

        if(if_find == False):
            print(f"             [XPON - Profiles - ACL Profile] {acl_pname[check_time]} Apply Not Found Test Fail",file = open(file_name, '+a'))
            if_error = True

    
    if(if_error == False):
        print(f"[MSAN1-12158][XPON - Profiles - ACL Profile] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-12158][XPON - Profiles - ACL Profile] Result Fail",file = open(file_name, '+a'))
    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def Ont_Alarm_Profile_Test(driver,username,password,file_name):
    if_error = False
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    driver.find_element(By.LINK_TEXT, "Profiles").click()
    time.sleep(5)
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "ONT Alarm").click()
    time.sleep(5)
    #*why need this if?                                                                capacity ? name number
    if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.i1").__len__() >   Ont_Alarm_profile_capacity-2):
        driver.find_elements(By.NAME, "rpXGSponOntAlarmprof_chkDel")[-1].click()
        driver.find_elements(By.NAME, "rpXGSponOntAlarmprof_chkDel")[-2].click()   
        pro.Ont_Alarm_Profile_Delete(driver)
    pro.Ont_Alarm_Profile_New(driver)
    pro.Ont_Alarm_Profile_New_Name(driver,"_____xpon_Ont_Alarm_profile_SFU")
    pro.Ont_Alarm_New_Low_Current_Threshold(driver,"0") #*not sure what value should input
    pro.Ont_Alarm_New_Up_Current_Threshold(driver,"0")
    pro.Ont_Alarm_New_Low_rxpower_thresh(driver,"0")
    pro.Ont_Alarm_New_Up_rxpower_thresh(driver,"0")
    pro.Ont_Alarm_New_Low_temp(driver,"0")
    pro.Ont_Alarm_New_Up_temp(driver,"0")
    pro.Ont_Alarm_New_Low_txpower_thresh(driver,"0")
    pro.Ont_Alarm_New_Up_txpower_thresh(driver,"0")
    pro.Ont_Alarm_New_Low_volt_thresh(driver,"3.59")    
    
    pro.Ont_Alarm_New_Up_volt_thresh(driver,"3.59")

    # pro.Ont_Alarm_New_Up_volt_thresh(driver,"3.59")
    # time.sleep(5)
    # pro.Ont_Alarm_New_Up_volt_thresh(driver,"3.6")
    # pro.Ont_Alarm_Profile_New_Apply(driver)
    # if(mod.IsAlert(driver) == True):                  #*in click back version, IsAlert enable? click back version suit IsAert?
    #     print("             [XPON - Profiles - Ont Alarm Profile] Valid Value Alert Test Fail",file = open(file_name, '+a'))
    #     # if_error = True
    # else:
    #     print(f"             [XPON - Profiles - Ont Alarm Profile] SFU Valid Value Alert Test ..",file = open(file_name, '+a'))
    #     # if_error = True
    # try:
    #     driver.find_element(By.NAME, "rperror_btnBack").click()
    #     print(f"             [XPON - Profiles - Ont Alarm Profile] SFU Apply Fail",file = open(file_name, '+a'))
    #     # if_error = True
    #     time.sleep(2)
    #     pro.Ont_Alarm_Profile_New(driver)
    #     pro.Ont_Alarm_Profile_New_Name(driver,"_____xpon_Ont_Alarm_profile_SFU")
    #     pro.Ont_Alarm_New_Low_Current_Threshold(driver,"0") #*not sure what value should input
    #     pro.Ont_Alarm_New_Up_Current_Threshold(driver,"0")
    #     pro.Ont_Alarm_New_Low_rxpower_thresh(driver,"0")
    #     pro.Ont_Alarm_New_Up_rxpower_thresh(driver,"0")
    #     pro.Ont_Alarm_New_Low_temp(driver,"0")
    #     pro.Ont_Alarm_New_Up_temp(driver,"0")
    #     pro.Ont_Alarm_New_Low_txpower_thresh(driver,"0")
    #     pro.Ont_Alarm_New_Up_txpower_thresh(driver,"0")
    #     pro.Ont_Alarm_New_Low_volt_thresh(driver,"3.59")    
    #     pro.Ont_Alarm_New_Up_volt_thresh(driver,"3.1")  
    #     pro.Ont_Alarm_Profile_New_Apply(driver)
    # except:
    #     pass    
    
    
    pro.Ont_Alarm_Profile_New_Apply(driver)
    if(mod.IsAlert(driver) == True):
        print(f"             [XPON - Profiles - Ont Alarm Profile] SFU Valid Value Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
        print(f"             [XPON - Profiles - Ont Alarm Profile] SFU Apply Fail",file = open(file_name, '+a'))
        if_error = True
    except:
        pass
    if_find = False                                       
    for index in range(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAlarmProf_name").__len__()):
        try:
            driver.switch_to.default_content()
            driver.find_element(By.ID, "userContinue").click()
            driver.switch_to.frame(0)
        except:
            try:
                driver.switch_to.default_content()
                driver.find_element(By.CLASS_NAME, "ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-front.ui-draggable")
                driver.find_element(By.ID, "lg_user").send_keys(username)
                driver.find_element(By.ID, "lg_pass").send_keys(password)
                driver.find_element(By.ID, "userLogin").click()
                driver.switch_to.frame(0)
            except:
                driver.switch_to.frame(0)      
        if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAlarmProf_name")[-(index+1)].get_attribute("textContent") == "_____xpon_Ont_Alarm_profile_SFU"):
            if_find = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAlarmProf_currThreshLow")[-(index+1)].get_attribute("textContent") != "0"):
                print(f"             [XPON - Profiles - Ont Alarm Profile] SFU Low Current Thresh:0 Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAlarmProf_currThreshUp")[-(index+1)].get_attribute("textContent") != "0"):
                print(f"             [XPON - Profiles - Ont Alarm Profile] SFU Up Current Thresh:0 Test Fail",file = open(file_name, '+a'))
                if_error = True    
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAlarmProf_rxPowerThreshLow")[-(index+1)].get_attribute("textContent") != "0.0"):
                print(f"             [XPON - Profiles - Ont Alarm Profile] SFU Low rxpower thresh:0.0 Test Fail",file = open(file_name, '+a'))
                if_error = True    
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAlarmProf_rxPowerThreshUp")[-(index+1)].get_attribute("textContent") != "0.0"):
                print(f"             [XPON - Profiles - Ont Alarm Profile] SFU Up rxpower thresh:0.0 Test Fail",file = open(file_name, '+a'))
                if_error = True    
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAlarmProf_temperThreshLow")[-(index+1)].get_attribute("textContent") != "0"):
                print(f"             [XPON - Profiles - Ont Alarm Profile] SFU Low temp:0 Test Fail",file = open(file_name, '+a'))
                if_error = True   
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAlarmProf_temperThreshUp")[-(index+1)].get_attribute("textContent") != "0"):
                print(f"             [XPON - Profiles - Ont Alarm Profile] SFU Up temp:0 Test Fail",file = open(file_name, '+a'))
                if_error = True   
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAlarmProf_txPowerThreshLow")[-(index+1)].get_attribute("textContent") != "0.0"):
                print(f"             [XPON - Profiles - Ont Alarm Profile] SFU Low txpower thresh:0.0 Test Fail",file = open(file_name, '+a'))
                if_error = True   
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAlarmProf_txPowerThreshUp")[-(index+1)].get_attribute("textContent") != "0.0"):
                print(f"             [XPON - Profiles - Ont Alarm Profile] SFU Up txpower thresh:0.0 Test Fail",file = open(file_name, '+a'))
                if_error = True   
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAlarmProf_voltThreshLow")[-(index+1)].get_attribute("textContent") != "3.59"):
                print(f"             [XPON - Profiles - Ont Alarm Profile] SFU Low volt thresh:3.59 Test Fail",file = open(file_name, '+a'))
                if_error = True   
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAlarmProf_voltThreshUp")[-(index+1)].get_attribute("textContent") != "3.59"):
                print(f"             [XPON - Profiles - Ont Alarm Profile] SFU Up volt thresh:3.59 Test Fail",file = open(file_name, '+a'))
                if_error = True   
                         
            break
    if(if_find == False):
        print(f"             [XPON - Profiles - Ont Alarm Profile] SFU Apply Not Found Test Fail",file = open(file_name, '+a'))
        if_error = True
    pro.Ont_Alarm_Profile_New(driver)
    pro.Ont_Alarm_Profile_New_Name(driver,"_____xpon_Ont_Alarm_profile_HGU")
    pro.Ont_Alarm_New_Low_Current_Threshold(driver,"0") 
    pro.Ont_Alarm_New_Up_Current_Threshold(driver,"0")
    pro.Ont_Alarm_New_Low_rxpower_thresh(driver,"0")
    pro.Ont_Alarm_New_Up_rxpower_thresh(driver,"0")
    pro.Ont_Alarm_New_Low_temp(driver,"0")
    pro.Ont_Alarm_New_Up_temp(driver,"0")
    pro.Ont_Alarm_New_Low_txpower_thresh(driver,"0")
    pro.Ont_Alarm_New_Up_txpower_thresh(driver,"0")
    pro.Ont_Alarm_New_Low_volt_thresh(driver,"3.59")
    pro.Ont_Alarm_New_Up_volt_thresh(driver,"3.59")
    pro.Ont_Alarm_Profile_New_Apply(driver)
    if(mod.IsAlert(driver) == True):
        print(f"             [XPON - Profiles - Ont Alarm Profile] HGU Valid Value Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
        print(f"             [XPON - Profiles - Ont Alarm Profile] HGU Apply Fail",file = open(file_name, '+a'))
        if_error = True
    except:
        pass
    if_find = False                                       
    for index in range(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAlarmProf_name").__len__()):
        try:
            driver.switch_to.default_content()
            driver.find_element(By.ID, "userContinue").click()
            driver.switch_to.frame(0)
        except:
            try:
                driver.switch_to.default_content()
                driver.find_element(By.CLASS_NAME, "ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-front.ui-draggable")
                driver.find_element(By.ID, "lg_user").send_keys(username)
                driver.find_element(By.ID, "lg_pass").send_keys(password)
                driver.find_element(By.ID, "userLogin").click()
                driver.switch_to.frame(0)
            except:
                driver.switch_to.frame(0)      
        if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAlarmProf_name")[-(index+1)].get_attribute("textContent") == "_____xpon_Ont_Alarm_profile_HGU"):
            if_find = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAlarmProf_currThreshLow")[-(index+1)].get_attribute("textContent") != "0"):
                print(f"             [XPON - Profiles - Ont Alarm Profile] HGU Low Current Thresh:0 Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAlarmProf_currThreshUp")[-(index+1)].get_attribute("textContent") != "0"):
                print(f"             [XPON - Profiles - Ont Alarm Profile] HGU Up Current Thresh:0 Test Fail",file = open(file_name, '+a'))
                if_error = True    
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAlarmProf_rxPowerThreshLow")[-(index+1)].get_attribute("textContent") != "0.0"):
                print(f"             [XPON - Profiles - Ont Alarm Profile] HGU Low rxpower thresh:0.0 Test Fail",file = open(file_name, '+a'))
                if_error = True    
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAlarmProf_rxPowerThreshUp")[-(index+1)].get_attribute("textContent") != "0.0"):
                print(f"             [XPON - Profiles - Ont Alarm Profile] HGU Up rxpower thresh:0.0 Test Fail",file = open(file_name, '+a'))
                if_error = True    
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAlarmProf_temperThreshLow")[-(index+1)].get_attribute("textContent") != "0"):
                print(f"             [XPON - Profiles - Ont Alarm Profile] HGU Low temp:0 Test Fail",file = open(file_name, '+a'))
                if_error = True   
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAlarmProf_temperThreshUp")[-(index+1)].get_attribute("textContent") != "0"):
                print(f"             [XPON - Profiles - Ont Alarm Profile] HGU Up temp:0 Test Fail",file = open(file_name, '+a'))
                if_error = True   
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAlarmProf_txPowerThreshLow")[-(index+1)].get_attribute("textContent") != "0.0"):
                print(f"             [XPON - Profiles - Ont Alarm Profile] HGU Low txpower thresh:0.0 Test Fail",file = open(file_name, '+a'))
                if_error = True   
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAlarmProf_txPowerThreshUp")[-(index+1)].get_attribute("textContent") != "0.0"):
                print(f"             [XPON - Profiles - Ont Alarm Profile] HGU Up txpower thresh:0.0 Test Fail",file = open(file_name, '+a'))
                if_error = True   
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAlarmProf_voltThreshLow")[-(index+1)].get_attribute("textContent") != "3.59"):
                print(f"             [XPON - Profiles - Ont Alarm Profile] HGU Low volt thresh:3.59 Test Fail",file = open(file_name, '+a'))
                if_error = True   
            if(driver.find_elements(By.CLASS_NAME, "td-table-content-xgspon.td-table-extend-text-left.rpXGSponOntAlarmProf_voltThreshUp")[-(index+1)].get_attribute("textContent") != "3.59"):
                print(f"             [XPON - Profiles - Ont Alarm Profile] HGU Up volt thresh:3.59 Test Fail",file = open(file_name, '+a'))
                if_error = True                            
            break
    if(if_find == False):
        print(f"             [XPON - Profiles - Ont Alarm Profile] HGU Apply Not Found Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(if_error == False):
        print(f"[MSAN1-12158][XPON - Profiles - Ont Alarm Profile] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-12158][XPON - Profiles - Ont Alarm Profile] Result Fail",file = open(file_name, '+a'))
    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))


# Xpon profile test
# =======================================================================================

# Xpon statistics test
def Port_Statistics_Current_Statistics_Test(driver,file_name,slot_x_1_aid,pon_x_1_aid):    

    if_error = False
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    # XPON/Statistics
    driver.find_element(By.XPATH, "/html/body/table/tbody/tr[2]/td[1]/div[2]/a[9]").click()
    time.sleep(5)
    driver.switch_to.frame(0)         
    driver.find_element(By.LINK_TEXT, "Port Statistics Current").click()
    time.sleep(5)    

    # select slot, port
    try:
        pro.Slot_Port_Select_Statistics(driver, slot_x_1_aid + "-" + pon_x_1_aid)        
    except:
        print("             [Statistics - Port Statistics Current] Not found slot-port Test Fail",file = open(file_name, '+a'))
        if_error = True
    # Load
    # XPON/Statistics/Port stattistics Current/Load
    driver.find_element(By.XPATH, "/html/body/form/div/div[2]/input[1]").click()
    # check table
    try:
        driver.find_element(By.CLASS_NAME, "div-row-begin-title")
    except:
        print(f"             [Statistics - Port Statistics Current] Load Column Dont Exist Test Fail",file = open(file_name, '+a'))
        if_error = True    
        
    # Refresh
    # XPON/Statistics/Port stattistics Current/Refresh
    driver.find_element(By.NAME, "rpstatusgpon_btnRefresh").click()
    # check table
    try:
        driver.find_element(By.CLASS_NAME, "div-row-begin-title")
    except:
        print(f"             [Statistics - Port Statistics Current] Refresh Column Dont Exist Test Fail",file = open(file_name, '+a'))
        if_error = True
        
    # Clear
    # XPON/Statistics/Port stattistics Current/Clear
    driver.find_element(By.XPATH, "/html/body/form/div/div[2]/input[2]").click()
    # check table
    try:
        driver.find_element(By.CLASS_NAME, "div-row-begin-title")
    except:
        print(f"             [Statistics - Port Statistics Current] Clear Column Dont Exist Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Result
    if(if_error == False):
        print(f"[MSAN1-11904][Statistics - Port Statistics Current] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11904][Statistics - Port Statistics Current] Result Fail",file = open(file_name, '+a'))


    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def Port_Statistics_History_Statistics_Test(driver,file_name,slot_x_1_aid, pon_x_1_aid):
    if_error = False
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    # # XPON/Statistics
    driver.find_element(By.XPATH, "/html/body/table/tbody/tr[2]/td[1]/div[2]/a[9]").click()
    time.sleep(5)
    driver.switch_to.frame(0)         
    driver.find_element(By.LINK_TEXT, "Port Statistics History").click()
    time.sleep(5)    

    # select slot, port 
    try:
        pro.Slot_Port_Select_Statistics(driver, slot_x_1_aid + "-" + pon_x_1_aid)        
    except:
        print("             [Statistics - Port Statistics History] Not found slot-port Test Fail",file = open(file_name, '+a'))
        if_error = True
    # Load  
    driver.find_element(By.CLASS_NAME, "font-btn").click()     
    # check table
    try:
        driver.find_element(By.CLASS_NAME, "div-row-begin-title")
    except:
        print(f"             [Statistics - Port Statistics History] Load Column Dont Exist Test Fail",file = open(file_name, '+a'))
        if_error = True        

    # Refresh
    driver.find_element(By.NAME, "rpstatusgpon_btnRefresh").click()
    # check table
    try:
        driver.find_element(By.CLASS_NAME, "div-row-begin-title")
    except:
        print(f"             [Statistics - Port Statistics History] Refresh Column Dont Exist Test Fail",file = open(file_name, '+a'))
        if_error = True
        
    # Result
    if(if_error == False):
        print(f"[MSAN1-11904][Statistics - Port Statistics History] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11904][Statistics - Port Statistics History] Result Fail",file = open(file_name, '+a'))
    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))


def Port_15_min_Statistics_Test(driver, file_name, slot_x_1_aid, pon_x_1_aid):
    if_error = False
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    # XPON/Statistics
    driver.find_element(By.XPATH, "/html/body/table/tbody/tr[2]/td[1]/div[2]/a[9]").click()
    time.sleep(5)
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Port 15-min").click()
    time.sleep(5)    

    # select slot, port 
    try:
        pro.Slot_Port_Select_Statistics(driver, slot_x_1_aid + "-" + pon_x_1_aid)        
    except:
        print("             [Statistics - Port 15-min] Not found slot-port Test Fail",file = open(file_name, '+a'))
        if_error = True
    # Load  
    driver.find_element(By.CLASS_NAME, "font-btn").click()
    # check table
    try:
        driver.find_element(By.CLASS_NAME, "div-row-begin-title")
    except:
        print(f"             [Statistics - Port 15-min] Load Column Dont Exist Test Fail",file = open(file_name, '+a'))
        if_error = True 
        
    # Refresh
    driver.find_element(By.NAME, "rpstatusgpon_btnRefresh").click()
    # check table
    try:
        driver.find_element(By.CLASS_NAME, "div-row-begin-title")
    except:
        print(f"             [Statistics - Port 15-min] Refresh Column Dont Exist Test Fail",file = open(file_name, '+a'))
        if_error = True
        
    # Result
    if(if_error == False):
        print(f"[MSAN1-11904][Statistics - Port 15-min] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11904][Statistics - Port 15-min] Result Fail",file = open(file_name, '+a'))
    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))


def Port_15_min_History_Statistics_Test(driver, file_name, slot_x_1_aid, pon_x_1_aid):
    if_error = False
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    # # XPON/Statistics
    driver.find_element(By.XPATH, "/html/body/table/tbody/tr[2]/td[1]/div[2]/a[9]").click()
    time.sleep(5)
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Port 15-min History").click()
    time.sleep(5)    

    # select slot,port
    try:
        pro.Slot_Port_Select_Statistics(driver, slot_x_1_aid + "-" + pon_x_1_aid)        
    except:
        print("             [Statistics - Port 15-min History] Not found slot-port Test Fail",file = open(file_name, '+a'))
        if_error = True
    # Load
    driver.find_element(By.CLASS_NAME, "font-btn").click()
    # check table
    try:
        driver.find_element(By.CLASS_NAME, "div-row-begin-title")
    except:
        print(f"             [Statistics - Port 15-min History] Load Column Dont Exist Test Fail",file = open(file_name, '+a'))
        if_error = True    

    # Refresh
    driver.find_element(By.NAME, "rpstatusgpon_btnRefresh").click()
    # check table
    try:
        driver.find_element(By.CLASS_NAME, "div-row-begin-title")
    except:
        print(f"             [Statistics - Port 15-min History] Refresh Column Dont Exist Test Fail",file = open(file_name, '+a'))
        if_error = True        

    # Result
    if(if_error == False):
        print(f"[MSAN1-11904][Statistics - Port 15-min History] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11904][Statistics - Port 15-min History] Result Fail",file = open(file_name, '+a'))
    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))


def ONT_Statistics_Test(driver, file_name, ont_x_1_1_aid):

    #test for scs
    screenshot_path = f'{str(datetime.datetime.now()).split(":")[0]}{str(datetime.datetime.now()).split(":")[1]}.{str(datetime.datetime.now()).split(":")[2][:5]}_screenshot.png'
    pyautogui.screenshot(screenshot_path)

    # Create a new document
    doc = Document()

    # Insert an image
    doc.add_picture(screenshot_path, width=Inches(6.0))

    # Save the document
    doc.save("document_test1.docx")
    pass
    # # # # #

    if_error = False
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    # # XPON/Statistics
    driver.find_element(By.XPATH, "/html/body/table/tbody/tr[2]/td[1]/div[2]/a[9]").click()
    time.sleep(5)
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "ONT Statistics").click()
    time.sleep(5)    

    # select slot port ont     
    try:
        pro.SOntPort_Select_Statistics(driver, ont_x_1_1_aid)
    except:
        print("             [Statistics - ONT Statistics] Not found slot-port Test Fail",file = open(file_name, '+a'))
        if_error = True
    pyautogui.screenshot(f'{str(datetime.datetime.now()).split(":")[0]}{str(datetime.datetime.now()).split(":")[1]}.{str(datetime.datetime.now()).split(":")[2][:5]}_screenshot.png')

    # Load  
    driver.find_element(By.CLASS_NAME, "font-btn").click()
    # check table
    try:
        driver.find_element(By.CLASS_NAME, "div-row-begin-title")     
    except:
        print(f"             [Statistics - ONT Statistics] Load Column Dont Exist Test Fail",file = open(file_name, '+a'))
        if_error = True    

    # Clear
    driver.find_element(By.ID, "rpXgponOntStatusclear").click() 
    # check table
    try:
        driver.find_element(By.CLASS_NAME, "div-row-begin-title")
    except:
        print(f"             [Statistics - ONT Statistics] Clear Column Dont Exist Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Result
    if(if_error == False):
        print(f"[MSAN1-00000][Statistics - ONT Statistics] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-00000][Statistics - ONT Statistics] Result Fail",file = open(file_name, '+a'))
    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))


# Xpon statistics test
# =======================================================================================

# Xpon diagnostic test

def O7_state_Diagnostic_Test(driver, file_name, pon_x_1_aid, ont_x_1_1_sn):
    # > in > alert test
    # > out > alert test
    # select, input valid value => check value?
    # > in > alert test
    # > out > alert test
    # input "@@@@@@@@@@@"
    # > in > alert test
    # > out > alert test

    if_error = False
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    # # XPON/Diagnostic
    driver.find_element(By.XPATH, "/html/body/table/tbody/tr[2]/td[1]/div[2]/a[11]").click()
    time.sleep(5)
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "O7 state").click()
    time.sleep(5)    

    # click in
    driver.find_element(By.NAME, "rpXGponDiagnostic_btnIn").click()
    # alert test
    if(mod.IsAlert(driver) == False):
        print("             [Diagnostic - O7 state] In, no vlaue Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    # click  out
    driver.find_element(By.NAME, "rpXGponDiagnostic_btnOut").click()
    # alert test
    if(mod.IsAlert(driver) == False):
        print("             [Diagnostic - O7 state] Out, no value Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)

    # input
    try:
        pro.Diagnostic_Port(driver, pon_x_1_aid)
    except:
        print("             [Diagnostic - O7 state] Not found port Test Fail",file = open(file_name, '+a'))
        if_error = True
        pyautogui.screenshot(f'{str(datetime.datetime.now()).split(":")[0]}{str(datetime.datetime.now()).split(":")[1]}.{str(datetime.datetime.now()).split(":")[2][:5]}_screenshot.png')
    pro.Diagnostic_SN(driver, ont_x_1_1_sn)
    
    # in, out
    # click in
    driver.find_element(By.NAME, "rpXGponDiagnostic_btnIn").click()  
    if(mod.IsAlert(driver) == True):
        print("             [Diagnostic - O7 state] In, valid value No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True 
    # click  out
    driver.find_element(By.NAME, "rpXGponDiagnostic_btnOut").click()   
    if(mod.IsAlert(driver) == True):
        print("             [Diagnostic - O7 state] Out, valid value No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True 

    # input "@@@"
    pro.Diagnostic_SN(driver, "@@@@@@@@@@@@@@@@@@@@")
    # in, out alert test
    # click in
    driver.find_element(By.NAME, "rpXGponDiagnostic_btnIn").click()
    if(mod.IsAlert(driver) == False):
        print("             [Diagnostic - O7 state] In,'@' Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    # click  out
    driver.find_element(By.NAME, "rpXGponDiagnostic_btnOut").click()
    if(mod.IsAlert(driver) == False):
        print("             [Diagnostic - O7 state] Out,'@' Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)

    # Result
    if(if_error == False):
        print(f"[MSAN1-11904][Diagnostic - O7 state] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11904][Diagnostic - O7 state] Result Fail",file = open(file_name, '+a'))
    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))
    
def Debug_cmd_Diagnostic_Test(driver, file_name, ont_x_1_1_aid):
    if_error = False
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    # # XPON/Diagnostic
    driver.find_element(By.XPATH, "/html/body/table/tbody/tr[2]/td[1]/div[2]/a[11]").click()
    time.sleep(5)
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "Debug cmd").click()
    time.sleep(5)    

    # input 
    ont_aid_array = ont_x_1_1_aid.split("-")
    try:
        pro.Diagnostic_Debug_cmd_system(driver,ont_aid_array[0])
    except:
        print("             [Diagnostic - Debug cmd] Not found system slot Test Fail",file = open(file_name, '+a'))
        if_error = True
        pyautogui.screenshot(f'{str(datetime.datetime.now()).split(":")[0]}{str(datetime.datetime.now()).split(":")[1]}.{str(datetime.datetime.now()).split(":")[2][:5]}_screenshot.png')

    driver.find_element(By.NAME, "rpXGponDiagnostic_btnIn").click() # backup
    # expect should show a sentence...
    #  > detect it
    try:
        driver.find_element(By.CLASS_NAME, "warnningmesseage")
        time.sleep(60)
    except:
        print("             [Diagnostic - Debug cmd]  System warnning message Test Fail",file = open(file_name, '+a'))
        if_error = True
    
    try:
        pro.Diagnostic_Debug_cmd_port(driver, ont_aid_array[0] + "-" + ont_aid_array[1])
    except:
        print("             [Diagnostic - Debug cmd] Not found cmd slot-port Test Fail",file = open(file_name, '+a'))
        if_error = True
        pyautogui.screenshot(f'{str(datetime.datetime.now()).split(":")[0]}{str(datetime.datetime.now()).split(":")[1]}.{str(datetime.datetime.now()).split(":")[2][:5]}_screenshot.png')

    driver.find_element(By.NAME, "rpXGponDiagnostic_btnIn1").click() # backup
    try:
        driver.find_element(By.CLASS_NAME, "warnningmesseage")
        time.sleep(60)
    except:
        print("             [Diagnostic - Debug cmd] Port warnning message Test Fail",file = open(file_name, '+a'))
        if_error = True
    
    try: # slot-port
        pro.Diagnostic_Debug_cmd_ont1(driver, ont_aid_array[0] + "-" + ont_aid_array[1])
    except:
        print("             [Diagnostic - Debug cmd] Not found ont slot-port Test Fail",file = open(file_name, '+a'))
        if_error = True
        pyautogui.screenshot(f'{str(datetime.datetime.now()).split(":")[0]}{str(datetime.datetime.now()).split(":")[1]}.{str(datetime.datetime.now()).split(":")[2][:5]}_screenshot.png')
    try: # number
        pro.Diagnostic_Debug_cmd_ont2(driver, ont_aid_array[2])
    except:
        print("             [Diagnostic - Debug cmd] Not found ont number Test Fail",file = open(file_name, '+a'))
        if_error = True
        pyautogui.screenshot(f'{str(datetime.datetime.now()).split(":")[0]}{str(datetime.datetime.now()).split(":")[1]}.{str(datetime.datetime.now()).split(":")[2][:5]}_screenshot.png')

    driver.find_element(By.NAME, "rpXGponDiagnostic_btnIn2").click() # backup
    try:
        driver.find_element(By.CLASS_NAME, "warnningmesseage")
        time.sleep(60)
    except:
        print("             [Diagnostic - Debug cmd]  Ont warnning message Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Result
    if(if_error == False):
        print(f"[MSAN1-11904][Diagnostic - Debug cmd] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11904][Diagnostic - Debug cmd] Result Fail",file = open(file_name, '+a'))
    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

# Xpon diagnostic test
# =======================================================================================

# Xpon ONT Staststics clear Test

def ONT_Staststics_clear_Test(driver, file_name):
    # > Maintenance > Config Reset > reset or resetall??? > XPON > Statistics > ONT Statistics > click clear btn > check error page
    # >> Reset
    pro.Maintenance_Config_Reset(driver)
    # >> click clear btn
    driver.switch_to.default_content()
    driver.find_element(By.LINK_TEXT, "XPON").click()
    # XPON/Statistics
    driver.find_element(By.XPATH, "/html/body/table/tbody/tr[2]/td[1]/div[2]/a[9]").click()
    time.sleep(5)
    driver.switch_to.frame(0)
    driver.find_element(By.LINK_TEXT, "ONT Statistics").click()
    time.sleep(5)    
    driver.find_element(By.ID, "rpXgponOntStatusclear").click() 
    # check table
    try:
        driver.find_element(By.CLASS_NAME, "div-row-begin-title")
        print(f"[MSAN1-00000][Statistics - ONT Statistics clear] Result Pass",file = open(file_name, '+a'))
    except:
        # it will reboot for 5 minutes
        print(f"             [Statistics - ONT Statistics clear] Clear Column Dont Exist Test Fail",file = open(file_name, '+a'))
        print(f"[MSAN1-00000][Statistics - ONT Statistics clear] Result Fail",file = open(file_name, '+a'))
        print("Test Finishd",file = open(file_name, '+a'))
        print("======================================================================================",file = open(file_name, '+a'))  

# Xpon ONT Staststics clear Test
# =======================================================================================   \

WAIT_TIME = 5

# EMS test

def EMS_Dashboard_AlarmStatus_Test(driver, file_name, test_report2):

    if_error = False
    driver.switch_to.default_content()
    time.sleep(WAIT_TIME) 
    driver.find_element(By.LINK_TEXT, "Dashboard").click()
    time.sleep(WAIT_TIME)
    d_All = int(driver.find_element(By.CLASS_NAME, "dashboard-text-xxl.bold.color_default.dashboard-underborder-green").get_attribute("textContent"))
    d_Critical = int(driver.find_element(By.CLASS_NAME, "dashboard-text-xxl.bold.color_critical").get_attribute("textContent"))
    d_Major = int(driver.find_element(By.CLASS_NAME, "dashboard-text-xxl.bold.color_major").get_attribute("textContent"))
    d_Minor = int(driver.find_element(By.CLASS_NAME, "dashboard-text-xxl.bold.color_minor").get_attribute("textContent"))
    d_Info = int(driver.find_element(By.CLASS_NAME, "dashboard-text-xxl.bold.color_info").get_attribute("textContent"))
    if(d_All != (d_Critical + d_Major + d_Minor + d_Info)):
        print("             [EMS - Dashboard - Alarm Status] All = Critical + Major + Minor + Info Test Fail",file = open(file_name, '+a'))
        if_error = True
        screenshot_path = f'{str(datetime.datetime.now()).split(":")[0]}{str(datetime.datetime.now()).split(":")[1]}.{str(datetime.datetime.now()).split(":")[2][:5]}_screenshot.png'
        pyautogui.screenshot(screenshot_path)
        test_report2.add_paragraph("             [EMS - Dashboard - Alarm Status] All = Critical + Major + Minor + Info Test Fail")
        test_report2.add_paragraph(f"             [EMS - Dashboard - Alarm Status] {d_All} = {d_Critical} + {d_Major} + {d_Minor} + {d_Info} Test Fail")
        test_report2.add_picture(screenshot_path, width=Inches(6.0))
    else:
        print("             [EMS - Dashboard - Alarm Status] All = Critical + Major + Minor + Info Test Pass",file = open(file_name, '+a'))
    if(d_All > 0):
        print("             [EMS - Dashboard - Alarm Status] All Test Fail",file = open(file_name, '+a'))
        if_error = True
        screenshot_path = f'{str(datetime.datetime.now()).split(":")[0]}{str(datetime.datetime.now()).split(":")[1]}.{str(datetime.datetime.now()).split(":")[2][:5]}_screenshot.png'
        pyautogui.screenshot(screenshot_path)
        test_report2.add_paragraph("             [EMS - Dashboard - Alarm Status] All Test Fail")
        test_report2.add_picture(screenshot_path, width=Inches(6.0))
    if(d_Critical > 0):
        print("             [EMS - Dashboard - Alarm Status] Critical Test Fail",file = open(file_name, '+a'))
        if_error = True
        screenshot_path = f'{str(datetime.datetime.now()).split(":")[0]}{str(datetime.datetime.now()).split(":")[1]}.{str(datetime.datetime.now()).split(":")[2][:5]}_screenshot.png'
        pyautogui.screenshot(screenshot_path)
        test_report2.add_paragraph("             [EMS - Dashboard - Alarm Status] Critical Test Fail")
        test_report2.add_picture(screenshot_path, width=Inches(6.0))
    if(d_Major <= 0):
        print("             [EMS - Dashboard - Alarm Status] Major Test Fail",file = open(file_name, '+a'))
        if_error = True
        screenshot_path = f'{str(datetime.datetime.now()).split(":")[0]}{str(datetime.datetime.now()).split(":")[1]}.{str(datetime.datetime.now()).split(":")[2][:5]}_screenshot.png'
        pyautogui.screenshot(screenshot_path)
        test_report2.add_paragraph("             [EMS - Dashboard - Alarm Status] Major Test Fail")
        test_report2.add_picture(screenshot_path, width=Inches(6.0))
    if(d_Minor <= 0):
        print("             [EMS - Dashboard - Alarm Status] Minor Test Fail",file = open(file_name, '+a'))
        if_error = True
        screenshot_path = f'{str(datetime.datetime.now()).split(":")[0]}{str(datetime.datetime.now()).split(":")[1]}.{str(datetime.datetime.now()).split(":")[2][:5]}_screenshot.png'
        pyautogui.screenshot(screenshot_path)
        test_report2.add_paragraph("             [EMS - Dashboard - Alarm Status] Minor Test Fail")
        test_report2.add_picture(screenshot_path, width=Inches(6.0))
    if(d_Info <= 0):
        print("             [EMS - Dashboard - Alarm Status] Info Test Fail",file = open(file_name, '+a'))
        if_error = True
        screenshot_path = f'{str(datetime.datetime.now()).split(":")[0]}{str(datetime.datetime.now()).split(":")[1]}.{str(datetime.datetime.now()).split(":")[2][:5]}_screenshot.png'
        pyautogui.screenshot(screenshot_path)
        test_report2.add_paragraph("             [EMS - Dashboard - Alarm Status] Info Test Fail")
        test_report2.add_picture(screenshot_path, width=Inches(6.0))    

    # Result
    if(if_error == False):
        print(f"[MSAN1-11904][EMS - Dashboard - Alarm Status] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11904][EMS - Dashboard - Alarm Status] Result Fail",file = open(file_name, '+a'))
    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def EMS_Alarm_Test(driver, file_name, test_report2):
    
    pass
    
    # # Alarm
    # driver.find_element(By.LINK_TEXT, "Alarm").click()
    # time.sleep(WAIT_TIME)
    # if(driver.find_element(By.ID, "alarm_total").get_attribute("textContent") <= "0"):
    #     print("             [EMS - Alarm - Alarm Status] Test Fail",file = open(file_name, '+a'))
    #     if_error = True
    #     screenshot_path = f'{str(datetime.datetime.now()).split(":")[0]}{str(datetime.datetime.now()).split(":")[1]}.{str(datetime.datetime.now()).split(":")[2][:5]}_screenshot.png'
    #     pyautogui.screenshot(screenshot_path)
    #     test_report2.add_paragraph("Alarm Test Fail")
    #     test_report2.add_picture(screenshot_path, width=Inches(6.0))

def EMS_Provision_path(driver,url):
    driver.switch_to.default_content()
    time.sleep(1) 

    driver.find_element(By.LINK_TEXT, "Provision").click()
    time.sleep(1)

    driver.find_element(By.LINK_TEXT, "Configuration").click()
    time.sleep(1)

    # input ip
    url_ip = url.split("/")[2]    
    driver.find_element(By.ID, "map_key_filter").clear()
    driver.find_element(By.ID, "map_key_filter").send_keys(url_ip)
    # driver.find_element(By.XPATH, "/html/body/div/div[4]/div[1]/div[1]/div/div[2]/div/div[2]/div[1]/div[1]/input").clear()
    # driver.find_element(By.XPATH, "/html/body/div/div[4]/div[1]/div[1]/div/div[2]/div/div[2]/div[1]/div[1]/input").send_keys(url_ip)
    time.sleep(1)

    # click filter
    driver.find_element(By.ID, "map_key_searsh").click()
    time.sleep(1)

    # click EMS
    driver.find_element(By.CLASS_NAME, "icon.expand-icon.oi.oi-plus").click()  # click '+'
    # time.sleep(2)

    # click Cecily
    driver.find_element(By.CLASS_NAME, "icon.expand-icon.oi.oi-plus").click()  # click '+'
    # time.sleep(2)

    # click IES 192.168.xxx.xxx
    # print(f"test after 192.168.: {url_ip[8:]}")
    driver.find_element(By.XPATH, f'//*[@title="IES6217_{url_ip[8:]}({url_ip})"]').click()

    driver.switch_to.frame(0)    

def EMS_Provision_ACL_ACL_Rule(driver,url):
   
    if_error = False
    
    # #-----------FW Web set start---------------------------------

    # # 路徑導向 Profile > ACL 
    # mod.Switch_Default(driver)
    # mod.Page_Switch(driver,"Profile")
    # mod.Switch_Frame(driver)
    # # set profile
    # pro.ACL_Profile_Mode(driver,1)
    # pro.ACL_Apply(driver)
    # # Profile ACL Apply New Profiles 1
    # pro.ACL_New(driver)
    # pro.ACL_New_Name(driver,"111111")
    # pro.ACL_New_Drop(driver,True)
    # pro.ACL_New_Apply(driver)

    # # ACL Rule > new 
    # mod.Switch_Default(driver)
    # mod.Page_Switch(driver,"ACL")
    # mod.SubPage_Switch(driver,"ACL Rule")
    # mod.Switch_Frame(driver)
    # time.sleep(2)

    # # port select
    # acl.Slot_Select(driver,glc_slot)
    # acl.Port_Select(driver,1)
    # acl.Load(driver)

    # acl.ACL_Rule_ACL_Profile(driver,1)
    # acl.ACL_Rule_Priority(driver,1)
    # acl.ACL_Rule_Apply(driver)

    # # select slot check
    # time.sleep(1)
    # driver.find_elements(By.NAME, "rpaclrule_rdoSlt")[int(glc_slot)-1].click()
    # time.sleep(5)

    # #-----------FW Web set end---------------------------------




    EMS_Provision_path(driver,url)
    
    # click ACL
    # driver.find_element(By.CLASS_NAME, "/html/body/div[2]/div[1]/div[1]/a").click()
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "ACL").click()
    
    # click ACL Rule
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "ACL Rule").click()

def EMS_ACL_Anti_MAC_Spoof(driver,url,list1,username,password,file_name):
    
    for list_element in list1:    
        print(f"             ({list_element})",file = open(file_name, '+a'))        
        slot = list_element.split(",")[1]
        port = list_element.split(",")[2]
        cardtype = list_element.split(",")[3]
        print(f"Now in case:{list_element[:1]},  Slot-Port:{slot}-{port}  {cardtype}")
        print(f"             Now in case:{list_element[:1]},  Slot-Port:{slot}-{port}",file = open(file_name, '+a'))

        match list_element[:1]:            
            case "1":
                EMS_ACL_Anti_MAC_Spoof_1(driver,url,slot,port,cardtype,username,password,file_name)
            case "2":
                EMS_ACL_Anti_MAC_Spoof_2(driver,url,slot,port,cardtype,username,password,file_name)                
            case "3":
                EMS_ACL_Anti_MAC_Spoof_3(driver,url,slot,port,cardtype,username,password,file_name)                
            case _:                
                print(f"             No Action (not in any case)",file = open(file_name, '+a'))                               
        print(f"",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def EMS_ACL_Anti_MAC_Spoof_1(driver,url,slot,port,cardtype,username,password,file_name):
    
    # --------------------- EMS web start ---------------------
    # EMS - ACL - Anti MAC Spoof
    
    # EMS website > login
    driver.get("http://192.168.128.8:9116/") # 連上網頁
    time.sleep(5)
    mod.Login_EMS(driver,username,"Pqa1234!!") # 登入
    time.sleep(5)

    if_EMS_error = False
    EMS_Provision_path(driver,url)
    time.sleep(2)    
    driver.find_element(By.LINK_TEXT, "ACL").click()          
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Anti MAC Spoof").click()
    time.sleep(3)
    try:
        # select slot
        e_acl.Select_Slot(driver,slot)
        
        # select port
        e_acl.Select_Port(driver,port)
    except:
        print(f"             [ACL - AntiMacspoof] EMS Slot Port Select fail",file = open(file_name, '+a'))
        print(f"             [ACL - AntiMacspoof] EMS web check fail",file = open(file_name, '+a'))
        if_EMS_error = True 
    if(if_EMS_error == False):
        # select 'Disable'
        e_acl.Anti_Macspoof_Anti_Macspoof_Select(driver,"Disable")
        e_acl.Anti_Macspoof_Spoof_Action_Select(driver,"Disable")    

        # save
        e_acl.Save(driver)  
        time.sleep(1)  
        pyautogui.press("enter")

        # check  
        # click IES 192.168.xxx.xxx   
        driver.switch_to.default_content() 
        url_ip = url.split("/")[2] 
        driver.find_element(By.XPATH, f'//*[@title="IES6217_{url_ip[8:]}({url_ip})"]').click()
        driver.find_element(By.XPATH, f'//*[@title="IES6217_{url_ip[8:]}({url_ip})"]').click()
        driver.switch_to.frame(0)
        time.sleep(1)
        driver.find_element(By.LINK_TEXT, "ACL").click()        
        time.sleep(1)
        driver.find_element(By.LINK_TEXT, "Anti MAC Spoof").click()
        time.sleep(2)
        e_acl.Select_Slot(driver,slot)
        e_acl.Select_Port(driver,port)
        time.sleep(1)
        # print(f"             [ACL - AntiMacspoof] slot:{slot}, port:{port}",file = open(file_name, '+a'))
        if(driver.find_element(By.XPATH, '//*[@id="acl_antimacspoof_macspoof_select"]/option[2]').is_selected() != True):
            if_EMS_error = True 
            print(f"             [ACL - AntiMacspoof] EMS Anti Macspoof 'Disable' Test fail",file = open(file_name, '+a'))
        else:
            print(f"             [ACL - AntiMacspoof] EMS Anti Macspoof 'Disable' Test pass",file = open(file_name, '+a'))
        if(driver.find_element(By.XPATH, '//*[@id="acl_antimacspoof_spoof_select"]/option[2]').is_selected() != True):
            if_EMS_error = True 
            print(f"             [ACL - AntiMacspoof] EMS Spoof Action 'Disable' Test fail",file = open(file_name, '+a'))
        else:
            print(f"             [ACL - AntiMacspoof] EMS Spoof Action 'Disable' Test pass",file = open(file_name, '+a'))

        # EMS Result
        if(if_EMS_error == True):
            print(f"             [ACL - AntiMacspoof] EMS web check fail",file = open(file_name, '+a'))
        else:
            print(f"             [ACL - AntiMacspoof] EMS web check pass",file = open(file_name, '+a'))
        # --------------------- EMS web end ----------------------- 

        # --------------------- FW web check start ----------------
        if_FW_error = False
        driver.get(url) # 連上網頁
        time.sleep(3)
        mod.Login(driver,username,password) # 登入
        time.sleep(3)
        # ACL > Anti Macspoof
        mod.Switch_Default(driver)
        mod.Page_Switch(driver,"ACL")
        # Anti Macspoof page
        driver.find_element(By.LINK_TEXT, "Anti Macspoof").click() 
        mod.Switch_Frame(driver)

        time.sleep(1)
        acl.Slot_Select(driver,slot)
        acl.Load(driver)
        if(driver.find_element(By.XPATH, f"/html/body/form/div[5]/div/div[{int(port)+7}]/div[2]/select/option[1]").is_selected() != True):
            print(f"             [ACL - AntiMacspoof] FW Anti Macspoof 'Disable' Test fail",file = open(file_name, '+a'))        
            if_FW_error = True
        else:
            print(f"             [ACL - AntiMacspoof] FW Anti Macspoof 'Disable' Test pass",file = open(file_name, '+a'))        
        if(driver.find_element(By.XPATH, f"/html/body/form/div[5]/div/div[{int(port)+7}]/div[3]/select/option[1]").is_selected() != True):
            print(f"             [ACL - AntiMacspoof] FW Spoof Action 'Disable' Test fail",file = open(file_name, '+a'))                
            if_FW_error = True
        else:
            print(f"             [ACL - AntiMacspoof] FW Spoof Action 'Disable' Test pass",file = open(file_name, '+a'))                
        
        # FW Result
        if(if_FW_error == True):
            print(f"             [ACL - AntiMacspoof] FW web check fail",file = open(file_name, '+a'))
        else:
            print(f"             [ACL - AntiMacspoof] FW web check pass",file = open(file_name, '+a'))  
        # --------------------- FW web check end ------------------

    
    # Final Result
    if("1440" in cardtype):              
        output_id = '5189'  # GLC1440
    else:
        output_id = '5341'  # GLC1540
    if((if_EMS_error == False) and (if_FW_error == False)):
        print(f"  [EMS1-{output_id}][ACL - AntiMacspoof] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"  [EMS1-{output_id}][ACL - AntiMacspoof] Result Fail",file = open(file_name, '+a'))

def EMS_ACL_Anti_MAC_Spoof_2(driver,url,slot,port,cardtype,username,password,file_name):    

    if_EMS_error = False
    print(f"             [ACL - AntiMacspoof] EMS web check pass (no action)",file = open(file_name, '+a'))  


    # --------------------- FW web check start ----------------
    if_FW_error = False
    driver.get(url) # 連上網頁
    time.sleep(3)
    mod.Login(driver,username,password) # 登入
    time.sleep(3)
    # ACL > Anti Macspoof
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"ACL")
    mod.Switch_Frame(driver)
    # Anti Macspoof page
    # driver.find_element(By.LINK_TEXT, "Anti Macspoof").click()  #..fail
    
    time.sleep(1)
    acl.Slot_Select(driver,slot)
    acl.Load(driver)
    try:
        msg = driver.find_element(By.CLASS_NAME, "div-row-cell-content.rpantispoof_TEXT_warning").text
        print(f"             [ACL - AntiMacspoof] FW Message:{msg}",file = open(file_name, '+a'))
        if(("not support" in msg) or ("n't support" in msg)):
            print(f"             [ACL - AntiMacspoof] FW x support pass",file = open(file_name, '+a'))
        else:
            print(f"             [ACL - AntiMacspoof] FW x support fail",file = open(file_name, '+a'))
            if_FW_error = True                        
    except:
        if_FW_error = True
        pass
    
    # FW Result
    if(if_FW_error == True):
        print(f"             [ACL - AntiMacspoof] FW web check fail",file = open(file_name, '+a'))
    else:
        print(f"             [ACL - AntiMacspoof] FW web check pass",file = open(file_name, '+a'))  
    # --------------------- FW web check end ------------------

    
    # Final Result    
    if("3416B" in cardtype):              
        output_id = '5265'  # OLC3416B        
    elif ("3708" in cardtype):
        output_id = '5303'  # OLC3708
    else:
        output_id = '5379'  # OLC3816
    if((if_EMS_error == False) and (if_FW_error == False)):
        print(f"  [EMS1-{output_id}][ACL - AntiMacspoof] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"  [EMS1-{output_id}][ACL - AntiMacspoof] Result Fail",file = open(file_name, '+a'))


def EMS_ACL_Anti_MAC_Spoof_3(driver,url,slot,port,cardtype,username,password,file_name):
    

    # --------------------- EMS web start ---------------------
    # EMS - ACL - Anti MAC Spoof
    
    # EMS website > login
    driver.get("http://192.168.128.8:9116/") # 連上網頁
    time.sleep(5)
    mod.Login_EMS(driver,username,"Pqa1234!!") # 登入
    time.sleep(5)

    if_EMS_error = False
    EMS_Provision_path(driver,url)
    time.sleep(2)    
    driver.find_element(By.LINK_TEXT, "ACL").click()          
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Anti MAC Spoof").click()
    time.sleep(3)

    if_select_slotport = True
    try:
        # select slot
        e_acl.Select_Slot(driver,slot)
        
        # select port
        e_acl.Select_Port(driver,port)
    except:
        print(f"             [ACL - AntiMacspoof] EMS Slot Port Select fail",file = open(file_name, '+a'))
        print(f"             [ACL - AntiMacspoof] EMS web check fail",file = open(file_name, '+a'))
        if_EMS_error = True 
        if_select_slotport = False


    if(if_select_slotport == True):

        # select 'Disable'
        e_acl.Anti_Macspoof_Anti_Macspoof_Select(driver,"Disable")  

        # save
        e_acl.Save(driver)  
        time.sleep(1)  
        pyautogui.press("enter")

        # check  
        # click IES 192.168.xxx.xxx   
        driver.switch_to.default_content() 
        url_ip = url.split("/")[2] 
        driver.find_element(By.XPATH, f'//*[@title="IES6217_{url_ip[8:]}({url_ip})"]').click()
        driver.find_element(By.XPATH, f'//*[@title="IES6217_{url_ip[8:]}({url_ip})"]').click()
        driver.switch_to.frame(0)
        time.sleep(1)
        driver.find_element(By.LINK_TEXT, "ACL").click()        
        time.sleep(1)
        driver.find_element(By.LINK_TEXT, "Anti MAC Spoof").click()
        time.sleep(2)
        e_acl.Select_Slot(driver,slot)
        e_acl.Select_Port(driver,port)
        time.sleep(1)
        print(f"             [ACL - AntiMacspoof] slot:{slot}, port:{port}",file = open(file_name, '+a'))
        if(driver.find_element(By.XPATH, '//*[@id="acl_antimacspoof_macspoof_select"]/option[2]').is_selected() != True):
            if_EMS_error = True 
            print(f"             [ACL - AntiMacspoof] EMS Anti Macspoof 'Disable' Test fail",file = open(file_name, '+a'))
        else:
            print(f"             [ACL - AntiMacspoof] EMS Anti Macspoof 'Disable' Test pass",file = open(file_name, '+a'))
        
        # EMS Result
        if(if_EMS_error == True):
            print(f"             [ACL - AntiMacspoof] EMS web check fail",file = open(file_name, '+a'))
        else:
            print(f"             [ACL - AntiMacspoof] EMS web check pass",file = open(file_name, '+a'))
        # --------------------- EMS web end ----------------------- 

        # --------------------- FW web check start ----------------
        if_FW_error = False
        driver.get(url) # 連上網頁
        time.sleep(3)
        mod.Login(driver,username,password) # 登入
        time.sleep(3)
        # ACL > Anti Macspoof
        mod.Switch_Default(driver)
        mod.Page_Switch(driver,"ACL")
        mod.Switch_Frame(driver)
        # Anti Macspoof page
        # driver.find_element(By.LINK_TEXT, "Anti Macspoof").click()  #..fail
        
        time.sleep(1)
        acl.Slot_Select(driver,slot)
        acl.Load(driver)
        if(driver.find_element(By.XPATH, f"/html/body/form/div[5]/div/div[{int(port)+7}]/div[2]/select/option[1]").is_selected() != True):
            print(f"             [ACL - AntiMacspoof] FW Anti Macspoof 'Disable' Test fail",file = open(file_name, '+a'))        
            if_FW_error = True
        else:
            print(f"             [ACL - AntiMacspoof] FW Anti Macspoof 'Disable' Test pass",file = open(file_name, '+a'))        
        
        # FW Result
        if(if_FW_error == True):
            print(f"             [ACL - AntiMacspoof] FW web check fail",file = open(file_name, '+a'))
        else:
            print(f"             [ACL - AntiMacspoof] FW web check pass",file = open(file_name, '+a'))  
        # --------------------- FW web check end ------------------

    
    # Final Result                      
    output_id = '5227'  # OLC3416   
    if((if_EMS_error == False) and (if_FW_error == False)):
        print(f"  [EMS1-{output_id}][ACL - AntiMacspoof] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"  [EMS1-{output_id}][ACL - AntiMacspoof] Result Fail",file = open(file_name, '+a'))

def EMS_ACL_ARP_Inspection(driver,url,slot,port,cardtype,username,password,case_n,file_name):
        
    match case_n:
        case "1":
            if("1440" in cardtype):              
                output_id = '5190'      # GLC1440
            else:
                output_id = '5342'      # GLC1540
        case "2":
            if("3416B" in cardtype):              
                output_id = '5266'      # OLC3416B        
            elif ("3708" in cardtype):
                output_id = '5304'      # OLC3708
            else:
                output_id = '5380'      # OLC3816
        case "3":
            output_id = '5228'          # OLC3416     
        case _:
            return     

    # --------------------- EMS web start ---------------------
    # EMS - ACL - Arp Inspection
    
    # EMS website > login
    driver.get("http://192.168.128.8:9116/") # 連上網頁
    time.sleep(5)
    mod.Login_EMS(driver,username,"Pqa1234!!") # 登入
    time.sleep(5)

    if_EMS_error = False
    EMS_Provision_path(driver,url)
    time.sleep(2)    
    driver.find_element(By.LINK_TEXT, "ACL").click()          
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Arp Inspection").click()
    time.sleep(3)

    try:
        # select slot
        e_acl.Select_Slot(driver,slot)
        
        # select port
        e_acl.Select_Port(driver,port)
    except:
        if_EMS_error = True
        print(f"             [ACL - Arp Inspection] EMS Slot Port Select fail",file = open(file_name, '+a'))
        print(f"             [ACL - Arp Inspection] EMS web check fail",file = open(file_name, '+a'))


    if(if_EMS_error == False):
        # select 'Enable'
        e_acl.ARP_Inspection_Select(driver, "Enable")     # # # #

        # save
        e_acl.Save(driver)  
        time.sleep(1)  
        pyautogui.press("enter")

        # check  
        # click IES 192.168.xxx.xxx   
        driver.switch_to.default_content() 
        url_ip = url.split("/")[2] 
        driver.find_element(By.XPATH, f'//*[@title="IES6217_{url_ip[8:]}({url_ip})"]').click()
        driver.find_element(By.XPATH, f'//*[@title="IES6217_{url_ip[8:]}({url_ip})"]').click()
        driver.switch_to.frame(0)
        time.sleep(1)
        driver.find_element(By.LINK_TEXT, "ACL").click()        
        time.sleep(1)
        driver.find_element(By.LINK_TEXT, "Arp Inspection").click()
        time.sleep(2)    
        e_acl.Select_Slot(driver,slot)                
        e_acl.Select_Port(driver,port)
        time.sleep(1)
                                        
        if(driver.find_element(By.XPATH, '//*[@id="acl_arp_inspection_select"]/option[1]').is_selected() != True):
            if_EMS_error = True 
            print(f"             [ACL - Arp Inspection] EMS Arp Inspection 'Enable' Test fail",file = open(file_name, '+a'))
        else:
            print(f"             [ACL - Arp Inspection] EMS Arp Inspection 'Enable' Test pass",file = open(file_name, '+a'))
        
        # EMS Result
        if(if_EMS_error == True):
            print(f"             [ACL - Arp Inspection] EMS web check fail",file = open(file_name, '+a'))
        else:
            print(f"             [ACL - Arp Inspection] EMS web check pass",file = open(file_name, '+a'))
        # --------------------- EMS web end ----------------------- 

        # --------------------- FW web check start ----------------
        if_FW_error = False
        driver.get(url) # 連上網頁
        time.sleep(3)
        mod.Login(driver,username,password) # 登入
        time.sleep(3)
        # ACL > Arp Inspection
        mod.Switch_Default(driver)
        mod.Page_Switch(driver,"ACL")
        time.sleep(1)
        # Arp Inspection page
        driver.find_element(By.LINK_TEXT, "ARP Inspection").click() 
        mod.Switch_Frame(driver)

        time.sleep(1)                    
        acl.Slot_Select(driver,slot)     
        acl.Load(driver)  
        if(driver.find_element(By.XPATH, f"/html/body/form/div[6]/div/div[{int(port)+5}]/div[2]/select/option[2]").is_selected() != True):
            print(f"             [ACL - Arp Inspection] FW Arp Inspection 'Enable' Test fail",file = open(file_name, '+a'))        
            if_FW_error = True
        else:
            print(f"             [ACL - Arp Inspection] FW Arp Inspection 'Enable' Test pass",file = open(file_name, '+a'))        
        
        # FW Result
        if(if_FW_error == True):
            print(f"             [ACL - Arp Inspection] FW web check fail",file = open(file_name, '+a'))
        else:
            print(f"             [ACL - Arp Inspection] FW web check pass",file = open(file_name, '+a'))  
        # --------------------- FW web check end ------------------

    
    # Final Result    
    if((if_EMS_error == False) and (if_FW_error == False)):
        print(f"  [EMS1-{output_id}][ACL - Arp Inspection] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"  [EMS1-{output_id}][ACL - Arp Inspection] Result Fail",file = open(file_name, '+a'))


def EMS_ACL_DHCP_L2Agent(driver,url,MSC_card,username,password,file_name):
    
    if_EMS_error = False
    if_FW_error = False

    # --------------------- EMS web start ---------------------
    # EMS - ACL - DHCP L2Agent
    
    # EMS website > login
    driver.get("http://192.168.128.8:9116/") # 連上網頁
    time.sleep(5)
    mod.Login_EMS(driver,username,"Pqa1234!!") # 登入
    time.sleep(5)
    
    EMS_Provision_path(driver,url)
    time.sleep(2)    
    driver.find_element(By.LINK_TEXT, "ACL").click()          
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "DHCP L2Agent").click()
    time.sleep(3)
    
    e_acl.DHCP_L2Agent_Max_Lease_Overflow_Mode(driver,"Deny New Lease")
    e_acl.DHCP_L2Agent_Option_82_Check(driver,"Disable")
    e_acl.DHCP_L2Agent_Option_82_Policy_Mode(driver,"Port")
    
    # save
    e_acl.Save(driver)  
    time.sleep(1)  
    pyautogui.press("enter")
    
    # check  
    # click IES 192.168.xxx.xxx   
    driver.switch_to.default_content() 
    url_ip = url.split("/")[2] 
    driver.find_element(By.XPATH, f'//*[@title="IES6217_{url_ip[8:]}({url_ip})"]').click()
    driver.find_element(By.XPATH, f'//*[@title="IES6217_{url_ip[8:]}({url_ip})"]').click()
    driver.switch_to.frame(0)
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "ACL").click()        
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "DHCP L2Agent").click()
    time.sleep(1)                                   
    if(driver.find_element(By.XPATH, '//*[@id="acl_dhcpl2agent_overflowmodel_select"]/option[1]').is_selected() != True):
        if_EMS_error = True 
        print(f"             [ACL - DHCP L2Agent] EMS Max Lease Overflow Mode 'Deny New Lease' Test fail",file = open(file_name, '+a'))
    else:
        print(f"             [ACL - DHCP L2Agent] EMS Max Lease Overflow Mode 'Deny New Lease' Test pass",file = open(file_name, '+a'))
    if(driver.find_element(By.XPATH, '//*[@id="acl_dhcpl2agent_option82check_select"]/option[2]').is_selected() != True):
        if_EMS_error = True 
        print(f"             [ACL - DHCP L2Agent] EMS Option 82 Check 'Disable' Test fail",file = open(file_name, '+a'))
    else:
        print(f"             [ACL - DHCP L2Agent] EMS Option 82 Check 'Disable' Test pass",file = open(file_name, '+a'))
    if(driver.find_element(By.XPATH, '//*[@id="acl_dhcpl2agent_option82policympde_select"]/option[2]').is_selected() != True):
        if_EMS_error = True 
        print(f"             [ACL - DHCP L2Agent] EMS Option 82 Policy Mode 'Port' Test fail",file = open(file_name, '+a'))
    else:
        print(f"             [ACL - DHCP L2Agent] EMS Option 82 Policy Mode 'Port' Test pass",file = open(file_name, '+a'))
    

    # New 1  DHCP L2 Agent Forbidden 
    e_acl.DHCP_L2Agent_DHCP_L2_Agent_Forbidden_New(driver)
    e_acl.DHCP_L2Agent_DHCP_L2_Agent_Forbidden(driver,"4094")
    e_acl.DHCP_L2Agent_DHCP_L2_Agent_Forbidden_LDRA(driver,True)
    e_acl.OK(driver)
    time.sleep(1)  
    pyautogui.press("enter")
    try:
        driver.find_element(By.ID, "popupClose").click()
        print(f"             [ACL - DHCP L2Agent] EMS DHCP L2 Agent Forbidden apply fail",file = open(file_name, '+a'))
        if_EMS_error = True 
    except:
        print(f"             [ACL - DHCP L2Agent] EMS DHCP L2 Agent Forbidden apply pass",file = open(file_name, '+a'))
        # check 
        if_find = False
        for index in range(driver.find_elements(By.CLASS_NAME, "zy_tr.acl_dhcpl2agent_forbiddenvid_table_row").__len__()):
            if(driver.find_elements(By.CLASS_NAME, "zy_td.acl_dhcpl2agent_forbiddenvid_vid")[index].text == "4094"):
                if(driver.find_elements(By.CLASS_NAME, "zy_td.acl_dhcpl2agent_forbiddenvid_ldra")[index].text == "V"):
                    print(f"             [ACL - DHCP L2Agent] EMS DHCP L2 Agent Forbidden Test pass",file = open(file_name, '+a'))
                    if_find = True
                    break                                   
        if(if_find == False):
            print(f"             [ACL - DHCP L2Agent] EMS DHCP L2 Agent Forbidden Test fail",file = open(file_name, '+a'))
            if_EMS_error = True 

        # prepare for select all delete test
        for i in range(1,4):
            e_acl.DHCP_L2Agent_DHCP_L2_Agent_Forbidden_New(driver)
            e_acl.DHCP_L2Agent_DHCP_L2_Agent_Forbidden(driver,i)
            e_acl.DHCP_L2Agent_DHCP_L2_Agent_Forbidden_LDRA(driver,True)
            e_acl.OK(driver)
            time.sleep(1)  
            pyautogui.press("enter")
            try:
                driver.find_element(By.ID, "popupClose").click()
                print(f"             [ACL - DHCP L2Agent] EMS DHCP L2 Agent Forbidden apply{i} fail",file = open(file_name, '+a'))
            except:
                pass

    # invalid input check
    test_keys = ["4095","0","@"]
    for i in test_keys:
        e_acl.DHCP_L2Agent_DHCP_L2_Agent_Forbidden_New(driver)
        e_acl.DHCP_L2Agent_DHCP_L2_Agent_Forbidden(driver,i)
        e_acl.DHCP_L2Agent_DHCP_L2_Agent_Forbidden_LDRA(driver,True)
        e_acl.OK(driver)
        time.sleep(1)  
        pyautogui.press("enter")
        try:
            driver.find_element(By.ID, "popupClose").click()
            print(f"             [ACL - DHCP L2Agent] EMS DHCP L2 Agent Forbidden invalid:{i} apply Test pass",file = open(file_name, '+a'))            
        except:
            print(f"             [ACL - DHCP L2Agent] EMS DHCP L2 Agent Forbidden invalid:{i} apply Test fail",file = open(file_name, '+a'))
            if_EMS_error = True 


    # New 2  DHCP L2 Agent 
    e_acl.DHCP_L2Agent_DHCP_L2_Agent_New(driver)
    e_acl.DHCP_L2Agent_DHCP_L2_Agent_VID(driver,"4094")
    e_acl.DHCP_L2Agent_DHCP_L2_Agent_LDRA(driver,True)
    e_acl.DHCP_L2Agent_DHCP_L2_Agent_Option_18_Interface_Id(driver,"123456789012345678901234567890123456789012345678901234567890123")
    e_acl.DHCP_L2Agent_DHCP_L2_Agent_Option_37_Remote_Id(driver,"123456789012345678901234567890123456789012345678901234567890123")
    e_acl.DHCP_L2Agent_DHCP_L2_Agent_Option_82_Circuit_Id(driver,"123456789012345678901234567890123456789012345678901234567890123")
    e_acl.DHCP_L2Agent_DHCP_L2_Agent_Option_82_Remote_Id(driver,"123456789012345678901234567890123456789012345678901234567890123")
    e_acl.DHCP_L2Agent_DHCP_L2_Agent_Option_82_Policy(driver,"Keep")
    e_acl.DHCP_L2Agent_DHCP_L2_Agent_Option_82_Linechar(driver,"Full")
    e_acl.DHCP_L2Agent_DHCP_L2_Agent_Enable_DHCP_Relay(driver,True)
    e_acl.DHCP_L2Agent_DHCP_L2_Agent_Primary_Relay_Server_IP(driver,"10.10.10.1")
    e_acl.DHCP_L2Agent_DHCP_L2_Agent_Secondary_Relay_Server_IP(driver,"10.10.10.2")
    e_acl.DHCP_L2Agent_DHCP_L2_Agent_Active_Server(driver,"Secondary Relay Server")
    e_acl.DHCP_L2Agent_DHCP_L2_Agent_Relay_Mode(driver,"Both")
          
    pyautogui.keyDown('ctrl')
    pyautogui.press('-')
    pyautogui.press('-')
    pyautogui.press('-')
    pyautogui.keyUp('ctrl') 
    time.sleep(0.5)  
    e_acl.OK(driver)
    
    time.sleep(1)  
    pyautogui.press("enter")
    try:
        driver.find_element(By.ID, "popupClose").click()
        print(f"             [ACL - DHCP L2Agent] EMS DHCP L2 Agent apply fail",file = open(file_name, '+a'))
        if_EMS_error = True 
    except:
        print(f"             [ACL - DHCP L2Agent] EMS DHCP L2 Agent apply pass",file = open(file_name, '+a'))    
    # check 
    if_find = False
    for index in range(driver.find_elements(By.CLASS_NAME, "zy_tr.acl_dhcpl2agent_vid_table_row").__len__()):
        if(driver.find_elements(By.CLASS_NAME, "zy_td.acl_dhcpl2agent_vid")[index].text == "4094"):                
            print(f"             [ACL - DHCP L2Agent] EMS DHCP L2 Agent Test pass",file = open(file_name, '+a'))
            # other contents now cannot be checked on EMS Web #need_add_1
            # ...
            if_find = True
            break    
    if(if_find == False):
        print(f"             [ACL - DHCP L2Agent] EMS DHCP L2 Agent Test fail",file = open(file_name, '+a'))
        if_EMS_error = True    

    # prepare for select all delete test
    for i in range(1,4):
        e_acl.DHCP_L2Agent_DHCP_L2_Agent_New(driver)
        e_acl.DHCP_L2Agent_DHCP_L2_Agent_VID(driver,i)  
        e_acl.OK(driver)
        time.sleep(1)  
        pyautogui.press("enter")
        try:
            driver.find_element(By.ID, "popupClose").click()
            print(f"             [ACL - DHCP L2Agent] EMS DHCP L2 Agent apply{i} fail",file = open(file_name, '+a'))
        except:
            pass
    # --------------------- EMS web end ----------------------- 

    # --------------------- FW web check start ----------------
    # ACL > DHCP => check value
    if_FW_error = False
    driver.get(url) # 連上網頁
    time.sleep(3)
    mod.Login(driver,username,password) # 登入
    time.sleep(3)    
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"ACL")
    time.sleep(1)    
    driver.find_element(By.LINK_TEXT, "DHCP").click() 
    mod.Switch_Frame(driver)
    time.sleep(1)           

    # check 
    if(driver.find_element(By.XPATH, f"//*[@name='rpdhcp_sltOverflowMode']/option[2]").is_selected() == False):
        print(f"             [ACL - DHCP L2Agent] FW Max Lease Overflow Mode Test Fail",file = open(file_name, '+a'))
        if_FW_error = True
    if(driver.find_element(By.XPATH, f"//*[@name='rpdhcp_chkOpt82']/option[1]").is_selected() == False):
        print(f"             [ACL - DHCP L2Agent] FW Option 82 Check Test Fail",file = open(file_name, '+a'))
        if_FW_error = True
    if(driver.find_element(By.XPATH, f"//*[@name='rpdhcp_opt82PolicyMode']/option[2]").is_selected() == False):
        print(f"             [ACL - DHCP L2Agent] FW Option 82 Policy Mode Test Fail",file = open(file_name, '+a'))
        if_FW_error = True

    # check DHCP L2 Agent Forbidden table
    if_find = False
    for index in range(driver.find_elements(By.CLASS_NAME, "td-table-content.rpdhcp_l2AgentForbidVid").__len__()):
        if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpdhcp_l2AgentForbidVid")[index].get_attribute("textContent") == "4094"):
            if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpdhcp_ForbidchkLdra")[index].get_attribute("textContent") == "V"):
                print(f"             [ACL - DHCP L2Agent] FW DHCP L2 Agent Forbidden Test pass",file = open(file_name, '+a'))
                if_find = True
                break            
    if(if_find == False):
        print(f"             [ACL - DHCP L2Agent] FW DHCP L2 Agent Forbidden Test fail",file = open(file_name, '+a'))
        if_FW_error = True

    # check DHCP L2 Agent table
    if_find = False
    for index in range(driver.find_elements(By.CLASS_NAME, "dhcpVlanConfList").__len__()):
        if(driver.find_elements(By.CLASS_NAME, "rpdhcp_l2AgentVid.td-table-content")[index].get_attribute("textContent") == "4094"):
            if_find = True
            driver.find_elements(By.NAME, "pfListSelected")[index].click()                                            
            if(driver.find_element(By.NAME, "rpdhcp_chkLdra").is_selected() != True):
                print(f"             [ACL - DHCP L2Agent] FW DHCP L2 Agent VID Enable LDRA Test Fail",file = open(file_name, '+a'))
                if_FW_error = True
            if(driver.find_element(By.NAME, "opt18OptionInfo").get_attribute("value") != "123456789012345678901234567890123456789012345678901234567890123"):
                print(f"             [ACL - DHCP L2Agent] FW DHCP L2 Agent VID Option 18 Interface Id Test Fail",file = open(file_name, '+a'))
                if_FW_error = True
            if(driver.find_element(By.NAME, "opt37OptionInfo").get_attribute("value") != "123456789012345678901234567890123456789012345678901234567890123"):
                print(f"             [ACL - DHCP L2Agent] FW DHCP L2 Agent VID Option 37 Remote Id Test Fail",file = open(file_name, '+a'))
                if_FW_error = True
            if(driver.find_element(By.NAME, "opt82CircuitOptionInfo").get_attribute("value") != "123456789012345678901234567890123456789012345678901234567890123"):
                print(f"             [ACL - DHCP L2Agent] FW DHCP L2 Agent VID Option 82 Circuit Id Test Fail",file = open(file_name, '+a'))
                if_FW_error = True
            if(driver.find_element(By.NAME, "opt82RemoteOptionInfo").get_attribute("value") != "123456789012345678901234567890123456789012345678901234567890123"):
                print(f"             [ACL - DHCP L2Agent] FW DHCP L2 Agent VID Option 82 Remote Id Test Fail",file = open(file_name, '+a'))
                if_FW_error = True
            if(driver.find_element(By.XPATH, f"//*[@name='rpdhcp_opt82Policy']/option[3]").is_selected() != True):
                print(f"             [ACL - DHCP L2Agent] FW DHCP L2 Agent VID Option 82 Policy Test Fail",file = open(file_name, '+a'))
                if_FW_error = True
            if(driver.find_element(By.XPATH, f"//*[@name='rpdhcp_opt82Linechar']/option[3]").is_selected() != True):
                print(f"             [ACL - DHCP L2Agent] FW DHCP L2 Agent VID Option 82 Linechar Test Fail",file = open(file_name, '+a'))
                if_FW_error = True
            if(driver.find_element(By.NAME, "rpdhcp_chkRelay").is_selected() != True):
                print(f"             [ACL - DHCP L2Agent] FW DHCP L2 Agent VID Enable DHCP Relay Test Fail",file = open(file_name, '+a'))
                if_FW_error = True
            if(driver.find_element(By.NAME, "rpdhcp_priRelaySvrIp").get_attribute("value") != "10.10.10.1"):
                print(f"             [ACL - DHCP L2Agent] FW DHCP L2 Agent VID Primary Relay Server IP Test Fail",file = open(file_name, '+a'))
                if_FW_error = True
            if(driver.find_element(By.NAME, "rpdhcp_sndRelaySvrIp").get_attribute("value") != "10.10.10.2"):
                print(f"             [ACL - DHCP L2Agent] FW DHCP L2 Agent VID Secondary Relay Server IP Test Fail",file = open(file_name, '+a'))
                if_FW_error = True
            if(driver.find_element(By.XPATH, f"//*[@name='rpdhcp_activeRelaySvrIdx']/option[2]").is_selected() != True):
                print(f"             [ACL - DHCP L2Agent] FW DHCP L2 Agent VID Active Server Test Fail",file = open(file_name, '+a'))
                if_FW_error = True
            if(driver.find_element(By.XPATH, f"//*[@name='rpdhcp_relayMode']/option[2]").is_selected() != True):
                print(f"             [ACL - DHCP L2Agent] FW DHCP L2 Agent VID Relay Mode Test Fail",file = open(file_name, '+a'))
                if_FW_error = True                    
            break
    if(if_find == False):
        print(f"             [ACL - DHCP L2Agent] FW DHCP L2 Agent VID not found Fail",file = open(file_name, '+a'))
        if_FW_error = True    
    print(f"             [ACL - DHCP L2Agent] FW DHCP L2 Agent value check done",file = open(file_name, '+a'))
    
    
    # --------------------- FW web check end ------------------

    # Selet One Delete Test
    # --------------------- EMS web start ---------------------
    # EMS - ACL - DHCP L2Agent => delete
    driver.get("http://192.168.128.8:9116/")
    time.sleep(5)
    mod.Login_EMS(driver,username,"Pqa1234!!") 
    time.sleep(5)
    EMS_Provision_path(driver,url)
    time.sleep(2)    
    driver.find_element(By.LINK_TEXT, "ACL").click()          
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "DHCP L2Agent").click()
    time.sleep(3)
    # delete - DHCP L2 Agent Forbidden Delete Test
    if_find = False
    for index in range(driver.find_elements(By.CLASS_NAME, "zy_tr.acl_dhcpl2agent_forbiddenvid_table_row").__len__()):
        if(driver.find_elements(By.CLASS_NAME, "zy_td.acl_dhcpl2agent_forbiddenvid_vid")[index].text == "4094"):            
            if(driver.find_elements(By.CLASS_NAME, "zy_td.acl_dhcpl2agent_forbiddenvid_ldra")[index].text == "V"):
                print(f"index:{index}")
                e_acl.DHCP_L2Agent_DHCP_L2_Agent_Forbidden_Select(driver,True,index+1)
                e_acl.DHCP_L2Agent_DHCP_L2_Agent_Forbidden_Delete(driver)
                time.sleep(1)  
                pyautogui.press("enter")
                if_find_2 = False
                for index in range(driver.find_elements(By.CLASS_NAME, "zy_tr.acl_dhcpl2agent_forbiddenvid_table_row").__len__()):
                    if(driver.find_elements(By.CLASS_NAME, "zy_td.acl_dhcpl2agent_forbiddenvid_vid")[index].text == "4094"):            
                        if(driver.find_elements(By.CLASS_NAME, "zy_td.acl_dhcpl2agent_forbiddenvid_ldra")[index].text == "V"):
                            print(f"             [ACL - DHCP L2Agent] EMS DHCP L2 Agent Forbidden Delete Test fail",file = open(file_name, '+a'))
                            if_EMS_error = True
                            if_find_2 = True
                            break
                if(if_find_2 == False):
                    print(f"             [ACL - DHCP L2Agent] EMS DHCP L2 Agent Forbidden Delete Test pass",file = open(file_name, '+a'))
                if_find = True
                break                                   
    if(if_find == False):
        print(f"             [ACL - DHCP L2Agent] EMS DHCP L2 Agent Forbidden Delete not found to be deleted Test fail",file = open(file_name, '+a'))
        if_EMS_error = True

    # delete - DHCP L2 Agent Delete Test
    if_find = False
    for index in range(driver.find_elements(By.CLASS_NAME, "zy_tr.acl_dhcpl2agent_vid_table_row").__len__()):
        if(driver.find_elements(By.CLASS_NAME, "zy_td.acl_dhcpl2agent_vid")[index].text == "4094"):                
            e_acl.DHCP_L2Agent_DHCP_L2_Agent_Select(driver,True,index+1)
            e_acl.DHCP_L2Agent_DHCP_L2_Agent_Delete(driver)
            time.sleep(1)  
            pyautogui.press("enter")
            if_find_2 = False
            for index in range(driver.find_elements(By.CLASS_NAME, "zy_tr.acl_dhcpl2agent_vid_table_row").__len__()):
                if(driver.find_elements(By.CLASS_NAME, "zy_td.acl_dhcpl2agent_vid")[index].text == "4094"): 
                    if_find_2 = True
                    print(f"             [ACL - DHCP L2Agent] EMS DHCP L2 Agent Delete Test fail",file = open(file_name, '+a'))
                    if_EMS_error = True
                    if_find = True
                    break    
            if(if_find_2 == False):
                    print(f"             [ACL - DHCP L2Agent] EMS DHCP L2 Agent Delete Test pass",file = open(file_name, '+a'))
            if_find = True    
            break
    if(if_find == False):
        print(f"             [ACL - DHCP L2Agent] EMS DHCP L2 Agent Delete not found to be deleted Test fail",file = open(file_name, '+a'))              
    # --------------------- EMS web end -----------------------
    # --------------------- FW web check start ----------------
    # ACL > DHCP => check if deleted
    driver.get(url) 
    time.sleep(3)
    mod.Login(driver,username,password) 
    time.sleep(3)    
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"ACL")
    time.sleep(1)    
    driver.find_element(By.LINK_TEXT, "DHCP").click() 
    mod.Switch_Frame(driver)
    time.sleep(1) 
    # check DHCP L2 Agent Forbidden table, the value shoud not exist 
    if_find = False
    for index in range(driver.find_elements(By.CLASS_NAME, "td-table-content.rpdhcp_l2AgentForbidVid").__len__()):
        if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpdhcp_l2AgentForbidVid")[index].get_attribute("textContent") == "4094"):
            if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpdhcp_ForbidchkLdra")[index].get_attribute("textContent") == "V"):
                print(f"             [ACL - DHCP L2Agent] FW DHCP L2 Agent Forbidden Delete Test fail",file = open(file_name, '+a'))
                if_FW_error = True
                if_find = True
                break            
    if(if_find == False):
        print(f"             [ACL - DHCP L2Agent] FW DHCP L2 Agent Forbidden Delete Test pass",file = open(file_name, '+a'))
        
    # check DHCP L2 Agent table, the value shoud not exist 
    if_find = False
    for index in range(driver.find_elements(By.CLASS_NAME, "dhcpVlanConfList").__len__()):
        if(driver.find_elements(By.CLASS_NAME, "rpdhcp_l2AgentVid.td-table-content")[index].get_attribute("textContent") == "4094"):
            if_find = True                                                       
            print(f"             [ACL - DHCP L2Agent] FW DHCP L2 Agent Delete Test fail",file = open(file_name, '+a'))
            if_FW_error = True                    
            break
    if(if_find == False):
        print(f"             [ACL - DHCP L2Agent] FW DHCP L2 Agent Delete Test pass",file = open(file_name, '+a'))                    
    # --------------------- FW web check end ------------------
    
    # Selet All Delete Test
    # --------------------- EMS web start ---------------------
    # EMS - ACL - DHCP L2Agent => delete
    driver.get("http://192.168.128.8:9116/")
    time.sleep(5)
    mod.Login_EMS(driver,username,"Pqa1234!!") 
    time.sleep(5)
    EMS_Provision_path(driver,url)
    time.sleep(2)    
    driver.find_element(By.LINK_TEXT, "ACL").click()          
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "DHCP L2Agent").click()
    time.sleep(3)
    # delete - DHCP L2 Agent Forbidden Delete Test
    e_acl.DHCP_L2Agent_DHCP_L2_Agent_Forbidden_Select_All(driver,True)
    e_acl.DHCP_L2Agent_DHCP_L2_Agent_Forbidden_Delete(driver)
    time.sleep(1)  
    pyautogui.press("enter")
    try:
        driver.find_element(By.CLASS_NAME, "zy_td.zy_checkbox")
        print(f"             [ACL - DHCP L2Agent] EMS DHCP L2 Agent Forbidden Delete All Test fail",file = open(file_name, '+a'))
        if_EMS_error = True
    except:
        print(f"             [ACL - DHCP L2Agent] EMS DHCP L2 Agent Forbidden Delete All Test pass",file = open(file_name, '+a'))    

    # delete - DHCP L2 Agent Delete Test
    e_acl.DHCP_L2Agent_DHCP_L2_Agent_Select_All(driver,True)
    e_acl.DHCP_L2Agent_DHCP_L2_Agent_Delete(driver)
    time.sleep(1)  
    pyautogui.press("enter")
    try:
        driver.find_element(By.CLASS_NAME, "zy_td.zy_checkbox")
        print(f"             [ACL - DHCP L2Agent] EMS DHCP L2 Agent Delete All Test fail",file = open(file_name, '+a'))
        if_EMS_error = True
    except:
        print(f"             [ACL - DHCP L2Agent] EMS DHCP L2 Agent Delete All Test pass",file = open(file_name, '+a'))               
    # --------------------- EMS web end -----------------------
    # --------------------- FW web check start ----------------
    # ACL > DHCP => check if deleted
    driver.get(url) 
    time.sleep(3)
    mod.Login(driver,username,password) 
    time.sleep(3)    
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"ACL")
    time.sleep(1)    
    driver.find_element(By.LINK_TEXT, "DHCP").click() 
    mod.Switch_Frame(driver)
    time.sleep(1) 
    # check DHCP L2 Agent Forbidden table, the value shoud not exist 
    try:
        driver.find_element(By.CLASS_NAME, "td-table-content.i1")
        print(f"             [ACL - DHCP L2Agent] FW DHCP L2 Agent Forbidden Delete All Test fail",file = open(file_name, '+a'))
        if_FW_error = True
    except:
        print(f"             [ACL - DHCP L2Agent] FW DHCP L2 Agent Forbidden Delete All Test pass",file = open(file_name, '+a'))

    # check DHCP L2 Agent table, the value shoud not exist 
    try:
        driver.find_element(By.CLASS_NAME, "i1.td-table-content")
        print(f"             [ACL - DHCP L2Agent] FW DHCP L2 Agent Delete All Test fail",file = open(file_name, '+a'))
        if_FW_error = True
    except:
        print(f"             [ACL - DHCP L2Agent] FW DHCP L2 Agent Delete All Test pass",file = open(file_name, '+a'))
    # --------------------- FW web check end ------------------

    # EMS Result
    if(if_EMS_error == True):
        print(f"             [ACL - DHCP L2Agent] EMS web check fail",file = open(file_name, '+a'))
    else:
        print(f"             [ACL - DHCP L2Agent] EMS web check pass",file = open(file_name, '+a')) 

    # FW Result
    if(if_FW_error == True):
        print(f"             [ACL - DHCP L2Agent] FW web check fail",file = open(file_name, '+a'))
    else:
        print(f"             [ACL - DHCP L2Agent] FW web check pass",file = open(file_name, '+a')) 

    # Final Result
    if("XB" in MSC_card):
        output_id = "000?"
    elif("XA" in MSC_card):
        output_id = "000?"
    elif("QA" in MSC_card):
        output_id = "000?"
    else:
        output_id = "0000"         
    if((if_EMS_error == False) and (if_FW_error == False)):
        print(f"  [EMS1-{output_id}][ACL - DHCP L2Agent] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"  [EMS1-{output_id}][ACL - DHCP L2Agent] Result Fail",file = open(file_name, '+a'))

def EMS_ACL_DHCP_Remote_Backup(driver,url,MSC_card,slot,username,password,file_name):
    
    if_EMS_error = False
    if_FW_error = False

    # --------------------- EMS web start ---------------------
    # EMS - ACL - DHCP Remote Backup
    
    # EMS website > login
    driver.get("http://192.168.128.8:9116/")
    time.sleep(5)
    mod.Login_EMS(driver,username,"Pqa1234!!")
    time.sleep(5)
    
    EMS_Provision_path(driver,url)
    time.sleep(2)    
    driver.find_element(By.LINK_TEXT, "ACL").click()          
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "DHCP Remote Backup").click()
    time.sleep(3)
    
    # it will crash
    # e_acl.DHCP_Remote_Backup_Apply(driver)
    # e_acl.DHCP_Remote_Backup_Slot(driver,slot)
    # e_acl.DHCP_Remote_Backup_Manual_Download(driver)

    # --------------------- EMS web end -----------------------

    # EMS Result
    if(if_EMS_error == True):
        print(f"             [ACL - DHCP Remote Backup] EMS web check fail",file = open(file_name, '+a'))
    else:
        print(f"             [ACL - DHCP Remote Backup] EMS web check pass",file = open(file_name, '+a')) 

    # FW Result
    if(if_FW_error == True):
        print(f"             [ACL - DHCP Remote Backup] FW web check fail",file = open(file_name, '+a'))
    else:
        print(f"             [ACL - DHCP Remote Backup] FW web check pass",file = open(file_name, '+a')) 

    # Final Result
    if("XB" in MSC_card):
        output_id = "000?"
    elif("XA" in MSC_card):
        output_id = "000?"
    elif("QA" in MSC_card):
        output_id = "000?"
    else:
        output_id = "0000"         
    if((if_EMS_error == False) and (if_FW_error == False)):
        print(f"  [EMS1-{output_id}][ACL - DHCP Remote Backup] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"  [EMS1-{output_id}][ACL - DHCP Remote Backup] Result Fail",file = open(file_name, '+a'))

def EMS_ACL_MAC_Count(driver,url,MSC_card,slot,port,username,password,file_name):
    

    if_EMS_error = False
    if_FW_error = False

    # --------------------- EMS web start ---------------------
    # EMS - ACL - MAC Count
    
    # EMS website > login
    driver.get("http://192.168.128.8:9116/")
    time.sleep(5)
    mod.Login_EMS(driver,username,"Pqa1234!!")
    time.sleep(5)
    
    EMS_Provision_path(driver,url)
    time.sleep(2)    
    driver.find_element(By.LINK_TEXT, "ACL").click()          
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "MAC Count").click()
    time.sleep(3)

    # Select Slot Port
    try:
        e_acl.Select_Slot(driver,slot)
        e_acl.Select_Port(driver,port)
    except:
        print(f"             [ACL - MAC Count] EMS Slot Port Select fail",file = open(file_name, '+a'))
        if_EMS_error = True
    
    if(if_EMS_error == False):

        # MAC Count Limit Test _ invalid/valid input apply check & value check
        test_keys = ["0","257","@"]
        for i in test_keys:
            e_acl.MAC_Count_Limit_Input(driver,i)
            e_acl.Save(driver)
            # wait until?
            time.sleep(1)  
            pyautogui.press("enter")            
            # try:
            #     driver.find_element(By.ID, "popupClose").click()          #need_add modify?
            #     print(f"             [ACL - MAC Count] EMS Limited Number invalid input:{i} apply Test pass*",file = open(file_name, '+a'))
            # except:
            #     print(f"             [ACL - MAC Count] EMS Limited Number invalid input:{i} apply Test fail*",file = open(file_name, '+a'))
            #     if_EMS_error = True

            # check output != input
            EMS_Reload_Page(driver,url)
            driver.find_element(By.LINK_TEXT, "ACL").click()        
            time.sleep(1)
            driver.find_element(By.LINK_TEXT, "MAC Count").click()
            time.sleep(1)   
            e_acl.Select_Slot(driver,slot)
            e_acl.Select_Port(driver,port)                     
            value = driver.find_element(By.ID, "acl_maccount_limit_num").get_attribute("value")
            if(value == i):
                print(f"             [ACL - MAC Count] EMS Limited Number invalid input:{value} = {i} Test fail",file = open(file_name, '+a'))
                if_EMS_error = True
            else:
                print(f"             [ACL - MAC Count] EMS Limited Number invalid input:{value} != {i} Test pass",file = open(file_name, '+a'))

        test_keys = ["1","256"]
        for i in test_keys:
            e_acl.MAC_Count_Limit_Input(driver,i)
            e_acl.Save(driver)
            time.sleep(1)  
            pyautogui.press("enter")
            # try:
            #     driver.find_element(By.ID, "popupClose").click()         #need_add modify?
            #     print(f"             [ACL - MAC Count] EMS Limited Number valid input:{i} apply Test fail*",file = open(file_name, '+a'))
            #     if_EMS_error = True
            # except:
            #     print(f"             [ACL - MAC Count] EMS Limited Number valid input:{i} apply Test pass*",file = open(file_name, '+a'))
            
            # check output = input            
            EMS_Reload_Page(driver,url)
            driver.find_element(By.LINK_TEXT, "ACL").click()        
            time.sleep(1)
            driver.find_element(By.LINK_TEXT, "MAC Count").click()
            time.sleep(1)   
            e_acl.Select_Slot(driver,slot)
            e_acl.Select_Port(driver,port)                     
            value = driver.find_element(By.ID, "acl_maccount_limit_num").get_attribute("value")
            if(value != i):
                print(f"             [ACL - MAC Count] EMS Limited Number valid input:{value} != {i} Test fail",file = open(file_name, '+a'))
                if_EMS_error = True
            else:
                print(f"             [ACL - MAC Count] EMS Limited Number valid input:{value} = {i} Test pass",file = open(file_name, '+a'))

        # New Vlan, Limit
        test_keys = ["0","257","@"]
        for i in test_keys:
            e_acl.MAC_Count_Limit_New(driver) 
            e_acl.MAC_Count_Limit_New_Vlan(driver,"4094") 
            e_acl.MAC_Count_Limit_New_Limit(driver,i) 
            e_acl.OK(driver)
            time.sleep(1)  
            pyautogui.press("enter") 
            try:
                driver.find_element(By.ID, "popupClose").click()
                print(f"             [ACL - MAC Count] EMS New invalid input:{i} apply Test pass",file = open(file_name, '+a'))
            except:
                print(f"             [ACL - MAC Count] EMS New invalid input:{i} apply Test fail",file = open(file_name, '+a'))
                if_EMS_error = True
        test_keys = ["1","256"]
        for i in test_keys:
            e_acl.MAC_Count_Limit_New(driver) 
            e_acl.MAC_Count_Limit_New_Vlan(driver,"4094") 
            e_acl.MAC_Count_Limit_New_Limit(driver,i) 
            e_acl.OK(driver)
            time.sleep(1)  
            pyautogui.press("enter") 
            try:
                driver.find_element(By.ID, "popupClose").click()
                print(f"             [ACL - MAC Count] EMS New valid input:{i} apply Test fail",file = open(file_name, '+a'))
                if_EMS_error = True
            except:
                print(f"             [ACL - MAC Count] EMS New valid input:{i} apply Test pass",file = open(file_name, '+a'))
        # check value
        if_find = False
        count = 0
        for index in range(driver.find_elements(By.CLASS_NAME, "zy_tr.acl_maccount_table_row").__len__()):
            if(driver.find_elements(By.CLASS_NAME, "zy_td.acl_maccount_table_vid")[index].get_attribute("textContent") == "4094"):
                if(driver.find_elements(By.CLASS_NAME, "zy_td.acl_maccount_table_limit")[index].text == "256"):
                    if_find = True                                                       
                    print(f"             [ACL - MAC Count] EMS New input on table Test pass",file = open(file_name, '+a'))
                count = count + 1                                       
        if(if_find == False):
            print(f"             [ACL - MAC Count] EMS New input on table Test fail",file = open(file_name, '+a'))                    
            if_EMS_error = True
        if(count > 1):
            print(f"             [ACL - MAC Count] EMS New input one identical Vlan Test fail",file = open(file_name, '+a'))                    
            if_EMS_error = True
        else:
            print(f"             [ACL - MAC Count] EMS New input one identical Vlan Test pass",file = open(file_name, '+a'))                                
        # --------------------- EMS web end -----------------------
        # --------------------- FW web check start ----------------
        # ACL > MAC Count 
        driver.get(url) 
        time.sleep(3)
        mod.Login(driver,username,password) 
        time.sleep(3)    
        mod.Switch_Default(driver)
        mod.Page_Switch(driver,"ACL")
        time.sleep(1)    
        driver.find_element(By.LINK_TEXT, "MAC Count").click() 
        mod.Switch_Frame(driver)
        time.sleep(1) 
        # select slot 
        driver.find_elements(By.NAME, "rpdsl_rdoSlt")[int(slot)-1].click()
        # select port
        driver.find_elements(By.NAME, "rpdsl_rdoSlt")[int(port)-1].click()
        # check value
        if_find = False        
        for index in range(1, driver.find_elements(By.CLASS_NAME, "tablelist").__len__()):
            if(driver.find_elements(By.CLASS_NAME, "rpmacCount_perVlanVlan")[index].get_attribute("textContent") == "4094"):
                if(driver.find_elements(By.CLASS_NAME, "rpmacCount_perVlanLimit")[index].text == "256"):
                    if_find = True                                                       
                    print(f"             [ACL - MAC Count] FW New input on table Test pass",file = open(file_name, '+a'))
                    break
        if(if_find == False):
            print(f"             [ACL - MAC Count] FW New input on table Test fail",file = open(file_name, '+a'))
            if_FW_error = True
        # --------------------- FW web check end ------------------

        # Select One Delete Test
        # --------------------- EMS web start ---------------------
        # EMS - ACL - MAC Count        
        driver.get("http://192.168.128.8:9116/")
        time.sleep(5)
        mod.Login_EMS(driver,username,"Pqa1234!!")
        time.sleep(5)        
        EMS_Provision_path(driver,url)
        time.sleep(2)    
        driver.find_element(By.LINK_TEXT, "ACL").click()          
        time.sleep(1)
        driver.find_element(By.LINK_TEXT, "MAC Count").click()
        time.sleep(3)
        if_find = False        
        for index in range(driver.find_elements(By.CLASS_NAME, "zy_tr.acl_maccount_table_row").__len__()):
            if(driver.find_elements(By.CLASS_NAME, "zy_td.acl_maccount_table_vid")[index].get_attribute("textContent") == "4094"):
                if(driver.find_elements(By.CLASS_NAME, "zy_td.acl_maccount_table_limit")[index].text == "256"):                    
                    if_find = True 
                    e_acl.MAC_Count_Limit_Select(driver,True,index+1)
                    e_acl.MAC_Count_Limit_Delete(driver)
                    time.sleep(1)  
                    pyautogui.press("enter")  
                    if_find_2 = False  
                    for index in range(driver.find_elements(By.CLASS_NAME, "zy_tr.acl_maccount_table_row").__len__()):
                        if(driver.find_elements(By.CLASS_NAME, "zy_td.acl_maccount_table_vid")[index].get_attribute("textContent") == "4094"):
                            if(driver.find_elements(By.CLASS_NAME, "zy_td.acl_maccount_table_limit")[index].text == "256"):                    
                                if_find_2 = True
                                print(f"             [ACL - MAC Count] EMS New Delete Test fail",file = open(file_name, '+a'))                    
                                if_EMS_error = True
                                break
                    if(if_find_2 == False):
                        print(f"             [ACL - MAC Count] EMS New Delete Test pass",file = open(file_name, '+a'))                    
                    break
        if(if_find == False):
            print(f"             [ACL - MAC Count] EMS New not found to be deleted Delete Test fail",file = open(file_name, '+a'))                    
            if_EMS_error = True        
        # --------------------- EMS web end -----------------------
        # --------------------- FW web check start ----------------
        # ACL > MAC Count 
        driver.get(url) 
        time.sleep(3)
        mod.Login(driver,username,password) 
        time.sleep(3)    
        mod.Switch_Default(driver)
        mod.Page_Switch(driver,"ACL")
        time.sleep(1)    
        driver.find_element(By.LINK_TEXT, "MAC Count").click() 
        mod.Switch_Frame(driver)
        time.sleep(1) 
        # select slot 
        driver.find_elements(By.NAME, "rpdsl_rdoSlt")[int(slot)-1].click()
        # select port
        driver.find_elements(By.NAME, "rpdsl_rdoSlt")[int(port)-1].click()
        # check value
        if_find = False        
        for index in range(1, driver.find_elements(By.CLASS_NAME, "tablelist").__len__()):
            if(driver.find_elements(By.CLASS_NAME, "rpmacCount_perVlanVlan")[index].get_attribute("textContent") == "4094"):
                if(driver.find_elements(By.CLASS_NAME, "rpmacCount_perVlanLimit")[index].text == "256"):
                    if_find = True                                                       
                    print(f"             [ACL - MAC Count] FW New Delete Test fail",file = open(file_name, '+a'))
                    if_FW_error = True
                    break
        if(if_find == False):
            print(f"             [ACL - MAC Count] FW New Delete Test pass",file = open(file_name, '+a'))            
        # --------------------- FW web check end ------------------
        
        # Select All Delete Test
        # --------------------- EMS web start ---------------------
        # EMS - ACL - MAC Count        
        driver.get("http://192.168.128.8:9116/")
        time.sleep(5)
        mod.Login_EMS(driver,username,"Pqa1234!!")
        time.sleep(5)        
        EMS_Provision_path(driver,url)
        time.sleep(2)    
        driver.find_element(By.LINK_TEXT, "ACL").click()          
        time.sleep(1)
        driver.find_element(By.LINK_TEXT, "MAC Count").click()
        time.sleep(3)
        e_acl.MAC_Count_Limit_Select_All(driver,True)
        e_acl.MAC_Count_Limit_Delete(driver)
        time.sleep(1)  
        pyautogui.press("enter") 
        try:
            driver.find_element(By.ID, "zy_td.zy_checkbox")
            print(f"             [ACL - MAC Count] EMS New Delete All Test fail",file = open(file_name, '+a'))                               
            if_EMS_error = True
        except:
            print(f"             [ACL - MAC Count] EMS New Delete All Test pass",file = open(file_name, '+a'))                                                       
        # --------------------- EMS web end -----------------------
        # --------------------- FW web check start ----------------
        # ACL > MAC Count 
        driver.get(url) 
        time.sleep(3)
        mod.Login(driver,username,password) 
        time.sleep(3)    
        mod.Switch_Default(driver)
        mod.Page_Switch(driver,"ACL")
        time.sleep(1)    
        driver.find_element(By.LINK_TEXT, "MAC Count").click() 
        mod.Switch_Frame(driver)
        time.sleep(1) 
        # select slot 
        driver.find_elements(By.NAME, "rpdsl_rdoSlt")[int(slot)-1].click()
        # select port
        driver.find_elements(By.NAME, "rpdsl_rdoSlt")[int(port)-1].click()
        # check value
        try:
            driver.find_element(By.CLASS_NAME, "tablelist")
            print(f"             [ACL - MAC Count] FW New Delete All Test fail",file = open(file_name, '+a'))                               
            if_EMS_error = True
        except:
            print(f"             [ACL - MAC Count] FW New Delete All Test pass",file = open(file_name, '+a'))                                                                                      
        # --------------------- FW web check end ------------------


    # EMS Result
    if(if_EMS_error == True):
        print(f"             [ACL - MAC Count] EMS web check fail",file = open(file_name, '+a'))
    else:
        print(f"             [ACL - MAC Count] EMS web check pass",file = open(file_name, '+a')) 

    # FW Result
    if(if_FW_error == True):
        print(f"             [ACL - MAC Count] FW web check fail",file = open(file_name, '+a'))
    else:
        print(f"             [ACL - MAC Count] FW web check pass",file = open(file_name, '+a')) 

    # Final Result 
    if("XB" in MSC_card):
        output_id = "000?"
    elif("XA" in MSC_card):
        output_id = "000?"
    elif("QA" in MSC_card):
        output_id = "000?"
    else:
        output_id = "0000"         
    if((if_EMS_error == False) and (if_FW_error == False)):
        print(f"  [EMS1-{output_id}][ACL - MAC Count] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"  [EMS1-{output_id}][ACL - MAC Count] Result Fail",file = open(file_name, '+a'))



# --------------------------------------------------------------------------
def EMS_Reload_Page(driver,url):
    # click IES 192.168.xxx.xxx twice to reload page 
    driver.switch_to.default_content() 
    url_ip = url.split("/")[2] 
    driver.find_element(By.XPATH, f'//*[@title="IES6217_{url_ip[8:]}({url_ip})"]').click()
    driver.find_element(By.XPATH, f'//*[@title="IES6217_{url_ip[8:]}({url_ip})"]').click()
    driver.switch_to.frame(0)
    time.sleep(1)


# use to detect chrome extension popup window text, need import win32
# def dumpWindow(hwnd, wantedText=None, wantedClass=None):
#     '''
#     :param hwnd: 窗口句柄
#     :param wantedText: 指定子窗口名
#     :param wantedClass: 指定子窗口类名
#     :return: 返回父窗口下所有子窗体的句柄
#     '''
#     windows = []
#     hwndChild = None
#     while True:
#         hwndChild = win32gui.FindWindowEx(hwnd, hwndChild, wantedClass, wantedText)
#         if hwndChild:
#             textName = win32gui.GetWindowText(hwndChild)
#             className = win32gui.GetClassName(hwndChild)
#             windows.append((hwndChild, textName, className))
#         else:
#             return windows



# EMS Test
# ======================================================================================= 