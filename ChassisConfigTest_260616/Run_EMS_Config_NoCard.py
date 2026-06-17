# 環境架設
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
# driver = webdriver.Chrome()
# driver = webdriver.Firefox()
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
# pip install webdriver-manager
# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

import module.xpon_module as xpon
import module.selenium_module as mod
import module.xpon_olt_status_module as olts
import module.xpon_olt_config_module as oltc
import module.xpon_batch_ont_config_module as bat
import module.xpon_ont_config_module as ontc
import module.xpon_profiles_module as pro
# import multicast_module as mul

# copy from GLC project-------------
import module.acl_module as acl  
import module.glc_test_module as glc
# ----------------------------------

from selenium.webdriver.support.ui import Select
import time
import datetime
import pyautogui
from docx import Document
from docx.shared import Inches

import module.ems_acl_module as e_acl
import module.ems_profile_module as e_pro
import module.ems_test_module as ems

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from module.customdriver import CustomDriver
import module.globals
import module.get_card
from module.variable_module import *

# import videocap_module as videocap

# time_sleep_before_find_element = 0 # 0.1
driver = CustomDriver(time_sleep = time_sleep_before_find_element)



start_time = time.time()
start_time0 = time.time()

# create "Report" folder if it doesn't exist
if not os.path.exists("Report"):
    os.makedirs("Report")


#    FW Web CardType Case       
# ====================================

driver.get(url) # 連上網頁
try:
    driver.maximize_window()    
except:
    pass
mod.Login(driver,username,password) # 登入
 
if "Neox".lower() in driver.title.lower():
    if_Neox = True
ems.parameter_add("if_Neox",if_Neox)

# FW get msc_card_type, msc_version
mod.Switch_Default(driver)
mod.Page_Switch(driver,"Home")
time.sleep(5)
mod.Switch_Frame(driver)
msc_card_type = driver.find_elements('class name',"td-table-content.SysinfoCardType.left-wrapper")[int(msc_slot)-1].get_attribute("textContent")
module.globals.msc_card_type = msc_card_type # test
msc_version = driver.find_elements('class name',"td-table-content.Sysinfofwversion.left-wrapper")[int(msc_slot)-1].get_attribute("textContent")

# Config Reset ---
ems.Maintenance_Config_Reset(driver)  #*自動化全程都不能點其他東西，測試頁面必須在最前面

# FW Sys - Access Control - SNMP, input value from ENV.txt ---
# FW Sys - User Account, input value from ENV.txt ---
ems.EMS_Set_Prepare(driver,snmp_get,snmp_set,snmp_version,username,password)

# cardtype case
list1 = module.get_card.get_card_case(driver,glc_port,pon_x_1_aid,pon_1_aid,msc_port,file_name='')

# kick?
# driver.quit()
ems.FW_Logout(driver)


#    EMS Web        
# ====================================
# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
# driver = CustomDriver(time_sleep = time_sleep_before_find_element)
driver.get(ems_url) 
time.sleep(5)
mod.Login_EMS(driver,username,ems_password)
time.sleep(5)
try:
    driver.find_element('id','helpMenu').click()
except:
    mod.Login_EMS(driver,username,ems_password)
    time.sleep(5)
    driver.find_element('id','helpMenu').click()
driver.find_element('id','about_ems_button').click()
time.sleep(3)
emsversion = driver.find_element('id','emsversion').text.split("\n")[0]
time.sleep(5)
driver.find_element('xpath', '//*[@type="button" and @class="button button_green"]').click()    ### click close

#    Set File Name
date1 = str(datetime.datetime.now()).split(":")[0]
date2 = str(datetime.datetime.now()).split(":")[1]
file_name = f"Report\Web_EMS_Config_NoCard_{emsversion}_{date1}{date2}.txt"
# file_name = f"Output\Web_EMS_test.txt"
ems.parameter_add("file_name",file_name)
ems.get_file_name(file_name)

#    Info in File
test_report = open(file_name,"w+")
print("EMS Web Auto Report",file = open(file_name, '+a'))
print(datetime.datetime.now(),file = open(file_name, '+a'))
print(f"EMS Web IP:{ems_url}  \nEMS Version:{emsversion} ",file = open(file_name, '+a'))
print(f"FW Web IP:{url}FW MSC:{msc_slot}-{msc_port}/{msc_card_type}/{msc_version}",file = open(file_name, '+a'))
print(f"{list1}",file = open(file_name, '+a'))
module.get_card.print_case(list1,file_name)
MSC_slot = list1.pop()
MSC_card = list1.pop()
print(f"  (find_element(), find_elements() will wait {time_sleep_before_find_element} sec )",file = open(file_name, '+a'))
print("======================================================================================",file = open(file_name, '+a'))

