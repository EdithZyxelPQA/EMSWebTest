from selenium.webdriver.common.by import By
from os import times
import time
from attr import field
from pyrsistent import s
import selenium_module as mod
from selenium.webdriver.support.ui import Select

# Main

def Main_Delete_Select_All(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponOntConfig_chkDelall")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Main_Delete(driver):
    driver.find_element(By.ID, "rpXgponOntConfig_TablebtnDelete").click()

def Main_Select_ONT_Template(driver,text):
    Select(driver.find_element(By.NAME, "rpXgponOntConfig_TableOntTemplate")).select_by_visible_text(text)

# QoS

def QoS_New(driver):
    driver.find_element(By.CLASS_NAME, "font-btn").click()

def QoS_Delete(driver):
    driver.find_element(By.ID, "rpXgponOntConfigQoS_TablebtnDelete").click()

def QoS_Delete_All_Select(driver,request):
    check_box = driver.find_element(By.NAME, "rpXGSponOntConfig_chkDelall")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def QoS_Delete_Select(driver,index):
    driver.find_elements(By.NAME, "rpXgponOntConfigQoS_chkDel")[index-1].click()

def QoS_New_Apply(driver):
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[0].click()

def QoS_New_ONT(driver,text):
    Select(driver.find_element(By.ID, "rpXgponOntConfigQoSLoad_IptTableOntPort")).select_by_visible_text(text)

def QoS_New_Tcont_Server(driver,text):
    Select(driver.find_element(By.ID, "rpXgponOntConfigQoS_qosId")).select_by_visible_text(text)

def QoS_New_US_Bandwidth_Profile(driver,text):
    Select(driver.find_element(By.ID, "rpXgponOntConfigQoSLoad_TableUsBwProfile")).select_by_visible_text(text)

def QoS_New_DS_Bandwidth_Profile(driver,text):
    Select(driver.find_element(By.ID, "rpXgponOntConfigQoSLoad_TableDsBwProfile")).select_by_visible_text(text)

# FDB

def FDB_New(driver):
    driver.find_element(By.CLASS_NAME, "font-btn").click()

def FDB_Delete(driver):
    driver.find_element(By.ID, "rpXgponOntConfig_TablebtnDelete").click()

def FDB_Delete_All_Select(driver,request):
    check_box = driver.find_element(By.NAME, "rpXgponOntConfigFdb_chkAllDel")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def FDB_Delete_Select(driver,index):
    driver.find_elements(By.NAME, "rpXgponOntConfigFdb_chkDel")[index-1].click()

def FDB_New_Apply(driver):
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[0].click()

def FDB_New_ONT(driver,text):
    Select(driver.find_element(By.ID, "rpXgponOntConfigFdb_IptTableOntPort")).select_by_visible_text(text)

def FDB_New_VLAN(driver,value):
    driver.find_element(By.ID, "rpXgponOntConfigFdb_TableVLAN").clear()
    driver.find_element(By.ID, "rpXgponOntConfigFdb_TableVLAN").send_keys(value)

def FDB_New_MAC(driver,value):
    driver.find_element(By.ID, "rpXgponOntConfigFdb_TableMac").clear()
    driver.find_element(By.ID, "rpXgponOntConfigFdb_TableMac").send_keys(value)




