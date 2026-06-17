from selenium.webdriver.common.by import By
from os import times
import time
from attr import field
from pyrsistent import s
import selenium_module as mod
from selenium.webdriver.support.ui import Select

def Save(driver):
    driver.find_element(By.NAME, "rpConfigSave").click()

def Back(driver):
    driver.find_element(By.NAME, "rpConfigSaveBack").click()
