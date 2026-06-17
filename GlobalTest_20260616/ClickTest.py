from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
import pytest, time, json, os, re
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options #無痕模式需要的
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import ElementNotInteractableException
from pytest_assume.plugin import assume
from libs.func import *
from deepdiff import DeepDiff

file = open("environment_parameter.json")
data = json.load(file)
file.close()

waitTime = data["ELEMENT"]["wait_time"]
uploadPath = data["AUTO_SITE"]["upload_path"]
emsURL = data["EMS"]["url"]
emsUsr = data["EMS"]["login_username"]
emsPwd = data["EMS"]["login_password"]
dutName = data["ZYXEL_DUT"]["NODE1"]["name"]
dutNodeName = data["ZYXEL_DUT"]["NODE1"]["name_display"]
dutDesc = data["ZYXEL_DUT"]["NODE1"]["description"]
dutIp = data["ZYXEL_DUT"]["NODE1"]["ip"]
dutURL = data["ZYXEL_DUT"]["NODE1"]["url"]
dutAdminName = data["ZYXEL_DUT"]["NODE1"]["login_username"]
dutAdminPwd = data["ZYXEL_DUT"]["NODE1"]["login_password"]
dutSet = data["ZYXEL_DUT"]["NODE1"]["set_community"]
dutGet = data["ZYXEL_DUT"]["NODE1"]["get_community"]
dutSnmpVer = data["ZYXEL_DUT"]["NODE1"]["snmp_ver"]
dutSnmp3Auth = data["ZYXEL_DUT"]["NODE1"]["snmp3_auth"]
dutSnmp3Hash = data["ZYXEL_DUT"]["NODE1"]["snmp3_hash"]
dutSnmp3Encrypt = data["ZYXEL_DUT"]["NODE1"]["snmp3_encrypt"]
dutAddr = data["ZYXEL_DUT"]["NODE1"]["geo_position"]
dutType = data["ZYXEL_DUT"]["NODE1"]["type"]
dutSlotTotal = data["ZYXEL_DUT"]["NODE1"]["slot_total"]

exeServiceOnt = data["ZYXEL_DUT"]["NODE1"]["ONTINFO"]["XPON"]["exe_provision_ont"]
serviceOntSN = data["ZYXEL_DUT"]["NODE1"]["ONTINFO"]["XPON"][exeServiceOnt]["sn_16"]
serviceOntPW = data["ZYXEL_DUT"]["NODE1"]["ONTINFO"]["XPON"][exeServiceOnt]["pw"]
serviceOntType = data["ZYXEL_DUT"]["NODE1"]["ONTINFO"]["XPON"][exeServiceOnt]["type"]

ontInfo = [data["ZYXEL_DUT"]["NODE1"]["ONTINFO"]["XPON"][exeServiceOnt]["slot_id"]
           ,data["ZYXEL_DUT"]["NODE1"]["ONTINFO"]["XPON"][exeServiceOnt]["port_id"]
           ,data["ZYXEL_DUT"]["NODE1"]["ONTINFO"]["XPON"][exeServiceOnt]["ont_id"]]
checkValue = []

class Test():
    def setup_method(self):
        options = webdriver.ChromeOptions()
        options.add_argument('ignore-certificate-errors')
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.implicitly_wait(waitTime)
        self.URL = emsURL
        self.vars = {}
        self.driver.get(self.URL)
        self.driver.maximize_window()
        self.driver.find_element(By.ID, "name").send_keys(emsUsr)
        self.driver.find_element(By.ID, "passwd").clear()
        self.driver.find_element(By.ID, "passwd").send_keys(emsPwd)
        self.driver.find_element(By.ID, "signin").click()
        WebDriverWait(self.driver, 180).until(EC.visibility_of_element_located((By.ID,"index_t_userName")))

    def teardown_method(self):
        self.driver.quit()

    def test_changePassword(self):
        self.driver.find_element(By.LINK_TEXT, "Dashboard").click()
        time.sleep(3)
        self.driver.find_element(By.CSS_SELECTOR, "#index_userMenu > img").click()
        self.driver.find_element(By.ID, "index_change_password").click()
        self.driver.find_element(By.CSS_SELECTOR, "#change_password_diag span").click()
        time.sleep(3)
        with assume: assert self.driver.find_element(By.ID, "i_menu_dashboard").get_attribute("className") == "active"
        with assume: assert self.driver.find_element(By.ID, "dashboard_net_title").is_displayed()

        self.driver.find_element(By.LINK_TEXT, "Dashboard").click()
        time.sleep(3)
        self.driver.find_element(By.CSS_SELECTOR, "#index_userMenu > img").click()
        self.driver.find_element(By.ID, "index_change_password").click()
        self.driver.find_element(By.ID, "change_password_close_btn").click()
        time.sleep(3)
        with assume: assert self.driver.find_element(By.ID, "i_menu_dashboard").get_attribute("className") == "active"
        with assume: assert self.driver.find_element(By.ID, "dashboard_net_title").is_displayed()

        self.driver.find_element(By.LINK_TEXT, "Dashboard").click()
        time.sleep(3)
        self.driver.find_element(By.CSS_SELECTOR, "#index_userMenu > img").click()
        self.driver.find_element(By.ID, "index_change_password").click()
        self.driver.find_element(By.ID, "change_password_diag").click()
        time.sleep(3)
        with assume: assert self.driver.find_element(By.ID, "i_menu_dashboard").get_attribute("className") == "active"
        with assume: assert self.driver.find_element(By.ID, "dashboard_net_title").is_displayed()

        self.driver.find_element(By.LINK_TEXT, "Dashboard").click()
        time.sleep(3)
        self.driver.find_element(By.CSS_SELECTOR, "#index_userMenu > img").click()
        self.driver.find_element(By.ID, "index_change_password").click()
        self.driver.find_element(By.CSS_SELECTOR, "#change_password_diag .button_green").click()
        self.driver.find_element(By.CSS_SELECTOR, "#message_diag > div > div > div.modal-footer > button").click()
        time.sleep(3)
        with assume: assert self.driver.find_element(By.ID, "i_menu_dashboard").get_attribute("className") == "active"
        with assume: assert self.driver.find_element(By.ID, "dashboard_net_title").is_displayed()

        self.driver.find_element(By.LINK_TEXT, "Dashboard").click()
        time.sleep(3)
        self.driver.find_element(By.CSS_SELECTOR, "#index_userMenu > img").click()
        self.driver.find_element(By.ID, "index_change_password").click()
        self.driver.find_element(By.CSS_SELECTOR, "#change_password_diag .button_green").click()
        self.driver.find_element(By.CSS_SELECTOR, "#message_diag > div > div > div.modal-header > button").click()
        time.sleep(3)
        with assume: assert self.driver.find_element(By.ID, "i_menu_dashboard").get_attribute("className") == "active"
        with assume: assert self.driver.find_element(By.ID, "dashboard_net_title").is_displayed()
        
