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

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from module.customdriver import CustomDriver
import module.globals
import module.get_card
import json
import os
import argparse
# create "Report" folder if not exist
if not os.path.exists("Report"):
    os.makedirs("Report")

# SET time_sleep_before_find_element
import os
if not os.path.isfile( os.path.join('ENV', 'time_sleep_before_find_element.txt') ):
    with open(os.path.join('ENV', 'time_sleep_before_find_element.txt'), 'w') as file:
        file.write("time_sleep_before_find_element = '0.3'")
_0_set_up_file = open("ENV\\time_sleep_before_find_element.txt",'r')
_0_lines = _0_set_up_file.readlines()
_0_set_up_file.close()
time_sleep_before_find_element = float(_0_lines[0].split("'")[1])    


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
        with open(env_file, 'r', encoding='utf-8') as f:
            d = json.load(f)

        url = d["ZYXEL_DUT"]["NODE1"]["url"]
        url_ip = url.split("/")[2]
        username = d['ZYXEL_DUT']['NODE1']["login_username"]
        password = d['ZYXEL_DUT']['NODE1']["login_password"]
        default_username = d['ZYXEL_DUT']['NODE1']["default_username"]
        default_password = d['ZYXEL_DUT']['NODE1']["default_password"]
        device_name = d['ZYXEL_DUT']['NODE1']["name"]
        map_name = d['ZYXEL_DUT']['NODE1']["map_name"]
        set_community = d['ZYXEL_DUT']['NODE1']["set_community"]
        get_community = d['ZYXEL_DUT']['NODE1']["get_community"]
        loop = d["LOOP"]["count"]

        # EMS
        ems_url = d["EMS"]["url"]
        ems_username = d["EMS"]["login_username"]
        ems_password = d["EMS"]["login_password"]
        ems.set_ems_credentials(ems_url, ems_password)  # 設定本 thread 的 EMS 連線資訊

        # Card
        msc_slot = d["ZYXEL_DUT"]["NODE1"]["CARDINFO"]["MSC"]["slot_id"]
        msc_port = d["ZYXEL_DUT"]["NODE1"]["CARDINFO"]["MSC"]["port_id"]
        glc_slot = d["ZYXEL_DUT"]["NODE1"]["CARDINFO"]["GLC1440X"]["slot_id"]
        glc_port = d["ZYXEL_DUT"]["NODE1"]["CARDINFO"]["GLC1440X"]["port_id"]

        # GPON (未修改)
        slot_1_aid = d["ZYXEL_DUT"]["NODE1"]["CARDINFO"]["OLC3416-42A"]["slot_id"]
        pon_1_aid = d["ZYXEL_DUT"]["NODE1"]["CARDINFO"]["OLC3416-42A"]["port_id"]

        # XPON
        slot_x_1_aid = d["ZYXEL_DUT"]["NODE1"]["ONTINFO"]["XPON"]["ONT1"]["slot_id"]
        pon_x_1_aid = d["ZYXEL_DUT"]["NODE1"]["ONTINFO"]["XPON"]["ONT1"]["port_id"]
        ont_x_1_1 = d["ZYXEL_DUT"]["NODE1"]["ONTINFO"]["XPON"]["ONT1"]["ont_id"]
        ont_x_1_1_aid = f'{slot_x_1_aid}-{pon_x_1_aid}-{ont_x_1_1}'

        ont_x_1_1_sn_12 = d["ZYXEL_DUT"]["NODE1"]["ONTINFO"]["XPON"]["ONT1"]["sn_12"]
        ont_x_1_1_sn = d["ZYXEL_DUT"]["NODE1"]["ONTINFO"]["XPON"]["ONT1"]["sn_16"]
        ont_x_1_1_pw = d["ZYXEL_DUT"]["NODE1"]["ONTINFO"]["XPON"]["ONT1"]["pw"]
        ont_x_1_1_ont_USER = d["ZYXEL_DUT"]["NODE1"]["ONTINFO"]["XPON"]["ONT1"]["ont_user"]
        ont_x_1_1_ont_PW = d["ZYXEL_DUT"]["NODE1"]["ONTINFO"]["XPON"]["ONT1"]["ont_pw"]

        service_mode_x_1 = d["ZYXEL_DUT"]["NODE1"]["ONTINFO"]["XPON"]["ONT1"]["service_mode"]
        service_mode_x_2 = service_mode_x_1
        inband_vlan = d["ZYXEL_DUT"]["NODE1"]["inband_vlan"]

        snmp_get = ''
        snmp_set = ''
        snmp_version = ''
        test_retry_num = 2

        # === Test Start ===
        # 每個 Thread 自己建 driver，避免共用衝突
        driver = CustomDriver(time_sleep=time_sleep_before_find_element)

        start_time = time.time()

        # --- FW Web CardType Case ---
        driver.get(url)
        mod.Login(driver, username, password)
        fw_title = driver.title

        if "Neox".lower() in driver.title.lower():
            if_Neox = True
        else:
            if_Neox = False
        ems.parameter_add("if_Neox", if_Neox)

        mod.Switch_Default(driver)
        mod.Page_Switch(driver, "Home")
        time.sleep(5)
        mod.Switch_Frame(driver)
        msc_card_type = driver.find_elements(
            'class name', "td-table-content.SysinfoCardType.left-wrapper"
        )[int(msc_slot) - 1].get_attribute("textContent")
        module.globals.msc_card_type = msc_card_type  # test
        msc_version = driver.find_elements(
            'class name', "td-table-content.Sysinfofwversion.left-wrapper"
        )[int(msc_slot) - 1].get_attribute("textContent")

        ems.Maintenance_Config_Reset(driver)  # 如需

        ems.EMS_Set_Prepare(driver, snmp_get, snmp_set, snmp_version, username, password)

        list1 = module.get_card.get_card_case(driver,glc_port,pon_x_1_aid,pon_1_aid,msc_port,file_name='')

        ems.FW_Logout(driver)

        # --- EMS Web ---
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

        # --- Set File Name（每個執行緒各寫自己的檔案，避免互卡）---
        date1 = str(datetime.datetime.now()).split(":")[0]
        date2 = str(datetime.datetime.now()).split(":")[1]
        file_name = f"Report/Web_EMS_Config_Retest_Sys_MVLAN_VLANTable_{fw_title}_{emsversion}_{date1}{date2}_{url_ip[-3:]}.log"
        ems.parameter_add("file_name", file_name)
        ems.get_file_name(file_name)

        # --- Info in File ---
        print("EMS Web Auto Report", file=open(file_name, '+a', encoding='utf-8'))
        print(datetime.datetime.now(), file=open(file_name, '+a', encoding='utf-8'))
        print(f"EMS Web IP:{ems_url}  \nEMS Version:{emsversion} ", file=open(file_name, '+a', encoding='utf-8'))
        print(f"FW Web IP:{url}FW MSC:{msc_slot}-{msc_port}/{msc_card_type}/{msc_version}", file=open(file_name, '+a', encoding='utf-8'))
        print(f"if_Neox: {ems.parameter_get('if_Neox')}", file=open(file_name, '+a', encoding='utf-8'))
        print(f"{list1}", file=open(file_name, '+a', encoding='utf-8'))

        MSC_slot = list1.pop()
        MSC_card = list1.pop()


        if args.slots:
            list1 = [e for e in list1 if e.split(",")[1] in args.slots]
            print(f"only slots: {args.slots}", file=open(file_name, '+a', encoding='utf-8'))
        module.get_card.print_case(list1, file_name)

        print(f"env file:{env_file}", file=open(file_name, '+a', encoding='utf-8'))
        print(f"  (find_element(), find_elements() will wait {time_sleep_before_find_element} sec )\n", file=open(file_name, '+a', encoding='utf-8'))

        print(f"EMS Test\nTest Start", file=open(file_name, '+a', encoding='utf-8'))

        print("======================================================================================",file = open(file_name, '+a'))
        print("No Card Test (System?)",file = open(file_name, '+a'))
        print("======================================================================================",file = open(file_name, '+a'))
        start_time3 = time.time()
        # [retest skip] ems.EMS_ACL_PPPoE(driver,url,MSC_card,username,password, ems_url, ems_password,file_name)
        # [retest skip] ems.EMS_ACL_Multicast(driver,url,MSC_card,username,password, ems_url, ems_password,file_name)
        # [retest skip] ems.EMS_ACL_DHCP_L2Agent(driver,url,MSC_card,username,password, ems_url, ems_password,file_name)
        # [retest skip] ems.EMS_ACL_ACL_Profile(driver,url,username,password, ems_url, ems_password,file_name)
        # [retest skip] ems.EMS_ACL_Egress_Profile(driver,url,username,password, ems_url, ems_password,file_name)
        # [retest skip] ems.EMS_ACL_Host_Protection(driver,url,username,password, ems_url, ems_password,file_name)
        # [retest skip] ems.EMS_ACL_ARP_Inspection_VLAN(driver,url,username,password, ems_url, ems_password,file_name)
        # [retest skip] ems.EMS_ACL_DHCP_Remote_Backup_Apply(driver,url,username,password, ems_url, ems_password,file_name)
        # [retest skip] ems.EMS_ACL_8021x_General_Setup_Test(driver,url,username,password, ems_url, ems_password,file_name)
        # [retest skip] ems.EMS_ACL_8021x_Radius_Server_Test(driver,url,username,password, ems_url, ems_password,file_name)
        # [retest skip] ems.EMS_ACL_8021x_User_Profile_Test(driver,url,username,password, ems_url, ems_password,file_name)
        # [retest skip] ems.Multicast_IGMP_Setup(driver,url,MSC_card,username,password, ems_url, ems_password,file_name)
        # [retest skip] ems.Multicast_MVLAN_And_MVLAN_Table(driver,url,MSC_card,username,password, ems_url, ems_password,file_name)

        ems.Sys_General_Setup(driver,url,MSC_card,username,password, ems_url, ems_password,file_name)
        # [retest skip] Ip_setup_gateway = ems.Sys_IPv4_Setup(driver,url,MSC_card,username,password, ems_url, ems_password,file_name)
        # [retest skip] ems.Sys_IPv6_Setup(driver,url,MSC_card,username,password, ems_url, ems_password,file_name)
        # [retest skip] ems.Sys_IP_Route(driver,url,MSC_card,username,password, ems_url, ems_password,file_name, Ip_setup_gateway)

        # [retest skip] ems.Switch_General(driver,url,MSC_card,username,password, ems_url, ems_password,file_name)
        # [retest skip] ems.Switch_Dot3ad(driver,url,MSC_card,MSC_slot,msc_port,username,password, ems_url, ems_password,file_name)
        # [retest skip] ems.Switch_Isolation(driver,url,MSC_card,username,password, ems_url, ems_password,file_name)
        # [retest skip] ems.Switch_DSCP_Priority_Mapping(driver,url,username,password, ems_url, ems_password,file_name)
        # [retest skip] ems.VLAN_Tag_Mode_Setup(driver,url,MSC_card,MSC_slot,username,password, ems_url, ems_password,file_name)
        ems.Multicast_VLAN_Mode(driver,url,MSC_card,username,password, ems_url, ems_password,file_name) # 4000

        # [retest skip] ems.EMS_Filter_Test(driver,url, ems_url, ems_password,file_name)
        # [retest skip] ems.EMS_Configure_Save_Test(driver,url, ems_url, ems_password,file_name)

        # [retest skip] ems.EMS_Refresh_Test(driver,username, ems_url, ems_password,file_name)
        # [retest skip] ems.FW_Refresh_Test(driver,url,username,password,file_name)

        end_time3 = time.time() 
        total_time = end_time3 - start_time3
        print(f'No Card Test    Total time: {int(total_time/60/60)} hr {int(total_time/60%60)} min {int(total_time%60)} sec',file = open(file_name, '+a'))
        print("[Page]",file = open(file_name, '+a'))

        





        print("======================================================================================", file=open(file_name, '+a', encoding='utf-8'))
        print("Card Test", file=open(file_name, '+a', encoding='utf-8'))
        print("======================================================================================", file=open(file_name, '+a', encoding='utf-8'))

        for i in range(len(list1)):
        #for i in range(2,3):
            list_element = list1[i]
            slot = list_element.split(",")[1]
            port = list_element.split(",")[2]
            cardtype = list_element.split(",")[3]


            print(f"\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> [ {cardtype} ]",file = open(file_name, '+a'))
            print(
                f"             Now in case:{list_element[:1]},  Slot-Port:{slot}-{port}, {cardtype}   ({i+1}/{len(list1)})",
                file=open(file_name, '+a', encoding='utf-8')
            )
            print("======================================================================================", file=open(file_name, '+a', encoding='utf-8'))
            
            # ACL
            # [retest skip] ems.EMS_ACL_Anti_MAC_Spoof(driver, url, list_element, username, password, ems_url, ems_password, file_name)
            # [retest skip] ems.EMS_ACL_ARP_Inspection(driver,url,list_element,username,password, ems_url, ems_password,file_name)
            # [retest skip] ems.EMS_ACL_DHCP_Remote_Backup(driver,url,list_element,username,password, ems_url, ems_password,file_name)
            # [retest skip] ems.EMS_ACL_MAC_Count(driver,url,list_element,username,password, ems_url, ems_password,file_name)
            # [retest skip] ems.EMS_ACL_MAC_Filter(driver,url,list_element,username,password, ems_url, ems_password,file_name)
            # [retest skip] ems.EMS_ACL_OUI_Filter(driver,url,list_element,username,password, ems_url, ems_password,file_name)
            # [retest skip] ems.EMS_ACL_Packet_Filter(driver,url,list_element,username,password, ems_url, ems_password,file_name)
            # [retest skip] ems.EMS_ACL_Rule_Profile(driver,url,list_element,username,password, ems_url, ems_password,file_name)
            # [retest skip] ems.EMS_ACL_Egress_Rule_Profile(driver,url,list_element,username,password, ems_url, ems_password,file_name)
            # [retest skip] ems.EMS_ACL_8021x_Port_Setting_Test(driver,url,list_element,username,password, ems_url, ems_password,file_name)
            if if_Neox:
               pass
               # [retest skip] ems.EMS_Neox_ACL_Loopguard(driver,url,list_element,username,password, ems_url, ems_password,file_name)
               # [retest skip] ems.EMS_Neox_ACL_BPDU_Ctrl(driver,url,list_element,username,password, ems_url, ems_password,file_name)
            # Multicast
            # [retest skip] ems.Multicast_Port_Mode(driver,url,list_element,username,password, ems_url, ems_password,file_name)
            # [retest skip] ems.Multicast_Multicast_MAC(driver,url,list_element,username,password, ems_url, ems_password,file_name)
            # [retest skip] ems.Multicast_Multicast_IP(driver,url,list_element,username,password, ems_url, ems_password,file_name)
            # Switch
            # [retest skip] ems.Switch_DSCP(driver,url,list_element,username,password, ems_url, ems_password,file_name)
            # [retest skip] ems.Switch_Storm_Control(driver,url,list_element,username,password, ems_url, ems_password,file_name)
            # Port    
            # [retest skip] ems.Port_GENNI(driver,url,list_element,MSC_slot,msc_port,username,password, ems_url, ems_password,file_name)
            # [retest skip] ems.Port_GE(driver,url,list_element,MSC_slot,username,password, ems_url, ems_password,file_name)
            # [retest skip] ems.Port_Qos(driver,url,list_element,username,password, ems_url, ems_password,file_name)
            # [retest skip] ems.Port_DHCP(driver,url,list_element,username,password, ems_url, ems_password,file_name)
            # VLAN    
            driver.get(url)
            ems.VLAN_VLAN_Table(driver,url,list_element,username,password, ems_url, ems_password,file_name) 
            # [retest skip] ems.VLAN_Untag_And_Copy_Cpbit(driver,url,list_element,username,password, ems_url, ems_password,file_name)
            
            # [retest skip] ems.xPON_OLT_Config(driver,url,list_element,username,password, ems_url, ems_password,file_name)
            # [retest skip] ems.GPON_OLT_Registration(driver,url,list_element,username,password, ems_url, ems_password,file_name)
            print("[Page]",file = open(file_name, '+a'))
            # print("\n______________________________________________________________________________________________________________________________________________________________\n",file = open(file_name, '+a'))

        
        # driver.get(url)
        # mod.Login(driver, username, password)
        # ems.Maintenance_Config_Reset(driver)
        try:
            driver.close()
        except:
            pass

        total_time = time.time() - start_time0
        print(f'Total time: {int(total_time/60/60)} hr {int(total_time/60%60)} min {int(total_time%60)} sec',
              file=open(file_name, '+a', encoding='utf-8'))


        # Erase Running
        # driver.get(url)
        # mod.Login(driver,username,password)
        # ems.Maintenance_Config_Reset(driver)
        # Wait 30 sec
        # time.sleep(30)
        # write memory
        # import module.telnet_module as tel
        # telnet = tel.Telnet(ip=url_ip)
        # telnet.send("write memory")
        # telnet.close()        
        

        return f"[{tname}] {env_file} ✔ done"

    except Exception as e:
        # 失敗也回傳字串，主執行緒可收集
        msg = f"[{tname}] {env_file} ✖ failed: {e}\n{traceback.format_exc()}"
        # 也可寫入一個 per-env 的錯誤檔
        err_file = f"Report/error_{env_file.replace('/', '_')}.log"
        print(msg, file=open(err_file, '+a', encoding='utf-8'))
        return msg


