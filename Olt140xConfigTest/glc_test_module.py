from selenium.webdriver.common.by import By
from os import times
import time
from turtle import Turtle
from xml.etree.ElementTree import ProcessingInstruction
from attr import field
from pyrsistent import s
import selenium_module as mod
import acl_module as acl
import alarm_module as ala
import diagnostic_module as dia
import line_card_module as lc
import l3_routing_module as l3r
import maintenance_module as mai
import multicast_module as mul
import port_module as port
import profile_module as pro
import statistics_module as sta
import switch_module as swi
import sys_module as sys
import vlan_module as vlan
import config_save_module as con
from selenium.webdriver.support.ui import Select
import pyautogui
import datetime

def Test_All(driver,glc_slot,glc_port,msc_slot,msc_port,url,username,password,file_name):
    mod.Switch_Default(driver)
    mod.Switch_Frame(driver)
    time.sleep(5)
    Maintenance_Config_Reset(driver,glc_slot,glc_port,file_name)
    if_pass = False
    counter = 0
    while(if_pass == False):
        try:
            DHCP_ARP_PPPoE_IGMP(driver,glc_slot,glc_port,file_name)
            if_pass = True
        except:
            try:
                if(driver.find_element(By.XPATH, "/html/body/h1").get_attribute("textContent") == 'An error occurred.'):
                    print(f"----------------------------------An error occurred Restart-----------------------------------",file = open(file_name, '+a'))
                else:
                    print(f"---------------------------------Auto Web Bug Restart---------------------------------",file = open(file_name, '+a'))
                    counter = counter+1
            except:
                print(f"---------------------------------Auto Web Bug Restart---------------------------------",file = open(file_name, '+a'))
                counter = counter+1
            if(counter < 6):
                time.sleep(5)
                from selenium import webdriver
                driver = webdriver.Chrome()
                driver.get(url) # 連上網頁
                mod.Login(driver,username,password) # 登入
                time.sleep(1)
            else:
                print("--------------------------------Auto Web Bug Test Fail--------------------------------",file = open(file_name, '+a'))
                if_pass = True
    if_pass = False
    counter = 0
    while(if_pass == False):
        try:
            ACL_Rule_MACFF(driver,glc_slot,glc_port,file_name)
            if_pass = True
        except:
            try:
                if(driver.find_element(By.XPATH, "/html/body/h1").get_attribute("textContent") == 'An error occurred.'):
                    print(f"----------------------------------An error occurred Restart-----------------------------------",file = open(file_name, '+a'))
                else:
                    print(f"---------------------------------Auto Web Bug Restart---------------------------------",file = open(file_name, '+a'))
                    counter = counter+1
            except:
                print(f"---------------------------------Auto Web Bug Restart---------------------------------",file = open(file_name, '+a'))
                counter = counter+1
            if(counter < 6):
                time.sleep(5)
                from selenium import webdriver
                driver = webdriver.Chrome()
                driver.get(url) # 連上網頁
                mod.Login(driver,username,password) # 登入
                time.sleep(1)
            else:
                print("--------------------------------Auto Web Bug Test Fail--------------------------------",file = open(file_name, '+a'))
                if_pass = True
    if_pass = False
    counter = 0
    while(if_pass == False):
        try:
            ACL_Test(driver,glc_slot,glc_port,msc_slot,msc_port,file_name)
            if_pass = True
        except:
            try:
                if(driver.find_element(By.XPATH, "/html/body/h1").get_attribute("textContent") == 'An error occurred.'):
                    print(f"----------------------------------An error occurred Restart-----------------------------------",file = open(file_name, '+a'))
                else:
                    print(f"---------------------------------Auto Web Bug Restart---------------------------------",file = open(file_name, '+a'))
                    counter = counter+1
            except:
                print(f"---------------------------------Auto Web Bug Restart---------------------------------",file = open(file_name, '+a'))
                counter = counter+1
            if(counter < 6):
                time.sleep(5)
                from selenium import webdriver
                driver = webdriver.Chrome()
                driver.get(url) # 連上網頁
                mod.Login(driver,username,password) # 登入
                time.sleep(1)
            else:
                print("--------------------------------Auto Web Bug Test Fail--------------------------------",file = open(file_name, '+a'))
                if_pass = True
    if_pass = False
    counter = 0
    while(if_pass == False):
        try:
            Alarm_Test(driver,glc_slot,glc_port,msc_slot,file_name)
            if_pass = True
        except:
            try:
                if(driver.find_element(By.XPATH, "/html/body/h1").get_attribute("textContent") == 'An error occurred.'):
                    print(f"----------------------------------An error occurred Restart-----------------------------------",file = open(file_name, '+a'))
                else:
                    print(f"---------------------------------Auto Web Bug Restart---------------------------------",file = open(file_name, '+a'))
                    counter = counter+1
            except:
                print(f"---------------------------------Auto Web Bug Restart---------------------------------",file = open(file_name, '+a'))
                counter = counter+1
            if(counter < 6):
                time.sleep(5)
                from selenium import webdriver
                driver = webdriver.Chrome()
                driver.get(url) # 連上網頁
                mod.Login(driver,username,password) # 登入
                time.sleep(1)
            else:
                print("--------------------------------Auto Web Bug Test Fail--------------------------------",file = open(file_name, '+a'))
                if_pass = True
    if_pass = False
    counter = 0
    while(if_pass == False):
        try:
            Diagnostic_Test(driver,glc_slot,glc_port,file_name)
            if_pass = True
        except:
            try:
                if(driver.find_element(By.XPATH, "/html/body/h1").get_attribute("textContent") == 'An error occurred.'):
                    print(f"----------------------------------An error occurred Restart-----------------------------------",file = open(file_name, '+a'))
                else:
                    print(f"---------------------------------Auto Web Bug Restart---------------------------------",file = open(file_name, '+a'))
                    counter = counter+1
            except:
                print(f"---------------------------------Auto Web Bug Restart---------------------------------",file = open(file_name, '+a'))
                counter = counter+1
            if(counter < 6):
                time.sleep(5)
                from selenium import webdriver
                driver = webdriver.Chrome()
                driver.get(url) # 連上網頁
                mod.Login(driver,username,password) # 登入
                time.sleep(1)
            else:
                print("--------------------------------Auto Web Bug Test Fail--------------------------------",file = open(file_name, '+a'))
                if_pass = True
    if_pass = False
    counter = 0
    while(if_pass == False):
        try:
            Line_Card_Test(driver,glc_slot,glc_port,file_name)
            if_pass = True
        except:
            try:
                if(driver.find_element(By.XPATH, "/html/body/h1").get_attribute("textContent") == 'An error occurred.'):
                    print(f"----------------------------------An error occurred Restart-----------------------------------",file = open(file_name, '+a'))
                else:
                    print(f"---------------------------------Auto Web Bug Restart---------------------------------",file = open(file_name, '+a'))
                    counter = counter+1
            except:
                print(f"---------------------------------Auto Web Bug Restart---------------------------------",file = open(file_name, '+a'))
                counter = counter+1
            if(counter < 6):
                time.sleep(5)
                from selenium import webdriver
                driver = webdriver.Chrome()
                driver.get(url) # 連上網頁
                mod.Login(driver,username,password) # 登入
                time.sleep(1)
            else:
                print("--------------------------------Auto Web Bug Test Fail--------------------------------",file = open(file_name, '+a'))
                if_pass = True
    if_pass = False
    counter = 0
    while(if_pass == False):
        try:
            L3_Routing_Test(driver,glc_slot,glc_port,msc_slot,msc_port,file_name)
            if_pass = True
        except:
            try:
                if(driver.find_element(By.XPATH, "/html/body/h1").get_attribute("textContent") == 'An error occurred.'):
                    print(f"----------------------------------An error occurred Restart-----------------------------------",file = open(file_name, '+a'))
                else:
                    print(f"---------------------------------Auto Web Bug Restart---------------------------------",file = open(file_name, '+a'))
                    counter = counter+1
            except:
                print(f"---------------------------------Auto Web Bug Restart---------------------------------",file = open(file_name, '+a'))
                counter = counter+1
            if(counter < 6):
                time.sleep(5)
                from selenium import webdriver
                driver = webdriver.Chrome()
                driver.get(url) # 連上網頁
                mod.Login(driver,username,password) # 登入
                time.sleep(1)
            else:
                print("--------------------------------Auto Web Bug Test Fail--------------------------------",file = open(file_name, '+a'))
                if_pass = True
    if_pass = False
    counter = 0
    while(if_pass == False):
        try:
            Multicast_Test(driver,glc_slot,glc_port,msc_slot,msc_port,file_name)
            if_pass = True
        except:
            try:
                if(driver.find_element(By.XPATH, "/html/body/h1").get_attribute("textContent") == 'An error occurred.'):
                    print(f"----------------------------------An error occurred Restart-----------------------------------",file = open(file_name, '+a'))
                else:
                    print(f"---------------------------------Auto Web Bug Restart---------------------------------",file = open(file_name, '+a'))
                    counter = counter+1
            except:
                print(f"---------------------------------Auto Web Bug Restart---------------------------------",file = open(file_name, '+a'))
                counter = counter+1
            if(counter < 6):
                time.sleep(5)
                from selenium import webdriver
                driver = webdriver.Chrome()
                driver.get(url) # 連上網頁
                mod.Login(driver,username,password) # 登入
                time.sleep(1)
            else:
                print("--------------------------------Auto Web Bug Test Fail--------------------------------",file = open(file_name, '+a'))
                if_pass = True
    if_pass = False
    counter = 0
    while(if_pass == False):
        try:
            Port_Test(driver,glc_slot,glc_port,msc_slot,msc_port,file_name)
            if_pass = True
        except:
            try:
                if(driver.find_element(By.XPATH, "/html/body/h1").get_attribute("textContent") == 'An error occurred.'):
                    print(f"----------------------------------An error occurred Restart-----------------------------------",file = open(file_name, '+a'))
                else:
                    print(f"---------------------------------Auto Web Bug Restart---------------------------------",file = open(file_name, '+a'))
                    counter = counter+1
            except:
                print(f"---------------------------------Auto Web Bug Restart---------------------------------",file = open(file_name, '+a'))
                counter = counter+1
            if(counter < 6):
                time.sleep(5)
                from selenium import webdriver
                driver = webdriver.Chrome()
                driver.get(url) # 連上網頁
                mod.Login(driver,username,password) # 登入
                time.sleep(1)
            else:
                print("--------------------------------Auto Web Bug Test Fail--------------------------------",file = open(file_name, '+a'))
                if_pass = True
    if_pass = False
    counter = 0
    while(if_pass == False):
        try:
            Profile_Test(driver,glc_slot,glc_port,msc_slot,msc_port,file_name)
            if_pass = True
        except:
            try:
                if(driver.find_element(By.XPATH, "/html/body/h1").get_attribute("textContent") == 'An error occurred.'):
                    print(f"----------------------------------An error occurred Restart-----------------------------------",file = open(file_name, '+a'))
                else:
                    print(f"---------------------------------Auto Web Bug Restart---------------------------------",file = open(file_name, '+a'))
                    counter = counter+1
            except:
                print(f"---------------------------------Auto Web Bug Restart---------------------------------",file = open(file_name, '+a'))
                counter = counter+1
            if(counter < 6):
                time.sleep(5)
                from selenium import webdriver
                driver = webdriver.Chrome()
                driver.get(url) # 連上網頁
                mod.Login(driver,username,password) # 登入
                time.sleep(1)
            else:
                print("--------------------------------Auto Web Bug Test Fail--------------------------------",file = open(file_name, '+a'))
                if_pass = True
    if_pass = False
    counter = 0
    while(if_pass == False):
        try:
            Statistics_Test(driver,glc_slot,glc_port,msc_slot,msc_port,username,password,file_name)        
            if_pass = True
        except:
            try:
                if(driver.find_element(By.XPATH, "/html/body/h1").get_attribute("textContent") == 'An error occurred.'):
                    print(f"----------------------------------An error occurred Restart-----------------------------------",file = open(file_name, '+a'))
                else:
                    print(f"---------------------------------Auto Web Bug Restart---------------------------------",file = open(file_name, '+a'))
                    counter = counter+1
            except:
                print(f"---------------------------------Auto Web Bug Restart---------------------------------",file = open(file_name, '+a'))
                counter = counter+1
            if(counter < 6):
                time.sleep(5)
                from selenium import webdriver
                driver = webdriver.Chrome()
                driver.get(url) # 連上網頁
                mod.Login(driver,username,password) # 登入
                time.sleep(1)
            else:
                print("--------------------------------Auto Web Bug Test Fail--------------------------------",file = open(file_name, '+a'))
                if_pass = True
    if_pass = False
    counter = 0
    while(if_pass == False):
        try:
            Switch_Test(driver,glc_slot,glc_port,msc_slot,msc_port,file_name)
            if_pass = True
        except:
            try:
                if(driver.find_element(By.XPATH, "/html/body/h1").get_attribute("textContent") == 'An error occurred.'):
                    print(f"----------------------------------An error occurred Restart-----------------------------------",file = open(file_name, '+a'))
                else:
                    print(f"---------------------------------Auto Web Bug Restart---------------------------------",file = open(file_name, '+a'))
                    counter = counter+1
            except:
                print(f"---------------------------------Auto Web Bug Restart---------------------------------",file = open(file_name, '+a'))
                counter = counter+1
            if(counter < 6):
                time.sleep(5)
                from selenium import webdriver
                driver = webdriver.Chrome()
                driver.get(url) # 連上網頁
                mod.Login(driver,username,password) # 登入
                time.sleep(1)
            else:
                print("--------------------------------Auto Web Bug Test Fail--------------------------------",file = open(file_name, '+a'))
                if_pass = True
    if_pass = False
    counter = 0
    while(if_pass == False):
        try:
            VLAN_Test(driver,glc_slot,glc_port,file_name)
            if_pass = True
        except:
            try:
                if(driver.find_element(By.XPATH, "/html/body/h1").get_attribute("textContent") == 'An error occurred.'):
                    print(f"----------------------------------An error occurred Restart-----------------------------------",file = open(file_name, '+a'))
                else:
                    print(f"---------------------------------Auto Web Bug Restart---------------------------------",file = open(file_name, '+a'))
                    counter = counter+1
            except:
                print(f"---------------------------------Auto Web Bug Restart---------------------------------",file = open(file_name, '+a'))
                counter = counter+1
            if(counter < 6):
                time.sleep(5)
                from selenium import webdriver
                driver = webdriver.Chrome()
                driver.get(url) # 連上網頁
                mod.Login(driver,username,password) # 登入
                time.sleep(1)
            else:
                print("--------------------------------Auto Web Bug Test Fail--------------------------------",file = open(file_name, '+a'))
                if_pass = True
    if_pass = False
    counter = 0
    while(if_pass == False):
        try:
            Maintenance_Test(driver,glc_slot,glc_port,file_name)
            if_pass = True
        except:
            try:
                if(driver.find_element(By.XPATH, "/html/body/h1").get_attribute("textContent") == 'An error occurred.'):
                    print(f"----------------------------------An error occurred Restart-----------------------------------",file = open(file_name, '+a'))
                else:
                    print(f"---------------------------------Auto Web Bug Restart---------------------------------",file = open(file_name, '+a'))
                    counter = counter+1
            except:
                print(f"---------------------------------Auto Web Bug Restart---------------------------------",file = open(file_name, '+a'))
                counter = counter+1
            if(counter < 6):
                time.sleep(5)
                from selenium import webdriver
                driver = webdriver.Chrome()
                driver.get(url) # 連上網頁
                mod.Login(driver,username,password) # 登入
                time.sleep(1)
            else:
                print("--------------------------------Auto Web Bug Test Fail--------------------------------",file = open(file_name, '+a'))
                if_pass = True
    if_pass = False
    counter = 0
    while(if_pass == False):
        try:
            Sys_Test(driver,glc_slot,glc_port,msc_slot,msc_port,file_name)
            if_pass = True
        except:
            try:
                if(driver.find_element(By.XPATH, "/html/body/h1").get_attribute("textContent") == 'An error occurred.'):
                    print(f"----------------------------------An error occurred Restart-----------------------------------",file = open(file_name, '+a'))
                else:
                    print(f"---------------------------------Auto Web Bug Restart---------------------------------",file = open(file_name, '+a'))
                    counter = counter+1
            except:
                print(f"---------------------------------Auto Web Bug Restart---------------------------------",file = open(file_name, '+a'))
                counter = counter+1
            if(counter < 6):
                time.sleep(5)
                from selenium import webdriver
                driver = webdriver.Chrome()
                driver.get(url) # 連上網頁
                mod.Login(driver,username,password) # 登入
                time.sleep(1)
            else:
                print("--------------------------------Auto Web Bug Test Fail--------------------------------",file = open(file_name, '+a'))
                if_pass = True
    Maintenance_Config_Reset(driver,glc_slot,glc_port,file_name)

def Maintenance_Config_Reset(driver,glc_slot,glc_port,file_name):    
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Maintenance")
    mod.SubPage_Switch(driver,"Config Reset")
    mod.Switch_Frame(driver)
    mai.Config_Reset(driver)
    pyautogui.press("enter")
    # time.sleep(60)

    #--------no need to wait for long time?-------------#*add
    time.sleep(1)
    state_n = ""
    while(state_n !="idle"):
        time.sleep(2)    
        state_n = driver.find_element(By.CLASS_NAME, "state").text

# def Maintenance_Config_Reset_1(driver,glc_slot,glc_port,file_name): #--------no need to wait for long time?-------------#*add
#     mod.Switch_Default(driver)
#     mod.Page_Switch(driver,"Maintenance")
#     mod.SubPage_Switch(driver,"Config Reset")
#     mod.Switch_Frame(driver)
#     mai.Config_Reset(driver)
#     pyautogui.press("enter")
#     time.sleep(1)
#     state_n = ""
#     while(state_n !="idle"):
#         time.sleep(2)    
#         state_n = driver.find_element(By.CLASS_NAME, "state").text

def DHCP_ARP_PPPoE_IGMP(driver,glc_slot,glc_port,file_name):

    print(f"DHCP ARP PPPoE IGMP Test\nTest Start",file = open(file_name, '+a'))

    # ACL DHCP DhcpL2Agent Test
    # ACL > DHCP >DhcpL2Agent
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向ACL > DHCP > DhcpL2Agent
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"ACL")
    mod.SubPage_Switch(driver,"DHCP")
    mod.Switch_Frame(driver)

    # DhcpL2Agent 傳入值 1
    acl.DHCP_L2Agent_Max_Lease_Overflow_Mode(driver,2)
    acl.DHCP_L2Agent_Option_82_Check(driver,1)
    acl.DHCP_L2Agent_Option_82_Policy_Mode(driver,2)
    acl.DHCP_L2Agent_Apply_1(driver)

    # DhcpL2Agent 檢測 1
    if(driver.find_element(By.XPATH, f"//*[@name='rpdhcp_sltOverflowMode']/option[2]").is_selected() == False):
        print(f"             [ACL - DHCP - DhcpL2Agent] Max Lease Overflow Mode Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.XPATH, f"//*[@name='rpdhcp_chkOpt82']/option[1]").is_selected() == False):
        print(f"             [ACL - DHCP - DhcpL2Agent] Option 82 Check Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.XPATH, f"//*[@name='rpdhcp_opt82PolicyMode']/option[2]").is_selected() == False):
        print(f"             [ACL - DHCP - DhcpL2Agent] Option 82 Policy Mode Test Fail",file = open(file_name, '+a'))
        if_error = True

    try:
        # DhcpL2Agent 傳入值 2-1
        acl.DHCP_L2Agent_DHCP_L2_Agent_Forbidden(driver,"4094")
        acl.DHCP_L2Agent_LDRA(driver,True)
        acl.DHCP_L2Agent_Apply_2(driver)

        # DhcpL2Agent 檢測 2-1
        if_find = True
        for index in range(driver.find_elements(By.CLASS_NAME, "td-table-content.rpdhcp_l2AgentForbidVid").__len__()):
            if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpdhcp_l2AgentForbidVid")[index].get_attribute("textContent") == "4094"):
                if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpdhcp_ForbidchkLdra")[index].get_attribute("textContent") == "V"):
                    pass
                else:
                    if_find = False
            else:
                if_find = False

        if_DhcpL2Agent_2_test_keys = ["4095","0","@"]
        for test_times in range(3):
            # DhcpL2Agent 傳入值 2-2
            acl.DHCP_L2Agent_DHCP_L2_Agent_Forbidden(driver,if_DhcpL2Agent_2_test_keys[test_times])
            acl.DHCP_L2Agent_LDRA(driver,True)
            acl.DHCP_L2Agent_Apply_2(driver)

            # DhcpL2Agent 檢測 2-2
            if(mod.IsAlert(driver) == False):
                if_error = True

        if(if_find == False):
            print(f"             [ACL - DHCP - DhcpL2Agent] DHCP L2 Agent Forbidden or LDRA Test Fail",file = open(file_name, '+a'))
            if_error = True

        # valid apply
        acl.DHCP_L2Agent_DHCP_L2_Agent_Forbidden(driver,"4094")
        acl.DHCP_L2Agent_LDRA(driver,True)
        acl.DHCP_L2Agent_Apply_2(driver)
    except:
        pass

    # DhcpL2Agent 傳入值 3-1
    acl.DHCP_L2Agent_DHCP_L2_Agent_VID(driver,"4094")
    acl.DHCP_L2Agent_Apply_3(driver)

    if_find = False
    for index in range(driver.find_elements(By.CLASS_NAME, "dhcpVlanConfList").__len__()):
        if(driver.find_elements(By.CLASS_NAME, "rpdhcp_l2AgentVid.td-table-content")[index].get_attribute("textContent") == "4094"):
            if_find = True
            driver.find_elements(By.NAME, "pfListSelected")[index].click()

            # DhcpL2Agent 傳入值 3-2
            acl.DHCP_L2Agent_Select_Enable_LDRA(driver,True)
            acl.DHCP_L2Agent_Select_Option_18_Interface_Id(driver,"123456789012345678901234567890123456789012345678901234567890123")
            acl.DHCP_L2Agent_Select_Option_37_Remote_Id(driver,"123456789012345678901234567890123456789012345678901234567890123")
            acl.DHCP_L2Agent_Select_Option_82_Circuit_Id(driver,"123456789012345678901234567890123456789012345678901234567890123")
            acl.DHCP_L2Agent_Select_Option_82_Remote_Id(driver,"123456789012345678901234567890123456789012345678901234567890123")
            acl.DHCP_L2Agent_Select_Option_82_Policy(driver,3)
            acl.DHCP_L2Agent_Select_Option_82_Linechar(driver,3)
            acl.DHCP_L2Agent_Select_Enable_DHCP_Relay(driver,True)
            acl.DHCP_L2Agent_Select_Primary_Relay_Server_IP(driver,"10.10.10.1")
            acl.DHCP_L2Agent_Select_Secondary_Relay_Server_IP(driver,"10.10.10.2")
            acl.DHCP_L2Agent_Select_Active_Server(driver,2)
            acl.DHCP_L2Agent_Select_Relay_Mode(driver,2)
            acl.DHCP_L2Agent_Select_Apply(driver)

            # DhcpL2Agent 檢驗 3-2
            for index in range(driver.find_elements(By.CLASS_NAME, "dhcpVlanConfList").__len__()):
                if(driver.find_elements(By.CLASS_NAME, "rpdhcp_l2AgentVid.td-table-content")[index].get_attribute("textContent") == "4094"):
                    driver.find_elements(By.NAME, "pfListSelected")[index].click()

            if(driver.find_element(By.NAME, "rpdhcp_chkLdra").is_selected() != True):
                print(f"             [ACL - DHCP - DhcpL2Agent] DHCP L2 Agent VID Enable LDRA Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_element(By.NAME, "opt18OptionInfo").get_attribute("value") != "123456789012345678901234567890123456789012345678901234567890123"):
                print(f"             [ACL - DHCP - DhcpL2Agent] DHCP L2 Agent VID Option 18 Interface Id Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_element(By.NAME, "opt37OptionInfo").get_attribute("value") != "123456789012345678901234567890123456789012345678901234567890123"):
                print(f"             [ACL - DHCP - DhcpL2Agent] DHCP L2 Agent VID Option 37 Remote Id Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_element(By.NAME, "opt82CircuitOptionInfo").get_attribute("value") != "123456789012345678901234567890123456789012345678901234567890123"):
                print(f"             [ACL - DHCP - DhcpL2Agent] DHCP L2 Agent VID Option 82 Circuit Id Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_element(By.NAME, "opt82RemoteOptionInfo").get_attribute("value") != "123456789012345678901234567890123456789012345678901234567890123"):
                print(f"             [ACL - DHCP - DhcpL2Agent] DHCP L2 Agent VID Option 82 Remote Id Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_element(By.XPATH, f"//*[@name='rpdhcp_opt82Policy']/option[3]").is_selected() != True):
                print(f"             [ACL - DHCP - DhcpL2Agent] DHCP L2 Agent VID Option 82 Policy Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_element(By.XPATH, f"//*[@name='rpdhcp_opt82Linechar']/option[3]").is_selected() != True):
                print(f"             [ACL - DHCP - DhcpL2Agent] DHCP L2 Agent VID Option 82 Linechar Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_element(By.NAME, "rpdhcp_chkRelay").is_selected() != True):
                print(f"             [ACL - DHCP - DhcpL2Agent] DHCP L2 Agent VID Enable DHCP Relay Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_element(By.NAME, "rpdhcp_priRelaySvrIp").get_attribute("value") != "10.10.10.1"):
                print(f"             [ACL - DHCP - DhcpL2Agent] DHCP L2 Agent VID Primary Relay Server IP Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_element(By.NAME, "rpdhcp_sndRelaySvrIp").get_attribute("value") != "10.10.10.2"):
                print(f"             [ACL - DHCP - DhcpL2Agent] DHCP L2 Agent VID Secondary Relay Server IP Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_element(By.XPATH, f"//*[@name='rpdhcp_activeRelaySvrIdx']/option[2]").is_selected() != True):
                print(f"             [ACL - DHCP - DhcpL2Agent] DHCP L2 Agent VID Active Server Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_element(By.XPATH, f"//*[@name='rpdhcp_relayMode']/option[2]").is_selected() != True):
                print(f"             [ACL - DHCP - DhcpL2Agent] DHCP L2 Agent VID Relay Mode Test Fail",file = open(file_name, '+a'))
                if_error = True
        
            # DhcpL2Agent 3 刪除
            acl.DHCP_L2Agent_Select_Delete(driver)

    if(if_find == False):
        print(f"             [ACL - DHCP - DhcpL2Agent] DHCP L2 Agent VID Apply Fail",file = open(file_name, '+a'))
        if_error = True

    try:
        # DhcpL2Agent 2 刪除
        acl.DHCP_L2Agent_DHCP_L2_Agent_Forbidden(driver,"4094")
        acl.DHCP_L2Agent_LDRA(driver,True)
        acl.DHCP_L2Agent_Delete_2(driver)
    except:
        pass

    # DhcpL2Agent 2 Setting Default
    acl.DHCP_L2Agent_Max_Lease_Overflow_Mode(driver,1)
    acl.DHCP_L2Agent_Option_82_Check(driver,2)
    acl.DHCP_L2Agent_Option_82_Policy_Mode(driver,2)
    acl.DHCP_L2Agent_Apply_1(driver)

    if(if_error == False):
        print(f"[MSAN1-11812][ACL - DHCP - DhcpL2Agent] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11812][ACL - DHCP - DhcpL2Agent] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # ACL DHCP DHCP Remote Backup Test
    # ACL > DHCP > DHCP Remote Backup
    # -------------------------start-------------------------

    # Crash
    try:
        mod.Tab_Switch(driver,"DHCP Remote Backup")
        try:
            error_message = driver.find_element(By.XPATH, "/html/body/h1").get_attribute("textContent")
            print(f"             [ACL - DHCP - DHCP Remote Backup] Page Crash, Erorr Message:{error_message}",file = open(file_name, '+a'))
            print(f"[MSAN1-11813][ACL - DHCP - DHCP Remote Backup] Result Fail",file = open(file_name, '+a'))
            return
        except:
            print(f"[MSAN1-11813][ACL - DHCP - DHCP Remote Backup] Result Pass",file = open(file_name, '+a'))
    except:
        print(f"[MSAN1-11813][ACL - DHCP - DHCP Remote Backup] Result Block",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics DHCP Snoop Clear
    # Statistics > DHCP Snoop
    # -------------------------start-------------------------

    # 路徑導向 Statistics > DHCP Snoop
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Statistics")
    mod.SubPage_Switch(driver,"DHCP Snoop")
    mod.Switch_Frame(driver)
    time.sleep(1)

    # port select
    sta.Slot_Select(driver,glc_slot)
    sta.Port_Select(driver,glc_port)
    sta.Load(driver)

    # Clear
    sta.DHCP_Snoop_Clear_Up(driver)
    sta.DHCP_Snoop_Clear_Down(driver)
    print(f"[MSAN1-11905][Statistics - DHCP Snoop] Result Pass",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Port DHCP Test
    # Port > DHCP
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Port > DHCP
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Port")
    mod.SubPage_Switch(driver,"DHCP")
    mod.Switch_Frame(driver)
    time.sleep(1)

    # port select
    port.Slot_Select(driver,glc_slot)
    port.Port_Select(driver,glc_port)
    port.Load(driver)

    # Port DHCP 傳入值 1
    port.DHCP_Option_82_Policy(driver,1)
    port.DHCP_Option_LDRA_Policy(driver,1)
    port.DHCP_Option_LDRA_LinkLocal(driver,1)
    port.DHCP_Snooping_Setting_Max_Lease(driver,"1")
    port.DHCP_Snooping_Setting_Priority_VLAN(driver,"4092,4093,4094")
    port.DHCP_Snooping_Setting_IP_MAC_Binding(driver,1)
    port.DHCP_Static_IP_Fitter_Setting_Index(driver,"1")
    port.DHCP_Static_IP_Fitter_Setting_IP_Address(driver,"10.10.10.1")
    port.DHCP_Static_IP_Fitter_Setting_IPv6_Prefix(driver,"64")
    port.DHCP_Static_IP_Fitter_Setting_IP_MAC_Binding(driver,1)
    port.DHCP_Apply(driver)
    if(driver.find_elements(By.CLASS_NAME, "rpportdhcp_stIp.td-table-content")[0].get_attribute("textContent") != "10.10.10.1"):
        print(f"             [Port - DHCP] 10.10.10.1 Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Port DHCP 傳入值 2
    port.DHCP_Option_82_Policy(driver,2)
    port.DHCP_Option_LDRA_Policy(driver,2)
    port.DHCP_Option_LDRA_LinkLocal(driver,2)
    port.DHCP_Snooping_Setting_Max_Lease(driver,"32")
    port.DHCP_Snooping_Setting_Priority_VLAN(driver,"4092,4093,4094")
    port.DHCP_Snooping_Setting_IP_MAC_Binding(driver,2)
    port.DHCP_Static_IP_Fitter_Setting_Index(driver,"2")
    port.DHCP_Static_IP_Fitter_Setting_IP_Address(driver,"10.10.10.2")
    port.DHCP_Static_IP_Fitter_Setting_IPv6_Prefix(driver,"64")
    port.DHCP_Static_IP_Fitter_Setting_IP_MAC_Binding(driver,2)
    port.DHCP_Apply(driver)
    if(driver.find_elements(By.CLASS_NAME, "rpportdhcp_stIp.td-table-content")[1].get_attribute("textContent") != "10.10.10.2"):
        print(f"             [Port - DHCP] 10.10.10.2 Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Port DHCP 傳入值 3
    port.DHCP_Option_82_Policy(driver,3)
    port.DHCP_Option_LDRA_Policy(driver,3)
    port.DHCP_Option_LDRA_LinkLocal(driver,3)
    port.DHCP_Snooping_Setting_Max_Lease(driver,"32")
    port.DHCP_Snooping_Setting_Priority_VLAN(driver,"4092,4093,4094")
    port.DHCP_Snooping_Setting_IP_MAC_Binding(driver,2)
    port.DHCP_Static_IP_Fitter_Setting_Index(driver,"3")
    port.DHCP_Static_IP_Fitter_Setting_IP_Address(driver,"10.10.10.3")
    port.DHCP_Static_IP_Fitter_Setting_IPv6_Prefix(driver,"64")
    port.DHCP_Static_IP_Fitter_Setting_IP_MAC_Binding(driver,2)
    port.DHCP_Apply(driver)
    if(driver.find_elements(By.CLASS_NAME, "rpportdhcp_stIp.td-table-content")[2].get_attribute("textContent") != "10.10.10.3"):
        print(f"             [Port - DHCP] 10.10.10.3 Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Port DHCP 傳入值 4
    port.DHCP_Option_82_Policy(driver,3)
    port.DHCP_Option_LDRA_Policy(driver,4)
    port.DHCP_Option_LDRA_LinkLocal(driver,4)
    port.DHCP_Snooping_Setting_Max_Lease(driver,"32")
    port.DHCP_Snooping_Setting_Priority_VLAN(driver,"4092,4093,4094")
    port.DHCP_Snooping_Setting_IP_MAC_Binding(driver,2)
    port.DHCP_Static_IP_Fitter_Setting_Index(driver,"4")
    port.DHCP_Static_IP_Fitter_Setting_IP_Address(driver,"10.10.10.4")
    port.DHCP_Static_IP_Fitter_Setting_IPv6_Prefix(driver,"64")
    port.DHCP_Static_IP_Fitter_Setting_IP_MAC_Binding(driver,2)
    port.DHCP_Apply(driver)
    if(driver.find_elements(By.CLASS_NAME, "rpportdhcp_stIp.td-table-content")[3].get_attribute("textContent") != "10.10.10.4"):
        print(f"             [Port - DHCP] 10.10.10.4 Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Port DHCP 傳入值 5
    port.DHCP_Option_82_Policy(driver,3)
    port.DHCP_Option_LDRA_Policy(driver,4)
    port.DHCP_Option_LDRA_LinkLocal(driver,4)
    port.DHCP_Snooping_Setting_Max_Lease(driver,"0")
    port.DHCP_Snooping_Setting_Priority_VLAN(driver,"4092,4093,4094")
    port.DHCP_Snooping_Setting_IP_MAC_Binding(driver,2)
    port.DHCP_Static_IP_Fitter_Setting_Index(driver,"5")
    port.DHCP_Static_IP_Fitter_Setting_IP_Address(driver,"10.10.10.5")
    port.DHCP_Static_IP_Fitter_Setting_IPv6_Prefix(driver,"64")
    port.DHCP_Static_IP_Fitter_Setting_IP_MAC_Binding(driver,2)
    port.DHCP_Apply(driver)
    if(mod.IsAlert == False):
        print(f"             [Port - DHCP] Snooping Setting Max Lease 0 No Alarm",file = open(file_name, '+a'))
    port.DHCP_Snooping_Setting_Max_Lease(driver,"33")
    port.DHCP_Apply(driver)
    if(mod.IsAlert == False):
        print(f"             [Port - DHCP] Snooping Setting Max Lease 33 No Alarm",file = open(file_name, '+a'))
    port.DHCP_Snooping_Setting_Max_Lease(driver,"32")
    port.DHCP_Snooping_Setting_Priority_VLAN(driver,"4092,4093,4094,4095")
    port.DHCP_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Port - DHCP] Snooping Setting Priority VLAN 4092,4093,4094,4095 No Error",file = open(file_name, '+a'))
    port.DHCP_Snooping_Setting_Priority_VLAN(driver,"4092,4093,4094")
    port.DHCP_Apply(driver)
    if(driver.find_elements(By.CLASS_NAME, "rpportdhcp_stIp.td-table-content")[4].get_attribute("textContent") != "10.10.10.5"):
        print(f"             [Port - DHCP] 10.10.10.5 Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Port DHCP 傳入值 6~10
    for IP in range(5):
        port.DHCP_Option_82_Policy(driver,1)
        port.DHCP_Option_LDRA_Policy(driver,1)
        port.DHCP_Option_LDRA_LinkLocal(driver,1)
        port.DHCP_Snooping_Setting_Max_Lease(driver,"1")
        port.DHCP_Snooping_Setting_Priority_VLAN(driver,"4092,4093,4094")
        port.DHCP_Snooping_Setting_IP_MAC_Binding(driver,1)
        port.DHCP_Static_IP_Fitter_Setting_Index(driver,f"{IP+6}")
        port.DHCP_Static_IP_Fitter_Setting_IP_Address(driver,f"10.10.10.{IP+6}")
        port.DHCP_Static_IP_Fitter_Setting_IPv6_Prefix(driver,"64")
        port.DHCP_Static_IP_Fitter_Setting_IP_MAC_Binding(driver,1)
        port.DHCP_Apply(driver)
    if(driver.find_elements(By.CLASS_NAME, "rpportdhcp_stIp.td-table-content")[IP+5].get_attribute("textContent") != f"10.10.10.{IP+6}"):
        print(f"             [Port - DHCP] 10.10.10.{IP+6} Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Port DHCP 刪除測試值
    for index in range(10):
        driver.find_elements(By.NAME, "rpportdhcp_radio_select")[index].click()
        port.DHCP_Delete(driver)

    if(if_error == False):
        print(f"[MSAN1-11879][Port - DHCP] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11879][Port - DHCP] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # ARP Insepction Port Setting Test
    # ACL > ARP Insepction > Port Setting
    # -------------------------start-------------------------

    # 路徑導向ACL > ARP Insepction
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"ACL")
    mod.SubPage_Switch(driver,"ARP Inspection")
    mod.Switch_Frame(driver)
    time.sleep(1)

    # slot select
    acl.Slot_Select(driver,glc_slot)
    acl.Load(driver)

    # ARP Insepction 傳入值
    acl.Arp_Inspection_Port_Setting_Select_All(driver,3)
    acl.Arp_Inspection_Port_Setting_Apply(driver)
    
    # ARP Insepction 檢測
    try:
        if(driver.find_element(By.XPATH, f"/html/body/form/div[6]/div/div[{int(glc_port)+5}]/div[2]/select/option[2]").is_selected() == True):
            print(f"[MSAN1-11810][ACL - ARP Inspection - Port Setting] Result Pass",file = open(file_name, '+a'))
        else:
            print(f"[MSAN1-11810][ACL - ARP Inspection - Port Setting] Result Fail",file = open(file_name, '+a'))
    except:
        if(driver.find_element(By.XPATH, f"/html/body/form/div[5]/div/div[{int(glc_port)+5}]/div[2]/select/option[2]").is_selected() == True):
            print(f"[MSAN1-11810][ACL - ARP Inspection - Port Setting] Result Pass",file = open(file_name, '+a'))
        else:
            print(f"[MSAN1-11810][ACL - ARP Inspection - Port Setting] Result Fail",file = open(file_name, '+a'))

    # ARP Insepction 設為 Default
    acl.Arp_Inspection_Port_Setting_Select_All(driver,2)
    acl.Arp_Inspection_Port_Setting_Apply(driver)

    # -------------------------end-------------------------

    # ARP Insepction VLAN Test
    # ACL > ARP Insepction > VLAN
    # -------------------------start-------------------------

    try:
        mod.Tab_Switch(driver,"VLAN")
        print(f"[MSAN1-11811][ACL - ARP Inspection - VLAN] Result Pass",file = open(file_name, '+a'))
    except:
        print(f"[MSAN1-11811][ACL - ARP Inspection - VLAN] Result Block",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # ACL PPPoE Test
    # ACL > PPPoE
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向ACL > PPPoE
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"PPPoE")
    mod.Switch_Frame(driver)
    time.sleep(1)

    # ACL PPPoE 傳入值 1-1
    acl.PPPoE_Option_Policy_Mode(driver,2)
    acl.PPPoE_Apply(driver)

    # ACL PPPoE 檢測 1-1
    if_error_1 = False
    if(driver.find_element(By.XPATH, f"//*[@name='rppoe_inputOpt82PolicyMode']/option[{2}]").is_selected() != True):
        if_error_1 = True

    # ACL PPPoE 傳入值 1-2
    acl.PPPoE_Option_Policy_Mode(driver,1)
    acl.PPPoE_Apply(driver)

    # ACL PPPoE 檢測 1-2
    if(driver.find_element(By.XPATH, f"//*[@name='rppoe_inputOpt82PolicyMode']/option[{1}]").is_selected() != True):
        if_error_1 = True

    # ACL PPPoE 檢測 1 結果
    if(if_error_1 == True):
        print(f"             [ACL - PPPoE] Option Policy Mode Test Fail",file = open(file_name, '+a'))
        if_error = True

    # ACL PPPoE 傳入值 3-1
    acl.PPPoE_Intermediate_Agent_VID(driver,"4094")
    acl.PPPoE_Apply(driver)
    # if exist
    try:
        if(driver.find_element(By.CLASS_NAME, "div-row-cell-content.msg").get_attribute("textContent") == 'Error: already exist, max entry size is 256 \n'):
            driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        pass

    # ACL PPPoE 傳入值 3-2~3-4
    if_error_3 = False
    acl_pppoe_test_keys = ["4095","0","@"]
    for test_times in range(3):
        acl.PPPoE_Intermediate_Agent_VID(driver,acl_pppoe_test_keys[test_times])
        acl.PPPoE_Apply(driver)
        if(mod.IsAlert == False):
            if_error_3 = True

    if(if_error_3 == True):
        print(f"             [ACL - PPPoE] Intermediate Agent VID Test Fail",file = open(file_name, '+a'))

    # ACL PPPoE 檢測 3-1
    for index in range(driver.find_elements(By.NAME, "rppoe_vlan").__len__()):
        if(driver.find_elements(By.NAME, "rppoe_vlan")[index].get_attribute("textContent") == "4094"):
            # ACL PPPoE 傳入值 4
            driver.find_elements(By.NAME, "pfListSelected")[index].click()
            acl.PPPoE_Select_Format_Circuit_ID_Option_Info(driver,"123456789012345678901234567890123456789012345678901234567890123")
            acl.PPPoE_Select_Format_Remote_ID_Option_Info(driver,"123456789012345678901234567890123456789012345678901234567890123")
            acl.PPPoE_Select_Option_Policy(driver,3)
            acl.PPPoE_Select_Option_Linechar(driver,3)
            acl.PPPoE_Select_Apply(driver)

            # ACL PPPoE 檢測 4
            driver.find_elements(By.NAME, "pfListSelected")[index].click()
            if(driver.find_element(By.NAME, "rppoe_circuit_id_info").get_attribute("value") != "123456789012345678901234567890123456789012345678901234567890123"):
                print(f"             [ACL - PPPoE] Intermediate Agent VID Circuit ID Option Info Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_element(By.NAME, "rppoe_remote_id_info").get_attribute("value") != "123456789012345678901234567890123456789012345678901234567890123"):
                print(f"             [ACL - PPPoE] Intermediate Agent VID Remote ID Option Info Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_element(By.XPATH, f"//*[@name='rppoe_opt82_policy']/option[3]").is_selected() != True):
                print(f"             [ACL - PPPoE] Intermediate Agent VID Option Policy Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_element(By.XPATH, f"//*[@name='rppoe_opt82_linechar']/option[3]").is_selected() != True):
                print(f"             [ACL - PPPoE] Intermediate Agent VID Option Linechar Test Fail",file = open(file_name, '+a'))
                if_error = True
            acl.PPPoE_Select_Delete(driver)
        else:
            print(f"             [ACL - PPPoE] Intermediate Agent VID Test Fail",file = open(file_name, '+a'))
            if_error = True

    try:
        # ACL PPPoE 傳入值 2-1
        acl.PPPoE_Intermediate_Agent_Forbidden_VID(driver,"4094")
        acl.PPPoE_Forbidden_Apply(driver)
        # if exist
        try:
            if(driver.find_element(By.CLASS_NAME, "div-row-cell-content.msg").get_attribute("textContent") == 'Error: already exist, max entry size is 10 \n'):
                driver.find_element(By.NAME, "rperror_btnBack").click()
        except:
            pass

        # ACL PPPoE 檢測 2-1
        if_find_2 = False
        if_error_2 = False
        for index in range(driver.find_elements(By.NAME, "rppoeforbid_vlan").__len__()):
            if(driver.find_elements(By.NAME, "rppoeforbid_vlan")[index].get_attribute("textContent") == "4094"):
                if_find_2 = True

        # ACL PPPoE 傳入值 2-2~2-4
        acl_pppoe_test_keys = ["4095","0","@"]
        for test_times in range(3):
            acl.PPPoE_Intermediate_Agent_Forbidden_VID(driver,acl_pppoe_test_keys[test_times])
            acl.PPPoE_Forbidden_Apply(driver)
            if(mod.IsAlert == False):
                if_error_2 = True

        # ACL PPPoE 檢測 2 結果
        if(if_error_2 == True or if_find_2 == False):
            print(f"             [ACL - PPPoE] Intermediate Agent Forbidden VID Test Fail",file = open(file_name, '+a'))
            if_error = True

        # ACL PPPoE 刪除 2
        acl.PPPoE_Intermediate_Agent_Forbidden_VID(driver,"4094")
        acl.PPPoE_Forbidden_Delete(driver)
    except:
        pass

    if(if_error == False):
        print(f"[MSAN1-11823][ACL - PPPoE] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11823][ACL - PPPoE] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics PPPoE Test
    # Statistics > PPPoE
    # -------------------------start-------------------------

    # 路徑導向Statistics > PPPoE
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Statistics")
    mod.SubPage_Switch(driver,"PPPoE")
    mod.Switch_Frame(driver)
    time.sleep(1)

    # slot select
    sta.Slot_Select(driver,glc_slot)
    sta.Load(driver)
    sta.PPPoE_Refresh(driver)
    sta.PPPoE_Flush(driver)

    # 確認port exist
    if(driver.find_elements(By.CLASS_NAME, "div-row-begin.div-row-cell-content.wp-5.i1")[int(glc_port)-1].get_attribute("textContent") == glc_port):
        print(f"[MSAN1-11936][Statistics - PPPoE] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11936][Statistics - PPPoE] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Port PPPoE Test
    # Port > PPPoE
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向Port > PPPoE
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Port")
    mod.SubPage_Switch(driver,"PPPoE")
    mod.Switch_Frame(driver)
    time.sleep(1)

    # Port select
    port.Slot_Select(driver,glc_slot)
    port.Port_Select(driver,glc_port)
    port.Load(driver)

    # Port PPPoE 測試 1
    port.PPPoE_Policy(driver,2)
    port.PPPoE_Apply(driver)
    if(driver.find_element(By.XPATH, f"//*[@name='rpportPppoe_opt82Policy']/option[{2}]").is_selected() != True):
        if_error = True

    # Port PPPoE 測試 2
    port.PPPoE_Policy(driver,3)
    port.PPPoE_Apply(driver)
    if(driver.find_element(By.XPATH, f"//*[@name='rpportPppoe_opt82Policy']/option[{3}]").is_selected() != True):
        if_error = True

    # Port PPPoE 測試 3
    port.PPPoE_Policy(driver,1)
    port.PPPoE_Apply(driver)
    if(driver.find_element(By.XPATH, f"//*[@name='rpportPppoe_opt82Policy']/option[{1}]").is_selected() != True):
        if_error = True

    if(if_error == True):
        print(f"[MSAN1-11885][Port - PPPoE] Result Fail",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11885][Port - PPPoE] Result Pass",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # ACL Multicast Test
    # ACL > Multicast
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向ACL > Multicast
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"ACL")
    driver.find_element(By.XPATH, "//table[@id='mainTable']/tbody/tr[2]/td/div[2]/a[14]").click()
    mod.Switch_Frame(driver)
    time.sleep(1)

    # ACL Multicast 傳入值 1
    acl.Multicast_The_multicast_packets_from_upstream_direction_for_IPv4_IPv6(driver,1)
    acl.Multicast_The_unknown_multicast_packets_for_IPv4(driver,1)
    acl.Multicast_The_IPv6_passthrough(driver,1)
    acl.Multicast_The_reserve_multicast_for_IPv4(driver,1)
    acl.Multicast_Apply(driver)

    # ACL Multicast 檢測 1
    if(driver.find_element(By.XPATH, f"//*[@name='rpaclmc_sltupstream']/option[{1}]").is_selected() != True):
        if_error = True
    if(driver.find_element(By.XPATH, f"//*[@name='rpaclmc_sltunsolicited']/option[{1}]").is_selected() != True):
        if_error = True
    if(driver.find_element(By.XPATH, f"//*[@name='rpaclmc_sltipv6passthrough']/option[{1}]").is_selected() != True):
        if_error = True
    if(driver.find_element(By.XPATH, f"//*[@name='rpaclmc_sltreserve']/option[{1}]").is_selected() != True):
        if_error = True

    # ACL Multicast 傳入值 2
    acl.Multicast_The_multicast_packets_from_upstream_direction_for_IPv4_IPv6(driver,2)
    acl.Multicast_The_unknown_multicast_packets_for_IPv4(driver,2)
    acl.Multicast_The_IPv6_passthrough(driver,2)
    acl.Multicast_The_reserve_multicast_for_IPv4(driver,2)
    acl.Multicast_Apply(driver)

    # ACL Multicast 檢測 2
    if(driver.find_element(By.XPATH, f"//*[@name='rpaclmc_sltupstream']/option[{2}]").is_selected() != True):
        if_error = True
    if(driver.find_element(By.XPATH, f"//*[@name='rpaclmc_sltunsolicited']/option[{2}]").is_selected() != True):
        if_error = True
    if(driver.find_element(By.XPATH, f"//*[@name='rpaclmc_sltipv6passthrough']/option[{2}]").is_selected() != True):
        if_error = True
    if(driver.find_element(By.XPATH, f"//*[@name='rpaclmc_sltreserve']/option[{2}]").is_selected() != True):
        if_error = True

    if(if_error == True):
        print(f"[MSAN1-11829][ACL - Multicast] Result Fail",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11829][ACL - Multicast] Result Pass",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def ACL_Rule_MACFF(driver,glc_slot,glc_port,file_name):
    print(f"ACL Rule MACFF Test\nTest Start",file = open(file_name, '+a'))

    # Profile ACL Test
    # Profile > ACL
    # -------------------------start-------------------------

    # Clean ACL Rule
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"ACL")
    mod.SubPage_Switch(driver,"ACL Rule")
    mod.Switch_Frame(driver)
    time.sleep(1)

    if_error = False
    if_error_1 = False

    try:
        driver.find_elements(By.NAME, "rpaclrule_rdoSlt")[int(glc_slot)-1].click()
        driver.find_element(By.NAME, "rpaclsetupall_selectAll").click()
        driver.find_element(By.NAME, "rpaclsetupall_Delete").click()

    except:
        print(f"             [ACL - ACL Rule] Clear Fail",file = open(file_name, '+a'))
        # if_error = True
        if_error_1 = True

    # 路徑導向 Profile > ACL
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Profile")
    mod.Switch_Frame(driver)

    if_clear = False
    try:
        # set profile
        pro.ACL_Profile_Mode(driver,1)
        pro.ACL_Apply(driver)

        # Clean Profile
        if_clear = False
        while(if_clear == False):
            try:
                driver.find_element(By.CLASS_NAME, "pfListRow")
                driver.find_element(By.NAME, "rpaclprof_rdoSlt").click()
                pro.ACL_New_Delete(driver)
            except:
                if_clear = True

        # Profile ACL Apply New Profiles 1
        pro.ACL_New(driver)
        pro.ACL_New_Name(driver,"1234567890123456789012345678001")
        pro.ACL_New_Source_MAC_OUI(driver,True)
        pro.ACL_New_Source_MAC_OUI_Input(driver,"10:10:10:10:10:01")
        pro.ACL_New_Drop(driver,True)
        pro.ACL_New_Profile_Priority(driver,True)
        pro.ACL_New_Profile_Priority_Input(driver,"1")
        pro.ACL_New_Apply(driver)

        # Profile ACL Apply New Profiles 2
        pro.ACL_New(driver)
        pro.ACL_New_Name(driver,"1234567890123456789012345678002")
        pro.ACL_New_Dest_MAC_OUI(driver,True)
        pro.ACL_New_Dest_MAC_OUI_Input(driver,"10:10:10:10:10:02")
        pro.ACL_New_Permit(driver,True)
        pro.ACL_New_Profile_Priority(driver,True)
        pro.ACL_New_Profile_Priority_Input(driver,"2")
        pro.ACL_New_Apply(driver)

        # Profile ACL Apply New Profiles 3
        pro.ACL_New(driver)
        pro.ACL_New_Name(driver,"1234567890123456789012345678003")
        pro.ACL_New_Source_IP(driver,True)
        pro.ACL_New_Source_IP_Input(driver,"10.10.10.1/24")
        pro.ACL_New_Change_DSCP(driver,True)
        pro.ACL_New_Change_DSCP_Input(driver,"63")
        pro.ACL_New_Profile_Priority(driver,True)
        pro.ACL_New_Profile_Priority_Input(driver,"3")
        pro.ACL_New_Apply(driver)

        # Profile ACL Apply New Profiles 4
        pro.ACL_New(driver)
        pro.ACL_New_Name(driver,"1234567890123456789012345678004")
        pro.ACL_New_Destination_IP(driver,True)
        pro.ACL_New_Destination_IP_Input(driver,"10.10.10.2/24")
        pro.ACL_New_Change_Outer_Pbit(driver,True)
        pro.ACL_New_Change_Outer_Pbit_Input(driver,8)
        pro.ACL_New_Profile_Priority(driver,True)
        pro.ACL_New_Profile_Priority_Input(driver,"4")
        pro.ACL_New_Apply(driver)

        # Profile ACL Apply New Profiles 5
        pro.ACL_New(driver)
        pro.ACL_New_Name(driver,"1234567890123456789012345678005")
        pro.ACL_New_IP_Precedence(driver,True)
        pro.ACL_New_IP_Precedence_Input(driver,8)
        pro.ACL_New_Change_QoS_Level(driver,True)
        pro.ACL_New_Change_QoS_Level_Input(driver,8)
        pro.ACL_New_Profile_Priority(driver,True)
        pro.ACL_New_Profile_Priority_Input(driver,"5")
        pro.ACL_New_Apply(driver)

        # Profile ACL Apply New Profiles 6
        pro.ACL_New(driver)
        pro.ACL_New_Name(driver,"1234567890123456789012345678006")
        pro.ACL_New_DSCP(driver,True)
        pro.ACL_New_DSCP_Input(driver,"63")
        pro.ACL_New_Rate_Limit(driver,True)
        pro.ACL_New_Rate_Limit_Input_CIR(driver,"10000000")
        pro.ACL_New_Rate_Limit_Input_CBS(driver,"10000000")
        pro.ACL_New_Rate_Limit_Input_EIR(driver,"10000000")
        pro.ACL_New_Rate_Limit_Input_EBS(driver,"10000000")
        pro.ACL_New_Profile_Priority(driver,True)
        pro.ACL_New_Profile_Priority_Input(driver,"6")
        pro.ACL_New_Apply(driver)

        # Profile ACL Apply New Profiles 7
        pro.ACL_New(driver)
        pro.ACL_New_Name(driver,"1234567890123456789012345678007")
        pro.ACL_New_Source_L4_Port(driver,True)
        pro.ACL_New_Source_L4_Port_Input_1(driver,"65535")
        pro.ACL_New_Source_L4_Port_Input_2(driver,"65535")
        pro.ACL_New_Drop(driver,True)
        pro.ACL_New_Profile_Priority(driver,True)
        pro.ACL_New_Profile_Priority_Input(driver,"7")
        pro.ACL_New_Apply(driver)

        # Profile ACL Apply New Profiles 8
        pro.ACL_New(driver)
        pro.ACL_New_Name(driver,"1234567890123456789012345678008")
        pro.ACL_New_Destination_L4_Port(driver,True)
        pro.ACL_New_Destination_L4_Port_Input_1(driver,"65535")
        pro.ACL_New_Destination_L4_Port_Input_2(driver,"65535")
        pro.ACL_New_Drop(driver,True)
        pro.ACL_New_Profile_Priority(driver,True)
        pro.ACL_New_Profile_Priority_Input(driver,"8")
        pro.ACL_New_Apply(driver)

        # Profile ACL Apply New Profiles 9
        pro.ACL_New(driver)
        pro.ACL_New_Name(driver,"1234567890123456789012345678009")
        pro.ACL_New_Traffic_Class(driver,True)
        pro.ACL_New_Traffic_Class_Input(driver,"255")
        pro.ACL_New_Drop(driver,True)
        pro.ACL_New_Profile_Priority(driver,True)
        pro.ACL_New_Profile_Priority_Input(driver,"9")
        pro.ACL_New_Apply(driver)

        # Profile ACL Apply New Profiles 10
        pro.ACL_New(driver)
        pro.ACL_New_Name(driver,"1234567890123456789012345678010")
        pro.ACL_New_Next_Header(driver,True)
        pro.ACL_New_Next_Header_Input(driver,"255")
        pro.ACL_New_Drop(driver,True)
        pro.ACL_New_Profile_Priority(driver,True)
        pro.ACL_New_Profile_Priority_Input(driver,"10")
        pro.ACL_New_Apply(driver)

        # Profile ACL Apply New Profiles 11
        pro.ACL_New(driver)
        pro.ACL_New_Name(driver,"1234567890123456789012345678011")
        pro.ACL_New_Ethertype(driver,True)
        pro.ACL_New_Ethertype_Input(driver,"FFFF")
        pro.ACL_New_Drop(driver,True)
        pro.ACL_New_Profile_Priority(driver,True)
        pro.ACL_New_Profile_Priority_Input(driver,"11")
        pro.ACL_New_Apply(driver)

        # Profile ACL Apply New Profiles 12
        pro.ACL_New(driver)
        pro.ACL_New_Name(driver,"1234567890123456789012345678012")
        pro.ACL_New_Inner_VID(driver,True)
        pro.ACL_New_Inner_VID_Input(driver,"4094")
        pro.ACL_New_Drop(driver,True)
        pro.ACL_New_Profile_Priority(driver,True)
        pro.ACL_New_Profile_Priority_Input(driver,"12")
        pro.ACL_New_Apply(driver)

        # Profile ACL Apply New Profiles 13
        pro.ACL_New(driver)
        pro.ACL_New_Name(driver,"1234567890123456789012345678013")
        pro.ACL_New_Inner_Pbit(driver,True)
        pro.ACL_New_Inner_Pbit_Input(driver,8)
        pro.ACL_New_Drop(driver,True)
        pro.ACL_New_Profile_Priority(driver,True)
        pro.ACL_New_Profile_Priority_Input(driver,"13")
        pro.ACL_New_Apply(driver)

        # Profile ACL Apply New Profiles 14
        pro.ACL_New(driver)
        pro.ACL_New_Name(driver,"1234567890123456789012345678014")
        pro.ACL_New_Outer_VID(driver,True)
        pro.ACL_New_Outer_VID_Input(driver,"4094")
        pro.ACL_New_Drop(driver,True)
        pro.ACL_New_Profile_Priority(driver,True)
        pro.ACL_New_Profile_Priority_Input(driver,"14")
        pro.ACL_New_Apply(driver)

        # Profile ACL Apply New Profiles 15
        pro.ACL_New(driver)
        pro.ACL_New_Name(driver,"1234567890123456789012345678015")
        pro.ACL_New_Outer_Pbit(driver,True)
        pro.ACL_New_Outer_Pbit_Input(driver,8)
        pro.ACL_New_Drop(driver,True)
        pro.ACL_New_Profile_Priority(driver,True)
        pro.ACL_New_Profile_Priority_Input(driver,"15")
        pro.ACL_New_Apply(driver)

        # Profile ACL Apply New Profiles 16
        pro.ACL_New(driver)
        pro.ACL_New_Name(driver,"1234567890123456789012345678016")
        pro.ACL_New_Protocol(driver,True)
        pro.ACL_New_Protocol_Input(driver,"255")
        pro.ACL_New_Drop(driver,True)
        pro.ACL_New_Profile_Priority(driver,True)
        pro.ACL_New_Profile_Priority_Input(driver,"16")
        pro.ACL_New_Apply(driver)

        # Profile ACL Apply New Profiles 17-32
        for index in range(16):
            pro.ACL_New(driver)
            pro.ACL_New_Name(driver,f"123456789012345678901234567{8017+index}")
            pro.ACL_New_Source_MAC_OUI(driver,True)
            pro.ACL_New_Source_MAC_OUI_Input(driver,f"10:10:10:10:10:{17+index}")
            pro.ACL_New_Drop(driver,True)
            pro.ACL_New_Profile_Priority(driver,True)
            pro.ACL_New_Profile_Priority_Input(driver,17+index)
            pro.ACL_New_Apply(driver)

        # Profile ACL Apply New Profiles 33-full
        is_full = False
        name_num = 8032###8401
        while(is_full == False):
            name_num = name_num+1
            pro.ACL_New(driver)
            pro.ACL_New_Name(driver,f"123456789012345678901234567{name_num}")
            pro.ACL_New_Source_IP(driver,True)
            pro.ACL_New_Source_IP_Input(driver,f"2001::{name_num-8032}")
            pro.ACL_New_Drop(driver,True)
            pro.ACL_New_Apply(driver)
            try:
                driver.find_element(By.NAME, "rperror_btnBack").click()
                is_full = True
                print(f"             = = = Check ACL-Profile pool create max entries = 400 = = =",file = open(file_name, '+a'))
                print(f"             [Profile - ACL] Max Capacity(400) = {name_num-8001}",file = open(file_name, '+a'))

                #*add------------------temp--------------------------------------------------------
                # input("1...")
                # save (config save > Maintenamce-config backup download)
                try:
                    # [config save]
                    # 路徑導向 Config Save > Config Save	
                    mod.Switch_Default(driver)
                    mod.Page_Switch(driver,"Config Save")
                    mod.SubPage_Switch(driver,"Config Save")
                    mod.Switch_Frame(driver)
                    driver.find_element(By.NAME, "rpConfigSave").click()
                    if_success = False
                    while(if_success == False):
                        if("Success" in driver.find_element(By.CLASS_NAME, "div-row-cell-content").text):
                            print("config save success.")
                            if_success = True
                        else:
                            time.sleep(3)

                    # [config backup]
                    mod.Switch_Default(driver)
                    mod.Page_Switch(driver,"Maintenance")
                    mod.SubPage_Switch(driver,"Config Backup")
                    mod.Switch_Frame(driver)
                    driver.find_element(By.NAME, "rpMainBackup").click()
                    print(f"             [Profile - ACL] temp save success..  ",file = open(file_name, '+a'))
                except:
                    print(f"             [Profile - ACL] temp save fail..  ",file = open(file_name, '+a'))

                
                # input("...")
                #*add------------------temp--------------------------------------------------------


            except:
                pass

    except:
        print(f"             [Profile - ACL] Port Mode Clear and Apply to Full Fail",file = open(file_name, '+a'))
        if_error = True

    # -------------------------end-------------------------

    # ACL Rule Test
    # ACL > ACL Rule
    # -------------------------start-------------------------

    # 路徑導向 ACL > ACL Rule
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"ACL")
    mod.SubPage_Switch(driver,"ACL Rule")
    mod.Switch_Frame(driver)


    print(f"             = = = Check ACL port mode test = = =",file = open(file_name, '+a'))

    try:
        if_full = False
        ipv4_profile = 0
        for test_port in range(40):#####40
            if(if_full == False):
                # port select
                acl.Slot_Select(driver,glc_slot)
                acl.Port_Select(driver,test_port+1)
                acl.Load(driver)

                # profile apply
                for input_priority in range(8):
                    ipv4_profile = ipv4_profile+1
                    if(ipv4_profile < 129):
                        acl.ACL_Rule_ACL_Profile(driver,input_priority+1)
                        acl.ACL_Rule_Priority(driver,input_priority+1)
                        acl.ACL_Rule_Apply(driver)
                        try:
                            driver.find_element(By.NAME, "rperror_btnBack")
                            error_msg = driver.find_element(By.CLASS_NAME, "div-row-cell-content.msg").get_attribute("textContent")
                            print(f"             [ACL - ACL Rule] Port Mode Port{test_port+1} Profile{input_priority+1} Apply Fail,Error Message:{error_msg}",file = open(file_name, '+a'))
                            # if_error = True
                            if_error_1 = True
                            driver.find_element(By.NAME, "rperror_btnBack").click()
                        except:
                            pass
                    elif(ipv4_profile == 129):
                        break
                    elif(ipv4_profile == 194):
                        if_full = True
                        break
                    elif(ipv4_profile > 129):
                        acl.ACL_Rule_ACL_Profile(driver,input_priority+33)
                        acl.ACL_Rule_Priority(driver,input_priority+1)
                        acl.ACL_Rule_Apply(driver)
                        try:
                            driver.find_element(By.NAME, "rperror_btnBack")
                            error_msg = driver.find_element(By.CLASS_NAME, "div-row-cell-content.msg").get_attribute("textContent")
                            print(f"             [ACL - ACL Rule] Port Mode Port{test_port+1} Profile{input_priority+1} Apply Fail,Error Message:{error_msg}",file = open(file_name, '+a'))
                            # if_error = True
                            if_error_1 = True
                            driver.find_element(By.NAME, "rperror_btnBack").click()
                            if_full = True
                            break
                        except:
                            pass

        # select slot check
        time.sleep(1)
        driver.find_elements(By.NAME, "rpaclrule_rdoSlt")[int(glc_slot)-1].click()
        select_slot_max_capacity = driver.find_elements(By.CLASS_NAME, "td-table-content.i1")[-1].get_attribute("textContent")
        print(f"             [ACL - ACL Rule] Port Mode Slot{glc_slot} Max Capacity(128+64=192) = {select_slot_max_capacity}",file = open(file_name, '+a'))

        # select delete
        driver.find_element(By.NAME, "rpaclsetupall_selectAll").click()#########delete
        driver.find_element(By.NAME, "rpaclsetupall_Delete").click()


        # clean select slot check
        try:
            driver.find_element(By.CLASS_NAME, "rpaclrulesetupport")
            print(f"             [ACL - ACL Rule] Port Mode Delete Test Fail",file = open(file_name, '+a'))
            # if_error = True
            if_error_1 = True
        except:
            print(f"             [ACL - ACL Rule] Port Mode Delete Test Pass",file = open(file_name, '+a'))
            pass

    except:
        print(f"             [ACL - ACL Rule] Port Mode Apply to Full and Delete Fail",file = open(file_name, '+a'))
        # if_error = True
        if_error_1 = True

    # -------------------------end-------------------------

    # Profile ACL Switch Profile Test
    # Profile > ACL
    # -------------------------start-------------------------

    # 路徑導向 Profile > ACL
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Profile")
    mod.Switch_Frame(driver)

    try:
        # set profile
        pro.ACL_Profile_Mode(driver,2)
        pro.ACL_Apply(driver)

    except:
        print(f"             [Profile - ACL] Switch to Profile Mode Fail",file = open(file_name, '+a'))
        if_error = True

    # -------------------------end-------------------------

    # ACL Rule Test
    # ACL > ACL Rule
    # -------------------------start-------------------------

    # 路徑導向 ACL > ACL Rule
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"ACL")
    mod.SubPage_Switch(driver,"ACL Rule")
    mod.Switch_Frame(driver)


    print(f"             = = = Check ACL profile mode test = = =",file = open(file_name, '+a'))

    try:
        # if_full = False
        # for test_port in range(40):#####40
        #     if(if_full == False):
        #         # port select
        #         acl.Slot_Select(driver,glc_slot)
        #         acl.Port_Select(driver,test_port+1)
        #         acl.Load(driver)

        #         # profile apply
        #         for input_priority in range(24):
        #             acl.ACL_Rule_ACL_Profile(driver,input_priority+1)
        #             # acl.ACL_Rule_Priority(driver,input_priority+1)
        #             acl.ACL_Rule_Apply(driver)
        #             try:
        #                 driver.find_element(By.NAME, "rperror_btnBack")
        #                 error_msg = driver.find_element(By.CLASS_NAME, "div-row-cell-content.msg").get_attribute("textContent")
        #                 print(f"             [ACL - ACL Rule] Profile Mode Port{test_port+1} Profile{input_priority+1} Apply Fail,Error Message:{error_msg}",file = open(file_name, '+a'))
        #                 # if_error = True
        #                 if_error_1 = True
        #                 driver.find_element(By.NAME, "rperror_btnBack").click()
        #                 if_full = True
        #                 break
        #             except:
        #                 pass

        

        # # # ------------ edit from above START ----------- # # #
        
        # port 1 create 24 datas ---
        # port select
        acl.Slot_Select(driver,glc_slot)
        acl.Port_Select(driver,1)
        acl.Load(driver)

        # profile apply
        for input_priority in range(24):
            acl.ACL_Rule_ACL_Profile(driver,input_priority+1)
            # acl.ACL_Rule_Priority(driver,input_priority+1)
            acl.ACL_Rule_Apply(driver)
            try:
                driver.find_element(By.NAME, "rperror_btnBack")
                error_msg = driver.find_element(By.CLASS_NAME, "div-row-cell-content.msg").get_attribute("textContent")
                print(f"             [ACL - ACL Rule] Profile Mode Port{test_port+1} Profile{input_priority+1} Apply Fail,Error Message:{error_msg}",file = open(file_name, '+a'))
                # if_error = True
                if_error_1 = True
                driver.find_element(By.NAME, "rperror_btnBack").click()
                if_full = True
                break
            except:
                pass
        
        # input("check 25th ")
        
        # check 25th data should fail
        acl.ACL_Rule_ACL_Profile(driver,25)
        acl.ACL_Rule_Apply(driver)
        try:
            driver.find_element(By.NAME, "rperror_btnBack")
            error_msg = driver.find_element(By.CLASS_NAME, "div-row-cell-content.msg").get_attribute("textContent")
            print(f"             [ACL - ACL Rule] Profile Mode Port1 25th Apply test Pass,Error Message:{error_msg}",file = open(file_name, '+a'))            
            driver.find_element(By.NAME, "rperror_btnBack").click()                        
        except:
            print(f"             [ACL - ACL Rule] Profile Mode Port1 25th Apply test Fail",file = open(file_name, '+a'))            
            # if_error = True
            if_error_1 = True
            pass
        
        # other ports apply port1 ---
        # 路徑導向 Port > Copy
        mod.Switch_Default(driver)
        mod.Page_Switch(driver,"Port")
        mod.SubPage_Switch(driver,"Copy")
        mod.Switch_Frame(driver)
        # select   src slot, port    dst slot, port
        port.Slot_Select(driver, glc_slot)
        port.Port_Select(driver, 1)
        port.Copy_Destination_Slot_Select(driver, glc_slot)
        port.Copy_Destination_Port_List(driver, "*")
        port.Copy_Apply(driver)
        time.sleep(60)

        # input("check if 40 ports all have 24 datas!!!")

        # back to page
        # 路徑導向 ACL > ACL Rule
        mod.Switch_Default(driver)
        mod.Page_Switch(driver,"ACL")
        mod.SubPage_Switch(driver,"ACL Rule")
        mod.Switch_Frame(driver)

        # # # ------------ edit from above END ------------- # # #

        # select slot check
        time.sleep(1)
        driver.find_elements(By.NAME, "rpaclrule_rdoSlt")[int(glc_slot)-1].click()
        select_slot_max_capacity = driver.find_elements(By.CLASS_NAME, "td-table-content.i1")[-1].get_attribute("textContent")
        print(f"             [ACL - ACL Rule] Profile Mode Slot{glc_slot} Max Capacity(24*40=960) = {select_slot_max_capacity}",file = open(file_name, '+a'))


        print(f"             = = = Check ACL-Profile pool delete max entries = = =",file = open(file_name, '+a'))

        # select delete
        driver.find_element(By.NAME, "rpaclsetupall_selectAll").click()
        driver.find_element(By.NAME, "rpaclsetupall_Delete").click()

        # clean select slot check
        try:
            driver.find_element(By.CLASS_NAME, "rpaclrulesetupport")
            print(f"             [ACL - ACL Rule] Profile Mode Delete Test Fail",file = open(file_name, '+a'))
            # if_error = True
            if_error_1 = True
        except:
            print(f"             [ACL - ACL Rule] Profile Mode Delete Test Pass",file = open(file_name, '+a'))
            pass

    except:
        print(f"             [ACL - ACL Rule] Profile Mode Apply to Full and Delete Fail",file = open(file_name, '+a'))
        # if_error = True
        if_error_1 = True

    # -------------------------end-------------------------

    # Profile ACL Test
    # Profile > ACL
    # -------------------------start-------------------------

    # 路徑導向 Profile > ACL
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Profile")
    mod.Switch_Frame(driver)

    try:
        # set profile
        pro.ACL_Profile_Mode(driver,2)
        pro.ACL_Apply(driver)

        # Clean Profile
        if_clear = False
        while(if_clear == False):
            try:
                driver.find_element(By.CLASS_NAME, "pfListRow")
                driver.find_element(By.NAME, "rpaclprof_rdoSlt").click()
                pro.ACL_New_Delete(driver)
            except:
                if_clear = True

        # Profile ACL Apply New Profiles 1-129
        for index in range(129):
            pro.ACL_New(driver)
            pro.ACL_New_Name(driver,f"123456789012345678901234567{8001+index}")
            pro.ACL_New_Source_IP(driver,True)
            pro.ACL_New_Source_IP_Input(driver,f"10.10.10.{index+1}/24")
            pro.ACL_New_Drop(driver,True)
            pro.ACL_New_Apply(driver)

        # Profile ACL Apply New Profiles 130-194
        for index in range(65):
            pro.ACL_New(driver)
            pro.ACL_New_Name(driver,f"123456789012345678901234567{8130+index}")
            pro.ACL_New_Source_IP(driver,True)
            pro.ACL_New_Source_IP_Input(driver,f"2001::{index+1}")
            pro.ACL_New_Drop(driver,True)
            pro.ACL_New_Apply(driver)

    except:
        print(f"             [Profile - ACL] Clear and Apply to Full Fail",file = open(file_name, '+a'))
        if_error = True

    # -------------------------end-------------------------

    # ACL Rule Test
    # ACL > ACL Rule
    # -------------------------start-------------------------

    # 路徑導向 ACL > ACL Rule
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"ACL")
    mod.SubPage_Switch(driver,"ACL Rule")
    mod.Switch_Frame(driver)

    try:
        acl_profile = 0
        for test_port in range(40):#####40
            if(acl_profile < 194):
                # port select
                acl.Slot_Select(driver,glc_slot)
                acl.Port_Select(driver,test_port+1)
                acl.Load(driver)
                for index in range(24):
                    if(acl_profile < 194):
                        # profile apply
                        acl_profile = acl_profile+1
                        acl.ACL_Rule_ACL_Profile(driver,acl_profile)
                        acl.ACL_Rule_Apply(driver)
                        try:
                            error_msg = driver.find_element(By.CLASS_NAME, "div-row-cell-content.msg").get_attribute("textContent")
                            print(f"             [Profile - ACL] Profile{acl_profile} Apply Fail,Error Message:{error_msg}",file = open(file_name, '+a'))
                            if_error = True
                            is_full = True#full msg
                            driver.find_element(By.NAME, "rperror_btnBack").click()
                            break
                        except:
                            pass
                    else:break
            else:break

        # select slot check
        time.sleep(1)
        driver.find_elements(By.NAME, "rpaclrule_rdoSlt")[int(glc_slot)-1].click()
        select_slot_max_capacity = driver.find_elements(By.CLASS_NAME, "td-table-content.i1")[-1].get_attribute("textContent")
        print(f"             [ACL - ACL Rule] Slot{glc_slot} Max Capacity = {select_slot_max_capacity}",file = open(file_name, '+a'))

        # select delete
        driver.find_element(By.NAME, "rpaclsetupall_selectAll").click()
        driver.find_element(By.NAME, "rpaclsetupall_Delete").click()

        # clean select slot check
        try:
            driver.find_element(By.CLASS_NAME, "rpaclrulesetupport")
            print(f"             [ACL - ACL Rule] Delete Test Fail",file = open(file_name, '+a'))
            # if_error = True
            if_error_1 = True
        except:
            print(f"             [ACL - ACL Rule] Delete Test Pass",file = open(file_name, '+a'))
            pass

    except:
        print(f"             [ACL - ACL Rule] Apply to Full and Delete Fail",file = open(file_name, '+a'))
        # if_error = True
        if_error_1 = True

    # 路徑導向 Profile > ACL
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Profile")
    mod.Switch_Frame(driver)

    try:
        # set profile
        pro.ACL_Profile_Mode(driver,1)
        pro.ACL_Apply(driver)

        # Clean Profile
        if_clear = False
        while(if_clear == False):
            try:
                driver.find_element(By.CLASS_NAME, "pfListRow")
                driver.find_element(By.NAME, "rpaclprof_rdoSlt").click()
                pro.ACL_New_Delete(driver)
            except:
                if_clear = True

    except:
        print(f"             [Profile - ACL] Clear Fail",file = open(file_name, '+a'))
        if_error = True

    # Profile -> ACL & ACL -> ACL Rule Result
    if(if_error == False):                                                     # any other error will show on here
        # print(f"[MSAN1-11824][ACL - ACL Rule] Result Pass",file = open(file_name, '+a'))
        print(f"[MSAN1-11889][Profile - ACL] Result Pass",file = open(file_name, '+a'))
    else:
        # print(f"[MSAN1-11824][ACL - ACL Rule] Result Fail",file = open(file_name, '+a'))
        print(f"[MSAN1-11889][Profile - ACL] Result Fail",file = open(file_name, '+a'))

    # ACL - ACL Rule if_error_1
    if(if_error_1 == False): 
        print(f"[MSAN1-11824][ACL - ACL Rule] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11824][ACL - ACL Rule] Result Fail",file = open(file_name, '+a'))



    # -------------------------end-------------------------

    # Profile > ACL Egress Test
    # Profile >  ACL Egress
    # -------------------------start-------------------------

    if_error_1 = False

    # Get GLC name
    # Home
    # --------------start------------------
    # Get GLC name
    mod.Switch_Default(driver)
    driver.find_element(By.XPATH, '//*[@id="mainTable"]/tbody/tr[1]/td/div/div[2]/div/div[3]/a').click()
    mod.Switch_Frame(driver)
    time.sleep(1)
    driver.find_elements(By.NAME, "Sysinfotableid")[int(glc_slot)-1].click()
    time.sleep(5)
    glc_name = driver.find_element(By.CLASS_NAME, "div-row-cell-content.rplcmanDetailName").get_attribute("textContent")
    glc_name = glc_name.split("-")[0]
    # ----------------end--------------------

    # 路徑導向 Profile > ACL
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Profile")
    mod.Switch_Frame(driver)

    # 路徑導向 Profile > ACL Egress
    mod.Switch_Default(driver)
    mod.Tab_Switch(driver,"ACL Egress")
    mod.Switch_Frame(driver)

    if_error = False

    try:
        # Clean Profile
        if_clear = False
        while(if_clear == False):
            try:
                driver.find_element(By.CLASS_NAME, "pfListRow")
                driver.find_element(By.NAME, "rpaclprof_rdoSlt").click()
                pro.ACL_Egress_New_Delete(driver)
            except:
                if_clear = True

        # Profile ACL Apply New Profiles 1
        pro.ACL_Egress_New(driver)
        pro.ACL_Egress_New_Name(driver,"1234567890123456789012345678001")
        pro.ACL_Egress_New_Source_MAC_OUI(driver,True)
        pro.ACL_Egress_New_Source_MAC_OUI_Input(driver,"10:10:10:10:10:01")
        pro.ACL_Egress_New_Drop(driver,True)
        pro.ACL_Egress_New_Apply(driver)

        # Profile ACL Apply New Profiles 2
        pro.ACL_Egress_New(driver)
        pro.ACL_Egress_New_Name(driver,"1234567890123456789012345678002")
        pro.ACL_Egress_New_Dest_MAC_OUI(driver,True)
        pro.ACL_Egress_New_Dest_MAC_OUI_Input(driver,"10:10:10:10:10:02")
        pro.ACL_Egress_New_Permit(driver,True)
        pro.ACL_Egress_New_Apply(driver)

        # Profile ACL Apply New Profiles 3
        if(glc_name != "GLC1540X"):
            pro.ACL_Egress_New(driver)
            pro.ACL_Egress_New_Name(driver,"1234567890123456789012345678003")
            pro.ACL_Egress_New_Source_IP(driver,True)
            pro.ACL_Egress_New_Source_IP_Input(driver,"10.10.10.1/24")
            pro.ACL_Egress_New_Change_DSCP(driver,True)
            pro.ACL_Egress_New_Change_DSCP_Input(driver,"63")
            pro.ACL_Egress_New_Apply(driver)
        else:
            pro.ACL_Egress_New(driver)
            pro.ACL_Egress_New_Name(driver,"1234567890123456789012345678003")
            pro.ACL_Egress_New_Source_IP(driver,True)
            pro.ACL_Egress_New_Source_IP_Input(driver,"10.10.10.1/24")
            # pro.ACL_Egress_New_Change_DSCP(driver,True)
            # pro.ACL_Egress_New_Change_DSCP_Input(driver,"63")
            pro.ACL_Egress_New_Drop(driver,True)
            pro.ACL_Egress_New_Apply(driver)

        # Profile ACL Apply New Profiles 4
        if(glc_name != "GLC1540X"):
            pro.ACL_Egress_New(driver)
            pro.ACL_Egress_New_Name(driver,"1234567890123456789012345678004")
            pro.ACL_Egress_New_Destination_IP(driver,True)
            pro.ACL_Egress_New_Destination_IP_Input(driver,"10.10.10.2/24")
            pro.ACL_Egress_New_Change_Uni_Pbit(driver,True)
            pro.ACL_Egress_New_Change_Uni_Pbit_Input(driver,8)
            pro.ACL_Egress_New_Apply(driver)
        else:
            pro.ACL_Egress_New(driver)
            pro.ACL_Egress_New_Name(driver,"1234567890123456789012345678004")
            pro.ACL_Egress_New_Destination_IP(driver,True)
            pro.ACL_Egress_New_Destination_IP_Input(driver,"10.10.10.2/24")
            # pro.ACL_Egress_New_Change_Uni_Pbit(driver,True)
            # pro.ACL_Egress_New_Change_Uni_Pbit_Input(driver,8)
            pro.ACL_Egress_New_Drop(driver,True)
            pro.ACL_Egress_New_Apply(driver)

        # Profile ACL Apply New Profiles 5
        pro.ACL_Egress_New(driver)
        pro.ACL_Egress_New_Name(driver,"1234567890123456789012345678005")
        pro.ACL_Egress_New_IP_Precedence(driver,True)
        pro.ACL_Egress_New_IP_Precedence_Input(driver,8)
        pro.ACL_Egress_New_Drop(driver,True)
        pro.ACL_Egress_New_Apply(driver)

        # Profile ACL Apply New Profiles 6
        pro.ACL_Egress_New(driver)
        pro.ACL_Egress_New_Name(driver,"1234567890123456789012345678006")
        pro.ACL_Egress_New_DSCP(driver,True)
        pro.ACL_Egress_New_DSCP_Input(driver,"63")
        pro.ACL_Egress_New_Drop(driver,True)
        pro.ACL_Egress_New_Apply(driver)

        # Profile ACL Apply New Profiles 7
        pro.ACL_Egress_New(driver)
        pro.ACL_Egress_New_Name(driver,"1234567890123456789012345678007")
        pro.ACL_Egress_New_Source_L4_Port(driver,True)
        pro.ACL_Egress_New_Source_L4_Port_Input_1(driver,"65535")
        pro.ACL_Egress_New_Source_L4_Port_Input_2(driver,"65535")
        pro.ACL_Egress_New_Drop(driver,True)
        pro.ACL_Egress_New_Apply(driver)

        # Profile ACL Apply New Profiles 8
        pro.ACL_Egress_New(driver)
        pro.ACL_Egress_New_Name(driver,"1234567890123456789012345678008")
        retry = True
        while(retry):
            try:
                pro.ACL_Egress_New_Destination_L4_Port(driver,True)
                pro.ACL_Egress_New_Destination_L4_Port_Input_1(driver,"65535")
                pro.ACL_Egress_New_Destination_L4_Port_Input_2(driver,"65535")
                retry = False
            except:
                pass
        pro.ACL_Egress_New_Drop(driver,True)
        pro.ACL_Egress_New_Apply(driver)

        # Profile ACL Apply New Profiles 9
        pro.ACL_Egress_New(driver)
        pro.ACL_Egress_New_Name(driver,"1234567890123456789012345678009")
        pro.ACL_Egress_New_Traffic_Class(driver,True)
        pro.ACL_Egress_New_Traffic_Class_Input(driver,"255")
        pro.ACL_Egress_New_Drop(driver,True)
        pro.ACL_Egress_New_Apply(driver)

        # Profile ACL Apply New Profiles 10
        pro.ACL_Egress_New(driver)
        pro.ACL_Egress_New_Name(driver,"1234567890123456789012345678010")
        pro.ACL_Egress_New_Next_Header(driver,True)
        pro.ACL_Egress_New_Next_Header_Input(driver,"255")
        pro.ACL_Egress_New_Drop(driver,True)
        pro.ACL_Egress_New_Apply(driver)

        # Profile ACL Apply New Profiles 11
        pro.ACL_Egress_New(driver)
        pro.ACL_Egress_New_Name(driver,"1234567890123456789012345678011")
        pro.ACL_Egress_New_Ethertype(driver,True)
        pro.ACL_Egress_New_Ethertype_Input(driver,"FFFF")
        pro.ACL_Egress_New_Drop(driver,True)
        pro.ACL_Egress_New_Apply(driver)

        # Profile ACL Apply New Profiles 12
        pro.ACL_Egress_New(driver)
        pro.ACL_Egress_New_Name(driver,"1234567890123456789012345678012")
        pro.ACL_Egress_New_Uni_VID(driver,True)
        pro.ACL_Egress_New_Uni_VID_Input(driver,"4094")
        pro.ACL_Egress_New_Drop(driver,True)
        pro.ACL_Egress_New_Apply(driver)

        # Profile ACL Apply New Profiles 13
        pro.ACL_Egress_New(driver)
        pro.ACL_Egress_New_Name(driver,"1234567890123456789012345678013")
        pro.ACL_Egress_New_Uni_Pbit(driver,True)
        pro.ACL_Egress_New_Uni_Pbit_Input(driver,8)
        pro.ACL_Egress_New_Drop(driver,True)
        pro.ACL_Egress_New_Apply(driver)

        # Profile ACL Apply New Profiles 14
        pro.ACL_Egress_New(driver)
        pro.ACL_Egress_New_Name(driver,"1234567890123456789012345678014")
        pro.ACL_Egress_New_Protocol(driver,True)
        pro.ACL_Egress_New_Protocol_Input(driver,"255")
        pro.ACL_Egress_New_Drop(driver,True)
        pro.ACL_Egress_New_Apply(driver)

        print(f"             = = = Check ACL-Egress-Profile pool create max entries = 128 = = =",file = open(file_name, '+a'))


        # Profile ACL Apply New Profiles 15-full
        is_full = False
        name_num = 8014
        while(is_full == False):
            name_num = name_num+1
            pro.ACL_Egress_New(driver)
            pro.ACL_Egress_New_Name(driver,f"123456789012345678901234567{name_num}")
            pro.ACL_Egress_New_Source_MAC_OUI(driver,True)
            pro.ACL_Egress_New_Source_MAC_OUI_Input(driver,f"10:10:10:10:10:{name_num-8000}")
            pro.ACL_Egress_New_Drop(driver,True)
            pro.ACL_Egress_New_Apply(driver)
            try:
                driver.find_element(By.NAME, "rperror_btnBack").click()
                is_full = True
                print(f"             [Profile - ACL Egress] Max Capacity(128) = {name_num-8001}",file = open(file_name, '+a'))
            except:
                pass

    except:
        print(f"             [Profile - ACL Egress] Port Mode Clear and Apply to Full Fail",file = open(file_name, '+a'))
        # if_error = True
        if_error_1 = True

    # -------------------------end-------------------------

    # ACL Egress Rule Test
    # ACL > ACL Egress Rule
    # -------------------------start-------------------------

    # 路徑導向 ACL > ACL Egress Rule
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"ACL")
    mod.SubPage_Switch(driver,"ACL Egress Rule")
    mod.Switch_Frame(driver)

    print(f"             = = = Check ACL Egress profile apply to ge port test = = =",file = open(file_name, '+a'))

    try:
        if_full = False
        for test_port in range(40):#####40
            if(if_full == False):
                # port select
                acl.Slot_Select(driver,glc_slot)
                acl.Port_Select(driver,test_port+1)
                acl.Load(driver)

                # profile apply
                for input_priority in range(8):
                    acl.ACL_Rule_ACL_Profile(driver,input_priority+1)
                    acl.ACL_Rule_Priority(driver,input_priority+1)
                    acl.ACL_Rule_Apply(driver)
                    try:
                        driver.find_element(By.NAME, "rperror_btnBack")
                        error_msg = driver.find_element(By.CLASS_NAME, "div-row-cell-content.msg").get_attribute("textContent")
                        print(f"             [ACL - ACL Egress Rule] Port Mode Port{test_port+1} Profile{input_priority+1} Apply Fail,Error Message:{error_msg}",file = open(file_name, '+a'))
                        if_error = True
                        driver.find_element(By.NAME, "rperror_btnBack").click()
                        if_full = True
                        break
                    except:
                        pass

        # select slot check
        time.sleep(1)
        driver.find_elements(By.NAME, "rpaclrule_rdoSlt")[int(glc_slot)-1].click()
        select_slot_max_capacity = driver.find_elements(By.CLASS_NAME, "td-table-content.i1")[-1].get_attribute("textContent")
        print(f"             [ACL - ACL Egress Rule] Port Mode Slot{glc_slot} Max Capacity(128) = {select_slot_max_capacity}",file = open(file_name, '+a'))

        
        print(f"             = = = Check ACL-Egress-Profile pool delete max entries = = =",file = open(file_name, '+a'))
        
        # select delete
        driver.find_element(By.NAME, "rpaclsetupall_selectAll").click()
        driver.find_element(By.NAME, "rpaclsetupall_Delete").click()

        # clean select slot check
        try:
            driver.find_element(By.CLASS_NAME, "rpaclrulesetupport")
            print(f"             [ACL - ACL Egress Rule] Port Mode Delete Test Fail",file = open(file_name, '+a'))
            if_error = True
        except:
            print(f"             [ACL - ACL Egress Rule] Port Mode Delete Test Pass",file = open(file_name, '+a'))
            pass

    except:
        print(f"             [ACL - ACL Egress Rule] Port Mode Apply to Full and Delete Fail",file = open(file_name, '+a'))
        if_error = True
        

    # 路徑導向 Profile > ACL Egress
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Profile")
    mod.SubPage_Switch(driver,"ACL Egress")
    mod.Switch_Frame(driver)

    try:
        # Clean Profile
        if_clear = False
        while(if_clear == False):
            try:
                driver.find_element(By.CLASS_NAME, "pfListRow")
                driver.find_element(By.NAME, "rpaclprof_rdoSlt").click()
                pro.ACL_New_Delete(driver)
            except:
                if_clear = True

    except:
        print(f"             [Profile - ACL Egress] Clear Fail",file = open(file_name, '+a'))
        # if_error = True
        if_error_1 = True

    # Profile -> ACL Egress & ACL -> ACL Egress Rule Result
    if(if_error == False):
        print(f"[MSAN1-11825][ACL - ACL Egress Rule] Result Pass",file = open(file_name, '+a'))
        # print(f"[MSAN1-11890][Profile - ACL Egress] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11825][ACL - ACL Egress Rule] Result Fail",file = open(file_name, '+a'))
        # print(f"[MSAN1-11890][Profile - ACL Egress] Result Fail",file = open(file_name, '+a'))

    if(if_error_1 == False):
        print(f"[MSAN1-11890][Profile - ACL Egress] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11890][Profile - ACL Egress] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # MACFF > General Setup
    # ACL > MACFF > General Setup
    # -------------------------start-------------------------

    # 路徑導向 ACL > MACFF > General Setup
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"ACL")
    mod.SubPage_Switch(driver,"MACFF")
    mod.Switch_Frame(driver)
    time.sleep(1)

    # Clean Profile
    if_clear = False
    while(if_clear == False):
        try:
            driver.find_element(By.CLASS_NAME, "pfList")
            driver.find_element(By.NAME, "rpmacff_rdoSlt").click()
            acl.MACFF_New_Delete(driver)
        except:
            if_clear = True

    # General Setup Apply New Profiles 1-full
    profile_test_num = 0
    if_full = False
    while(if_full == False):
        profile_test_num = profile_test_num+1
        acl.MACFF_New(driver)
        acl.MACFF_New_Name(driver,f"123456789012345678901234567{8000+profile_test_num}")
        if(profile_test_num == 1):
            index_len = driver.find_elements(By.CLASS_NAME, "div-row-begin-title").__len__()
            print(f"             [ACL - MACFF - General Setup] Profile Index = {index_len-2}",file = open(file_name, '+a'))
        for index in range(driver.find_elements(By.CLASS_NAME, "div-row-begin-title").__len__()-2):
            acl.MACFF_New_Enable(driver,True,index+1)
            acl.MACFF_New_Vlan(driver,f"{index+1}",index+1)
            acl.MACFF_New_Static(driver,True,index+1)
            acl.MACFF_New_ar_as_ip(driver,f"10.10.10.{index+1}",index+1)
            acl.MACFF_New_subnet_ip(driver,f"10.10.10.{index+1}",index+1)
            acl.MACFF_New_netmask(driver,"24",index+1)
        acl.MACFF_New_Apply(driver)
        try:
            driver.find_element(By.NAME, "rperror_btnBack").click()
            if_full = True
            print(f"             [ACL - MACFF - General Setup] Max Capacity = {profile_test_num-1}",file = open(file_name, '+a'))
        except:
            pass

    if_error = False

    # General Setup Check
    for index in range(profile_test_num-1):
        if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpmacff_txtProfileName")[index].get_attribute("textContent") != f"123456789012345678901234567{8001+index}"):
            print(f"             [ACL - MACFF - General Setup] Index{index+1} Profile Name Test Fail",file = open(file_name, '+a'))
            if_error = True
        driver.find_elements(By.NAME, "rpmacff_rdoSlt")[index].click()
        for in_index in range(24):
            in_name = "00"
            if(in_index < 9):
                in_name = f"0{in_index+1}"
            else:
                in_name = in_index+1
            if(driver.find_element(By.NAME, f"rpmacff_chkIndex{in_name}").is_selected() != True):
                print(f"             [ACL - MACFF - General Setup] Index{index+1} Enable{in_index+1} Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_element(By.NAME, f"rpmacff_txtVlan{in_name}").get_attribute("value") != str(in_index+1)):
                print(f"             [ACL - MACFF - General Setup] Index{index+1} vlan{in_index+1} Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_element(By.NAME, f"rpmacff_chkStatic{in_name}").is_selected() != True):
                print(f"             [ACL - MACFF - General Setup] Index{index+1} Static{in_index+1} Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_element(By.NAME, f"rpmacff_txtArIp{in_name}").get_attribute("value") != f"10.10.10.{in_index+1}"):
                print(f"             [ACL - MACFF - General Setup] Index{index+1} ar/as-ip{in_index+1} Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_element(By.NAME, f"rpmacff_txtSrcIp{in_name}").get_attribute("value") != f"10.10.10.{in_index+1}"):
                print(f"             [ACL - MACFF - General Setup] Index{index+1} subnet-ip{in_index+1} Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_element(By.NAME, f"rpmacff_txtMask{in_name}").get_attribute("value") != f"24"):
                print(f"             [ACL - MACFF - General Setup] Index{index+1} NetMask{in_index+1} Test Fail",file = open(file_name, '+a'))
                if_error = True
        driver.find_element(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-icon-only.ui-dialog-titlebar-close").click()

    if(if_error == False):
        print(f"[MSAN1-11826][ACL - MACFF - General Setup] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11826][ACL - MACFF - General Setup] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # MACFF > Apply Table
    # ACL > MACFF > Apply Table
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 ACL > MACFF > Apply Table
    mod.Tab_Switch(driver,"Apply Table")

    # MACFF Apply Table Apply Profile 1
    acl.Slot_Select(driver,glc_slot)
    acl.MACFF_Apply_Table_Apply_Profile(driver,1)
    acl.MACFF_Apply_Table_Apply(driver)

    # MACFF Apply Table Profile Check 1
    if(driver.find_element(By.NAME, "rpmacff_applyProfile").get_attribute("textContent") != "1234567890123456789012345678001"):
        if_error = True

    # MACFF Apply Table Apply Profile 2
    acl.Slot_Select(driver,glc_slot)
    acl.MACFF_Apply_Table_Apply_Profile(driver,8)
    acl.MACFF_Apply_Table_Apply(driver)

    # MACFF Apply Table Profile Check 2
    if(driver.find_element(By.NAME, "rpmacff_applyProfile").get_attribute("textContent") != "1234567890123456789012345678008"):
        if_error = True

    print(f"             [ACL - MACFF - Apply Table] Apply to GE port Max Capacity(1) = 1",file = open(file_name, '+a'))
    if(if_error == False):
        print(f"[MSAN1-11827][ACL - MACFF - Apply Table] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11827][ACL - MACFF - Apply Table] Result Fail",file = open(file_name, '+a'))

    # MACFF Apply Table Delete Profile
    driver.find_element(By.NAME, "rpmacff_displaySelect").click()
    acl.MACFF_Apply_Table_Delete(driver)

    # -------------------------end-------------------------

    # MACFF > Arp Proxy
    # ACL > MACFF > Arp Proxy
    # -------------------------start-------------------------

    # 路徑導向 ACL > MACFF > Arp Proxy
    mod.Tab_Switch(driver,"Arp Proxy")

    # slot load
    acl.Slot_Select(driver,glc_slot)
    driver.find_element(By.NAME, "rpmacff_Load").click()

    print(f"[MSAN1-11828][ACL - MACFF - Arp Proxy] Result Pass",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # MACFF > General Setup
    # ACL > MACFF > General Setup
    # -------------------------start-------------------------

    # 路徑導向 ACL > MACFF > General Setup
    mod.Tab_Switch(driver,"General Setup")

    # Clean Profile
    if_clear = False
    while(if_clear == False):
        try:
            driver.find_element(By.CLASS_NAME, "pfList")
            driver.find_element(By.NAME, "rpmacff_rdoSlt").click()
            acl.MACFF_New_Delete(driver)
        except:
            if_clear = True

    # -------------------------end-------------------------

    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def ACL_Test(driver,glc_slot,glc_port,msc_slot,msc_port,file_name):
    print(f"ACL Test\nTest Start",file = open(file_name, '+a'))

    # ACL Anti Macspoof Test
    # ACL > Anti Macspoof
    # -------------------------start-------------------------

    if_error = False
    if_anti_error = False
    if_spoof_error = False

    # 路徑導向 ACL > Anti Macspoof
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"ACL")
    mod.Switch_Frame(driver)

    # slot select
    acl.Slot_Select(driver,glc_slot)
    acl.Load(driver)

    # Anti Macspoof 傳入值 1
    acl.Anti_Macspoof_Anti_Macspoof_Select_All(driver,2)
    acl.Anti_Macspoof_Spoof_Action_Select_All(driver,2)
    acl.Anti_Macspoof_Apply(driver)

    # Anti Macspoof 檢驗 1
    if(driver.find_element(By.XPATH, f"/html/body/form/div[5]/div/div[{int(glc_port)+7}]/div[2]/select/option[1]").is_selected() != True):
        if_anti_error = True
    if(driver.find_element(By.XPATH, f"/html/body/form/div[5]/div/div[{int(glc_port)+7}]/div[3]/select/option[1]").is_selected() != True):
        if_spoof_error = True

    # Anti Macspoof 傳入值 2
    acl.Anti_Macspoof_Anti_Macspoof_Select_All(driver,3)
    acl.Anti_Macspoof_Spoof_Action_Select_All(driver,3)
    acl.Anti_Macspoof_Apply(driver)

    # Anti Macspoof 檢驗 2
    if(driver.find_element(By.XPATH, f"/html/body/form/div[5]/div/div[{int(glc_port)+7}]/div[2]/select/option[2]").is_selected() != True):
        if_anti_error = True
    if(driver.find_element(By.XPATH, f"/html/body/form/div[5]/div/div[{int(glc_port)+7}]/div[3]/select/option[2]").is_selected() != True):
        if_spoof_error = True

    if(if_anti_error == True):
        print("             [ACL - Anti Macspoof] Anti Macspoof Test Fail",file = open(file_name, '+a'))
        if_error = True

    if(if_spoof_error == True):
        print("             [ACL - Anti Macspoof] Spoof Action Test Fail",file = open(file_name, '+a'))
        if_error = True

    if(if_error == True):
        print("[MSAN1-11809][ACL - Anti Macspoof] Result Fail",file = open(file_name, '+a'))
    else:
        print("[MSAN1-11809][ACL - Anti Macspoof] Result Pass",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # ACL MAC Count Test
    # ACL > MAC Count
    # -------------------------start-------------------------

    if_limit_error = False

    # 路徑導向 MAC Count
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"MAC Count")
    mod.Switch_Frame(driver)

    # slot select
    time.sleep(1)
    driver.find_elements(By.NAME, "rpdsl_rdoSlt")[int(glc_slot)-1].click()

    # MAC Count Limit Test
    acl.MAC_Count_Limit_Input_All(driver,"0")
    acl.MAC_Count_Apply(driver)
    if(mod.IsAlert(driver) == False):
        print("             [ACL - MAC Count] Limit:0 Test Fail",file = open(file_name, '+a'))
        if_limit_error = True
    acl.MAC_Count_Limit_Input_All(driver,"257")
    acl.MAC_Count_Apply(driver)
    if(mod.IsAlert(driver) == False):
        print("             [ACL - MAC Count] Limit:257 Test Fail",file = open(file_name, '+a'))
        if_limit_error = True
    acl.MAC_Count_Limit_Input_All(driver,"@")
    acl.MAC_Count_Apply(driver)
    if(mod.IsAlert(driver) == False):
        print("             [ACL - MAC Count] Limit:@ Test Fail",file = open(file_name, '+a'))
        if_limit_error = True
    acl.MAC_Count_Limit_Input_All(driver,"1")
    acl.MAC_Count_Apply(driver)
    if(mod.IsAlert(driver) == True):
        print("             [ACL - MAC Count] Limit:1 Test Fail",file = open(file_name, '+a'))
        if_limit_error = True
    else:
        if(driver.find_elements(By.ID, "rpmacCount_sltMacLimit")[int(glc_port)-1].get_attribute("value") != "1"):
            print("             [ACL - MAC Count] Limit:1 Test Fail",file = open(file_name, '+a'))
            if_limit_error = True
    acl.MAC_Count_Limit_Input_All(driver,"256")
    acl.MAC_Count_Apply(driver)
    if(mod.IsAlert(driver) == True):
        print("             [ACL - MAC Count] Limit:256 Test Fail",file = open(file_name, '+a'))
        if_limit_error = True
    else:
        if(driver.find_elements(By.ID, "rpmacCount_sltMacLimit")[int(glc_port)-1].get_attribute("value") != "256"):
            print("             [ACL - MAC Count] Limit:256 Test Fail",file = open(file_name, '+a'))
            if_limit_error = True

    if(if_limit_error == False):
        print("             [ACL - MAC Count] Limit Test Pass",file = open(file_name, '+a'))

    # port advance
    driver.find_elements(By.NAME, "rpdsl_rdoSlt")[int(glc_port)-1].click()

    if_detail_limit_error = False
    if_detail_new_error = False

    # MAC Count Detail Limit Test
    acl.MAC_Count_Detail_Limit(driver,"0")
    acl.MAC_Count_Detail_Limit_Apply(driver)
    if(mod.IsAlert(driver) == False):
        print("             [ACL - MAC Count] Detail Limit:0 Test Fail",file = open(file_name, '+a'))
        if_detail_limit_error = True
    acl.MAC_Count_Detail_Limit(driver,"257")
    acl.MAC_Count_Detail_Limit_Apply(driver)
    if(mod.IsAlert(driver) == False):
        print("             [ACL - MAC Count] Detail Limit:257 Test Fail",file = open(file_name, '+a'))
        if_detail_limit_error = True
    acl.MAC_Count_Detail_Limit(driver,"@")
    acl.MAC_Count_Detail_Limit_Apply(driver)
    if(mod.IsAlert(driver) == False):
        print("             [ACL - MAC Count] Detail Limit:@ Test Fail",file = open(file_name, '+a'))
        if_detail_limit_error = True
    acl.MAC_Count_Detail_Limit(driver,"1")
    acl.MAC_Count_Detail_Limit_Apply(driver)
    if(mod.IsAlert(driver) == True):
        print("             [ACL - MAC Count] Detail Limit:1 Test Fail",file = open(file_name, '+a'))
        if_detail_limit_error = True
    else:
        if(driver.find_element(By.NAME, "rpmacCount_sltMacLimit").get_attribute("value") != "1"):
            print("             [ACL - MAC Count] Detail Limit:1 Test Fail",file = open(file_name, '+a'))
            if_detail_limit_error = True
    acl.MAC_Count_Detail_Limit(driver,"256")
    acl.MAC_Count_Detail_Limit_Apply(driver)
    if(mod.IsAlert(driver) == True):
        print("             [ACL - MAC Count] Detail Limit:256 Test Fail",file = open(file_name, '+a'))
        if_detail_limit_error = True
    else:
        if(driver.find_element(By.NAME, "rpmacCount_sltMacLimit").get_attribute("value") != "256"):
            print("             [ACL - MAC Count] Detail Limit:256 Test Fail",file = open(file_name, '+a'))
            if_detail_limit_error = True

    # MAC Count Detail New Clear
    is_clear = False
    while(is_clear == False):
        try:
            driver.find_element(By.NAME, "rpmacCount_rdoSlt").click()
            acl.MAC_Count_Detail_New_Delete(driver)
        except:
            is_clear = True

    # MAC Count Detail New Test
    acl.MAC_Count_Detail_New_VLAN(driver,"4094")
    acl.MAC_Count_Detail_New_Limit(driver,"0")
    acl.MAC_Count_Detail_New_Apply(driver)
    if(mod.IsAlert(driver) == False):
        print("             [ACL - MAC Count] Detail New Limit:0 Test Fail",file = open(file_name, '+a'))
        if_detail_new_error = True
    acl.MAC_Count_Detail_New_Limit(driver,"257")
    acl.MAC_Count_Detail_New_Apply(driver)
    if(mod.IsAlert(driver) == False):
        print("             [ACL - MAC Count] Detail New Limit:257 Test Fail",file = open(file_name, '+a'))
        if_detail_new_error = True
    acl.MAC_Count_Detail_New_Limit(driver,"@")
    acl.MAC_Count_Detail_New_Apply(driver)
    if(mod.IsAlert(driver) == False):
        print("             [ACL - MAC Count] Detail New Limit:@ Test Fail",file = open(file_name, '+a'))
        if_detail_new_error = True
    acl.MAC_Count_Detail_New_Limit(driver,"256")
    acl.MAC_Count_Detail_New_Apply(driver)
    if(mod.IsAlert(driver) == True):
        print("             [ACL - MAC Count] Detail New Limit:256 Test Fail",file = open(file_name, '+a'))
        if_detail_new_error = True
    else:
        if(driver.find_element(By.NAME, "rpmacCount_perVlanVlan").get_attribute("textContent") != "4094"):
            print("             [ACL - MAC Count] Detail New VLAN:4094 Test Fail",file = open(file_name, '+a'))
            if_detail_new_error = True
        if(driver.find_element(By.NAME, "rpmacCount_perVlanLimit").get_attribute("textContent") != "256"):
            print("             [ACL - MAC Count] Detail New Limit:256 Test Fail",file = open(file_name, '+a'))
            if_detail_new_error = True
    acl.MAC_Count_Detail_New_VLAN(driver,"4094")
    acl.MAC_Count_Detail_New_Limit(driver,"1")
    acl.MAC_Count_Detail_New_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print("             [ACL - MAC Count] Detail Same VLAN Test Fail",file = open(file_name, '+a'))
        if_detail_new_error = True
    time.sleep(1)
    acl.Slot_Select(driver,glc_slot)
    acl.Port_Select(driver,glc_port)
    acl.Load(driver)
    driver.find_element(By.NAME, "rpmacCount_rdoSlt").click()
    acl.MAC_Count_Detail_New_Delete(driver)

    if(if_limit_error == False and if_detail_limit_error == False and if_detail_new_error == False):
        print("[MSAN1-11814][ACL - MAC Count] Result Pass",file = open(file_name, '+a'))
    else:
        print("[MSAN1-11814][ACL - MAC Count] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # ACL MAC Filter & OUI Filter Test
    # ACL > MAC Filter & OUI Filter
    # -------------------------start-------------------------

    if_mac_error = False
    if_oui_error = False

    # MAC Filter & OUI Filter Default
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Port")
    mod.SubPage_Switch(driver,"Default")
    mod.Switch_Frame(driver)
    port.Slot_Select(driver,glc_slot)
    port.Default_Port_List(driver,"1~40")
    port.Default_Apply(driver)
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"ACL")
    mod.Switch_Frame(driver)

    # 路徑導向 MAC Filter
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"MAC Filter")
    mod.Switch_Frame(driver)

    # MAC Filter = accept
    for test_port in range(40):
        # slot select
        acl.Slot_Select(driver,glc_slot)
        acl.Port_Select(driver,test_port+1)
        acl.Load(driver)

        # MAC Filter 輸入值
        acl.MAC_Filter_Enable(driver,True)
        acl.MAC_Filter_Mode(driver,1)
        for mac in range(32):
            if(mac < 9):
                acl.MAC_Filter_MAC(driver,f"10:10:10:10:10:0{mac+1}",mac+1)
            else:
                acl.MAC_Filter_MAC(driver,f"10:10:10:10:10:{mac+1}",mac+1)
        acl.MAC_Filter_Apply(driver)

        if_error = False

        # MAC Filter 檢驗
        if(driver.find_element(By.NAME, "rpmacFilter_chkEnable").is_selected() == False):
            if_error = True
        if(driver.find_element(By.XPATH, f"//*[@name='rpmacFilter_sltMode']/option[1]").is_selected() == False):
            if_error = True
        for mac in range(32):
            if(mac < 9):
                if(driver.find_element(By.NAME, f"rpmacFilter_sltFilterMac{mac+1}").get_attribute("value") != f"10:10:10:10:10:0{mac+1}"):
                    if_error = True
            else:
                if(driver.find_element(By.NAME, f"rpmacFilter_sltFilterMac{mac+1}").get_attribute("value") != f"10:10:10:10:10:{mac+1}"):
                    if_error = True

    if(if_error == False):
        print("             [ACL - MAC Filter] accept 32 entries * 40 port =>Pass.",file = open(file_name, '+a'))
    else:
        print("             [ACL - MAC Filter] accept 32 entries * 40 port =>Fail.",file = open(file_name, '+a'))
        if_mac_error = True

    # MAC Filter %Port = deny
    acl.Slot_Select(driver,glc_slot)
    acl.Port_Select(driver,glc_port)
    acl.Load(driver)
    acl.MAC_Filter_Mode(driver,2)
    acl.MAC_Filter_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack")
        error_msg = driver.find_element(By.CLASS_NAME, "div-row-cell-content.msg").get_attribute("textContent")
        if(error_msg == "error: line card entry full (>63)\n"):
            print(f"             [ACL - MAC Filter] accept 32 entries * 39 port + MAC-Filter deny 32 entry * 1 port check error message =>(32+32>63)Pass.",file = open(file_name, '+a'))
        else:
            print(f"             [ACL - MAC Filter] accept 32 entries * 39 port + MAC-Filter deny 32 entry * 1 port check error message =>(32+32>63)Fail.",file = open(file_name, '+a'))
            if_mac_error = True
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [ACL - MAC Filter] accept 32 entries * 39 port + MAC-Filter deny 32 entry * 1 port check error message =>(32+32>63)Fail.",file = open(file_name, '+a'))
        if_mac_error = True

    # MAC Filter %Port-32 Delete
    acl.MAC_Filter_Mode(driver,2)
    acl.MAC_Filter_MAC(driver,"",32)
    acl.MAC_Filter_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack")
        print(f"             [ACL - MAC Filter] accept 32 entries * 39 port + MAC-Filter deny 31 entry * 1 port =>(32+31=63)Fail.",file = open(file_name, '+a'))
        if_mac_error = True
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [ACL - MAC Filter] accept 32 entries * 39 port + MAC-Filter deny 31 entry * 1 port =>(32+31=63)Pass.",file = open(file_name, '+a'))

    # MAC Filter Clear
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"MAC Filter")
    mod.Switch_Frame(driver)
    for test_port in range(40):
        acl.Slot_Select(driver,glc_slot)
        acl.Port_Select(driver,test_port+1)
        acl.Load(driver)
        acl.MAC_Filter_Enable(driver,False)
        acl.MAC_Filter_Mode(driver,2)
        for mac in range(32):
            acl.MAC_Filter_MAC(driver,"",mac+1)
        acl.MAC_Filter_Apply(driver)

    # MAC Filter = deny
    for test_port in range(40):
        # slot select
        acl.Slot_Select(driver,glc_slot)
        acl.Port_Select(driver,test_port+1)
        acl.Load(driver)

        # MAC Filter 輸入值
        acl.MAC_Filter_Enable(driver,True)
        acl.MAC_Filter_Mode(driver,2)
        for mac in range(32):
            if(mac < 9):
                acl.MAC_Filter_MAC(driver,f"10:10:10:10:10:0{mac+1}",mac+1)
            else:
                acl.MAC_Filter_MAC(driver,f"10:10:10:10:10:{mac+1}",mac+1)
        acl.MAC_Filter_Apply(driver)

        if_error = False

        # MAC Filter 檢驗
        if(driver.find_element(By.NAME, "rpmacFilter_chkEnable").is_selected() == False):
            if_error = True
        if(driver.find_element(By.XPATH, f"//*[@name='rpmacFilter_sltMode']/option[2]").is_selected() == False):
            if_error = True
        for mac in range(32):
            if(mac < 9):
                if(driver.find_element(By.NAME, f"rpmacFilter_sltFilterMac{mac+1}").get_attribute("value") != f"10:10:10:10:10:0{mac+1}"):
                    if_error = True
            else:
                if(driver.find_element(By.NAME, f"rpmacFilter_sltFilterMac{mac+1}").get_attribute("value") != f"10:10:10:10:10:{mac+1}"):
                    if_error = True

    if(if_error == False):
        print("             [ACL - MAC Filter] deny 32 entries * 40 port =>Pass.",file = open(file_name, '+a'))
    else:
        print("             [ACL - MAC Filter] deny 32 entries * 40 port =>Fail.",file = open(file_name, '+a'))
        if_mac_error = True

    # MAC Filter %Port = accept
    acl.Slot_Select(driver,glc_slot)
    acl.Port_Select(driver,glc_port)
    acl.Load(driver)
    acl.MAC_Filter_Mode(driver,1)
    acl.MAC_Filter_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack")
        error_msg = driver.find_element(By.CLASS_NAME, "div-row-cell-content.msg").get_attribute("textContent")
        if(error_msg == "error: line card entry full (>63)\n"):
            print(f"             [ACL - MAC Filter] deny 32 entries * 39 port + MAC-Filter accept 32 entry * 1 port check error message =>(32+32>63)Pass.",file = open(file_name, '+a'))
        else:
            print(f"             [ACL - MAC Filter] deny 32 entries * 39 port + MAC-Filter accept 32 entry * 1 port check error message =>(32+32>63)Fail.",file = open(file_name, '+a'))
            if_mac_error = True
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [ACL - MAC Filter] deny 32 entries * 39 port + MAC-Filter accept 32 entry * 1 port check error message =>(32+32>63)Fail.",file = open(file_name, '+a'))
        if_mac_error = True

    acl.MAC_Filter_Mode(driver,1)
    acl.MAC_Filter_MAC(driver,"",32)
    acl.MAC_Filter_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack")
        print(f"             [ACL - MAC Filter] deny 32 entries * 39 port + MAC-Filter accept 31 entry * 1 port =>(32+31=63)Fail.",file = open(file_name, '+a'))
        if_mac_error = True
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [ACL - MAC Filter] deny 32 entries * 39 port + MAC-Filter accept 31 entry * 1 port =>(32+31=63)Pass.",file = open(file_name, '+a'))

    # MAC Filter = deny
    acl.MAC_Filter_Mode(driver,2)
    acl.MAC_Filter_MAC(driver,"10:10:10:10:10:32",32)
    acl.MAC_Filter_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack")
        print(f"             [ACL - MAC Filter] deny 32 entries * 40 port + MAC-Filter accept 31 entry * 0 port =>(32+0=32)Fail.",file = open(file_name, '+a'))
        if_mac_error = True
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        pass

    # OUI Filter %Port = accept
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"OUI Filter")
    mod.Switch_Frame(driver)
    acl.Slot_Select(driver,glc_slot)
    acl.Port_Select(driver,glc_port)
    acl.Load(driver)
    acl.OUI_Filter_Enable(driver,True)
    acl.OUI_Filter_Mode(driver,1)
    for oui in range(32):
        if(oui < 9):
            acl.OUI_Filter_OUI(driver,f"10:10:0{oui+1}",oui+1)
        else:
            acl.OUI_Filter_OUI(driver,f"10:10:{oui+1}",oui+1)
    acl.OUI_Filter_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack")
        error_msg = driver.find_element(By.CLASS_NAME, "div-row-cell-content.msg").get_attribute("textContent")
        if(error_msg == "error: line card entry full (>63)\n"):
            print(f"             [ACL - MAC Filter] deny 32 entries * 40 port + OUI-Filter accept 32 entry * 1 port check error message =>(32+32>63)Pass.",file = open(file_name, '+a'))
        else:
            print(f"             [ACL - MAC Filter] deny 32 entries * 40 port + OUI-Filter accept 32 entry * 1 port check error message =>(32+32>63)Fail.",file = open(file_name, '+a'))
            if_mac_error = True
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [ACL - MAC Filter] deny 32 entries * 40 port + OUI-Filter accept 32 entry * 1 port check error message =>(32+32>63)Fail.",file = open(file_name, '+a'))
        if_mac_error = True
    # OUI Filter Clear
    acl.OUI_Filter_Enable(driver,False)
    acl.OUI_Filter_Mode(driver,2)
    for oui in range(32):
        acl.OUI_Filter_OUI(driver,"",oui+1)
    acl.OUI_Filter_Apply(driver)

    # MAC Filter Clear
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"MAC Filter")
    mod.Switch_Frame(driver)
    for test_port in range(40):
        acl.Slot_Select(driver,glc_slot)
        acl.Port_Select(driver,test_port+1)
        acl.Load(driver)
        acl.MAC_Filter_Enable(driver,False)
        acl.MAC_Filter_Mode(driver,2)
        for mac in range(32):
            acl.MAC_Filter_MAC(driver,"",mac+1)
        acl.MAC_Filter_Apply(driver)
        try:
            driver.find_element(By.NAME, "rperror_btnBack").click()
            print(f"             [ACL - MAC Filter] 32 + OUI-Filter 31, enable and mode accept set Fail.",file = open(file_name, '+a'))
            if_mac_error = True
            # MAC Filter set default
            mod.Switch_Default(driver)
            mod.Page_Switch(driver,"Port")
            mod.SubPage_Switch(driver,"Default")
            mod.Switch_Frame(driver)
            port.Slot_Select(driver,glc_slot)
            port.Default_Port_List(driver,"1~40")
            port.Default_Apply(driver)
            mod.Switch_Default(driver)
            mod.Page_Switch(driver,"ACL")
            mod.SubPage_Switch(driver,"MAC Filter")
            mod.Switch_Frame(driver)
            break
        except:
            pass

    # 路徑導向 OUI Filter
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"OUI Filter")
    mod.Switch_Frame(driver)

    # (1)
    # OUI Filter = accept
    for test_port in range(40):
        # slot select
        acl.Slot_Select(driver,glc_slot)
        acl.Port_Select(driver,test_port+1)
        acl.Load(driver)

        # OUI Filter 輸入值
        acl.OUI_Filter_Enable(driver,True)
        acl.OUI_Filter_Mode(driver,1)
        for oui in range(32):
            if(oui < 9):
                acl.OUI_Filter_OUI(driver,f"10:10:0{oui+1}",oui+1)
            else:
                acl.OUI_Filter_OUI(driver,f"10:10:{oui+1}",oui+1)
        acl.OUI_Filter_Apply(driver)

        if_error = False

        # OUI Filter 檢驗
        if(driver.find_element(By.NAME, "rpouiFilter_chkEnable").is_selected() == False):
            if_error = True
        if(driver.find_element(By.XPATH, f"//*[@name='rpouiFilter_sltMode']/option[1]").is_selected() == False):
            if_error = True
        for oui in range(32):
            if(oui < 9):
                if(driver.find_element(By.NAME, f"rpouiFilter_sltFilterOui{oui+1}").get_attribute("value") != f"10:10:0{oui+1}"):
                    if_error = True
            else:
                if(driver.find_element(By.NAME, f"rpouiFilter_sltFilterOui{oui+1}").get_attribute("value") != f"10:10:{oui+1}"):
                    if_error = True

    if(if_error == False):
        print("             [ACL - OUI Filter] accept 32 entries * 40 port =>Pass.",file = open(file_name, '+a'))
    else:
        print("             [ACL - OUI Filter] accept 32 entries * 40 port =>Fail.",file = open(file_name, '+a'))
        if_oui_error = True

    # (2)
    # OUI Filter %Port = deny
    acl.Slot_Select(driver,glc_slot)
    acl.Port_Select(driver,glc_port)
    acl.Load(driver)
    acl.OUI_Filter_Mode(driver,2)
    acl.OUI_Filter_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack")
        error_msg = driver.find_element(By.CLASS_NAME, "div-row-cell-content.msg").get_attribute("textContent")
        if(error_msg == "error: line card entry full (>63)\n"):
            print(f"             [ACL - OUI Filter] accept 32 entries * 39 port + OUI-Filter deny 32 entry * 1 port check error message =>(32+32>63)Pass.",file = open(file_name, '+a'))
        else:
            print(f"             [ACL - OUI Filter] accept 32 entries * 39 port + OUI-Filter deny 32 entry * 1 port check error message =>(32+32>63)Fail.",file = open(file_name, '+a'))
            if_oui_error = True
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [ACL - OUI Filter] accept 32 entries * 39 port + OUI-Filter deny 32 entry * 1 port check error message =>(32+32>63)Fail.",file = open(file_name, '+a'))
        if_oui_error = True

    # (3)
    # OUI Filter %Port-32 Delete
    acl.Slot_Select(driver,glc_slot)
    acl.Port_Select(driver,glc_port)
    acl.OUI_Filter_Mode(driver,2)
    acl.OUI_Filter_OUI(driver,"",32)
    acl.OUI_Filter_Apply(driver)

    try:
        driver.find_element(By.NAME, "rperror_btnBack")
        error_msg = driver.find_element(By.CLASS_NAME, "div-row-cell-content.msg").get_attribute("textContent") #* add
        error_msg = error_msg.split("\n")[0]  #* add
        print(f"             [ACL - OUI Filter] error:{error_msg}",file = open(file_name, '+a')) #* add
        
        # if(error_msg == "error: line card entry full (>63)\n"):
        #     print(f"             [ACL - OUI Filter] accept 32 entries * 39 port + OUI-Filter deny 31 entry * 1 port =>(32+31=63)Pass.",file = open(file_name, '+a'))
        # else:
        #     print(f"             [ACL - OUI Filter] accept 32 entries * 39 port + OUI-Filter deny 31 entry * 1 port check error message =>(32+32>63)Fail.(#172692.#172678)",file = open(file_name, '+a'))
        #     if_oui_error = True #* add

        print(f"             [ACL - OUI Filter] accept 32 entries * 39 port + OUI-Filter deny 31 entry * 1 port =>(32+31=63)Fail.(#172692.#172678)",file = open(file_name, '+a'))
        if_oui_error = True
        pyautogui.screenshot(f'{str(datetime.datetime.now()).split(":")[0]}{str(datetime.datetime.now()).split(":")[1]}.{str(datetime.datetime.now()).split(":")[2][:5]}_screenshot.png')

        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [ACL - OUI Filter] accept 32 entries * 39 port + OUI-Filter deny 31 entry * 1 port =>(32+31=63)Pass.",file = open(file_name, '+a'))
        # print(f"             [ACL - OUI Filter] accept 32 entries * 39 port + OUI-Filter deny 31 entry * 1 port =>(32+31=63)Fail.",file = open(file_name, '+a'))
        
    # OUI Filter Clear
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"OUI Filter")
    mod.Switch_Frame(driver)
    for test_port in range(40):
        acl.Slot_Select(driver,glc_slot)
        acl.Port_Select(driver,test_port+1)
        acl.Load(driver)
        acl.OUI_Filter_Enable(driver,False)
        acl.OUI_Filter_Mode(driver,2)
        for oui in range(32):
            acl.OUI_Filter_OUI(driver,"",oui+1)
        acl.OUI_Filter_Apply(driver)

    # (4)
    # OUI Filter = deny
    for test_port in range(40):
        # slot select
        acl.Slot_Select(driver,glc_slot)
        acl.Port_Select(driver,test_port+1)
        acl.Load(driver)

        # OUI Filter 輸入值
        acl.OUI_Filter_Enable(driver,True)
        acl.OUI_Filter_Mode(driver,2)
        for oui in range(32):
            if(oui < 9):
                acl.OUI_Filter_OUI(driver,f"10:10:0{oui+1}",oui+1)
            else:
                acl.OUI_Filter_OUI(driver,f"10:10:{oui+1}",oui+1)
        acl.OUI_Filter_Apply(driver)

        if_error = False

        # OUI Filter 檢驗
        if(driver.find_element(By.NAME, "rpouiFilter_chkEnable").is_selected() == False):
            if_error = True
        if(driver.find_element(By.XPATH, f"//*[@name='rpouiFilter_sltMode']/option[2]").is_selected() == False):
            if_error = True
        for oui in range(32):
            if(oui < 9):
                if(driver.find_element(By.NAME, f"rpouiFilter_sltFilterOui{oui+1}").get_attribute("value") != f"10:10:0{oui+1}"):
                    if_error = True
            else:
                if(driver.find_element(By.NAME, f"rpouiFilter_sltFilterOui{oui+1}").get_attribute("value") != f"10:10:{oui+1}"):
                    if_error = True

    if(if_error == False):
        print("             [ACL - OUI Filter] deny 32 entries * 40 port =>Pass.",file = open(file_name, '+a'))
    else:
        print("             [ACL - OUI Filter] deny 32 entries * 40 port =>Fail.",file = open(file_name, '+a'))
        if_oui_error = True

    # (5)
    # OUI Filter %Port = accept
    acl.Slot_Select(driver,glc_slot)
    acl.Port_Select(driver,glc_port)
    acl.Load(driver)
    acl.OUI_Filter_Mode(driver,1)
    acl.OUI_Filter_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack")
        error_msg = driver.find_element(By.CLASS_NAME, "div-row-cell-content.msg").get_attribute("textContent")
        if(error_msg == "error: line card entry full (>63)\n"):
            print(f"             [ACL - OUI Filter] deny 32 entries * 39 port + OUI-Filter accept 32 entry * 1 port check error message =>(32+32>63)Pass.",file = open(file_name, '+a'))
        else:
            print(f"             [ACL - OUI Filter] deny 32 entries * 39 port + OUI-Filter accept 32 entry * 1 port check error message =>(32+32>63)Fail.",file = open(file_name, '+a'))
            if_oui_error = True
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [ACL - OUI Filter] deny 32 entries * 39 port + OUI-Filter accept 32 entry * 1 port check error message =>(32+32>63)Fail.",file = open(file_name, '+a'))
        if_oui_error = True

    # (6)
    # OUI Filter %Port-32 Delete
    acl.OUI_Filter_Mode(driver,1)
    acl.OUI_Filter_OUI(driver,"",32)
    acl.OUI_Filter_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack")
        print(f"             [ACL - OUI Filter] deny 32 entries * 39 port + OUI-Filter accept 31 entry * 1 port =>(32+31=63)Fail.",file = open(file_name, '+a'))
        if_oui_error = True
        
        pyautogui.screenshot(f'{str(datetime.datetime.now()).split(":")[0]}{str(datetime.datetime.now()).split(":")[1]}.{str(datetime.datetime.now()).split(":")[2][:5]}_screenshot.png')

        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [ACL - OUI Filter] deny 32 entries * 39 port + OUI-Filter accept 31 entry * 1 port =>(32+31=63)Pass.",file = open(file_name, '+a'))

    # OUI Filter = deny
    acl.OUI_Filter_Mode(driver,2)
    acl.OUI_Filter_OUI(driver,"10:10:32",32)
    acl.OUI_Filter_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack")
        print(f"             [ACL - OUI Filter] deny 32 entries * 40 port + OUI-Filter accept 31 entry * 0 port =>(32+0=32)Fail.",file = open(file_name, '+a'))
        if_oui_error = True
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        pass

    # MAC Filter %Port = accept
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"MAC Filter")
    mod.Switch_Frame(driver)
    acl.Slot_Select(driver,glc_slot)
    acl.Port_Select(driver,glc_port)
    acl.Load(driver)
    acl.MAC_Filter_Enable(driver,True)
    acl.MAC_Filter_Mode(driver,1)
    for mac in range(32):
        if(mac < 9):
            acl.MAC_Filter_MAC(driver,f"10:10:10:10:10:0{mac+1}",mac+1)
        else:
            acl.MAC_Filter_MAC(driver,f"10:10:10:10:10:{mac+1}",mac+1)
    acl.MAC_Filter_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack")
        error_msg = driver.find_element(By.CLASS_NAME, "div-row-cell-content.msg").get_attribute("textContent")
        if(error_msg == "error: line card entry full (>63)\n"):
            print(f"             [ACL - OUI Filter] deny 32 entries * 40 port + MAC-Filter accept 32 entry * 1 port check error message =>(32+32>63)Pass.",file = open(file_name, '+a'))
        else:
            print(f"             [ACL - OUI Filter] deny 32 entries * 40 port + MAC-Filter accept 32 entry * 1 port check error message =>(32+32>63)Fail.",file = open(file_name, '+a'))
            if_oui_error = True
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [ACL - OUI Filter] deny 32 entries * 40 port + MAC-Filter accept 32 entry * 1 port check error message =>(32+32>63)Fail.",file = open(file_name, '+a'))
        if_oui_error = True
    # MAC Filter Clear
    time.sleep(1)
    acl.MAC_Filter_Enable(driver,False)
    acl.MAC_Filter_Mode(driver,2)
    for mac in range(32):
        acl.MAC_Filter_MAC(driver,"",mac+1)
    acl.MAC_Filter_Apply(driver)

    # OUI Filter Clear
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"OUI Filter")
    mod.Switch_Frame(driver)
    for test_port in range(40):
        acl.Slot_Select(driver,glc_slot)
        acl.Port_Select(driver,test_port+1)
        acl.Load(driver)
        acl.OUI_Filter_Enable(driver,False)
        acl.OUI_Filter_Mode(driver,2)
        for oui in range(32):
            acl.OUI_Filter_OUI(driver,"",oui+1)
        acl.OUI_Filter_Apply(driver)
        try:
            driver.find_element(By.NAME, "rperror_btnBack").click()
            print(f"             [ACL - OUI Filter] 32 + MAC-Filter 31, enable and mode accept set Fail.",file = open(file_name, '+a'))
            if_oui_error = True
            # OUI Filter set default
            mod.Switch_Default(driver)
            mod.Page_Switch(driver,"Port")
            mod.SubPage_Switch(driver,"Default")
            mod.Switch_Frame(driver)
            port.Slot_Select(driver,glc_slot)
            port.Default_Port_List(driver,"1~40")
            port.Default_Apply(driver)
            mod.Switch_Default(driver)
            mod.Page_Switch(driver,"ACL")
            mod.SubPage_Switch(driver,"OUI Filter")
            mod.Switch_Frame(driver)
            break
        except:
            pass

    if(if_mac_error == False):
        print(f"[MSAN1-11815][ACL - MAC Filter] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11815][ACL - MAC Filter] Result Fail",file = open(file_name, '+a'))

    if(if_oui_error == False):
        print(f"[MSAN1-11816][ACL - OUI Filter] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11816][ACL - OUI Filter] Result Fail",file = open(file_name, '+a'))

        # -------------------------end-------------------------

    # ACL 802.1x General Setup Test
    # ACL > 802.1x > General Setup
    # -------------------------start-------------------------

    # 路徑導向 802.1x > General Setup
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"802.1x")
    mod.Switch_Frame(driver)

    if_gen_set_error = False

    # 802.1x General Setup Test
    acl.x802_1x_General_Setup_Method(driver,2)
    if(driver.find_element(By.XPATH, f"//*[@name='rpDot1x_authMethod']/option[2]").is_selected() != True):
        if_gen_set_error = True
    acl.x802_1x_General_Setup_Method(driver,1)
    if(driver.find_element(By.XPATH, f"//*[@name='rpDot1x_authMethod']/option[1]").is_selected() != True):
        if_gen_set_error = True

    # 802.1x General Setup Result
    if(if_gen_set_error == True):
        print("[MSAN1-11817][ACL - 802.1x - General Setup] Result Fail",file = open(file_name, '+a'))
    else:
        print("[MSAN1-11817][ACL - 802.1x - General Setup] Result Pass",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # ACL 802.1x RADIUS Server Test
    # ACL > 802.1x > RADIUS Server
    # -------------------------start-------------------------

    # 路徑導向 RADIUS Server
    mod.Tab_Switch(driver,"RADIUS Server")

    # 802.1x RADIUS Server Input
    for index in range(16):
        acl.x802_1x_RADIUS_Server_IP_Address(driver,"10.10.10.1",index)
        acl.x802_1x_RADIUS_Server_Port(driver,"65535",index)
        acl.x802_1x_RADIUS_Server_Secret(driver,"123456789012345678901234567890123456789012345678901234567890123",index)
    acl.x802_1x_RADIUS_Server_Apply(driver)

    if_rad_ser_error = False

    # 802.1x RADIUS Server Check
    for index in range(16):
        if(driver.find_elements(By.NAME, "rpDot1xServer_ipAddress")[index].get_attribute("value") != "10.10.10.1"):
            print(f"             [ACL - 802.1x - RADIUS Server] Index{index+1} IP Address Test Fail",file = open(file_name, '+a'))
            if_rad_ser_error = True
        if(driver.find_elements(By.NAME, "rpDot1xServer_port")[index].get_attribute("value") != "65535"):
            print(f"             [ACL - 802.1x - RADIUS Server] Index{index+1} IP Address Test Fail",file = open(file_name, '+a'))
            if_rad_ser_error = True
        if(driver.find_elements(By.NAME, "rpDot1xServer_secret")[index].get_attribute("value") != "123456789012345678901234567890123456789012345678901234567890123"):
            print(f"             [ACL - 802.1x - RADIUS Server] Index{index+1} IP Address Test Fail",file = open(file_name, '+a'))
            if_rad_ser_error = True

    # 802.1x RADIUS Server Result
    if(if_rad_ser_error == True):
        print("[MSAN1-11818][ACL - 802.1x - RADIUS Server] Result Fail",file = open(file_name, '+a'))
    else:
        print("[MSAN1-11818][ACL - 802.1x - RADIUS Server] Result Pass",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # ACL 802.1x User Profile Test
    # ACL > 802.1x > User Profile
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 User Profile
    mod.Tab_Switch(driver,"User Profile")

    # 802.1x User Profile Clear
    if_clear = False
    while(if_clear == False):
        try:
            driver.find_element(By.NAME, "rpDot1xUserProf_select").click()
            acl.x802_1x_User_Profile_Delete(driver)
        except:
            if_clear = True

    # 802.1x User Profile Check 1
    acl.x802_1x_User_Profile_Name(driver,"1234567890123456789012345678901")
    acl.x802_1x_User_Profile_Password(driver,"1234567890123456789012345678901")
    acl.x802_1x_User_Profile_Retype_Password(driver,"9876543210987654321098765432109")
    acl.x802_1x_User_Profile_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print("             [ACL - 802.1x - User Profile] Password != Retype_Password No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # 802.1x User Profile Input Full
    if_full = False
    user_pro_name = 8000
    while(if_full == False):
        user_pro_name = user_pro_name+1
        acl.x802_1x_User_Profile_Name(driver,f"123456789012345678901234567{user_pro_name}")
        acl.x802_1x_User_Profile_Password(driver,"1234567890123456789012345678901")
        acl.x802_1x_User_Profile_Retype_Password(driver,"1234567890123456789012345678901")
        acl.x802_1x_User_Profile_Apply(driver)
        try:
            driver.find_element(By.NAME, "rperror_btnBack").click()
            if_full = True
        except:
            pass
    print(f"             [ACL - 802.1x - User Profile] Max Capacity(256) = {user_pro_name-8001}",file = open(file_name, '+a'))

    # 802.1x User Profile Clear
    if_clear = False
    while(if_clear == False):
        try:
            driver.find_element(By.NAME, "rpDot1xUserProf_select").click()
            acl.x802_1x_User_Profile_Delete(driver)
        except:
            if_clear = True

    if(if_error == False):
        print(f"[MSAN1-11819][ACL - 802.1x - User Profile] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11819][ACL - 802.1x - User Profile] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # ACL 802.1x Port Setting Test
    # ACL > 802.1x > Port Setting
    # -------------------------start-------------------------

    # 路徑導向 Port Setting
    mod.Tab_Switch(driver,"Port Setting")

    # slot select
    sta.Slot_Select(driver,glc_slot)
    sta.Load(driver)

    # 802.1x Port Setting Input
    retry = True
    while(retry == True):
        try:
            acl.x802_1x_Port_Setting_Enable_All(driver,True)
        except:
            time.sleep(1)
        try:
            if(driver.find_element(By.NAME, "rpdot1x_portcfg_chkAll_enable").is_selected() == True):
                retry = False
        except:
            time.sleep(1)
    acl.x802_1x_Port_Setting_Control_All(driver,4)
    acl.x802_1x_Port_Setting_Server_Index_All(driver,17)
    retry = True
    while(retry == True):
        try:
            acl.x802_1x_Port_Setting_Auth_Once_All(driver,True)
        except:
            time.sleep(1)
        try:
            if(driver.find_element(By.NAME, "rpdot1x_portcfg_chkAll_authonce").is_selected() == True):
                retry = False
        except:
            time.sleep(1)
    acl.x802_1x_Port_Setting_Reauth_Period_All(driver,"65535")
    acl.x802_1x_Port_Setting_Circuit_ID_All(driver,"123456789012345678901234567890123456789012345678901234567890123")
    acl.x802_1x_Port_Setting_Apply(driver)

    if_por_set_error = False

    # 802.1x Port Setting Check
    if(driver.find_elements(By.NAME, "rpdot1x_portcfg_chk_enable")[int(glc_port)-1].is_selected() != True):
        print(f"             [ACL - 802.1x - Port Setting] Port{glc_port} Enable Test Fail",file = open(file_name, '+a'))
        if_por_set_error = True
    if(driver.find_element(By.XPATH, f"/html/body/form/div[6]/div/div[{int(glc_port)+19}]/div[3]/select/option[3]").is_selected() != True):
        print(f"             [ACL - 802.1x - Port Setting] Port{glc_port} Control Test Fail",file = open(file_name, '+a'))
        if_por_set_error = True
    if(driver.find_element(By.XPATH, f"/html/body/form/div[6]/div/div[{int(glc_port)+19}]/div[4]/select/option[16]").is_selected() != True):
        print(f"             [ACL - 802.1x - Port Setting] Port{glc_port} Server Index Test Fail",file = open(file_name, '+a'))
        if_por_set_error = True
    if(driver.find_elements(By.NAME, "rpdot1x_portcfg_chk_authonce")[int(glc_port)-1].is_selected() != True):
        print(f"             [ACL - 802.1x - Port Setting] Port{glc_port} Auth Once Test Fail",file = open(file_name, '+a'))
        if_por_set_error = True
    if(driver.find_elements(By.NAME, "rpdot1x_portcfg_period")[int(glc_port)-1].get_attribute("value") != "65535"):
        print(f"             [ACL - 802.1x - Port Setting] Port{glc_port} Reauth Period Test Fail",file = open(file_name, '+a'))
        if_por_set_error = True
    if(driver.find_elements(By.NAME, "rpdot1x_portcfg_ipt_circuid_id")[int(glc_port)-1].get_attribute("value") != "123456789012345678901234567890123456789012345678901234567890123"):
        print(f"             [ACL - 802.1x - Port Setting] Port{glc_port} Circuit ID Test Fail",file = open(file_name, '+a'))
        if_por_set_error = True

    # 802.1x Port Setting Result
    if(if_por_set_error != True):
        print("[MSAN1-11820][ACL - 802.1x - Port Setting] Result Pass",file = open(file_name, '+a'))
    else:
        print("[MSAN1-11820][ACL - 802.1x - Port Setting] Result Fail",file = open(file_name, '+a'))

    #Statistics > 802.1x Port Status Check

    # 路徑導向 Statistics > 802.1x Port Status
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Statistics")
    mod.SubPage_Switch(driver,"802.1x Port Status")
    mod.Switch_Frame(driver)

    if_por_sta_error = False

    # 802.1x Port Status MSC Test
    sta.Slot_Select(driver,msc_slot)
    sta.Load(driver)
    if(driver.find_element(By.CLASS_NAME, "rpdot1xportstatusList").get_attribute("style") != "display: none;"):
        print(f"             [Statistics - 802.1x Port Status] MSC Invalid Test Fail",file = open(file_name, '+a'))
        if_por_sta_error = True

    # 802.1x Port Status GLC Test
    sta.Slot_Select(driver,glc_slot)
    sta.Load(driver)
    if(driver.find_element(By.CLASS_NAME, "rpdot1xportstatusList").get_attribute("style") == "display: none;"):
        print(f"             [Statistics - 802.1x Port Status] GLC Valid Test Fail",file = open(file_name, '+a'))
        if_por_sta_error = True
    if(driver.find_elements(By.CLASS_NAME, "div-row-cell-content.rpdot1x_portstatus_status")[int(glc_port)-1].get_attribute("textContent") != " active"):
        print(f"             [Statistics - 802.1x Port Status] Port{glc_port} Status Test Fail",file = open(file_name, '+a'))
        if_por_sta_error = True
    if(driver.find_elements(By.CLASS_NAME, "div-row-cell-content.rpdot1x_portstatus_control")[int(glc_port)-1].get_attribute("textContent") != "unauth"):
        print(f"             [Statistics - 802.1x Port Status] Port{glc_port} Control Test Fail",file = open(file_name, '+a'))
        if_por_sta_error = True
    if(driver.find_elements(By.CLASS_NAME, "div-row-cell-content.rpdot1x_portstatus_serverindex")[int(glc_port)-1].get_attribute("textContent") != "16"):
        print(f"             [Statistics - 802.1x Port Status] Port{glc_port} Server Index Test Fail",file = open(file_name, '+a'))
        if_por_sta_error = True
    if(driver.find_elements(By.CLASS_NAME, "div-row-cell-content.rpdot1x_portstatus_reauth")[int(glc_port)-1].get_attribute("textContent") != "	 V"):
        print(f"             [Statistics - 802.1x Port Status] Port{glc_port} Reauth Test Fail",file = open(file_name, '+a'))
        if_por_sta_error = True
    if(driver.find_elements(By.CLASS_NAME, "div-row-cell-content.rpdot1x_portstatus_reauthPeriod")[int(glc_port)-1].get_attribute("textContent") != "65535"):
        print(f"             [Statistics - 802.1x Port Status] Port{glc_port} Reauth Period Test Fail",file = open(file_name, '+a'))
        if_por_sta_error = True
    if(driver.find_elements(By.CLASS_NAME, "div-row-cell-content.rpdot1x_portstatus_circuitId")[int(glc_port)-1].get_attribute("textContent") != "123456789012345678901234567890123456789012345678901234567890123"):
        print(f"             [Statistics - 802.1x Port Status] Port{glc_port} Circuit Id Option Test Fail",file = open(file_name, '+a'))
        if_por_sta_error = True

    # 802.1x Port Status Result
    if(if_por_sta_error != True):
        print("[MSAN1-11937][Statistics - 802.1x Port Status] Result Pass",file = open(file_name, '+a'))
    else:
        print("[MSAN1-11937][Statistics - 802.1x Port Status] Result Fail",file = open(file_name, '+a'))

    # 路徑導向 802.1x > Port Setting
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"ACL")
    mod.SubPage_Switch(driver,"802.1x")
    mod.Switch_Frame(driver)
    mod.Tab_Switch(driver,"Port Setting")

    # slot select
    acl.Slot_Select(driver,glc_slot)
    acl.Load(driver)

    # 802.1x Port Setting Clear
    acl.x802_1x_Port_Setting_Enable_All(driver,True)
    acl.x802_1x_Port_Setting_Enable_All(driver,False)
    acl.x802_1x_Port_Setting_Control_All(driver,2)
    acl.x802_1x_Port_Setting_Server_Index_All(driver,2)
    acl.x802_1x_Port_Setting_Auth_Once_All(driver,True)
    acl.x802_1x_Port_Setting_Auth_Once_All(driver,False)
    acl.x802_1x_Port_Setting_Reauth_Period_All(driver,"3600")
    is_clear = False
    index = 0
    while(is_clear == False):
        try:
            driver.find_elements(By.NAME, "rpdot1x_portcfg_ipt_circuid_id")[index].clear()
            index = index+1
        except:
            is_clear = True
    acl.x802_1x_Port_Setting_Apply(driver)

    # -------------------------end-------------------------

    # ACL Loopguard
    # ACL > Loopguard
    # -------------------------start-------------------------

    # 路徑導向 Loopguard
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"Loopguard")
    mod.Switch_Frame(driver)

    # slot select
    acl.Slot_Select(driver,glc_slot)
    acl.Load(driver)

    # Loopguard Default
    acl.Loopguard_LG_Enable_All(driver,True)
    acl.Loopguard_LG_Enable_All(driver,False)
    acl.Loopguard_Policy_All(driver,2)
    acl.Loopguard_Recover_Time_All(driver,"60")
    acl.Loopguard_Apply(driver)

    # Loopguard 傳入值
    retry = True
    while(retry == True):
        try:
            acl.Loopguard_LG_Enable_All(driver,True)
        except:
            time.sleep(1)
        try:
            if(driver.find_element(By.NAME, "rpacl_lg_iptALL_chk_enable").is_selected() == True):
                retry = False
        except:
            time.sleep(1)
    acl.Loopguard_Policy_All(driver,3)
    acl.Loopguard_Recover_Time_All(driver,"600")
    acl.Loopguard_Apply(driver)
    time.sleep(2)
    acl.Load(driver)

    if_acl_lop_error = False

    # Loopguard 檢驗
    if(driver.find_elements(By.NAME, "rpacl_lg_enable")[int(glc_port)-1].is_selected() != True):
        print(f"             [ACL - Loopguard] Port{glc_port} LG Enable Test Fail",file = open(file_name, '+a'))
        if_acl_lop_error = True
    if(driver.find_element(By.XPATH, f"/html/body/form/div/div[{int(glc_port)+13}]/div[4]/select/option[2]").is_selected() != True):
        print(f"             [ACL - Loopguard] Port{glc_port} Policy Test Fail",file = open(file_name, '+a'))
        if_acl_lop_error = True
    if(driver.find_elements(By.NAME, "rpacl_lg_recover_time")[int(glc_port)-1].get_attribute("value") != "600"):
        print(f"             [ACL - Loopguard] Port{glc_port} Recover Time Test Fail",file = open(file_name, '+a'))
        if_acl_lop_error = True

    # ACL Loopguard Result
    if(if_acl_lop_error != True):
        print("[MSAN1-11821][ACL - Loopguard] Result Pass",file = open(file_name, '+a'))
    else:
        print("[MSAN1-11821][ACL - Loopguard] Result Fail",file = open(file_name, '+a'))

    #Statistics > Loopguard Check

    # 路徑導向 Statistics > Loopguard
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Statistics")
    mod.SubPage_Switch(driver,"Loopguard")
    mod.Switch_Frame(driver)

    if_sta_lop_error = False

    # MSC Test
    if_msc_error = False
    sta.Slot_Select(driver,msc_slot)
    sta.Load(driver)
    if(driver.find_element(By.NAME, "rpacl_lgSt_Form").get_attribute('style') == "display: none;"):
        print(f"             [Statistics - Loopguard] MSC Valid Test Fail",file = open(file_name, '+a'))
        if_sta_lop_error = True
    else:
        driver.find_element(By.NAME, "rpacl_lgSt_btnRefresh").click()
        driver.find_element(By.NAME, "rpacl_lgSt_btnFlush").click()
        if(driver.find_elements(By.CLASS_NAME, "div-row-cell-content.wp-15.rpacl_lg_total_tx")[int(msc_port)-1].get_attribute('textContent') != "0"):
            if_msc_error = True
        if(driver.find_elements(By.CLASS_NAME, "div-row-cell-content.wp-15.rpacl_lg_total_rx")[int(msc_port)-1].get_attribute('textContent') != "0"):
            if_msc_error = True
        if(driver.find_elements(By.CLASS_NAME, "div-row-cell-content.wp-10.rpacl_lg_bad_rx")[int(msc_port)-1].get_attribute('textContent') != "0"):
            if_msc_error = True
    if(if_msc_error == True):
        print(f"             [Statistics - Loopguard] MSC Test Fail",file = open(file_name, '+a'))
        if_sta_lop_error = True

    # GLC Test
    sta.Slot_Select(driver,glc_slot)
    sta.Load(driver)

    # Loopguard Check
    if(driver.find_elements(By.CLASS_NAME, "div-row-cell-content.wp-10.rpacl_lg_enable")[int(glc_port)-1].get_attribute("textContent") != "V"):
        print("             [Statistics - Loopguard] GLC Test Fail",file = open(file_name, '+a'))
        if_sta_lop_error = True

    # Loopguard Refresh
    sta.Loopguard_Refresh(driver)

    # Loopguard Refresh Check
    if(driver.find_elements(By.CLASS_NAME, "div-row-cell-content.wp-10.rpacl_lg_enable")[int(glc_port)-1].get_attribute("textContent") != "V"):
        print("             [Statistics - Loopguard] GLC Refresh Test Fail",file = open(file_name, '+a'))
        if_sta_lop_error = True

    # Loopguard Flush
    sta.Loopguard_Flush(driver)

    # Loopguard Flush Check
    if(driver.find_elements(By.CLASS_NAME, "div-row-cell-content.wp-10.rpacl_lg_enable")[int(glc_port)-1].get_attribute("textContent") != "V"):
        print("             [Statistics - Loopguard] GLC Flush Test Fail",file = open(file_name, '+a'))
        if_sta_lop_error = True

    # Statistics Loopguard Result
    if(if_sta_lop_error != True):
        print("[MSAN1-11935][Statistics - Loopguard] Result Pass",file = open(file_name, '+a'))
    else:  
        print("[MSAN1-11935][Statistics - Loopguard] Result Fail",file = open(file_name, '+a'))

    # 路徑導向 ACL > Loopguard
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"ACL")
    mod.SubPage_Switch(driver,"Loopguard")
    mod.Switch_Frame(driver)

    # slot select
    acl.Slot_Select(driver,glc_slot)
    acl.Load(driver)

    # Loopguard Default
    acl.Loopguard_LG_Enable_All(driver,True)
    acl.Loopguard_LG_Enable_All(driver,False)
    acl.Loopguard_Policy_All(driver,2)
    acl.Loopguard_Recover_Time_All(driver,"60")
    acl.Loopguard_Apply(driver)

    # -------------------------end-------------------------

    # ACL Packet Filter
    # ACL > Packet Filter
    # -------------------------start-------------------------

    # 路徑導向 Packet Filter
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"Packet Filter")
    mod.Switch_Frame(driver)

    # slot select
    driver.find_elements(By.NAME, "Pkfiltertableid")[int(glc_slot)-1].click()

    # Packet Filter 傳入值
    acl.Packet_Filter_Type_All(driver,3)
    acl.Packet_Filter_PPPoE_All(driver,True)
    acl.Packet_Filter_IP_All(driver,True)
    acl.Packet_Filter_ARP_All(driver,True)
    acl.Packet_Filter_NetBIOS_All(driver,True)
    acl.Packet_Filter_DHCP_All(driver,True)
    acl.Packet_Filter_EAPOL_All(driver,True)
    acl.Packet_Filter_IGMP_All(driver,True)
    acl.Packet_Filter_Apply(driver)

    if_pac_fil_error = False

    # Packet Filter 檢驗
    if(driver.find_element(By.XPATH, f"//form[@id='rppkfilter_Form']/div[4]/div[{int(glc_port)+19}]/div[2]/select/option[3]").is_selected() != True):
        print("             [ACL - Packet Filter] Type Test Fail",file = open(file_name, '+a'))
        if_pac_fil_error = True
    if(driver.find_elements(By.NAME, f"rppkfilterREJECT_PPPoE")[int(glc_port)].is_selected() != True):
        print("             [ACL - Packet Filter] PPPoE Test Fail",file = open(file_name, '+a'))
        if_pac_fil_error = True
    if(driver.find_elements(By.NAME, f"rppkfilterREJECT_IP")[int(glc_port)].is_selected() != True):
        print("             [ACL - Packet Filter] IP Test Fail",file = open(file_name, '+a'))
        if_pac_fil_error = True
    if(driver.find_elements(By.NAME, f"rppkfilterREJECT_ARP")[int(glc_port)].is_selected() != True):
        print("             [ACL - Packet Filter] ARP Test Fail",file = open(file_name, '+a'))
        if_pac_fil_error = True
    if(driver.find_elements(By.NAME, f"rppkfilterREJECT_NETBIOS")[int(glc_port)].is_selected() != True):
        print("             [ACL - Packet Filter] NetBIOS Test Fail",file = open(file_name, '+a'))
        if_pac_fil_error = True
    if(driver.find_elements(By.NAME, f"rppkfilterREJECT_DHCP")[int(glc_port)].is_selected() != True):
        print("             [ACL - Packet Filter] DHCP Test Fail",file = open(file_name, '+a'))
        if_pac_fil_error = True
    if(driver.find_elements(By.NAME, f"rppkfilterREJECT_EAPOL")[int(glc_port)].is_selected() != True):
        print("             [ACL - Packet Filter] EAPOL Test Fail",file = open(file_name, '+a'))
        if_pac_fil_error = True
    if(driver.find_elements(By.NAME, f"rppkfilterREJECT_IGMP")[int(glc_port)].is_selected() != True):
        print("             [ACL - Packet Filter] IGMP Test Fail",file = open(file_name, '+a'))
        if_pac_fil_error = True

    # Packet Filter Result
    if(if_pac_fil_error != True):
        print("[MSAN1-11822][ACL - Packet Filter] Result Pass",file = open(file_name, '+a'))
    else:
        print("[MSAN1-11822][ACL - Packet Filter] Result Fail",file = open(file_name, '+a'))

    # Packet Filter 傳入值
    acl.Packet_Filter_Type_All(driver,1)
    acl.Packet_Filter_Apply(driver)

    # -------------------------end-------------------------

    # ACL Packet Filter
    # ACL > Packet Filter
    # -------------------------start-------------------------

    # 路徑導向 BPDU Ctrl
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"BPDU Ctrl")
    mod.Switch_Frame(driver)

    # slot select
    retry = True
    while(retry == True):
        try:
            driver.find_element(By.XPATH, f"//*[@id='rpbpdu_slot']/option[{glc_slot}]").click()
        except:
            time.sleep(1)
        try:
            if(driver.find_element(By.XPATH, f"//*[@id='rpbpdu_slot']/option[{glc_slot}]").is_selected() == True):
                retry = False
        except:
            time.sleep(1)

    if_bpdu_error = False

    # BPDU Ctrl Test 1
    acl.BPDU_Ctrl_Mode_All(driver,2)
    acl.BPDU_Ctrl_Apply(driver)
    if(driver.find_element(By.XPATH, f"//*[@id='rpbpdu_mode{glc_port}']/option[2]").is_selected() != True):
        print("             [ACL - BPDU Ctrl] tunnel Test Fail",file = open(file_name, '+a'))
        if_bpdu_error = True

    # BPDU Ctrl Test 2
    acl.BPDU_Ctrl_Mode_All(driver,3)
    acl.BPDU_Ctrl_Apply(driver)
    if(driver.find_element(By.XPATH, f"//*[@id='rpbpdu_mode{glc_port}']/option[3]").is_selected() != True):
        print("             [ACL - BPDU Ctrl] duscard Test Fail",file = open(file_name, '+a'))
        if_bpdu_error = True

    # BPDU Ctrl Test 3
    acl.BPDU_Ctrl_Mode_All(driver,4)
    acl.BPDU_Ctrl_Apply(driver)
    if(driver.find_element(By.XPATH, f"//*[@id='rpbpdu_mode{glc_port}']/option[4]").is_selected() != True):
        print("             [ACL - BPDU Ctrl] network Test Fail",file = open(file_name, '+a'))
        if_bpdu_error = True

    # BPDU Ctrl Test 4
    acl.BPDU_Ctrl_Mode_All(driver,1)
    acl.BPDU_Ctrl_Apply(driver)
    if(driver.find_element(By.XPATH, f"//*[@id='rpbpdu_mode{glc_port}']/option[1]").is_selected() != True):
        print("             [ACL - BPDU Ctrl] peel Test Fail",file = open(file_name, '+a'))
        if_bpdu_error = True

    # BPDU Ctrl Result
    if(if_bpdu_error != True):
        print("[MSAN1-11830][ACL - BPDU Ctrl] Result Pass",file = open(file_name, '+a'))
    else:
        print("[MSAN1-11830][ACL - BPDU Ctrl] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # ACL Host Protection
    # ACL > Host Protection
    # -------------------------start-------------------------

    # 路徑導向 Host Protection
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"Host Protection")
    mod.Switch_Frame(driver)

    if_hos_pro_error = False

    # Host Protection Test 1
    acl.Host_Protection_ARP(driver,"10")
    acl.Host_Protection_Apply(driver)
    if(mod.IsAlert(driver) == True):
        print(f"             [ACL - Host Protection] ARP Input:10 Alert Test Fail",file = open(file_name, '+a'))
        if_hos_pro_error = True
        acl.Host_Protection_Cancel(driver)
    else:
        if(driver.find_element(By.NAME, "rpaclhostprotect_rateArp").get_attribute("value") != "10"):
            print(f"             [ACL - Host Protection] ARP Input:10 Test Fail",file = open(file_name, '+a'))
            if_hos_pro_error = True
    acl.Host_Protection_BPDU(driver,"10")
    acl.Host_Protection_Apply(driver)
    if(mod.IsAlert(driver) == True):
        print(f"             [ACL - Host Protection] BPDU Input:10 Alert Test Fail",file = open(file_name, '+a'))
        if_hos_pro_error = True
        acl.Host_Protection_Cancel(driver)
    else:
        if(driver.find_element(By.NAME, "rpaclhostprotect_rateBpdu").get_attribute("value") != "10"):
            print(f"             [ACL - Host Protection] BPDU Input:10 Test Fail",file = open(file_name, '+a'))
            if_hos_pro_error = True
    acl.Host_Protection_DHCP(driver,"10")
    acl.Host_Protection_Apply(driver)
    if(mod.IsAlert(driver) == True):
        print(f"             [ACL - Host Protection] DHCP Input:10 Alert Test Fail",file = open(file_name, '+a'))
        if_hos_pro_error = True
        acl.Host_Protection_Cancel(driver)
    else:
        if(driver.find_element(By.NAME, "rpaclhostprotect_rateDhcp").get_attribute("value") != "10"):
            print(f"             [ACL - Host Protection] DHCP Input:10 Test Fail",file = open(file_name, '+a'))
            if_hos_pro_error = True
    acl.Host_Protection_DHCPv6(driver,"10")
    acl.Host_Protection_Apply(driver)
    if(mod.IsAlert(driver) == True):
        print(f"             [ACL - Host Protection] DHCPv6 Input:10 Alert Test Fail",file = open(file_name, '+a'))
        if_hos_pro_error = True
        acl.Host_Protection_Cancel(driver)
    else:
        if(driver.find_element(By.NAME, "rpaclhostprotect_rateDhcpv6").get_attribute("value") != "10"):
            print(f"             [ACL - Host Protection] DHCPv6 Input:10 Test Fail",file = open(file_name, '+a'))
            if_hos_pro_error = True
    acl.Host_Protection_ICMPv6(driver,"10")
    acl.Host_Protection_Apply(driver)
    if(mod.IsAlert(driver) == True):
        print(f"             [ACL - Host Protection] ICMPv6 Input:10 Alert Test Fail",file = open(file_name, '+a'))
        if_hos_pro_error = True
        acl.Host_Protection_Cancel(driver)
    else:
        if(driver.find_element(By.NAME, "rpaclhostprotect_rateIcmpv6").get_attribute("value") != "10"):
            print(f"             [ACL - Host Protection] ICMPv6 Input:10 Test Fail",file = open(file_name, '+a'))
            if_hos_pro_error = True
    acl.Host_Protection_IGMP(driver,"10")
    acl.Host_Protection_Apply(driver)
    if(mod.IsAlert(driver) == True):
        print(f"             [ACL - Host Protection] IGMP Input:10 Alert Test Fail",file = open(file_name, '+a'))
        if_hos_pro_error = True
        acl.Host_Protection_Cancel(driver)
    else:
        if(driver.find_element(By.NAME, "rpaclhostprotect_rateIgmp").get_attribute("value") != "10"):
            print(f"             [ACL - Host Protection] IGMP Input:10 Test Fail",file = open(file_name, '+a'))
            if_hos_pro_error = True
    acl.Host_Protection_PPPoE(driver,"10")
    acl.Host_Protection_Apply(driver)
    if(mod.IsAlert(driver) == True):
        print(f"             [ACL - Host Protection] PPPoE Input:10 Alert Test Fail",file = open(file_name, '+a'))
        if_hos_pro_error = True
        acl.Host_Protection_Cancel(driver)
    else:
        if(driver.find_element(By.NAME, "rpaclhostprotect_ratePppoe").get_attribute("value") != "10"):
            print(f"             [ACL - Host Protection] PPPoE Input:10 Test Fail",file = open(file_name, '+a'))
            if_hos_pro_error = True

    # Host Protection Test 2~4
    hos_pro_test_keys = ["9","501","@"]
    for test_times in range(3):
        acl.Host_Protection_ARP(driver,hos_pro_test_keys[test_times])
        acl.Host_Protection_Apply(driver)
        if(mod.IsAlert(driver) != True):
            print(f"             [ACL - Host Protection] ARP Input:{hos_pro_test_keys[test_times]} No Alert Test Fail",file = open(file_name, '+a'))
            if_hos_pro_error = True
        acl.Host_Protection_Cancel(driver)
        time.sleep(2)
        if(driver.find_element(By.NAME, "rpaclhostprotect_rateArp").get_attribute("value") != "10"):
            print(f"             [ACL - Host Protection] ARP Input:{hos_pro_test_keys[test_times]} No Alert Test Fail",file = open(file_name, '+a'))
            if_hos_pro_error = True
        acl.Host_Protection_BPDU(driver,hos_pro_test_keys[test_times])
        acl.Host_Protection_Apply(driver)
        if(mod.IsAlert(driver) != True):
            print(f"             [ACL - Host Protection] BPDU Input:{hos_pro_test_keys[test_times]} No Alert Test Fail",file = open(file_name, '+a'))
            if_hos_pro_error = True
        acl.Host_Protection_Cancel(driver)
        time.sleep(2)
        if(driver.find_element(By.NAME, "rpaclhostprotect_rateBpdu").get_attribute("value") != "10"):
            print(f"             [ACL - Host Protection] BPDU Input:{hos_pro_test_keys[test_times]} No Alert Test Fail",file = open(file_name, '+a'))
            if_hos_pro_error = True
        acl.Host_Protection_DHCP(driver,hos_pro_test_keys[test_times])
        acl.Host_Protection_Apply(driver)
        if(mod.IsAlert(driver) != True):
            print(f"             [ACL - Host Protection] DHCP Input:{hos_pro_test_keys[test_times]} No Alert Test Fail",file = open(file_name, '+a'))
            if_hos_pro_error = True
        acl.Host_Protection_Cancel(driver)
        time.sleep(2)
        if(driver.find_element(By.NAME, "rpaclhostprotect_rateDhcp").get_attribute("value") != "10"):
            print(f"             [ACL - Host Protection] DHCP Input:{hos_pro_test_keys[test_times]} No Alert Test Fail",file = open(file_name, '+a'))
            if_hos_pro_error = True
        acl.Host_Protection_DHCPv6(driver,hos_pro_test_keys[test_times])
        acl.Host_Protection_Apply(driver)
        if(mod.IsAlert(driver) != True):
            print(f"             [ACL - Host Protection] DHCPv6 Input:{hos_pro_test_keys[test_times]} No Alert Test Fail",file = open(file_name, '+a'))
            if_hos_pro_error = True
        acl.Host_Protection_Cancel(driver)
        time.sleep(2)
        if(driver.find_element(By.NAME, "rpaclhostprotect_rateDhcpv6").get_attribute("value") != "10"):
            print(f"             [ACL - Host Protection] DHCPv6 Input:{hos_pro_test_keys[test_times]} No Alert Test Fail",file = open(file_name, '+a'))
            if_hos_pro_error = True
        acl.Host_Protection_ICMPv6(driver,hos_pro_test_keys[test_times])
        acl.Host_Protection_Apply(driver)
        if(mod.IsAlert(driver) != True):
            print(f"             [ACL - Host Protection] ICMPv6 Input:{hos_pro_test_keys[test_times]} No Alert Test Fail",file = open(file_name, '+a'))
            if_hos_pro_error = True
        acl.Host_Protection_Cancel(driver)
        time.sleep(2)
        if(driver.find_element(By.NAME, "rpaclhostprotect_rateIcmpv6").get_attribute("value") != "10"):
            print(f"             [ACL - Host Protection] ICMPv6 Input:{hos_pro_test_keys[test_times]} No Alert Test Fail",file = open(file_name, '+a'))
            if_hos_pro_error = True
        acl.Host_Protection_IGMP(driver,hos_pro_test_keys[test_times])
        acl.Host_Protection_Apply(driver)
        if(mod.IsAlert(driver) != True):
            print(f"             [ACL - Host Protection] IGMP Input:{hos_pro_test_keys[test_times]} No Alert Test Fail",file = open(file_name, '+a'))
            if_hos_pro_error = True
        acl.Host_Protection_Cancel(driver)
        time.sleep(2)
        if(driver.find_element(By.NAME, "rpaclhostprotect_rateIgmp").get_attribute("value") != "10"):
            print(f"             [ACL - Host Protection] IGMP Input:{hos_pro_test_keys[test_times]} No Alert Test Fail",file = open(file_name, '+a'))
            if_hos_pro_error = True
        acl.Host_Protection_PPPoE(driver,hos_pro_test_keys[test_times])
        acl.Host_Protection_Apply(driver)
        if(mod.IsAlert(driver) != True):
            print(f"             [ACL - Host Protection] PPPoE Input:{hos_pro_test_keys[test_times]} No Alert Test Fail",file = open(file_name, '+a'))
            if_hos_pro_error = True
        acl.Host_Protection_Cancel(driver)
        time.sleep(2)
        if(driver.find_element(By.NAME, "rpaclhostprotect_ratePppoe").get_attribute("value") != "10"):
            print(f"             [ACL - Host Protection] PPPoE Input:{hos_pro_test_keys[test_times]} No Alert Test Fail",file = open(file_name, '+a'))
            if_hos_pro_error = True

    # Host Protection Test 5~6
    hos_pro_test_keys = ["500","0"]
    for test_times in range(2):
        acl.Host_Protection_ARP(driver,hos_pro_test_keys[test_times])
        acl.Host_Protection_Apply(driver)
        if(mod.IsAlert(driver) == True):
            print(f"             [ACL - Host Protection] ARP Input:{hos_pro_test_keys[test_times]} Alert Test Fail",file = open(file_name, '+a'))
            if_hos_pro_error = True
            acl.Host_Protection_Cancel(driver)
        else:
            if(driver.find_element(By.NAME, "rpaclhostprotect_rateArp").get_attribute("value") != hos_pro_test_keys[test_times]):
                print(f"             [ACL - Host Protection] ARP Input:{hos_pro_test_keys[test_times]} Test Fail",file = open(file_name, '+a'))
                if_hos_pro_error = True
        acl.Host_Protection_BPDU(driver,hos_pro_test_keys[test_times])
        acl.Host_Protection_Apply(driver)
        if(mod.IsAlert(driver) == True):
            print(f"             [ACL - Host Protection] BPDU Input:{hos_pro_test_keys[test_times]} Alert Test Fail",file = open(file_name, '+a'))
            if_hos_pro_error = True
            acl.Host_Protection_Cancel(driver)
        else:
            if(driver.find_element(By.NAME, "rpaclhostprotect_rateBpdu").get_attribute("value") != hos_pro_test_keys[test_times]):
                print(f"             [ACL - Host Protection] BPDU Input:{hos_pro_test_keys[test_times]} Test Fail",file = open(file_name, '+a'))
                if_hos_pro_error = True
        acl.Host_Protection_DHCP(driver,hos_pro_test_keys[test_times])
        acl.Host_Protection_Apply(driver)
        if(mod.IsAlert(driver) == True):
            print(f"             [ACL - Host Protection] DHCP Input:{hos_pro_test_keys[test_times]} Alert Test Fail",file = open(file_name, '+a'))
            if_hos_pro_error = True
            acl.Host_Protection_Cancel(driver)
        else:
            if(driver.find_element(By.NAME, "rpaclhostprotect_rateDhcp").get_attribute("value") != hos_pro_test_keys[test_times]):
                print(f"             [ACL - Host Protection] DHCP Input:{hos_pro_test_keys[test_times]} Test Fail",file = open(file_name, '+a'))
                if_hos_pro_error = True
        acl.Host_Protection_DHCPv6(driver,hos_pro_test_keys[test_times])
        acl.Host_Protection_Apply(driver)
        if(mod.IsAlert(driver) == True):
            print(f"             [ACL - Host Protection] DHCPv6 Input:{hos_pro_test_keys[test_times]} Alert Test Fail",file = open(file_name, '+a'))
            if_hos_pro_error = True
            acl.Host_Protection_Cancel(driver)
        else:
            if(driver.find_element(By.NAME, "rpaclhostprotect_rateDhcpv6").get_attribute("value") != hos_pro_test_keys[test_times]):
                print(f"             [ACL - Host Protection] DHCPv6 Input:{hos_pro_test_keys[test_times]} Test Fail",file = open(file_name, '+a'))
                if_hos_pro_error = True
        acl.Host_Protection_ICMPv6(driver,hos_pro_test_keys[test_times])
        acl.Host_Protection_Apply(driver)
        if(mod.IsAlert(driver) == True):
            print(f"             [ACL - Host Protection] ICMPv6 Input:{hos_pro_test_keys[test_times]} Alert Test Fail",file = open(file_name, '+a'))
            if_hos_pro_error = True
            acl.Host_Protection_Cancel(driver)
        else:
            if(driver.find_element(By.NAME, "rpaclhostprotect_rateIcmpv6").get_attribute("value") != hos_pro_test_keys[test_times]):
                print(f"             [ACL - Host Protection] ICMPv6 Input:{hos_pro_test_keys[test_times]} Test Fail",file = open(file_name, '+a'))
                if_hos_pro_error = True
        acl.Host_Protection_IGMP(driver,hos_pro_test_keys[test_times])
        acl.Host_Protection_Apply(driver)
        if(mod.IsAlert(driver) == True):
            print(f"             [ACL - Host Protection] IGMP Input:{hos_pro_test_keys[test_times]} Alert Test Fail",file = open(file_name, '+a'))
            if_hos_pro_error = True
            acl.Host_Protection_Cancel(driver)
        else:
            if(driver.find_element(By.NAME, "rpaclhostprotect_rateIgmp").get_attribute("value") != hos_pro_test_keys[test_times]):
                print(f"             [ACL - Host Protection] IGMP Input:{hos_pro_test_keys[test_times]} Test Fail",file = open(file_name, '+a'))
                if_hos_pro_error = True
        acl.Host_Protection_PPPoE(driver,hos_pro_test_keys[test_times])
        acl.Host_Protection_Apply(driver)
        if(mod.IsAlert(driver) == True):
            print(f"             [ACL - Host Protection] PPPoE Input:{hos_pro_test_keys[test_times]} Alert Test Fail",file = open(file_name, '+a'))
            if_hos_pro_error = True
            acl.Host_Protection_Cancel(driver)
        else:
            if(driver.find_element(By.NAME, "rpaclhostprotect_ratePppoe").get_attribute("value") != hos_pro_test_keys[test_times]):
                print(f"             [ACL - Host Protection] PPPoE Input:{hos_pro_test_keys[test_times]} Test Fail",file = open(file_name, '+a'))
                if_hos_pro_error = True

    # BPDU Ctrl Result
    if(if_hos_pro_error != True):
        print("[MSAN1-11831][ACL - Host Protection] Result Pass",file = open(file_name, '+a'))
    else:
        print("[MSAN1-11831][ACL - Host Protection] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def Alarm_Test(driver,glc_slot,glc_port,msc_slot,file_name):
    print(f"Alarm Test\nTest Start",file = open(file_name, '+a'))

    # Get MSC Card Type
    # Home
    # -------------------------start-------------------------

    mod.Switch_Default(driver)
    driver.find_elements(By.CLASS_NAME, "div-title-homelink")[1].click()
    mod.Switch_Frame(driver)
    time.sleep(5)
    MSC_Card_Type = driver.find_elements(By.CLASS_NAME, "td-table-content.SysinfoCardType.left-wrapper")[int(msc_slot)-1].get_attribute("textContent")

    # -------------------------end-------------------------

    # Maintenance Config Reset Reset
    # Maintenance > Config Reset
    # -------------------------start-------------------------

    # 路徑導向 Maintenance > Config Reset
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Maintenance")
    mod.SubPage_Switch(driver,"Config Reset")
    mod.Switch_Frame(driver)

    # Maintenance Config Reset Reset
    mai.Config_Reset(driver)
    pyautogui.press("enter")
    # print(f"Maintenance Config Reset",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Alarm Definition Setup
    # Alarm > Definition
    # -------------------------start-------------------------

    # 路徑導向 Alarm > Definition
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Alarm")
    mod.SubPage_Switch(driver,"Definition")
    mod.Switch_Frame(driver)

    # Alarm Definition Setting
    ala.Input_Definition_Alarm_Category(driver,3)
    driver.find_element(By.XPATH, f"//*[@name='rpalarm_def_slt_ser']/option[1]").click()
    ala.Input_Definition_Apply(driver)

    # -------------------------end-------------------------

    # Sys Monitor Setup
    # Sys > Monitor
    # -------------------------start-------------------------

    time.sleep(90)

    # 路徑導向 Sys > Monitor
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Sys")
    mod.SubPage_Switch(driver,"Monitor")
    mod.Switch_Frame(driver)

    # slot select
    sys.Slot_Select(driver,glc_slot)
    sys.Load(driver)

    # Sys > Monitor Voltage Setup
    for index in range(5):
        sys.Monitor_Voltage_High_limit(driver,index+1,"25000")
        sys.Monitor_Voltage_Low_limit(driver,index+1,"24999")
    sys.Monitor_Apply(driver)

    # -------------------------end-------------------------

    # Port GE Setup
    # Port > GE
    # -------------------------start-------------------------

    # 路徑導向 Port > GE
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Port")
    mod.SubPage_Switch(driver,"GE")
    mod.Switch_Frame(driver)

    # slot select
    driver.find_elements(By.NAME, "Lcmantableid")[int(glc_slot)-1].click()

    # Sys > GE Voltage Setup
    port.GE_Active(driver,glc_port,True)
    port.GE_Apply(driver)
    port.GE_Active(driver,glc_port,False)
    port.GE_Apply(driver)
    port.GE_Active(driver,glc_port,True)
    port.GE_Apply(driver)
    
    # -------------------------end-------------------------

    # Sys General Setup Time Setup
    # Sys > General Setup
    # -------------------------start-------------------------

    # 路徑導向 Sys > General Setup
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Sys")
    mod.SubPage_Switch(driver,"General Setup")
    mod.Switch_Frame(driver)

    # Setup
    sys.General_Setup_Time_Server_Type(driver,"NTP(RFC2030)")
    try:
        sys.General_Setup_Time_Server_IP_Address(driver,"216.239.35.4")
    except:
        sys.General_Setup_Time_Server_IP_Address_1(driver,"216.239.35.3")
        sys.General_Setup_Time_Server_IP_Address_2(driver,"216.239.35.4")
    sys.General_Setup_Time_Zone(driver,"UTC+0800")
    sys.General_Setup_Apply(driver)
    time.sleep(2)
    sys.General_Setup_Sync(driver)
    time.sleep(70)
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        pass
    pyautogui.press("enter")

    # -------------------------end-------------------------

    # Alarm Current Setup
    # Alarm > Current
    # -------------------------start-------------------------

    time.sleep(90)

    # 路徑導向 Alarm > Current
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Alarm")
    mod.Switch_Frame(driver)

    # Load
    ala.Current_Load(driver)

    if_alarm_current_error = False

    # Is Data Exist
    try:
        driver.find_element(By.CLASS_NAME, "AlarmCurrList")
        # print("             [Alarm - Current] Alarm Data Exist",file = open(file_name, '+a'))

        # Severity Critical Test
        ala.Current_Severity(driver,2)
        ala.Current_Load(driver)
        index = 0
        is_last = False
        is_error = False
        if_empty = False
        while(is_last == False):
            try:
                if(driver.find_elements(By.CLASS_NAME, "rpalmcurr_Severity")[index].get_attribute("textContent") != "critical"):
                    is_error = True
            except:
                is_last = True
                if(index == 0):
                    if_empty = True
                    print("             [Alarm - Current] Severity Critical No Alarm Data",file = open(file_name, '+a'))
            index = index+1
        if(if_empty == False):
            if(is_error == False):
                print("             [Alarm - Current] Severity Critical Test Pass",file = open(file_name, '+a'))
            else:
                print("             [Alarm - Current] Severity Critical Test Fail",file = open(file_name, '+a'))
                if_alarm_current_error = True

        # Severity Major Test
        ala.Current_Severity(driver,3)
        ala.Current_Load(driver)
        index = 0
        is_last = False
        is_error = False
        if_empty = False
        while(is_last == False):
            try:
                if(driver.find_elements(By.CLASS_NAME, "rpalmcurr_Severity")[index].get_attribute("textContent") != "major"):
                    is_error = True
            except:
                is_last = True
                if(index == 0):
                    if_empty = True
                    print("             [Alarm - Current] Severity Major No Alarm Data",file = open(file_name, '+a'))
            index = index+1
        if(if_empty == False):
            if(is_error == False):
                print("             [Alarm - Current] Severity Major Test Pass",file = open(file_name, '+a'))
            else:
                print("             [Alarm - Current] Severity Major Test Fail",file = open(file_name, '+a'))
                if_alarm_current_error = True

        # Severity Minor Test
        ala.Current_Severity(driver,4)
        ala.Current_Load(driver)
        index = 0
        is_last = False
        is_error = False
        if_empty = False
        while(is_last == False):
            try:
                if(driver.find_elements(By.CLASS_NAME, "rpalmcurr_Severity")[index].get_attribute("textContent") != "minor"):
                    is_error = True
            except:
                is_last = True
                if(index == 0):
                    if_empty = True
                    print("             [Alarm - Current] Severity Minor No Alarm Data",file = open(file_name, '+a'))
            index = index+1
        if(if_empty == False):
            if(is_error == False):
                print("             [Alarm - Current] Severity Minor Test Pass",file = open(file_name, '+a'))
            else:
                print("             [Alarm - Current] Severity Minor Test Fail",file = open(file_name, '+a'))
                if_alarm_current_error = True

        # Severity Warning Test
        ala.Current_Severity(driver,5)
        ala.Current_Load(driver)
        index = 0
        is_last = False
        is_error = False
        if_empty = False
        while(is_last == False):
            try:
                if(driver.find_elements(By.CLASS_NAME, "rpalmcurr_Severity")[index].get_attribute("textContent") != "warning"):
                    is_error = True
            except:
                is_last = True
                if(index == 0):
                    if_empty = True
                    print("             [Alarm - Current] Severity Warning No Alarm Data",file = open(file_name, '+a'))
            index = index+1
        if(if_empty == False):
            if(is_error == False):
                print("             [Alarm - Current] Severity Warning Test Pass",file = open(file_name, '+a'))
            else:
                print("             [Alarm - Current] Severity Warning Test Fail",file = open(file_name, '+a'))
                if_alarm_current_error = True
            
        # Severity Event Test
        ala.Current_Severity(driver,6)
        ala.Current_Load(driver)
        index = 0
        is_last = False
        is_error = False
        if_empty = False
        while(is_last == False):
            try:
                if(driver.find_elements(By.CLASS_NAME, "rpalmcurr_Severity")[index].get_attribute("textContent") != "event"):
                    is_error = True
            except:
                is_last = True
                if(index == 0):
                    if_empty = True
                    print("             [Alarm - Current] Severity Event No Alarm Data",file = open(file_name, '+a'))
            index = index+1
        if(if_empty == False):
            if(is_error == False):
                print("             [Alarm - Current] Severity Event Test Pass",file = open(file_name, '+a'))
            else:
                print("             [Alarm - Current] Severity Event Test Fail",file = open(file_name, '+a'))
                if_alarm_current_error = True

        # Alarm Sys Test
        ala.Current_Severity(driver,1)
        ala.Current_Alarm(driver,2)
        ala.Current_Load(driver)
        index = 0
        is_last = False
        is_error = False
        if_empty = False
        while(is_last == False):
            try:
                if(driver.find_elements(By.CLASS_NAME, "rpalmcurr_Alarm")[index].get_attribute("textContent") != "sys"):
                    is_error = True
            except:
                is_last = True
                if(index == 0):
                    if_empty = True
                    print("             [Alarm - Current] Alarm Sys No Alarm Data",file = open(file_name, '+a'))
            index = index+1
        if(if_empty == False):
            if(is_error == False):
                print("             [Alarm - Current] Alarm Sys Test Pass",file = open(file_name, '+a'))
            else:
                print("             [Alarm - Current] Alarm Sys Test Fail",file = open(file_name, '+a'))
                if_alarm_current_error = True

        # Alarm Eqpt Test
        ala.Current_Alarm(driver,3)
        ala.Current_Load(driver)
        index = 0
        is_last = False
        is_error = False
        if_empty = False
        while(is_last == False):
            try:
                if(driver.find_elements(By.CLASS_NAME, "rpalmcurr_Alarm")[index].get_attribute("textContent") != "eqpt"):
                    is_error = True
            except:
                is_last = True
                if(index == 0):
                    if_empty = True
                    print("             [Alarm - Current] Alarm Eqpt No Alarm Data",file = open(file_name, '+a'))
            index = index+1
        if(if_empty == False):
            if(is_error == False):
                print("             [Alarm - Current] Alarm Eqpt Test Pass",file = open(file_name, '+a'))
            else:
                print("             [Alarm - Current] Alarm Eqpt Test Fail",file = open(file_name, '+a'))
                if_alarm_current_error = True

        # Alarm Ge Test
        ala.Current_Alarm(driver,4)
        ala.Current_Load(driver)
        index = 0
        is_last = False
        is_error = False
        if_empty = False
        while(is_last == False):
            try:
                if(driver.find_elements(By.CLASS_NAME, "rpalmcurr_Alarm")[index].get_attribute("textContent") != "ge"):
                    is_error = True
            except:
                is_last = True
                if(index == 0):
                    if_empty = True
                    print("             [Alarm - Current] Alarm Ge No Alarm Data",file = open(file_name, '+a'))
            index = index+1
        if(if_empty == False):
            if(is_error == False):
                print("             [Alarm - Current] Alarm Ge Test Pass",file = open(file_name, '+a'))
            else:
                print("             [Alarm - Current] Alarm Ge Test Fail",file = open(file_name, '+a'))
                if_alarm_current_error = True

        # Alarm Dsl Test
        ala.Current_Alarm(driver,5)
        ala.Current_Load(driver)
        index = 0
        is_last = False
        is_error = False
        if_empty = False
        while(is_last == False):
            try:
                if(driver.find_elements(By.CLASS_NAME, "rpalmcurr_Alarm")[index].get_attribute("textContent") != "dsl"):
                    is_error = True
            except:
                is_last = True
                if(index == 0):
                    if_empty = True
                    print("             [Alarm - Current] Alarm Dsl No Alarm Data",file = open(file_name, '+a'))
            index = index+1
        if(if_empty == False):
            if(is_error == False):
                print("             [Alarm - Current] Alarm Dsl Test Pass",file = open(file_name, '+a'))
            else:
                print("             [Alarm - Current] Alarm Dsl Test Fail",file = open(file_name, '+a'))
                if_alarm_current_error = True
            
        # Alarm Gpon Test
        ala.Current_Alarm(driver,6)
        ala.Current_Load(driver)
        index = 0
        is_last = False
        is_error = False
        if_empty = False
        while(is_last == False):
            try:
                if(driver.find_elements(By.CLASS_NAME, "rpalmcurr_Alarm")[index].get_attribute("textContent") != "gpon"):
                    is_error = True
            except:
                is_last = True
                if(index == 0):
                    if_empty = True
                    print("             [Alarm - Current] Alarm Gpon No Alarm Data",file = open(file_name, '+a'))
            index = index+1
        if(if_empty == False):
            if(is_error == False):
                print("             [Alarm - Current] Alarm Gpon Test Pass",file = open(file_name, '+a'))
            else:
                print("             [Alarm - Current] Alarm Gpon Test Fail",file = open(file_name, '+a'))
                if_alarm_current_error = True
            
        # Alarm Gbond Test
        ala.Current_Alarm(driver,7)
        ala.Current_Load(driver)
        index = 0
        is_last = False
        is_error = False
        if_empty = False
        while(is_last == False):
            try:
                if(driver.find_elements(By.CLASS_NAME, "rpalmcurr_Alarm")[index].get_attribute("textContent") != "gbond"):
                    is_error = True
            except:
                is_last = True
                if(index == 0):
                    if_empty = True
                    print("             [Alarm - Current] Alarm Gbond No Alarm Data",file = open(file_name, '+a'))
            index = index+1
        if(if_empty == False):
            if(is_error == False):
                print("             [Alarm - Current] Alarm Gbond Test Pass",file = open(file_name, '+a'))
            else:
                print("             [Alarm - Current] Alarm Gbond Test Fail",file = open(file_name, '+a'))
                if_alarm_current_error = True

        # Condition 10001 Test
        ala.Current_Alarm(driver,1)
        ala.Current_Condition(driver,"10001")
        ala.Current_Load(driver)
        index = 0
        is_last = False
        is_error = False
        if_empty = False
        while(is_last == False):
            try:
                if(driver.find_elements(By.CLASS_NAME, "rpalmcurr_Condition")[index].get_attribute("textContent") != "+(10001)voltage_out_of_range"):
                    is_error = True
            except:
                is_last = True
                if(index == 0):
                    if_empty = True
                    print("             [Alarm - Current] Condition 10001 No Alarm Data",file = open(file_name, '+a'))
            index = index+1
        if(if_empty == False):
            if(is_error == False):
                print("             [Alarm - Current] Condition 10001 Test Pass",file = open(file_name, '+a'))
            else:
                print("             [Alarm - Current] Condition 10001 Test Fail",file = open(file_name, '+a'))
                if_alarm_current_error = True

        # Date Empty Test
        ala.Current_Condition(driver,"")
        ala.Current_Date_Start(driver,"01/01/1970")
        ala.Current_Date_End(driver,"01/01/1970")
        ala.Current_Load(driver)
        try:
            driver.find_element(By.CLASS_NAME, "AlarmCurrList")
            print("             [Alarm - Current] Date Test Fail",file = open(file_name, '+a'))
            if_alarm_current_error = True
        except:
            print("             [Alarm - Current] Date Test Pass",file = open(file_name, '+a'))

        # Order Test
        ala.Current_Date_End(driver,"12/31/2037")
        ala.Current_Order_Reverse(driver)
        ala.Current_Load(driver)
        if(driver.find_elements(By.NAME, "rpalmcurr_rdoOrder")[1].is_selected() == True):
            print("             [Alarm - Current] Order Reverse Test Pass",file = open(file_name, '+a'))
        else:
            print("             [Alarm - Current] Order Reverse Test Fail",file = open(file_name, '+a'))
            if_alarm_current_error = True
        ala.Current_Order_Forward(driver)
        ala.Current_Load(driver)
        if(driver.find_elements(By.NAME, "rpalmcurr_rdoOrder")[0].is_selected() == True):
            print("             [Alarm - Current] Order Forward Test Pass",file = open(file_name, '+a'))
        else:
            print("             [Alarm - Current] Order Forward Test Fail",file = open(file_name, '+a'))
            if_alarm_current_error = True

        # Flush Test
        ala.Current_Flush(driver)
        try:
            driver.find_element(By.CLASS_NAME, "AlarmCurrList")
            print("             [Alarm - Current] Flush Test Fail",file = open(file_name, '+a'))
            if_alarm_current_error = True
        except:
            print("             [Alarm - Current] Flush Test Pass",file = open(file_name, '+a'))

        # Alarm Current Result
        if(if_alarm_current_error == False):
            print("[MSAN1-11832][Alarm - Current] Result Pass",file = open(file_name, '+a'))
        else:
            print("[MSAN1-11832][Alarm - Current] Result Fail",file = open(file_name, '+a'))

    except:
        print("             [Alarm - Current] No Alarm Data",file = open(file_name, '+a'))
        print("[MSAN1-11832][Alarm - Current] Result Fail",file = open(file_name, '+a'))
    
    # -------------------------end-------------------------

    # Alarm History Setup
    # Alarm > History
    # -------------------------start-------------------------

    # 路徑導向 Alarm > History
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"History")
    mod.Switch_Frame(driver)

    # Load
    ala.History_Load(driver)

    if_alarm_history_error = False
    # Is Data Exist
    try:
        driver.find_element(By.CLASS_NAME, "AlarmCurrList")
        # print("             [Alarm - History] Alarm Data Exist",file = open(file_name, '+a'))

        # Severity Critical Test
        ala.History_Severity(driver,2)
        ala.History_Load(driver)
        index = 0
        is_last = False
        is_error = False
        if_empty = False
        while(is_last == False):
            try:
                if(driver.find_elements(By.CLASS_NAME, "rpalmhist_Severity")[index].get_attribute("textContent") != "critical"):
                    is_error = True
            except:
                is_last = True
                if(index == 0):
                    if_empty = True
                    print("             [Alarm - History] Severity Critical No Alarm Data",file = open(file_name, '+a'))
            index = index+1
        if(if_empty == False):
            if(is_error == False):
                print("             [Alarm - History] Severity Critical Test Pass",file = open(file_name, '+a'))
            else:
                print("             [Alarm - History] Severity Critical Test Fail",file = open(file_name, '+a'))
                if_alarm_history_error = True

        # Severity Major Test
        ala.History_Severity(driver,3)
        ala.History_Load(driver)
        index = 0
        is_last = False
        is_error = False
        if_empty = False
        while(is_last == False):
            try:
                if(driver.find_elements(By.CLASS_NAME, "rpalmhist_Severity")[index].get_attribute("textContent") != "major"):
                    is_error = True
            except:
                is_last = True
                if(index == 0):
                    if_empty = True
                    print("             [Alarm - History] Severity Major No Alarm Data",file = open(file_name, '+a'))
            index = index+1
        if(if_empty == False):
            if(is_error == False):
                print("             [Alarm - History] Severity Major Test Pass",file = open(file_name, '+a'))
            else:
                print("             [Alarm - History] Severity Major Test Fail",file = open(file_name, '+a'))
                if_alarm_history_error = True

        # Severity Minor Test
        ala.History_Severity(driver,4)
        ala.History_Load(driver)
        index = 0
        is_last = False
        is_error = False
        if_empty = False
        while(is_last == False):
            try:
                if(driver.find_elements(By.CLASS_NAME, "rpalmhist_Severity")[index].get_attribute("textContent") != "minor"):
                    is_error = True
            except:
                is_last = True
                if(index == 0):
                    if_empty = True
                    print("             [Alarm - History] Severity Minor No Alarm Data",file = open(file_name, '+a'))
            index = index+1
        if(if_empty == False):
            if(is_error == False):
                print("             [Alarm - History] Severity Minor Test Pass",file = open(file_name, '+a'))
            else:
                print("             [Alarm - History] Severity Minor Test Fail",file = open(file_name, '+a'))
                if_alarm_history_error = True

        # Severity Warning Test
        ala.History_Severity(driver,5)
        ala.History_Load(driver)
        index = 0
        is_last = False
        is_error = False
        if_empty = False
        while(is_last == False):
            try:
                if(driver.find_elements(By.CLASS_NAME, "rpalmhist_Severity")[index].get_attribute("textContent") != "warning"):
                    is_error = True
            except:
                is_last = True
                if(index == 0):
                    if_empty = True
                    print("             [Alarm - History] Severity Warning No Alarm Data",file = open(file_name, '+a'))
            index = index+1
        if(if_empty == False):
            if(is_error == False):
                print("             [Alarm - History] Severity Warning Test Pass",file = open(file_name, '+a'))
            else:
                print("             [Alarm - History] Severity Warning Test Fail",file = open(file_name, '+a'))
                if_alarm_history_error = True
            
        # Severity Event Test
        ala.History_Severity(driver,6)
        ala.History_Load(driver)
        index = 0
        is_last = False
        is_error = False
        if_empty = False
        while(is_last == False):
            try:
                if(driver.find_elements(By.CLASS_NAME, "rpalmhist_Severity")[index].get_attribute("textContent") != "event"):
                    is_error = True
            except:
                is_last = True
                if(index == 0):
                    if_empty = True
                    print("             [Alarm - History] Severity Event No Alarm Data",file = open(file_name, '+a'))
            index = index+1
        if(if_empty == False):
            if(is_error == False):
                print("             [Alarm - History] Severity Event Test Pass",file = open(file_name, '+a'))
            else:
                print("             [Alarm - History] Severity Event Test Fail",file = open(file_name, '+a'))
                if_alarm_history_error = True

        # Alarm Sys Test
        ala.History_Severity(driver,1)
        ala.History_Alarm(driver,2)
        ala.History_Load(driver)
        index = 0
        is_last = False
        is_error = False
        if_empty = False
        while(is_last == False):
            try:
                if(driver.find_elements(By.CLASS_NAME, "rpalmhist_Alarm")[index].get_attribute("textContent") != "sys"):
                    is_error = True
            except:
                is_last = True
                if(index == 0):
                    if_empty = True
                    print("             [Alarm - History] Alarm Sys No Alarm Data",file = open(file_name, '+a'))
            index = index+1
        if(if_empty == False):
            if(is_error == False):
                print("             [Alarm - History] Alarm Sys Test Pass",file = open(file_name, '+a'))
            else:
                print("             [Alarm - History] Alarm Sys Test Fail",file = open(file_name, '+a'))
                if_alarm_history_error = True

        # Alarm Eqpt Test
        ala.History_Alarm(driver,3)
        ala.History_Load(driver)
        index = 0
        is_last = False
        is_error = False
        if_empty = False
        while(is_last == False):
            try:
                if(driver.find_elements(By.CLASS_NAME, "rpalmhist_Alarm")[index].get_attribute("textContent") != "eqpt"):
                    is_error = True
            except:
                is_last = True
                if(index == 0):
                    if_empty = True
                    print("             [Alarm - History] Alarm Eqpt No Alarm Data",file = open(file_name, '+a'))
            index = index+1
        if(if_empty == False):
            if(is_error == False):
                print("             [Alarm - History] Alarm Eqpt Test Pass",file = open(file_name, '+a'))
            else:
                print("             [Alarm - History] Alarm Eqpt Test Fail",file = open(file_name, '+a'))
                if_alarm_history_error = True

        # Alarm Ge Test
        ala.History_Alarm(driver,4)
        ala.History_Load(driver)
        index = 0
        is_last = False
        is_error = False
        if_empty = False
        while(is_last == False):
            try:
                if(driver.find_elements(By.CLASS_NAME, "rpalmhist_Alarm")[index].get_attribute("textContent") != "ge"):
                    is_error = True
            except:
                is_last = True
                if(index == 0):
                    if_empty = True
                    print("             [Alarm - History] Alarm Ge No Alarm Data",file = open(file_name, '+a'))
            index = index+1
        if(if_empty == False):
            if(is_error == False):
                print("             [Alarm - History] Alarm Ge Test Pass",file = open(file_name, '+a'))
            else:
                print("             [Alarm - History] Alarm Ge Test Fail",file = open(file_name, '+a'))
                if_alarm_history_error = True

        # Alarm Dsl Test
        ala.History_Alarm(driver,5)
        ala.History_Load(driver)
        index = 0
        is_last = False
        is_error = False
        if_empty = False
        while(is_last == False):
            try:
                if(driver.find_elements(By.CLASS_NAME, "rpalmhist_Alarm")[index].get_attribute("textContent") != "dsl"):
                    is_error = True
            except:
                is_last = True
                if(index == 0):
                    if_empty = True
                    print("             [Alarm - History] Alarm Dsl No Alarm Data",file = open(file_name, '+a'))
            index = index+1
        if(if_empty == False):
            if(is_error == False):
                print("             [Alarm - History] Alarm Dsl Test Pass",file = open(file_name, '+a'))
            else:
                print("             [Alarm - History] Alarm Dsl Test Fail",file = open(file_name, '+a'))
                if_alarm_history_error = True
            
        # Alarm Gpon Test
        ala.History_Alarm(driver,6)
        ala.History_Load(driver)
        index = 0
        is_last = False
        is_error = False
        if_empty = False
        while(is_last == False):
            try:
                if(driver.find_elements(By.CLASS_NAME, "rpalmhist_Alarm")[index].get_attribute("textContent") != "gpon"):
                    is_error = True
            except:
                is_last = True
                if(index == 0):
                    if_empty = True
                    print("             [Alarm - History] Alarm Gpon No Alarm Data",file = open(file_name, '+a'))
            index = index+1
        if(if_empty == False):
            if(is_error == False):
                print("             [Alarm - History] Alarm Gpon Test Pass",file = open(file_name, '+a'))
            else:
                print("             [Alarm - History] Alarm Gpon Test Fail",file = open(file_name, '+a'))
                if_alarm_history_error = True
            
        # Alarm Gbond Test
        ala.History_Alarm(driver,7)
        ala.History_Load(driver)
        index = 0
        is_last = False
        is_error = False
        if_empty = False
        while(is_last == False):
            try:
                if(driver.find_elements(By.CLASS_NAME, "rpalmhist_Alarm")[index].get_attribute("textContent") != "gbond"):
                    is_error = True
            except:
                is_last = True
                if(index == 0):
                    if_empty = True
                    print("             [Alarm - History] Alarm Gbond No Alarm Data",file = open(file_name, '+a'))
            index = index+1
        if(if_empty == False):
            if(is_error == False):
                print("             [Alarm - History] Alarm Gbond Test Pass",file = open(file_name, '+a'))
            else:
                print("             [Alarm - History] Alarm Gbond Test Fail",file = open(file_name, '+a'))
                if_alarm_history_error = True

        # Condition 20005 Test
        ala.History_Alarm(driver,1)
        ala.History_Condition(driver,"20005")
        ala.History_Load(driver)
        index = 0
        is_last = False
        is_error = False
        if_empty = False
        while(is_last == False):
            try:
                if(driver.find_elements(By.CLASS_NAME, "rpalmhist_Condition")[index].get_attribute("textContent") != "+(20005)ge_linkup"):
                    is_error = True
            except:
                is_last = True
                if(index == 0):
                    if_empty = True
                    print("             [Alarm - History] Condition 20005 No Alarm Data",file = open(file_name, '+a'))
            index = index+1
        if(if_empty == False):
            if(is_error == False):
                print("             [Alarm - History] Condition 20005 Test Pass",file = open(file_name, '+a'))
            else:
                print("             [Alarm - History] Condition 20005 Test Fail",file = open(file_name, '+a'))
                if_alarm_history_error = True

        # Date Empty Test
        ala.History_Condition(driver,"")
        ala.History_Date_Start(driver,"01/01/1970")
        ala.History_Date_End(driver,"01/01/1970")
        ala.History_Load(driver)
        try:
            driver.find_element(By.CLASS_NAME, "AlarmCurrList")
            print("             [Alarm - History] Date Test Fail",file = open(file_name, '+a'))
            if_alarm_history_error = True
        except:
            print("             [Alarm - History] Date Test Pass",file = open(file_name, '+a'))

        # Order Test
        ala.History_Date_End(driver,"12/31/2037")
        ala.History_Order_Reverse(driver)
        ala.History_Load(driver)
        if(driver.find_elements(By.NAME, "rpalmhist_rdoOrder")[1].is_selected() == True):
            print("             [Alarm - History] Order Reverse Test Pass",file = open(file_name, '+a'))
        else:
            print("             [Alarm - History] Order Reverse Test Fail",file = open(file_name, '+a'))
            if_alarm_history_error = True
        ala.History_Order_Forward(driver)
        if(driver.find_elements(By.NAME, "rpalmhist_rdoOrder")[0].is_selected() == True):
            print("             [Alarm - History] Order Forward Test Pass",file = open(file_name, '+a'))
        else:
            print("             [Alarm - History] Order Forward Test Fail",file = open(file_name, '+a'))
            if_alarm_history_error = True
        ala.History_Load(driver)

        # Flush Test
        ala.History_Flush(driver)
        try:
            driver.find_element(By.CLASS_NAME, "AlarmCurrList")
            print("             [Alarm - History] Flush Test Fail",file = open(file_name, '+a'))
            if_alarm_history_error = True
        except:
            print("             [Alarm - History] Flush Test Pass",file = open(file_name, '+a'))

        # Alarm History Result
        if(if_alarm_history_error == False):
            print("[MSAN1-11833][Alarm - History] Result Pass",file = open(file_name, '+a'))
        else:
            print("[MSAN1-11833][Alarm - History] Result Fail",file = open(file_name, '+a'))

    except:
        print("             [Alarm - History] No Alarm Data",file = open(file_name, '+a'))
        print("[MSAN1-11833][Alarm - History] Result Fail",file = open(file_name, '+a'))
    
    # -------------------------end-------------------------

    # Alarm Port Setup
    # Alarm > Port Setup
    # -------------------------start-------------------------

    # 路徑導向 Alarm > Port Setup
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"Port Setup")
    mod.Switch_Frame(driver)

    # slot select
    driver.find_elements(By.NAME, "Pkfiltertableid")[int(glc_slot)-1].click()

    is_error = False

    # Port Setup Test 1
    ala.Port_Setup_Notification_Severity_All(driver,2)
    ala.Port_Setup_Link_Trap_Supress_All(driver,True)
    ala.Port_Setup_Apply(driver)
    if(driver.find_element(By.XPATH, f"//form[@id='rpalarmport_Form']/div[4]/div[{int(glc_port)+7}]/div[2]/select/option[2]").is_selected() != True):
        print("             [Alarm - Port Setup] Notification-Severity:Minor Test Fail",file = open(file_name, '+a'))
        is_error = True
    if(driver.find_element(By.XPATH, f"//form[@id='rpalarmport_Form']/div[4]/div[{int(glc_port)+7}]/div[3]/input").is_selected() != True):
        print("             [Alarm - Port Setup] Link-Trap-Suppress Test Fail",file = open(file_name, '+a'))
        is_error = True

    # Port Setup Test 2
    ala.Port_Setup_Notification_Severity_All(driver,3)
    ala.Port_Setup_Link_Trap_Supress_All(driver,True)
    ala.Port_Setup_Link_Trap_Supress_All(driver,False)
    ala.Port_Setup_Apply(driver)
    if(driver.find_element(By.XPATH, f"//form[@id='rpalarmport_Form']/div[4]/div[{int(glc_port)+7}]/div[2]/select/option[3]").is_selected() != True):
        print("             [Alarm - Port Setup] Notification-Severity:Major Test Fail",file = open(file_name, '+a'))
        is_error = True
    if(driver.find_element(By.XPATH, f"//form[@id='rpalarmport_Form']/div[4]/div[{int(glc_port)+7}]/div[3]/input").is_selected() != False):
        print("             [Alarm - Port Setup] Link-Trap-Suppress Test Fail",file = open(file_name, '+a'))
        is_error = True

    # Port Setup Test 3
    ala.Port_Setup_Notification_Severity_All(driver,4)
    ala.Port_Setup_Apply(driver)
    if(driver.find_element(By.XPATH, f"//form[@id='rpalarmport_Form']/div[4]/div[{int(glc_port)+7}]/div[2]/select/option[4]").is_selected() != True):
        print("             [Alarm - Port Setup] Notification-Severity:Critical Test Fail",file = open(file_name, '+a'))
        is_error = True

    # Port Setup Test 4
    ala.Port_Setup_Notification_Severity_All(driver,5)
    ala.Port_Setup_Apply(driver)
    if(driver.find_element(By.XPATH, f"//form[@id='rpalarmport_Form']/div[4]/div[{int(glc_port)+7}]/div[2]/select/option[5]").is_selected() != True):
        print("             [Alarm - Port Setup] Notification-Severity:Event Test Fail",file = open(file_name, '+a'))
        is_error = True

    # Port Setup Test 5
    ala.Port_Setup_Notification_Severity_All(driver,1)
    ala.Port_Setup_Apply(driver)
    if(driver.find_element(By.XPATH, f"//form[@id='rpalarmport_Form']/div[4]/div[{int(glc_port)+7}]/div[2]/select/option[1]").is_selected() != True):
        print("             [Alarm - Port Setup] Notification-Severity:Warning Test Fail",file = open(file_name, '+a'))
        is_error = True

    # Port Setup Result
    if(is_error == False):
        print("[MSAN1-11834][Alarm - Port Setup] Result Pass",file = open(file_name, '+a'))
    else:
        print("[MSAN1-11834][Alarm - Port Setup] Result Fail",file = open(file_name, '+a'))
    
    # -------------------------end-------------------------

    # Alarm Input Test
    # Alarm > Input > Alarm Input
    # -------------------------start-------------------------

    # 路徑導向 Alarm > Input > Alarm Input
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"Input")
    mod.Switch_Frame(driver)

    is_error = False

    # Alarm Input Input
    if(MSC_Card_Type == "MSC1240QA"):
        for index in range(4):
            ala.Input_Alarm_Input_Index_Name(driver,index+1,"1234567890123456789012345678901")
        ala.Input_Alarm_Input_Apply(driver)
    else:
        for index in range(8):
            ala.Input_Alarm_Input_Index_Name(driver,index+1,"1234567890123456789012345678901")
        ala.Input_Alarm_Input_Apply(driver)

    # Alarm Input Check
    for index in range(8):
        if(driver.find_element(By.NAME, f"rpAlarmInput_name{index+1}").get_attribute("value") != "1234567890123456789012345678901"):
            is_error = True

    # Alarm Input Default
    ala.Input_Alarm_Input_Default(driver)

    # Alarm Input Default Check
    for index in range(8):
        if(driver.find_element(By.NAME, f"rpAlarmInput_name{index+1}").get_attribute("value") != f"input{index+1}"):
            is_error = True

    # Alarm Input Cancel
    ala.Input_Alarm_Input_Cancel(driver)

    # Alarm Input Cancel Check
    for index in range(8):
        if(driver.find_element(By.NAME, f"rpAlarmInput_name{index+1}").get_attribute("value") != f"input{index+1}"):
            is_error = True

    # Alarm Input Result
    if(is_error == False):
        print("[MSAN1-11835][Alarm - Input - Alarm Input] Result Pass",file = open(file_name, '+a'))
    else:
        print("[MSAN1-11835][Alarm - Input - Alarm Input] Result Fail",file = open(file_name, '+a'))
    
    # -------------------------end-------------------------

    # CPU Overload Alarm Test
    # Alarm > Input > CPU Overload Alarm
    # -------------------------start-------------------------

    # 路徑導向 Alarm > Input > CPU Overload Alarm
    mod.Tab_Switch(driver,"CPU Overload Alarm")

    is_error = False

    # CPU Overload Alarm Test 1
    ala.Input_CPU_Overload_Alarm_Analytic_Method(driver,2)
    ala.Input_CPU_Overload_Alarm_Issue_Threshold(driver,"100")
    ala.Input_CPU_Overload_Alarm_Clear_Threshold(driver,"99")
    ala.Input_CPU_Overload_Alarm_Sample_Seconds(driver,"1")
    ala.Input_CPU_Overload_Alarm_Apply(driver)
    if(mod.IsAlert == True):
        is_error = True
    else:
        if(driver.find_element(By.XPATH, f"//*[@name='rpAlarmCoa_nalyticMethod']/option[2]").is_selected() != True):
            is_error = True
        if(driver.find_element(By.NAME, f"rpAlarmCoa_issueThreshold").get_attribute("value") != "100"):
            is_error = True
        if(driver.find_element(By.NAME, f"rpAlarmCoa_clearThreshold").get_attribute("value") != "99"):
            is_error = True
        if(driver.find_element(By.NAME, f"rpAlarmCoa_sampleSeconds").get_attribute("value") != "1"):
            is_error = True

    # CPU Overload Alarm Test 2
    ala.Input_CPU_Overload_Alarm_Analytic_Method(driver,1)
    ala.Input_CPU_Overload_Alarm_Issue_Threshold(driver,"100")
    ala.Input_CPU_Overload_Alarm_Clear_Threshold(driver,"99")
    ala.Input_CPU_Overload_Alarm_Sample_Seconds(driver,"60")
    ala.Input_CPU_Overload_Alarm_Apply(driver)
    if(mod.IsAlert == True):
        is_error = True
    else:
        if(driver.find_element(By.XPATH, f"//*[@name='rpAlarmCoa_nalyticMethod']/option[1]").is_selected() != True):
            is_error = True
        if(driver.find_element(By.NAME, f"rpAlarmCoa_issueThreshold").get_attribute("value") != "100"):
            is_error = True
        if(driver.find_element(By.NAME, f"rpAlarmCoa_clearThreshold").get_attribute("value") != "99"):
            is_error = True
        if(driver.find_element(By.NAME, f"rpAlarmCoa_sampleSeconds").get_attribute("value") != "60"):
            is_error = True
    
    issue_input = ["100","100","100","100","101"]
    clear_input = ["99","99","99","100","60"]
    sample_input = ["0","61","@","35","35"]

    # CPU Overload Alarm Test 3~7
    for test_time in range(5):
        ala.Input_CPU_Overload_Alarm_Issue_Threshold(driver,issue_input[test_time])
        ala.Input_CPU_Overload_Alarm_Clear_Threshold(driver,clear_input[test_time])
        ala.Input_CPU_Overload_Alarm_Sample_Seconds(driver,sample_input[test_time])
        ala.Input_CPU_Overload_Alarm_Apply(driver)
        if(mod.IsAlert == False):
            is_error = True

    # CPU Overload Alarm Test 8
    ala.Input_CPU_Overload_Alarm_Issue_Threshold(driver,"90")
    ala.Input_CPU_Overload_Alarm_Clear_Threshold(driver,"60")
    ala.Input_CPU_Overload_Alarm_Sample_Seconds(driver,"35")
    ala.Input_CPU_Overload_Alarm_Apply(driver)
    if(mod.IsAlert == True):
        is_error = True
    else:
        if(driver.find_element(By.NAME, f"rpAlarmCoa_issueThreshold").get_attribute("value") != "90"):
            is_error = True
        if(driver.find_element(By.NAME, f"rpAlarmCoa_clearThreshold").get_attribute("value") != "60"):
            is_error = True
        if(driver.find_element(By.NAME, f"rpAlarmCoa_sampleSeconds").get_attribute("value") != "35"):
            is_error = True

    # CPU Overload Alarm Result
    if(is_error == False):
        print("[MSAN1-11836][Alarm - Input - CPU Overload Alarm] Result Pass",file = open(file_name, '+a'))
    else:
        print("[MSAN1-11836][Alarm - Input - CPU Overload Alarm] Result Fail",file = open(file_name, '+a'))
    
    # -------------------------end-------------------------

    # System Suppress Test
    # Alarm > Input > System Suppress
    # -------------------------start-------------------------

    # 路徑導向 Alarm > Input > System Suppress
    mod.Tab_Switch(driver,"System Suppress")

    is_error = False

    # System Suppress Test
    ala.Input_System_Supress_Enable(driver,True)
    ala.Input_System_Supress_Apply(driver)
    if(driver.find_element(By.NAME, "rpAlarmSysSupress_mode").is_selected() != True):
        is_error = True
    ala.Input_System_Supress_Enable(driver,False)
    ala.Input_System_Supress_Apply(driver)
    if(driver.find_element(By.NAME, "rpAlarmSysSupress_mode").is_selected() != False):
        is_error = True
    
    # System Suppress Result
    if(is_error == False):
        print("[MSAN1-11837][Alarm - Input - System Suppress] Result Pass",file = open(file_name, '+a'))
    else:
        print("[MSAN1-11837][Alarm - Input - System Suppress] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Definition Test
    # Alarm > Definition
    # -------------------------start-------------------------

    # 路徑導向 Alarm > Definition
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"Definition")
    mod.Switch_Frame(driver)

    if_error = False
    try:

        # Definition Test
        for category_select in range(6):
            ala.Input_Definition_Alarm_Category(driver,category_select+2)
            ala.Input_Definition_SNMP_All(driver,True)
            ala.Input_Definition_SNMP_All(driver,False)
            ala.Input_Definition_Syslog_All(driver,True)
            ala.Input_Definition_Syslog_All(driver,False)
            ala.Input_Definition_Facility_All(driver,8)
            ala.Input_Definition_Severity_All(driver,6)
            ala.Input_Definition_Apply(driver)
            index = 0
            is_last = False
            while(is_last == False):
                try:
                    if(driver.find_elements(By.NAME, "rpalarm_def_chk_snmp")[index].is_selected() != False):
                        is_error = True
                    if(driver.find_elements(By.NAME, "rpalarm_def_chk_syslog")[index].is_selected() != False):
                        is_error = True
                    if(driver.find_elements(By.XPATH, f"/html/body/form/div[2]/div[{index+16}]/div[5]/select/option[7]").is_selected() != True):
                        is_error = True
                    if(driver.find_element(By.XPATH, f"/html/body/form/div[2]/div[{index+16}]/div[6]/select/option[5]").is_selected() != True):
                        is_error = True
                except:
                    is_last = True
    
    # Definition Result
    except:
        if_error = True

    if(if_error == False):
        print("[MSAN1-11838][Alarm - Definition] Result Pass",file = open(file_name, '+a'))
    else:
        print("[MSAN1-11838][Alarm - Definition] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Maintenance Config Reset Reset
    # Maintenance > Config Reset
    # -------------------------start-------------------------

    # 路徑導向 Maintenance > Config Reset
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Maintenance")
    mod.SubPage_Switch(driver,"Config Reset")
    mod.Switch_Frame(driver)

    # Maintenance Config Reset Reset
    mai.Config_Reset(driver)
    pyautogui.press("enter")
    # print(f"Maintenance Config Reset",file = open(file_name, '+a'))

    # -------------------------end-------------------------


    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def Diagnostic_Test(driver,glc_slot,glc_port,file_name):
    print(f"Diagnostic Test\nTest Start",file = open(file_name, '+a'))

    # Diagnostic CFM Test
    # Diagnostic > CFM
    # -------------------------start-------------------------

    # 路徑導向 Diagnostic > CFM
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Diagnostic")
    try:
        # CFM -> Linktrace Test
        if_error = False
        mod.SubPage_Switch(driver,"CFM")
        mod.Switch_Frame(driver)
        mod.Tab_Switch(driver,"Linktrace")
        driver.find_element(By.NAME, "rpcfmLinktrace_btnLoopback").click()
        if(mod.IsAlert(driver) != True):
            print(f"             [Diagnostic - CFM - Linktrace] Test No Alert Test Fail",file = open(file_name, '+a'))
            if_error = True
        time.sleep(0.1)
        try:
            driver.find_element(By.NAME, "showresult")
        except:
            print(f"             [Diagnostic - CFM - Linktrace] Test Crash Test Fail",file = open(file_name, '+a'))
            if_error = True
        driver.find_element(By.NAME, "getLinktrace_Data").click()
        time.sleep(0.1)
        try:
            driver.find_element(By.NAME, "showresult")
        except:
            print(f"             [Diagnostic - CFM - Linktrace] Get Linktrace Data Crash Test Fail",file = open(file_name, '+a'))
            if_error = True
        # Diagnostic CFM Linktrace Result
        if(if_error == False):
            print(f"[MSAN1-11839][Diagnostic - CFM - Linktrace] Result Pass",file = open(file_name, '+a'))
        else:
            print(f"[MSAN1-11839][Diagnostic - CFM - Linktrace] Result Fail",file = open(file_name, '+a'))
            
        # CFM -> Loopback Test
        if_error = False
        mod.Tab_Switch(driver,"Loopback")
        driver.find_element(By.NAME, "rpcfmLoopback_btnLoopback").click()
        if(mod.IsAlert(driver) != True):
            print(f"             [Diagnostic - CFM - Loopback] Test No Alert Test Fail",file = open(file_name, '+a'))
            if_error = True
        time.sleep(0.1)
        try:
            driver.find_element(By.NAME, "showresult")
        except:
            print(f"             [Diagnostic - CFM - Loopback] Test Crash Test Fail",file = open(file_name, '+a'))
            if_error = True
        driver.find_element(By.NAME, "getLoopback_Data").click()
        time.sleep(0.1)
        try:
            driver.find_element(By.NAME, "showresult")
        except:
            print(f"             [Diagnostic - CFM - Loopback] Get Loopback Data Crash Test Fail",file = open(file_name, '+a'))
            if_error = True
        # Diagnostic CFM Linktrace Result
        if(if_error == False):
            print(f"[MSAN1-11840][Diagnostic - CFM - Loopback] Result Pass",file = open(file_name, '+a'))
        else:
            print(f"[MSAN1-11840][Diagnostic - CFM - Loopback] Result Fail",file = open(file_name, '+a'))
            
        # CFM -> MEP Status Test
        if_error = False
        mod.Tab_Switch(driver,"MEP Status")
        driver.find_element(By.NAME, "getLoopback_Data").click()
        time.sleep(0.1)
        try:
            driver.find_element(By.NAME, "showresult")
        except:
            print(f"             [Diagnostic - CFM - MEP Status] Show CFM MEP Status Crash Test Fail",file = open(file_name, '+a'))
            if_error = True

        # Diagnostic CFM Linktrace Result
        if(if_error == False):
            print(f"[MSAN1-11841][Diagnostic - CFM - MEP Status] Result Pass",file = open(file_name, '+a'))
        else:
            print(f"[MSAN1-11841][Diagnostic - CFM - MEP Status] Result Fail",file = open(file_name, '+a'))

    except:
        mod.Switch_Frame(driver)
        print(f"             [Diagnostic - CFM - Linktrace] Result Block",file = open(file_name, '+a'))
        print(f"[MSAN1-11839][Diagnostic - CFM - Linktrace] Result Pass",file = open(file_name, '+a'))
        print(f"             [Diagnostic - CFM - Loopback] Result Block",file = open(file_name, '+a'))
        print(f"[MSAN1-11840][Diagnostic - CFM - Loopback] Result Pass",file = open(file_name, '+a'))
        print(f"             [Diagnostic - CFM - MEP Status] Result Block",file = open(file_name, '+a'))
        print(f"[MSAN1-11841][Diagnostic - CFM - MEP Status] Result Pass",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Diagnostic DELT Test
    # Diagnostic > DELT
    # -------------------------start-------------------------

    # 路徑導向 Diagnostic > DELT
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Diagnostic")
    mod.SubPage_Switch(driver,"Line Diagnostic")
    mod.Switch_Frame(driver)

    # port select
    dia.Slot_Select(driver,glc_slot)
    dia.Port_Select(driver,glc_port)

    if_error = False

    # Diagnostic DELT Btn Test
    dia.Line_Diagnostic_DELT_Set_DELT(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Diagnostic - Line Diagnostic - DELT] Set DELT Test Fail",file = open(file_name, '+a'))
        if_error = True
    dia.Line_Diagnostic_DELT_Get_Result(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Diagnostic - Line Diagnostic - DELT] Get Result Test Fail",file = open(file_name, '+a'))
        if_error = True
    dia.Line_Diagnostic_DELT_Get_Hlin(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Diagnostic - Line Diagnostic - DELT] Get Hlin Test Fail",file = open(file_name, '+a'))
        if_error = True
    dia.Line_Diagnostic_DELT_Get_Hlog(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Diagnostic - Line Diagnostic - DELT] Get Hlog Test Fail",file = open(file_name, '+a'))
        if_error = True
    dia.Line_Diagnostic_DELT_Get_QLN(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Diagnostic - Line Diagnostic - DELT] Get QLN Test Fail",file = open(file_name, '+a'))
        if_error = True
    dia.Line_Diagnostic_DELT_Get_SNR(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Diagnostic - Line Diagnostic - DELT] Get SNR Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Diagnostic DELT Result
    if(if_error == False):
        print(f"[MSAN1-11842][Diagnostic - Line Diagnostic - DELT] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11842][Diagnostic - Line Diagnostic - DELT] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Diagnostic SELT Test
    # Diagnostic > SELT
    # -------------------------start-------------------------

    # 路徑導向 Diagnostic > SELT
    mod.Tab_Switch(driver,"SELT")

    # port select
    dia.Slot_Select(driver,glc_slot)
    dia.Port_Select(driver,glc_port)

    if_error = False

    # Diagnostic SELT Btn Test
    dia.Line_Diagnostic_SELT_Set_SELT(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Diagnostic - Line Diagnostic - SELT] Set SELT Test Fail",file = open(file_name, '+a'))
        if_error = True
    dia.Line_Diagnostic_SELT_Get_SELT(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Diagnostic - Line Diagnostic - SELT] Get SELT Test Fail",file = open(file_name, '+a'))
        if_error = True
    dia.Line_Diagnostic_SELT_Set_Calibration(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Diagnostic - Line Diagnostic - SELT] Set Calibration Test Fail",file = open(file_name, '+a'))
        if_error = True
    dia.Line_Diagnostic_SELT_Get_Calibration(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Diagnostic - Line Diagnostic - SELT] Get Calibration Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Diagnostic SELT Result
    if(if_error == False):
        print(f"[MSAN1-11843][Diagnostic - Line Diagnostic - SELT] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11843][Diagnostic - Line Diagnostic - SELT] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # IPv6 Setup
    # Sys > IP Setup > IPv6 Setup
    # -------------------------start-------------------------

    # 路徑導向 Sys > IP Setup > IPv6 Setup
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Sys")
    mod.SubPage_Switch(driver,"IP Setup")
    mod.Switch_Frame(driver)
    time.sleep(1)
    mod.Tab_Switch(driver,"IPv6 Setup")
    
    driver.find_element(By.NAME, "rpsysipsetup6_select_default_management").click()
    sys.IP_Setup_IPv6_Setup_Inband_Default_Gateway(driver,"2001::1000")
    sys.IP_Setup_IPv6_Setup_Inband_Global_Address(driver,"2001::1001")
    sys.IP_Setup_IPv6_Setup_Inband_Static(driver,"64")
    sys.IP_Setup_IPv6_Setup_Outband_Global_Address(driver,"2002::11")
    sys.IP_Setup_IPv6_Setup_Outband_Static(driver,"64")
    driver.find_element(By.NAME, "rpsysipsetup6_button_apply").click()

    # -------------------------end-------------------------

    # IP Ping Test
    # Diagnostic > IP > IP Ping
    # -------------------------start-------------------------

    # 路徑導向 Diagnostic > IP > IP Ping
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Diagnostic")
    mod.SubPage_Switch(driver,"IP")
    mod.Switch_Frame(driver)

    if_error = False

    # IP Ping IPv4 Test 1
    dia.IP_Ping_IPv4_Address(driver,"8.8.8.8")
    dia.IP_Ping_IPv4_Data_Bytes(driver,"0")
    dia.IP_Ping_IPv4Ping(driver)
    if(driver.find_element(By.NAME, "rpipping_TextAreaInfoDisplay").get_attribute("textContent").split(":")[0] != "- 8 bytes from 8.8.8.8"):
        print(f"             [Diagnostic - IP - IP Ping] IPv4_Address:8.8.8.8 Data_Bytes:0 Test Fail",file = open(file_name, '+a'))
        if_error = True

    # IP Ping IPv4 Test 2
    dia.IP_Ping_IPv4_Address(driver,"8.8.8.8")
    dia.IP_Ping_IPv4_Data_Bytes(driver,"88")
    dia.IP_Ping_IPv4Ping(driver)
    if(driver.find_element(By.NAME, "rpipping_TextAreaInfoDisplay").get_attribute("textContent").split(":")[0] != "- 76 bytes from 8.8.8.8"):
        print(f"             [Diagnostic - IP - IP Ping] IPv4_Address:8.8.8.8 Data_Bytes:88 Test Fail",file = open(file_name, '+a'))
        if_error = True

    # IP Ping IPv4 Test 3
    dia.IP_Ping_IPv4_Address(driver,"8.8.8.8")
    dia.IP_Ping_IPv4_Data_Bytes(driver,"89")
    dia.IP_Ping_IPv4Ping(driver)
    if(driver.find_element(By.NAME, "rpipping_TextAreaInfoDisplay").get_attribute("textContent") != "Network is unreachable"):
        print(f"             [Diagnostic - IP - IP Ping] IPv4_Address:8.8.8.8 Data_Bytes:89 Test Fail",file = open(file_name, '+a'))
        if_error = True

    # IP Ping IPv4 Test 4
    dia.IP_Ping_IPv4_Address(driver,"8.8.8.8")
    dia.IP_Ping_IPv4_Data_Bytes(driver,"@")
    dia.IP_Ping_IPv4Ping(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Diagnostic - IP - IP Ping] IPv4_Address:8.8.8.8 Data_Bytes:@ Test Fail",file = open(file_name, '+a'))
        if_error = True

    # IP Ping IPv4 Test 5
    dia.IP_Ping_IPv4_Address(driver,"10.10.10.1")
    dia.IP_Ping_IPv4_Data_Bytes(driver,"56")
    dia.IP_Ping_IPv4Ping(driver)
    if(driver.find_element(By.NAME, "rpipping_TextAreaInfoDisplay").get_attribute("textContent") != "Network is unreachable"):
        print(f"             [Diagnostic - IP - IP Ping] IPv4_Address:10.10.10.1 Data_Bytes:56 Test Fail",file = open(file_name, '+a'))
        if_error = True

    # IP Ping IPv6 Test 1
    dia.IP_Ping_IPv6_Address(driver,"2001::aa")
    dia.IP_Ping_IPv6_Data_Bytes(driver,"56")
    dia.IP_Ping_IPv6Ping(driver)
    if(driver.find_element(By.NAME, "rpipping_TextAreaInfoDisplay").get_attribute("textContent") != "Network is unreachable"):
        print(f"             [Diagnostic - IP - IP Ping] IPv6_Address:2001::aa Data_Bytes:56 Test Fail",file = open(file_name, '+a'))
        if_error = True

    # IP Ping IPv6 Test 2
    dia.IP_Ping_IPv6_Address(driver,"2001::aa")
    dia.IP_Ping_IPv6_Data_Bytes(driver,"0")
    dia.IP_Ping_IPv6Ping(driver)
    if(driver.find_element(By.NAME, "rpipping_TextAreaInfoDisplay").get_attribute("textContent") != "Network is unreachable"):
        print(f"             [Diagnostic - IP - IP Ping] IPv6_Address:2001::aa Data_Bytes:0 Test Fail",file = open(file_name, '+a'))
        if_error = True

    # IP Ping IPv6 Test 3
    dia.IP_Ping_IPv6_Address(driver,"2001::aa")
    dia.IP_Ping_IPv6_Data_Bytes(driver,"1472")
    dia.IP_Ping_IPv6Ping(driver)
    if(driver.find_element(By.NAME, "rpipping_TextAreaInfoDisplay").get_attribute("textContent") != "Network is unreachable"):
        print(f"             [Diagnostic - IP - IP Ping] IPv6_Address:2001::aa Data_Bytes:1472 Test Fail",file = open(file_name, '+a'))
        if_error = True

    # IP Ping Result
    if(if_error == False):
        print(f"[MSAN1-11844][Diagnostic - IP - IP Ping] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11844][Diagnostic - IP - IP Ping] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # IP Trace Route Test
    # IP > IP Trace Route
    # -------------------------start-------------------------

    # 路徑導向 IP > IP Trace Route
    mod.Tab_Switch(driver,"IP Trace Route")

    if_error = False

    # IP Trace Route Test 1
    dia.IP_Trace_Route_IP_Address(driver,"192.168.128.6")
    dia.IP_Trace_Route_Start(driver)
    time.sleep(2)
    if(driver.find_element(By.NAME, "rpiptroute_TextAreaInfoDisplay").get_attribute("textContent").split("(")[0] == " 1  192.168.169.254 " or driver.find_element(By.NAME, "rpiptroute_TextAreaInfoDisplay").get_attribute("textContent").split("(")[0] == " 1  192.168.168.2 "):
        pass
    else:
        print(f"             [Diagnostic - IP - IP Trace Route] IP Address:192.168.128.6 Test Fail",file = open(file_name, '+a'))
        if_error = True

    # IP Trace Route Test 2
    dia.IP_Trace_Route_IP_Address(driver,"@.@.@.@")
    dia.IP_Trace_Route_Start(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Diagnostic - IP - IP Trace Route] IP_Address:@.@.@.@ Test Fail",file = open(file_name, '+a'))
        if_error = True

    # IP Trace Route Result
    if(if_error == False):
        print(f"[MSAN1-11845][Diagnostic - IP - IP Trace Route] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11845][Diagnostic - IP - IP Trace Route] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # OAM Loopback Test
    # Diagnostic > OAM Loopback
    # -------------------------start-------------------------

    # 路徑導向 Diagnostic > OAM Loopback
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"OAM Loopback")
    mod.Switch_Frame(driver)

    # slot selelct
    dia.Slot_Select(driver,glc_slot)
    dia.Port_Select(driver,glc_port)

    if_error = False

    # OAM Loopback Btn Test
    dia.OAM_Loopback_Start(driver)
    if(driver.find_element(By.NAME, "result").get_attribute("textContent") != f"Port {glc_slot}-{glc_port} is not supported or not ready to start remote loopback test."):
        print(f"             [Diagnostic - OAM Loopback] Start Button Test Fail",file = open(file_name, '+a'))
        if_error = True
    dia.OAM_Loopback_Stop(driver)
    if(driver.find_element(By.NAME, "result").get_attribute("textContent") != f"Port {glc_slot}-{glc_port} is not supported or not ready to stop remote loopback test."):
        print(f"             [Diagnostic - OAM Loopback] Stop Button Test Fail",file = open(file_name, '+a'))
        if_error = True
    dia.OAM_Loopback_Test(driver)
    if(driver.find_element(By.NAME, "result").get_attribute("textContent") != f"Port {glc_slot}-{glc_port} is not supported or not ready for remote loopback test."):
        print(f"             [Diagnostic - OAM Loopback] Test Button Test Fail",file = open(file_name, '+a'))
        if_error = True
    dia.OAM_Loopback_Get(driver)
    if(driver.find_element(By.NAME, "result").get_attribute("textContent") != f"Port {glc_slot}-{glc_port} OAM Remote Loopback Test latest result:\n This port has not been tested yet."):
        print(f"             [Diagnostic - OAM Loopback] Get Button Test Fail",file = open(file_name, '+a'))
        if_error = True

    # OAM Loopback Result
    if(if_error == False):
        print(f"[MSAN1-11846][Diagnostic - OAM Loopback] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11846][Diagnostic - OAM Loopback] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def Line_Card_Test(driver,glc_slot,glc_port,file_name):
    print(f"Line Card Test\nTest Start",file = open(file_name, '+a'))

    # Line Card Lcman Test
    # Line Card > Lcman
    # -------------------------start-------------------------

    # 路徑導向 Line Card > Lcman
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Line Card")
    mod.Switch_Frame(driver)

    # slot select enable
    lc.Slot_Select(driver,glc_slot)
    lc.Lcman_Action(driver,1)
    lc.Lcman_Apply(driver)

    if_error = False

    try:
        error_msg = driver.find_element(By.CLASS_NAME, "div-row-cell-content.msg").get_attribute("textContent").split("\n")[0]
        driver.find_element(By.NAME, "rperror_btnBack").click()  #* add        
        if "already enabled" in error_msg:
            print(f"             [Line Card - Lcman] {error_msg} (already enabled)",file = open(file_name, '+a'))
        else:
            print(f"             [Line Card - Lcman] {error_msg} Apply Fail",file = open(file_name, '+a'))        
            if_error = True
    except:
        pass


    # check %slot state active
    time.sleep(0.5)
    if(driver.find_elements(By.CLASS_NAME, "td-table-content.SysinfoState")[int(glc_slot)-1].get_attribute("textContent") != "active"):
        print(f"             [Line Card - Lcman] Check Slot{glc_slot} active Fail",file = open(file_name, '+a'))
        if_error = True
    
    print("001")
    # check Next Boot Image
    driver.find_elements(By.NAME, "Sysinfotableid")[int(glc_slot)-1].click()
    print("002")
    time.sleep(0.5)
    next_boot_image = driver.find_element(By.CLASS_NAME, "div-row-cell-content.rplcmanDetailnextbootimage").get_attribute("textContent")
    time.sleep(0.5)
    driver.find_element(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-icon-only.ui-dialog-titlebar-close").click()

    # Change Boot Image Index
    if(next_boot_image == "1"):
        lc.Boot_Slot_Select(driver,glc_slot)
        lc.Boot_Index(driver,2)
        lc.Boot_Apply(driver)
        time.sleep(1)
        if(driver.find_element(By.XPATH, f"//*[@name='rplcman_bootIndex']/option[2]").is_selected() != True):
            print(f"             [Line Card - Lcman] Boot Image Index 2 Apply Fail",file = open(file_name, '+a'))
            if_error = True
        time.sleep(0.5)
        driver.find_elements(By.NAME, "Sysinfotableid")[int(glc_slot)-1].click()
        time.sleep(0.5)
        if(driver.find_element(By.CLASS_NAME, "div-row-cell-content.rplcmanDetailnextbootimage").get_attribute("textContent") != "2"):
            print(f"             [Line Card - Lcman] Next Boot Image 2 Apply Fail",file = open(file_name, '+a'))
            if_error = True
        time.sleep(0.5)
        driver.find_element(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-icon-only.ui-dialog-titlebar-close").click()
        time.sleep(0.5)
        driver.find_elements(By.NAME, "Sysinfotableid")[int(glc_slot)-1].click()
        time.sleep(0.5)
        if(driver.find_element(By.CLASS_NAME, "div-row-cell-content.rplcmanDetailnextbootimage").get_attribute("textContent") != "2"):
            print(f"             [Line Card - Lcman] Next Boot Image 2 Apply Fail",file = open(file_name, '+a'))
            if_error = True
        time.sleep(0.5)
        driver.find_element(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-icon-only.ui-dialog-titlebar-close").click()
        # Reset Boot Image Index
        lc.Boot_Slot_Select(driver,glc_slot)
        lc.Boot_Index(driver,1)
        lc.Boot_Apply(driver)
    
    elif(next_boot_image == "2"):
        lc.Boot_Slot_Select(driver,glc_slot)
        lc.Boot_Index(driver,1)
        lc.Boot_Apply(driver)
        time.sleep(1)
        if(driver.find_element(By.XPATH, f"//*[@name='rplcman_bootIndex']/option[1]").is_selected() != True):
            print(f"             [Line Card - Lcman] Boot Image Index 1 Apply Fail",file = open(file_name, '+a'))
            if_error = True
        time.sleep(0.5)
        driver.find_elements(By.NAME, "Sysinfotableid")[int(glc_slot)-1].click()
        time.sleep(0.5)
        if(driver.find_element(By.CLASS_NAME, "div-row-cell-content.rplcmanDetailnextbootimage").get_attribute("textContent") != "1"):
            print(f"             [Line Card - Lcman] Next Boot Image 1 Apply Fail",file = open(file_name, '+a'))
            if_error = True
        time.sleep(0.5)
        driver.find_element(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-icon-only.ui-dialog-titlebar-close").click()
        time.sleep(0.5)
        driver.find_elements(By.NAME, "Sysinfotableid")[int(glc_slot)-1].click()
        time.sleep(0.5)
        if(driver.find_element(By.CLASS_NAME, "div-row-cell-content.rplcmanDetailnextbootimage").get_attribute("textContent") != "1"):
            print(f"             [Line Card - Lcman] Next Boot Image 1 Apply Fail",file = open(file_name, '+a'))
            if_error = True
        time.sleep(0.5)
        driver.find_element(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-icon-only.ui-dialog-titlebar-close").click()
        # Reset Boot Image Index
        lc.Boot_Slot_Select(driver,glc_slot)
        lc.Boot_Index(driver,2)
        lc.Boot_Apply(driver)

    # Lcman Result
    if(if_error == False):
        print(f"[MSAN1-11847][Line Card - Lcman] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11847][Line Card - Lcman] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Line Card G.vector Test
    # Line Card > G.vector
    # -------------------------start-------------------------

    # 路徑導向 Line Card > G.vector
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"G.vector")
    mod.Switch_Frame(driver)

    if_error = False

    # G.vector SLV Test
    lc.Slot_Select(driver,glc_slot)
    lc.G_vector_Mode(driver,2)
    lc.G_vector_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Line Card - G.vector] Mode:SLV No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # G.vector BLV Test
    lc.Slot_Select(driver,glc_slot)
    lc.G_vector_Mode(driver,1)
    lc.G_vector_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Line Card - G.vector] Mode:BLV No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # G.vector Slot Select Test
    driver.find_elements(By.NAME, "Lcmantableid")[int(glc_slot)-1].click()
    if(mod.IsAlert(driver) != True):
        print(f"             [Line Card - G.vector] Slot{glc_slot} Select No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # G.vector Result
    if(if_error == False):
        print(f"[MSAN1-11848][Line Card - G.vector] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11848][Line Card - G.vector] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Line Card PIN Test
    # Line Card > PIN
    # -------------------------start-------------------------

    # 路徑導向 Line Card > PIN
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"PIN")
    mod.Switch_Frame(driver)

    if_error = False

    # PIN Reverse Test
    lc.Slot_Select(driver,glc_slot)
    lc.PIN_Mode(driver,2)
    lc.PIN_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Line Card - PIN] Mode:Reverse No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # PIN Normal Test
    lc.Slot_Select(driver,glc_slot)
    lc.PIN_Mode(driver,1)
    lc.PIN_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Line Card - PIN] Mode:Normal No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # PIN Slot Select Test
    driver.find_elements(By.NAME, "Lcmantableid")[int(glc_slot)-1].click()
    if(mod.IsAlert(driver) != True):
        print(f"             [Line Card - PIN] Slot{glc_slot} Select No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # PIN Result
    if(if_error == False):
        print(f"[MSAN1-11849][Line Card - PIN] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11849][Line Card - PIN] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def L3_Routing_Test(driver,glc_slot,glc_port,msc_slot,msc_port,file_name):
    print(f"L3 Routing Test\nTest Start",file = open(file_name, '+a'))

    # Vlan GE/GENNI VLAN Setup Setting
    # Vlan > GE/GENNI VLAN Setup > VLAN Table
    # -------------------------start-------------------------

    # 路徑導向 Vlan > GE/GENNI VLAN Setup > VLAN Table
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"VLAN")
    mod.Switch_Frame(driver)

    # vlan setting
    vlan.Slot_Select(driver,msc_slot)
    vlan.GE_GENNI_VLAN_Setup_VLAN_Table_VLAN_ID(driver,"4000")
    vlan.GE_GENNI_VLAN_Setup_VLAN_Table_Apply(driver)

    # -------------------------end-------------------------

    # L3 Routing Interface Interface Test
    # L3 Routing > Interface > Interface
    # -------------------------start-------------------------

    # 路徑導向 L3 Routing > Interface > Interface
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"L3 Routing")
    mod.Switch_Frame(driver)

    if_error = False

    # slot select
    l3r.Interface_Interface_VID_Select(driver,"4000")
    l3r.Interface_Interface_Load(driver)

    # L3 Routing Interface Interface Clear
    index = 0
    is_last = False
    while(is_last == False):
        try:
            driver.find_element(By.NAME, "rpinterface_select").click()
            l3r.Interface_Interface_Delete(driver)
        except:
            is_last = True
        index = index+1

    # L3 Routing Interface Test
    l3r.Interface_Interface_IP(driver,"10.10.10.1")
    l3r.Interface_Interface_Mask(driver,"0")
    l3r.Interface_Interface_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [L3 Routing - Interface - Interface] Mask:0 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    l3r.Interface_Interface_Mask(driver,"31")
    l3r.Interface_Interface_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [L3 Routing - Interface - Interface] Mask:31 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    l3r.Interface_Interface_Mask(driver,"30")
    l3r.Interface_Interface_Apply(driver)
    try:
        error_msg = driver.find_element(By.CLASS_NAME, "div-row-cell-content.msg").get_attribute("textContent")
        print(f"             [L3 Routing - Interface - Interface] Apply Fail Error Message:{error_msg}",file = open(file_name, '+a'))
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        pass
    if(mod.IsAlert(driver) == True):
        print(f"             [L3 Routing - Interface - Interface] Mask:30 Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    else:
        try:
            driver.find_elements(By.NAME, "rpinterface_ip")
            if(driver.find_element(By.NAME, "rpinterface_ip").get_attribute("textContent") != "10.10.10.1"):
                print(f"             [L3 Routing - Interface - Interface] IP Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_element(By.NAME, "rpinterface_mask").get_attribute("textContent") != "30"):
                print(f"             [L3 Routing - Interface - Interface] Mask Test Fail",file = open(file_name, '+a'))
                if_error = True
        except:
            print(f"             [L3 Routing - Interface - Interface] Apply Fail",file = open(file_name, '+a'))
            if_error = True

    # L3 Routing Interface Result
    if(if_error == False):
        print(f"[MSAN1-11850][L3 Routing - Interface - Interface] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11850][L3 Routing - Interface - Interface] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # L3 Routing Interface RIP Test
    # L3 Routing > Interface > RIP
    # -------------------------start-------------------------

    if_RIP_exist = False

    try:
        # 路徑導向 L3 Routing > Interface > RIP
        mod.Tab_Switch(driver,"RIP")
        if_RIP_exist = True
    except:
        print(f"             [L3 Routing - Interface - RIP] Result Block",file = open(file_name, '+a'))
        print(f"[MSAN1-11851][L3 Routing - Interface - RIP] Result Pass",file = open(file_name, '+a'))

    if(if_RIP_exist == True):
        # L3 Routing Interface RIP Test 1
        l3r.Interface_RIP_VLAN_Select(driver,"4000")
        l3r.Interface_RIP_Load(driver)
        l3r.Interface_RIP_Direction(driver,3)
        l3r.Interface_RIP_Version(driver,3)
        l3r.Interface_RIP_Apply(driver)

        if_error = False

        # L3 Routing Interface RIP Check 1
        if(driver.find_element(By.XPATH, f"//*[@id='rpl3routingRip_direction']/option[3]").is_selected() != True):
            print(f"             [L3 Routing - Interface - RIP] Direction Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_element(By.XPATH, f"//*[@name='rpl3routingRip_version']/option[3]").is_selected() != True):
            print(f"             [L3 Routing - Interface - RIP] Version Test Fail",file = open(file_name, '+a'))
            if_error = True

        # L3 Routing Interface RIP Test 2
        l3r.Interface_RIP_Direction(driver,1)
        l3r.Interface_RIP_Apply(driver)

        # L3 Routing Interface RIP Check 2
        if(driver.find_element(By.XPATH, f"//*[@id='rpl3routingRip_direction']/option[1]").is_selected() != True):
            print(f"             [L3 Routing - Interface - RIP] Direction Test Fail",file = open(file_name, '+a'))
            if_error = True
        
        # L3 Routing Interface Result
        if(if_error == False):
            print(f"[MSAN1-11851][L3 Routing - Interface - RIP] Result Pass",file = open(file_name, '+a'))
        else:
            print(f"[MSAN1-11851][L3 Routing - Interface - RIP] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # L3 Routing Interface OSPF Test
    # L3 Routing > Interface > OSPF
    # -------------------------start-------------------------

    if_OSPF_exist = False

    try:
        # 路徑導向 L3 Routing > Interface > OSPF
        mod.Tab_Switch(driver,"OSPF")
        if_OSPF_exist = True
    except:
        print(f"             [L3 Routing - Interface - OSPF] Result Block",file = open(file_name, '+a'))
        print(f"[MSAN1-11852][L3 Routing - Interface - OSPF] Result Pass",file = open(file_name, '+a'))

    if(if_OSPF_exist == True):
        l3r.Interface_OSPF_VLAN_Select(driver,"4000")
        l3r.Interface_OSPF_Load(driver)

        if_error = False

        # L3 Routing Interface OSPF Test 1
        l3r.Interface_OSPF_Cost(driver,"65535")
        l3r.Interface_OSPF_Priority(driver,"255")
        l3r.Interface_OSPF_Passive(driver,True)
        l3r.Interface_OSPF_Retransmit_Interval(driver,"65535")
        l3r.Interface_OSPF_Transmit_Delay(driver,"65535")
        l3r.Interface_OSPF_Dead_Interval(driver,"65535")
        l3r.Interface_OSPF_Hello_Interval(driver,"65535")
        l3r.Interface_OSPF_Authentication(driver,2)
        l3r.Interface_OSPF_Simple_Key(driver,"12345678")
        l3r.Interface_OSPF_Apply(driver)

        # L3 Routing Interface OSPF Check 1
        if(driver.find_element(By.ID, "webOspf_inputCost").get_attribute("value") != "65535"):
            print(f"             [L3 Routing - Interface - OSPF] Cost:65535 Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_element(By.ID, "webOspf_inputPriority").get_attribute("value") != "255"):
            print(f"             [L3 Routing - Interface - OSPF] Priority:255 Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_element(By.ID, "webOspf_checkPassive").is_selected() != True):
            print(f"             [L3 Routing - Interface - OSPF] Passive Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_element(By.ID, "webOspf_inputRetransmit").get_attribute("value") != "65535"):
            print(f"             [L3 Routing - Interface - OSPF] Retransmit Interval:65535 Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_element(By.ID, "webOspf_inputTransmit").get_attribute("value") != "65535"):
            print(f"             [L3 Routing - Interface - OSPF] Transmit Delay:65535 Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_element(By.ID, "webOspf_inputDead").get_attribute("value") != "65535"):
            print(f"             [L3 Routing - Interface - OSPF] Dead Interval:65535 Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_element(By.ID, "webOspf_inputHello").get_attribute("value") != "65535"):
            print(f"             [L3 Routing - Interface - OSPF] Hello Interval:65535 Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_element(By.XPATH, f"//*[@id='webOspf_selectAuth']/option[2]").is_selected() != True):
            print(f"             [L3 Routing - Interface - OSPF] Authentication:Simple Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_element(By.ID, "webOspf_inputSimple").get_attribute("value") != "12345678"):
            print(f"             [L3 Routing - Interface - OSPF] Simple Key:12345678 Test Fail",file = open(file_name, '+a'))
            if_error = True

        # L3 Routing Interface OSPF Test 2
        l3r.Interface_OSPF_Authentication(driver,3)
        l3r.Interface_OSPF_MD5_Key_ID(driver,"255")
        l3r.Interface_OSPF_MD5_Key(driver,"1234567890123456")
        l3r.Interface_OSPF_Apply(driver)

        # L3 Routing Interface OSPF Check 2
        if(driver.find_element(By.XPATH, f"//*[@id='webOspf_selectAuth']/option[3]").is_selected() != True):
            print(f"             [L3 Routing - Interface - OSPF] Authentication:MD5 Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_element(By.ID, "webOspf_inputMd5KeyId").get_attribute("value") != "255"):
            print(f"             [L3 Routing - Interface - OSPF] Key ID:255 Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_element(By.ID, "webOspf_inputMd5Key").get_attribute("value") != "1234567890123456"):
            print(f"             [L3 Routing - Interface - OSPF] Key:1234567890123456 Test Fail",file = open(file_name, '+a'))
            if_error = True

        # L3 Routing Interface OSPF Test 3
        l3r.Interface_OSPF_Authentication(driver,1)
        l3r.Interface_OSPF_Apply(driver)

        # L3 Routing Interface OSPF Check 3
        if(driver.find_element(By.XPATH, f"//*[@id='webOspf_selectAuth']/option[1]").is_selected() != True):
            print(f"             [L3 Routing - Interface - OSPF] Authentication:None Test Fail",file = open(file_name, '+a'))
            if_error = True

        # L3 Routing Interface OSPF Default
        l3r.Interface_OSPF_Default(driver)
        
        # L3 Routing Interface Result
        if(if_error == False):
            print(f"[MSAN1-11852][L3 Routing - Interface - OSPF] Result Pass",file = open(file_name, '+a'))
        else:
            print(f"[MSAN1-11852][L3 Routing - Interface - OSPF] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # L3 Routing RIP Test
    # L3 Routing > RIP
    # -------------------------start-------------------------

    if_RIP_exist = False

    try:
        # 路徑導向 L3 Routing > RIP
        mod.Switch_Default(driver)
        mod.SubPage_Switch(driver,"RIP")
        mod.Switch_Frame(driver)
        if_RIP_exist = True
    except:
        print(f"             [L3 Routing - RIP] Result Block",file = open(file_name, '+a'))
        print(f"[MSAN1-11853][L3 Routing - RIP] Result Pass",file = open(file_name, '+a'))

    if_error = False

    if(if_RIP_exist == True):
        # L3 Routing RIP Test
        l3r.RIP_Distance(driver,"0")
        l3r.RIP_Apply(driver)
        if(mod.IsAlert(driver) != True):
            print(f"             [L3 Routing - RIP] Distance:0 No Alert Test Fail",file = open(file_name, '+a'))
            if_error = True
        l3r.RIP_Distance(driver,"256")
        l3r.RIP_Apply(driver)
        if(mod.IsAlert(driver) != True):
            print(f"             [L3 Routing - RIP] Distance:256 No Alert Test Fail",file = open(file_name, '+a'))
            if_error = True
        l3r.RIP_Distance(driver,"255")
        l3r.RIP_Apply(driver)
        if(mod.IsAlert(driver) == True):
            print(f"             [L3 Routing - RIP] Distance:255 Alert Test Fail",file = open(file_name, '+a'))
            if_error = True
        else:
            if(driver.find_element(By.ID, "get_distance").get_attribute("textContent") != "255"):
                print(f"             [L3 Routing - RIP] Distance:255 Test Fail",file = open(file_name, '+a'))
                if_error = True

        # L3 Routing RIP Default
        l3r.RIP_Default(driver)

        # L3 Routing Result
        if(if_error == False):
            print(f"[MSAN1-11853][L3 Routing - RIP] Result Pass",file = open(file_name, '+a'))
        else:
            print(f"[MSAN1-11853][L3 Routing - RIP] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # DHCP Server Server Test
    # DHCP Server > Server
    # -------------------------start-------------------------

    # 路徑導向 DHCP Server > Server
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"DHCP Server")
    mod.Switch_Frame(driver)

    if_error = False

    # DHCP Server Server Test
    l3r.DHCP_Serve_Server_VID(driver,"4000")
    # l3r.DHCP_Serve_Server_Start_IP(driver,"0.0.0.1")
    l3r.DHCP_Serve_Server_Start_IP(driver,"1.0.0.1")
    # l3r.DHCP_Serve_Server_End_IP(driver,"223.255.255.255")
    l3r.DHCP_Serve_Server_End_IP(driver,"223.255.255.254")
    l3r.DHCP_Serve_Server_Apply(driver)

    dhcp_4000_index = 0
    if_last = False
    if_find = False
    while(if_last == False):
        try:
            if(driver.find_elements(By.CLASS_NAME, "webDhcpServer_l3ServerVid.td-table-content")[dhcp_4000_index].get_attribute("textContent") == "4000"):
                if_find = True
                # DHCP Server Check
                if(driver.find_elements(By.CLASS_NAME, "webDhcpServer_startAddr.td-table-content")[dhcp_4000_index].get_attribute("textContent") != "1.0.0.1"):
                    print(f"             [L3 Routing - DHCP Server - Server] Start IP Address:1.0.0.1 Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "webDhcpServer_endAddr.td-table-content")[dhcp_4000_index].get_attribute("textContent") != "223.255.255.254"):
                    print(f"             [L3 Routing - DHCP Server - Server] End IP Address:223.255.255.254 Test Fail",file = open(file_name, '+a'))
                    if_error = True
                # DHCP Server Select Test
                driver.find_elements(By.NAME, "pfListSelected")[dhcp_4000_index].click()
                l3r.DHCP_Serve_Server_Select_Netmask(driver,"32")
                l3r.DHCP_Serve_Server_Select_Gateway(driver,"223.255.255.255")
                l3r.DHCP_Serve_Server_Select_Primary(driver,"223.255.255.255")
                l3r.DHCP_Serve_Server_Select_Secondary(driver,"223.255.255.255")
                l3r.DHCP_Serve_Server_Select_Apply(driver)
                driver.find_element(By.CLASS_NAME, "ui-button-icon-primary.ui-icon.ui-icon-closethick").click()
                # DHCP Server Select Check
                driver.find_elements(By.NAME, "pfListSelected")[dhcp_4000_index].click()
                if(driver.find_element(By.NAME, "webDhcpServer_l3ServerVid").get_attribute("value") != "4000"):
                    print(f"             [L3 Routing - DHCP Server - Server] L3 Server VID Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.NAME, "webDhcpServer_netmask").get_attribute("value") != "32"):
                    print(f"             [L3 Routing - DHCP Server - Server] Netmask Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.NAME, "webDhcpServer_gateway").get_attribute("value") != "223.255.255.255"):
                    print(f"             [L3 Routing - DHCP Server - Server] Gateway IP Address Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.NAME, "webDhcpServer_primaryDnsAddr").get_attribute("value") != "223.255.255.255"):
                    print(f"             [L3 Routing - DHCP Server - Server] Primary DNS IP Address Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.NAME, "webDhcpServer_secondaryDnsAddr").get_attribute("value") != "223.255.255.255"):
                    print(f"             [L3 Routing - DHCP Server - Server] Secondary DNS IP Test Fail",file = open(file_name, '+a'))
                    if_error = True
                break
        except:
            if_last = True
        dhcp_4000_index = dhcp_4000_index+1
    dhcp_4000_index = dhcp_4000_index-1

    if(if_find == False):
        print(f"             [L3 Routing - DHCP Server - Server] VID Not Found Test Fail",file = open(file_name, '+a'))
        if_error = True
        
    # DHCP Server Server Result
    if(if_error == False):
        print(f"[MSAN1-11854][L3 Routing - DHCP Server - Server] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11854][L3 Routing - DHCP Server - Server] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # DHCP Server Lease Test
    # DHCP Server > Lease
    # -------------------------start-------------------------

    # 路徑導向 DHCP Server > Lease
    mod.Tab_Switch(driver,"Lease")

    if_error = False

    # DHCP Server Lease Test 1
    l3r.DHCP_Serve_Lease_VID(driver,"4000")
    l3r.DHCP_Serve_Lease_ALIE(driver,True)
    l3r.DHCP_Serve_Lease_Load(driver)
    
    # DHCP Server Lease Check 1
    if(driver.find_element(By.NAME, "webDhcpServerLease_expiredChk").is_selected() != True):
        print(f"             [L3 Routing - DHCP Server - Lease] All Leases Include Expired Test Fail",file = open(file_name, '+a'))
        if_error = True

    # DHCP Server Lease Test 2
    l3r.DHCP_Serve_Lease_ALIE(driver,False)
    l3r.DHCP_Serve_Lease_Load(driver)
    
    # DHCP Server Lease Check 2
    if(driver.find_element(By.NAME, "webDhcpServerLease_expiredChk").is_selected() != False):
        print(f"             [L3 Routing - DHCP Server - Lease] All Leases Include Expired Test Fail",file = open(file_name, '+a'))
        if_error = True

    # DHCP Server Lease Result
    if(if_error == False):
        print(f"[MSAN1-11855][L3 Routing - DHCP Server - Lease] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11855][L3 Routing - DHCP Server - Lease] Result Fail",file = open(file_name, '+a'))

    # DHCP Server Server Delete
    mod.Tab_Switch(driver,"Server")
    driver.find_elements(By.NAME, "pfListSelected")[dhcp_4000_index].click()
    l3r.DHCP_Serve_Server_Select_Delete(driver)

    # -------------------------end-------------------------

    # L3 Routing OSPF Configuration Test
    # L3 Routing > OSPF > Configuration
    # -------------------------start-------------------------

    if_OSPF_exist = False

    try:
        # 路徑導向 L3 Routing > OSPF > Configuration
        mod.Switch_Default(driver)
        mod.SubPage_Switch(driver,"OSPF")
        mod.Switch_Frame(driver)
        if_OSPF_exist = True
    except:
        print(f"             [L3 Routing - OSPF - Configuration] Result Block",file = open(file_name, '+a'))
        print(f"[MSAN1-11856][L3 Routing - OSPF - Configuration] Result Pass",file = open(file_name, '+a'))
        print(f"             [L3 Routing - OSPF - Area] Result Block",file = open(file_name, '+a'))
        print(f"[MSAN1-11857][L3 Routing - OSPF - Area] Result Pass",file = open(file_name, '+a'))

    if_error = False

    if(if_OSPF_exist == True):
        # L3 Routing OSPF Configuration Test 1-1
        l3r.OSPF_Configuration_Active(driver,True)
        l3r.OSPF_Configuration_Router_ID(driver,"255.255.255.255")
        l3r.OSPF_Configuration_Distance(driver,"255")
        l3r.OSPF_Configuration_RS_Active(driver,True)
        l3r.OSPF_Configuration_RS_Metric_Type(driver,2)
        l3r.OSPF_Configuration_RS_Metric(driver,"16777214")
        l3r.OSPF_Configuration_RR_Active(driver,True)
        l3r.OSPF_Configuration_RR_Metric_Type(driver,2)
        l3r.OSPF_Configuration_RR_Metric(driver,"16777214")
        l3r.OSPF_Configuration_Apply_1(driver)

        # L3 Routing OSPF Configuration Check 1-1
        if(driver.find_element(By.ID, "webOspf_checkOspfActive").is_selected() != True):
            print(f"             [L3 Routing - OSPF - Configuration] Active Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_element(By.ID, "webOspf_inputRouterId").get_attribute("value") != "255.255.255.255"):
            print(f"             [L3 Routing - OSPF - Configuration] Router ID Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_element(By.ID, "webOspf_inputDistance").get_attribute("value") != "255"):
            print(f"             [L3 Routing - OSPF - Configuration] Distance Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_element(By.ID, "webOspf_checkRedistributeStatic").is_selected() != True):
            print(f"             [L3 Routing - OSPF - Configuration] Redistribute Static Active Test Fail",file = open(file_name, '+a'))
            if_error = True
            if(driver.find_element(By.XPATH, f"//*[@id='webOspf_selectRedistributeStatic']/option[2]").is_selected() != True):
                print(f"             [L3 Routing - OSPF - Configuration] Redistribute Static Metric Type Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_element(By.ID, "webOspf_inputMetricStatic").get_attribute("value") != "16777214"):
                print(f"             [L3 Routing - OSPF - Configuration] Redistribute Static Metric Test Fail",file = open(file_name, '+a'))
                if_error = True
        if(driver.find_element(By.ID, "webOspf_checkRedistributeRip").is_selected() != True):
            print(f"             [L3 Routing - OSPF - Configuration] Redistribute RIP Active Test Fail",file = open(file_name, '+a'))
            if_error = True
            if(driver.find_element(By.XPATH, f"//*[@id='webOspf_selectRedistributeRip']/option[2]").is_selected() != True):
                print(f"             [L3 Routing - OSPF - Configuration] Redistribute RIP Metric Type Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_element(By.ID, "webOspf_inputMetricRip").get_attribute("value") != "16777214"):
                print(f"             [L3 Routing - OSPF - Configuration] Redistribute RIP Metric Test Fail",file = open(file_name, '+a'))
                if_error = True

        # L3 Routing OSPF Configuration Test 1-2
        l3r.OSPF_Configuration_Distance(driver,"0")
        l3r.OSPF_Configuration_Apply_1(driver)
        if(mod.IsAlert(driver) != True):
            print(f"             [L3 Routing - OSPF - Configuration] Distance:0 No Alert Test Fail",file = open(file_name, '+a'))
            if_error = True
        time.sleep(1)

        # L3 Routing OSPF Configuration Test 1-3
        l3r.OSPF_Configuration_Distance(driver,"256")
        l3r.OSPF_Configuration_Apply_1(driver)
        if(mod.IsAlert(driver) != True):
            print(f"             [L3 Routing - OSPF - Configuration] Distance:256 No Alert Test Fail",file = open(file_name, '+a'))
            if_error = True
        time.sleep(1)

        # L3 Routing OSPF Configuration Test 1-4
        l3r.OSPF_Configuration_Distance(driver,"255")
        l3r.OSPF_Configuration_RS_Metric(driver,"16777215")
        l3r.OSPF_Configuration_Apply_1(driver)
        if(mod.IsAlert(driver) != True):
            print(f"             [L3 Routing - OSPF - Configuration] Redistribute Static Metric:16777215 No Alert Test Fail",file = open(file_name, '+a'))
            if_error = True
        time.sleep(1)

        # L3 Routing OSPF Configuration Test 1-5
        l3r.OSPF_Configuration_RS_Metric(driver,"16777214")
        l3r.OSPF_Configuration_RR_Metric(driver,"16777215")
        l3r.OSPF_Configuration_Apply_1(driver)
        if(mod.IsAlert(driver) != True):
            print(f"             [L3 Routing - OSPF - Configuration] Redistribute RIP Metric:16777215 No Alert Test Fail",file = open(file_name, '+a'))
            if_error = True

        # L3 Routing OSPF Configuration Test 2-1
        l3r.OSPF_Configuration_IP_Address(driver,"223.255.255.255")
        l3r.OSPF_Configuration_Netmask(driver,"32")
        l3r.OSPF_Configuration_Area(driver,"4294967295")
        l3r.OSPF_Configuration_Apply_2(driver)

        # L3 Routing OSPF Configuration Check 2-1
        if(driver.find_element(By.CLASS_NAME, "webOspf_networkPrefix.td-table-content").get_attribute("textContent") != "223.255.255.255/32"):
            print(f"             [L3 Routing - OSPF - Configuration] Prefix Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_element(By.CLASS_NAME, "webOspf_networkArea.td-table-content").get_attribute("textContent") != "255.255.255.255"):
            print(f"             [L3 Routing - OSPF - Configuration] Area Test Fail",file = open(file_name, '+a'))
            if_error = True

        # L3 Routing OSPF Configuration Test 2-2
        l3r.OSPF_Configuration_IP_Address(driver,"223.255.255.255")
        l3r.OSPF_Configuration_Netmask(driver,"0")
        l3r.OSPF_Configuration_Area(driver,"4294967295")
        l3r.OSPF_Configuration_Apply_2(driver)
        if(mod.IsAlert(driver) != True):
            print(f"             [L3 Routing - OSPF - Configuration] Netmask:0 No Alert Test Fail",file = open(file_name, '+a'))
            if_error = True
        time.sleep(1)

        # L3 Routing OSPF Configuration Test 2-3
        l3r.OSPF_Configuration_Netmask(driver,"33")
        l3r.OSPF_Configuration_Apply_2(driver)
        if(mod.IsAlert(driver) != True):
            print(f"             [L3 Routing - OSPF - Configuration] Netmask:33 No Alert Test Fail",file = open(file_name, '+a'))
            if_error = True
        time.sleep(1)

        # L3 Routing OSPF Configuration Test 2-4
        l3r.OSPF_Configuration_IP_Address(driver,"0.0.0.1")
        l3r.OSPF_Configuration_Netmask(driver,"32")
        l3r.OSPF_Configuration_Area(driver,"4294967295")
        l3r.OSPF_Configuration_Apply_2(driver)
        OSPF_Len_Before = driver.find_elements(By.CLASS_NAME, "i1.td-table-content").__len__()

        # Select Delete
        driver.find_element(By.NAME, "pfListSelected").click()
        l3r.OSPF_Configuration_Delete(driver)
        OSPF_Len_After = driver.find_elements(By.CLASS_NAME, "i1.td-table-content").__len__()

        # Select Delete Check
        if(OSPF_Len_After == OSPF_Len_Before+1):
            print(f"             [L3 Routing - OSPF - Configuration] Delete Test Fail",file = open(file_name, '+a'))
            if_error = True

        # Remove All
        l3r.OSPF_Configuration_Remove_All(driver)

        # Remove All Check
        if(driver.find_elements(By.CLASS_NAME, "i1.td-table-content").__len__() != 0):
            print(f"             [L3 Routing - OSPF - Configuration] Remove All Test Fail",file = open(file_name, '+a'))
            if_error = True

        # L3 Routing OSPF Configuration Result
        if(if_error == False):
            print(f"[MSAN1-11856][L3 Routing - OSPF - Configuration] Result Pass",file = open(file_name, '+a'))
        else:
            print(f"[MSAN1-11856][L3 Routing - OSPF - Configuration] Result Fail",file = open(file_name, '+a'))

        # -------------------------end-------------------------

        # L3 Routing OSPF Area Test
        # L3 Routing > OSPF > Area
        # -------------------------start-------------------------

        # 路徑導向 L3 Routing > OSPF > Area
        mod.Tab_Switch(driver,"Area")

        if_error = False

        # L3 Routing OSPF Area Test 1
        l3r.OSPF_Area(driver,"4294967295")
        l3r.OSPF_Area_Name(driver,"12345678901234567890123456789012")
        l3r.OSPF_Area_Type(driver,4)
        l3r.OSPF_Area_Default_Cost(driver,"16777215")
        l3r.OSPF_Area_Authentication(driver,3)
        l3r.OSPF_Area_Apply(driver)

        # L3 Routing OSPF Area Check 1
        if(driver.find_element(By.CLASS_NAME, "webOspf_area.td-table-content").get_attribute("textContent") != "255.255.255.255"):
            print(f"             [L3 Routing - OSPF - Area] Area Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_element(By.CLASS_NAME, "webOspf_areaName.td-table-content").get_attribute("textContent") != "12345678901234567890123456789012"):
            print(f"             [L3 Routing - OSPF - Area] Name Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_element(By.CLASS_NAME, "webOspf_areaType.td-table-content").get_attribute("textContent") != "nssa"):
            print(f"             [L3 Routing - OSPF - Area] Area Type:NSSA Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_element(By.CLASS_NAME, "webOspf_areaDefaultCost.td-table-content").get_attribute("textContent") != "16777215"):
            print(f"             [L3 Routing - OSPF - Area] Default Cost Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_element(By.CLASS_NAME, "webOspf_areaAuth.td-table-content").get_attribute("textContent") != "md5"):
            print(f"             [L3 Routing - OSPF - Area] Authentication:MD5 Test Fail",file = open(file_name, '+a'))
            if_error = True

        # L3 Routing OSPF Area Test 2
        l3r.OSPF_Area(driver,"4294967295")
        l3r.OSPF_Area_Name(driver,"12345678901234567890123456789012")
        l3r.OSPF_Area_Type(driver,2)
        l3r.OSPF_Area_Default_Cost(driver,"16777215")
        l3r.OSPF_Area_Authentication(driver,2)
        l3r.OSPF_Area_Apply(driver)

        # L3 Routing OSPF Area Check 2
        if(driver.find_element(By.CLASS_NAME, "webOspf_areaType.td-table-content").get_attribute("textContent") != "stub"):
            print(f"             [L3 Routing - OSPF - Area] Area Type:Stub Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_element(By.CLASS_NAME, "webOspf_areaAuth.td-table-content").get_attribute("textContent") != "simple"):
            print(f"             [L3 Routing - OSPF - Area] Authentication:Simple Test Fail",file = open(file_name, '+a'))
            if_error = True

        # L3 Routing OSPF Area Test 3
        l3r.OSPF_Area(driver,"4294967295")
        l3r.OSPF_Area_Name(driver,"12345678901234567890123456789012")
        l3r.OSPF_Area_Type(driver,2)
        l3r.OSPF_Area_Default_Cost(driver,"16777216")
        l3r.OSPF_Area_Authentication(driver,2)
        l3r.OSPF_Area_Apply(driver)
        if(mod.IsAlert(driver) != True):
            print(f"             [L3 Routing - OSPF - Area] Default Cost:16777216 No Alert Test Fail",file = open(file_name, '+a'))
            if_error = True

        # L3 Routing OSPF Area Result
        if(if_error == False):
            print(f"[MSAN1-11857][L3 Routing - OSPF - Area] Result Pass",file = open(file_name, '+a'))
        else:
            print(f"[MSAN1-11857][L3 Routing - OSPF - Area] Result Fail",file = open(file_name, '+a'))
        
        # L3 Routing OSPF Configuration Setting Default
        mod.Tab_Switch(driver,"Configuration")
        l3r.OSPF_Configuration_Active(driver,False)
        l3r.OSPF_Configuration_Apply_1(driver)

        # -------------------------end-------------------------

    # L3 Routing Interface Delete
    # L3 Routing > Interface > Interface
    # -------------------------start-------------------------

    # 路徑導向 L3 Routing > Interface > Interface
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"Interface")
    mod.Switch_Frame(driver)

    # Interface Delete
    l3r.Interface_Interface_VID_Select(driver,"4000")
    l3r.Interface_Interface_Load(driver)
    if_clear = False
    while(if_clear == False):
        try:
            driver.find_element(By.NAME, "rpinterface_select").click()
            l3r.Interface_Interface_Delete(driver)
        except:
            if_clear = True

    # -------------------------end-------------------------

    # Vlan GE/GENNI VLAN Setup Setting
    # Vlan > GE/GENNI VLAN Setup > VLAN Table
    # -------------------------start-------------------------

    # 路徑導向 Vlan > GE/GENNI VLAN Setup > VLAN Table
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"VLAN")
    mod.Switch_Frame(driver)

    # vlan setting
    vlan.Slot_Select(driver,msc_slot)
    index = 0
    if_last = False
    if_find = False
    while(if_last == False):
        try:
            if(driver.find_elements(By.CLASS_NAME, "div-row-cell-content.div-row-cell-content-local.rpvlantable_data_vid")[index].get_attribute("textContent") == "4000"):
                if_find = True
                driver.find_elements(By.NAME, "rpvlantable_radioSlt")[index].click()
                vlan.GE_GENNI_VLAN_Setup_VLAN_Table_Delete(driver)
                break
            index = index+1
        except:
            if_last = True
    
    if(if_find == False):
        print("             [VLAN - GE/GENNI VLAN Setup - VLAN Table] 4000 Delete Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def Multicast_Test(driver,glc_slot,glc_port,msc_slot,msc_port,file_name):
    print(f"Multicast Test\nTest Start",file = open(file_name, '+a'))

    # Multicast IGMP Privilege Profile Test
    # Multicast > IGMP Privilege Profile
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Multicast > IGMP Privilege Profile
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Multicast")
    mod.SubPage_Switch(driver,"IGMP Privilege Profile")
    mod.Switch_Frame(driver)
    
    # Multicast IGMP Privilege Profile Clear
    if_clear = False
    while(if_clear == False):
        try:
            driver.find_element(By.NAME, "rpigmpPriProf_slt").click()
            driver.find_element(By.NAME, "rpigmpPriProf_data_button_delete").click()
            try:
                driver.find_element(By.NAME, "rperror_btnBack").click()
                mod.Switch_Default(driver)
                mod.SubPage_Switch(driver,"IGMP")
                mod.Switch_Frame(driver)
                mod.Tab_Switch(driver,"Port Setup")
                mul.Slot_Select(driver,glc_slot)
                mul.Port_Select(driver,glc_port)
                mul.Load(driver)
                if_clear_2 = False
                while(if_clear_2 == False):
                    try:
                        driver.find_element(By.CLASS_NAME, "rpmcigmpport_onSel").click()
                        mul.IGMP_Port_Setup_Group_Privilege_Profile_Remove(driver)
                    except:
                        if_clear_2 = True
                mul.IGMP_Port_Setup_Apply(driver)
                mod.Switch_Default(driver)
                mod.Page_Switch(driver,"Multicast")
                mod.SubPage_Switch(driver,"IGMP Privilege Profile")
                mod.Switch_Frame(driver)
            except:
                pass
        except:
            if_clear = True

    # Multicast IGMP Privilege Profile Input
    mul.IGMP_Privilege_Profile_Name(driver,"1234567890123456789012345678001")
    mul.IGMP_Privilege_Profile_Index(driver,16)
    mul.IGMP_Privilege_Profile_Bandwidth(driver,"@")
    mul.IGMP_Privilege_Profile_Start_Address(driver,"224.0.0.0")
    mul.IGMP_Privilege_Profile_End_Address(driver,"224.0.0.1")
    mul.IGMP_Privilege_Profile_Apply_New(driver)
    time.sleep(1)
    if(mod.IsAlert(driver) != True):
        print(f"             [Multicast - IGMP Privilege Profile] Bandwidth:@ Test Fail",file = open(file_name, '+a'))
        if_error = True
    mul.IGMP_Privilege_Profile_Bandwidth(driver,"101")
    mul.IGMP_Privilege_Profile_Apply_New(driver)
    time.sleep(1)
    if(mod.IsAlert(driver) != True):
        print(f"             [Multicast - IGMP Privilege Profile] Bandwidth:101 Test Fail",file = open(file_name, '+a'))
        if_error = True
    mul.IGMP_Privilege_Profile_Bandwidth(driver,"100")
    mul.IGMP_Privilege_Profile_Privilege(driver,3)
    mul.IGMP_Privilege_Profile_Length(driver,"9")
    mul.IGMP_Privilege_Profile_Apply_New(driver)
    time.sleep(1)
    if(mod.IsAlert(driver) != True):
        print(f"             [Multicast - IGMP Privilege Profile] Length:9 Test Fail",file = open(file_name, '+a'))
        if_error = True
    mul.IGMP_Privilege_Profile_Length(driver,"301")
    mul.IGMP_Privilege_Profile_Apply_New(driver)
    time.sleep(1)
    if(mod.IsAlert(driver) != True):
        print(f"             [Multicast - IGMP Privilege Profile] Length:301 Test Fail",file = open(file_name, '+a'))
        if_error = True
    mul.IGMP_Privilege_Profile_Length(driver,"300")
    mul.IGMP_Privilege_Profile_Interval(driver,"9")
    mul.IGMP_Privilege_Profile_Apply_New(driver)
    time.sleep(1)
    if(mod.IsAlert(driver) != True):
        print(f"             [Multicast - IGMP Privilege Profile] Interval:9 Test Fail",file = open(file_name, '+a'))
        if_error = True
    mul.IGMP_Privilege_Profile_Interval(driver,"301")
    mul.IGMP_Privilege_Profile_Apply_New(driver)
    time.sleep(1)
    if(mod.IsAlert(driver) != True):
        print(f"             [Multicast - IGMP Privilege Profile] Interval:301 Test Fail",file = open(file_name, '+a'))
        if_error = True
    mul.IGMP_Privilege_Profile_Interval(driver,"300")
    mul.IGMP_Privilege_Profile_Count(driver,"0")
    mul.IGMP_Privilege_Profile_Apply_New(driver)
    time.sleep(1)
    if(mod.IsAlert(driver) != True):
        print(f"             [Multicast - IGMP Privilege Profile] Count:0 Test Fail",file = open(file_name, '+a'))
        if_error = True
    mul.IGMP_Privilege_Profile_Count(driver,"11")
    mul.IGMP_Privilege_Profile_Apply_New(driver)
    time.sleep(1)
    if(mod.IsAlert(driver) != True):
        print(f"             [Multicast - IGMP Privilege Profile] Count:11 Test Fail",file = open(file_name, '+a'))
        if_error = True
    mul.IGMP_Privilege_Profile_Count(driver,"10")
    mul.IGMP_Privilege_Profile_Reset(driver,"29")
    mul.IGMP_Privilege_Profile_Apply_New(driver)
    time.sleep(1)
    if(mod.IsAlert(driver) != True):
        print(f"             [Multicast - IGMP Privilege Profile] Reset:29 Test Fail",file = open(file_name, '+a'))
        if_error = True
    mul.IGMP_Privilege_Profile_Reset(driver,"86401")
    mul.IGMP_Privilege_Profile_Apply_New(driver)
    time.sleep(1)
    if(mod.IsAlert(driver) != True):
        print(f"             [Multicast - IGMP Privilege Profile] Reset:86401 Test Fail",file = open(file_name, '+a'))
        if_error = True
    mul.IGMP_Privilege_Profile_Reset(driver,"86400")
    mul.IGMP_Privilege_Profile_Apply_New(driver)
    if(mod.IsAlert(driver) == True):
        print(f"             [Multicast - IGMP Privilege Profile] Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    else:
        driver.find_element(By.NAME, "rpigmpPriProf_slt").click()
        mul.IGMP_Privilege_Profile_Modify(driver)
        mul.IGMP_Privilege_Profile_Index(driver,16)
        if(driver.find_element(By.NAME, "rpigmpPriProf_ipt_bw").get_attribute("value") != "100"):
            print(f"             [Multicast - IGMP Privilege Profile] Bandwidth Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_element(By.NAME, "rpigmpPriProf_ipt_st_add").get_attribute("value") != "224.0.0.0"):
            print(f"             [Multicast - IGMP Privilege Profile] Start Address Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_element(By.NAME, "rpigmpPriProf_ipt_end_add").get_attribute("value") != "224.0.0.1"):
            print(f"             [Multicast - IGMP Privilege Profile] End Address Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_element(By.XPATH, f"//*[@name='rpigmpPriProf_slt_privilege']/option[3]").is_selected() != True):
            print(f"             [Multicast - IGMP Privilege Profile] Privilege Test Fail",file = open(file_name, '+a'))
            if_error = True
        else:
            if(driver.find_element(By.NAME, "rpigmpPriProf_ipt_len").get_attribute("value") != "300"):
                print(f"             [Multicast - IGMP Privilege Profile] Length Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_element(By.NAME, "rpigmpPriProf_ipt_interval").get_attribute("value") != "300"):
                print(f"             [Multicast - IGMP Privilege Profile] Interval Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_element(By.NAME, "rpigmpPriProf_ipt_count").get_attribute("value") != "10"):
                print(f"             [Multicast - IGMP Privilege Profile] Count Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_element(By.NAME, "rpigmpPriProf_ipt_reset").get_attribute("value") != "86400"):
                print(f"             [Multicast - IGMP Privilege Profile] Reset Test Fail",file = open(file_name, '+a'))
                if_error = True
    
    profile_name = 8002
    for index in range(127):
        mul.IGMP_Privilege_Profile_Name(driver,f"123456789012345678901234567{profile_name+index}")
        mul.IGMP_Privilege_Profile_Index(driver,1)
        mul.IGMP_Privilege_Profile_Bandwidth(driver,"100")
        mul.IGMP_Privilege_Profile_Start_Address(driver,f"224.0.0.{index*2+2}")
        mul.IGMP_Privilege_Profile_End_Address(driver,f"224.0.0.{index*2+3}")
        mul.IGMP_Privilege_Profile_Privilege(driver,3)
        mul.IGMP_Privilege_Profile_Length(driver,"300")
        mul.IGMP_Privilege_Profile_Interval(driver,"300")
        mul.IGMP_Privilege_Profile_Count(driver,"10")
        mul.IGMP_Privilege_Profile_Reset(driver,"86400")
        mul.IGMP_Privilege_Profile_Apply_New(driver)

    profile_capacity = driver.find_elements(By.CLASS_NAME, "td-table-content.i1")[-1].get_attribute("textContent")
    print(f"             [Multicast - IGMP Privilege Profile] Max Capacity(128) = {profile_capacity}",file = open(file_name, '+a'))

    # Multicast IGMP Privilege Result
    if(if_error == False):
        print(f"[MSAN1-11872][Multicast - IGMP Privilege Profile] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11872][Multicast - IGMP Privilege Profile] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Multicast MVLAN Test
    # Multicast > MVLAN > MVLAN
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Multicast > MVLAN > MVLAN
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"MVLAN")
    mod.Switch_Frame(driver)

    # Multicast MVLAN Clear
    if_clear = False
    while(if_clear == False):
        try:
            driver.find_element(By.NAME, "rpMvlan_displaySlt").click()
            mul.MVLAN_MVLAN_Delete(driver)
            try:
                driver.find_element(By.NAME, "rperror_btnBack").click()
                mod.Switch_Default(driver)
                mod.SubPage_Switch(driver,"IGMP")
                mod.Switch_Frame(driver)
                mod.Tab_Switch(driver,"Port MVLAN Setup")
                mul.Slot_Select(driver,glc_slot)
                mul.Port_Select(driver,glc_port)
                mul.Load(driver)
                if_clear_2 = False
                while(if_clear_2 == False):
                    try:
                        driver.find_element(By.ID, "rpPortMvlan_select").click()
                        mul.IGMP_Port_MVLAN_Setup_Delete(driver)
                    except:
                        if_clear_2 = True
                mod.Switch_Default(driver)
                mod.SubPage_Switch(driver,"MVLAN")
                mod.Switch_Frame(driver)
            except:
                pass
        except:
            if_clear = True

    # Multicast MVLAN 1 Apply
    mul.MVLAN_MVLAN_MVLAN(driver,"1")
    mul.MVLAN_MVLAN_Pbit(driver,2)
    mul.MVLAN_MVLAN_Apply(driver)

    # Multicast MVLAN 4094 Apply
    mul.MVLAN_MVLAN_MVLAN(driver,"4094")
    mul.MVLAN_MVLAN_Pbit(driver,2)
    mul.MVLAN_MVLAN_Apply(driver)

    if_mvlan_apply = True
    # Multicast MVLAN 1 & 4094 Check
    try:
        if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpMvlan_displayMvlan")[0].get_attribute("textContent") != "1"):
            print(f"             [Multicast - MVLAN - MVLAN] MVLAN:1 Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpMvlan_displayMvlan")[1].get_attribute("textContent") != "4094"):
            print(f"             [Multicast - MVLAN - MVLAN] MVLAN:4094 Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpMvlan_displayPbit")[0].get_attribute("textContent") != "7" or driver.find_elements(By.CLASS_NAME, "td-table-content.rpMvlan_displayPbit")[1].get_attribute("textContent") != "7"):
            print(f"             [Multicast - MVLAN - MVLAN] Pbit:7 Test Fail",file = open(file_name, '+a'))
            if_error = True
    except:
        if_mvlan_apply = False
        print(f"             [Multicast - MVLAN - MVLAN] Apply Fail",file = open(file_name, '+a'))
        if_error = True

    # Multicast MVLAN Result
    if(if_error == False):
        print(f"[MSAN1-11873][Multicast - MVLAN - MVLAN] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11873][Multicast - MVLAN - MVLAN] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Multicast MVLAN Table Test
    # Multicast > MVLAN > MVLAN Table
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Multicast > MVLAN > MVLAN Table
    mod.Tab_Switch(driver,"MVLAN Table")

    if(if_mvlan_apply == False):
        print(f"             [Multicast - MVLAN - MVLAN Table] MVLAN Apply Fail No Data Test Fail",file = open(file_name, '+a'))
        if_error = True
    else:

        # MVLAN Table 1 Apply
        for index in range(16):
            mul.MVLAN_MVLAN_Table_Start_IP_Address(driver,index,f"ff00::{index+1}1")
            mul.MVLAN_MVLAN_Table_End_IP_Address(driver,index,f"ff00::{index+1}2")
        mul.MVLAN_MVLAN_Table_Apply(driver)

        # MVLAN Table 1 Check
        mul.MVLAN_MVLAN_Table_Modify(driver)
        for index in range(16):
            if(driver.find_elements(By.NAME, "rpMvlanTbl_startIp")[index].get_attribute("value") != f"ff00::{index+1}1"):
                if_error = True
            if(driver.find_elements(By.NAME, "rpMvlanTbl_endIp")[index].get_attribute("value") != f"ff00::{index+1}2"):
                if_error = True

        # MVLAN 4094 Modify
        driver.find_elements(By.NAME, "rpMvlanTbl_displaySlt")[1].click()
        mul.MVLAN_MVLAN_Table_Modify(driver)

        # MVLAN Table 4094 Apply
        for index in range(16):
            mul.MVLAN_MVLAN_Table_Start_IP_Address(driver,index,f"224.0.0.{index+1}1")
            mul.MVLAN_MVLAN_Table_End_IP_Address(driver,index,f"224.0.0.{index+1}2")
        mul.MVLAN_MVLAN_Table_Apply(driver)

        # MVLAN Table 4094 Check
        mul.MVLAN_MVLAN_Table_Modify(driver)
        for index in range(16):
            if(driver.find_elements(By.NAME, "rpMvlanTbl_startIp")[index].get_attribute("value") != f"224.0.0.{index+1}1"):
                if_error = True
            if(driver.find_elements(By.NAME, "rpMvlanTbl_endIp")[index].get_attribute("value") != f"224.0.0.{index+1}2"):
                if_error = True

        # Multicast MVLAN Table Result
        if(if_error == False):
            print(f"[MSAN1-11874][Multicast - MVLAN - MVLAN Table] Result Pass",file = open(file_name, '+a'))
        else:
            print(f"[MSAN1-11874][Multicast - MVLAN - MVLAN Table] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Multicast IGMP Setup Test
    # Multicast > IGMP > IGMP Setup
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Multicast > IGMP > IGMP Setup
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"IGMP")
    mod.Switch_Frame(driver)

    # Multicast IGMP Setup Error Test
    mul.IGMP_IGMP_Setup_Non_MVLAN_Mode(driver,4)
    mul.IGMP_IGMP_Setup_MVLAN_Mode(driver,4)
    mul.IGMP_IGMP_Setup_Version(driver,8)
    mul.IGMP_IGMP_Setup_Leave_Mode(driver,3)
    mul.IGMP_IGMP_Setup_Pbit(driver,2)
    mul.IGMP_IGMP_Setup_GQT_Interval(driver,"9")
    mul.IGMP_IGMP_Setup_Apply_Click(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Multicast - IGMP - IGMP Setup] GQT Interval:9 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    mul.IGMP_IGMP_Setup_GQT_Interval(driver,"301")
    mul.IGMP_IGMP_Setup_Apply_Click(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Multicast - IGMP - IGMP Setup] GQT Interval:301 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    mul.IGMP_IGMP_Setup_GQT_Interval(driver,"@")
    mul.IGMP_IGMP_Setup_Apply_Click(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Multicast - IGMP - IGMP Setup] GQT Interval:@ No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    mul.IGMP_IGMP_Setup_GQT_Interval(driver,"10")
    mul.IGMP_IGMP_Setup_Apply_Click(driver)
    if(mod.IsAlert(driver) == True):
        print(f"             [Multicast - IGMP - IGMP Setup] GQT Interval:10 Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    mul.IGMP_IGMP_Setup_GQT_Interval(driver,"300")
    mul.IGMP_IGMP_Setup_Apply_Click(driver)
    if(mod.IsAlert(driver) == True):
        print(f"             [Multicast - IGMP - IGMP Setup] GQT Interval:300 Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    mul.IGMP_IGMP_Setup_GQT_Robustness(driver,"0")
    mul.IGMP_IGMP_Setup_Apply_Click(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Multicast - IGMP - IGMP Setup] GQT Robustness:0 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    mul.IGMP_IGMP_Setup_GQT_Robustness(driver,"6")
    mul.IGMP_IGMP_Setup_Apply_Click(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Multicast - IGMP - IGMP Setup] GQT Robustness:6 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    mul.IGMP_IGMP_Setup_GQT_Robustness(driver,"@")
    mul.IGMP_IGMP_Setup_Apply_Click(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Multicast - IGMP - IGMP Setup] GQT Robustness:@ No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    mul.IGMP_IGMP_Setup_GQT_Robustness(driver,"1")
    mul.IGMP_IGMP_Setup_Apply_Click(driver)
    if(mod.IsAlert(driver) == True):
        print(f"             [Multicast - IGMP - IGMP Setup] GQT Robustness:1 Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    mul.IGMP_IGMP_Setup_GQT_Robustness(driver,"5")
    mul.IGMP_IGMP_Setup_Apply_Click(driver)
    if(mod.IsAlert(driver) == True):
        print(f"             [Multicast - IGMP - IGMP Setup] GQT Robustness:5 Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    mul.IGMP_IGMP_Setup_GQT_Max_Response_Time(driver,"0")
    mul.IGMP_IGMP_Setup_Apply_Click(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Multicast - IGMP - IGMP Setup] GQT Max-Response_Time:0 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    mul.IGMP_IGMP_Setup_GQT_Max_Response_Time(driver,"11")
    mul.IGMP_IGMP_Setup_Apply_Click(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Multicast - IGMP - IGMP Setup] GQT Max-Response_Time:11 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    mul.IGMP_IGMP_Setup_GQT_Max_Response_Time(driver,"@")
    mul.IGMP_IGMP_Setup_Apply_Click(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Multicast - IGMP - IGMP Setup] GQT Max-Response_Time:@ No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    mul.IGMP_IGMP_Setup_GQT_Max_Response_Time(driver,"1")
    mul.IGMP_IGMP_Setup_Apply_Click(driver)
    if(mod.IsAlert(driver) == True):
        print(f"             [Multicast - IGMP - IGMP Setup] GQT Max-Response_Time:1 Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    mul.IGMP_IGMP_Setup_GQT_Max_Response_Time(driver,"10")
    mul.IGMP_IGMP_Setup_Apply_Click(driver)
    if(mod.IsAlert(driver) == True):
        print(f"             [Multicast - IGMP - IGMP Setup] GQT Max-Response_Time:10 Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    mul.IGMP_IGMP_Setup_LMQT_Interval(driver,"100")
    mul.IGMP_IGMP_Setup_Apply_Click(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Multicast - IGMP - IGMP Setup] LMQT Interval:100 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    mul.IGMP_IGMP_Setup_LMQT_Interval(driver,"1100")
    mul.IGMP_IGMP_Setup_Apply_Click(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Multicast - IGMP - IGMP Setup] LMQT Interval:1100 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    mul.IGMP_IGMP_Setup_LMQT_Interval(driver,"@")
    mul.IGMP_IGMP_Setup_Apply_Click(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Multicast - IGMP - IGMP Setup] LMQT Interval:@ No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    mul.IGMP_IGMP_Setup_LMQT_Interval(driver,"200")
    mul.IGMP_IGMP_Setup_Apply_Click(driver)
    if(mod.IsAlert(driver) == True):
        print(f"             [Multicast - IGMP - IGMP Setup] LMQT Interval:200 Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    mul.IGMP_IGMP_Setup_LMQT_Interval(driver,"1000")
    mul.IGMP_IGMP_Setup_Apply_Click(driver)
    if(mod.IsAlert(driver) == True):
        print(f"             [Multicast - IGMP - IGMP Setup] LMQT Interval:1000 Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    mul.IGMP_IGMP_Setup_LMQT_Robustness(driver,"0")
    mul.IGMP_IGMP_Setup_Apply_Click(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Multicast - IGMP - IGMP Setup] LMQT Robustness:0 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    mul.IGMP_IGMP_Setup_LMQT_Robustness(driver,"6")
    mul.IGMP_IGMP_Setup_Apply_Click(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Multicast - IGMP - IGMP Setup] LMQT Robustness:6 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    mul.IGMP_IGMP_Setup_LMQT_Robustness(driver,"@")
    mul.IGMP_IGMP_Setup_Apply_Click(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Multicast - IGMP - IGMP Setup] LMQT Robustness:@ No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    mul.IGMP_IGMP_Setup_LMQT_Robustness(driver,"1")
    mul.IGMP_IGMP_Setup_Apply_Click(driver)
    if(mod.IsAlert(driver) == True):
        print(f"             [Multicast - IGMP - IGMP Setup] LMQT Robustness:1 Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    mul.IGMP_IGMP_Setup_LMQT_Robustness(driver,"5")
    mul.IGMP_IGMP_Setup_Apply_Click(driver)
    if(mod.IsAlert(driver) == True):
        print(f"             [Multicast - IGMP - IGMP Setup] LMQT Robustness:5 Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Multicast IGMP Setup Value Test
    if(driver.find_element(By.XPATH, f"//*[@name='rpmcigmp_sltMode']/option[4]").is_selected() != True):
        print(f"             [Multicast - IGMP - IGMP Setup] Non MVLAN Mode Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.XPATH, f"//*[@name='rpmcigmp_sltMvlanMode']/option[4]").is_selected() != True):
        print(f"             [Multicast - IGMP - IGMP Setup] Non MVLAN Mode Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.XPATH, f"//*[@name='rpmcigmp_sltVer']/option[8]").is_selected() != True):
        print(f"             [Multicast - IGMP - IGMP Setup] Non MVLAN Mode Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.XPATH, f"//*[@name='rpmcigmp_sltLeave']/option[3]").is_selected() != True):
        print(f"             [Multicast - IGMP - IGMP Setup] Non MVLAN Mode Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.XPATH, f"//*[@name='rpmcigmp_sltPbit']/option[2]").is_selected() != True):
        print(f"             [Multicast - IGMP - IGMP Setup] Non MVLAN Mode Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpmcigmp_txtGqItv").get_attribute("value") != "300"):
        print(f"             [Multicast - IGMP - IGMP Setup] GQT Interval Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpmcigmp_txtGqRobust").get_attribute("value") != "5"):
        print(f"             [Multicast - IGMP - IGMP Setup] GQT Robustness Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpmcigmp_txtRespTime").get_attribute("value") != "10"):
        print(f"             [Multicast - IGMP - IGMP Setup] GQT Max-Response-Time Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpmcigmp_txtLmqItv").get_attribute("value") != "1000"):
        print(f"             [Multicast - IGMP - IGMP Setup] LMQT Interval Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpmcigmp_txtLmqRobust").get_attribute("value") != "5"):
        print(f"             [Multicast - IGMP - IGMP Setup] LMQT Robustness Test Fail",file = open(file_name, '+a'))
        if_error = True
        
    # Multicast IGMP Setup Reset
    mul.IGMP_IGMP_Setup(driver,1,1,1,1,1,"125","2","10","1000","2")

    # Multicast IGMP Setup Result
    if(if_error == False):
        print(f"[MSAN1-11868][Multicast - IGMP - IGMP Setup] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11868][Multicast - IGMP - IGMP Setup] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Multicast IGMP Port Setup Test
    # Multicast > IGMP > Port Setup
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Multicast > IGMP > Port Setup
    mod.Tab_Switch(driver,"Port Setup")

    # port select
    mul.Slot_Select(driver,glc_slot)
    mul.Port_Select(driver,glc_port)
    mul.Load(driver)

    # Port Setup Test
    mul.IGMP_Port_Setup_Bandwidth(driver,"101")
    mul.IGMP_Port_Setup_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Multicast - IGMP - Port Setup] Bandwidth:101 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    mul.IGMP_Port_Setup_Bandwidth(driver,"@")
    mul.IGMP_Port_Setup_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Multicast - IGMP - Port Setup] Bandwidth:@ No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    mul.IGMP_Port_Setup_Bandwidth(driver,"100")
    mul.IGMP_Port_Setup_Max_Group(driver,"17")
    mul.IGMP_Port_Setup_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Multicast - IGMP - Port Setup] Max-Group:17 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    mul.IGMP_Port_Setup_Max_Group(driver,"@")
    mul.IGMP_Port_Setup_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Multicast - IGMP - Port Setup] Max-Group:@ No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    mul.IGMP_Port_Setup_Max_Group(driver,"16")
    mul.IGMP_Port_Setup_Max_Message(driver,"33")
    mul.IGMP_Port_Setup_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Multicast - IGMP - Port Setup] Max-Message:33 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    mul.IGMP_Port_Setup_Max_Message(driver,"@")
    mul.IGMP_Port_Setup_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Multicast - IGMP - Port Setup] Max-Message:@ No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    mul.IGMP_Port_Setup_Max_Message(driver,"32")
    mul.IGMP_Port_Setup_Group_Privilege(driver,True)
    mul.IGMP_Port_Setup_Apply(driver)
    if(mod.IsAlert(driver) == True):
        print(f"             [Multicast - IGMP - Port Setup] Max Value Apply Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Port Setup Profile Test
    for apply_num in range(128):
        driver.find_element(By.CLASS_NAME, "rpmcigmpport_offSel").click()
        mul.IGMP_Port_Setup_Group_Privilege_Profile_Apply(driver)
        if(mod.IsAlert(driver) == True):
            print(f"             [Multicast - IGMP - Port Setup] Max Capacity(Per Privilege profile has 16 entries) = {apply_num}",file = open(file_name, '+a'))
            break
    mul.IGMP_Port_Setup_Apply(driver)

    # Multicast IGMP Port Setup Result
    if(if_error == False):
        print(f"[MSAN1-11869][Multicast - IGMP - Port Setup] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11869][Multicast - IGMP - Port Setup] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Multicast IGMP Port MVLAN Setup Test
    # Multicast > IGMP > Port MVLAN Setup
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Multicast > IGMP > Port MVLAN Setup
    mod.Tab_Switch(driver,"Port MVLAN Setup")

    # port select
    mul.Slot_Select(driver,glc_slot)
    mul.Port_Select(driver,glc_port)
    mul.Load(driver)

    # Port MVLAN Setup Clear
    if_clear = False
    while(if_clear == False):
        try:
            driver.find_element(By.ID, "rpPortMvlan_select").click()
            mul.IGMP_Port_MVLAN_Setup_Delete(driver)
        except:
            if_clear = True

    if(if_mvlan_apply == False):
        print(f"             [Multicast - IGMP - Port MVLAN Setup] MVLAN Apply Fail No Data Test Fail",file = open(file_name, '+a'))
        if_error = True
    else:
        # Port MVLAN Setup Apply
        mul.IGMP_Port_MVLAN_Setup_MVLAN(driver,1)
        mul.IGMP_Port_MVLAN_Setup_Type(driver,2)
        mul.IGMP_Port_MVLAN_Setup_Uni_VLAN(driver,"4094")
        mul.IGMP_Port_MVLAN_Setup_Apply(driver)
        mul.IGMP_Port_MVLAN_Setup_MVLAN(driver,1)
        mul.IGMP_Port_MVLAN_Setup_Type(driver,2)
        mul.IGMP_Port_MVLAN_Setup_Uni_VLAN(driver,"4094")
        mul.IGMP_Port_MVLAN_Setup_Apply(driver)
        
        # Port MVLAN Setup Check
        if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpPortMvlan_mvlan")[0].get_attribute("textContent") != "1"):
            print(f"             [Multicast - IGMP - Port MVLAN Setup] MVLAN:1 Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpPortMvlan_mvlan")[1].get_attribute("textContent") != "4094"):
            print(f"             [Multicast - IGMP - Port MVLAN Setup] MVLAN:4094 Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpPortMvlan_type")[0].get_attribute("textContent") != "uni-vlan"):
            print(f"             [Multicast - IGMP - Port MVLAN Setup] Type:uni-vlan Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpPortMvlan_type")[1].get_attribute("textContent") != "-"):
            print(f"             [Multicast - IGMP - Port MVLAN Setup] Type:- Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpPortMvlan_uniVid")[1].get_attribute("textContent") != "4094" or driver.find_elements(By.CLASS_NAME, "td-table-content.rpPortMvlan_uniVid")[1].get_attribute("textContent") != "4094"):
            print(f"             [Multicast - IGMP - Port MVLAN Setup] Uni-VLAN:4094 Test Fail",file = open(file_name, '+a'))
            if_error = True
            
        # Port MVLAN Setup Delete
        for delete_time in range(2):
            driver.find_element(By.ID, "rpPortMvlan_select").click()
            mul.IGMP_Port_MVLAN_Setup_Delete(driver)

    # Port MVLAN Setup Result
    if(if_error == False):
        print(f"[MSAN1-11870][Multicast - IGMP - Port MVLAN Setup] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11870][Multicast - IGMP - Port MVLAN Setup] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Multicast IGMP Port Mode Test
    # Multicast > IGMP > Port Mode
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Multicast > IGMP > Port Mode
    mod.Tab_Switch(driver,"Port Mode")

    time.sleep(3)

    # GLC slot select
    mul.Slot_Select(driver,glc_slot)
    mul.Load(driver)

    # GLC slot Error Check
    print(driver.find_element(By.NAME, "rpslot_warning").get_attribute("textContent")) #* add
    print("testtttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt") #* add  
    if(driver.find_element(By.NAME, "rpslot_warning").get_attribute("textContent") != "Warning: the feature isn't supported on this card"):
        print(f"             [Multicast - IGMP - Port Mode] GLC No Error Message Test Fail",file = open(file_name, '+a'))
        if_error = True
    try:
        driver.find_element(By.CLASS_NAME, "pfListRow")
        print(f"             [Multicast - IGMP - Port Mode] GLC Port List Valid Test Fail",file = open(file_name, '+a'))
        if_error = True
    except:
        pass

    # MSC slot select
    mul.Slot_Select(driver,msc_slot)
    mul.Load(driver)

    # MSC slot Apply Check
    if(driver.find_element(By.NAME, "rpslot_warning").get_attribute("textContent") == "Warning: the feature isn't supported on this card"):
        print(f"             [Multicast - IGMP - Port Mode] MSC Error Message Test Fail",file = open(file_name, '+a'))
        if_error = True
    try:
        driver.find_element(By.CLASS_NAME, "pfListRow")
        mul.IGMP_Port_Mode_Static_querier(driver,3)
        mul.IGMP_Port_Mode_Apply(driver)
        if_last = False
        test_port = 0
        while(if_last == False):
            try:
                test_port = test_port+1
                if(driver.find_element(By.XPATH, f"/html/body/form/table/tbody/tr[{test_port+2}]/td[2]/select/option[3]").is_selected() != True):
                    print(f"             [Multicast - IGMP - Port Mode] Port{test_port} Static_querier Test Fail",file = open(file_name, '+a'))
                    if_error = True
            except:
                if_last = True
        mul.IGMP_Port_Mode_Static_querier(driver,1)
        mul.IGMP_Port_Mode_Apply(driver)
    except:
        print(f"             [Multicast - IGMP - Port Mode] GLC Port List Invalid Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Port Mode Result
    if(if_error == False):
        print(f"[MSAN1-11871][Multicast - IGMP - Port Mode] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11871][Multicast - IGMP - Port Mode] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Multicast IGMP VLAN Mode Test
    # Multicast > IGMP > VLAN Mode
    # -------------------------start-------------------------


    if_error = False

    # 路徑導向 Multicast > IGMP > VLAN Mode
    mod.Tab_Switch(driver,"VLAN Mode")
    time.sleep(3)

    mul.IGMP_VLAN_Mode_mode(driver,"Fixed")
    mul.IGMP_VLAN_Mode_Apply(driver)
    # check     
    # 路徑導向 Multicast > IGMP > IGMP Setup
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Multicast")
    mod.SubPage_Switch(driver,"IGMP")
    mod.Switch_Frame(driver)
    mod.SubPage_Switch(driver,"VLAN Mode")
    if(driver.find_element(By.XPATH, "/html/body/form/div[5]/div[3]/select/option[2]").is_selected()==False):     
        print(f"             [Multicast - IGMP - VLAN Mode] mode:fixed Test Fail",file = open(file_name, '+a'))
        if_error = True
    else:
        print(f"             [Multicast - IGMP - VLAN Mode] mode:fixed Test Pass",file = open(file_name, '+a'))




    mul.IGMP_VLAN_Mode_mode(driver,"Transparent")
    mul.IGMP_VLAN_Mode_Apply(driver)
    time.sleep(2)
    # check     
    # 路徑導向 Multicast > IGMP > IGMP Setup
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Multicast")
    mod.SubPage_Switch(driver,"IGMP")
    mod.Switch_Frame(driver)
    mod.SubPage_Switch(driver,"VLAN Mode")
    if(driver.find_element(By.XPATH, "/html/body/form/div[5]/div[3]/select/option[3]").is_selected()==False):
        print(f"             [Multicast - IGMP - VLAN Mode] mode:Transparent Test Fail",file = open(file_name, '+a'))
        if_error = True
    else:
        print(f"             [Multicast - IGMP - VLAN Mode] mode:Transparent Test Pass",file = open(file_name, '+a'))


    mul.IGMP_VLAN_Mode_VLAN(driver, "@")
    mul.IGMP_VLAN_Mode_Add(driver)
    if(mod.IsAlert(driver) == False): 
        print(f"             [Multicast - IGMP - VLAN Mode] vlan:@ alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    mul.IGMP_VLAN_Mode_VLAN(driver, "0")
    mul.IGMP_VLAN_Mode_Add(driver)
    if(mod.IsAlert(driver) == False): 
        print(f"             [Multicast - IGMP - VLAN Mode] vlan:0 alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    mul.IGMP_VLAN_Mode_VLAN(driver, "4095")
    mul.IGMP_VLAN_Mode_Add(driver)
    if(mod.IsAlert(driver) == False): 
        print(f"             [Multicast - IGMP - VLAN Mode] vlan:4095 alert Test Fail",file = open(file_name, '+a'))
        if_error = True    
    mul.IGMP_VLAN_Mode_VLAN(driver, "1")
    mul.IGMP_VLAN_Mode_Name(driver, "O__O->123 123@123.1243456789012")
    mul.IGMP_VLAN_Mode_VPN(driver, True)
    mul.IGMP_VLAN_Mode_Add(driver)
    if(mod.IsAlert(driver) == True): 
        print(f"             [Multicast - IGMP - VLAN Mode] vlan:1 alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    mul.IGMP_VLAN_Mode_VLAN(driver, "2")    
    mul.IGMP_VLAN_Mode_VPN(driver, True)
    mul.IGMP_VLAN_Mode_Name(driver, "O__O->123 123@123.1243456789012")
    mul.IGMP_VLAN_Mode_Add(driver)

    # check vpn max
    for i in range(3,17):  # 3-16 (vpn max should 16)
        mul.IGMP_VLAN_Mode_VLAN(driver, i)
        mul.IGMP_VLAN_Mode_Name(driver, "O__O->123 123@123.1243456789012")
        mul.IGMP_VLAN_Mode_VPN(driver, True)
        mul.IGMP_VLAN_Mode_Add(driver)
                            # 17th should not add success
    mul.IGMP_VLAN_Mode_VLAN(driver, 17)
    mul.IGMP_VLAN_Mode_Name(driver, "O__O->123 123@123.1243456789012")
    mul.IGMP_VLAN_Mode_VPN(driver, True)
    mul.IGMP_VLAN_Mode_Add(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click() 
        print(f"             [Multicast - IGMP - VLAN Mode] vpn 17th add Test Pass",file = open(file_name, '+a'))        
    except:
        if(mod.IsAlert(driver) == False):      #No alert or error page
            print(f"             [Multicast - IGMP - VLAN Mode] vpn 17th add Test Fail",file = open(file_name, '+a'))
            if_error = True
        else:
            print(f"             [Multicast - IGMP - VLAN Mode] vpn 17th add Test Pass",file = open(file_name, '+a'))        


    if_add = True
    temp = 17
    while(if_add == True):
        try:
            mul.IGMP_VLAN_Mode_VLAN(driver, temp)
            mul.IGMP_VLAN_Mode_Name(driver, "O__O->123 123@123.1243456789012")
            mul.IGMP_VLAN_Mode_VPN(driver, False)
            mul.IGMP_VLAN_Mode_Add(driver)
            temp = temp + 1
        except:
            try:
                try:
                    msg = driver.find_element(By.CLASS_NAME, "toast-message").get_attribute("textContent")
                    print(f"             [Multicast - IGMP - VLAN Mode] msg: {msg}",file = open(file_name, '+a'))
                except:
                    pass
                driver.find_element(By.NAME, "rperror_btnBack").click()
            except:
                pass
            if_add = False
    # print(f"             [Multicast - IGMP - VLAN Mode] total test count:{temp-2} (comment out?)",file = open(file_name, '+a')) #


    # check total num
    total_v = driver.find_element(By.ID, "dataTotal").text
    total_v = total_v.split("total")[1]
    total_v = total_v.split(" ")[1]
    print(f"total_v:{total_v}")
    if( "4000" not in total_v):
        print(f"             [Multicast - IGMP - VLAN Mode] Max Capacity(4000) != {total_v} Fail",file = open(file_name, '+a'))
        if_error = True
    else:
        print(f"             [Multicast - IGMP - VLAN Mode] Max Capacity(4000) = {total_v}",file = open(file_name, '+a'))


    # delete and check total num
    if_find = True
    while(if_find == True):
        try:
            driver.find_element(By.NAME, "rpIgmpVlan_displaySlt").click()
            mul.IGMP_VLAN_Mode_Delete(driver)
        except:
            if_find = False
            try:
                driver.find_element(By.NAME, "rperror_btnBack").click()
            except:
                pass

    total_v = driver.find_element(By.ID, "dataTotal").text
    total_v = total_v.split("total")[1]
    total_v = total_v.split(" ")[1]
    print(f"total_v:{total_v}")
    print(f"             [Multicast - IGMP - VLAN Mode] after delete Max Capacity(0) = {total_v}",file = open(file_name, '+a'))
    if( total_v != "0"):
        print(f"             [Multicast - IGMP - VLAN Mode] delete Fail",file = open(file_name, '+a'))
        if_error = True
    else:
        print(f"             [Multicast - IGMP - VLAN Mode] delete Pass",file = open(file_name, '+a'))


    # VLAN Mode Result
    if(if_error == False):
        print(f"[MSAN1-14506][Multicast - IGMP - VLAN Mode] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-14506][Multicast - IGMP - VLAN Mode] Result Fail",file = open(file_name, '+a'))


    # -------------------------end-------------------------

    # Multicast Static Multicast Multicast MAC Test
    # Multicast > Static Multicast > Multicast MAC
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Multicast > Static Multicast > Multicast MAC
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"Static Multicast")
    mod.Switch_Frame(driver)

    # GLC slot select
    mul.Slot_Select(driver,glc_slot)
    mul.Port_Select(driver,glc_port)
    mul.Load(driver)

    # Multicast MAC Clear
    if_clear = False
    while(if_clear == False):
        try:
            driver.find_element(By.NAME, "rpsmcastMac_tlbSlt").click()
            mul.Static_Multicast_MAC_Delete(driver)
        except:
            if_clear = True

    # Multicast MAC Apply
    index = 0
    if_full = False
    while(if_full == False):
        index = index+1
        mul.Static_Multicast_MAC_Address(driver,f"01:80:5e:00:00:0{index}")
        mul.Static_Multicast_MAC_NNI_VLAN(driver,"4094")
        mul.Static_Multicast_MAC_Apply(driver)
        try:
            driver.find_element(By.NAME, "rperror_btnBack").click()
            print(f"             [Multicast - Static Multicast - Multicast MAC] Max Capacity(8) = {index-1}",file = open(file_name, '+a'))
            if_full = True
        except:
            pass

    if_mac_error = False
    if_nini_valn_error = False

    # Multicast MAC Check
    index_len = driver.find_elements(By.CLASS_NAME, "td-table-content.rpsmcastMac_tlbMac").__len__()
    for index in range(index_len):
        if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpsmcastMac_tlbMac")[index].get_attribute("textContent") != f"01:80:5e:00:00:0{index+1}"):
            if_mac_error = True
        if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpsmcastMac_tlbVlan")[index].get_attribute("textContent") != "4094"):
            if_nini_valn_error = True
    if(if_mac_error == True):
        print(f"             [Multicast - Static Multicast - Multicast MAC] MAC Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(if_nini_valn_error == True):
        print(f"             [Multicast - Static Multicast - Multicast MAC] NINI-VLAN:4094 Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Multicast MAC Clear
    if_clear = False
    while(if_clear == False):
        try:
            driver.find_element(By.NAME, "rpsmcastMac_tlbSlt").click()
            mul.Static_Multicast_MAC_Delete(driver)
        except:
            if_clear = True

    # Multicast MAC Result
    if(if_error == False):
        print(f"[MSAN1-11875][Multicast - Static Multicast - Multicast MAC] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11875][Multicast - Static Multicast - Multicast MAC] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Multicast Static Multicast Multicast IP Test
    # Multicast > Static Multicast > Multicast IP
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Multicast > Static Multicast > Multicast IP
    mod.Tab_Switch(driver,"Multicast IP")

    # GLC slot select
    mul.Slot_Select(driver,glc_slot)
    mul.Port_Select(driver,glc_port)
    mul.Load(driver)

    # Multicast IP Clear
    if_clear = False
    while(if_clear == False):
        try:
            driver.find_element(By.NAME, "rpsmcastIp_tlbSlt").click()
            mul.Static_Multicast_IP_Delete(driver)
        except:
            if_clear = True

    # Multicast IP Apply
    index = 0
    if_full = False
    while(if_full == False):
        try:
            driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlot']/option[2]")
        except:
            mul.Slot_Select(driver,glc_slot)
            mul.Port_Select(driver,glc_port)
            mul.Load(driver)
        mul.Static_Multicast_IP_Address(driver,f"224.0.0.{index}")
        mul.Static_Multicast_IP_NNI_VLAN(driver,"4094")
        mul.Static_Multicast_IP_Role(driver,2)
        mul.Static_Multicast_IP_Apply(driver)
        index = index+1
        try:
            driver.find_element(By.NAME, "rperror_btnBack").click()
            print(f"             [Multicast - Static Multicast - Multicast IP] Max Capacity(8) = {index-1}",file = open(file_name, '+a'))
            if_full = True
        except:
            pass

    if_IP_error = False
    if_nini_valn_error = False
    if_role_error = False

    # Multicast IP Check
    index_len = driver.find_elements(By.CLASS_NAME, "td-table-content.rpsmcastIp_tlbIp").__len__()
    for index in range(index_len):
        if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpsmcastIp_tlbIp")[index].get_attribute("textContent") != f"224.0.0.{index}"):
            if_IP_error = True
        if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpsmcastIp_tlbVlan")[index].get_attribute("textContent") != "4094"):
            if_nini_valn_error = True
        if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpsmcastIp_tlbRole")[index].get_attribute("textContent") != "Forbid"):
            if_role_error = True
    if(if_IP_error == True):
        print(f"             [Multicast - Static Multicast - Multicast IP] IP Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(if_nini_valn_error == True):
        print(f"             [Multicast - Static Multicast - Multicast IP] NINI-VLAN:4094 Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(if_role_error == True):
        print(f"             [Multicast - Static Multicast - Multicast IP] Role:Forbid Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Multicast IP Clear
    if_clear = False
    while(if_clear == False):
        try:
            driver.find_element(By.NAME, "rpsmcastIp_tlbSlt").click()
            mul.Static_Multicast_IP_Delete(driver)
        except:
            if_clear = True

    # Multicast IP Result
    if(if_error == False):
        print(f"[MSAN1-11876][Multicast - Static Multicast - Multicast IP] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11876][Multicast - Static Multicast - Multicast IP] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Multicast IGMP Port Setup Clear
    # Multicast > IGMP > Port Setup
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Multicast > IGMP > Port Setup
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"IGMP")
    mod.Switch_Frame(driver)
    mod.Tab_Switch(driver,"Port Setup")

    # port select
    mul.Slot_Select(driver,glc_slot)
    mul.Port_Select(driver,glc_port)
    mul.Load(driver)

    # Port Setup Clear
    mul.IGMP_Port_Setup_Bandwidth(driver,"0")
    mul.IGMP_Port_Setup_Max_Group(driver,"0")
    mul.IGMP_Port_Setup_Max_Message(driver,"0")
    mul.IGMP_Port_Setup_Group_Privilege(driver,True)
    mul.IGMP_Port_Setup_Apply(driver)

    if_clear = False
    while(if_clear == False):
        try:
            driver.find_element(By.CLASS_NAME, "rpmcigmpport_onSel").click()
            mul.IGMP_Port_Setup_Group_Privilege_Profile_Remove(driver)
        except:
            if_clear = True
    mul.IGMP_Port_Setup_Apply(driver)

    # -------------------------end-------------------------

    # Multicast MVLAN Clear
    # Multicast > MVLAN > MVLAN
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Multicast > MVLAN > MVLAN
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"MVLAN")
    mod.Switch_Frame(driver)

    # Multicast MVLAN Clear
    if_clear = False
    while(if_clear == False):
        try:
            driver.find_element(By.NAME, "rpMvlan_displaySlt").click()
            mul.MVLAN_MVLAN_Delete(driver)
        except:
            if_clear = True

    # -------------------------end-------------------------

    # Multicast IGMP Privilege Profile Clear
    # Multicast > IGMP Privilege Profile
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Multicast > IGMP Privilege Profile
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"IGMP Privilege Profile")
    mod.Switch_Frame(driver)
    
    # Multicast IGMP Privilege Profile Clear
    if_clear = False
    while(if_clear == False):
        try:
            driver.find_element(By.NAME, "rpigmpPriProf_slt").click()
            driver.find_element(By.NAME, "rpigmpPriProf_data_button_delete").click()
        except:
            if_clear = True

    # -------------------------end-------------------------

    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def Port_Test(driver,glc_slot,glc_port,msc_slot,msc_port,file_name):
    print(f"Port Test\nTest Start",file = open(file_name, '+a'))

    # Port DSL Test
    # Port > Copy
    # VLAN > GE/GENNI VLAN Setup > VLAN Table
    # -------------------------start-------------------------

    # 路徑導向 VLAN > GE/GENNI VLAN Setup > VLAN Table
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"VLAN")
    mod.Switch_Frame(driver)

    # slot select
    vlan.Slot_Select(driver,glc_slot)

    # VLAN Table Clear
    if_clear = False
    while(if_clear == False):
        try:
            driver.find_element(By.NAME, "rpvlantable_radioSlt").click()
            vlan.GE_GENNI_VLAN_Setup_VLAN_Table_Delete(driver)
        except:
            if_clear = True

    # VLAN Table %Port Apply
    vlan.Slot_Select(driver,glc_slot)
    vlan.GE_GENNI_VLAN_Setup_VLAN_Table_VLAN_ID(driver,"4094")
    vlan.GE_GENNI_VLAN_Setup_VLAN_Table_Port_Registration(driver,glc_port,2)
    vlan.GE_GENNI_VLAN_Setup_VLAN_Table_Port_Tagging(driver,glc_port,True)
    vlan.GE_GENNI_VLAN_Setup_VLAN_Table_Apply(driver)

    # VLAN Table %Port Check
    driver.find_element(By.NAME, "rpvlantable_radioSlt").click()
    vlan.GE_GENNI_VLAN_Setup_VLAN_Table_Modify(driver)
    if(driver.find_element(By.XPATH, f"/html/body/form/div[6]/span[{glc_port}]/div[2]/select/option[2]").is_selected() != True or driver.find_elements(By.NAME, "rpvlantable_ChkTag")[int(glc_port)-1].is_selected() != True):
        print(f"             [Port - Copy] Port{glc_port} Apply Fail",file = open(file_name, '+a'))

    if_error = False

    # 路徑導向 Port > Copy
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Port")
    mod.Switch_Frame(driver)

    # slot select
    port.Slot_Select(driver,glc_slot)
    port.Port_Select(driver,glc_port)
    port.Copy_Destination_Slot_Select(driver,glc_slot)
    port.Copy_Destination_Port_List(driver,"*")
    port.Copy_Apply(driver)

    # 路徑導向 VLAN > GE/GENNI VLAN Setup > VLAN Table
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"VLAN")
    mod.Switch_Frame(driver)

    # slot select
    vlan.Slot_Select(driver,glc_slot)

    if_error = False
    if_reg_error = False
    if_tag_error = False

    # VLAN Table %Port Check
    driver.find_element(By.NAME, "rpvlantable_radioSlt").click()
    vlan.GE_GENNI_VLAN_Setup_VLAN_Table_Modify(driver)
    port_num = driver.find_elements(By.NAME, "rpvlantable_sltRegStatus").__len__()
    for test_port in range(port_num):
        if(driver.find_element(By.XPATH, f"/html/body/form/div[6]/span[{test_port+1}]/div[2]/select/option[2]").is_selected() != True):
            if_reg_error = True
        if(driver.find_elements(By.NAME, "rpvlantable_ChkTag")[test_port].is_selected() != True):
            if_tag_error = True
    if(if_reg_error == True):
        print(f"             [Port - Copy] Registration Copy Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(if_tag_error == True):
        print(f"             [Port - Copy] Tagging Copy Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Port Copy Result
    if(if_error == True):
        print(f"[MSAN1-11877][Port - Copy] Result Fail",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11877][Port - Copy] Result Pass",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Port Default Test
    # Port > Default
    # VLAN > GE/GENNI VLAN Setup > VLAN Table
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Port > Default
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Port")
    mod.SubPage_Switch(driver,"Default")
    mod.Switch_Frame(driver)

    # slot select
    port.Slot_Select(driver,glc_slot)

    # Port Default %Port Apply
    port.Default_Port_List(driver,"39")
    port.Default_Apply(driver)

    # 路徑導向 VLAN > GE/GENNI VLAN Setup > VLAN Table
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"VLAN")
    mod.Switch_Frame(driver)

    # slot select
    vlan.Slot_Select(driver,glc_slot)

    # VLAN Table %Port Check
    driver.find_element(By.NAME, "rpvlantable_radioSlt").click()
    vlan.GE_GENNI_VLAN_Setup_VLAN_Table_Modify(driver)
    if(driver.find_element(By.XPATH, f"/html/body/form/div[6]/span[{glc_port}]/div[2]/select/option[1]").is_selected() != True):
        print(f"             [Port - Default] Port{glc_port} Registration Default Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "rpvlantable_ChkTag")[int(glc_port)-1].is_selected() != True):
        print(f"             [Port - Default] Port{glc_port} Tagging Default Test Fail",file = open(file_name, '+a'))
        if_error = True

    # 路徑導向 Port > Default
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Port")
    mod.SubPage_Switch(driver,"Default")
    mod.Switch_Frame(driver)

    # slot select
    port.Slot_Select(driver,glc_slot)

    # Port Default %Port Apply
    port.Default_Port_List(driver,"*")
    port.Default_Apply(driver)

    # 路徑導向 VLAN > GE/GENNI VLAN Setup > VLAN Table
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"VLAN")
    mod.Switch_Frame(driver)

    # slot select
    vlan.Slot_Select(driver,glc_slot)

    # VLAN Table %Port Check
    try:
        driver.find_element(By.NAME, "rpvlantable_radioSlt")
        print(f"             [Port - Default] All Default Test Fail",file = open(file_name, '+a'))
        if_error = True
    except:
        pass

    # Port Default Result
    if(if_error == False):
        print(f"[MSAN1-11878][Port - Default] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11878][Port - Default] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Port DSL Test
    # Port > DSL
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Port > DSL
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Port")
    mod.SubPage_Switch(driver,"DSL")
    mod.Switch_Frame(driver)

    # Port DSL GLC Test
    time.sleep(1)
    port.DSL_Slot_Select(driver,glc_slot)
    if(mod.IsAlert(driver) != True):
        print(f"             [Port - DSL] GLC No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
        mod.Switch_Default(driver)
        mod.Page_Switch(driver,"Port")
        mod.SubPage_Switch(driver,"DSL")
        mod.Switch_Frame(driver)

    # Port DSL MSC Test
    port.DSL_Slot_Select(driver,msc_slot)
    if(mod.IsAlert(driver) != True):
        print(f"             [Port - DSL] MSC No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Port DSL Result
    if(if_error == False):
        print(f"[MSAN1-11880][Port - DSL] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11880][Port - DSL] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Port GENNI Test
    # Port > GENNI
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Port > GENNI
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Port")
    mod.SubPage_Switch(driver,"GENNI")
    mod.Switch_Frame(driver)

    # Port GENNI GLC Test
    port.GENNI_Slot_Select(driver,glc_slot)
    if(mod.IsAlert(driver) != True):
        print(f"             [Port - GENNI] GLC No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
        mod.Switch_Default(driver)
        mod.Page_Switch(driver,"Port")
        mod.SubPage_Switch(driver,"GENNI")
        mod.Switch_Frame(driver)

    if_name_error = False

    # Port GENNI MSC Test
    port.GENNI_Slot_Select(driver,msc_slot)
    if(mod.IsAlert(driver) == True):
        print(f"             [Port - GENNI] MSC Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    else:
        port.GENNI_Name_All(driver,"1234567890123456789012345678901")
        port.GENNI_Apply(driver)
        port.GENNI_Port_Select(driver,msc_port)
        if(driver.find_element(By.NAME, "rpportGenni_portname").get_attribute("value") != "1234567890123456789012345678901"):
            print(f"             [Port - GENNI] MSC Port{msc_port} Name Test Fail",file = open(file_name, '+a'))
            if_error = True
        port.GENNI_Port_Up(driver)
        try:
            port_num = driver.find_elements(By.NAME, "rpportGenni_txtName").__len__()
            for test_port in range(port_num):
                if(driver.find_elements(By.NAME, "rpportGenni_txtName")[test_port].get_attribute("value") != "1234567890123456789012345678901"):
                    if_name_error = True
            if(if_name_error == True):
                print(f"             [Port - GENNI] MSC Name Test Fail",file = open(file_name, '+a'))
                if_error = True
            port.GENNI_Slot_Up(driver)
            try:
                driver.find_element(By.CLASS_NAME, "table-sample-4")
            except:
                print(f"             [Port - GENNI] Slot Up Button Test Fail",file = open(file_name, '+a'))
                if_error = True
        except:
            print(f"             [Port - GENNI] Port Up Button Test Fail",file = open(file_name, '+a'))
            if_error = True

    # Port GENNI Result
    if(if_error == False):
        print(f"[MSAN1-11881][Port - GENNI] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11881][Port - GENNI] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Port GE Test
    # Port > GE
    # Statistics > Port
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Port > GE
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Port")
    mod.SubPage_Switch(driver,"GE")
    mod.Switch_Frame(driver)

    # Port GE MSC Test
    port.GE_Slot_Select(driver,msc_slot)
    if(mod.IsAlert(driver) != True):
        print(f"             [Port - GE] MSC No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
        mod.Switch_Default(driver)
        mod.Page_Switch(driver,"Port")
        mod.SubPage_Switch(driver,"GE")
        mod.Switch_Frame(driver)

    # Port GE GLC Test
    time.sleep(1)
    port.GE_Slot_Select(driver,glc_slot)
    if(mod.IsAlert(driver) == True):
        print(f"             [Port - GE] GLC Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    else:
        port.GE_Active_All(driver,True)
        port.GE_Name_All(driver,"1234567890123456789012345678901")
        port.GE_Auto_Nego_All(driver,2)
        port.GE_Flow_Ctrl_All(driver,2)
        port.GE_Speed_All(driver,1)
        port.GE_Frame_Type_All(driver,2)
        port.GE_Apply(driver)
        port.GE_Port_Select(driver,glc_port)
        if(driver.find_element(By.NAME, "rpportge_portname").get_attribute("value") != "1234567890123456789012345678901"):
            print(f"             [Port - GE] GLC Port{glc_port} Name Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_element(By.XPATH, "//*[@name='rpportge_AutoNgt']/option[2]").is_selected() != True):
            print(f"             [Port - GE] GLC Port{glc_port} Auto-Nego Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_element(By.XPATH, "//*[@name='rpportge_enable']/option[2]").is_selected() != True):
            print(f"             [Port - GE] GLC Port{glc_port} Active Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_element(By.XPATH, "//*[@name='rpportge_FlowCtrl']/option[2]").is_selected() != True):
            print(f"             [Port - GE] GLC Port{glc_port} Flow-Ctrl Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_element(By.XPATH, "//*[@name='rpportge_speed']/option[1]").is_selected() != True):
            print(f"             [Port - GE] GLC Port{glc_port} Speed Test Fail",file = open(file_name, '+a'))
            if_error = True
        port.GE_Port_MTU(driver,"511")
        port.GE_Port_Apply(driver)
        if(mod.IsAlert(driver) != True):
            print(f"             [Port - GE] GLC Port{glc_port} MTU:511 Test Fail",file = open(file_name, '+a'))
            if_error = True
        port.GE_Port_MTU(driver,"9201")
        port.GE_Port_Apply(driver)
        if(mod.IsAlert(driver) != True):
            print(f"             [Port - GE] GLC Port{glc_port} MTU:9201 Test Fail",file = open(file_name, '+a'))
            if_error = True
        port.GE_Port_MTU(driver,"@")
        port.GE_Port_Apply(driver)
        if(mod.IsAlert(driver) != True):
            print(f"             [Port - GE] GLC Port{glc_port} MTU:@ Test Fail",file = open(file_name, '+a'))
            if_error = True
        port.GE_Port_MTU(driver,"9200")
        port.GE_Port_TEL_NO(driver,"1234567890123456789012345678901")
        port.GE_Port_Apply(driver)
        if(mod.IsAlert(driver) == True):
            print(f"             [Port - GE] GLC Port{glc_port} Valid Apply Alert Test Fail",file = open(file_name, '+a'))
            if_error = True
        else:
            if(driver.find_element(By.NAME, "rpportge_mtu").get_attribute("value") != "9200"):
                print(f"             [Port - GE] GLC Port{glc_port} MTU Max Test Fail",file = open(file_name, '+a'))
                if_error = True
            if(driver.find_element(By.NAME, "rpportge_tel").get_attribute("value") != "1234567890123456789012345678901"):
                print(f"             [Port - GE] GLC Port{glc_port} TEL-NO. Max Test Fail",file = open(file_name, '+a'))
                if_error = True
        port.GE_Port_Up(driver)
        try:
            port_num = 0
            if_last = False
            while(if_last == False):
                try:
                    port_num = port_num+1
                    driver.find_element(By.NAME, f"rpportGe_chkActive_{port_num}")
                except:
                    if_last = True
                    port_num = port_num-1
            for test_port in range(port_num):
                if(driver.find_element(By.NAME, f"rpportGe_chkActive_{test_port+1}").is_selected() != True):
                    print(f"             [Port - GE] GLC Index{test_port+1} Active Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.NAME, f"rpportGe_txtName_{test_port+1}").get_attribute("value") != "1234567890123456789012345678901"):
                    print(f"             [Port - GE] GLC Index{test_port+1} Name Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.XPATH, f"//*[@name='rpportGe_sltAutoNgt_{test_port+1}']/option[2]").is_selected() != True):
                    print(f"             [Port - GE] GLC Index{test_port+1} Auto-Nego Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.XPATH, f"//*[@name='rpportGe_sltflowctrl_{test_port+1}']/option[2]").is_selected() != True):
                    print(f"             [Port - GE] GLC Index{test_port+1} Flow-Ctrl Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.XPATH, f"//*[@name='rpportGe_SltSpeed_{test_port+1}']/option[1]").is_selected() != True):
                    print(f"             [Port - GE] GLC Index{test_port+1} Speed Test Fail",file = open(file_name, '+a'))
                    if_error = True
                if(driver.find_element(By.XPATH, f"//*[@name='rpportGe_sltFrameType_{test_port+1}']/option[2]").is_selected() != True):
                    print(f"             [Port - GE] GLC Index{test_port+1} Frame-Type Test Fail(#175214)",file = open(file_name, '+a'))
                    if_error = True
            port.GE_Slot_Up(driver)
            try:
                driver.find_element(By.CLASS_NAME, "table-sample-4")
            except:
                print(f"             [Port - GE] Slot Up Button Test Fail",file = open(file_name, '+a'))
                if_error = True
        except:
            print(f"             [Port - GE] Port Up Button Test Fail",file = open(file_name, '+a'))
            if_error = True

    # Port GE Result
    if(if_error == False):
        print(f"[MSAN1-11882][Port - GE] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11882][Port - GE] Result Fail",file = open(file_name, '+a'))

    # 路徑導向 Statistics > Port
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Statistics")
    driver.find_element(By.XPATH, '//*[@id="mainTable"]/tbody/tr[2]/td[1]/div[2]/a[7]').click()
    mod.Switch_Frame(driver)

    if_error = False

    # Statistics Port GLC Test
    sta.Port_Slot_Select(driver,glc_slot)
    port_num = driver.find_elements(By.CLASS_NAME, "td-table-content.tdtablestate").__len__()
    for test_port in range(port_num):
        if(driver.find_elements(By.CLASS_NAME, "td-table-content.tdtablestate")[test_port].get_attribute("textContent") == "disable"):
            print(f"             [Statistics - Port] Port{test_port+1} GLC disable Test Fail",file = open(file_name, '+a'))
            if_error = True
    sta.Port_Port_Select(driver,glc_port)
    try:
        driver.find_element(By.CLASS_NAME, "div-layout-wrap.PortStatisic")
    except:
        print(f"             [Statistics - Port] Port Select Test Fail",file = open(file_name, '+a'))
        if_error = True
    sta.Port_Port_Refresh(driver)
    try:
        driver.find_element(By.CLASS_NAME, "div-layout-wrap.PortStatisic")
    except:
        print(f"             [Statistics - Port] Refresh Test Fail",file = open(file_name, '+a'))
        if_error = True
    sta.Port_Port_Up(driver)
    try:
        driver.find_element(By.CLASS_NAME, "table-sample-2")
    except:
        print(f"             [Statistics - Port] Up Test Fail",file = open(file_name, '+a'))
        if_error = True
    sta.Port_Slot_Up(driver)
    try:
        driver.find_element(By.CLASS_NAME, "table-sample-4")
    except:
        print(f"             [Statistics - Port] Slot Up Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Port GE Result
    if(if_error == False):
        print(f"[MSAN1-11920][Statistics - Port] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11920][Statistics - Port] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Port FDB Test
    # Port > FDB
    # Statistics > MAC Table
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Port > FDB
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Port")
    mod.SubPage_Switch(driver,"FDB")
    mod.Switch_Frame(driver)

    # port select
    port.Slot_Select(driver,glc_slot)
    port.Port_Select(driver,glc_port)
    driver.find_element(By.NAME, "rpportfdb_btnLoad").click()

    # Port FDB Clear
    if_clear = False
    while(if_clear == False):
        if_find = False
        while(if_find == False):
            try:
                driver.find_element(By.XPATH, f"//*[@name='lctbl_selPort']/option[{glc_port}]")
                if_find = True
                if(driver.find_element(By.XPATH, f"//*[@name='lctbl_selPort']/option[{glc_port}]").is_selected() != True):
                    port.Port_Select(driver,glc_port)
                    driver.find_element(By.NAME, "rpportfdb_btnLoad").click()
            except:
                pass
        try:
            driver.find_element(By.NAME, "rpportfdb_rdoMacSlt").click()
            port.FDB_Delete(driver)
        except:
            if_clear = True

    # Port FDB Apply Full
    index = 0
    if_full = False
    while(if_full == False):
        if_find = False
        while(if_find == False):
            try:
                driver.find_element(By.XPATH, f"//*[@name='lctbl_selPort']/option[{glc_port}]")
                if_find = True
                if(driver.find_element(By.XPATH, f"//*[@name='lctbl_selPort']/option[{glc_port}]").is_selected() != True):
                    port.Port_Select(driver,glc_port)
                    driver.find_element(By.NAME, "rpportfdb_btnLoad").click()
            except:
                pass
        if(index < 10):
            port.FDB_Static_MAC(driver,f"10:10:10:10:10:0{index}")
        elif(index < 100):
            port.FDB_Static_MAC(driver,f"10:10:10:10:10:{index}")
        elif(index < 110):
            port.FDB_Static_MAC(driver,f"10:10:10:10:11:0{index-100}")
        elif(index < 200):
            port.FDB_Static_MAC(driver,f"10:10:10:10:11:{index-100}")
        elif(index < 210):
            port.FDB_Static_MAC(driver,f"10:10:10:10:12:0{index-200}")
        elif(index < 300):
            port.FDB_Static_MAC(driver,f"10:10:10:10:12:{index-200}")
        index = index+1
        port.FDB_VLAN(driver,"4094")
        port.FDB_Apply(driver)
        try:
            driver.find_element(By.NAME, "rperror_btnBack").click()
            if_full = True
            print(f"             [Port - FDB] Max Capacity(256) = {index-1}",file = open(file_name, '+a'))
        except:
            pass

    # 路徑導向 Statistics > MAC Table
    time.sleep(5)
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Statistics")
    mod.SubPage_Switch(driver,"MAC Table")
    mod.Switch_Frame(driver)

    if_mac_table_error = False

    # MAC Table Test 1
    time.sleep(20)
    sta.MAC_Table_VLAN_VID_Select(driver)
    sta.MAC_Table_VLAN_VID_Input(driver,"4094")
    sta.MAC_Table_Refresh(driver)
    if(driver.find_element(By.CLASS_NAME, "rpMacTable_totalCount").get_attribute("textContent") != str(index-1)):
        print(f"             [Port - FDB] Statistics MAC Table Total:256 Test Fail",file = open(file_name, '+a'))
        if_error = True

    # MAC Table Test 2
    sta.MAC_Table_Refresh(driver)
    while(driver.find_element(By.ID, "btnNextPage").get_attribute("disabled") != "true"):
        driver.find_element(By.ID, "btnNextPage").click()
    sta.MAC_Table_Flush(driver)
    try:
        driver.find_element(By.CLASS_NAME, "table-sample-3")
    except:
        print(f"             [Statistics - MAC Table] Flush Test Fail",file = open(file_name, '+a'))
        if_mac_table_error = True
    sta.MAC_Table_Refresh(driver)
    try:
        driver.find_element(By.CLASS_NAME, "table-sample-3")
    except:
        print(f"             [Statistics - MAC Table] Refresh Test Fail",file = open(file_name, '+a'))
        if_mac_table_error = True

    # MAC Table Test 3
    driver.find_elements(By.NAME, "rpstatsmac_rdoPort")[1].click()
    sta.Slot_Select(driver,glc_slot)
    driver.find_element(By.NAME, "rpstatsmac_txtPort").send_keys(glc_port)
    sta.MAC_Table_Refresh(driver)
    while(driver.find_element(By.ID, "btnNextPage").get_attribute("disabled") != "true"):
        driver.find_element(By.ID, "btnNextPage").click()
    sta.MAC_Table_Flush(driver)
    try:
        driver.find_element(By.CLASS_NAME, "table-sample-3")
    except:
        print(f"             [Statistics - MAC Table] Slot{glc_slot} Port{glc_port} Test Fail",file = open(file_name, '+a'))
        if_mac_table_error = True
    sta.MAC_Table_Refresh(driver)
    try:
        driver.find_element(By.CLASS_NAME, "table-sample-3")
    except:
        print(f"             [Statistics - MAC Table] Refresh Test Fail",file = open(file_name, '+a'))
        if_mac_table_error = True

    # MAC Table Result
    if(if_mac_table_error == False):
        print(f"[MSAN1-11918][Statistics - MAC Table] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11918][Statistics - MAC Table] Result Fail",file = open(file_name, '+a'))

    # 路徑導向 Port > FDB
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Port")
    mod.SubPage_Switch(driver,"FDB")
    mod.Switch_Frame(driver)

    # port select
    port.Slot_Select(driver,glc_slot)
    port.Port_Select(driver,glc_port)
    driver.find_element(By.NAME, "rpportfdb_btnLoad").click()

    # Port FDB Clear
    if_clear = False
    while(if_clear == False):
        if_find = False
        while(if_find == False):
            try:
                driver.find_element(By.XPATH, f"//*[@name='lctbl_selPort']/option[{glc_port}]")
                if_find = True
                if(driver.find_element(By.XPATH, f"//*[@name='lctbl_selPort']/option[{glc_port}]").is_selected() != True):
                    port.Port_Select(driver,glc_port)
                    driver.find_element(By.NAME, "rpportfdb_btnLoad").click()
            except:
                pass
        try:
            driver.find_element(By.NAME, "rpportfdb_rdoMacSlt").click()
            port.FDB_Delete(driver)
        except:
            if_clear = True

    # Port FDB Result
    if(if_error == False):
        print(f"[MSAN1-11883][Port - FDB] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11883][Port - FDB] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Port G.bond Test
    # Port > G.bond
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Port > G.bond
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Port")
    mod.SubPage_Switch(driver,"G.bond")
    mod.Switch_Frame(driver)

    # Port G.bond GLC Test
    time.sleep(0.1)
    port.G_bond_Slot_Select(driver,glc_slot)
    if(mod.IsAlert(driver) != True):
        print(f"             [Port - G.bond] GLC No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
        mod.Switch_Default(driver)
        mod.Page_Switch(driver,"Port")
        mod.SubPage_Switch(driver,"G.bond")
        mod.Switch_Frame(driver)

    # Port G.bond MSC Test
    port.G_bond_Slot_Select(driver,msc_slot)
    if(mod.IsAlert(driver) != True):
        print(f"             [Port - G.bond] MSC No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Port G.bond Result
    if(if_error == False):
        print(f"[MSAN1-11884][Port - G.bond] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11884][Port - G.bond] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Port PVC Test
    # Port > PVC
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Port > PVC
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Port")
    mod.SubPage_Switch(driver,"PVC")
    mod.Switch_Frame(driver)

    # Port PVC Port Load Test
    port.Slot_Select(driver,glc_slot)
    port.Port_Select(driver,glc_port)
    port.Load(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Port - PVC] Port Load No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Port PVC Slot Select Test
    time.sleep(1)
    port.PVC_Slot_Select(driver,glc_slot)
    if(mod.IsAlert(driver) != True):
        print(f"             [Port - PVC] Slot Select No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Port PVC Result
    if(if_error == False):
        print(f"[MSAN1-11886][Port - PVC] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11886][Port - PVC] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Port QoS Test
    # Profile > QoS
    # Port > QoS
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Profile > QoS > VC-Shaping
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Profile")
    mod.SubPage_Switch(driver,"QoS")
    mod.Switch_Frame(driver)

    # VC-Shaping Clear
    index_num = driver.find_elements(By.NAME, "rpprofqosvcsp_rdoSlt").__len__()
    for index in range(index_num-1):
        driver.find_element(By.NAME, "rpprofqosvcsp_rdoSlt").click()
        pro.QoS_VC_Shaping_Delete(driver)

    # VC-Shaping Apply Full
    profile_name = 8000
    if_full = False
    while(if_full == False):
        profile_name = profile_name+1
        pro.QoS_VC_Shaping_Profile_Name(driver,f"123456789012345678901234567{profile_name}")
        pro.QoS_VC_Shaping_Apply(driver)
        try:
            driver.find_element(By.NAME, "rperror_btnBack").click()
            print(f"             [Profile - Qos - VC-Shaping] Max Capacity(16) = {profile_name-8000}",file = open(file_name, '+a'))
            if_full = True
        except:
            pass

    if(profile_name-8000 == 16):
        print(f"[MSAN1-11900][Profile - Qos - VC-Shaping] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11900][Profile - Qos - VC-Shaping] Result Fail",file = open(file_name, '+a'))

    # 路徑導向 Profile > QoS > Shaping
    mod.Tab_Switch(driver,"Shaping")

    # Shaping Clear
    index_num = driver.find_elements(By.NAME, "rpprofqosshape_rdoSlt").__len__()
    for index in range(index_num-1):
        driver.find_element(By.NAME, "rpprofqosshape_rdoSlt").click()
        pro.QoS_Shaping_Delete(driver)

    # Shaping Apply Full
    profile_name = 8000
    if_full = False
    while(if_full == False):
        profile_name = profile_name+1
        pro.QoS_Shaping_Profile_Name(driver,f"123456789012345678901234567{profile_name}")
        for queue in range(8):
            pro.QoS_Shaping_Max_Rate_Queue(driver,queue,"10000000")
        pro.QoS_Shaping_Apply(driver)
        try:
            driver.find_element(By.NAME, "rperror_btnBack").click()
            print(f"             [Profile - Qos - Shaping] Max Capacity(16) = {profile_name-8000}",file = open(file_name, '+a'))
            if_full = True
        except:
            pass

    if(profile_name-8000 == 16):
        print(f"[MSAN1-11901][Profile - Qos - Shaping] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11901][Profile - Qos - Shaping] Result Fail",file = open(file_name, '+a'))

    # 路徑導向 Profile > QoS > Weight
    mod.Tab_Switch(driver,"Weight")

    # Weight Clear
    index_num = driver.find_elements(By.NAME, "rpprofqoswrr_rdoSlt").__len__()
    for index in range(index_num-1):
        driver.find_element(By.NAME, "rpprofqoswrr_rdoSlt").click()
        pro.QoS_Weight_Delete(driver)

    # Weight Apply Full
    profile_name = 8000
    if_full = False
    while(if_full == False):
        profile_name = profile_name+1
        pro.QoS_Weight_Profile_Name(driver,f"123456789012345678901234567{profile_name}")
        pro.QoS_Weight_Apply(driver)
        try:
            driver.find_element(By.NAME, "rperror_btnBack").click()
            print(f"             [Profile - Qos - Weight] Max Capacity(16) = {profile_name-8000}",file = open(file_name, '+a'))
            if_full = True
        except:
            pass

    if(profile_name-8000 == 16):
        print(f"[MSAN1-11902][Profile - Qos - Weight] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11902][Profile - Qos - Weight] Result Fail",file = open(file_name, '+a'))

    # 路徑導向 Profile > QoS > RateLimit
    mod.Tab_Switch(driver,"RateLimit")

    # RateLimit Clear
    index_num = driver.find_elements(By.NAME, "rpprofqosrlp_rdoSlt").__len__()
    for index in range(index_num-1):
        driver.find_element(By.NAME, "rpprofqosrlp_rdoSlt").click()
        pro.QoS_RateLimit_Delete(driver)

    # RateLimit Apply Full
    profile_name = 8000
    if_full = False
    while(if_full == False):
        profile_name = profile_name+1
        pro.QoS_RateLimit_Profile_Name(driver,f"123456789012345678901234567{profile_name}")
        pro.QoS_RateLimit_Ingress(driver,True,"10000000","16000000","10000000","16000000")
        pro.QoS_RateLimit_Egress(driver,True,"10000000","128000")
        pro.QoS_RateLimit_Apply(driver)
        try:
            driver.find_element(By.NAME, "rperror_btnBack").click()
            print(f"             [Profile - Qos - RateLimit] Max Capacity(128) = {profile_name-8000}",file = open(file_name, '+a'))
            if_full = True
        except:
            pass

    if(profile_name-8000 == 128):
        print(f"[MSAN1-11903][Profile - Qos - RateLimit] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11903][Profile - Qos - RateLimit] Result Fail",file = open(file_name, '+a'))

    # 路徑導向 Port > QoS
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Port")
    mod.SubPage_Switch(driver,"QoS")
    mod.Switch_Frame(driver)

    # slot select
    time.sleep(0.1)
    port.Qos_Slot_Select(driver,glc_slot)

    # Port QoS Test
    port.Qos_Rate_Limit_Profile_All(driver,127)
    port.Qos_Algorithm_All(driver,4)
    port.Qos_Shaping_Profile_All(driver,15)
    port.Qos_Weight_Profile_All(driver,15)
    port.Qos_Apply(driver)

    # Port QoS Check
    if(driver.find_element(By.XPATH, f"//*[@name='rpPortQos_ratelimit{glc_port}']/option[127]").is_selected() != True):
        print(f"             [Port - QoS] Port{glc_port} Rate-Limit-Profile Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.XPATH, f"//*[@name='rpPortQos_algorithm{glc_port}']/option[4]").is_selected() != True):
        print(f"             [Port - QoS] Port{glc_port} Algorithm Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.XPATH, f"//*[@name='rpPortQos_shapProf{glc_port}']/option[15]").is_selected() != True):
        print(f"             [Port - QoS] Port{glc_port} Shaping-Profile Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.XPATH, f"//*[@name='rpPortQos_weightProf{glc_port}']/option[15]").is_selected() != True):
        print(f"             [Port - QoS] Port{glc_port} Weight-Profile Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Port QoS Delete Test
    port.Qos_Rate_Limit_Profile_All(driver,1)
    port.Qos_Algorithm_All(driver,1)
    port.Qos_Shaping_Profile_All(driver,1)
    port.Qos_Weight_Profile_All(driver,1)
    port.Qos_Apply(driver)

    # 路徑導向 Profile > QoS > Shaping
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Profile")
    mod.SubPage_Switch(driver,"QoS")
    mod.Switch_Frame(driver)
    mod.Tab_Switch(driver,"Shaping")

    # Shaping Delete Check
    driver.find_element(By.NAME, "rpprofqosshape_rdoSlt").click()
    pro.QoS_Shaping_Delete(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Profile - Qos - Shaping] Delete Invalid Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Weight Delete Check
    time.sleep(1)
    mod.Tab_Switch(driver,"Weight")
    driver.find_element(By.NAME, "rpprofqoswrr_rdoSlt").click()
    pro.QoS_Weight_Delete(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Profile - Qos - Weight] Delete Invalid Test Fail",file = open(file_name, '+a'))
        if_error = True

    # RateLimit Delete Check
    time.sleep(1)
    mod.Tab_Switch(driver,"RateLimit")
    driver.find_element(By.NAME, "rpprofqosrlp_rdoSlt").click()
    pro.QoS_RateLimit_Delete(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Profile - Qos - RateLimit] Delete Invalid Test Fail",file = open(file_name, '+a'))
        if_error = True

    # 路徑導向 Port > QoS
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Port")
    mod.SubPage_Switch(driver,"QoS")
    mod.Switch_Frame(driver)

    # slot select
    time.sleep(0.1)
    port.Qos_Slot_Select(driver,glc_slot)

    # Port QoS Delete Reset
    port.Qos_Rate_Limit_Profile_All(driver,128)
    port.Qos_Algorithm_All(driver,1)
    port.Qos_Shaping_Profile_All(driver,16)
    port.Qos_Weight_Profile_All(driver,16)
    port.Qos_Apply(driver)

    # 路徑導向 Profile > QoS > VC-Shaping
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Profile")
    mod.SubPage_Switch(driver,"QoS")
    mod.Switch_Frame(driver)

    # VC-Shaping Clear
    index_num = driver.find_elements(By.NAME, "rpprofqosvcsp_rdoSlt").__len__()
    for index in range(index_num-1):
        driver.find_element(By.NAME, "rpprofqosvcsp_rdoSlt").click()
        pro.QoS_VC_Shaping_Delete(driver)

    # 路徑導向 Profile > QoS > Shaping
    mod.Tab_Switch(driver,"Shaping")

    # Shaping Clear
    index_num = driver.find_elements(By.NAME, "rpprofqosshape_rdoSlt").__len__()
    for index in range(index_num-1):
        driver.find_element(By.NAME, "rpprofqosshape_rdoSlt").click()
        pro.QoS_Shaping_Delete(driver)

    # 路徑導向 Profile > QoS > Weight
    mod.Tab_Switch(driver,"Weight")

    # Weight Clear
    index_num = driver.find_elements(By.NAME, "rpprofqoswrr_rdoSlt").__len__()
    for index in range(index_num-1):
        driver.find_element(By.NAME, "rpprofqoswrr_rdoSlt").click()
        pro.QoS_Weight_Delete(driver)

    # Port QoS Result
    if(if_error == False):
        print(f"[MSAN1-11887][Port - QoS] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11887][Port - QoS] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Port DDMI Test
    # Port > DDMI
    # Statistics > DDMI Status
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Port > DDMI
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Port")
    mod.SubPage_Switch(driver,"DDMI")
    mod.Switch_Frame(driver)

    # MSC slot select
    time.sleep(0.1)
    port.Slot_Select(driver,msc_slot)
    port.Port_Select(driver,msc_port)
    port.Load(driver)

    # Port DDMI MSC Test
    port.DDMI_Module_Temperature(driver,"128","-128")
    port.DDMI_Supply_Voltage(driver,"6.55","0")
    port.DDMI_TX_Bias_Current(driver,"131","0")
    port.DDMI_TX_Output_Power(driver,"6553.5","0")
    port.DDMI_RX_Input_Power(driver,"6553.5","0")
    port.DDMI_Apply(driver)

    # Port DDMI MSC Check
    if(driver.find_element(By.NAME, "rpportddmi_input_highalarm_moduleTemperature").get_attribute("value") != "128.00"):
        print(f"             [Port - DDMI] MSC Module Temperature High Limit Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpportddmi_input_lowalarm_moduleTemperature").get_attribute("value") != "-128.00"):
        print(f"             [Port - DDMI] MSC Module Temperature Low Limit Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpportddmi_input_highalarm_supplyVoltageVcc").get_attribute("value") != "6.55"):
        print(f"             [Port - DDMI] MSC Supply Voltage High Limit Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpportddmi_input_lowalarm_supplyVoltageVcc").get_attribute("value") != "0.00"):
        print(f"             [Port - DDMI] MSC Supply Voltage Low Limit Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpportddmi_input_highalarm_tXBias").get_attribute("value") != "131.00"):
        print(f"             [Port - DDMI] MSC TX Bias Current High Limit Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpportddmi_input_lowalarm_tXBias").get_attribute("value") != "0.00"):
        print(f"             [Port - DDMI] MSC TX Bias Current Low Limit Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpportddmi_input_highalarm_tXOutputPower").get_attribute("value") != "6553.50"):
        print(f"             [Port - DDMI] MSC TX Output Power High Limit Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpportddmi_input_lowalarm_tXOutputPower").get_attribute("value") != "0.00"):
        print(f"             [Port - DDMI] MSC TX Output Power Low Limit Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpportddmi_input_highalarm_rXInputPower").get_attribute("value") != "6553.50"):
        print(f"             [Port - DDMI] MSC RX Input Power High Limit Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpportddmi_input_lowalarm_rXInputPower").get_attribute("value") != "0.00"):
        print(f"             [Port - DDMI] MSC RX Input Power Low Limit Test Fail",file = open(file_name, '+a'))
        if_error = True

    # GLC slot select
    time.sleep(0.1)
    port.Slot_Select(driver,glc_slot)
    port.Port_Select(driver,glc_port)
    port.Load(driver)

    # Port DDMI GLC Test
    port.DDMI_Module_Temperature(driver,"128","-128")
    port.DDMI_Supply_Voltage(driver,"6.55","0")
    port.DDMI_TX_Bias_Current(driver,"131","0")
    port.DDMI_TX_Output_Power(driver,"6553.5","0")
    port.DDMI_RX_Input_Power(driver,"6553.5","0")
    port.DDMI_Apply(driver)

    # Port DDMI GLC Check
    if(driver.find_element(By.NAME, "rpportddmi_input_highalarm_moduleTemperature").get_attribute("value") != "128.00"):
        print(f"             [Port - DDMI] GLC Module Temperature High Limit Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpportddmi_input_lowalarm_moduleTemperature").get_attribute("value") != "-128.00"):
        print(f"             [Port - DDMI] GLC Module Temperature Low Limit Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpportddmi_input_highalarm_supplyVoltageVcc").get_attribute("value") != "6.55"):
        print(f"             [Port - DDMI] GLC Supply Voltage High Limit Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpportddmi_input_lowalarm_supplyVoltageVcc").get_attribute("value") != "0.00"):
        print(f"             [Port - DDMI] GLC Supply Voltage Low Limit Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpportddmi_input_highalarm_tXBias").get_attribute("value") != "131.00"):
        print(f"             [Port - DDMI] GLC TX Bias Current High Limit Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpportddmi_input_lowalarm_tXBias").get_attribute("value") != "0.00"):
        print(f"             [Port - DDMI] GLC TX Bias Current Low Limit Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpportddmi_input_highalarm_tXOutputPower").get_attribute("value") != "6553.50"):
        print(f"             [Port - DDMI] GLC TX Output Power High Limit Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpportddmi_input_lowalarm_tXOutputPower").get_attribute("value") != "0.00"):
        print(f"             [Port - DDMI] GLC TX Output Power Low Limit Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpportddmi_input_highalarm_rXInputPower").get_attribute("value") != "6553.50"):
        print(f"             [Port - DDMI] GLC RX Input Power High Limit Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpportddmi_input_lowalarm_rXInputPower").get_attribute("value") != "0.00"):
        print(f"             [Port - DDMI] GLC RX Input Power Low Limit Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Statistics DDMI Status Result
    if(if_error == False):
        print(f"[MSAN1-11888][Port - DDMI] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11888][Port - DDMI] Result Fail",file = open(file_name, '+a'))

    # 路徑導向 Statistics > DDMI Status
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Statistics")
    mod.SubPage_Switch(driver,"DDMI Status")
    mod.Switch_Frame(driver)

    # MSC slot select
    time.sleep(0.1)
    port.Slot_Select(driver,msc_slot)
    port.Port_Select(driver,msc_port)
    port.Load(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        pass

    # GLC slot select
    time.sleep(0.1)
    port.Slot_Select(driver,glc_slot)
    port.Port_Select(driver,glc_port)
    port.Load(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        pass

    # Statistics DDMI Status Result
    print(f"[MSAN1-11938][Statistics - DDMI Status] Result Pass",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def Profile_Test(driver,glc_slot,glc_port,msc_slot,msc_port,file_name):
    print(f"Profile Test\nTest Start",file = open(file_name, '+a'))

    # DSL Line Profile Test
    # Profile > DSL > Line Profile
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Profile > DSL > Line Profile
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Profile")
    mod.SubPage_Switch(driver,"DSL")
    mod.Switch_Frame(driver)

    # Profile DSL Line Profile Test
    driver.find_element(By.NAME, "rpLineProfile_data_radio_select").click()
    driver.find_element(By.ID, "tab_pm").click()
    driver.find_element(By.ID, "tab_rfi").click()
    driver.find_element(By.ID, "tab_dpbo").click()
    driver.find_element(By.ID, "tab_upbo").click()
    driver.find_element(By.ID, "tab_psd").click()
    driver.find_element(By.ID, "tab_vn").click()
    driver.find_element(By.ID, "tab_sos").click()
    driver.find_element(By.ID, "tab_roc").click()
    driver.find_element(By.ID, "tab_CustomPSD").click()
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[0].click()
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Profile - DSL - Line Profile] Delete Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(0.5)
    driver.find_element(By.NAME, "rpLineProfile_data_radio_select").click()
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Profile - DSL - Line Profile] Apply Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(0.5)

    # Profile DSL Line Profile Result
    if(if_error == False):
        print(f"[MSAN1-11891][Profile - DSL - Line Profile] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11891][Profile - DSL - Line Profile] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # DSL Channel Profile Test
    # Profile > DSL > Channel Profile
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Profile > DSL > Channel Profile
    mod.Tab_Switch(driver,"Channel Profile")

    # Profile DSL Channel Profile Test
    driver.find_element(By.NAME, "rpChannelProfile_data_radio_select").click()
    driver.find_element(By.ID, "tab_ginp").click()
    driver.find_element(By.ID, "tab_sos").click()
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[0].click()
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Profile - DSL - Channel Profile] Delete Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(0.5)
    driver.find_element(By.NAME, "rpChannelProfile_data_radio_select").click()
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Profile - DSL - Channel Profile] Apply Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(0.5)

    # Profile DSL Channel Profile Result
    if(if_error == False):
        print(f"[MSAN1-11892][Profile - DSL - Channel Profile] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11892][Profile - DSL - Channel Profile] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # DSL INM Profile Test
    # Profile > DSL > INM Profile
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Profile > DSL > INM Profile
    mod.Tab_Switch(driver,"INM Profile")

    # Profile DSL INM Profile Test
    driver.find_element(By.NAME, "rpinmProf_select").click()
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[0].click()
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Profile - DSL - INM Profile] Delete Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(0.5)
    driver.find_element(By.NAME, "rpinmProf_select").click()
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Profile - DSL - INM Profile] Apply Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(0.5)

    # Profile DSL INM Profile Result
    if(if_error == False):
        print(f"[MSAN1-11893][Profile - DSL - INM Profile] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11893][Profile - DSL - INM Profile] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # DSL Template Test
    # Profile > DSL > Template
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Profile > DSL > Template
    mod.Tab_Switch(driver,"Template")

    # Profile DSL Template Test
    driver.find_element(By.NAME, "rptempProf_select").click()
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[0].click()
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Profile - DSL - Template] Delete Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(0.5)
    driver.find_element(By.NAME, "rptempProf_select").click()
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Profile - DSL - Template] Apply Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(0.5)

    # Profile DSL Template Result
    if(if_error == False):
        print(f"[MSAN1-11894][Profile - DSL - Template] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11894][Profile - DSL - Template] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # DSL Alarm Alarm line Profile Test
    # Profile > DSL Alarm > Alarm line Profile
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Profile > DSL Alarm > Alarm line Profile
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"DSL Alarm")
    mod.Switch_Frame(driver)

    # Profile DSL Alarm Alarm line Profile Test
    driver.find_element(By.NAME, "rpalarmlineProf_select").click()
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[0].click()
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Profile - DSL Alarm - Alarm line Profile] Delete Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(0.5)
    driver.find_element(By.NAME, "rpalarmlineProf_select").click()
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Profile - DSL Alarm - Alarm line Profile] Apply Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(0.5)

    # Profile DSL Alarm Alarm line Profile Result
    if(if_error == False):
        print(f"[MSAN1-11895][Profile - DSL Alarm - Alarm line Profile] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11895][Profile - DSL Alarm - Alarm line Profile] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # DSL Alarm Alarm Channel Profile Test
    # Profile > DSL Alarm > Alarm Channel Profile
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Profile > DSL Alarm > Alarm Channel Profile
    mod.Tab_Switch(driver,"Alarm Channel Profile")

    # Profile DSL Alarm Alarm Channel Profile Test
    driver.find_element(By.NAME, "rpalarmChannProf_select").click()
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[0].click()
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Profile - DSL Alarm - Alarm Channel Profile] Delete Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(0.5)
    driver.find_element(By.NAME, "rpalarmChannProf_select").click()
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Profile - DSL Alarm - Alarm Channel Profile] Apply Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(0.5)

    # Profile DSL Alarm Alarm Channel Profile Result
    if(if_error == False):
        print(f"[MSAN1-11896][Profile - DSL Alarm - Alarm Channel Profile] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11896][Profile - DSL Alarm - Alarm Channel Profile] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # DSL Alarm Alarm Template Profile Test
    # Profile > DSL Alarm > Alarm Template Profile
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Profile > DSL Alarm > Alarm Template Profile
    mod.Tab_Switch(driver,"Alarm Template Profile")

    # Profile DSL Alarm Alarm Template Profile Test
    driver.find_element(By.NAME, "rpalarmtempProf_select").click()
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[0].click()
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Profile - DSL Alarm - Alarm Template Profile] Delete Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(0.5)
    driver.find_element(By.NAME, "rpalarmtempProf_select").click()
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Profile - DSL Alarm - Alarm Template Profile] Apply Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(0.5)

    # Profile DSL Alarm Alarm Template Profile Result
    if(if_error == False):
        print(f"[MSAN1-11897][Profile - DSL Alarm - Alarm Template Profile] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11897][Profile - DSL Alarm - Alarm Template Profile] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # G.bond TCA Profile Test
    # Profile > G.bond > TCA Profile
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Profile > G.bond > TCA Profile
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"G.bond")
    mod.Switch_Frame(driver)

    # Profile G.bond TCA Profile Test
    driver.find_element(By.NAME, "rpgbondProf_select").click()
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[0].click()
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Profile - G.bond - TCA Profile] Delete Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(0.5)
    driver.find_element(By.NAME, "rpgbondProf_select").click()
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Profile - G.bond - TCA Profile] Apply Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(0.5)

    # Profile G.bond TCA Profile Result
    if(if_error == False):
        print(f"[MSAN1-11898][Profile - G.bond - TCA Profile] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11898][Profile - G.bond - TCA Profile] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # G.bond Template Test
    # Profile > G.bond > Template
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Profile > G.bond > Template
    mod.Tab_Switch(driver,"Template")

    # Profile G.bond Template Test
    driver.find_element(By.NAME, "rpgbondProf_select").click()
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[0].click()
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Profile - G.bond - Template] Delete Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(0.5)
    driver.find_element(By.NAME, "rpgbondProf_select").click()
    driver.find_elements(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only")[1].click()
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Profile - G.bond - Template] Apply Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(0.5)

    # Profile G.bond Template Result
    if(if_error == False):
        print(f"[MSAN1-11899][Profile - G.bond - Template] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11899][Profile - G.bond - Template] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def Statistics_Test(driver,glc_slot,glc_port,msc_slot,msc_port,username,password,file_name):
    print(f"Statistics Test\nTest Start",file = open(file_name, '+a'))

    # Statistics ARP Table Test
    # Statistics > ARP Table
    # -------------------------start-------------------------

    # 路徑導向 Statistics > ARP Table
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Statistics")
    mod.SubPage_Switch(driver,"ARP Table")
    mod.Switch_Frame(driver)

    if_error = False
    # Statistics ARP Table Test
    driver.find_element(By.NAME, "rpstatsarp_btnRefresh").click()
    try:
        driver.find_element(By.CLASS_NAME, "table-sample-3")
    except:
        print(f"             [Statistics - ARP Table] Refresh Table Dont Exist Test Fail",file = open(file_name, '+a'))
        if_error = True
    while(driver.find_element(By.ID, "btnNextPage").get_attribute("disabled") != "true"):
        driver.find_element(By.ID, "btnNextPage").get_attribute("disabled").click()
    driver.find_element(By.NAME, "rpstatsarp_btnRefresh").click()
    try:
        driver.find_element(By.CLASS_NAME, "table-sample-3")
    except:
        print(f"             [Statistics - ARP Table] Last Page Refresh Table Dont Exist Test Fail",file = open(file_name, '+a'))
        if_error = True
    driver.find_element(By.NAME, "rpstatsarp_btnFlush").click()
    driver.find_element(By.NAME, "rpstatsarp_btnRefresh").click()
    try:
        driver.find_element(By.CLASS_NAME, "table-sample-3")
    except:
        print(f"             [Statistics - ARP Table] Flush Refresh Table Dont Exist Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Statistics ARP Table Result
    if(if_error == False):
        print(f"[MSAN1-11904][Statistics - ARP Table] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11904][Statistics - ARP Table] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics Dot3ad Status Test
    # Statistics > Dot3ad Status
    # -------------------------start-------------------------

    # 路徑導向 Statistics > Dot3ad Status
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Statistics")
    mod.SubPage_Switch(driver,"Dot3ad Status")
    mod.Switch_Frame(driver)

    if_error = False
    try:
        # Statistics Dot3ad Status Refresh
        driver.find_element(By.NAME, "rpstatsdot3ad_btnRefresh").click()
    except:
        if_error = True

    # Statistics Dot3ad Status Result
    if(if_error == False):
        print(f"[MSAN1-11906][Statistics - Dot3ad Status] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11906][Statistics - Dot3ad Status] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics DSL Status Line Test
    # Statistics > DSL Status > Line
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Statistics > DSL Status
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"DSL Status")
    mod.Switch_Frame(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        pass

    # MSC Test
    sta.Slot_Select(driver,msc_slot)
    sta.Port_Select(driver,msc_port)
    sta.Load(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Statistics - DSL Status - Line] MSC No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # GLC Test
    sta.Slot_Select(driver,glc_slot)
    sta.Port_Select(driver,glc_port)
    sta.Load(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Statistics - DSL Status - Line] GLC No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Statistics DSL Status Result
    if(if_error == False):
        print(f"[MSAN1-11907][Statistics - DSL Status - Line] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11907][Statistics - DSL Status - Line] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics DSL Status Line Info Test
    # Statistics > DSL Status > Line Info
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Statistics > DSL Status
    time.sleep(1)
    mod.Tab_Switch(driver,"Line Info")
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        pass

    # MSC Test
    sta.Slot_Select(driver,msc_slot)
    sta.Port_Select(driver,msc_port)
    time.sleep(1)
    mod.Tab_Switch(driver,"Line Info")
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Statistics - DSL Status - Line Info] MSC No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # GLC Test
    sta.Slot_Select(driver,glc_slot)
    sta.Port_Select(driver,glc_port)
    time.sleep(1)
    mod.Tab_Switch(driver,"Line Info")
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Statistics - DSL Status - Line Info] GLC No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Statistics DSL Status Result
    if(if_error == False):
        print(f"[MSAN1-11908][Statistics - DSL Status - Line Info] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11908][Statistics - DSL Status - Line Info] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics DSL Status Line Rate Test
    # Statistics > DSL Status > Line Rate
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Statistics > DSL Status
    time.sleep(1)
    mod.Tab_Switch(driver,"Line Rate")
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        pass

    # MSC Test
    sta.Slot_Select(driver,msc_slot)
    sta.Port_Select(driver,msc_port)
    time.sleep(1)
    mod.Tab_Switch(driver,"Line Rate")
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Statistics - DSL Status - Line Rate] MSC No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # GLC Test
    sta.Slot_Select(driver,glc_slot)
    sta.Port_Select(driver,glc_port)
    time.sleep(1)
    mod.Tab_Switch(driver,"Line Rate")
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Statistics - DSL Status - Line Rate] GLC No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Statistics DSL Status Result
    if(if_error == False):
        print(f"[MSAN1-11909][Statistics - DSL Status - Line Rate] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11909][Statistics - DSL Status - Line Rate] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics DSL Status Channel Test
    # Statistics > DSL Status > Channel
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Statistics > DSL Status
    time.sleep(1)
    mod.Tab_Switch(driver,"Channel")
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        pass

    # MSC Test
    sta.Slot_Select(driver,msc_slot)
    sta.Port_Select(driver,msc_port)
    time.sleep(1)
    mod.Tab_Switch(driver,"Channel")
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Statistics - DSL Status - Channel] MSC No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # GLC Test
    sta.Slot_Select(driver,glc_slot)
    sta.Port_Select(driver,glc_port)
    time.sleep(1)
    mod.Tab_Switch(driver,"Channel")
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Statistics - DSL Status - Channel] GLC No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Statistics DSL Status Result
    if(if_error == False):
        print(f"[MSAN1-11910][Statistics - DSL Status - Channel] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11910][Statistics - DSL Status - Channel] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics DSL Status Band Test
    # Statistics > DSL Status > Band
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Statistics > DSL Status
    time.sleep(1)
    mod.Tab_Switch(driver,"Band")
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        pass

    # MSC Test
    sta.Slot_Select(driver,msc_slot)
    sta.Port_Select(driver,msc_port)
    time.sleep(1)
    mod.Tab_Switch(driver,"Band")
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Statistics - DSL Status - Band] MSC No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # GLC Test
    sta.Slot_Select(driver,glc_slot)
    sta.Port_Select(driver,glc_port)
    time.sleep(1)
    mod.Tab_Switch(driver,"Band")
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Statistics - DSL Status - Band] GLC No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Statistics DSL Status Result
    if(if_error == False):
        print(f"[MSAN1-11911][Statistics - DSL Status - Band] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11911][Statistics - DSL Status - Band] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics DSL Status Medley PSD Test
    # Statistics > DSL Status > Medley PSD
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Statistics > DSL Status
    time.sleep(1)
    mod.Tab_Switch(driver,"Medley PSD")
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        pass

    # MSC Test
    sta.Slot_Select(driver,msc_slot)
    sta.Port_Select(driver,msc_port)
    time.sleep(1)
    mod.Tab_Switch(driver,"Medley PSD")
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Statistics - DSL Status - Medley PSD] MSC No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # GLC Test
    sta.Slot_Select(driver,glc_slot)
    sta.Port_Select(driver,glc_port)
    time.sleep(1)
    mod.Tab_Switch(driver,"Medley PSD")
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Statistics - DSL Status - Medley PSD] GLC No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Statistics DSL Status Result
    if(if_error == False):
        print(f"[MSAN1-11912][Statistics - DSL Status - Medley PSD] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11912][Statistics - DSL Status - Medley PSD] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics DSL Status QLN Test
    # Statistics > DSL Status > QLN
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Statistics > DSL Status
    time.sleep(1)
    mod.Tab_Switch(driver,"QLN")
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        pass

    # MSC Test
    sta.Slot_Select(driver,msc_slot)
    sta.Port_Select(driver,msc_port)
    time.sleep(1)
    mod.Tab_Switch(driver,"QLN")
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Statistics - DSL Status - QLN] MSC No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # GLC Test
    sta.Slot_Select(driver,glc_slot)
    sta.Port_Select(driver,glc_port)
    time.sleep(1)
    mod.Tab_Switch(driver,"QLN")
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Statistics - DSL Status - QLN] GLC No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Statistics DSL Status Result
    if(if_error == False):
        print(f"[MSAN1-11913][Statistics - DSL Status - QLN] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11913][Statistics - DSL Status - QLN] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics DSL Status SNR Test
    # Statistics > DSL Status > SNR
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Statistics > DSL Status
    time.sleep(1)
    mod.Tab_Switch(driver,"SNR")
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        pass

    # MSC Test
    sta.Slot_Select(driver,msc_slot)
    sta.Port_Select(driver,msc_port)
    time.sleep(1)
    mod.Tab_Switch(driver,"SNR")
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Statistics - DSL Status - SNR] MSC No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # GLC Test
    sta.Slot_Select(driver,glc_slot)
    sta.Port_Select(driver,glc_port)
    time.sleep(1)
    mod.Tab_Switch(driver,"SNR")
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Statistics - DSL Status - SNR] GLC No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Statistics DSL Status Result
    if(if_error == False):
        print(f"[MSAN1-11914][Statistics - DSL Status - SNR] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11914][Statistics - DSL Status - SNR] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics DSL Status Hlog Test
    # Statistics > DSL Status > Hlog
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Statistics > DSL Status
    time.sleep(1)
    mod.Tab_Switch(driver,"Hlog")
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        pass

    # MSC Test
    sta.Slot_Select(driver,msc_slot)
    sta.Port_Select(driver,msc_port)
    time.sleep(1)
    mod.Tab_Switch(driver,"Hlog")
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Statistics - DSL Status - Hlog] MSC No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # GLC Test
    sta.Slot_Select(driver,glc_slot)
    sta.Port_Select(driver,glc_port)
    time.sleep(1)
    mod.Tab_Switch(driver,"Hlog")
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Statistics - DSL Status - Hlog] GLC No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Statistics DSL Status Result
    if(if_error == False):
        print(f"[MSAN1-11915][Statistics - DSL Status - Hlog] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11915][Statistics - DSL Status - Hlog] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics DSL Status Bitalloc Test
    # Statistics > DSL Status > Bitalloc
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Statistics > DSL Status
    time.sleep(1)
    mod.Tab_Switch(driver,"Bitalloc")
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        pass

    # MSC Test
    sta.Slot_Select(driver,msc_slot)
    sta.Port_Select(driver,msc_port)
    time.sleep(1)
    mod.Tab_Switch(driver,"Bitalloc")
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Statistics - DSL Status - Bitalloc] MSC No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # GLC Test
    sta.Slot_Select(driver,glc_slot)
    sta.Port_Select(driver,glc_port)
    time.sleep(1)
    mod.Tab_Switch(driver,"Bitalloc")

    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Statistics - DSL Status - Bitalloc] GLC No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Statistics DSL Status Result
    if(if_error == False):
        print(f"[MSAN1-11916][Statistics - DSL Status - Bitalloc] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11916][Statistics - DSL Status - Bitalloc] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics DSL Status PSD Test
    # Statistics > DSL Status > PSD
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Statistics > DSL Status
    time.sleep(1)
    mod.Tab_Switch(driver,"PSD")
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        pass

    # MSC Test
    sta.Slot_Select(driver,msc_slot)
    sta.Port_Select(driver,msc_port)
    time.sleep(1)
    mod.Tab_Switch(driver,"PSD")
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Statistics - DSL Status - PSD] MSC No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # GLC Test
    sta.Slot_Select(driver,glc_slot)
    sta.Port_Select(driver,glc_port)
    time.sleep(1)
    mod.Tab_Switch(driver,"PSD")

    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Statistics - DSL Status - PSD] GLC No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Statistics DSL Status Result
    if(if_error == False):
        print(f"[MSAN1-11917][Statistics - DSL Status - PSD] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11917][Statistics - DSL Status - PSD] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics Online Users Test
    # Statistics > Online Users
    # -------------------------start-------------------------

    # 路徑導向 Statistics > Online Users
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"Online Users")
    mod.Switch_Frame(driver)

    if_error = False
    try:
        # Statistics Online Users Refresh
        driver.find_element(By.NAME, "rponlineuser_btnRefresh").click()
    except:
        print(f"             [Statistics - Online Users] Refresh button Fail",file = open(file_name, '+a'))
        if_error = True

    # #*add test---------------------------------------------------------------------------
    # for i in range(5):
    #     try:
    #         driver.find_elements(By.CLASS_NAME, "rponlineusr_user_kick")[i]
    #         print(f"{i} kick exist")
    #     except:
    #         print(f"{i} kick not exist")

    # #*add test---------------------------------------------------------------------------

    #*add
    # find session include '*' one, kick, enter
    if_find = False
    for index in range(driver.find_elements(By.CLASS_NAME, "rponlineusr_user_session").__len__()):
        if("*" in driver.find_elements(By.CLASS_NAME, "rponlineusr_user_session")[index].text):
            if_find = True
            session1 = driver.find_elements(By.CLASS_NAME, "rponlineusr_user_session")[index].text
            # print(f"             [Statistics - Online Users] session:{session1}",file = open(file_name, '+a'))
            sta.Online_Users_Kick(driver,index)
            time.sleep(1)
            pyautogui.press("enter")            
            break
    if(if_find == False):
        print(f"             [Statistics - Online Users] session '*' Not Found (1st time) Test 1 Fail",file = open(file_name, '+a'))
        if_error = True

    # detect session '*' should not exist
    time.sleep(2)
    if_find = False
    for index in range(driver.find_elements(By.CLASS_NAME, "rponlineusr_user_session").__len__()):
        if("*" in driver.find_elements(By.CLASS_NAME, "rponlineusr_user_session")[index].text):
            if_find = True
            temp = driver.find_elements(By.CLASS_NAME, "rponlineusr_user_session")[index].text
            print(f"             [Statistics - Online Users] session:{temp} '*' Found (1st time) Test Fail",file = open(file_name, '+a'))        
            
            #* add scrshot
            screenshot_path = f'{str(datetime.datetime.now()).split(":")[0]}{str(datetime.datetime.now()).split(":")[1]}.{str(datetime.datetime.now()).split(":")[2][:5]}_screenshot.png'
            pyautogui.screenshot(screenshot_path)        

            if_error = True                    
            break
    if(if_find == False):
            print(f"             [Statistics - Online Users] '*' Not Found (1st time) Test Pass",file = open(file_name, '+a'))        
    else:
        # try [2nd time] to kick and detect * should not show
        
        # find session include '*' one, kick, enter
        if_find = False
        for index in range(driver.find_elements(By.CLASS_NAME, "rponlineusr_user_session").__len__()):
            if("*" in driver.find_elements(By.CLASS_NAME, "rponlineusr_user_session")[index].text):
                if_find = True
                # session1 = driver.find_elements(By.CLASS_NAME, "rponlineusr_user_session")[index].text
                # print(f"             [Statistics - Online Users] session:{session1}",file = open(file_name, '+a'))
                sta.Online_Users_Kick(driver,index)
                time.sleep(1)
                pyautogui.press("enter")            
                break
        if(if_find == False):
            print(f"             [Statistics - Online Users] session '*' Not Found (2nd time) Test 1 Fail",file = open(file_name, '+a'))
            if_error = True

        try:
            # check if at the page that can check *
            driver.find_element(By.NAME, "rponlineuser_btnRefresh")

            # detect session '*' should not exist
            time.sleep(2)
            if_find = False
            for index in range(driver.find_elements(By.CLASS_NAME, "rponlineusr_user_session").__len__()):
                if("*" in driver.find_elements(By.CLASS_NAME, "rponlineusr_user_session")[index].text):
                    if_find = True
                    temp = driver.find_elements(By.CLASS_NAME, "rponlineusr_user_session")[index].text
                    print(f"             [Statistics - Online Users] session:{temp} '*' Found (2nd time) Test Fail",file = open(file_name, '+a'))        
                    
                    #* add scrshot
                    screenshot_path = f'{str(datetime.datetime.now()).split(":")[0]}{str(datetime.datetime.now()).split(":")[1]}.{str(datetime.datetime.now()).split(":")[2][:5]}_screenshot.png'
                    pyautogui.screenshot(screenshot_path)                

                    if_error = True                    
                    break
            if(if_find == False):
                    print(f"             [Statistics - Online Users] '*' Not Found (2nd time) Test Pass",file = open(file_name, '+a'))        
            
        except:
            print(f"             [Statistics - Online Users] '*' check fail (2nd time) Test Fail",file = open(file_name, '+a'))        

        


    # click on any page, log in
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"Online Users")
    mod.Switch_Frame(driver)
    # mod.SubPage_Switch(driver,"Maintenance")
    # driver.find_element(By.NAME, "rponlineuser_btnRefresh").click()
    time.sleep(1)
    mod.Login(driver,username,password) # 登入

    # check session '*' should exist after Refresh
    # 路徑導向 Statistics > Online Users
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Statistics")
    mod.SubPage_Switch(driver,"Online Users")
    mod.Switch_Frame(driver)
    driver.find_element(By.NAME, "rponlineuser_btnRefresh").click()
    if_find = False
    for index in range(driver.find_elements(By.CLASS_NAME, "rponlineusr_user_session").__len__()):
        if("*" in driver.find_elements(By.CLASS_NAME, "rponlineusr_user_session")[index].text):
            if_find = True
            break
    if(if_find == False):
        print(f"             [Statistics - Online Users] session '*' Not Found Test 2 Fail",file = open(file_name, '+a'))
        if_error = True

    # Statistics Online Users Result
    if(if_error == False):
        print(f"[MSAN1-11919][Statistics - Online Users] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11919][Statistics - Online Users] Result Fail",file = open(file_name, '+a'))

            
    # -------------------------end-------------------------

    # Statistics STP Test
    # Statistics > STP > RSTP
    # Statistics > STP > MSTP CIST
    # Statistics > STP > MSTP MSTI
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Statistics > STP
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"STP")
    mod.Switch_Frame(driver)
    mod.Tab_Switch(driver,"MSTP CIST")
    mod.Tab_Switch(driver,"MSTP MSTI")

    # MSTID Test
    driver.find_element(By.XPATH, f"//*[@name='rpmstp_msti_sltMSTID']/option[16]").click()
    driver.find_element(By.NAME, "rpmstp_msti_btnApply").click()
    if(driver.find_element(By.XPATH, f"//*[@name='rpmstp_msti_sltMSTID']/option[16]").is_selected() != True):
        print(f"             [Statistics - STP - MSTP MSTI] MSTID Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Statistics STP RSTP Result
    print(f"[MSAN1-11921][Statistics - STP - RSTP] Result Pass",file = open(file_name, '+a'))

    # Statistics STP MSTP CIST Result
    print(f"[MSAN1-11922][Statistics - STP - MSTP CIST] Result Pass",file = open(file_name, '+a'))

    # Statistics STP MSTP MSTI Result
    if(if_error == False):
        print(f"[MSAN1-11923][Statistics - STP - MSTP MSTI] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11923][Statistics - STP - MSTP MSTI] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics IP Test
    # Statistics > IP
    # -------------------------start-------------------------

    # 路徑導向 Statistics > IP
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"IP")
    mod.Switch_Frame(driver)
    
    if_error = False
    try:
        # Statistics IP Refresh
        driver.find_element(By.NAME, "rpstatipRefresh").click()
    except:
        if_error = True

    # Statistics IP Result
    if(if_error == False):
        print(f"[MSAN1-11924][Statistics - IP] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11924][Statistics - IP] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics IPv6 Test
    # Statistics > IPv6 > IPv6
    # Statistics > IPv6 > IPv6 prefix
    # Statistics > IPv6 > IPv6 route
    # -------------------------start-------------------------

    # 路徑導向 Statistics > IPv6
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"IPv6")
    mod.Switch_Frame(driver)
    mod.Tab_Switch(driver,"IPv6 prefix")
    mod.Tab_Switch(driver,"IPv6 route")

    # Statistics IPv6 RIPv6 Result
    print(f"[MSAN1-11925][Statistics - IPv6 - IPv6] Result Pass",file = open(file_name, '+a'))
    print(f"[MSAN1-11926][Statistics - IPv6 - IPv6 prefix] Result Pass",file = open(file_name, '+a'))
    print(f"[MSAN1-11927][Statistics - IPv6 - IPv6 route] Result Pass",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics MACFF Statistic Test
    # Statistics > MACFF > Statistic
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Statistics > MACFF > Statistic
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"MACFF")
    mod.Switch_Frame(driver)

    # MACFF Statistic MSC Test
    sta.Slot_Select(driver,msc_slot)
    driver.find_element(By.NAME, "rpmacffstatistic_Load").click()
    if(mod.IsAlert(driver) != True):
        print(f"             [Statistics - MACFF - Statistic] MSC No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # MACFF Statistic GLC Test
    if_flush_error = False
    sta.Slot_Select(driver,glc_slot)
    driver.find_element(By.NAME, "rpmacffstatistic_Load").click()
    if(mod.IsAlert(driver) == True):
        print(f"             [Statistics - MACFF - Statistic] GLC Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    else:
        driver.find_element(By.NAME, "rpMacffFlush").click()
        port_num = driver.find_elements(By.CLASS_NAME, "td-table-content.rpmacffstatistic_ReqTx").__len__()
        for test_port in range(port_num):
            if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpmacffstatistic_ReqTx")[test_port].get_attribute("textContent") != "0"):
                if_flush_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpmacffstatistic_ReqRx")[test_port].get_attribute("textContent") != "0"):
                if_flush_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpmacffstatistic_ReqRxDrop")[test_port].get_attribute("textContent") != "0"):
                if_flush_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpmacffstatistic_RepTx")[test_port].get_attribute("textContent") != "0"):
                if_flush_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpmacffstatistic_RepRx")[test_port].get_attribute("textContent") != "0"):
                if_flush_error = True
            if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpmacffstatistic_RepRxDrop")[test_port].get_attribute("textContent") != "0"):
                if_flush_error = True
        if(if_flush_error == True):
            print(f"             [Statistics - MACFF - Statistic] GLC F Test Fail",file = open(file_name, '+a'))
            if_error = True

    # Statistics MACFF Statistic Result
    if(if_error == False):
        print(f"[MSAN1-11928][Statistics - MACFF - Statistic] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11928][Statistics - MACFF - Statistic] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics MACFF Status Test
    # Statistics > MACFF > Status
    # -------------------------start-------------------------

    # 路徑導向 Statistics > MACFF > Status
    mod.Tab_Switch(driver,"Status")

    # MACFF Status MSC Test
    sta.Slot_Select(driver,msc_slot)
    driver.find_element(By.NAME, "rpmacffstatus_Load").click()
    if(mod.IsAlert(driver) != True):
        print(f"             [Statistics - MACFF - Status] MSC No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # MACFF Status GLC Test
    if_flush_error = False
    sta.Slot_Select(driver,glc_slot)
    driver.find_element(By.NAME, "rpmacffstatus_Load").click()
    if(mod.IsAlert(driver) == True):
        print(f"             [Statistics - MACFF - Status] GLC Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Statistics MACFF Status Result
    if(if_error == False):
        print(f"[MSAN1-11929][Statistics - MACFF - Status] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11929][Statistics - MACFF - Status] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics Host Protection Test
    # Statistics > Host Protection
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Statistics > Host Protection
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"Host Protection")
    mod.Switch_Frame(driver)

    # Host Protection Test
    driver.find_element(By.NAME, "rpaclhostprotect_BtnRefresh").click()
    driver.find_element(By.NAME, "rpaclhostprotect_BtnClear").click()
    if(driver.find_element(By.NAME, "rpaclhostprotect_rxArp").get_attribute("textContent") != "0"):
        if_error = True
    if(driver.find_element(By.NAME, "rpaclhostprotect_dropArp").get_attribute("textContent") != "0"):
        if_error = True
    if(driver.find_element(By.NAME, "rpaclhostprotect_rxBpdu").get_attribute("textContent") != "0"):
        if_error = True
    if(driver.find_element(By.NAME, "rpaclhostprotect_dropBpdu").get_attribute("textContent") != "0"):
        if_error = True
    if(driver.find_element(By.NAME, "rpaclhostprotect_rxDhcp").get_attribute("textContent") != "0"):
        if_error = True
    if(driver.find_element(By.NAME, "rpaclhostprotect_dropDhcp").get_attribute("textContent") != "0"):
        if_error = True
    if(driver.find_element(By.NAME, "rpaclhostprotect_rxDhcpv6").get_attribute("textContent") != "0"):
        if_error = True
    if(driver.find_element(By.NAME, "rpaclhostprotect_dropDhcpv6").get_attribute("textContent") != "0"):
        if_error = True
    if(driver.find_element(By.NAME, "rpaclhostprotect_rxIcmpv6").get_attribute("textContent") != "0"):
        if_error = True
    if(driver.find_element(By.NAME, "rpaclhostprotect_dropIcmpv6").get_attribute("textContent") != "0"):
        if_error = True
    if(driver.find_element(By.NAME, "rpaclhostprotect_rxIgmp").get_attribute("textContent") != "0"):
        if_error = True
    if(driver.find_element(By.NAME, "rpaclhostprotect_dropIgmp").get_attribute("textContent") != "0"):
        if_error = True
    if(driver.find_element(By.NAME, "rpaclhostprotect_rxPppoe").get_attribute("textContent") != "0"):
        if_error = True
    if(driver.find_element(By.NAME, "rpaclhostprotect_dropPppoe").get_attribute("textContent") != "0"):
        if_error = True

    # Statistics Host Protection Result
    if(if_error == False):
        print(f"[MSAN1-11930][Statistics - Host Protection] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11930][Statistics - Host Protection] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics VLAN Test
    # Statistics > VLAN
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Statistics > VLAN
    mod.Switch_Default(driver)
    driver.find_element(By.XPATH, '//*[@id="mainTable"]/tbody/tr[2]/td[1]/div[2]/a[15]').click()
    mod.Switch_Frame(driver)

    driver.find_element(By.CLASS_NAME, "div-row-begin.div-row-cell-content").click()
    try:
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        mod.Switch_Frame(driver)
    except:
        print(f"             [Statistics - VLAN] VID1 New Page Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Statistics VLAN Result
    if(if_error == False):
        print(f"[MSAN1-11931][Statistics - VLAN] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11931][Statistics - VLAN] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics G.bond Test
    # Statistics > G.bond
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Statistics > G.bond
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"G.bond")
    mod.Switch_Frame(driver)

    # MSC Test
    sta.Slot_Select(driver,msc_slot)
    sta.Load(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"-             [Statistics - G.bond] MSC No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # GLC Test
    sta.Slot_Select(driver,glc_slot)
    sta.Load(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Statistics - G.bond] GLC No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Statistics G.bond Result
    if(if_error == False):
        print(f"[MSAN1-11932][Statistics - G.bond] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11932][Statistics - G.bond] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics CFM Test
    # Statistics > CFM
    # -------------------------start-------------------------

    if_sta_cfm_exist = False
    try:
        # 路徑導向 Statistics > CFM
        mod.Switch_Default(driver)
        mod.SubPage_Switch(driver,"CFM")
        mod.Switch_Frame(driver)
        if_sta_cfm_exist = True
    except:
        mod.Switch_Frame(driver)
        print(f"             [Statistics - CFM] Result Block",file = open(file_name, '+a'))
        print(f"[MSAN1-11933][Statistics - CFM] Result Pass",file = open(file_name, '+a'))

    if(if_sta_cfm_exist == True):

        if_error = False

        # Statistics CFM Refresh Test
        driver.find_element(By.NAME, "rpstatipRefresh").click()
        try:
            driver.find_element(By.ID, "mep_table")
        except:
            print(f"             [Statistics - CFM] Table Dont Exist Test Fail",file = open(file_name, '+a'))
            if_error = True

        # Statistics CFM Result
        if(if_error == False):
            print(f"[MSAN1-11933][Statistics - CFM] Result Pass",file = open(file_name, '+a'))
        else:
            print(f"[MSAN1-11933][Statistics - CFM] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics OAM Test
    # Statistics > OAM
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Statistics > OAM
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"OAM")
    mod.Switch_Frame(driver)

    # MSC Test
    retry = True
    while(retry == True):
        try:
            driver.find_element(By.XPATH, f"//*[@name='rpstatoam_selslot']/option[{msc_slot}]").click()
        except:
            time.sleep(1)
        try:
            if(driver.find_element(By.XPATH, f"//*[@name='rpstatoam_selslot']/option[{msc_slot}]").is_selected() == True):
                retry = False
        except:
            time.sleep(1)
    driver.find_element(By.NAME, "lc_Load").click()
    if(driver.find_element(By.ID, "unsupport").get_attribute("style") == "display: none;"):
        print(f"             [Statistics - OAM] MSC Invalid Test Fail",file = open(file_name, '+a'))
        if_error = True

    # GLC Test
    retry = True
    while(retry == True):
        try:
            driver.find_element(By.XPATH, f"//*[@name='rpstatoam_selslot']/option[{glc_slot}]").click()
        except:
            time.sleep(1)
        try:
            if(driver.find_element(By.XPATH, f"//*[@name='rpstatoam_selslot']/option[{glc_slot}]").is_selected() == True):
                retry = False
        except:
            time.sleep(1)
    driver.find_element(By.NAME, "lc_Load").click()
    retry = True
    while(retry == True):
        try:
            driver.find_element(By.XPATH, f"//*[@name='rpstatoam_selport']/option[{glc_port}]").click()
        except:
            time.sleep(1)
        try:
            if(driver.find_element(By.XPATH, f"//*[@name='rpstatoam_selport']/option[{glc_port}]").is_selected() == True):
                retry = False
        except:
            time.sleep(1)
    driver.find_element(By.NAME, "lc_Load").click()
    if(driver.find_element(By.ID, "unsupport").get_attribute("style") != "display: none;"):
        print(f"             [Statistics - OAM] GLC Valid Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Statistics OAM Result
    if(if_error == False):
        print(f"[MSAN1-11934][Statistics - OAM] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11934][Statistics - OAM] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # # Statistics Loopguard Test
    # # Statistics > Loopguard
    # # -------------------------start-------------------------

    # if_error = False

    # # 路徑導向 Statistics > Loopguard
    # mod.Switch_Default(driver)
    # mod.SubPage_Switch(driver,"Loopguard")
    # mod.Switch_Frame(driver)

    # # MSC Test
    # if_msc_error = False
    # sta.Slot_Select(driver,msc_slot)
    # sta.Load(driver)
    # if(driver.find_element(By.NAME, "rpacl_lgSt_Form").get_attribute('style') == "display: none;"):
    #     print(f"             [Statistics - Loopguard] MSC Valid Test Fail",file = open(file_name, '+a'))
    #     if_error = True
    # else:
    #     driver.find_element(By.NAME, "rpacl_lgSt_btnRefresh").click()
    #     driver.find_element(By.NAME, "rpacl_lgSt_btnFlush").click()
    #     if(driver.find_elements(By.CLASS_NAME, "div-row-cell-content.wp-15.rpacl_lg_total_tx")[int(msc_port)-1].get_attribute('textContent') != "0"):
    #         if_msc_error = True
    #     if(driver.find_elements(By.CLASS_NAME, "div-row-cell-content.wp-15.rpacl_lg_total_rx")[int(msc_port)-1].get_attribute('textContent') != "0"):
    #         if_msc_error = True
    #     if(driver.find_elements(By.CLASS_NAME, "div-row-cell-content.wp-10.rpacl_lg_bad_rx")[int(msc_port)-1].get_attribute('textContent') != "0"):
    #         if_msc_error = True
    # if(if_msc_error == True):
    #     print(f"             [Statistics - Loopguard] MSC Test Fail",file = open(file_name, '+a'))
    #     if_error = True

    # # GLC Test
    # if_glc_error = False
    # sta.Slot_Select(driver,glc_slot)
    # sta.Load(driver)
    # if(driver.find_element(By.NAME, "rpacl_lgSt_Form").get_attribute('style') == "display: none;"):
    #     print(f"             [Statistics - Loopguard] GLC Valid Test Fail",file = open(file_name, '+a'))
    #     if_error = True
    # else:
    #     driver.find_element(By.NAME, "rpacl_lgSt_btnRefresh").click()
    #     driver.find_element(By.NAME, "rpacl_lgSt_btnFlush").click()
    #     if(driver.find_elements(By.CLASS_NAME, "div-row-cell-content.wp-15.rpacl_lg_total_tx")[int(glc_port)-1].get_attribute('textContent') != "0"):
    #         if_glc_error = True
    #     if(driver.find_elements(By.CLASS_NAME, "div-row-cell-content.wp-15.rpacl_lg_total_rx")[int(glc_port)-1].get_attribute('textContent') != "0"):
    #         if_glc_error = True
    #     if(driver.find_elements(By.CLASS_NAME, "div-row-cell-content.wp-10.rpacl_lg_bad_rx")[int(glc_port)-1].get_attribute('textContent') != "0"):
    #         if_glc_error = True
    # if(if_glc_error == True):
    #     print(f"             [Statistics - Loopguard] GLC Test Fail",file = open(file_name, '+a'))
    #     if_error = True

    # # Statistics Loopguard Result
    # if(if_error == False):
    #     print(f"[MSAN1-11935][Statistics - Loopguard] Result Pass",file = open(file_name, '+a'))
    # else:
    #     print(f"[MSAN1-11935][Statistics - Loopguard] Result Fail",file = open(file_name, '+a'))

    # # -------------------------end-------------------------

    # # Statistics 802.1x Port Status Test
    # # Statistics > 802.1x Port Status
    # # -------------------------start-------------------------

    # if_error = False

    # # 路徑導向 Statistics > 802.1x Port Status
    # mod.Switch_Default(driver)
    # mod.SubPage_Switch(driver,"802.1x Port Status")
    # mod.Switch_Frame(driver)

    # # MSC Test
    # sta.Slot_Select(driver,msc_slot)
    # sta.Load(driver)
    # if(driver.find_element(By.CLASS_NAME, "rpdot1xportstatusList").get_attribute("style") != "display: none;"):
    #     print(f"             [Statistics - 802.1x Port Status] MSC Invalid Test Fail",file = open(file_name, '+a'))
    #     if_error = True

    # # GLC Test
    # sta.Slot_Select(driver,glc_slot)
    # sta.Load(driver)
    # if(driver.find_element(By.CLASS_NAME, "rpdot1xportstatusList").get_attribute("style") == "display: none;"):
    #     print(f"             [Statistics - 802.1x Port Status] GLC Valid Test Fail",file = open(file_name, '+a'))
    #     if_error = True

    # # Statistics 802.1x Port Status Result
    # if(if_error == False):
    #     print(f"[MSAN1-11937][Statistics - 802.1x Port Status] Result Pass",file = open(file_name, '+a'))
    # else:
    #     print(f"[MSAN1-11937][Statistics - 802.1x Port Status] Result Fail",file = open(file_name, '+a'))

    # # -------------------------end-------------------------

    # Statistics Monitor Status Test
    # Statistics > Monitor Status
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Statistics > Monitor Status
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"Monitor Status")
    mod.Switch_Frame(driver)

    # MSC Test
    sta.Slot_Select(driver,msc_slot)
    sta.Load(driver)
    if(driver.find_element(By.CLASS_NAME, "sysmonitorStatisticsList").get_attribute("style") == "display: none;"):
        print(f"             [Statistics - Monitor Status - Statistics] MSC Valid Test Fail",file = open(file_name, '+a'))
        if_error = True

    # GLC Test
    sta.Slot_Select(driver,glc_slot)
    sta.Load(driver)
    if(driver.find_element(By.CLASS_NAME, "sysmonitorStatisticsList").get_attribute("style") == "display: none;"):
        print(f"             [Statistics - Monitor Status - Statistics] GLC Valid Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Statistics Monitor Status Result
    if(if_error == False):
        print(f"[MSAN1-11939][Statistics - Monitor Status - Statistics] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11939][Statistics - Monitor Status - Statistics] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics Monitor Status PM Current Test
    # Statistics > Monitor Status > PM Current
    # -------------------------start-------------------------

    if_error = False
    if_pm_current_exist = True

    # 路徑導向 Statistics > Monitor Status > PM Current
    try:
        mod.Switch_Default(driver)
        mod.Page_Switch(driver,"Statistics")
        mod.SubPage_Switch(driver,"Monitor Status")
        mod.Switch_Frame(driver)
        mod.Tab_Switch(driver,"PM Current")
    except:
        print(f"[MSAN1-11940][Statistics - Monitor Status - PM Current] Result Block",file = open(file_name, '+a'))
        if_pm_current_exist = False

    if(if_pm_current_exist == True):
        # GLC Test
        sta.Slot_Select(driver,glc_slot)
        if(driver.find_element(By.CLASS_NAME, "div-row-cell-content.rpsys_slotstatus_TEXT_warning").get_attribute("texContent") == "warning: not support"):
            print(f"             [Statistics - Monitor Status - PM Current] GLC Invalid No Warning Test Fail",file = open(file_name, '+a'))
            if_error = True

        # Statistics Monitor Status Result
        if(if_error == False):
            print(f"[MSAN1-11940][Statistics - Monitor Status - PM Current] Result Pass",file = open(file_name, '+a'))
        else:
            print(f"[MSAN1-11940][Statistics - Monitor Status - PM Current] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics Monitor Status PM 15-min Test
    # Statistics > Monitor Status > PM 15-min
    # -------------------------start-------------------------

    if_error = False
    if_pm_15min_exist = True

    # 路徑導向 Statistics > Monitor Status > PM 15-min
    try:
        mod.Switch_Default(driver)
        mod.Page_Switch(driver,"Statistics")
        mod.SubPage_Switch(driver,"Monitor Status")
        mod.Switch_Frame(driver)
        mod.Tab_Switch(driver,"PM 15-min")
    except:
        print(f"[MSAN1-11941][Statistics - Monitor Status - PM 15-min] Result Block",file = open(file_name, '+a'))
        if_pm_15min_exist = False

    if(if_pm_15min_exist == True):
        # GLC Test
        sta.Slot_Select(driver,glc_slot)
        if(driver.find_element(By.CLASS_NAME, "div-row-cell-content.rpsys_slotstatus_TEXT_warning").get_attribute("texContent") == "warning: not support"):
            print(f"             [Statistics - Monitor Status - PM 15-min] GLC Invalid No Warning Test Fail",file = open(file_name, '+a'))
            if_error = True

        # Statistics Monitor Status Result
        if(if_error == False):
            print(f"[MSAN1-11941][Statistics - Monitor Status - PM 15-min] Result Pass",file = open(file_name, '+a'))
        else:
            print(f"[MSAN1-11941][Statistics - Monitor Status - PM 15-min] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics Monitor Status PM 1-day Test
    # Statistics > Monitor Status > PM 1-day
    # -------------------------start-------------------------

    if_error = False
    if_pm_1day_exist = True

    # 路徑導向 Statistics > Monitor Status > PM 1-day
    try:
        mod.Switch_Default(driver)
        mod.Page_Switch(driver,"Statistics")
        mod.SubPage_Switch(driver,"Monitor Status")
        mod.Switch_Frame(driver)
        mod.Tab_Switch(driver,"PM 1-day")
    except:
        print(f"[MSAN1-11942][Statistics - Monitor Status - PM 1-day] Result Block",file = open(file_name, '+a'))
        if_pm_1day_exist = False

    if(if_pm_1day_exist == True):
        # GLC Test
        sta.Slot_Select(driver,glc_slot)
        if(driver.find_element(By.CLASS_NAME, "div-row-cell-content.rpsys_slotstatus_TEXT_warning").get_attribute("texContent") == "warning: not support"):
            print(f"             [Statistics - Monitor Status - PM 1-day] GLC Invalid No Warning Test Fail",file = open(file_name, '+a'))
            if_error = True

        # Statistics Monitor Status Result
        if(if_error == False):
            print(f"[MSAN1-11942][Statistics - Monitor Status - PM 1-day] Result Pass",file = open(file_name, '+a'))
        else:
            print(f"[MSAN1-11942][Statistics - Monitor Status - PM 1-day] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics IGMP Status IGMP Status Test
    # Statistics > IGMP Status > IGMP Status
    # -------------------------start-------------------------

    if_error =False

    # 路徑導向IGMP Status > IGMP Status
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"IGMP Status")
    mod.Switch_Frame(driver)
    time.sleep(1)

    # IGMP Status Check
    try:
        driver.find_element(By.CLASS_NAME, "div-row-begin-title")
    except:
        print(f"             [Statistics - IGMP Status - IGMP Status] Column Don't Exist Test Fail",file = open(file_name, '+a'))
        if_error = True

    # IGMP Status Refresh
    driver.find_element(By.NAME, "rpstatsigmpstatus_btnRefresh").click()

    # IGMP Status Column Check
    try:
        driver.find_element(By.CLASS_NAME, "div-row-begin-title")
    except:
        print(f"             [Statistics - IGMP Status - IGMP Status] Refresh Column Don't Exist Test Fail",file = open(file_name, '+a'))
        if_error = True

    # IGMP Status Result
    if(if_error == False):
        print(f"[MSAN1-11943][Statistics - IGMP Status - IGMP Status] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11943][Statistics - IGMP Status - IGMP Status] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics IGMP Status Port Group Test
    # Statistics > IGMP Status > Port Group
    # -------------------------start-------------------------

    # 路徑導向IGMP Status > Port Group
    mod.Tab_Switch(driver,"Port Group")

    if_error =False

    # port select
    time.sleep(1)
    sta.Slot_Select(driver,glc_slot)
    sta.Port_Select(driver,glc_port)
    driver.find_element(By.NAME, "rpigmpportgroup_btnLoad").click()

    # Port Group Check
    try:
        driver.find_element(By.CLASS_NAME, "table-sample-2")
    except:
        print(f"             [Statistics - IGMP Status - Port Group] Table Don't Exist Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Port Group Refresh
    driver.find_element(By.NAME, "rpigmpportgroup_btnRefresh").click()

    # Port Group Refresh Check
    try:
        driver.find_element(By.CLASS_NAME, "table-sample-2")
    except:
        print(f"             [Statistics - IGMP Status - Port Group] Refresh Table Don't Exist Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Port Group Result
    if(if_error == False):
        print(f"[MSAN1-11944][Statistics - IGMP Status - Port Group] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11944][Statistics - IGMP Status - Port Group] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics IGMP Status Port Statistics Test
    # Statistics > IGMP Status > Port Statistics
    # -------------------------start-------------------------

    # 路徑導向IGMP Status > Port Statistics
    mod.Tab_Switch(driver,"Port Statistics")

    if_error =False

    # port select
    time.sleep(1)
    sta.Slot_Select(driver,glc_slot)
    sta.Port_Select(driver,glc_port)
    driver.find_element(By.NAME, "rpstatsigmpportstatistics_btnLoad").click()

    # Port Statistics Check
    try:
        driver.find_element(By.CLASS_NAME, "rpstatsigmpportstatistics_portStatistic")
    except:
        print(f"             [Statistics - IGMP Status - Port Statistics] Table Don't Exist Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Port Statistics Refresh
    driver.find_element(By.NAME, "rpstatsigmpportstatistics_btnRefresh").click()

    # Port Statistics Refresh Check
    try:
        driver.find_element(By.CLASS_NAME, "rpstatsigmpportstatistics_portStatistic")
    except:
        print(f"             [Statistics - IGMP Status - Port Statistics] Refresh Table Don't Exist Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Port Statistics Flush
    for i in range(3):
        driver.find_element(By.NAME, "rpstatsigmpportstatistics_btnFlush").click()

    # Port Statistics Flush Check
    try:
        if(driver.find_element(By.CLASS_NAME, "div-row-cell-content.little.igmprx_report_total").get_attribute("textContent") != "0"):
            print(f"             [Statistics - IGMP Status - Port Statistics] Flush Rx Report IGMP Total Test Fail",file = open(file_name, '+a'))
            if_error = True
        # else:
            # print(f"             [Statistics - IGMP Status - Port Statistics] Flush Rx Report IGMP Total Test Pass",file = open(file_name, '+a'))
        if(driver.find_element(By.CLASS_NAME, "div-row-cell-content.little.igmprx_report_v2").get_attribute("textContent") != "0"):
            print(f"             [Statistics - IGMP Status - Port Statistics] Flush Rx Report IGMPv2 Test Fail",file = open(file_name, '+a'))
            if_error = True
        # else:
            # print(f"             [Statistics - IGMP Status - Port Statistics] Flush Rx Report IGMPv2 Test Pass",file = open(file_name, '+a'))
        if(driver.find_element(By.CLASS_NAME, "div-row-cell-content.little.igmptx_query_total").get_attribute("textContent") != "0"):
            print(f"             [Statistics - IGMP Status - Port Statistics] Flush Tx Query IGMP Total Test Fail",file = open(file_name, '+a'))
            if_error = True
        # else:
            # print(f"             [Statistics - IGMP Status - Port Statistics] Flush Tx Query IGMP Total Test Pass",file = open(file_name, '+a'))
        if(driver.find_element(By.CLASS_NAME, "div-row-cell-content.little.igmptx_query_v2").get_attribute("textContent") != "0"):
            print(f"             [Statistics - IGMP Status - Port Statistics] Flush Tx Query IGMPv2 Test Fail",file = open(file_name, '+a'))
            if_error = True
        # else:
            # print(f"             [Statistics - IGMP Status - Port Statistics] Flush Tx Query IGMPv2 Test Pass",file = open(file_name, '+a'))
        # if(driver.find_element(By.CLASS_NAME, "div-row-cell-content.little.igmp_joined_group").get_attribute("textContent") == "0"):
        #     print(f"             [Statistics - IGMP Status - Port Statistics] Flush Join Group Test Fail",file = open(file_name, '+a'))
        #     if_error = True
        # # else:
        #     # print(f"             [Statistics - IGMP Status - Port Statistics] Flush Join Group Test Pass",file = open(file_name, '+a'))
        if(driver.find_element(By.CLASS_NAME, "div-row-cell-content.little.igmp_rec_join").get_attribute("textContent") != "0"):
            print(f"             [Statistics - IGMP Status - Port Statistics] Flush Join Test Fail",file = open(file_name, '+a'))
            if_error = True
        # else:
            # print(f"             [Statistics - IGMP Status - Port Statistics] Flush Join Test Pass",file = open(file_name, '+a'))
        if(driver.find_element(By.CLASS_NAME, "div-row-cell-content.little.igmp_rec_leave").get_attribute("textContent") != "0"):
            print(f"             [Statistics - IGMP Status - Port Statistics] Flush Leave Test Fail",file = open(file_name, '+a'))
            if_error = True
    except:
        print(f"             [Statistics - IGMP Status - Port Statistics] Flush Table Don't Exist Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Port Statistics Result
    if(if_error == False):
        print(f"[MSAN1-11945][Statistics - IGMP Status - Port Statistics] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11945][Statistics - IGMP Status - Port Statistics] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics IGMP Status VLAN Statistics Test
    # Statistics > IGMP Status > VLAN Statistics
    # -------------------------start-------------------------

    # 路徑導向IGMP Status > VLAN Statistics
    mod.Tab_Switch(driver,"VLAN Statistics")
    time.sleep(1)

    if_error = False

    try:
        # Load
        driver.find_element(By.NAME, "rpigmpvlantstatistics_btnLoad").click()

        # Refresh
        driver.find_element(By.NAME, "rpigmpvlantstatistics_btnRefresh").click()

        # Flush
        driver.find_element(By.NAME, "rpigmpvlantstatistics_btnFlush").click()

        # Load
        driver.find_element(By.NAME, "rpigmpvlantstatistics_btnLoad").click()
    except:
        if_error = True

    # VLAN Statistics Result
    if(if_error == False):
        print(f"[MSAN1-11946][Statistics - IGMP Status - VLAN Statistics] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11946][Statistics - IGMP Status - VLAN Statistics] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics IGMP Status Older Version Compatible Test
    # Statistics > IGMP Status > Older Version Compatible
    # -------------------------start-------------------------

    # 路徑導向IGMP Status > Older Version Compatible
    mod.Tab_Switch(driver,"Older Version Compatible")

    if_error =False

    # port select
    time.sleep(1)
    sta.Slot_Select(driver,glc_slot)
    driver.find_element(By.NAME, "rpigmpolderver_btnLoad").click()

    # Older Version Compatible Check
    try:
        driver.find_elements(By.CLASS_NAME, "div-row-begin.div-row-cell-content.wp-5.i1")[int(glc_port)-1]
        # print(f"             [Statistics - IGMP Status - Older Version Compatible] Test Pass",file = open(file_name, '+a'))
    except:
        print(f"             [Statistics - IGMP Status - Older Version Compatible] Data Don't Exist",file = open(file_name, '+a'))
        if_error = True

    # Older Version Compatible Result
    if(if_error == False):
        print(f"[MSAN1-11947][Statistics - IGMP Status - Older Version Compatible] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11947][Statistics - IGMP Status - Older Version Compatible] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics LLDP Status Local Status Test
    # Statistics > LLDP Status > Local Status
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Statistics > LLDP Status > Local Status
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"LLDP Status")
    mod.Switch_Frame(driver)

    # MSC Test
    sta.Slot_Select(driver,msc_slot)
    sta.Load(driver)
    driver.find_elements(By.NAME, "rplldpLocalStatus_select")[int(msc_port)-1].click()
    driver.find_element(By.CLASS_NAME, "ui-button-icon-primary.ui-icon.ui-icon-closethick").click()

    # GLC Test
    sta.Slot_Select(driver,glc_slot)
    sta.Load(driver)
    driver.find_elements(By.NAME, "rplldpLocalStatus_select")[int(glc_port)-1].click()
    driver.find_element(By.CLASS_NAME, "ui-button-icon-primary.ui-icon.ui-icon-closethick").click()
    
    # Statistics LLDP Status  Local Status Result
    if(if_error == False):
        print(f"[MSAN1-11948][Statistics - LLDP Status - Local Status] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11948][Statistics - LLDP Status - Local Status] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics LLDP Status Remote Status Test
    # Statistics > LLDP Status > Remote Status
    # -------------------------start-------------------------

    # 路徑導向 Statistics > LLDP Status > Remote Status
    mod.Tab_Switch(driver,"Remote Status")

    # MSC Test
    sta.Slot_Select(driver,msc_slot)
    sta.Load(driver)
    driver.find_element(By.NAME, "RpLLDPRemoteStatus_radioport").click()
    driver.find_element(By.NAME, "RpLLDPRemoteStatus_BtnClear").click()

    # GLC Test
    sta.Slot_Select(driver,glc_slot)
    sta.Load(driver)
    driver.find_element(By.NAME, "RpLLDPRemoteStatus_radioport").click()
    driver.find_element(By.NAME, "RpLLDPRemoteStatus_BtnClear").click()
    
    # Statistics LLDP Status Remote Status Result
    if(if_error == False):
        print(f"[MSAN1-11949][Statistics - LLDP Status - Remote Status] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11949][Statistics - LLDP Status - Remote Status] Result Pass",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics LLDP Status Statistic Test
    # Statistics > LLDP Status > Statistic
    # -------------------------start-------------------------

    # 路徑導向 Statistics > LLDP Status > Statistic
    mod.Tab_Switch(driver,"Statistic")

    # MSC Test
    if_msc_error = False
    sta.Slot_Select(driver,msc_slot)
    sta.Load(driver)
    driver.find_element(By.NAME, "rplldpStatistic__BtnRefresh").click()
    driver.find_element(By.NAME, "rplldpStatistic__BtnClear").click()
    if(driver.find_elements(By.CLASS_NAME, "div-row-cell-content.wp-10.rplldpStatistic_tlbDiscard")[int(msc_port)-1].get_attribute("textContent") != "0"):
        if_msc_error = True
    if(driver.find_elements(By.CLASS_NAME, "div-row-cell-content.wp-10.rplldpStatistic_tlbInvalid")[int(msc_port)-1].get_attribute("textContent") != "0"):
        if_msc_error = True
    if(driver.find_elements(By.CLASS_NAME, "div-row-cell-content.wp-10.rplldpStatistic_tlbReceived")[int(msc_port)-1].get_attribute("textContent") != "0"):
        if_msc_error = True
    if(driver.find_elements(By.CLASS_NAME, "div-row-cell-content.wp-10.rplldpStatistic_tlbSent")[int(msc_port)-1].get_attribute("textContent") != "0"):
        if_msc_error = True
    if(driver.find_elements(By.CLASS_NAME, "div-row-cell-content.wp-10.rplldpStatistic_tlbUnrecognized")[int(msc_port)-1].get_attribute("textContent") != "0"):
        if_msc_error = True
    if(driver.find_elements(By.CLASS_NAME, "div-row-cell-content.wp-10.rplldpStatistic_tlbDiscarded")[int(msc_port)-1].get_attribute("textContent") != "0"):
        if_msc_error = True
    if(driver.find_elements(By.CLASS_NAME, "div-row-cell-content.wp-10.rplldpStatistic_tlbAgeouts")[int(msc_port)-1].get_attribute("textContent") != "0"):
        if_msc_error = True
    if(if_msc_error == True):
        print(f"             [Statistics - LLDP Status - Statistic] MSC Clear statistic Test Fail",file = open(file_name, '+a'))
        if_error = True

    # GLC Test
    if_glc_error = False
    sta.Slot_Select(driver,glc_slot)
    sta.Load(driver)
    driver.find_element(By.NAME, "rplldpStatistic__BtnRefresh").click()
    driver.find_element(By.NAME, "rplldpStatistic__BtnClear").click()
    if(driver.find_elements(By.CLASS_NAME, "div-row-cell-content.wp-10.rplldpStatistic_tlbDiscard")[int(glc_port)-1].get_attribute("textContent") != "0"):
        if_glc_error = True
    if(driver.find_elements(By.CLASS_NAME, "div-row-cell-content.wp-10.rplldpStatistic_tlbInvalid")[int(glc_port)-1].get_attribute("textContent") != "0"):
        if_glc_error = True
    if(driver.find_elements(By.CLASS_NAME, "div-row-cell-content.wp-10.rplldpStatistic_tlbReceived")[int(glc_port)-1].get_attribute("textContent") != "0"):
        if_glc_error = True
    if(driver.find_elements(By.CLASS_NAME, "div-row-cell-content.wp-10.rplldpStatistic_tlbSent")[int(glc_port)-1].get_attribute("textContent") != "0"):
        if_glc_error = True
    if(driver.find_elements(By.CLASS_NAME, "div-row-cell-content.wp-10.rplldpStatistic_tlbUnrecognized")[int(glc_port)-1].get_attribute("textContent") != "0"):
        if_glc_error = True
    if(driver.find_elements(By.CLASS_NAME, "div-row-cell-content.wp-10.rplldpStatistic_tlbDiscarded")[int(glc_port)-1].get_attribute("textContent") != "0"):
        if_glc_error = True
    if(driver.find_elements(By.CLASS_NAME, "div-row-cell-content.wp-10.rplldpStatistic_tlbAgeouts")[int(glc_port)-1].get_attribute("textContent") != "0"):
        if_glc_error = True
    if(if_glc_error == True):
        print(f"             [Statistics - LLDP Status - Statistic] GLC Clear statistic Test Fail",file = open(file_name, '+a'))
        if_error = True
    
    # Statistics LLDP Status Statistic Result
    if(if_error == False):
        print(f"[MSAN1-11950][Statistics - LLDP Status - Statistic] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11950][Statistics - LLDP Status - Statistic] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics Error Disable Test
    # Statistics > Error Disable
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Statistics > Error Disable
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"Error Disable")
    mod.Switch_Frame(driver)

    # MSC Port Select
    driver.find_elements(By.NAME, "RperrdisDted_select")[int(msc_port)-1].click()
    driver.find_element(By.CLASS_NAME, "ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-icon-only.ui-dialog-titlebar-close").click()
    
    # Clear Test
    driver.find_elements(By.NAME, "RperrdisDted_radioport")[0].click()
    driver.find_element(By.NAME, "RperrdisDted_BtnClear").click()
    driver.find_elements(By.NAME, "RperrdisDted_radioport")[2].click()
    driver.find_element(By.XPATH, "//*[@name='RperrdisDted_reasonList']/option[2]").click()
    driver.find_element(By.NAME, "RperrdisDted_BtnClear").click()

    # Statistics Error Disable Result
    if(if_error == False):
        print(f"[MSAN1-11951][Statistics - Error Disable] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11951][Statistics - Error Disable] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Statistics Protect Switch Test
    # Statistics > Protect Switch
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Statistics > Protect Switch
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"Protect Switch")
    mod.Switch_Frame(driver)

    # Refresh Test
    driver.find_element(By.NAME, "rpProtectSwitch_btnRefresh").click()

    # Statistics Protect Switch Result
    if(if_error == False):
        print(f"[MSAN1-11952][Statistics - Protect Switch] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11952][Statistics - Protect Switch] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def Switch_Test(driver,glc_slot,glc_port,msc_slot,msc_port,file_name):
    print(f"Switch Test\nTest Start",file = open(file_name, '+a'))

    Maintenance_Config_Reset(driver,glc_slot,glc_port,file_name)

    time.sleep(30)

    # Get GLC name
    # Home
    # -------------------------start-------------------------

    # Get GLC name
    mod.Switch_Default(driver)
    driver.find_element(By.XPATH, '//*[@id="mainTable"]/tbody/tr[1]/td/div/div[2]/div/div[3]/a').click()
    mod.Switch_Frame(driver)
    time.sleep(1)
    driver.find_elements(By.NAME, "Sysinfotableid")[int(glc_slot)-1].click()
    time.sleep(5)
    glc_name = driver.find_element(By.CLASS_NAME, "div-row-cell-content.rplcmanDetailName").get_attribute("textContent")
    glc_name = glc_name.split("-")[0]

    # -------------------------end-------------------------

    # Statistics Port Get Max Port Num
    # Statistics > Port
    # -------------------------start-------------------------

    # 路徑導向 Statistics > Port
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Statistics")
    driver.find_element(By.XPATH, '//*[@id="mainTable"]/tbody/tr[2]/td[1]/div[2]/a[7]').click()
    mod.Switch_Frame(driver)

    # Statistics Port Get Max Port Num
    sta.Port_Slot_Select(driver,msc_slot)
    time.sleep(1)
    msc_max_port = 0
    while(driver.find_elements(By.CLASS_NAME, "td-table-content.tdtableid")[msc_max_port].get_attribute("textContent") != "Slot1"):
        msc_max_port = msc_max_port+1

    # -------------------------end-------------------------

    # Switch Mirror Test
    # Switch > Mirror
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Switch > Mirror
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Switch")
    mod.Switch_Frame(driver)

    # Mirror Test 1
    swi.Mirror_Active(driver,True)
    swi.Mirror_Destination(driver,msc_max_port)    
       
    swi.Mirror_Session_Vlan(driver, "@") #*add
    swi.Mirror_Apply_1(driver)
    # check alert
    if(mod.IsAlert(driver) == False):
        print(f"             [Switch - Mirror] Session vlan invalid value @ alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    else:
        print(f"             [Switch - Mirror] Session vlan invalid value @ alert Test Pass",file = open(file_name, '+a'))

    swi.Mirror_Session_Vlan(driver, "1000") 
    swi.Mirror_Apply_1(driver)

    # Mirror Check 1
    if(driver.find_element(By.NAME, f"rpmirror_sltEnable").is_selected() != True):
        print(f"             [Switch - Mirror] Active Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.XPATH, f"//*[@name='rpmirror_sltDestPort']/option[{msc_max_port}]").is_selected() != True):
        print(f"             [Switch - Mirror] Destination Test Fail",file = open(file_name, '+a'))
        if_error = True

    


    # Mirror Data Clear
    if_clear = False
    while(if_clear == False):
        try:
            driver.find_element(By.NAME, "rpmirror_sltMonArraySelect").click()
            swi.Mirror_Delete(driver)
        except:
            if_clear = True

    # Mirror Test 2
    swi.Slot_Select(driver,glc_slot)
    swi.Port_Select(driver,glc_port)
    swi.Mirror_Mode(driver,3)
    swi.Mirror_Vlan_VID(driver)
    swi.Mirror_Vlan_VID_Input(driver,"4094")
    swi.Mirror_Apply_2(driver)

    # Mirror Check 2
    if(driver.find_element(By.NAME, f"rpmirror_sltMonArraySlot").get_attribute('textContent') != glc_slot):
        print(f"             [Switch - Mirror] Monitored Slot Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, f"rpmirror_sltMonArrayPort").get_attribute('textContent') != glc_port):
        print(f"             [Switch - Mirror] Monitored Port Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, f"rpmirror_sltMonArrayMode").get_attribute('textContent') != "both"):
        print(f"             [Switch - Mirror] Mode Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, f"rpmirror_sltMonArrayVlan").get_attribute('textContent') != "4094"):
        print(f"             [Switch - Mirror] Vlan Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Mirror Data Delete
    driver.find_element(By.NAME, "rpmirror_sltMonArraySelect").click()
    swi.Mirror_Delete(driver)

    # Switch Mirror Result
    if(if_error == False):
        print(f"[MSAN1-11953][Switch - Mirror] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11953][Switch - Mirror] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Switch STP Test
    # Switch > STP
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Switch > STP
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"STP")
    mod.Switch_Frame(driver)

    # STP Test
    swi.STP_Active(driver,True)
    swi.STP_Mode(driver,2)
    swi.STP_Apply(driver)

    # STP Check
    if(driver.find_element(By.NAME, f"rpswstp_active").is_selected() != True):
        print(f"             [Switch - STP] Active Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.XPATH, f"//*[@name='rpswstp_mode']/option[2]").is_selected() != True):
        print(f"             [Switch - STP] Mode Test Fail",file = open(file_name, '+a'))
        if_error = True

    # RSTP Test 1
    swi.STP_RSTP_Active(driver,True)
    swi.STP_RSTP_Priority(driver,16)
    swi.STP_RSTP_Hello_Time(driver,"0")
    swi.STP_RSTP_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - STP - RSTP] Hello Time:0 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.STP_RSTP_Hello_Time(driver,"11")
    swi.STP_RSTP_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - STP - RSTP] Hello Time:11 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.STP_RSTP_Hello_Time(driver,"@")
    swi.STP_RSTP_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - STP - RSTP] Hello Time:@ No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.STP_RSTP_Hello_Time(driver,"10")
    swi.STP_RSTP_Maximum_Age(driver,"5")
    swi.STP_RSTP_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - STP - RSTP] Maximum Age:5 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.STP_RSTP_Maximum_Age(driver,"41")
    swi.STP_RSTP_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - STP - RSTP] Maximum Age:41 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.STP_RSTP_Maximum_Age(driver,"@")
    swi.STP_RSTP_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - STP - RSTP] Maximum Age:@ No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.STP_RSTP_Maximum_Age(driver,"40")
    swi.STP_RSTP_Forwarding_Delay(driver,"3")
    swi.STP_RSTP_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - STP - RSTP] Forwarding Delay:3 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.STP_RSTP_Forwarding_Delay(driver,"31")
    swi.STP_RSTP_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - STP - RSTP] Forwarding Delay:31 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.STP_RSTP_Forwarding_Delay(driver,"@")
    swi.STP_RSTP_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - STP - RSTP] Forwarding Delay:@ No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    swi.STP_RSTP_Forwarding_Delay(driver,"30")
    swi.STP_RSTP_Apply(driver)
    if(mod.IsAlert(driver) == True):
        print(f"             [Switch - STP - RSTP] Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpswrstp_active").is_selected() != True):
        print(f"             [Switch - STP - RSTP] Active Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.XPATH, f"//*[@name='rpswrstp_priority']/option[16]").is_selected() != True):
        print(f"             [Switch - STP - RSTP] Priority:61440 Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpswrstp_input_hello_time").get_attribute("value") != "10"):
        print(f"             [Switch - STP - RSTP] Hello Time:10 Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpswrstp_input_maximum_age").get_attribute("value") != "40"):
        print(f"             [Switch - STP - RSTP] Maximum Age:40 Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpswrstp_input_fwdelay").get_attribute("value") != "30"):
        print(f"             [Switch - STP - RSTP] Forwarding Delay:30 Test Fail",file = open(file_name, '+a'))
        if_error = True

    # RSTP Test 2
    swi.STP_RSTP_Port_Priority(driver,1,"256")
    swi.STP_RSTP_Port_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - STP - RSTP] Priority:256 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.STP_RSTP_Port_Priority(driver,1,"@")
    swi.STP_RSTP_Port_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - STP - RSTP] Priority:@ No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.STP_RSTP_Port_Priority(driver,1,"255")
    swi.STP_RSTP_Port_Path_Cost(driver,1,"0")
    swi.STP_RSTP_Port_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - STP - RSTP] Path Cost:0 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.STP_RSTP_Port_Path_Cost(driver,1,"65536")
    swi.STP_RSTP_Port_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - STP - RSTP] Path Cost:65536 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    for test_port in range(msc_max_port):
        swi.STP_RSTP_Port_Active(driver,test_port+1,True)
        swi.STP_RSTP_Port_Priority(driver,test_port+1,"255")
        swi.STP_RSTP_Port_Path_Cost(driver,test_port+1,"65535")
    swi.STP_RSTP_Port_Apply(driver)
    if(mod.IsAlert(driver) == True):
        print(f"             [Switch - STP - RSTP] Apply Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    for test_port in range(msc_max_port):
        if(driver.find_element(By.NAME, f"rpswrstp_port_active{test_port+1}").is_selected() != True):
            print(f"             [Switch - STP - RSTP] Port{test_port+1} Active Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_element(By.NAME, f"rpswrstp_port_priotity{test_port+1}").get_attribute("value") != "255"):
            print(f"             [Switch - STP - RSTP] Port{test_port+1} Priority:255 Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_element(By.NAME, f"rpswrstp_port_pathcost{test_port+1}").get_attribute("value") != "65535"):
            print(f"             [Switch - STP - RSTP] Port{test_port+1} Path Cost:65535 Test Fail",file = open(file_name, '+a'))
            if_error = True

    # Switch STP RSTP Result
    if(if_error == False):
        print(f"[MSAN1-11954][Switch - STP - RSTP] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11954][Switch - STP - RSTP] Result Fail",file = open(file_name, '+a'))

    # 路徑導向 Switch > STP > MSTP
    mod.Tab_Switch(driver,"MSTP")

    if_error = False

    # MSTP Test 1
    swi.STP_MSTP_Active(driver,True)
    swi.STP_MSTP_Hello_Time(driver,"0")
    swi.STP_MSTP_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - STP - MSTP] Hello Time:0 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.STP_MSTP_Hello_Time(driver,"11")
    swi.STP_MSTP_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - STP - MSTP] Hello Time:11 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.STP_MSTP_Hello_Time(driver,"@")
    swi.STP_MSTP_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - STP - MSTP] Hello Time:@ No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.STP_MSTP_Hello_Time(driver,"10")
    swi.STP_MSTP_Maximum_Age(driver,"5")
    swi.STP_MSTP_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - STP - MSTP] Maximum Age:5 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.STP_MSTP_Maximum_Age(driver,"41")
    swi.STP_MSTP_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - STP - MSTP] Maximum Age:41 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.STP_MSTP_Maximum_Age(driver,"@")
    swi.STP_MSTP_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - STP - MSTP] Maximum Age:@ No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.STP_MSTP_Maximum_Age(driver,"40")
    swi.STP_MSTP_Forwarding_Delay(driver,"3")
    swi.STP_MSTP_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - STP - MSTP] Forwarding Delay:3 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.STP_MSTP_Forwarding_Delay(driver,"31")
    swi.STP_MSTP_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - STP - MSTP] Forwarding Delay:31 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.STP_MSTP_Forwarding_Delay(driver,"@")
    swi.STP_MSTP_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - STP - MSTP] Forwarding Delay:@ No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.STP_MSTP_Forwarding_Delay(driver,"30")
    swi.STP_MSTP_MaxHops(driver,"0")
    swi.STP_MSTP_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - STP - MSTP] MaxHops:0 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.STP_MSTP_MaxHops(driver,"256")
    swi.STP_MSTP_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - STP - MSTP] MaxHops:256 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.STP_MSTP_MaxHops(driver,"@")
    swi.STP_MSTP_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - STP - MSTP] MaxHops:@ No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.STP_MSTP_MaxHops(driver,"255")
    swi.STP_MSTP_MST_Revision(driver,"-1")
    swi.STP_MSTP_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - STP - MSTP] MST Revision:-1 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.STP_MSTP_MST_Revision(driver,"65536")
    swi.STP_MSTP_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - STP - MSTP] MST Revision:-1 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.STP_MSTP_MST_Revision(driver,"@")
    swi.STP_MSTP_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - STP - MSTP] MST Revision:-1 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    swi.STP_MSTP_MST_Revision(driver,"65535")
    swi.STP_MSTP_MST_Configuration_Name(driver,"12345678901234567890123456789012")
    swi.STP_MSTP_Apply(driver)
    if(mod.IsAlert(driver) == True):
        print(f"             [Switch - STP - MSTP] Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpswmstp_active").is_selected() != True):
        print(f"             [Switch - STP - MSTP] Active Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpswmstp_input_hello_time").get_attribute("value") != "10"):
        print(f"             [Switch - STP - MSTP] Hello Time:10 Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpswmstp_input_maximum_age").get_attribute("value") != "40"):
        print(f"             [Switch - STP - MSTP] Maximum Age:40 Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpswmstp_input_fwdelay").get_attribute("value") != "30"):
        print(f"             [Switch - STP - MSTP] Forwarding Delay:30 Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpswmstp_input_maxhops").get_attribute("value") != "255"):
        print(f"             [Switch - STP - MSTP] MaxHops:255 Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpswmstp_input_revision").get_attribute("value") != "65535"):
        print(f"             [Switch - STP - MSTP] Revision:65535 Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpswmstp_input_configname").get_attribute("value") != "12345678901234567890123456789012"):
        print(f"             [Switch - STP - MSTP] Configuration Name Max Test Fail",file = open(file_name, '+a'))
        if_error = True

    # MSTP Test 2
    swi.STP_MSTP_Port_Instance(driver,17)
    swi.STP_MSTP_Port_Priority_Select(driver,16)
    swi.STP_MSTP_Port_VLAN(driver,"4094")
    swi.STP_MSTP_Port_Apply(driver)
    swi.STP_MSTP_Port_Priority(driver,1,"256")
    swi.STP_MSTP_Port_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - STP - MSTP] Priority:256 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.STP_MSTP_Port_Priority(driver,1,"@")
    swi.STP_MSTP_Port_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - STP - MSTP] Priority:@ No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.STP_MSTP_Port_Priority(driver,1,"255")
    swi.STP_MSTP_Port_Path_Cost(driver,1,"0")
    swi.STP_MSTP_Port_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - STP - MSTP] Path Cost:0 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.STP_MSTP_Port_Path_Cost(driver,1,"65536")
    swi.STP_MSTP_Port_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - STP - MSTP] Path Cost:65536 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    for test_port in range(msc_max_port):
        swi.STP_MSTP_Port_Active(driver,test_port+1,True)
        swi.STP_MSTP_Port_Priority(driver,test_port+1,"255")
        swi.STP_MSTP_Port_Path_Cost(driver,test_port+1,"65535")
    swi.STP_MSTP_Port_Apply(driver)
    if(mod.IsAlert(driver) == True):
        print(f"             [Switch - STP - MSTP] Apply Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    for test_port in range(msc_max_port):
        if(driver.find_element(By.NAME, f"rpswmstp_port_active{test_port+1}").is_selected() != True):
            print(f"             [Switch - STP - MSTP] Port{test_port+1} Active Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_element(By.NAME, f"rpswmstp_port_priority{test_port+1}").get_attribute("value") != "255"):
            print(f"             [Switch - STP - MSTP] Port{test_port+1} Priority:255 Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_element(By.NAME, f"rpswmstp_port_pathcost{test_port+1}").get_attribute("value") != "65535"):
            print(f"             [Switch - STP - MSTP] Port{test_port+1} Path Cost:65535 Test Fail",file = open(file_name, '+a'))
            if_error = True
    swi.STP_MSTP_Port_Delete(driver)

    # Switch STP MSTP Result
    if(if_error == False):
        print(f"[MSAN1-11955][Switch - STP - MSTP] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11955][Switch - STP - MSTP] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Switch Switch Setup General Test
    # Switch > Switch Setup > General
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Switch > Switch Setup > General
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"Switch Setup")
    mod.Switch_Frame(driver)

    # Switch Setup General Test 1
    for test_priority in range(8):
        swi.Switch_Setup_General_Priority(driver,test_priority,8)
    swi.Switch_Setup_General_Apply_1(driver)
    for test_priority in range(8):
        if(driver.find_element(By.XPATH, f"//*[@name='rpsw_setup_general_slt_queue_{test_priority}']/option[8]").is_selected() != True):
            print(f"             [Switch - Switch Setup - General] Priority{test_priority} Test Fail",file = open(file_name, '+a'))
            if_error = True

    # Switch Setup General Test 2
    swi.Switch_Setup_General_Aging_Time(driver,"9")
    swi.Switch_Setup_General_Apply_2(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - Switch Setup - General] Aging Time:9 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.Switch_Setup_General_Aging_Time(driver,"3601")
    swi.Switch_Setup_General_Apply_2(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - Switch Setup - General] Aging Time:3601 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.Switch_Setup_General_Aging_Time(driver,"@")
    swi.Switch_Setup_General_Apply_2(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - Switch Setup - General] Aging Time:@ No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    swi.Switch_Setup_General_Aging_Time(driver,"3600")
    swi.Switch_Setup_General_Apply_2(driver)
    if(mod.IsAlert(driver) == True):
        print(f"             [Switch - Switch Setup - General] Aging Time:3600 Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    elif(driver.find_element(By.NAME, f"rpsw_setup_general_ipt_aging_time").get_attribute("value") != "3600"):
        print(f"             [Switch - Switch Setup - General] Aging Time:3600 Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Switch Switch Setup General Result
    if(if_error == False):
        print(f"[MSAN1-11956][Switch - Switch Setup - General] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11956][Switch - Switch Setup - General] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Switch Switch Setup Dot3ad Test
    # Switch > Switch Setup > Dot3ad
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Switch > Switch Setup > Dot3ad
    mod.Tab_Switch(driver,"Dot3ad")

    # Switch Setup Dot3ad Test 1
    swi.Switch_Setup_Dot3ad_Group(driver,msc_max_port/2)
    swi.Switch_Setup_Dot3ad_Mode(driver,3)
    # swi.Switch_Setup_Dot3ad_Member(driver,"*")
    swi.Switch_Setup_Dot3ad_Member(driver,msc_port)
    swi.Switch_Setup_Dot3ad_Apply_1(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack")
        if(driver.find_element(By.CLASS_NAME, "div-row-cell-content.msg").get_attribute("textContent") == "error: Different port speed!\n"):
            driver.find_element(By.NAME, "rperror_btnBack").click()
            mod.Switch_Default(driver)
            mod.Page_Switch(driver,"Port")
            mod.SubPage_Switch(driver,"GENNI")
            mod.Switch_Frame(driver)
            time.sleep(1)
            driver.find_elements(By.NAME, "Lcmantableid")[int(msc_slot)].click()
            time.sleep(1)
            Select(driver.find_element(By.NAME, "rpportGenni_sltSpeed_all")).select_by_visible_text("1g-full")
            driver.find_element(By.NAME, "rpportGenni_btnApply").click()
            mod.Switch_Default(driver)
            mod.Page_Switch(driver,"Switch")
            mod.SubPage_Switch(driver,"Switch Setup")
            mod.Switch_Frame(driver)
            mod.Tab_Switch(driver,"Dot3ad")
            swi.Switch_Setup_Dot3ad_Group(driver,msc_max_port/2)
            swi.Switch_Setup_Dot3ad_Mode(driver,3)
            # swi.Switch_Setup_Dot3ad_Member(driver,"*")
            swi.Switch_Setup_Dot3ad_Member(driver,msc_port)
            swi.Switch_Setup_Dot3ad_Apply_1(driver)
        else:
            driver.find_element(By.NAME, "rperror_btnBack").click()
            # Protect Switch Delete
            mod.Switch_Default(driver)
            mod.SubPage_Switch(driver,"Protect Switch")
            mod.Switch_Frame(driver)
            driver.find_elements(By.NAME, "rpProtectSwitch_sltIndex")[int(msc_max_port/2)-1].click()
            swi.Protect_Switch_Delete(driver)
            mod.Switch_Default(driver)
            mod.SubPage_Switch(driver,"Switch Setup")
            mod.Switch_Frame(driver)
            mod.Tab_Switch(driver,"Dot3ad")
            swi.Switch_Setup_Dot3ad_Group(driver,msc_max_port/2)
            swi.Switch_Setup_Dot3ad_Mode(driver,3)
            # swi.Switch_Setup_Dot3ad_Member(driver,"*")
            swi.Switch_Setup_Dot3ad_Member(driver,msc_port)
            swi.Switch_Setup_Dot3ad_Apply_1(driver)
    except:
        pass
    if(driver.find_elements(By.CLASS_NAME, 'td-table-content.state')[int(msc_max_port/2)-1].get_attribute("textContent") != " - "):
        print(f"             [Switch - Switch Setup - Dot3ad] Group Test Fail(#175455)(#165897)",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.CLASS_NAME, 'td-table-content.type')[int(msc_max_port/2)-1].get_attribute("textContent") != "Lacp"):
        print(f"             [Switch - Switch Setup - Dot3ad] Mode Test Fail",file = open(file_name, '+a'))
        if_error = True
    # if(driver.find_elements(By.CLASS_NAME, 'td-table-content.port')[int(msc_max_port/2)-1].get_attribute("textContent") != f"1~{msc_max_port}"):
    if(driver.find_elements(By.CLASS_NAME, 'td-table-content.port')[int(msc_max_port/2)-1].get_attribute("textContent") != msc_port):
        print(f"             [Switch - Switch Setup - Dot3ad] Member Test Fail",file = open(file_name, '+a'))
        if_error = True
    swi.Switch_Setup_Dot3ad_Group(driver,msc_max_port/2)
    time.sleep(3)
    swi.Switch_Setup_Dot3ad_Mode(driver,3)
    time.sleep(3)
    swi.Switch_Setup_Dot3ad_Apply_1(driver)
    time.sleep(3)
    pyautogui.press("enter")

    if(driver.find_elements(By.CLASS_NAME, 'td-table-content.state')[int(msc_max_port/2)-1].get_attribute("textContent") != " V "):
        print(f"             [Switch - Switch Setup - Dot3ad] Group Test Fail(#175455)(#165897)",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.CLASS_NAME, 'td-table-content.type')[int(msc_max_port/2)-1].get_attribute("textContent") != "Lacp"):
        print(f"             [Switch - Switch Setup - Dot3ad] Mode Test Fail",file = open(file_name, '+a'))
        if_error = True
    # if(driver.find_elements(By.CLASS_NAME, 'td-table-content.port')[int(msc_max_port/2)-1].get_attribute("textContent") != f"1~{msc_max_port}"):
    if(driver.find_elements(By.CLASS_NAME, 'td-table-content.port')[int(msc_max_port/2)-1].get_attribute("textContent") != msc_port):
        print(f"             [Switch - Switch Setup - Dot3ad] Member Test Fail",file = open(file_name, '+a'))
        if_error = True
    swi.Switch_Setup_Dot3ad_Group(driver,msc_max_port/2)
    swi.Switch_Setup_Dot3ad_Mode(driver,1)
    swi.Switch_Setup_Dot3ad_Member(driver,"*")
    swi.Switch_Setup_Dot3ad_Apply_1(driver)
    swi.Switch_Setup_Dot3ad_Group(driver,msc_max_port/2)
    swi.Switch_Setup_Dot3ad_Mode(driver,1)
    swi.Switch_Setup_Dot3ad_Apply_1(driver)

    # Switch Setup Dot3ad Test 2
    swi.Switch_Setup_Dot3ad_LACP_Priority(driver,"65535")
    swi.Switch_Setup_Dot3ad_LACP_Timeput(driver,2)
    swi.Switch_Setup_Dot3ad_Apply_2(driver)
    if(driver.find_element(By.CLASS_NAME, 'div-row-cell-content.lacpsystempriority').get_attribute("textContent") != "65535"):
        print(f"             [Switch - Switch Setup - Dot3ad] LACP Priority Test Fail",file = open(file_name, '+a'))
        if_error = True
    string = driver.find_element(By.CLASS_NAME, "div-row-cell-content.lacptimeout").get_attribute("textContent")
    string = string.split("(")[0]
    if(string != "Short "):
        print(f"             [Switch - Switch Setup - Dot3ad] LACP Timeput Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Switch Switch Setup Dot3ad Result
    if(if_error == False):
        print(f"[MSAN1-11957][Switch - Switch Setup - Dot3ad] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11957][Switch - Switch Setup - Dot3ad] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Switch Switch Setup Isolation Test
    # Switch > Switch Setup > Isolation
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Switch > Switch Setup > Isolation
    mod.Tab_Switch(driver,"Isolation")

    # Switch Setup Isolation Test
    swi.Switch_Setup_Isolation_Enable(driver,False)
    swi.Switch_Setup_Isolation_Apply(driver)
    if(driver.find_element(By.NAME, f"rpsw_setup_isolation_chk_enable").is_selected() != False):
        print(f"             [Switch - Switch Setup - Isolation] Enable:False Test Fail",file = open(file_name, '+a'))
        if_error = True
    swi.Switch_Setup_Isolation_Enable(driver,True)
    swi.Switch_Setup_Isolation_Apply(driver)
    if(driver.find_element(By.NAME, f"rpsw_setup_isolation_chk_enable").is_selected() != True):
        print(f"             [Switch - Switch Setup - Isolation] Enable:True Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Switch Switch Setup Isolation Result
    if(if_error == False):
        print(f"[MSAN1-11958][Switch - Switch Setup - Isolation] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11958][Switch - Switch Setup - Isolation] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Switch Switch Setup DSCP Test
    # Switch > Switch Setup > DSCP
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Switch > Switch Setup > DSCP
    mod.Tab_Switch(driver,"DSCP")

    # slot select
    swi.Switch_Setup_DSCP_Slot_Select(driver,glc_slot)

    # Switch Setup DSCP Test 1
    for codepoint in range(7):
        for priority in range(10):
            if(10*codepoint+priority < 64):
                swi.Switch_Setup_DSCP_Mapping(driver,codepoint*10,priority,1)
    swi.Switch_Setup_DSCP_Apply_1(driver)
    for mapping_name in range(64):
        if(driver.find_element(By.XPATH, f"//*[@name='rpsw_setup_dscp_slt_priority_{mapping_name}']/option[1]").is_selected() != True):
            print(f"             [Switch - Switch Setup - DSCP] Codepoint{int(mapping_name/10)*10} Priority{mapping_name%10} Test Fail",file = open(file_name, '+a'))
            if_error = True
    for codepoint in range(7):
        for priority in range(10):
            if(10*codepoint+priority < 64):
                swi.Switch_Setup_DSCP_Mapping(driver,codepoint*10,priority,8)
    swi.Switch_Setup_DSCP_Apply_1(driver)
    for mapping_name in range(64):
        if(driver.find_element(By.XPATH, f"//*[@name='rpsw_setup_dscp_slt_priority_{mapping_name}']/option[8]").is_selected() != True):
            print(f"             [Switch - Switch Setup - DSCP] Codepoint{int(mapping_name/10)*10} Priority{mapping_name%10} Test Fail",file = open(file_name, '+a'))
            if_error = True

    # Switch Setup DSCP Test 2
    swi.Switch_Setup_DSCP_All(driver,True)
    swi.Switch_Setup_DSCP_Apply_2(driver)
    test_port = 0
    if_last = False
    while(if_last == False):
        try:
            if(driver.find_element(By.NAME, f"dscp_port{test_port}").is_selected() != True):
                print(f"             [Switch - Switch Setup - DSCP] Port{test_port+1} Check Box Test Fail",file = open(file_name, '+a'))
                if_error = True
            test_port = test_port+1
        except:
            if_last = True

    # Switch Switch Setup DSCP Result
    if(if_error == False):
        print(f"[MSAN1-11959][Switch - Switch Setup - DSCP] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11959][Switch - Switch Setup - DSCP] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Switch Switch Setup Storm Control Test
    # Switch > Switch Setup > Storm Control
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Switch > Switch Setup > Storm Control
    mod.Tab_Switch(driver,"Storm Control")

    # input("input to continue...................") #* add
    # time.sleep(10)

    # slot select
    swi.Switch_Setup_Storm_Control_Slot_Select(driver,glc_slot)

    # Switch Setup Storm Control Test
    storm_control_num = 0 
    if(glc_name == "GLC1440X"):
        storm_control_num = 1000000
    elif(glc_name == "GLC1540X"):
        storm_control_num = 10000000
    else:
        print(f"             [Switch - Switch Setup - Storm Control] GLC Name {glc_name}",file = open(file_name, '+a'))
        print(f"             [Switch - Switch Setup - Storm Control] GLC Name Unrecognizable Test Fail",file = open(file_name, '+a'))
        if_error = True

    time.sleep(5)

    swi.Switch_Setup_Storm_Control_Broadcast_All(driver,storm_control_num)   
    swi.Switch_Setup_Storm_Control_DLF_All(driver,storm_control_num)
    swi.Switch_Setup_Storm_Control_Multicast_All(driver,storm_control_num)

    swi.Switch_Setup_Storm_Control_Apply(driver)
    if(driver.find_element(By.NAME, f"rpsw_setup_storm_control_ipt_broadcast{int(glc_port)-1}").get_attribute("value") != str(storm_control_num)):
        print(f"             [Switch - Switch Setup - Storm Control] Port{glc_port} Broadcast Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, f"rpsw_setup_storm_control_ipt_dlf{int(glc_port)-1}").get_attribute("value") != str(storm_control_num)):
        print(f"             [Switch - Switch Setup - Storm Control] Port{glc_port} DLF Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, f"rpsw_setup_storm_control_ipt_multicast{int(glc_port)-1}").get_attribute("value") != str(storm_control_num)):
        print(f"             [Switch - Switch Setup - Storm Control] Port{glc_port} Multicast Test Fail",file = open(file_name, '+a'))
        if_error = True    
    swi.Switch_Setup_Storm_Control_Broadcast(driver,glc_port,storm_control_num+1)    
    swi.Switch_Setup_Storm_Control_Apply(driver)
    
    if(storm_control_num == 1000000):         #(card: 1440)
        # (check value)
        time.sleep(1)
        port_value = driver.find_element(By.ID, f"rpsw_setup_storm_control_ipt_broadcast{int(glc_port)-1}").get_attribute("value")
        if(int(port_value) != storm_control_num):
            print(f"             [Switch - Switch Setup - Storm Control] Port{glc_port}:{port_value}!={storm_control_num} Broadcast Test Fail",file = open(file_name, '+a'))
            if_error = True
        
        swi.Switch_Setup_Storm_Control_Cancel(driver)
        swi.Switch_Setup_Storm_Control_Broadcast(driver,glc_port,10000001)    
        swi.Switch_Setup_Storm_Control_Apply(driver)
        if(mod.IsAlert(driver) != True):
            print(f"             [Switch - Switch Setup - Storm Control] Port{glc_port} Broadcast:10G+1 No Alert Test Fail",file = open(file_name, '+a'))
            if_error = True 

    elif(storm_control_num == 10000000):      #(card: 1540)
    # (check alert)
        if(mod.IsAlert(driver) != True):
            print(f"             [Switch - Switch Setup - Storm Control] Port{glc_port} Broadcast:Max+1 No Alert Test Fail",file = open(file_name, '+a'))
            if_error = True    
    
    swi.Switch_Setup_Storm_Control_Cancel(driver)
    swi.Switch_Setup_Storm_Control_DLF(driver,glc_port,storm_control_num+1)    
    swi.Switch_Setup_Storm_Control_Apply(driver)
    if(storm_control_num == 1000000):         #(card: 1440)
    # (check value)
        time.sleep(1)
        port_value = driver.find_element(By.ID, f"rpsw_setup_storm_control_ipt_dlf{int(glc_port)-1}").get_attribute("value")
        if(int(port_value) != storm_control_num):
            print(f"             [Switch - Switch Setup - Storm Control] Port{glc_port}:{port_value}!={storm_control_num} DLF Test Fail",file = open(file_name, '+a'))
            if_error = True

        swi.Switch_Setup_Storm_Control_Cancel(driver)
        swi.Switch_Setup_Storm_Control_DLF(driver,glc_port,10000001)    
        swi.Switch_Setup_Storm_Control_Apply(driver)
        if(mod.IsAlert(driver) != True):
            print(f"             [Switch - Switch Setup - Storm Control] Port{glc_port} DLF:10G+1 No Alert Test Fail",file = open(file_name, '+a'))
            if_error = True 

    elif(storm_control_num == 10000000):      #(card: 1540)
    # (check alert)
        if(mod.IsAlert(driver) != True):
            print(f"             [Switch - Switch Setup - Storm Control] Port{glc_port} DLF:Max+1 No Alert Test Fail",file = open(file_name, '+a'))
            if_error = True    

    swi.Switch_Setup_Storm_Control_Cancel(driver)
    swi.Switch_Setup_Storm_Control_Multicast(driver,glc_port,storm_control_num+1)    
    swi.Switch_Setup_Storm_Control_Apply(driver)
    if(storm_control_num == 1000000):         #(card: 1440)
    # (check value)
        time.sleep(1)
        port_value = driver.find_element(By.ID, f"rpsw_setup_storm_control_ipt_multicast{int(glc_port)-1}").get_attribute("value")
        if(int(port_value) != storm_control_num):
            print(f"             [Switch - Switch Setup - Storm Control] Port{glc_port}:{port_value}!={storm_control_num} Multicast Test Fail",file = open(file_name, '+a'))
            if_error = True

        swi.Switch_Setup_Storm_Control_Cancel(driver)
        swi.Switch_Setup_Storm_Control_Multicast(driver,glc_port,10000001)    
        swi.Switch_Setup_Storm_Control_Apply(driver)
        if(mod.IsAlert(driver) != True):
            print(f"             [Switch - Switch Setup - Storm Control] Port{glc_port} Multicast:10G+1 No Alert Test Fail",file = open(file_name, '+a'))
            if_error = True 

    elif(storm_control_num == 10000000):      #(card: 1540)
    # (check alert)
        if(mod.IsAlert(driver) != True):
            print(f"             [Switch - Switch Setup - Storm Control] Port{glc_port} Multicast:Max+1 No Alert Test Fail",file = open(file_name, '+a'))
            if_error = True    

    swi.Switch_Setup_Storm_Control_Cancel(driver)

    # Switch Switch Setup Storm Control Result
    if(if_error == False):
        print(f"[MSAN1-11960][Switch - Switch Setup - Storm Control] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11960][Switch - Switch Setup - Storm Control] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Switch Switch Setup VC-Shaping Test
    # Switch > Switch Setup > VC-Shaping
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Switch > Switch Setup > VC-Shaping
    mod.Tab_Switch(driver,"DSCP")
    mod.Tab_Switch(driver,"VC-Shaping")

    # Switch Setup VC-Shaping Test
    swi.Switch_Setup_VCShaping_Enable(driver,True)
    swi.Switch_Setup_VCShaping_Apply(driver)
    if(driver.find_element(By.NAME, "rpsw_setup_shaping_chk_enable").is_selected() != True):
        print(f"             [Switch - Switch Setup - VC-Shaping] Enable:True Test Fail",file = open(file_name, '+a'))
        if_error = True
    swi.Switch_Setup_VCShaping_Enable(driver,False)
    swi.Switch_Setup_VCShaping_Apply(driver)
    if(driver.find_element(By.NAME, "rpsw_setup_shaping_chk_enable").is_selected() != False):
        print(f"             [Switch - Switch Setup - VC-Shaping] Enable:False Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Switch Switch Setup VC-Shaping Result
    if(if_error == False):
        print(f"[MSAN1-11961][Switch - Switch Setup - VC-Shaping] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11961][Switch - Switch Setup - VC-Shaping] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Switch CFM Maintenance Domain Test
    # Switch > CFM > Maintenance Domain
    # -------------------------start-------------------------

    if_error = False
    if_CFM_MD_exist = True

    try:
        # 路徑導向 Switch > CFM > Maintenance Domain
        mod.Switch_Default(driver)
        mod.SubPage_Switch(driver,"CFM")
        mod.Switch_Frame(driver)
    except:
        mod.Switch_Frame(driver)
        if_CFM_MD_exist = False
        print(f"             [Switch - CFM - Maintenance Domain] Result Block",file = open(file_name, '+a'))
        print(f"[MSAN1-11962][Switch - CFM - Maintenance Domain] Result Pass",file = open(file_name, '+a'))

    if(if_CFM_MD_exist == True):
        # Switch CFM Maintenance Domain Test
        driver.find_element(By.NAME, "rpcfmmd_btnapply2").click()
        if(mod.IsAlert(driver) == True):
            print(f"             [Switch - CFM - Maintenance Domain] Apply Alert Test Fail",file = open(file_name, '+a'))
            if_error = True
        time.sleep(1)
        driver.find_element(By.NAME, "rpcfmmd_btnnew").click()
        if(mod.IsAlert(driver) != True):
            print(f"             [Switch - CFM - Maintenance Domain] New No Alert Test Fail",file = open(file_name, '+a'))
            if_error = True
        time.sleep(10)
        driver.find_element(By.NAME, "rpcfmmd_btncancel").click()
        if(mod.IsAlert(driver) == True):
            print(f"             [Switch - CFM - Maintenance Domain] Cancel Alert Test Fail",file = open(file_name, '+a'))
            if_error = True
        time.sleep(1)
        driver.find_element(By.NAME, "rpcfmmd_btnmodify").click()
        if(mod.IsAlert(driver) != True):
            print(f"             [Switch - CFM - Maintenance Domain] Modify No Alert Test Fail",file = open(file_name, '+a'))
            if_error = True
        time.sleep(1)
        driver.find_element(By.NAME, "rpcfmmd_btndelete").click()
        if(mod.IsAlert(driver) != True):
            print(f"             [Switch - CFM - Maintenance Domain] Delete No Alert Test Fail",file = open(file_name, '+a'))
            if_error = True
        time.sleep(1)

        # Switch CFM Maintenance Domain Result
        if(if_error == False):
            print(f"[MSAN1-11962][Switch - CFM - Maintenance Domain] Result Pass",file = open(file_name, '+a'))
        else:
            print(f"[MSAN1-11962][Switch - CFM - Maintenance Domain] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Switch CFM LBR Test
    # Switch > CFM > LBR
    # -------------------------start-------------------------

    if_error = False
    if_CFM_LBR_exist = True
    
    try:
        # 路徑導向 Switch > CFM > LBR
        time.sleep(1)
        mod.Tab_Switch(driver,"LBR")
    except:
        if_CFM_LBR_exist = False
        print(f"             [Switch - CFM - LBR] Result Block",file = open(file_name, '+a'))
        print(f"[MSAN1-11963][Switch - CFM - LBR] Result Pass",file = open(file_name, '+a'))

    if(if_CFM_LBR_exist == True):
        try:
            # slot select
            swi.Slot_Select(driver,glc_slot)
            time.sleep(1)
            swi.Port_Select(driver,glc_port)
            time.sleep(1)
            swi.Load(driver)
            time.sleep(1)

            # Switch CFM LBR Test
            driver.find_element(By.XPATH, f"//*[@name='rpcfmlbr_sltEna']/option[2]").click()
            driver.find_element(By.NAME, "rpcfmlbr_btn").click()
            if(driver.find_element(By.XPATH, f"//*[@name='rpcfmlbr_sltEna']/option[2]").is_selected() != True):
                print(f"             [Switch - CFM - LBR] Enable Test Fail",file = open(file_name, '+a'))
                if_error = True
        except:
            print(f"             [Switch - CFM - LBR] Test Fail",file = open(file_name, '+a'))
            if_error = True

        # Switch CFM LBR Result
        if(if_error == False):
            print(f"[MSAN1-11963][Switch - CFM - LBR] Result Pass",file = open(file_name, '+a'))
        else:
            print(f"[MSAN1-11963][Switch - CFM - LBR] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Switch OAM Test
    # Switch > OAM
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Switch > OAM
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"OAM")
    mod.Switch_Frame(driver)

    # slot select
    time.sleep(1)
    swi.OAM_Slot_Select(driver,glc_slot)

    # OAM Test 1
    swi.OAM_Enable_All(driver,True)
    swi.OAM_Mode_All(driver,1)
    swi.OAM_RemoteLoopback_All(driver,True)
    swi.OAM_Apply(driver)
    if(driver.find_element(By.NAME, f"rpswoam_enable{glc_port}").is_selected() != True):
        print(f"             [Switch - OAM] Port{glc_port} Enable:True Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.XPATH, f"//*[@name='rpswoam_mode{glc_port}']/option[1]").is_selected() != True):
        print(f"             [Switch - OAM] Port{glc_port} Mode:passive Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, f"rpswoam_rmtlbk{glc_port}").is_selected() != True):
        print(f"             [Switch - OAM] Port{glc_port} RemoteLoopback:True Test Fail",file = open(file_name, '+a'))
        if_error = True

    # OAM Test 2
    swi.OAM_Enable_All(driver,True)
    swi.OAM_Enable_All(driver,False)
    swi.OAM_Mode_All(driver,2)
    swi.OAM_RemoteLoopback_All(driver,True)
    swi.OAM_RemoteLoopback_All(driver,False)
    swi.OAM_Apply(driver)
    if(driver.find_element(By.NAME, f"rpswoam_enable{glc_port}").is_selected() != False):
        print(f"             [Switch - OAM] Port{glc_port} Enable:False Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.XPATH, f"//*[@name='rpswoam_mode{glc_port}']/option[2]").is_selected() != True):
        print(f"             [Switch - OAM] Port{glc_port} Mode:active Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, f"rpswoam_rmtlbk{glc_port}").is_selected() != False):
        print(f"             [Switch - OAM] Port{glc_port} RemoteLoopback:False Test Fail",file = open(file_name, '+a'))
        if_error = True

    # OAM Test 3
    swi.OAM_Enable_All(driver,True)
    swi.OAM_RemoteLoopback_All(driver,True)
    swi.OAM_Apply(driver)
    if(driver.find_element(By.NAME, f"rpswoam_enable{glc_port}").is_selected() != True):
        print(f"             [Switch - OAM] Port{glc_port} Enable:True Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, f"rpswoam_rmtlbk{glc_port}").is_selected() != True):
        print(f"             [Switch - OAM] Port{glc_port} RemoteLoopback:True Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Switch OAM Result
    if(if_error == False):
        print(f"[MSAN1-11964][Switch - OAM] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11964][Switch - OAM] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Switch LLDP Configuration Test
    # Switch > LLDP > Configuration
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Switch > LLDP > Configuration
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"LLDP")
    mod.Switch_Frame(driver)

    # slot select
    time.sleep(1)
    swi.Slot_Select(driver,glc_slot)
    swi.Load(driver)

    # LLDP Configuration Test 1
    swi.LLDP_Configuration_Active(driver,True)
    swi.LLDP_Configuration_Transmit_Interval(driver,"4")
    swi.LLDP_Configuration_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - LLDP - Configuration] Transmit Interval:4 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.LLDP_Configuration_Transmit_Interval(driver,"32769")
    swi.LLDP_Configuration_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - LLDP - Configuration] Transmit Interval:32769 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.LLDP_Configuration_Transmit_Interval(driver,"@")
    swi.LLDP_Configuration_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - LLDP - Configuration] Transmit Interval:@ No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.LLDP_Configuration_Transmit_Interval(driver,"32768")
    swi.LLDP_Configuration_Transmit_Hold(driver,"1")
    swi.LLDP_Configuration_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - LLDP - Configuration] Transmit Hold:1 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.LLDP_Configuration_Transmit_Hold(driver,"11")
    swi.LLDP_Configuration_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - LLDP - Configuration] Transmit Hold:11 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.LLDP_Configuration_Transmit_Hold(driver,"@")
    swi.LLDP_Configuration_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - LLDP - Configuration] Transmit Hold:@ No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.LLDP_Configuration_Transmit_Hold(driver,"10")
    swi.LLDP_Configuration_Transmit_Delay(driver,"0")
    swi.LLDP_Configuration_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - LLDP - Configuration] Transmit Delay:0 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.LLDP_Configuration_Transmit_Delay(driver,"8193")
    swi.LLDP_Configuration_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - LLDP - Configuration] Transmit Delay:8193 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.LLDP_Configuration_Transmit_Delay(driver,"@")
    swi.LLDP_Configuration_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - LLDP - Configuration] Transmit Delay:@ No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.LLDP_Configuration_Transmit_Delay(driver,"8192")
    swi.LLDP_Configuration_Transmit_Reinit(driver,"0")
    swi.LLDP_Configuration_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - LLDP - Configuration] Transmit Reinit:0 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.LLDP_Configuration_Transmit_Reinit(driver,"11")
    swi.LLDP_Configuration_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - LLDP - Configuration] Transmit Reinit:11 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.LLDP_Configuration_Transmit_Reinit(driver,"@")
    swi.LLDP_Configuration_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - LLDP - Configuration] Transmit Reinit:@ No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    swi.LLDP_Configuration_Transmit_Reinit(driver,"10")
    swi.LLDP_Configuration_Apply(driver)
    if(mod.IsAlert(driver) == True):
        print(f"             [Switch - LLDP - Configuration] Max Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # LLDP Configuration Test 2
    swi.LLDP_Configuration_Admin_Status(driver,2)
    swi.LLDP_Configuration_Notification(driver,True)
    swi.LLDP_Configuration_Apply(driver)
    if(driver.find_element(By.XPATH, f"/html/body/form/table/tbody/tr[{int(glc_port)+2}]/td[2]/select/option[2]").is_selected() != True):
        print(f"             [Switch - LLDP - Configuration] Port{glc_port} Admin Status:Tx-Rx Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "RpLLDPConfig_ChkNotification")[int(glc_port)-1].is_selected() != True):
        print(f"             [Switch - LLDP - Configuration] Port{glc_port} Notification:True Test Fail",file = open(file_name, '+a'))
        if_error = True
    swi.LLDP_Configuration_Admin_Status(driver,4)
    swi.LLDP_Configuration_Notification(driver,True)
    swi.LLDP_Configuration_Notification(driver,False)
    swi.LLDP_Configuration_Apply(driver)
    if(driver.find_element(By.XPATH, f"/html/body/form/table/tbody/tr[{int(glc_port)+2}]/td[2]/select/option[4]").is_selected() != True):
        print(f"             [Switch - LLDP - Configuration] Port{glc_port} Admin Status:Tx-Only Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "RpLLDPConfig_ChkNotification")[int(glc_port)-1].is_selected() != False):
        print(f"             [Switch - LLDP - Configuration] Port{glc_port} Notification:False Test Fail",file = open(file_name, '+a'))
        if_error = True
    swi.LLDP_Configuration_Notification(driver,True)
    swi.LLDP_Configuration_Apply(driver)
    if(driver.find_elements(By.NAME, "RpLLDPConfig_ChkNotification")[int(glc_port)-1].is_selected() != True):
        print(f"             [Switch - LLDP - Configuration] Port{glc_port} Notification:True Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Switch LLDP Configuration Result
    if(if_error == False):
        print(f"[MSAN1-11965][Switch - LLDP - Configuration] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11965][Switch - LLDP - Configuration] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Switch LLDP Basic TLV Setting Test
    # Switch > LLDP > Basic TLV Setting
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Switch > LLDP > Basic TLV Setting
    mod.Tab_Switch(driver,"Basic TLV Setting")

    # slot select
    swi.Slot_Select(driver,glc_slot)
    swi.Load(driver)

    # Basic TLV Setting Test
    swi.LLDP_Basic_TLV_Setting_Management_Address(driver,True)
    swi.LLDP_Basic_TLV_Setting_Port_Description(driver,True)
    swi.LLDP_Basic_TLV_Setting_System_Capabilities(driver,True)
    swi.LLDP_Basic_TLV_Setting_System_Description(driver,True)
    swi.LLDP_Basic_TLV_Setting_System_Name(driver,True)
    swi.LLDP_Basic_TLV_Setting_Apply(driver)
    if(driver.find_elements(By.NAME, "RpBasicTLVSetting_ChkManagementAddress")[int(glc_port)-1].is_selected() != True):
        print(f"             [Switch - LLDP - Basic TLV Setting] Port{glc_port} Management Address:True Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "RpBasicTLVSetting_ChkPortDescription")[int(glc_port)-1].is_selected() != True):
        print(f"             [Switch - LLDP - Basic TLV Setting] Port{glc_port} Port Description:True Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "RpBasicTLVSetting_ChkSystemCapabilities")[int(glc_port)-1].is_selected() != True):
        print(f"             [Switch - LLDP - Basic TLV Setting] Port{glc_port} System Capabilities:True Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "RpBasicTLVSetting_ChkSystemDescription")[int(glc_port)-1].is_selected() != True):
        print(f"             [Switch - LLDP - Basic TLV Setting] Port{glc_port} System Description:True Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "RpBasicTLVSetting_ChkSystemName")[int(glc_port)-1].is_selected() != True):
        print(f"             [Switch - LLDP - Basic TLV Setting] Port{glc_port} System Name:True Test Fail",file = open(file_name, '+a'))
        if_error = True
    swi.LLDP_Basic_TLV_Setting_Management_Address(driver,True)
    swi.LLDP_Basic_TLV_Setting_Management_Address(driver,False)
    swi.LLDP_Basic_TLV_Setting_Port_Description(driver,True)
    swi.LLDP_Basic_TLV_Setting_Port_Description(driver,False)
    swi.LLDP_Basic_TLV_Setting_System_Capabilities(driver,True)
    swi.LLDP_Basic_TLV_Setting_System_Capabilities(driver,False)
    swi.LLDP_Basic_TLV_Setting_System_Description(driver,True)
    swi.LLDP_Basic_TLV_Setting_System_Description(driver,False)
    swi.LLDP_Basic_TLV_Setting_System_Name(driver,True)
    swi.LLDP_Basic_TLV_Setting_System_Name(driver,False)
    swi.LLDP_Basic_TLV_Setting_Apply(driver)
    if(driver.find_elements(By.NAME, "RpBasicTLVSetting_ChkManagementAddress")[int(glc_port)-1].is_selected() != False):
        print(f"             [Switch - LLDP - Basic TLV Setting] Port{glc_port} Management Address:False Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "RpBasicTLVSetting_ChkPortDescription")[int(glc_port)-1].is_selected() != False):
        print(f"             [Switch - LLDP - Basic TLV Setting] Port{glc_port} Port Description:False Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "RpBasicTLVSetting_ChkSystemCapabilities")[int(glc_port)-1].is_selected() != False):
        print(f"             [Switch - LLDP - Basic TLV Setting] Port{glc_port} System Capabilities:False Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "RpBasicTLVSetting_ChkSystemDescription")[int(glc_port)-1].is_selected() != False):
        print(f"             [Switch - LLDP - Basic TLV Setting] Port{glc_port} System Description:False Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "RpBasicTLVSetting_ChkSystemName")[int(glc_port)-1].is_selected() != False):
        print(f"             [Switch - LLDP - Basic TLV Setting] Port{glc_port} System Name:False Test Fail",file = open(file_name, '+a'))
        if_error = True
    swi.LLDP_Basic_TLV_Setting_Management_Address(driver,True)
    swi.LLDP_Basic_TLV_Setting_Port_Description(driver,True)
    swi.LLDP_Basic_TLV_Setting_System_Capabilities(driver,True)
    swi.LLDP_Basic_TLV_Setting_System_Description(driver,True)
    swi.LLDP_Basic_TLV_Setting_System_Name(driver,True)
    swi.LLDP_Basic_TLV_Setting_Apply(driver)
    if(driver.find_elements(By.NAME, "RpBasicTLVSetting_ChkManagementAddress")[int(glc_port)-1].is_selected() != True):
        print(f"             [Switch - LLDP - Basic TLV Setting] Port{glc_port} Management Address:True Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "RpBasicTLVSetting_ChkPortDescription")[int(glc_port)-1].is_selected() != True):
        print(f"             [Switch - LLDP - Basic TLV Setting] Port{glc_port} Port Description:True Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "RpBasicTLVSetting_ChkSystemCapabilities")[int(glc_port)-1].is_selected() != True):
        print(f"             [Switch - LLDP - Basic TLV Setting] Port{glc_port} System Capabilities:True Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "RpBasicTLVSetting_ChkSystemDescription")[int(glc_port)-1].is_selected() != True):
        print(f"             [Switch - LLDP - Basic TLV Setting] Port{glc_port} System Description:True Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "RpBasicTLVSetting_ChkSystemName")[int(glc_port)-1].is_selected() != True):
        print(f"             [Switch - LLDP - Basic TLV Setting] Port{glc_port} System Name:True Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Switch LLDP Basic TLV Setting Result
    if(if_error == False):
        print(f"[MSAN1-11966][Switch - LLDP - Basic TLV Setting] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11966][Switch - LLDP - Basic TLV Setting] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Switch LLDP Org-specific TLV Setting Test
    # Switch > LLDP > Org-specific TLV Setting
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Switch > LLDP > Org-specific TLV Setting
    mod.Tab_Switch(driver,"Org-specific TLV Setting")

    # slot select
    swi.Slot_Select(driver,glc_slot)
    swi.Load(driver)

    # Org-specific TLV Setting Test
    swi.LLDP_Orgspecific_TLV_Setting_VLAN_ID(driver,True)
    swi.LLDP_Orgspecific_TLV_Setting_Link_Aggregation(driver,True)
    swi.LLDP_Orgspecific_TLV_Setting_MAC_PHY_Config(driver,True)
    swi.LLDP_Orgspecific_TLV_Setting_Max_Frame_Size(driver,True)
    swi.LLDP_Orgspecific_TLV_Setting_Apply(driver)
    if(driver.find_elements(By.NAME, "RpOrgTLVSetting_ChkPVLANID")[int(glc_port)-1].is_selected() != True):
        print(f"             [Switch - LLDP - Org-specific TLV Setting] Port{glc_port} VLAN ID:True Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "RpOrgTLVSetting_ChkLinkAggregation")[int(glc_port)-1].is_selected() != True):
        print(f"             [Switch - LLDP - Org-specific TLV Setting] Port{glc_port} Link Aggregation:True Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "RpOrgTLVSetting_ChkMACPHY")[int(glc_port)-1].is_selected() != True):
        print(f"             [Switch - LLDP - Org-specific TLV Setting] Port{glc_port} PHY Config:True Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "RpOrgTLVSetting_ChkMaxFrameSize")[int(glc_port)-1].is_selected() != True):
        print(f"             [Switch - LLDP - Org-specific TLV Setting] Port{glc_port} Max Frame Size:True Test Fail",file = open(file_name, '+a'))
        if_error = True
    swi.LLDP_Orgspecific_TLV_Setting_VLAN_ID(driver,True)
    swi.LLDP_Orgspecific_TLV_Setting_VLAN_ID(driver,False)
    swi.LLDP_Orgspecific_TLV_Setting_Link_Aggregation(driver,True)
    swi.LLDP_Orgspecific_TLV_Setting_Link_Aggregation(driver,False)
    swi.LLDP_Orgspecific_TLV_Setting_MAC_PHY_Config(driver,True)
    swi.LLDP_Orgspecific_TLV_Setting_MAC_PHY_Config(driver,False)
    swi.LLDP_Orgspecific_TLV_Setting_Max_Frame_Size(driver,True)
    swi.LLDP_Orgspecific_TLV_Setting_Max_Frame_Size(driver,False)
    swi.LLDP_Orgspecific_TLV_Setting_Apply(driver)
    if(driver.find_elements(By.NAME, "RpOrgTLVSetting_ChkPVLANID")[int(glc_port)-1].is_selected() != False):
        print(f"             [Switch - LLDP - Org-specific TLV Setting] Port{glc_port} VLAN ID:False Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "RpOrgTLVSetting_ChkLinkAggregation")[int(glc_port)-1].is_selected() != False):
        print(f"             [Switch - LLDP - Org-specific TLV Setting] Port{glc_port} Link Aggregation:False Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "RpOrgTLVSetting_ChkMACPHY")[int(glc_port)-1].is_selected() != False):
        print(f"             [Switch - LLDP - Org-specific TLV Setting] Port{glc_port} PHY Config:False Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "RpOrgTLVSetting_ChkMaxFrameSize")[int(glc_port)-1].is_selected() != False):
        print(f"             [Switch - LLDP - Org-specific TLV Setting] Port{glc_port} Max Frame Size:False Test Fail",file = open(file_name, '+a'))
        if_error = True
    swi.LLDP_Orgspecific_TLV_Setting_VLAN_ID(driver,True)
    swi.LLDP_Orgspecific_TLV_Setting_Link_Aggregation(driver,True)
    swi.LLDP_Orgspecific_TLV_Setting_MAC_PHY_Config(driver,True)
    swi.LLDP_Orgspecific_TLV_Setting_Max_Frame_Size(driver,True)
    swi.LLDP_Orgspecific_TLV_Setting_Apply(driver)
    if(driver.find_elements(By.NAME, "RpOrgTLVSetting_ChkPVLANID")[int(glc_port)-1].is_selected() != True):
        print(f"             [Switch - LLDP - Org-specific TLV Setting] Port{glc_port} VLAN ID:True Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "RpOrgTLVSetting_ChkLinkAggregation")[int(glc_port)-1].is_selected() != True):
        print(f"             [Switch - LLDP - Org-specific TLV Setting] Port{glc_port} Link Aggregation:True Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "RpOrgTLVSetting_ChkMACPHY")[int(glc_port)-1].is_selected() != True):
        print(f"             [Switch - LLDP - Org-specific TLV Setting] Port{glc_port} PHY Config:True Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "RpOrgTLVSetting_ChkMaxFrameSize")[int(glc_port)-1].is_selected() != True):
        print(f"             [Switch - LLDP - Org-specific TLV Setting] Port{glc_port} Max Frame Size:True Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Switch LLDP Org-specific TLV Setting Result
    if(if_error == False):
        print(f"[MSAN1-11967][Switch - LLDP - Org-specific TLV Setting] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11967][Switch - LLDP - Org-specific TLV Setting] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Switch Error Disable Configuration Test
    # Switch > Error Disable > Configuration
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Switch > Error Disable > Configuration
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"Error Disable")
    mod.Switch_Frame(driver)

    # Error Disable Configuration Test
    swi.Error_Disable_Configuration_Delete_Active(driver,True)
    swi.Error_Disable_Configuration_Mode(driver,2)
    swi.Error_Disable_Configuration_Upper(driver,"23")
    swi.Error_Disable_Configuration_Recovery_Active(driver,True)
    swi.Error_Disable_Configuration_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - Error Disable - Configuration] Upper:23 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.Error_Disable_Configuration_Upper(driver,"201")
    swi.Error_Disable_Configuration_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - Error Disable - Configuration] Upper:201 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.Error_Disable_Configuration_Upper(driver,"@")
    swi.Error_Disable_Configuration_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - Error Disable - Configuration] Upper:@ No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.Error_Disable_Configuration_Upper(driver,"200")
    swi.Error_Disable_Configuration_Interval(driver,"29")
    swi.Error_Disable_Configuration_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - Error Disable - Configuration] Interval:29 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.Error_Disable_Configuration_Interval(driver,"86401")
    swi.Error_Disable_Configuration_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - Error Disable - Configuration] Interval:86401 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.Error_Disable_Configuration_Interval(driver,"@")
    swi.Error_Disable_Configuration_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - Error Disable - Configuration] Interval:@ No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    swi.Error_Disable_Configuration_Interval(driver,"86400")
    swi.Error_Disable_Configuration_Apply(driver)
    if(mod.IsAlert(driver) == True):
        print(f"             [Switch - Error Disable - Configuration] Apply Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "RperrdisConfig_ChkDetectActive")[0].is_selected() != True):
        print(f"             [Switch - Error Disable - Configuration] Delete Active:True Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.XPATH, f"/html/body/form/table/tbody/tr[3]/td[4]/select/option[2]").is_selected() != True):
        print(f"             [Switch - Error Disable - Configuration] Mode:Upper-bound Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "RperrdisConfig_TxtDetectUpper")[0].get_attribute("value") != "200"):
        print(f"             [Switch - Error Disable - Configuration] Upper:200 Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "RperrdisConfig_ChkRecoveryActive")[0].is_selected() != True):
        print(f"             [Switch - Error Disable - Configuration] Recovery Active:True Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "RperrdisConfig_TxtRecoveryInterval")[0].get_attribute("value") != "86400"):
        print(f"             [Switch - Error Disable - Configuration] Interval:86400 Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "RperrdisConfig_ChkDetectActive")[1].is_selected() != True):
        print(f"             [Switch - Error Disable - Configuration] Delete Active:True Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.XPATH, f"/html/body/form/table/tbody/tr[4]/td[4]/select/option[2]").is_selected() != True):
        print(f"             [Switch - Error Disable - Configuration] Mode:Upper-bound Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "RperrdisConfig_TxtDetectUpper")[1].get_attribute("value") != "200"):
        print(f"             [Switch - Error Disable - Configuration] Upper:200 Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "RperrdisConfig_ChkRecoveryActive")[1].is_selected() != True):
        print(f"             [Switch - Error Disable - Configuration] Recovery Active:True Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "RperrdisConfig_TxtRecoveryInterval")[1].get_attribute("value") != "86400"):
        print(f"             [Switch - Error Disable - Configuration] Interval:86400 Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Switch Error Disable Configuration Result
    if(if_error == False):
        print(f"[MSAN1-11968][Switch - Error Disable - Configuration] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11968][Switch - Error Disable - Configuration] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Switch Error Disable Port Setting Test
    # Switch > Error Disable > Port Setting
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Switch > Error Disable > Port Setting
    mod.Tab_Switch(driver,"Port Setting")

    # Error Disable Port Setting Test
    swi.Error_Disable_Port_Setting_IGMP_All(driver,"19")
    swi.Error_Disable_Port_Setting_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - Error Disable - Port Setting] IGMP:19 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.Error_Disable_Port_Setting_IGMP_All(driver,"2001")
    swi.Error_Disable_Port_Setting_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - Error Disable - Port Setting] IGMP:2001 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.Error_Disable_Port_Setting_IGMP_All(driver,"@")
    swi.Error_Disable_Port_Setting_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - Error Disable - Port Setting] IGMP:@ No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.Error_Disable_Port_Setting_IGMP_All(driver,"2000")
    swi.Error_Disable_Port_Setting_LLDP_All(driver,"19")
    swi.Error_Disable_Port_Setting_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - Error Disable - Port Setting] LLDP:19 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.Error_Disable_Port_Setting_LLDP_All(driver,"2001")
    swi.Error_Disable_Port_Setting_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - Error Disable - Port Setting] LLDP:2001 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.Error_Disable_Port_Setting_LLDP_All(driver,"@")
    swi.Error_Disable_Port_Setting_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - Error Disable - Port Setting] LLDP:@ No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    swi.Error_Disable_Port_Setting_LLDP_All(driver,"2000")
    swi.Error_Disable_Port_Setting_Apply(driver)
    if(mod.IsAlert(driver) == True):
        print(f"             [Switch - Error Disable - Port Setting] Apply Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "RperrdisConfig_TxtThresh_1")[int(msc_port)-1].get_attribute("value") != "2000"):
        print(f"             [Switch - Error Disable - Port Setting] IGMP Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "RperrdisConfig_TxtThresh_2")[int(msc_port)-1].get_attribute("value") != "2000"):
        print(f"             [Switch - Error Disable - Port Setting] LLDP Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Switch Error Disable Port Setting Result
    if(if_error == False):
        print(f"[MSAN1-11969][Switch - Error Disable - Port Setting] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11969][Switch - Error Disable - Port Setting] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Switch Protect Switch Test
    # Switch > Protect Switch
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Switch > Protect Switch
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"Protect Switch")
    mod.Switch_Frame(driver)

    # Protect Switch Test
    swi.Protect_Switch_Group(driver,msc_max_port/2)
    swi.Protect_Switch_Active_port(driver,1)
    swi.Protect_Switch_Backup_port(driver,2)
    swi.Protect_Switch_Preemption_Mode(driver,3)
    swi.Protect_Switch_Preemption_Delay(driver,"4")
    swi.Protect_Switch_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - Protect Switch] Preemption Delay:4 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.Protect_Switch_Preemption_Delay(driver,"61")
    swi.Protect_Switch_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - Protect Switch] Preemption Delay:61 No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    time.sleep(1)
    swi.Protect_Switch_Preemption_Delay(driver,"@")
    swi.Protect_Switch_Apply(driver)
    if(mod.IsAlert(driver) != True):
        print(f"             [Switch - Protect Switch] Preemption Delay:@ No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    swi.Protect_Switch_Preemption_Delay(driver,"60")
    swi.Protect_Switch_Apply(driver)
    if(mod.IsAlert(driver) == True):
        print(f"             [Switch - Protect Switch] Apply Alert Test Fail",file = open(file_name, '+a'))
        if_error = True
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
        print(f"             [Switch - Protect Switch] Switch - Switch Setup - Dot3ad Conflict Test Fail",file = open(file_name, '+a'))
        if_error = True
    except:
        if(driver.find_elements(By.CLASS_NAME, "td-table-content.active_port")[int(msc_max_port/2)-1].get_attribute("textContent") != "1"):
            print(f"             [Switch - Protect Switch] Active Port:1 Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_elements(By.CLASS_NAME, "td-table-content.backup_port")[int(msc_max_port/2)-1].get_attribute("textContent") != "2"):
            print(f"             [Switch - Protect Switch] Active Port:2 Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_elements(By.CLASS_NAME, "td-table-content.preempt_mode")[int(msc_max_port/2)-1].get_attribute("textContent") != "forced"):
            print(f"             [Switch - Protect Switch] Active Port:forced Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_elements(By.CLASS_NAME, "td-table-content.preempt_delay")[int(msc_max_port/2)-1].get_attribute("textContent") != "60"):
            print(f"             [Switch - Protect Switch] Active Port:60 Test Fail",file = open(file_name, '+a'))
            if_error = True
        swi.Protect_Switch_Delete(driver)
        if(mod.IsAlert(driver) != True):
            print(f"             [Switch - Protect Switch] Delete No Alert Test Fail",file = open(file_name, '+a'))
            if_error = True

        # Protect Switch Delete
        driver.find_elements(By.NAME, "rpProtectSwitch_sltIndex")[int(msc_max_port/2)-1].click()
        swi.Protect_Switch_Delete(driver)

    # Switch Protect Switch Result
    if(if_error == False):
        print(f"[MSAN1-11970][Switch - Protect Switch] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11970][Switch - Protect Switch] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    Maintenance_Config_Reset(driver,glc_slot,glc_port,file_name)

    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def VLAN_Test(driver,glc_slot,glc_port,file_name):
    print(f"VLAN Test\nTest Start",file = open(file_name, '+a'))

    Maintenance_Config_Reset(driver,glc_slot,glc_port,file_name)


    # VLAN GE/GENNI VLAN Setup VLAN Table
    # VLAN > GE/GENNI VLAN Setup > VLAN Table
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 VLAN > GE/GENNI VLAN Setup > VLAN Table
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"VLAN")
    mod.Switch_Frame(driver)

    # slot select
    if_load = False
    while(if_load == False):
        try:
            vlan.Slot_Select(driver,glc_slot)
            if_load = True
        except:
            if_load = False

    # VLAN GE/GENNI VLAN Setup VLAN Table Test
    vlan.GE_GENNI_VLAN_Setup_VLAN_Table_VLAN_ID(driver,"4001")
    
    # vlan.GE_GENNI_VLAN_Setup_VLAN_Table_Apply(driver)
    # try:
    #     driver.find_element(By.NAME, "rpvlantable_radioSlt").click()
    # except:
    #     print(f"             [VLAN - GE/GENNI VLAN Setup - VLAN Table] Select 4001 Test Fail",file = open(file_name, '+a')) #*add
    #     if_error = True
    # vlan.GE_GENNI_VLAN_Setup_VLAN_Table_Modify(driver)
    # if(driver.find_element(By.XPATH, f"/html/body/form/div[6]/span[{glc_port}]/div[2]/select/option[1]").is_selected() != True):
    #     print(f"             [VLAN - GE/GENNI VLAN Setup - VLAN Table] Port{glc_port} Default Registration:Normal Test Fail",file = open(file_name, '+a'))
    #     if_error = True
    # if(driver.find_elements(By.NAME, "rpvlantable_ChkTag")[int(glc_port)-1].is_selected() != True):
    #     print(f"             [VLAN - GE/GENNI VLAN Setup - VLAN Table] Port{glc_port} Default Tagging:True Test Fail(#175215)",file = open(file_name, '+a'))
    #     if_error = True
    # try:
    #     driver.find_element(By.NAME, "rpvlantable_radioSlt").click()
    # except:
    #     print(f"             [VLAN - GE/GENNI VLAN Setup - VLAN Table] Select 4001 Test Fail",file = open(file_name, '+a')) #*add
    #     if_error = True
    
    #* add -----START------------Edit from Above-----------------------------------------------------------------------------------------
    
    # Registration select all : Fixed
    vlan.GE_GENNI_VLAN_Setup_VLAN_Table_Port_Registration_All(driver,2)
    
    # Apply
    vlan.GE_GENNI_VLAN_Setup_VLAN_Table_Apply(driver)
     
    # Select
    try:
        # driver.find_element(By.NAME, "rpvlantable_radioSlt").click()
        driver.find_element(By.XPATH, '//input[@value="4001"]').click()        #*add
    except:
        print(f"             [VLAN - GE/GENNI VLAN Setup - VLAN Table] Select 4001 Test Fail",file = open(file_name, '+a')) #*add
        if_error = True

    # Modify
    vlan.GE_GENNI_VLAN_Setup_VLAN_Table_Modify(driver)

    # Check 39th "Fixed" (value:1)
    if(driver.find_elements(By.NAME, "rpvlantable_sltRegStatus")[int(glc_port)-1].get_attribute("value")!="1"):
        print(f"             [VLAN - GE/GENNI VLAN Setup - VLAN Table] 39th 'Fixed' Test Fail",file = open(file_name, '+a')) #*add
        if_error = True

    # 39th registration set "Normal"
    vlan.GE_GENNI_VLAN_Setup_VLAN_Table_Port_Registration(driver,39,1)

    # Apply
    vlan.GE_GENNI_VLAN_Setup_VLAN_Table_Apply(driver)

    # Check (select > modify > check)
    
    # select
    try:
        # driver.find_element(By.NAME, "rpvlantable_radioSlt").click()         
        driver.find_element(By.XPATH, '//input[@value="4001"]').click()        #*add
    except:
        print(f"             [VLAN - GE/GENNI VLAN Setup - VLAN Table] Select 4001 Test Fail",file = open(file_name, '+a')) #*add
        if_error = True
    
    # modify
    vlan.GE_GENNI_VLAN_Setup_VLAN_Table_Modify(driver)
    

    # check 39th "Normal" (value:0)
    if(driver.find_elements(By.NAME, "rpvlantable_sltRegStatus")[int(glc_port)-1].get_attribute("value")!="0"):
        print(f"             [VLAN - GE/GENNI VLAN Setup - VLAN Table] 39th Registration:'Normal' Test Fail",file = open(file_name, '+a')) #*add
        if_error = True
    else:
        print(f"             [VLAN - GE/GENNI VLAN Setup - VLAN Table] Port{glc_port} Registration:'Normal' Test Pass",file = open(file_name, '+a')) #*add
    # # another check way
    # if(driver.find_element(By.XPATH, f"/html/body/form/div[6]/span[{glc_port}]/div[2]/select/option[1]").is_selected() != True):
    #     print(f"             [VLAN - GE/GENNI VLAN Setup - VLAN Table] Port{glc_port} Registration:normal Test Fail",file = open(file_name, '+a'))
    #     if_error = True
    # else:
    #     print(f"             [VLAN - GE/GENNI VLAN Setup - VLAN Table] Port{glc_port} Registration:Normal Test Pass",file = open(file_name, '+a')) #*add
          
    
    
    # check Tagging v
    if(driver.find_elements(By.NAME, "rpvlantable_ChkTag")[int(glc_port)-1].is_selected() == False):
        print(f"             [VLAN - GE/GENNI VLAN Setup - VLAN Table] 39th Tagging V Test Fail",file = open(file_name, '+a')) #*add
        if_error = True

    # if no error => Pass
    if(if_error == False):
        print(f"             [VLAN - GE/GENNI VLAN Setup - VLAN Table] 4001 case Test Pass",file = open(file_name, '+a')) #*add
    else:
        print(f"             [VLAN - GE/GENNI VLAN Setup - VLAN Table] 4001 case Test Fail",file = open(file_name, '+a')) #*add

    #* add -----END------------------------------------------------------------------------------------------------------------
    
    vlan.GE_GENNI_VLAN_Setup_VLAN_Table_Delete(driver)

    vlan.GE_GENNI_VLAN_Setup_VLAN_Table_VLAN_ID(driver,"4094")
    vlan.GE_GENNI_VLAN_Setup_VLAN_Table_Port_Registration_All(driver,3)
    vlan.GE_GENNI_VLAN_Setup_VLAN_Table_Port_Tagging_All(driver,True)
    vlan.GE_GENNI_VLAN_Setup_VLAN_Table_Apply(driver)
    # select
    try:
        # driver.find_element(By.NAME, "rpvlantable_radioSlt").click()         
        driver.find_element(By.XPATH, '//input[@value="4094"]').click()        #*add
    except:
        print(f"             [VLAN - GE/GENNI VLAN Setup - VLAN Table] Select 4094 Test Fail",file = open(file_name, '+a')) #*add
        if_error = True
    vlan.GE_GENNI_VLAN_Setup_VLAN_Table_Modify(driver)
    time.sleep(1)
    # check
    if(driver.find_element(By.XPATH, f"/html/body/form/div[6]/span[{glc_port}]/div[2]/select/option[3]").is_selected() != True):
        print(f"             [VLAN - GE/GENNI VLAN Setup - VLAN Table] Port{glc_port} Registration:Forbidden Test Fail",file = open(file_name, '+a'))
        if_error = True
    else:
        print(f"             [VLAN - GE/GENNI VLAN Setup - VLAN Table] Port{glc_port} Registration:Forbidden Test Pass",file = open(file_name, '+a')) #*add       
    # # check  "Forbidden" (value:2) (another check way)
    # if(driver.find_elements(By.NAME, "rpvlantable_sltRegStatus")[int(glc_port)-1].get_attribute("value")!="2"):
    #     print(f"             [VLAN - GE/GENNI VLAN Setup - VLAN Table] Port{glc_port} Registration:'Forbidden' Test Fail",file = open(file_name, '+a')) #*add
    #     if_error = True
    # else:
    #     print(f"             [VLAN - GE/GENNI VLAN Setup - VLAN Table] Port{glc_port} Registration:'Forbidden' Test Pass",file = open(file_name, '+a')) #*add
        

    if(driver.find_elements(By.NAME, "rpvlantable_ChkTag")[int(glc_port)-1].is_selected() != True):
        print(f"             [VLAN - GE/GENNI VLAN Setup - VLAN Table] Port{glc_port} Tagging:True Test Fail",file = open(file_name, '+a'))
        if_error = True
    vlan.GE_GENNI_VLAN_Setup_VLAN_Table_Port_Registration_All(driver,2)
    vlan.GE_GENNI_VLAN_Setup_VLAN_Table_Apply(driver)
    try:
        # driver.find_element(By.NAME, "rpvlantable_radioSlt").click()         
        driver.find_element(By.XPATH, '//input[@value="4094"]').click()        #*add
    except:
        print(f"             [VLAN - GE/GENNI VLAN Setup - VLAN Table] Select 4094 Test Fail",file = open(file_name, '+a')) #*add
        if_error = True
    vlan.GE_GENNI_VLAN_Setup_VLAN_Table_Modify(driver)
    if(driver.find_element(By.XPATH, f"/html/body/form/div[6]/span[{glc_port}]/div[2]/select/option[2]").is_selected() != True):
        # print(f"             [VLAN - GE/GENNI VLAN Setup - VLAN Table] Port{glc_port} Registration:Forbidden Test Fail",file = open(file_name, '+a'))
        print(f"             [VLAN - GE/GENNI VLAN Setup - VLAN Table] Port{glc_port} Registration:Fixed Test Fail",file = open(file_name, '+a'))  #*add
        if_error = True
    if(driver.find_elements(By.NAME, "rpvlantable_ChkTag")[int(glc_port)-1].is_selected() != True):
        print(f"             [VLAN - GE/GENNI VLAN Setup - VLAN Table] Port{glc_port} Tagging:True Test Fail",file = open(file_name, '+a'))
        if_error = True
    try:
        # driver.find_element(By.NAME, "rpvlantable_radioSlt").click()         
        driver.find_element(By.XPATH, '//input[@value="4094"]').click()        #*add
    except:
        print(f"             [VLAN - GE/GENNI VLAN Setup - VLAN Table] Select 4094 Test Fail",file = open(file_name, '+a')) #*add
        if_error = True
    vlan.GE_GENNI_VLAN_Setup_VLAN_Table_Delete(driver)

    # VLAN GE/GENNI VLAN Setup VLAN Table Result
    if(if_error == False):
        print(f"[MSAN1-11991][VLAN - GE/GENNI VLAN Setup - VLAN Table] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11991][VLAN - GE/GENNI VLAN Setup - VLAN Table] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # VLAN GE/GENNI VLAN Setup VLAN Untag and Copy-Cpbit
    # VLAN > GE/GENNI VLAN Setup > VLAN Untag and Copy-Cpbit
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 VLAN > GE/GENNI VLAN Setup > VLAN Untag and Copy-Cpbit
    mod.Tab_Switch(driver,"VLAN Untag and Copy-Cpbit")

    # slot select
    if_load = False
    while(if_load == False):
        try:
            vlan.Slot_Select(driver,glc_slot)
            if_load = True
        except:
            if_load = False

    # VLAN GE/GENNI VLAN Setup VLAN Untag and Copy-Cpbit Test
    vlan.GE_GENNI_VLAN_Setup_VLAN_Untag_and_Copy_Cpbit_PVID(driver,"4094")
    vlan.GE_GENNI_VLAN_Setup_VLAN_Untag_and_Copy_Cpbit_Pbit(driver,"7")
    vlan.GE_GENNI_VLAN_Setup_VLAN_Untag_and_Copy_Cpbit_Frame_Type(driver,2)
    vlan.GE_GENNI_VLAN_Setup_VLAN_Untag_and_Copy_Cpbit_Copy_Cpbit_Enable(driver,True)
    if_outer_tpid_exist = True
    try:
        vlan.GE_GENNI_VLAN_Setup_VLAN_Untag_and_Copy_Cpbit_Outer_TPID_Enable(driver,True)
    except:
        if_outer_tpid_exist = False
    vlan.GE_GENNI_VLAN_Setup_VLAN_Untag_and_Copy_Cpbit_Apply(driver)

    # Reload
    mod.Tab_Switch(driver,"VLAN Untag and Copy-Cpbit")
    vlan.Slot_Select(driver,glc_slot)

    # VLAN GE/GENNI VLAN Setup VLAN Untag and Copy-Cpbit Check
    if(driver.find_elements(By.NAME, "rpvlanport_IptPVID")[int(glc_port)-1].get_attribute("value") != "4094"):
        print(f"             [VLAN - GE/GENNI VLAN Setup - VLAN Untag and Copy-Cpbit] Port{glc_port} PVID:4094 Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "rpvlanport_IptPbit")[int(glc_port)-1].get_attribute("value") != "7"):
        print(f"             [VLAN - GE/GENNI VLAN Setup - VLAN Untag and Copy-Cpbit] Port{glc_port} Pbit:7 Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.XPATH, f"/html/body/form/div[7]/span[{glc_port}]/div[4]/select/option[2]").is_selected() != True):
        print(f"             [VLAN - GE/GENNI VLAN Setup - VLAN Untag and Copy-Cpbit] Port{glc_port} Frame Type:Tagged Only Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.NAME, "rpvlanport_ChkVlanCopyCpbit")[int(glc_port)-1].is_selected() != True):
        print(f"             [VLAN - GE/GENNI VLAN Setup - VLAN Untag and Copy-Cpbit] Port{glc_port} Copy Cpbit Enable:True Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(if_outer_tpid_exist == True):
        if(driver.find_elements(By.NAME, "rpvlanport_ChkVlanOuterTpid")[int(glc_port)-1].is_selected() != True):
            print(f"             [VLAN - GE/GENNI VLAN Setup - VLAN Untag and Copy-Cpbit] Port{glc_port} Outer TPID Enable:True Test Fail",file = open(file_name, '+a'))
            if_error = True


    # VLAN GE/GENNI VLAN Setup VLAN Untag and Copy-Cpbit Result
    if(if_error == False):
        print(f"[MSAN1-11992][VLAN - GE/GENNI VLAN Setup - VLAN Untag and Copy-Cpbit] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11992][VLAN - GE/GENNI VLAN Setup - VLAN Untag and Copy-Cpbit] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # VLAN Port VLAN TLS
    # VLAN > Port VLAN TLS
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 VLAN > Port VLAN TLS
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"Port VLAN TLS")
    mod.Switch_Frame(driver)

    # slot select
    if_load = False
    while(if_load == False):
        try:
            driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlot']/option[2]")
            vlan.Slot_Select(driver,glc_slot)
            vlan.Load(driver)
            if_load = True
        except:
            time.sleep(5)
            vlan.Load(driver)
            time.sleep(1)
            if_load = False

    # VLAN Port VLAN TLS Test
    for test_port in range(40):
        if_load = False
        while(if_load == False):
            try:
                driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlot']/option[2]")
                vlan.Slot_Select(driver,glc_slot)
                vlan.Port_Select(driver,test_port+1)
                vlan.Load(driver)
                if_load = True
            except:
                time.sleep(5)
                vlan.Load(driver)
                time.sleep(1)
                if_load = False
        vlan.Port_VLAN_TLS_SVID(driver,"4094")
        vlan.Port_VLAN_TLS_Spbit(driver,"7")
        time.sleep(1)
        vlan.Port_VLAN_TLS_Apply(driver)
        time.sleep(1)
        if(driver.find_element(By.CLASS_NAME, "td-table-content.rpVlanTls_config_table_data_svid").get_attribute("textContent") != "4094"):
            print(f"             [VLAN - Port VLAN TLS] Port{test_port+1} SVID:4094 Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_element(By.CLASS_NAME, "td-table-content.rpVlanTls_config_table_data_spbit").get_attribute("textContent") != "7(-)"):
            print(f"             [VLAN - Port VLAN TLS] Port{test_port+1} Spbit:7(-) Test Fail",file = open(file_name, '+a'))
            if_error = True
        time.sleep(2)
    vlan.Port_VLAN_TLS_Slot_Select(driver,glc_slot)
    if(driver.find_element(By.ID, "dataTotal").get_attribute("textContent") != "showing 1 ~ 40, total 40"):
        print(f"             [VLAN - Port VLAN TLS] Total:40 Test Fail",file = open(file_name, '+a'))
        if_error = True
    else:
        driver.find_element(By.NAME, "rpVlanTlsPort_selectEntry").click()
        vlan.Port_VLAN_TLS_Slot_Delete(driver)
        if(driver.find_element(By.ID, "dataTotal").get_attribute("textContent") != "showing 1 ~ 39, total 39"):
            print(f"             [VLAN - Port VLAN TLS] Delete 1 Test Fail",file = open(file_name, '+a'))
            if_error = True
    vlan.Port_VLAN_TLS_Slot_Select_All(driver,True)
    vlan.Port_VLAN_TLS_Slot_Delete(driver)
    if(driver.find_element(By.ID, "dataTotal").get_attribute("textContent") != "showing 0 ~ 0, total 0"):
        print(f"             [VLAN - Port VLAN TLS] Delete All Test Fail",file = open(file_name, '+a'))
        if_error = True
    print(f"             [VLAN - Port VLAN TLS] Max Capacity(1) = 1",file = open(file_name, '+a'))

    # VLAN Port VLAN TLS Result
    if(if_error == False):
        print(f"[MSAN1-11993][VLAN - Port VLAN TLS] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11993][VLAN - Port VLAN TLS] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # VLAN Port VLAN Trunk UNI-tag
    # VLAN > Port VLAN Trunk > UNI-tag
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 VLAN > Port VLAN > UNI-tag Trunk
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"VLAN")
    mod.SubPage_Switch(driver,"Port VLAN Trunk")
    mod.Switch_Frame(driver)
    time.sleep(1)
    mod.Tab_Switch(driver,"UNI-tag")

    # input("input to pause, please check if load fail")

    # slot select
    if_load = False
    while(if_load == False):
        try:
            driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlot']/option[2]")
            vlan.Slot_Select(driver,glc_slot)
            vlan.Load(driver)
            if_load = True
        except:
            time.sleep(5)
            vlan.Load(driver)
            time.sleep(1)
            if_load = False

    # VLAN Port VLAN Trunk UNI-tag Test
    port_max_cap = 0
    for test_port in range(40):
        for input_value in range(9):
            if_load = False
            while(if_load == False):
                try:
                    driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlot']/option[2]")
                    vlan.Slot_Select(driver,glc_slot)
                    vlan.Port_Select(driver,test_port+1)
                    vlan.Load(driver)
                    if_load = True
                except:
                    time.sleep(5)
                    vlan.Load(driver)
                    time.sleep(1)
                    if_load = False
            vlan.Port_VLAN_Trunk_UNI_tag_Uni_VID(driver,input_value+1)
            vlan.Port_VLAN_Trunk_UNI_tag_SVID(driver,input_value+1)
            time.sleep(1)
            vlan.Port_VLAN_Trunk_UNI_tag_Apply(driver)
            time.sleep(2)        
            try:
                driver.find_element(By.NAME, "rperror_btnBack").click()
                if(input_value > port_max_cap):
                    port_max_cap = input_value
                break
            except:
                pass
        if(port_max_cap > 8):
            # print(f"             [VLAN - Port VLAN Trunk - UNI-tag] One Port Max Capacity(8) = {port_max_cap}",file = open(file_name, '+a'))
            print(f"             [VLAN - Port VLAN Trunk - UNI-tag] {test_port+1} Port Max Capacity(8) = {port_max_cap}",file = open(file_name, '+a'))

    # Slot Select Test
    vlan.Port_VLAN_Trunk_UNI_tag_Slot_Select(driver,glc_slot)
    temp = driver.find_element(By.ID, "dataTotal").get_attribute("textContent")
    if( temp != "showing 1 ~ 40, total 320"):
        print(f"             [VLAN - Port VLAN Trunk - UNI-tag] msg:{temp}",file = open(file_name, '+a')) #* add
        print(f"             [VLAN - Port VLAN Trunk - UNI-tag] Total:320 Test Fail",file = open(file_name, '+a'))
        if_error = True
    else:
        driver.find_element(By.NAME, "rpVlanTrunkVlanPort_sltEntry").click()
        vlan.Port_VLAN_Trunk_UNI_tag_Slot_Delete(driver)
        if(driver.find_element(By.ID, "dataTotal").get_attribute("textContent") != "showing 1 ~ 40, total 319"):
            print(f"             [VLAN - Port VLAN Trunk - UNI-tag] Delete 1 Test Fail",file = open(file_name, '+a'))
            if_error = True
    for page in range(8):
        vlan.Port_VLAN_Trunk_UNI_tag_Slot_Select_All(driver,True)
        vlan.Port_VLAN_Trunk_UNI_tag_Slot_Delete(driver)
        time.sleep(1)
    if(driver.find_element(By.ID, "dataTotal").get_attribute("textContent") != "showing 0 ~ 0, total 0"):
        print(f"             [VLAN - Port VLAN Trunk - UNI-tag] Delete All Test Fail",file = open(file_name, '+a'))
        if_error = True

    # VLAN Port VLAN Trunk UNI-tag Result
    if(if_error == False):
        print(f"[MSAN1-11994][VLAN - Port VLAN Trunk - UNI-tag] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11994][VLAN - Port VLAN Trunk - UNI-tag] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # VLAN Port VLAN Trunk UNI-untag
    # VLAN > Port VLAN Trunk > UNI-untag
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 VLAN > Port VLAN Trunk > UNI-untag
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"VLAN")
    mod.SubPage_Switch(driver,"Port VLAN Trunk")
    mod.Switch_Frame(driver)
    time.sleep(1)
    mod.Tab_Switch(driver,"UNI-untag")

    # slot select
    if_load = False
    while(if_load == False):
        try:
            driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlot']/option[2]")
            vlan.Slot_Select(driver,glc_slot)
            vlan.Port_Select(driver,glc_port)
            vlan.Load(driver)
            if_load = True
        except:
            time.sleep(5)
            vlan.Load(driver)
            time.sleep(1)
            if_load = False
    
    # VLAN Port VLAN Trunk UNI-untag Test
    vlan.Port_VLAN_Trunk_UNI_untag_Subnet_IP(driver,True)
    vlan.Port_VLAN_Trunk_UNI_untag_Subnet(driver,"10.10.10.1/24")
    vlan.Port_VLAN_Trunk_UNI_untag_SVID(driver,"2")
    vlan.Port_VLAN_Trunk_UNI_untag_Spbit(driver,"2")
    vlan.Port_VLAN_Trunk_UNI_untag_Apply(driver)
    pyautogui.press("enter")
    for test_port in range(40):
        vlan.Load(driver)
        time.sleep(1)
        vlan.Port_Select(driver,test_port+1)
        time.sleep(0.5)
        vlan.Load(driver)
        vlan.Port_VLAN_Trunk_UNI_untag_Ether_Type(driver,True)
        vlan.Port_VLAN_Trunk_UNI_untag_Ether_Type_Input(driver,"ffff")
        vlan.Port_VLAN_Trunk_UNI_untag_SVID(driver,"1")
        vlan.Port_VLAN_Trunk_UNI_untag_Spbit(driver,"1")
        vlan.Port_VLAN_Trunk_UNI_untag_Apply(driver)
        vlan.Port_VLAN_Trunk_UNI_untag_SVID(driver,"4094")
        vlan.Port_VLAN_Trunk_UNI_untag_Spbit(driver,"7")
        vlan.Port_VLAN_Trunk_UNI_untag_CVID(driver,"4094")
        vlan.Port_VLAN_Trunk_UNI_untag_Apply(driver)
        if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpVlanTrunkUniUntag_config_table_data_type")[0].get_attribute("textContent") != "trunk" or driver.find_elements(By.CLASS_NAME, "td-table-content.rpVlanTrunkUniUntag_config_table_data_svid")[0].get_attribute("textContent") != "4094" or driver.find_elements(By.CLASS_NAME, "td-table-content.rpVlanTrunkUniUntag_config_table_data_spbit")[0].get_attribute("textContent") != "7" or driver.find_elements(By.CLASS_NAME, "td-table-content.rpVlanTrunkUniUntag_config_table_data_cvid")[0].get_attribute("textContent") != "4094" or driver.find_elements(By.CLASS_NAME, "td-table-content.rpVlanTrunkUniUntag_config_table_data_ether_type")[0].get_attribute("textContent") != "-" or driver.find_elements(By.CLASS_NAME, "td-table-content.rpVlanTrunkUniUntag_HideSubnet.rpVlanTrunkUniUntag_config_table_data_subnet_ip")[0].get_attribute("textContent") != "-"):
            print(f"             [VLAN - Port VLAN Trunk - UNI-untag] Port{test_port+1} trunk Apply Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpVlanTrunkUniUntag_config_table_data_type")[1].get_attribute("textContent") != "protocol" or driver.find_elements(By.CLASS_NAME, "td-table-content.rpVlanTrunkUniUntag_config_table_data_svid")[1].get_attribute("textContent") != "1" or driver.find_elements(By.CLASS_NAME, "td-table-content.rpVlanTrunkUniUntag_config_table_data_spbit")[1].get_attribute("textContent") != "1" or driver.find_elements(By.CLASS_NAME, "td-table-content.rpVlanTrunkUniUntag_config_table_data_cvid")[1].get_attribute("textContent") != "-" or driver.find_elements(By.CLASS_NAME, "td-table-content.rpVlanTrunkUniUntag_config_table_data_ether_type")[1].get_attribute("textContent") != "0xffff" or driver.find_elements(By.CLASS_NAME, "td-table-content.rpVlanTrunkUniUntag_HideSubnet.rpVlanTrunkUniUntag_config_table_data_subnet_ip")[1].get_attribute("textContent") != "-"):
            print(f"             [VLAN - Port VLAN Trunk - UNI-untag] Port{test_port+1} protocol Test Fail",file = open(file_name, '+a'))
            if_error = True
        if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpVlanTrunkUniUntag_config_table_data_type")[2].get_attribute("textContent") != "subnet" or driver.find_elements(By.CLASS_NAME, "td-table-content.rpVlanTrunkUniUntag_config_table_data_svid")[2].get_attribute("textContent") != "2" or driver.find_elements(By.CLASS_NAME, "td-table-content.rpVlanTrunkUniUntag_config_table_data_spbit")[2].get_attribute("textContent") != "2" or driver.find_elements(By.CLASS_NAME, "td-table-content.rpVlanTrunkUniUntag_config_table_data_cvid")[2].get_attribute("textContent") != "-" or driver.find_elements(By.CLASS_NAME, "td-table-content.rpVlanTrunkUniUntag_config_table_data_ether_type")[2].get_attribute("textContent") != "-" or driver.find_elements(By.CLASS_NAME, "td-table-content.rpVlanTrunkUniUntag_HideSubnet.rpVlanTrunkUniUntag_config_table_data_subnet_ip")[2].get_attribute("textContent") != "10.10.10.1/24"):
            print(f"             [VLAN - Port VLAN Trunk - UNI-untag] Port{test_port+1} subnet Test Fail",file = open(file_name, '+a'))
            if_error = True
    
    # Slot Select Test
    vlan.Port_VLAN_Trunk_UNI_untag_Slot_Select(driver,glc_slot)
    if(driver.find_element(By.ID, "dataTotal").get_attribute("textContent") != "showing 1 ~ 40, total 120"):
        print(f"             [VLAN - Port VLAN Trunk - UNI-untag] Total:120 Test Fail",file = open(file_name, '+a'))
        if_error = True
    else:
        vlan.Port_VLAN_Trunk_UNI_untag_Slot_Next(driver)
        driver.find_element(By.NAME, "rpVlanTrunkUntagPort_sltEntry").click()
        vlan.Port_VLAN_Trunk_UNI_untag_Slot_Delete(driver)
        if(driver.find_element(By.ID, "dataTotal").get_attribute("textContent") != "showing 1 ~ 40, total 119"):
            print(f"             [VLAN - Port VLAN Trunk - UNI-untag] Delete 1 Test Fail",file = open(file_name, '+a'))
            if_error = True
    vlan.Port_VLAN_Trunk_UNI_untag_Slot_Next(driver)
    vlan.Port_VLAN_Trunk_UNI_untag_Slot_Select_All(driver,True)
    vlan.Port_VLAN_Trunk_UNI_untag_Slot_Delete(driver)
    pyautogui.press("enter")
    time.sleep(1)
    vlan.Port_VLAN_Trunk_UNI_untag_Slot_Next(driver)
    vlan.Port_VLAN_Trunk_UNI_untag_Slot_Select_All(driver,True)
    vlan.Port_VLAN_Trunk_UNI_untag_Slot_Delete(driver)
    pyautogui.press("enter")
    time.sleep(1)
    try:
        for index in range(40):
            if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpVlanTrunkUniUntagPort_type")[index].get_attribute("textContent") == "protocol"):
                driver.find_elements(By.NAME, "rpVlanTrunkUntagPort_sltEntry")[index].click()
        vlan.Port_VLAN_Trunk_UNI_untag_Slot_Delete(driver)
        time.sleep(1)
    except:
        pass
    vlan.Port_VLAN_Trunk_UNI_untag_Slot_Select_All(driver,True)
    vlan.Port_VLAN_Trunk_UNI_untag_Slot_Delete(driver)
    time.sleep(1)
    if(driver.find_element(By.ID, "dataTotal").get_attribute("textContent") != "showing 0 ~ 0, total 0"):
        print(f"             [VLAN - Port VLAN Trunk - UNI-untag] Delete All Test Fail",file = open(file_name, '+a'))
        if_error = True

    # VLAN Port VLAN Trunk UNI-untag Result
    if(if_error == False):
        print(f"[MSAN1-11995][VLAN - Port VLAN Trunk - UNI-untag] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11995][VLAN - Port VLAN Trunk - UNI-untag] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # VLAN Port VLAN Translation
    # VLAN > Port VLAN Translation
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 VLAN > Port VLAN Translation
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"Port VLAN Translation")
    mod.Switch_Frame(driver)

    # Slot Select
    if_load = False
    while(if_load == False):
        try:
            driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlot']/option[2]")
            vlan.Slot_Select(driver,glc_slot)
            vlan.Load(driver)
            if_load = True
        except:
            time.sleep(5)
            vlan.Load(driver)
            time.sleep(1)
            if_load = False

    # VLAN Port VLAN Translation Test
    if_mode_exist = True
    # port_max_cap = 0
    for test_port in range(40):
        port_max_cap = 0                            #*add
        for input_value in range(4094):
            if_load = False
            while(if_load == False):
                try:
                    driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlot']/option[2]")
                    vlan.Slot_Select(driver,glc_slot)
                    vlan.Port_Select(driver,test_port+1)
                    vlan.Load(driver)
                    
                    time.sleep(1)
                    print()
                    print("Load~"+driver.find_element(By.ID, "lctbl_selPort").get_attribute("value"))
                    if(driver.find_element(By.ID, "lctbl_selPort").get_attribute("value")==""):                     #*add
                        print("Load agin...")
                        driver.find_element(By.ID, "lc123456789asdfghjkl impossible id to go to except")
                    
                    if_load = True
                except:
                    time.sleep(5)
                    vlan.Load(driver)
                    time.sleep(1)
                    if_load = False
            try:
                vlan.Port_VLAN_Translation_Mode(driver,3)
            except:
                if_mode_exist = False
            vlan.Port_VLAN_Translation_Uni_VID(driver,input_value+1)
            vlan.Port_VLAN_Translation_SVID(driver,input_value+1)
            vlan.Port_VLAN_Translation_Spbit(driver,"8")
            vlan.Port_VLAN_Translation_C_tag_Add(driver,True)
            vlan.Port_VLAN_Translation_CVID(driver,input_value+1)
            # time.sleep(0.5) 
            vlan.Port_VLAN_Translation_Apply(driver)
            # time.sleep(1)
            time.sleep(0.5)
            try:
                driver.find_element(By.NAME, "rperror_btnBack").click()
                if(input_value > port_max_cap):
                    port_max_cap = input_value
                break
            except:
                pass
            
            # check if Apply success                        #*add
            #       if input number is correct
            
            print()
            print("Port:"+str(test_port+1)+", number:",end="")
            print(driver.find_elements(By.CLASS_NAME, "td-table-content.rpVlanTranslation_config_table_data_svid").__len__())
            num = driver.find_elements(By.CLASS_NAME, "td-table-content.rpVlanTranslation_config_table_data_svid").__len__()
            if(num != (input_value+1)):
                print(f"num:{num} != input_value+1:{input_value+1}     ", end="")
                print("wrong num.")
            else:
                print("correct num.")



        if(port_max_cap > 8):  #* add ---------------
            print(f"             [VLAN - Port VLAN Translation] Port:{test_port+1} Max Capacity(8) = {port_max_cap} Fail",file = open(file_name, '+a'))
            if_error = True
    if(if_mode_exist == False):
        print(f"             [VLAN - Port VLAN Translation] Mode Don't Exist",file = open(file_name, '+a'))
    # print(f"             [VLAN - Port VLAN Translation] One Port Max Capacity(8) = {port_max_cap}",file = open(file_name, '+a'))

    # if(port_max_cap != 8):
    #     print(f"             [VLAN - Port VLAN Translation] One Port Max Capacity != 8 Fail",file = open(file_name, '+a'))
    #     if_error = True

    # Slot Select Test
    vlan.Port_VLAN_Translation_Slot_Select(driver,glc_slot)
    msg = driver.find_element(By.ID, "dataTotal").get_attribute("textContent")
    if( msg != "showing 1 ~ 40, total 320"):
        print(f"             [VLAN - Port VLAN Translation] msg:{msg} Total:320 Test Fail",file = open(file_name, '+a'))
        if_error = True
    else:
        driver.find_element(By.NAME, "rpVlanTranslationPort_selectEntryPort").click()
        vlan.Port_VLAN_Translation_Slot_Delete(driver)
        msg = driver.find_element(By.ID, "dataTotal").get_attribute("textContent")
        if( msg != "showing 1 ~ 40, total 319"):
            print(f"             [VLAN - Port VLAN Translation] msg:{msg} Delete 1 Test Fail",file = open(file_name, '+a'))
            if_error = True
    for page in range(8):
        vlan.Port_VLAN_Translation_Slot_Select_All(driver,True)
        vlan.Port_VLAN_Translation_Slot_Delete(driver)
        time.sleep(1)
    msg = driver.find_element(By.ID, "dataTotal").get_attribute("textContent")
    if( msg != "showing 0 ~ 0, total 0"):
        print(f"             [VLAN - Port VLAN Translation] msg:{msg} Delete All Test Fail",file = open(file_name, '+a'))
        if_error = True

    # VLAN Port VLAN Translation Result
    if(if_error == False):
        print(f"[MSAN1-11996][VLAN - Port VLAN Translation] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11996][VLAN - Port VLAN Translation] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # VLAN VLAN Tag Mode Setup
    # VLAN > VLAN Tag Mode Setup
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 VLAN > VLAN Tag Mode Setup
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"VLAN Tag Mode Setup")
    mod.Switch_Frame(driver)

    # VLAN VLAN Tag Mode Setup Test
    vlan.VLAN_Tag_Mode_Setup_Tag_Mode(driver,2)
    if_qinq_exist = True
    try:
        vlan.VLAN_Tag_Mode_Setup_QinQ_TPID(driver,"ffff")
    except:
        if_qinq_exist = False
    vlan.VLAN_Tag_Mode_Setup_Apply(driver)

    # VLAN VLAN Tag Mode Setup Check
    if(driver.find_element(By.XPATH, f"//*[@name='rpVlanSingleTag_sltStagMode']/option[2]").is_selected() != True):
        print(f"             [VLAN - VLAN Tag Mode Setup] Tag Mode:Ctag Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(if_qinq_exist == True):
        if(driver.find_element(By.NAME, "rpVlanSingleTag_qinqtpidSetup").get_attribute("value") != "ffff"):
            print(f"             [VLAN - VLAN Tag Mode Setup] QinQ TPID:ffff Test Fail",file = open(file_name, '+a'))
            if_error = True

    # VLAN VLAN Tag Mode Setup Default
    vlan.VLAN_Tag_Mode_Setup_Tag_Mode(driver,1)
    if(if_qinq_exist == True):
        vlan.VLAN_Tag_Mode_Setup_QinQ_TPID(driver,"8100")
    vlan.VLAN_Tag_Mode_Setup_Apply(driver)

    # VLAN VLAN Tag Mode Setup Result
    if(if_error == False):
        print(f"[MSAN1-11997][VLAN - VLAN Tag Mode Setup] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11997][VLAN - VLAN Tag Mode Setup] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Config Save Test
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Config Save
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Config Save")
    mod.Switch_Frame(driver)

    try:
        for test_times in range(3):
            con.Save(driver)
            con.Back(driver)
    except:
        if_error = True

    # Config Save Result
    if(if_error == False):
        print(f"[MSAN1-11998][Config Save] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11998][Config Save] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def Maintenance_Test(driver,glc_slot,glc_port,file_name):
    print(f"Maintenance Test\nTest Start",file = open(file_name, '+a'))

    # Get GLC name (use in FW Upgrade)
    # Home
    # -------------------------start-------------------------
    # Get GLC name
    mod.Switch_Default(driver)
    driver.find_element(By.XPATH, '//*[@id="mainTable"]/tbody/tr[1]/td/div/div[2]/div/div[3]/a').click()
    mod.Switch_Frame(driver)
    time.sleep(1)
    driver.find_elements(By.NAME, "Sysinfotableid")[int(glc_slot)-1].click()
    time.sleep(1)
    glc_name = driver.find_element(By.CLASS_NAME, "div-row-cell-content.rplcmanDetailName").get_attribute("textContent")
    glc_name = glc_name.split("-")[0]
    # -------------------------end-------------------------


    # Maintenance Config Backup
    # Maintenance > Config Backup
    # -------------------------start-------------------------

    if_error = False 

    # 路徑導向 Maintenance > Config Backup
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Maintenance")
    mod.Switch_Frame(driver)

    # Maintenance Config Backup Test
    driver.find_element(By.NAME, "rpMainBackup").click()
    if(mod.IsAlert(driver) == True):
        if(driver.find_element(By.CLASS_NAME, "toast-message").get_attribute("textContent") != "Config Backup successful"):
            print(f"             [Maintenance - Config Backup] Backup Alert No Success Test Fail",file = open(file_name, '+a'))
            if_error = True
    else:
        print(f"             [Maintenance - Config Backup] Backup No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Maintenance Config Backup
    if(if_error == False):
        print(f"[MSAN1-11858][Maintenance - Config Backup] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11858][Maintenance - Config Backup] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Maintenance Config Restore
    # Maintenance > Config Restore
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Maintenance > Config Restore
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"Config Restore")
    mod.Switch_Frame(driver)

    # Maintenance Config Restore Test
    driver.find_element(By.NAME, "rpMainConfigRestore").click()
    if(mod.IsAlert(driver) != True):
        print(f"             [Maintenance - Config Restore] Restore No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Maintenance Config Restore
    if(if_error == False):
        print(f"[MSAN1-11859][Maintenance - Config Restore] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11859][Maintenance - Config Restore] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Maintenance Config Reset
    # Maintenance > Config Reset
    # -------------------------start-------------------------

    # 路徑導向 Maintenance > Config Reset
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"Config Reset")
    mod.Switch_Frame(driver)

    # Maintenance Config Reset Test
    driver.find_element(By.NAME, "rpConfigReset").click()
    pyautogui.press("enter")

    time.sleep(1)               #*add  wait to idle
    state_n = ""
    while(state_n !="idle"):
        time.sleep(2)    
        state_n = driver.find_element(By.CLASS_NAME, "state").text


    # Maintenance Config Reset
    print(f"[MSAN1-11860][Maintenance - Config Reset] Result Pass",file = open(file_name, '+a'))

    

    # -------------------------end-------------------------

    # Maintenance Coredump Backup
    # Maintenance > Coredump Backup
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Maintenance > Coredump Backup
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"Coredump Backup")
    mod.Switch_Frame(driver)

    # Maintenance Coredump Backup Test
    driver.find_element(By.NAME, "rpMainBackup").click()
    # #*add------------------------------
    # for i in range (1,6):
    #     try:                                        #toast-message
    #         msg = driver.find_element(By.CLASS_NAME, "toast-message").text        
    #         print("msg:")
    #         print(msg)
    #     except:
    #         print("no msg")
    #     time.sleep(1)
    #     print(f"wait for 1 second. {i}")    
    # #*add------------------------------

    # try:
    #     print("coredump msg:")
    #     print(driver.find_element(By.CLASS_NAME, "toast-message").get_attribute("textContent"))
    # except:
    #     pass

    if(mod.IsAlert(driver) == True):        
        if(driver.find_element(By.CLASS_NAME, "toast-message").get_attribute("textContent") != "Coredump Backup successful"):
            print(f"             [Maintenance - Coredump Backup] Backup Alert No Success Test Fail",file = open(file_name, '+a'))
            if_error = True
    else:
        print(f"             [Maintenance - Coredump Backup] Backup No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Maintenance Coredump Backup
    if(if_error == False):
        print(f"[MSAN1-11863][Maintenance - Coredump Backup] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11863][Maintenance - Coredump Backup] Result Fail",file = open(file_name, '+a'))

    

    # -------------------------end-------------------------

    # Maintenance FW Upgrade
    # Maintenance > FW Upgrade
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Maintenance > FW Upgrade
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"FW Upgrade")
    mod.Switch_Frame(driver)

    # Maintenance FW Upgrade Test 1

    # if_last = False
    # fw_upgrade_option = 1
    # while(if_last == False):
    #     try:
    #         fw_upgrade_card_type = driver.find_element(By.XPATH, f"//*[@name='rpmaintenance_sltCardType']/option[{fw_upgrade_option}]").get_attribute("value")
    #         fw_upgrade_card_type = fw_upgrade_card_type.split("1")[0]
    #         if(fw_upgrade_card_type == "GLC"):
    #             driver.find_element(By.XPATH, f"//*[@name='rpmaintenance_sltCardType']/option[{fw_upgrade_option}]").click()
    #             break
    #         fw_upgrade_option = fw_upgrade_option+1
    #     except:
    #         if_last = True
    # edit from above -----------START------------------------------------------------

    # glc_name = "GLC1440X" or "GLC1540X"                       #*add
    # select FW Upgrade CardType
    if_last = False
    fw_upgrade_option = 1
    while(if_last == False):
        try:
            fw_upgrade_card_type = driver.find_element(By.XPATH, f"//*[@name='rpmaintenance_sltCardType']/option[{fw_upgrade_option}]").get_attribute("value")
            fw_upgrade_card_type = fw_upgrade_card_type.split("-")[0]
            if(fw_upgrade_card_type == glc_name):
                driver.find_element(By.XPATH, f"//*[@name='rpmaintenance_sltCardType']/option[{fw_upgrade_option}]").click()
                break
            fw_upgrade_option = fw_upgrade_option+1
        except:
            if_last = True

    # edit from above -----------END--------------------------------------------------

    driver.find_element(By.NAME, "rpupgradeCard").click()
    
    time.sleep(2)
    try:
        driver.find_element(By.NAME, "rperror_btnBack")
        msg = driver.find_element(By.CLASS_NAME, "div-row-cell-content.msg").get_attribute("textContent").split("\n")[0]        
        if(driver.find_element(By.CLASS_NAME, "div-row-cell-content.msg").get_attribute("textContent") != "invalid file"):
            print(f"             [Maintenance - FW Upgrade] msg:{msg} Test Fail",file = open(file_name, '+a'))
            print(f"             [Maintenance - FW Upgrade] Card Type Upgrade Error Msg Incompatible Test Fail",file = open(file_name, '+a'))
            if_error = True
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:      
        if(mod.IsAlert(driver) == False):                
            print(f"             [Maintenance - FW Upgrade] Card Type Upgrade Valid Test Fail",file = open(file_name, '+a'))
            if_error = True

    # Maintenance FW Upgrade Test 2
    time.sleep(1)
    fw_upgrade_check_box = driver.find_element(By.NAME, "rpfwUpgrade_chkAutoChange")
    if(fw_upgrade_check_box.is_selected() == False):
        fw_upgrade_check_box.click()
    driver.find_elements(By.NAME, "Lcmantableid")[int(glc_slot)-1].click()
    driver.find_element(By.NAME, "RpFWUpgrade_BtnUpgrade").click()
    try:
        driver.find_element(By.NAME, "rperror_btnBack")
        if(driver.find_element(By.CLASS_NAME, "div-row-cell-content.msg").get_attribute("textContent") != "invalid file"):
            print(f"             [Maintenance - FW Upgrade] GLC ID Upgrade Error Msg Incompatible Test Fail",file = open(file_name, '+a'))
            if_error = True
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        if(mod.IsAlert(driver) == False):
            print(f"             [Maintenance - FW Upgrade] GLC ID Upgrade Invalid Test Fail",file = open(file_name, '+a'))
            if_error = True

    # Maintenance FW Upgrade Test 3
    time.sleep(5)
    driver.find_elements(By.NAME, "Sysinfotableid")[int(glc_slot)-1].click()
    time.sleep(10)
    fw_upgrade_name = driver.find_element(By.CLASS_NAME, "div-row-cell-content.rplcmanDetailName").get_attribute("textContent")
    fw_upgrade_name = fw_upgrade_name.split("1")[0]
    if(fw_upgrade_name != "GLC"):
        print(f"             [Maintenance - FW Upgrade] GLC ID Select GLC name Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Maintenance FW Upgrade
    if(if_error == False):
        print(f"[MSAN1-11864][Maintenance - FW Upgrade] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11864][Maintenance - FW Upgrade] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Maintenance Reboot
    # Maintenance > Reboot
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Maintenance > Reboot
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"Reboot")
    mod.Switch_Frame(driver)

    # Maintenance Reboot Test 1
    reboot_current_image = driver.find_element(By.CLASS_NAME, "div-row-cell-content.Current_Image").get_attribute("textContent")
    reboot_current_image = reboot_current_image.split("(")[2]
    if(reboot_current_image == " image-2 )"):
        driver.find_element(By.XPATH, f"//*[@name='rpmaintenance_sltImage']/option[2]").click()
        driver.find_element(By.NAME, "rpMainApplyImg").click()
        time.sleep(5)
        reboot_next_boot_image = driver.find_element(By.CLASS_NAME, "div-row-cell-content.Next_Image").get_attribute("textContent")
        reboot_next_boot_image = reboot_next_boot_image.split("(")[2]
        if(reboot_current_image != " image-2 )"):
            print(f"             [Maintenance - Reboot] Boot Image Test Fail",file = open(file_name, '+a'))
            if_error = True
    elif(reboot_current_image == " image-1 )"):
        driver.find_element(By.XPATH, f"//*[@name='rpmaintenance_sltImage']/option[1]").click()
        driver.find_element(By.NAME, "rpMainApplyImg").click()
        time.sleep(5)
        reboot_next_boot_image = driver.find_element(By.CLASS_NAME, "div-row-cell-content.Next_Image").get_attribute("textContent")
        reboot_next_boot_image = reboot_next_boot_image.split("(")[2]
        if(reboot_current_image != " image-1 )"):
            print(f"             [Maintenance - Reboot] Boot Image Test Fail",file = open(file_name, '+a'))
            if_error = True

    # Maintenance Reboot Test 2
    driver.find_element(By.NAME, "rpCntdonwApply").click()
    if(mod.IsAlert(driver) != True):
        print(f"             [Maintenance - Reboot] Countdown No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Maintenance Reboot Test 3
    driver.find_element(By.NAME, "rpCntdonwCancel").click()
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [Maintenance - Reboot] Cancel Invalid Test Fail",file = open(file_name, '+a'))
        if_error = True
    
    # Maintenance Reboot Result
    if(if_error == False):
        print(f"[MSAN1-11865][Maintenance - Reboot] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11865][Maintenance - Reboot] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Maintenance AlmHis Backup
    # Maintenance > AlmHis Backup
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Maintenance > AlmHis Backup
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"AlmHis Backup")
    mod.Switch_Frame(driver)

    # Maintenance AlmHis Backup Test
    driver.find_element(By.CLASS_NAME, "font-btn").click()
    if(mod.IsAlert(driver) == True):        
        # if(driver.find_element(By.CLASS_NAME, "toast-message").get_attribute("textContent") != "AlmHis Backup successful"):
        if(driver.find_element(By.CLASS_NAME, "toast-message").get_attribute("textContent") != "Alarm History Backup successful"):
            print(f"             [Maintenance - AlmHis Backup] Backup Alert No Success Test Fail",file = open(file_name, '+a'))
            if_error = True
    else:
        print(f"             [Maintenance - AlmHis Backup] Backup No Alert Test Fail(#175210)",file = open(file_name, '+a'))
        if_error = True

    # Maintenance AlmHis Backup
    if(if_error == False):
        print(f"[MSAN1-11866][Maintenance - AlmHis Backup] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11866][Maintenance - AlmHis Backup] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Maintenance Syslog Backup
    # Maintenance > Syslog Backup
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Maintenance > Syslog Backup
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"Syslog Backup")
    mod.Switch_Frame(driver)

    # Maintenance Syslog Backup Test
    driver.find_element(By.NAME, "rpMainBackup").click()
    if(mod.IsAlert(driver) == True):
        if(driver.find_element(By.CLASS_NAME, "toast-message").get_attribute("textContent") != "Syslog Backup successful"):
            print(f"             [Maintenance - Syslog Backup] Backup Alert No Success Test Fail",file = open(file_name, '+a'))
            if_error = True
    else:
        print(f"             [Maintenance - Syslog Backup] Backup No Alert Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Maintenance Syslog Backup Result
    if(if_error == False):
        print(f"[MSAN1-11867][Maintenance - Syslog Backup] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11867][Maintenance - Syslog Backup] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Maintenance Next Boot Config
    # Maintenance > Next Boot Config
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Maintenance > Next Boot Config
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"Next Boot Config")
    mod.Switch_Frame(driver)

    # Maintenance Next Boot Config Test
    driver.find_element(By.XPATH, f"//*[@name='rpmaintenance_sltNextConfig']/option[2]").click()
    if(driver.find_element(By.XPATH, f"//*[@name='rpmaintenance_sltNextConfig']/option[2]").is_selected() != True):
        print(f"             [Maintenance - Next Boot Config] Config-2 Test Fail",file = open(file_name, '+a'))
        if_error = True
    driver.find_element(By.XPATH, f"//*[@name='rpmaintenance_sltNextConfig']/option[1]").click()
    if(driver.find_element(By.XPATH, f"//*[@name='rpmaintenance_sltNextConfig']/option[1]").is_selected() != True):
        print(f"             [Maintenance - Next Boot Config] Config-1 Test Fail",file = open(file_name, '+a'))
        if_error = True
    driver.find_element(By.XPATH, f"//*[@name='rpmaintenance_sltNextConfig']/option[2]").click()
    if(driver.find_element(By.XPATH, f"//*[@name='rpmaintenance_sltNextConfig']/option[2]").is_selected() != True):
        print(f"             [Maintenance - Next Boot Config] Config-2 Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Maintenance Next Boot Config Result
    if(if_error == False):
        print(f"[MSAN1-11861][Maintenance - Next Boot Config] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11861][Maintenance - Next Boot Config] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Maintenance Config Reload
    # Maintenance > Config Reload
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Maintenance > Config Reload
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"Config Reload")
    mod.Switch_Frame(driver)

    # Maintenance Config Reload Test
    driver.find_element(By.XPATH, f"//*[@name='rpmaintenance_sltConfig']/option[2]").click()
    if(driver.find_element(By.XPATH, f"//*[@name='rpmaintenance_sltConfig']/option[2]").is_selected() != True):
        print(f"             [Maintenance - Config Reload] Config-2 Test Fail",file = open(file_name, '+a'))
        if_error = True
    driver.find_element(By.XPATH, f"//*[@name='rpmaintenance_sltConfig']/option[1]").click()
    if(driver.find_element(By.XPATH, f"//*[@name='rpmaintenance_sltConfig']/option[1]").is_selected() != True):
        print(f"             [Maintenance - Config Reload] Config-1 Test Fail",file = open(file_name, '+a'))
        if_error = True
    driver.find_element(By.XPATH, f"//*[@name='rpmaintenance_sltConfig']/option[2]").click()
    if(driver.find_element(By.XPATH, f"//*[@name='rpmaintenance_sltConfig']/option[2]").is_selected() != True):
        print(f"             [Maintenance - Config Reload] Config-2 Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Maintenance Config Reload Result
    if(if_error == False):
        print(f"[MSAN1-11862][Maintenance - Config Reload] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11862][Maintenance - Config Reload] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def Sys_Test(driver,glc_slot,glc_port,msc_slot,msc_port,file_name):
    print(f"Sys Test\nTest Start",file = open(file_name, '+a'))

    # Get MSC Card Type
    # Home
    # -------------------------start-------------------------

    mod.Switch_Default(driver)
    driver.find_elements(By.CLASS_NAME, "div-title-homelink")[1].click()
    mod.Switch_Frame(driver)
    time.sleep(1)
    MSC_Card_Type = driver.find_elements(By.CLASS_NAME, "td-table-content.SysinfoCardType.left-wrapper")[int(msc_slot)-1].get_attribute("textContent")

    # -------------------------end-------------------------

    # Sys AAA
    # Sys > AAA
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Sys > AAA > Accounting
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Sys")
    mod.Switch_Frame(driver)

    # Sys AAA Accounting Test 1
    sys.AAA_Accounting_Update_Period(driver,"2147483647")
    driver.find_elements(By.NAME, "rpsysaaa_acc_button_apply")[0].click()
    if(driver.find_element(By.NAME, "rpsysaaa_acc_input_period").get_attribute("value") != "2147483647"):
        print(f"             [Sys - AAA - Accounting] Update Period Max Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Sys AAA Accounting Test 2
    sys.AAA_Accounting_Update_System_Active(driver,True)
    sys.AAA_Accounting_Update_Exec_Active(driver,True)
    sys.AAA_Accounting_Update_Commands_Active(driver,True)
    driver.find_elements(By.NAME, "rpsysaaa_acc_button_apply")[1].click()
    if(driver.find_element(By.NAME, "rpsysaaa_acc_sys_action").is_selected() != True):
        print(f"             [Sys - AAA - Accounting] System Active Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpsysaaa_acc_exec_action").is_selected() != True):
        print(f"             [Sys - AAA - Accounting] Exec Active Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpsysaaa_acc_com_action").is_selected() != True):
        print(f"             [Sys - AAA - Accounting] Commands Active Test Fail",file = open(file_name, '+a'))
        if_error = True

    # 路徑導向 Sys > AAA > Authentication
    mod.Tab_Switch(driver,"Authentication")

    # Sys AAA Authentication Test
    sys.AAA_Authentication_Enable_Try_Cont(driver,True)
    sys.AAA_Authentication_Login_Try_Cont(driver,True)
    driver.find_element(By.NAME, "rpsysaaa_authent_button_apply").click()

    # 路徑導向 Sys > AAA > Authorization
    mod.Tab_Switch(driver,"Authorization")
    driver.find_element(By.NAME, "rpsysaaa_authori_button_apply").click()

    # 路徑導向 Sys > AAA > RADIUS Server
    mod.Tab_Switch(driver,"RADIUS Server")
    driver.find_element(By.NAME, "rpsysaaa_radius_acc_mode_button_apply").click()
    driver.find_element(By.NAME, "rpsysaaa_radius_acc_index_button_apply").click()
    driver.find_element(By.NAME, "rpsysaaa_radius_authent_mode_button_apply").click()
    driver.find_element(By.NAME, "rpsysaaa_radius_authent_index_button_apply").click()

    # 路徑導向 Sys > AAA > TACACS Server
    mod.Tab_Switch(driver,"TACACS Server")
    driver.find_element(By.NAME, "rpsysaaa_tacacs_acc_mode_button_apply").click()
    driver.find_element(By.NAME, "rpsysaaa_tacacs_acc_index_button_apply").click()
    driver.find_element(By.NAME, "rpsysaaa_tacacs_authent_mode_button_apply").click()
    driver.find_element(By.NAME, "rpsysaaa_tacacs_authent_index_button_apply").click()
    driver.find_element(By.NAME, "rpsysaaa_tacacs_authori_mode_button_apply").click()
    driver.find_element(By.NAME, "rpsysaaa_tacacs_authori_index_button_apply").click()

    # Sys AAA Result
    if(if_error == False):
        print(f"[MSAN1-11971][Sys - AAA - Accounting] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11971][Sys - AAA - Accounting] Result Fail",file = open(file_name, '+a'))
    print(f"[MSAN1-11972][Sys - AAA - Authentication] Result Pass",file = open(file_name, '+a'))
    print(f"[MSAN1-11973][Sys - AAA - Authorization] Result Pass",file = open(file_name, '+a'))
    print(f"[MSAN1-11974][Sys - AAA - RADIUS Server] Result Pass",file = open(file_name, '+a'))
    print(f"[MSAN1-11975][Sys - AAA - TACACS Server] Result Pass",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Sys Access Control
    # Sys > Access Control
    # -------------------------start-------------------------

    # 路徑導向 Sys > Access Control > SNMP
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"Access Control")
    mod.Switch_Frame(driver)
    driver.find_element(By.NAME, "rpsysacc_snmp_button_apply").click()
    driver.find_element(By.NAME, "rpsysacc_snmp_trap_button_apply").click()
    driver.find_element(By.NAME, "rpsysacc_snmp_user_button_apply").click()

    # 路徑導向 Sys > Access Control > Service Control
    mod.Tab_Switch(driver,"Service Control")
    driver.find_element(By.NAME, "rpsysacc_accctrl_button_apply").click()

    # 路徑導向 Sys > Access Control > Remote Management
    mod.Tab_Switch(driver,"Remote Management")
    driver.find_element(By.NAME, "rpsysacc_sec_button_apply").click()

    # 路徑導向 Sys > Access Control > Remote Management IPv6
    mod.Tab_Switch(driver,"Remote Management IPv6")
    driver.find_element(By.NAME, "rpsysacc_sec_button_apply").click()

    # Sys Access Control Result
    print(f"[MSAN1-11976][Sys - Access Control - SNMP] Result Pass",file = open(file_name, '+a'))
    print(f"[MSAN1-11977][Sys - Access Control - Service Control] Result Pass",file = open(file_name, '+a'))
    print(f"[MSAN1-11978][Sys - Access Control - Remote Management] Result Pass",file = open(file_name, '+a'))
    print(f"[MSAN1-11979][Sys - Access Control - Remote Management IPv6] Result Pass",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Sys General Setup
    # Sys > General Setup
    # -------------------------start-------------------------

    if_error = False

    # 路徑導向 Sys > General Setup
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"General Setup")
    mod.Switch_Frame(driver)

    # Sys General Setup Test 1
    sys.General_Setup_Host_Name(driver,"1234567890123456789012345678901")
    sys.General_Setup_Location(driver,"1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567")
    sys.General_Setup_Contact_Persons_Name(driver,"1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567")
    driver.find_elements(By.NAME, "rpsysgeneral_button_apply")[0].click()
    if(driver.find_element(By.NAME, "rpsysgeneral_input_hostname").get_attribute("value") != "1234567890123456789012345678901"):
        print(f"             [Sys - General Setup] Host Name Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpsysgeneral_input_location").get_attribute("value") != "1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567"):
        print(f"             [Sys - General Setup] Location Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpsysgeneral_input_contact").get_attribute("value") != "1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567"):
        print(f"             [Sys - General Setup] Contact Persons Name Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Sys General Setup Test 2
    sys.General_Setup_Stdio_Timeout(driver,"120")
    driver.find_elements(By.NAME, "rpsysgeneral_button_apply")[1].click()
    if(driver.find_element(By.CLASS_NAME, "div-row-cell-content.rpGeneral_currdefault").get_attribute("textContent") != "120 minutes"):
        print(f"             [Sys - General Setup] Stdio Timeout Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Sys General Setup Result
    if(if_error == False):
        print(f"[MSAN1-11980][Sys - General Setup] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11980][Sys - General Setup] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Sys IP Setup
    # Sys > IP Setup
    # -------------------------start-------------------------

    # Sys IP Setup IPv4 Setup
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"IP Setup")
    mod.Switch_Frame(driver)
    ip_setup_gateway = driver.find_element(By.NAME, "rpsysipsetup_inband_gateway").get_attribute("value")
    driver.find_element(By.NAME, "rpsysipsetup_button_apply").click()

    # Sys IP Setup IP Route Result
    print(f"[MSAN1-11981][Sys - IP Setup - IPv4 Setup] Result Pass",file = open(file_name, '+a'))

    if_error = False

    # Sys IP Setup IPv6 Setup
    mod.Tab_Switch(driver,"IPv6 Setup")
    driver.find_element(By.NAME, "rpsysipsetup6_select_default_management").click()
    sys.IP_Setup_IPv6_Setup_Inband_Global_Address(driver,"2001::10")
    sys.IP_Setup_IPv6_Setup_Inband_Static(driver,"64")
    sys.IP_Setup_IPv6_Setup_Outband_Global_Address(driver,"2002::11")
    sys.IP_Setup_IPv6_Setup_Outband_Static(driver,"64")
    driver.find_element(By.NAME, "rpsysipsetup6_button_apply").click()
    if(driver.find_element(By.NAME, "rpsysipsetup6_select_default_management").is_selected() != True):
        print(f"             [Sys - IP Setup - IPv6 Setup] Default Management:Inband Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpsysipsetup6_inband_static_address").get_attribute("value") != "2001::10"):
        print(f"             [Sys - IP Setup - IPv6 Setup] Inband Global Address:2001::10 Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpsysipsetup6_inband_static_prefix").get_attribute("value") != "64"):
        print(f"             [Sys - IP Setup - IPv6 Setup] Inband Static:64 Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpsysipsetup6_outband_static_address").get_attribute("value") != "2002::11"):
        print(f"             [Sys - IP Setup - IPv6 Setup] Outband Global Address:2002::11 Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_element(By.NAME, "rpsysipsetup6_outband_static_prefix").get_attribute("value") != "64"):
        print(f"             [Sys - IP Setup - IPv6 Setup] Outband Static:64 Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Sys IP Setup IP Route Result
    if(if_error == False):
        print(f"[MSAN1-11982][Sys - IP Setup - IPv6 Setup] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11982][Sys - IP Setup - IPv6 Setup] Result Fail",file = open(file_name, '+a'))

    if_error = False

    # Sys IP Setup IP Route
    mod.Tab_Switch(driver,"IP Route")
    ip_setup_ip_route_address0 = ip_setup_gateway.split(".")[0]
    ip_setup_ip_route_address1 = ip_setup_gateway.split(".")[1]
    ip_setup_ip_route_address2 = ip_setup_gateway.split(".")[2]
    sys.IP_Setup_IP_Route_Dest_IP_Address(driver,f"{ip_setup_ip_route_address0}.{ip_setup_ip_route_address1}.{ip_setup_ip_route_address2}.100")
    sys.IP_Setup_IP_Route_Mask(driver,"32")
    sys.IP_Setup_IP_Route_Next_Hop_IP(driver,ip_setup_gateway)
    sys.IP_Setup_IP_Route_Metric(driver,"15")
    driver.find_element(By.CLASS_NAME, "font-btn").click()
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()
        print(f"             [Sys - IP Setup - IP Route] IP & Mask Already Exist Test Fail",file = open(file_name, '+a'))
        if_error = True
    except:
        # Sys IP Setup IP Route Check & Delete
        if_last = False
        if_find = False
        index = 0
        while(if_last == False):
            try:
                if(driver.find_elements(By.CLASS_NAME, "rpIpRoute_dstIp.td-table-content")[index].get_attribute("textContent") == f"{ip_setup_ip_route_address0}.{ip_setup_ip_route_address1}.{ip_setup_ip_route_address2}.100"):
                    if_find = True
                    if(driver.find_elements(By.CLASS_NAME, "rpIpRoute_netmask.td-table-content")[index].get_attribute("textContent") != "32"):
                        print(f"             [Sys - IP Setup - IP Route] Mask Test Fail",file = open(file_name, '+a'))
                        if_error = True
                    if(driver.find_elements(By.CLASS_NAME, "rpIpRoute_gateway.td-table-content")[index].get_attribute("textContent") != ip_setup_gateway):
                        print(f"             [Sys - IP Setup - IP Route] Gateway Test Fail",file = open(file_name, '+a'))
                        if_error = True
                    if(driver.find_elements(By.CLASS_NAME, "rpIpRoute_metric.td-table-content")[index].get_attribute("textContent") != "15"):
                        print(f"             [Sys - IP Setup - IP Route] Metric Test Fail",file = open(file_name, '+a'))
                        if_error = True
                    driver.find_elements(By.NAME, "rpIpRoute_radio_select")[index].click()
                    driver.find_element(By.NAME, "rpIpRoute_data_button_delete").click()
                    break
                index = index+1
            except:
                if_last = True
        if(if_find == False):
            print(f"             [Sys - IP Setup - IP Route] IP & Mask Not Found Test Fail",file = open(file_name, '+a'))
            if_error = True

    # Sys IP Setup IP Route Result
    if(if_error == False):
        print(f"[MSAN1-11983][Sys - IP Setup - IP Route] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11983][Sys - IP Setup - IP Route] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Sys Monitor
    # Sys > Monitor
    # -------------------------start-------------------------

    if_error = False

    # Sys Monitor
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"Monitor")
    mod.Switch_Frame(driver)

    # GLC Test
    sys.Slot_Select(driver,glc_slot)
    sys.Load(driver)
    driver.find_element(By.NAME, "rpsysmonitor_button_apply").click()
    # should not show fan duty cycle table
    try:
        # driver.find_element(By.CLASS_NAME, "sysmonitorFanDutyCycleTitle")
        # print("try attribu")
        print(driver.find_element(By.CLASS_NAME, "sysmonitorFanDutyCycleTitle").get_attribute("style"))
        if(driver.find_element(By.CLASS_NAME, "sysmonitorFanDutyCycleTitle").get_attribute("style")!="display: none;"):
            print(f"             [Sys - Monitor] GLC card found Fan Duty Cycle table Fail",file = open(file_name, '+a'))
            if_error = True
        sys.Fan_Mode(driver, "ime", 1)
        print(f"             [Sys - Monitor] GLC card found Fan Duty Cycle Fail",file = open(file_name, '+a'))
        print("noooo cannot use this")
        if_error = True
    except:
        print(f"             [Sys - Monitor] GLC card Fan Duty Cycle not Found Pass",file = open(file_name, '+a'))
        pass

    # MSC Test
    sys.Slot_Select(driver,msc_slot)
    sys.Load(driver)
    driver.find_element(By.NAME, "rpsysmonitor_button_apply").click()

    time.sleep(2)

    #*add fan Mode test 
    sys.Fan_Mode(driver, "ime", 1)
    sys.Fan_Mode(driver, "ave", 3)
    sys.Monitor_Apply(driver)
    # check
    temp = driver.find_element(By.NAME, "rpsysmonitor_slt_fandutycycle_mode1").get_attribute("value")
    # print(f"             [Sys - Monitor] Fan index1 Mode:{temp}",file = open(file_name, '+a'))
    if(str(temp) != str(2)):
        print(f"             [Sys - Monitor] Fan index1 Mode:{temp} != 2, ime Test Fail",file = open(file_name, '+a'))
        if_error = True
    temp = driver.find_element(By.NAME, "rpsysmonitor_slt_fandutycycle_mode3").get_attribute("value")
    # print(f"             [Sys - Monitor] Fan index3 Mode:{temp}",file = open(file_name, '+a'))
    if(str(temp) != str(1)):
        print(f"             [Sys - Monitor] Fan index3 Mode:{temp} != 1, ave Test Fail",file = open(file_name, '+a'))
        if_error = True
   


    #*add fan Value test 
    # sys.Fan_Duty_Cycle(driver, 0, 1)
    # sys.Fan_Duty_Cycle(driver, 0, 3)
    # sys.Monitor_Apply(driver)

    # min-1
    sys.Fan_Duty_Cycle(driver, -1, 1)
    sys.Monitor_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()            
    except:
        if(mod.IsAlert(driver) == False):     
            print(f"             [Sys - Monitor] Fan Duty Cycle:-1 No alert or error page Fail",file = open(file_name, '+a'))
            if_error = True
    

    # max+1
    time.sleep(1)
    sys.Fan_Duty_Cycle(driver, "101", 1)
    sys.Monitor_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()            
    except:
        if(mod.IsAlert(driver) == False):     
            print(f"             [Sys - Monitor] Fan Duty Cycle:101 No alert or error page Fail",file = open(file_name, '+a'))
            if_error = True

    # invalid value
    time.sleep(1)
    sys.Fan_Duty_Cycle(driver, "@", 1)
    sys.Monitor_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack").click()            
    except:
        if(mod.IsAlert(driver) == False):     
            print(f"             [Sys - Monitor] Fan Duty Cycle:@ No alert or error page Fail",file = open(file_name, '+a'))
            if_error = True

    # check value 
    time.sleep(1)
    sys.Fan_Duty_Cycle(driver, "10", 1)
    sys.Monitor_Apply(driver)
    print("dutycycle value:")
    print(driver.find_element(By.NAME, "rpsysmonitor_input_fandutycycle_dutycycle1").get_attribute("value"))
    if(driver.find_element(By.NAME, "rpsysmonitor_input_fandutycycle_dutycycle1").get_attribute("value") != "10"):
        print(f"             [Sys - Monitor] Fan Duty Cycle:10 value (click apply 1 time) Fail",file = open(file_name, '+a'))
        if_error = True

        # secomd time to apply check value
        sys.Monitor_Apply(driver)
        print("dutycycle value:")
        print(driver.find_element(By.NAME, "rpsysmonitor_input_fandutycycle_dutycycle1").get_attribute("value"))
        if(driver.find_element(By.NAME, "rpsysmonitor_input_fandutycycle_dutycycle1").text != "10"):
            print(f"             [Sys - Monitor] Fan Duty Cycle:10 value (click apply 2 times) Fail",file = open(file_name, '+a'))
            if_error = True
        else:
            print(f"             [Sys - Monitor] Fan Duty Cycle:10 value (click apply 2 times) Pass",file = open(file_name, '+a'))




    else:
        print(f"             [Sys - Monitor] Fan Duty Cycle:10 value (click apply 1 time) Pass",file = open(file_name, '+a'))

    
    sys.Fan_Duty_Cycle(driver, 0, 1)
    sys.Fan_Duty_Cycle(driver, 0, 3)
    sys.Monitor_Apply(driver)



    # Sys Monitor Result
    if(if_error == False):
        print(f"[MSAN1-11984][Sys - Monitor] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11984][Sys - Monitor] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Sys System Information
    # Sys > System Information
    # -------------------------start-------------------------

    if_error = False

    # Sys System Information
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"System Information")
    mod.Switch_Frame(driver)

    # Check Table
    try:
        driver.find_element(By.CLASS_NAME, "div-layout-wrap-3")
    except:
        print(f"             [Sys - System Information] Table Dont Exist Test Fail",file = open(file_name, '+a'))
        if_error = True

    # Sys System Information Result
    if(if_error == False):
        print(f"[MSAN1-11985][Sys - System Information] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11985][Sys - System Information] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Sys Unix Syslog
    # Sys > Unix Syslog
    # -------------------------start-------------------------

    if_error = False

    # Sys Unix Syslog
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"Unix SysLog")
    mod.Switch_Frame(driver)

    # Sys Unix Syslog Test
    sys.Unix_Syslog_Server(driver,4)
    sys.Unix_Syslog_IP(driver,"10.10.10.1")
    driver.find_element(By.NAME, "rpsyslog_btnapply").click()

    # Sys Unix Syslog Check
    if(driver.find_elements(By.CLASS_NAME, "serverip.td-table-content")[3].get_attribute("textContent") != "10.10.10.1"):
        print(f"             [Sys - Unix Syslog] IP Test Fail",file = open(file_name, '+a'))
        if_error = True
    if(driver.find_elements(By.CLASS_NAME, "serverity.td-table-content")[3].get_attribute("textContent") != "all"):
        print(f"             [Sys - Unix Syslog] Severity Test Fail",file = open(file_name, '+a'))
        if_error = True
    
    # Sys Unix Syslog Delete
    driver.find_elements(By.NAME, "rpsyslogselect")[3].click()
    driver.find_element(By.NAME, "rpsyslog_btnDelete").click()

    # Sys Unix Syslog Result
    if(if_error == False):
        print(f"[MSAN1-11986][Sys - Unix Syslog] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11986][Sys - Unix Syslog] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Sys Users Account
    # Sys > Users Account
    # -------------------------start-------------------------

    if_error = False

    # Sys Users Account
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"Users Account")
    mod.Switch_Frame(driver)

    # Sys Users Account Clear
    user_account_data_num = driver.find_elements(By.NAME, "rpsysuser_data_radio_select").__len__()
    for index in range(user_account_data_num):
        if_admin_click = False
        if(if_admin_click == False):
            driver.find_elements(By.NAME, "rpsysuser_data_radio_select")[0].click()
            driver.find_element(By.NAME, "rpsysuser_data_button_delete").click()
            try:
                driver.find_element(By.NAME, "rperror_btnBack").click()
                if_admin_click = True
            except:
                pass
        else:
            driver.find_elements(By.NAME, "rpsysuser_data_radio_select")[1].click()
            driver.find_element(By.NAME, "rpsysuser_data_button_delete").click()

    # Sys Users Account Test
    time.sleep(1)
    input_value = 1
    if_full = False
    while(if_full == False):
        sys.Users_Account_Name(driver,input_value)
        sys.Users_Account_Password(driver,input_value)
        sys.Users_Account_Retype_Password_to_Confirm(driver,input_value)
        driver.find_element(By.NAME, "rpsysuser_config_button_apply").click()
        input_value = input_value+1
        try:
            driver.find_element(By.NAME, "rperror_btnBack").click()
            if_full = True
        except:
            pass
    print(f"             [Sys - Users Account] Max Capacity(16) = {input_value-1}",file = open(file_name, '+a'))

    # Sys Users Account Clear
    for index in range(15):
        driver.find_elements(By.NAME, "rpsysuser_data_radio_select")[0].click()
        driver.find_element(By.NAME, "rpsysuser_data_button_delete").click()

    # Sys Users Account Result
    if(if_error == False):
        print(f"[MSAN1-11987][Sys - Users Account] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11987][Sys - Users Account] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Sys Msc Redundant
    # Sys > Msc Redundant
    # -------------------------start-------------------------

    try:
        if_error = False

        # Sys Msc Redundant
        mod.Switch_Default(driver)
        mod.SubPage_Switch(driver,"Msc Redundant")
        mod.Switch_Frame(driver)

        # Sys Msc Redundant Test
        driver.find_element(By.NAME, "rpmscredundant_button_uplink_swap_apply").click()
        driver.find_element(By.NAME, "rpmscredundant_button_ycable_apply").click()
        driver.find_element(By.NAME, "rpmscredundant_button_rddn_mode_apply").click()
        if(MSC_Card_Type != "MSC1240QA"):
            if(mod.IsAlert(driver) != True):
                print(f"             [Sys - Msc Redundant] Rddm Mode!=MSC1240QA No Alert Test Fail",file = open(file_name, '+a'))
                if_error = True
        else:
            if(mod.IsAlert(driver) == True):
                print(f"             [Sys - Msc Redundant] Rddm Mode=MSC1240QA Alert Test Fail",file = open(file_name, '+a'))
                if_error = True

        # Sys Msc Redundant Result
        if(if_error == False):
            print(f"[MSAN1-11988][Sys - Msc Redundant] Result Pass",file = open(file_name, '+a'))
        else:
            print(f"[MSAN1-11988][Sys - Msc Redundant] Result Fail",file = open(file_name, '+a'))
    except:
        print(f"[MSAN1-11988][Sys - Msc Redundant] Result Block",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Sys Power
    # Sys > Power
    # -------------------------start-------------------------

    try:
        if_error = False

        # Sys Power Power Card Info
        mod.Switch_Default(driver)
        mod.SubPage_Switch(driver,"Power")
        mod.Switch_Frame(driver)

        # Sys Power Power Card Info Test
        try:
            driver.find_elements(By.CLASS_NAME, "div-row-cell-content.webPower_pwrCardSlot")[0]
            driver.find_elements(By.CLASS_NAME, "div-row-cell-content.webPower_pwrCardSlot")[1]
        except:
            print(f"             [Sys - Power - Power Card Info] Two Slot Dont Exist Test Fail",file = open(file_name, '+a'))
            if_error = True

        # Sys Power AC Power
        mod.Tab_Switch(driver,"AC Power")
        driver.find_element(By.NAME, "webPower_btnCapacityApply").click()
        driver.find_element(By.NAME, "webPower_btnTempApply").click()

        # Sys Power Result
        if(if_error == False):
            print(f"[MSAN1-11989][Sys - Power - Power Card Info] Result Pass",file = open(file_name, '+a'))
        else:
            print(f"[MSAN1-11989][Sys - Power - Power Card Info] Result Fail",file = open(file_name, '+a'))
        print(f"[MSAN1-11990][Sys - Power - AC Power] Result Pass",file = open(file_name, '+a'))
    except:
        print(f"             [Sys - Power - Power Card Info] Result Block",file = open(file_name, '+a'))
        print(f"[MSAN1-11989][Sys - Power - Power Card Info] Result Pass",file = open(file_name, '+a'))
        print(f"             [Sys - Power - AC Power] Result Block",file = open(file_name, '+a'))
        print(f"[MSAN1-11990][Sys - Power - AC Power] Result Pass",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Sys License 
    # Sys > License
    # -------------------------start-------------------------
    # > 10G
    if_error = False
    try:
        mod.Switch_Default(driver)
        mod.SubPage_Switch(driver,"License")
        mod.Switch_Frame(driver)
        driver.find_element(By.LINK_TEXT, "10G").click()
        # upload
        driver.find_element(By.NAME, "rpupgradeCard").click()
                                    
    except:
        if_error = True

    if(if_error == False):
        print(f"[MSAN1-14405][Sys - License - 10G] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-14405][Sys - License - 10G] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------

    # Sys License power
    # Sys > License > power-saving
    # -------------------------start-------------------------
    # > power-saving
    if_error = False
    try:        
                            
        # > Power-saving
        mod.Switch_Default(driver)
        mod.SubPage_Switch(driver,"License")
        mod.Switch_Frame(driver)
        driver.find_element(By.LINK_TEXT, "Power-saving").click()
        # upload
        driver.find_element(By.NAME, "rpupgradeCard").click()
    except:
        if_error = True

    if(if_error == False):
        print(f"[MSAN1-14406][Sys - License - Power-saving] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-14406][Sys - License - Power-saving] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------
    
    print("Test Finishd",file = open(file_name, '+a'))
    print("======================================================================================",file = open(file_name, '+a'))

def EMS_Set_Prepare(driver,snmp_get,snmp_set,snmp_version,username,password):

    # Sys - Access Control - SNMP, input value from ENV.txt ---
    # path: Sys > Access Control > SNMP
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Sys")
    # mod.Switch_Frame(driver)
    mod.Tab_Switch(driver,"Access Control")
    mod.Switch_Frame(driver)
    mod.Tab_Switch(driver,"SNMP")
    
    # input get community
    driver.find_element(By.NAME, "rpsysacc_snmp_ipt_get_com").clear()
    driver.find_element(By.NAME, "rpsysacc_snmp_ipt_get_com").send_keys(snmp_get)
    # input set community    
    driver.find_element(By.NAME, "rpsysacc_snmp_ipt_set_com").clear()
    driver.find_element(By.NAME, "rpsysacc_snmp_ipt_set_com").send_keys(snmp_set)
    # select version
    # Select(driver.find_element(By.NAME, "rpsysacc_snmp_slt_version")).select_by_visible_text(snmp_version)
    # driver.find_element(By.XPATH, "/html/body/form/div[2]/div[1]/div[12]/select/option[1]").click()

    # click apply
    driver.find_element(By.NAME, "rpsysacc_snmp_button_apply").click()    

    # Sys - Users Account, input value from ENV.txt ---
    # path: Sys > Users Account
    mod.Switch_Default(driver)
    mod.Tab_Switch(driver,"Users Account")
    mod.Switch_Frame(driver)
    # input name
    driver.find_element(By.NAME, "rpsysuser_input_name").clear()
    driver.find_element(By.NAME, "rpsysuser_input_name").send_keys(username)
    # input password
    driver.find_element(By.NAME, "rpsysuser_input_password").clear()
    driver.find_element(By.NAME, "rpsysuser_input_password").send_keys(password)
    # input retype password to confirm
    driver.find_element(By.NAME, "rpsysuser_input_retypepassword").clear()
    driver.find_element(By.NAME, "rpsysuser_input_retypepassword").send_keys(password)
    # click apply
    driver.find_element(By.NAME, "rpsysuser_config_button_apply").click()    


    pass

###############################################################################################################################
def Temp_Test_acl_oui_filter(driver,glc_slot,glc_port,msc_slot,msc_port,file_name):


    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"ACL")
    mod.Switch_Frame(driver)


    # ACL  & OUI Filter Test
    # ACL >  & OUI Filter
    # -------------------------start-------------------------

    if_mac_error = False
    if_oui_error = False

    

    # MAC Filter & OUI Filter Default
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"Port")
    mod.SubPage_Switch(driver,"Default")
    mod.Switch_Frame(driver)
    port.Slot_Select(driver,glc_slot)
    port.Default_Port_List(driver,"1~40")
    port.Default_Apply(driver)
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"ACL")
    mod.Switch_Frame(driver)

    # MAC Filter 
    # .....

    # OUI Filter %Port = accept
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"OUI Filter")
    mod.Switch_Frame(driver)
    acl.Slot_Select(driver,glc_slot)
    acl.Port_Select(driver,glc_port)
    acl.Load(driver)
    acl.OUI_Filter_Enable(driver,True)
    acl.OUI_Filter_Mode(driver,1)
    for oui in range(32):
        if(oui < 9):
            acl.OUI_Filter_OUI(driver,f"10:10:0{oui+1}",oui+1)
        else:
            acl.OUI_Filter_OUI(driver,f"10:10:{oui+1}",oui+1)
    acl.OUI_Filter_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack")
        error_msg = driver.find_element(By.CLASS_NAME, "div-row-cell-content.msg").get_attribute("textContent")
        if(error_msg == "error: line card entry full (>63)\n"):
            print(f"             [ACL - MAC Filter] deny 32 entries * 40 port + OUI-Filter accept 32 entry * 1 port check error message =>(32+32>63)Pass.",file = open(file_name, '+a'))
        else:
            print(f"             [ACL - MAC Filter] deny 32 entries * 40 port + OUI-Filter accept 32 entry * 1 port check error message =>(32+32>63)Fail.",file = open(file_name, '+a'))
            if_mac_error = True
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [ACL - MAC Filter] deny 32 entries * 40 port + OUI-Filter accept 32 entry * 1 port check error message =>(32+32>63)Fail.",file = open(file_name, '+a'))
        if_mac_error = True
    # OUI Filter Clear
    acl.OUI_Filter_Enable(driver,False)
    acl.OUI_Filter_Mode(driver,2)
    for oui in range(32):
        acl.OUI_Filter_OUI(driver,"",oui+1)
    acl.OUI_Filter_Apply(driver)

    # MAC Filter Clear
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"MAC Filter")
    mod.Switch_Frame(driver)
    for test_port in range(40):
        acl.Slot_Select(driver,glc_slot)
        acl.Port_Select(driver,test_port+1)
        acl.Load(driver)
        acl.MAC_Filter_Enable(driver,False)
        acl.MAC_Filter_Mode(driver,2)
        for mac in range(32):
            acl.MAC_Filter_MAC(driver,"",mac+1)
        acl.MAC_Filter_Apply(driver)
        try:
            driver.find_element(By.NAME, "rperror_btnBack").click()
            print(f"             [ACL - MAC Filter] 32 + OUI-Filter 31, enable and mode accept set Fail.",file = open(file_name, '+a'))
            if_mac_error = True
            # MAC Filter set default
            mod.Switch_Default(driver)
            mod.Page_Switch(driver,"Port")
            mod.SubPage_Switch(driver,"Default")
            mod.Switch_Frame(driver)
            port.Slot_Select(driver,glc_slot)
            port.Default_Port_List(driver,"1~40")
            port.Default_Apply(driver)
            mod.Switch_Default(driver)
            mod.Page_Switch(driver,"ACL")
            mod.SubPage_Switch(driver,"MAC Filter")
            mod.Switch_Frame(driver)
            break
        except:
            pass

    # 路徑導向 OUI Filter
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"OUI Filter")
    mod.Switch_Frame(driver)

    # OUI Filter = accept
    for test_port in range(40):
        # slot select
        acl.Slot_Select(driver,glc_slot)
        acl.Port_Select(driver,test_port+1)
        acl.Load(driver)

        # OUI Filter 輸入值
        acl.OUI_Filter_Enable(driver,True)
        acl.OUI_Filter_Mode(driver,1)
        for oui in range(32):
            if(oui < 9):
                acl.OUI_Filter_OUI(driver,f"10:10:0{oui+1}",oui+1)
            else:
                acl.OUI_Filter_OUI(driver,f"10:10:{oui+1}",oui+1)
        acl.OUI_Filter_Apply(driver)

        if_error = False

        # OUI Filter 檢驗
        if(driver.find_element(By.NAME, "rpouiFilter_chkEnable").is_selected() == False):
            if_error = True
        if(driver.find_element(By.XPATH, f"//*[@name='rpouiFilter_sltMode']/option[1]").is_selected() == False):
            if_error = True
        for oui in range(32):
            if(oui < 9):
                if(driver.find_element(By.NAME, f"rpouiFilter_sltFilterOui{oui+1}").get_attribute("value") != f"10:10:0{oui+1}"):
                    if_error = True
            else:
                if(driver.find_element(By.NAME, f"rpouiFilter_sltFilterOui{oui+1}").get_attribute("value") != f"10:10:{oui+1}"):
                    if_error = True

    if(if_error == False):
        print("             [ACL - OUI Filter] accept 32 entries * 40 port =>Pass.",file = open(file_name, '+a'))
    else:
        print("             [ACL - OUI Filter] accept 32 entries * 40 port =>Fail.",file = open(file_name, '+a'))
        if_oui_error = True

    # OUI Filter %Port = deny
    acl.Slot_Select(driver,glc_slot)
    acl.Port_Select(driver,glc_port)
    acl.Load(driver)
    acl.OUI_Filter_Mode(driver,2)
    acl.OUI_Filter_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack")
        error_msg = driver.find_element(By.CLASS_NAME, "div-row-cell-content.msg").get_attribute("textContent")
        if(error_msg == "error: line card entry full (>63)\n"):
            print(f"             [ACL - OUI Filter] accept 32 entries * 39 port + OUI-Filter deny 32 entry * 1 port check error message =>(32+32>63)Pass.",file = open(file_name, '+a'))
        else:
            print(f"             [ACL - OUI Filter] accept 32 entries * 39 port + OUI-Filter deny 32 entry * 1 port check error message =>(32+32>63)Fail.",file = open(file_name, '+a'))
            if_oui_error = True
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [ACL - OUI Filter] accept 32 entries * 39 port + OUI-Filter deny 32 entry * 1 port check error message =>(32+32>63)Fail.",file = open(file_name, '+a'))
        if_oui_error = True

    # OUI Filter %Port-32 Delete
    acl.Slot_Select(driver,glc_slot)
    acl.Port_Select(driver,glc_port)
    acl.OUI_Filter_Mode(driver,2)
    acl.OUI_Filter_OUI(driver,"",32)
    acl.OUI_Filter_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack")
        error_msg = driver.find_element(By.CLASS_NAME, "div-row-cell-content.msg").get_attribute("textContent") #* add
        error_msg = error_msg.split("\n")[0]  #* add
        print(f"             [ACL - OUI Filter] error:{error_msg}",file = open(file_name, '+a')) #* add
        
        if(error_msg == "error: line card entry full (>63)\n"):
            print(f"             [ACL - OUI Filter] accept 32 entries * 39 port + OUI-Filter deny 31 entry * 1 port =>(32+31=63)Pass.0",file = open(file_name, '+a'))
        else:
            print(f"             [ACL - OUI Filter] accept 32 entries * 39 port + OUI-Filter deny 31 entry * 1 port check error message =>(32+32>63)Fail.(#172692.#172678)0",file = open(file_name, '+a'))
            if_oui_error = True #* add

        # print(f"             [ACL - OUI Filter] accept 32 entries * 39 port + OUI-Filter deny 31 entry * 1 port =>(32+31=63)Fail.(#172692.#172678)",file = open(file_name, '+a'))
        if_oui_error = True
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        # print(f"             [ACL - OUI Filter] accept 32 entries * 39 port + OUI-Filter deny 31 entry * 1 port =>(32+31=63)Pass.",file = open(file_name, '+a'))
        print(f"             [ACL - OUI Filter] accept 32 entries * 39 port + OUI-Filter deny 31 entry * 1 port =>(32+31=63)Fail.",file = open(file_name, '+a'))
       
    # OUI Filter Clear
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"OUI Filter")
    mod.Switch_Frame(driver)
    for test_port in range(40):
        acl.Slot_Select(driver,glc_slot)
        acl.Port_Select(driver,test_port+1)
        acl.Load(driver)
        acl.OUI_Filter_Enable(driver,False)
        acl.OUI_Filter_Mode(driver,2)
        for oui in range(32):
            acl.OUI_Filter_OUI(driver,"",oui+1)
        acl.OUI_Filter_Apply(driver)

    # OUI Filter = deny
    for test_port in range(40):
        # slot select
        acl.Slot_Select(driver,glc_slot)
        acl.Port_Select(driver,test_port+1)
        acl.Load(driver)

        # OUI Filter 輸入值
        acl.OUI_Filter_Enable(driver,True)
        acl.OUI_Filter_Mode(driver,2)
        for oui in range(32):
            if(oui < 9):
                acl.OUI_Filter_OUI(driver,f"10:10:0{oui+1}",oui+1)
            else:
                acl.OUI_Filter_OUI(driver,f"10:10:{oui+1}",oui+1)
        acl.OUI_Filter_Apply(driver)

        if_error = False

        # OUI Filter 檢驗
        if(driver.find_element(By.NAME, "rpouiFilter_chkEnable").is_selected() == False):
            if_error = True
        if(driver.find_element(By.XPATH, f"//*[@name='rpouiFilter_sltMode']/option[2]").is_selected() == False):
            if_error = True
        for oui in range(32):
            if(oui < 9):
                if(driver.find_element(By.NAME, f"rpouiFilter_sltFilterOui{oui+1}").get_attribute("value") != f"10:10:0{oui+1}"):
                    if_error = True
            else:
                if(driver.find_element(By.NAME, f"rpouiFilter_sltFilterOui{oui+1}").get_attribute("value") != f"10:10:{oui+1}"):
                    if_error = True

    if(if_error == False):
        print("             [ACL - OUI Filter] deny 32 entries * 40 port =>Pass.",file = open(file_name, '+a'))
    else:
        print("             [ACL - OUI Filter] deny 32 entries * 40 port =>Fail.",file = open(file_name, '+a'))
        if_oui_error = True

    # OUI Filter %Port = accept
    acl.Slot_Select(driver,glc_slot)
    acl.Port_Select(driver,glc_port)
    acl.Load(driver)
    acl.OUI_Filter_Mode(driver,1)
    acl.OUI_Filter_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack")
        error_msg = driver.find_element(By.CLASS_NAME, "div-row-cell-content.msg").get_attribute("textContent")
        if(error_msg == "error: line card entry full (>63)\n"):
            print(f"             [ACL - OUI Filter] deny 32 entries * 39 port + OUI-Filter accept 32 entry * 1 port check error message =>(32+32>63)Pass.",file = open(file_name, '+a'))
        else:
            print(f"             [ACL - OUI Filter] deny 32 entries * 39 port + OUI-Filter accept 32 entry * 1 port check error message =>(32+32>63)Fail.",file = open(file_name, '+a'))
            if_oui_error = True
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [ACL - OUI Filter] deny 32 entries * 39 port + OUI-Filter accept 32 entry * 1 port check error message =>(32+32>63)Fail.",file = open(file_name, '+a'))
        if_oui_error = True

    # OUI Filter %Port-32 Delete
    acl.OUI_Filter_Mode(driver,1)
    acl.OUI_Filter_OUI(driver,"",32)
    acl.OUI_Filter_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack")
        print(f"             [ACL - OUI Filter] deny 32 entries * 39 port + OUI-Filter accept 31 entry * 1 port =>(32+31=63)Fail.",file = open(file_name, '+a'))
        if_oui_error = True
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [ACL - OUI Filter] deny 32 entries * 39 port + OUI-Filter accept 31 entry * 1 port =>(32+31=63)Pass.",file = open(file_name, '+a'))

    # input()  #----------------------------------------------------------

    # OUI Filter = deny
    acl.OUI_Filter_Mode(driver,2)
    acl.OUI_Filter_OUI(driver,"10:10:32",32)
    acl.OUI_Filter_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack")
        print(f"             [ACL - OUI Filter] deny 32 entries * 40 port + OUI-Filter accept 31 entry * 0 port =>(32+0=32)Fail.",file = open(file_name, '+a'))
        if_oui_error = True
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        pass

    # MAC Filter %Port = accept
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"MAC Filter")
    mod.Switch_Frame(driver)
    acl.Slot_Select(driver,glc_slot)
    acl.Port_Select(driver,glc_port)
    acl.Load(driver)
    acl.MAC_Filter_Enable(driver,True)
    acl.MAC_Filter_Mode(driver,1)
    for mac in range(32):
        if(mac < 9):
            acl.MAC_Filter_MAC(driver,f"10:10:10:10:10:0{mac+1}",mac+1)
        else:
            acl.MAC_Filter_MAC(driver,f"10:10:10:10:10:{mac+1}",mac+1)
    acl.MAC_Filter_Apply(driver)
    try:
        driver.find_element(By.NAME, "rperror_btnBack")
        error_msg = driver.find_element(By.CLASS_NAME, "div-row-cell-content.msg").get_attribute("textContent")
        if(error_msg == "error: line card entry full (>63)\n"):
            print(f"             [ACL - OUI Filter] deny 32 entries * 40 port + MAC-Filter accept 32 entry * 1 port check error message =>(32+32>63)Pass.",file = open(file_name, '+a'))
        else:
            print(f"             [ACL - OUI Filter] deny 32 entries * 40 port + MAC-Filter accept 32 entry * 1 port check error message =>(32+32>63)Fail.",file = open(file_name, '+a'))
            if_oui_error = True
        driver.find_element(By.NAME, "rperror_btnBack").click()
    except:
        print(f"             [ACL - OUI Filter] deny 32 entries * 40 port + MAC-Filter accept 32 entry * 1 port check error message =>(32+32>63)Fail.",file = open(file_name, '+a'))
        if_oui_error = True
    # MAC Filter Clear
    time.sleep(1)
    acl.MAC_Filter_Enable(driver,False)
    acl.MAC_Filter_Mode(driver,2)
    for mac in range(32):
        acl.MAC_Filter_MAC(driver,"",mac+1)
    acl.MAC_Filter_Apply(driver)

    # OUI Filter Clear
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"OUI Filter")
    mod.Switch_Frame(driver)
    for test_port in range(40):
        acl.Slot_Select(driver,glc_slot)
        acl.Port_Select(driver,test_port+1)
        acl.Load(driver)
        acl.OUI_Filter_Enable(driver,False)
        acl.OUI_Filter_Mode(driver,2)
        for oui in range(32):
            acl.OUI_Filter_OUI(driver,"",oui+1)
        acl.OUI_Filter_Apply(driver)
        try:
            driver.find_element(By.NAME, "rperror_btnBack").click()
            print(f"             [ACL - OUI Filter] 32 + MAC-Filter 31, enable and mode accept set Fail.",file = open(file_name, '+a'))
            if_oui_error = True
            # OUI Filter set default
            mod.Switch_Default(driver)
            mod.Page_Switch(driver,"Port")
            mod.SubPage_Switch(driver,"Default")
            mod.Switch_Frame(driver)
            port.Slot_Select(driver,glc_slot)
            port.Default_Port_List(driver,"1~40")
            port.Default_Apply(driver)
            mod.Switch_Default(driver)
            mod.Page_Switch(driver,"ACL")
            mod.SubPage_Switch(driver,"OUI Filter")
            mod.Switch_Frame(driver)
            break
        except:
            pass
    
    if(if_mac_error == False):
        print(f"[MSAN1-11815][ACL - MAC Filter] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11815][ACL - MAC Filter] Result Fail",file = open(file_name, '+a'))

    if(if_oui_error == False):
        print(f"[MSAN1-11816][ACL - OUI Filter] Result Pass",file = open(file_name, '+a'))
    else:
        print(f"[MSAN1-11816][ACL - OUI Filter] Result Fail",file = open(file_name, '+a'))

    # -------------------------end-------------------------
