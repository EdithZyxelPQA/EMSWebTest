from selenium.webdriver.common.by import By
from os import times
import time
from attr import field
from pyrsistent import s
import module.selenium_module as mod
from selenium.webdriver.support.ui import Select

def Active(driver,request):
    check_box = driver.find_element(By.ID, "rpXgponOltConfig_TableActive")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Name(driver,value):
    driver.find_element(By.ID, "rpXgponOltConfig_TableName").clear()
    driver.find_element(By.ID, "rpXgponOltConfig_TableName").send_keys(value)

def Tel(driver,value):
    driver.find_element(By.ID, "rpXgponOltConfig_tel").clear()
    driver.find_element(By.ID, "rpXgponOltConfig_tel").send_keys(value)

def Register_Method(driver,text):
    Select(driver.find_element(By.ID, "rpXgponOltConfig_RegisterMethod")).select_by_visible_text(text)

def Ranging_distance(driver,value):
    driver.find_element(By.ID, "rpXgponOltConfig_TableRangingDistance").clear()
    driver.find_element(By.ID, "rpXgponOltConfig_TableRangingDistance").send_keys(value)

def ONT_Template(driver,text):
    Select(driver.find_element(By.ID, "rpXgponOltConfig_TableOntTemplate")).select_by_visible_text(text)

def Apply(driver):
    driver.find_element(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only").click()




