from os import times
import time
from attr import field
from pyrsistent import s
import module.selenium_module as mod
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import module.ems_module as e_mod

# OLT Config

def OLT_Config_Slot_Port(driver,slot,port):
    Select(driver.find_element(By.ID,"xpon_oltconfig_slot_combobox")).select_by_value(slot)
    Select(driver.find_element(By.ID,"xpon_oltconfig_port_combobox")).select_by_visible_text(port)

def OLT_Config_Active(driver,request):
    e_mod.Checkbox_EMS(driver,"xpon_oltconfig_active_checkbox",request)

def OLT_Config_Name(driver,text):
    e_mod.Input_text(driver,By.ID,"xpon_oltconfig_name_text",text)

def OLT_Config_Register_Method(driver,text):
    Select(driver.find_element(By.ID,"xpon_oltconfig_method_combobox")).select_by_visible_text(text)

def OLT_Config_Max_distance_for_ONT(driver,text):
    e_mod.Input_text(driver,By.ID,"xpon_oltconfig_distance_text",text)

def OLT_Config_ONT_Template(driver,text):
    e_mod.Input_text(driver,By.ID,"xpon_oltconfig_template_combobox",text)

def OLT_Config_Fec(driver,request):
    e_mod.Checkbox_EMS(driver,"xpon_oltconfig_fec_checkbox",request)

def OLT_Config_Apply(driver):
    e_mod.Click(driver,By.ID,"xpon_oltconfig_apply_button")
