from selenium.webdriver.common.by import By
from os import times
import time
from attr import field
from pyrsistent import s
import module.selenium_module as mod
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

# Line Diagnostic

# Line Diagnostic -> DELT

def Line_Diagnostic_DELT_Set_DELT(driver):
    driver.find_element(By.ID, "set_delt").click()

def Line_Diagnostic_DELT_Get_Result(driver):
    driver.find_element(By.ID, "get_result").click()

def Line_Diagnostic_DELT_Get_Hlin(driver):
    driver.find_element(By.ID, "get_hlin").click()

def Line_Diagnostic_DELT_Get_Hlog(driver):
    driver.find_element(By.ID, "get_hlog").click()

def Line_Diagnostic_DELT_Get_QLN(driver):
    driver.find_element(By.ID, "get_qln").click()

def Line_Diagnostic_DELT_Get_SNR(driver):
    driver.find_element(By.ID, "get_snr").click()

# Line Diagnostic -> SELT

def Line_Diagnostic_SELT_Set_SELT(driver):
    driver.find_element(By.NAME, "rpSetSELTPort").click()

def Line_Diagnostic_SELT_Get_SELT(driver):
    driver.find_element(By.NAME, "rpGetSELTDate").click()

def Line_Diagnostic_SELT_Set_Calibration(driver):
    driver.find_element(By.NAME, "rpSetCalibrationPort").click()

def Line_Diagnostic_SELT_Get_Calibration(driver):
    driver.find_element(By.NAME, "rpGetCalibrationPort").click()

# IP

# IP -> IP Ping

def IP_Ping_IPv4_Address(driver,value):
    input = driver.find_element(By.NAME, "inputPingIPv4Address")
    input.clear()
    input.send_keys(value)

def IP_Ping_IPv4_Data_Bytes(driver,value):
    input = driver.find_element(By.NAME, "inputPingIPv4Bytes")
    input.clear()
    input.send_keys(value)

def IP_Ping_IPv4Ping(driver):
    driver.find_element(By.NAME, "rpDiagIPv4Ping").click()

def IP_Ping_IPv6_Address(driver,value):
    input = driver.find_element(By.NAME, "inputPingIPv6Address")
    input.clear()
    input.send_keys(value)

def IP_Ping_IPv6_Data_Bytes(driver,value):
    input = driver.find_element(By.NAME, "inputPingIPv6Bytes")
    input.clear()
    input.send_keys(value)

def IP_Ping_IPv6Ping(driver):
    driver.find_element(By.NAME, "rpDiagIPv6Ping").click()

# IP -> IP Trace Route

def IP_Trace_Route_IP_Address(driver,value):
    input = driver.find_element(By.NAME, "rpiptroute_iptIp")
    input.clear()
    input.send_keys(value)

def IP_Trace_Route_Start(driver):
    driver.find_element(By.NAME, "rpiptroute_BtnStart").click()

# OAM Loopback

def OAM_Loopback_Start(driver):
    driver.find_element(By.NAME, "rpOamLoopbackEnet_btnOamLoopbackStart").click()

def OAM_Loopback_Stop(driver):
    driver.find_element(By.NAME, "rpOamLoopbackEnet_btnOamLoopbackStop").click()

def OAM_Loopback_Test(driver):
    driver.find_element(By.NAME, "rpOamLoopbackEnet_btnOamLoopbackTest").click()

def OAM_Loopback_Get(driver):
    driver.find_element(By.NAME, "rpOamLoopbackEnet_btnOamLoopbackGet").click()
