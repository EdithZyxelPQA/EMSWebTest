# 變更解析度 1920x1080
import ctypes
from ctypes import wintypes
import sys

# 定義必要的常數
DM_PELSWIDTH = 0x00080000
DM_PELSHEIGHT = 0x00100000
CDS_UPDATEREGISTRY = 0x00000001
CDS_TEST = 0x00000002
DISP_CHANGE_SUCCESSFUL = 0
ENUM_CURRENT_SETTINGS = -1

# 定義 C 語言的 DEVMODE 結構 (這是 Windows API 要求的格式)
class DEVMODE(ctypes.Structure):
    _fields_ = [
        ("dmDeviceName", ctypes.c_wchar * 32),
        ("dmSpecVersion", wintypes.WORD),
        ("dmDriverVersion", wintypes.WORD),
        ("dmSize", wintypes.WORD),
        ("dmDriverExtra", wintypes.WORD),
        ("dmFields", wintypes.DWORD),
        ("dmOrientation", ctypes.c_short),
        ("dmPaperSize", ctypes.c_short),
        ("dmPaperLength", ctypes.c_short),
        ("dmPaperWidth", ctypes.c_short),
        ("dmScale", ctypes.c_short),
        ("dmCopies", ctypes.c_short),
        ("dmDefaultSource", ctypes.c_short),
        ("dmPrintQuality", ctypes.c_short),
        ("dmColor", ctypes.c_short),
        ("dmDuplex", ctypes.c_short),
        ("dmYResolution", ctypes.c_short),
        ("dmTTOption", ctypes.c_short),
        ("dmCollate", ctypes.c_short),
        ("dmFormName", ctypes.c_wchar * 32),
        ("dmLogPixels", wintypes.WORD),
        ("dmBitsPerPel", wintypes.DWORD),
        ("dmPelsWidth", wintypes.DWORD),
        ("dmPelsHeight", wintypes.DWORD),
        ("dmDisplayFlags", wintypes.DWORD),
        ("dmDisplayFrequency", wintypes.DWORD),
        ("dmICMMethod", wintypes.DWORD),
        ("dmICMIntent", wintypes.DWORD),
        ("dmMediaType", wintypes.DWORD),
        ("dmDitherType", wintypes.DWORD),
        ("dmReserved1", wintypes.DWORD),
        ("dmReserved2", wintypes.DWORD),
        ("dmPanningWidth", wintypes.DWORD),
        ("dmPanningHeight", wintypes.DWORD),
    ]

def change_resolution(width, height):
    """
    變更螢幕解析度
    :param width: 寬度 (例如 1920)
    :param height: 高度 (例如 1080)
    """
    user32 = ctypes.windll.user32
    devmode = DEVMODE()
    devmode.dmSize = ctypes.sizeof(DEVMODE)

    # 1. 獲取當前的螢幕設定 (以免覆蓋掉刷新率等其他設定)
    if user32.EnumDisplaySettingsW(None, ENUM_CURRENT_SETTINGS, ctypes.byref(devmode)) == 0:
        print("無法獲取當前螢幕設定")
        return False

    # 2. 設定新的寬高
    devmode.dmPelsWidth = width
    devmode.dmPelsHeight = height
    
    # 告訴 API 我們只要改這兩個欄位
    devmode.dmFields = DM_PELSWIDTH | DM_PELSHEIGHT

    # 3. 測試設定是否有效 (CDS_TEST)
    result = user32.ChangeDisplaySettingsW(ctypes.byref(devmode), CDS_TEST)
    if result != DISP_CHANGE_SUCCESSFUL:
        print(f"不支援此解析度: {width}x{height} (錯誤碼: {result})")
        return False

    # 4. 真正套用設定 (CDS_UPDATEREGISTRY 會將設定寫入註冊表，永久生效)
    # 如果只想暫時生效直到重開機，可移除 CDS_UPDATEREGISTRY
    result = user32.ChangeDisplaySettingsW(ctypes.byref(devmode), CDS_UPDATEREGISTRY)
    
    if result == DISP_CHANGE_SUCCESSFUL:
        print(f"成功變更解析度為 {width}x{height}")
        return True
    else:
        print("變更解析度失敗")
        return False

# 在這裡輸入你想要的解析度
TARGET_WIDTH = 1920
TARGET_HEIGHT = 1080

print(f"正在嘗試切換至 {TARGET_WIDTH}x{TARGET_HEIGHT}...")
change_resolution(TARGET_WIDTH, TARGET_HEIGHT)








