# 變更解析度為 1920x1080
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

# if __name__ == "__main__":
# 在這裡輸入你想要的解析度
TARGET_WIDTH = 1920
TARGET_HEIGHT = 1080

print(f"正在嘗試切換至 {TARGET_WIDTH}x{TARGET_HEIGHT}...")
change_resolution(TARGET_WIDTH, TARGET_HEIGHT)
# ====================================================================================================================================
# 環境架設
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
# driver = webdriver.Chrome()
# driver = webdriver.Firefox()
from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
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
# from docx import Document
# from docx.shared import Inches

import ems_acl_module as e_acl
import ems_profile_module as e_pro
import ems_test_module as ems
import ems_test_module_OLT1408 as emss
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import time
import datetime
import telnetlib
from customdriver import CustomDriver
# from variable_module import *
import pyautogui
import get_card
from dataclasses import asdict
import argparse
import os
# import videocap_module as videocap

time_sleep_before_find_element = 0 # 0.1
# driver = CustomDriver(time_sleep = time_sleep_before_find_element)
# try:
#     driver.maximize_window()    
# except:
#     pass


start_time = time.time()
start_time0 = time.time()










# -*- coding: utf-8 -*-
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import json, time, datetime, traceback
# 建議：若 ems / module 有全域狀態，改用 thread-local 或在函式內建立實例
thread_local = threading.local()

