from selenium.webdriver.common.by import By
from os import times
import time
from attr import field
from pyrsistent import s
import module.selenium_module as mod
from selenium.webdriver.support.ui import Select

def Port_Select(driver,slot,port):
    Select(driver.find_element(By.ID, "xgponSelOltPort")).select_by_visible_text(f"{slot}-{port}")

def ONT_Select_1(driver,slot,port):
    Select(driver.find_element(By.ID, "xgponSelOntPort")).select_by_visible_text(f"{slot}-{port}-1")
    
def ONT_aid_Select(driver,ont):
    Select(driver.find_element(By.ID, "xgponSelOntPort")).select_by_visible_text(f"{ont}")

def Refresh(driver):
    driver.find_element(By.ID, "xgponSelLoad").click()

