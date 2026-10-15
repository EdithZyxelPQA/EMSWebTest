from selenium.webdriver.common.by import By
from os import times
import time
from attr import field
from pyrsistent import s
import selenium_module as mod
from selenium.webdriver.support.ui import Select

# Current

def Current_Severity(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpalmcurr_sltSvrt']/option[{sel}]").click()

def Current_Alarm(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpalmcurr_sltAlm']/option[{sel}]").click()

def Current_Condition(driver,value):
    input = driver.find_element(By.NAME, "rpalmcurr_txtCondition")
    input.clear()
    input.send_keys(value)

def Current_Date_Start(driver,value):
    input = driver.find_element(By.NAME, "rpalmcurr_txtSDate")
    input.clear()
    input.send_keys(value)

def Current_Date_End(driver,value):
    input = driver.find_element(By.NAME, "rpalmcurr_txtEDate")
    input.clear()
    input.send_keys(value)

def Current_Order_Forward(driver):
    driver.find_elements(By.NAME, "rpalmcurr_rdoOrder")[0].click()

def Current_Order_Reverse(driver):
    driver.find_elements(By.NAME, "rpalmcurr_rdoOrder")[1].click()

def Current_Load(driver):
    driver.find_element(By.NAME, "rpalmcurr_btnLoad").click()

def Current_Flush(driver):
    driver.find_element(By.NAME, "rpalmcurr_btnFlush").click()

# History

def History_Severity(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpalmhist_sltSvrt']/option[{sel}]").click()

def History_Alarm(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpalmhist_sltAlm']/option[{sel}]").click()

def History_Condition(driver,value):
    input = driver.find_element(By.NAME, "rpalmhist_txtCondition")
    input.clear()
    input.send_keys(value)

def History_Date_Start(driver,value):
    input = driver.find_element(By.NAME, "rpalmhist_txtSDate")
    input.clear()
    input.send_keys(value)

def History_Date_End(driver,value):
    input = driver.find_element(By.NAME, "rpalmhist_txtEDate")
    input.clear()
    input.send_keys(value)

def History_Order_Forward(driver):
    driver.find_elements(By.NAME, "rpalmhist_rdoOrder")[0].click()

def History_Order_Reverse(driver):
    driver.find_elements(By.NAME, "rpalmhist_rdoOrder")[1].click()

def History_Load(driver):
    driver.find_element(By.NAME, "rpalmhist_btnLoad").click()

def History_Flush(driver):
    driver.find_element(By.NAME, "rpalmhist_btnFlush").click()

# Port Setup

def Port_Setup_Notification_Severity_All(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpalarmseverity']/option[{sel}]").click()

def Port_Setup_Link_Trap_Supress_All(driver,request):
    check_box = driver.find_element(By.NAME, "rpalarmsuppress")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Port_Setup_Apply(driver):
    driver.find_element(By.NAME, "rpalarmport_btnApply").click()

def Port_Setup_Cancel(driver):
    driver.find_element(By.NAME, "rpalarmport_btnCancel").click()

# Input

# Input -> Alarm Input

def Input_Alarm_Input_Index_Name(driver,index,value):
    input = driver.find_element(By.NAME, f"rpAlarmInput_name{index}")
    input.clear()
    input.send_keys(value)

def Input_Alarm_Input_Apply(driver):
    driver.find_element(By.NAME, "rpAlarmInputApply").click()

def Input_Alarm_Input_Default(driver):
    driver.find_element(By.NAME, "rpAlarmInputDefault").click()

def Input_Alarm_Input_Cancel(driver):
    driver.find_element(By.NAME, "rpAlarmInputCancel").click()

# Input -> CPU Overload Alarm

def Input_CPU_Overload_Alarm_Analytic_Method(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpAlarmCoa_nalyticMethod']/option[{sel}]").click()

def Input_CPU_Overload_Alarm_Issue_Threshold(driver,value):
    input = driver.find_element(By.NAME, f"rpAlarmCoa_issueThreshold")
    input.clear()
    input.send_keys(value)

def Input_CPU_Overload_Alarm_Clear_Threshold(driver,value):
    input = driver.find_element(By.NAME, f"rpAlarmCoa_clearThreshold")
    input.clear()
    input.send_keys(value)

def Input_CPU_Overload_Alarm_Sample_Seconds(driver,value):
    input = driver.find_element(By.NAME, f"rpAlarmCoa_sampleSeconds")
    input.clear()
    input.send_keys(value)

def Input_CPU_Overload_Alarm_Apply(driver):
    driver.find_element(By.NAME, "rpAlarmCoaApply").click()

def Input_CPU_Overload_Alarm_Cancel(driver):
    driver.find_element(By.NAME, "rpAlarmCoaCancel").click()

# Input -> System Supress

def Input_System_Supress_Enable(driver,request):
    check_box = driver.find_element(By.NAME, "rpAlarmSysSupress_mode")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Input_System_Supress_Apply(driver):
    driver.find_element(By.NAME, "rpAlarmSysSupressApply").click()

def Input_System_Supress_Cancel(driver):
    driver.find_element(By.NAME, "rpAlarmSysSupressCancel").click()

# Definition

def Input_Definition_Alarm_Category(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpalarm_def_slt_category']/option[{sel}]").click()

def Input_Definition_SNMP_All(driver,request):
    check_box = driver.find_element(By.NAME, "rpalarm_def_chkAll_snmp")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Input_Definition_Syslog_All(driver,request):
    check_box = driver.find_element(By.NAME, "rpalarm_def_chkAll_syslog")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def Input_Definition_Facility_All(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpalarm_def_sltAll_fac']/option[{sel}]").click()

def Input_Definition_Severity_All(driver,sel):
    driver.find_element(By.XPATH, f"//*[@name='rpalarm_def_sltAll_ser']/option[{sel}]").click()

def Input_Definition_Apply(driver):
    driver.find_element(By.NAME, "rpalarm_def_button_apply").click()