def process_env(env_file: str):
    """處理單一 env 設定檔；可在多執行緒中被呼叫。"""
    tname = threading.current_thread().name
    start_time0 = time.time()

    try:
        with open(env_file, 'r') as f:
            d = json.load(f)

        msc_card_type = 'default'

        url = d["ZYXEL_DUT"]["NODE1"]["url"]
        url_ip = url.split("/")[2]   
        username = d['ZYXEL_DUT']['NODE1']["login_username"]
        password = d['ZYXEL_DUT']['NODE1']["login_password"]
        login_username = d['ZYXEL_DUT']['NODE1']["login_username"]
        login_password = d['ZYXEL_DUT']['NODE1']["login_password"]
        default_username = d['ZYXEL_DUT']['NODE1']["default_username"]
        default_password = d['ZYXEL_DUT']['NODE1']["default_password"]
        loop = d["LOOP"]["count"]

        # EMS
        ems_url = d["EMS"]["url"]
        ems_username = d["EMS"]["login_username"]
        ems_password = d["EMS"]["login_password"]

        #Card
        msc_slot = d["ZYXEL_DUT"]["NODE1"]["CARDINFO"]["MSC"]["slot_id"]
        msc_port = d["ZYXEL_DUT"]["NODE1"]["CARDINFO"]["MSC"]["port_id"]
        glc_slot = d["ZYXEL_DUT"]["NODE1"]["CARDINFO"]["GLC1440X"]["slot_id"] #/ d["ZYXEL_DUT"]["NODE1"]["CARDINFO"]["GLC1540X"]["slot_id"]
        glc_port = d["ZYXEL_DUT"]["NODE1"]["CARDINFO"]["GLC1440X"]["port_id"] #/["GLC1540X"]["port_id"]
        OLT_Port = d["ZYXEL_DUT"]["NODE1"]["CARDINFO"]["OLT140x"]["port_id"]
        OLT_Eth_Port = d["ZYXEL_DUT"]["NODE1"]["CARDINFO"]["OLT140x"]["eth_port_id"]

        #Xpon
        slot_x_1_aid = d["ZYXEL_DUT"]["NODE1"]["ONTINFO"]["XPON"]["ONT1"]["slot_id"]
        pon_x_1_aid = d["ZYXEL_DUT"]["NODE1"]["ONTINFO"]["XPON"]["ONT1"]["port_id"]
        ont_x_1_1 = d["ZYXEL_DUT"]["NODE1"]["ONTINFO"]["XPON"]["ONT1"]["ont_id"]
        ont_x_1_2 = "d['Xpon']['Ont_x_1_2']"         ## not sure if use
        ont_x_1_1_aid = f'{slot_x_1_aid}-{pon_x_1_aid}-{ont_x_1_1}'
        ont_x_1_2_aid = "d['Xpon']['Ont_x_1_2_aid']" ##


        ont_x_1_1_sn_12 = d["ZYXEL_DUT"]["NODE1"]["ONTINFO"]["XPON"]["ONT1"]["sn_12"]
        ont_x_1_1_sn = d["ZYXEL_DUT"]["NODE1"]["ONTINFO"]["XPON"]["ONT1"]["sn_16"]
        ont_x_1_1_pw = d["ZYXEL_DUT"]["NODE1"]["ONTINFO"]["XPON"]["ONT1"]["pw"]
        ont_x_1_1_ont_USER = d["ZYXEL_DUT"]["NODE1"]["ONTINFO"]["XPON"]["ONT1"]["ont_user"]
        ont_x_1_1_ont_PW = d["ZYXEL_DUT"]["NODE1"]["ONTINFO"]["XPON"]["ONT1"]["ont_pw"]

        ont_x_1_2_sn_12 = "d['Xpon']['ONT']['ONT_x_1_2_SN_12']"   ##
        ont_x_1_2_sn = "d['Xpon']['ONT']['ONT_x_1_2_SN']"             ## use
        ont_x_1_2_pw = "d['Xpon']['ONT']['ONT_x_1_2_PW']"             ## 
        ont_x_1_2_ont_USER = "d['Xpon']['ONT']['ONT_x_1_2_ont_USER']" ##
        ont_x_1_2_ont_PW = "d['Xpon']['ONT']['ONT_x_1_2_ont_PW']"     ##


        test_retry_num = 3
        
        # ========================= Telnet ================================
 
        def Input_cmd_func(input_cmd_file_name):
            # Get command from txt
            f = open(input_cmd_file_name,'r', encoding="utf-8")
            My_List = []
            done = 0
            while (not done):
                aline = f.readline()
                if(aline!=''):
                    My_List.append(aline.strip())
                else:
                    done = 1
            return My_List

        def Telnet_func(host_ip,username, password,My_List,output_file, _type=0):	

            print(f"\n= = = = = = = = start = = = = = = = = = = = = = = = =\n",file = open(output_file, '+a'))  

            def wait_for_specific_words(tn,words):
                while True:
                    output = tn.read_until(b"\n").decode("utf-8")
                    output = str(output)
                    for word in words:
                        if(word.decode("utf-8") in output):
                            break
            wordds = [b"# ",b"-- more --, next page: Space, continue: c, quit: ESC"]


            # username = 'admin'
            # password = '1234'
            print(f'### telnet {host_ip}',file = open(output_file, '+a'))
            tnet_hndl = telnetlib.Telnet(host_ip)
            if(_type==1):
                print(tnet_hndl.read_until(b"User name: "),file = open(output_file, '+a'))
                tnet_hndl.write(username.encode('ascii') + b"\n")
            else:
                print(tnet_hndl.read_until(b"login: "),file = open(output_file, '+a')) # for IES52xx
                tnet_hndl.write(username.encode('ascii') + b"\n")
            print(tnet_hndl.read_until(b"Password: "),file = open(output_file, '+a'))
            tnet_hndl.write(password.encode('ascii') + b"\n")
            print(tnet_hndl.read_until(b"# "),file = open(output_file, '+a'))
            for cmd in My_List:


                if((cmd=="c")or(cmd=="y")):
                    cmd = bytes(cmd, encoding='UTF-8')
                    tnet_hndl.write(cmd)
                else:
                    cmd = bytes(cmd, encoding='UTF-8')
                    tnet_hndl.write(cmd + b"\n")
                print(cmd,file = open(output_file, '+a'))  # print command

                time.sleep(0) # 1 # 0.3

                if_find = False
                for i in range(3):
                    set_timeout = 5
                    if(i>0):
                        set_timeout = 20
                    for wor in wordds:
                        # print(f'start read until {wor}')
                        try:
                            # list_1 = str(tnet_hndl.read_until(wor,timeout=10)).split('\\r\\n')
                            list_1 = str(tnet_hndl.read_until(wor,timeout=set_timeout)).split('\\r\\n')
                            if_find = True
                            # print(f'read until {wor} pass')
                            break
                        except ConnectionResetError as e:
                            print(f'{cmd} //read until {wor} fail ({i+1}t)')
                            print('timeout occurred')
                            continue
                    if(if_find == True):
                        break
                if(if_find == False):
                    print(f"'{cmd}' //read until all words fail",file = open(output_file, '+a'))

                list_1.pop(0) ### delete the first line
                for i in list_1:
                    print(f':{i}',file = open(output_file, '+a'))  # print return data
                print('\n',file = open(output_file, '+a'))
            tnet_hndl.close()

            print(f"\n= = = = = = = = done. = = = = = = = = = = = = = = = =\n",file = open(output_file, '+a'))  

        My_List = ['er ru ext','y']
        output_file = 'temp_erase_log.txt'
        output_file_f = open(output_file,"w+")
        Telnet_func(url_ip,username,password,My_List,output_file, _type=1)
        time.sleep(10)        
        
        
        # ========================= Initial ================================
        
        # 每個 Thread 自己建 driver，避免共用衝突
        driver = CustomDriver(time_sleep=time_sleep_before_find_element)
        try:
            driver.maximize_window()    
        except:
            pass        
        #   Login
        driver.get(ems_url)
        mod.Login_EMS(driver,ems_username,ems_password)
        time.sleep(5)

        # Get EMS version
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

        # driver.get("http://192.168.169.207")
        # # may need click the browser
        # time.sleep(2)
        # pyautogui.write(username)
        # pyautogui.press("tab")
        # pyautogui.write(password)
        # pyautogui.press("enter")
        driver.get(f"http://{username}:{password}@{url_ip}")
        time.sleep(5)

        #   Get Web Info
        mod.Switch_Default(driver)
        mod.Switch_Specific_Frame(driver,3)
        driver.find_element(By.LINK_TEXT,"Basic Setting").click()
        time.sleep(1)
        mod.Switch_Default(driver)
        mod.Switch_Specific_Frame(driver,4)
        driver.find_element(By.LINK_TEXT,"System Info").click()
        mod.Switch_Default(driver)
        mod.Switch_Specific_Frame(driver,6)
        time.sleep(1)
        model_name = driver.find_element(By.XPATH,"/html/body/form/table[5]/tbody/tr[3]/td[2]").text
        model_version = driver.find_element(By.XPATH,"/html/body/form/table[5]/tbody/tr[5]/td[2]").text.split("|")[0]
        #    Set File Name
        date1 = str(datetime.datetime.now()).split(":")[0]
        date2 = str(datetime.datetime.now()).split(":")[1]
        # file_name = f"Output\Web_{model_name}_{model_version}_{date1}{date2}.txt"
        file_name = f"Output\Web_EMS_{model_name}_{emsversion}_{date1}{date2}_{url_ip[-3:]}.txt"

        #    Info in File
        test_report = open(file_name,"w+")
        print("Web Auto Report",file = open(file_name, '+a'))
        print(datetime.datetime.now(),file = open(file_name, '+a'))
        print(f"EMS Web url: {ems_url}",file = open(file_name, '+a'))
        print(f"EMS Web Version: {emsversion}\nFW Web IP:{url}\nFW Web model: {model_name}\nFW Web version: {model_version}",file = open(file_name, '+a'))

        #    Set Logout Time
        mod.Switch_Default(driver)
        mod.Switch_Specific_Frame(driver,3)
        driver.find_element(By.LINK_TEXT,"Management").click()
        time.sleep(1)
        mod.Switch_Default(driver)
        mod.Switch_Specific_Frame(driver,4)
        driver.find_element(By.LINK_TEXT,"Access Control").click()
        mod.Switch_Default(driver)
        mod.Switch_Specific_Frame(driver,6)
        time.sleep(1)
        driver.find_element(By.XPATH,'/html/body/table/tbody/tr[2]/td/table/tbody/tr[6]/td[3]/a').click()
        time.sleep(2)
        driver.find_element(By.NAME,"RpAccessSv_IptHttpTimeout").send_keys(Keys.CONTROL + 'a')
        driver.find_element(By.NAME,"RpAccessSv_IptHttpTimeout").send_keys('255')
        driver.find_element(By.NAME,'RpAccessSv_BtnApply').click()
        time.sleep(2)
        if(model_name=="OLT1404A-IA"):
            a=int(OLT_Eth_Port)-4
            Pon_Name="PON "+OLT_Port
            Pon_Name_L="pon-"+OLT_Port
            Eth_Name="ETH "+str(a)
            Eth_Name_L="eth-"+str(a)
            print(Pon_Name,Eth_Name,Pon_Name_L,Eth_Name_L)
        elif(model_name=="OLT1404B-IA"):
            a=int(OLT_Eth_Port)-4
            Pon_Name="PON "+OLT_Port
            Pon_Name_L="pon-"+OLT_Port
            Eth_Name="ETH "+str(a)
            Eth_Name_L="eth-"+str(a)
            print(Pon_Name,Eth_Name,Pon_Name_L,Eth_Name_L)
        elif(model_name=="OLT1408A-IA"):
            a=int(OLT_Eth_Port)-8
            Pon_Name="PON "+OLT_Port
            Pon_Name_L="pon-"+OLT_Port
            Eth_Name="ETH "+str(a)
            Eth_Name_L="eth-"+str(a)
            print(Pon_Name,Eth_Name,Pon_Name_L,Eth_Name_L)
        elif(model_name=="OLT1408B-IA"):
            a=int(OLT_Eth_Port)-8
            Pon_Name="PON "+OLT_Port
            Pon_Name_L="pon-"+OLT_Port
            Eth_Name="ETH "+str(a)
            Eth_Name_L="eth-"+str(a)
            print(Pon_Name,Eth_Name,Pon_Name_L,Eth_Name_L)
        elif(model_name=="OLT1408A-C"):
            a=int(OLT_Eth_Port)-8
            Pon_Name="PON "+OLT_Port
            Pon_Name_L="pon-"+OLT_Port
            Eth_Name="ETH "+str(a)
            Eth_Name_L="eth-"+str(a)        
        # ========================= Test Start ================================
         
        print(f"EMS - Configuration for OLT140x Test Start",file = open(file_name, '+a'))
        driver.get(ems_url)
        mod.Login_EMS(driver,username,ems_password)
        time.sleep(5)
        emss.get_file_name(file_name)
        emss.Basic_General(driver,url,ems_url,file_name)  
        emss.Basic_Switch(driver,url,ems_url,file_name)                                                                                            #set fail   k
        emss.Basic_IP(driver,url,ems_url,file_name)                                                                                                    #set fail   k
        emss.Basic_Port(driver,url,ems_url,username,password,url_ip,file_name,Pon_Name,Eth_Name,Pon_Name_L,Eth_Name_L)                                                      #OK         k
        emss.IP_Static(driver,url,ems_url,file_name)                                                                                                 #
        emss.IP_DHCP(driver,url,ems_url,file_name)                                                                                                     #           k
        emss.Advanced_VLAN(driver,url,ems_url,file_name,Pon_Name,Eth_Name,Pon_Name_L,Eth_Name_L,OLT_Eth_Port)                                                       #VLAN - Protocol Based SET Fail k
        emss.Advanced_Static(driver,url,ems_url,file_name)                                                                                             #OK         k
        emss.Advanced_Filtering(driver,url,ems_url,file_name)                                                                                          #OK         k
        emss.Advanced_Broadcast(driver,url,ems_url,file_name,Pon_Name,Eth_Name,Pon_Name_L,Eth_Name_L)                                                 #OK         k
        emss.Advanced_Link(driver,url,ems_url,file_name,Pon_Name,Eth_Name,Pon_Name_L,Eth_Name_L)                                                       #OK         k
        emss.Advanced_Port(driver,url,ems_url,file_name,Pon_Name,Eth_Name,OLT_Port,OLT_Eth_Port)                                                       #ok         k
        emss.Advanced_Classifier(driver,url,ems_url,file_name)                                                                                         #EMS Ethernet Type無法修改
        emss.Advanced_Policy(driver,url,ems_url,file_name)                                                                                             #OK         k
        emss.Advanced_Queqe(driver,url,ems_url,file_name,Pon_Name,Eth_Name,Pon_Name_L,Eth_Name_L,OLT_Eth_Port,OLT_Port)                                                      #OK         k
        emss.Advanced_VLANStacking(driver,url,ems_url,file_name,Pon_Name,Eth_Name,Pon_Name_L,Eth_Name_L,OLT_Port,OLT_Eth_Port)                                               #OK         k
        emss.Advanced_Multicast(driver,url,ems_url,file_name,Pon_Name,Eth_Name,Pon_Name_L,Eth_Name_L,OLT_Port,OLT_Eth_Port)                                                #set fail   k
        emss.Advanced_IP(driver,url,ems_url,file_name,Pon_Name,Eth_Name,Pon_Name_L,Eth_Name_L,OLT_Port,OLT_Eth_Port)                                                        #OK         k
        emss.Advanced_Loop(driver,url,ems_url,file_name,Pon_Name,Eth_Name,Pon_Name_L,Eth_Name_L,OLT_Port,OLT_Eth_Port)                                                       #OK         k
        emss.Advanced_PPPoE(driver,url,ems_url,file_name,Pon_Name,Eth_Name,Pon_Name_L,Eth_Name_L,OLT_Port,OLT_Eth_Port)                                                      #OK         k
        emss.GPON_OLT(driver,url,ems_url,file_name,Pon_Name,Eth_Name,Pon_Name_L,Eth_Name_L)                                                            #           k
        emss.Configure_Save(driver,url,ems_url,file_name)                                                                                              #OK         k

        # ========================= Test Finish ================================
        # try:
        #     driver.close()
        # except:
        #     pass
        try:
            output_file_f.close()
        except:
            pass        

        total_time = time.time() - start_time0
        print(f'Total time: {int(total_time/60/60)} hr {int(total_time/60%60)} min {int(total_time%60)} sec',
              file=open(file_name, '+a', encoding='utf-8'))

        return f"[{tname}] {env_file} ✔ done"

    except Exception as e:
        try:
            output_file_f.close()
        except:
            pass

        # 失敗也回傳字串，主執行緒可收集
        msg = f"[{tname}] {env_file} ✖ failed: {e}\n{traceback.format_exc()}"
        # 也可寫入一個 per-env 的錯誤檔
        err_file = f"Report/error_{env_file.replace('/', '_')}.log"
        print(msg, file=open(err_file, '+a', encoding='utf-8'))
        return msg



