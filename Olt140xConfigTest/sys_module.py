from selenium.webdriver.common.by import By
from operator import index
from os import times
import time
from attr import field
from pyrsistent import s
import selenium_module as mod
from selenium.webdriver.support.ui import Select

def Slot_Select(driver,slot):
    retry = True
    while(retry == True):
        try:
            driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlot']/option[{slot}]").click()
        except:
            time.sleep(1)
        try:
            if(driver.find_element(By.XPATH, f"//*[@name='lctbl_selSlot']/option[{slot}]").is_selected() == True):
                retry = False
        except:
            time.sleep(1)

def Port_Select(driver,port):
    retry = True
    while(retry == True):
        try:
            driver.find_element(By.XPATH, f"//*[@name='lctbl_selPort']/option[{port}]").click()
        except:
            time.sleep(1)
        try:
            if(driver.find_element(By.XPATH, f"//*[@name='lctbl_selPort']/option[{port}]").is_selected() == True):
                retry = False
        except:
            time.sleep(1)

def Load(driver):
    driver.find_element(By.NAME, "lctbl_selLoad").click()

# AAA

# AAA > Accounting

def AAA_Accounting_Update_Period(driver,value):
    input = driver.find_element(By.NAME, f"rpsysaaa_acc_input_period")
    input.clear()
    input.send_keys(value)

def AAA_Accounting_Update_System_Active(driver,request):
    check_box = driver.find_element(By.NAME, f"rpsysaaa_acc_sys_action")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def AAA_Accounting_Update_Exec_Active(driver,request):
    check_box = driver.find_element(By.NAME, f"rpsysaaa_acc_exec_action")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def AAA_Accounting_Update_Commands_Active(driver,request):
    check_box = driver.find_element(By.NAME, f"rpsysaaa_acc_com_action")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

# AAA > Authentication

def AAA_Authentication_Enable_Try_Cont(driver,request):
    check_box = driver.find_element(By.NAME, f"rpsysaaa_authent_enable_chkbox_try_cont")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def AAA_Authentication_Login_Try_Cont(driver,request):
    check_box = driver.find_element(By.NAME, f"rpsysaaa_authent_login_chkbox_try_cont")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

# AAA > Authorization

# AAA > RADIUS Server

# AAA > TACACS Server

# Access Control

# Access Control > SNMP

# Access Control > Service Control

# Access Control > Remote Management

# Access Control > Remote Management IPv6

# General Setup

def General_Setup_Host_Name(driver,value):
    input = driver.find_element(By.NAME, f"rpsysgeneral_input_hostname")
    input.clear()
    input.send_keys(value)

def General_Setup_Location(driver,value):
    input = driver.find_element(By.NAME, f"rpsysgeneral_input_location")
    input.clear()
    input.send_keys(value)

def General_Setup_Contact_Persons_Name(driver,value):
    input = driver.find_element(By.NAME, f"rpsysgeneral_input_contact")
    input.clear()
    input.send_keys(value)

def General_Setup_Stdio_Timeout(driver,value):
    input = driver.find_element(By.NAME, f"rpsysgeneral_input_stdiodefault")
    input.clear()
    input.send_keys(value)

def General_Setup_Time_Server_Type(driver,text):
    Select(driver.find_element(By.NAME, "rpsysgeneral_slt_time_server_type")).select_by_visible_text(text)

def General_Setup_Time_Server_IP_Address(driver,value):
    input = driver.find_element(By.NAME, f"rpsysgeneral_input_timeserver_ip")
    input.clear()
    input.send_keys(value)

def General_Setup_Time_Server_IP_Address_1(driver,value):
    input = driver.find_element(By.NAME, f"rpsysgeneral_input_timeserver_1_ip")
    input.clear()
    input.send_keys(value)

def General_Setup_Time_Server_IP_Address_2(driver,value):
    input = driver.find_element(By.NAME, f"rpsysgeneral_input_timeserver_2_ip")
    input.clear()
    input.send_keys(value)

def General_Setup_Sync(driver):
    driver.find_element(By.NAME, "rpsysgeneral_button_timeserver_sync").click()

def General_Setup_Time_Zone(driver,text):
    Select(driver.find_element(By.NAME, "rpsysgeneral_slt_time_zone")).select_by_visible_text(text)

def General_Setup_Apply(driver):
    driver.find_element(By.NAME, "rpsysgeneral_button_timeserver_apply").click()

