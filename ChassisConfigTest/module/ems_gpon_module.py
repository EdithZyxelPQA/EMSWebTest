from os import times
import time
from attr import field
from pyrsistent import s
import module.selenium_module as mod
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import module.ems_module as e_mod

# OLT Registration

def OLT_Registration_Slot_Port(driver,slot,port):
    Select(driver.find_element(By.ID,"gpon_oltregistration_slot_combobox")).select_by_value(slot)
    Select(driver.find_element(By.ID,"gpon_oltregistration_port_combobox")).select_by_visible_text(port)

def OLT_Registration_Active(driver,request):
    e_mod.Checkbox_EMS(driver,"gpon_oltregistration_active_checkbox",request)

def OLT_Registration_Register_Method(driver,text):
    Select(driver.find_element(By.ID,"gpon_oltregistration_method_combobox")).select_by_visible_text(text)

def OLT_Registration_Keep_Alive(driver,text):
    e_mod.Input_text(driver,By.ID,"gpon_oltregistration_keepalive_text",text)

def OLT_Registration_Max_distance_for_ONT(driver,text):
    e_mod.Input_text(driver,By.ID,"gpon_oltregistration_distance_text",text)

def OLT_Registration_Transceiver(driver,text):
    Select(driver.find_element(By.ID,"gpon_oltregistration_transceiver_combobox")).select_by_value(text)

def OLT_Registration_Template_Active(driver,request):
    e_mod.Checkbox_EMS(driver,"gpon_oltregistration_templateactive_checkbox",request)

def OLT_Registration_Template(driver,text):
    e_mod.Input_text(driver,By.ID,"gpon_oltregistration_template_combobox",text)

def OLT_Registration_Apply(driver):
    e_mod.Click(driver,By.ID,"gpon_oltregistration_apply_btn")
