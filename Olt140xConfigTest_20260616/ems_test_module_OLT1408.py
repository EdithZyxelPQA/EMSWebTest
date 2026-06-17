from os import times
import time
import datetime
from attr import field
from pyrsistent import s
import selenium_module as mod
import xpon_olt_status_module as olts
import xpon_olt_config_module as oltc
import xpon_batch_ont_config_module as bat
import xpon_ont_config_module as ontc
import xpon_profiles_module as pro
import multicast_module as mul
import xpon_profiles_config_module as procf
from selenium.webdriver.support.ui import Select
import pyautogui
import web_share.EMS.ems_module as e_mod
import ems_profile_module as e_pro
SUCCESS_TEXT = "uccess"
# from robot.api import TestSuite
# from robot.api import ResultWriter
# from robot.libraries.BuiltIn import BuiltIn
from selenium import webdriver
# from robot.libraries.BuiltIn import RobotNotRunningError
# from robot.api import logger

# import win32com.client as win32 #
# from docx import Document
# from docx.shared import Inches
from customdriver import CustomDriver

import ems_module_OLT1408 as e_swi


# from variable_module import *
import web_share.EMS.ems_module as e_mod
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
# import variable_module

import linecache
import sys as real_sys
import traceback
import io
from functools import wraps
from dataclasses import dataclass, asdict

def run(driver,cfg):
    print(f"running on {cfg.url} as {cfg.username}")

def get_file_name(n):                           # ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! 
    global file_name
    file_name = n

# 定義一個裝飾器，用於自動重試
def retry(max_retries=2, delay=2):
    # file_name = parameter_get("file_name")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"                                                                                           [TIME]",file = open(file_name, '+a'))
            start_time = time.time()      
            tmp = None
            try:
                driver_tmp = args[0]
            except:
                pass            
            for attempt in range(max_retries):                
                try:
                    # print(f"Executing {func.__name__}, Attempt: {attempt + 1}")                
                    # return func(*args, **kwargs)
                    tmp = func(*args, **kwargs)
                    
                    total_time = time.time() - start_time
                    print(f'                                                                                           [TIME {int(total_time/60/60)}:{int(total_time/60%60)}:{int(total_time%60)}]   {str(datetime.datetime.now())}',file = open(file_name, '+a'))
                    
                    return tmp
                except Exception as e:

                    try:
                        e = str(e).split("Stacktrace")[0]
                    except:
                        pass

                    print(f"\nError in {func.__name__}: {e}",file = open(file_name, '+a'))
                    PrintException(file_name)
                    if attempt < max_retries - 1:
                        # print(f"Retrying {func.__name__} after {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print(f"{func.__name__} failed after {max_retries} attempts. Skipping...",file = open(file_name, '+a'))                      
                        print(f"======================================================================================",file = open(file_name, '+a'))
                        
                        total_time = time.time() - start_time
                        print(f'                                                                                           [TIME {int(total_time/60/60)}:{int(total_time/60%60)}:{int(total_time%60)}]   {str(datetime.datetime.now())}',file = open(file_name, '+a'))

                        try:
                            # driver.save_screenshot(f"D:/tmp.png")                    
                            driver_tmp.save_screenshot(f'Report/{str(datetime.datetime.now()).split(":")[0]}{str(datetime.datetime.now()).split(":")[1]}.{str(datetime.datetime.now()).split(":")[2][:5]}_{func.__name__}_screenshot.png')
                        except:
                            pass   


                        return None                
                    print(f"-------------------------------------- Retry -----------------------------------------",file = open(file_name, '+a'))    
       
       
        return wrapper
    return decorator   

def PrintException(file_name): # author:Apogentus, https://stackoverflow.com/questions/14519177/python-exception-handling-line-number
    exc_type, exc_obj, tb = real_sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)

    print(f'             traceback start',file = open(file_name, '+a'))
    with io.StringIO() as buffer:
        traceback.print_exc(file=buffer)
        err_info = buffer.getvalue()

    try:
        err_info = err_info.split("Stacktrace")[0]
    except:
        pass
    print(err_info,file = open(file_name, '+a'))
    print(f'             traceback end',file = open(file_name, '+a'))




def EMS_Provision_Config_path(driver,url,file_name):

    print(f"--------------------------------------------------------------------------------------",file = open(file_name, '+a'))

    time.sleep(2)
    driver.switch_to.default_content()
    time.sleep(1) 
    Wait_Block(driver)
    driver.find_element(By.LINK_TEXT,"Provision").click()
    time.sleep(2)
    Wait_Block(driver)
    driver.find_element(By.LINK_TEXT,"Configuration").click()
    time.sleep(1)
    Wait_Block(driver)
    driver.find_element(By.LINK_TEXT,"Configuration").click()
    time.sleep(1)
    Wait_Block(driver)

    # input ip
    url_ip = url.split("/")[2]    
    driver.find_element(By.ID, "map_key_filter").clear()
    driver.find_element(By.ID, "map_key_filter").send_keys(url_ip)
    time.sleep(1)
    # click filter
    driver.find_element(By.ID, "map_key_searsh").click()
    time.sleep(1)
    # click EMS
    # driver.find_element(By.CLASS_NAME, "icon.expand-icon.oi.oi-plus").click()  # click '+'  
    # click Cecily                     
    # driver.find_element(By.CLASS_NAME, "icon.expand-icon.oi.oi-plus").click()  # click '+'

    try:
        num = len(driver.find_elements(By.CLASS_NAME, "icon.expand-icon.oi.oi-plus"))
        for i in range(num):
            driver.find_elements(By.CLASS_NAME, "icon.expand-icon.oi.oi-plus")[i].click()  # click '+'
    except:
        pass

    driver.find_element(By.CLASS_NAME, "list-group-item.node-navMenuTree.node-selected").click()  # click '[]'
    
    # click IES 192.168.xxx.xxx
    # print(f"test after 192.168.: {url_ip[8:]}")
    # driver.find_element(By.XPATH, f'//*[@title="IES6217_{url_ip[8:]}({url_ip})"]').click()
    time.sleep(1)
    driver.find_element('xpath',f"//*[contains(text(),'{url_ip}')]").click()
    driver.switch_to.frame(0)   

def Wait_Block(driver):
    # try:
    #     if_block = True
    #     count = 0
    #     time.sleep(1) # time.sleep(0.2)
    #     while((if_block == True) and (count < 300)):  # 10
    #         if("block" in driver.find_element(By.ID,"configure_loader").get_attribute("style")):
    #             time.sleep(0.5)   
    #             count = count + 1     
    #         else:
    #             if_block = False
    #     time.sleep(0.1)
    # except:
    #     pass
    e_mod.Wait_Block(driver)
@retry()
def Basic_General(driver,url,ems_url,file_name):
    # # Basic_General_set up
    print(f"======================================================================================",file = open(file_name, '+a'))
    print(f"Basic Setting - General Setup Test Start",file = open(file_name, '+a'))
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(10)
    driver.find_element(By.LINK_TEXT,"Basic Setting").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"General Setup").click()
    time.sleep(2)
    driver.find_element(By.LINK_TEXT,"Basic Setting").click() 
    time.sleep(1)
    e_swi.Basic_General_System(driver,"O _ O->OLT1408_EMS_SystemName_Test_xxxxxxxxxxxxxxxxxxxxxxxxxxx63")
    e_swi.Basic_General_Location(driver,"O _ O->OLT1408_EMS_Location_xx31")
    e_swi.Basic_General_Contact(driver,"O _ O->OLT1408_EMS_Contact_xxx31")
    e_swi.Basic_General_UseTime(driver,"NTP(RFC-1305)")
    e_swi.Basic_General_TimeIP(driver,"216.239.35.4")
    e_swi.Basic_General_TimeZone(driver,"UTC+0800")
    e_swi.Basic_General_Daylight(driver,True)
    e_swi.Basic_General_StartDate_Week(driver,"First")
    e_swi.Basic_General_StartDate_Day(driver,"Monday")
    e_swi.Basic_General_StartDate_Month(driver,"January")
    e_swi.Basic_General_StartDate_Hour(driver,"0:00")
    e_swi.Basic_General_EndDate_Week(driver,"Last")
    e_swi.Basic_General_EndDate_Day(driver,"Sunday")
    e_swi.Basic_General_EndDate_Month(driver,"December")
    e_swi.Basic_General_EndDate_Hour(driver,"23:00")
    e_swi.Basic_General_Apply(driver,file_name)

    # # Basic_General_setup EMS check
    time.sleep(2)
    driver.find_element(By.LINK_TEXT,"Basic Setting").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"General Setup").click()
    if_temp_error = False 
    time.sleep(3)
    if(driver.find_element(By.ID,"basic_generalsetup_hostname_text").get_attribute("value") == "O _ O->OLT1408_EMS_SystemName_Test_xxxxxxxxxxxxxxxxxxxxxxxxxxx63" ):
        print(f"             [EMS1-6445][Basic - General Setup - New] EMS System (O _ O->OLT1408_EMS_SystemName_Test_xxxxxxxxxxxxxxxxxxxxxxxxxxx63) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - New] EMS System ({driver.find_element(By.ID,"basic_generalsetup_hostname_text").get_attribute("value")} != O _ O->OLT1408_EMS_SystemName_Test_xxxxxxxxxxxxxxxxxxxxxxxxxxx63) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(driver.find_element(By.ID,"basic_generalsetup_location_text").get_attribute("value") == "O _ O->OLT1408_EMS_Location_xx31" ):
        print(f"             [EMS1-6445][Basic - General Setup - New] EMS Location (O _ O->OLT1408_EMS_Location_xx31) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - New] EMS Location ({driver.find_element(By.ID,"basic_generalsetup_location_text").get_attribute("value")} != O _ O->OLT1408_EMS_Location_xx31) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(driver.find_element(By.ID,"basic_generalsetup_personname_text").get_attribute("value") == "O _ O->OLT1408_EMS_Contact_xxx31" ):
        print(f"             [EMS1-6445][Basic - General Setup - New] EMS Contact (O _ O->OLT1408_EMS_Contact_xxx31) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - New] EMS Contact ({driver.find_element(By.ID,"basic_generalsetup_personname_text").get_attribute("value")} != O _ O->OLT1408_EMS_Contact_xxx31) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(Select(driver.find_element(By.ID,"basic_generalsetup_timeservertype_select")).first_selected_option.get_attribute("text") == "NTP(RFC-1305)" ):
        print(f"             [EMS1-6445][Basic - General Setup - New] EMS UseTime (NTP(RFC-1305)) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - New] EMS UseTime ({Select(driver.find_element(By.ID,"basic_generalsetup_timeservertype_select")).first_selected_option.get_attribute("text")} != NTP(RFC-1305)) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(driver.find_element(By.ID,"basic_generalsetup_timeserveripaddress_text").get_attribute("value") == "216.239.35.4" ):
        print(f"             [EMS1-6445][Basic - General Setup - New] EMS TimeIP (216.239.35.4) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - New] EMS TimeIP ({driver.find_element(By.ID,"basic_generalsetup_timeserveripaddress_text").get_attribute("value")} != 216.239.35.4) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(Select(driver.find_element(By.ID,"basic_generalsetup_timezone_select")).first_selected_option.get_attribute("text") == "UTC+0800" ):
        print(f"             [EMS1-6445][Basic - General Setup - New] EMS TimeZone (UTC+0800) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - New] EMS TimeZone ({Select(driver.find_element(By.ID,"basic_generalsetup_timezone_select")).first_selected_option.get_attribute("text")} != UTC+0800) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(driver.find_element(By.ID,"basic_generalsetup_daylight_checkbox").is_selected() == True):
        print(f"             [EMS1-6445][Basic - General Setup - New] EMS Daylight (True) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - New] EMS Daylight ({driver.find_element(By.ID,"basic_generalsetup_daylight_checkbox").is_selected()} != True) fail',file = open(file_name, '+a'))
        if_temp_error = True   
    if(Select(driver.find_element(By.ID,"basic_generalsetup_startdate1_select")).first_selected_option.get_attribute("text") == "First" and Select(driver.find_element(By.ID,"basic_generalsetup_startdate2_select")).first_selected_option.get_attribute("text") == "Monday" and Select(driver.find_element(By.ID,"basic_generalsetup_startdate3_select")).first_selected_option.get_attribute("text") == "January" and Select(driver.find_element(By.ID,"basic_generalsetup_startdate4_select")).first_selected_option.get_attribute("text") == "0:00"):
        print(f"             [EMS1-6445][Basic - General Setup - New] EMS StartDate pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6445][Basic - General Setup - New] EMS StartDate fail",file = open(file_name, '+a'))
        if_temp_error = True
    if(Select(driver.find_element(By.ID,"basic_generalsetup_enddate1_select")).first_selected_option.get_attribute("text") == "Last" and Select(driver.find_element(By.ID,"basic_generalsetup_enddate2_select")).first_selected_option.get_attribute("text") == "Sunday" and Select(driver.find_element(By.ID,"basic_generalsetup_enddate3_select")).first_selected_option.get_attribute("text") == "December" and Select(driver.find_element(By.ID,"basic_generalsetup_enddate4_select")).first_selected_option.get_attribute("text") == "23:00"):
        print(f"             [EMS1-6445][Basic - General Setup - New] EMS EndDate pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6445][Basic - General Setup - New] EMS EndDate fail",file = open(file_name, '+a'))
        if_temp_error = True
    # if(if_temp_error==False):
    #     print(f"             [EMS1-6445][Basic - General Setup] EMS Result pass",file = open(file_name, '+a'))
    # else:
    #     print(f"             [EMS1-6445][Basic - General Setup] EMS Result fail",file = open(file_name, '+a'))


    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Basic Setting").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"General Setup").click()
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    time.sleep(1)

    # # Basic_General_setup 192.168.169.207 Check

    # if_temp_error = False 
    if(driver.find_element(By.NAME,"RpGeneral_IptTextSystemName").get_attribute("value") == "O _ O->OLT1408_EMS_SystemName_Test_xxxxxxxxxxxxxxxxxxxxxxxxxxx63" ):
        print(f"             [EMS1-6445][Basic - General Setup - New] System (O _ O->OLT1408_EMS_SystemName_Test_xxxxxxxxxxxxxxxxxxxxxxxxxxx63) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - New] System ({driver.find_element(By.NAME,"RpGeneral_IptTextSystemName").get_attribute("value")} != O _ O->OLT1408_EMS_SystemName_Test_xxxxxxxxxxxxxxxxxxxxxxxxxxx63) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(driver.find_element(By.NAME,"RpGeneral_IptTextLocation").get_attribute("value") == "O _ O->OLT1408_EMS_Location_xx31" ):
        print(f"             [EMS1-6445][Basic - General Setup - New] Location (O _ O->OLT1408_EMS_Location_xx31) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - New] Location ({driver.find_element(By.NAME,"RpGeneral_IptTextLocation").get_attribute("value")} != O _ O->OLT1408_EMS_Location_xx31) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(driver.find_element(By.NAME,"RpGeneral_IptTextContact").get_attribute("value") == "O _ O->OLT1408_EMS_Contact_xxx31" ):
        print(f"             [EMS1-6445][Basic - General Setup - New] Contact (O _ O->OLT1408_EMS_Contact_xxx31) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - New] Contact ({driver.find_element(By.NAME,"RpGeneral_IptTextContact").get_attribute("value")} != O _ O->OLT1408_EMS_Contact_xxx31) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(Select(driver.find_element(By.NAME,"RpGeneral_SltTimeProtocol")).first_selected_option.get_attribute("text") == "NTP(RFC-1305)" ):
        print(f"             [EMS1-6445][Basic - General Setup - New] UseTime (NTP(RFC-1305)) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - New] UseTime ({Select(driver.find_element(By.NAME,"RpGeneral_SltTimeProtocol")).first_selected_option.get_attribute("text")} != NTP(RFC-1305)) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(driver.find_element(By.NAME,"RpGeneral_IptTextTimeSvrIP").get_attribute("value") == "216.239.35.4" ):
        print(f"             [EMS1-6445][Basic - General Setup - New] TimeIP (216.239.35.4) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup] TimeIP ({driver.find_element(By.NAME,"RpGeneral_IptTextTimeSvrIP").get_attribute("value")} != 216.239.35.4) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(Select(driver.find_element(By.NAME,"RpGeneral_SltTimeZone")).first_selected_option.get_attribute("text") == "UTC+0800" ):
        print(f"             [EMS1-6445][Basic - General Setup - New] TimeZone (UTC+0800) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - New] TimeZone ({Select(driver.find_element(By.NAME,"RpGeneral_SltTimeZone")).first_selected_option.get_attribute("text")} != UTC+0800) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(driver.find_element(By.NAME,"RpGeneral_CheckDaylightSavingTime").is_selected() == True ):
        print(f"             [EMS1-6445][Basic - General Setup - New] Daylight (True) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - New] Daylight ({driver.find_element(By.NAME,"RpGeneral_CheckDaylightSavingTime").is_selected()} != True) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(Select(driver.find_element(By.NAME,"RpGeneral_SltStartWeek")).first_selected_option.get_attribute("text") == "First" and Select(driver.find_element(By.NAME,"RpGeneral_SltStartDay")).first_selected_option.get_attribute("text") == "Monday" and Select(driver.find_element(By.NAME,"RpGeneral_SltStartMonth")).first_selected_option.get_attribute("text") == "January" and Select(driver.find_element(By.NAME,"RpGeneral_SltStartHour")).first_selected_option.get_attribute("text") == "0:00"):
        print(f"             [EMS1-6445][Basic - General Setup - New] StartDate pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6445][Basic - General Setup - New] StartDate fail",file = open(file_name, '+a'))
        if_temp_error = True
    if(Select(driver.find_element(By.NAME,"RpGeneral_SltEndWeek")).first_selected_option.get_attribute("text") == "Last" and Select(driver.find_element(By.NAME,"RpGeneral_SltEndDay")).first_selected_option.get_attribute("text") == "Sunday" and Select(driver.find_element(By.NAME,"RpGeneral_SltEndMonth")).first_selected_option.get_attribute("text") == "December" and Select(driver.find_element(By.NAME,"RpGeneral_SltEndHour")).first_selected_option.get_attribute("text") == "23:00"):
        print(f"             [EMS1-6445][Basic - General Setup - New] EndDate pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6445][Basic - General Setup - New] EndDate fail",file = open(file_name, '+a'))
        if_temp_error = True
    # if(if_temp_error==False):
    #     print(f"             [EMS1-6445][Basic - General Setup] Result Pass",file = open(file_name, '+a'))
    # else:
    #     print(f"             [EMS1-6445][Basic - General Setup] Result Fail",file = open(file_name, '+a'))
    

    # # Basic_General_modify
        
    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT,"Basic Setting").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"General Setup").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"Basic Setting").click() 
    time.sleep(1)
    e_swi.Basic_General_System(driver,"O _ O->OLT1408_EMS_SystemName_Test_xxxxxxxxxxxxxxxxxxxxxxxxx63_m")
    e_swi.Basic_General_Location(driver,"O _ O->OLT1408_EMS_Location_m_31")
    e_swi.Basic_General_Contact(driver,"O _ O->OLT1408_EMS_Contact_m_x31")
    e_swi.Basic_General_UseTime(driver,"Daytime(RFC-867)")
    e_swi.Basic_General_TimeIP(driver,"216.239.35.1")
    e_swi.Basic_General_TimeZone(driver,"UTC-0100")
    e_swi.Basic_General_Daylight(driver,True)
    e_swi.Basic_General_StartDate_Week(driver,"Last")
    e_swi.Basic_General_StartDate_Day(driver,"Sunday")
    e_swi.Basic_General_StartDate_Month(driver,"December")
    e_swi.Basic_General_StartDate_Hour(driver,"23:00")
    e_swi.Basic_General_EndDate_Week(driver,"First")
    e_swi.Basic_General_EndDate_Day(driver,"Monday")
    e_swi.Basic_General_EndDate_Month(driver,"January")
    e_swi.Basic_General_EndDate_Hour(driver,"0:00")
    e_swi.Basic_General_Apply(driver,file_name)
    time.sleep(1)
    e_swi.Basic_General_StartDate_Hour(driver,"23:00")
    e_swi.Basic_General_Apply(driver,file_name)

    # # Basic_General_modufy EMS check
    time.sleep(2)
    driver.find_element(By.LINK_TEXT,"Basic Setting").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"General Setup").click()
    # if_temp_error = False 
    time.sleep(3)
    if(driver.find_element(By.ID,"basic_generalsetup_hostname_text").get_attribute("value") == "O _ O->OLT1408_EMS_SystemName_Test_xxxxxxxxxxxxxxxxxxxxxxxxx63_m"):
        print(f"             [EMS1-6445][Basic - General Setup - Modify] EMS System (O _ O->OLT1408_EMS_SystemName_Test_xxxxxxxxxxxxxxxxxxxxxxxxx63_m) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - Modify] EMS System ({driver.find_element(By.ID,"basic_generalsetup_hostname_text").get_attribute("value")} != O _ O->OLT1408_EMS_SystemName_Test_xxxxxxxxxxxxxxxxxxxxxxxxx63_m) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(driver.find_element(By.ID,"basic_generalsetup_location_text").get_attribute("value") == "O _ O->OLT1408_EMS_Location_m_31" ):
        print(f"             [EMS1-6445][Basic - General Setup - Modify] EMS Location (O _ O->OLT1408_EMS_Location_m_31) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - Modify] EMS Location ({driver.find_element(By.ID,"basic_generalsetup_location_text").get_attribute("value")} != O _ O->OLT1408_EMS_Location_m_31) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(driver.find_element(By.ID,"basic_generalsetup_personname_text").get_attribute("value") == "O _ O->OLT1408_EMS_Contact_m_x31" ):
        print(f"             [EMS1-6445][Basic - General Setup - Modify] EMS Contact (O _ O->OLT1408_EMS_Contact_m_x31) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - Modify] EMS Contact ({driver.find_element(By.ID,"basic_generalsetup_personname_text").get_attribute("value")} != O _ O->OLT1408_EMS_Contact_m_x31) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(Select(driver.find_element(By.ID,"basic_generalsetup_timeservertype_select")).first_selected_option.get_attribute("text") == "Daytime(RFC-867)" ):
        print(f"             [EMS1-6445][Basic - General Setup - Modify] EMS UseTime (Daytime(RFC-867)) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - Modify] EMS UseTime ({Select(driver.find_element(By.ID,"basic_generalsetup_timeservertype_select")).first_selected_option.get_attribute("text")} != Daytime(RFC-867)) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(driver.find_element(By.ID,"basic_generalsetup_timeserveripaddress_text").get_attribute("value") == "216.239.35.1" ):
        print(f"             [EMS1-6445][Basic - General Setup - Modify] EMS TimeIP (216.239.35.1) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - Modify] EMS TimeIP ({driver.find_element(By.ID,"basic_generalsetup_timeserveripaddress_text").get_attribute("value")} != 216.239.35.1) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(Select(driver.find_element(By.ID,"basic_generalsetup_timezone_select")).first_selected_option.get_attribute("text") == "UTC-0100" ):
        print(f"             [EMS1-6445][Basic - General Setup - Modify] EMS TimeZone (UTC-0100) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - Modify] EMS TimeZone ({Select(driver.find_element(By.ID,"basic_generalsetup_timezone_select")).first_selected_option.get_attribute("text")} != UTC-0100) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(driver.find_element(By.ID,"basic_generalsetup_daylight_checkbox").is_selected() == True):
        print(f"             [EMS1-6445][Basic - General Setup - Modify] EMS Daylight (True) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - Modify] EMS Daylight ({driver.find_element(By.ID,"basic_generalsetup_daylight_checkbox").is_selected()} != True) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(Select(driver.find_element(By.ID,"basic_generalsetup_startdate1_select")).first_selected_option.get_attribute("text") == "Last" and Select(driver.find_element(By.ID,"basic_generalsetup_startdate2_select")).first_selected_option.get_attribute("text") == "Sunday" and Select(driver.find_element(By.ID,"basic_generalsetup_startdate3_select")).first_selected_option.get_attribute("text") == "December" and Select(driver.find_element(By.ID,"basic_generalsetup_startdate4_select")).first_selected_option.get_attribute("text") == "23:00"):
        print(f"             [EMS1-6445][Basic - General Setup - Modify] EMS StartDate pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6445][Basic - General Setup - Modify] EMS StartDate fail",file = open(file_name, '+a'))
        if_temp_error = True
    if(Select(driver.find_element(By.ID,"basic_generalsetup_enddate1_select")).first_selected_option.get_attribute("text") == "First" and Select(driver.find_element(By.ID,"basic_generalsetup_enddate2_select")).first_selected_option.get_attribute("text") == "Monday" and Select(driver.find_element(By.ID,"basic_generalsetup_enddate3_select")).first_selected_option.get_attribute("text") == "January" and Select(driver.find_element(By.ID,"basic_generalsetup_enddate4_select")).first_selected_option.get_attribute("text") == "0:00"):
        print(f"             [EMS1-6445][Basic - General Setup - Modify] EMS EndDate pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6445][Basic - General Setup - Modify] EMS EndDate fail",file = open(file_name, '+a'))
        if_temp_error = True
    # if(if_temp_error==False):
    #     print(f"             [EMS1-6445][Basic - General Setup - Modify] EMS Result pass",file = open(file_name, '+a'))
    # else:
    #     print(f"             [EMS1-6445][Basic - General Setup - Modify] EMS Result fail",file = open(file_name, '+a'))

    # # Basic_General_modify 192.168.169.207 check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Basic Setting").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"General Setup").click()
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    time.sleep(3)
    # if_temp_error = False 
    if(driver.find_element(By.NAME,"RpGeneral_IptTextSystemName").get_attribute("value") == "O _ O->OLT1408_EMS_SystemName_Test_xxxxxxxxxxxxxxxxxxxxxxxxx63_m" ):
        print(f"             [EMS1-6445][Basic - General Setup - Modify] System (O _ O->OLT1408_EMS_SystemName_Test_xxxxxxxxxxxxxxxxxxxxxxxxx63_m) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - Modify] System ({driver.find_element(By.NAME,"RpGeneral_IptTextSystemName").get_attribute("value")} != O _ O->OLT1408_EMS_SystemName_Test_xxxxxxxxxxxxxxxxxxxxxxxxx63_m) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(driver.find_element(By.NAME,"RpGeneral_IptTextLocation").get_attribute("value") == "O _ O->OLT1408_EMS_Location_m_31" ):
        print(f"             [EMS1-6445][Basic - General Setup - Modify] Location (O _ O->OLT1408_EMS_Location_m_31) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - Modify] Location ({driver.find_element(By.NAME,"RpGeneral_IptTextLocation").get_attribute("value")} != O _ O->OLT1408_EMS_Location_m_31) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(driver.find_element(By.NAME,"RpGeneral_IptTextContact").get_attribute("value") == "O _ O->OLT1408_EMS_Contact_m_x31" ):
        print(f"             [EMS1-6445][Basic - General Setup - Modify] Contact (O _ O->OLT1408_EMS_Contact_m_x31) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - Modify] Contact ({driver.find_element(By.NAME,"RpGeneral_IptTextContact").get_attribute("value")} != O _ O->OLT1408_EMS_Contact_m_x31) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(Select(driver.find_element(By.NAME,"RpGeneral_SltTimeProtocol")).first_selected_option.get_attribute("text") == "Daytime(RFC-867)" ):
        print(f"             [EMS1-6445][Basic - General Setup - Modify] UseTime (Daytime(RFC-867)) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - Modify] UseTime ({Select(driver.find_element(By.NAME,"RpGeneral_SltTimeProtocol")).first_selected_option.get_attribute("text")} != Daytime(RFC-867)) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(driver.find_element(By.NAME,"RpGeneral_IptTextTimeSvrIP").get_attribute("value") == "216.239.35.1" ):
        print(f"             [EMS1-6445][Basic - General Setup - Modify] TimeIP (216.239.35.1) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - Modify] TimeIP ({driver.find_element(By.NAME,"RpGeneral_IptTextTimeSvrIP").get_attribute("value")} != 216.239.35.1) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(Select(driver.find_element(By.NAME,"RpGeneral_SltTimeZone")).first_selected_option.get_attribute("text") == "UTC-0100" ):
        print(f"             [EMS1-6445][Basic - General Setup - Modify] TimeZone (UTC-0100) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - Modify] TimeZone ({Select(driver.find_element(By.NAME,"RpGeneral_SltTimeZone")).first_selected_option.get_attribute("text")} != UTC-0100) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(driver.find_element(By.NAME,"RpGeneral_CheckDaylightSavingTime").is_selected() == True ):
        print(f"             [EMS1-6445][Basic - General Setup - Modify] Daylight (True) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - Modify] Daylight ({driver.find_element(By.NAME,"RpGeneral_CheckDaylightSavingTime").is_selected()} != True) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(Select(driver.find_element(By.NAME,"RpGeneral_SltStartWeek")).first_selected_option.get_attribute("text") == "Last" and Select(driver.find_element(By.NAME,"RpGeneral_SltStartDay")).first_selected_option.get_attribute("text") == "Sunday" and Select(driver.find_element(By.NAME,"RpGeneral_SltStartMonth")).first_selected_option.get_attribute("text") == "December" and Select(driver.find_element(By.NAME,"RpGeneral_SltStartHour")).first_selected_option.get_attribute("text") == "23:00"):
        print(f"             [EMS1-6445][Basic - General Setup - Modify] StartDate pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6445][Basic - General Setup - Modify] StartDate fail",file = open(file_name, '+a'))
        if_temp_error = True
    if(Select(driver.find_element(By.NAME,"RpGeneral_SltEndWeek")).first_selected_option.get_attribute("text") == "First" and Select(driver.find_element(By.NAME,"RpGeneral_SltEndDay")).first_selected_option.get_attribute("text") == "Monday" and Select(driver.find_element(By.NAME,"RpGeneral_SltEndMonth")).first_selected_option.get_attribute("text") == "January" and Select(driver.find_element(By.NAME,"RpGeneral_SltEndHour")).first_selected_option.get_attribute("text") == "0:00"):
        print(f"             [EMS1-6445][Basic - General Setup - Modify] EndDate pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6445][Basic - General Setup - Modify] EndDate fail",file = open(file_name, '+a'))
        if_temp_error = True
    # if(if_temp_error==False):
    #     print(f"             [EMS1-6445][Basic - General Setup - Modify] Result Pass",file = open(file_name, '+a'))
    # else:
    #     print(f"             [EMS1-6445][Basic - General Setup - Modify] Result Fail",file = open(file_name, '+a'))

    # # Basic_General_delete
    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT,"Basic Setting").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"General Setup").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"Basic Setting").click() 
    time.sleep(1)
    e_swi.Basic_General_System(driver,"OLT1404A")
    e_swi.Basic_General_Location(driver," ")
    e_swi.Basic_General_Contact(driver," ")
    e_swi.Basic_General_UseTime(driver,"None")
    e_swi.Basic_General_TimeIP(driver,"0.0.0.0")
    e_swi.Basic_General_TimeZone(driver,"UTC")
    e_swi.Basic_General_Daylight(driver,False)
    e_swi.Basic_General_Apply(driver,file_name)


    # # Basic_General_delete EMS check
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"Basic Setting").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"General Setup").click()
    # if_temp_error = False 
    time.sleep(3)
    if(driver.find_element(By.ID,"basic_generalsetup_hostname_text").get_attribute("value") == "OLT1404A"):
        print(f"             [EMS1-6445][Basic - General Setup - Delete] EMS System (OLT1404A) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - Delete] EMS System ({driver.find_element(By.ID,"basic_generalsetup_hostname_text").get_attribute("value")} != OLT1404A) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(driver.find_element(By.ID,"basic_generalsetup_location_text").get_attribute("value") == " " ):
        print(f"             [EMS1-6445][Basic - General Setup - Delete] EMS Location ( ) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - Delete] EMS Location ({driver.find_element(By.ID,"basic_generalsetup_location_text").get_attribute("value")} !=  ) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(driver.find_element(By.ID,"basic_generalsetup_personname_text").get_attribute("value") == " " ):
        print(f"             [EMS1-6445][Basic - General Setup - Delete] EMS Contact ( ) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - Delete] EMS Contact ({driver.find_element(By.ID,"basic_generalsetup_personname_text").get_attribute("value")} !=  ) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(Select(driver.find_element(By.ID,"basic_generalsetup_timeservertype_select")).first_selected_option.get_attribute("text") == "None" ):
        print(f"             [EMS1-6445][Basic - General Setup - Delete] EMS UseTime (None) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - Delete] EMS UseTime ({Select(driver.find_element(By.ID,"basic_generalsetup_timeservertype_select")).first_selected_option.get_attribute("text")} != None) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(driver.find_element(By.ID,"basic_generalsetup_timeserveripaddress_text").get_attribute("value") == "0.0.0.0" ):
        print(f"             [EMS1-6445][Basic - General Setup - Delete] EMS TimeIP (0.0.0.0) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - Delete] EMS TimeIP ({driver.find_element(By.ID,"basic_generalsetup_timeserveripaddress_text").get_attribute("value")} != 0.0.0.0) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(Select(driver.find_element(By.ID,"basic_generalsetup_timezone_select")).first_selected_option.get_attribute("text") == "UTC" ):
        print(f"             [EMS1-6445][Basic - General Setup - Delete] EMS TimeZone (UTC) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - Delete] EMS TimeZone ({Select(driver.find_element(By.ID,"basic_generalsetup_timezone_select")).first_selected_option.get_attribute("text")} != UTC) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(driver.find_element(By.ID,"basic_generalsetup_daylight_checkbox").is_selected() == False):
        print(f"             [EMS1-6445][Basic - General Setup - Delete] EMS Daylight (False) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - Delete] EMS Daylight ({driver.find_element(By.ID,"basic_generalsetup_daylight_checkbox").is_selected()} != False) fail',file = open(file_name, '+a'))
        if_temp_error = True
    
    #if(if_temp_error==False):
    #    print(f"             [EMS1-6445][Basic - General Setup - Delete] EMS Result pass",file = open(file_name, '+a'))
    #else:
    #    print(f"             [EMS1-6445][Basic - General Setup - Delete] EMS Result fail",file = open(file_name, '+a'))

    # # Basic_General_delete 192.168.196.207 check
    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Basic Setting").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"General Setup").click()
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    time.sleep(3)
    #if_temp_error = False 
    if(driver.find_element(By.NAME,"RpGeneral_IptTextSystemName").get_attribute("value") == "OLT1404A" ):
        print(f"             [EMS1-6445][Basic - General Setup - Delete] System (OLT1404A) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - Delete] System ({driver.find_element(By.NAME,"RpGeneral_IptTextSystemName").get_attribute("value")} != OLT1404A) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(driver.find_element(By.NAME,"RpGeneral_IptTextLocation").get_attribute("value") == " " ):
        print(f"             [EMS1-6445][Basic - General Setup - Delete] Location ( ) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - Delete] Location ({driver.find_element(By.NAME,"RpGeneral_IptTextLocation").get_attribute("value")} !=  ) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(driver.find_element(By.NAME,"RpGeneral_IptTextContact").get_attribute("value") == " " ):
        print(f"             [EMS1-6445][Basic - General Setup - Delete] Contact ( ) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - Delete] Contact ({driver.find_element(By.NAME,"RpGeneral_IptTextContact").get_attribute("value")} !=  ) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(Select(driver.find_element(By.NAME,"RpGeneral_SltTimeProtocol")).first_selected_option.get_attribute("text") == "None" ):
        print(f"             [EMS1-6445][Basic - General Setup - Delete] UseTime (None) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - Delete] UseTime ({Select(driver.find_element(By.NAME,"RpGeneral_SltTimeProtocol")).first_selected_option.get_attribute("text")} != None) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(driver.find_element(By.NAME,"RpGeneral_IptTextTimeSvrIP").get_attribute("value") == "0.0.0.0" ):
        print(f"             [EMS1-6445][Basic - General Setup - Delete] TimeIP (0.0.0.0) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - Delete] TimeIP ({driver.find_element(By.NAME,"RpGeneral_IptTextTimeSvrIP").get_attribute("value")} != 0.0.0.0) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(Select(driver.find_element(By.NAME,"RpGeneral_SltTimeZone")).first_selected_option.get_attribute("text") == "UTC" ):
        print(f"             [EMS1-6445][Basic - General Setup - Delete] TimeZone (UTC) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - Delete] TimeZone ({Select(driver.find_element(By.NAME,"RpGeneral_SltTimeZone")).first_selected_option.get_attribute("text")} != UTC) fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(driver.find_element(By.NAME,"RpGeneral_CheckDaylightSavingTime").is_selected() == False ):
        print(f"             [EMS1-6445][Basic - General Setup - Delete] Daylight (False) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6445][Basic - General Setup - Delete] Daylight ({driver.find_element(By.NAME,"RpGeneral_CheckDaylightSavingTime").is_selected()} != False) fail',file = open(file_name, '+a'))
        if_temp_error = True
   
    # if(if_temp_error==False):
    #     print(f"             [EMS1-6445][Basic - General Setup - Delete] Result Pass",file = open(file_name, '+a'))
    # else:
    #     print(f"             [EMS1-6445][Basic - General Setup - Delete] Result Fail",file = open(file_name, '+a'))
    

    if(if_temp_error==False):
        print(f"             [EMS1-6445][Basic - General Setup] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6445][Basic - General Setup] Result Fail",file = open(file_name, '+a'))

    print(f"======================================================================================",file = open(file_name, '+a'))


@retry()
def Basic_Switch(driver,url,ems_url,file_name):

    # # Switch_setup
    print(f"======================================================================================",file = open(file_name, '+a'))
    print(f"Basic Setting - Switch Setup Test Start",file = open(file_name, '+a'))
    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT,"Basic Setting").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"Switch Setup").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"Basic Setting").click() 
    time.sleep(1)
    e_swi.Basic_Switch_WRED(driver,True)
    e_swi.Basic_Switch_Downstream_Macro(driver,"cir")
    e_swi.Basic_Switch_Downstream_Shaper(driver,"enable")
    e_swi.Basic_Switch_Bridge(driver,True)
    e_swi.Basic_Switch_SmartIsolation(driver,True)
    e_swi.Basic_Switch_AgingTime(driver,"86400")
    e_swi.Basic_Switch_Priority7(driver,"0")
    e_swi.Basic_Switch_Priority6(driver,"1")
    e_swi.Basic_Switch_Priority5(driver,"2")
    e_swi.Basic_Switch_Priority4(driver,"3")
    e_swi.Basic_Switch_Priority3(driver,"4")
    e_swi.Basic_Switch_Priority2(driver,"5")
    e_swi.Basic_Switch_Priority1(driver,"6")
    e_swi.Basic_Switch_Priority0(driver,"7")
    e_swi.Basic_Switch_Apply(driver,file_name)
    time.sleep(1)

    # # switch_setup_EMS_check
    time.sleep(3)
    driver.find_element(By.LINK_TEXT,"Basic Setting").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"Switch Setup").click()
    time.sleep(2)
    if_temp_error = False

    if(driver.find_element(By.ID,"basic_switch_wredactive_checkbox").is_selected() == True ):
        print(f"             [EMS1-6446][Basic - Switch Setup - New] EMS WRED (True) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - New] EMS WRED ({driver.find_element(By.ID,"basic_switch_wredactive_checkbox").is_selected()} != True) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.ID,"basic_switch_downstreammacro_select")).first_selected_option.get_attribute("text") == "cir" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - New] EMS Downstream_Macro (cir) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - New] EMS Downstream_Macro ({Select(driver.find_element(By.ID,"basic_switch_downstreammacro_select")).first_selected_option.get_attribute("text")} != cir) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.ID,"basic_switch_downstreamshaper_select")).first_selected_option.get_attribute("text") == "enable" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - New] EMS Downstream_Shaper (enable) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - New] EMS Downstream_Shaper ({Select(driver.find_element(By.ID,"basic_switch_downstreamshaper_select")).first_selected_option.get_attribute("text")} != enable) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.ID,"basic_switch_bridgeactive_checkbox").is_selected() == True ):
        print(f"             [EMS1-6446][Basic - Switch Setup - New] EMS Bridge (True) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - New] EMS Bridge ({driver.find_element(By.ID,"basic_switch_bridgeactive_checkbox").is_selected()} != True) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.ID,"basic_switch_smartactive_checkbox").is_selected() == True ):
        print(f"             [EMS1-6446][Basic - Switch Setup - New] EMS SmartIsolation (True) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - New] EMS SmartIsolation ({driver.find_element(By.ID,"basic_switch_smartactive_checkbox").is_selected()} != True) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.ID,"basic_switch_agingiime_text").get_attribute("value") == "86400" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - New] EMS AgingTime (86400) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - New] EMS AgingTime ({driver.find_element(By.ID,"basic_switch_agingiime_text").get_attribute("value")} != 86400) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.ID,"basic_switch_priority7_select")).first_selected_option.get_attribute("text") == "0" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - New] EMS Priority7 (0) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - New] EMS Priority7 ({Select(driver.find_element(By.ID,"basic_switch_priority7_select")).first_selected_option.get_attribute("text")} != 0) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.ID,"basic_switch_priority6_select")).first_selected_option.get_attribute("text") == "1" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - New] EMS Priority6 (1) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - New] EMS Priority6 ({Select(driver.find_element(By.ID,"basic_switch_priority6_select")).first_selected_option.get_attribute("text")} != 1) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.ID,"basic_switch_priority5_select")).first_selected_option.get_attribute("text") == "2" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - New] EMS Priority5 (2) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - New] EMS Priority5 ({Select(driver.find_element(By.ID,"basic_switch_priority5_select")).first_selected_option.get_attribute("text")} != 2) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.ID,"basic_switch_priority4_select")).first_selected_option.get_attribute("text") == "3" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - New] EMS Priority4 (3) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - New] EMS Priority4 ({Select(driver.find_element(By.ID,"basic_switch_priority4_select")).first_selected_option.get_attribute("text")} != 3) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.ID,"basic_switch_priority3_select")).first_selected_option.get_attribute("text") == "4" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - New] EMS Priority3 (4) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - New] EMS Priority3 ({Select(driver.find_element(By.ID,"basic_switch_priority3_select")).first_selected_option.get_attribute("text")} != 4) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.ID,"basic_switch_priority2_select")).first_selected_option.get_attribute("text") == "5" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - New] EMS Priority2 (5) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - New] EMS Priority2 ({Select(driver.find_element(By.ID,"basic_switch_priority2_select")).first_selected_option.get_attribute("text")} != 5) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.ID,"basic_switch_priority1_select")).first_selected_option.get_attribute("text") == "6" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - New] EMS Priority1 (6) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - New] EMS Priority1 ({Select(driver.find_element(By.ID,"basic_switch_priority1_select")).first_selected_option.get_attribute("text")} != 6) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.ID,"basic_switch_priority0_select")).first_selected_option.get_attribute("text") == "7" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - New] EMS Priority0 (7) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - New] EMS Priority0 ({Select(driver.find_element(By.ID,"basic_switch_priority0_select")).first_selected_option.get_attribute("text")} != 7) fail',file = open(file_name, '+a'))
        if_temp_error = True

    # if(if_temp_error==False):
    #     print(f"             [EMS1-6446][Basic - Switch Setup - New] EMS Result pass",file = open(file_name, '+a'))
    # else:
    #     print(f"             [EMS1-6446][Basic - Switch Setup - New] EMS Result fail",file = open(file_name, '+a'))

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Basic Setting").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"Switch Setup").click()
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    time.sleep(1)

    # # Basic_Switch_setup 192.168.169.207 Check

    # if_temp_error = False 
    if(driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[2]/td/table[1]/tbody/tr[4]/td[4]/input").is_selected() == True ):
        print(f"             [EMS1-6446][Basic - Switch Setup - New] WRED (True) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - New] WRED ({driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[2]/td/table[1]/tbody/tr[4]/td[4]/input").is_selected()} != True) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rpswitch_SltDsMeterMacroMode")).first_selected_option.get_attribute("text") == "cir" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - New] Downstream_Macro (cir) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - New] Downstream_Macro ({Select(driver.find_element(By.NAME,"rpswitch_SltDsMeterMacroMode")).first_selected_option.get_attribute("text")} != cir) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rpswitch_SltDsMeterShaperMode")).first_selected_option.get_attribute("text") == "enable" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - New] Downstream_Shaper (enable) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - New] Downstream_Shaper ({Select(driver.find_element(By.NAME,"rpswitch_SltDsMeterShaperMode")).first_selected_option.get_attribute("text")} != enable) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpswitch_ChkBPDUCtrlActive").is_selected() == True ):
        print(f"             [EMS1-6446][Basic - Switch Setup - New] Bridge (True) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - New] Bridge ({driver.find_element(By.NAME,"rpswitch_ChkBPDUCtrlActive").is_selected()} != True) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpswitch_ChkSmartIsolationActive").is_selected() == True ):
        print(f"             [EMS1-6446][Basic - Switch Setup - New] SmartIsolation (True) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - New] SmartIsolation ({driver.find_element(By.NAME,"rpswitch_ChkSmartIsolationActive").is_selected()} != True) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpswitch_IptAgingTimer").get_attribute("value") == "86400" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - New] AgingTime (86400) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - New] AgingTime ({driver.find_element(By.NAME,"rpswitch_IptAgingTimer").get_attribute("value")} != 86400) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?1")).first_selected_option.get_attribute("text") == "0" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - New] Priority7 (0) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - New] Priority7 ({Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?1")).first_selected_option.get_attribute("text")} != 0) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?2")).first_selected_option.get_attribute("text") == "1" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - New] Priority6 (1) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - New] Priority6 ({Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?2")).first_selected_option.get_attribute("text")} != 1) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?3")).first_selected_option.get_attribute("text") == "2" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - New] Priority5 (2) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - New] Priority5 ({Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?3")).first_selected_option.get_attribute("text")} != 2) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?4")).first_selected_option.get_attribute("text") == "3" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - New] Priority4 (3) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - New] Priority4 ({Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?4")).first_selected_option.get_attribute("text")} != 3) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?5")).first_selected_option.get_attribute("text") == "4" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - New] Priority3 (4) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - New] Priority3 ({Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?5")).first_selected_option.get_attribute("text")} != 4) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?6")).first_selected_option.get_attribute("text") == "5" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - New] Priority2 (5) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - New] Priority2 ({Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?6")).first_selected_option.get_attribute("text")} != 5) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?7")).first_selected_option.get_attribute("text") == "6" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - New] Priority1 (6) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - New] Priority1 ({Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?7")).first_selected_option.get_attribute("text")} != 6) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?8")).first_selected_option.get_attribute("text") == "7" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - New] Priority0 (7) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - New] Priority0 ({Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?8")).first_selected_option.get_attribute("text")} != 7) fail',file = open(file_name, '+a'))
        if_temp_error = True

    # if(if_temp_error==False):
    #     print(f"             [EMS1-6446][Basic - Switch Setup - New] Result Pass",file = open(file_name, '+a'))
    # else:
    #     print(f"             [EMS1-6446][Basic - Switch Setup - New] Result Fail",file = open(file_name, '+a'))

    # #Basic_Switch_Modify
        
    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT,"Basic Setting").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"Switch Setup").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"Basic Setting").click() 
    time.sleep(1)

    e_swi.Basic_Switch_WRED(driver,False)
    e_swi.Basic_Switch_Downstream_Macro(driver,"pir")
    e_swi.Basic_Switch_Downstream_Shaper(driver,"disable")
    e_swi.Basic_Switch_Bridge(driver,False)
    e_swi.Basic_Switch_SmartIsolation(driver,False)
    e_swi.Basic_Switch_AgingTime(driver,"30")
    e_swi.Basic_Switch_Priority7(driver,"7")
    e_swi.Basic_Switch_Priority6(driver,"7")
    e_swi.Basic_Switch_Priority5(driver,"7")
    e_swi.Basic_Switch_Priority4(driver,"7")
    e_swi.Basic_Switch_Priority3(driver,"7")
    e_swi.Basic_Switch_Priority2(driver,"7")
    e_swi.Basic_Switch_Priority1(driver,"7")
    e_swi.Basic_Switch_Priority0(driver,"7")
    e_swi.Basic_Switch_Apply(driver,file_name)
    time.sleep(1)

    # # switch_Modify_EMS_check
    time.sleep(3)
    driver.find_element(By.LINK_TEXT,"Basic Setting").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"Switch Setup").click()
    # if_temp_error = False
    time.sleep(2)

    if(driver.find_element(By.ID,"basic_switch_wredactive_checkbox").is_selected() == False ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Modify] EMS WRED (False) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Modify] EMS WRED ({driver.find_element(By.ID,"basic_switch_wredactive_checkbox").is_selected()} != False) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.ID,"basic_switch_downstreammacro_select")).first_selected_option.get_attribute("text") == "pir" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Modify] EMS Downstream_Macro (pir) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Modify] EMS Downstream_Macro ({Select(driver.find_element(By.ID,"basic_switch_downstreammacro_select")).first_selected_option.get_attribute("text")} != pir) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.ID,"basic_switch_downstreamshaper_select")).first_selected_option.get_attribute("text") == "disable" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Modify] EMS Downstream_Shaper (disable) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Modify] EMS Downstream_Shaper ({Select(driver.find_element(By.ID,"basic_switch_downstreamshaper_select")).first_selected_option.get_attribute("text")} != disable) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.ID,"basic_switch_bridgeactive_checkbox").is_selected() == False ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Modify] EMS Bridge (False) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Modify] EMS Bridge ({driver.find_element(By.ID,"basic_switch_bridgeactive_checkbox").is_selected()} != False) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.ID,"basic_switch_smartactive_checkbox").is_selected() == False ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Modify] EMS SmartIsolation (False) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Modify] EMS SmartIsolation ({driver.find_element(By.ID,"basic_switch_smartactive_checkbox").is_selected()} != False) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.ID,"basic_switch_agingiime_text").get_attribute("value") == "30" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Modify] EMS AgingTime (30) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Modify] EMS AgingTime ({driver.find_element(By.ID,"basic_switch_agingiime_text").get_attribute("value")} != 30) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.ID,"basic_switch_priority7_select")).first_selected_option.get_attribute("text") == "7" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Modify] EMS Priority7 (7) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Modify] EMS Priority7 ({Select(driver.find_element(By.ID,"basic_switch_priority7_select")).first_selected_option.get_attribute("text")} != 7) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.ID,"basic_switch_priority6_select")).first_selected_option.get_attribute("text") == "7" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Modify] EMS Priority6 (7) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Modify] EMS Priority6 ({Select(driver.find_element(By.ID,"basic_switch_priority6_select")).first_selected_option.get_attribute("text")} != 7) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.ID,"basic_switch_priority5_select")).first_selected_option.get_attribute("text") == "7" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Modify] EMS Priority5 (7) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Modify] EMS Priority5 ({Select(driver.find_element(By.ID,"basic_switch_priority5_select")).first_selected_option.get_attribute("text")} != 7) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.ID,"basic_switch_priority4_select")).first_selected_option.get_attribute("text") == "7" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Modify] EMS Priority4 (7) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Modify] EMS Priority4 ({Select(driver.find_element(By.ID,"basic_switch_priority4_select")).first_selected_option.get_attribute("text")} != 7) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.ID,"basic_switch_priority3_select")).first_selected_option.get_attribute("text") == "7" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Modify] EMS Priority3 (7) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Modify] EMS Priority3 ({Select(driver.find_element(By.ID,"basic_switch_priority3_select")).first_selected_option.get_attribute("text")} != 7) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.ID,"basic_switch_priority2_select")).first_selected_option.get_attribute("text") == "7" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Modify] EMS Priority2 (7) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Modify] EMS Priority2 ({Select(driver.find_element(By.ID,"basic_switch_priority2_select")).first_selected_option.get_attribute("text")} != 7) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.ID,"basic_switch_priority1_select")).first_selected_option.get_attribute("text") == "7" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Modify] EMS Priority1 (7) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Modify] EMS Priority1 ({Select(driver.find_element(By.ID,"basic_switch_priority1_select")).first_selected_option.get_attribute("text")} != 7) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.ID,"basic_switch_priority0_select")).first_selected_option.get_attribute("text") == "7" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Modify] EMS Priority0 (7) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Modify] EMS Priority0 ({Select(driver.find_element(By.ID,"basic_switch_priority0_select")).first_selected_option.get_attribute("text")} != 7) fail',file = open(file_name, '+a'))
        if_temp_error = True

    # if(if_temp_error==False):
    #     print(f"             [EMS1-6446][Basic - Switch Setup - Modify] EMS Result Pass",file = open(file_name, '+a'))
    # else:
    #     print(f"             [EMS1-6446][Basic - Switch Setup - Modify] EMS Result Fail",file = open(file_name, '+a'))

    driver.get(url)
    time.sleep(3)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Basic Setting").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"Switch Setup").click()
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    time.sleep(2)

    # # Basic_Switch_Modify 192.168.169.207 Check

    # if_temp_error = False 
    if(driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[2]/td/table[1]/tbody/tr[4]/td[4]/input").is_selected() == False ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Modify] WRED (False) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Modify] WRED ({driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[2]/td/table[1]/tbody/tr[4]/td[4]/input").is_selected()} != False) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rpswitch_SltDsMeterMacroMode")).first_selected_option.get_attribute("text") == "pir" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Modify] Downstream_Macro (pir) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Modify] Downstream_Macro ({Select(driver.find_element(By.NAME,"rpswitch_SltDsMeterMacroMode")).first_selected_option.get_attribute("text")} != pir) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rpswitch_SltDsMeterShaperMode")).first_selected_option.get_attribute("text") == "disable" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Modify] Downstream_Shaper (disable) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Modify] Downstream_Shaper ({Select(driver.find_element(By.NAME,"rpswitch_SltDsMeterShaperMode")).first_selected_option.get_attribute("text")} != disable) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpswitch_ChkBPDUCtrlActive").is_selected() == False ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Modify] Bridge (False) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Modify] Bridge ({driver.find_element(By.NAME,"rpswitch_ChkBPDUCtrlActive").is_selected()} != False) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpswitch_ChkSmartIsolationActive").is_selected() == False ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Modify] SmartIsolation (False) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Modify] SmartIsolation ({driver.find_element(By.NAME,"rpswitch_ChkSmartIsolationActive").is_selected()} != False) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpswitch_IptAgingTimer").get_attribute("value") == "30" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Modify] AgingTime (30) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Modify] AgingTime ({driver.find_element(By.NAME,"rpswitch_IptAgingTimer").get_attribute("value")} != 30) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?1")).first_selected_option.get_attribute("text") == "7" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Modify] Priority7 (7) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Modify] Priority7 ({Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?1")).first_selected_option.get_attribute("text")} != 7) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?2")).first_selected_option.get_attribute("text") == "7" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Modify] Priority6 (7) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Modify] Priority6 ({Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?2")).first_selected_option.get_attribute("text")} != 7) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?3")).first_selected_option.get_attribute("text") == "7" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Modify] Priority5 (7) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Modify] Priority5 ({Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?3")).first_selected_option.get_attribute("text")} != 7) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?4")).first_selected_option.get_attribute("text") == "7" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Modify] Priority4 (7) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Modify] Priority4 ({Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?4")).first_selected_option.get_attribute("text")} != 7) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?5")).first_selected_option.get_attribute("text") == "7" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Modify] Priority3 (7) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Modify] Priority3 ({Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?5")).first_selected_option.get_attribute("text")} != 7) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?6")).first_selected_option.get_attribute("text") == "7" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Modify] Priority2 (7) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Modify] Priority2 ({Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?6")).first_selected_option.get_attribute("text")} != 7) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?7")).first_selected_option.get_attribute("text") == "7" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Modify] Priority1 (7) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Modify] Priority1 ({Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?7")).first_selected_option.get_attribute("text")} != 7) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?8")).first_selected_option.get_attribute("text") == "7" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Modify] Priority0 (7) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Modify] Priority0 ({Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?8")).first_selected_option.get_attribute("text")} != 7) fail',file = open(file_name, '+a'))
        if_temp_error = True

    # if(if_temp_error==False):
    #     print(f"             [EMS1-6446][Basic - Switch Setup - Modify] Result Pass",file = open(file_name, '+a'))
    # else:
    #     print(f"             [EMS1-6446][Basic - Switch Setup - Modify] Result Fail",file = open(file_name, '+a'))



# #Basic_Switch_Delete
        
    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT,"Basic Setting").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"Switch Setup").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"Basic Setting").click() 
    time.sleep(1)

    e_swi.Basic_Switch_WRED(driver,False)
    e_swi.Basic_Switch_Downstream_Macro(driver,"pir")
    e_swi.Basic_Switch_Downstream_Shaper(driver,"disable")
    e_swi.Basic_Switch_Bridge(driver,False)
    e_swi.Basic_Switch_SmartIsolation(driver,False)
    e_swi.Basic_Switch_AgingTime(driver,"300")
    e_swi.Basic_Switch_Priority7(driver,"7")
    e_swi.Basic_Switch_Priority6(driver,"6")
    e_swi.Basic_Switch_Priority5(driver,"5")
    e_swi.Basic_Switch_Priority4(driver,"4")
    e_swi.Basic_Switch_Priority3(driver,"3")
    e_swi.Basic_Switch_Priority2(driver,"2")
    e_swi.Basic_Switch_Priority1(driver,"1")
    e_swi.Basic_Switch_Priority0(driver,"0")
    e_swi.Basic_Switch_Apply(driver,file_name)
    time.sleep(1)

    # # switch_Delete_EMS_check
    time.sleep(3)
    driver.find_element(By.LINK_TEXT,"Basic Setting").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"Switch Setup").click()
    # if_temp_error = False
    time.sleep(2)

    if(driver.find_element(By.ID,"basic_switch_wredactive_checkbox").is_selected() == False ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Delete] EMS WRED (False) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Delete] EMS WRED ({driver.find_element(By.ID,"basic_switch_wredactive_checkbox").is_selected()} != False) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.ID,"basic_switch_downstreammacro_select")).first_selected_option.get_attribute("text") == "pir" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Delete] EMS Downstream_Macro (pir) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Delete] EMS Downstream_Macro ({Select(driver.find_element(By.ID,"basic_switch_downstreammacro_select")).first_selected_option.get_attribute("text")} != pir) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.ID,"basic_switch_downstreamshaper_select")).first_selected_option.get_attribute("text") == "disable" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Delete] EMS Downstream_Shaper (disable) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Delete] EMS Downstream_Shaper ({Select(driver.find_element(By.ID,"basic_switch_downstreamshaper_select")).first_selected_option.get_attribute("text")} != disable) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.ID,"basic_switch_bridgeactive_checkbox").is_selected() == False ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Delete] EMS Bridge (False) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Delete] EMS Bridge ({driver.find_element(By.ID,"basic_switch_bridgeactive_checkbox").is_selected()} != False) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.ID,"basic_switch_smartactive_checkbox").is_selected() == False ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Delete] EMS SmartIsolation (False) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Delete] EMS SmartIsolation ({driver.find_element(By.ID,"basic_switch_smartactive_checkbox").is_selected()} != False) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.ID,"basic_switch_agingiime_text").get_attribute("value") == "300" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Delete] EMS AgingTime (300) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Delete] EMS AgingTime ({driver.find_element(By.ID,"basic_switch_agingiime_text").get_attribute("value")} != 300) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.ID,"basic_switch_priority7_select")).first_selected_option.get_attribute("text") == "7" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Delete] EMS Priority7 (7) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Delete] EMS Priority7 ({Select(driver.find_element(By.ID,"basic_switch_priority7_select")).first_selected_option.get_attribute("text")} != 7) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.ID,"basic_switch_priority6_select")).first_selected_option.get_attribute("text") == "6" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Delete] EMS Priority6 (6) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Delete] EMS Priority6 ({Select(driver.find_element(By.ID,"basic_switch_priority6_select")).first_selected_option.get_attribute("text")} != 6) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.ID,"basic_switch_priority5_select")).first_selected_option.get_attribute("text") == "5" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Delete] EMS Priority5 (5) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Delete] EMS Priority5 ({Select(driver.find_element(By.ID,"basic_switch_priority5_select")).first_selected_option.get_attribute("text")} != 5) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.ID,"basic_switch_priority4_select")).first_selected_option.get_attribute("text") == "4" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Delete] EMS Priority4 (4) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Delete] EMS Priority4 ({Select(driver.find_element(By.ID,"basic_switch_priority4_select")).first_selected_option.get_attribute("text")} != 4) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.ID,"basic_switch_priority3_select")).first_selected_option.get_attribute("text") == "3" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Delete] EMS Priority3 (3) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Delete] EMS Priority3 ({Select(driver.find_element(By.ID,"basic_switch_priority3_select")).first_selected_option.get_attribute("text")} != 3) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.ID,"basic_switch_priority2_select")).first_selected_option.get_attribute("text") == "2" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Delete] EMS Priority2 (2) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Delete] EMS Priority2 ({Select(driver.find_element(By.ID,"basic_switch_priority2_select")).first_selected_option.get_attribute("text")} != 2) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.ID,"basic_switch_priority1_select")).first_selected_option.get_attribute("text") == "1" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Delete] EMS Priority1 (1) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Delete] EMS Priority1 ({Select(driver.find_element(By.ID,"basic_switch_priority1_select")).first_selected_option.get_attribute("text")} != 1) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.ID,"basic_switch_priority0_select")).first_selected_option.get_attribute("text") == "0" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Delete] EMS Priority0 (0) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Delete] EMS Priority0 ({Select(driver.find_element(By.ID,"basic_switch_priority0_select")).first_selected_option.get_attribute("text")} != 0) fail',file = open(file_name, '+a'))
        if_temp_error = True

    # if(if_temp_error==False):
    #     print(f"             [EMS1-6446][Basic - Switch Setup - Delete] EMS Result Pass",file = open(file_name, '+a'))
    # else:
    #     print(f"             [EMS1-6446][Basic - Switch Setup - Delete] EMS Result Fail",file = open(file_name, '+a'))

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Basic Setting").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"Switch Setup").click()
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    time.sleep(1)

    # # Basic_Switch_Delete 192.168.169.207 Check
                                        
    # if_temp_error = False              
    if(driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[2]/td/table[1]/tbody/tr[4]/td[4]/input").is_selected() == False ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Delete] WRED (False) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Delete] WRED ({driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[2]/td/table[1]/tbody/tr[4]/td[4]/input").is_selected()} != False) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rpswitch_SltDsMeterMacroMode")).first_selected_option.get_attribute("text") == "pir" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Delete] Downstream_Macro (pir) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Delete] Downstream_Macro ({Select(driver.find_element(By.NAME,"rpswitch_SltDsMeterMacroMode")).first_selected_option.get_attribute("text")} != pir) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rpswitch_SltDsMeterShaperMode")).first_selected_option.get_attribute("text") == "disable" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Delete] Downstream_Shaper (disable) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Delete] Downstream_Shaper ({Select(driver.find_element(By.NAME,"rpswitch_SltDsMeterShaperMode")).first_selected_option.get_attribute("text")} != disable) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpswitch_ChkBPDUCtrlActive").is_selected() == False ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Delete] Bridge (False) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Delete] Bridge ({driver.find_element(By.NAME,"rpswitch_ChkBPDUCtrlActive").is_selected()} != False) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpswitch_ChkSmartIsolationActive").is_selected() == False ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Delete] SmartIsolation (False) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Delete] SmartIsolation ({driver.find_element(By.NAME,"rpswitch_ChkSmartIsolationActive").is_selected()} != False) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpswitch_IptAgingTimer").get_attribute("value") == "300" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Delete] AgingTime (300) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Delete] AgingTime ({driver.find_element(By.NAME,"rpswitch_IptAgingTimer").get_attribute("value")} != 300) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?1")).first_selected_option.get_attribute("text") == "7" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Delete] Priority7 (7) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Delete] Priority7 ({Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?1")).first_selected_option.get_attribute("text")} != 7) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?2")).first_selected_option.get_attribute("text") == "6" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Delete] Priority6 (6) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Delete] Priority6 ({Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?2")).first_selected_option.get_attribute("text")} != 6) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?3")).first_selected_option.get_attribute("text") == "5" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Delete] Priority5 (5) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Delete] Priority5 ({Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?3")).first_selected_option.get_attribute("text")} != 5) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?4")).first_selected_option.get_attribute("text") == "4" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Delete] Priority4 (4) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Delete] Priority4 ({Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?4")).first_selected_option.get_attribute("text")} != 4) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?5")).first_selected_option.get_attribute("text") == "3" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Delete] Priority3 (3) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Delete] Priority3 ({Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?5")).first_selected_option.get_attribute("text")} != 3) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?6")).first_selected_option.get_attribute("text") == "2" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Delete] Priority2 (2) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Delete] Priority2 ({Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?6")).first_selected_option.get_attribute("text")} != 2) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?7")).first_selected_option.get_attribute("text") == "1" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Delete] Priority1 (1) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Delete] Priority1 ({Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?7")).first_selected_option.get_attribute("text")} != 1) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?8")).first_selected_option.get_attribute("text") == "0" ):
        print(f"             [EMS1-6446][Basic - Switch Setup - Delete] Priority0 (0) pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6446][Basic - Switch Setup - Delete] Priority0 ({Select(driver.find_element(By.NAME,"rpswitch_SltQueuePri?8")).first_selected_option.get_attribute("text")} != 0) fail',file = open(file_name, '+a'))
        if_temp_error = True

    # if(if_temp_error==False):
    #     print(f"             [EMS1-6446][Basic - Switch Setup - Delete] Result Pass",file = open(file_name, '+a'))
    # else:
    #     print(f"             [EMS1-6446][Basic - Switch Setup - Delete] Result Fail",file = open(file_name, '+a'))


    if(if_temp_error==False):
        print(f"             [EMS1-6446][Basic - Switch Setup] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6446][Basic - Switch Setup] Result Fail",file = open(file_name, '+a'))

    print(f"======================================================================================",file = open(file_name, '+a'))

@retry()
def Basic_IP(driver,url,ems_url,file_name):
    #[EMS1-6447][Basic - IP Setup - Apply] Result
    #[EMS1-6513][Basic - IP Setup - Interface - New] Result 
    print(f"======================================================================================",file = open(file_name, '+a'))
    print(f"Basic Setting - IP Setup Test Start",file = open(file_name, '+a'))

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)   
    driver.find_element(By.LINK_TEXT, "VLAN").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)
    driver.find_element(By.ID,"advance_vlan_static_profile_new_btn").click()
    time.sleep(1)
    e_swi.VLAN_Static_VLAN(driver,True,"Name_Test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx64","100","Forbidden","UnTagging",file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Basic Setting").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "IP Setup").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Basic Setting").click() 
    time.sleep(1)
    driver.find_element(By.ID,"basic_ipinterface_profile_new_btn").click()
    time.sleep(1)
    e_swi.Basic_IP_Interface(driver,"10.10.10.1","255.255.255.0","100",file_name)
    driver.find_element(By.ID,"basic_ipinterface_profile_new_btn").click()
    e_swi.Basic_IP_Interface(driver,"10.10.11.1","255.255.255.0","100",file_name)
    e_swi.Management_IP_Address(driver,"192.168.0.10","255.255.255.0","0.0.0.0",file_name)

    #[EMS1-6447][Basic - IP Setup - Apply] Result check
    #[EMS1-6513][Basic - IP Setup - Interface - New] Result check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Basic Setting").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"IP Setup").click()
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    time.sleep(1)
    if_temp_error = False
    if_find =False
    for i in range(1,driver.find_elements(By.NAME,"rpip_ChkDel").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td[2]/table[4]/tbody/tr[{i*2}]/td[5]/div").text
        if(ele == '100'):
            if_find = True
            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td[2]/table[4]/tbody/tr[{i*2}]/td[4]/div").text != '255.255.255.0' ):
                if_temp_error = True 
            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td[2]/table[4]/tbody/tr[{i*2}]/td[3]/div").text != '10.10.10.1' and  driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td[2]/table[4]/tbody/tr[{i*2}]/td[3]/div").text != '10.10.11.1'):
                if_temp_error = True 
    if(if_temp_error==False and if_find==True):
        print(f"             [EMS1-6513][Basic - IP Setup - Interface - New] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6513][Basic - IP Setup - Interface - New] Result Fail",file = open(file_name, '+a'))
    if_temp_error = False  
    if(driver.find_element(By.NAME,f"rpip_IptOutBandIPAddr").get_attribute("value") == '192.168.0.10'):
        print(f"             [EMS1-6447][Basic - IP Setup - Apply] IP_Address (192.168.0.10) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6447][Basic - IP Setup - Apply] IP_Address ({driver.find_element(By.NAME,f"rpip_IptOutBandIPAddr").text} != 255.255.255.0) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(driver.find_element(By.NAME,f"rpip_IptOutBandSubnetMask").get_attribute("value") == '255.255.255.0'):
        print(f"             [EMS1-6447][Basic - IP Setup - Apply] IP_Address (255.255.255.0) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6447][Basic - IP Setup - Apply] IP_Address ({driver.find_element(By.NAME,f"rpip_IptOutBandSubnetMask").text} != 192.168.0.10) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(driver.find_element(By.NAME,f"rpip_IptOutBandDefaultGateway").get_attribute("value") == '0.0.0.0'):
        print(f"             [EMS1-6447][Basic - IP Setup - Apply] IP_Address (0.0.0.0) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6447][Basic - IP Setup - Apply] IP_Address ({driver.find_element(By.NAME,f"rpip_IptOutBandDefaultGateway").text} != 0.0.0.0) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    
    if(if_temp_error == False):
        print(f"             [EMS1-6447][Basic - IP Setup - Apply] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6447][Basic - IP Setup - Apply] Result Fail",file = open(file_name, '+a'))


    #[EMS1-6514][Basic - IP Setup - Interface - Delete] Result
    
    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Basic Setting").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "IP Setup").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Basic Setting").click() 
    time.sleep(1)
    e_swi.Management_IP_Address(driver,"192.168.0.1","255.255.255.0","0.0.0.0",file_name)
    if_find = False
    for i in range(1,int(driver.find_element(By.ID,"pageTotal").text)+1):
        for j in range(1,driver.find_elements(By.NAME,"basic_ipinterface_profile_checkbox").__len__()+1):
            ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[7]/div[1]/div[{j}]/div[4]").text
            if(ele == '100'):
                driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[7]/div[1]/div[{j}]/div[5]/label").click()
                if_find =True
                time.sleep(1)
        driver.find_element(By.ID,"btnNextPage").click()
    driver.find_element(By.ID,"basic_ipinterface_profile_del_btn").click()
    
    #[EMS1-6514][Basic - IP Setup - Interface - Delete] Result check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Basic Setting").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"IP Setup").click()
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    time.sleep(1)
    for i in range(1,driver.find_elements(By.NAME,"rpip_ChkDel").__len__()+1):
        if_temp_error = False
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td[2]/table[4]/tbody/tr[{i*2}]/td[5]/div").text
        if(ele == "100"):
            if_temp_error=True

    if(if_temp_error==False and if_find == True):
        print(f"             [EMS1-6514][Basic - IP Setup - Interface - Delete] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6514][Basic - IP Setup - Interface - Delete] Result Fail",file = open(file_name, '+a'))

    #[EMS1-6515][Basic - IP Setup - Interface - Page Switch] Result

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Basic Setting").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "IP Setup").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Basic Setting").click() 
    time.sleep(1)
    for i in range(1,12):
        driver.find_element(By.ID,"basic_ipinterface_profile_new_btn").click()
        time.sleep(1)
        e_swi.Basic_IP_Interface(driver,f"10.10.{i}.1","255.255.255.0","100",file_name)
    driver.find_element(By.ID,'btnNextPage').click()
    time.sleep(1)
    if(driver.find_element(By.XPATH,'//*[@id="sys_route_profile_table"]/div[2]/div[1]').text == "11"):
        print(f"             [EMS1-6515][Basic - IP Setup - Interface - Page Switch] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6515][Basic - IP Setup - Interface - Page Switch] Result Fail",file = open(file_name, '+a'))
    for i in range(1,3):
        for i in range(1,driver.find_elements(By.NAME,"basic_ipinterface_profile_checkbox").__len__()+1):
            ele = driver.find_element(By.XPATH,f'//*[@id="sys_route_profile_table"]/div[{i}]/div[4]').text
            if(ele == '100'):
                driver.find_element(By.XPATH,f'//*[@id="sys_route_profile_table"]/div[{i}]/div[5]/label').click()
        driver.find_element(By.ID,"basic_ipinterface_profile_del_btn").click()
        time.sleep(1)
        msg = e_swi.alert_accept_text(driver)
        try:
            e_pro.Close(driver)
        except:
            pass

    print(f"======================================================================================",file = open(file_name, '+a'))

@retry()
def Basic_Port(driver,url,ems_url,username,password,url_ip,file_name,Pon_Name,Eth_Name,Pon_Name_L,Eth_Name_L):
    print(f"======================================================================================",file = open(file_name, '+a'))
    print(f"Basic Setting - Port Setup Test Start",file = open(file_name, '+a'))
    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Basic Setting").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Port Setup").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Basic Setting").click()
    time.sleep(1)
    # # Basic_Port_set
    e_swi.Basic_Portset(driver,Eth_Name,True,"O _ O->UP","Auto","7","Network","set",file_name)
    e_swi.Basic_Portset(driver,Pon_Name,True,"O _ O->DW","2500M / Full Duplex","7","Network","set",file_name)

    # # Basic_Port_set 192.168.169.207 check

    driver.get(url)
    time.sleep(2)
    try:
        mod.Switch_Default(driver)
        mod.Switch_Specific_Frame(driver,3)
        driver.find_element(By.LINK_TEXT,"Basic Setting").click()
    except:
        driver.get(f"http://{username}:{password}@{url_ip}")
        time.sleep(2)
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
        driver.find_element(By.NAME,"RpAccessSv_IptHttpTimeout").clear()
        driver.find_element(By.NAME,"RpAccessSv_IptHttpTimeout").send_keys('255')
        driver.find_element(By.NAME,'RpAccessSv_BtnApply').click()
        time.sleep(2)
        mod.Switch_Default(driver)
        mod.Switch_Specific_Frame(driver,3)
        driver.find_element(By.LINK_TEXT,"Basic Setting").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"Port Setup").click()
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    time.sleep(1)
    if_temp_error = False
    print(f"--------------------------------------------------------------------------------------",file = open(file_name, '+a'))
    for i in range(1,driver.find_elements(By.NAME,"rpport_ChkPortActive").__len__()+1):
        if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[2]/div").text == Eth_Name_L):

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[3]/div/input").is_selected() == True ):
                print(f"             [EMS1-6448][Basic - Port Setup - New] {Eth_Name} Active (True) pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6448][Basic - Port Setup - New] {Eth_Name} Active ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[3]/div/input").is_selected()} != True) fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[4]/div/input").get_attribute("value") == "O _ O->UP" ):
                print(f"             [EMS1-6448][Basic - Port Setup - New] {Eth_Name} Name (O _ O->UP) pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6448][Basic - Port Setup - New] {Eth_Name} Name ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[4]/div/input").get_attribute("value")} != O _ O->UP) fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[6]/div/select")).first_selected_option.get_attribute("text") == "Auto" ):
                print(f"             [EMS1-6448][Basic - Port Setup - New] {Eth_Name} speed (Auto) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6448][Basic - Port Setup - New] {Eth_Name} speed ({Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[6]/div/select")).first_selected_option.get_attribute("text")} != Auto) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[7]/div/select")).first_selected_option.get_attribute("text") == "7" ):
                print(f"             [EMS1-6448][Basic - Port Setup - New] {Eth_Name} priority (7) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6448][Basic - Port Setup - New] {Eth_Name} priority ({Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[7]/div/select")).first_selected_option.get_attribute("text")} != 7) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[8]/div/select")).first_selected_option.get_attribute("text") == "Network" ):
                print(f"             [EMS1-6448][Basic - Port Setup - New] {Eth_Name} Control (Network) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6448][Basic - Port Setup - New] {Eth_Name} Control ({Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[8]/div/select")).first_selected_option.get_attribute("text")} != Network) Fail',file = open(file_name, '+a'))
                if_temp_error = True

        if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[2]/div").text == Pon_Name_L):

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[3]/div/input").is_selected() == True ):
                print(f"             [EMS1-6448][Basic - Port Setup - New] {Pon_Name} Active (True) pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6448][Basic - Port Setup - New] {Pon_Name} Active ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[3]/div/input").is_selected()} != True) fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[4]/div/input").get_attribute("value") == "O _ O->DW" ):
                print(f"             [EMS1-6448][Basic - Port Setup - New] {Pon_Name} Name (O _ O->DW) pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6448][Basic - Port Setup - New] {Pon_Name} Name ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[4]/div/input").get_attribute("value")} != O _ O->DW) fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[6]/div/select")).first_selected_option.get_attribute("text") == "2500M / Full Duplex" ):
                print(f"             [EMS1-6448][Basic - Port Setup - New] {Pon_Name} speed (2500M / Full Duplex) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6448][Basic - Port Setup - New] {Pon_Name} speed ({Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[6]/div/select")).first_selected_option.get_attribute("text")} != 2500M / Full Duplex) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[7]/div/select")).first_selected_option.get_attribute("text") == "7" ):
                print(f"             [EMS1-6448][Basic - Port Setup - New] {Pon_Name} priority (7) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6448][Basic - Port Setup - New] {Pon_Name} priority ({Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[7]/div/select")).first_selected_option.get_attribute("text")} != 7) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[8]/div/select")).first_selected_option.get_attribute("text") == "Network" ):
                print(f"             [EMS1-6448][Basic - Port Setup - New] {Pon_Name} Control (Network) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6448][Basic - Port Setup - New] {Pon_Name} Control ({Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[8]/div/select")).first_selected_option.get_attribute("text")} != Network) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            
    # if(if_temp_error==False):
    #     print(f"             [EMS1-6448][Basic - Port Setup] Result Pass",file = open(file_name, '+a'))
    # else:
    #     print(f"             [EMS1-6448][Basic - Port Setup] Result Fail",file = open(file_name, '+a'))

    # # Basic_Port_modify
        
    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT,"Basic Setting").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"Port Setup").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"Basic Setting").click() 
    time.sleep(1)
    e_swi.Basic_Portset(driver,Eth_Name,True,"O _ m->UP","Auto","1","Tunnel","Modify",file_name)
    e_swi.Basic_Portset(driver,Pon_Name,True,"O _ m->DW","2500M / Full Duplex","1","Tunnel","Modify",file_name)

    # # Basic_Port_modify 192.168.169.207 check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Basic Setting").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"Port Setup").click()
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    time.sleep(1)

    # if_temp_error = False
    print(f"--------------------------------------------------------------------------------------",file = open(file_name, '+a'))
    for i in range(1,driver.find_elements(By.NAME,"rpport_ChkPortActive").__len__()+1):
        if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[2]/div").text == Eth_Name_L):

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[3]/div/input").is_selected() == True ):
                print(f"             [EMS1-6448][Basic - Port Setup - Modify] {Eth_Name} Active (True) pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6448][Basic - Port Setup - Modify] {Eth_Name} Active ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[3]/div/input").is_selected()} != True) fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[4]/div/input").get_attribute("value") == "O _ m->UP" ):
                print(f"             [EMS1-6448][Basic - Port Setup - Modify] {Eth_Name} Name (O _ m->UP) pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6448][Basic - Port Setup - Modify] {Eth_Name} Name ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[4]/div/input").get_attribute("value")} != O _ m->UP) fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[6]/div/select")).first_selected_option.get_attribute("text") == "Auto" ):
                print(f"             [EMS1-6448][Basic - Port Setup - Modify] {Eth_Name} speed (Auto) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6448][Basic - Port Setup - Modify] {Eth_Name} speed ({Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[6]/div/select")).first_selected_option.get_attribute("text")} != Auto) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[7]/div/select")).first_selected_option.get_attribute("text") == "1" ):
                print(f"             [EMS1-6448][Basic - Port Setup - Modify] {Eth_Name} priority (1) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6448][Basic - Port Setup - Modify] {Eth_Name} priority ({Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[7]/div/select")).first_selected_option.get_attribute("text")} != 1) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[8]/div/select")).first_selected_option.get_attribute("text") == "Tunnel" ):
                print(f"             [EMS1-6448][Basic - Port Setup - Modify] {Eth_Name} Control (Tunnel) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6448][Basic - Port Setup - Modify] {Eth_Name} Control ({Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[8]/div/select")).first_selected_option.get_attribute("text")} != Tunnel) Fail',file = open(file_name, '+a'))
                if_temp_error = True

        if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[2]/div").text == Pon_Name_L):

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[3]/div/input").is_selected() == True ):
                print(f"             [EMS1-6448][Basic - Port Setup - Modify] {Pon_Name} Active (True) pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6448][Basic - Port Setup - Modify] {Pon_Name} Active ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[3]/div/input").is_selected()} != True) fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[4]/div/input").get_attribute("value") == "O _ m->DW" ):
                print(f"             [EMS1-6448][Basic - Port Setup - Modify] {Pon_Name} Name (O _ m->DW) pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6448][Basic - Port Setup - Modify] {Pon_Name} Name ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[4]/div/input").get_attribute("value")} != O _ m->DW) fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[6]/div/select")).first_selected_option.get_attribute("text") == "2500M / Full Duplex" ):
                print(f"             [EMS1-6448][Basic - Port Setup - Modify] {Pon_Name} speed (2500M / Full Duplex) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6448][Basic - Port Setup - Modify] {Pon_Name} speed ({Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[6]/div/select")).first_selected_option.get_attribute("text")} != 2500M / Full Duplex) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[7]/div/select")).first_selected_option.get_attribute("text") == "1" ):
                print(f"             [EMS1-6448][Basic - Port Setup - Modify] {Pon_Name} priority (1) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6448][Basic - Port Setup - Modify] {Pon_Name} priority ({Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[7]/div/select")).first_selected_option.get_attribute("text")} != 1) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[8]/div/select")).first_selected_option.get_attribute("text") == "Tunnel" ):
                print(f"             [EMS1-6448][Basic - Port Setup - Modify] {Pon_Name} Control (Tunnel) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6448][Basic - Port Setup - Modify] {Pon_Name} Control ({Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[8]/div/select")).first_selected_option.get_attribute("text")} != Tunnel) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            
    # if(if_temp_error==False):
    #     print(f"             [EMS1-6448][Basic - Port Setup - Modify] Result Pass",file = open(file_name, '+a'))
    # else:
    #     print(f"             [EMS1-6448][Basic - Port Setup - Modify] Result Fail",file = open(file_name, '+a'))

    # # Basic_Port_delete
        
    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT,"Basic Setting").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"Port Setup").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"Basic Setting").click() 
    time.sleep(1)
    e_swi.Basic_Portset(driver,Eth_Name,True," ","Auto","0","Peer","Delete",file_name)
    e_swi.Basic_Portset(driver,Pon_Name,True," ","2500M / Full Duplex","0","Peer","Delete",file_name)

    # # Basic_Port_delete 192.168.169.207 check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Basic Setting").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"Port Setup").click()
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    time.sleep(1)

    # if_temp_error = False
    print(f"--------------------------------------------------------------------------------------",file = open(file_name, '+a'))
    for i in range(1,driver.find_elements(By.NAME,"rpport_ChkPortActive").__len__()+1):
        if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[2]/div").text == Eth_Name_L):

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[3]/div/input").is_selected() == True ):
                print(f"             [EMS1-6448][Basic - Port Setup - Delete] {Eth_Name} Active (True) pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6448][Basic - Port Setup - Delete] {Eth_Name} Active ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[3]/div/input").is_selected()} != True) fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[4]/div/input").get_attribute("value") == " " ):
                print(f"             [EMS1-6448][Basic - Port Setup - Delete] {Eth_Name} Name ( ) pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6448][Basic - Port Setup - Delete] {Eth_Name} Name ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[4]/div/input").get_attribute("value")} !=  ) fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[6]/div/select")).first_selected_option.get_attribute("text") == "Auto" ):
                print(f"             [EMS1-6448][Basic - Port Setup - Delete] {Eth_Name} speed (Auto) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6448][Basic - Port Setup - Delete] {Eth_Name} speed ({Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[6]/div/select")).first_selected_option.get_attribute("text")} != Auto) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[7]/div/select")).first_selected_option.get_attribute("text") == "0" ):
                print(f"             [EMS1-6448][Basic - Port Setup - Delete] {Eth_Name} priority (0) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6448][Basic - Port Setup - Delete] {Eth_Name} priority ({Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[7]/div/select")).first_selected_option.get_attribute("text")} != 0) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[8]/div/select")).first_selected_option.get_attribute("text") == "Peer" ):
                print(f"             [EMS1-6448][Basic - Port Setup - Delete] {Eth_Name} Control (Peer) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6448][Basic - Port Setup - Delete] {Eth_Name} Control ({Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[8]/div/select")).first_selected_option.get_attribute("text")} != Peer) Fail',file = open(file_name, '+a'))
                if_temp_error = True

        if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[2]/div").text == Pon_Name_L):

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[3]/div/input").is_selected() == True ):
                print(f"             [EMS1-6448][Basic - Port Setup - Delete] {Pon_Name} Active (True) pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6448][Basic - Port Setup - Delete] {Pon_Name} Active ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[3]/div/input").is_selected()} != True) fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[4]/div/input").get_attribute("value") == " " ):
                print(f"             [EMS1-6448][Basic - Port Setup - Delete] {Pon_Name} Name ( ) pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6448][Basic - Port Setup - Delete] {Pon_Name} Name ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[4]/div/input").get_attribute("value")} !=  ) fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[6]/div/select")).first_selected_option.get_attribute("text") == "2500M / Full Duplex" ):
                print(f"             [EMS1-6448][Basic - Port Setup - Delete] {Pon_Name} speed (2500M / Full Duplex) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6448][Basic - Port Setup - Delete] {Pon_Name} speed ({Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[6]/div/select")).first_selected_option.get_attribute("text")} != 2500M / Full Duplex) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[7]/div/select")).first_selected_option.get_attribute("text") == "0" ):
                print(f"             [EMS1-6448][Basic - Port Setup - Delete] {Pon_Name} priority (0) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6448][Basic - Port Setup - Delete] {Pon_Name} priority ({Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[7]/div/select")).first_selected_option.get_attribute("text")} != 0) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[8]/div/select")).first_selected_option.get_attribute("text") == "Peer" ):
                print(f"             [EMS1-6448][Basic - Port Setup - Delete] {Pon_Name} Control (Peer) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6448][Basic - Port Setup - Delete] {Pon_Name} Control ({Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[{(i+1)*2}]/td[8]/div/select")).first_selected_option.get_attribute("text")} != Peer) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            
    if(if_temp_error==False):
        print(f"             [EMS1-6448][Basic - Port Setup] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6448][Basic - Port Setup] Result Fail",file = open(file_name, '+a'))

    print(f"======================================================================================",file = open(file_name, '+a'))

@retry()
def IP_Static(driver,url,ems_url,file_name):

    #[EMS1-6450][IP - Static Route - New] Result
    print(f"======================================================================================",file = open(file_name, '+a'))
    print(f"IP Application - Static Route Test Start",file = open(file_name, '+a'))

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "VLAN").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)
    driver.find_element(By.ID,"advance_vlan_static_profile_new_btn").click()
    time.sleep(1)
    e_swi.VLAN_Static_VLAN(driver,True,"Name_Test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx64","100","Forbidden","UnTagging",file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Basic Setting").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "IP Setup").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Basic Setting").click() 
    time.sleep(1)
    driver.find_element(By.ID,"basic_ipinterface_profile_new_btn").click()
    time.sleep(1)
    e_swi.Basic_IP_Interface(driver,"10.10.10.1","255.255.255.0","100",file_name)
    driver.find_element(By.ID,"basic_ipinterface_profile_new_btn").click()
    time.sleep(1)
    e_swi.Basic_IP_Interface(driver,"10.10.11.1","255.255.255.0","100",file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "IP Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Static Route").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "IP Application").click()
    time.sleep(1)
    driver.find_element(By.ID,"ip_iproute_profile_new_btn").click()
    e_swi.IP_Static_Route(driver,True,"Name_Testx","10.10.11.1","255.255.0.0","10.10.10.1","15",file_name)

    # 192.168.169.207 New_check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"IP Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"Static Routing").click()
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    time.sleep(1)
    if_find=False
    for i in range(1,driver.find_elements(By.NAME,"rpsroute_ChkTabDelete").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[{i+2}]/td[4]/div").text
        if(ele == 'Name_Testx'):
            if_find=True
            driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[{i+2}]/td[2]/div/a").click()
            time.sleep(1)
        if_temp_error = False
        if(driver.find_element(By.NAME,"rpsroute_ChkSwActive").is_selected() == True ):
            print(f"             [EMS1-6450][IP - Static Route - New] Active (True) Pass",file = open(file_name, '+a'))
        else:
            print(f'             [EMS1-6450][IP - Static Route - New] Active ({driver.find_element(By.NAME,"rpsroute_ChkSwActive").is_selected()} != True) Fail',file = open(file_name, '+a'))
            if_temp_error = True

        if(driver.find_element(By.NAME,"rpsroute_IptTextSwName").get_attribute("value") == "Name_Testx" ):
            print(f"             [EMS1-6450][IP - Static Route - New] Name (Name_Testx) Pass",file = open(file_name, '+a'))
        else:
            print(f'             [EMS1-6450][IP - Static Route - New] Name ({driver.find_element(By.NAME,"rpsroute_IptTextSwName").get_attribute("value")} != Name_Testx) Fail',file = open(file_name, '+a'))
            if_temp_error = True

        if(driver.find_element(By.NAME,"rpsroute_IptTextSwDestIPAddr").get_attribute("value") == "10.10.11.1" ):
            print(f"             [EMS1-6450][IP - Static Route - New] Destination_IP (10.10.11.1) Pass",file = open(file_name, '+a'))
        else:
            print(f'             [EMS1-6450][IP - Static Route - New] Destination_IP ({driver.find_element(By.NAME,"rpsroute_IptTextSwDestIPAddr").get_attribute("value")} != 10.10.11.1) Fail',file = open(file_name, '+a'))
            if_temp_error = True

        if(driver.find_element(By.NAME,"rpsroute_IptTextSwIPSubnet").get_attribute("value") == "255.255.0.0" ):
            print(f"             [EMS1-6450][IP - Static Route - New] IP_Subnet (255.255.0.0) Pass",file = open(file_name, '+a'))
        else:
            print(f'             [EMS1-6450][IP - Static Route - New] IP_Subnet ({driver.find_element(By.NAME,"rpsroute_IptTextSwIPSubnet").get_attribute("value")} != 255.255.0.0) Fail',file = open(file_name, '+a'))
            if_temp_error = True
            
        if(driver.find_element(By.NAME,"rpsroute_IptTextSwGatewayIP").get_attribute("value") == "10.10.10.1" ):
            print(f"             [EMS1-6450][IP - Static Route - New] Gateway_IP (10.10.10.1) Pass",file = open(file_name, '+a'))
        else:
            print(f'             [EMS1-6450][IP - Static Route - New] Gateway_IP ({driver.find_element(By.NAME,"rpsroute_IptTextSwGatewayIP").get_attribute("value")} != 10.10.10.1) Fail',file = open(file_name, '+a'))
            if_temp_error = True

        if(driver.find_element(By.NAME,"rpsroute_IptTextSwMetric").get_attribute("value") == "15" ):
            print(f"             [EMS1-6450][IP - Static Route - New] Metric (15) Pass",file = open(file_name, '+a'))
        else:
            print(f'             [EMS1-6450][IP - Static Route - New] Metric ({driver.find_element(By.NAME,"rpsroute_IptTextSwMetric").get_attribute("value")} != 15) Fail',file = open(file_name, '+a'))
            if_temp_error = True

        if(if_temp_error==False):
            print(f"             [EMS1-6450][IP - Static Route - New] Result Pass",file = open(file_name, '+a'))
        else:
            print(f'             [EMS1-6450][IP - Static Route - New] Result Fail',file = open(file_name, '+a'))
    if(if_find==False):
        print(f"             [EMS1-6450][IP - Static Route - New] Result Fail",file = open(file_name, '+a'))

    #192.168.169.207 modify
    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "IP Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Static Route").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "IP Application").click()
    time.sleep(1)
    if_find=False
    for i in range(1,driver.find_elements(By.NAME,"ip_iproute_profile_checkbox").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[3]/div[1]/div[{i}]/div[3]").text
        if(ele == 'Name_Testx'):
            if_find=True
            driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[3]/div[1]/div[{i}]/div[8]/label").click()
            time.sleep(1)
            driver.find_element(By.ID,"ip_iproute_profile_mod_btn").click()
            e_swi.IP_Static_Route(driver,True,"Name_Testm","10.10.11.1","255.255.0.0","10.10.10.1","15",file_name)

    #192.168.169.207 modify_check
        
    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"IP Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"Static Routing").click()
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    time.sleep(1)
    for i in range(1,driver.find_elements(By.NAME,"rpsroute_ChkTabDelete").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[{i+2}]/td[4]/div").text
        if(ele == 'Name_Testm'):
            driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[{i+2}]/td[2]/div/a").click()
            time.sleep(1)
        if_temp_error = False
        if(driver.find_element(By.NAME,"rpsroute_ChkSwActive").is_selected() == True ):
            print(f"             [EMS1-6517][IP - Static Route - Modify] Active (True) Pass",file = open(file_name, '+a'))
        else:
            print(f'             [EMS1-6517][IP - Static Route - Modify] Active ({driver.find_element(By.NAME,"rpsroute_ChkSwActive").is_selected()} != True) Fail',file = open(file_name, '+a'))
            if_temp_error = True

        if(driver.find_element(By.NAME,"rpsroute_IptTextSwName").get_attribute("value") == "Name_Testm" ):
            print(f"             [EMS1-6517][IP - Static Route - Modify] Name (Name_Testm) Pass",file = open(file_name, '+a'))
        else:
            print(f'             [EMS1-6517][IP - Static Route - Modify] Name ({driver.find_element(By.NAME,"rpsroute_IptTextSwName").get_attribute("value")} != Name_Testm) Fail',file = open(file_name, '+a'))
            if_temp_error = True

        if(driver.find_element(By.NAME,"rpsroute_IptTextSwDestIPAddr").get_attribute("value") == "10.10.11.1" ):
            print(f"             [EMS1-6517][IP - Static Route - Modify] Destination_IP (10.10.11.1) Pass",file = open(file_name, '+a'))
        else:
            print(f'             [EMS1-6517][IP - Static Route - Modify] Destination_IP ({driver.find_element(By.NAME,"rpsroute_IptTextSwDestIPAddr").get_attribute("value")} != 10.10.11.1) Fail',file = open(file_name, '+a'))
            if_temp_error = True

        if(driver.find_element(By.NAME,"rpsroute_IptTextSwIPSubnet").get_attribute("value") == "255.255.0.0" ):
            print(f"             [EMS1-6517][IP - Static Route - Modify] IP_Subnet (255.255.0.0) Pass",file = open(file_name, '+a'))
        else:
            print(f'             [EMS1-6517][IP - Static Route - Modify] IP_Subnet ({driver.find_element(By.NAME,"rpsroute_IptTextSwIPSubnet").get_attribute("value")} != 255.255.0.0) Fail',file = open(file_name, '+a'))
            if_temp_error = True
            
        if(driver.find_element(By.NAME,"rpsroute_IptTextSwGatewayIP").get_attribute("value") == "10.10.10.1" ):
            print(f"             [EMS1-6517][IP - Static Route - Modify] Gateway_IP (10.10.10.1) Pass",file = open(file_name, '+a'))
        else:
            print(f'             [EMS1-6517][IP - Static Route - Modify] Gateway_IP ({driver.find_element(By.NAME,"rpsroute_IptTextSwGatewayIP").get_attribute("value")} != 10.10.10.1) Fail',file = open(file_name, '+a'))
            if_temp_error = True

        if(driver.find_element(By.NAME,"rpsroute_IptTextSwMetric").get_attribute("value") == "15" ):
            print(f"             [EMS1-6517][IP - Static Route - Modify] Metric (15) Pass",file = open(file_name, '+a'))
        else:
            print(f'             [EMS1-6517][IP - Static Route - Modify] Metric ({driver.find_element(By.NAME,"rpsroute_IptTextSwMetric").get_attribute("value")} != 15) Fail',file = open(file_name, '+a'))
            if_temp_error = True

        if(if_temp_error==False):
            print(f"             [EMS1-6517][IP - Static Route - Modify] Result Pass",file = open(file_name, '+a'))
        else:
            print(f'             [EMS1-6517][IP - Static Route - Modify] Result Fail',file = open(file_name, '+a'))

    if(if_find==False):
        print(f"             [EMS1-6517][IP - Static Route - Modify] Result Fail",file = open(file_name, '+a'))

    #192.168.169.207 Delete
    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "IP Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Static Route").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "IP Application").click()
    time.sleep(1)
    if_find=False
    for i in range(1,driver.find_elements(By.NAME,"ip_iproute_profile_checkbox").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[3]/div[1]/div[{i}]/div[3]").text
        if(ele == 'Name_Testm'):
            if_find=True
            driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[3]/div[1]/div[{i}]/div[8]/label").click()
            time.sleep(1)
            driver.find_element(By.ID,"ip_iproute_profile_del_btn").click()
            time.sleep(1)
            msg = e_swi.alert_accept_text(driver)
            try:
                e_pro.Close(driver)
            except:
                pass


    driver.find_element(By.LINK_TEXT, "Basic Setting").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "IP Setup").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Basic Setting").click() 
    time.sleep(1)
    e_swi.Management_IP_Address(driver,"192.168.0.1","255.255.255.0","0.0.0.0",file_name)
    time.sleep(1)
    msg = e_swi.alert_accept_text(driver)
    try:
        e_pro.Close(driver)
    except:
        pass
    if_find = False
    for i in range(1,int(driver.find_element(By.ID,"pageTotal").text)+1):
        for j in range(1,driver.find_elements(By.NAME,"basic_ipinterface_profile_checkbox").__len__()+1):
            ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[7]/div[1]/div[{j}]/div[4]").text
            if(ele == '100'):
                driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[7]/div[1]/div[{j}]/div[5]/label").click()
                if_find =True
                time.sleep(1)
        driver.find_element(By.ID,"btnNextPage").click()
    driver.find_element(By.ID,"basic_ipinterface_profile_del_btn").click()
    time.sleep(1)
    msg = e_swi.alert_accept_text(driver)
    try:
        e_pro.Close(driver)
    except:
        pass



    #192.168.169.207 Delete_check
    
    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"IP Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"Static Routing").click()
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    time.sleep(1)
    if_temp_error = False
    for i in range(1,driver.find_elements(By.NAME,"rpsroute_ChkTabDelete").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[{i+2}]/td[4]/div").text
        if(ele == 'Name_Testm'):
            if_temp_error = True
    if(if_temp_error==False and if_find==True):
        print(f"             [EMS1-6518][IP - Static Route - Delete] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6518][IP - Static Route - Delete] Result Fail",file = open(file_name, '+a'))

    #[EMS1-6519][IP - Static Route - Page Switch] Result Pass/Fail

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "IP Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Static Route").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "IP Application").click()
    time.sleep(1)
    for i in range(1,12):
        driver.find_element(By.ID,"ip_iproute_profile_new_btn").click()
        e_swi.IP_Static_Route(driver,False,"Name_Testx",f"10.10.{i}.1","255.255.0.0",f"10.10.{i}.1","15",file_name)
    driver.find_element(By.ID,'btnNextPage').click()
    if(driver.find_element(By.XPATH,'//*[@id="ip_iproute_profile_table"]/div[2]/div[1]').text == '11'):
        print(f"             [EMS1-6519][IP - Static Route - Page Switch] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6519][IP - Static Route - Page Switch] Result Fail",file = open(file_name, '+a'))

    for i in range(1,3):
        e_mod.Checkbox_EMS(driver,"ip_iproute_profile_checkbox",True)
        driver.find_element(By.ID,"ip_iproute_profile_del_btn").click()
        time.sleep(2)
        msg = e_swi.alert_accept_text(driver)
        try:
            e_pro.Close(driver)
        except:
            pass     
    print(f"======================================================================================",file = open(file_name, '+a'))

    '''driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "VLAN").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)
    if_find=False
    for i in range(1,driver.find_elements(By.NAME,"advance_vlan_static_profile_checkbox").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[23]/div[2]/div[1]/div[{i}]/div[3]").text
        if(ele == '100'):
            if_find=True
            driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[23]/div[2]/div[1]/div[{i}]/div[5]/label").click()
            time.sleep(1)
            driver.find_element(By.ID,"advance_vlan_static_profile_del_btn").click()'''

@retry()
def IP_DHCP(driver,url,ems_url,file_name):
    print(f"======================================================================================",file = open(file_name, '+a'))
    print(f"IP Application - DHCP Relay Test Start",file = open(file_name, '+a'))    

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT,"IP Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"DHCP").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"IP Application").click() 
    time.sleep(1)
    # EMS DHCP_Relay
    e_mod.Checkbox_EMS(driver,"ip_dhcp_vlan_profile_checkbox",True)
    driver.find_element(By.ID,"ip_dhcp_vlan_profile_del_btn").click()
    time.sleep(1)
    msg = e_swi.alert_accept_text(driver)
    try:
        e_pro.Close(driver)
    except:
        pass
    time.sleep(1)
    e_swi.DHCP_Relay(driver,True,"192.168.10.11","192.168.10.12","192.168.10.13",True,True,True,file_name)

    # 192.168.169.207 DHCP_Relay check
    
    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"IP Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"DHCP").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    driver.find_element(By.LINK_TEXT,"Global").click()
    time.sleep(1)
    if_temp_error = False
    if(driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td[3]/input").is_selected() == True ):
        print(f"             [EMS1-6451][IP - DHCP Relay] Active (True) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6451][IP - DHCP Relay] Active ({driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td[3]/input").is_selected()} != True) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    
    if(driver.find_element(By.NAME,"rpdhcp_IptTextRelayDHCP1").get_attribute("value") == "192.168.10.11" ):
        print(f"             [EMS1-6451][IP - DHCP Relay] DHCP1 (192.168.10.11) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6451][IP - DHCP Relay] DHCP1 ({driver.find_element(By.NAME,"rpdhcp_IptTextRelayDHCP1").get_attribute("value")} != 192.168.10.11) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpdhcp_IptTextRelayDHCP2").get_attribute("value") == "192.168.10.12" ):
        print(f"             [EMS1-6451][IP - DHCP Relay] DHCP2 (192.168.10.12) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6451][IP - DHCP Relay] DHCP2 ({driver.find_element(By.NAME,"rpdhcp_IptTextRelayDHCP2").get_attribute("value")} != 192.168.10.12) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpdhcp_IptTextRelayDHCP3").get_attribute("value") == "192.168.10.13" ):
        print(f"             [EMS1-6451][IP - DHCP Relay] DHCP3 (192.168.10.13) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6451][IP - DHCP Relay] DHCP3 ({driver.find_element(By.NAME,"rpdhcp_IptTextRelayDHCP3").get_attribute("value")} != 192.168.10.13) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpdhcpRelay_ChkOption82").is_selected() == True ):
        print(f"             [EMS1-6451][IP - DHCP Relay] Relay_Option (True) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6451][IP - DHCP Relay] Relay_Option ({driver.find_element(By.NAME,"rpdhcpRelay_ChkOption82").is_selected()} != True) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpdhcprelay_ChkFormat").is_selected() == True ):
        print(f"             [EMS1-6451][IP - DHCP Relay] Relay_Format (True) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6451][IP - DHCP Relay] Relay_Format ({driver.find_element(By.NAME,"rpdhcprelay_ChkFormat").is_selected()} != True) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpdhcpRelay_ChkInfo").is_selected() == True ):
        print(f"             [EMS1-6451][IP - DHCP Relay] Information (True) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6451][IP - DHCP Relay] Information ({driver.find_element(By.NAME,"rpdhcpRelay_ChkInfo").is_selected()} != True) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    
    #EMS DHCP_VLAN_NEW
    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Basic Setting").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "IP Setup").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Basic Setting").click() 
    time.sleep(1)
    driver.find_element(By.ID,"basic_ipinterface_profile_new_btn").click()
    time.sleep(1)
    e_swi.Basic_IP_Interface(driver,"10.10.10.1","255.255.255.0","100",file_name)
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"IP Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"DHCP").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"IP Application").click() 
    time.sleep(1)
    e_swi.DHCP_Relay(driver,False," "," "," ",False,False,False,file_name)
    time.sleep(1)
    driver.find_element(By.ID,"ip_dhcp_vlan_profile_new_btn").click()
    e_swi.DHCP_VLAN(driver,"100","Server","10.10.10.11","10","255.255.255.0","10.10.10.254","10.10.10.12","10.10.10.13",file_name)
    
    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"IP Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"DHCP").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    driver.find_element(By.LINK_TEXT,"Global").click()
    time.sleep(1)
    if_temp_error = False
    if(driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td[3]/input").is_selected() == False ):
        print(f"             [EMS1-6451][IP - DHCP Relay] Active (False) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6451][IP - DHCP Relay] Active ({driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[2]/td[3]/input").is_selected()} != False) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    
    if(driver.find_element(By.NAME,"rpdhcp_IptTextRelayDHCP1").get_attribute("value") == "0.0.0.0" ):
        print(f"             [EMS1-6451][IP - DHCP Relay] DHCP1 (0.0.0.0) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6451][IP - DHCP Relay] DHCP1 ({driver.find_element(By.NAME,"rpdhcp_IptTextRelayDHCP1").get_attribute("value")} != 0.0.0.0) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpdhcp_IptTextRelayDHCP2").get_attribute("value") == "0.0.0.0" ):
        print(f"             [EMS1-6451][IP - DHCP Relay] DHCP2 (0.0.0.0) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6451][IP - DHCP Relay] DHCP2 ({driver.find_element(By.NAME,"rpdhcp_IptTextRelayDHCP2").get_attribute("value")} != 0.0.0.0) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpdhcp_IptTextRelayDHCP3").get_attribute("value") == "0.0.0.0" ):
        print(f"             [EMS1-6451][IP - DHCP Relay] DHCP3 (0.0.0.0) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6451][IP - DHCP Relay] DHCP3 ({driver.find_element(By.NAME,"rpdhcp_IptTextRelayDHCP3").get_attribute("value")} != 0.0.0.0) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpdhcpRelay_ChkOption82").is_selected() == False ):
        print(f"             [EMS1-6451][IP - DHCP Relay] Relay_Option (False) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6451][IP - DHCP Relay] Relay_Option ({driver.find_element(By.NAME,"rpdhcpRelay_ChkOption82").is_selected()} != False) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpdhcprelay_ChkFormat").is_selected() == False ):
        print(f"             [EMS1-6451][IP - DHCP Relay] Relay_Format (False) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6451][IP - DHCP Relay] Relay_Format ({driver.find_element(By.NAME,"rpdhcprelay_ChkFormat").is_selected()} != False) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpdhcpRelay_ChkInfo").is_selected() == False ):
        print(f"             [EMS1-6451][IP - DHCP Relay] Information (False) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6451][IP - DHCP Relay] Information ({driver.find_element(By.NAME,"rpdhcpRelay_ChkInfo").is_selected()} != False) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(if_temp_error==False):
        print(f"             [EMS1-6451][IP - DHCP Relay] Result Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6451][IP - DHCP Relay] Result Fail',file = open(file_name, '+a'))
    print(f"--------------------------------------------------------------------------------------",file = open(file_name, '+a'))
    #192.168.169.207 DHCP_VLAN_NEW_check
    
    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"IP Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"DHCP").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    driver.find_element(By.LINK_TEXT,"VLAN").click()
    time.sleep(1)
    if_find=False
    for i in range(1,driver.find_elements(By.NAME,"rpdhcp_ChkTabDelete").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[{i*2}]/td[2]/div/a").text
        if(ele == '100'):
            if_find=True
            driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[{i*2}]/td[2]/div/a").click()
            time.sleep(1)
            if_temp_error = False
            if(driver.find_element(By.NAME,"rpdhcp_IptTextSwVID").get_attribute("value") == "100" ):
                print(f"             [EMS1-6520][IP - DHCP VLAN - New] VID (100) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6520][IP - DHCP VLAN - New] VID ({driver.find_element(By.NAME,"rpdhcp_IptTextSwVID").get_attribute("value")} != 100) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[3]/td[2]/table[1]/tbody/tr[4]/td[3]/input[1]").is_selected() == True ):
                print(f"             [EMS1-6520][IP - DHCP VLAN - New] DHCP_Status (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6520][IP - DHCP VLAN - New] DHCP_Status ({driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[3]/td[2]/table[1]/tbody/tr[4]/td[3]/input[1]").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            
            if(driver.find_element(By.NAME,"rpdhcp_IptTextSvrStartAddr").get_attribute("value") == "10.10.10.11" ):
                print(f"             [EMS1-6520][IP - DHCP VLAN - New] Client_Ip (10.10.10.11) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6520][IP - DHCP VLAN - New] Client_Ip ({driver.find_element(By.NAME,"rpdhcp_IptTextSvrStartAddr").get_attribute("value")} != 10.10.10.11) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,"rpdhcp_IptTextSvrSizePool").get_attribute("value") == "10" ):
                print(f"             [EMS1-6520][IP - DHCP VLAN - New] Pool_size (10) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6520][IP - DHCP VLAN - New] Pool_size ({driver.find_element(By.NAME,"rpdhcp_IptTextSvrSizePool").get_attribute("value")} != 10) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,"rpdhcp_IptTextSvrSubnet").get_attribute("value") == "255.255.255.0" ):
                print(f"             [EMS1-6520][IP - DHCP VLAN - New] Ip_Subnet (255.255.255.0) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6520][IP - DHCP VLAN - New] Ip_Subnet ({driver.find_element(By.NAME,"rpdhcp_IptTextSvrSubnet").get_attribute("value")} != 255.255.255.0) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,"rpdhcp_IptTextSvrGateway").get_attribute("value") == "10.10.10.254" ):
                print(f"             [EMS1-6520][IP - DHCP VLAN - New] Default_Gateway (10.10.10.254) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6520][IP - DHCP VLAN - New] Default_Gateway ({driver.find_element(By.NAME,"rpdhcp_IptTextSvrGateway").get_attribute("value")} != 10.10.10.254) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,"rpdhcp_IptTextSvrPrimDNS").get_attribute("value") == "10.10.10.12" ):
                print(f"             [EMS1-6520][IP - DHCP VLAN - New] Primary_DNS (10.10.10.12) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6520][IP - DHCP VLAN - New] Primary_DNS ({driver.find_element(By.NAME,"rpdhcp_IptTextSvrPrimDNS").get_attribute("value")} != 10.10.10.12) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,"rpdhcp_IptTextSvrSecondDNS").get_attribute("value") == "10.10.10.13" ):
                print(f"             [EMS1-6520][IP - DHCP VLAN - New] Secondary_DNS (10.10.10.13) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6520][IP - DHCP VLAN - New] Secondary_DNS ({driver.find_element(By.NAME,"rpdhcp_IptTextSvrSecondDNS").get_attribute("value")} != 10.10.10.13) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(if_temp_error==False):
                print(f"             [EMS1-6520][IP - DHCP VLAN - New] Result Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6520][IP - DHCP VLAN - New] Result Fail',file = open(file_name, '+a'))
    if(if_find==False):
        print(f"             [EMS1-6520][IP - DHCP VLAN - New] Result Fail",file = open(file_name, '+a'))
    #EMS DHCP_VLAN_Modify

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT,"IP Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"DHCP").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"IP Application").click() 
    time.sleep(1)
    if_find=False
    for i in range(1,driver.find_elements(By.NAME,"ip_dhcp_vlan_profile_checkbox").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[12]/div[2]/div[1]/div[{i}]/div[2]").text
        if(ele == '100'):
            if_find=True
            driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[12]/div[2]/div[1]/div[{i}]/div[5]/label").click()
            time.sleep(1)
            driver.find_element(By.ID,"ip_dhcp_vlan_profile_mod_btn").click()
            e_swi.DHCP_VLAN(driver,"100","Server","10.10.10.12","10","255.255.255.0","10.10.10.254","10.10.10.13","10.10.10.14",file_name)

    #192.168.169.207 DHCP_VLAN_Modify_check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"IP Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"DHCP").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    driver.find_element(By.LINK_TEXT,"VLAN").click()
    time.sleep(1)
    
    for i in range(1,driver.find_elements(By.NAME,"rpdhcp_ChkTabDelete").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[{i*2}]/td[2]/div/a").text
        if(ele == '100'):
            driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[{i*2}]/td[2]/div/a").click()
            time.sleep(1)
            if_temp_error = False
            if(driver.find_element(By.NAME,"rpdhcp_IptTextSwVID").get_attribute("value") == "100" ):
                print(f"             [EMS1-6521][IP - DHCP VLAN - Modify] VID (100) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6521][IP - DHCP VLAN - Modify] VID ({driver.find_element(By.NAME,"rpdhcp_IptTextSwVID").get_attribute("value")} != 100) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[3]/td[2]/table[1]/tbody/tr[4]/td[3]/input[1]").is_selected() == True ):
                print(f"             [EMS1-6521][IP - DHCP VLAN - Modify] DHCP_Status (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6521][IP - DHCP VLAN - Modify] DHCP_Status ({driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[3]/td[2]/table[1]/tbody/tr[4]/td[3]/input[1]").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            
            if(driver.find_element(By.NAME,"rpdhcp_IptTextSvrStartAddr").get_attribute("value") == "10.10.10.12" ):
                print(f"             [EMS1-6521][IP - DHCP VLAN - Modify] Client_Ip (10.10.10.12) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6521][IP - DHCP VLAN - Modify] Client_Ip ({driver.find_element(By.NAME,"rpdhcp_IptTextSvrStartAddr").get_attribute("value")} != 10.10.10.12) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,"rpdhcp_IptTextSvrSizePool").get_attribute("value") == "10" ):
                print(f"             [EMS1-6521][IP - DHCP VLAN - Modify] Pool_size (10) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6521][IP - DHCP VLAN - Modify] Pool_size ({driver.find_element(By.NAME,"rpdhcp_IptTextSvrSizePool").get_attribute("value")} != 10) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,"rpdhcp_IptTextSvrSubnet").get_attribute("value") == "255.255.255.0" ):
                print(f"             [EMS1-6521][IP - DHCP VLAN - Modify] Ip_Subnet (255.255.255.0) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6521][IP - DHCP VLAN - Modify] Ip_Subnet ({driver.find_element(By.NAME,"rpdhcp_IptTextSvrSubnet").get_attribute("value")} != 255.255.255.0) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,"rpdhcp_IptTextSvrGateway").get_attribute("value") == "10.10.10.254" ):
                print(f"             [EMS1-6521][IP - DHCP VLAN - Modify] Default_Gateway (10.10.10.254) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6521][IP - DHCP VLAN - Modify] Default_Gateway ({driver.find_element(By.NAME,"rpdhcp_IptTextSvrGateway").get_attribute("value")} != 10.10.10.254) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,"rpdhcp_IptTextSvrPrimDNS").get_attribute("value") == "10.10.10.13" ):
                print(f"             [EMS1-6521][IP - DHCP VLAN - Modify] Primary_DNS (10.10.10.13) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6521][IP - DHCP VLAN - Modify] Primary_DNS ({driver.find_element(By.NAME,"rpdhcp_IptTextSvrPrimDNS").get_attribute("value")} != 10.10.10.13) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,"rpdhcp_IptTextSvrSecondDNS").get_attribute("value") == "10.10.10.14" ):
                print(f"             [EMS1-6521][IP - DHCP VLAN - Modify] Secondary_DNS (10.10.10.14) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6521][IP - DHCP VLAN - Modify] Secondary_DNS ({driver.find_element(By.NAME,"rpdhcp_IptTextSvrSecondDNS").get_attribute("value")} != 10.10.10.14) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(if_temp_error==False):
                print(f"             [EMS1-6521][IP - DHCP VLAN - Modify] Result Pass",file = open(file_name, '+a'))
            else:
                print(f"             [EMS1-6521][IP - DHCP VLAN - Modify] Result Fail",file = open(file_name, '+a'))
    if(if_find==False):
        print(f"             [EMS1-6521][IP - DHCP VLAN - Modify] Result Fail",file = open(file_name, '+a'))
    #EMS DHCP_VLAN_Delete
        
    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT,"IP Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"DHCP").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"IP Application").click() 
    time.sleep(1)
    if_find=False
    for i in range(1,driver.find_elements(By.NAME,"ip_dhcp_vlan_profile_checkbox").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[12]/div[2]/div[1]/div[{i}]/div[2]").text
        if(ele == '100'):
            if_find=True
            driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[12]/div[2]/div[1]/div[{i}]/div[5]/label").click()
            time.sleep(1)
            driver.find_element(By.ID,"ip_dhcp_vlan_profile_del_btn").click()
            time.sleep(1)
            msg = e_swi.alert_accept_text(driver)
            try:
                e_pro.Close(driver)
            except:
                pass
            time.sleep(1)

    driver.find_element(By.LINK_TEXT, "Basic Setting").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "IP Setup").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Basic Setting").click() 
    time.sleep(1)
    if_find = False
    for i in range(1,int(driver.find_element(By.ID,"pageTotal").text)+1):
        for j in range(1,driver.find_elements(By.NAME,"basic_ipinterface_profile_checkbox").__len__()+1):
            ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[7]/div[1]/div[{j}]/div[4]").text
            if(ele == '100'):
                driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[7]/div[1]/div[{j}]/div[5]/label").click()
                if_find =True
                time.sleep(1)
        driver.find_element(By.ID,"btnNextPage").click()
    driver.find_element(By.ID,"basic_ipinterface_profile_del_btn").click()

    #192.168.169.207 DHCP_VLAN_Delete_check
    
    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"IP Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"DHCP").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    driver.find_element(By.LINK_TEXT,"VLAN").click()
    time.sleep(1)
    
    if_temp_error = False
    for i in range(1,driver.find_elements(By.NAME,"rpdhcp_ChkTabDelete").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[{i*2}]/td[2]/div/a").text
        if(ele == '100'):
            if_temp_error = True
    if(if_temp_error==False and if_find==True):
        print(f"             [EMS1-6522][IP - DHCP VLAN - Delete] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6522][IP - DHCP VLAN - Delete] Result Fail",file = open(file_name, '+a'))

    # [EMS1-6523][IP - DHCP VLAN - Page Switch] Result Pass
    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "VLAN").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)
    for i in range(1000,1011):
        driver.find_element(By.ID,"advance_vlan_static_profile_new_btn").click()
        time.sleep(1)
        e_swi.VLAN_Static_VLAN(driver,True,"Name_Test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx63",f"{i}","Forbidden","UnTagging",file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Basic Setting").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "IP Setup").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Basic Setting").click() 
    time.sleep(1)
    for i in range(1000,1011):
        driver.find_element(By.ID,"basic_ipinterface_profile_new_btn").click()
        time.sleep(1)
        e_swi.Basic_IP_Interface(driver,f"{i-999}.10.10.1","255.0.0.0",f"{i}",file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT,"IP Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"DHCP").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"IP Application").click() 
    time.sleep(1)
    
    for i in range(1000,1011):
        driver.find_element(By.ID,"ip_dhcp_vlan_profile_new_btn").click()
        e_swi.DHCP_VLAN(driver,f"{i}","Server","10.10.10.11","10","255.255.255.0","10.10.10.254","10.10.10.12","10.10.10.13",file_name)
    driver.find_element(By.ID,'btnNextPage1').click()
    time.sleep(1)
    if(driver.find_element(By.XPATH,'//*[@id="ip_dhcp_vlan_profile_table"]/div[2]/div[1]').text == "11"):
        print(f"             [EMS1-6523][IP - DHCP VLAN - Page Switch] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6523][IP - DHCP VLAN - Page Switch] Result Fail",file = open(file_name, '+a'))
    for i in range(1,3):
        e_mod.Checkbox_EMS(driver,"ip_dhcp_vlan_profile_checkbox",True)
        driver.find_element(By.ID,"ip_dhcp_vlan_profile_del_btn").click()
        time.sleep(1)
        msg = e_swi.alert_accept_text(driver)
        try:
            e_pro.Close(driver)
        except:
            pass
        time.sleep(1)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Basic Setting").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "IP Setup").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Basic Setting").click() 
    time.sleep(1)
    for i in range(1,3):
        for i in range(1,driver.find_elements(By.NAME,"basic_ipinterface_profile_checkbox").__len__()+1):
            ele = driver.find_element(By.XPATH,f'//*[@id="sys_route_profile_table"]/div[{i}]/div[3]').text
            if(ele == '255.0.0.0'):
                driver.find_element(By.XPATH,f'//*[@id="sys_route_profile_table"]/div[{i}]/div[5]/label').click()
        driver.find_element(By.ID,"basic_ipinterface_profile_del_btn").click()
        time.sleep(1)
        msg = e_swi.alert_accept_text(driver)
        try:
            e_pro.Close(driver)
        except:
            pass
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "VLAN").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)
    for i in range(1,3):
        for i in range(1,driver.find_elements(By.NAME,"advance_vlan_static_profile_checkbox").__len__()+1):
            ele = driver.find_element(By.XPATH,f'//*[@id="advance_vlan_static_profile_table"]/div[{i}]/div[4]').text
            if(ele == 'Name_Test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx63'):
                driver.find_element(By.XPATH,f'//*[@id="advance_vlan_static_profile_table"]/div[{i}]/div[5]/label').click()
        driver.find_element(By.ID,"advance_vlan_static_profile_del_btn").click()
        time.sleep(1)
        msg = e_swi.alert_accept_text(driver)
        try:
            e_pro.Close(driver)
        except:
            pass
    #EMS DHCP_L2_NEW
    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT,"IP Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"DHCP").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"IP Application").click() 
    time.sleep(1)
    driver.find_element(By.ID,"ip_dhcp_agent_profile_new_btn").click()
    time.sleep(1)
    e_swi.DHCP_L2(driver,'100','Option 82 Circuit Id new','Option 82 Remote Id new','Option 18 Interface Id new','Option 37 Remote Id new',True)
    #192.168.169.207 DHCP_L2_NEW_check
    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"IP Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"DHCP").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    driver.find_element(By.LINK_TEXT,"Option").click()
    time.sleep(1)
    if_find=False
    for i in range(1,driver.find_elements(By.NAME,"rpdhcpl2agent_ChkTabDelete").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[{i*2}]/td[2]/div/a").text
        if(ele == '100'):
            if_find=True
            driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[{i*2}]/td[2]/div/a").click()
            time.sleep(1)
            if_temp_error = False
            if(driver.find_element(By.NAME,"rpdhcpl2agent_IptTextVID").get_attribute("value") == "100" ):
                print(f"             [EMS1-6524][IP - DHCP L2 - New] VID (100) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6524][IP - DHCP L2 - New] VID ({driver.find_element(By.NAME,"rpdhcpl2agent_IptTextVID").get_attribute("value")} != 100) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            if(driver.find_element(By.NAME,"rpdhcpl2agent_IptTextOpt82CircuitId").get_attribute("value") == "Option 82 Circuit Id new" ):
                print(f"             [EMS1-6524][IP - DHCP L2 - New] (Option 82 Circuit Id new) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6524][IP - DHCP L2 - New] ({driver.find_element(By.NAME,"rpdhcpl2agent_IptTextOpt82CircuitId").get_attribute("value")} != Option 82 Circuit Id new) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            if(driver.find_element(By.NAME,"rpdhcpl2agent_IptTextOpt82RemoteId").get_attribute("value") == "Option 82 Remote Id new" ):
                print(f"             [EMS1-6524][IP - DHCP L2 - New] (Option 82 Remote Id new) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6524][IP - DHCP L2 - New] ({driver.find_element(By.NAME,"rpdhcpl2agent_IptTextOpt82RemoteId").get_attribute("value")} != Option 82 Remote Id new) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            if(driver.find_element(By.NAME,"rpdhcpl2agent_IptTextOpt18InterfaceId").get_attribute("value") == "Option 18 Interface Id new" ):
                print(f"             [EMS1-6524][IP - DHCP L2 - New] (Option 18 Interface Id new) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6524][IP - DHCP L2 - New] ({driver.find_element(By.NAME,"rpdhcpl2agent_IptTextOpt18InterfaceId").get_attribute("value")} != Option 18 Interface Id new) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            if(driver.find_element(By.NAME,"rpdhcpl2agent_IptTextOpt37RemoteId").get_attribute("value") == "Option 37 Remote Id new" ):
                print(f"             [EMS1-6524][IP - DHCP L2 - New] (Option 37 Remote Id new) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6524][IP - DHCP L2 - New] ({driver.find_element(By.NAME,"rpdhcpl2agent_IptTextOpt37RemoteId").get_attribute("value")} != Option 37 Remote Id new) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            if(driver.find_element(By.NAME,"rpdhcpl2agent_ldraEnable").is_selected() == True ):
                print(f"             [EMS1-6524][IP - DHCP L2 - New] LDRA ENABLE (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6524][IP - DHCP L2 - New] LDRA ENABLE ({driver.find_element(By.NAME,"rpdhcpl2agent_ldraEnable").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            if(if_temp_error==False):
                print(f"             [EMS1-6524][IP - DHCP L2 - New] Result Pass",file = open(file_name, '+a'))
            else:
                print(f"             [EMS1-6524][IP - DHCP L2 - New] Result Fail",file = open(file_name, '+a'))
    if(if_find==False):
        print(f"             [EMS1-6524][IP - DHCP L2 - New] Result Fail",file = open(file_name, '+a'))
    #EMS DHCP_L2_Modify
    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT,"IP Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"DHCP").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"IP Application").click() 
    time.sleep(1)
    if_find=False
    for i in range(1,driver.find_elements(By.NAME,"ip_dhcp_agent_profile_checkbox").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[15]/div[2]/div[1]/div[{i}]/div[2]").text
        if(ele == '100'):
            if_find=True
            driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[15]/div[2]/div[1]/div[{i}]/div[8]/label").click()
            time.sleep(1)
            driver.find_element(By.ID,"ip_dhcp_agent_profile_mod_btn").click()
            e_swi.DHCP_L2(driver,'100','Option 82 Circuit Id modify','Option 82 Remote Id modify','Option 18 Interface Id modify','Option 37 Remote Id modify',True)
    #192.168.169.207 DHCP_L2_Modify_check
    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"IP Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"DHCP").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    driver.find_element(By.LINK_TEXT,"Option").click()
    time.sleep(1)
    if_find=False
    for i in range(1,driver.find_elements(By.NAME,"rpdhcpl2agent_ChkTabDelete").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[{i*2}]/td[2]/div/a").text
        if(ele == '100'):
            if_find=True
            driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[{i*2}]/td[2]/div/a").click()
            time.sleep(1)
            if_temp_error = False
            if(driver.find_element(By.NAME,"rpdhcpl2agent_IptTextVID").get_attribute("value") == "100" ):
                print(f"             [EMS1-6526][IP - DHCP L2 - Modify] VID (100) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6526][IP - DHCP L2 - Modify] VID ({driver.find_element(By.NAME,"rpdhcpl2agent_IptTextVID").get_attribute("value")} != 100) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            if(driver.find_element(By.NAME,"rpdhcpl2agent_IptTextOpt82CircuitId").get_attribute("value") == "Option 82 Circuit Id modify" ):
                print(f"             [EMS1-6526][IP - DHCP L2 - Modify] (Option 82 Circuit Id modify) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6526][IP - DHCP L2 - Modify] ({driver.find_element(By.NAME,"rpdhcpl2agent_IptTextOpt82CircuitId").get_attribute("value")} != Option 82 Circuit Id modify) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            if(driver.find_element(By.NAME,"rpdhcpl2agent_IptTextOpt82RemoteId").get_attribute("value") == "Option 82 Remote Id modify" ):
                print(f"             [EMS1-6526][IP - DHCP L2 - Modify] (Option 82 Remote Id modify) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6526][IP - DHCP L2 - Modify] ({driver.find_element(By.NAME,"rpdhcpl2agent_IptTextOpt82RemoteId").get_attribute("value")} != Option 82 Remote Id modify) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            if(driver.find_element(By.NAME,"rpdhcpl2agent_IptTextOpt18InterfaceId").get_attribute("value") == "Option 18 Interface Id modify" ):
                print(f"             [EMS1-6526][IP - DHCP L2 - Modify] (Option 18 Interface Id modify) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6526][IP - DHCP L2 - Modify] ({driver.find_element(By.NAME,"rpdhcpl2agent_IptTextOpt18InterfaceId").get_attribute("value")} != Option 18 Interface Id modify) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            if(driver.find_element(By.NAME,"rpdhcpl2agent_IptTextOpt37RemoteId").get_attribute("value") == "Option 37 Remote Id modify" ):
                print(f"             [EMS1-6526][IP - DHCP L2 - Modify] (Option 37 Remote Id modify) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6526][IP - DHCP L2 - Modify] ({driver.find_element(By.NAME,"rpdhcpl2agent_IptTextOpt37RemoteId").get_attribute("value")} != Option 37 Remote Id modify) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            if(driver.find_element(By.NAME,"rpdhcpl2agent_ldraEnable").is_selected() == True ):
                print(f"             [EMS1-6526][IP - DHCP L2 - Modify] LDRA ENABLE (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6526][IP - DHCP L2 - Modify] LDRA ENABLE ({driver.find_element(By.NAME,"rpdhcpl2agent_ldraEnable").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            if(if_temp_error==False):
                print(f"             [EMS1-6526][IP - DHCP L2 - Modify] Result Pass",file = open(file_name, '+a'))
            else:
                print(f"             [EMS1-6526][IP - DHCP L2 - Modify] Result Fail",file = open(file_name, '+a'))
    if(if_find==False):
        print(f"             [EMS1-6526][IP - DHCP L2 - Modify] Result Fail",file = open(file_name, '+a'))
    #EMS DHCP_L2_Delete
    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT,"IP Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"DHCP").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"IP Application").click() 
    time.sleep(1)
    if_find=False
    for i in range(1,driver.find_elements(By.NAME,"ip_dhcp_agent_profile_checkbox").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[15]/div[2]/div[1]/div[{i}]/div[2]").text
        if(ele == '100'):
            if_find=True
            driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[15]/div[2]/div[1]/div[{i}]/div[8]/label").click()
            time.sleep(1)
            driver.find_element(By.ID,"ip_dhcp_agent_profile_del_btn").click()
    #192.168.169.207 DHCP_L2_Delete_check
    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"IP Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"DHCP").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    driver.find_element(By.LINK_TEXT,"Option").click()
    time.sleep(1)
    
    if_temp_error = False
    for i in range(1,driver.find_elements(By.NAME,"rpdhcpl2agent_ChkTabDelete").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[{i*2}]/td[2]/div/a").text
        if(ele == '100'):
            if_temp_error = True
    if(if_temp_error==False and if_find==True):
        print(f"             [EMS1-6527][IP - DHCP L2 - Delete] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6527][IP - DHCP L2 - Delete] Result Fail",file = open(file_name, '+a'))

    #[EMS1-6528][IP - DHCP L2 - Page Switch] Result 
       
    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT,"IP Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"DHCP").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"IP Application").click() 
    time.sleep(1)
    for i in range(1,12):
        driver.find_element(By.ID,"ip_dhcp_agent_profile_new_btn").click()
        time.sleep(1)
        e_swi.DHCP_L2(driver,f'{i}',' ',' ',' ',' ',True)
    driver.find_element(By.ID,'btnNextPage2').click()
    time.sleep(1)
    if(driver.find_element(By.XPATH,'//*[@id="ip_dhcp_agent_profile_table"]/div[2]/div[1]').text == "11"):
        print(f"             [EMS1-6528][IP - DHCP L2 - Page Switch] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6528][IP - DHCP L2 - Page Switch] Result Fail",file = open(file_name, '+a'))
    for i in range(1,3):
        e_mod.Checkbox_EMS(driver,"ip_dhcp_agent_profile_checkbox",True)
        driver.find_element(By.ID,"ip_dhcp_agent_profile_del_btn").click()
        time.sleep(1)
        msg = e_swi.alert_accept_text(driver)
        try:
            e_pro.Close(driver)
        except:
            pass
        time.sleep(1)
    
    '''driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT,"IP Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"DHCP").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"IP Application").click() 
    time.sleep(1)
    driver.find_element(By.ID,"ip_dhcp_vlan_profile_new_btn").click()
    e_swi.DHCP_VLAN(driver,"100","Relay","10.10.10.1","10.10.10.2","10.10.10.3",True,True,True,file_name)
    
    #192.168.169.207 DHCP_L2_NEW_check
    
    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"IP Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"DHCP").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    driver.find_element(By.LINK_TEXT,"VLAN").click()
    time.sleep(1)
    if_find=False
    for i in range(1,driver.find_elements(By.NAME,"rpdhcp_ChkTabDelete").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[{i*2}]/td[2]/div/a").text
        if(ele == '100'):
            if_find=True
            driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[{i*2}]/td[2]/div/a").click()
            time.sleep(1)
            if_temp_error = False
            if(driver.find_element(By.NAME,"rpdhcp_IptTextSwVID").get_attribute("value") == "100" ):
                print(f"             [EMS1-6524][IP - DHCP L2 - New] VID (100) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6524][IP - DHCP L2 - New] VID ({driver.find_element(By.NAME,"rpdhcp_IptTextSwVID").get_attribute("value")} != 100) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[3]/td[2]/table[1]/tbody/tr[4]/td[3]/input[2]").is_selected() == True ):
                print(f"             [EMS1-6524][IP - DHCP L2 - New] DHCP_Status (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6524][IP - DHCP L2 - New] DHCP_Status ({driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[3]/td[2]/table[1]/tbody/tr[4]/td[3]/input[2]").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            
            if(driver.find_element(By.NAME,"rpdhcp_VLANSetting_IptTextRelayDHCP1").get_attribute("value") == "10.10.10.1" ):
                print(f"             [EMS1-6524][IP - DHCP L2 - New] DHCP_Server1 (10.10.10.1) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6524][IP - DHCP L2 - New] DHCP_Server1 ({driver.find_element(By.NAME,"rpdhcp_VLANSetting_IptTextRelayDHCP1").get_attribute("value")} != 10.10.10.1) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,"rpdhcp_VLANSetting_IptTextRelayDHCP2").get_attribute("value") == "10.10.10.2" ):
                print(f"             [EMS1-6524][IP - DHCP L2 - New] DHCP_Server2 (10.10.10.2) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6524][IP - DHCP L2 - New] DHCP_Server2 ({driver.find_element(By.NAME,"rpdhcp_VLANSetting_IptTextRelayDHCP2").get_attribute("value")} != 10.10.10.2) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,"rpdhcp_VLANSetting_IptTextRelayDHCP3").get_attribute("value") == "10.10.10.3" ):
                print(f"             [EMS1-6524][IP - DHCP L2 - New] DHCP_Server3 (10.10.10.3) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6524][IP - DHCP L2 - New] DHCP_Server3 ({driver.find_element(By.NAME,"rpdhcp_VLANSetting_IptTextRelayDHCP3").get_attribute("value")} != 10.10.10.3) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[3]/td[2]/table[1]/tbody/tr[28]/td[3]/input").is_selected() == True ):
                print(f"             [EMS1-6524][IP - DHCP L2 - New] Relay_Agent (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6524][IP - DHCP L2 - New] Relay_Agent ({driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[3]/td[2]/table[1]/tbody/tr[28]/td[3]/input").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[3]/td[2]/table[1]/tbody/tr[30]/td[3]/input").is_selected() == True ):
                print(f"             [EMS1-6524][IP - DHCP L2 - New] Format (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6524][IP - DHCP L2 - New] Format ({driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[3]/td[2]/table[1]/tbody/tr[30]/td[3]/input").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH ,"/html/body/form/table/tbody/tr[3]/td[2]/table[1]/tbody/tr[31]/td[3]/input[1]").is_selected() == True ):
                print(f"             [EMS1-6524][IP - DHCP L2 - New] Information (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6524][IP - DHCP L2 - New] Information ({driver.find_element(By.XPATH ,"/html/body/form/table/tbody/tr[3]/td[2]/table[1]/tbody/tr[31]/td[3]/input[1]").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(if_temp_error==False):
                print(f"             [EMS1-6524][IP - DHCP L2 - New] Result Pass",file = open(file_name, '+a'))
            else:
                print(f"             [EMS1-6524][IP - DHCP L2 - New] Result Fail",file = open(file_name, '+a'))
    if(if_find==False):
        print(f"             [EMS1-6524][IP - DHCP L2 - New] Result Fail",file = open(file_name, '+a'))
   
    #EMS DHCP_L2_Modify
    
    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT,"IP Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"DHCP").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"IP Application").click() 
    time.sleep(1)
    if_find=False
    for i in range(1,driver.find_elements(By.NAME,"ip_dhcp_vlan_profile_checkbox").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[12]/div[2]/div[1]/div[{i}]/div[2]").text
        if(ele == '100'):
            if_find=True
            driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[12]/div[2]/div[1]/div[{i}]/div[5]/label").click()
            time.sleep(1)
            driver.find_element(By.ID,"ip_dhcp_vlan_profile_mod_btn").click()
            e_swi.DHCP_VLAN(driver,"100","Relay","10.10.10.11","10.10.10.12","10.10.10.13",True,True,True,file_name)

    #192.168.169.207 DHCP_L2_Modify_check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"IP Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"DHCP").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    driver.find_element(By.LINK_TEXT,"VLAN").click()
    time.sleep(1)
    
    for i in range(1,driver.find_elements(By.NAME,"rpdhcp_ChkTabDelete").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[{i*2}]/td[2]/div/a").text
        if(ele == '100'):
            driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[{i*2}]/td[2]/div/a").click()
            time.sleep(1)
            if_temp_error = False
            if(driver.find_element(By.NAME,"rpdhcp_IptTextSwVID").get_attribute("value") == "100" ):
                print(f"             [EMS1-6526][IP - DHCP L2 - Modify] VID (100) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6526][IP - DHCP L2 - Modify] VID ({driver.find_element(By.NAME,"rpdhcp_IptTextSwVID").get_attribute("value")} != 100) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[3]/td[2]/table[1]/tbody/tr[4]/td[3]/input[2]").is_selected() == True ):
                print(f"             [EMS1-6526][IP - DHCP L2 - Modify] DHCP_Status (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6526][IP - DHCP L2 - Modify] DHCP_Status ({driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[3]/td[2]/table[1]/tbody/tr[4]/td[3]/input[2]").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            
            if(driver.find_element(By.NAME,"rpdhcp_VLANSetting_IptTextRelayDHCP1").get_attribute("value") == "10.10.10.11" ):
                print(f"             [EMS1-6526][IP - DHCP L2 - Modify] DHCP_Server1 (10.10.10.11) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6526][IP - DHCP L2 - Modify] DHCP_Server1 ({driver.find_element(By.NAME,"rpdhcp_VLANSetting_IptTextRelayDHCP1").get_attribute("value")} != 10.10.10.11) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,"rpdhcp_VLANSetting_IptTextRelayDHCP2").get_attribute("value") == "10.10.10.12" ):
                print(f"             [EMS1-6526][IP - DHCP L2 - Modify] DHCP_Server2 (10.10.10.12) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6526][IP - DHCP L2 - Modify] DHCP_Server2 ({driver.find_element(By.NAME,"rpdhcp_VLANSetting_IptTextRelayDHCP2").get_attribute("value")} != 10.10.10.12) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,"rpdhcp_VLANSetting_IptTextRelayDHCP3").get_attribute("value") == "10.10.10.13" ):
                print(f"             [EMS1-6526][IP - DHCP L2 - Modify] DHCP_Server3 (10.10.10.13) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6526][IP - DHCP L2 - Modify] DHCP_Server3 ({driver.find_element(By.NAME,"rpdhcp_VLANSetting_IptTextRelayDHCP3").get_attribute("value")} != 10.10.10.13) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[3]/td[2]/table[1]/tbody/tr[28]/td[3]/input").is_selected() == True ):
                print(f"             [EMS1-6526][IP - DHCP L2 - Modify] Relay_Agent (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6526][IP - DHCP L2 - Modify] Relay_Agent ({driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[3]/td[2]/table[1]/tbody/tr[28]/td[3]/input").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[3]/td[2]/table[1]/tbody/tr[30]/td[3]/input").is_selected() == True ):
                print(f"             [EMS1-6526][IP - DHCP L2 - Modify] Format (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6526][IP - DHCP L2 - Modify] Format ({driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[3]/td[2]/table[1]/tbody/tr[30]/td[3]/input").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH ,"/html/body/form/table/tbody/tr[3]/td[2]/table[1]/tbody/tr[31]/td[3]/input[1]").is_selected() == True ):
                print(f"             [EMS1-6526][IP - DHCP L2 - Modify] Information (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6526][IP - DHCP L2 - Modify] Information ({driver.find_element(By.XPATH ,"/html/body/form/table/tbody/tr[3]/td[2]/table[1]/tbody/tr[31]/td[3]/input[1]").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(if_temp_error==False):
                print(f"             [EMS1-6526][IP - DHCP L2 - Modify] Result Pass",file = open(file_name, '+a'))
            else:
                print(f"             [EMS1-6526][IP - DHCP L2 - Modify] Result Fail",file = open(file_name, '+a'))
    if(if_find==False):
        print(f"             [EMS1-6526][IP - DHCP L2 - Modify] Result Fail",file = open(file_name, '+a'))
    #EMS DHCP_L2_Delete
        
    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT,"IP Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"DHCP").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"IP Application").click() 
    time.sleep(1)
    if_find=False
    for i in range(1,driver.find_elements(By.NAME,"ip_dhcp_vlan_profile_checkbox").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[12]/div[2]/div[1]/div[{i}]/div[2]").text
        if(ele == '100'):
            if_find=True
            driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[12]/div[2]/div[1]/div[{i}]/div[5]/label").click()
            time.sleep(1)
            driver.find_element(By.ID,"ip_dhcp_vlan_profile_del_btn").click()

    #192.168.169.207 DHCP_L2_Delete_check    
    
    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"IP Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"DHCP").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    driver.find_element(By.LINK_TEXT,"VLAN").click()
    time.sleep(1)
    
    if_temp_error = False
    for i in range(1,driver.find_elements(By.NAME,"rpdhcp_ChkTabDelete").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[{i*2}]/td[2]/div/a").text
        if(ele == '100'):
            if_temp_error = True
    if(if_temp_error==False and if_find==True):
        print(f"             [EMS1-6527][IP - DHCP L2 - Delete] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6527][IP - DHCP L2 - Delete] Result Fail",file = open(file_name, '+a'))'''

    print(f"======================================================================================",file = open(file_name, '+a'))

@retry()
def Advanced_VLAN(driver,url,ems_url,file_name,Pon_Name,Eth_Name,Pon_Name_L,Eth_Name_L,OLT_Eth_Port):
    print(f"======================================================================================",file = open(file_name, '+a'))
    print(f"Advanced Application - VLAN Test Start",file = open(file_name, '+a'))
    
    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "VLAN").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)
    e_swi.VLAN_Port_isolation(driver,False,file_name)

    #VLAN - Port Isolation_Check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"VLAN").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    mod.Switch_Specific_Frame(driver,0)
    driver.find_element(By.LINK_TEXT,"VLAN Port Setting").click()
    mod.Switch_Default(driver)
    driver.switch_to.frame("main")
    time.sleep(1)

    if_temp_error = False
    if(driver.find_element(By.NAME,"rpvlanport_ChkSysPortIsolation").is_selected() == False ):
        print(f"             [EMS1-6452][VLAN - Port Isolation] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6452][VLAN - Port Isolation] Result Fail",file = open(file_name, '+a'))
        if_temp_error = True
        
    #VLAN - Port Setting
    
    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "VLAN").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)
    e_swi.VLAN_Port_Setting(driver,Pon_Name,True,"4094","Untag Only",True,file_name)
    time.sleep(1)
    e_swi.VLAN_Port_Setting(driver,Eth_Name,True,"4094","Untag Only",True,file_name)

    #VLAN - Port Setting check
        
    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"VLAN").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    mod.Switch_Specific_Frame(driver,0)
    driver.find_element(By.LINK_TEXT,"VLAN Port Setting").click()
    mod.Switch_Default(driver)
    driver.switch_to.frame("main")
    time.sleep(1)
    if_temp_error = False
    for i in range(1,driver.find_elements(By.NAME,"rpvlanport_ChkIngress").__len__()+1):
        if(driver.find_element(By.XPATH,f"/html/body/form/table[1]/tbody/tr[2]/td/table[2]/tbody/tr[{(i+1)*2}]/td[2]/div").text == Pon_Name_L):

            if(driver.find_element(By.XPATH,f"/html/body/form/table[1]/tbody/tr[2]/td/table[2]/tbody/tr[{(i+1)*2}]/td[3]/div/input").is_selected() == True ):
                print(f"             [EMS1-6529][VLAN - Port Setting] Pon4_Ingress (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6529][VLAN - Port Setting] Pon4_Ingress ({driver.find_element(By.XPATH,f"/html/body/form/table[1]/tbody/tr[2]/td/table[2]/tbody/tr[{(i+1)*2}]/td[3]/div/input").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            
            if(driver.find_element(By.XPATH,f"/html/body/form/table[1]/tbody/tr[2]/td/table[2]/tbody/tr[{(i+1)*2}]/td[4]/div/input").get_attribute("value") == "4094" ):
                print(f"             [EMS1-6529][VLAN - Port Setting] Pon4_PVID (4094) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6529][VLAN - Port Setting] Pon4_PVID ({driver.find_element(By.XPATH,f"/html/body/form/table[1]/tbody/tr[2]/td/table[2]/tbody/tr[{(i+1)*2}]/td[4]/div/input").get_attribute("value")} != 4094) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            
            if(Select(driver.find_element(By.XPATH,f"/html/body/form/table[1]/tbody/tr[2]/td/table[2]/tbody/tr[{(i+1)*2}]/td[5]/div/select")).first_selected_option.get_attribute("text") == "Untag Only" ):
                print(f"             [EMS1-6529][VLAN - Port Setting] Pon4_FrameType (Untag Only) pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6529][VLAN - Port Setting] Pon4_FrameType ({Select(driver.find_element(By.XPATH,f"/html/body/form/table[1]/tbody/tr[2]/td/table[2]/tbody/tr[{(i+1)*2}]/td[5]/div/select")).first_selected_option.get_attribute("text")} != Untag Only) fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,f"/html/body/form/table[1]/tbody/tr[2]/td/table[2]/tbody/tr[{(i+1)*2}]/td[6]/div/input").is_selected() == True ):
                print(f"             [EMS1-6529][VLAN - Port Setting] Pon4_VLAN (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6529][VLAN - Port Setting] Pon4_VLAN ({driver.find_element(By.XPATH,f"/html/body/form/table[1]/tbody/tr[2]/td/table[2]/tbody/tr[{(i+1)*2}]/td[6]/div/input").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True

    for i in range(1,driver.find_elements(By.NAME,"rpvlanport_ChkIngress").__len__()+1):
        if(driver.find_element(By.XPATH,f"/html/body/form/table[1]/tbody/tr[2]/td/table[2]/tbody/tr[{(i+1)*2}]/td[2]/div").text == Eth_Name_L):

            if(driver.find_element(By.XPATH,f"/html/body/form/table[1]/tbody/tr[2]/td/table[2]/tbody/tr[{(i+1)*2}]/td[3]/div/input").is_selected() == True ):
                print(f"             [EMS1-6529][VLAN - Port Setting] eth8_Ingress (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6529][VLAN - Port Setting] eth8_Ingress ({driver.find_element(By.XPATH,f"/html/body/form/table[1]/tbody/tr[2]/td/table[2]/tbody/tr[{(i+1)*2}]/td[3]/div/input").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,f"/html/body/form/table[1]/tbody/tr[2]/td/table[2]/tbody/tr[{(i+1)*2}]/td[4]/div/input").get_attribute("value") == "4094" ):
                print(f"             [EMS1-6529][VLAN - Port Setting] eth8_PVID (4094) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6529][VLAN - Port Setting] eth8_PVID ({driver.find_element(By.XPATH,f"/html/body/form/table[1]/tbody/tr[2]/td/table[2]/tbody/tr[{(i+1)*2}]/td[4]/div/input").get_attribute("value")} != 4094) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(Select(driver.find_element(By.XPATH,f"/html/body/form/table[1]/tbody/tr[2]/td/table[2]/tbody/tr[{(i+1)*2}]/td[5]/div/select")).first_selected_option.get_attribute("text") == "Untag Only" ):
                print(f"             [EMS1-6529][VLAN - Port Setting] eth8_FrameType (Untag Only) pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6529][VLAN - Port Setting] eth8_FrameType ({Select(driver.find_element(By.XPATH,f"/html/body/form/table[1]/tbody/tr[2]/td/table[2]/tbody/tr[{(i+1)*2}]/td[5]/div/select")).first_selected_option.get_attribute("text")} != Untag Only) fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,f"/html/body/form/table[1]/tbody/tr[2]/td/table[2]/tbody/tr[{(i+1)*2}]/td[6]/div/input").is_selected() == True ):
                print(f"             [EMS1-6529][VLAN - Port Setting] eth8_VLAN (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6529][VLAN - Port Setting] eth8_VLAN ({driver.find_element(By.XPATH,f"/html/body/form/table[1]/tbody/tr[2]/td/table[2]/tbody/tr[{(i+1)*2}]/td[6]/div/input").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True

    if(if_temp_error==False):
        print(f"             [EMS1-6529][VLAN - Port Setting] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6529][VLAN - Port Setting] Result Fail",file = open(file_name, '+a'))

    print(f"======================================================================================",file = open(file_name, '+a'))

    #VLAN - Subnet Based Apply Result

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "VLAN").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)
    e_swi.VLAN_Subnet_Based_Apply(driver,False,False,file_name)


    #VLAN - Subnet Based Apply Result check
        
    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"VLAN").click()
    time.sleep(3)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    mod.Switch_Specific_Frame(driver,0)
    driver.find_element(By.LINK_TEXT,"VLAN Port Setting").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    driver.switch_to.frame("main")
    driver.find_element(By.LINK_TEXT,"Subnet Based Vlan").click()

    if_temp_error = False
    if(driver.find_element(By.NAME,"rpsubnetbasedvlan_ChkFeatureActive").is_selected() == False ):
        print(f"             [EMS1-6530][VLAN - Subnet Based] Active (False) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6530][VLAN - Subnet Based] Active ({driver.find_element(By.NAME,"rpsubnetbasedvlan_ChkFeatureActive").is_selected()} != False) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpdhcpvlanoverride_ChkActive").is_selected() == False ):
        print(f"             [EMS1-6530][VLAN - Subnet Based] DHCP_Vlan (False) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6530][VLAN - Subnet Based] DHCP_Vlan ({driver.find_element(By.NAME,"rpdhcpvlanoverride_ChkActive").is_selected()} != False) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(if_temp_error==False):
        print(f"             [EMS1-6530][VLAN - Subnet Based - Apply] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6530][VLAN - Subnet Based - Apply] Result Fail",file = open(file_name, '+a'))

    #VLAN - Subnet Based New Result
    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "VLAN").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)
    driver.find_element(By.ID,"advance_vlan_subnet_profile_new_btn").click()
    e_swi.VLAN_Subnet_Based(driver,True,"Name_Test_xxxxxxxxxxxxxxxxxxxx31","10.10.10.1","32","4094","7",file_name)



    #VLAN - Subnet Based New Result check
        
    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"VLAN").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    mod.Switch_Specific_Frame(driver,0)
    driver.find_element(By.LINK_TEXT,"VLAN Port Setting").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    driver.switch_to.frame("main")
    driver.find_element(By.LINK_TEXT,"Subnet Based Vlan").click()
    mod.Switch_Default(driver)
    driver.switch_to.frame("main")

    for i in range(1,driver.find_elements(By.NAME,"rpsubnetbasedvlan_ChkDelete").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[4]/tbody/tr[{i*2}]/td[4]/div").text
        if(ele == 'Name_Test_xxxxxxxxxxxxxxxxxxxx31'):
            driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[4]/tbody/tr[{i*2}]/td[2]/div/a").click()
            time.sleep(1)
            if_temp_error = False
            if(driver.find_element(By.NAME,"rpsubnetbasedvlan_ChkActive").is_selected() == True ):
                print(f"             [EMS1-6531][VLAN - Subnet Based - New] Active (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6531][VLAN - Subnet Based - New] Active ({driver.find_element(By.NAME,"rpsubnetbasedvlan_ChkActive").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,"rpsubnetbasedvlan_IptTextName").get_attribute("value") == "Name_Test_xxxxxxxxxxxxxxxxxxxx31" ):
                print(f"             [EMS1-6531][VLAN - Subnet Based - New] Name (Name_Test_xxxxxxxxxxxxxxxxxxxx31) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6531][VLAN - Subnet Based - New] Name ({driver.find_element(By.NAME,"rpsubnetbasedvlan_IptTextName").get_attribute("value")} != Name_Test_xxxxxxxxxxxxxxxxxxxx31) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,"rpsubnetbasedvlan_IptTextIp").get_attribute("value") == "10.10.10.1" ):
                print(f"             [EMS1-6531][VLAN - Subnet Based - New] IP (10.10.10.1) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6531][VLAN - Subnet Based - New] IP ({driver.find_element(By.NAME,"rpsubnetbasedvlan_IptTextIp").get_attribute("value")} != 10.10.10.1) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,"rpsubnetbasedvlan_IptTextMaxbits").get_attribute("value") == "32" ):
                print(f"             [EMS1-6531][VLAN - Subnet Based - New] Mask_Bits (32) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6531][VLAN - Subnet Based - New] Mask_Bits ({driver.find_element(By.NAME,"rpsubnetbasedvlan_IptTextMaxbits").get_attribute("value")} != 32) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,"rpsubnetbasedvlan_IptTextVID").get_attribute("value") == "4094" ):
                print(f"             [EMS1-6531][VLAN - Subnet Based - New] VID (4094) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6531][VLAN - Subnet Based - New] VID ({driver.find_element(By.NAME,"rpsubnetbasedvlan_IptTextVID").get_attribute("value")} != 4094) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,"rpsubnetbasedvlan_IptTextPri").get_attribute("value") == "7" ):
                print(f"             [EMS1-6531][VLAN - Subnet Based - New] Priority (7) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6531][VLAN - Subnet Based - New] Priority ({driver.find_element(By.NAME,"rpsubnetbasedvlan_IptTextPri").get_attribute("value")} != 7) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(if_temp_error==False):
                print(f"             [EMS1-6531][VLAN - Subnet Based - New] Result Pass",file = open(file_name, '+a'))
            else:
                print(f"             [EMS1-6531][VLAN - Subnet Based - New] Result Fail",file = open(file_name, '+a'))

    #VLAN - Subnet Based Modify Result

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "VLAN").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)
    for i in range(1,driver.find_elements(By.NAME,"advance_vlan_subnet_profile_checkbox").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[17]/div[2]/div[1]/div[{i}]/div[3]").text
        if(ele == 'Name_Test_xxxxxxxxxxxxxxxxxxxx31'):
            driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[17]/div[2]/div[1]/div[{i}]/div[8]/label").click()
            time.sleep(1)
    driver.find_element(By.ID,"advance_vlan_subnet_profile_mod_btn").click()
    e_swi.VLAN_Subnet_Based(driver,True,"Name_Test_xxxxxxxxxxxxxxxxx_m_31","10.10.10.1","32","1","0",file_name)
    #VLAN - Subnet Based Modify Result check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"VLAN").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    mod.Switch_Specific_Frame(driver,0)
    driver.find_element(By.LINK_TEXT,"VLAN Port Setting").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    driver.switch_to.frame("main")
    driver.find_element(By.LINK_TEXT,"Subnet Based Vlan").click()
    time.sleep(1)

    if_find = False
    for i in range(1,driver.find_elements(By.NAME,"rpsubnetbasedvlan_ChkDelete").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[4]/tbody/tr[{i*2}]/td[4]/div").text
        if(ele == 'Name_Test_xxxxxxxxxxxxxxxxx_m_31'):
            driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[4]/tbody/tr[{i*2}]/td[2]/div/a").click()
            time.sleep(1)
            if_temp_error = False
            if(driver.find_element(By.NAME,"rpsubnetbasedvlan_ChkActive").is_selected() == True ):
                print(f"             [EMS1-6532][VLAN - Subnet Based - Modify] Active (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6532][VLAN - Subnet Based - Modify] Active ({driver.find_element(By.NAME,"rpsubnetbasedvlan_ChkActive").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,"rpsubnetbasedvlan_IptTextName").get_attribute("value") == "Name_Test_xxxxxxxxxxxxxxxxx_m_31" ):
                print(f"             [EMS1-6532][VLAN - Subnet Based - Modify] Name (Name_Test_xxxxxxxxxxxxxxxxx_m_31) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6532][VLAN - Subnet Based - Modify] Name ({driver.find_element(By.NAME,"rpsubnetbasedvlan_IptTextName").get_attribute("value")} != Name_Test_xxxxxxxxxxxxxxxxx_m_31) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,"rpsubnetbasedvlan_IptTextIp").get_attribute("value") == "10.10.10.1" ):
                print(f"             [EMS1-6532][VLAN - Subnet Based - Modify] IP (10.10.10.1) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6532][VLAN - Subnet Based - Modify] IP ({driver.find_element(By.NAME,"rpsubnetbasedvlan_IptTextIp").get_attribute("value")} != 10.10.10.1) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,"rpsubnetbasedvlan_IptTextMaxbits").get_attribute("value") == "32" ):
                print(f"             [EMS1-6532][VLAN - Subnet Based - Modify] Mask_Bits (32) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6532][VLAN - Subnet Based - Modify] Mask_Bits ({driver.find_element(By.NAME,"rpsubnetbasedvlan_IptTextMaxbits").get_attribute("value")} != 32) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,"rpsubnetbasedvlan_IptTextVID").get_attribute("value") == "1" ):
                print(f"             [EMS1-6532][VLAN - Subnet Based - Modify] VID (1) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6532][VLAN - Subnet Based - Modify] VID ({driver.find_element(By.NAME,"rpsubnetbasedvlan_IptTextVID").get_attribute("value")} != 1) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,"rpsubnetbasedvlan_IptTextPri").get_attribute("value") == "0" ):
                print(f"             [EMS1-6532][VLAN - Subnet Based - Modify] Priority (0) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6532][VLAN - Subnet Based - Modify] Priority ({driver.find_element(By.NAME,"rpsubnetbasedvlan_IptTextPri").get_attribute("value")} != 0) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            if_find = True
            break
    if if_find == False:
        print(f"             [EMS1-6532][VLAN - Subnet Based - Modify] 'Name_Test_xxxxxxxxxxxxxxxxx_m_31' Not Found Test Fail",file = open(file_name, '+a'))   
        if_temp_error = True
    if(if_temp_error==False):
        print(f"             [EMS1-6532][VLAN - Subnet Based - Modify] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6532][VLAN - Subnet Based - Modify] Result Fail",file = open(file_name, '+a'))       

    #VLAN - Subnet Based Delete Result

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "VLAN").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)
    
    for i in range(1,driver.find_elements(By.NAME,"advance_vlan_subnet_profile_checkbox").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[17]/div[2]/div[1]/div[{i}]/div[3]").text
        if(ele == 'Name_Test_xxxxxxxxxxxxxxxxx_m_31'):
            driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[17]/div[2]/div[1]/div[{i}]/div[8]/label").click()
            time.sleep(1)
    driver.find_element(By.ID,"advance_vlan_subnet_profile_del_btn").click()

    #VLAN - Subnet Based Delete Result check
                
    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"VLAN").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    mod.Switch_Specific_Frame(driver,0)
    driver.find_element(By.LINK_TEXT,"VLAN Port Setting").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    driver.switch_to.frame("main")
    driver.find_element(By.LINK_TEXT,"Subnet Based Vlan").click()
    time.sleep(1)
    if_temp_error = False

    for i in range(1,driver.find_elements(By.NAME,"rpsubnetbasedvlan_ChkDelete").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[4]/tbody/tr[{i*2}]/td[4]/div").text
        if(ele == 'Name_Test_xxxxxxxxxxxxxxxxx_m_31'):
            if_temp_error = True
    if(if_temp_error==False):
        print(f"             [EMS1-6533][VLAN - Subnet Based - Delete] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6533][VLAN - Subnet Based - Delete] Result Fail",file = open(file_name, '+a'))

    # [EMS1-6534][VLAN - Subnet Based - Page Switch] Result Pass

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "VLAN").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)
    for i in range(1,12):
        driver.find_element(By.ID,"advance_vlan_subnet_profile_new_btn").click()
        time.sleep(1)
        e_swi.VLAN_Subnet_Based(driver,True,"Name_Test_xxxxxxxxxxxxxxxxxxxx31",f"10.10.10.{i}","32","4094","7",file_name)
    
    driver.find_element(By.ID,"btnNextPage1").click()
    if(driver.find_element(By.XPATH,'//*[@id="advance_vlan_subnet_profile_table"]/div[2]/div[1]').text == "11"):
        print(f"             [EMS1-6534][VLAN - Subnet Based - Page Switch] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6534][VLAN - Subnet Based - Page Switch] Result Fail",file = open(file_name, '+a'))
    e_mod.Checkbox_EMS(driver,"advance_vlan_subnet_profile_checkbox",True)
    driver.find_element(By.ID,"advance_vlan_subnet_profile_del_btn").click()
    time.sleep(1)
    msg = e_swi.alert_accept_text(driver)
    try:
        e_pro.Close(driver)
    except:
        pass
    time.sleep(1)
    e_mod.Checkbox_EMS(driver,"advance_vlan_subnet_profile_checkbox",True)
    driver.find_element(By.ID,"advance_vlan_subnet_profile_del_btn").click()
    time.sleep(1)
    msg = e_swi.alert_accept_text(driver)
    try:
        e_pro.Close(driver)
    except:
        pass

   

    

    print(f"======================================================================================",file = open(file_name, '+a'))

    #VLAN - Protocol Based New Result

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "VLAN").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)
    driver.find_element(By.ID,"advance_vlan_protocol_profile_new_btn").click()
    e_swi.Protocol_Based_VLAN(driver,True,Eth_Name,"Name_Test_xxxxxxxxxxxxxxxxxxxx31","first","IP","4094","7",file_name)

    #VLAN - Protocol Based New Result check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"VLAN").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    mod.Switch_Specific_Frame(driver,0)
    driver.find_element(By.LINK_TEXT,"VLAN Port Setting").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    driver.switch_to.frame("main")
    driver.find_element(By.LINK_TEXT,"Protocol Based Vlan").click()
    time.sleep(1)
    if_find=False
    for i in range(1,driver.find_elements(By.NAME,"rpprotobasedvlan_ChkDelete").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[{i*2}]/td[5]/div").text
        if(ele == 'Name_Test_xxxxxxxxxxxxxxxxxxxx31'):
            driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[{i*2}]/td[2]/div/a").click()
            if_find=True
            time.sleep(1)
            if_temp_error = False
            if(driver.find_element(By.NAME,"rpprotobasedvlan_ChkActive").is_selected() == True ):
                print(f"             [EMS1-6535][VLAN - Protocol Based - New] Active (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6535][VLAN - Protocol Based - New] Active ({driver.find_element(By.NAME,"rpprotobasedvlan_ChkActive").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            
            if(driver.find_element(By.NAME,"rpprotobasedvlan_IptTextPort").get_attribute("value") == OLT_Eth_Port ):
                print(f"             [EMS1-6535][VLAN - Protocol Based - New] Port {OLT_Eth_Port} Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6535][VLAN - Protocol Based - New] Port {driver.find_element(By.NAME,"rpprotobasedvlan_IptTextPort").get_attribute("value")} != {OLT_Eth_Port} Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,"rpprotobasedvlan_IptTextName").get_attribute("value") == "Name_Test_xxxxxxxxxxxxxxxxxxxx31" ):
                print(f"             [EMS1-6535][VLAN - Protocol Based - New] Name (Name_Test_xxxxxxxxxxxxxxxxxxxx31) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6535][VLAN - Protocol Based - New] Name ({driver.find_element(By.NAME,"rpprotobasedvlan_IptTextName").get_attribute("value")} != Name_Test_xxxxxxxxxxxxxxxxxxxx31) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,"rpprotobasedvlan_RPgL2Protocol").is_selected() == True ):
                if(Select(driver.find_element(By.NAME,"rpprotobasedvlan_SltL2Protocol")).first_selected_option.get_attribute("text") == "IP" ):
                    print(f"             [EMS1-6535][VLAN - Protocol Based - New] ETH_Type (IP) Pass",file = open(file_name, '+a'))
                else:
                    print(f'             [EMS1-6535][VLAN - Protocol Based - New] ETH_Type ({driver.find_element(By.NAME,"rpprotobasedvlan_RPgL2Protocol").is_selected()} != IP) Fail',file = open(file_name, '+a'))
                    if_temp_error = True
            else:
                 if(driver.find_element(By.NAME,"rpprotobasedvlan_IptTextL2Protocol").get_attribute("value") == "ffff" ):
                    print(f"             [EMS1-6535][VLAN - Protocol Based - New] ETH_Type (ffff) Pass",file = open(file_name, '+a'))
                 else:
                    print(f'             [EMS1-6535][VLAN - Protocol Based - New] ETH_Type ({driver.find_element(By.NAME,"rpprotobasedvlan_IptTextL2Protocol").get_attribute("value")} != ffff) Fail',file = open(file_name, '+a'))
                    if_temp_error = True

            if(driver.find_element(By.NAME,"rpprotobasedvlan_IptTextVID").get_attribute("value") == "4094" ):
                print(f"             [EMS1-6535][VLAN - Protocol Based - New] VID (4094) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6535][VLAN - Protocol Based - New] VID ({driver.find_element(By.NAME,"rpprotobasedvlan_IptTextVID").get_attribute("value")} != 4094) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(Select(driver.find_element(By.NAME,"rpprotobasedvlan_SltPriority")).first_selected_option.get_attribute("text") == "7" ):
                print(f"             [EMS1-6535][VLAN - Protocol Based - New] Priority (7) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6535][VLAN - Protocol Based - New] Priority ({Select(driver.find_element(By.NAME,"rpprotobasedvlan_SltPriority")).first_selected_option.get_attribute("text")} != 7) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(if_temp_error==False):
                print(f"             [EMS1-6535][VLAN - Protocol Based - New] Result Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6535][VLAN - Protocol Based - New] Result Fail',file = open(file_name, '+a'))      
    if(if_find==False):
        print(f"             [EMS1-6535][VLAN - Protocol Based - New] Result Fail",file = open(file_name, '+a'))
    #VLAN - Protocol Based Modify Result

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "VLAN").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)
    if_find=False
    for i in range(1,driver.find_elements(By.NAME,"advance_vlan_protocol_profile_checkbox").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[20]/div[2]/div[1]/div[{i}]/div[4]").text
        if(ele == 'Name_Test_xxxxxxxxxxxxxxxxxxxx31'):
            if_find=True
            driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[20]/div[2]/div[1]/div[{i}]/div[8]/label").click()
            time.sleep(1)
            driver.find_element(By.ID,"advance_vlan_protocol_profile_mod_btn").click()
            e_swi.Protocol_Based_VLAN(driver,True,Eth_Name,"Name_Test_xxxxxxxxxxxxxxxxx_m_31","second","ffff","1","0",file_name)

    #VLAN - Protocol Based Modify Result check 
                
    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"VLAN").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    mod.Switch_Specific_Frame(driver,0)
    driver.find_element(By.LINK_TEXT,"VLAN Port Setting").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    driver.switch_to.frame("main")
    driver.find_element(By.LINK_TEXT,"Protocol Based Vlan").click()
    time.sleep(1)

    for i in range(1,driver.find_elements(By.NAME,"rpprotobasedvlan_ChkDelete").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[{i*2}]/td[5]/div").text
        if(ele == 'Name_Test_xxxxxxxxxxxxxxxxx_m_31'):
            driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[{i*2}]/td[2]/div/a").click()
            time.sleep(1)
            if_temp_error = False
            if(driver.find_element(By.NAME,"rpprotobasedvlan_ChkActive").is_selected() == True ):
                print(f"             [EMS1-6536][VLAN - Protocol Based - Modify] Active (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6536][VLAN - Protocol Based - Modify] Active ({driver.find_element(By.NAME,"rpprotobasedvlan_ChkActive").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            
            if(driver.find_element(By.NAME,"rpprotobasedvlan_IptTextPort").get_attribute("value") == OLT_Eth_Port ):
                print(f"             [EMS1-6536][VLAN - Protocol Based - Modify] Port {OLT_Eth_Port} Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6536][VLAN - Protocol Based - Modify] Port {driver.find_element(By.NAME,"rpprotobasedvlan_IptTextPort").get_attribute("value")} != {OLT_Eth_Port} Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,"rpprotobasedvlan_IptTextName").get_attribute("value") == "Name_Test_xxxxxxxxxxxxxxxxx_m_31" ):
                print(f"             [EMS1-6536][VLAN - Protocol Based - Modify] Name (Name_Test_xxxxxxxxxxxxxxxxx_m_31) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6536][VLAN - Protocol Based - Modify] Name ({driver.find_element(By.NAME,"rpprotobasedvlan_IptTextName").get_attribute("value")} != Name_Test_xxxxxxxxxxxxxxxxx_m_31) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,"rpprotobasedvlan_RPgL2Protocol").is_selected() == True ):
                if(Select(driver.find_element(By.NAME,"rpprotobasedvlan_SltL2Protocol")).first_selected_option.get_attribute("text") == "IP" ):
                    print(f"             [EMS1-6536][VLAN - Protocol Based - Modify] ETH_Type (IP) Pass",file = open(file_name, '+a'))
                else:
                    print(f'             [EMS1-6536][VLAN - Protocol Based - Modify] ETH_Type ({Select(driver.find_element(By.NAME,"rpprotobasedvlan_SltL2Protocol")).first_selected_option.get_attribute("text")} != IP) Fail',file = open(file_name, '+a'))
                    if_temp_error = True
            else:
                 if(driver.find_element(By.NAME,"rpprotobasedvlan_IptTextL2Protocol").get_attribute("value") == "ffff" ):
                    print(f"             [EMS1-6536][VLAN - Protocol Based - Modify] ETH_Type (ffff) Pass",file = open(file_name, '+a'))
                 else:
                    print(f'             [EMS1-6536][VLAN - Protocol Based - Modify] ETH_Type ({driver.find_element(By.NAME,"rpprotobasedvlan_IptTextL2Protocol").get_attribute("value")} != ffff) Fail',file = open(file_name, '+a'))
                    if_temp_error = True

            if(driver.find_element(By.NAME,"rpprotobasedvlan_IptTextVID").get_attribute("value") == "1" ):
                print(f"             [EMS1-6536][VLAN - Protocol Based - Modify] VID (1) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6536][VLAN - Protocol Based - Modify] VID ({driver.find_element(By.NAME,"rpprotobasedvlan_IptTextVID").get_attribute("value")} != 1) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(Select(driver.find_element(By.NAME,"rpprotobasedvlan_SltPriority")).first_selected_option.get_attribute("text") == "0" ):
                print(f"             [EMS1-6536][VLAN - Protocol Based - Modify] Priority (0) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6536][VLAN - Protocol Based - Modify] Priority ({Select(driver.find_element(By.NAME,"rpprotobasedvlan_SltPriority")).first_selected_option.get_attribute("text")} != 0) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(if_temp_error==False):
                print(f"             [EMS1-6536][VLAN - Protocol Based - Modify] Result Pass",file = open(file_name, '+a'))
            else:
                print(f"             [EMS1-6536][VLAN - Protocol Based - Modify] Result Fail",file = open(file_name, '+a'))      
    if(if_find==False):
        print(f"             [EMS1-6536][VLAN - Protocol Based - Modify] Result Fail",file = open(file_name, '+a'))
    #VLAN - Protocol Based Delete Result 

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "VLAN").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)
    if_find=False
    for i in range(1,driver.find_elements(By.NAME,"advance_vlan_protocol_profile_checkbox").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[20]/div[2]/div[1]/div[{i}]/div[4]").text
        if(ele == 'Name_Test_xxxxxxxxxxxxxxxxx_m_31'):
            if_find=True
            driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[20]/div[2]/div[1]/div[{i}]/div[8]/label").click()
            time.sleep(1)
            driver.find_element(By.ID,"advance_vlan_protocol_profile_del_btn").click()
            time.sleep(1)
            if(driver.find_element(By.XPATH,'//*[@id="message_text"]').text == 'Set fail.'):
                print(f"             [EMS1-6537][VLAN - Protocol Based - Delete] EMS Delete Fail",file = open(file_name, '+a'))
            break


    #VLAN - Protocol Based Delete Result check
    
    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"VLAN").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    mod.Switch_Specific_Frame(driver,0)
    driver.find_element(By.LINK_TEXT,"VLAN Port Setting").click()
    time.sleep(2)
    mod.Switch_Default(driver)
    driver.switch_to.frame("main")
    driver.find_element(By.LINK_TEXT,"Protocol Based Vlan").click()
    time.sleep(1)

    if_temp_error = False
    for i in range(1,driver.find_elements(By.NAME,"rpprotobasedvlan_ChkDelete").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[{i*2}]/td[5]/div").text
    if(ele == 'Name_Test_xxxxxxxxxxxxxxxxx_m_31'):
        if_temp_error = True
    if(if_temp_error==True and if_find==True):
        print(f"             [EMS1-6537][VLAN - Protocol Based - Delete] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6537][VLAN - Protocol Based - Delete] Result Fail",file = open(file_name, '+a'))


    #VLAN - Protocol Based Page Switch Result check

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "VLAN").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)

    for i in range(601,608):
        driver.find_element(By.ID,"advance_vlan_protocol_profile_new_btn").click()
        time.sleep(1)
        e_swi.Protocol_Based_VLAN(driver,True,Eth_Name,"Name_Test_xxxxxxxxxxxxxxxxxxxx31","second",f"{i}","4094","7",file_name)
    for i in range(608,612):
        driver.find_element(By.ID,"advance_vlan_protocol_profile_new_btn").click()
        time.sleep(1)
        e_swi.Protocol_Based_VLAN(driver,False,Pon_Name,"Name_Test_xxxxxxxxxxxxxxxxxxxx31","second",f"{i}","4094","7",file_name)
    
    driver.find_element(By.ID,"btnNextPage2").click()
    if(driver.find_element(By.XPATH,'//*[@id="advance_vlan_protocol_profile_table"]/div[2]/div[1]').text == "11"):
        print(f"             [EMS1-6538][VLAN - Protocol Based - Page Switch] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6538][VLAN - Protocol Based - Page Switch] Result Fail",file = open(file_name, '+a'))
    e_mod.Checkbox_EMS(driver,"advance_vlan_protocol_profile_checkbox",True)
    driver.find_element(By.ID,"advance_vlan_protocol_profile_del_btn").click()
    time.sleep(1)
    msg = e_swi.alert_accept_text(driver)
    try:
        e_pro.Close(driver)
    except:
        pass
    time.sleep(1)
    e_mod.Checkbox_EMS(driver,"advance_vlan_protocol_profile_checkbox",True)
    driver.find_element(By.ID,"advance_vlan_protocol_profile_del_btn").click()
    time.sleep(1)
    msg = e_swi.alert_accept_text(driver)
    try:
        e_pro.Close(driver)
    except:
        pass

    print(f"======================================================================================",file = open(file_name, '+a'))

    #VLAN - Static VLAN New Result

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "VLAN").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)
    driver.find_element(By.ID,"advance_vlan_static_profile_new_btn").click()
    time.sleep(1)
    e_swi.VLAN_Static_VLAN(driver,True,"Name_Test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx64","4094","Forbidden","UnTagging",file_name)
    
    #VLAN - Static VLAN New Result check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"VLAN").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    mod.Switch_Specific_Frame(driver,0)
    driver.find_element(By.LINK_TEXT,"Static VLAN").click()
    mod.Switch_Default(driver)
    driver.switch_to.frame("main")
    time.sleep(1)
    if_find=False
    for i in range(1,driver.find_elements(By.NAME,"rpvlantag_ChkDel").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table[4]/tbody/tr[{(2*i)+1}]/td[2]/div/a").text
        # if(ele == 'Name_Test_xxxxxxxxxxxxxxxxxxxx32'):
        if(ele == '4094'):
            driver.find_element(By.XPATH,f"/html/body/form/table[4]/tbody/tr[{(2*i)+1}]/td[2]/div/a").click()
            time.sleep(1)
            if_temp_error = False
            if_find=True
            if(driver.find_element(By.NAME,"rpvlantag_ChkActive").is_selected() == True ):
                print(f"             [EMS1-6539][VLAN - Static VLAN - New] Active (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6539][VLAN - Static VLAN - New] Active ({driver.find_element(By.NAME,"rpvlantag_ChkActive").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,"rpvlantag_IptName").get_attribute("value") == "Name_Test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx64" ):
                print(f"             [EMS1-6539][VLAN - Static VLAN - New] Name (Name_Test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx64) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6539][VLAN - Static VLAN - New] Name ({driver.find_element(By.NAME,"rpvlantag_IptName").get_attribute("value")} != Name_Test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx64) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,"rpvlantag_IptGroupID").get_attribute("value") == "4094" ):
                print(f"             [EMS1-6539][VLAN - Static VLAN - New] VLAN_ID (4094) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6539][VLAN - Static VLAN - New] VLAN_ID ({driver.find_element(By.NAME,"rpvlantag_IptGroupID").get_attribute("value")} != 4094) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if_click=False
            for i in range(2,18):
                if(driver.find_element(By.XPATH,f"/html/body/form/table[2]/tbody/tr[{(2*i)+1}]/td[3]/table/tbody/tr/td[2]/input").is_selected() == False):
                    print(f'             [EMS1-6539][VLAN - Static VLAN - New] Control ({i} != True) Fail',file = open(file_name, '+a'))
                    if_click=True
                    if_temp_error = True
            if(if_click==False):
                print(f"             [EMS1-6539][VLAN - Static VLAN - New] Control Pass",file = open(file_name, '+a'))

            if_click=False
            for i in range(2,18):
                if(driver.find_element(By.XPATH,f"/html/body/form/table[2]/tbody/tr[{(2*i)+1}]/td[4]/div/input").is_selected() == True):
                    print(f'             [EMS1-6539][VLAN - Static VLAN - New] Tagging ({i} != False) Fail',file = open(file_name, '+a'))
                    if_click=True
                    if_temp_error = True
            if(if_click==False):
                print(f"             [EMS1-6539][VLAN - Static VLAN - New] Tagging Pass",file = open(file_name, '+a'))
            
            if(if_temp_error==False):
                print(f"             [EMS1-6539][VLAN - Static VLAN - New] Result Pass",file = open(file_name, '+a'))
            else:
                print(f"             [EMS1-6539][VLAN - Static VLAN - New] Result Fail",file = open(file_name, '+a'))
    if(if_find==False):
        print(f"             [EMS1-6539][VLAN - Static VLAN - New] Result Fail",file = open(file_name, '+a'))

    #VLAN - Static VLAN Modify Result
    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "VLAN").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)
    if_find=False
    for i in range(1,driver.find_elements(By.NAME,"advance_vlan_static_profile_checkbox").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[23]/div[2]/div[1]/div[{i}]/div[3]").text
        if(ele == '4094'):
            if_find=True
            driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[23]/div[2]/div[1]/div[{i}]/div[5]/label").click()
            time.sleep(1)
            driver.find_element(By.ID,"advance_vlan_static_profile_mod_btn").click()
            e_swi.VLAN_Static_VLAN(driver,True,"Name_Test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_m_64","4094","Fixed","Tagging",file_name)

    #VLAN - Static VLAN Modify Result check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"VLAN").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    mod.Switch_Specific_Frame(driver,0)
    driver.find_element(By.LINK_TEXT,"Static VLAN").click()
    mod.Switch_Default(driver)
    driver.switch_to.frame("main")
    time.sleep(1)

    for i in range(1,driver.find_elements(By.NAME,"rpvlantag_ChkDel").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table[4]/tbody/tr[{(2*i)+1}]/td[2]/div/a").text
        # if(ele == 'Name_Test_xxxxxxxxxxxxxxxxxxxx32'):
        if(ele == '4094'):
            driver.find_element(By.XPATH,f"/html/body/form/table[4]/tbody/tr[{(2*i)+1}]/td[2]/div/a").click()
            time.sleep(1)
            if_temp_error = False
            if(driver.find_element(By.NAME,"rpvlantag_ChkActive").is_selected() == True ):
                print(f"             [EMS1-6540][VLAN - Static VLAN - Modify] Active (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6540][VLAN - Static VLAN - Modify] Active ({driver.find_element(By.NAME,"rpvlantag_ChkActive").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,"rpvlantag_IptName").get_attribute("value") == "Name_Test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_m_64" ):
                print(f"             [EMS1-6540][VLAN - Static VLAN - Modify] Name (Name_Test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_m_64) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6540][VLAN - Static VLAN - Modify] Name ({driver.find_element(By.NAME,"rpvlantag_IptName").get_attribute("value")} != Name_Test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_m_64) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,"rpvlantag_IptGroupID").get_attribute("value") == "4094" ):
                print(f"             [EMS1-6540][VLAN - Static VLAN - Modify] VLAN_ID (4094) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6540][VLAN - Static VLAN - Modify] VLAN_ID ({driver.find_element(By.NAME,"rpvlantag_IptGroupID").get_attribute("value")} != 4094) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if_click=False
            for i in range(2,18):
                if(driver.find_element(By.XPATH,f"/html/body/form/table[2]/tbody/tr[{(2*i)+1}]/td[3]/table/tbody/tr/td[1]/input").is_selected() == False):
                    print(f'             [EMS1-6540][VLAN - Static VLAN - Modify] Control ({i} != True) Fail',file = open(file_name, '+a'))
                    if_click=True
                    if_temp_error = True
            if(if_click==False):
                print(f"             [EMS1-6540][VLAN - Static VLAN - Modify] Control Pass",file = open(file_name, '+a'))

            if_click=False
            for i in range(2,18):
                if(driver.find_element(By.XPATH,f"/html/body/form/table[2]/tbody/tr[{(2*i)+1}]/td[4]/div/input").is_selected() == False):
                    print(f'             [EMS1-6540][VLAN - Static VLAN - Modify] Tagging ({i} != True) Fail',file = open(file_name, '+a'))
                    if_click=True
                    if_temp_error = True
            if(if_click==False):
                print(f"             [EMS1-6540][VLAN - Static VLAN - Modify] Tagging Pass",file = open(file_name, '+a'))    
                
            if(if_temp_error==False):
                print(f"             [EMS1-6540][VLAN - Static VLAN - Modify] Result Pass",file = open(file_name, '+a'))
            else:
                print(f"             [EMS1-6540][VLAN - Static VLAN - Modify] Result Fail",file = open(file_name, '+a'))
    if(if_find==False):    
        print(f"             [EMS1-6540][VLAN - Static VLAN - Modify] Result Fail",file = open(file_name, '+a'))
    #VLAN - Static VLAN Delete Result

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "VLAN").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)
    if_find=False
    for i in range(1,driver.find_elements(By.NAME,"advance_vlan_static_profile_checkbox").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[23]/div[2]/div[1]/div[{i}]/div[3]").text
        if(ele == '4094'):
            if_find=True
            driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[23]/div[2]/div[1]/div[{i}]/div[5]/label").click()
            time.sleep(1)
            driver.find_element(By.ID,"advance_vlan_static_profile_del_btn").click()



    #VLAN - Static VLAN Delete Result check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"VLAN").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    mod.Switch_Specific_Frame(driver,0)
    driver.find_element(By.LINK_TEXT,"Static VLAN").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    driver.switch_to.frame("main")
    if_temp_error = False
    for i in range(1,driver.find_elements(By.NAME,"rpvlantag_ChkDel").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table[4]/tbody/tr[{(2*i)+1}]/td[2]/div/a").text
        if(ele == '4094'):
            if_temp_error = True
    if(if_temp_error==False and if_find==True):
        print(f"             [EMS1-6541][VLAN - Static VLAN - Delete] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6541][VLAN - Static VLAN - Delete] Result Fail",file = open(file_name, '+a'))

    #[EMS1-6542][VLAN - Static VLAN - Page Switch]

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "VLAN").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)
    for i in range(11,22):
        driver.find_element(By.ID,"advance_vlan_static_profile_new_btn").click()
        time.sleep(1)
        e_swi.VLAN_Static_VLAN(driver,True,"Name_Test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx64",f"{i}","Forbidden","UnTagging",file_name)
    driver.find_element(By.ID,'btnNextPage3').click()
    time.sleep(1)
    if(driver.find_element(By.XPATH,'//*[@id="advance_vlan_static_profile_table"]/div[2]/div[1]').text == "11"):
        print(f"             [EMS1-6542][VLAN - Static VLAN - Page Switch] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6542][VLAN - Static VLAN - Page Switch] Result Fail",file = open(file_name, '+a'))
    for i in range(1,3):
        for i in range(1,driver.find_elements(By.NAME,"advance_vlan_static_profile_checkbox").__len__()+1):
            ele = driver.find_element(By.XPATH,f'//*[@id="advance_vlan_static_profile_table"]/div[{i}]/div[4]').text
            if(ele == 'Name_Test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx64'):
                driver.find_element(By.XPATH,f'//*[@id="advance_vlan_static_profile_table"]/div[{i}]/div[5]/label').click()
        driver.find_element(By.ID,"advance_vlan_static_profile_del_btn").click()
        time.sleep(1)
        msg = e_swi.alert_accept_text(driver)
        try:
            e_pro.Close(driver)
        except:
            pass

        
    print(f"======================================================================================",file = open(file_name, '+a'))


@retry()
def Advanced_Static(driver,url,ems_url,file_name):
    #EMS [Advanced - Static Multicast] New Result 
    print(f"======================================================================================",file = open(file_name, '+a'))
    print(f"Advanced Application - Static Multicast Forwarding Test Start",file = open(file_name, '+a'))

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Static Multicast Forwarding").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    driver.find_element(By.ID,"advance_staticmulticastforward_profile_new_btn").click()
    e_swi.Advanced_Static_Multicast(driver,True,"01:00:5E:00:00:01","4094","8")

    #192.168.169.207 [Advanced - Static Multicast] New Result check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"Static Multicast Forwarding").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    time.sleep(1)
    for i in range(1,driver.find_elements(By.NAME,"rpmcastfwd_ChkDelete").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[{i*2}]/td[6]/div").text
        if(ele == '4094'):
            driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[{i*2}]/td[2]/div/a").click()
            time.sleep(1)
    if_temp_error = False
    if_MAC_error  =  False
    if(driver.find_element(By.NAME,"rpmcastfwd_ChkActive").is_selected() == True ):
        print(f"             [EMS1-6453][Advanced - Static Multicast - New] Active (True) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6453][Advanced - Static Multicast - New] Active ({driver.find_element(By.NAME,"rpmcastfwd_ChkActive").is_selected()} != True) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(driver.find_element(By.NAME,"rpmcastfwd_IptTextMacAddr1").get_attribute("value") != "01" ):
        print(f'             [EMS1-6453][Advanced - Static Multicast - New] MAC_1 ({driver.find_element(By.NAME,"rpmcastfwd_IptTextMacAddr1").get_attribute("value")} != 01) Fail',file = open(file_name, '+a'))
        if_temp_error = True
        if_MAC_error  = True
    if(driver.find_element(By.NAME,"rpmcastfwd_IptTextMacAddr2").get_attribute("value") != "00" ):
        print(f'             [EMS1-6453][Advanced - Static Multicast - New] MAC_2 ({driver.find_element(By.NAME,"rpmcastfwd_IptTextMacAddr2").get_attribute("value")} != 00) Fail',file = open(file_name, '+a'))
        if_temp_error = True
        if_MAC_error  = True
    if(driver.find_element(By.NAME,"rpmcastfwd_IptTextMacAddr3").get_attribute("value") != "5e" ):
        print(f'             [EMS1-6453][Advanced - Static Multicast - New] MAC_3 ({driver.find_element(By.NAME,"rpmcastfwd_IptTextMacAddr3").get_attribute("value")} != 5e) Fail',file = open(file_name, '+a'))
        if_temp_error = True
        if_MAC_error  = True
    if(driver.find_element(By.NAME,"rpmcastfwd_IptTextMacAddr4").get_attribute("value") != "00" ):
        print(f'             [EMS1-6453][Advanced - Static Multicast - New] MAC_4 ({driver.find_element(By.NAME,"rpmcastfwd_IptTextMacAddr4").get_attribute("value")} != 00) Fail',file = open(file_name, '+a'))
        if_temp_error = True
        if_MAC_error  = True
    if(driver.find_element(By.NAME,"rpmcastfwd_IptTextMacAddr5").get_attribute("value") != "00" ):
        print(f'             [EMS1-6453][Advanced - Static Multicast - New] MAC_5 ({driver.find_element(By.NAME,"rpmcastfwd_IptTextMacAddr5").get_attribute("value")} != 00) Fail',file = open(file_name, '+a'))
        if_temp_error = True
        if_MAC_error  = True
    if(driver.find_element(By.NAME,"rpmcastfwd_IptTextMacAddr6").get_attribute("value") != "01" ):
        print(f'             [EMS1-6453][Advanced - Static Multicast - New] MAC_6 ({driver.find_element(By.NAME,"rpmcastfwd_IptTextMacAddr6").get_attribute("value")} != 01) Fail',file = open(file_name, '+a'))
        if_temp_error = True
        if_MAC_error  = True
    if(if_MAC_error == False):
        print(f"             [EMS1-6453][Advanced - Static Multicast - New] MAC Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6453][Advanced - Static Multicast - New] MAC Fail',file = open(file_name, '+a'))

    if(driver.find_element(By.NAME,"rpmcastfwd_IptTextVID").get_attribute("value") == "4094" ):
        print(f"             [EMS1-6453][Advanced - Static Multicast - New] VID (4094) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6453][Advanced - Static Multicast - New] VID ({driver.find_element(By.NAME,"rpmcastfwd_IptTextVID").get_attribute("value")} != 4094) fail',file = open(file_name, '+a'))
        if_temp_error = True
       
    if(driver.find_element(By.NAME,"rpmcastfwd_IptTextPort").get_attribute("value") == "8" ):
        print(f"             [EMS1-6453][Advanced - Static Multicast - New] Port (8) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6453][Advanced - Static Multicast - New] Port ({driver.find_element(By.NAME,"rpmcastfwd_IptTextPort").get_attribute("value")} != 8) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(if_temp_error == False):
        print(f"             [EMS1-6453][Advanced - Static Multicast - New] Result Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6453][Advanced - Static Multicast - New] Result Fail',file = open(file_name, '+a'))
    
    #EMS [Advanced - Static Multicast] Modify Result

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Static Multicast Forwarding").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    if_find = False
    for i in range(1,int(driver.find_element(By.ID,"pageTotal").text)+1):
        for j in range(1,driver.find_elements(By.NAME,"advance_staticmulticastforward_profile_checkbox").__len__()+1):
            ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[3]/div[1]/div[{j}]/div[4]").text
            if(ele == '4094'):
                driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[3]/div[1]/div[{j}]/div[6]/label").click()
                if_find =True
                time.sleep(1)
            if(if_find==True):
                break
        if(if_find==True):
            break 
        else:
            driver.find_element(By.ID,"btnNextPage").click()
    driver.find_element(By.ID,"advance_staticmulticastforward_profile_mod_btn").click()
    e_swi.Advanced_Static_Multicast(driver,True,"01:00:5E:00:00:01","4094","1,8")

    #192.168.169.207 [Advanced - Static Multicast] Modify Result check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"Static Multicast Forwarding").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    time.sleep(1)
    for i in range(1,driver.find_elements(By.NAME,"rpmcastfwd_ChkDelete").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[{i*2}]/td[6]/div").text
        if(ele == '4094'):
            driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[{i*2}]/td[2]/div/a").click()
            time.sleep(1)
    if_temp_error = False
    if_MAC_error  =  False
    if(driver.find_element(By.NAME,"rpmcastfwd_ChkActive").is_selected() == True ):
        print(f"             [EMS1-6543][Advanced - Static Multicast - Modify] Active (True) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6543][Advanced - Static Multicast - Modify] Active ({driver.find_element(By.NAME,"rpmcastfwd_ChkActive").is_selected()} != True) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(driver.find_element(By.NAME,"rpmcastfwd_IptTextMacAddr1").get_attribute("value") != "01" ):
        print(f'             [EMS1-6543][Advanced - Static Multicast - Modify] MAC_1 ({driver.find_element(By.NAME,"rpmcastfwd_IptTextMacAddr1").get_attribute("value")} != 01) Fail',file = open(file_name, '+a'))
        if_temp_error = True
        if_MAC_error  = True
    if(driver.find_element(By.NAME,"rpmcastfwd_IptTextMacAddr2").get_attribute("value") != "00" ):
        print(f'             [EMS1-6543][Advanced - Static Multicast - Modify] MAC_2 ({driver.find_element(By.NAME,"rpmcastfwd_IptTextMacAddr2").get_attribute("value")} != 00) Fail',file = open(file_name, '+a'))
        if_temp_error = True
        if_MAC_error  = True
    if(driver.find_element(By.NAME,"rpmcastfwd_IptTextMacAddr3").get_attribute("value") != "5e" ):
        print(f'             [EMS1-6543][Advanced - Static Multicast - Modify] MAC_3 ({driver.find_element(By.NAME,"rpmcastfwd_IptTextMacAddr3").get_attribute("value")} != 5e) Fail',file = open(file_name, '+a'))
        if_temp_error = True
        if_MAC_error  = True
    if(driver.find_element(By.NAME,"rpmcastfwd_IptTextMacAddr4").get_attribute("value") != "00" ):
        print(f'             [EMS1-6543][Advanced - Static Multicast - Modify] MAC_4 ({driver.find_element(By.NAME,"rpmcastfwd_IptTextMacAddr4").get_attribute("value")} != 00) Fail',file = open(file_name, '+a'))
        if_temp_error = True
        if_MAC_error  = True
    if(driver.find_element(By.NAME,"rpmcastfwd_IptTextMacAddr5").get_attribute("value") != "00" ):
        print(f'             [EMS1-6543][Advanced - Static Multicast - Modify] MAC_5 ({driver.find_element(By.NAME,"rpmcastfwd_IptTextMacAddr5").get_attribute("value")} != 00) Fail',file = open(file_name, '+a'))
        if_temp_error = True
        if_MAC_error  = True
    if(driver.find_element(By.NAME,"rpmcastfwd_IptTextMacAddr6").get_attribute("value") != "01" ):
        print(f'             [EMS1-6543][Advanced - Static Multicast - Modify] MAC_6 ({driver.find_element(By.NAME,"rpmcastfwd_IptTextMacAddr6").get_attribute("value")} != 01) Fail',file = open(file_name, '+a'))
        if_temp_error = True
        if_MAC_error  = True
    if(if_MAC_error == False):
        print(f"             [EMS1-6543][Advanced - Static Multicast - Modify] MAC Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6543][Advanced - Static Multicast - Modify] MAC Fail',file = open(file_name, '+a'))

    if(driver.find_element(By.NAME,"rpmcastfwd_IptTextVID").get_attribute("value") == "4094" ):
        print(f"             [EMS1-6543][Advanced - Static Multicast - Modify] VID (4094) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6543][Advanced - Static Multicast - Modify] VID ({driver.find_element(By.NAME,"rpmcastfwd_IptTextVID").get_attribute("value")} != 4094) fail',file = open(file_name, '+a'))
        if_temp_error = True
       
    if(driver.find_element(By.NAME,"rpmcastfwd_IptTextPort").get_attribute("value") == "1,8" ):
        print(f"             [EMS1-6543][Advanced - Static Multicast - Modify] Port (1,8) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6543][Advanced - Static Multicast - Modify] Port ({driver.find_element(By.NAME,"rpmcastfwd_IptTextPort").get_attribute("value")} != 1,8) fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(if_temp_error == False):
        print(f"             [EMS1-6543][Advanced - Static Multicast - Modify] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6543][Advanced - Static Multicast - Modify] Result Fail",file = open(file_name, '+a'))

    #EMS [Advanced - Static Multicast] Delete Result

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Static Multicast Forwarding").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    if_find = False
    for i in range(1,int(driver.find_element(By.ID,"pageTotal").text)+1):
        for j in range(1,driver.find_elements(By.NAME,"advance_staticmulticastforward_profile_checkbox").__len__()+1):
            ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[3]/div[1]/div[{j}]/div[4]").text
            if(ele == '4094'):
                driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[3]/div[1]/div[{j}]/div[6]/label").click()
                if_find =True
                time.sleep(1)
            if(if_find==True):
                break
        if(if_find==True):
            break 
        else:
            driver.find_element(By.ID,"btnNextPage").click()
    driver.find_element(By.ID,"advance_staticmulticastforward_profile_del_btn").click()

    #192.168.169.207 [Advanced - Static Multicast] Delete Result check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"Static Multicast Forwarding").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    time.sleep(1)
    if_temp_error = False
    for i in range(1,driver.find_elements(By.NAME,"rpmcastfwd_ChkDelete").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[{i*2}]/td[6]/div").text
        if(ele == '4094'):
            if_temp_error = True
    if(if_temp_error==False):
        print(f"             [EMS1-6544][Advanced - Static Multicast - Delete] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6544][Advanced - Static Multicast - Delete] Result Fail",file = open(file_name, '+a'))

    #Static Multicast Forwarding Table Page Switch

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Static Multicast Forwarding").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    for i in range(1,12):
        driver.find_element(By.ID,"advance_staticmulticastforward_profile_new_btn").click()
        if(i >= 10):
            e_swi.Advanced_Static_Multicast(driver,True,f"01:00:5E:00:00:{i}","4094","8")
        else:
            e_swi.Advanced_Static_Multicast(driver,True,f"01:00:5E:00:00:0{i}","4094","8")
        time.sleep(1)
        msg = e_swi.alert_accept_text(driver)
        try:
            e_pro.Close(driver)
        except:
            pass
    driver.find_element(By.ID,'btnNextPage').click()
    time.sleep(1)
    if(driver.find_element(By.XPATH,'//*[@id="advance_staticmulticastforward_profile_table"]/div[2]/div[1]').text == "11"):
        print(f"             [EMS1-6545][Advanced - Static Multicast - Page Switch] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6545][Advanced - Static Multicast - Page Switch] Result Fail",file = open(file_name, '+a'))
    for i in range(1,3):
        e_mod.Checkbox_EMS(driver,"advance_staticmulticastforward_profile_checkbox",True)
        driver.find_element(By.ID,"advance_staticmulticastforward_profile_del_btn").click()
        time.sleep(1)
        msg = e_swi.alert_accept_text(driver)
        try:
            e_pro.Close(driver)
        except:
            pass
        time.sleep(1)

    

    print(f"======================================================================================",file = open(file_name, '+a'))            

@retry()
def Advanced_Filtering(driver,url,ems_url,file_name):
    # EMS [EMS1-6454][Advanced - Filtering - New] Result
    print(f"======================================================================================",file = open(file_name, '+a'))
    print(f"Advanced Application - Filtering Test Start",file = open(file_name, '+a'))
     
    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Filtering").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    driver.find_element(By.ID,"advance_filtering_profile_new_btn").click()
    time.sleep(1)
    e_swi.Advanced_Filtering(driver,True,"Name_Test_xxxxxxxxxxxxxxxxxxxx31","Discard source","00:01:02:03:04:05","4094")

    # 192.168.169.207 [EMS1-6454][Advanced - Filtering - New] Result check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"Filtering").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    time.sleep(1)

    for i in range(1,driver.find_elements(By.NAME,"rpfilter_ChkTabDelete").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td/table/tbody/tr[{i*2}]/td[4]/div").text
        if(ele == 'Name_Test_xxxxxxxxxxxxxxxxxxxx31'):
            driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td/table/tbody/tr[{i*2}]/td[2]/div/a").click()
            time.sleep(1)
    if_temp_error = False
    if_MAC_error  =  False
    if(driver.find_element(By.NAME,"rpfilter_ChkSwActive").is_selected() == True ):
        print(f"             [EMS1-6454][Advanced - Filtering - New] Active Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6454][Advanced - Filtering - New] Active Fail",file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpfilter_IptTextName").get_attribute("value") == "Name_Test_xxxxxxxxxxxxxxxxxxxx31" ):
        print(f"             [EMS1-6454][Advanced - Filtering - New] Name Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6454][Advanced - Filtering - New] Name Fail",file = open(file_name, '+a'))
        if_temp_error = True
       
    if(driver.find_element(By.NAME,"rpfilter_ChkSrcDiscard").is_selected() == True ):
        print(f"             [EMS1-6454][Advanced - Filtering - New] Action Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6454][Advanced - Filtering - New] Action Fail",file = open(file_name, '+a'))
        if_temp_error = True


    if(driver.find_element(By.NAME,"rpfilter_IptMacAddr1").get_attribute("value") != "00" ):
        print(f"             [EMS1-6454][Advanced - Filtering - New] MAC1 Fail",file = open(file_name, '+a'))
        if_temp_error = True
        if_MAC_error  = True
    if(driver.find_element(By.NAME,"rpfilter_IptMacAddr2").get_attribute("value") != "01" ):
        print(f"             [EMS1-6454][Advanced - Filtering - New] MAC2 Fail",file = open(file_name, '+a'))
        if_temp_error = True
        if_MAC_error  = True
    if(driver.find_element(By.NAME,"rpfilter_IptMacAddr3").get_attribute("value") != "02" ):
        print(f"             [EMS1-6454][Advanced - Filtering - New] MAC3 Fail",file = open(file_name, '+a'))
        if_temp_error = True
        if_MAC_error  = True
    if(driver.find_element(By.NAME,"rpfilter_IptMacAddr4").get_attribute("value") != "03" ):
        print(f"             [EMS1-6454][Advanced - Filtering - New] MAC4 Fail",file = open(file_name, '+a'))
        if_temp_error = True
        if_MAC_error  = True
    if(driver.find_element(By.NAME,"rpfilter_IptMacAddr5").get_attribute("value") != "04" ):
        print(f"             [EMS1-6454][Advanced - Filtering - New] MAC5 Fail",file = open(file_name, '+a'))
        if_temp_error = True
        if_MAC_error  = True
    if(driver.find_element(By.NAME,"rpfilter_IptMacAddr6").get_attribute("value") != "05" ):
        print(f"             [EMS1-6454][Advanced - Filtering - New] MAC6 Fail",file = open(file_name, '+a'))
        if_temp_error = True
        if_MAC_error  = True
    if(if_MAC_error == False):
        print(f"             [EMS1-6454][Advanced - Filtering - New] MAC Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6454][Advanced - Filtering - New] MAC Fail",file = open(file_name, '+a'))

    if(driver.find_element(By.NAME,"rpfilter_IptVID").get_attribute("value") == "4094" ):
        print(f"             [EMS1-6454][Advanced - Filtering - New] VID Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6454][Advanced - Filtering - New] VID Fail",file = open(file_name, '+a'))
        if_temp_error = True

    if(if_temp_error == False):
        print(f"             [EMS1-6454][Advanced - Filtering - New] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6454][Advanced - Filtering - New] Result Fail",file = open(file_name, '+a'))

    # EMS [EMS1-6454][Advanced - Filtering] Modify Result

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Filtering").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    if_find = False
    for i in range(1,int(driver.find_element(By.ID,"pageTotal").text)+1):
        for j in range(1,driver.find_elements(By.NAME,"advance_filtering_profile_checkbox").__len__()+1):
            ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[3]/div[1]/div[{j}]/div[3]").text
            if(ele == 'Name_Test_xxxxxxxxxxxxxxxxxxxx31'):
                driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[3]/div[1]/div[{j}]/div[7]/label").click()
                if_find =True
                time.sleep(1)
            if(if_find==True):
                break
        if(if_find==True):
            break 
        else:
            driver.find_element(By.ID,"btnNextPage").click()
    driver.find_element(By.ID,"advance_filtering_profile_mod_btn").click()
    time.sleep(1)
    e_swi.Advanced_Filtering(driver,True,"Name_Test_xxxxxxxxxxxxxxxxx_m_31","Discard both","00:01:02:03:04:05","4094")


    # 192.168.169.207 [EMS1-6454][Advanced - Filtering] Modify Result check
    
    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"Filtering").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    time.sleep(1)

    for i in range(1,driver.find_elements(By.NAME,"rpfilter_ChkTabDelete").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td/table/tbody/tr[{i*2}]/td[4]/div").text
        if(ele == 'Name_Test_xxxxxxxxxxxxxxxxx_m_31'):
            driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td/table/tbody/tr[{i*2}]/td[2]/div/a").click()
            time.sleep(1)
    if_temp_error = False
    if_MAC_error  =  False
    if(driver.find_element(By.NAME,"rpfilter_ChkSwActive").is_selected() == True ):
        print(f"             [EMS1-6546][Advanced - Filtering - Modify] Active Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6546][Advanced - Filtering - Modify] Active Fail",file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpfilter_IptTextName").get_attribute("value") == "Name_Test_xxxxxxxxxxxxxxxxx_m_31" ):
        print(f"             [EMS1-6546][Advanced - Filtering - Modify] Name Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6546][Advanced - Filtering - Modify] Name Fail",file = open(file_name, '+a'))
        if_temp_error = True
       
    if(driver.find_element(By.NAME,"rpfilter_ChkSrcDiscard").is_selected() == True  and driver.find_element(By.NAME,"rpfilter_ChkDestDiscard").is_selected() == True):
        print(f"             [EMS1-6546][Advanced - Filtering - Modify] Action Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6546][Advanced - Filtering - Modify] Action Fail",file = open(file_name, '+a'))
        if_temp_error = True


    if(driver.find_element(By.NAME,"rpfilter_IptMacAddr1").get_attribute("value") != "00" ):
        print(f"             [EMS1-6546][Advanced - Filtering - Modify] MAC1 Fail",file = open(file_name, '+a'))
        if_temp_error = True
        if_MAC_error  = True
    if(driver.find_element(By.NAME,"rpfilter_IptMacAddr2").get_attribute("value") != "01" ):
        print(f"             [EMS1-6546][Advanced - Filtering - Modify] MAC2 Fail",file = open(file_name, '+a'))
        if_temp_error = True
        if_MAC_error  = True
    if(driver.find_element(By.NAME,"rpfilter_IptMacAddr3").get_attribute("value") != "02" ):
        print(f"             [EMS1-6546][Advanced - Filtering - Modify] MAC3 Fail",file = open(file_name, '+a'))
        if_temp_error = True
        if_MAC_error  = True
    if(driver.find_element(By.NAME,"rpfilter_IptMacAddr4").get_attribute("value") != "03" ):
        print(f"             [EMS1-6546][Advanced - Filtering - Modify] MAC4 Fail",file = open(file_name, '+a'))
        if_temp_error = True
        if_MAC_error  = True
    if(driver.find_element(By.NAME,"rpfilter_IptMacAddr5").get_attribute("value") != "04" ):
        print(f"             [EMS1-6546][Advanced - Filtering - Modify] MAC5 Fail",file = open(file_name, '+a'))
        if_temp_error = True
        if_MAC_error  = True
    if(driver.find_element(By.NAME,"rpfilter_IptMacAddr6").get_attribute("value") != "05" ):
        print(f"             [EMS1-6546][Advanced - Filtering - Modify] MAC6 Fail",file = open(file_name, '+a'))
        if_temp_error = True
        if_MAC_error  = True
    if(if_MAC_error == False):
        print(f"             [EMS1-6546][Advanced - Filtering - Modify] MAC Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6546][Advanced - Filtering - Modify] MAC Fail",file = open(file_name, '+a'))

    if(driver.find_element(By.NAME,"rpfilter_IptVID").get_attribute("value") == "4094" ):
        print(f"             [EMS1-6546][Advanced - Filtering - Modify] VID Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6546][Advanced - Filtering - Modify] VID Fail",file = open(file_name, '+a'))
        if_temp_error = True

    if(if_temp_error == False):
        print(f"             [EMS1-6546][Advanced - Filtering - Modify] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6546][Advanced - Filtering - Modify] Result Fail",file = open(file_name, '+a'))

    # EMS [EMS1-6454][Advanced - Filtering] Delete Result 

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Filtering").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    if_find = False
    for i in range(1,int(driver.find_element(By.ID,"pageTotal").text)+1):
        for j in range(1,driver.find_elements(By.NAME,"advance_filtering_profile_checkbox").__len__()+1):
            ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[3]/div[1]/div[{j}]/div[3]").text
            if(ele == 'Name_Test_xxxxxxxxxxxxxxxxx_m_31'):
                driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[3]/div[1]/div[{j}]/div[7]/label").click()
                if_find =True
                time.sleep(1)
            if(if_find==True):
                break
        if(if_find==True):
            break 
        else:
            driver.find_element(By.ID,"btnNextPage").click()
    driver.find_element(By.ID,"advance_filtering_profile_del_btn").click()
    time.sleep(1)

    # 192.168.169.207 [EMS1-6454][Advanced - Filtering] Delete Result check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"Filtering").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    time.sleep(1)

    if_temp_error = False
    for i in range(1,driver.find_elements(By.NAME,"rpfilter_ChkTabDelete").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td/table/tbody/tr[{i*2}]/td[4]/div").text
        if(ele == 'Name_Test_xxxxxxxxxxxxxxxxx_m_31'):
            if_temp_error = True
    if(if_temp_error==False):
        print(f"             [EMS1-6547][Advanced - Filtering - Delete] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6547][Advanced - Filtering - Delete] Result Fail",file = open(file_name, '+a'))

    #[EMS1-6548][Advanced - Filtering - Page Switch]

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Filtering").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    for i in range(1,12):
        driver.find_element(By.ID,"advance_filtering_profile_new_btn").click()
        time.sleep(1)
        if(i<10):
            e_swi.Advanced_Filtering(driver,True,"Name_Test_xxxxxxxxxxxxxxxxxxxx31","Discard source",f"00:01:02:03:04:0{i}","4094")
        else:
            e_swi.Advanced_Filtering(driver,True,"Name_Test_xxxxxxxxxxxxxxxxxxxx31","Discard source",f"00:01:02:03:04:{i}","4094")
        msg = e_swi.alert_accept_text(driver)
        try:
            e_pro.Close(driver)
        except:
            pass
    driver.find_element(By.ID,'btnNextPage').click()
    if(driver.find_element(By.XPATH,'//*[@id="advance_filtering_profile_table"]/div[2]/div[1]').text == '11'):
        print(f"             [EMS1-6548][Advanced - Filtering - Page Switch] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6548][Advanced - Filtering - Page Switch] Result Fail",file = open(file_name, '+a'))
    for i in range(1,3):
        e_mod.Checkbox_EMS(driver,"advance_filtering_profile_checkbox",True)
        driver.find_element(By.ID,"advance_filtering_profile_del_btn").click()
        time.sleep(1)
        msg = e_swi.alert_accept_text(driver)
        try:
            e_pro.Close(driver)
        except:
            pass

    print(f"======================================================================================",file = open(file_name, '+a'))            

@retry()
def Advanced_Broadcast(driver,url,ems_url,file_name,Pon_Name,Eth_Name,Pon_Name_L,Eth_Name_L):
    #EMS [EMS1-6455][Advanced - Broadcast Storm Control - Active Apply] Result 
    #EMS [EMS1-6549][Advanced - Broadcast Storm Control - Port] Port Apply Result
    print(f"======================================================================================",file = open(file_name, '+a'))
    print(f"Advanced Application - Broadcast Storm Control Test Start",file = open(file_name, '+a'))

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Broadcast Storm Control").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    e_swi.Advanced_Broadcast_Apply(driver,True,file_name)
    e_swi.Advanced_Broadcast_port_Apply(driver,Pon_Name,True,True,True,"262143",True,"262143",True,"262143",file_name)
    e_swi.Advanced_Broadcast_port_Apply(driver,Eth_Name,True,True,True,"262143",True,"262143",True,"262143",file_name)

    #192.168.169.207 [EMS1-6455][Advanced - Broadcast Storm Control - Active Apply] Result check
    #192.168.169.207 [EMS1-6549][Advanced - Broadcast Storm Control - Port] Port Apply Result check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"Broadcast Storm Control").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    time.sleep(1)

    if_temp_error = False
    if(driver.find_element(By.NAME,"rpbcaststorm_ChkActive").is_selected() == True ):
        print(f"             [EMS1-6455][Advanced - Broadcast Storm Control - Active Apply] Result (True) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6455][Advanced - Broadcast Storm Control - Active Apply] Result ({driver.find_element(By.NAME,"rpbcaststorm_ChkActive").is_selected()} != True) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(if_temp_error == False):
        print(f"             [EMS1-6455][Advanced - Broadcast Storm Control - Active Apply] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6455][Advanced - Broadcast Storm Control - Active Apply] Result Fail",file = open(file_name, '+a'))
    print(f"--------------------------------------------------------------------------------------",file = open(file_name, '+a'))
    if_temp_error = False
    for i in range(1,driver.find_elements(By.NAME,"rpbcaststorm_ChkEnCounter").__len__()+1):
        if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[2]/div").text == Pon_Name_L):
            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[3]/div/input").is_selected() == True ):
                print(f"             [EMS1-6549][Advanced - Broadcast Storm Control - Port] {Pon_Name} Counter Result (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6549][Advanced - Broadcast Storm Control - Port] {Pon_Name} Counter Result ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[3]/div/input").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[4]/div/input").is_selected() == True ):
                print(f"             [EMS1-6549][Advanced - Broadcast Storm Control - Port] {Pon_Name} Logging Result (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6549][Advanced - Broadcast Storm Control - Port] {Pon_Name} Logging Result ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[4]/div/input").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            
            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[5]/div/input[1]").is_selected() == True ):
                print(f"             [EMS1-6549][Advanced - Broadcast Storm Control - Port] {Pon_Name} Broadcast_Apply Result (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6549][Advanced - Broadcast Storm Control - Port] {Pon_Name} Broadcast_Apply Result ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[5]/div/input[1]").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[5]/div/input[2]").get_attribute("value") == "262143" ):
                print(f"             [EMS1-6549][Advanced - Broadcast Storm Control - Port] {Pon_Name} Broadcast Result (262143) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6549][Advanced - Broadcast Storm Control - Port] {Pon_Name} Broadcast Result ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[5]/div/input[2]").get_attribute("value")} != 262143) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[6]/div/input[1]").is_selected() == True ):
                print(f"             [EMS1-6549][Advanced - Broadcast Storm Control - Port] {Pon_Name} Multicast_Apply Result (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6549][Advanced - Broadcast Storm Control - Port] {Pon_Name} Multicast_Apply Result ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[6]/div/input[1]").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[6]/div/input[2]").get_attribute("value") == "262143" ):
                print(f"             [EMS1-6549][Advanced - Broadcast Storm Control - Port] {Pon_Name} Multicast Result (262143) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6549][Advanced - Broadcast Storm Control - Port] {Pon_Name} Multicast Result ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[6]/div/input[2]").get_attribute("value")} != 262143) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[7]/div/input[1]").is_selected() == True ):
                print(f"             [EMS1-6549][Advanced - Broadcast Storm Control - Port] {Pon_Name} DLF_Apply Result (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6549][Advanced - Broadcast Storm Control - Port] {Pon_Name} DLF_Apply Result ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[7]/div/input[1]").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[7]/div/input[2]").get_attribute("value") == "262143" ):
                print(f"             [EMS1-6549][Advanced - Broadcast Storm Control - Port] {Pon_Name} DLF Result (262143) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6549][Advanced - Broadcast Storm Control - Port] {Pon_Name} DLF Result ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[7]/div/input[2]").get_attribute("value")} != 262143) Fail',file = open(file_name, '+a'))
                if_temp_error = True

    for i in range(1,driver.find_elements(By.NAME,"rpbcaststorm_ChkEnCounter").__len__()+1):
        if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[2]/div").text == Eth_Name_L):

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[3]/div/input").is_selected() == True ):
                print(f"             [EMS1-6549][Advanced - Broadcast Storm Control - Port] {Eth_Name} Counter Result (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6549][Advanced - Broadcast Storm Control - Port] {Eth_Name} Counter Result ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[3]/div/input").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[4]/div/input").is_selected() == True ):
                print(f"             [EMS1-6549][Advanced - Broadcast Storm Control - Port] {Eth_Name} Logging Result (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6549][Advanced - Broadcast Storm Control - Port] {Eth_Name} Logging Result ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[4]/div/input").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            
            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[5]/div/input[1]").is_selected() == True ):
                print(f"             [EMS1-6549][Advanced - Broadcast Storm Control - Port] {Eth_Name} Broadcast_Apply Result (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6549][Advanced - Broadcast Storm Control - Port] {Eth_Name} Broadcast_Apply Result ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[5]/div/input[1]").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[5]/div/input[2]").get_attribute("value") == "262143" ):
                print(f"             [EMS1-6549][Advanced - Broadcast Storm Control - Port] {Eth_Name} Broadcast Result (262143) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6549][Advanced - Broadcast Storm Control - Port] {Eth_Name} Broadcast Result ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[5]/div/input[2]").get_attribute("value")} != 262143) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[6]/div/input[1]").is_selected() == True ):
                print(f"             [EMS1-6549][Advanced - Broadcast Storm Control - Port] {Eth_Name} Multicast_Apply Result (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6549][Advanced - Broadcast Storm Control - Port] {Eth_Name} Multicast_Apply Result ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[6]/div/input[1]").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[6]/div/input[2]").get_attribute("value") == "262143" ):
                print(f"             [EMS1-6549][Advanced - Broadcast Storm Control - Port] {Eth_Name} Multicast Result (262143) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6549][Advanced - Broadcast Storm Control - Port] {Eth_Name} Multicast Result ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[6]/div/input[2]").get_attribute("value")} != 262143) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[7]/div/input[1]").is_selected() == True ):
                print(f"             [EMS1-6549][Advanced - Broadcast Storm Control - Port] {Eth_Name} DLF_Apply Result (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6549][Advanced - Broadcast Storm Control - Port] {Eth_Name} DLF_Apply Result ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[7]/div/input[1]").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[7]/div/input[2]").get_attribute("value") == "262143" ):
                print(f"             [EMS1-6549][Advanced - Broadcast Storm Control - Port] {Eth_Name} DLF Result (262143) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6549][Advanced - Broadcast Storm Control - Port] {Eth_Name} DLF Result ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*(i+1))+1}]/td[7]/div/input[2]").get_attribute("value")} != 262143) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            
    if(if_temp_error == False):
        print(f"             [EMS1-6549][Advanced - Broadcast Storm Control - Port] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6549][Advanced - Broadcast Storm Control - Port] Result Fail",file = open(file_name, '+a'))

    print(f"======================================================================================",file = open(file_name, '+a'))

@retry()
def Advanced_Link(driver,url,ems_url,file_name,Pon_Name,Eth_Name,Pon_Name_L,Eth_Name_L):
    #[EMS1-6456][Advanced - Link Aggregation] Apply Result
    #[EMS1-6550][Advanced - Link Aggregation - Group]
    #[EMS1-6551][Advanced - Link Aggregation - Port Apply]
    print(f"======================================================================================",file = open(file_name, '+a'))
    print(f"Advanced Application - Link Aggregation Test Start",file = open(file_name, '+a'))

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Link Aggregation").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    e_swi.Advanced_LinkAggregation_Apply(driver,True,"1",file_name)
    e_swi.Advanced_LinkAggregation_GroupApply(driver,"T12",True,"src-dst-ip",True,file_name)
    e_swi.Advanced_LinkAggregation_PortApply(driver,Eth_Name,"None","1",file_name)

    #[EMS1-6456][Advanced - Link Aggregation] Apply Result check
    #[EMS1-6550][Advanced - Link Aggregation - Group] check
    #[EMS1-6551][Advanced - Link Aggregation - Port Apply] check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"Link Aggregation").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    mod.Switch_Specific_Frame(driver,0)
    driver.find_element(By.LINK_TEXT,"Link Aggregation Setting").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    driver.switch_to.frame("main")
    driver.find_element(By.LINK_TEXT,"LACP").click()
    time.sleep(3)

    # [Advanced - Link Aggregation - System]
    if_temp_error = False
    if(driver.find_element(By.NAME,"rplacp_ChkLACPSys").is_selected() == True ):
        print(f"             [EMS1-6456][Advanced - Link Aggregation] Active Result (True) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6456][Advanced - Link Aggregation] Active Result ({driver.find_element(By.NAME,"rplacp_ChkLACPSys").is_selected()} != True) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    
    if(driver.find_element(By.NAME,"rplacp_IptSystemPriority").get_attribute("value") == "1" ):
        print(f"             [EMS1-6456][Advanced - Link Aggregation] System Priority Result (1) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6456][Advanced - Link Aggregation] System Priority Result ({driver.find_element(By.NAME,"rplacp_IptSystemPriority").get_attribute("value")} != 1) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    
    if(if_temp_error == False):
        print(f"             [EMS1-6456][Advanced - Link Aggregation] Result Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6456][Advanced - Link Aggregation] Result Fail',file = open(file_name, '+a'))

    print(f"--------------------------------------------------------------------------------------",file = open(file_name, '+a'))
    # [Advanced - Link Aggregation - Port]
    if_temp_error = False
    t=''
    for i in Eth_Name:
        if i.isdigit():
            t += i
    tmp_num = int(t)
    if(Select(driver.find_element(By.NAME,f"rplacp_SltLACPTimeout?{int(tmp_num)}")).first_selected_option.get_attribute("text") == "1" ):
        print(f"             [EMS1-6551][Advanced - Link Aggregation] Port LACP Timeout Result (1) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6551][Advanced - Link Aggregation] Port LACP Timeout Result ({Select(driver.find_element(By.NAME,f"rplacp_SltLACPTimeout?{tmp_num}")).first_selected_option.get_attribute("text")} != 1) Fail',file = open(file_name, '+a'))    
        if_temp_error = True
    if(if_temp_error == False):
        print(f"             [EMS1-6551][Advanced - Link Aggregation - Port Apply] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6551][Advanced - Link Aggregation - Port Apply] Result Fail",file = open(file_name, '+a'))
    print(f"--------------------------------------------------------------------------------------",file = open(file_name, '+a'))
    # [Advanced - Link Aggregation - Group]
    if_temp_error = False
    if(driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[24]/td[3]/div/input").is_selected() == True ):
        print(f"             [EMS1-6550][Advanced - Link Aggregation - Group] LACP Active Result (True) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6550][Advanced - Link Aggregation - Group] LACP Active Result ({driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[24]/td[3]/div/input").is_selected()} != True) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    driver.find_element(By.LINK_TEXT,"Link Aggregation Setting").click()

    if(driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[2]/td/table[1]/tbody/tr[24]/td[3]/div/input").is_selected() == True ):
        print(f"             [EMS1-6550][Advanced - Link Aggregation - Group] Active Result (True) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6550][Advanced - Link Aggregation - Group] Active Result ({driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[2]/td/table[1]/tbody/tr[24]/td[3]/div/input").is_selected()} != True) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rptrunk_SltCriteria?12,1")).first_selected_option.get_attribute("text") == "src-dst-ip" ):
        print(f"             [EMS1-6550][Advanced - Link Aggregation - Group] Criteria Result (src-dst-ip) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6550][Advanced - Link Aggregation - Group] Criteria Result ({Select(driver.find_element(By.NAME,"rptrunk_SltCriteria?12,1")).first_selected_option.get_attribute("text")} != src-dst-ip) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(if_temp_error == False):
        print(f"             [EMS1-6550][Advanced - Link Aggregation - Group] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6550][Advanced - Link Aggregation - Group] Result Fail",file = open(file_name, '+a')) 


    print(f"======================================================================================",file = open(file_name, '+a'))



@retry()
def Advanced_Port(driver,url,ems_url,file_name,Pon_Name,Eth_Name,OLT_Port,OLT_Eth_Port):
    #[EMS1-6457][Advanced - Port Security] Apply Result
    #[EMS1-6552][Advanced - Port Security - Port] Port Apply Result 
    print(f"======================================================================================",file = open(file_name, '+a'))
    print(f"Advanced Application - Port Security Test Start",file = open(file_name, '+a'))

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Port Security").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    e_swi.Advanced_PortSecurity_Apply(driver,True,True,file_name)
    e_swi.Advanced_PortSecurity_PortApply(driver,Pon_Name,True,True,False,"1023",file_name)
    e_swi.Advanced_PortSecurity_PortApply(driver,Eth_Name,True,None,False,"8191",file_name)

    #[EMS1-6457][Advanced - Port Security] Apply Result check
    #[EMS1-6552][Advanced - Port Security - Port] Port Apply Result check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"Port Security").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    time.sleep(1)

    if_temp_error = False
    
    if(driver.find_element(By.NAME,"rpportsecu_ChkSwActive").is_selected() == True ):
        print(f"             [EMS1-6457][Advanced - Port Security - Port Security] Active Result (True) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6457][Advanced - Port Security - Port Security] Active Result ({driver.find_element(By.NAME,"rpportsecu_ChkSwActive").is_selected()} != True) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpportsecu_ChkAntiMacSpoofActive").is_selected() == True ):
        print(f"             [EMS1-6457][Advanced - Port Security - Anti Mac Spoof] Active Result (True) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6457][Advanced - Port Security - Anti Mac Spoof] Active Result ({driver.find_element(By.NAME,"rpportsecu_ChkAntiMacSpoofActive").is_selected()} != True) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(if_temp_error == False):
        print(f"             [EMS1-6457][Advanced - Port Security] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6457][Advanced - Port Security] Result Fail",file = open(file_name, '+a'))
    print(f"--------------------------------------------------------------------------------------",file = open(file_name, '+a'))
    if_temp_error = False
    for i in range(1,driver.find_elements(By.NAME,"rpportsecu_ChkPortActive").__len__()+1):
        if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[4]/tbody/tr[{2*(i+1)}]/td[2]/div").text == OLT_Port):
            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[4]/tbody/tr[{2*(i+1)}]/td[3]/div/input").is_selected() == True ):
                print(f"             [EMS1-6552][Advanced - Port Security - Port] {Pon_Name} Active Result (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6552][Advanced - Port Security - Port] {Pon_Name} Active Result ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[4]/tbody/tr[{2*(i+1)}]/td[3]/div/input").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            
            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[4]/tbody/tr[{2*(i+1)}]/td[4]/div/input").is_selected() == True ):
                print(f"             [EMS1-6552][Advanced - Port Security - Port] {Pon_Name} Anti_Mac Result (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6552][Advanced - Port Security - Port] {Pon_Name} Anti_Mac Result ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[4]/tbody/tr[{2*(i+1)}]/td[4]/div/input").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            
            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[4]/tbody/tr[{2*(i+1)}]/td[5]/div/input").is_selected() == False ):
                print(f"             [EMS1-6552][Advanced - Port Security - Port] {Pon_Name} Address_Learning Result (False) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6552][Advanced - Port Security - Port] {Pon_Name} Address_Learning Result ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[4]/tbody/tr[{2*(i+1)}]/td[5]/div/input").is_selected()} != False) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            
            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[4]/tbody/tr[{2*(i+1)}]/td[6]/div/input").get_attribute("value") == "1023" ):
                print(f"             [EMS1-6552][Advanced - Port Security - Port] {Pon_Name} Limit_Number Result (1023) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6552][Advanced - Port Security - Port] {Pon_Name} Limit_Number Result ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[4]/tbody/tr[{2*(i+1)}]/td[6]/div/input").get_attribute("value")} != 1023) Fail',file = open(file_name, '+a'))
                if_temp_error = True

    for i in range(1,driver.find_elements(By.NAME,"rpportsecu_ChkPortActive").__len__()+1):
        if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[4]/tbody/tr[{2*(i+1)}]/td[2]/div").text == OLT_Eth_Port):

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[4]/tbody/tr[{2*(i+1)}]/td[3]/div/input").is_selected() == True ):
                print(f"             [EMS1-6552][Advanced - Port Security - Port] {Eth_Name} Active Result (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6552][Advanced - Port Security - Port] {Eth_Name} Active Result ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[4]/tbody/tr[{2*(i+1)}]/td[3]/div/input").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            
            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[4]/tbody/tr[{2*(i+1)}]/td[5]/div/input").is_selected() == False ):
                print(f"             [EMS1-6552][Advanced - Port Security - Port] {Eth_Name} Address_Learning Result (False) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6552][Advanced - Port Security - Port] {Eth_Name} Address_Learning Result ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[4]/tbody/tr[{2*(i+1)}]/td[5]/div/input").is_selected()} != False) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            
            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[4]/tbody/tr[{2*(i+1)}]/td[6]/div/input").get_attribute("value") == "8191" ):
                print(f"             [EMS1-6552][Advanced - Port Security - Port] {Eth_Name} Limit_Number Result (8191) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6552][Advanced - Port Security - Port] {Eth_Name} Limit_Number Result ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[4]/tbody/tr[{2*(i+1)}]/td[6]/div/input").get_attribute("value")} != 8191) Fail',file = open(file_name, '+a'))
                if_temp_error = True

    if(if_temp_error == False):
        print(f"             [EMS1-6552][Advanced - Port Security - Port] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6552][Advanced - Port Security - Port] Result Fail",file = open(file_name, '+a'))

    print(f"======================================================================================",file = open(file_name, '+a'))

@retry()
def Advanced_Classifier(driver,url,ems_url,file_name):
    #EMS [EMS1-6458][Advanced - Classifier - New] Result 
    print(f"======================================================================================",file = open(file_name, '+a'))
    print(f"Advanced Application - Classifier Test Start",file = open(file_name, '+a'))

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Classifier").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)
    driver.find_element(By.ID,"advance_classifier_profile_new_btn").click()
    time.sleep(1)
    e_swi.Advanced_Classifier(driver,True,"Name_Test_xxxxxxxxxxxxxxxxxxxx31","All","4094","7","Others","0800","00:01:02:03:04:05","Any","10:11:12:13:14:15","Any","63","All",False,"IPv4","10.11.12.13","24","Any","20.21.22.23","24","Any",file_name)

    #[EMS1-6458][Advanced - Classifier - New] Result check
    
    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"Classifier").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    time.sleep(1)
    for i in range(1,driver.find_elements(By.NAME,"rpclassifier_ChkTabDelete").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td/table[2]/tbody/tr[{(2*i)+1}]/td[4]/div").text
        if(ele == 'Name_Test_xxxxxxxxxxxxxxxxxxxx31'):
            driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td/table[2]/tbody/tr[{(2*i)+1}]/td[2]/div/a").click()
            time.sleep(1)

    if_temp_error = False
    if(driver.find_element(By.NAME,"rpclassifier_ChkSwActive").is_selected() == True):
        print(f"             [EMS1-6458][Advanced - Classifier - New] Active (True) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6458][Advanced - Classifier - New] Active ({driver.find_element(By.NAME,"rpclassifier_ChkSwActive").is_selected()} != True) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    
    if(driver.find_element(By.NAME,"rpclassifier_IptTextSwName").get_attribute("value") == "Name_Test_xxxxxxxxxxxxxxxxxxxx31"):
        print(f"             [EMS1-6458][Advanced - Classifier - New] Name (Name_Test_xxxxxxxxxxxxxxxxxxxx31) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6458][Advanced - Classifier - New] Name ({driver.find_element(By.NAME,"rpclassifier_IptTextSwName").get_attribute("value")} != Name_Test_xxxxxxxxxxxxxxxxxxxx31) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rpclassifier_SltPktFormat")).first_selected_option.get_attribute("text") == "All"):
        print(f"             [EMS1-6458][Advanced - Classifier - New] Packet_Format (All) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6458][Advanced - Classifier - New] Packet_Format ({Select(driver.find_element(By.NAME,"rpclassifier_SltPktFormat")).first_selected_option.get_attribute("text")} != All) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[3]/td/table[1]/tbody/tr[8]/td[4]/input[2]").is_selected() == True and driver.find_element(By.NAME,"rpclassifier_IptTextVlan").get_attribute("value") == "4094"):
        print(f"             [EMS1-6458][Advanced - Classifier - New] VLAN (True) (4094) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6458][Advanced - Classifier - New] VLAN ({driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[3]/td/table[1]/tbody/tr[8]/td[4]/input[2]").is_selected()} != True) ({driver.find_element(By.NAME,"rpclassifier_IptTextVlan").get_attribute("value")} != 4094) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[3]/td/table[1]/tbody/tr[10]/td[2]/input[2]").is_selected() == True and Select(driver.find_element(By.NAME,"rpclassifier_SltPriority")).first_selected_option.get_attribute("text") == "7"):
        print(f"             [EMS1-6458][Advanced - Classifier - New] Priority (True) (7) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6458][Advanced - Classifier - New] Priority ({driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[3]/td/table[1]/tbody/tr[10]/td[2]/input[2]").is_selected()} != True) ({Select(driver.find_element(By.NAME,"rpclassifier_SltPriority")).first_selected_option.get_attribute("text")} != 7) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[3]/td/table[1]/tbody/tr[12]/td[2]/input[1]").is_selected() == True and Select(driver.find_element(By.ID,"rpclassifier_SltL2Protocol")).first_selected_option.get_attribute("text") == "IP"):
        print(f"             [EMS1-6458][Advanced - Classifier - New] Ethernet_Type (True) (IP) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6458][Advanced - Classifier - New] Ethernet_Type ({driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[3]/td/table[1]/tbody/tr[12]/td[2]/input[1]").is_selected()} != True) ({Select(driver.find_element(By.ID,"rpclassifier_SltL2Protocol")).first_selected_option.get_attribute("text")} != IP) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    
    if(driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[3]/td/table[1]/tbody/tr[14]/td[3]/input[2]").is_selected() == True and driver.find_element(By.NAME,"rpclassifier_IptTextL2SrcAddr1").get_attribute("value") == "00" and driver.find_element(By.NAME,"rpclassifier_IptTextL2SrcAddr2").get_attribute("value") == "01" and driver.find_element(By.NAME,"rpclassifier_IptTextL2SrcAddr3").get_attribute("value") == "02" and driver.find_element(By.NAME,"rpclassifier_IptTextL2SrcAddr4").get_attribute("value") == "03" and driver.find_element(By.NAME,"rpclassifier_IptTextL2SrcAddr5").get_attribute("value") == "04" and driver.find_element(By.NAME,"rpclassifier_IptTextL2SrcAddr6").get_attribute("value") == "05"):
        print(f"             [EMS1-6458][Advanced - Classifier - New] Source_MAC_Address (True) (00:01:02:03:04:05) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6458][Advanced - Classifier - New] Source_MAC_Address ({driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[3]/td/table[1]/tbody/tr[14]/td[3]/input[2]").is_selected()} != True) ({driver.find_element(By.NAME,"rpclassifier_IptTextL2SrcAddr1").get_attribute("value")} != 00 {driver.find_element(By.NAME,"rpclassifier_IptTextL2SrcAddr2").get_attribute("value")} != 01 {driver.find_element(By.NAME,"rpclassifier_IptTextL2SrcAddr3").get_attribute("value")} != 02 {driver.find_element(By.NAME,"rpclassifier_IptTextL2SrcAddr4").get_attribute("value")} != 03 {driver.find_element(By.NAME,"rpclassifier_IptTextL2SrcAddr5").get_attribute("value")} != 04 {driver.find_element(By.NAME,"rpclassifier_IptTextL2SrcAddr6").get_attribute("value")} != 05) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    
    if(driver.find_element(By.NAME,"rpclassifier_SorportRadio").is_selected() == True):
        print(f"             [EMS1-6458][Advanced - Classifier - New] Source_Port (True) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6458][Advanced - Classifier - New] Source_Port ({driver.find_element(By.NAME,"rpclassifier_SorportRadio").is_selected()} != True) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    
    if(driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[3]/td/table[1]/tbody/tr[17]/td[3]/input[2]").is_selected() == True and driver.find_element(By.NAME,"rpclassifier_IptTextL2DestAddr1").get_attribute("value") == "10" and driver.find_element(By.NAME,"rpclassifier_IptTextL2DestAddr2").get_attribute("value") == "11" and driver.find_element(By.NAME,"rpclassifier_IptTextL2DestAddr3").get_attribute("value") == "12" and driver.find_element(By.NAME,"rpclassifier_IptTextL2DestAddr4").get_attribute("value") == "13" and driver.find_element(By.NAME,"rpclassifier_IptTextL2DestAddr5").get_attribute("value") == "14" and driver.find_element(By.NAME,"rpclassifier_IptTextL2DestAddr6").get_attribute("value") == "15"):
        print(f"             [EMS1-6458][Advanced - Classifier - New] Destination_MAC_Address (True) (10:11:12:13:14:15) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6458][Advanced - Classifier - New] Destination_MAC_Address ({driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[3]/td/table[1]/tbody/tr[17]/td[3]/input[2]").is_selected()} != True) ({driver.find_element(By.NAME,"rpclassifier_IptTextL2DestAddr1").get_attribute("value")} != 10 {driver.find_element(By.NAME,"rpclassifier_IptTextL2DestAddr2").get_attribute("value")} != 11 {driver.find_element(By.NAME,"rpclassifier_IptTextL2DestAddr3").get_attribute("value")} != 12 {driver.find_element(By.NAME,"rpclassifier_IptTextL2DestAddr4").get_attribute("value")} != 13 {driver.find_element(By.NAME,"rpclassifier_IptTextL2DestAddr5").get_attribute("value")} != 14 {driver.find_element(By.NAME,"rpclassifier_IptTextL2DestAddr6").get_attribute("value")} != 15) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpclassifier_DestportRadio").is_selected() == True):
        print(f"             [EMS1-6458][Advanced - Classifier - New] Destination_Port (True) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6458][Advanced - Classifier - New] Destination_Port ({driver.find_element(By.NAME,"rpclassifier_DestportRadio").is_selected()} != True) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[3]/td/table[1]/tbody/tr[20]/td[4]/input[2]").is_selected() == True and driver.find_element(By.NAME,"rpclassifier_IptTextDSCP").get_attribute("value") == "63"):
        print(f"             [EMS1-6458][Advanced - Classifier - New] DSCP (True) (63) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6458][Advanced - Classifier - New] DSCP ({driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[3]/td/table[1]/tbody/tr[20]/td[4]/input[2]").is_selected()} != True) ({driver.find_element(By.NAME,"rpclassifier_IptTextDSCP").get_attribute("value")} != 63) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    
    if(driver.find_element(By.NAME,"rpclassifier_RPgL3Protocol").is_selected() == True and Select(driver.find_element(By.NAME,"rpclassifier_SltL3Protocol")).first_selected_option.get_attribute("text") == "All" and driver.find_element(By.NAME,"rpclassifier_ChkTcpEstablish").is_selected() == False):
        print(f"             [EMS1-6458][Advanced - Classifier - New] IP_Protocol (True) (All) (False) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6458][Advanced - Classifier - New] IP_Protocol ({driver.find_element(By.NAME,"rpclassifier_RPgL3Protocol").is_selected()} != True) ({Select(driver.find_element(By.NAME,"rpclassifier_SltL3Protocol")).first_selected_option.get_attribute("text")} != All) ({driver.find_element(By.NAME,"rpclassifier_ChkTcpEstablish").is_selected()} != False) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpclassifier_RPgIPType").is_selected() == True):
        print(f"             [EMS1-6458][Advanced - Classifier - New] IP_Type (True) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6458][Advanced - Classifier - New] IP_Type ({driver.find_element(By.NAME,"rpclassifier_RPgIPType").is_selected()} != True) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpclassifier_IptTextL3SrcIP").get_attribute("value") == "10.11.12.13" and driver.find_element(By.NAME,"rpclassifier_IptTextL3SrcIPMask").get_attribute("value") == "24" and driver.find_element(By.NAME,"rpclassifier_RPgL3SrcSocket").is_selected() == True):
        print(f"             [EMS1-6458][Advanced - Classifier - New] Layer3/4 Source (10.11.12.13) (24) (True) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6458][Advanced - Classifier - New] Layer3/4 Source ({driver.find_element(By.NAME,"rpclassifier_IptTextL3SrcIP").get_attribute("value")} != 10.11.12.13) ({driver.find_element(By.NAME,"rpclassifier_IptTextL3SrcIPMask").get_attribute("value")} != 24) ({driver.find_element(By.NAME,"rpclassifier_RPgL3SrcSocket").is_selected()} != True) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpclassifier_IptTextL3DestIP").get_attribute("value") == "20.21.22.23" and driver.find_element(By.NAME,"rpclassifier_IptTextL3DestIPMask").get_attribute("value") == "24" and driver.find_element(By.NAME,"rpclassifier_RPgL3DestSocket").is_selected() == True):
        print(f"             [EMS1-6458][Advanced - Classifier - New] Layer3/4 Destination (20.21.22.23) (24) (True) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6458][Advanced - Classifier - New] Layer3/4 Destination ({driver.find_element(By.NAME,"rpclassifier_IptTextL3DestIP").get_attribute("value")} != 20.21.22.23) ({driver.find_element(By.NAME,"rpclassifier_IptTextL3DestIPMask").get_attribute("value")} != 24) ({driver.find_element(By.NAME,"rpclassifier_RPgL3DestSocket").is_selected()} != True) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(if_temp_error == False):
        print(f"             [EMS1-6458][Advanced - Classifier - New] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6458][Advanced - Classifier - New] Result Fail",file = open(file_name, '+a'))


    #[EMS1-6558][Advanced - Classifier - Detail] Result 

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Classifier").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(2)
    if_find =False
    for i in range(1,int(driver.find_element(By.ID,"pageTotal").text)+1):
        for j in range(1,driver.find_elements(By.NAME,"advance_classifier_profile_checkbox").__len__()+1):
            ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div[2]/div[3]/div[1]/div[{j+1}]/div[3]").text
            if(ele == 'Name_Test_xxxxxxxxxxxxxxxxxxxx31'):
                driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div[2]/div[3]/div[1]/div[{j+1}]/div[4]/a").click()
                if_find =True
                time.sleep(5)
            if(if_find==True):
                break
        if(if_find==True):
            break 
        else:
            driver.find_element(By.ID,"btnNextPage").click()
    # time.sleep(2)
    time.sleep(10)
    
    if_temp_error = False
    if(driver.find_element(By.ID,"classifier_name").get_attribute("value") == "Name_Test_xxxxxxxxxxxxxxxxxxxx31"):
        print(f"             [EMS1-6558][Advanced - Classifier - Detail] Name (Name_Test_xxxxxxxxxxxxxxxxxxxx31) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6558][Advanced - Classifier - Detail] Name ({driver.find_element(By.ID,"classifier_name").get_attribute("value")} != Name_Test_xxxxxxxxxxxxxxxxxxxx31) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    
    if(driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/div/div[1]/div/div[4]/div/div/div[1]").text == "VLAN = 4094;"):
        print(f"             [EMS1-6558][Advanced - Classifier - Detail] VLAN (VLAN = 4094;) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6558][Advanced - Classifier - Detail] VLAN ({driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/div/div[1]/div/div[4]/div/div/div[1]").get_attribute("value")} != VLAN = 4094;) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    
    if(driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/div/div[1]/div/div[4]/div/div/div[2]").text == "Priority = 7;"):
        print(f"             [EMS1-6558][Advanced - Classifier - Detail] Priority (Priority = 7;) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6558][Advanced - Classifier - Detail] Priority ({driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/div/div[1]/div/div[4]/div/div/div[2]").get_attribute("value")} != Priority = 7;) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/div/div[1]/div/div[4]/div/div/div[3]").text == "DSCP = 63;"):
        print(f"             [EMS1-6558][Advanced - Classifier - Detail] DSCP (DSCP = 63;) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6558][Advanced - Classifier - Detail] DSCP ({driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/div/div[1]/div/div[4]/div/div/div[3]").get_attribute("value")} != DSCP = 63;) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/div/div[1]/div/div[4]/div/div/div[4]").text == "EtherType = ip;"):
        print(f"             [EMS1-6558][Advanced - Classifier - Detail] EtherType (EtherType = ip;) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6558][Advanced - Classifier - Detail] EtherType ({driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/div/div[1]/div/div[4]/div/div/div[4]").get_attribute("value")} != EtherType = ip;) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/div/div[1]/div/div[4]/div/div/div[5]").text == "SrcMac = 00:01:02:03:04:05;"):
        print(f"             [EMS1-6558][Advanced - Classifier - Detail] SrcMac (SrcMac = 00:01:02:03:04:05;) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6558][Advanced - Classifier - Detail] SrcMac ({driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/div/div[1]/div/div[4]/div/div/div[5]").get_attribute("value")} != SrcMac = 00:01:02:03:04:05;) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/div/div[1]/div/div[4]/div/div/div[6]").text == "DestMac = 10:11:12:13:14:15;"):
        print(f"             [EMS1-6558][Advanced - Classifier - Detail] DestMac (DestMac = 10:11:12:13:14:15;) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6558][Advanced - Classifier - Detail] DestMac ({driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/div/div[1]/div/div[4]/div/div/div[6]").get_attribute("value")} != DestMac = 10:11:12:13:14:15;) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/div/div[1]/div/div[4]/div/div/div[7]").text == "SrcIP = 10.11.12.13/24;"):
        print(f"             [EMS1-6558][Advanced - Classifier - Detail] SrcIP (SrcIP = 10.11.12.13/24;) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6558][Advanced - Classifier - Detail] SrcIP ({driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/div/div[1]/div/div[4]/div/div/div[7]").get_attribute("value")} != SrcIP = 10.11.12.13/24;) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/div/div[1]/div/div[4]/div/div/div[8]").text == "DestIP = 20.21.22.23/24;"):
        print(f"             [EMS1-6558][Advanced - Classifier - Detail] DestIP (DestIP = 20.21.22.23/24;) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6558][Advanced - Classifier - Detail] DestIP ({driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/div/div[1]/div/div[4]/div/div/div[8]").get_attribute("value")} != DestIP = 20.21.22.23/24;) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(if_temp_error == False):
        print(f"             [EMS1-6558][Advanced - Classifier - Detail] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6558][Advanced - Classifier - Detail] Result Fail",file = open(file_name, '+a'))

    print(f"======================================================================================",file = open(file_name, '+a'))

    driver.find_element(By.XPATH,'//*[@id="classifier_background"]/div/div[5]/input').click()


    #[EMS1-6553][Advanced - Classifier - Delete] Result
    if_find = False
    for i in range(1,int(driver.find_element(By.ID,"pageTotal").text)+1):
        for j in range(1,driver.find_elements(By.NAME,"advance_classifier_profile_checkbox").__len__()+1):
            ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div[2]/div[3]/div[1]/div[{j+1}]/div[3]").text
            if(ele == 'Name_Test_xxxxxxxxxxxxxxxxxxxx31'):
                driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div[2]/div[3]/div[1]/div[{j+1}]/div[5]/label").click()
                if_find =True
                time.sleep(1)
            if(if_find==True):
                break
        if(if_find==True):
            break 
        else:
            driver.find_element(By.ID,"btnNextPage").click()
    driver.find_element(By.ID,"advance_classifier_profile_del_btn").click()
    time.sleep(1)
    
    #[EMS1-6553][Advanced - Classifier - Delete] Result check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"Classifier").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    time.sleep(1)

    if_temp_error = False
    for i in range(1,driver.find_elements(By.NAME,"rpclassifier_ChkTabDelete").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td/table[2]/tbody/tr[{(i*2)+1}]/td[4]/div").text
        if(ele == 'Name_Test_xxxxxxxxxxxxxxxxxxxx31'):
            if_temp_error = True
    if(if_temp_error==False):
        print(f"             [EMS1-6553][Advanced - Classifier - Delete] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6553][Advanced - Classifier - Delete] Result Fail",file = open(file_name, '+a'))

    #[EMS1-6554][Advanced - Classifier - Page Switch]

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Classifier").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)
    for i in range(1,12):
        driver.find_element(By.ID,"advance_classifier_profile_new_btn").click()
        time.sleep(1)
        e_swi.Advanced_Classifier(driver,True,f"Name_Test_xxxxxxxxxxxxxxxxxxxx{i}","All","4094","7","Others","0800","00:01:02:03:04:05","Any","10:11:12:13:14:15","Any","63","All",False,"IPv4","10.11.12.13","24","Any","20.21.22.23","24","Any",file_name)
    driver.find_element(By.ID,'btnNextPage').click()
    if(driver.find_element(By.XPATH,'//*[@id="advance_classifier_profile_table"]/div[2]/div[1]').text == '11'):
        print(f"             [EMS1-6554][Advanced - Classifier - Page Switch] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6554][Advanced - Classifier - Page Switch] Result Fail",file = open(file_name, '+a'))

    for i in range(1,3):
        e_mod.Checkbox_EMS(driver,"advance_classifier_profile_checkbox",True)
        driver.find_element(By.ID,"advance_classifier_profile_del_btn").click()
        time.sleep(2)
        msg = e_swi.alert_accept_text(driver)
        try:
            e_pro.Close(driver)
        except:
            pass     

    print(f"======================================================================================",file = open(file_name, '+a'))

@retry()
def Advanced_Policy(driver,url,ems_url,file_name):
    #[EMS1-6459][Advanced - Policy - New] Result
    print(f"======================================================================================",file = open(file_name, '+a')) 
    print(f"Advanced Application - Policy Rule Test Start",file = open(file_name, '+a'))

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Classifier").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)
    driver.find_element(By.ID,"advance_classifier_profile_new_btn").click()
    time.sleep(1)
    e_swi.Advanced_Classifier(driver,True,"Name_Test_xxxxxxxxxxxxxxxxxxxx31","All","4094","7","Others","0800","00:01:02:03:04:05","Any","10:11:12:13:14:15","Any","63","All",False,"IPv4","10.11.12.13","24","Any","20.21.22.23","24","Any",file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Policy Rule").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)
    driver.find_element(By.ID,"advance_policy_profile_new_btn").click()
    e_swi.Advanced_Policy(driver,True,"Name_Test_xxxxxxxxxxxxxxxxxxxx31","ETH 1","ETH 1",file_name)

    #[EMS1-6459][Advanced - Policy - New] Result check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"Policy Rule").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    time.sleep(1)
    for i in range(1,driver.find_elements(By.NAME,"rppolicy_ChkTabDelete").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[{(2*i)+1}]/td[4]/div").text
        if(ele == 'Name_Test_xxxxxxxxxxxxxxxxxxxx31'):
            driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[{(2*i)+1}]/td[2]/div/a").click()
            time.sleep(1)

    if_temp_error = False
    if(driver.find_element(By.NAME,"rppolicy_ChkSwActive").is_selected() == True):
        print(f"             [EMS1-6459][Advanced - Policy - New] Active (True) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6459][Advanced - Policy - New] Active ({driver.find_element(By.NAME,"rppolicy_ChkSwActive").is_selected()} != True) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rppolicy_IptTextSwName").get_attribute("value") == "Name_Test_xxxxxxxxxxxxxxxxxxxx31"):
        print(f"             [EMS1-6459][Advanced - Policy - New] Name (Name_Test_xxxxxxxxxxxxxxxxxxxx31) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6459][Advanced - Policy - New] Name ({driver.find_element(By.NAME,"rppolicy_IptTextSwName").get_attribute("value")} != Name_Test_xxxxxxxxxxxxxxxxxxxx31) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rppolicy_SltList")).first_selected_option.get_attribute("text") == "Name_Test_xxxxxxxxxxxxxxxxxxxx31"):
        print(f"             [EMS1-6459][Advanced - Policy - New] Classifier (Name_Test_xxxxxxxxxxxxxxxxxxxx31) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6459][Advanced - Policy - New] Classifier ({Select(driver.find_element(By.NAME,"rppolicy_SltList")).first_selected_option.get_attribute("text")} != Name_Test_xxxxxxxxxxxxxxxxxxxx31) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    
    if(driver.find_element(By.NAME,"rppolicy_IptTextEgressPort").get_attribute("value") == "eth-1"):
        print(f"             [EMS1-6459][Advanced - Policy - New] Egress_Port (eth-1) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6459][Advanced - Policy - New] Egress_Port ({driver.find_element(By.NAME,"rppolicy_IptTextEgressPort").get_attribute("value")} != eth-1) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    
    if(driver.find_element(By.NAME,"rppolicy_IptTextMirrorPort").get_attribute("value") == "eth-1"):
        print(f"             [EMS1-6459][Advanced - Policy - New] Mirror_Port (eth-1) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6459][Advanced - Policy - New] Mirror_Port ({driver.find_element(By.NAME,"rppolicy_IptTextMirrorPort").get_attribute("value")} != eth-1) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    
    if(Select(driver.find_element(By.NAME,"rppolicy_SltPriority")).first_selected_option.get_attribute("text") == "0"):
        print(f"             [EMS1-6459][Advanced - Policy - New] Priority (0) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6459][Advanced - Policy - New] Priority ({Select(driver.find_element(By.NAME,"rppolicy_SltPriority")).first_selected_option.get_attribute("text")} != 0) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rppolicy_SltTos")).first_selected_option.get_attribute("text") == "0"):
        print(f"             [EMS1-6459][Advanced - Policy - New] TOS (0) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6459][Advanced - Policy - New] TOS ({Select(driver.find_element(By.NAME,"rppolicy_SltTos")).first_selected_option.get_attribute("text")} != 0) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[3]/td[2]/table[1]/tbody/tr[7]/td/input").is_selected() == True):
        print(f"             [EMS1-6459][Advanced - Policy - New] Forwarding (True) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6459][Advanced - Policy - New] Forwarding ({driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[3]/td[2]/table[1]/tbody/tr[7]/td/input").is_selected()} != True) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(if_temp_error == False):
        print(f"             [EMS1-6459][Advanced - Policy - New] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6459][Advanced - Policy - New] Result Fail",file = open(file_name, '+a'))

    #[EMS1-6557][Advanced - Policy - Detail] Result 

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Policy Rule").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)
    if_find =False
    for i in range(1,int(driver.find_element(By.ID,"pageTotal").text)+1):
        for j in range(1,driver.find_elements(By.NAME,"advance_policy_profile_checkbox").__len__()+1):
            ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div[2]/div[3]/div[1]/div[{j+1}]/div[3]").text
            if(ele == 'Name_Test_xxxxxxxxxxxxxxxxxxxx31'):
                driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div[2]/div[3]/div[1]/div[{j+1}]/div[4]/a").click()
                if_find =True                
                time.sleep(5)
            if(if_find==True):
                break
        if(if_find==True):
            break 
        else:
            driver.find_element(By.ID,"btnNextPage").click()
    #[EMS1-6557][Advanced - Policy - Detail] Result check
    if_temp_error = False
    if(driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/div/div[1]/div/div[4]/div/div/div[2]").text == "Name_Test_xxxxxxxxxxxxxxxxxxxx31;"):
        print(f"             [EMS1-6557][Advanced - Policy - Detail] Classifiers (Name_Test_xxxxxxxxxxxxxxxxxxxx31;) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6557][Advanced - Policy - Detail] Classifiers ({driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/div/div[1]/div/div[4]/div/div/div[2]").get_attribute("value")} != Name_Test_xxxxxxxxxxxxxxxxxxxx31;) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    
    if(driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/div/div[1]/div/div[4]/div/div/div[9]").text == "Discard the packet;"):
        print(f"             [EMS1-6557][Advanced - Policy] Action VLAN (Discard the packet;) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6557][Advanced - Policy] Action VLAN ({driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/div/div[1]/div/div[4]/div/div/div[9]").get_attribute("value")} != Discard the packet;) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    
    if(if_temp_error == False):
        print(f"             [EMS1-6557][Advanced - Policy - Detail] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6557][Advanced - Policy - Detail] Result Fail",file = open(file_name, '+a'))

    print(f"======================================================================================",file = open(file_name, '+a'))

    driver.find_element(By.XPATH,'//*[@id="policy_background"]/div/div[5]/input').click()


    #[EMS1-6555][Advanced - Policy - Delete] Result
    if_find = False
    for i in range(1,int(driver.find_element(By.ID,"pageTotal").text)+1):
        for j in range(1,driver.find_elements(By.NAME,"advance_policy_profile_checkbox").__len__()+1):
            ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div[2]/div[3]/div[1]/div[{j}]/div[3]").text
            if(ele == 'Name_Test_xxxxxxxxxxxxxxxxxxxx31'):
                driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div[2]/div[3]/div[1]/div[{j}]/div[5]/label").click()
                if_find =True
                time.sleep(1)
            if(if_find==True):
                break
        if(if_find==True):
            break 
        else:
            driver.find_element(By.ID,"btnNextPage").click()
    driver.find_element(By.ID,"advance_policy_profile_del_btn").click()
    time.sleep(1)
    driver.find_element(By.XPATH,"/html/body/div[5]/div/div/div[3]/button").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Classifier").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    if_find = False
    for i in range(1,int(driver.find_element(By.ID,"pageTotal").text)+1):
        for j in range(1,driver.find_elements(By.NAME,"advance_classifier_profile_checkbox").__len__()+1):
            ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div[2]/div[3]/div[1]/div[{j+1}]/div[3]").text
            if(ele == 'Name_Test_xxxxxxxxxxxxxxxxxxxx31'):
                driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div[2]/div[3]/div[1]/div[{j+1}]/div[5]/label").click()
                if_find =True
                time.sleep(1)
            if(if_find==True):
                break
        if(if_find==True):
            break 
        else:
            driver.find_element(By.ID,"btnNextPage").click()
    driver.find_element(By.ID,"advance_classifier_profile_del_btn").click()
    time.sleep(1)

    #[EMS1-6555][Advanced - Policy - Delete] Result check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"Policy Rule").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    time.sleep(1)

    if_temp_error = False
    for i in range(1,driver.find_elements(By.NAME,"rppolicy_ChkTabDelete").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td[2]/table[2]/tbody/tr[{(2*i)+1}]/td[4]/div").text
        if(ele == 'Name_Test_xxxxxxxxxxxxxxxxxxxx31'):
            if_temp_error = True
    if(if_temp_error==False):
        print(f"             [EMS1-6555][Advanced - Policy - Delete] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6555][Advanced - Policy - Delete] Result Fail",file = open(file_name, '+a'))

    #[EMS1-6556][Advanced - Policy - Page Switch] Result Pass/Fail

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Classifier").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)
    for i in range(1,12):
        driver.find_element(By.ID,"advance_classifier_profile_new_btn").click()
        time.sleep(1)
        e_swi.Advanced_Classifier(driver,True,f"Name_Test_xxxxxxxxxxxxxxxxxxxx{i}","All","4094","7","Others","0800","00:01:02:03:04:05","Any","10:11:12:13:14:15","Any","63","All",False,"IPv4","10.11.12.13","24","Any","20.21.22.23","24","Any",file_name)

    time.sleep(2)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"Policy Rule").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    for i in range(1,12):
        driver.find_element(By.ID,"advance_policy_profile_new_btn").click()
        e_swi.Advanced_Policy(driver,True,f"Name_Test_xxxxxxxxxxxxxxxxxxxx{i}","ETH 1","ETH 1",file_name)
    driver.find_element(By.ID,'btnNextPage').click()
    time.sleep(2)
    if(driver.find_element(By.XPATH,'//*[@id="advance_policy_profile_table"]/div[2]/div[1]').text == '11'):
        print(f"             [EMS1-6556][Advanced - Policy - Page Switch] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6556][Advanced - Policy - Page Switch] Result Fail",file = open(file_name, '+a'))

    for i in range(1,3):
        e_mod.Checkbox_EMS(driver,"advance_policy_profile_checkbox",True)
        driver.find_element(By.ID,"advance_policy_profile_del_btn").click()
        time.sleep(2)
        msg = e_swi.alert_accept_text(driver)
        try:
            e_pro.Close(driver)
        except:
            pass     
    
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Classifier").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    for i in range(1,3):
        e_mod.Checkbox_EMS(driver,"advance_classifier_profile_checkbox",True)
        driver.find_element(By.ID,"advance_classifier_profile_del_btn").click()
        time.sleep(2)
        msg = e_swi.alert_accept_text(driver)
        try:
            e_pro.Close(driver)
        except:
            pass     


    print(f"======================================================================================",file = open(file_name, '+a'))

@retry()
def Advanced_Queqe(driver,url,ems_url,file_name,Pon_Name,Eth_Name,Pon_Name_L,Eth_Name_L,OLT_Eth_Port,OLT_Port):
    #[EMS1-6460][Advanced - Queue Method] Result
    print(f"======================================================================================",file = open(file_name, '+a'))
    print(f"Advanced Application - Queue Method Test Start",file = open(file_name, '+a'))

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Queue Method").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)
    e_swi.Advanced_Queue(driver,Pon_Name,"WFQ","127","127","127","127","127","127","127","127","Q7",file_name)
    #[EMS1-6460][Advanced - Queue Method] Result check
    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"Queuing Method").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    time.sleep(1)

    if_temp_error = False
    for i in range(1,int(OLT_Eth_Port)+1):
        if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[4]/td/table/tbody/tr[{5+(i*3)}]/td[2]/div").text == Pon_Name_L):
            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[4]/td/table/tbody/tr[{5+(i*3)}]/td[3]/div/input").is_selected() == False):
                print(f"             [EMS1-6460][Advanced - Queue Method] {Pon_Name} Method (False) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6460][Advanced - Queue Method] {Pon_Name} Method ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[4]/td/table/tbody/tr[{5+(i*3)}]/td[3]/div/input").is_selected()} != False) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,f"rpqueuemethod_IptTextQ0Weight?{int(OLT_Port)}").get_attribute("value") == "127"):
                print(f"             [EMS1-6460][Advanced - Queue Method] {Pon_Name} Q0 (127) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6460][Advanced - Queue Method] {Pon_Name} Q0 ({driver.find_element(By.NAME,f"rpqueuemethod_IptTextQ0Weight?{int(OLT_Port)}").get_attribute("value")} != 127) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            
            if(driver.find_element(By.NAME,f"rpqueuemethod_IptTextQ1Weight?{int(OLT_Port)}").get_attribute("value") == "127"):
                print(f"             [EMS1-6460][Advanced - Queue Method] {Pon_Name} Q1 (127) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6460][Advanced - Queue Method] {Pon_Name} Q1 ({driver.find_element(By.NAME,f"rpqueuemethod_IptTextQ1Weight?{int(OLT_Port)}").get_attribute("value")} != 127) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            
            if(driver.find_element(By.NAME,f"rpqueuemethod_IptTextQ2Weight?{int(OLT_Port)}").get_attribute("value") == "127"):
                print(f"             [EMS1-6460][Advanced - Queue Method] {Pon_Name} Q2 (127) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6460][Advanced - Queue Method] {Pon_Name} Q2 ({driver.find_element(By.NAME,f"rpqueuemethod_IptTextQ2Weight?{int(OLT_Port)}").get_attribute("value")} != 127) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,f"rpqueuemethod_IptTextQ3Weight?{int(OLT_Port)}").get_attribute("value") == "127"):
                print(f"             [EMS1-6460][Advanced - Queue Method] {Pon_Name} Q3 (127) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6460][Advanced - Queue Method] {Pon_Name} Q3 ({driver.find_element(By.NAME,f"rpqueuemethod_IptTextQ3Weight?{int(OLT_Port)}").get_attribute("value")} != 127) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,f"rpqueuemethod_IptTextQ4Weight?{int(OLT_Port)}").get_attribute("value") == "127"):
                print(f"             [EMS1-6460][Advanced - Queue Method] {Pon_Name} Q4 (127) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6460][Advanced - Queue Method] {Pon_Name} Q4 ({driver.find_element(By.NAME,f"rpqueuemethod_IptTextQ4Weight?{int(OLT_Port)}").get_attribute("value")} != 127) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,f"rpqueuemethod_IptTextQ5Weight?{int(OLT_Port)}").get_attribute("value") == "127"):
                print(f"             [EMS1-6460][Advanced - Queue Method] {Pon_Name} Q5 (127) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6460][Advanced - Queue Method] {Pon_Name} Q5 ({driver.find_element(By.NAME,f"rpqueuemethod_IptTextQ5Weight?{int(OLT_Port)}").get_attribute("value")} != 127) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,f"rpqueuemethod_IptTextQ6Weight?{int(OLT_Port)}").get_attribute("value") == "127"):
                print(f"             [EMS1-6460][Advanced - Queue Method] {Pon_Name} Q6 (127) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6460][Advanced - Queue Method] {Pon_Name} Q6 ({driver.find_element(By.NAME,f"rpqueuemethod_IptTextQ6Weight?{int(OLT_Port)}").get_attribute("value")} != 127) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,f"rpqueuemethod_IptTextQ7Weight?{int(OLT_Port)}").get_attribute("value") == "127"):
                print(f"             [EMS1-6460][Advanced - Queue Method] {Pon_Name} Q7 (127) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6460][Advanced - Queue Method] {Pon_Name} Q7 ({driver.find_element(By.NAME,f"rpqueuemethod_IptTextQ7Weight?{int(OLT_Port)}").get_attribute("value")} != 127) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(Select(driver.find_element(By.NAME,f"rpqueuemethod_SltHybridSpq?{int(OLT_Port)}")).first_selected_option.get_attribute("text") == "Q7"):
                print(f"             [EMS1-6460][Advanced - Queue Method] {Pon_Name} Lowest_Queue (Q7) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6460][Advanced - Queue Method] {Pon_Name} Lowest_Queue ({Select(driver.find_element(By.NAME,f"rpqueuemethod_SltHybridSpq?{int(OLT_Port)}")).first_selected_option.get_attribute("text")} != Q7) Fail',file = open(file_name, '+a'))
                if_temp_error = True

    if(if_temp_error == False):
        print(f"             [EMS1-6460][Advanced - Queue Method] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6460][Advanced - Queue Method] Result Fail",file = open(file_name, '+a'))

    print(f"======================================================================================",file = open(file_name, '+a'))

@retry()
def Advanced_VLANStacking(driver,url,ems_url,file_name,Pon_Name,Eth_Name,Pon_Name_L,Eth_Name_L,OLT_Port,OLT_Eth_Port):
    #[EMS1-6461][Advanced - VLAN Stacking] Result
    print(f"======================================================================================",file = open(file_name, '+a'))
    print(f"Advanced Application - VLAN Stacking Test Start",file = open(file_name, '+a'))

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "VLAN Stacking").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)
    e_swi.Advanced_VLAN_Stacking(driver,Pon_Name,"Tunnel Port","ffff","4094","7",file_name)
    e_swi.Advanced_VLAN_Stacking(driver,Eth_Name,"Tunnel Port","ffff","4094","7",file_name)

    #[EMS1-6461][Advanced - VLAN Stacking] Result check
    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"VLAN Stacking").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    time.sleep(1)

    if_temp_error = False

    if(Select(driver.find_element(By.NAME,f"rpenhanceVlanStack_SltPortRole?{int(OLT_Port)}")).first_selected_option.get_attribute("text") == "Tunnel Port"):
        print(f"             [EMS1-6461][Advanced - VLAN Stacking] {Pon_Name} Role (Tunnel Port) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6461][Advanced - VLAN Stacking] {Pon_Name} Role ({Select(driver.find_element(By.NAME,f"rpenhanceVlanStack_SltPortRole?{int(OLT_Port)}")).first_selected_option.get_attribute("text")} != Tunnel Port) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    
    if(driver.find_element(By.NAME,f"rpenhanceVlanStack_IptTextTunnelTPID?{int(OLT_Port)}").get_attribute("value") == "ffff"):
        print(f"             [EMS1-6461][Advanced - VLAN Stacking] {Pon_Name} TPID (ffff) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6461][Advanced - VLAN Stacking] {Pon_Name} TPID ({driver.find_element(By.NAME,f"rpenhanceVlanStack_IptTextTunnelTPID?{int(OLT_Port)}").get_attribute("value")} != ffff) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,f"rpenhanceVlanStack_SltPortRole?{int(OLT_Eth_Port)}")).first_selected_option.get_attribute("text") == "Tunnel Port"):
        print(f"             [EMS1-6461][Advanced - VLAN Stacking] {Eth_Name} Role (Tunnel Port) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6461][Advanced - VLAN Stacking] {Eth_Name} Role ({Select(driver.find_element(By.NAME,f"rpenhanceVlanStack_SltPortRole?{int(OLT_Eth_Port)}")).first_selected_option.get_attribute("text")} != Tunnel Port) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    
    if(driver.find_element(By.NAME,f"rpenhanceVlanStack_IptTextTunnelTPID?{int(OLT_Eth_Port)}").get_attribute("value") == "ffff"):
        print(f"             [EMS1-6461][Advanced - VLAN Stacking] {Eth_Name} TPID (ffff) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6461][Advanced - VLAN Stacking] {Eth_Name} TPID ({driver.find_element(By.NAME,f"rpenhanceVlanStack_IptTextTunnelTPID?{int(OLT_Eth_Port)}").get_attribute("value")} != ffff) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    driver.find_element(By.LINK_TEXT,"Port-based QinQ").click()

    if(driver.find_element(By.NAME,f"rpportbasedQinq_IptTextSPVID?{int(OLT_Port)}").get_attribute("value") == "4094"):
        print(f"             [EMS1-6461][Advanced - VLAN Stacking] {Pon_Name} SPVID (4094) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6461][Advanced - VLAN Stacking] {Pon_Name} SPVID ({driver.find_element(By.NAME,f"rpportbasedQinq_IptTextSPVID?{int(OLT_Port)}").get_attribute("value")} != 4094) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,f"rpportbasedQinq_SltPri?{int(OLT_Port)}")).first_selected_option.get_attribute("text") == "7"):
        print(f"             [EMS1-6461][Advanced - VLAN Stacking] {Pon_Name} Priority (7) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6461][Advanced - VLAN Stacking] {Pon_Name} Priority ({Select(driver.find_element(By.NAME,f"rpportbasedQinq_SltPri?{int(OLT_Port)}")).first_selected_option.get_attribute("text")} != 7) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,f"rpportbasedQinq_IptTextSPVID?{int(OLT_Eth_Port)}").get_attribute("value") == "4094"):
        print(f"             [EMS1-6461][Advanced - VLAN Stacking] {Eth_Name} SPVID (4094) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6461][Advanced - VLAN Stacking] {Eth_Name} SPVID ({driver.find_element(By.NAME,f"rpportbasedQinq_IptTextSPVID?{int(OLT_Eth_Port)}").get_attribute("value")} != 4094) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,f"rpportbasedQinq_SltPri?{int(OLT_Eth_Port)}")).first_selected_option.get_attribute("text") == "7"):
        print(f"             [EMS1-6461][Advanced - VLAN Stacking] {Eth_Name} Priority (7) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6461][Advanced - VLAN Stacking] {Eth_Name} Priority ({Select(driver.find_element(By.NAME,f"rpportbasedQinq_SltPri?{int(OLT_Eth_Port)}")).first_selected_option.get_attribute("text")} != 7) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(if_temp_error == False):
        print(f"             [EMS1-6461][Advanced - VLAN Stacking] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6461][Advanced - VLAN Stacking] Result Fail",file = open(file_name, '+a'))

    print(f"======================================================================================",file = open(file_name, '+a'))

@retry()
def Advanced_Multicast(driver,url,ems_url,file_name,Pon_Name,Eth_Name,Pon_Name_L,Eth_Name_L,OLT_Port,OLT_Eth_Port):
    #[EMS1-6465][Advanced - Multicast - Port]Port Apply Result
    #[EMS1-6559][Advanced - Multicast - IGMP Action]
    #[EMS1-6560][Advanced - Multicast Channel - New] Result
    print(f"======================================================================================",file = open(file_name, '+a'))
    print(f"Advanced Application - Multicast Test Start",file = open(file_name, '+a'))

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Multicast").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    e_swi.Advanced_Multicast_Port_Apply(driver,Pon_Name,False,'None',file_name)
    e_swi.Advanced_Multicast_Port_Apply(driver,Eth_Name,False,"Fixed",file_name)
    e_swi.Advanced_Multicast_Mode_Apply(driver,"Snooping",True,"16711450","16711450","7",True,"Drop","Drop","Ani vlan","Ani vlan",file_name)
    driver.find_element(By.ID,"advance_multicast_channelprofile_new_btn").click()
    e_swi.Advanced_Multicast_Channel(driver,True,"224.0.0.0","239.255.255.255","4000","7","10.10.10.1","32","6000","100","7200",file_name)  
    

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"Multicast").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    driver.find_element(By.LINK_TEXT,"Multicast Setting").click()
    time.sleep(1)
    #[EMS1-6465][Advanced - Multicast - Port]Port Apply Result check
    if_temp_error = False
    for i in range(1,driver.find_elements(By.NAME,"RpIGMP_ChkIGMPImmLveActive").__len__()+1):
        if(driver.find_element(By.XPATH,f"/html/body/form/table[2]/tbody/tr[{i+1}]/td[1]").text == Pon_Name_L):
            if(driver.find_element(By.XPATH,f"/html/body/form/table[2]/tbody/tr[{i+1}]/td[2]/input").is_selected() == False):
                print(f"             [EMS1-6465][Advanced - Multicast - Port] {Pon_Name} Port Apply Immed_Leave (False) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6465][Advanced - Multicast - Port] {Pon_Name} Port Apply Immed_Leave ({driver.find_element(By.XPATH,f"/html/body/form/table[2]/tbody/tr[{i+1}]/td[2]/input").is_selected()} != False) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(Select(driver.find_element(By.NAME,f"RpIGMP_querierMode_select?{int(OLT_Port)}")).first_selected_option.get_attribute("text") == "Edge"):
                print(f"             [EMS1-6465][Advanced - Multicast - Port] {Pon_Name} Port Apply IGMP (Edge) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6465][Advanced - Multicast - Port] {Pon_Name} Port Apply IGMP ({Select(driver.find_element(By.NAME,f"RpIGMP_querierMode_select?{int(OLT_Port)}")).first_selected_option.get_attribute("text")} != Edge) Fail',file = open(file_name, '+a'))
                if_temp_error = True
        
    for k in range(1,driver.find_elements(By.NAME,"RpIGMP_ChkIGMPImmLveActive").__len__()+1):
        if(driver.find_element(By.XPATH,f"/html/body/form/table[2]/tbody/tr[{k+1}]/td[1]").text == Eth_Name_L):

            if(driver.find_element(By.XPATH,f"/html/body/form/table[2]/tbody/tr[{k+1}]/td[2]/input").is_selected() == False):
                print(f"             [EMS1-6465][Advanced - Multicast - Port] {Eth_Name} Port Apply Immed_Leave (False) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6465][Advanced - Multicast - Port] {Eth_Name} Port Apply Immed_Leave ({driver.find_element(By.XPATH,f"/html/body/form/table[2]/tbody/tr[{k+1}]/td[2]/input").is_selected()} != False) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(Select(driver.find_element(By.NAME,f"RpIGMP_querierMode_select?{int(OLT_Eth_Port)}")).first_selected_option.get_attribute("text") == "Fixed"):
                print(f"             [EMS1-6465][Advanced - Multicast - Port] {Eth_Name} Port Apply IGMP (Fixed) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6465][Advanced - Multicast - Port] {Eth_Name} Port Apply IGMP ({Select(driver.find_element(By.NAME,f"RpIGMP_querierMode_select?{int(OLT_Eth_Port)}")).first_selected_option.get_attribute("text")} != Fixed) Fail',file = open(file_name, '+a'))
                if_temp_error = True

    if(if_temp_error == False):
        print(f"             [EMS1-6465][Advanced - Multicast - Port] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6465][Advanced - Multicast - Port] Result Fail",file = open(file_name, '+a'))
    print(f"--------------------------------------------------------------------------------------",file = open(file_name, '+a'))
    #[EMS1-6559][Advanced - Multicast - IGMP Action] check
    if_temp_error = False
    if(driver.find_element(By.XPATH,"/html/body/form/table[1]/tbody/tr[1]/td[2]/div[1]/input[2]").is_selected() == True):
        print(f"             [EMS1-6559][Advanced - Multicast - IGMP Action] Active (True) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6559][Advanced - Multicast - IGMP Action] Active ({driver.find_element(By.XPATH,"/html/body/form/table[1]/tbody/tr[1]/td[2]/div[1]/input[2]").is_selected()} != True) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"RpIGMP_ChkMLDenable").is_selected() == True):
        print(f"             [EMS1-6559][Advanced - Multicast - IGMP Action] MLD (True) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6559][Advanced - Multicast - IGMP Action] MLD ({driver.find_element(By.NAME,"RpIGMP_ChkMLDenable").is_selected()} != True) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"RpIGMP_IptHostTimeout").get_attribute("value") == "16711450"):
        print(f"             [EMS1-6559][Advanced - Multicast - IGMP Action] Host_Timeout (16711450) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6559][Advanced - Multicast - IGMP Action] Host_Timeout ({driver.find_element(By.NAME,"RpIGMP_IptHostTimeout").get_attribute("value")} != 16711450) Pass',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"RpIGMP_IptLeaveTimeout").get_attribute("value") == "16711450"):
        print(f"             [EMS1-6559][Advanced - Multicast - IGMP Action] Leave _Timeout (16711450) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6559][Advanced - Multicast - IGMP Action] Leave _Timeout ({driver.find_element(By.NAME,"RpIGMP_IptLeaveTimeout").get_attribute("value")} != 16711450) Pass',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"RpIGMP_Slt8021PPriority")).first_selected_option.get_attribute("text") == "7"):
        print(f"             [EMS1-6559][Advanced - Multicast - IGMP Action] Priority (7) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6559][Advanced - Multicast - IGMP Action] Priority ({Select(driver.find_element(By.NAME,"RpIGMP_Slt8021PPriority")).first_selected_option.get_attribute("text")} != 7) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"RpIGMP_ChkV3mode").is_selected() == True):
        print(f"             [EMS1-6559][Advanced - Multicast - IGMP Action] MGMDv3 (True) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6559][Advanced - Multicast - IGMP Action] MGMDv3 ({driver.find_element(By.NAME,"RpIGMP_ChkV3mode").is_selected()} != True) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.XPATH,"/html/body/form/table[1]/tbody/tr[3]/td[2]/input[2]").is_selected() == True):
        print(f"             [EMS1-6559][Advanced - Multicast - IGMP Action] Multicast_Frame (True) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6559][Advanced - Multicast - IGMP Action] Multicast_Frame ({driver.find_element(By.XPATH,"/html/body/form/table[1]/tbody/tr[3]/td[2]/input[2]").is_selected()} != True) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.XPATH,"/html/body/form/table[1]/tbody/tr[4]/td[2]/input[2]").is_selected() == True):
        print(f"             [EMS1-6559][Advanced - Multicast - IGMP Action] Multicast_Group (True) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6559][Advanced - Multicast - IGMP Action] Multicast_Group ({driver.find_element(By.XPATH,"/html/body/form/table[1]/tbody/tr[4]/td[2]/input[2]").is_selected()} != True) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.XPATH,"/html/body/form/table[1]/tbody/tr[5]/td[2]/input[2]").is_selected() == True):
        print(f"             [EMS1-6559][Advanced - Multicast - IGMP Action] Report_Tag (True) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6559][Advanced - Multicast - IGMP Action] Report_Tag ({driver.find_element(By.XPATH,"/html/body/form/table[1]/tbody/tr[5]/td[2]/input[2]").is_selected()} != True) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.XPATH,"/html/body/form/table[1]/tbody/tr[6]/td[2]/input[2]").is_selected() == True):
        print(f"             [EMS1-6559][Advanced - Multicast - IGMP Action] Query_Tag (True) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6559][Advanced - Multicast - IGMP Action] Query_Tag ({driver.find_element(By.XPATH,"/html/body/form/table[1]/tbody/tr[6]/td[2]/input[2]").is_selected()} != True) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(if_temp_error == False):
        print(f"             [EMS1-6559][Advanced - Multicast - IGMP Action] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6559][Advanced - Multicast - IGMP Action] Result Fail",file = open(file_name, '+a'))

    print(f"======================================================================================",file = open(file_name, '+a'))

    #[EMS1-6560][Advanced - Multicast Channel - New] Result check
    driver.find_element(By.LINK_TEXT,"Mcast Channel").click()
    time.sleep(1)

    for i in range(2,driver.find_elements(By.NAME,"rpMcastChannel_ChkTabDelete").__len__()+2):
        driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[3]/tbody/tr[{(2*i)+1}]/td[2]/div/a").click()
        time.sleep(1)
        if(driver.find_element(By.NAME,"rpMcastChannel_IptStartGroupIp").get_attribute("value") == "224.0.0.0"):
            break

    if_temp_error = False
    if(driver.find_element(By.NAME,"rpMcastChannel_ChkActiveEnable").is_selected() == True):
        print(f"             [EMS1-6560][Advanced - Multicast Channel - New] Active (True) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6560][Advanced - Multicast Channel - New] Active ({driver.find_element(By.NAME,"rpMcastChannel_ChkActiveEnable").is_selected()} != True) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    
    if(driver.find_element(By.NAME,"rpMcastChannel_IptStartGroupIp").get_attribute("value") == "224.0.0.0"):
        print(f"             [EMS1-6560][Advanced - Multicast Channel - New] Star_IP (224.0.0.0) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6560][Advanced - Multicast Channel - New] Star_IP ({driver.find_element(By.NAME,"rpMcastChannel_IptStartGroupIp").get_attribute("value")} != 224.0.0.0) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpMcastChannel_IptEndGroupIp").get_attribute("value") == "239.255.255.255"):
        print(f"             [EMS1-6560][Advanced - Multicast Channel - New] End_IP (239.255.255.255) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6560][Advanced - Multicast Channel - New] End_IP ({driver.find_element(By.NAME,"rpMcastChannel_IptEndGroupIp").get_attribute("value")} != 239.255.255.255) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpMcastChannel_IptVlan").get_attribute("value") == "4000"):
        print(f"             [EMS1-6560][Advanced - Multicast Channel - New] Vlan (4000) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6560][Advanced - Multicast Channel - New] Vlan ({driver.find_element(By.NAME,"rpMcastChannel_IptVlan").get_attribute("value")} != 4000) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rpMcastChannel_SltPbit")).first_selected_option.get_attribute("text") == "7"):
        print(f"             [EMS1-6560][Advanced - Multicast Channel - New] Pbit (7) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6560][Advanced - Multicast Channel - New] Pbit ({Select(driver.find_element(By.NAME,"rpMcastChannel_SltPbit")).first_selected_option.get_attribute("text")} != 7) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpMcastChannel_IptSrcIp").get_attribute("value") == "10.10.10.1"):
        print(f"             [EMS1-6560][Advanced - Multicast Channel - New] Src_IP (10.10.10.1) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6560][Advanced - Multicast Channel - New] Src_IP ({driver.find_element(By.NAME,"rpMcastChannel_IptSrcIp").get_attribute("value")} != 10.10.10.1) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpMcastChannel_IptPackageMember").get_attribute("value") == "32"):
        print(f"             [EMS1-6560][Advanced - Multicast Channel - New] package_member (32) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6560][Advanced - Multicast Channel - New] package_member ({driver.find_element(By.NAME,"rpMcastChannel_IptPackageMember").get_attribute("value")} != 32) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpMcastChannel_IptPreviewDuration").get_attribute("value") == "6000"):
        print(f"             [EMS1-6560][Advanced - Multicast Channel - New] preview_duration (6000) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6560][Advanced - Multicast Channel - New] preview_duration ({driver.find_element(By.NAME,"rpMcastChannel_IptPreviewDuration").get_attribute("value")} != 6000) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpMcastChannel_IptPreviewCount").get_attribute("value") == "100"):
        print(f"             [EMS1-6560][Advanced - Multicast Channel - New] preview_count (100) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6560][Advanced - Multicast Channel - New] preview_count ({driver.find_element(By.NAME,"rpMcastChannel_IptPreviewCount").get_attribute("value")} != 100) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpMcastChannel_IptPreviewBlackout").get_attribute("value") == "7200"):
        print(f"             [EMS1-6560][Advanced - Multicast Channel - New] preview_blackout (7200) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6560][Advanced - Multicast Channel - New] preview_blackout ({driver.find_element(By.NAME,"rpMcastChannel_IptPreviewBlackout").get_attribute("value")} != 7200) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(if_temp_error == False):
        print(f"             [EMS1-6560][Advanced - Multicast Channel - New] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6560][Advanced - Multicast Channel - New] Result Fail",file = open(file_name, '+a'))

    #[EMS1-6561][Advanced - Multicast Channel - Modify] Result
    
    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Multicast").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()

    for i in range(1,driver.find_elements(By.NAME,"advance_multicast_channelprofile_checkbox").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[21]/div/div[3]/div[1]/div[{i+1}]/div[3]").text
        if(ele == '224.0.0.0'):
            driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[21]/div/div[3]/div[1]/div[{i+1}]/div[8]/label").click()
            time.sleep(1)
            break
    driver.find_element(By.ID,"advance_multicast_channelprofile_mod_btn").click()
    e_swi.Advanced_Multicast_Channel(driver,True,"224.0.0.0","239.255.255.255","4000","0","10.10.10.11","1","1","1","1",file_name)

    #[EMS1-6561][Advanced - Multicast Channel - Modify] Result check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"Multicast").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    driver.find_element(By.LINK_TEXT,"Multicast Setting").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"Mcast Channel").click()
    time.sleep(1)

    for i in range(2,driver.find_elements(By.NAME,"rpMcastChannel_ChkTabDelete").__len__()+2):
        driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[3]/tbody/tr[{(2*i)+1}]/td[2]/div/a").click()
        time.sleep(1)
        if(driver.find_element(By.NAME,"rpMcastChannel_IptStartGroupIp").get_attribute("value") == "224.0.0.0"):
            break

    if_temp_error = False
    if(driver.find_element(By.NAME,"rpMcastChannel_ChkActiveEnable").is_selected() == True):
        print(f"             [EMS1-6561][Advanced - Multicast Channel - Modify] Active (True) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6561][Advanced - Multicast Channel - Modify] Active ({driver.find_element(By.NAME,"rpMcastChannel_ChkActiveEnable").is_selected()} != True) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    
    if(driver.find_element(By.NAME,"rpMcastChannel_IptStartGroupIp").get_attribute("value") == "224.0.0.0"):
        print(f"             [EMS1-6561][Advanced - Multicast Channel - Modify] Star_IP (224.0.0.0) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6561][Advanced - Multicast Channel - Modify] Star_IP ({driver.find_element(By.NAME,"rpMcastChannel_IptStartGroupIp").get_attribute("value")} != 224.0.0.0) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpMcastChannel_IptEndGroupIp").get_attribute("value") == "239.255.255.255"):
        print(f"             [EMS1-6561][Advanced - Multicast Channel - Modify] End_IP (239.255.255.255) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6561][Advanced - Multicast Channel - Modify] End_IP ({driver.find_element(By.NAME,"rpMcastChannel_IptEndGroupIp").get_attribute("value")} != 239.255.255.255) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpMcastChannel_IptVlan").get_attribute("value") == "4000"):
        print(f"             [EMS1-6561][Advanced - Multicast Channel - Modify] Vlan (4000) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6561][Advanced - Multicast Channel - Modify] Vlan ({driver.find_element(By.NAME,"rpMcastChannel_IptVlan").get_attribute("value")} != 4000) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,"rpMcastChannel_SltPbit")).first_selected_option.get_attribute("text") == "0"):
        print(f"             [EMS1-6561][Advanced - Multicast Channel - Modify] Pbit (0) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6561][Advanced - Multicast Channel - Modify] Pbit ({Select(driver.find_element(By.NAME,"rpMcastChannel_SltPbit")).first_selected_option.get_attribute("text")} != 0) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpMcastChannel_IptSrcIp").get_attribute("value") == "10.10.10.11"):
        print(f"             [EMS1-6561][Advanced - Multicast Channel - Modify] Src_IP (10.10.10.11) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6561][Advanced - Multicast Channel - Modify] Src_IP ({driver.find_element(By.NAME,"rpMcastChannel_IptSrcIp").get_attribute("value")} != 10.10.10.11) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpMcastChannel_IptPackageMember").get_attribute("value") == "1"):
        print(f"             [EMS1-6561][Advanced - Multicast Channel - Modify] package_member (1) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6561][Advanced - Multicast Channel - Modify] package_member ({driver.find_element(By.NAME,"rpMcastChannel_IptPackageMember").get_attribute("value")} != 1) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpMcastChannel_IptPreviewDuration").get_attribute("value") == "1"):
        print(f"             [EMS1-6561][Advanced - Multicast Channel - Modify] preview_duration (1) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6561][Advanced - Multicast Channel - Modify] preview_duration ({driver.find_element(By.NAME,"rpMcastChannel_IptPreviewDuration").get_attribute("value")} != 1) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpMcastChannel_IptPreviewCount").get_attribute("value") == "1"):
        print(f"             [EMS1-6561][Advanced - Multicast Channel - Modify] preview_count (1) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6561][Advanced - Multicast Channel - Modify] preview_count ({driver.find_element(By.NAME,"rpMcastChannel_IptPreviewCount").get_attribute("value")} != 1) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpMcastChannel_IptPreviewBlackout").get_attribute("value") == "1"):
        print(f"             [EMS1-6561][Advanced - Multicast Channel - Modify] preview_blackout (1) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6561][Advanced - Multicast Channel - Modify] preview_blackout ({driver.find_element(By.NAME,"rpMcastChannel_IptPreviewBlackout").get_attribute("value")} != 1) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(if_temp_error == False):
        print(f"             [EMS1-6561][Advanced - Multicast Channel - Modify] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6561][Advanced - Multicast Channel - Modify] Result Fail",file = open(file_name, '+a'))

    #[EMS1-6562][Advanced - Multicast Channel - Delete] Result

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Multicast").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()

    for i in range(1,driver.find_elements(By.NAME,"advance_multicast_channelprofile_checkbox").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[21]/div/div[3]/div[1]/div[{i+1}]/div[3]").text
        if(ele == '224.0.0.0'):
            driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[21]/div/div[3]/div[1]/div[{i+1}]/div[8]/label").click()
            time.sleep(1)
            break
    driver.find_element(By.ID,"advance_multicast_channelprofile_del_btn").click()

    #[EMS1-6562][Advanced - Multicast Channel - Delete] Result check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"Multicast").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    driver.find_element(By.LINK_TEXT,"Multicast Setting").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"Mcast Channel").click()
    time.sleep(1)
    if_temp_error = False
    for i in range(2,driver.find_elements(By.NAME,"rpMcastChannel_ChkTabDelete").__len__()+2):
        driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[3]/tbody/tr[{(2*i)+1}]/td[2]/div/a").click()
        time.sleep(1)
        if(driver.find_element(By.NAME,"rpMcastChannel_IptStartGroupIp").get_attribute("value") == "224.0.0.0"):
            if_temp_error=True
            break
    
    if(if_temp_error==False):
        print(f"             [EMS1-6562][Advanced - Multicast Channel - Delete] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6562][Advanced - Multicast Channel - Delete] Result Fail",file = open(file_name, '+a'))

    #[EMS1-6563][Advanced - Multicast Channel - Page Switch]

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Multicast").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    for i in range(1,23,2):
        driver.find_element(By.ID,"advance_multicast_channelprofile_new_btn").click()
        e_swi.Advanced_Multicast_Channel(driver,True,f"224.0.0.{i}",f"224.0.0.{i+1}","4000","7","10.10.10.1","32","6000","100","7200",file_name)  
        msg = e_swi.alert_accept_text(driver)
        try:
            e_pro.Close(driver)
        except:
            pass 
    driver.find_element(By.ID,'btnNextPage').click()
    time.sleep(1)
    if(driver.find_element(By.XPATH,'//*[@id="advance_multicast_channelprofile_table"]/div[2]/div[1]').text == "11"):
        print(f"             [EMS1-6563][Advanced - Multicast Channel - Page Switch] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6563][Advanced - Multicast Channel - Page Switch] Result Fail",file = open(file_name, '+a'))
    e_mod.Checkbox_EMS(driver,"advance_multicast_channelprofile_checkbox",True)
    driver.find_element(By.ID,"advance_multicast_channelprofile_del_btn").click()
    time.sleep(1)
    msg = e_swi.alert_accept_text(driver)
    try:
        e_pro.Close(driver)
    except:
        pass
    time.sleep(1)
    e_mod.Checkbox_EMS(driver,"advance_multicast_channelprofile_checkbox",True)
    driver.find_element(By.ID,"advance_multicast_channelprofile_del_btn").click()
    time.sleep(1)
    msg = e_swi.alert_accept_text(driver)
    try:
        e_pro.Close(driver)
    except:
        pass

    print(f"======================================================================================",file = open(file_name, '+a'))

@retry()
def Advanced_IP(driver,url,ems_url,file_name,Pon_Name,Eth_Name,Pon_Name_L,Eth_Name_L,OLT_Port,OLT_Eth_Port):
    #[EMS1-6462][Advanced - IP Source Guard - DHCP Snooping] Result
    print(f"======================================================================================",file = open(file_name, '+a'))
    print(f"Advanced Application - IP Source Guard Test Start",file = open(file_name, '+a'))

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "IP Source Guard").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    e_swi.Advanced_IP_Source(driver,True,"4094",file_name)

    #[EMS1-6462][Advanced - IP Source Guard - DHCP Snooping] Result check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"IP Source Guard").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    driver.find_element(By.LINK_TEXT,"DHCP Snooping").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"Configure").click()
    time.sleep(1)
    
    if_temp_error = False
    if(driver.find_element(By.NAME,"rpDhcpSnpConf_Chk_Active").is_selected() == True):
        print(f"             [EMS1-6462][Advanced - IP Source Guard - DHCP Snooping] Active (True) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6462][Advanced - IP Source Guard - DHCP Snooping] Active ({driver.find_element(By.NAME,"rpDhcpSnpConf_Chk_Active").is_selected()} != True) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    
    if(driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[5]/td[2]/div/input[1]").is_selected() == True and driver.find_element(By.NAME,"rpDhcpSnpConf_Ipt_DhcpVlan").get_attribute("value") == "4094"):
        print(f"             [EMS1-6462][Advanced - IP Source Guard - DHCP Snooping] DHCP Vlan (True) (4094) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6462][Advanced - IP Source Guard - DHCP Snooping] DHCP Vlan ({driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[2]/td/table/tbody/tr[5]/td[2]/div/input[1]").is_selected()} != True) ({driver.find_element(By.NAME,"rpDhcpSnpConf_Ipt_DhcpVlan").get_attribute("value")} != 4094) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(if_temp_error == False):
        print(f"             [EMS1-6462][Advanced - IP Source Guard - DHCP Snooping] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6462][Advanced - IP Source Guard - DHCP Snooping] Result Fail",file = open(file_name, '+a'))

    #[EMS1-6564][Advanced - IP Source Guard - Port Configure] Port Configure Apply Result
    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "IP Source Guard").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    e_swi.Advanced_DHCP_Snooping(driver,Pon_Name,"Trusted","2048",file_name)
    e_swi.Advanced_DHCP_Snooping(driver,Eth_Name,"Trusted","2048",file_name)

    #[EMS1-6564][Advanced - IP Source Guard - Port Configure] Port Configure Apply Result check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"IP Source Guard").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    driver.find_element(By.LINK_TEXT,"DHCP Snooping").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"Configure").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"Port").click()
    time.sleep(1)

    if_temp_error = False
    if(Select(driver.find_element(By.NAME,f"rpDhcpSnpConfI_Sel_TrustState?{int(OLT_Port)}")).first_selected_option.get_attribute("text") == "Trusted"):
        print(f"             [EMS1-6564][Advanced - IP Source Guard - Port Configure] {Pon_Name} Port Configure Apply state (Trusted) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6564][Advanced - IP Source Guard - Port Configure] {Pon_Name} Port Configure Apply state ({Select(driver.find_element(By.NAME,f"rpDhcpSnpConfI_Sel_TrustState?{int(OLT_Port)}")).first_selected_option.get_attribute("text")} != Trusted) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,f"rpDhcpSnpConfI_Ipt_Rate?{int(OLT_Port)}").get_attribute("value") == "2048"):
        print(f"             [EMS1-6564][Advanced - IP Source Guard - Port Configure] {Pon_Name} Port Configure Apply Rate (2048) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6564][Advanced - IP Source Guard - Port Configure] {Pon_Name} Port Configure Apply Rate ({driver.find_element(By.NAME,f"rpDhcpSnpConfI_Ipt_Rate?{int(OLT_Port)}").get_attribute("value")} != 2048) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    
    if(Select(driver.find_element(By.NAME,f"rpDhcpSnpConfI_Sel_TrustState?{int(OLT_Eth_Port)}")).first_selected_option.get_attribute("text") == "Trusted"):
        print(f"             [EMS1-6564][Advanced - IP Source Guard - Port Configure] {Eth_Name} Port Configure Apply state (Trusted) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6564][Advanced - IP Source Guard - Port Configure] {Eth_Name} Port Configure Apply state ({Select(driver.find_element(By.NAME,f"rpDhcpSnpConfI_Sel_TrustState?{int(OLT_Eth_Port)}")).first_selected_option.get_attribute("text")} != Trusted) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,f"rpDhcpSnpConfI_Ipt_Rate?{int(OLT_Eth_Port)}").get_attribute("value") == "2048"):
        print(f"             [EMS1-6564][Advanced - IP Source Guard - Port Configure] {Eth_Name} Port Configure Apply Rate (2048) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6564][Advanced - IP Source Guard - Port Configure] {Eth_Name} Port Configure Apply Rate ({driver.find_element(By.NAME,f"rpDhcpSnpConfI_Ipt_Rate?{int(OLT_Eth_Port)}").get_attribute("value")} != 2048) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(if_temp_error == False):
        print(f"             [EMS1-6564][Advanced - IP Source Guard - Port Configure] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6564][Advanced - IP Source Guard - Port Configure] Result Fail",file = open(file_name, '+a'))

    #[EMS1-6565][Advanced - IP Source Guard - Static Binding - New] Result

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "IP Source Guard").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)
    driver.find_element(By.ID,"advance_ipsg_static_profile_new_btn").click()
    e_swi.Advanced_Static_Binding(driver,"00:01:02:03:04:05","10.10.10.1","4094","Any",file_name)


    #[EMS1-6565][Advanced - IP Source Guard - Static Binding - New] Result check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"IP Source Guard").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    driver.find_element(By.LINK_TEXT,"Static Binding").click()
    time.sleep(1)

    for i in range(1,driver.find_elements(By.NAME,"rpIpsgStatic_Chk_Del").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td/table/tbody/tr[{i*2}]/td[7]/div").text
        if(ele == '4094'):
            driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td/table/tbody/tr[{i*2}]/td[2]/a").click()
            time.sleep(1)
    
    if_temp_error = False
    if(driver.find_element(By.NAME,"rpIpsgStatic_Ipt_MacAddr1").get_attribute("value") == "00" and driver.find_element(By.NAME,"rpIpsgStatic_Ipt_MacAddr2").get_attribute("value") == "01" and driver.find_element(By.NAME,"rpIpsgStatic_Ipt_MacAddr3").get_attribute("value") == "02" and driver.find_element(By.NAME,"rpIpsgStatic_Ipt_MacAddr4").get_attribute("value") == "03" and driver.find_element(By.NAME,"rpIpsgStatic_Ipt_MacAddr5").get_attribute("value") == "04" and driver.find_element(By.NAME,"rpIpsgStatic_Ipt_MacAddr6").get_attribute("value") == "05"):
        print(f"             [EMS1-6565][Advanced - IP Source Guard - Static Binding - New] MAC_Address (00:01:02:03:04:05) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6565][Advanced - IP Source Guard - Static Binding - New] MAC_Address ({driver.find_element(By.NAME,"rpIpsgStatic_Ipt_MacAddr1").get_attribute("value")} != 00 {driver.find_element(By.NAME,"rpIpsgStatic_Ipt_MacAddr2").get_attribute("value")} != 01 {driver.find_element(By.NAME,"rpIpsgStatic_Ipt_MacAddr3").get_attribute("value")} != 02 {driver.find_element(By.NAME,"rpIpsgStatic_Ipt_MacAddr4").get_attribute("value")} != 03 {driver.find_element(By.NAME,"rpIpsgStatic_Ipt_MacAddr5").get_attribute("value")} != 04 {driver.find_element(By.NAME,"rpIpsgStatic_Ipt_MacAddr6").get_attribute("value")} != 05) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    
    if(driver.find_element(By.NAME,"rpIpsgStatic_Ipt_IpAddr").get_attribute("value") == "10.10.10.1"):
        print(f"             [EMS1-6565][Advanced - IP Source Guard - Static Binding - New] IP_Address (10.10.10.1) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6565][Advanced - IP Source Guard - Static Binding - New] IP_Address ({driver.find_element(By.NAME,"rpIpsgStatic_Ipt_IpAddr").get_attribute("value")} != 10.10.10.1) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpIpsgStatic_Ipt_VID").get_attribute("value") == "4094"):
        print(f"             [EMS1-6565][Advanced - IP Source Guard - Static Binding - New] VLAN (4094) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6565][Advanced - IP Source Guard - Static Binding - New] VLAN ({driver.find_element(By.NAME,"rpIpsgStatic_Ipt_VID").get_attribute("value")} != 4094) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[2]/td/table[1]/tbody/tr[9]/td[2]/div/input").is_selected() == True):
        print(f"             [EMS1-6565][Advanced - IP Source Guard - Static Binding - New] Port (True) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6565][Advanced - IP Source Guard - Static Binding - New] Port ({driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[2]/td/table[1]/tbody/tr[9]/td[2]/div/input").is_selected()} != True) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(if_temp_error == False):
        print(f"             [EMS1-6565][Advanced - IP Source Guard - Static Binding - New] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6565][Advanced - IP Source Guard - Static Binding - New] Result Fail",file = open(file_name, '+a'))

    #[EMS1-6566][Advanced - IP Source Guard - Static Binding - Modify] Result

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "IP Source Guard").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)

    if_find = False
    for i in range(1,int(driver.find_element(By.ID,"pageTotal1").text)+1):
        for j in range(1,driver.find_elements(By.NAME,"advance_ipsg_static_profile_checkbox").__len__()+1):
            ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[18]/div[2]/div[1]/div[{j}]/div[6]").text
            if(ele == '4094'):
                driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[18]/div[2]/div[1]/div[{j}]/div[8]/label").click()
                if_find =True
                time.sleep(1)
            if(if_find==True):
                break
        if(if_find==True):
            break 
        else:
            driver.find_element(By.ID,"btnNextPage1").click()
    driver.find_element(By.ID,"advance_ipsg_static_profile_mod_btn").click()
    time.sleep(1)
    e_swi.Advanced_Static_Binding(driver,"00:01:02:03:04:05","10.10.10.1","4094","1,8",file_name)

    #[EMS1-6566][Advanced - IP Source Guard - Static Binding - Modify] Result check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"IP Source Guard").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    driver.find_element(By.LINK_TEXT,"Static Binding").click()
    time.sleep(1)

    for i in range(1,driver.find_elements(By.NAME,"rpIpsgStatic_Chk_Del").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td/table/tbody/tr[{i*2}]/td[7]/div").text
        if(ele == '4094'):
            driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td/table/tbody/tr[{i*2}]/td[2]/a").click()
            time.sleep(1)
    
    if_temp_error = False
    if(driver.find_element(By.NAME,"rpIpsgStatic_Ipt_MacAddr1").get_attribute("value") == "00" and driver.find_element(By.NAME,"rpIpsgStatic_Ipt_MacAddr2").get_attribute("value") == "01" and driver.find_element(By.NAME,"rpIpsgStatic_Ipt_MacAddr3").get_attribute("value") == "02" and driver.find_element(By.NAME,"rpIpsgStatic_Ipt_MacAddr4").get_attribute("value") == "03" and driver.find_element(By.NAME,"rpIpsgStatic_Ipt_MacAddr5").get_attribute("value") == "04" and driver.find_element(By.NAME,"rpIpsgStatic_Ipt_MacAddr6").get_attribute("value") == "05"):
        print(f"             [EMS1-6566][Advanced - IP Source Guard - Static Binding - Modify] MAC_Address (00:01:02:03:04:05) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6566][Advanced - IP Source Guard - Static Binding - Modify] MAC_Address ({driver.find_element(By.NAME,"rpIpsgStatic_Ipt_MacAddr1").get_attribute("value")} != 00 {driver.find_element(By.NAME,"rpIpsgStatic_Ipt_MacAddr2").get_attribute("value")} != 01 {driver.find_element(By.NAME,"rpIpsgStatic_Ipt_MacAddr3").get_attribute("value")} != 02 {driver.find_element(By.NAME,"rpIpsgStatic_Ipt_MacAddr4").get_attribute("value")} != 03 {driver.find_element(By.NAME,"rpIpsgStatic_Ipt_MacAddr5").get_attribute("value")} != 04 {driver.find_element(By.NAME,"rpIpsgStatic_Ipt_MacAddr6").get_attribute("value")} != 05) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    
    if(driver.find_element(By.NAME,"rpIpsgStatic_Ipt_IpAddr").get_attribute("value") == "10.10.10.1"):
        print(f"             [EMS1-6566][Advanced - IP Source Guard - Static Binding - Modify] IP_Address (10.10.10.1) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6566][Advanced - IP Source Guard - Static Binding - Modify] IP_Address ({driver.find_element(By.NAME,"rpIpsgStatic_Ipt_IpAddr").get_attribute("value")} != 10.10.10.1) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpIpsgStatic_Ipt_VID").get_attribute("value") == "4094"):
        print(f"             [EMS1-6566][Advanced - IP Source Guard - Static Binding - Modify] VLAN (4094) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6566][Advanced - IP Source Guard - Static Binding - Modify] VLAN ({driver.find_element(By.NAME,"rpIpsgStatic_Ipt_VID").get_attribute("value")} != 4094) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[2]/td/table[1]/tbody/tr[8]/td[3]/input[1]").is_selected() == True and driver.find_element(By.NAME,"rpIpsgStatic_Ipt_Port").get_attribute("value") == "1,8" ):
        print(f"             [EMS1-6566][Advanced - IP Source Guard - Static Binding - Modify] Port (True) (1,8) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6566][Advanced - IP Source Guard - Static Binding - Modify] Port ({driver.find_element(By.XPATH,"/html/body/form/table/tbody/tr[2]/td/table[1]/tbody/tr[8]/td[3]/input[1]").is_selected()} != True) ({driver.find_element(By.NAME,"rpIpsgStatic_Ipt_Port").get_attribute("value")} != 1,8) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(if_temp_error == False):
        print(f"             [EMS1-6566][Advanced - IP Source Guard - Static Binding - Modify] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6566][Advanced - IP Source Guard - Static Binding - Modify] Result Fail",file = open(file_name, '+a'))

    #[EMS1-6567][Advanced - IP Source Guard - Static Binding - Delete] Result

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "IP Source Guard").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)

    if_find = False
    for i in range(1,int(driver.find_element(By.ID,"pageTotal1").text)+1):
        for j in range(1,driver.find_elements(By.NAME,"advance_ipsg_static_profile_checkbox").__len__()+1):
            ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[18]/div[2]/div[1]/div[{j}]/div[6]").text
            if(ele == '4094'):
                driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[18]/div[2]/div[1]/div[{j}]/div[8]/label").click()
                if_find =True
                time.sleep(1)
            if(if_find==True):
                break 
        if(if_find==True):
            break
        else:
            driver.find_element(By.ID,"btnNextPage1").click()
    driver.find_element(By.ID,"advance_ipsg_static_profile_del_btn").click()
    time.sleep(1)

    #[EMS1-6567][Advanced - IP Source Guard - Static Binding - Delete] Result check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"IP Source Guard").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    driver.find_element(By.LINK_TEXT,"Static Binding").click()
    time.sleep(1)

    if_temp_error = False
    for i in range(1,driver.find_elements(By.NAME,"rpIpsgStatic_Chk_Del").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td/table/tbody/tr[{i*2}]/td[7]/div").text
        if(ele == '4094'):
            if_temp_error = True
    if(if_temp_error==False):
        print(f"             [EMS1-6567][Advanced - IP Source Guard - Static Binding - Delete] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6567][Advanced - IP Source Guard - Static Binding - Delete] Result Fail",file = open(file_name, '+a'))

    # [EMS1-6568][Advanced - IP Source Guard - Static Binding - Page Switch] Result
    
    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "IP Source Guard").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(2)
    for i in range(1,12):
        driver.find_element(By.ID,"advance_ipsg_static_profile_new_btn").click()
        e_swi.Advanced_Static_Binding(driver,"00:01:02:03:04:05","10.10.10.1",f"{i}","Any",file_name)
        time.sleep(2)
    driver.find_element(By.ID,'btnNextPage1').click()
    time.sleep(2)
    if(driver.find_element(By.XPATH,'//*[@id="advance_ipsg_static_profile_table"]/div[2]/div[1]').text == '11'):
        print(f"             [EMS1-6568][Advanced - IP Source Guard - Static Binding - Page Switch] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6568][Advanced - IP Source Guard - Static Binding - Page Switch] Result Fail",file = open(file_name, '+a'))

    for i in range(1,3):
        e_mod.Checkbox_EMS(driver,"advance_ipsg_static_profile_checkbox",True)
        driver.find_element(By.ID,"advance_ipsg_static_profile_del_btn").click()
        time.sleep(2)
        msg = e_swi.alert_accept_text(driver)
        try:
            e_pro.Close(driver)
        except:
            pass
    

    #[EMS1-6569][Advanced - IP Source Guard - VLAN Configure - Active Apply] Result

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "IP Source Guard").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)
    e_swi.Advanced_VLAN_Configure(driver,"4094","4094")

    #[EMS1-6569][Advanced - IP Source Guard - VLAN Configure - Active Apply] Result check

    if_temp_error = False
    for i in range(1,driver.find_elements(By.NAME,"advance_ipsg_vlan_information_checkbox").__len__()+3):
        ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[22]/div[2]/div/div[{i+1}]/div[1]/span").text
        if(ele == "4094"):
            if_temp_error = True
    if(if_temp_error==True):
        print(f"             [EMS1-6569][Advanced - IP Source Guard - VLAN Configure - Active Apply] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6569][Advanced - IP Source Guard - VLAN Configure - Active Apply] Result Fail",file = open(file_name, '+a'))
    print(f"--------------------------------------------------------------------------------------",file = open(file_name, '+a'))
    #[EMS1-6570][Advanced - IP Source Guard - VLAN Configure - Table] Apply  Result
    e_swi.Advanced_VLAN_Configure_Table(driver,4094,"Yes",True,True,file_name)
    #[EMS1-6570][Advanced - IP Source Guard - VLAN Configure - Table] Apply  Result check
    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"IP Source Guard").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    driver.find_element(By.LINK_TEXT,"DHCP Snooping").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"Configure").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"VLAN").click()
    time.sleep(1)
    driver.find_element(By.NAME,"rpDhcpSnpConfV_Ipt_StartVlan").send_keys(e_swi.Keys.CONTROL + 'a')
    driver.find_element(By.NAME,"rpDhcpSnpConfV_Ipt_StartVlan").send_keys("4094")
    driver.find_element(By.NAME,"rpDhcpSnpConfV_Ipt_EndVlan").send_keys(e_swi.Keys.CONTROL + 'a')
    driver.find_element(By.NAME,"rpDhcpSnpConfV_Ipt_EndVlan").send_keys("4094")
    driver.find_element(By.NAME,"rpDhcpSnpConfV_Btn_Apply1").click()
    time.sleep(1)
    if_find = False
    for i in range(1,driver.find_elements(By.NAME,"rpDhcpSnpConfV_Chk_Inf").__len__()+2):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td/table[1]/tbody/tr[{i*2}]/td[2]/div").text
        if(ele == '4094'):
            if_temp_error = False
            if(Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td/table[1]/tbody/tr[{i*2}]/td[3]/div/select")).first_selected_option.get_attribute("text") == "Yes"):
                print(f"             [EMS1-6570][Advanced - IP Source Guard - VLAN Configure - Table] Enable Result (Yes) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6570][Advanced - IP Source Guard - VLAN Configure - Table] Enable Result ({Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td/table[1]/tbody/tr[{i*2}]/td[3]/div/select")).first_selected_option.get_attribute("text")} != Yes) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td/table[1]/tbody/tr[{i*2}]/td[4]/div/input").is_selected() == True):
                print(f"             [EMS1-6570][Advanced - IP Source Guard - VLAN Configure - Table] Option82 Result (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6570][Advanced - IP Source Guard - VLAN Configure - Table] Option82 Result ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td/table[1]/tbody/tr[{i*2}]/td[4]/div/input").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td/table[1]/tbody/tr[{i*2}]/td[5]/div/input").is_selected() == True):
                print(f"             [EMS1-6570][Advanced - IP Source Guard - VLAN Configure - Table] Information Result (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6570][Advanced - IP Source Guard - VLAN Configure - Table] Information Result ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td/table[1]/tbody/tr[{i*2}]/td[5]/div/input").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            if_find = True
            break
    if if_find == False:    
        print(f"             [EMS1-6570][Advanced - IP Source Guard - VLAN Configure - Table] '4094' Not Found Test Fail",file = open(file_name, '+a'))
        if_temp_error = True
    if(if_temp_error==False):
        print(f"             [EMS1-6570][Advanced - IP Source Guard - VLAN Configure - Table] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6570][Advanced - IP Source Guard - VLAN Configure - Table] Result Fail",file = open(file_name, '+a'))

    print(f"======================================================================================",file = open(file_name, '+a'))

@retry()
def Advanced_Loop(driver,url,ems_url,file_name,Pon_Name,Eth_Name,Pon_Name_L,Eth_Name_L,OLT_Port,OLT_Eth_Port):
    #[EMS1-6463][Advanced - Loop Guard - Active Apply] Apply Result
    print(f"======================================================================================",file = open(file_name, '+a'))
    print(f"Advanced Application - Loop Guard Test Start",file = open(file_name, '+a'))

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Loop Guard").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    e_swi.Advanced_Loop_Guard_Apply(driver,True,"120",file_name)
    e_swi.Advanced_Loop_Guard_Port_Apply(driver,Pon_Name,True,"4094",file_name)
    e_swi.Advanced_Loop_Guard_Port_Apply(driver,Eth_Name,True,"4094",file_name)

    #[EMS1-6463][Advanced - Loop Guard - Active Apply] Apply Result check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"Loop Guard").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)

    if_temp_error = False
    if(driver.find_element(By.NAME,"rploopguard_ChkSwActive").is_selected() == True):
        print(f"             [EMS1-6463][Advanced - Loop Guard - Active Apply] Apply Active (True) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6463][Advanced - Loop Guard - Active Apply] Apply Active ({driver.find_element(By.NAME,"rploopguard_ChkSwActive").is_selected()} != True) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rploopguard_IptDetectionTime").get_attribute("value") == "120"):
        print(f"             [EMS1-6463][Advanced - Loop Guard - Active Apply] Apply Detection_Time (120) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6463][Advanced - Loop Guard - Active Apply] Apply Detection_Time ({driver.find_element(By.NAME,"rploopguard_IptDetectionTime").get_attribute("value")} != 120) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    
    if(if_temp_error==False):
        print(f"             [EMS1-6463][Advanced - Loop Guard - Active Apply] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6463][Advanced - Loop Guard - Active Apply] Result Fail",file = open(file_name, '+a'))
    print(f"--------------------------------------------------------------------------------------",file = open(file_name, '+a'))
    if_temp_error = False
    for i in range(1,driver.find_elements(By.NAME,"rploopguard_ChkPortActive").__len__()+1):
        if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*i)+1}]/td[2]/div").text == Pon_Name_L):
            if(driver.find_element(By.XPATH,f"//input[@value='?{OLT_Port}']").get_attribute("checked") == "true"):
                print(f"             [EMS1-6571][Advanced - Loop Guard - Port Apply] {Pon_Name} Port Apply Active (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'''             [EMS1-6571][Advanced - Loop Guard - Port Apply] {Pon_Name} Port Apply Active ({driver.find_element(By.XPATH,f"//input[@value='?{OLT_Port}']").get_attribute("checked")} != true) Fail''',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,f"rploopguard_IptVid?{int(OLT_Port)}").get_attribute("value") == "4094"):
                print(f"             [EMS1-6571][Advanced - Loop Guard - Port Apply] {Pon_Name} Port Apply Vid (4094) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6571][Advanced - Loop Guard - Port Apply] {Pon_Name} Port Apply Vid ({driver.find_element(By.NAME,f"rploopguard_IptVid?{int(OLT_Port)}").get_attribute("value")} != 4094) Fail',file = open(file_name, '+a'))
                if_temp_error = True
    for i in range(1,driver.find_elements(By.NAME,"rploopguard_ChkPortActive").__len__()+1):
        if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr/td/table[2]/tbody/tr[{(2*i)+1}]/td[2]/div").text == Eth_Name_L):

            if(driver.find_element(By.XPATH,f"//input[@value='?{OLT_Eth_Port}']").get_attribute("checked") == "true"):
                print(f"             [EMS1-6571][Advanced - Loop Guard - Port Apply] {Eth_Name} Port Apply Active (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'''             [EMS1-6571][Advanced - Loop Guard - Port Apply] {Eth_Name} Port Apply Active ({driver.find_element(By.XPATH,f"//input[@value='?{OLT_Eth_Port}']").get_attribute("checked")} != true) Fail''',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,f"rploopguard_IptVid?{int(OLT_Eth_Port)}").get_attribute("value") == "4094"):
                print(f"             [EMS1-6571][Advanced - Loop Guard - Port Apply] {Eth_Name} Port Apply Vid (4094) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6571][Advanced - Loop Guard - Port Apply] {Eth_Name} Port Apply Vid ({driver.find_element(By.NAME,f"rploopguard_IptVid?{int(OLT_Eth_Port)}").get_attribute("value")} != 4094) Fail',file = open(file_name, '+a'))
                if_temp_error = True

    if(if_temp_error==False):
        print(f"             [EMS1-6571][Advanced - Loop Guard - Port Apply] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6571][Advanced - Loop Guard - Port Apply] Result Fail",file = open(file_name, '+a'))

    print(f"======================================================================================",file = open(file_name, '+a'))

@retry()
def Advanced_PPPoE(driver,url,ems_url,file_name,Pon_Name,Eth_Name,Pon_Name_L,Eth_Name_L,OLT_Port,OLT_Eth_Port):
    #[EMS1-6464][Advanced - PPPoE IA - Active Apply] Result
    print(f"======================================================================================",file = open(file_name, '+a'))
    print(f"Advanced Application - PPPoE Test Start",file = open(file_name, '+a'))

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "PPPoE").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    e_swi.Advanced_PPPoE_IA_Apply(driver,True,file_name)

    #[EMS1-6464][Advanced - PPPoE IA - Active Apply] Result check
    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"PPPoE").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    driver.find_element(By.LINK_TEXT,"Click here").click()
    time.sleep(1)
    if_temp_error = False
    if(driver.find_element(By.NAME,"rpPPPoEIAConfig_ChkActive").is_selected() == True):
        print(f"             [EMS1-6464][Advanced - PPPoE IA - Active Apply] Result (True) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6464][Advanced - PPPoE IA - Active Apply] Result ({driver.find_element(By.NAME,"rpPPPoEIAConfig_ChkActive").is_selected()} != True) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    if(if_temp_error == False):
        print(f"             [EMS1-6464][Advanced - PPPoE IA - Active Apply] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6464][Advanced - PPPoE IA - Active Apply] Result Fail",file = open(file_name, '+a'))


    #[EMS1-6572][Advanced - PPPoE IA Option - New] Result

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "PPPoE").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    driver.find_element(By.ID,"advance_pppoe_option_profile_new_btn").click()
    e_swi.Advanced_PPPoE_IA_Option(driver,"4094","circuit","remote",file_name)

    #[EMS1-6572][Advanced - PPPoE IA Option - New] Result check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"PPPoE").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    driver.find_element(By.LINK_TEXT,"Click here").click()
    time.sleep(1)

    for i in range(1,driver.find_elements(By.NAME,"rpPPPoEIAConfig_ChkTabDelete").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td[2]/table[3]/tbody/tr[{i*2}]/td[2]/div/a").text
        if(ele == '4094'):
            driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td[2]/table[3]/tbody/tr[{i*2}]/td[2]/div/a").click()
            time.sleep(1)

    if_temp_error = False
    if(driver.find_element(By.NAME,"rpPPPoEIAConfig_IptTextVID").get_attribute("value") == "4094"):
        print(f"             [EMS1-6572][Advanced - PPPoE IA Option - New] VID (4094) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6572][Advanced - PPPoE IA Option - New] VID ({driver.find_element(By.NAME,"rpPPPoEIAConfig_IptTextVID").get_attribute("value")} != 4094) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpPPPoEIAConfig_IptTextoptCircuitId").get_attribute("value") == "circuit"):
        print(f"             [EMS1-6572][Advanced - PPPoE IA Option - New] Option_Circuit_Id (circuit) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6572][Advanced - PPPoE IA Option - New] Option_Circuit_Id ({driver.find_element(By.NAME,"rpPPPoEIAConfig_IptTextoptCircuitId").get_attribute("value")} != circuit) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpPPPoEIAConfig_IptTextoptRemoteId").get_attribute("value") == "remote"):
        print(f"             [EMS1-6572][Advanced - PPPoE IA Option - New] Option_Remote_Id (remote) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6572][Advanced - PPPoE IA Option - New] Option_Remote_Id ({driver.find_element(By.NAME,"rpPPPoEIAConfig_IptTextoptRemoteId").get_attribute("value")} != remote) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    
    if(if_temp_error==False):
        print(f"             [EMS1-6572][Advanced - PPPoE IA Option - New] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6572][Advanced - PPPoE IA Option - New] Result Fail",file = open(file_name, '+a'))

    #[EMS1-6573][Advanced - PPPoE IA Option - Modify] Result

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "PPPoE").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()

    if_find = False
    for i in range(1,int(driver.find_element(By.ID,"pageTotal1").text)+1):
        for j in range(1,driver.find_elements(By.NAME,"advance_pppoe_option_profile_checkbox").__len__()+1):
            ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[6]/div[2]/div[1]/div[{j}]/div[2]").text
            if(ele == '4094'):
                driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[6]/div[2]/div[1]/div[{j}]/div[5]/label").click()
                if_find =True
                time.sleep(1)
            if(if_find==True):
                break
        if(if_find==True):
            break 
        else:
            driver.find_element(By.ID,"btnNextPage1").click()
    
    driver.find_element(By.ID,"advance_pppoe_option_profile_mod_btn").click()
    e_swi.Advanced_PPPoE_IA_Option(driver,"4094","circuit_modify","remote_modify",file_name)

    #[EMS1-6573][Advanced - PPPoE IA Option - Modify] Result check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"PPPoE").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    driver.find_element(By.LINK_TEXT,"Click here").click()
    time.sleep(1)

    for i in range(1,driver.find_elements(By.NAME,"rpPPPoEIAConfig_ChkTabDelete").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td[2]/table[3]/tbody/tr[{i*2}]/td[2]/div/a").text
        if(ele == '4094'):
            driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td[2]/table[3]/tbody/tr[{i*2}]/td[2]/div/a").click()
            time.sleep(1)

    if_temp_error = False
    if(driver.find_element(By.NAME,"rpPPPoEIAConfig_IptTextVID").get_attribute("value") == "4094"):
        print(f"             [EMS1-6573][Advanced - PPPoE IA Option - Modify] VID (4094) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6573][Advanced - PPPoE IA Option - Modify] VID ({driver.find_element(By.NAME,"rpPPPoEIAConfig_IptTextVID").get_attribute("value")} != 4094) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpPPPoEIAConfig_IptTextoptCircuitId").get_attribute("value") == "circuit_modify"):
        print(f"             [EMS1-6573][Advanced - PPPoE IA Option - Modify] Option_Circuit_Id (circuit_modify) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6573][Advanced - PPPoE IA Option - Modify] Option_Circuit_Id ({driver.find_element(By.NAME,"rpPPPoEIAConfig_IptTextoptCircuitId").get_attribute("value")} != circuit_modify) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(driver.find_element(By.NAME,"rpPPPoEIAConfig_IptTextoptRemoteId").get_attribute("value") == "remote_modify"):
        print(f"             [EMS1-6573][Advanced - PPPoE IA Option - Modify] Option_Remote_Id (remote_modify) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6573][Advanced - PPPoE IA Option - Modify] Option_Remote_Id ({driver.find_element(By.NAME,"rpPPPoEIAConfig_IptTextoptRemoteId").get_attribute("value")} != remote_modify) Fail',file = open(file_name, '+a'))
        if_temp_error = True
    
    if(if_temp_error==False):
        print(f"             [EMS1-6573][Advanced - PPPoE IA Option - Modify] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6573][Advanced - PPPoE IA Option - Modify] Result Fail",file = open(file_name, '+a'))

    #[EMS1-6574][Advanced - PPPoE IA Option - Delete] Result

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "PPPoE").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()

    if_find = False
    for i in range(1,int(driver.find_element(By.ID,"pageTotal1").text)+1):
        for j in range(1,driver.find_elements(By.NAME,"advance_pppoe_option_profile_checkbox").__len__()+1):
            ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[6]/div[2]/div[1]/div[{j}]/div[2]").text
            if(ele == '4094'):
                driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[6]/div[2]/div[1]/div[{j}]/div[5]/label").click()
                if_find =True
                time.sleep(1)
            if(if_find==True):
                break 
        if(if_find==True):
            break
        else:
            driver.find_element(By.ID,"btnNextPage1").click()
    
    driver.find_element(By.ID,"advance_pppoe_option_profile_del_btn").click()
    time.sleep(1)
    msg = e_swi.alert_accept_text(driver)
    try:
        e_pro.Close(driver)
    except:
        pass

    #[EMS1-6574][Advanced - PPPoE IA Option - Delete] Result check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"PPPoE").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    driver.find_element(By.LINK_TEXT,"Click here").click()
    time.sleep(1)

    if_temp_error = False
    for i in range(1,driver.find_elements(By.NAME,"rpPPPoEIAConfig_ChkTabDelete").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td[2]/table[3]/tbody/tr[{i*2}]/td[2]/div/a").text
        if(ele == '4094'):
            if_temp_error = True
    if(if_temp_error==False):
        print(f"             [EMS1-6574][Advanced - PPPoE IA Option - Delete] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6574][Advanced - PPPoE IA Option - Delete] Result Fail",file = open(file_name, '+a'))

    #[EMS1-6575][Advanced - PPPoE IA Option - Page Switch] Result

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "PPPoE").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)
    for i in range(1,12):
        driver.find_element(By.ID,"advance_pppoe_option_profile_new_btn").click()
        e_swi.Advanced_PPPoE_IA_Option(driver,f"{i}","circuit","remote",file_name)
    driver.find_element(By.ID,'btnNextPage1').click()
    time.sleep(2)
    if(driver.find_element(By.XPATH,'//*[@id="advance_pppoe_option_profile_table"]/div[2]/div[1]').text == '11'):
        print(f"             [EMS1-6575][Advanced - PPPoE IA Option - Page Switch] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6575][Advanced - PPPoE IA Option - Page Switch] Result Fail",file = open(file_name, '+a'))

    for i in range(1,3):
        e_mod.Checkbox_EMS(driver,"advance_pppoe_option_profile_checkbox",True)
        driver.find_element(By.ID,"advance_pppoe_option_profile_del_btn").click()
        time.sleep(2)
        msg = e_swi.alert_accept_text(driver)
        try:
            e_pro.Close(driver)
        except:
            pass

    #[EMS1-6576][Advanced - PPPoE - Port Apply] Port Apply Result

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "PPPoE").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)
    e_swi.Advanced_PPPoE_Port_Apply(driver,Pon_Name,"Trusted",file_name)
    e_swi.Advanced_PPPoE_Port_Apply(driver,Eth_Name,"Trusted",file_name)

    #[EMS1-6576][Advanced - PPPoE - Port Apply] Port Apply Result check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"PPPoE").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    driver.find_element(By.LINK_TEXT,"Click here").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"Port").click()

    if_temp_error = False
    if(Select(driver.find_element(By.NAME,f"rpPPPoEIAConfI_Sel_TrustState?{int(OLT_Port)}")).first_selected_option.get_attribute("text") == "Trusted"):
        print(f"             [EMS1-6576][Advanced - PPPoE - Port Apply] {Pon_Name} Port Apply Server_Trusted_State (Trusted) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6576][Advanced - PPPoE - Port Apply] {Pon_Name} Port Apply Server_Trusted_State ({Select(driver.find_element(By.NAME,f"rpPPPoEIAConfI_Sel_TrustState?{int(OLT_Port)}")).first_selected_option.get_attribute("text")} != Trusted) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(Select(driver.find_element(By.NAME,f"rpPPPoEIAConfI_Sel_TrustState?{int(OLT_Eth_Port)}")).first_selected_option.get_attribute("text") == "Trusted"):
        print(f"             [EMS1-6576][Advanced - PPPoE - Port Apply] {Eth_Name} Port Apply Server_Trusted_State (Trusted) Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6576][Advanced - PPPoE - Port Apply] {Eth_Name} Port Apply Server_Trusted_State ({Select(driver.find_element(By.NAME,f"rpPPPoEIAConfI_Sel_TrustState?{int(OLT_Eth_Port)}")).first_selected_option.get_attribute("text")} != Trusted) Fail',file = open(file_name, '+a'))
        if_temp_error = True

    if(if_temp_error==False):
        print(f"             [EMS1-6576][Advanced - PPPoE - Port Apply] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6576][Advanced - PPPoE - Port Apply] Result Fail",file = open(file_name, '+a'))

    #[EMS1-6577][Advanced - PPPoE VLAN - New] Result

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "PPPoE").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)
    driver.find_element(By.ID,"advance_pppoe_vlan_profile_new_btn").click()
    time.sleep(3)
    e_swi.Advanced_PPPoE_VLAN(driver,"4094","4094","Yes",True,True,file_name)
    msg = e_swi.alert_accept_text(driver)
    try:
        e_pro.Close(driver)
    except:
        pass

    #[EMS1-6577][Advanced - PPPoE VLAN - New] Result check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"PPPoE").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    driver.find_element(By.LINK_TEXT,"Click here").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"VLAN").click()
    driver.find_element(By.NAME,"rpPPPoEIAConfV_Ipt_StartVlan").send_keys(e_swi.Keys.CONTROL + 'a')
    driver.find_element(By.NAME,"rpPPPoEIAConfV_Ipt_StartVlan").send_keys("4094")
    driver.find_element(By.NAME,"rpPPPoEIAConfV_Ipt_EndVlan").send_keys(e_swi.Keys.CONTROL + 'a')
    driver.find_element(By.NAME,"rpPPPoEIAConfV_Ipt_EndVlan").send_keys("4094")
    driver.find_element(By.NAME,"rpPPPoEIAConfV_Btn_Apply1").click()
    time.sleep(5)
    if_temp_error = False
    if_find = False
    for i in range(1,driver.find_elements(By.NAME,"rpPPPoEIAConfV_Chk_RemoteID").__len__()+2):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td/table[1]/tbody/tr[{i*2}]/td[2]/div").text
        if(ele == '4094'):
            if(Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td/table[1]/tbody/tr[{i*2}]/td[3]/div/select")).first_selected_option.get_attribute("text") == "Yes"):
                print(f"             [EMS1-6577][Advanced - PPPoE VLAN - New] Enable (Yes) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6577][Advanced - PPPoE VLAN - New] Enable ({Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td/table[1]/tbody/tr[{i*2}]/td[3]/div/select")).first_selected_option.get_attribute("text")} != Yes) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td/table[1]/tbody/tr[{i*2}]/td[4]/div/input").is_selected() == True):
                print(f"             [EMS1-6577][Advanced - PPPoE VLAN - New] Circuit_id (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6577][Advanced - PPPoE VLAN - New] Circuit_id ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td/table[1]/tbody/tr[{i*2}]/td[4]/div/input").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td/table[1]/tbody/tr[{i*2}]/td[5]/div/input").is_selected() == True):
                print(f"             [EMS1-6577][Advanced - PPPoE VLAN - New] Remote_id (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6577][Advanced - PPPoE VLAN - New] Remote_id ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td/table[1]/tbody/tr[{i*2}]/td[5]/div/input").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            if_find = True
    if if_find == False:
        print(f"             [EMS1-6577][Advanced - PPPoE VLAN - New] 4094 Not Found Test Fail",file = open(file_name, '+a'))
        if_temp_error = True

    if(if_temp_error==False):
        print(f"             [EMS1-6577][Advanced - PPPoE VLAN - New] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6577][Advanced - PPPoE VLAN - New] Result Fail",file = open(file_name, '+a'))
           
    
    #[EMS1-6578][Advanced - PPPoE VLAN - Modify] Result

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "PPPoE").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)

    if_find = False
    for i in range(1,int(driver.find_element(By.ID,"pageTotal2").text)+1):
        for j in range(1,driver.find_elements(By.NAME,"advance_pppoe_vlan_profile_checkbox").__len__()+1):
            ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[14]/div[2]/div[1]/div[{j}]/div[2]").text
            if(ele == '4094'):
                driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[14]/div[2]/div[1]/div[{j}]/div[6]/label").click()
                if_find =True
                time.sleep(1)
            if(if_find==True):
                break 
        if(if_find==True):
            break
        else:
            driver.find_element(By.ID,"btnNextPage2").click()
    
    driver.find_element(By.ID,"advance_pppoe_vlan_profile_mod_btn").click()
    e_swi.Advanced_PPPoE_VLAN_Modify(driver,"Yes",False,False,file_name)

    #[EMS1-6578][Advanced - PPPoE VLAN - Modify] Result check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"PPPoE").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    driver.find_element(By.LINK_TEXT,"Click here").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"VLAN").click()
    driver.find_element(By.NAME,"rpPPPoEIAConfV_Ipt_StartVlan").send_keys(e_swi.Keys.CONTROL + 'a')
    driver.find_element(By.NAME,"rpPPPoEIAConfV_Ipt_StartVlan").send_keys("4094")
    driver.find_element(By.NAME,"rpPPPoEIAConfV_Ipt_EndVlan").send_keys(e_swi.Keys.CONTROL + 'a')
    driver.find_element(By.NAME,"rpPPPoEIAConfV_Ipt_EndVlan").send_keys("4094")
    driver.find_element(By.NAME,"rpPPPoEIAConfV_Btn_Apply1").click()
    time.sleep(3)
    if_temp_error = False
    if_find = False
    for i in range(1,driver.find_elements(By.NAME,"rpPPPoEIAConfV_Chk_RemoteID").__len__()+2):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td/table[1]/tbody/tr[{i*2}]/td[2]/div").text
        if(ele == '4094'):
            if(Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td/table[1]/tbody/tr[{i*2}]/td[3]/div/select")).first_selected_option.get_attribute("text") == "Yes"):
                print(f"             [EMS1-6578][Advanced - PPPoE VLAN - Modify] Enable (Yes) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6578][Advanced - PPPoE VLAN - Modify] Enable ({Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td/table[1]/tbody/tr[{i*2}]/td[3]/div/select")).first_selected_option.get_attribute("text")} != Yes) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td/table[1]/tbody/tr[{i*2}]/td[4]/div/input").is_selected() == False):
                print(f"             [EMS1-6578][Advanced - PPPoE VLAN - Modify] Circuit_id (False) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6578][Advanced - PPPoE VLAN - Modify] Circuit_id ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td/table[1]/tbody/tr[{i*2}]/td[4]/div/input").is_selected()} != False) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td/table[1]/tbody/tr[{i*2}]/td[5]/div/input").is_selected() == False):
                print(f"             [EMS1-6578][Advanced - PPPoE VLAN - Modify] Remote_id (False) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6578][Advanced - PPPoE VLAN - Modify] Remote_id ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td/table[1]/tbody/tr[{i*2}]/td[5]/div/input").is_selected()} != False) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            if_find = True
    if if_find == False:
        print(f"             [EMS1-6578][Advanced - PPPoE VLAN - Modify] 4094 Not Found Test Fail",file = open(file_name, '+a')) 
        if_temp_error = True
    if(if_temp_error==False):
        print(f"             [EMS1-6578][Advanced - PPPoE VLAN - Modify] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"             [EMS1-6578][Advanced - PPPoE VLAN - Modify] Result Fail",file = open(file_name, '+a')) 

    #[EMS1-6579][Advanced - PPPoE VLAN - Delete] Result

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "PPPoE").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)

    if_find = False
    for i in range(1,int(driver.find_element(By.ID,"pageTotal2").text)+1):
        for j in range(1,driver.find_elements(By.NAME,"advance_pppoe_vlan_profile_checkbox").__len__()+1):
            ele = driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[14]/div[2]/div[1]/div[{j}]/div[2]").text
            if(ele == '4094'):
                driver.find_element(By.XPATH,f"/html/body/div[3]/div[2]/div/div/div/div[14]/div[2]/div[1]/div[{j}]/div[6]/label").click()
                if_find =True
                time.sleep(1)
            if(if_find==True):
                break
        if(if_find==True):
            break 
        else:
            driver.find_element(By.ID,"btnNextPage2").click()
    
    driver.find_element(By.ID,"advance_pppoe_vlan_profile_del_btn").click()

    #[EMS1-6579][Advanced - PPPoE VLAN - Delete] Result check

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"PPPoE").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    driver.find_element(By.LINK_TEXT,"Click here").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"VLAN").click()
    driver.find_element(By.NAME,"rpPPPoEIAConfV_Ipt_StartVlan").send_keys(e_swi.Keys.CONTROL + 'a')
    driver.find_element(By.NAME,"rpPPPoEIAConfV_Ipt_StartVlan").send_keys("4094")
    driver.find_element(By.NAME,"rpPPPoEIAConfV_Ipt_EndVlan").send_keys(e_swi.Keys.CONTROL + 'a')
    driver.find_element(By.NAME,"rpPPPoEIAConfV_Ipt_EndVlan").send_keys("4094")
    driver.find_element(By.NAME,"rpPPPoEIAConfV_Btn_Apply1").click()
    time.sleep(1)
    for i in range(1,driver.find_elements(By.NAME,"rpPPPoEIAConfV_Chk_RemoteID").__len__()+2):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td/table[1]/tbody/tr[{i*2}]/td[2]/div").text
        if(ele == '4094'):
            if_temp_error = False
            if(Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td/table[1]/tbody/tr[{i*2}]/td[3]/div/select")).first_selected_option.get_attribute("text") == "No"):
                print(f"             [EMS1-6579][Advanced - PPPoE VLAN - Delete] Enable (No) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6579][Advanced - PPPoE VLAN - Delete] Enable ({Select(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td/table[1]/tbody/tr[{i*2}]/td[3]/div/select")).first_selected_option.get_attribute("text")} != No) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td/table[1]/tbody/tr[{i*2}]/td[4]/div/input").is_selected() == False):
                print(f"             [EMS1-6579][Advanced - PPPoE VLAN - Delete] Circuit_id (False) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6579][Advanced - PPPoE VLAN - Delete] Circuit_id ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td/table[1]/tbody/tr[{i*2}]/td[4]/div/input").is_selected()} != False) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td/table[1]/tbody/tr[{i*2}]/td[5]/div/input").is_selected() == False):
                print(f"             [EMS1-6579][Advanced - PPPoE VLAN - Delete] Remote_id (False) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6579][Advanced - PPPoE VLAN - Delete] Remote_id ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td/table[1]/tbody/tr[{i*2}]/td[5]/div/input").is_selected()} != False) Fail',file = open(file_name, '+a'))
                if_temp_error = True
            
            if(if_temp_error==False):
                print(f"             [EMS1-6579][Advanced - PPPoE VLAN - Delete] Result Pass",file = open(file_name, '+a'))
            else:
                print(f"             [EMS1-6579][Advanced - PPPoE VLAN - Delete] Result Fail",file = open(file_name, '+a'))

    #[EMS1-6580][Advanced - PPPoE VLAN - Page Switch] Result

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "PPPoE").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    time.sleep(1)
    if_temp_error=False
    if_find=False
    for i in range(1,12):
        driver.find_element(By.ID,"advance_pppoe_vlan_profile_new_btn").click()
        e_swi.Advanced_PPPoE_VLAN(driver,f"{i}",f"{i}","Yes",True,True,file_name)
        msg = e_swi.alert_accept_text(driver)
        try:
            e_pro.Close(driver)
            if(msg == 'PPPoE IA VLAN exceed maximum number 4 '):
                print(f"             [EMS1-6580][Advanced - PPPoE VLAN - Page Switch] {msg}",file = open(file_name, '+a'))
                print(f"             [EMS1-6580][Advanced - PPPoE VLAN - Page Switch] Result Pass",file = open(file_name, '+a'))
                if_find=True
                if_temp_error=True
                break
        except:
            pass
    if(if_find == False):
        driver.find_element(By.ID,'btnNextPage2').click()
        time.sleep(2)
        if(driver.find_element(By.XPATH,'//*[@id="advance_pppoe_vlan_profile_table"]/div[2]/div[1]').text == '11'):
            print(f"             [EMS1-6580][Advanced - PPPoE VLAN - Page Switch] Result Pass",file = open(file_name, '+a'))
        else:
            print(f"             [EMS1-6580][Advanced - PPPoE VLAN - Page Switch] Result Fail",file = open(file_name, '+a'))
            if_temp_error=True
    if(if_temp_error==False):
        for i in range(1,3):
            e_mod.Checkbox_EMS(driver,"advance_pppoe_vlan_profile_checkbox",True)
            driver.find_element(By.ID,"advance_pppoe_vlan_profile_del_btn").click()
            time.sleep(2)
            msg = e_swi.alert_accept_text(driver)
            try:
                e_pro.Close(driver)
            except:
                pass
    else:
        e_mod.Checkbox_EMS(driver,"advance_pppoe_vlan_profile_checkbox",True)
        driver.find_element(By.ID,"advance_pppoe_vlan_profile_del_btn").click()
        time.sleep(2)
        msg = e_swi.alert_accept_text(driver)
        try:
            e_pro.Close(driver)
        except:
            pass
    print(f"======================================================================================",file = open(file_name, '+a'))

@retry()
def GPON_OLT(driver,url,ems_url,file_name,Pon_Name,Eth_Name,Pon_Name_L,Eth_Name_L):
    set_fail = False
    #[EMS1-6449][GPON Setting - OLT Registration - Apply] Result
    print(f"======================================================================================",file = open(file_name, '+a')) 
    print(f"GPON Setting - OLT Registration Test Start",file = open(file_name, '+a'))

    OLT_Port = Pon_Name.replace("PON ", "")

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "GPON Setting").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "OLT Registration").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "GPON Setting").click()
    e_swi.GPON_OLT_Apply(driver,Pon_Name,True,"E",True,"128",True,"20",file_name)

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"GPON Setting").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"OLT Registration").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    time.sleep(1)
    for i in range(1,driver.find_elements(By.NAME,"rpoltregistration_ChkDelete").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[{(i*2)+2}]/td[2]/div/a").text
        if(ele == OLT_Port):
            driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[{(i*2)+2}]/td[2]/div/a").click()
            time.sleep(1)
            if_temp_error = False
            if(driver.find_element(By.NAME,f"rpoltregistration_ChkActive").is_selected() == True):
                print(f"             [EMS1-6449][GPON Setting - OLT Registration - Apply] Active (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6449][GPON Setting - OLT Registration - Apply] Active ({driver.find_element(By.NAME,f"rpoltregistration_ChkActive").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(Select(driver.find_element(By.NAME,f"rpoltregistration_SltAid")).first_selected_option.get_attribute("text") == OLT_Port):
                print(f"             [EMS1-6449][GPON Setting - OLT Registration - Apply] AID (4) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6449][GPON Setting - OLT Registration - Apply] AID ({Select(driver.find_element(By.NAME,f"rpoltregistration_SltAid")).first_selected_option.get_attribute("text")} != {OLT_Port}) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(Select(driver.find_element(By.NAME,f"rpoltregistration_RegisterMethod")).first_selected_option.get_attribute("text") == "E"):
                print(f"             [EMS1-6449][GPON Setting - OLT Registration - Apply] Register_Method (E) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6449][GPON Setting - OLT Registration - Apply] Register_Method ({Select(driver.find_element(By.NAME,f"rpoltregistration_RegisterMethod")).first_selected_option.get_attribute("text")} != E) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,f"rpoltregistration_OntTemplateChkActive").is_selected() == True):
                print(f"             [EMS1-6449][GPON Setting - OLT Registration - Apply] ONT_Template Active (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6449][GPON Setting - OLT Registration - Apply] ONT_Template Active ({driver.find_element(By.NAME,f"rpoltregistration_OntTemplateChkActive").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(Select(driver.find_element(By.NAME,f"rpoltregistration_Template")).first_selected_option.get_attribute("text") == "Temp128"):
                print(f"             [EMS1-6449][GPON Setting - OLT Registration - Apply] Template (Temp128) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6449][GPON Setting - OLT Registration - Apply] Template ({Select(driver.find_element(By.NAME,f"rpoltregistration_Template")).first_selected_option.get_attribute("text")} != Temp128) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,f"rpoltregistration_ChkFecActive").is_selected() == True):
                print(f"             [EMS1-6449][GPON Setting - OLT Registration - Apply] Fec_Active (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6449][GPON Setting - OLT Registration - Apply] Fec_Active ({driver.find_element(By.NAME,f"rpoltregistration_ChkFecActive").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,f"rpoltregistration_IptTextRangingDistance").get_attribute("value") == "20"):
                print(f"             [EMS1-6449][GPON Setting - OLT Registration - Apply] Ranging_Distance (20) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6449][GPON Setting - OLT Registration - Apply] Ranging_Distance ({driver.find_element(By.NAME,f"rpoltregistration_IptTextRangingDistance").get_attribute("value")} != 20) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(if_temp_error==False):
                print(f"             [EMS1-6449][GPON Setting - OLT Registration - Apply] Result Pass",file = open(file_name, '+a'))
            else:
                set_fail = True
                print(f'             [EMS1-6449][GPON Setting - OLT Registration - Apply] Result Fail',file = open(file_name, '+a'))

    #[EMS1-6581][Advanced - PPPoE - ONT Option - New] Result

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "PPPoE").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    if(set_fail == False):
        e_swi.Advanced_PPPoE_ONTOption(driver,Pon_Name,"128",True,True,file_name)

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"PPPoE").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    driver.find_element(By.LINK_TEXT,"Click here").click()
    time.sleep(2)
    driver.find_element(By.LINK_TEXT,"Ont Option").click()
    time.sleep(1)
    Select(driver.find_element(By.NAME,"rpPPPoEontOption_SltDestinationPort")).select_by_visible_text(Pon_Name_L)
    time.sleep(1)
    if_temp_error =False
    for i in range(1,driver.find_elements(By.NAME,"rpPPPoEontOption_ChkPassThrough").__len__()+2):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[4]/td[2]/table/tbody/tr[{(2*i)+1}]/td[3]/div").text
        if(ele == '128'):
            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[4]/td[2]/table/tbody/tr[{(2*i)+1}]/td[4]/div/input").is_selected() == True):
                print(f"             [EMS1-6581][Advanced - PPPoE - ONT Option - New] pass_through (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6581][Advanced - PPPoE - ONT Option - New] pass_through ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[4]/td[2]/table/tbody/tr[{(2*i)+1}]/td[4]/div/input").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[4]/td[2]/table/tbody/tr[{(2*i)+1}]/td[5]/div/input").is_selected() == True):
                print(f"             [EMS1-6581][Advanced - PPPoE - ONT Option - New] disable (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6581][Advanced - PPPoE - ONT Option - New] disable ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[4]/td[2]/table/tbody/tr[{(2*i)+1}]/td[5]/div/input").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True

    #[EMS1-6581][Advanced - PPPoE - ONT Option - Modify] Result

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "PPPoE").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    if(set_fail == False):
        e_swi.Advanced_PPPoE_ONTOption(driver,Pon_Name,"128",True,False,file_name)

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"PPPoE").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    driver.find_element(By.LINK_TEXT,"Click here").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"Ont Option").click()
    time.sleep(1)
    Select(driver.find_element(By.NAME,"rpPPPoEontOption_SltDestinationPort")).select_by_visible_text(Pon_Name_L)
    time.sleep(1)
    for i in range(1,driver.find_elements(By.NAME,"rpPPPoEontOption_ChkPassThrough").__len__()+2):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[4]/td[2]/table/tbody/tr[{(2*i)+1}]/td[3]/div").text
        if(ele == '128'):
            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[4]/td[2]/table/tbody/tr[{(2*i)+1}]/td[4]/div/input").is_selected() == True):
                print(f"             [EMS1-6581][Advanced - PPPoE - ONT Option - Modify] pass_through (True) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6581][Advanced - PPPoE - ONT Option - Modify] pass_through ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[4]/td[2]/table/tbody/tr[{(2*i)+1}]/td[4]/div/input").is_selected()} != True) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[4]/td[2]/table/tbody/tr[{(2*i)+1}]/td[5]/div/input").is_selected() == False):
                print(f"             [EMS1-6581][Advanced - PPPoE - ONT Option - Modify] disable (False) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6581][Advanced - PPPoE - ONT Option - Modify] disable ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[4]/td[2]/table/tbody/tr[{(2*i)+1}]/td[5]/div/input").is_selected()} != False) Fail',file = open(file_name, '+a'))
                if_temp_error = True

    #[EMS1-6581][Advanced - PPPoE - ONT Option - Delete] Result

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "PPPoE").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Advanced Application").click()
    if(set_fail == False):
        e_swi.Advanced_PPPoE_ONTOption(driver,Pon_Name,"128",False,False,file_name)

    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"Advanced Application").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"PPPoE").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    driver.find_element(By.LINK_TEXT,"Click here").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT,"Ont Option").click()
    time.sleep(1)
    Select(driver.find_element(By.NAME,"rpPPPoEontOption_SltDestinationPort")).select_by_visible_text(Pon_Name_L)
    time.sleep(1)
    for i in range(1,driver.find_elements(By.NAME,"rpPPPoEontOption_ChkPassThrough").__len__()+2):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[4]/td[2]/table/tbody/tr[{(2*i)+1}]/td[3]/div").text
        if(ele == '128'):
            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[4]/td[2]/table/tbody/tr[{(2*i)+1}]/td[4]/div/input").is_selected() == False):
                print(f"             [EMS1-6581][Advanced - PPPoE - ONT Option - Delete] pass_through (False) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6581][Advanced - PPPoE - ONT Option - Delete] pass_through ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[4]/td[2]/table/tbody/tr[{(2*i)+1}]/td[4]/div/input").is_selected()} != False) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[4]/td[2]/table/tbody/tr[{(2*i)+1}]/td[5]/div/input").is_selected() == False):
                print(f"             [EMS1-6581][Advanced - PPPoE - ONT Option - Delete] disable (False) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6581][Advanced - PPPoE - ONT Option - Delete] disable ({driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[4]/td[2]/table/tbody/tr[{(2*i)+1}]/td[5]/div/input").is_selected()} != False) Fail',file = open(file_name, '+a'))
                if_temp_error = True

    if(if_temp_error==False and set_fail== False):
        print(f"             [EMS1-6581][Advanced - PPPoE - ONT Option] Result Pass",file = open(file_name, '+a'))
    else:
        print(f'             [EMS1-6581][Advanced - PPPoE - ONT Option] Result Fail',file = open(file_name, '+a'))

    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    driver.find_element(By.LINK_TEXT, "GPON Setting").click() 
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "OLT Registration").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "GPON Setting").click()

    Select(driver.find_element(By.ID,"gpon_oltregistration_port_combobox")).select_by_visible_text(Pon_Name)
    time.sleep(1)
    driver.find_element(By.ID,'gpon_oltregistration_apply_btn').click()
    
    driver.get(url)
    time.sleep(2)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,3)
    driver.find_element(By.LINK_TEXT,"GPON Setting").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,4)
    driver.find_element(By.LINK_TEXT,"OLT Registration").click()
    time.sleep(1)
    mod.Switch_Default(driver)
    mod.Switch_Specific_Frame(driver,6)
    time.sleep(1)
    if_temp_error = False
    for i in range(1,driver.find_elements(By.NAME,"rpoltregistration_ChkDelete").__len__()+1):
        ele = driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[{(i*2)+2}]/td[2]/div/a").text
        if(ele == OLT_Port):
            driver.find_element(By.XPATH,f"/html/body/form/table/tbody/tr[2]/td/table[2]/tbody/tr[{(i*2)+2}]/td[2]/div/a").click()
            time.sleep(1)
            if(driver.find_element(By.NAME,f"rpoltregistration_ChkActive").is_selected() == False):
                print(f"             [EMS1-6516][GPON Setting - OLT Registration - Delete] Active (False) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6516][GPON Setting - OLT Registration - Delete] Active ({driver.find_element(By.NAME,f"rpoltregistration_ChkActive").is_selected()} != False) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(Select(driver.find_element(By.NAME,f"rpoltregistration_SltAid")).first_selected_option.get_attribute("text") == OLT_Port):
                print(f"             [EMS1-6516][GPON Setting - OLT Registration - Delete] AID (4) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6516][GPON Setting - OLT Registration - Delete] AID ({Select(driver.find_element(By.NAME,f"rpoltregistration_SltAid")).first_selected_option.get_attribute("text")} != {OLT_Port}) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(Select(driver.find_element(By.NAME,f"rpoltregistration_RegisterMethod")).first_selected_option.get_attribute("text") == "A"):
                print(f"             [EMS1-6516][GPON Setting - OLT Registration - Delete] Register_Method (A) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6516][GPON Setting - OLT Registration - Delete] Register_Method ({Select(driver.find_element(By.NAME,f"rpoltregistration_RegisterMethod")).first_selected_option.get_attribute("text")} != A) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,f"rpoltregistration_OntTemplateChkActive").is_selected() == False):
                print(f"             [EMS1-6516][GPON Setting - OLT Registration - Delete] ONT_Template Active (False) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6516][GPON Setting - OLT Registration - Delete] ONT_Template Active ({driver.find_element(By.NAME,f"rpoltregistration_OntTemplateChkActive").is_selected()} != False) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,f"rpoltregistration_ChkFecActive").is_selected() == False):
                print(f"             [EMS1-6516][GPON Setting - OLT Registration - Delete] Fec_Active (False) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6516][GPON Setting - OLT Registration - Delete] Fec_Active ({driver.find_element(By.NAME,f"rpoltregistration_ChkFecActive").is_selected()} != False) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(driver.find_element(By.NAME,f"rpoltregistration_IptTextRangingDistance").get_attribute("value") == "20"):
                print(f"             [EMS1-6516][GPON Setting - OLT Registration - Delete] Ranging_Distance (20) Pass",file = open(file_name, '+a'))
            else:
                print(f'             [EMS1-6516][GPON Setting - OLT Registration - Delete] Ranging_Distance ({driver.find_element(By.NAME,f"rpoltregistration_IptTextRangingDistance").get_attribute("value")} != 20) Fail',file = open(file_name, '+a'))
                if_temp_error = True

            if(if_temp_error==False):
                print(f"             [EMS1-6516][GPON Setting - OLT Registration - Delete] Result Pass",file = open(file_name, '+a'))
            else:
                print(f"             [EMS1-6516][GPON Setting - OLT Registration - Delete] Result Fail",file = open(file_name, '+a'))

    print(f"======================================================================================",file = open(file_name, '+a'))


@retry()
def Configure_Save(driver,url,ems_url,file_name):
    print(f"======================================================================================",file = open(file_name, '+a'))
    print(f"Configure Save Test Start",file = open(file_name, '+a'))
    driver.get(ems_url)
    EMS_Provision_Config_path(driver,url,file_name)
    time.sleep(1)
    e_swi.Configure_Save(driver,file_name)
    print(f"======================================================================================",file = open(file_name, '+a'))