# 環境架設
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service as ChromeService

import module.xpon_module as xpon
import module.selenium_module as mod
import module.xpon_olt_status_module as olts
import module.xpon_olt_config_module as oltc
import module.xpon_batch_ont_config_module as bat
import module.xpon_ont_config_module as ontc
import module.xpon_profiles_module as pro

# copy from GLC project-------------
import module.acl_module as acl  
import module.glc_test_module as glc
# ----------------------------------

from selenium.webdriver.support.ui import Select
import time
import datetime

import module.ems_acl_module as e_acl
import module.ems_profile_module as e_pro
import module.ems_test_module as ems
import module.ems_module as e_mod

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from module.customdriver import CustomDriver
import module.globals
import module.get_card
from module.variable_module import *

# import videocap_module as videocap

time_sleep_before_find_element = 0  
driver = CustomDriver(time_sleep = time_sleep_before_find_element)



start_time = time.time()
start_time0 = time.time()

# create "Report" folder if it doesn't exist
if not os.path.exists("Report"):
    os.makedirs("Report")


#    EMS Web        
# ====================================
driver.get(ems_url) 
try:
    driver.maximize_window()    
except:
    pass
time.sleep(5)
mod.Login_EMS(driver,username,ems_password)
time.sleep(5)

# if "Neox".lower() in driver.title.lower():
#     if_Neox = True
# ems.parameter_add("if_Neox",if_Neox)

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
file_name = f"Report\Web_EMS_Profiles_{emsversion}_{date1}{date2}.txt"
ems.parameter_add("file_name",file_name)
ems.get_file_name(file_name)

#    Info in File
test_report = open(file_name,"w+")
print("EMS Web Auto Report",file = open(file_name, '+a'))
print(datetime.datetime.now(),file = open(file_name, '+a'))
print(f"EMS Web IP:{ems_url}  \nEMS Version:{emsversion} ",file = open(file_name, '+a'))
print(f"  (find_element(), find_elements() will wait {time_sleep_before_find_element} sec )",file = open(file_name, '+a'))
print("======================================================================================",file = open(file_name, '+a'))

try:
    driver.maximize_window()    
except:
    pass

print(f"EMS Test\nTest Start",file = open(file_name, '+a')) 
# # #    Provision > Profile 
# # # ====================================

print(f"EMS - Profile Test Start\n",file = open(file_name, '+a'))

ems.EMS_delete_profiles(driver,ems_url,username,ems_password,file_name)
ems.Create_zzz_profile_for_Sort_test(driver,ems_url,username,ems_password,file_name)

ems.ONT_QoS_Bandwidth_Profile(driver,ems_url,username,ems_password,file_name)
ems.ONT_Security_Profile(driver,ems_url,username,ems_password,file_name)
ems.Rate_Limit_Profile(driver,ems_url,username,ems_password,file_name)
ems.Shaping_Profile(driver,ems_url,username,ems_password,file_name) 
ems.IGMP_Group_Privilege_Profile(driver,ems_url,username,ems_password,file_name) 
ems.ONT_Service_Profile(driver,ems_url,username,ems_password,file_name)
ems.ONT_Multicast_Profile(driver,ems_url,username,ems_password,file_name)       
ems.ONT_UNI_Profile(driver,ems_url,username,ems_password,file_name)   
ems.ONT_ONT_Profile(driver,ems_url,username,ems_password,file_name) 
ems.ONT_VoIP_SIP_Profile(driver,ems_url,username,ems_password,file_name)
ems.ONT_VoIP_Common_Profile(driver,ems_url,username,ems_password,file_name)  
ems.ONT_VoIP_Dial_Plan_Profile(driver,ems_url,username,ems_password,file_name) 
ems.ONT_ACL_Profile(driver,ems_url,username,ems_password,file_name)  
ems.ONT_Alarm_Profile(driver,ems_url,username,ems_password,file_name)  
ems.ONT_Template_Profile(driver,ems_url,username,ems_password,file_name)
ems.Weight_Profile(driver,ems_url,username,ems_password,file_name)  
ems.GE_Template(driver,ems_url,username,ems_password,file_name) 

print(f"EMS - Profile Test End\n",file = open(file_name, '+a'))

end_time = time.time() 
total_time = end_time - start_time
print(f'Profile Test   Total time: {int(total_time/60/60)} hr {int(total_time/60%60)} min {int(total_time%60)} sec',file = open(file_name, '+a'))
print("[Page]",file = open(file_name, '+a'))




driver.quit()
