from selenium.webdriver.common.by import By
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

# ARP Table

# DHCP Snoop

def DHCP_Snoop_Clear_Up(driver):
    driver.find_elements(By.NAME, "rpShDhcpClear")[0].click()

def DHCP_Snoop_Clear_Down(driver):
    driver.find_elements(By.NAME, "rpShDhcpClear")[1].click()
    
# Dot3ad Status

# DSL Status

# MAC Table

def MAC_Table_VLAN_VID_Select(driver):
    driver.find_elements(By.NAME, "rpstatsmac_rdoVlan")[1].click()

def MAC_Table_VLAN_VID_Input(driver,value):
    input = driver.find_element(By.NAME, "rpstatsmac_txtVid")
    input.clear()
    input.send_keys(value)

def MAC_Table_Refresh(driver):
    driver.find_element(By.NAME, "rpstatsmac_btnRefresh").click()

def MAC_Table_Flush(driver):
    driver.find_element(By.NAME, "rpstatsmac_btnFlush").click()

# Online Users

def Online_Users_Kick(driver, index):
    driver.find_elements(By.NAME, "rponlineusr_btnKick")[index].click()

# Port

def Port_Slot_Select(driver,slot):
    driver.find_elements(By.NAME, "Lcmantableid")[int(slot)-1].click()

def Port_Slot_Up(driver):
    driver.find_element(By.NAME, "rpstatusdsl_btnUp").click()

def Port_Port_Select(driver,port):
    driver.find_elements(By.NAME, f"Lcmantableid")[int(port)-1].click()

def Port_Port_Up(driver):
    driver.find_element(By.NAME, "rpstatusdsl_btnUp").click()

def Port_Port_Refresh(driver):
    driver.find_element(By.NAME, "rpstatusdsl_btnRefresh").click()

def Port_Port_Clear(driver):
    driver.find_element(By.NAME, "rpstatusdsl_btnClear").click()
    
# STP

# IP

# IPv6

# MACFF

# Host Protection

def Host_Protection_Clear_Statistic(driver):
    driver.find_element(By.NAME, "rpaclhostprotect_BtnClear").click()

def Host_Protection_Refresh(driver):
    driver.find_element(By.NAME, "rpaclhostprotect_BtnRefresh").click()

# SFP

# IPBPVC

# VLAN

# G.bond

# H248

# Proxy Server

# Termination

# N1mac

# vtur

# OAM

# IMA

# Loopguard

def Loopguard_Refresh(driver):
    driver.find_element(By.NAME, "rpacl_lgSt_btnRefresh").click()

def Loopguard_Flush(driver):
    driver.find_element(By.NAME, "rpacl_lgSt_btnFlush").click()

# PPPoE

def PPPoE_Refresh(driver):
    driver.find_element(By.XPATH, "/html/body/form/div/div[1]/input[1]").click()

def PPPoE_Flush(driver):
    driver.find_element(By.XPATH, "/html/body/form/div/div[1]/input[2]").click()

# Vlancount

# Macff

# CDR

# PVC

# VOIP DNS

# 802.1x Port Status

# DDMI Status

# Monitor Status

# IGMP Status

# LLDP Status

# Error Disable

# Protect Switch