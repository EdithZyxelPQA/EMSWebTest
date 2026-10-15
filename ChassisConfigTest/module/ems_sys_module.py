from operator import index
from os import times
import time
from attr import field
from pyrsistent import s
import module.selenium_module as mod
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import module.ems_module as e_mod

from selenium.webdriver.common.keys import Keys
# .clear() -> .send_keys(Keys.CONTROL + 'a')


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
    input.send_keys(Keys.CONTROL + 'a')
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

# General Setup #

def General_Setup_Host_Name(driver,value):
    input = driver.find_element(By.ID, f"sys_generalsetup_hostname_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def General_Setup_Location(driver,value):
    input = driver.find_element(By.ID, f"sys_generalsetup_location_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def General_Setup_Contact_Persons_Name(driver,value):
    input = driver.find_element(By.ID, f"sys_generalsetup_personname_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def General_Setup_Product_Model(driver,value):
    input = driver.find_element(By.ID, f"sys_generalsetup_model_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def General_Setup_System_Up_Time(driver,value):
    input = driver.find_element(By.ID, f"sys_generalsetup_uptime_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def General_Setup_Stdio_Default(driver,value):
    input = driver.find_element(By.ID, f"sys_generalsetup_stdio_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)    

def General_Setup_Apply_1(driver):
    driver.find_element(By.ID, "sys_generalsetup_apply_button").click()

def General_Setup_Apply_2(driver):
    driver.find_element(By.ID, "sys_generalsetup_apply2_button").click()

# def General_Setup_Stdio_Timeout(driver,value):
#     input = driver.find_element(By.NAME, f"rpsysgeneral_input_stdiodefault")
#     input.send_keys(Keys.CONTROL + 'a')
#     input.send_keys(value)

def General_Setup_Time_Server_Enable(driver,text):
    Select(driver.find_element(By.ID, "sys_generalsetup_timeserver_select")).select_by_visible_text(text)

def General_Setup_Time_Server_Type(driver,text):
    Select(driver.find_element(By.ID, "sys_generalsetup_timeservertype_select")).select_by_visible_text(text)

def General_Setup_Time_Server_IP_Address_1(driver,value):
    input = driver.find_element(By.ID, f"sys_generalsetup_timeserveripaddress1_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def General_Setup_Time_Server_IP_Address_2(driver,value):
    input = driver.find_element(By.ID, f"sys_generalsetup_timeserveripaddress2_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def General_Setup_Time_Server_IP_Address_1_Delete(driver):
    driver.find_element(By.ID, "sys_generalsetup_deleteaddress1_button").click()

def General_Setup_Time_Server_IP_Address_2_Delete(driver):
    driver.find_element(By.ID, "sys_generalsetup_deleteaddress2_button").click()

def General_Setup_Sync(driver):
    driver.find_element(By.ID, "sys_generalsetup_sync_button").click()

def General_Setup_New_Date_Year(driver,year,month,day):
    input = driver.find_element(By.ID, f"sys_generalsetup_newdate_year_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(year)
    input = driver.find_element(By.ID, f"sys_generalsetup_newdate_mouth_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(month)
    input = driver.find_element(By.ID, f"sys_generalsetup_newdate_day_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(day)    

def General_Setup_Time_Zone(driver,text):
    Select(driver.find_element(By.ID, "sys_generalsetup_timezone_select")).select_by_visible_text(text)

def General_Setup_Daylight_Saving_Time(driver,request):
    e_mod.Checkbox_EMS(driver,"sys_generalsetup_daylight_checkbox",request)

def General_Setup_StartDate(driver,text1,text2,text3,text4):
    Select(driver.find_element(By.ID, "sys_generalsetup_startdate1_select")).select_by_visible_text(text1)
    Select(driver.find_element(By.ID, "sys_generalsetup_startdate2_select")).select_by_visible_text(text2)
    Select(driver.find_element(By.ID, "sys_generalsetup_startdate3_select")).select_by_visible_text(text3)
    Select(driver.find_element(By.ID, "sys_generalsetup_startdate4_select")).select_by_visible_text(text4)

def General_Setup_EndDate(driver,text1,text2,text3,text4):
    Select(driver.find_element(By.ID, "sys_generalsetup_enddate1_select")).select_by_visible_text(text1)
    Select(driver.find_element(By.ID, "sys_generalsetup_enddate2_select")).select_by_visible_text(text2)
    Select(driver.find_element(By.ID, "sys_generalsetup_enddate3_select")).select_by_visible_text(text3)
    Select(driver.find_element(By.ID, "sys_generalsetup_enddate4_select")).select_by_visible_text(text4)

def General_Setup_Apply_3(driver):
    driver.find_element(By.ID, "sys_generalsetup_apply3_button").click()

# IP Setup

# IP Setup > IPv4 Setup #

def IP_Setup_IPv4_Apply(driver):
    driver.find_element(By.ID, "sys_ipv4_apply_button").click()

def IP_Setup_IPv4_Inband_Pbit(driver,value):
    driver.find_element(By.ID, f"sys_ipv4_pbit_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, f"sys_ipv4_pbit_text").send_keys(value)

def IP_Setup_IPv4_Inband_Renew(driver):
    driver.find_element(By.ID, "sys_ipv4_inband_renew_button").click()

def IP_Setup_IPv4_Inband_Release(driver):
    driver.find_element(By.ID, "sys_ipv4_inband_release_button").click()

def IP_Setup_IPv4_Outband_Mode(driver,mode):
    # mode: "static" / "dynamic"
    driver.find_element(By.XPATH, f'//*[@for="sys_ipv4_outband_{mode.lower()}_radio"]').click()

def IP_Setup_IPv4_Outband_IP(driver,value):
    driver.find_element(By.ID, f"sys_ipv4_outband_address_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, f"sys_ipv4_outband_address_text").send_keys(value)

def IP_Setup_IPv4_Outband_Mask(driver,value):
    driver.find_element(By.ID, f"sys_ipv4_outband_mask_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, f"sys_ipv4_outband_mask_text").send_keys(value)

def IP_Setup_IPv4_Outband_Gateway(driver,value):
    driver.find_element(By.ID, f"sys_ipv4_outband_gateway_text").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.ID, f"sys_ipv4_outband_gateway_text").send_keys(value)

def IP_Setup_IPv4_Outband_Renew(driver):
    driver.find_element(By.ID, "sys_ipv4_outband_renew_button").click()

def IP_Setup_IPv4_Outband_Release(driver):
    driver.find_element(By.ID, "sys_ipv4_outband_release_button").click()

# IP Setup > IPv6 Setup #

def IP_Setup_IPv6_Setup_Inband_Default_Gateway(driver,value):
    input = driver.find_element(By.ID, f"sys_ipv6_inband_gateway_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def IP_Setup_IPv6_Setup_Inband_Global_Address(driver,value):
    input = driver.find_element(By.ID, f"sys_ipv6_inband_gu_address_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def IP_Setup_IPv6_Setup_Inband_Netmask(driver,value):
    input = driver.find_element(By.ID, f"sys_ipv6_inband_gu_netmask_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def IP_Setup_IPv6_Setup_Inband_Renew(driver):
    e_mod.Click(driver,'id','sys_ipv6_inband_renew_button')

def IP_Setup_IPv6_Setup_Inband_Release(driver):
    e_mod.Click(driver,'id','sys_ipv6_inband_release_button')

def IP_Setup_IPv6_Setup_Outband_Global_Address(driver,value):
    input = driver.find_element(By.ID, f"sys_ipv6_outband_gu_address_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def IP_Setup_IPv6_Setup_Outband_Netmask(driver,value):
    input = driver.find_element(By.ID, f"sys_ipv6_outband_gu_netmask_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def IP_Setup_IPv6_Setup_Outband_Renew(driver):
    e_mod.Click(driver,'id','sys_ipv6_outband_renew_button')

def IP_Setup_IPv6_Setup_Outband_Release(driver):
    e_mod.Click(driver,'id','sys_ipv6_outband_release_button')

# IP Setup > IP Route #

def IP_Setup_IP_Route_New(driver):
    e_mod.Click(driver,'id','sys_iproute_profile_new_btn')

def IP_Setup_IP_Route_Dest_IP_Address(driver,value):
    input = driver.find_element(By.ID, f"sys_iproute_destip_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def IP_Setup_IP_Route_Mask(driver,value):
    input = driver.find_element(By.ID, f"sys_iproute_mask_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def IP_Setup_IP_Route_Next_Hop_IP(driver,value):
    input = driver.find_element(By.ID, f"sys_iproute_nexthop_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def IP_Setup_IP_Route_Metric(driver,value):
    input = driver.find_element(By.ID, f"sys_iproute_metric_text")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def IP_Setup_IP_Route_Select(driver,index):
    e_mod.Checkbox_EMS(driver,f"sys_iproute_profile_checkbox{index}",True)

def IP_Setup_IP_Route_Delete(driver):
    e_mod.Click(driver,'id','sys_iproute_profile_del_btn')

# Monitor

def Monitor_Voltage_High_limit(driver,index,value):
    input = driver.find_elements(By.NAME, "rpsysmonitor_input_vol_high")[index-1]
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def Monitor_Voltage_Low_limit(driver,index,value):
    input = driver.find_elements(By.NAME, "rpsysmonitor_input_vol_low")[index-1]
    input.send_keys(Keys.CONTROL + 'a')
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
    driver.find_element(By.NAME, f"rpsysmonitor_input_fandutycycle_dutycycle{index}").send_keys(Keys.CONTROL + 'a')
    driver.find_element(By.NAME, f"rpsysmonitor_input_fandutycycle_dutycycle{index}").send_keys(value)


# System Information

# Unix Syslog

def Unix_Syslog_Server(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpSyslog_server']/option[{sel}]").click()

def Unix_Syslog_IP(driver,value):
    input = driver.find_element(By.NAME, f"rpSyslog_ip")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

# Users Account

def Users_Account_Name(driver,value):
    input = driver.find_element(By.NAME, f"rpsysuser_input_name")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def Users_Account_Password(driver,value):
    input = driver.find_element(By.NAME, f"rpsysuser_input_password")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

def Users_Account_Retype_Password_to_Confirm(driver,value):
    input = driver.find_element(By.NAME, f"rpsysuser_input_retypepassword")
    input.send_keys(Keys.CONTROL + 'a')
    input.send_keys(value)

# Msc Redundant

# Power

# Power > Power Card Info

# Power > AC Power

