from selenium.webdriver.common.by import By
from os import times
import time
from attr import field
from pyrsistent import s
import selenium_module as mod
from selenium.webdriver.support.ui import Select


def Action(driver,text):
    Select(driver.find_element(By.ID, "rpxont_action")).select_by_visible_text(text)

def Create_config_with_default_template_profile(driver,text):
    Select(driver.find_element(By.ID, "rpXgponOntConfig_OntTemplate")).select_by_visible_text(text)

def ONT_description(driver,value):
    driver.find_element(By.ID, "rpxont_create_description").clear()
    driver.find_element(By.ID, "rpxont_create_description").send_keys(value)

def Apply(driver):
    driver.find_element(By.NAME, "rpXGponOntSetup_btnApply").click()