# env_list = [
#     "ENV/ENV_WEB_207.json",
#     # "ENV/ENV_WEB_84.json",
#     # "ENV/ENV_WEB_85.json",
# ]

def _normalize_ip(value: str) -> str:
    value = value.strip()
    if "://" in value:
        value = value.split("://", 1)[1]
    value = value.split("/", 1)[0]
    value = value.split(":", 1)[0]
    return value.strip()


def _load_env_file(env_file: str):
    with open(env_file, "r", encoding="utf-8") as f:
        return json.load(f)


def _get_node1_ip(env_data: dict) -> str:
    return env_data.get("ZYXEL_DUT", {}).get("NODE1", {}).get("ip", "")


def _get_node1_url_ip(env_data: dict) -> str:
    url = env_data.get("ZYXEL_DUT", {}).get("NODE1", {}).get("url", "")
    return _normalize_ip(url)


def find_env_files_by_device_ip(device_ip: str, env_dir: str = "ENV") -> list[str]:
    target_ip = _normalize_ip(device_ip)
    matched_files = []

    for env_name in sorted(os.listdir(env_dir)):
        if not env_name.lower().endswith(".json"):
            continue

        env_file = os.path.join(env_dir, env_name)
        try:
            env_data = _load_env_file(env_file)
        except (json.JSONDecodeError, OSError):
            continue

        node_ip = _normalize_ip(_get_node1_ip(env_data))
        node_url_ip = _get_node1_url_ip(env_data)
        if target_ip in {node_ip, node_url_ip}:
            matched_files.append(env_file)

    return matched_files


