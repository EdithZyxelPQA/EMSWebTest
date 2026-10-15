# 環境架設
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
# driver = webdriver.Chrome()
# driver = webdriver.Firefox()
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
# pip install webdriver-manager
# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

import xpon_module as xpon
import selenium_module as mod
import xpon_olt_status_module as olts
import xpon_olt_config_module as oltc
import xpon_batch_ont_config_module as bat
import xpon_ont_config_module as ontc
import xpon_profiles_module as pro
# import multicast_module as mul

# copy from GLC project-------------
import acl_module as acl  
import glc_test_module as glc
# ----------------------------------

from selenium.webdriver.support.ui import Select
import time
import datetime
import pyautogui
from docx import Document
from docx.shared import Inches

import ems_acl_module as e_acl
import ems_profile_module as e_pro
import ems_test_module as ems

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from customdriver import CustomDriver
import variable_module
import get_card

# import videocap_module as videocap

time_sleep_before_find_element = 0 # 0.1
driver = CustomDriver(time_sleep = time_sleep_before_find_element)

# 讀取ENV.txt檔
set_up_file = open("ENV.txt",'r')
lines = set_up_file.readlines()
set_up_file.close()
url = lines[0].split("=")[1]
url_ip = url.split("/")[2] 
username = lines[1].split("=")[1]
password = lines[2].split("=")[1]
loop = int(lines[3].split("'")[1])

#Card
msc_slot = lines[6].split("'")[1]
msc_port = lines[7].split("'")[1]
glc_slot = lines[8].split("'")[1]
glc_port = lines[9].split("'")[1]

#Gpon
slot_1_aid = lines[12].split("'")[1]
pon_1_aid = lines[13].split("'")[1]
ont_1_1 = lines[16].split("'")[1]
ont_1_2 = lines[17].split("'")[1]
ont_1_1_aid = lines[19].split("'")[1]
ont_1_2_aid = lines[20].split("'")[1]

slot_2_aid = lines[24].split("'")[1]
pon_2_aid = lines[25].split("'")[1]
ont_2_1 = lines[28].split("'")[1]
ont_2_2 = lines[29].split("'")[1]
ont_2_1_aid = lines[31].split("'")[1]
ont_2_2_aid = lines[32].split("'")[1]

ont_1_1_sn = lines[36].split("'")[1]
ont_1_1_pw = lines[37].split("'")[1]
ont_1_1_ont_USER = lines[38].split("=")[1]
ont_1_1_ont_PW = lines[39].split("=")[1]

ont_1_2_sn = lines[41].split("'")[1]
ont_1_2_pw = lines[42].split("'")[1]
ont_1_2_ont_USER = lines[43].split("=")[1]
ont_1_2_ont_PW = lines[44].split("=")[1]

ont_2_1_sn = lines[46].split("'")[1]
ont_2_1_pw = lines[47].split("'")[1]
ont_2_1_ont_USER = lines[48].split("=")[1]
ont_2_1_ont_PW = lines[49].split("=")[1]

ont_2_2_sn = lines[51].split("'")[1]
ont_2_2_pw = lines[52].split("'")[1]
ont_2_2_ont_USER = lines[53].split("=")[1]
ont_2_2_ont_PW = lines[54].split("=")[1]

#Xpon
slot_x_1_aid = lines[58].split("'")[1]
pon_x_1_aid = lines[59].split("'")[1]
ont_x_1_1 = lines[62].split("'")[1]
ont_x_1_2 = lines[63].split("'")[1]
ont_x_1_1_aid = lines[65].split("'")[1]
ont_x_1_2_aid = lines[66].split("'")[1]

slot_x_2_aid = lines[70].split("'")[1]
pon_x_2_aid = lines[71].split("'")[1]
ont_x_2_1 = lines[74].split("'")[1]
ont_x_2_2 = lines[75].split("'")[1]
ont_x_2_1_aid = lines[77].split("'")[1]
ont_x_2_2_aid = lines[78].split("'")[1]

ont_x_1_1_sn = lines[82].split("'")[1]
ont_x_1_1_pw = lines[83].split("'")[1]
ont_x_1_1_ont_USER = lines[84].split("=")[1]
ont_x_1_1_ont_PW = lines[85].split("=")[1]

ont_x_1_2_sn = lines[87].split("'")[1]
ont_x_1_2_pw = lines[88].split("'")[1]
ont_x_1_2_ont_USER = lines[89].split("=")[1]


