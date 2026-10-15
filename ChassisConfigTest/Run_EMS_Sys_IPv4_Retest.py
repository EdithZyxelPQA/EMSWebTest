# Retest only Sys_IPv4_Setup (No Card Test) for one env, e.g.:
#   python -u Run_EMS_Sys_IPv4_Retest.py 168_85
import argparse
import datetime
import json
import os
import time

from selenium.webdriver.common.by import By

import module.ems_test_module as ems
import module.selenium_module as mod
from module.customdriver import CustomDriver

if not os.path.exists("Report"):
    os.makedirs("Report")

_0_lines = open(os.path.join('ENV', 'time_sleep_before_find_element.txt'), 'r').readlines()
time_sleep_before_find_element = float(_0_lines[0].split("'")[1])

parser = argparse.ArgumentParser(description="Retest Sys_IPv4_Setup")
parser.add_argument('env_id', type=str, help='env id (e.g. 168_85 -> ENV/ENV_WEB_168_85.json)')
args = parser.parse_args()
env_file = f"ENV/ENV_WEB_{args.env_id}.json"

with open(env_file, 'r', encoding='utf-8') as f:
    d = json.load(f)

url = d["ZYXEL_DUT"]["NODE1"]["url"]
url_ip = url.split("/")[2]
username = d['ZYXEL_DUT']['NODE1']["login_username"]
password = d['ZYXEL_DUT']['NODE1']["login_password"]
ems_url = d["EMS"]["url"]
ems_password = d["EMS"]["login_password"]
ems.set_ems_credentials(ems_url, ems_password)
msc_slot = d["ZYXEL_DUT"]["NODE1"]["CARDINFO"]["MSC"]["slot_id"]

start_time0 = time.time()
driver = CustomDriver(time_sleep=time_sleep_before_find_element)

# --- FW Web: MSC card type ---
driver.get(url)
mod.Login(driver, username, password)
fw_title = driver.title
mod.Switch_Default(driver)
mod.Page_Switch(driver, "Home")
time.sleep(5)
mod.Switch_Frame(driver)
MSC_card = driver.find_elements(
    'class name', "td-table-content.SysinfoCardType.left-wrapper"
)[int(msc_slot) - 1].get_attribute("textContent")
ems.FW_Logout(driver)

# --- EMS Web: version ---
driver.get(ems_url)
try:
    driver.maximize_window()
except:
    pass
time.sleep(5)
mod.Login_EMS(driver, username, ems_password)
time.sleep(5)
try:
    driver.find_element('id', 'helpMenu').click()
except:
    mod.Login_EMS(driver, username, ems_password)
    time.sleep(5)
    driver.find_element('id', 'helpMenu').click()
driver.find_element('id', 'about_ems_button').click()
time.sleep(3)
emsversion = driver.find_element('id', 'emsversion').text.split("\n")[0]
time.sleep(5)
driver.find_element('xpath', '//*[@type="button" and @class="button button_green"]').click()

# --- Report ---
date1 = str(datetime.datetime.now()).split(":")[0]
date2 = str(datetime.datetime.now()).split(":")[1]
file_name = f"Report/Web_EMS_Config_Sys_IPv4_Retest_{fw_title}_{emsversion}_{date1}{date2}_{url_ip[-3:]}.log"
ems.parameter_add("file_name", file_name)
ems.get_file_name(file_name)

print("EMS Web Auto Report (Sys_IPv4_Setup Retest)", file=open(file_name, '+a', encoding='utf-8'))
print(datetime.datetime.now(), file=open(file_name, '+a', encoding='utf-8'))
print(f"EMS Web IP:{ems_url}  \nEMS Version:{emsversion} ", file=open(file_name, '+a', encoding='utf-8'))
print(f"FW Web IP:{url}  MSC slot:{msc_slot} {MSC_card}", file=open(file_name, '+a', encoding='utf-8'))
print(f"env file:{env_file}\n", file=open(file_name, '+a', encoding='utf-8'))

ems.Sys_IPv4_Setup(driver, url, MSC_card, username, password, ems_url, ems_password, file_name)

try:
    driver.quit()
except:
    pass

total_time = time.time() - start_time0
print(f'Total time: {int(total_time/60/60)} hr {int(total_time/60%60)} min {int(total_time%60)} sec',
      file=open(file_name, '+a', encoding='utf-8'))
print(f"Report: {file_name}")