print(f"EMS Test\nTest Start",file = open(file_name, '+a')) 



#    Provision > Node Configuration        
# ====================================

print("======================================================================================",file = open(file_name, '+a'))
print("======================================================================================",file = open(file_name, '+a'))
print("======================================================================================",file = open(file_name, '+a'))
print(f"EMS - Node Configuration Test Start\n",file = open(file_name, '+a'))


print("======================================================================================",file = open(file_name, '+a'))
print("No Card Test",file = open(file_name, '+a'))
print("======================================================================================",file = open(file_name, '+a'))
start_time = time.time()
# ems.EMS_test_all_NoCard(driver,url,list1,MSC_card,MSC_slot,msc_port,username,password,file_name,test_retry_num)
ems.EMS_ACL_PPPoE(driver,url,MSC_card,username,password,file_name)
ems.EMS_ACL_Multicast(driver,url,MSC_card,username,password,file_name)
ems.EMS_ACL_DHCP_L2Agent(driver,url,MSC_card,username,password,file_name)
ems.EMS_ACL_ACL_Profile(driver,url,username,password,file_name)
ems.EMS_ACL_Egress_Profile(driver,url,username,password,file_name)
ems.EMS_ACL_Host_Protection(driver,url,username,password,file_name)
ems.EMS_ACL_ARP_Inspection_VLAN(driver,url,username,password,file_name)
ems.EMS_ACL_DHCP_Remote_Backup_Apply(driver,url,username,password,file_name)
ems.Multicast_IGMP_Setup(driver,url,MSC_card,username,password,file_name)
ems.Multicast_MVLAN_And_MVLAN_Table(driver,url,MSC_card,username,password,file_name)

# EMS_test_all_Sys(driver,url,MSC_card,username,password,file_name,test_limit)
ems.Sys_General_Setup(driver,url,MSC_card,username,password,file_name)
Ip_setup_gateway = ems.Sys_IPv4_Setup(driver,url,MSC_card,username,password,file_name)
ems.Sys_IPv6_Setup(driver,url,MSC_card,username,password,file_name)
ems.Sys_IP_Route(driver,url,MSC_card,username,password,file_name, Ip_setup_gateway)

ems.Switch_General(driver,url,MSC_card,username,password,file_name)
ems.Switch_Dot3ad(driver,url,MSC_card,MSC_slot,msc_port,username,password,file_name)
ems.Switch_Isolation(driver,url,MSC_card,username,password,file_name)
ems.Switch_DSCP_Priority_Mapping(driver,url,username,password,file_name)
ems.VLAN_Tag_Mode_Setup(driver,url,MSC_card,MSC_slot,username,password,file_name)
ems.Multicast_VLAN_Mode(driver,url,MSC_card,username,password,file_name) # 4000

ems.EMS_Filter_Test(driver,url,file_name)
ems.EMS_Configure_Save_Test(driver,url,file_name)



end_time = time.time() 
total_time = end_time - start_time
print(f'No Card Test    Total time: {int(total_time/60/60)} hr {int(total_time/60%60)} min {int(total_time%60)} sec',file = open(file_name, '+a'))
print("[Page]",file = open(file_name, '+a'))

ems.EMS_Refresh_Test(driver,username,file_name)
ems.FW_Refresh_Test(driver,url,username,password,file_name)
end_time = time.time() 
total_time = end_time - start_time
print(f'END   Test    Total time: {int(total_time/60/60)} hr {int(total_time/60%60)} min {int(total_time%60)} sec',file = open(file_name, '+a'))

# print("======================================================================================",file = open(file_name, '+a'))
# print("Card Test",file = open(file_name, '+a'))
# print("======================================================================================",file = open(file_name, '+a'))
# start_time = time.time()
# for i in range(list1.__len__()):

#     list_element = list1[i]

#     slot = list_element.split(",")[1]
#     port = list_element.split(",")[2]
#     cardtype = list_element.split(",")[3]
#     print(f"             Now in case:{list_element[:1]},  Slot-Port:{slot}-{port}, {cardtype}   ({i+1}/{list1.__len__()})",file = open(file_name, '+a'))
#     print("======================================================================================",file = open(file_name, '+a'))
#     ems.EMS_test_all_ACL(driver,url,list_element,MSC_card,MSC_slot,username,password,file_name,test_retry_num) # no MAC, OUI Test !
#     ems.EMS_test_all_Multicast(driver,url,list_element,MSC_card,MSC_slot,username,password,file_name,test_retry_num)
#     ems.EMS_test_all_Switch(driver,url,list_element,MSC_card,MSC_slot,msc_port,username,password,file_name,test_retry_num)
#     ems.EMS_test_all_Port(driver,url,list_element,MSC_card,MSC_slot,msc_port,username,password,file_name,test_retry_num)
#     ems.EMS_test_all_VLAN(driver,url,list_element,MSC_card,MSC_slot,msc_port,username,password,file_name,test_retry_num)
#     print("[Page]",file = open(file_name, '+a'))