ont_x_1_2_ont_PW = lines[90].split("=")[1]

ont_x_2_1_sn = lines[92].split("'")[1]
ont_x_2_1_pw = lines[93].split("'")[1]
ont_x_2_1_ont_USER = lines[94].split("=")[1]
ont_x_2_1_ont_PW = lines[95].split("=")[1]

ont_x_2_2_sn = lines[97].split("'")[1]
ont_x_2_2_pw = lines[98].split("'")[1]
ont_x_2_2_ont_USER = lines[99].split("=")[1]
ont_x_2_2_ont_PW = lines[100].split("=")[1]

# service_mode_x_1 = lines[104].split("'")[1]
service_mode_x_1 = ''

# snmp_get = lines[110].split("=")[1]
snmp_get = ''
snmp_set = '' #lines[111].split("=")[1]
snmp_version = '' #lines[112].split("=")[1]

ont_1_1 = int(ont_1_1)-1
ont_1_2 = int(ont_1_2)-1
ont_2_1 = int(ont_2_1)-1
ont_2_2 = int(ont_2_2)-1

ems_password = "Pqa1234!!"
test_retry_num = 3

start_time = time.time()

#    FW Web CardType Case       
# ====================================

driver.get(url) # 連上網頁
mod.Login(driver,username,password) # 登入
 
# FW get msc_card_type, msc_version
mod.Switch_Default(driver)
mod.Page_Switch(driver,"Home")
time.sleep(5)
mod.Switch_Frame(driver)
msc_card_type = driver.find_elements('class name',"td-table-content.SysinfoCardType.left-wrapper")[int(msc_slot)-1].get_attribute("textContent")
variable_module.msc_card_type = msc_card_type # test
msc_version = driver.find_elements('class name',"td-table-content.Sysinfofwversion.left-wrapper")[int(msc_slot)-1].get_attribute("textContent")

# Config Reset ---
# ems.Maintenance_Config_Reset(driver)  #*自動化全程都不能點其他東西，測試頁面必須在最前面

# FW Sys - Access Control - SNMP, input value from ENV.txt ---
# FW Sys - User Account, input value from ENV.txt ---
ems.EMS_Set_Prepare(driver,snmp_get,snmp_set,snmp_version,username,password)

# cardtype case
list1 = get_card.get_card_case(driver,glc_port,pon_x_1_aid,pon_1_aid,file_name='')

# kick?
# driver.quit()
ems.FW_Logout(driver)


#    EMS Web        
# ====================================
# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
# driver = CustomDriver(time_sleep = time_sleep_before_find_element)
driver.get("https://192.168.128.8:9116/") 
time.sleep(5)
mod.Login_EMS(driver,username,ems_password)
time.sleep(5)
driver.find_element('id','about').click()
time.sleep(3)
emsversion = driver.find_element('id','emsversion').text.split("\n")[0]
time.sleep(5)
driver.find_element('xpath', '//*[@type="button" and @class="button button_green"]').click()    ### click close

#    Set File Name
date1 = str(datetime.datetime.now()).split(":")[0]
date2 = str(datetime.datetime.now()).split(":")[1]
file_name = f"Output\Web_EMS_{emsversion}_{date1}{date2}.txt"
# file_name = f"Output\Web_EMS_test.txt"

#    Info in File
test_report = open(file_name,"w+")
print("EMS Web Auto Report",file = open(file_name, '+a'))
print(datetime.datetime.now(),file = open(file_name, '+a'))
print(f"EMS Web IP:http://192.168.128.8:9116/  \nEMS Version:{emsversion} ",file = open(file_name, '+a'))
print(f"FW Web IP:{url}FW MSC:{msc_slot}/{msc_card_type}/{msc_version}",file = open(file_name, '+a'))
print(f"FW Web IP:{url}FW MSC:{msc_slot}-{msc_port}/{msc_card_type}/{msc_version}",file = open(file_name, '+a'))
print(f"{list1}",file = open(file_name, '+a'))
get_card.print_case(list1,file_name)
MSC_slot = list1.pop()
MSC_card = list1.pop()
print(f"  (find_element(), find_elements() will wait {time_sleep_before_find_element} sec )",file = open(file_name, '+a'))
print("======================================================================================",file = open(file_name, '+a'))

print(f"EMS Test\nTest Start",file = open(file_name, '+a')) 


###############################################

ems.Multicast_IGMP_Setup(driver,url,MSC_card,username,password,file_name)