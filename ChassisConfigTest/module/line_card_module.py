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
            driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlot']/option[{slot}]").click()
        except:
            time.sleep(1)
        try:
            if(driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlot']/option[{slot}]").is_selected() == True):
                retry = False
        except:
            time.sleep(1)

# Lcman

def Lcman_Action(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rplcman_sltAction']/option[{sel}]").click()

def Lcman_Apply(driver):
    driver.find_element(By.NAME, "rpLcmanApply").click()

def Boot_Slot_Select(driver,slot):
    retry = True
    while(retry == True):
        try:
            driver.find_element(By.XPATH, f"//*[@name='rplcman_bootSlot']/option[{slot}]").click()
        except:
            time.sleep(1)
        try:
            if(driver.find_element(By.XPATH, f"//*[@name='rplcman_bootSlot']/option[{slot}]").is_selected() == True):
                retry = False
        except:
            time.sleep(1)

def Boot_Index(driver,index):
    driver.find_element(By.XPATH, f"//*[@name='rplcman_bootIndex']/option[{index}]").click()

def Boot_Apply(driver):
    driver.find_element(By.NAME, "rpLcmanBootApply").click()

# G.vector

def G_vector_Mode(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rplcman_gvector_sltAction']/option[{sel}]").click()

def G_vector_Apply(driver):
    driver.find_element(By.NAME, "lctbl_selLoad").click()

# PIN

def PIN_Mode(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rplcman_pin_sltAction']/option[{sel}]").click()

def PIN_Apply(driver):
    driver.find_element(By.NAME, "lctbl_selLoad").click()