# IP Setup

# IP Setup > IPv4 Setup

# IP Setup > IPv6 Setup

def IP_Setup_IPv6_Setup_Inband_Default_Gateway(driver,value):
    input = driver.find_element(By.NAME, f"rpsysipsetup6_inband_default_gateway")
    input.clear()
    input.send_keys(value)

def IP_Setup_IPv6_Setup_Inband_Global_Address(driver,value):
    input = driver.find_element(By.NAME, f"rpsysipsetup6_inband_static_address")
    input.clear()
    input.send_keys(value)

def IP_Setup_IPv6_Setup_Inband_Static(driver,value):
    input = driver.find_element(By.NAME, f"rpsysipsetup6_inband_static_prefix")
    input.clear()
    input.send_keys(value)

def IP_Setup_IPv6_Setup_Outband_Global_Address(driver,value):
    input = driver.find_element(By.NAME, f"rpsysipsetup6_outband_static_address")
    input.clear()
    input.send_keys(value)

def IP_Setup_IPv6_Setup_Outband_Static(driver,value):
    input = driver.find_element(By.NAME, f"rpsysipsetup6_outband_static_prefix")
    input.clear()
    input.send_keys(value)

# IP Setup > IP Route

def IP_Setup_IP_Route_Dest_IP_Address(driver,value):
    input = driver.find_element(By.NAME, f"rpIpRoute_inputDstIp")
    input.clear()
    input.send_keys(value)

def IP_Setup_IP_Route_Mask(driver,value):
    input = driver.find_element(By.NAME, f"rpIpRoute_inputNetmask")
    input.clear()
    input.send_keys(value)

def IP_Setup_IP_Route_Next_Hop_IP(driver,value):
    input = driver.find_element(By.NAME, f"rpIpRoute_inputGateway")
    input.clear()
    input.send_keys(value)

def IP_Setup_IP_Route_Metric(driver,value):
    input = driver.find_element(By.NAME, f"rpIpRoute_inputMetric")
    input.clear()
    input.send_keys(value)

# Monitor

def Monitor_Voltage_High_limit(driver,index,value):
    input = driver.find_elements(By.NAME, "rpsysmonitor_input_vol_high")[index-1]
    input.clear()
    input.send_keys(value)

def Monitor_Voltage_Low_limit(driver,index,value):
    input = driver.find_elements(By.NAME, "rpsysmonitor_input_vol_low")[index-1]
    input.clear()
    input.send_keys(value)

def Monitor_Apply(driver):
    driver.find_element(By.NAME, "rpsysmonitor_button_apply").click()

def Monitor_Cancel(driver):
    driver.find_element(By.NAME, "rpsysmonitor_button_cancel").click()

def Fan_Mode(driver, text, index):
    driver.find_elements(By.NAME, f"rpsysmonitor_rdoDutyCycle{index}")[1].click()
    Select(driver.find_element(By.NAME, f"rpsysmonitor_slt_fandutycycle_mode{index}")).select_by_visible_text(text)

def Fan_Duty_Cycle(driver, value, index):
    try:
        driver.find_elements(By.NAME, f"rpsysmonitor_rdoDutyCycle{index}")[0].click()
    except:
        pass
    driver.find_element(By.NAME, f"rpsysmonitor_input_fandutycycle_dutycycle{index}").clear()
    driver.find_element(By.NAME, f"rpsysmonitor_input_fandutycycle_dutycycle{index}").send_keys(value)


# System Information

# Unix Syslog

def Unix_Syslog_Server(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpSyslog_server']/option[{sel}]").click()

def Unix_Syslog_IP(driver,value):
    input = driver.find_element(By.NAME, f"rpSyslog_ip")
    input.clear()
    input.send_keys(value)

# Users Account

def Users_Account_Name(driver,value):
    input = driver.find_element(By.NAME, f"rpsysuser_input_name")
    input.clear()
    input.send_keys(value)

def Users_Account_Password(driver,value):
    input = driver.find_element(By.NAME, f"rpsysuser_input_password")
    input.clear()
    input.send_keys(value)

def Users_Account_Retype_Password_to_Confirm(driver,value):
    input = driver.find_element(By.NAME, f"rpsysuser_input_retypepassword")
    input.clear()
    input.send_keys(value)

# Msc Redundant

# Power

# Power > Power Card Info

# Power > AC Power