def resolve_env_files(inputs: list[str]) -> list[str]:
    env_files = []
    for value in inputs:
        direct_file = value if value.lower().endswith(".json") else f"ENV/ENV_WEB_{value}.json"
        if os.path.exists(direct_file):
            env_files.append(direct_file)
            continue

        matched_files = find_env_files_by_device_ip(value)
        if not matched_files:
            raise FileNotFoundError(f"Cannot find env file for device IP: {value}")
        env_files.extend(matched_files)

    return list(dict.fromkeys(env_files))


def prompt_device_ips() -> list[str]:
    raw_value = input("Please enter device IP (separate multiple IPs with space or comma): ").strip()
    return [value for value in raw_value.replace(",", " ").split() if value]

#  =====================================================================
#  ENV File Setting
#  =====================================================================  python Run_EMS_Config_all.py 82
# 1. 設定參數解析器
parser = argparse.ArgumentParser(description="Run EMS automation by device IP or env id.")
parser.add_argument(
    "targets",
    type=str,
    nargs="*",
    help="Device IP, env id, or env json path. Examples: 192.168.169.84 84 ENV/ENV_WEB_207.json",
)

args = parser.parse_args()
target_inputs = args.targets or prompt_device_ips()
if not target_inputs:
    raise SystemExit("No device IP or env id was provided.")

env_list = resolve_env_files(target_inputs)
print(f"Selected env files: {env_list}")
#  =====================================================================






# 可調整同時 worker 數：預設 = min(4, len(env_list))，避免把機器或目標站點壓垮
max_workers = min(4, len(env_list))  

results = []
with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="ENV") as executor:
    future_map = {executor.submit(process_env, env_file): env_file for env_file in env_list}
    for future in as_completed(future_map):
        res = future.result()
        results.append(res)
        print(res)

print("\n=== All tasks finished ===")
for r in results:
    print(r)



