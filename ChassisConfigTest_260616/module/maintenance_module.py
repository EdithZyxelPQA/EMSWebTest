from selenium.webdriver.common.by import By
from os import times
import time
from attr import field
from pyrsistent import s
import module.selenium_module as mod
from selenium.webdriver.support.ui import Select

def Config_Reset(driver):
    driver.find_element(By.NAME, "rpConfigReset").click()