# env_list = [
#     # NeoX
#     # "ENV/ENV_WEB_88.json",    # NeoX-06
#     # "ENV/ENV_WEB_222.json",    # NeoX-06
#     # "ENV/ENV_WEB_202.json",    # NeoX-06
#     # "ENV/ENV_WEB_204.json",     # NeoX-03

#     # IESxx
#     # "ENV/ENV_WEB_203.json",  # version
#     # "ENV/ENV_WEB_205.json",
#     # "ENV/ENV_WEB_206.json",    # IES6217
#     # "ENV/ENV_WEB_208.json",    # XB
#     # "ENV/ENV_WEB_209.json",  # version
#     # "ENV/ENV_WEB_225.json",    # XA
#     # "ENV/ENV_WEB_226.json",
#     "ENV/ENV_WEB_82.json",     # IES5206
#     # "ENV/ENV_WEB_83.json",     # IES4204 QB
# ]


#  =====================================================================
#  ENV File Setting
#  =====================================================================  python Run_EMS_Config_all.py 82
# 1. 設定參數解析器
parser = argparse.ArgumentParser(description="指定一個或多個環境編號")

# 2. 修改 nargs='*' 允許接收多個數值，並設定預設值為 ['82']
parser.add_argument(
    'env_ids', 
    type=str, 
    nargs='*', 
    default=['82'], 
    help='輸入一個或多個環境編號 (例如: 82 206 222)'
)

parser.add_argument(
    '--slots',
    type=str,
    nargs='*',
    default=None,
    help='只跑指定 slot 的卡 (例如: --slots 1 8)，不指定則全部'
)

args = parser.parse_args()

# 3. 使用列表推導式 (List Comprehension) 產生 env_list
env_list = [f"ENV/ENV_WEB_{eid}.json" for eid in args.env_ids]

# 測試列印結果
print(f"目前執行的環境列表: {env_list}")
#  =====================================================================




# 可調整同時 worker 數：預設 = min(4, len(env_list))，避免把機器或目標站點壓垮
max_workers = len(env_list) # min(4, len(env_list))  

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