# ems.EMS_MSC_Not_Support_Test(driver,username,url,MSC_slot,file_name)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# # ACL
# ems.EMS_ACL_Anti_MAC_Spoof(driver,url,list1,username,password,file_name)                  # V case
# ems.EMS_ACL_ARP_Inspection(driver,url,list1,username,password,file_name)                  #   case 
# ems.EMS_ACL_DHCP_L2Agent(driver,url,MSC_card,username,password,file_name)                 #   msc   => card?
# ems.EMS_ACL_MAC_Count(driver,url,list1,username,password,file_name)                       #   case
# ems.EMS_ACL_MAC_Filter(driver,url,list1,username,password,file_name)                      #   case 
# ems.EMS_ACL_OUI_Filter(driver,url,list1,username,password,file_name)                      #   case  undone
# ems.EMS_ACL_Packet_Filter(driver,url,list1,username,password,file_name)                   #   case

# # Multicast
# ems.Multicast_Port_Mode(driver,url,MSC_card,MSC_slot,username,password,file_name)         # msc need_modify          => card?
# ems.Multicast_Multicast_MAC(driver,url,list1,username,password,file_name)                 # case
# ems.Multicast_Multicast_IP(driver,url,list1,username,password,file_name)                  # case

# # Switch
# ems.Switch_DSCP(driver,url,list1,username,password,file_name)                               # case  
# ems.Switch_Storm_Control(driver,url,list1,username,password,file_name)                      # case   

# # Port
# ems.Port_GENNI(driver,url,list1,MSC_slot,msc_port,username,password,file_name)                      # case  
# ems.Port_GE(driver,url,list1,MSC_slot,username,password,file_name)                      # case  
# ems.Port_Qos(driver,url,list1,username,password,file_name)                           # undone  X   case
# ems.Port_DHCP(driver,url,list1,username,password,file_name)                     # case

# # VLAN
# ems.VLAN_VLAN_Table(driver,url,list1,username,password,file_name)                  # case
# ems.VLAN_Untag_And_Copy_Cpbit(driver,url,list1,username,password,file_name)        # case

# # # No Card (173min)
# ems.EMS_ACL_DHCP_Remote_Backup(driver,url,MSC_card,MSC_slot,username,password,file_name)  #   msc
# ems.EMS_ACL_PPPoE(driver,url,MSC_card,username,password,file_name)                        #   msc  
# ems.EMS_ACL_Multicast(driver,url,MSC_card,username,password,file_name)                    #   msc
# ems.Multicast_IGMP_Setup(driver,url,MSC_card,username,password,file_name)                 # msc need_modify   X
# ems.Multicast_VLAN_Mode(driver,url,MSC_card,username,password,file_name)                  # msc need_modify   X
# ems.Multicast_MVLAN_And_MVLAN_Table(driver,url,MSC_card,username,password,file_name)      # msc
# # (Sys)                                                                                     # msc                                                                               
# ems.Sys_General_Setup(driver,url,MSC_card,username,password,file_name) 
# Ip_setup_gateway = ems.Sys_IPv4_Setup(driver,url,MSC_card,username,password,file_name)
# ems.Sys_IPv6_Setup(driver,url,MSC_card,username,password,file_name)
# ems.Sys_IP_Route(driver,url,MSC_card,username,password,file_name, Ip_setup_gateway)    
# ems.Switch_General(driver,url,MSC_card,username,password,file_name)                         # msc 
# ems.Switch_Dot3ad(driver,url,MSC_card,MSC_slot,msc_port,username,password,file_name)        # msc   undone
# ems.Switch_Isolation(driver,url,MSC_card,username,password,file_name)                       # msc 
# ems.VLAN_Tag_Mode_Setup(driver,url,MSC_card,MSC_slot,username,password,file_name)         # msc



# end_time = time.time() 
# total_time = end_time - start_time
# print(f'Card Test   Total time: {int(total_time/60/60)} hr {int(total_time/60%60)} min {int(total_time%60)} sec',file = open(file_name, '+a'))








print("[Page]",file = open(file_name, '+a'))

driver.quit()