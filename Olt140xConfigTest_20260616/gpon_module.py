from selenium.webdriver.common.by import By
from os import times
import time
from attr import field
from pyrsistent import s
import selenium_module as mod
from selenium.webdriver.support.ui import Select
# from web_auto_project.selenium_module import IsAlert

# Slot切換(整個GPON都通用)
def Slot_Select(driver,slot):
    select = driver.find_element(By.XPATH, f"//*[@id='lctbl_selSlot']/option[{slot}]")
    select.click()

def Get_Max_Slot(driver):
    try:
        slot = 1
        while(driver.find_element(By.XPATH, f"//*[@id='lctbl_selSlot']/option[{slot}]")):
            slot = slot+1
    except:
        return slot-1

def Get_Max_Port(driver):
    try:
        port = 1
        while(driver.find_element(By.XPATH, f"//*[@id='lctbl_selPort']/option[{port}]")):
            port = port+1
    except:
        return port-1

def Multi_Page_Test(driver,slot,pon,aid):
    name_array = ["rpGponPortTca_txtFecCorrByteTh","rpGponPortTca_txtFecCorrCodeWordTh","rpGponPortTca_txtFecUncorrCodeWordTh","rpGponPortTca_txtBipErrTh","rpGponPortTca_txtReiErrTh","rpGponPortTca_txtFecCodeWordTh","rpGponPortTca_txtBipByteTh","rpGponPortTca_txtRxPloamCrcErrTh","rpGponPortTca_txtRxPloamNonIdleTh","rpGponPortTca_txtPositiveDriftTh","rpGponPortTca_txtNegativeDriftTh","rpGponPortTca_txtRxOmciPktCrcErrTh","rpGponPortTca_txtUnreceivedBurstTh","rpGponPortTca_txtLCDGIErrTh","rpGponPortTca_txtRDIErrTh","rpGponPortTca_txtRxOmciPktTh"]
    configuration_name_array = ["rpGponPortTca_FecCorrByteTh","rpGponPortTca_FecCorrCodeWordTh","rpGponPortTca_FecUncorrCodeWordTh","rpGponPortTca_BipErrTh","rpGponPortTca_ReiErrTh","rpGponPortTca_FecCodeWordTh","rpGponPortTca_BipByteTh","rpGponPortTca_RxPloamCrcErrTh","rpGponPortTca_RxPloamNonIdleTh","rpGponPortTca_PositiveDriftTh","rpGponPortTca_NegativeDriftTh","rpGponPortTca_RxOmciPktCrcErrTh","rpGponPortTca_UnreceivedBurstTh","rpGponPortTca_LCDGIErrTh","rpGponPortTca_RDIErrTh","rpGponPortTca_RxOmciPktTh"]
    status_name_array = ["rpGponPortTcaStatus_FecCorrByteTh","rpGponPortTcaStatus_FecCorrCodeWordTh","rpGponPortTcaStatus_FecUncorrCodeWordTh","rpGponPortTcaStatus_BipErrTh","rpGponPortTcaStatus_ReiErrTh","rpGponPortTcaStatus_FecCodeWordTh","rpGponPortTcaStatus_BipByteTh","rpGponPortTcaStatus_RxPloamCrcErrTh","rpGponPortTcaStatus_RxPloamNonIdleTh","rpGponPortTcaStatus_PositiveDriftTh","rpGponPortTcaStatus_NegativeDriftTh","rpGponPortTcaStatus_RxOmciPktCrcErrTh","rpGponPortTcaStatus_UnreceivedBurstTh","rpGponPortTcaStatus_LCDGIErrTh","rpGponPortTcaStatus_RDIErrTh","rpGponPortTcaStatus_RxOmciPktTh"]

    print(f"{slot}-{pon}-{aid+1} GPON Profile Test\nTest Start",file = open("ONT_Status_Test_report.txt", '+a'))

# ONT Alarm Profile Test
# GPON > ONT Alarm Profile
# -------------------------start-------------------------

    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"GPON")
    mod.SubPage_Switch(driver,"ONT Alarm Profile")
    mod.Switch_Frame(driver)
    ONT_Ala_Name(driver,"0123456789012345678901234567890")
    ONT_Ala_LBCT_Low(driver,"0")
    ONT_Ala_LBCT_Up(driver,"79")
    ONT_Ala_RPT_Low(driver,"-127")
    ONT_Ala_RPT_Up(driver,"0")
    ONT_Ala_TT_Low(driver,"-40")
    ONT_Ala_TT_Up(driver,"100")
    ONT_Ala_TPT_Low(driver,"-15.3")
    ONT_Ala_TPT_Up(driver,"6.5")
    ONT_Ala_PFVT_Low(driver,"2.80")
    ONT_Ala_PFVT_Up(driver,"3.59")
    ONT_Ala_Apply_Up(driver)
    if_find = False
    if_error = False
    if(driver.find_elements(By.CLASS_NAME, "listOntAlarmprof").__len__() == 0):
        print("-ONT Alarm Profile- Apply Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
    else:
        for index in range(driver.find_elements(By.CLASS_NAME, "listOntAlarmprof").__len__()):
            if(driver.find_elements(By.CLASS_NAME, "rpGponOntAlarmprof_name")[index].get_attribute("value") == "0123456789012345678901234567890"):
                if_find = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpGponOntAlarmprof_currThr")[index].get_attribute("textContent") == "0~79"):
                    pass
                else:
                    print("-ONT Alarm Profile- curr-thresh Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpGponOntAlarmprof_rxpwrThr")[index].get_attribute("textContent") == "-127.0~0.0"):
                    pass
                else:
                    print("-ONT Alarm Profile- rxpower-thresh Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpGponOntAlarmprof_tempThr")[index].get_attribute("textContent") == "-40~100"):
                    pass
                else:
                    print("-ONT Alarm Profile- temp-thresh Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpGponOntAlarmprof_txpwrThr")[index].get_attribute("textContent") == "-15.3~6.5"):
                    pass
                else:
                    print("-ONT Alarm Profile- txpower-thresh Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                    if_error = True
                if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpGponOntAlarmprof_voltThr")[index].get_attribute("textContent") == "2.80~3.59"):
                    pass
                else:
                    print("-ONT Alarm Profile- volt-thresh Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                    if_error = True
                driver.find_elements(By.NAME, "rpGponOntAlarmprof_chkDel")[index].click()
                ONT_Ala_Apply_Down(driver)
                break
        if(if_find == False):
            print("-ONT Alarm Profile- Apply Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
        else:
            if(if_error == False):
                print("-ONT Alarm Profile- Pass",file = open("ONT_Status_Test_report.txt", '+a'))

# -------------------------end-------------------------
    
# ONT VoIP Common Profile Test
# GPON > ONT VoIP Profile > VoIP Common Profile
# -------------------------start-------------------------
    
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"ONT VoIP Profile")
    mod.Switch_Frame(driver)
    ONT_VoIP_Com_Name(driver,"012345678901234")
    ONT_VoIP_Com_min_Local_Port(driver,"65535")
    ONT_VoIP_Com_max_Local_Port(driver,"65535")
    ONT_VoIP_Com_dscp_mark(driver,"63")
    time.sleep(3)
    ONT_VoIP_Com_piggyback(driver,True)
    time.sleep(1)
    ONT_VoIP_Com_tone(driver,True)
    time.sleep(2)
    ONT_VoIP_Com_dtmf(driver,True)
    time.sleep(1)
    ONT_VoIP_Com_cas(driver,True)
    time.sleep(1)
    ONT_VoIP_Com_jitter_target(driver,"5000")
    ONT_VoIP_Com_max_jitter_buffer(driver,"500")
    ONT_VoIP_Com_ptsn_protocol(driver,"999")
    ONT_VoIP_Com_announce_type(driver,4)
    time.sleep(1)
    ONT_VoIP_Com_echo_cancel(driver,False)
    time.sleep(1)
    ONT_VoIP_Com_fax_mode(driver,2)
    ONT_VoIP_Com_1st_codec(driver,17)
    ONT_VoIP_Com_2nd_codec(driver,17)
    ONT_VoIP_Com_3rd_codec(driver,17)
    ONT_VoIP_Com_4th_codec(driver,17)
    ONT_VoIP_Com_1st_packet_period(driver,"30")
    ONT_VoIP_Com_2nd_packet_period(driver,"30")
    ONT_VoIP_Com_3rd_packet_period(driver,"30")
    ONT_VoIP_Com_4th_packet_period(driver,"30")
    time.sleep(3)
    ONT_VoIP_Com_1st_silence(driver,True)
    time.sleep(1)
    ONT_VoIP_Com_2nd_silence(driver,True)
    time.sleep(1)
    ONT_VoIP_Com_3rd_silence(driver,True)
    time.sleep(1)
    ONT_VoIP_Com_4th_silence(driver,True)
    time.sleep(1)
    ONT_VoIP_Com_oob_dtmf(driver,True)
    time.sleep(1)
    ONT_VoIP_Com_signal_code(driver,6)
    time.sleep(1)
    ONT_VoIP_Com_Apply_Up(driver)
    if_find = False
    if(driver.find_elements(By.CLASS_NAME, "listVoipCommon").__len__() == 0):
        print("-ONT VoIP Common Profile- Apply Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
    else:
        for index in range(driver.find_elements(By.CLASS_NAME, "listVoipCommon").__len__()):
            if(driver.find_elements(By.ID, "rpGponVoipCommon_name")[index].get_attribute("value") == "012345678901234"):
                if_find = True
                if(driver.find_elements(By.NAME, "rpGponVoipCommon_rule")[index].get_attribute("textContent") == "min local port=65535, max local port=65535, dscp mark=63, piggyback=enable, tone=enable, dtmf=enable, cas=enable, jitter target=5000, max jitter buffer=500, pstn protocol=999, announce type=voi-ann, echo cancel=disable, fax mode=T38, 1st codec=G729, 2nd codec=G729, 3rd codec=G729, 4th codec=G729, 1st packet period=30, 2nd packet period=30, 3rd packet period=30, 4th packet period=30, 1st silence=enable, 2nd silence=enable, 3rd silence=enable, 4th silence=enable, oob dtmf=enable, signal code=mul-par,"):
                    print("-ONT VoIP Common Profile- Pass",file = open("ONT_Status_Test_report.txt", '+a'))
                else:
                    print("-ONT VoIP Common Profile- Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
            driver.find_elements(By.NAME, "rpGponVoipCommon_chkDel")[index].click()
            ONT_VoIP_Com_Apply_Down(driver)
            break
        if(if_find == False):
            print("-ONT VoIP Common Profile- Apply Not Found",file = open("ONT_Status_Test_report.txt", '+a'))

# -------------------------end-------------------------
    
# ONT VoIP SIP Profile Test
# GPON > ONT VoIP Profile > VoIP SIP Profile
# -------------------------start-------------------------

    mod.Tab_Switch(driver,"VoIP SIP Profile")
    ONT_VoIP_SIP_Name(driver,"012345678901234")
    ONT_VoIP_SIP_PSA(driver,"012345678901234567890123456789012345678901234567890123456789012")
    ONT_VoIP_SIP_OPA(driver,"012345678901234567890123456789012345678901234567890123456789012")
    ONT_VoIP_SIP_PD(driver,"1.1.1.254")
    ONT_VoIP_SIP_SD(driver,"2.2.2.254")
    ONT_VoIP_SIP_RET(driver,"25200")
    ONT_VoIP_SIP_RHST(driver,"720")
    ONT_VoIP_SIP_HPU(driver,"012345678901234567890123456789012345678901234567890123456789012")
    ONT_VoIP_SIP_SR(driver,"012345678901234567890123456789012345678901234567890123456789012")
    ONT_VoIP_SIP_S(driver,"0123")
    time.sleep(3)
    ONT_VoIP_SIP_CI_cal_num(driver,True)
    time.sleep(1)
    ONT_VoIP_SIP_CI_cal_nam(driver,True)
    time.sleep(1)
    ONT_VoIP_SIP_CI_cid_bio(driver,True)
    time.sleep(1)
    ONT_VoIP_SIP_CI_cid_num(driver,True)
    time.sleep(1)
    ONT_VoIP_SIP_CI_cid_nam(driver,True)
    time.sleep(1)
    ONT_VoIP_SIP_CI_ACR(driver,True)
    time.sleep(1)
    ONT_VoIP_SIP_CW_cal_wai(driver,True)
    time.sleep(1)
    ONT_VoIP_SIP_CW_cid_ann(driver,True)
    time.sleep(1)
    ONT_VoIP_SIP_CPOT_3way(driver,True)
    time.sleep(1)
    ONT_VoIP_SIP_CPOT_cal_tra(driver,True)
    time.sleep(1)
    ONT_VoIP_SIP_CPOT_cal_hol(driver,True)
    time.sleep(1)
    ONT_VoIP_SIP_CPOT_cal_par(driver,True)
    time.sleep(1)
    ONT_VoIP_SIP_CPOT_not_dis(driver,True)
    time.sleep(1)
    ONT_VoIP_SIP_CPOT_flash(driver,True)
    time.sleep(1)
    ONT_VoIP_SIP_CPOT_origin(driver,True)
    time.sleep(1)
    ONT_VoIP_SIP_CPOT_6way(driver,True)
    time.sleep(1)
    ONT_VoIP_SIP_CP_spl_rin(driver,True)
    time.sleep(1)
    ONT_VoIP_SIP_CP_dia_ton(driver,True)
    time.sleep(1)
    ONT_VoIP_SIP_CP_vis_ind(driver,True)
    time.sleep(1)
    ONT_VoIP_SIP_CP_cal_for(driver,True)
    time.sleep(1)
    ONT_VoIP_SIP_DC_enable(driver,True)
    time.sleep(1)
    ONT_VoIP_SIP_DC_dia_opt(driver,True)
    time.sleep(1)
    ONT_VoIP_SIP_DCU(driver,"012345678901234567890123456789012345678901234567890123456789012")
    ONT_VoIP_SIP_BLAU(driver,"012345678901234567890123456789012345678901234567890123456789012")
    ONT_VoIP_SIP_CFU(driver,"012345678901234567890123456789012345678901234567890123456789012")
    ONT_VoIP_SIP_Apply_Up(driver)
    if_find = False
    if(driver.find_elements(By.CLASS_NAME, "listVoipSip").__len__() == 0):
        print("-ONT VoIP SIP Profile- Apply Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
    else:
        for index in range(driver.find_elements(By.CLASS_NAME, "listVoipSip").__len__()):
            if(driver.find_elements(By.ID, "rpGponVoipSip_name")[index].get_attribute("value") == "012345678901234"):
                if_find = True
                if(driver.find_elements(By.NAME, "rpGponVoipSip_rule")[index].get_attribute("textContent") == "proxy service address=012345678901234567890123456789012345678901234567890123456789012, outband proxy address=012345678901234567890123456789012345678901234567890123456789012, primary dns=1.1.1.254, secondary dns=2.2.2.254, registration expiration time=25200, re-registration head start time=720, host part uri=012345678901234567890123456789012345678901234567890123456789012, sip registrar=012345678901234567890123456789012345678901234567890123456789012, softwitch=0123, cal-num=enable, cal-nam=enable, cid-blo=enable, cid-num=enable, cid-nam=enable, acr=enable, cal-wai=enable, cid-ann=enable, 3way=enable, cal-tra=enable, cal-hol=enable, cal-par=enable, not-dis=enable, flash=enable, origin=enable, 6way=enable, spl-rin=enable, dia-ton=enable, vis-ind=enable, cal-for=enable, enable=enable, dia-opt=enable, direction connect uri=012345678901234567890123456789012345678901234567890123456789012, bridged line agent uri=012345678901234567890123456789012345678901234567890123456789012, conference factory uri=012345678901234567890123456789012345678901234567890123456789012, "):
                    print("-ONT VoIP SIP Profile- Pass",file = open("ONT_Status_Test_report.txt", '+a'))
                else:
                    print("-ONT VoIP SIP Profile- Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
            driver.find_elements(By.NAME, "rpGponVoipSip_chkDel")[index].click()
            ONT_VoIP_SIP_Apply_Down(driver)
            break
        if(if_find == False):
            print("-ONT VoIP SIP Profile- Apply Not Found",file = open("ONT_Status_Test_report.txt", '+a'))

# -------------------------end-------------------------
    
# ONT VoIP Dial Plan Profile Test
# GPON > ONT VoIP Profile > VoIP Dial Plan Profile
# -------------------------start-------------------------

    mod.Tab_Switch(driver,"VoIP Dial Plan Profile")
    ONT_VoIP_Dial_Name(driver,"012345678901234")
    ONT_VoIP_Dial_MS(driver,"256")
    ONT_VoIP_Dial_CDT(driver,"8000")
    ONT_VoIP_Dial_PDT(driver,"32000")
    ONT_VoIP_Dial_format(driver,4)
    ONT_VoIP_Dial_CT(driver,"0123456789012345678901234567")
    ONT_VoIP_Dial_Apply_Up(driver)
    if_find = False
    if(driver.find_elements(By.CLASS_NAME, "listVoipDialPlan").__len__() == 0):
        print("-ONT VoIP Dial Plan Profile- Apply Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
    else:
        for index in range(driver.find_elements(By.CLASS_NAME, "listVoipDialPlan").__len__()):
            if(driver.find_elements(By.ID, "rpGponVoipDialPlan_name")[index].get_attribute("value") == "012345678901234"):
                if_find = True
                if(driver.find_elements(By.NAME, "rpGponVoipDialPlan_rule")[index].get_attribute("textContent") == "max-size=256, critical-dial-timeout=8000, partial-dial-timeout=32000, format=ven-spe, contant-table1=0123456789012345678901234567, contant-table2=, contant-table3=, contant-table4=, "):
                    print("-ONT VoIP Dial Plan Profile- Pass",file = open("ONT_Status_Test_report.txt", '+a'))
                else:
                    print("-ONT VoIP Dial Plan Profile- Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
            driver.find_elements(By.NAME, "rpGponVoipDialPlan_chkDel")[index].click()
            ONT_VoIP_Dial_Apply_Down(driver)
            break
        if(if_find == False):
            print("-ONT VoIP Dial Plan Profile- Apply Not Found",file = open("ONT_Status_Test_report.txt", '+a'))

# -------------------------end-------------------------

# OLT Registration Test
# GPON > OLT Registration > OLT Registration
# -------------------------start-------------------------

    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"OLT Registration")
    mod.Switch_Frame(driver)
    time.sleep(0.3)
    Slot_Select(driver,slot)
    time.sleep(0.3)
    OLT_Reg_OLT_Reg_Load(driver)
    if_error = False
    for index in range(driver.find_elements(By.CLASS_NAME, "listPort").__len__()):
        time.sleep(1)
        OLT_Reg_OLT_Reg_Active(driver,index+1,True)
        time.sleep(1)
        OLT_Reg_OLT_Reg_Register_Method(driver,index+1,2)
        OLT_Reg_OLT_Reg_KeepAlive(driver,index+1,"168")
        OLT_Reg_OLT_Reg_Max_distance(driver,index+1,"60")
        OLT_Reg_OLT_Reg_Transceive(driver,index+1,22)
        time.sleep(1)
        OLT_Reg_OLT_Reg_Template_Active(driver,index+1,False)
        time.sleep(1)
    OLT_Reg_OLT_Reg_Apply(driver)
    if(mod.IsAlert(driver)):
        if_error = True
    for index in range(driver.find_elements(By.CLASS_NAME, "listPort").__len__()):
        time.sleep(1)
        OLT_Reg_OLT_Reg_Active(driver,index+1,False)
        time.sleep(1)
        OLT_Reg_OLT_Reg_Register_Method(driver,index+1,3)
        OLT_Reg_OLT_Reg_Transceive(driver,index+1,0)
        time.sleep(1)
        OLT_Reg_OLT_Reg_Template_Active(driver,index+1,True)
        time.sleep(1)
        OLT_Reg_OLT_Reg_Template(driver,index+1,128)
    OLT_Reg_OLT_Reg_Apply(driver)
    if(mod.IsAlert(driver)):
        if_error = True
    for index in range(driver.find_elements(By.CLASS_NAME, "listPort").__len__()):
        OLT_Reg_OLT_Reg_Register_Method(driver,index+1,5)
    OLT_Reg_OLT_Reg_Apply(driver)
    if(mod.IsAlert(driver)):
        if_error = True
    for index in range(driver.find_elements(By.CLASS_NAME, "listPort").__len__()):
        OLT_Reg_OLT_Reg_KeepAlive(driver,index+1,"@")
        OLT_Reg_OLT_Reg_Apply(driver)
        if(mod.IsAlert(driver)):
            OLT_Reg_OLT_Reg_Cancel(driver)
            time.sleep(2)
        else:
            if_error = True
    OLT_Reg_OLT_Reg_Max_dis_Test_Keys = ["19","61","@"]
    for test_num in range(3):
        for index in range(driver.find_elements(By.CLASS_NAME, "listPort").__len__()):
            OLT_Reg_OLT_Reg_Max_distance(driver,index+1,OLT_Reg_OLT_Reg_Max_dis_Test_Keys[test_num])
            OLT_Reg_OLT_Reg_Apply(driver)
            if(mod.IsAlert(driver)):
                OLT_Reg_OLT_Reg_Cancel(driver)
                time.sleep(2)
            else:
                if_error = True
    for index in range(driver.find_elements(By.CLASS_NAME, "listPort").__len__()):
        OLT_Reg_OLT_Reg_KeepAlive(driver,index+1,"0")
        OLT_Reg_OLT_Reg_Max_distance(driver,index+1,"20")
        OLT_Reg_OLT_Reg_Transceive(driver,index+1,12)
    time.sleep(1)
    OLT_Reg_OLT_Reg_Active(driver,1,True)
    time.sleep(1)
    OLT_Reg_OLT_Reg_Active(driver,16,True)
    OLT_Reg_OLT_Reg_Apply(driver)
    if(mod.IsAlert(driver)):
        if_error = True
    if(if_error):
        print("-OLT Registration- Fail",file = open("ONT_Status_Test_report.txt", '+a'))
    else:
        print("-OLT Registration- Pass",file = open("ONT_Status_Test_report.txt", '+a'))

# -------------------------end-------------------------
    
# TCA Configuration Test
# GPON > OLT Registration > TCA Configuration
# -------------------------start-------------------------

    valid = True
    test_keys = ["4294967295","4294967296","0"]
    if_error = False
    enable_test = True
    counter = 0
    pon = int(pon)
    slot = int(slot)
    while enable_test:
        if(counter > 20):
            driver.refresh()
            counter = 0
        try:
            mod.Switch_Default(driver)
            mod.Page_Switch(driver,"GPON")
            mod.SubPage_Switch(driver,"OLT Registration")
            mod.Switch_Frame(driver)
            mod.Tab_Switch(driver,"TCA Configuration")
            time.sleep(0.3)
            Slot_Select(driver,slot)
            time.sleep(0.3)
            OLT_Reg_TCA_Con_Load(driver)
            time.sleep(0.3)
            OLT_Reg_TCA_Pon_Select(driver,pon)
            OLT_Reg_TCA_Enable(driver,True)
            OLT_Reg_TCA_Apply(driver)
            if(OLT_Reg_TCA_configuration_value(driver,"rpGponPortTca_FecMode",pon) == "Disable"):
                if_error = True
            
            mod.Tab_Switch(driver,"TCA Status")
            
            time.sleep(0.3)
            Slot_Select(driver,slot)
            time.sleep(0.3)
            OLT_Reg_TCA_Sta_Load(driver)
            time.sleep(0.3)
            if(OLT_Reg_TCA_Sta_status_value(driver,"rpGponPortTcaStatus_FecMode",pon) == "Disable"):
                if_error = True
            
            mod.Tab_Switch(driver,"TCA Configuration")
            
            time.sleep(0.3)
            Slot_Select(driver,slot)
            time.sleep(0.3)
            OLT_Reg_TCA_Con_Load(driver)
            time.sleep(0.3)
            OLT_Reg_TCA_Pon_Select(driver,pon)
            time.sleep(0.3)
            OLT_Reg_TCA_Enable(driver,False)
            OLT_Reg_TCA_Apply(driver)
            if(OLT_Reg_TCA_configuration_value(driver,"rpGponPortTca_FecMode",pon) == "Enable"):
                if_error = True

            mod.Tab_Switch(driver,"TCA Status")
            
            time.sleep(0.3)
            Slot_Select(driver,slot)
            time.sleep(0.3)
            OLT_Reg_TCA_Sta_Load(driver)
            time.sleep(0.3)
            if(OLT_Reg_TCA_Sta_status_value(driver,"rpGponPortTcaStatus_FecMode",pon) == "Enable"):
                if_error = True
            enable_test = False
        except:
            enable_test = True
            counter = counter+1
            # print(f"{slot}-{pon} Enable Test Fail")
    for field in range(name_array.__len__()):
        name = name_array[field]
        configuration_name = configuration_name_array[field]
        status_name = status_name_array[field]
        for key_num in range (test_keys.__len__()):
            enable_test = True
            counter = 0
            while enable_test:
                if(counter == 20):
                    driver.refresh()
                    mod.Switch_Default(driver)
                    mod.Page_Switch(driver,"GPON")
                    mod.SubPage_Switch(driver,"OLT Registration")
                    mod.Switch_Frame(driver)
                try: 
                    mod.Tab_Switch(driver,"TCA Configuration")
                    time.sleep(0.3)
                    Slot_Select(driver,slot)
                    time.sleep(0.5)
                    OLT_Reg_TCA_Con_Load(driver)
                    time.sleep(0.5)
                    OLT_Reg_TCA_Pon_Select(driver,pon)
                    prev_value = OLT_Reg_TCA_value(driver,name)
                    OLT_Reg_TCA_input(driver,test_keys[key_num],name)
                    OLT_Reg_TCA_Apply(driver)
                    # configuration check
                    if(mod.IsAlert(driver)):
                        OLT_Reg_TCA_Cancel(driver)
                        valid = False
                        if(str(test_keys[key_num]) == str(prev_value)):
                            if_error = True
                    else:
                        valid = True
                        if(int(OLT_Reg_TCA_configuration_value(driver,configuration_name,pon)) > 4294967295):
                            if_error = True
                        elif(int(OLT_Reg_TCA_configuration_value(driver,configuration_name,pon)) < 0):
                            if_error = True
                    # value check
                    time.sleep(0.3)
                    Slot_Select(driver,slot)
                    time.sleep(0.5)
                    OLT_Reg_TCA_Con_Load(driver)
                    time.sleep(0.5)
                    OLT_Reg_TCA_Pon_Select(driver,pon)
                    now_value = OLT_Reg_TCA_value(driver,name)
                    if(valid):
                        if(str(test_keys[key_num]) != str(now_value)):
                            if_error = True
                    else:
                        if(now_value != prev_value):
                            if_error = True
                    # status check
                    mod.Tab_Switch(driver,"TCA Status")
                    time.sleep(0.3)
                    Slot_Select(driver,slot)
                    time.sleep(0.5)
                    OLT_Reg_TCA_Sta_Load(driver)
                    time.sleep(0.5)
                    if(str(OLT_Reg_TCA_Sta_status_value(driver,status_name,pon)) != str(now_value)):
                            if_error = True
                    enable_test = False
                except:
                    counter = counter+1
                    enable_test = True
                if(counter == 30):
                    enable_test = False
                    if_error = True
                    break
    if(if_error):
        print("-TCA Configuration- Fail",file = open("ONT_Status_Test_report.txt", '+a'))
    else:
        print("-TCA Configuration- Pass",file = open("ONT_Status_Test_report.txt", '+a'))

# -------------------------end-------------------------
    
# Ingress Profile Test
# GPON > ONT Qos > Ingress Profile
# -------------------------start-------------------------

    if_find = False
    if_error = False
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"ONT Qos")
    mod.Switch_Frame(driver)
    ONT_Qos_Ing_Pro_Name(driver,"0123456789012345678901234567890")
    ONT_Qos_Ing_Pro_0tc(driver,1)
    ONT_Qos_Ing_Pro_1tc(driver,1)
    ONT_Qos_Ing_Pro_2tc(driver,1)
    ONT_Qos_Ing_Pro_3tc(driver,1)
    ONT_Qos_Ing_Pro_4tc(driver,1)
    ONT_Qos_Ing_Pro_5tc(driver,1)
    ONT_Qos_Ing_Pro_6tc(driver,1)
    ONT_Qos_Ing_Pro_7tc(driver,1)
    ONT_Qos_Ing_Pro_Apply_Up(driver)
    if(driver.find_elements(By.CLASS_NAME, "listIngprof").__len__() == 0):
        if_find == False
    else:
        for index in range(driver.find_elements(By.CLASS_NAME, "listIngprof").__len__()):
            if(driver.find_elements(By.ID, "rpGponIngprof_name")[index].get_attribute("value") == "0123456789012345678901234567890"):
                if_find = True
                if(driver.find_elements(By.NAME, "rpGponIngprof_rule")[index].get_attribute("textContent") != "DOT1P0TC=0, DOT1P1TC=0, DOT1P2TC=0, DOT1P3TC=0, DOT1P4TC=0, DOT1P5TC=0, DOT1P6TC=0, DOT1P7TC=0"):
                    if_error = True
                break
    ONT_Qos_Ing_Pro_Name(driver,"0123456789012345678901234567890")
    ONT_Qos_Ing_Pro_0tc(driver,8)
    ONT_Qos_Ing_Pro_1tc(driver,8)
    ONT_Qos_Ing_Pro_2tc(driver,8)
    ONT_Qos_Ing_Pro_3tc(driver,8)
    ONT_Qos_Ing_Pro_4tc(driver,8)
    ONT_Qos_Ing_Pro_5tc(driver,8)
    ONT_Qos_Ing_Pro_6tc(driver,8)
    ONT_Qos_Ing_Pro_7tc(driver,8)
    ONT_Qos_Ing_Pro_Apply_Up(driver)
    if(driver.find_elements(By.CLASS_NAME, "listIngprof").__len__() == 0):
        if_find == False
    else:
        for index in range(driver.find_elements(By.CLASS_NAME, "listIngprof").__len__()):
            if(driver.find_elements(By.ID, "rpGponIngprof_name")[index].get_attribute("value") == "0123456789012345678901234567890"):
                if(driver.find_elements(By.NAME, "rpGponIngprof_rule")[index].get_attribute("textContent") != "DOT1P0TC=7, DOT1P1TC=7, DOT1P2TC=7, DOT1P3TC=7, DOT1P4TC=7, DOT1P5TC=7, DOT1P6TC=7, DOT1P7TC=7"):
                    if_error = True
                break
    ONT_Qos_Ing_Pro_Name(driver,"0123456789012345678901234567890")
    ONT_Qos_Ing_Pro_0tc(driver,1)
    ONT_Qos_Ing_Pro_1tc(driver,2)
    ONT_Qos_Ing_Pro_2tc(driver,3)
    ONT_Qos_Ing_Pro_3tc(driver,4)
    ONT_Qos_Ing_Pro_4tc(driver,5)
    ONT_Qos_Ing_Pro_5tc(driver,6)
    ONT_Qos_Ing_Pro_6tc(driver,7)
    ONT_Qos_Ing_Pro_7tc(driver,8)
    ONT_Qos_Ing_Pro_Apply_Up(driver)
    if(driver.find_elements(By.CLASS_NAME, "listIngprof").__len__() == 0):
        if_find == False
    else:
        for index in range(driver.find_elements(By.CLASS_NAME, "listIngprof").__len__()):
            if(driver.find_elements(By.ID, "rpGponIngprof_name")[index].get_attribute("value") == "0123456789012345678901234567890"):
                if(driver.find_elements(By.NAME, "rpGponIngprof_rule")[index].get_attribute("textContent") != "DOT1P0TC=0, DOT1P1TC=1, DOT1P2TC=2, DOT1P3TC=3, DOT1P4TC=4, DOT1P5TC=5, DOT1P6TC=6, DOT1P7TC=7"):
                    if_error = True
                break
    ONT_Qos_Ing_Pro_Name(driver,"0123456789012345678901234567890")
    ONT_Qos_Ing_Pro_0tc(driver,9)
    ONT_Qos_Ing_Pro_1tc(driver,9)
    ONT_Qos_Ing_Pro_2tc(driver,9)
    ONT_Qos_Ing_Pro_3tc(driver,9)
    ONT_Qos_Ing_Pro_4tc(driver,9)
    ONT_Qos_Ing_Pro_5tc(driver,9)
    ONT_Qos_Ing_Pro_6tc(driver,9)
    ONT_Qos_Ing_Pro_7tc(driver,9)
    ONT_Qos_Ing_Pro_Apply_Up(driver)
    if(driver.find_elements(By.CLASS_NAME, "listIngprof").__len__() == 0):
        if_find == False
    else:
        for index in range(driver.find_elements(By.CLASS_NAME, "listIngprof").__len__()):
            if(driver.find_elements(By.ID, "rpGponIngprof_name")[index].get_attribute("value") == "0123456789012345678901234567890"):
                if(driver.find_elements(By.NAME, "rpGponIngprof_rule")[index].get_attribute("textContent") != "DOT1P0TC=null, DOT1P1TC=null, DOT1P2TC=null, DOT1P3TC=null, DOT1P4TC=null, DOT1P5TC=null, DOT1P6TC=null, DOT1P7TC=null"):
                    if_error = True
                driver.find_elements(By.NAME, "rpGponIngprof_chkDel")[index].click()
                ONT_Qos_Ing_Pro_Apply_Down(driver)
                break
    
    if(if_find == False):
        print("-ONT Qos Ingress Profile- Apply Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
    else:
        if(if_error):
            print("-ONT Qos Ingress Profile- Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        else:
            print("-ONT Qos Ingress Profile- Pass",file = open("ONT_Status_Test_report.txt", '+a'))

# -------------------------end-------------------------
    
# Bandwidth Profile Test
# GPON > ONT Qos > Bandwidth Profile
# -------------------------start-------------------------

    if_find = False
    if_error = False
    mod.Tab_Switch(driver,"Bandwidth Profile")
    ONT_Qos_Ban_Pro_Name(driver,"0123456789012345678901234567890")
    ONT_Qos_Ban_Pro_SIR(driver,"0")
    ONT_Qos_Ban_Pro_AIR(driver,"0")
    ONT_Qos_Ban_Pro_PIR(driver,"0")
    ONT_Qos_Ban_Pro_Apply_Up(driver)
    if(driver.find_elements(By.CLASS_NAME, "listBwprof").__len__() == 0):
        if_find == False
    else:
        for index in range(driver.find_elements(By.CLASS_NAME, "listBwprof").__len__()):
            if(driver.find_elements(By.ID, "rpGponBwprof_name")[index].get_attribute("value") == "0123456789012345678901234567890"):
                if_find = True
                if(driver.find_elements(By.NAME, "rpGponBwprof_rule")[index].get_attribute("textContent") != "sir=0, air=0, pir=0"):
                    if_error = True
                break
    ONT_Qos_Ban_Pro_Name(driver,"0123456789012345678901234567890")
    ONT_Qos_Ban_Pro_SIR(driver,"2400001")
    ONT_Qos_Ban_Pro_AIR(driver,"2400000")
    ONT_Qos_Ban_Pro_PIR(driver,"2400000")
    ONT_Qos_Ban_Pro_Apply_Up(driver)
    if(mod.IsAlert(driver) == False):
        if_error = True
    ONT_Qos_Ban_Pro_SIR(driver,"2400000")
    ONT_Qos_Ban_Pro_AIR(driver,"2400001")
    ONT_Qos_Ban_Pro_Apply_Up(driver)
    if(mod.IsAlert(driver) == False):
        if_error = True
    ONT_Qos_Ban_Pro_AIR(driver,"2400000")
    ONT_Qos_Ban_Pro_PIR(driver,"2400001")
    ONT_Qos_Ban_Pro_Apply_Up(driver)
    if(mod.IsAlert(driver) == False):
        if_error = True
    ONT_Qos_Ban_Pro_PIR(driver,"2400000")
    ONT_Qos_Ban_Pro_Apply_Up(driver)
    if(driver.find_elements(By.CLASS_NAME, "listBwprof").__len__() == 0):
        if_find == False
    else:
        for index in range(driver.find_elements(By.CLASS_NAME, "listBwprof").__len__()):
            if(driver.find_elements(By.ID, "rpGponBwprof_name")[index].get_attribute("value") == "0123456789012345678901234567890"):
                if_find = True
                if(driver.find_elements(By.NAME, "rpGponBwprof_rule")[index].get_attribute("textContent") != "sir=2400000, air=2400000, pir=2400000"):
                    if_error = True
                driver.find_elements(By.NAME, "rpGponBwprof_chkDel")[index].click()
                ONT_Qos_Ban_Pro_Apply_Down(driver)
                break
    
    if(if_find == False):
        print("-ONT Qos Bandwidth Profile- Apply Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
    else:
        if(if_error):
            print("-ONT Qos Bandwidth Profile- Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        else:
            print("-ONT Qos Bandwidth Profile- Pass",file = open("ONT_Status_Test_report.txt", '+a'))


# -------------------------end-------------------------
    
# Pbit Profile Test
# GPON > ONT Qos > Pbit Profile
# -------------------------start-------------------------

    if_find = False
    if_error = False
    mod.Tab_Switch(driver,"Pbit Profile")
    ONT_Qos_Pbit_Pro_Name(driver,"0123456789012345678901234567890")
    ONT_Qos_Pbit_Pro_P0tc(driver,1)
    ONT_Qos_Pbit_Pro_P1tc(driver,2)
    ONT_Qos_Pbit_Pro_P2tc(driver,3)
    ONT_Qos_Pbit_Pro_P3tc(driver,4)
    ONT_Qos_Pbit_Pro_P4tc(driver,5)
    ONT_Qos_Pbit_Pro_P5tc(driver,6)
    ONT_Qos_Pbit_Pro_P6tc(driver,7)
    ONT_Qos_Pbit_Pro_P7tc(driver,8)
    ONT_Qos_Pbit_Pro_Apply_Up(driver)
    if(driver.find_elements(By.CLASS_NAME, "listPbitprof").__len__() == 0):
        if_find == False
    else:
        for index in range(driver.find_elements(By.CLASS_NAME, "listPbitprof").__len__()):
            if(driver.find_elements(By.ID, "rpGponPbitprof_name")[index].get_attribute("value") == "0123456789012345678901234567890"):
                if_find = True
                if(driver.find_elements(By.NAME, "rpGponPbitprof_rule")[index].get_attribute("textContent") != "P0to=0, P1to=1, P2to=2, P3to=3, P4to=4, P5to=5, P6to=6, P7to=7"):
                    if_error = True
                break
    ONT_Qos_Pbit_Pro_Name(driver,"0123456789012345678901234567890")
    ONT_Qos_Pbit_Pro_P0tc(driver,9)
    ONT_Qos_Pbit_Pro_P1tc(driver,9)
    ONT_Qos_Pbit_Pro_P2tc(driver,9)
    ONT_Qos_Pbit_Pro_P3tc(driver,9)
    ONT_Qos_Pbit_Pro_P4tc(driver,9)
    ONT_Qos_Pbit_Pro_P5tc(driver,9)
    ONT_Qos_Pbit_Pro_P6tc(driver,9)
    ONT_Qos_Pbit_Pro_P7tc(driver,9)
    ONT_Qos_Pbit_Pro_Apply_Up(driver)
    if(driver.find_elements(By.CLASS_NAME, "listPbitprof").__len__() == 0):
        if_find == False
    else:
        for index in range(driver.find_elements(By.CLASS_NAME, "listPbitprof").__len__()):
            if(driver.find_elements(By.ID, "rpGponPbitprof_name")[index].get_attribute("value") == "0123456789012345678901234567890"):
                if_find = True
                if(driver.find_elements(By.NAME, "rpGponPbitprof_rule")[index].get_attribute("textContent") != "P0to=drop, P1to=drop, P2to=drop, P3to=drop, P4to=drop, P5to=drop, P6to=drop, P7to=drop"):
                    if_error = True
                driver.find_elements(By.NAME, "rpGponPbitprof_chkDel")[index].click()
                ONT_Qos_Pbit_Pro_Apply_Down(driver)
                break
    
    if(if_find == False):
        print("-ONT Qos Pbit Profile- Apply Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
    else:
        if(if_error):
            print("-ONT Qos Pbit Profile- Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        else:
            print("-ONT Qos Pbit Profile- Pass",file = open("ONT_Status_Test_report.txt", '+a'))

# -------------------------end-------------------------
    
# CAC Profile Test
# GPON > ONT Qos > CAC Profile
# -------------------------start-------------------------

    if_find = False
    if_error = False
    mod.Tab_Switch(driver,"CAC Profile")
    ONT_Qos_CAC_Pro_Name(driver,"0123456789012345678901234567890")
    ONT_Qos_CAC_Pro_Bandwidth(driver,"0")
    ONT_Qos_CAC_Pro_Apply_Up(driver)
    if(driver.find_elements(By.CLASS_NAME, "listCacprof").__len__() == 0):
        if_find == False
    else:
        for index in range(driver.find_elements(By.CLASS_NAME, "listCacprof").__len__()):
            if(driver.find_elements(By.ID, "rpGponCacprof_name")[index].get_attribute("value") == "0123456789012345678901234567890"):
                if_find = True
                if(driver.find_elements(By.NAME, "rpGponCacprof_mcastBw")[index].get_attribute("textContent") != "100"):
                    if_error = True
                break
    ONT_Qos_CAC_Pro_Name(driver,"0123456789012345678901234567890")
    ONT_Qos_CAC_Pro_Bandwidth(driver,"1200000")
    ONT_Qos_CAC_Pro_Apply_Up(driver)
    if(driver.find_elements(By.CLASS_NAME, "listCacprof").__len__() == 0):
        if_find == False
    else:
        for index in range(driver.find_elements(By.CLASS_NAME, "listCacprof").__len__()):
            if(driver.find_elements(By.ID, "rpGponCacprof_name")[index].get_attribute("value") == "0123456789012345678901234567890"):
                if_find = True
                if(driver.find_elements(By.NAME, "rpGponCacprof_mcastBw")[index].get_attribute("textContent") != "1200000"):
                    if_error = True
                driver.find_elements(By.NAME, "rpGponCacprof_chkDel")[index].click()
                ONT_Qos_CAC_Pro_Apply_Down(driver)
                break
    
    if(if_find == False):
        print("-ONT Qos CAC Profile- Apply Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
    else:
        if(if_error):
            print("-ONT Qos CAC Profile- Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        else:
            print("-ONT Qos CAC Profile- Pass",file = open("ONT_Status_Test_report.txt", '+a'))

# -------------------------end-------------------------
    
# WRED/DS-Meter Test
# GPON > ONT Qos > WRED/DS-Meter
# -------------------------start-------------------------

    if_error = False
    mod.Tab_Switch(driver,"WRED/DS-Meter")
    ONT_Qos_WRED_WRED_Enable(driver)
    ONT_Qos_WRED_DS_CIR(driver)
    ONT_Qos_WRED_Apply(driver)
    if(driver.find_elements(By.NAME, "rpGponQosDsMeter_wred")[1].is_selected() != True or driver.find_elements(By.NAME, "rpGponQosDsMeter_dsmeter")[1].is_selected() != True):
        if_error = True
    ONT_Qos_WRED_WRED_Disable(driver)
    ONT_Qos_WRED_DS_PIR(driver)
    ONT_Qos_WRED_Apply(driver)
    if(driver.find_elements(By.NAME, "rpGponQosDsMeter_wred")[0].is_selected() != True or driver.find_elements(By.NAME, "rpGponQosDsMeter_dsmeter")[0].is_selected() != True):
        if_error = True
    
    if(if_error):
        print("-ONT Qos WRED/DS-Meter- Fail",file = open("ONT_Status_Test_report.txt", '+a'))
    else:
        print("-ONT Qos WRED/DS-Meter- Pass",file = open("ONT_Status_Test_report.txt", '+a'))

# -------------------------end-------------------------
    
# ONT Model Test
# GPON > ONT Model
# -------------------------start-------------------------

    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"ONT Model")
    mod.Switch_Frame(driver)
    ONT_Model_Name(driver,"01234567890123")
    ONT_Model_ID(driver,"8")
    ONT_Model_VV(driver,"01234567890123")
    ONT_Model_SV(driver,"01234567890123")
    ONT_Model_Card1(driver,"254")
    ONT_Model_Card2(driver,"253")
    ONT_Model_Card3(driver,"252")
    ONT_Model_Card4(driver,"251")
    ONT_Model_Card5(driver,"250")
    ONT_Model_Apply_Up(driver)
    if_find = False
    if(driver.find_elements(By.CLASS_NAME, "listOntModel").__len__() == 0):
        print("-ONT Model- Apply Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
    else:
        for index in range(driver.find_elements(By.CLASS_NAME, "listOntModel").__len__()):
            if(driver.find_elements(By.ID, "rpGponOntModel_name")[index].get_attribute("value") == "01234567890123"):
                if_find = True
                if(driver.find_elements(By.NAME, "rpGponOntModel_rule")[index].get_attribute("textContent") != "model ID=8, vendor version=01234567890123, software version=01234567890123, card1=254, card2=253, card3=252, card4=251, card5=250"):
                    print("-ONT Model- Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                else:
                    print("-ONT Model- Pass",file = open("ONT_Status_Test_report.txt", '+a'))
                driver.find_elements(By.NAME, "rpGponOntModel_chkDel")[index].click()
                ONT_Model_Apply_Down(driver)
                break
        if(if_find == False):
            print("-ONT Model- Apply Not Found",file = open("ONT_Status_Test_report.txt", '+a'))

# -------------------------end-------------------------
    
# File Transfer Test
# GPON > File Transfer
# -------------------------start-------------------------

    # 導向路徑Status
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"ONT Quick Setup")
    mod.Switch_Frame(driver)
    time.sleep(1)
    mod.Tab_Switch(driver,"Status")
    retry = True
    counter = 0
    while retry and counter <= 25:
        try:
            Slot_Select(driver,slot)
            retry = False
        except:
            counter = counter+1
            retry = True
        time.sleep(0.5)
        if(mod.IsAlert(driver)):
            break
        if(counter == 26):
            driver.find_element(By.ID, "dontexist")
        time.sleep(0.5)
    retry = True
    counter = 0
    while retry and counter <= 20:
        try:
            ONT_Qui_Port_Select(driver,pon)
            time.sleep(0.5)
            ONT_Qui_Sta_Load(driver)
            time.sleep(1)
            ONT_Qui_Sta_Load(driver)
            time.sleep(0.5)
            retry = False
        except:
            counter = counter+1
            retry = True
        if(counter == 21):
            driver.find_element(By.ID, "dontexist")

    # Check Status的IS
    ont_aid = f"{slot}{pon}{aid}"
    retry = True
    now_page = 1
    while retry:
        row_num = 0
        retry_2 = True
        while retry_2:
            try:
                characters = "ont-"
                now_aid = driver.find_elements(By.CLASS_NAME, "td-table-content.rpGponOntStatus_ontAid")[row_num].get_attribute("textContent")
                for i in range(len(characters)):
                    now_aid = now_aid.replace(characters[i],"")
                if(now_aid == ont_aid):
                    retry = False
                    retry_2 = False
                    if(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_actStatus")[row_num].get_attribute("textContent") == "IS"):
                        print("-Status- IS",file = open("ONT_Status_Test_report.txt", '+a'))
                    else:
                        print("-Status- NOT IS",file = open("ONT_Status_Test_report.txt", '+a'))
                    break
                else:
                    if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                        row_num = row_num+1
                    else:
                        retry_2 = False
            except:
                if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                    row_num = row_num+1
                else:
                    retry_2 = False
        if(now_page < ONT_Qui_Page_Total(driver)):
            ONT_Qui_Next(driver)
            time.sleep(1)
            now_page = now_page+1
        elif(retry == True):
            retry = False
            print ("-Status- ONT Not Found",file = open("ONT_Status_Test_report.txt", '+a'))

    if_error = False
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"File Transfer")
    mod.Switch_Frame(driver)
    try:
        File_Transfer_ONT(driver,slot,pon,aid)
        time.sleep(1)
        File_Transfer_LFN(driver,"0123456789012345678901234")
        File_Transfer_URI(driver,"0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789")
        File_Transfer_UN(driver,"0123456789012345678901234")
        File_Transfer_PW(driver,"0123456789012345678901234")
        File_Transfer_Upload(driver)
    except:
        if_error = True
    try:
        File_Transfer_ONT(driver,slot,pon,aid)
        time.sleep(1)
        File_Transfer_LFN(driver,"0123456789012345678901234")
        File_Transfer_URI(driver,"0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789")
        File_Transfer_UN(driver,"0123456789012345678901234")
        File_Transfer_PW(driver,"0123456789012345678901234")
        File_Transfer_Download(driver)
    except:
        if_error = True
    if(if_error):
        print("-File Transfer- Fail",file = open("ONT_Status_Test_report.txt", '+a'))
    else:
        print("-File Transfer- Pass",file = open("ONT_Status_Test_report.txt", '+a'))

# -------------------------end-------------------------

    print("Test Finishd",file = open("ONT_Status_Test_report.txt", '+a'))
    print("======================================================================================",file = open("ONT_Status_Test_report.txt", '+a'))

def ONT_Profile_Max_Capacity_Check(driver,slot,pon,aid):

    print(f"ONT Profile Max Capacity Check\nTest Start",file = open("ONT_Status_Test_report.txt", '+a'))

    # ONT Alarm Profile Test
    # GPON > ONT Alarm Profile
    # -------------------------start-------------------------

    # 導向路徑ONT Quick Setup > ONT Alarm Profile
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"GPON")
    mod.SubPage_Switch(driver,"ONT Alarm Profile")
    mod.Switch_Frame(driver)
    if_full = False
    input_name = 1001
    while if_full == False:
        ONT_Ala_Name(driver,input_name)
        ONT_Ala_Apply_Up(driver)
        input_name = input_name+1
        try:
            driver.find_element(By.CLASS_NAME, "toast-message").get_attribute("textContent")
            if_full = True
            print("ONT Alarm Max Capacity =",driver.find_elements(By.CLASS_NAME, "td-table-content.i1")[-1].get_attribute("textContent"),file = open("ONT_Status_Test_report.txt", '+a'))
        except:
            pass

    # -------------------------end-------------------------

    # ONT VoIP Profile Test
    # GPON > ONT VoIP Profile
    # -------------------------start-------------------------

    # 導向路徑ONT Quick Setup > ONT VoIP Common Profile
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"GPON")
    mod.SubPage_Switch(driver,"ONT VoIP Profile")
    mod.Switch_Frame(driver)
    if_full = False
    input_name = 1001
    while if_full == False:
        ONT_VoIP_Com_Name(driver,input_name)
        ONT_VoIP_Com_Apply_Up(driver)
        input_name = input_name+1
        try:
            driver.find_element(By.CLASS_NAME, "toast-message")
            if_full = True
            print("ONT VoIP Common Max Capacity =",driver.find_elements(By.CLASS_NAME, "td-table-content-center.i1")[-1].get_attribute("textContent"),file = open("ONT_Status_Test_report.txt", '+a'))
        except:
            pass

    # 導向路徑ONT Quick Setup > ONT VoIP SIP Profile
    mod.Find_by_link_text_wait_click(driver,"VoIP SIP Profile",40)
    if_full = False
    input_name = 1001
    while if_full == False:
        ONT_VoIP_SIP_Name(driver,input_name)
        ONT_VoIP_SIP_Apply_Up(driver)
        input_name = input_name+1
        try:
            driver.find_element(By.CLASS_NAME, "toast-message")
            if_full = True
            print("ONT VoIP SIP Max Capacity =",driver.find_elements(By.CLASS_NAME, "td-table-content-center.i1")[-1].get_attribute("textContent"),file = open("ONT_Status_Test_report.txt", '+a'))
        except:
            pass

    # 導向路徑ONT Quick Setup > ONT VoIP Dial Plan Profile
    mod.Find_by_link_text_wait_click(driver,"VoIP Dial Plan Profile",40)
    if_full = False
    input_name = 1001
    while if_full == False:
        ONT_VoIP_Dial_Name(driver,input_name)
        ONT_VoIP_Dial_Apply_Up(driver)
        input_name = input_name+1
        try:
            driver.find_element(By.CLASS_NAME, "toast-message")
            if_full = True
            print("ONT VoIP Dial Plan Max Capacity =",driver.find_elements(By.CLASS_NAME, "td-table-content-center.i1")[-1].get_attribute("textContent"),file = open("ONT_Status_Test_report.txt", '+a'))
        except:
            pass

    # -------------------------end-------------------------

    # ONT Qos Profile Test
    # GPON > ONT Qos
    # -------------------------start-------------------------

    # 導向路徑ONT Quick Setup > ONT Qos > Ingress Profile
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"GPON")
    mod.SubPage_Switch(driver,"ONT Qos")
    mod.Switch_Frame(driver)
    if_full = False
    input_name = 1001
    while if_full == False:
        ONT_Qos_Ing_Pro_Name(driver,input_name)
        ONT_Qos_Ing_Pro_Apply_Up(driver)
        input_name = input_name+1
        try:
            driver.find_element(By.CLASS_NAME, "toast-message")
            if_full = True
            print("ONT Qos Ingress Profile Max Capacity =",driver.find_elements(By.CLASS_NAME, "td-table-content.i1")[-1].get_attribute("textContent"),file = open("ONT_Status_Test_report.txt", '+a'))
        except:
            pass

    # 導向路徑ONT Quick Setup > ONT Qos > Bandwidth Profile
    mod.Find_by_link_text_wait_click(driver,"Bandwidth Profile",40)
    if_full = False
    input_name = 1001
    while if_full == False:
        ONT_Qos_Ban_Pro_Name(driver,input_name)
        ONT_Qos_Ban_Pro_SIR(driver,"0")
        ONT_Qos_Ban_Pro_AIR(driver,"0")
        ONT_Qos_Ban_Pro_PIR(driver,"0")
        ONT_Qos_Ban_Pro_Apply_Up(driver)
        input_name = input_name+1
        try:
            driver.find_element(By.CLASS_NAME, "toast-message")
            if_full = True
            print("ONT Qos Bandwidth Profile Max Capacity =",driver.find_elements(By.CLASS_NAME, "td-table-content.i1")[-1].get_attribute("textContent"),file = open("ONT_Status_Test_report.txt", '+a'))
        except:
            pass

    # 導向路徑ONT Quick Setup > ONT Qos > Pbit Profile
    mod.Find_by_link_text_wait_click(driver,"Pbit Profile",40)
    if_full = False
    input_name = 1001
    while if_full == False:
        ONT_Qos_Pbit_Pro_Name(driver,input_name)
        ONT_Qos_Pbit_Pro_Apply_Up(driver)
        input_name = input_name+1
        try:
            driver.find_element(By.CLASS_NAME, "toast-message")
            if_full = True
            print("ONT Qos Pbit Profile Max Capacity =",driver.find_elements(By.CLASS_NAME, "td-table-content.i1")[-1].get_attribute("textContent"),file = open("ONT_Status_Test_report.txt", '+a'))
        except:
            pass

    # 導向路徑ONT Quick Setup > ONT Qos > CAC Profile
    mod.Find_by_link_text_wait_click(driver,"CAC Profile",40)
    if_full = False
    input_name = 1001
    while if_full == False:
        ONT_Qos_CAC_Pro_Name(driver,input_name)
        ONT_Qos_CAC_Pro_Bandwidth(driver,"100")
        ONT_Qos_CAC_Pro_Apply_Up(driver)
        input_name = input_name+1
        try:
            driver.find_element(By.CLASS_NAME, "toast-message")
            if_full = True
            print("ONT Qos CAC Profile Max Capacity =",driver.find_elements(By.CLASS_NAME, "td-table-content.i1")[-1].get_attribute("textContent"),file = open("ONT_Status_Test_report.txt", '+a'))
        except:
            pass

    # -------------------------end-------------------------

    # ONT Quick Setup & ONT Status Profile Test
    # GPON > ONT Quick Setup
    # -------------------------start-------------------------

    slot_num = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15"]

    # 導向路徑ONT Quick Setup > ONT Quick Setup
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"GPON")
    mod.SubPage_Switch(driver,"ONT Quick Setup")
    mod.Switch_Frame(driver)
    for test_pon in range(15):
        mod.Find_by_xpath_wait_click(driver,f"//*[@id='lctbl_selSlot']/option[{slot}]",50)
        ONT_Qui_Port_Select(driver,test_pon+1)
        ONT_Qui_ONT_Qui_Load(driver)
        for test_page in range(4):
            test_sn = 1700000000000000+(test_pon+1)*100000000000+(test_page+1)*100000000
            driver.find_element(By.NAME, "rpGponOntSetup_chkAllActive").click()
            driver.find_element(By.ID, "rpGponOntSteup_allTxtSn").send_keys(test_sn)
            driver.find_element(By.NAME, "rpGponOntSetup_saChkSNStep").click()
            driver.find_element(By.ID, "rpGponOntSteup_allTxtPw").send_keys("12345678901234567890")
            # driver.find_element(By.ID, "rpGponOntSteup_txtDes_all").send_keys("1234567890123456789012345678901")
            Select(driver.find_element(By.ID, "allPortTemp")).select_by_visible_text(f"pon-{slot}-{pon}")
            Select(driver.find_element(By.ID, "allOntTemp")).select_by_visible_text(f"Template-{slot}-{pon}-128")
            Select(driver.find_element(By.ID, "allAction")).select_by_visible_text("Add")
            ONT_Qui_ONT_Qui_Apply(driver)
            if(test_page < 3):
                ONT_Qui_ONT_Qui_Next(driver)

        # 導向路徑Status
        mod.Tab_Switch(driver,"Status")
        time.sleep(2)
        mod.Find_by_xpath_wait_click(driver,f"//*[@id='lctbl_selSlot']/option[{slot}]",50)
        ONT_Qui_Port_Select(driver,test_pon+1)
        ONT_Qui_Sta_Load(driver)
        for click in range(3):
            mod.Find_by_id_wait_click(driver,"btnNextPage",40)
        string = driver.find_elements(By.NAME, "rpGponOntStatus_ontAid")[-1].get_attribute("textContent")
        string = string.split("-")[3]
        print(f"ONT {slot}-{test_pon+1} Status Max Capacity ={string}",file = open("ONT_Status_Test_report.txt", '+a'))

        # 導向路徑ONT Quick Setup
        mod.Tab_Switch(driver,"ONT Quick Setup")
        mod.Find_by_xpath_wait_click(driver,f"//*[@id='lctbl_selSlot']/option[{slot}]",50)
        ONT_Qui_Port_Select(driver,test_pon+1)
        ONT_Qui_ONT_Qui_Load(driver)
        for test_page in range(4):
            driver.find_element(By.ID, "rpGponOntSteup_allTxtPw").send_keys("98765432109876543210")
            Select(driver.find_element(By.ID, "allAction")).select_by_visible_text("Modify")
            ONT_Qui_ONT_Qui_Apply(driver)
            if(test_page < 3):
                ONT_Qui_ONT_Qui_Next(driver)

        # 導向路徑Status
        mod.Tab_Switch(driver,"Status")
        time.sleep(2)
        mod.Find_by_xpath_wait_click(driver,f"//*[@id='lctbl_selSlot']/option[{slot}]",50)
        ONT_Qui_Port_Select(driver,test_pon+1)
        ONT_Qui_Sta_Load(driver)
        for click in range(3):
            mod.Find_by_id_wait_click(driver,"btnNextPage",40)
        if(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_cfgPw")[-1].get_attribute("textContent") == "98765432109876543210"):
            print(f"ONT {slot}-{test_pon+1} Status Modify Test Pass",file = open("ONT_Status_Test_report.txt", '+a'))
        else:
            print(f"ONT {slot}-{test_pon+1} Status Modify Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))

        # 導向路徑ONT Quick Setup
        mod.Tab_Switch(driver,"ONT Quick Setup")
        mod.Find_by_xpath_wait_click(driver,f"//*[@id='lctbl_selSlot']/option[{slot}]",50)
        ONT_Qui_Port_Select(driver,test_pon+1)
        ONT_Qui_ONT_Qui_Load(driver)
        for test_page in range(4):
            Select(driver.find_element(By.ID, "allAction")).select_by_visible_text("Delete")
            ONT_Qui_ONT_Qui_Apply(driver)
            if(test_page < 3):
                ONT_Qui_ONT_Qui_Next(driver)

    # -------------------------end-------------------------

    # Delete ONT Profile Data
    # -------------------------start-------------------------

    try:

        # 導向路徑ONT Quick Setup > ONT Qos
        mod.Switch_Default(driver)
        mod.Page_Switch(driver,"GPON")
        mod.SubPage_Switch(driver,"ONT Qos")
        mod.Switch_Frame(driver)
        driver.find_element(By.NAME, "rpGponIngprof_chkAllDel").click()
        driver.find_element(By.ID, "rpGponIngprof_btnDel").click()
        mod.Find_by_link_text_wait_click(driver,"Bandwidth Profile",40)
        driver.find_element(By.NAME, "rpGponBwprof_chkAllDel").click()
        driver.find_element(By.ID, "rpGponBwprof_btnDel").click()
        mod.Find_by_link_text_wait_click(driver,"Pbit Profile",40)
        driver.find_element(By.NAME, "rpGponPbitprof_chkAllDel").click()
        driver.find_element(By.ID, "rpGponPbitprof_btnDel").click()
        mod.Find_by_link_text_wait_click(driver,"CAC Profile",40)
        driver.find_element(By.NAME, "rpGponCacprof_chkAllDel").click()
        driver.find_element(By.ID, "rpGponCacprof_btnDel").click()

        # 導向路徑ONT Quick Setup > ONT VoIP Profile
        mod.Switch_Default(driver)
        mod.Page_Switch(driver,"GPON")
        mod.SubPage_Switch(driver,"ONT VoIP Profile")
        mod.Switch_Frame(driver)
        driver.find_element(By.NAME, "rpGponVoipCommon_chkAllDel").click()
        driver.find_element(By.ID, "rpGponVoipCommon_btnDel").click()
        mod.Find_by_link_text_wait_click(driver,"VoIP SIP Profile",40)
        driver.find_element(By.NAME, "rpGponVoipSip_chkAllDel").click()
        driver.find_element(By.ID, "rpGponVoipSip_btnDel").click()
        mod.Find_by_link_text_wait_click(driver,"VoIP Dial Plan Profile",40)
        driver.find_element(By.NAME, "rpGponVoipDialPlan_chkAllDel").click()
        driver.find_element(By.ID, "rpGponVoipDialPlan_btnDel").click()
        
        # 導向路徑ONT Quick Setup > ONT VoIP Profile
        mod.Switch_Default(driver)
        mod.Page_Switch(driver,"GPON")
        mod.SubPage_Switch(driver,"ONT Alarm Profile")
        mod.Switch_Frame(driver)
        driver.find_element(By.NAME, "rpGponOntAlarmprof_chkAllDel").click()
        driver.find_element(By.ID, "rpGponOntAlarmprof_btnDel").click()

        print("ONT Profile Data Reset Pass",file = open("ONT_Status_Test_report.txt", '+a'))

    except:
        print("ONT Profile Data Reset Fail",file = open("ONT_Status_Test_report.txt", '+a'))
    
    # -------------------------end-------------------------

    print("Test Finishd",file = open("ONT_Status_Test_report.txt", '+a'))
    print("======================================================================================",file = open("ONT_Status_Test_report.txt", '+a'))

# ONT Alarm Profile

def ONT_Ala_Name(driver,name):
    input = driver.find_element(By.ID, "rpGponOntAlarmprof_addName")
    input.clear()
    input.send_keys(name)

def ONT_Ala_LBCT_Low(driver,vlaue):
    input = driver.find_element(By.ID, "rpGponOntAlarmprof_lowCurr")
    input.clear()
    input.send_keys(vlaue)

def ONT_Ala_LBCT_Up(driver,vlaue):
    input = driver.find_element(By.ID, "rpGponOntAlarmprof_upCurr")
    input.clear()
    input.send_keys(vlaue)

def ONT_Ala_RPT_Low(driver,vlaue):
    input = driver.find_element(By.ID, "rpGponOntAlarmprof_lowRxPwr")
    input.clear()
    input.send_keys(vlaue)

def ONT_Ala_RPT_Up(driver,vlaue):
    input = driver.find_element(By.ID, "rpGponOntAlarmprof_upRxPwr")
    input.clear()
    input.send_keys(vlaue)

def ONT_Ala_TT_Low(driver,vlaue):
    input = driver.find_element(By.ID, "rpGponOntAlarmprof_lowTemp")
    input.clear()
    input.send_keys(vlaue)

def ONT_Ala_TT_Up(driver,vlaue):
    input = driver.find_element(By.ID, "rpGponOntAlarmprof_upTemp")
    input.clear()
    input.send_keys(vlaue)

def ONT_Ala_TPT_Low(driver,vlaue):
    input = driver.find_element(By.ID, "rpGponOntAlarmprof_lowTxPwr")
    input.clear()
    input.send_keys(vlaue)

def ONT_Ala_TPT_Up(driver,vlaue):
    input = driver.find_element(By.ID, "rpGponOntAlarmprof_upTxPwr")
    input.clear()
    input.send_keys(vlaue)

def ONT_Ala_PFVT_Low(driver,vlaue):
    input = driver.find_element(By.ID, "rpGponOntAlarmprof_lowVolt")
    input.clear()
    input.send_keys(vlaue)

def ONT_Ala_PFVT_Up(driver,vlaue):
    input = driver.find_element(By.ID, "rpGponOntAlarmprof_upVolt")
    input.clear()
    input.send_keys(vlaue)

def ONT_Ala_Apply_Up(driver):
    driver.find_element(By.ID, "rpGponOntAlarmprof_btnAdd").click()

def ONT_Ala_Apply_Down(driver):
    driver.find_element(By.ID, "rpGponOntAlarmprof_btnDel").click()

# ONT VoIP Profile

# ONT VoIP Profile -> VoIP Common Profile

def ONT_VoIP_Com_Name(driver,name):
    input = driver.find_element(By.ID, "rpGponVoipCommon_addName")
    input.clear()
    input.send_keys(name)

def ONT_VoIP_Com_min_Local_Port(driver,vlaue):
    input = driver.find_element(By.ID, "rpGponVoipCommon_minPort")
    input.clear()
    input.send_keys(vlaue)

def ONT_VoIP_Com_max_Local_Port(driver,vlaue):
    input = driver.find_element(By.ID, "rpGponVoipCommon_maxPort")
    input.clear()
    input.send_keys(vlaue)

def ONT_VoIP_Com_dscp_mark(driver,vlaue):
    input = driver.find_element(By.ID, "rpGponVoipCommon_dscpMark")
    input.clear()
    input.send_keys(vlaue)

def ONT_VoIP_Com_piggyback(driver,request):
    check_box = driver.find_element(By.NAME, "rpGponVoipCommon_piggyback")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ONT_VoIP_Com_tone(driver,request):
    check_box = driver.find_element(By.NAME, "rpGponVoipCommon_tone")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ONT_VoIP_Com_dtmf(driver,request):
    check_box = driver.find_element(By.NAME, "rpGponVoipCommon_dtmf")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ONT_VoIP_Com_cas(driver,request):
    check_box = driver.find_element(By.NAME, "rpGponVoipCommon_cas")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ONT_VoIP_Com_jitter_target(driver,vlaue):
    input = driver.find_element(By.ID, "rpGponVoipCommon_jitterTarget")
    input.clear()
    input.send_keys(vlaue)

def ONT_VoIP_Com_max_jitter_buffer(driver,vlaue):
    input = driver.find_element(By.ID, "rpGponVoipCommon_jitterBuf")
    input.clear()
    input.send_keys(vlaue)

def ONT_VoIP_Com_ptsn_protocol(driver,vlaue):
    input = driver.find_element(By.ID, "rpGponVoipCommon_pstn")
    input.clear()
    input.send_keys(vlaue)

def ONT_VoIP_Com_announce_type(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpGponVoipCommon_announce']/option[{sel}]")
    select.click()

def ONT_VoIP_Com_echo_cancel(driver,request):
    check_box = driver.find_element(By.NAME, "rpGponVoipCommon_echo")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ONT_VoIP_Com_fax_mode(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpGponVoipCommon_fax']/option[{sel}]")
    select.click()

def ONT_VoIP_Com_1st_codec(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpGponVoipCommon_1stCodec']/option[{sel}]")
    select.click()

def ONT_VoIP_Com_2nd_codec(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpGponVoipCommon_2ndCodec']/option[{sel}]")
    select.click()

def ONT_VoIP_Com_3rd_codec(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpGponVoipCommon_3rdCodec']/option[{sel}]")
    select.click()

def ONT_VoIP_Com_4th_codec(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpGponVoipCommon_4thCodec']/option[{sel}]")
    select.click()

def ONT_VoIP_Com_1st_packet_period(driver,vlaue):
    input = driver.find_element(By.ID, "rpGponVoipCommon_1stPktPeriod")
    input.clear()
    input.send_keys(vlaue)

def ONT_VoIP_Com_2nd_packet_period(driver,vlaue):
    input = driver.find_element(By.ID, "rpGponVoipCommon_2ndPktPeriod")
    input.clear()
    input.send_keys(vlaue)

def ONT_VoIP_Com_3rd_packet_period(driver,vlaue):
    input = driver.find_element(By.ID, "rpGponVoipCommon_3rdPktPeriod")
    input.clear()
    input.send_keys(vlaue)

def ONT_VoIP_Com_4th_packet_period(driver,vlaue):
    input = driver.find_element(By.ID, "rpGponVoipCommon_4thPktPeriod")
    input.clear()
    input.send_keys(vlaue)

def ONT_VoIP_Com_1st_silence(driver,request):
    check_box = driver.find_element(By.NAME, "rpGponVoipCommon_1stSilence")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ONT_VoIP_Com_2nd_silence(driver,request):
    check_box = driver.find_element(By.NAME, "rpGponVoipCommon_2ndSilence")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ONT_VoIP_Com_3rd_silence(driver,request):
    check_box = driver.find_element(By.NAME, "rpGponVoipCommon_3rdSilence")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ONT_VoIP_Com_4th_silence(driver,request):
    check_box = driver.find_element(By.NAME, "rpGponVoipCommon_4thSilence")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ONT_VoIP_Com_oob_dtmf(driver,request):
    check_box = driver.find_element(By.NAME, "rpGponVoipCommon_oobDtmf")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ONT_VoIP_Com_signal_code(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpGponVoipCommon_signalCode']/option[{sel}]")
    select.click()

def ONT_VoIP_Com_Apply_Up(driver):
    driver.find_element(By.ID, "rpGponVoipCommon_btnAdd").click()

def ONT_VoIP_Com_Apply_Down(driver):
    driver.find_element(By.ID, "rpGponVoipCommon_btnDel").click()

# ONT VoIP Profile -> VoIP SIP Profile

def ONT_VoIP_SIP_Name(driver,name):
    input = driver.find_element(By.ID, "rpGponVoipSip_addName")
    input.clear()
    input.send_keys(name)

def ONT_VoIP_SIP_PSA(driver,value):
    input = driver.find_element(By.ID, "rpGponVoipSip_proxyAddr")
    input.clear()
    input.send_keys(value)

def ONT_VoIP_SIP_OPA(driver,value):
    input = driver.find_element(By.ID, "rpGponVoipSip_outbandAddr")
    input.clear()
    input.send_keys(value)

def ONT_VoIP_SIP_PD(driver,value):
    input = driver.find_element(By.ID, "rpGponVoipSip_priDns")
    input.clear()
    input.send_keys(value)

def ONT_VoIP_SIP_SD(driver,value):
    input = driver.find_element(By.ID, "rpGponVoipSip_secDns")
    input.clear()
    input.send_keys(value)

def ONT_VoIP_SIP_RET(driver,value):
    input = driver.find_element(By.ID, "rpGponVoipSip_regExpTime")
    input.clear()
    input.send_keys(value)

def ONT_VoIP_SIP_RHST(driver,value):
    input = driver.find_element(By.ID, "rpGponVoipSip_reregHeadStartTime")
    input.clear()
    input.send_keys(value)

def ONT_VoIP_SIP_HPU(driver,value):
    input = driver.find_element(By.ID, "rpGponVoipSip_hostPartUri")
    input.clear()
    input.send_keys(value)

def ONT_VoIP_SIP_SR(driver,value):
    input = driver.find_element(By.ID, "rpGponVoipSip_registrar")
    input.clear()
    input.send_keys(value)

def ONT_VoIP_SIP_S(driver,value):
    input = driver.find_element(By.ID, "rpGponVoipSip_softswitch")
    input.clear()
    input.send_keys(value)
    
def ONT_VoIP_SIP_CI_cal_num(driver,request):
    check_box = driver.find_element(By.NAME, "rpGponVoipSip_calNum")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def ONT_VoIP_SIP_CI_cal_nam(driver,request):
    check_box = driver.find_element(By.NAME, "rpGponVoipSip_calNam")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def ONT_VoIP_SIP_CI_cid_bio(driver,request):
    check_box = driver.find_element(By.NAME, "rpGponVoipSip_cidBlo")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def ONT_VoIP_SIP_CI_cid_num(driver,request):
    check_box = driver.find_element(By.NAME, "rpGponVoipSip_cidNum")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def ONT_VoIP_SIP_CI_cid_nam(driver,request):
    check_box = driver.find_element(By.NAME, "rpGponVoipSip_cidNam")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def ONT_VoIP_SIP_CI_ACR(driver,request):
    check_box = driver.find_element(By.NAME, "rpGponVoipSip_acr")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def ONT_VoIP_SIP_CW_cal_wai(driver,request):
    check_box = driver.find_element(By.NAME, "rpGponVoipSip_calWai")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def ONT_VoIP_SIP_CW_cid_ann(driver,request):
    check_box = driver.find_element(By.NAME, "rpGponVoipSip_cidAnn")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def ONT_VoIP_SIP_CPOT_3way(driver,request):
    check_box = driver.find_element(By.NAME, "rpGponVoipSip_3way")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def ONT_VoIP_SIP_CPOT_cal_tra(driver,request):
    check_box = driver.find_element(By.NAME, "rpGponVoipSip_calTra")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def ONT_VoIP_SIP_CPOT_cal_hol(driver,request):
    check_box = driver.find_element(By.NAME, "rpGponVoipSip_calHol")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def ONT_VoIP_SIP_CPOT_cal_par(driver,request):
    check_box = driver.find_element(By.NAME, "rpGponVoipSip_calPar")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def ONT_VoIP_SIP_CPOT_not_dis(driver,request):
    check_box = driver.find_element(By.NAME, "rpGponVoipSip_notDis")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def ONT_VoIP_SIP_CPOT_flash(driver,request):
    check_box = driver.find_element(By.NAME, "rpGponVoipSip_flash")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def ONT_VoIP_SIP_CPOT_origin(driver,request):
    check_box = driver.find_element(By.NAME, "rpGponVoipSip_origin")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def ONT_VoIP_SIP_CPOT_6way(driver,request):
    check_box = driver.find_element(By.NAME, "rpGponVoipSip_6way")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def ONT_VoIP_SIP_CP_spl_rin(driver,request):
    check_box = driver.find_element(By.NAME, "rpGponVoipSip_splRin")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def ONT_VoIP_SIP_CP_dia_ton(driver,request):
    check_box = driver.find_element(By.NAME, "rpGponVoipSip_diaTon")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def ONT_VoIP_SIP_CP_vis_ind(driver,request):
    check_box = driver.find_element(By.NAME, "rpGponVoipSip_visInd")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def ONT_VoIP_SIP_CP_cal_for(driver,request):
    check_box = driver.find_element(By.NAME, "rpGponVoipSip_calFor")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def ONT_VoIP_SIP_DC_enable(driver,request):
    check_box = driver.find_element(By.NAME, "rpGponVoipSip_enable")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()
    
def ONT_VoIP_SIP_DC_dia_opt(driver,request):
    check_box = driver.find_element(By.NAME, "rpGponVoipSip_diaOpt")
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ONT_VoIP_SIP_DCU(driver,value):
    input = driver.find_element(By.ID, "rpGponVoipSip_dirConUri")
    input.clear()
    input.send_keys(value)

def ONT_VoIP_SIP_BLAU(driver,value):
    input = driver.find_element(By.ID, "rpGponVoipSip_briLineAgentUri")
    input.clear()
    input.send_keys(value)

def ONT_VoIP_SIP_CFU(driver,value):
    input = driver.find_element(By.ID, "rpGponVoipSip_conFactUri")
    input.clear()
    input.send_keys(value)

def ONT_VoIP_SIP_Apply_Up(driver):
    driver.find_element(By.ID, "rpGponVoipSip_btnAdd").click()

def ONT_VoIP_SIP_Apply_Down(driver):
        driver.find_element(By.ID, "rpGponVoipSip_btnDel").click()

# ONT VoIP Profile -> VoIP Dial Plan Profile

def ONT_VoIP_Dial_Name(driver,name):
    input = driver.find_element(By.ID, "rpGponVoipDialPlan_addName")
    input.clear()
    input.send_keys(name)

def ONT_VoIP_Dial_MS(driver,vlaue):
    input = driver.find_element(By.ID, "rpGponVoipDialPlan_maxSize")
    input.clear()
    input.send_keys(vlaue)

def ONT_VoIP_Dial_CDT(driver,vlaue):
    input = driver.find_element(By.ID, "rpGponVoipDialPlan_criDialTimeout")
    input.clear()
    input.send_keys(vlaue)

def ONT_VoIP_Dial_PDT(driver,vlaue):
    input = driver.find_element(By.ID, "rpGponVoipDialPlan_parDialTimeout")
    input.clear()
    input.send_keys(vlaue)
    
def ONT_VoIP_Dial_format(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpGponVoipDialPlan_format']/option[{sel}]")
    select.click()

def ONT_VoIP_Dial_CT(driver,vlaue):
    input = driver.find_element(By.ID, "rpGponVoipDialPlan_token1")
    input.clear()
    input.send_keys(vlaue)

def ONT_VoIP_Dial_Apply_Up(driver):
    driver.find_element(By.ID, "rpGponVoipDialPlan_btnAdd").click()

def ONT_VoIP_Dial_Apply_Down(driver):
    driver.find_element(By.ID, "rpGponVoipDialPlan_btnDel").click()

# OLT Registration

# OLT Registration -> OLT Registration

# Load
def OLT_Reg_OLT_Reg_Load(driver):
    btn = driver.find_element(By.NAME, "rpGponPortReg_btnLoad")
    btn.click()

# Active(勾選框) *request = True or False，決定是否勾選
def OLT_Reg_OLT_Reg_Active(driver,pon,request):
    check_box = driver.find_elements(By.NAME, "rpGponPortReg_chkActive")[pon-1]
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

# Register-Method(下拉式選單) *sel為第幾個選項
def OLT_Reg_OLT_Reg_Register_Method(driver,pon,sel):
    select = driver.find_elements(By.XPATH, f"//*[@id='rpGponPortReg_sltReg']/option[{sel}]")[pon-1]
    select.click()

# KeepAlive(數字輸入框) *key為輸入值
def OLT_Reg_OLT_Reg_KeepAlive(driver,pon,key):
    input = driver.find_elements(By.XPATH, f"//*[@id='rpGponPortReg_keepalive']")[pon-1]
    input.clear()
    input.send_keys(key)

# Max distance for ONT(數字輸入框) *key為輸入值
def OLT_Reg_OLT_Reg_Max_distance(driver,pon,key):
    input = driver.find_elements(By.XPATH, f"//*[@id='rpGponPortReg_txtRang']")[pon-1]
    input.clear()
    input.send_keys(key)

# Transceiver(下拉式選單) *sel為第幾個選項
def OLT_Reg_OLT_Reg_Transceive(driver,pon,sel):
    select = driver.find_elements(By.XPATH, f"//*[@id='rpGponPortReg_sltTrans']/option[{sel+1}]")[pon-1]
    select.click()

# Template Active(勾選框) *request = True or False，決定是否勾選
def OLT_Reg_OLT_Reg_Template_Active(driver,pon,request):
    active = driver.find_elements(By.NAME, "rpGponPortReg_tempActive")[pon-1]
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()

# Template(下拉式選單) *sel為第幾個選項
def OLT_Reg_OLT_Reg_Template(driver,pon,sel):
    select = driver.find_elements(By.XPATH, f"//*[@id='rpGponPortReg_sltTemp']/option[{sel-124}]")[pon-1]
    select.click()

# Apply
def OLT_Reg_OLT_Reg_Apply(driver):
    btn = driver.find_element(By.XPATH, "//*[@id='rpGponPortReg_btnApply']")
    btn.click()
    
# Cancel
def OLT_Reg_OLT_Reg_Cancel(driver):
    btn = driver.find_element(By.ID, "rpGponPortReg_btnCancel")
    btn.click()

# OLT Registration -> Port Status

# Link Status
def OLT_Reg_Port_Sta_Link_Status(driver,pon):
    value = driver.find_elements(By.CLASS_NAME, "td-table-content.rpGponPortStatus_status")[pon-1].get_attribute("textContent")
    return value

# Ranging Max
def OLT_Reg_Port_Sta_Ranging_Max(driver,pon):
    value = driver.find_elements(By.CLASS_NAME, "td-table-content.rpGponPortStatus_rangMax")[pon-1].get_attribute("textContent")
    return value
    
# Key Exchange Interval
def OLT_Reg_Port_Sta_Key_Exchange_Interval(driver,pon):
    value = driver.find_elements(By.CLASS_NAME, "td-table-content.rpGponPortStatus_keyExcInt")[pon-1].get_attribute("textContent")
    return value
    
# Sn Acq Interval
def OLT_Reg_Port_Sta_Sn_Acq_Interval(driver,pon):
    value = driver.find_elements(By.CLASS_NAME, "td-table-content.rpGponPortStatus_snAcqInt")[pon-1].get_attribute("textContent")
    return value
    
# Rogue Det State
def OLT_Reg_Port_Sta_Rogue_Det_State(driver,pon):
    value = driver.find_elements(By.CLASS_NAME, "td-table-content.rpGponPortStatus_rogDetState")[pon-1].get_attribute("textContent")
    return value
    
# Los Status
def OLT_Reg_Port_Sta_Los_Status(driver,pon):
    value = driver.find_elements(By.CLASS_NAME, "td-table-content.rpGponPortStatus_losStatus")[pon-1].get_attribute("textContent")
    return value

# Transceiver Type
def OLT_Reg_Port_Sta_Transceive_Type(driver,pon):
    value = driver.find_elements(By.CLASS_NAME, "td-table-content.rpGponPortStatus_trans")[pon-1].get_attribute("textContent")
    return value

# Tx Power
def OLT_Reg_Port_Sta_Tx_Power(driver,pon):
    value = driver.find_elements(By.CLASS_NAME, "td-table-content.rpGponPortStatus_txPower")[pon-1].get_attribute("textContent")
    return value

# ONT Link Status
def OLT_Reg_Port_Sta_ONT_Link_Status(driver,pon):
    value = driver.find_elements(By.CLASS_NAME, "td-table-content.rpGponPortStatus_ontLinkStatus")[pon-1].get_attribute("textContent")
    return value

# OLT Registration -> TCA Configuration & TCA Status

# Pon Select
def OLT_Reg_TCA_Pon_Select(driver,pon):
    select = driver.find_elements(By.NAME, "rpGponPortTca_chkSel")[pon-1]
    select.click()

def OLT_Reg_TCA_Con_Load(driver):
    driver.find_element(By.NAME, "rpGponPortTca_btnLoad").click()

def OLT_Reg_TCA_Sta_Load(driver):
    driver.find_element(By.NAME, "rpGponPortTcaStatus_btnLoad").click()

# DS FEC mode Enable *request = True or False，決定是否勾選
def OLT_Reg_TCA_Enable(driver,request):
    enable = driver.find_element(By.NAME, "rpGponPortTca_chkActive")
    if(enable.is_selected() == True):
        if(request == False):
            enable.click()
    else:
        if(request == True):
            enable.click()

# Apply
def OLT_Reg_TCA_Apply(driver):
    apply = driver.find_element(By.ID, "rpGponPortTca_btnAdd")
    apply.click()

# Cancel
def OLT_Reg_TCA_Cancel(driver):
    cancel = driver.find_element(By.ID, "rpGponPortTca_btnCancel")
    cancel.click()

def OLT_Reg_TCA_input(driver,value,name):
    input = driver.find_element(By.NAME, name)
    input.clear()
    input.send_keys(value)
    
def OLT_Reg_TCA_value(driver,name):
    value = driver.find_element(By.NAME, name).get_attribute("value")
    return value

def OLT_Reg_TCA_configuration_value(driver,configuration_name,pon):
    value = driver.find_element(By.CSS_SELECTOR, f".listPortTca:nth-child({pon}) .{configuration_name}").get_attribute("textContent")
    return value

def OLT_Reg_TCA_Sta_status_value(driver,status_name,pon):
    value = driver.find_element(By.CSS_SELECTOR, f".listTcaStatus:nth-child({pon}) .{status_name}").get_attribute("textContent")
    return value

# TCA Reset為特定值
def OLT_Reg_TCA_reset(driver,slot,pon,value):
    
    name_array = ["rpGponPortTca_txtFecCorrByteTh","rpGponPortTca_txtFecCorrCodeWordTh","rpGponPortTca_txtFecUncorrCodeWordTh","rpGponPortTca_txtBipErrTh","rpGponPortTca_txtReiErrTh","rpGponPortTca_txtFecCodeWordTh","rpGponPortTca_txtBipByteTh","rpGponPortTca_txtRxPloamCrcErrTh","rpGponPortTca_txtRxPloamNonIdleTh","rpGponPortTca_txtPositiveDriftTh","rpGponPortTca_txtNegativeDriftTh","rpGponPortTca_txtRxOmciPktCrcErrTh","rpGponPortTca_txtUnreceivedBurstTh","rpGponPortTca_txtLCDGIErrTh","rpGponPortTca_txtRDIErrTh","rpGponPortTca_txtRxOmciPktTh"]
    configuration_name_array = ["rpGponPortTca_FecCorrByteTh","rpGponPortTca_FecCorrCodeWordTh","rpGponPortTca_FecUncorrCodeWordTh","rpGponPortTca_BipErrTh","rpGponPortTca_ReiErrTh","rpGponPortTca_FecCodeWordTh","rpGponPortTca_BipByteTh","rpGponPortTca_RxPloamCrcErrTh","rpGponPortTca_RxPloamNonIdleTh","rpGponPortTca_PositiveDriftTh","rpGponPortTca_NegativeDriftTh","rpGponPortTca_RxOmciPktCrcErrTh","rpGponPortTca_UnreceivedBurstTh","rpGponPortTca_LCDGIErrTh","rpGponPortTca_RDIErrTh","rpGponPortTca_RxOmciPktTh"]
    status_name_array = ["rpGponPortTcaStatus_FecCorrByteTh","rpGponPortTcaStatus_FecCorrCodeWordTh","rpGponPortTcaStatus_FecUncorrCodeWordTh","rpGponPortTcaStatus_BipErrTh","rpGponPortTcaStatus_ReiErrTh","rpGponPortTcaStatus_FecCodeWordTh","rpGponPortTcaStatus_BipByteTh","rpGponPortTcaStatus_RxPloamCrcErrTh","rpGponPortTcaStatus_RxPloamNonIdleTh","rpGponPortTcaStatus_PositiveDriftTh","rpGponPortTcaStatus_NegativeDriftTh","rpGponPortTcaStatus_RxOmciPktCrcErrTh","rpGponPortTcaStatus_UnreceivedBurstTh","rpGponPortTcaStatus_LCDGIErrTh","rpGponPortTcaStatus_RDIErrTh","rpGponPortTcaStatus_RxOmciPktTh"]

    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"GPON")
    mod.SubPage_Switch(driver,"OLT Registration")
    mod.Switch_Frame(driver)
    mod.Tab_Switch(driver,"TCA Configuration")
    time.sleep(0.3)
    Slot_Select(driver,slot)
    time.sleep(0.3)
    OLT_Reg_TCA_Pon_Select(driver,pon)
    for field in range(name_array.__len__()):
        name = name_array[field]
        OLT_Reg_TCA_input(driver,value,name)
    OLT_Reg_TCA_Apply(driver)

# 傳值測試一個slot中的一個pon *會建立TCA_test_report(slot)_(pon).txt檔回傳結果 *test_keys以陣列型式輸入
def OLT_Reg_TCA_Test(driver,test_keys,slot,pon):

    name_array = ["rpGponPortTca_txtFecCorrByteTh","rpGponPortTca_txtFecCorrCodeWordTh","rpGponPortTca_txtFecUncorrCodeWordTh","rpGponPortTca_txtBipErrTh","rpGponPortTca_txtReiErrTh","rpGponPortTca_txtFecCodeWordTh","rpGponPortTca_txtBipByteTh","rpGponPortTca_txtRxPloamCrcErrTh","rpGponPortTca_txtRxPloamNonIdleTh","rpGponPortTca_txtPositiveDriftTh","rpGponPortTca_txtNegativeDriftTh","rpGponPortTca_txtRxOmciPktCrcErrTh","rpGponPortTca_txtUnreceivedBurstTh","rpGponPortTca_txtLCDGIErrTh","rpGponPortTca_txtRDIErrTh","rpGponPortTca_txtRxOmciPktTh"]
    configuration_name_array = ["rpGponPortTca_FecCorrByteTh","rpGponPortTca_FecCorrCodeWordTh","rpGponPortTca_FecUncorrCodeWordTh","rpGponPortTca_BipErrTh","rpGponPortTca_ReiErrTh","rpGponPortTca_FecCodeWordTh","rpGponPortTca_BipByteTh","rpGponPortTca_RxPloamCrcErrTh","rpGponPortTca_RxPloamNonIdleTh","rpGponPortTca_PositiveDriftTh","rpGponPortTca_NegativeDriftTh","rpGponPortTca_RxOmciPktCrcErrTh","rpGponPortTca_UnreceivedBurstTh","rpGponPortTca_LCDGIErrTh","rpGponPortTca_RDIErrTh","rpGponPortTca_RxOmciPktTh"]
    status_name_array = ["rpGponPortTcaStatus_FecCorrByteTh","rpGponPortTcaStatus_FecCorrCodeWordTh","rpGponPortTcaStatus_FecUncorrCodeWordTh","rpGponPortTcaStatus_BipErrTh","rpGponPortTcaStatus_ReiErrTh","rpGponPortTcaStatus_FecCodeWordTh","rpGponPortTcaStatus_BipByteTh","rpGponPortTcaStatus_RxPloamCrcErrTh","rpGponPortTcaStatus_RxPloamNonIdleTh","rpGponPortTcaStatus_PositiveDriftTh","rpGponPortTcaStatus_NegativeDriftTh","rpGponPortTcaStatus_RxOmciPktCrcErrTh","rpGponPortTcaStatus_UnreceivedBurstTh","rpGponPortTcaStatus_LCDGIErrTh","rpGponPortTcaStatus_RDIErrTh","rpGponPortTcaStatus_RxOmciPktTh"]

    valid = True
    enable = True
    
    test_report = open(f"TCA_test_report{slot}_{pon}.txt","w+")

    enable_test = True
    counter = 0
    while enable_test:
        if(counter > 20):
            driver.refresh()
            counter = 0
        try:
            mod.Switch_Default(driver)
            mod.Page_Switch(driver,"GPON")
            mod.SubPage_Switch(driver,"OLT Registration")
            mod.Switch_Frame(driver)
            mod.Tab_Switch(driver,"TCA Configuration")
            time.sleep(0.3)
            Slot_Select(driver,slot)
            OLT_Reg_TCA_Pon_Select(driver,pon)
            OLT_Reg_TCA_Enable(driver,True)
            enable = True
            OLT_Reg_TCA_Apply(driver)
            if(OLT_Reg_TCA_configuration_value(driver,"rpGponPortTca_FecMode",pon) == "Disable"):
                print("Enable Error! slot = ",slot," pon = ",pon," enable_value = ",enable,file = open(f"TCA_test_report{slot}_{pon}.txt", 'a'))
            # else:
            #     print("pass-0o slot = ",slot," pon = ",pon," enable_value = ",enable,file = open(f"TCA_test_report{slot}_{pon}.txt", 'a'))
            mod.Tab_Switch(driver,"TCA Status")
            
            time.sleep(0.3)
            Slot_Select(driver,slot)
            if(OLT_Reg_TCA_Sta_status_value(driver,"rpGponPortTcaStatus_FecMode",pon) == "Disable"):
                print("Enable Error! slot = ",slot," pon = ",pon," enable_value = ",enable,file = open(f"TCA_test_report{slot}_{pon}.txt", 'a'))
            # else:
            #     print("pass-0o slot = ",slot," pon = ",pon," enable_value = ",enable,file = open(f"TCA_test_report{slot}_{pon}.txt", 'a'))
            
            mod.Tab_Switch(driver,"TCA Configuration")
            
            time.sleep(0.3)
            Slot_Select(driver,slot)
            OLT_Reg_TCA_Pon_Select(driver,pon)
            OLT_Reg_TCA_Enable(driver,False)
            enable = False
            OLT_Reg_TCA_Apply(driver)
            if(OLT_Reg_TCA_configuration_value(driver,"rpGponPortTca_FecMode",pon) == "Enable"):
                print("Enable Error! slot = ",slot," pon = ",pon," enable_value = ",enable,file = open(f"TCA_test_report{slot}_{pon}.txt", 'a'))
            # else:
            #     print("pass-0o slot = ",slot," pon = ",pon," enable_value = ",enable,file = open(f"TCA_test_report{slot}_{pon}.txt", 'a'))
            mod.Tab_Switch(driver,"TCA Status")
            
            time.sleep(0.3)
            Slot_Select(driver,slot)
            if(OLT_Reg_TCA_Sta_status_value(driver,"rpGponPortTcaStatus_FecMode",pon) == "Enable"):
                print("Enable Error! slot = ",slot," pon = ",pon," enable_value = ",enable,file = open(f"TCA_test_report{slot}_{pon}.txt", 'a'))
            # else:
            #     print("pass-0o slot = ",slot," pon = ",pon," enable_value = ",enable,file = open(f"TCA_test_report{slot}_{pon}.txt", 'a'))
            enable_test = False
        except:
            enable_test = True
            counter = counter+1
            # print(f"{slot}-{pon} Enable Test Fail")
    for field in range(name_array.__len__()):
        name = name_array[field]
        configuration_name = configuration_name_array[field]
        status_name = status_name_array[field]
        for key_num in range (test_keys.__len__()):
            enable_test = True
            counter = 0
            while enable_test:
                if(counter > 20):
                    driver.refresh()
                    counter = 0
                    mod.Switch_Default(driver)
                    mod.Page_Switch(driver,"GPON")
                    mod.SubPage_Switch(driver,"OLT Registration")
                    mod.Switch_Frame(driver)
                try: 
                    mod.Tab_Switch(driver,"TCA Configuration")
                    time.sleep(0.3)
                    Slot_Select(driver,slot)
                    OLT_Reg_TCA_Pon_Select(driver,pon)
                    prev_value = OLT_Reg_TCA_value(driver,name)
                    OLT_Reg_TCA_input(driver,test_keys[key_num],name)
                    OLT_Reg_TCA_Apply(driver)
                    # configuration check
                    if(mod.IsAlert(driver)):
                        OLT_Reg_TCA_Cancel(driver)
                        valid = False
                        if(str(test_keys[key_num]) == str(prev_value)):
                            print("Configure Error! Alert but write in invalid value. slot = ",slot," pon = ",pon," test_field = ",field+1," test_key_now = ",test_keys[key_num]," prev_value = ",prev_value," is_valid = ",valid,file = open(f"TCA_test_report{slot}_{pon}.txt", 'a'))
                        # else:
                        #     print("pass-1x slot = ",slot," pon = ",pon," test_field = ",field+1," test_key_now = ",test_keys[key_num]," prev_value = ",prev_value,file = open(f"TCA_test_report{slot}_{pon}.txt", 'a'))
                    else:
                        valid = True
                        if(int(OLT_Reg_TCA_configuration_value(driver,configuration_name,pon)) > 4294967295):
                            print("Configure Error! No Alert but value is too big. slot = ",slot," pon = ",pon," test_field = ",field+1," test_key_now = ",test_keys[key_num]," prev_value = ",prev_value," is_valid = ",valid,file = open(f"TCA_test_report{slot}_{pon}.txt", 'a'))
                        elif(int(OLT_Reg_TCA_configuration_value(driver,configuration_name,pon)) < 0):
                            print("Configure Error! No Alert but value is too small. slot = ",slot," pon = ",pon," test_field = ",field+1," test_key_now = ",test_keys[key_num]," prev_value = ",prev_value," is_valid = ",valid,file = open(f"TCA_test_report{slot}_{pon}.txt", 'a'))
                        # else:
                        #     print("pass-1o slot = ",slot," pon = ",pon," test_field = ",field+1," test_key_now = ",test_keys[key_num]," prev_value = ",prev_value,file = open(f"TCA_test_report{slot}_{pon}.txt", 'a'))
                    # value check
                    time.sleep(0.3)
                    Slot_Select(driver,slot)
                    OLT_Reg_TCA_Pon_Select(driver,pon)
                    now_value = OLT_Reg_TCA_value(driver,name)
                    if(valid):
                        if(str(test_keys[key_num]) != str(now_value)):
                            print("Input Value Error! No Alert but value didn't changed. slot = ",slot," pon = ",pon," test_field = ",field+1," test_key_now = ",test_keys[key_num]," now_value = ",now_value," prev_value = ",prev_value," is_valid = ",valid,file = open(f"TCA_test_report{slot}_{pon}.txt", 'a'))
                        # else:
                        #     print("pass-2o slot = ",slot," pon = ",pon," test_field = ",field+1," test_key_now = ",test_keys[key_num]," now_value = ",now_value,file = open(f"TCA_test_report{slot}_{pon}.txt", 'a'))
                    else:
                        if(now_value != prev_value):
                            print("Input Value Error! Alert but value changed. slot = ",slot," pon = ",pon," test_field = ",field+1," test_key_now = ",test_keys[key_num]," now_value = ",now_value," prev_value = ",prev_value," is_valid = ",valid,file = open(f"TCA_test_report{slot}_{pon}.txt", 'a'))
                        # else:
                        #     print("pass-2x slot = ",slot," pon = ",pon," test_field = ",field+1," test_key_now = ",test_keys[key_num]," now_value = ",now_value,file = open(f"TCA_test_report{slot}_{pon}.txt", 'a'))
                    # status check
                    mod.Tab_Switch(driver,"TCA Status")
                    time.sleep(0.3)
                    Slot_Select(driver,slot)
                    if(str(OLT_Reg_TCA_Sta_status_value(driver,status_name,pon)) != str(now_value)):
                            print("Status Error! Status valus != now_value. slot = ",slot," pon = ",pon," test_field = ",field+1," test_key_now = ",test_keys[key_num]," status_value = ",OLT_Reg_TCA_Sta_status_value(driver,status_name,pon)," now_value = ",now_value," prev_value = ",prev_value," is_valid = ",valid,file = open(f"TCA_test_report{slot}_{pon}.txt", 'a'))
                    # else:
                    #         print("pass-3o slot = ",slot," pon = ",pon," test_field = ",field+1," test_key_now = ",test_keys[key_num]," now_value = ",now_value,file = open(f"TCA_test_report{slot}_{pon}.txt", 'a'))
                    enable_test = False
                except:
                    counter = counter+1
                    enable_test = True
            if(counter > 20):
                print(f"{slot}-{pon} Test Fail")
                return
        # print(f"{slot}-{pon}-{field+1} Test Success")
    print(f"TCA {slot}-{pon} Test Finished",file = open(f"TCA_test_report{slot}_{pon}.txt", 'a'))
    test_report.close()

# 傳值測試一個slot中的一個pon中的一個欄位 *會建立TCA_test_report(slot)_(pon)_(field).txt檔回傳結果 *field：測試第幾個欄位，請輸入數字 *test_keys以陣列型式輸入
def OLT_Reg_TCA_Field_Test(driver,test_keys,slot,pon,field):
    
    name_array = ["rpGponPortTca_txtFecCorrByteTh","rpGponPortTca_txtFecCorrCodeWordTh","rpGponPortTca_txtFecUncorrCodeWordTh","rpGponPortTca_txtBipErrTh","rpGponPortTca_txtReiErrTh","rpGponPortTca_txtFecCodeWordTh","rpGponPortTca_txtBipByteTh","rpGponPortTca_txtRxPloamCrcErrTh","rpGponPortTca_txtRxPloamNonIdleTh","rpGponPortTca_txtPositiveDriftTh","rpGponPortTca_txtNegativeDriftTh","rpGponPortTca_txtRxOmciPktCrcErrTh","rpGponPortTca_txtUnreceivedBurstTh","rpGponPortTca_txtLCDGIErrTh","rpGponPortTca_txtRDIErrTh","rpGponPortTca_txtRxOmciPktTh"]
    configuration_name_array = ["rpGponPortTca_FecCorrByteTh","rpGponPortTca_FecCorrCodeWordTh","rpGponPortTca_FecUncorrCodeWordTh","rpGponPortTca_BipErrTh","rpGponPortTca_ReiErrTh","rpGponPortTca_FecCodeWordTh","rpGponPortTca_BipByteTh","rpGponPortTca_RxPloamCrcErrTh","rpGponPortTca_RxPloamNonIdleTh","rpGponPortTca_PositiveDriftTh","rpGponPortTca_NegativeDriftTh","rpGponPortTca_RxOmciPktCrcErrTh","rpGponPortTca_UnreceivedBurstTh","rpGponPortTca_LCDGIErrTh","rpGponPortTca_RDIErrTh","rpGponPortTca_RxOmciPktTh"]
    status_name_array = ["rpGponPortTcaStatus_FecCorrByteTh","rpGponPortTcaStatus_FecCorrCodeWordTh","rpGponPortTcaStatus_FecUncorrCodeWordTh","rpGponPortTcaStatus_BipErrTh","rpGponPortTcaStatus_ReiErrTh","rpGponPortTcaStatus_FecCodeWordTh","rpGponPortTcaStatus_BipByteTh","rpGponPortTcaStatus_RxPloamCrcErrTh","rpGponPortTcaStatus_RxPloamNonIdleTh","rpGponPortTcaStatus_PositiveDriftTh","rpGponPortTcaStatus_NegativeDriftTh","rpGponPortTcaStatus_RxOmciPktCrcErrTh","rpGponPortTcaStatus_UnreceivedBurstTh","rpGponPortTcaStatus_LCDGIErrTh","rpGponPortTcaStatus_RDIErrTh","rpGponPortTcaStatus_RxOmciPktTh"]

    valid = True
    test_report = open(f"TCA_test_report{slot}_{pon}_{field}.txt","w+")

    field = field-1
    name = name_array[field]
    configuration_name = configuration_name_array[field]
    status_name = status_name_array[field]
    for key_num in range (test_keys.__len__()):

        enable_test = True
        counter = 0
        while enable_test:
            if(counter > 20):
                driver.refresh()
                counter = 0
            try: 
                mod.Switch_Default(driver)
                mod.Page_Switch(driver,"GPON")
                mod.SubPage_Switch(driver,"OLT Registration")
                mod.Switch_Frame(driver)
                mod.Tab_Switch(driver,"TCA Configuration")
                time.sleep(0.3)
                Slot_Select(driver,slot)
                OLT_Reg_TCA_Pon_Select(driver,pon)
                prev_value = OLT_Reg_TCA_value(driver,name)
                OLT_Reg_TCA_input(driver,test_keys[key_num],name)
                OLT_Reg_TCA_Apply(driver)
                # configuration check
                if(mod.IsAlert(driver)):
                    OLT_Reg_TCA_Cancel(driver)
                    valid = False
                    if(str(test_keys[key_num]) == str(prev_value)):
                        print("Configure Error! Alert but write in invalid value. slot = ",slot," pon = ",pon," test_field = ",field+1," test_key_now = ",test_keys[key_num]," prev_value = ",prev_value," is_valid = ",valid,file = open(f"TCA_test_report{slot}_{pon}_{field+1}.txt", 'a'))
                    # else:
                    #     print("pass-1x slot = ",slot," pon = ",pon," test_field = ",field+1," test_key_now = ",test_keys[key_num]," prev_value = ",prev_value,file = open(f"TCA_test_report{slot}_{pon}_{field+1}.txt", 'a'))
                else:
                    valid = True
                    if(int(OLT_Reg_TCA_configuration_value(driver,configuration_name,pon)) > 4294967295):
                        print("Configure Error! No Alert but value is too big. slot = ",slot," pon = ",pon," test_field = ",field+1," test_key_now = ",test_keys[key_num]," prev_value = ",prev_value," is_valid = ",valid,file = open(f"TCA_test_report{slot}_{pon}_{field+1}.txt", 'a'))
                    elif(int(OLT_Reg_TCA_configuration_value(driver,configuration_name,pon)) < 0):
                        print("Configure Error! No Alert but value is too small. slot = ",slot," pon = ",pon," test_field = ",field+1," test_key_now = ",test_keys[key_num]," prev_value = ",prev_value," is_valid = ",valid,file = open(f"TCA_test_report{slot}_{pon}_{field+1}.txt", 'a'))
                    # else:
                    #     print("pass-1o slot = ",slot," pon = ",pon," test_field = ",field+1," test_key_now = ",test_keys[key_num]," prev_value = ",prev_value,file = open(f"TCA_test_report{slot}_{pon}_{field+1}.txt", 'a'))
                # value check
                time.sleep(0.3)
                Slot_Select(driver,slot)
                OLT_Reg_TCA_Pon_Select(driver,pon)
                now_value = OLT_Reg_TCA_value(driver,name)
                if(valid):
                    if(str(test_keys[key_num]) != str(now_value)):
                        print("Input Value Error! No Alert but value didn't changed. slot = ",slot," pon = ",pon," test_field = ",field+1," test_key_now = ",test_keys[key_num]," now_value = ",now_value," prev_value = ",prev_value," is_valid = ",valid,file = open(f"TCA_test_report{slot}_{pon}_{field+1}.txt", 'a'))
                    # else:
                    #     print("pass-2o slot = ",slot," pon = ",pon," test_field = ",field+1," test_key_now = ",test_keys[key_num]," now_value = ",now_value,file = open(f"TCA_test_report{slot}_{pon}_{field+1}.txt", 'a'))
                else:
                    if(now_value != prev_value):
                        print("Input Value Error! Alert but value changed. slot = ",slot," pon = ",pon," test_field = ",field+1," test_key_now = ",test_keys[key_num]," now_value = ",now_value," prev_value = ",prev_value," is_valid = ",valid,file = open(f"TCA_test_report{slot}_{pon}_{field+1}.txt", 'a'))
                    # else:
                    #     print("pass-2x slot = ",slot," pon = ",pon," test_field = ",field+1," test_key_now = ",test_keys[key_num]," now_value = ",now_value,file = open(f"TCA_test_report{slot}_{pon}_{field+1}.txt", 'a'))
                # status check
                mod.Tab_Switch(driver,"TCA Status")
                time.sleep(0.3)
                Slot_Select(driver,slot)
                if(str(OLT_Reg_TCA_Sta_status_value(driver,status_name,pon)) != str(now_value)):
                        print("Status Error! Status valus != now_value. slot = ",slot," pon = ",pon," test_field = ",field+1," test_key_now = ",test_keys[key_num]," status_value = ",OLT_Reg_TCA_Sta_status_value(driver,status_name,pon)," now_value = ",now_value," prev_value = ",prev_value," is_valid = ",valid,file = open(f"TCA_test_report{slot}_{pon}_{field+1}.txt", 'a'))
                # else:
                #         print("pass-3o slot = ",slot," pon = ",pon," test_field = ",field+1," test_key_now = ",test_keys[key_num]," now_value = ",now_value,file = open(f"TCA_test_report{slot}_{pon}_{field+1}.txt", 'a'))
                enable_test = False
            # print(f"{slot}-{pon}-{field+1} test success")
            except:
                counter = counter+1
                enable_test = True
                # print(f"{slot}-{pon}-{field+1} test fail")
        if(counter > 20):
            print(f"{slot}-{pon}-{field+1} Test Fail")
            return
    print(f"TCA {slot}-{pon}-{field+1} Test Finished",file = open(f"TCA_test_report{slot}_{pon}_{field+1}.txt", 'a'))
    test_report.close()

# 傳值測試多個slot&多個pon *會建立TCA_Multi_Test_report.txt檔回傳結果 *start_slot：開始測試的slot *end_slot：結束測試的slot *start_pon：開始測試的pon *end_pon：結束測試的pon *test_keys以陣列型式輸入
def OLT_Reg_TCA_Multi_Test(driver,start_slot,end_slot,start_pon,end_pon,test_keys,url,username,password):

    name_array = ["rpGponPortTca_txtFecCorrByteTh","rpGponPortTca_txtFecCorrCodeWordTh","rpGponPortTca_txtFecUncorrCodeWordTh","rpGponPortTca_txtBipErrTh","rpGponPortTca_txtReiErrTh","rpGponPortTca_txtFecCodeWordTh","rpGponPortTca_txtBipByteTh","rpGponPortTca_txtRxPloamCrcErrTh","rpGponPortTca_txtRxPloamNonIdleTh","rpGponPortTca_txtPositiveDriftTh","rpGponPortTca_txtNegativeDriftTh","rpGponPortTca_txtRxOmciPktCrcErrTh","rpGponPortTca_txtUnreceivedBurstTh","rpGponPortTca_txtLCDGIErrTh","rpGponPortTca_txtRDIErrTh","rpGponPortTca_txtRxOmciPktTh"]
    configuration_name_array = ["rpGponPortTca_FecCorrByteTh","rpGponPortTca_FecCorrCodeWordTh","rpGponPortTca_FecUncorrCodeWordTh","rpGponPortTca_BipErrTh","rpGponPortTca_ReiErrTh","rpGponPortTca_FecCodeWordTh","rpGponPortTca_BipByteTh","rpGponPortTca_RxPloamCrcErrTh","rpGponPortTca_RxPloamNonIdleTh","rpGponPortTca_PositiveDriftTh","rpGponPortTca_NegativeDriftTh","rpGponPortTca_RxOmciPktCrcErrTh","rpGponPortTca_UnreceivedBurstTh","rpGponPortTca_LCDGIErrTh","rpGponPortTca_RDIErrTh","rpGponPortTca_RxOmciPktTh"]
    status_name_array = ["rpGponPortTcaStatus_FecCorrByteTh","rpGponPortTcaStatus_FecCorrCodeWordTh","rpGponPortTcaStatus_FecUncorrCodeWordTh","rpGponPortTcaStatus_BipErrTh","rpGponPortTcaStatus_ReiErrTh","rpGponPortTcaStatus_FecCodeWordTh","rpGponPortTcaStatus_BipByteTh","rpGponPortTcaStatus_RxPloamCrcErrTh","rpGponPortTcaStatus_RxPloamNonIdleTh","rpGponPortTcaStatus_PositiveDriftTh","rpGponPortTcaStatus_NegativeDriftTh","rpGponPortTcaStatus_RxOmciPktCrcErrTh","rpGponPortTcaStatus_UnreceivedBurstTh","rpGponPortTcaStatus_LCDGIErrTh","rpGponPortTcaStatus_RDIErrTh","rpGponPortTcaStatus_RxOmciPktTh"]

    test_report = open("TCA_Multi_Test_report.txt","w+")
    print("Test Start",file = open("TCA_Multi_Test_report.txt", 'a'))
    
    # 設定
    valid = True
    ## enable = True
    TCA_Config_Failure = 0
    TCA_Status_Failure = 0

    slot = start_slot
    while slot <= end_slot:
        pon = start_pon
        while pon <= end_pon:

            # 測試Enable Check Box
            try_amount = 0
            is_failed = True
            while is_failed:
                if(try_amount > 20):
                    print("enable refresh")
                    time.sleep(10)
                    driver.refresh()
                    # driver.get(url)
                    try_amount = 0
                try:
                    mod.Switch_Default(driver)
                    mod.Page_Switch(driver,"GPON")
                    mod.SubPage_Switch(driver,"OLT Registration")
                    mod.Switch_Frame(driver)
                    mod.Tab_Switch(driver,"TCA Configuration")
                    time.sleep(0.3)
                    Slot_Select(driver,slot)
                    OLT_Reg_TCA_Pon_Select(driver,pon)
                    OLT_Reg_TCA_Enable(driver,True)
                    ## enable = True
                    OLT_Reg_TCA_Apply(driver)
                    if(OLT_Reg_TCA_configuration_value(driver,"rpGponPortTca_FecMode",pon) == "Disable"):
                        print(f" TCA Configure Fail, {slot}-{pon} Enable input is Enable,Configure is Disable.",file = open("TCA_Multi_Test_report.txt", 'a'))
                        TCA_Config_Failure = TCA_Config_Failure+1
                    # else:
                    #     print("pass-0o slot = ",slot," pon = ",pon," enable_value = ",enable,file = open(f"TCA_Multi_Test_report.txt", 'a'))
                    mod.Tab_Switch(driver,"TCA Status")
                    
                    time.sleep(0.3)
                    Slot_Select(driver,slot)
                    if(OLT_Reg_TCA_Sta_status_value(driver,"rpGponPortTcaStatus_FecMode",pon) == "Disable"):
                        print(f" TCA Status Fail, {slot}-{pon} Enable input is Enable,Status is Disable.",file = open("TCA_Multi_Test_report.txt", 'a'))
                        TCA_Status_Failure = TCA_Status_Failure+1
                    # else:
                    #     print("pass-0o slot = ",slot," pon = ",pon," enable_value = ",enable,file = open(f"TCA_Multi_Test_report.txt", 'a'))
                    
                    mod.Tab_Switch(driver,"TCA Configuration")
                    
                    time.sleep(0.3)
                    Slot_Select(driver,slot)
                    OLT_Reg_TCA_Pon_Select(driver,pon)
                    OLT_Reg_TCA_Enable(driver,False)
                    ## enable = False
                    OLT_Reg_TCA_Apply(driver)
                    if(OLT_Reg_TCA_configuration_value(driver,"rpGponPortTca_FecMode",pon) == "Enable"):
                        print(f" TCA Configure Fail, {slot}-{pon} Enable input is Disable,Configure is Enable.",file = open("TCA_Multi_Test_report.txt", 'a'))
                        TCA_Config_Failure = TCA_Config_Failure+1
                    # else:
                    #     print("pass-0o slot = ",slot," pon = ",pon," enable_value = ",enable,file = open(f"TCA_Multi_Test_report.txt", 'a'))
                    mod.Tab_Switch(driver,"TCA Status")
                    
                    time.sleep(0.3)
                    Slot_Select(driver,slot)
                    if(OLT_Reg_TCA_Sta_status_value(driver,"rpGponPortTcaStatus_FecMode",pon) == "Enable"):
                        print(f" TCA Status Fail, {slot}-{pon} Enable input is Disable,Status is Enable.",file = open("TCA_Multi_Test_report.txt", 'a'))
                        TCA_Status_Failure = TCA_Status_Failure+1
                    # else:
                    #     print("pass-0o slot = ",slot," pon = ",pon," enable_value = ",enable,file = open(f"TCA_Multi_Test_report.txt", 'a'))
                    is_failed = False
                except:
                    is_failed = True
                    try_amount = try_amount+1
                    # print(f"{slot}-{pon} Enable Test Fail")

            # 測試輸入框
            for field in range(name_array.__len__()):
                name = name_array[field]
                configuration_name = configuration_name_array[field]
                status_name = status_name_array[field]
                for key_num in range (test_keys.__len__()):
                    is_failed = True
                    try_amount = 0
                    while is_failed:
                        if(try_amount == 20):
                            print("refresh")
                            time.sleep(10)
                            driver.refresh()
                            # driver.get(url)
                            # try_amount = 0
                            mod.Switch_Default(driver)
                            mod.Page_Switch(driver,"GPON")
                            mod.SubPage_Switch(driver,"OLT Registration")
                            mod.Switch_Frame(driver)
                        if(try_amount == 25):
                            print("get url")
                            time.sleep(10)
                            mod.Login(driver,username,password)
                            driver.get(url)
                            mod.Switch_Default(driver)
                            mod.Page_Switch(driver,"GPON")
                            mod.SubPage_Switch(driver,"OLT Registration")
                            mod.Switch_Frame(driver)
                        if(try_amount == 40):
                            print("function die")
                            break
                        try:
                            mod.Tab_Switch(driver,"TCA Configuration")
                            time.sleep(0.3)
                            Slot_Select(driver,slot)
                            OLT_Reg_TCA_Pon_Select(driver,pon)
                            prev_value = OLT_Reg_TCA_value(driver,name)
                            OLT_Reg_TCA_input(driver,test_keys[key_num],name)
                            OLT_Reg_TCA_Apply(driver)
                            # configuration check
                            if(mod.IsAlert(driver)):
                                OLT_Reg_TCA_Cancel(driver)
                                valid = False
                                if(str(test_keys[key_num]) == str(prev_value)):
                                    print(f"TCA Configure Fail, {slot}-{pon} field{field+1} alert but import configure value {test_keys[key_num]}.",file = open("TCA_Multi_Test_report.txt", 'a'))
                                    TCA_Config_Failure = TCA_Config_Failure+1
                                # else:
                                #     print("pass-1x slot = ",slot," pon = ",pon," test_field = ",field+1," test_key_now = ",test_keys[key_num]," prev_value = ",prev_value,file = open("TCA_Multi_Test_report.txt", 'a'))
                            else:
                                valid = True
                                if(int(OLT_Reg_TCA_configuration_value(driver,configuration_name,pon)) > 4294967295):
                                    print(f" TCA Configure Fail, {slot}-{pon} field{field+1} no alert but import configure a too big value {OLT_Reg_TCA_configuration_value(driver,configuration_name,pon)}.",file = open("TCA_Multi_Test_report.txt", 'a'))
                                    TCA_Config_Failure = TCA_Config_Failure+1
                                elif(int(OLT_Reg_TCA_configuration_value(driver,configuration_name,pon)) < 0):
                                    print(f" TCA Configure Fail, {slot}-{pon} field{field+1} no alert but import configure a too small value {OLT_Reg_TCA_configuration_value(driver,configuration_name,pon)}.",file = open("TCA_Multi_Test_report.txt", 'a'))
                                    TCA_Config_Failure = TCA_Config_Failure+1
                                # else:
                                #     print("pass-1o slot = ",slot," pon = ",pon," test_field = ",field+1," test_key_now = ",test_keys[key_num]," prev_value = ",prev_value,file = open("TCA_Multi_Test_report.txt", 'a'))
                            # value check
                            time.sleep(0.3)
                            Slot_Select(driver,slot)
                            OLT_Reg_TCA_Pon_Select(driver,pon)
                            now_value = OLT_Reg_TCA_value(driver,name)
                            if(valid):
                                if(str(test_keys[key_num]) != str(now_value)):
                                    print(f" TCA Configure Fail, {slot}-{pon} field{field+1} no alert but didn't import field value {test_keys[key_num]}.",file = open("TCA_Multi_Test_report.txt", 'a'))
                                    TCA_Config_Failure = TCA_Config_Failure+1
                                # else:
                                #     print("pass-2o slot = ",slot," pon = ",pon," test_field = ",field+1," test_key_now = ",test_keys[key_num]," now_value = ",now_value,file = open("TCA_Multi_Test_report.txt", 'a'))
                            else:
                                if(now_value != prev_value):
                                    print(f" TCA Configure Fail, {slot}-{pon} field{field+1} alert but import field value {now_value}.",file = open("TCA_Multi_Test_report.txt", 'a'))
                                    TCA_Config_Failure = TCA_Config_Failure+1
                                # else:
                                #     print("pass-2x slot = ",slot," pon = ",pon," test_field = ",field+1," test_key_now = ",test_keys[key_num]," now_value = ",now_value,file = open("TCA_Multi_Test_report.txt", 'a'))
                            # status check
                            mod.Tab_Switch(driver,"TCA Status")
                            time.sleep(0.3)
                            Slot_Select(driver,slot)
                            if(str(OLT_Reg_TCA_Sta_status_value(driver,status_name,pon)) != str(now_value)):
                                print(f" TCA Status Fail, {slot}-{pon} field{field+1} didn't import value {now_value}.",file = open("TCA_Multi_Test_report.txt", 'a'))
                                TCA_Status_Failure = TCA_Status_Failure+1
                            # else:
                            #         print("pass-3o slot = ",slot," pon = ",pon," test_field = ",field+1," test_key_now = ",test_keys[key_num]," now_value = ",now_value,file = open("TCA_Multi_Test_report.txt", 'a'))
                            # print(f"{slot}-{pon}-{field+1} Sucess")
                            print("Latest progress：slot = ",slot," pon = ",pon," field = ",field+1,file = open("TCA_Multi_Test_Latest_Progress.txt", '+w'))
                            is_failed = False
                        except:
                            time.sleep(1)
                            is_failed = True
                            try_amount = try_amount+1
            time.sleep(0.5)
            pon = pon+1
        slot = slot+1
    if(TCA_Config_Failure == 0):
        print("[MSAN1-4194]OLT Registration - TCA Configuration Test Pass",file = open("TCA_Multi_Test_report.txt", 'a'))
    else:
        print("[MSAN1-4194]OLT Registration - TCA Configuration Test Fail ",TCA_Config_Failure,file = open("TCA_Multi_Test_report.txt", 'a'))
    if(TCA_Status_Failure == 0):
        print("[MSAN1-4197]OLT Registration - TCA Status Test Pass",file = open("TCA_Multi_Test_report.txt", 'a'))
    else:
        print("[MSAN1-4197]OLT Registration - TCA Status Test Fail ",TCA_Status_Failure,file = open("TCA_Multi_Test_report.txt", 'a'))
    
    print("Test Finished",file = open("TCA_Multi_Test_report.txt", 'a'))
    print("======================================================================================",file = open("TCA_Multi_Test_report.txt", 'a'))
    test_report.close()

# ONT Qos

    # ONT Qos -> Ingress Profile

def ONT_Qos_Ing_Pro_Name(driver,name):
    input = driver.find_element(By.ID, "rpGponIngprof_addName")
    input.clear()
    input.send_keys(name)
    
def ONT_Qos_Ing_Pro_0tc(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpGponIngprof_dot1p0']/option[{sel}]")
    select.click()
    
def ONT_Qos_Ing_Pro_1tc(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpGponIngprof_dot1p1']/option[{sel}]")
    select.click()
    
def ONT_Qos_Ing_Pro_2tc(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpGponIngprof_dot1p2']/option[{sel}]")
    select.click()
    
def ONT_Qos_Ing_Pro_3tc(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpGponIngprof_dot1p3']/option[{sel}]")
    select.click()
    
def ONT_Qos_Ing_Pro_4tc(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpGponIngprof_dot1p4']/option[{sel}]")
    select.click()
    
def ONT_Qos_Ing_Pro_5tc(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpGponIngprof_dot1p5']/option[{sel}]")
    select.click()
    
def ONT_Qos_Ing_Pro_6tc(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpGponIngprof_dot1p6']/option[{sel}]")
    select.click()
    
def ONT_Qos_Ing_Pro_7tc(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpGponIngprof_dot1p7']/option[{sel}]")
    select.click()
    
def ONT_Qos_Ing_Pro_Apply_Up(driver):
    btn = driver.find_element(By.ID, "rpGponIngprof_btnAdd")
    btn.click()
    
def ONT_Qos_Ing_Pro_Apply_Down(driver):
    btn = driver.find_element(By.ID, "rpGponIngprof_btnDel")
    btn.click()

    # ONT Qos -> Bandwidth Profile

def ONT_Qos_Ban_Pro_Name(driver,name):
    input = driver.find_element(By.ID, "rpGponBwprof_addName")
    input.clear()
    input.send_keys(name)

def ONT_Qos_Ban_Pro_SIR(driver,key):
    input = driver.find_element(By.ID, "rpGponBwprof_sir")
    input.clear()
    input.send_keys(key)

def ONT_Qos_Ban_Pro_AIR(driver,key):
    input = driver.find_element(By.ID, "rpGponBwprof_air")
    input.clear()
    input.send_keys(key)

def ONT_Qos_Ban_Pro_PIR(driver,key):
    input = driver.find_element(By.ID, "rpGponBwprof_pir")
    input.clear()
    input.send_keys(key)
    
def ONT_Qos_Ban_Pro_Apply_Up(driver):
    btn = driver.find_element(By.ID, "rpGponBwprof_btnAdd")
    btn.click()
    
def ONT_Qos_Ban_Pro_Apply_Down(driver):
    btn = driver.find_element(By.ID, "rpGponBwprof_btnDel")
    btn.click()

    # ONT Qos -> Pbit Profile

def ONT_Qos_Pbit_Pro_Name(driver,name):
    input = driver.find_element(By.ID, "rpGponPbitprof_addName")
    input.clear()
    input.send_keys(name)
    
def ONT_Qos_Pbit_Pro_P0tc(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpGponPbitprof_p0']/option[{sel}]")
    select.click()
    
def ONT_Qos_Pbit_Pro_P1tc(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpGponPbitprof_p1']/option[{sel}]")
    select.click()
    
def ONT_Qos_Pbit_Pro_P2tc(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpGponPbitprof_p2']/option[{sel}]")
    select.click()
    
def ONT_Qos_Pbit_Pro_P3tc(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpGponPbitprof_p3']/option[{sel}]")
    select.click()
    
def ONT_Qos_Pbit_Pro_P4tc(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpGponPbitprof_p4']/option[{sel}]")
    select.click()
    
def ONT_Qos_Pbit_Pro_P5tc(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpGponPbitprof_p5']/option[{sel}]")
    select.click()
    
def ONT_Qos_Pbit_Pro_P6tc(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpGponPbitprof_p6']/option[{sel}]")
    select.click()
    
def ONT_Qos_Pbit_Pro_P7tc(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpGponPbitprof_p7']/option[{sel}]")
    select.click()
    
def ONT_Qos_Pbit_Pro_Apply_Up(driver):
    btn = driver.find_element(By.ID, "rpGponPbitprof_btnAdd")
    btn.click()
    
def ONT_Qos_Pbit_Pro_Apply_Down(driver):
    btn = driver.find_element(By.ID, "rpGponPbitprof_btnDel")
    btn.click()

    # ONT Qos -> CAC Profile

def ONT_Qos_CAC_Pro_Name(driver,name):
    input = driver.find_element(By.ID, "rpGponCacprof_addName")
    input.clear()
    input.send_keys(name)

def ONT_Qos_CAC_Pro_Bandwidth(driver,key):
    input = driver.find_element(By.ID, "rpGponCacprof_addMcastBw")
    input.clear()
    input.send_keys(key)
    
def ONT_Qos_CAC_Pro_Apply_Up(driver):
    btn = driver.find_element(By.ID, "rpGponCacprof_btnAdd")
    btn.click()
    
def ONT_Qos_CAC_Pro_Apply_Down(driver):
    btn = driver.find_element(By.ID, "rpGponCacprof_btnDel")
    btn.click()

    # ONT Qos -> WRED/DS-Meter

def ONT_Qos_WRED_WRED_Disable(driver):
    btn = driver.find_elements(By.NAME, "rpGponQosDsMeter_wred")[0]
    btn.click()

def ONT_Qos_WRED_WRED_Enable(driver):
    btn = driver.find_elements(By.NAME, "rpGponQosDsMeter_wred")[1]
    btn.click()

def ONT_Qos_WRED_DS_PIR(driver):
    btn = driver.find_elements(By.NAME, "rpGponQosDsMeter_dsmeter")[0]
    btn.click()

def ONT_Qos_WRED_DS_CIR(driver):
    btn = driver.find_elements(By.NAME, "rpGponQosDsMeter_dsmeter")[1]
    btn.click()
    
def ONT_Qos_WRED_Apply(driver):
    btn = driver.find_element(By.NAME, "rpGponDsMeter_btnApply")
    btn.click()

# ONT Config

    # ONT Config -> ONT Wan

def ONT_Con_ONT_Wan_Slot_Pon_Select(driver,slot,pon):
    Select(driver.find_element(By.ID, "gponSelOltPort")).select_by_visible_text(f"{slot}-{pon}")

def ONT_Con_ONT_Wan_Tem_Select(driver,tem):
    Select(driver.find_element(By.ID, "rpGponOntWanConfig_ont")).select_by_visible_text(f"{tem}")

def ONT_Con_ONT_Wan_Load(driver):
    driver.find_element(By.NAME, "rpGponOntWanConfig_btnLoad").click()

def ONT_Con_ONT_Wan_ID_Select(driver,text):
    Select(driver.find_element(By.ID, "rpOntWan_SltWanId")).select_by_visible_text(f"{text}")

def ONT_Con_ONT_Wan_Active_enable(driver):
    driver.find_element(By.ID, "rpGponOntWanConfig_RdoActiveEnable").click()

def ONT_Con_ONT_Wan_Active_disable(driver):
    driver.find_element(By.ID, "rpGponOntWanConfig_RdoActiveDisable").click()

def ONT_Con_ONT_Wan_Default_disable(driver):
    driver.find_element(By.ID, "rpGponOntWanConfig_RdoDefaultDisable").click()
    
def ONT_Con_ONT_Wan_Connection_Type_bridge(driver):
    driver.find_element(By.ID, "rpGponOntWanConfig_RdoTypeBridge").click()

def ONT_Con_ONT_Wan_Connection_Type_ipoe(driver):
    driver.find_element(By.ID, "rpGponOntWanConfig_RdoTypeIpoe").click()
    
def ONT_Con_ONT_Wan_Connection_Type_PPPoE(driver):
    driver.find_element(By.ID, "rpGponOntWanConfig_RdoTypePppoe").click()

def ONT_Con_ONT_Wan_Connection_Type_PPPoE_UN(driver,username):
    input = driver.find_element(By.ID, "rpGponOntWanConfig_TxtPppoeUsername")
    input.clear()
    input.send_keys(username)
    
def ONT_Con_ONT_Wan_Connection_Type_PPPoE_PW(driver,password):
    input = driver.find_element(By.ID, "rpGponOntWanConfig_TxtPppoePassword")
    input.clear()
    input.send_keys(password)

def ONT_Con_ONT_Wan_Service_voip(driver,request):
    active = driver.find_element(By.ID, "rpGponOntWanConfig_ChkServiceVoip")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()

def ONT_Con_ONT_Wan_Service_iptv(driver,request):
    active = driver.find_element(By.ID, "rpGponOntWanConfig_ChkServiceIptv")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()

def ONT_Con_ONT_Wan_Service_tr069(driver,request):
    active = driver.find_element(By.ID, "rpGponOntWanConfig_ChkServiceMgmt")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()
    
def ONT_Con_ONT_Wan_VLAN_vid(driver,key):
    input = driver.find_element(By.ID, "rpGponOntWanConfig_TxtVlanId")
    input.clear()
    input.send_keys(key)
    
def ONT_Con_ONT_Wan_VLAN_priority(driver,sel):
    driver.find_element(By.XPATH, f"//*[@id='rpGponOntWanConfig_SltVlanPrioirity']/option[{sel}]").click()
    
def ONT_Con_ONT_Wan_VLAN_mvlan(driver,key):
    input = driver.find_element(By.ID, "rpGponOntWanConfig_TxtMvlan")
    input.clear()
    input.send_keys(key)
    
def ONT_Con_ONT_Wan_IPv4_dynamic(driver):
    driver.find_element(By.ID, "rpGponOntWanConfig_RdoDhcpEnable").click()
    
def ONT_Con_ONT_Wan_IPv4_static(driver):
    driver.find_element(By.ID, "rpGponOntWanConfig_RdoDhcpDisable").click()

def ONT_Con_ONT_Wan_IPv4_address(driver,key):
    input = driver.find_element(By.ID, "rpGponOntWanConfig_TxtIpAddress")
    input.clear()
    input.send_keys(key)

def ONT_Con_ONT_Wan_IPv4_mask(driver,key):
    input = driver.find_element(By.ID, "rpGponOntWanConfig_TxtIpMask")
    input.clear()
    input.send_keys(key)

def ONT_Con_ONT_Wan_IPv4_gateway(driver,key):
    input = driver.find_element(By.ID, "rpGponOntWanConfig_TxtIpGateway")
    input.clear()
    input.send_keys(key)

def ONT_Con_ONT_Wan_DNS_primary(driver,key):
    input = driver.find_element(By.ID, "rpGponOntWanConfig_TxtPrimaryDns")
    input.clear()
    input.send_keys(key)

def ONT_Con_ONT_Wan_DNS_secondary(driver,key):
    input = driver.find_element(By.ID, "rpGponOntWanConfig_TxtSecondaryDns")
    input.clear()
    input.send_keys(key)

def ONT_Con_ONT_Wan_IP_NAT_enable(driver):
    driver.find_element(By.ID, "rpGponOntWanConfig_RdoNATEnable").click()
    
def ONT_Con_ONT_Wan_IP_NAT_disable(driver):
    driver.find_element(By.ID, "rpGponOntWanConfig_RdoNATDisable").click()

def ONT_Con_ONT_Wan_LAN_port1(driver,request):
    active = driver.find_element(By.ID, "rpGponOntWanConfig_ChkLanportBinding1")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()

def ONT_Con_ONT_Wan_LAN_port2(driver,request):
    active = driver.find_element(By.ID, "rpGponOntWanConfig_ChkLanportBinding2")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()

def ONT_Con_ONT_Wan_LAN_port3(driver,request):
    active = driver.find_element(By.ID, "rpGponOntWanConfig_ChkLanportBinding3")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()

def ONT_Con_ONT_Wan_LAN_port4(driver,request):
    active = driver.find_element(By.ID, "rpGponOntWanConfig_ChkLanportBinding4")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()

def ONT_Con_ONT_Wan_2_4G_SSID1(driver,request):
    active = driver.find_element(By.ID, "rpGponOntWanConfig_ChkWifiSSIDBinding1")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()

def ONT_Con_ONT_Wan_2_4G_SSID2(driver,request):
    active = driver.find_element(By.ID, "rpGponOntWanConfig_ChkWifiSSIDBinding2")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()

def ONT_Con_ONT_Wan_2_4G_SSID3(driver,request):
    active = driver.find_element(By.ID, "rpGponOntWanConfig_ChkWifiSSIDBinding3")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()

def ONT_Con_ONT_Wan_2_4G_SSID4(driver,request):
    active = driver.find_element(By.ID, "rpGponOntWanConfig_ChkWifiSSIDBinding4")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()

def ONT_Con_ONT_Wan_5G_SSID1(driver,request):
    active = driver.find_element(By.ID, "rpGponOntWanConfig_ChkWifi5gSSIDBinding1")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()

def ONT_Con_ONT_Wan_5G_SSID2(driver,request):
    active = driver.find_element(By.ID, "rpGponOntWanConfig_ChkWifi5gSSIDBinding2")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()

def ONT_Con_ONT_Wan_5G_SSID3(driver,request):
    active = driver.find_element(By.ID, "rpGponOntWanConfig_ChkWifi5gSSIDBinding3")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()

def ONT_Con_ONT_Wan_5G_SSID4(driver,request):
    active = driver.find_element(By.ID, "rpGponOntWanConfig_ChkWifi5gSSIDBinding4")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()

def ONT_Con_ONT_Wan_Apply(driver):
    driver.find_element(By.NAME, "rpGponOntWanConfig_BtnApply").click()

def ONT_Con_ONT_Wan_Delete(driver):
    driver.find_element(By.NAME, "rpGponOntWanConfig_BtnDelete").click()

def ONT_Con_ONT_Wan_Web_Check(driver,ont_aid,slot,port,aid_num,newpage_username,newpage_password):
    print(f"{ont_aid} ONT WAN Web Check\nTest Start",file = open("ONT_Status_Test_report.txt", '+a'))

    # 導向路徑ONT Quick Setup
    driver.switch_to.window(driver.window_handles[0])
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"GPON")
    mod.SubPage_Switch(driver,"ONT Quick Setup")
    mod.Switch_Frame(driver)
    retry = True
    while retry:
        try:
            Slot_Select(driver,slot)
            retry = False
        except:
            retry = True
        time.sleep(0.5)
        if(mod.IsAlert(driver)):
            break
        time.sleep(0.5)
    retry = True
    counter = 0
    while retry and counter <= 20:
        try:
            ONT_Qui_Port_Select(driver,port)
            time.sleep(0.5)
            ONT_Qui_ONT_Qui_Load(driver)
            time.sleep(0.5)
            retry = False
        except:
            counter = counter+1
            retry = True
    driver.find_elements(By.ID, "rpGponOntSetup_ontAid")[aid_num].click()

    # 登入新分頁
    try:
        driver.switch_to.window(driver.window_handles[1])
        mod.Find_by_id_wait(driver,"card_sysinfo_modelname",10)
    except:
        try:
            driver.switch_to.window(driver.window_handles[1])
            username2_ = driver.find_element(By.ID, "username")
            username2_.send_keys(newpage_username)
            password2_ = driver.find_element(By.ID, "userpassword")
            password2_.send_keys(newpage_password)
            driver.find_element(By.ID, "loginBtn").click()
            time.sleep(2)
        except:
            print("ONT Wed Open Fail",file = open("ONT_Status_Test_report.txt", '+a'))
            print("Test Finishd",file = open("ONT_Status_Test_report.txt", '+a'))
            print("======================================================================================",file = open("ONT_Status_Test_report.txt", '+a'))
            return 0

# ONT Wan
# GPON > ONT Config > ONT Wan
# -------------------------start-------------------------

    # ONT Web路徑導向Network Setting > Broadband
    driver.find_element(By.ID, "h_menu_list").click()
    time.sleep(0.5)
    driver.find_element(By.LINK_TEXT, "Network Setting").click()
    time.sleep(0.5)
    driver.find_element(By.XPATH, "//div[@id='Broadband']/span").click()
    time.sleep(1)

    # ONT Web 確認 Default
    if_find = False
    counter = 0
    while if_find == False and counter < 120:
        try:
            driver.find_element(By.ID, "Network_Broadband_Broad_Table")
            if_find = True
        except:
            counter = counter+1
            time.sleep(1)
    if(driver.find_element(By.XPATH, "//*[@id='Network_Broadband_Broad_Table']/tbody/tr[1]/td[10]").get_attribute("textContent") != "Y"):
        print(f"-WAN 1 Default- Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
    if(driver.find_element(By.XPATH, "//*[@id='Network_Broadband_Broad_Table']/tbody/tr[2]/td[10]").get_attribute("textContent") != "N"):
        print(f"-WAN 2 Default- Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
    if(driver.find_element(By.XPATH, "//*[@id='Network_Broadband_Broad_Table']/tbody/tr[3]/td[10]").get_attribute("textContent") != "N"):
        print(f"-WAN 3 Default- Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
    if(driver.find_element(By.XPATH, "//*[@id='Network_Broadband_Broad_Table']/tbody/tr[4]/td[10]").get_attribute("textContent") != "N"):
        print(f"-WAN 4 Default- Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
    if(driver.find_element(By.XPATH, "//*[@id='Network_Broadband_Broad_Table']/tbody/tr[5]/td[10]").get_attribute("textContent") != "N"):
        print(f"-WAN 5 Default- Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
    if(driver.find_element(By.XPATH, "//*[@id='Network_Broadband_Broad_Table']/tbody/tr[6]/td[10]").get_attribute("textContent") != "N"):
        print(f"-WAN 6 Default- Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
    if(driver.find_element(By.XPATH, "//*[@id='Network_Broadband_Broad_Table']/tbody/tr[7]/td[10]").get_attribute("textContent") != "N"):
        print(f"-WAN 7 Default- Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
    if(driver.find_element(By.XPATH, "//*[@id='Network_Broadband_Broad_Table']/tbody/tr[8]/td[10]").get_attribute("textContent") != "N"):
        print(f"-WAN 8 Default- Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
    
    # 原頁面路徑導向ONT WAN 17-16-2
    driver.switch_to.window(driver.window_handles[0])
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"ONT Config")
    mod.Switch_Frame(driver)
    mod.Tab_Switch(driver,"ONT WAN")
    retry = True
    while retry:
        try:
            ONT_Con_ONT_Wan_Slot_Pon_Select(driver,slot,port)
            retry = False
        except:
            retry = True
        time.sleep(0.5)
        if(mod.IsAlert(driver)):
            break
        time.sleep(0.5)
    retry = True
    counter = 0
    while retry and counter <= 20:
        try:
            ONT_Con_ONT_Wan_Tem_Select(driver,aid_num+1)
            time.sleep(0.5)
            ONT_Con_ONT_Wan_Load(driver)
            time.sleep(0.5)
            retry = False
        except:
            counter = counter+1
            retry = True

    # 避免某個奇怪的bug,把1以外的紀錄都刪掉
    if_delete = False
    for index in range(driver.find_elements(By.CLASS_NAME, "listWanConfig").__len__()):
        if(driver.find_elements(By.NAME, "rpGponOntWanConfig_WanId")[index].get_attribute("textContent") != "1"):
            if_delete = True
            driver.find_elements(By.NAME, "rpGponOntWanConfig_chkDel")[index].click()
    if(if_delete):
        ONT_Con_ONT_Wan_Delete(driver)

    # 設定測試id
    ONT_Web_VOIP_WAN_ID = ["WAN_Select_1_label","WAN_Select_2_label","WAN_Select_3_label","WAN_Select_4_label","WAN_Select_5_label","WAN_Select_6_label"]

    for for_wan_id in range(6):
        wan_id = for_wan_id + 2
        
        # ONT WAN 傳入值測試 第一次
        driver.switch_to.window(driver.window_handles[0])
        mod.Switch_Frame(driver)
        time.sleep(1)
        ONT_Con_ONT_Wan_ID_Select(driver,wan_id)
        time.sleep(0.1)
        ONT_Con_ONT_Wan_Active_enable(driver)
        ONT_Con_ONT_Wan_Connection_Type_bridge(driver)
        ONT_Con_ONT_Wan_IP_NAT_disable(driver)
        ONT_Con_ONT_Wan_LAN_port1(driver,False)
        ONT_Con_ONT_Wan_LAN_port2(driver,False)
        ONT_Con_ONT_Wan_LAN_port3(driver,False)
        ONT_Con_ONT_Wan_LAN_port4(driver,False)
        time.sleep(1)
        time.sleep(7)
        ONT_Con_ONT_Wan_Apply(driver)
        time.sleep(7)

        # ONT Wan 切至Web確認 第一次
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(10)
        driver.refresh()
        if_find = False
        refresh_counter = 0
        while if_find == False and refresh_counter < 120:
            try:
                driver.find_element(By.CLASS_NAME, "icon-broadband-edit")
                if_find = True
            except:
                refresh_counter = refresh_counter+1
                time.sleep(1)
        if(if_find == False and refresh_counter == 120):
            time.sleep(2)
            driver.refresh()
            time.sleep(2)
            try:  
                driver.refresh()
                time.sleep(2)
                driver.find_element(By.CLASS_NAME, "icon-broadband-edit")
            except:
                username2_ = driver.find_element(By.ID, "username")
                username2_.send_keys(newpage_username)
                password2_ = driver.find_element(By.ID, "userpassword")
                password2_.send_keys(newpage_password)
                mod.Find_by_id_wait_click(driver,"h_menu_list",50)
                mod.Find_by_link_text_wait_click(driver,"Network Setting",50)
                mod.Find_by_xpath_wait_click(driver,"//div[@id='Broadband']/span",50)
        time.sleep(2)
        driver.find_elements(By.CLASS_NAME, "icon-broadband-edit")[wan_id-1].click()
        time.sleep(10)
        finish_loading = False
        counter = 0
        mod.Find_by_id_wait(driver,"wan_enable",30)
        while finish_loading == False and counter < 120:
            if(driver.find_element(By.ID, "wan_enable").get_attribute("class") != "switch active "):
                time.sleep(1)
                counter = counter+1
                # print(f"-WAN {wan_id} Connection Type- Bridge Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                # print(f"-WAN {wan_id} Active- Enable Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
            else:
                time.sleep(10)
                finish_loading = True
                if(driver.find_element(By.XPATH, "//*[@id='bb_modeSelect']/option[2]").is_selected() != True):
                    print(f"-WAN {wan_id} Connection Type- Bridge Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        if(finish_loading == False and counter == 120):
            print(f"-WAN {wan_id}- 1st Apply Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        time.sleep(7)

        # ONT WAN 傳入值測試 第二次
        driver.switch_to.window(driver.window_handles[0])
        mod.Switch_Frame(driver)
        time.sleep(1)
        ONT_Con_ONT_Wan_ID_Select(driver,wan_id)
        time.sleep(0.1)
        ONT_Con_ONT_Wan_Active_disable(driver)
        ONT_Con_ONT_Wan_Connection_Type_ipoe(driver)
        ONT_Con_ONT_Wan_Service_iptv(driver,True)
        ONT_Con_ONT_Wan_VLAN_vid(driver,"4094")
        ONT_Con_ONT_Wan_VLAN_priority(driver,8)
        ONT_Con_ONT_Wan_VLAN_mvlan(driver,"4094")
        ONT_Con_ONT_Wan_IPv4_static(driver)
        ONT_Con_ONT_Wan_IPv4_address(driver,"100.100.100.254")
        ONT_Con_ONT_Wan_IPv4_mask(driver,"255.255.255.0")
        ONT_Con_ONT_Wan_IPv4_gateway(driver,"3.3.3.254")
        ONT_Con_ONT_Wan_DNS_primary(driver,"4.4.4.254")
        ONT_Con_ONT_Wan_DNS_secondary(driver,"5.5.5.254")
        ONT_Con_ONT_Wan_IP_NAT_enable(driver)
        ONT_Con_ONT_Wan_2_4G_SSID1(driver,True)
        ONT_Con_ONT_Wan_2_4G_SSID2(driver,True)
        ONT_Con_ONT_Wan_2_4G_SSID3(driver,True)
        ONT_Con_ONT_Wan_2_4G_SSID4(driver,True)
        ONT_Con_ONT_Wan_5G_SSID1(driver,True)
        ONT_Con_ONT_Wan_5G_SSID2(driver,True)
        ONT_Con_ONT_Wan_5G_SSID3(driver,True)
        ONT_Con_ONT_Wan_5G_SSID4(driver,True)
        time.sleep(1)
        time.sleep(7)
        ONT_Con_ONT_Wan_Apply(driver)
        time.sleep(7)

        # ONT Wan 切至Web確認 第二次
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(10)
        driver.refresh()
        if_find = False
        refresh_counter = 0
        while if_find == False and refresh_counter < 120:
            try:
                driver.find_element(By.CLASS_NAME, "icon-broadband-edit")
                if_find = True
            except:
                refresh_counter = refresh_counter+1
                time.sleep(1)
        if(if_find == False and refresh_counter == 120):
            time.sleep(2)
            driver.refresh()
            time.sleep(2)
            try:  
                driver.refresh()
                time.sleep(2)
                driver.find_element(By.ID, "Network_Broadband")
            except:
                username2_ = driver.find_element(By.ID, "username")
                username2_.send_keys(newpage_username)
                password2_ = driver.find_element(By.ID, "userpassword")
                password2_.send_keys(newpage_password)
                driver.find_element(By.ID, "h_menu_list").click()
                time.sleep(3)
                driver.find_element(By.LINK_TEXT, "Network Setting").click()
                time.sleep(3)
                driver.find_element(By.XPATH, "//div[@id='Broadband']/span").click()
                time.sleep(2)
        time.sleep(2)
        driver.find_elements(By.CLASS_NAME, "icon-broadband-edit")[wan_id-1].click()
        time.sleep(10)

        finish_loading = False
        counter = 0
        mod.Find_by_id_wait(driver,"wan_enable",30)
        while finish_loading == False and counter < 120:
            if(driver.find_element(By.ID, "bb_enblVlan").get_attribute("class") != "switch active "):
                # print(f"-WAN {wan_id} VLAN- Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                time.sleep(1)
                counter = counter+1
            else:
                time.sleep(10)
                finish_loading = True
                if(driver.find_element(By.ID, "wan_enable").get_attribute("class") != "switch  "):
                    print(f"-WAN {wan_id} Active- Disable Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                if(driver.find_element(By.XPATH, "//*[@id='bb_modeSelect']/option[1]").is_selected() != True):
                    print(f"-WAN {wan_id} Connection Type- ipoe Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                elif(driver.find_element(By.XPATH, "//*[@id='bb_srvLinkTypeSelect']/option[1]").is_selected() != True):
                    print(f"-WAN {wan_id} Connection Type- ipoe Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                if(driver.find_element(By.ID, "bb_igmpEnable").get_attribute("class") != "switch active "):
                    print(f"-WAN {wan_id} IPTV- Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                # if(driver.find_element(By.ID, "bb_enblVlan").get_attribute("class") != "switch active "):
                #     print(f"-WAN {wan_id} VLAN- Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                if(driver.find_element(By.XPATH, "//*[@id='bb_vlanPrio']/option[8]").is_selected() != True):
                    print(f"-WAN {wan_id} VLAN- priority Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                if(driver.find_element(By.ID, "bb_vlanId").get_attribute("value") != "4094"):
                    print(f"-WAN {wan_id} VLAN- Vid Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                if(driver.find_element(By.ID, "bb_enblMvlan").get_attribute("class") != "switch active "):
                    print(f"-WAN {wan_id} MVLAN- Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                elif(driver.find_element(By.ID, "bb_mVlanId").get_attribute("value") != "4094"):
                    print(f"-WAN {wan_id} MVLAN- Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                try:
                    if(driver.find_element(By.ID, "a_bb_ipAddrValue_1").get_attribute("value") != "100" or driver.find_element(By.ID, "a_bb_ipAddrValue_2").get_attribute("value") != "100" or driver.find_element(By.ID, "a_bb_ipAddrValue_3").get_attribute("value") != "100" or driver.find_element(By.ID, "a_bb_ipAddrValue_4").get_attribute("value") != "254"):
                        print(f"-WAN {wan_id} IPv4- Address Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                    if(driver.find_element(By.ID, "a_bb_ipMask_1").get_attribute("value") != "255" or driver.find_element(By.ID, "a_bb_ipMask_2").get_attribute("value") != "255" or driver.find_element(By.ID, "a_bb_ipMask_3").get_attribute("value") != "255" or driver.find_element(By.ID, "a_bb_ipMask_4").get_attribute("value") != "0"):
                        print(f"-WAN {wan_id} IPv4- Mask Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                    if(driver.find_element(By.ID, "a_bb_gwValue_1").get_attribute("value") != "3" or driver.find_element(By.ID, "a_bb_gwValue_2").get_attribute("value") != "3" or driver.find_element(By.ID, "a_bb_gwValue_3").get_attribute("value") != "3" or driver.find_element(By.ID, "a_bb_gwValue_4").get_attribute("value") != "254"):
                        print(f"-WAN {wan_id} IPv4- Gateway Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                except:
                    print(f"-WAN {wan_id} IPv4- Static Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                try:
                    if(driver.find_element(By.ID, "a_ipDns1_1").get_attribute("value") != "4" or driver.find_element(By.ID, "a_ipDns1_2").get_attribute("value") != "4" or driver.find_element(By.ID, "a_ipDns1_3").get_attribute("value") != "4" or driver.find_element(By.ID, "a_ipDns1_4").get_attribute("value") != "254"):
                        print(f"-WAN {wan_id} DNS- Primary Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                    if(driver.find_element(By.ID, "a_ipDns2_1").get_attribute("value") != "5" or driver.find_element(By.ID, "a_ipDns2_2").get_attribute("value") != "5" or driver.find_element(By.ID, "a_ipDns2_3").get_attribute("value") != "5" or driver.find_element(By.ID, "a_ipDns2_4").get_attribute("value") != "254"):
                        print(f"-WAN {wan_id} DNS- Secondary Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                except:
                    print(f"-WAN {wan_id} DNS- Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                if(driver.find_element(By.ID, "bb_natEnable").get_attribute("class") != "switch active "):
                    print(f"-WAN {wan_id} IP NAT- Enable Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        if(finish_loading == False and counter == 120):
            print(f"-WAN {wan_id}- 2nd Apply Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        time.sleep(7)

        # ONT WAN 傳入值測試 第三次
        driver.switch_to.window(driver.window_handles[0])
        mod.Switch_Frame(driver)
        time.sleep(1)
        ONT_Con_ONT_Wan_ID_Select(driver,wan_id)
        time.sleep(0.1)
        ONT_Con_ONT_Wan_Connection_Type_PPPoE(driver)
        ONT_Con_ONT_Wan_Connection_Type_PPPoE_UN(driver,"admin")
        ONT_Con_ONT_Wan_Connection_Type_PPPoE_PW(driver,"1234")
        ONT_Con_ONT_Wan_Service_voip(driver,True)
        ONT_Con_ONT_Wan_Service_iptv(driver,False)
        ONT_Con_ONT_Wan_VLAN_vid(driver,"")
        ONT_Con_ONT_Wan_VLAN_priority(driver,1)
        ONT_Con_ONT_Wan_VLAN_mvlan(driver,"")
        ONT_Con_ONT_Wan_IPv4_dynamic(driver)
        ONT_Con_ONT_Wan_DNS_primary(driver,"")
        ONT_Con_ONT_Wan_DNS_secondary(driver,"")
        ONT_Con_ONT_Wan_IP_NAT_disable(driver)
        ONT_Con_ONT_Wan_2_4G_SSID1(driver,False)
        ONT_Con_ONT_Wan_2_4G_SSID2(driver,False)
        ONT_Con_ONT_Wan_2_4G_SSID3(driver,False)
        ONT_Con_ONT_Wan_2_4G_SSID4(driver,False)
        ONT_Con_ONT_Wan_5G_SSID1(driver,False)
        ONT_Con_ONT_Wan_5G_SSID2(driver,False)
        ONT_Con_ONT_Wan_5G_SSID3(driver,False)
        ONT_Con_ONT_Wan_5G_SSID4(driver,False)
        time.sleep(1)
        time.sleep(7)
        ONT_Con_ONT_Wan_Apply(driver)
        time.sleep(7)

        # ONT Wan 切至Web確認 第三次
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(10)
        driver.refresh()
        if_find = False
        refresh_counter = 0
        while if_find == False and refresh_counter < 120:
            try:
                driver.find_element(By.CLASS_NAME, "icon-broadband-edit")
                if_find = True
            except:
                refresh_counter = refresh_counter+1
                time.sleep(1)
        if(if_find == False and refresh_counter == 120):
            time.sleep(2)
            driver.refresh()
            time.sleep(2)
            try:  
                driver.refresh()
                time.sleep(2)
                driver.find_element(By.CLASS_NAME, "icon-broadband-edit")
            except:
                username2_ = driver.find_element(By.ID, "username")
                username2_.send_keys(newpage_username)
                password2_ = driver.find_element(By.ID, "userpassword")
                password2_.send_keys(newpage_password)
                driver.find_element(By.ID, "h_menu_list").click()
                time.sleep(3)
                driver.find_element(By.LINK_TEXT, "Network Setting").click()
                time.sleep(3)
                driver.find_element(By.XPATH, "//div[@id='Broadband']/span").click()
                time.sleep(2)
        time.sleep(2)
        driver.find_elements(By.CLASS_NAME, "icon-broadband-edit")[wan_id-1].click()
        time.sleep(10)
        
        
        finish_loading = False
        if_find = False
        counter = 0
        while finish_loading == False and counter < 120:
            try:
                driver.find_element(By.XPATH, "//*[@id='bb_srvLinkTypeSelect']/option[2]")
                if_find = True
            except:
                time.sleep(2)
                counter = counter+1
            if(if_find == True and driver.find_element(By.XPATH, "//*[@id='bb_srvLinkTypeSelect']/option[2]").is_selected() != True):
                time.sleep(1)
                counter = counter+1
                # print(f"-WAN {wan_id} Active- Enable Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
            elif(if_find):
                time.sleep(10)
                finish_loading = True
                if(driver.find_element(By.ID, "bb_pppUsername").get_attribute("value") == "admin"):
                    driver.find_element(By.ID, "bb_pppPassword_maskCheck").click()
                    if(driver.find_element(By.ID, "bb_pppPassword").get_attribute("value") != "1234"):
                        print(f"-WAN {wan_id} Connection Type- PPPoE Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                else:
                    print(f"-WAN {wan_id} Connection Type- PPPoE Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                if(driver.find_element(By.ID, "bb_igmpEnable").get_attribute("class") != "switch  "):
                    print(f"-WAN {wan_id} IPTV- Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                if(driver.find_element(By.ID, "bb_enblVlan").get_attribute("class") != "switch  "):
                    print(f"-WAN {wan_id} VLAN- Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                if(driver.find_element(By.ID, "bb_enblMvlan").get_attribute("class") != "switch  disabled"):
                    print(f"-WAN {wan_id} MVLAN- Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                try:
                    driver.find_element(By.ID, "a_bb_ipAddrValue")
                    print(f"-WAN {wan_id} IPv4 Address- Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                except:
                    pass
                try:
                    driver.find_element(By.ID, "a_ipDns1")
                    print(f"-WAN {wan_id} DNS- Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                except:
                    pass
                if(driver.find_element(By.ID, "bb_natEnable").get_attribute("class") != "switch  "):
                    print(f"-WAN {wan_id} IP NAT- Disable Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        if(finish_loading == False and counter == 120):
            print(f"-WAN {wan_id}- 3rd Apply Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        time.sleep(7)

        # ONT Web路徑導向VoIP > SIP > SIP Service Provider ONT Web voip Check
        if_find = False
        counter = 0
        while if_find == False and counter < 120:
            try:
                driver.find_element(By.ID, "h_menu_list").click()
                time.sleep(0.5)
                if_find = True
            except:
                counter = counter+1
                time.sleep(1)
        driver.find_element(By.LINK_TEXT, "VoIP").click()
        time.sleep(3)
        driver.find_element(By.XPATH, "//div[@id='SIP']/span").click()
        if_find = False
        counter = 0
        while if_find == False and counter < 120:
            try:
                driver.find_element(By.ID, "tab_VoIP_SIPServiceProvider_Tab").click()
                time.sleep(0.5)
                if_find = True
            except:
                counter = counter+1
                time.sleep(1)
        if_find = False
        counter = 0
        while if_find == False and counter < 120:
            try:
                driver.find_element(By.ID, "VoIP_SIPServiceProvider_Edit1").click()
                time.sleep(0.5)
                if_find = True
            except:
                counter = counter+1
                time.sleep(1)
        if_find = False
        counter = 0
        while if_find == False and counter < 120:
            try:
                driver.find_element(By.ID, "icon-icon-extend").click()
                time.sleep(0.5)
                if_find = True
            except:
                counter = counter+1
                time.sleep(1)
        time.sleep(5)
        try:
            if(driver.find_element(By.ID, ONT_Web_VOIP_WAN_ID[wan_id-2]).get_attribute("class") != "custom-control custom-checkbox active "):
                print(f"-WAN {wan_id} VoIP- Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        except:
            print(f"-WAN {wan_id} VoIP- Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))

        # ONT WAN 傳入值測試 第四次
        driver.switch_to.window(driver.window_handles[0])
        mod.Switch_Frame(driver)
        time.sleep(1)
        ONT_Con_ONT_Wan_ID_Select(driver,wan_id)
        time.sleep(0.1)
        ONT_Con_ONT_Wan_Service_voip(driver,False)
        ONT_Con_ONT_Wan_Service_tr069(driver,True)
        time.sleep(1)
        time.sleep(7)
        ONT_Con_ONT_Wan_Apply(driver)
        time.sleep(7)

        # ONT Wan 切至Web確認 第四次
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(10)
        driver.refresh()
        if_find = False
        refresh_counter = 0
        while if_find == False and refresh_counter < 120:
            try:
                driver.find_element(By.ID, "tab_VoIP_SIPServiceProvider_Tab")
                if_find = True
            except:
                refresh_counter = refresh_counter+1
                time.sleep(1)
        if(if_find == False and refresh_counter == 120):
            time.sleep(2)
            driver.refresh()
            time.sleep(2)
            try:  
                driver.refresh()
                time.sleep(2)
                driver.find_element(By.ID, "tab_VoIP_SIPServiceProvider_Tab")
            except:
                username2_ = driver.find_element(By.ID, "username")
                username2_.send_keys(newpage_username)
                password2_ = driver.find_element(By.ID, "userpassword")
                password2_.send_keys(newpage_password)
                driver.find_element(By.ID, "h_menu_list").click()
                time.sleep(3)
                driver.find_element(By.LINK_TEXT, "VoIP").click()
                time.sleep(3)
                driver.find_element(By.XPATH, "//div[@id='SIP']/span").click()
                time.sleep(1)
        time.sleep(2)
        if_find = False
        counter = 0
        while if_find == False and counter < 120:
            try:
                driver.find_element(By.ID, "tab_VoIP_SIPServiceProvider_Tab").click()
                time.sleep(3)
                if_find = True
            except:
                counter = counter+1
                time.sleep(1)
        time.sleep(10)
        driver.find_element(By.ID, "VoIP_SIPServiceProvider_Edit1").click()
        time.sleep(10)
        driver.find_element(By.ID, "icon-icon-extend").click()
        time.sleep(5)

        try:
            if(driver.find_element(By.ID, ONT_Web_VOIP_WAN_ID[wan_id-2]).get_attribute("class") == "custom-control custom-checkbox active "):
                print(f"-WAN {wan_id} VoIP- Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        except:
            pass
        time.sleep(7)

        # ONT Web路徑導向VoIP > Maintenance > TR-069 Client ONT Web tr069 Check
        mod.Find_by_id_wait_click(driver,"h_menu_list",120)
        mod.Find_by_link_text_wait_click(driver,"Maintenance",10)
        mod.Find_by_xpath_wait_click(driver,"//div[@id='TR-069_Client']/span",10)
        time.sleep(5)

        if(driver.find_elements(By.CLASS_NAME, "custom-control-input")[wan_id+7].is_selected() == True):
            print(f"-WAN {wan_id} TR069- Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))

        # ONT Web路徑導回Network Setting > Broadband
        if_find = False
        counter = 0
        while if_find == False and counter < 120:
            try:
                driver.find_element(By.ID, "h_menu_list").click()
                time.sleep(0.5)
                if_find = True
            except:
                counter = counter+1
                time.sleep(1)
        if_find = False
        counter = 0
        while if_find == False and counter < 120:
            try:
                driver.find_element(By.LINK_TEXT, "Network Setting").click()
                time.sleep(0.5)
                if_find = True
            except:
                counter = counter+1
                time.sleep(1)
        if_find = False
        counter = 0
        while if_find == False and counter < 120:
            try:
                driver.find_element(By.XPATH, "//div[@id='Broadband']/span").click()
                time.sleep(0.5)
                if_find = True
            except:
                counter = counter+1
                time.sleep(1)
        time.sleep(1)

        # ONT WAN 回歸預設值並刪除
        driver.switch_to.window(driver.window_handles[0])
        mod.Switch_Frame(driver)
        time.sleep(1)
        ONT_Con_ONT_Wan_ID_Select(driver,wan_id)
        time.sleep(3)
        ONT_Con_ONT_Wan_Connection_Type_ipoe(driver)
        ONT_Con_ONT_Wan_Service_tr069(driver,False)
        time.sleep(3)
        ONT_Con_ONT_Wan_Apply(driver)
        for index in range(driver.find_elements(By.CLASS_NAME, "listWanConfig").__len__()):
            if(driver.find_elements(By.NAME, "rpGponOntWanConfig_WanId")[index].get_attribute("textContent") == f"{wan_id}"):
                driver.find_elements(By.NAME, "rpGponOntWanConfig_chkDel")[index].click()
        ONT_Con_ONT_Wan_Delete(driver)

        print(f"WAN {wan_id} Test Finished",file = open("ONT_Status_Test_report.txt", '+a'))

# -------------------------end-------------------------

# ONT LAN
# GPON > ONT Config > ONT LAN
# -------------------------start-------------------------

    # 設定 WAN 8 為 ONT LAN 的測試環境
    ONT_Con_ONT_Wan_ID_Select(driver,8)
    ONT_Con_ONT_Wan_Active_enable(driver)
    ONT_Con_ONT_Wan_Default_disable(driver)
    ONT_Con_ONT_Wan_Connection_Type_ipoe(driver)
    ONT_Con_ONT_Wan_VLAN_vid(driver,"1000")
    ONT_Con_ONT_Wan_VLAN_priority(driver,1)
    ONT_Con_ONT_Wan_VLAN_mvlan(driver,"2000")
    ONT_Con_ONT_Wan_IPv4_static(driver)
    ONT_Con_ONT_Wan_IP_NAT_disable(driver)
    ONT_Con_ONT_Wan_LAN_port4(driver,True)
    ONT_Con_ONT_Wan_Apply(driver)

    # 切至ONT LAN 17-16-2
    mod.Tab_Switch(driver,"ONT LAN")
    retry = True
    while retry:
        try:
            ONT_Con_ONT_Lan_Slot_Pon_Select(driver,slot,port)
            retry = False
        except:
            retry = True
        time.sleep(0.5)
        if(mod.IsAlert(driver)):
            break
        time.sleep(0.5)
    retry = True
    counter = 0
    while retry and counter <= 20:
        try:
            ONT_Con_ONT_Lan_Tem_Select(driver,aid_num+1)
            time.sleep(0.5)
            ONT_Con_ONT_Wan_Load(driver)
            time.sleep(0.5)
            retry = False
        except:
            counter = counter+1
            retry = True
    
    # ONT LAN 傳入值測試 第一次
    ONT_Con_ONT_Lan_ID_Select(driver,8)
    ONT_Con_ONT_Lan_IPv4_Address(driver,"192.168.8.100")
    ONT_Con_ONT_Lan_IPv4_Mask(driver,"255.255.255.0")
    ONT_Con_ONT_Lan_DHCP_disable(driver)
    time.sleep(3)
    ONT_Con_ONT_Lan_Apply(driver)
    time.sleep(10)

    # ONT Web路徑導向 Network Setting > Home Networking
    driver.switch_to.window(driver.window_handles[1])
    mod.Find_by_id_wait_click(driver,"h_menu_list",120)
    mod.Find_by_link_text_wait_click(driver,"Network Setting",10)
    mod.Find_by_xpath_wait_click(driver,'//*[@id="network"]/li[3]',10)

    # 重新整理
    time.sleep(10)
    driver.refresh()
    if_find = False
    refresh_counter = 0
    while if_find == False and refresh_counter < 120:
        try:
            driver.find_element(By.ID, "ls_gp_select")
            if_find = True
        except:
            refresh_counter = refresh_counter+1
            time.sleep(1)
    if(if_find == False and refresh_counter == 120):
        time.sleep(2)
        driver.refresh()
        time.sleep(2)
        try:  
            driver.refresh()
            time.sleep(2)
            driver.find_element(By.ID, "ls_gp_select")
        except:
            username2_ = driver.find_element(By.ID, "username")
            username2_.send_keys(newpage_username)
            password2_ = driver.find_element(By.ID, "userpassword")
            password2_.send_keys(newpage_password)
            mod.Find_by_id_wait_click(driver,"h_menu_list",120)
            mod.Find_by_link_text_wait_click(driver,"Network Setting",10)
            mod.Find_by_xpath_wait_click(driver,'//*[@id="network"]/li[3]',10)
    time.sleep(2)

    # ONT LAN 確認 第一次
    retry = True
    counter = 0
    while retry and counter < 80:
        try:
            Select(driver.find_element(By.ID, "ls_gp_select")).select_by_visible_text("BR_WAN8")
            retry = False
        except:
            time.sleep(1)
    time.sleep(10)
    if(driver.find_element(By.ID, "a_ls_ip_value_1").get_attribute("value") != "192" or driver.find_element(By.ID, "a_ls_ip_value_2").get_attribute("value") != "168" or driver.find_element(By.ID, "a_ls_ip_value_3").get_attribute("value") != "8" or driver.find_element(By.ID, "a_ls_ip_value_4").get_attribute("value") != "100"):
        print(f"-LAN 8 IPv4 Address- address Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
    if(driver.find_element(By.ID, "a_ls_subnetmask_value_1").get_attribute("value") != "255" or driver.find_element(By.ID, "a_ls_subnetmask_value_2").get_attribute("value") != "255" or driver.find_element(By.ID, "a_ls_subnetmask_value_3").get_attribute("value") != "255" or driver.find_element(By.ID, "a_ls_subnetmask_value_4").get_attribute("value") != "0"):
        print(f"-LAN 8 IPv4 Address- mask Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
    if(driver.find_element(By.XPATH, '//*[@id="LANSetup_DHCP2"]/input').is_selected() != True):
        print(f"-LAN 8 DHCP- disable Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
    
    # ONT LAN 傳入值測試 第二次
    driver.switch_to.window(driver.window_handles[0])
    mod.Switch_Frame(driver)
    ONT_Con_ONT_Lan_ID_Select(driver,8)
    ONT_Con_ONT_Lan_IPv4_Address(driver,"192.168.8.100")
    ONT_Con_ONT_Lan_IPv4_Mask(driver,"255.255.255.0")
    mod.Find_by_id_wait_click(driver,"rpOntLan_RdoTypeDhcpRelay",20)
    ONT_Con_ONT_Lan_DHCP_relay_ip(driver,"192.168.8.201")
    time.sleep(3)
    ONT_Con_ONT_Lan_Apply(driver)
    time.sleep(10)

    # 切至Web 重新整理
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(5)
    driver.refresh()
    if_find = False
    refresh_counter = 0
    while if_find == False and refresh_counter < 120:
        try:
            driver.find_element(By.ID, "ls_gp_select")
            if_find = True
        except:
            refresh_counter = refresh_counter+1
            time.sleep(1)
    if(if_find == False and refresh_counter == 120):
        time.sleep(2)
        driver.refresh()
        time.sleep(2)
        try:  
            driver.refresh()
            time.sleep(2)
            driver.find_element(By.ID, "ls_gp_select")
        except:
            username2_ = driver.find_element(By.ID, "username")
            username2_.send_keys(newpage_username)
            password2_ = driver.find_element(By.ID, "userpassword")
            password2_.send_keys(newpage_password)
            mod.Find_by_id_wait_click(driver,"h_menu_list",120)
            mod.Find_by_link_text_wait_click(driver,"Network Setting",10)
            mod.Find_by_xpath_wait_click(driver,'//*[@id="network"]/li[3]',10)
    time.sleep(2)

    # ONT LAN 確認 第二次
    retry = True
    counter = 0
    while retry and counter < 80:
        try:
            Select(driver.find_element(By.ID, "ls_gp_select")).select_by_visible_text("BR_WAN8")
            retry = False
        except:
            time.sleep(1)
    time.sleep(2)
    if(driver.find_element(By.XPATH, '//*[@id="LANSetup_DHCP3"]/input').is_selected() != True):
        print(f"-LAN 8 DHCP- relay Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
    elif(driver.find_element(By.ID, "a_ls_dhcprelayaddr_value_1").get_attribute("value") != "192" or driver.find_element(By.ID, "a_ls_dhcprelayaddr_value_2").get_attribute("value") != "168" or driver.find_element(By.ID, "a_ls_dhcprelayaddr_value_3").get_attribute("value") != "8" or driver.find_element(By.ID, "a_ls_dhcprelayaddr_value_4").get_attribute("value") != "201"):
        print(f"-LAN 8 DHCP- relay Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
    
    # ONT LAN 傳入值測試 第三次
    driver.switch_to.window(driver.window_handles[0])
    mod.Switch_Frame(driver)
    ONT_Con_ONT_Lan_ID_Select(driver,8)
    ONT_Con_ONT_Lan_IPv4_Address(driver,"192.168.8.100")
    ONT_Con_ONT_Lan_IPv4_Mask(driver,"255.255.255.0")
    ONT_Con_ONT_Lan_DHCP_server(driver)
    ONT_Con_ONT_Lan_DHCP_server_begin(driver,"192.168.8.200")
    ONT_Con_ONT_Lan_DHCP_server_end(driver,"192.168.8.210")
    ONT_Con_ONT_Lan_DNS_isp(driver)
    time.sleep(3)
    ONT_Con_ONT_Lan_Apply(driver)
    time.sleep(10)

    # 切至Web 重新整理
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(5)
    driver.refresh()
    if_find = False
    refresh_counter = 0
    while if_find == False and refresh_counter < 120:
        try:
            driver.find_element(By.ID, "ls_gp_select")
            if_find = True
        except:
            refresh_counter = refresh_counter+1
            time.sleep(1)
    if(if_find == False and refresh_counter == 120):
        time.sleep(2)
        driver.refresh()
        time.sleep(2)
        try:  
            driver.refresh()
            time.sleep(2)
            driver.find_element(By.ID, "ls_gp_select")
        except:
            username2_ = driver.find_element(By.ID, "username")
            username2_.send_keys(newpage_username)
            password2_ = driver.find_element(By.ID, "userpassword")
            password2_.send_keys(newpage_password)
            mod.Find_by_id_wait_click(driver,"h_menu_list",120)
            mod.Find_by_link_text_wait_click(driver,"Network Setting",10)
            mod.Find_by_xpath_wait_click(driver,'//*[@id="network"]/li[3]',10)
    time.sleep(2)

    # ONT LAN 確認 第三次
    retry = True
    counter = 0
    while retry and counter < 80:
        try:
            Select(driver.find_element(By.ID, "ls_gp_select")).select_by_visible_text("BR_WAN8")
            retry = False
        except:
            time.sleep(1)
    time.sleep(2)
    if(driver.find_element(By.XPATH, '//*[@id="LANSetup_DHCP1"]/input').is_selected() != True):
        print(f"-LAN 8 DHCP- server Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
    elif(driver.find_element(By.ID, "a_ls_dhcpstart_value_1").get_attribute("value") != "192" or driver.find_element(By.ID, "a_ls_dhcpstart_value_2").get_attribute("value") != "168" or driver.find_element(By.ID, "a_ls_dhcpstart_value_3").get_attribute("value") != "8" or driver.find_element(By.ID, "a_ls_dhcpstart_value_4").get_attribute("value") != "200"):
        print(f"-LAN 8 DHCP- server Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
    elif(driver.find_element(By.ID, "a_ls_dhcpend_value_1").get_attribute("value") != "192" or driver.find_element(By.ID, "a_ls_dhcpend_value_2").get_attribute("value") != "168" or driver.find_element(By.ID, "a_ls_dhcpend_value_3").get_attribute("value") != "8" or driver.find_element(By.ID, "a_ls_dhcpend_value_4").get_attribute("value") != "210"):
        print(f"-LAN 8 DHCP- server Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
    elif(driver.find_element(By.XPATH, '//*[@id="LANSetup_DNSFromISP1"]/input').is_selected() != True):
        print(f"-LAN 8 DNS- isp Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
    else:
        print(f"-LAN 8 DNS- isp Test Pass",file = open("ONT_Status_Test_report.txt", '+a'))
    
    # ONT LAN 傳入值測試 第四次
    driver.switch_to.window(driver.window_handles[0])
    mod.Switch_Frame(driver)
    ONT_Con_ONT_Lan_ID_Select(driver,8)
    ONT_Con_ONT_Lan_IPv4_Address(driver,"192.168.8.100")
    ONT_Con_ONT_Lan_IPv4_Mask(driver,"255.255.255.0")
    ONT_Con_ONT_Lan_DHCP_server(driver)
    ONT_Con_ONT_Lan_DHCP_server_begin(driver,"192.168.8.200")
    ONT_Con_ONT_Lan_DHCP_server_end(driver,"192.168.8.210")
    ONT_Con_ONT_Lan_DNS_proxy(driver)
    time.sleep(3)
    ONT_Con_ONT_Lan_Apply(driver)
    time.sleep(10)

    # 切至Web 重新整理
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(5)
    driver.refresh()
    if_find = False
    refresh_counter = 0
    while if_find == False and refresh_counter < 120:
        try:
            driver.find_element(By.ID, "ls_gp_select")
            if_find = True
        except:
            refresh_counter = refresh_counter+1
            time.sleep(1)
    if(if_find == False and refresh_counter == 120):
        time.sleep(2)
        driver.refresh()
        time.sleep(2)
        try:  
            driver.refresh()
            time.sleep(2)
            driver.find_element(By.ID, "ls_gp_select")
        except:
            username2_ = driver.find_element(By.ID, "username")
            username2_.send_keys(newpage_username)
            password2_ = driver.find_element(By.ID, "userpassword")
            password2_.send_keys(newpage_password)
            mod.Find_by_id_wait_click(driver,"h_menu_list",120)
            mod.Find_by_link_text_wait_click(driver,"Network Setting",10)
            mod.Find_by_xpath_wait_click(driver,'//*[@id="network"]/li[3]',10)
    time.sleep(2)

    # ONT LAN 確認 第四次
    retry = True
    counter = 0
    while retry and counter < 80:
        try:
            Select(driver.find_element(By.ID, "ls_gp_select")).select_by_visible_text("BR_WAN8")
            retry = False
        except:
            time.sleep(1)
    time.sleep(2)
    if(driver.find_element(By.XPATH, '//*[@id="LANSetup_DHCP1"]/input').is_selected() != True):
        print(f"-LAN 8 DHCP- server Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
    elif(driver.find_element(By.XPATH, '//*[@id="LANSetup_DNSDNSProxy1"]/input').is_selected() != True):
        print(f"-LAN 8 DNS- proxy Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
    else:
        print(f"-LAN 8 DNS- proxy Test Pass",file = open("ONT_Status_Test_report.txt", '+a'))
    
    # ONT LAN 傳入值測試 第五次
    driver.switch_to.window(driver.window_handles[0])
    mod.Switch_Frame(driver)
    ONT_Con_ONT_Lan_ID_Select(driver,8)
    ONT_Con_ONT_Lan_IPv4_Address(driver,"192.168.8.100")
    ONT_Con_ONT_Lan_IPv4_Mask(driver,"255.255.255.0")
    mod.Find_by_id_wait_click(driver,"rpOntLan_RdoTypeDhcpServer",20)
    ONT_Con_ONT_Lan_DHCP_server_begin(driver,"192.168.8.200")
    ONT_Con_ONT_Lan_DHCP_server_end(driver,"192.168.8.210")
    mod.Find_by_id_wait_click(driver,"rpOntLan_RdoTypeDnsStatic",20)
    ONT_Con_ONT_Lan_DNS_static_primary(driver,"192.168.8.1")
    ONT_Con_ONT_Lan_DNS_static_secondary(driver,"192.168.8.2")
    time.sleep(3)
    ONT_Con_ONT_Lan_Apply(driver)
    time.sleep(10)

    # 切至Web 重新整理
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(5)
    driver.refresh()
    if_find = False
    refresh_counter = 0
    while if_find == False and refresh_counter < 120:
        try:
            driver.find_element(By.ID, "ls_gp_select")
            if_find = True
        except:
            refresh_counter = refresh_counter+1
            time.sleep(1)
    if(if_find == False and refresh_counter == 120):
        time.sleep(2)
        driver.refresh()
        time.sleep(2)
        try:  
            driver.refresh()
            time.sleep(2)
            driver.find_element(By.ID, "ls_gp_select")
        except:
            username2_ = driver.find_element(By.ID, "username")
            username2_.send_keys(newpage_username)
            password2_ = driver.find_element(By.ID, "userpassword")
            password2_.send_keys(newpage_password)
            mod.Find_by_id_wait_click(driver,"h_menu_list",120)
            mod.Find_by_link_text_wait_click(driver,"Network Setting",10)
            mod.Find_by_xpath_wait_click(driver,'//*[@id="network"]/li[3]',10)
    time.sleep(2)

    # ONT LAN 確認 第五次
    retry = True
    counter = 0
    while retry and counter < 80:
        try:
            Select(driver.find_element(By.ID, "ls_gp_select")).select_by_visible_text("BR_WAN8")
            retry = False
        except:
            time.sleep(1)
    time.sleep(2)
    if(driver.find_element(By.XPATH, '//*[@id="LANSetup_DHCP1"]/input').is_selected() != True):
        print(f"-LAN 8 DHCP- server Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
    # 3416-42A + PMG5622GA static Test Fail
    elif(driver.find_element(By.XPATH, '//*[@id="LANSetup_DNSStatic1"]/input').is_selected() != True):
        print(f"-LAN 8 DNS- static Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
    elif(driver.find_element(By.ID, "a_ls_dnsaddr1_1").get_attribute("value") != "192" or driver.find_element(By.ID, "a_ls_dnsaddr1_2").get_attribute("value") != "168" or driver.find_element(By.ID, "a_ls_dnsaddr1_3").get_attribute("value") != "8" or driver.find_element(By.ID, "a_ls_dnsaddr1_4").get_attribute("value") != "1"):
        print(f"-LAN 8 DHCP- server Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
    elif(driver.find_element(By.ID, "a_ls_dnsaddr2_1").get_attribute("value") != "192" or driver.find_element(By.ID, "a_ls_dnsaddr2_2").get_attribute("value") != "168" or driver.find_element(By.ID, "a_ls_dnsaddr2_3").get_attribute("value") != "8" or driver.find_element(By.ID, "a_ls_dnsaddr2_4").get_attribute("value") != "2"):
        print(f"-LAN 8 DHCP- server Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
    time.sleep(10)

    print("LAN 8 Test Finished",file = open("ONT_Status_Test_report.txt", '+a'))

    # 刪除ONT LAN 8 設定
    driver.switch_to.window(driver.window_handles[0])
    mod.Switch_Frame(driver)
    time.sleep(1)
    for index in range(driver.find_elements(By.CLASS_NAME, "listLan").__len__()):
        if(driver.find_elements(By.NAME, "rpOntLan_Id")[index].get_attribute("textContent") == "8"):
            driver.find_elements(By.NAME, "rpGponOntLan_chkDel")[index].click()
            ONT_Con_ONT_Lan_Delete(driver)
            break

# -------------------------end-------------------------

    # 路徑導向ONT WAN 17-16-2
    mod.Tab_Switch(driver,"ONT WAN")
    retry = True
    while retry:
        try:
            ONT_Con_ONT_Wan_Slot_Pon_Select(driver,slot,port)
            retry = False
        except:
            retry = True
        time.sleep(0.5)
        if(mod.IsAlert(driver)):
            break
        time.sleep(0.5)
    retry = True
    counter = 0
    while retry and counter <= 20:
        try:
            ONT_Con_ONT_Wan_Tem_Select(driver,aid_num+1)
            time.sleep(0.5)
            ONT_Con_ONT_Wan_Load(driver)
            time.sleep(0.5)
            retry = False
        except:
            counter = counter+1
            retry = True

    # 刪除ONT WAN 8 設定
    time.sleep(1)
    for index in range(driver.find_elements(By.CLASS_NAME, "listWanConfig").__len__()):
        if(driver.find_elements(By.NAME, "rpGponOntWanConfig_WanId")[index].get_attribute("textContent") == "8"):
            driver.find_elements(By.NAME, "rpGponOntWanConfig_chkDel")[index].click()
            ONT_Con_ONT_Wan_Delete(driver)
            break

    print("Test Finishd",file = open("ONT_Status_Test_report.txt", '+a'))
    print("======================================================================================",file = open("ONT_Status_Test_report.txt", '+a'))

    # ONT Config -> ONT Lan

def ONT_Con_ONT_Lan_Slot_Pon_Select(driver,slot,pon):
    Select(driver.find_element(By.ID, "gponSelOltPort")).select_by_visible_text(f"{slot}-{pon}")

def ONT_Con_ONT_Lan_Tem_Select(driver,tem):
    Select(driver.find_element(By.ID, "rpGponOntLan_ont")).select_by_visible_text(f"{tem}")

def ONT_Con_ONT_Lan_Load(driver):
    driver.find_element(By.NAME, "rpGponOntLan_btnLoad").click()

def ONT_Con_ONT_Lan_ID_Select(driver,text):
    Select(driver.find_element(By.ID, "rpOntLan_SltLanId")).select_by_visible_text(f"{text}")

def ONT_Con_ONT_Lan_IPv4_Address(driver,key):
    input = driver.find_element(By.ID, "rpOntLan_TxtIpAddress")
    input.clear()
    input.send_keys(key)

def ONT_Con_ONT_Lan_IPv4_Mask(driver,key):
    input = driver.find_element(By.ID, "rpOntLan_TxtIpMask")
    input.clear()
    input.send_keys(key)

def ONT_Con_ONT_Lan_DHCP_disable(driver):
    driver.find_element(By.ID, "rpOntLan_RdoTypeDhcpDisable").click()

def ONT_Con_ONT_Lan_DHCP_server(driver):
    driver.find_element(By.ID, "rpOntLan_RdoTypeDhcpServer").click()

def ONT_Con_ONT_Lan_DHCP_server_begin(driver,key):
    input = driver.find_element(By.ID, "rpOntLan_TxtIpBeginAddress")
    input.clear()
    input.send_keys(key)

def ONT_Con_ONT_Lan_DHCP_server_end(driver,key):
    input = driver.find_element(By.ID, "rpOntLan_TxtIpEndAddress")
    input.clear()
    input.send_keys(key)

def ONT_Con_ONT_Lan_DHCP_relay(driver):
    driver.find_element(By.ID, "rpOntLan_RdoTypeDhcpRelay").click()

def ONT_Con_ONT_Lan_DHCP_relay_ip(driver,key):
    input = driver.find_element(By.ID, "rpOntLan_TxtIpRelayAddress")
    input.clear()
    input.send_keys(key)

def ONT_Con_ONT_Lan_DNS_isp(driver):
    driver.find_element(By.ID, "rpOntLan_RdoTypeDnsIsp").click()

def ONT_Con_ONT_Lan_DNS_proxy(driver):
    driver.find_element(By.ID, "rpOntLan_RdoTypeDnsProxy").click()

def ONT_Con_ONT_Lan_DNS_static(driver):
    driver.find_element(By.ID, "rpOntLan_RdoTypeDnsStatic").click()

def ONT_Con_ONT_Lan_DNS_static_primary(driver,key):
    input = driver.find_element(By.ID, "rpOntLan_TxtPridns")
    input.clear()
    input.send_keys(key)

def ONT_Con_ONT_Lan_DNS_static_secondary(driver,key):
    input = driver.find_element(By.ID, "rpOntLan_TxtSecdns")
    input.clear()
    input.send_keys(key)

def ONT_Con_ONT_Lan_Apply(driver):
    driver.find_element(By.NAME, "rpOntLan_BtnApply").click()

def ONT_Con_ONT_Lan_Delete(driver):
    driver.find_element(By.NAME, "rpOntLan_BtnDelete").click()

    # ONT Config -> ONT WiFi

def ONT_Con_ONT_WiFi_Slot_Pon_Select(driver,slot,pon):
    Select(driver.find_element(By.ID, "gponSelOltPort")).select_by_visible_text(f"{slot}-{pon}")

def ONT_Con_ONT_WiFi_Tem_Select(driver,tem):
    Select(driver.find_element(By.ID, "rpGponOntWifi_ont")).select_by_visible_text(f"{tem}")

def ONT_Con_ONT_WiFi_Load(driver):
    driver.find_element(By.NAME, "rpGponOntWifi_btnLoad").click()

# ONT Config > ONT WiFi Check
def ONT_Con_ONT_WiFi_Web_Check(driver,ont_aid,slot,port,aid_num,newpage_username,newpage_password):
    print(f"{ont_aid} ONT WiFi Web Check\nTest Start",file = open("ONT_Status_Test_report.txt", '+a'))
    
    # 導向路徑ONT Quick Setup
    driver.switch_to.window(driver.window_handles[0])
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"GPON")
    mod.SubPage_Switch(driver,"ONT Quick Setup")
    mod.Switch_Frame(driver)
    retry = True
    while retry:
        try:
            Slot_Select(driver,slot)
            retry = False
        except:
            retry = True
        time.sleep(0.5)
        if(mod.IsAlert(driver)):
            break
        time.sleep(0.5)
    retry = True
    counter = 0
    while retry and counter <= 20:
        try:
            ONT_Qui_Port_Select(driver,port)
            time.sleep(0.5)
            ONT_Qui_ONT_Qui_Load(driver)
            time.sleep(0.5)
            retry = False
        except:
            counter = counter+1
            retry = True
    driver.find_elements(By.ID, "rpGponOntSetup_ontAid")[aid_num].click()

    # 登入新分頁
    try:
        time.sleep(8)
        driver.find_element(By.CLASS_NAME, "card-block")
    except:
        try:
            driver.switch_to.window(driver.window_handles[1])
            username2_ = driver.find_element(By.ID, "username")
            username2_.send_keys(newpage_username)
            password2_ = driver.find_element(By.ID, "userpassword")
            password2_.send_keys(newpage_password)
            driver.find_element(By.ID, "loginBtn").click()
            time.sleep(2)
        except:
            print("ONT Wed Open Fail",file = open("ONT_Status_Test_report.txt", '+a'))
            print("Test Finishd",file = open("ONT_Status_Test_report.txt", '+a'))
            print("======================================================================================",file = open("ONT_Status_Test_report.txt", '+a'))
            return 0

# ONT WiFi Index = 1
# GPON > ONT Config > ONT WiFi
# -------------------------start-------------------------

    # ONT Web路徑導向Maintenance > Remote MGMT
    driver.find_element(By.ID, "h_menu_list").click()
    time.sleep(0.5)
    driver.find_element(By.LINK_TEXT, "Network Setting").click()
    time.sleep(0.5)
    driver.find_element(By.XPATH, "//div[@id='Wireless']/span").click()

    # 原頁面路徑導向ONT WiFi 17-16-2
    driver.switch_to.window(driver.window_handles[0])
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"ONT Config")
    mod.Switch_Frame(driver)
    mod.Tab_Switch(driver,"ONT WiFi")
    retry = True
    while retry:
        try:
            ONT_Con_ONT_WiFi_Slot_Pon_Select(driver,slot,port)
            retry = False
        except:
            retry = True
        time.sleep(0.5)
        if(mod.IsAlert(driver)):
            break
        time.sleep(0.5)
    retry = True
    counter = 0
    while retry and counter <= 20:
        try:
            ONT_Con_ONT_WiFi_Tem_Select(driver,aid_num+1)
            time.sleep(0.5)
            ONT_Con_ONT_WiFi_Load(driver)
            time.sleep(0.5)
            retry = False
        except:
            counter = counter+1
            retry = True

    # 設定測試值及id
    ONT_WiFi_Band_Name = ["2.4GHz","5GHz"]
    ONT_WiFi_Band_ID_Request = ["rpOntWifi_RdoBand2_4g","rpOntWifi_RdoBand5g"]
    ONT_WiFi_Channel_First_Request = ["1","36"]
    ONT_WiFi_Channel_Second_Request = ["13","128"]
    ONT_WiFi_Bandwidth_Second_Check = ["0","80"]
    ONT_WiFi_Index_Num = ["2","3","4"]

    for band_num in range(2):

        # ONT Web關閉WPS
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[1])
        try:  
            driver.refresh()
            time.sleep(2)
            driver.find_element(By.ID, "tab_Wireless_General_Tab")
        except:
            time.sleep(2)
            driver.refresh()
            time.sleep(2)
            try:  
                driver.refresh()
                time.sleep(2)
                driver.find_element(By.ID, "tab_Wireless_General_Tab")
            except:
                username2_ = driver.find_element(By.ID, "username")
                username2_.send_keys(newpage_username)
                password2_ = driver.find_element(By.ID, "userpassword")
                password2_.send_keys(newpage_password)
                driver.find_element(By.ID, "h_menu_list").click()
                time.sleep(0.5)
                driver.find_element(By.LINK_TEXT, "Network Setting").click()
                time.sleep(0.5)
                driver.find_element(By.XPATH, "//div[@id='Wireless']/span").click()
                time.sleep(2)
        driver.find_element(By.XPATH, f"//*[@id='wifi_radio_general']/option[{band_num+1}]").click()
        time.sleep(1)
        driver.find_element(By.ID, "tab_Wireless_WPS_Tab").click()
        time.sleep(3)
        try:
            if(driver.find_element(By.ID, "enableMethod1").get_attribute("class") == "switch active "):
                driver.find_element(By.ID, "enableMethod1").click()
                time.sleep(3)
        except:
            pass
        if(driver.find_element(By.ID, "enableWPS").get_attribute("class") == "switch active "):
            driver.find_element(By.ID, "enableWPS").click()
            time.sleep(3)
            driver.find_element(By.ID, "Network_Wireless_WPS_ApplyBtn").click()

        # Index 1傳入值測試 第一次
        driver.switch_to.window(driver.window_handles[0])
        mod.Switch_Frame(driver)
        ONT_Con_ONT_WiFi_Band(driver,ONT_WiFi_Band_ID_Request[band_num])
        ONT_Con_ONT_WiFi_Index(driver,"1")
        ONT_Con_ONT_WiFi_SSID_def_btn(driver,False)
        ONT_Con_ONT_WiFi_SSID(driver,"ZYXEL5678901234567890123456789A1")
        ONT_Con_ONT_WiFi_SSID_Enable_Mode(driver,"rpOntWifi_RdoSSIDDisable")
        ONT_Con_ONT_WiFi_Security_Mode(driver,"rpOntWifi_RdoSecurityNone")
        # ONT_Con_ONT_WiFi_PW_def_btn(driver,False)
        # ONT_Con_ONT_WiFi_PW(driver,"ZYXEL5678901234567890123456789012345678901234567890123456789AB1")
        ONT_Con_ONT_WiFi_Channel(driver,ONT_WiFi_Channel_First_Request[band_num])
        ONT_Con_ONT_WiFi_Bandwidth(driver,1)
        ONT_Con_ONT_WiFi_Max_Clients(driver,"1")
        ONT_Con_ONT_WiFi_Apply(driver)
        time.sleep(4)

        # Index 1切至Web確認 第一次
        driver.switch_to.window(driver.window_handles[1])
        try:
            time.sleep(30)
            driver.refresh()
            driver.find_element(By.ID, "tab_Wireless_General_Tab")
        except:
            time.sleep(2)
            driver.refresh()
            time.sleep(2)
            try:  
                driver.refresh()
                time.sleep(2)
                driver.find_element(By.ID, "tab_Wireless_General_Tab")
            except:
                username2_ = driver.find_element(By.ID, "username")
                username2_.send_keys(newpage_username)
                password2_ = driver.find_element(By.ID, "userpassword")
                password2_.send_keys(newpage_password)
                driver.find_element(By.ID, "h_menu_list").click()
                time.sleep(0.5)
                driver.find_element(By.LINK_TEXT, "Network Setting").click()
                time.sleep(0.5)
                driver.find_element(By.XPATH, "//div[@id='Wireless']/span").click()
                time.sleep(2)
        time.sleep(2)
        driver.find_element(By.XPATH, f"//*[@id='wifi_radio_general']/option[{band_num+1}]").click()
        time.sleep(1)
        if(driver.find_element(By.ID, "wifi_ssid_000_11general11_000").get_attribute("value") != "ZYXEL5678901234567890123456789A1"):
            print(f"ONT WiFi {ONT_WiFi_Band_Name[band_num]} Index1 SSID Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        if(driver.find_element(By.ID, "ssid_state_general_enable").get_attribute("class") == "switch  "):
            pass
        elif(driver.find_element(By.ID, "ssid_state_general_enable").get_attribute("class") == "switch active "):
            print(f"ONT WiFi {ONT_WiFi_Band_Name[band_num]} Index1 SSID Enable Mode Disable WiFi-On Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        try:
            driver.find_element(By.CLASS_NAME, "infobox")
            print(f"ONT WiFi {ONT_WiFi_Band_Name[band_num]} Index1 Security Mode Disable Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        except:
            pass
        if(driver.find_element(By.ID, "wifi_channel_general").get_attribute("value") != ONT_WiFi_Channel_First_Request[band_num]):
            print(f"ONT WiFi {ONT_WiFi_Band_Name[band_num]} Index1 Channel {ONT_WiFi_Channel_First_Request[band_num]} Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        if(driver.find_element(By.ID, "wifi_bandwidth_general").get_attribute("value") != "20"):
            print(f"ONT WiFi {ONT_WiFi_Band_Name[band_num]} Index1 Bandwidth 1st Select Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        if(driver.find_element(By.ID, "wifi_maxclient_000_11general11_000").get_attribute("value") != "1"):
            print(f"ONT WiFi {ONT_WiFi_Band_Name[band_num]} Index1 Max Client 1 Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        
        # Index 1傳入值測試 第二次
        driver.switch_to.window(driver.window_handles[0])
        mod.Switch_Frame(driver)
        ONT_Con_ONT_WiFi_Band(driver,ONT_WiFi_Band_ID_Request[band_num])
        ONT_Con_ONT_WiFi_Index(driver,"1")
        ONT_Con_ONT_WiFi_SSID_def_btn(driver,True)
        ONT_Con_ONT_WiFi_SSID_Enable_Mode(driver,"rpOntWifi_RdoSSIDEnaleBroadcast")
        ONT_Con_ONT_WiFi_Security_Mode(driver,"rpOntWifi_RdoSecurityWPA2")
        ONT_Con_ONT_WiFi_PW_def_btn(driver,False)
        ONT_Con_ONT_WiFi_PW(driver,"ZYXEL5678901234567890123456789012345678901234567890123456789AB1")
        ONT_Con_ONT_WiFi_Channel(driver,ONT_WiFi_Channel_Second_Request[band_num])
        ONT_Con_ONT_WiFi_Bandwidth(driver,3)
        ONT_Con_ONT_WiFi_Max_Clients(driver,"32")
        ONT_Con_ONT_WiFi_Apply(driver)
        time.sleep(10)

        # Index 1切至Web確認 第二次
        driver.switch_to.window(driver.window_handles[1])
        try:
            time.sleep(30)
            driver.refresh()
            driver.find_element(By.ID, "tab_Wireless_General_Tab")
        except:
            time.sleep(2)
            driver.refresh()
            time.sleep(2)
            try:  
                driver.refresh()
                time.sleep(2)
                driver.find_element(By.ID, "tab_Wireless_General_Tab")
            except:
                username2_ = driver.find_element(By.ID, "username")
                username2_.send_keys(newpage_username)
                password2_ = driver.find_element(By.ID, "userpassword")
                password2_.send_keys(newpage_password)
                driver.find_element(By.ID, "h_menu_list").click()
                time.sleep(0.5)
                driver.find_element(By.LINK_TEXT, "Network Setting").click()
                time.sleep(0.5)
                driver.find_element(By.XPATH, "//div[@id='Wireless']/span").click()
                time.sleep(2)
        time.sleep(1)
        driver.find_element(By.XPATH, f"//*[@id='wifi_radio_general']/option[{band_num+1}]").click()
        time.sleep(1)
        if(driver.find_element(By.ID, "ssid_state_general_enable").get_attribute("class") == "switch active "):
            pass
        elif(driver.find_element(By.ID, "ssid_state_general_enable").get_attribute("class") == "switch  "):
            print(f"ONT WiFi {ONT_WiFi_Band_Name[band_num]} Index1 SSID Enable Mode Enable&Disable WiFi-Off Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        if(driver.find_element(By.ID, "wifi_hide_ssid_000_11general11_000_label").get_attribute("class") == "custom-control custom-checkbox  " or driver.find_element(By.ID, "wifi_hide_ssid_000_11general11_000_label").get_attribute("class") == "custom-control custom-checkbox  disabled"):
            pass
        elif(driver.find_element(By.ID, "wifi_hide_ssid_000_11general11_000_label").get_attribute("class") == "custom-control custom-checkbox active "):
            print(f"ONT WiFi {ONT_WiFi_Band_Name[band_num]} Index1 SSID Enable Mode Enable&Disable Hide SSID-On Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        try:
            driver.find_element(By.CLASS_NAME, "infobox")
            driver.find_element(By.ID, "wifi_wpa_psk_000_11general11_000_maskCheck").click()
            if(driver.find_element(By.ID, "wifi_wpa_psk_000_11general11_000").get_attribute("value") != "ZYXEL5678901234567890123456789012345678901234567890123456789AB1"):
                print(f"ONT WiFi {ONT_WiFi_Band_Name[band_num]} Index1 Password Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        except:
            print(f"ONT WiFi {ONT_WiFi_Band_Name[band_num]} Index1 Security Mode Enable Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
            print(f"ONT WiFi {ONT_WiFi_Band_Name[band_num]} Index1 Password Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        if(driver.find_element(By.ID, "wifi_channel_general").get_attribute("value") != ONT_WiFi_Channel_Second_Request[band_num]):
            print(f"ONT WiFi {ONT_WiFi_Band_Name[band_num]} Index1 Channel {ONT_WiFi_Channel_Second_Request[band_num]} Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        if(driver.find_element(By.ID, "wifi_bandwidth_general").get_attribute("value") != ONT_WiFi_Bandwidth_Second_Check[band_num]):
            print(f"ONT WiFi {ONT_WiFi_Band_Name[band_num]} Index1 Bandwidth 3rd Select Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        if(driver.find_element(By.ID, "wifi_maxclient_000_11general11_000").get_attribute("value") != "32"):
            print(f"ONT WiFi {ONT_WiFi_Band_Name[band_num]} Index1 Max Client 32 Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        
        # Index 1傳入值測試 第三次
        driver.switch_to.window(driver.window_handles[0])
        mod.Switch_Frame(driver)
        ONT_Con_ONT_WiFi_Band(driver,ONT_WiFi_Band_ID_Request[band_num])
        ONT_Con_ONT_WiFi_Index(driver,"1")
        ONT_Con_ONT_WiFi_SSID_def_btn(driver,True)
        ONT_Con_ONT_WiFi_SSID_Enable_Mode(driver,"rpOntWifi_RdoSSIDEnale")
        ONT_Con_ONT_WiFi_Tx_Power(driver,1)
        ONT_Con_ONT_WiFi_Apply(driver)
        time.sleep(4)

        # Index 1切至Web確認 第三次
        driver.switch_to.window(driver.window_handles[1])
        try:
            time.sleep(30)
            driver.refresh()
            driver.find_element(By.ID, "tab_Wireless_General_Tab")
        except:
            time.sleep(2)
            driver.refresh()
            time.sleep(10)
            driver.refresh()
            time.sleep(2)
            try:  
                driver.refresh()
                time.sleep(2)
                driver.find_element(By.ID, "tab_Wireless_General_Tab")
            except:
                username2_ = driver.find_element(By.ID, "username")
                username2_.send_keys(newpage_username)
                password2_ = driver.find_element(By.ID, "userpassword")
                password2_.send_keys(newpage_password)
                driver.find_element(By.ID, "h_menu_list").click()
                time.sleep(0.5)
                driver.find_element(By.LINK_TEXT, "Network Setting").click()
                time.sleep(0.5)
                driver.find_element(By.XPATH, "//div[@id='Wireless']/span").click()
                time.sleep(2)
        time.sleep(1)
        driver.find_element(By.XPATH, f"//*[@id='wifi_radio_general']/option[{band_num+1}]").click()
        time.sleep(1)
        if(driver.find_element(By.ID, "ssid_state_general_enable").get_attribute("class") == "switch active "):
            pass
        elif(driver.find_element(By.ID, "ssid_state_general_enable").get_attribute("class") == "switch  "):
            print(f"ONT WiFi {ONT_WiFi_Band_Name[band_num]} Index1 SSID Enable Mode Enable WiFi-Off Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        if(driver.find_element(By.ID, "wifi_hide_ssid_000_11general11_000_label").get_attribute("class") == "custom-control custom-checkbox active "):
            pass
        elif(driver.find_element(By.ID, "wifi_hide_ssid_000_11general11_000_label").get_attribute("class") == "custom-control custom-checkbox  "):
            print(f"ONT WiFi {ONT_WiFi_Band_Name[band_num]} Index1 SSID Enable Mode Enable Hide SSID-Off Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        elif(driver.find_element(By.ID, "wifi_hide_ssid_000_11general11_000_label").get_attribute("class") == "custom-control custom-checkbox  disabled"):
            print(f"ONT WiFi {ONT_WiFi_Band_Name[band_num]} Index1 SSID Enable Mode Enable WPS-Fail Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        driver.find_element(By.ID, "tab_Wireless_Others_Tab").click()
        time.sleep(2)
        if(driver.find_element(By.ID, "pwrPcnt").get_attribute("value") != "20"):
            print(f"ONT WiFi {ONT_WiFi_Band_Name[band_num]} Index1 Max Client 20% Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        
        # Index 1傳入值測試 第四次
        driver.switch_to.window(driver.window_handles[0])
        mod.Switch_Frame(driver)
        ONT_Con_ONT_WiFi_Band(driver,ONT_WiFi_Band_ID_Request[band_num])
        ONT_Con_ONT_WiFi_Index(driver,"1")
        ONT_Con_ONT_WiFi_Tx_Power(driver,5)
        ONT_Con_ONT_WiFi_Apply(driver)
        time.sleep(4)

        # Index 1切至Web確認 第四次
        driver.switch_to.window(driver.window_handles[1])
        try:
            time.sleep(30)
            driver.refresh()
            driver.find_element(By.ID, "tab_Wireless_General_Tab")
        except:
            time.sleep(2)
            driver.refresh()
            time.sleep(2)
            try:  
                driver.refresh()
                time.sleep(2)
                driver.find_element(By.ID, "tab_Wireless_General_Tab")
            except:
                username2_ = driver.find_element(By.ID, "username")
                username2_.send_keys(newpage_username)
                password2_ = driver.find_element(By.ID, "userpassword")
                password2_.send_keys(newpage_password)
                driver.find_element(By.ID, "h_menu_list").click()
                time.sleep(0.5)
                driver.find_element(By.LINK_TEXT, "Network Setting").click()
                time.sleep(0.5)
                driver.find_element(By.XPATH, "//div[@id='Wireless']/span").click()
                time.sleep(2)
        time.sleep(1)
        driver.find_element(By.XPATH, f"//*[@id='wifi_radio_general']/option[{band_num+1}]").click()
        time.sleep(1)
        driver.find_element(By.ID, "tab_Wireless_Others_Tab").click()
        time.sleep(2)
        if(driver.find_element(By.ID, "pwrPcnt").get_attribute("value") != "100"):
            print(f"ONT WiFi {ONT_WiFi_Band_Name[band_num]} Index1 Max Client 100% Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))

        for index_num in range(3):
            # Index 2 3 4傳入值測試 第一次
            driver.switch_to.window(driver.window_handles[0])
            mod.Switch_Frame(driver)
            ONT_Con_ONT_WiFi_Band(driver,ONT_WiFi_Band_ID_Request[band_num])
            ONT_Con_ONT_WiFi_Index(driver,ONT_WiFi_Index_Num[index_num])
            ONT_Con_ONT_WiFi_SSID_def_btn(driver,False)
            ONT_Con_ONT_WiFi_SSID(driver,"ZYXEL5678901234567890123456789A1")
            ONT_Con_ONT_WiFi_SSID_Enable_Mode(driver,"rpOntWifi_RdoSSIDDisable")
            ONT_Con_ONT_WiFi_Security_Mode(driver,"rpOntWifi_RdoSecurityNone")
            ONT_Con_ONT_WiFi_Apply(driver)
            time.sleep(4)

            # Index 2 3 4切至Web確認 第一次
            driver.switch_to.window(driver.window_handles[1])
            try:  
                time.sleep(30)
                driver.refresh()
                time.sleep(2)
                driver.refresh()
                time.sleep(2)
                driver.find_element(By.ID, "tab_Wireless_General_Tab")
            except:
                time.sleep(2)
                driver.refresh()
                time.sleep(2)
                try:  
                    driver.refresh()
                    time.sleep(2)
                    driver.find_element(By.ID, "tab_Wireless_General_Tab")
                except:
                    username2_ = driver.find_element(By.ID, "username")
                    username2_.send_keys(newpage_username)
                    password2_ = driver.find_element(By.ID, "userpassword")
                    password2_.send_keys(newpage_password)
                    driver.find_element(By.ID, "h_menu_list").click()
                    time.sleep(0.5)
                    driver.find_element(By.LINK_TEXT, "Network Setting").click()
                    time.sleep(0.5)
                    driver.find_element(By.XPATH, "//div[@id='Wireless']/span").click()
                    time.sleep(2)
            time.sleep(2)
            driver.find_element(By.XPATH, f"//*[@id='wifi_radio_general']/option[{band_num+1}]").click()
            time.sleep(1)
            driver.find_element(By.ID, "tab_Wireless_Guest_Tab").click()
            time.sleep(1)
            driver.find_element(By.ID, f"Network_Wireless_Guest_Edit{index_num+1}").click()
            time.sleep(1)
            if(driver.find_element(By.ID, "wifi_ssid_0110moreap0110").get_attribute("value") != "ZYXEL5678901234567890123456789A1"):
                print(f"ONT WiFi {ONT_WiFi_Band_Name[band_num]} Index{index_num+2} SSID Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
            if(driver.find_element(By.ID, "ssid_state_MoreAPedit_enable").get_attribute("class") == "switch  "):
                pass
            elif(driver.find_element(By.ID, "ssid_state_MoreAPedit_enable").get_attribute("class") == "switch active "):
                print(f"ONT WiFi {ONT_WiFi_Band_Name[band_num]} Index{index_num+2} SSID Enable Mode Disable WiFi-On Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
            try:
                driver.find_element(By.CLASS_NAME, "infobox")
                print(f"ONT WiFi {ONT_WiFi_Band_Name[band_num]} Index{index_num+2} Security Mode Disable Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
            except:
                pass

            # Index 2 3 4傳入值測試 第二次
            driver.switch_to.window(driver.window_handles[0])
            mod.Switch_Frame(driver)
            ONT_Con_ONT_WiFi_Band(driver,ONT_WiFi_Band_ID_Request[band_num])
            ONT_Con_ONT_WiFi_Index(driver,ONT_WiFi_Index_Num[index_num])
            ONT_Con_ONT_WiFi_SSID_def_btn(driver,True)
            ONT_Con_ONT_WiFi_SSID_Enable_Mode(driver,"rpOntWifi_RdoSSIDEnaleBroadcast")
            ONT_Con_ONT_WiFi_Security_Mode(driver,"rpOntWifi_RdoSecurityWPA2")
            ONT_Con_ONT_WiFi_PW_def_btn(driver,False)
            ONT_Con_ONT_WiFi_PW(driver,"ZYXEL5678901234567890123456789012345678901234567890123456789AB1")
            ONT_Con_ONT_WiFi_Apply(driver)
            time.sleep(4)

            # Index 2 3 4切至Web確認 第二次
            driver.switch_to.window(driver.window_handles[1])
            try:
                time.sleep(30)
                driver.refresh()
                time.sleep(2)
                driver.refresh()
                time.sleep(2)
                driver.find_element(By.ID, "tab_Wireless_General_Tab")
            except:
                time.sleep(2)
                driver.refresh()
                time.sleep(2)
                try:  
                    driver.refresh()
                    time.sleep(2)
                    driver.find_element(By.ID, "tab_Wireless_General_Tab")
                except:
                    username2_ = driver.find_element(By.ID, "username")
                    username2_.send_keys(newpage_username)
                    password2_ = driver.find_element(By.ID, "userpassword")
                    password2_.send_keys(newpage_password)
                    driver.find_element(By.ID, "h_menu_list").click()
                    time.sleep(0.5)
                    driver.find_element(By.LINK_TEXT, "Network Setting").click()
                    time.sleep(0.5)
                    driver.find_element(By.XPATH, "//div[@id='Wireless']/span").click()
                    time.sleep(2)
            time.sleep(2)
            driver.find_element(By.XPATH, f"//*[@id='wifi_radio_general']/option[{band_num+1}]").click()
            time.sleep(1)
            driver.find_element(By.ID, "tab_Wireless_Guest_Tab").click()
            time.sleep(1)
            driver.find_element(By.ID, f"Network_Wireless_Guest_Edit{index_num+1}").click()
            time.sleep(1)
            if(driver.find_element(By.ID, "ssid_state_MoreAPedit_enable").get_attribute("class") == "switch active "):
                pass
            elif(driver.find_element(By.ID, "ssid_state_MoreAPedit_enable").get_attribute("class") == "switch  "):
                print(f"ONT WiFi {ONT_WiFi_Band_Name[band_num]} Index{index_num+2} SSID Enable Mode Enable&Disable WiFi-Off Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
            if(driver.find_element(By.ID, "wifi_hide_ssid_0110moreap0110_label").get_attribute("class") == "custom-control custom-checkbox  " or driver.find_element(By.ID, "wifi_hide_ssid_0110moreap0110_label").get_attribute("class") == "custom-control custom-checkbox  disabled"):
                pass
            elif(driver.find_element(By.ID, "wifi_hide_ssid_0110moreap0110_label").get_attribute("class") == "custom-control custom-checkbox active "):
                print(f"ONT WiFi {ONT_WiFi_Band_Name[band_num]} Index{index_num+2} SSID Enable Mode Enable&Disable Hide SSID-On Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
            try:
                driver.find_element(By.CLASS_NAME, "infobox")
                driver.find_element(By.ID, "wifi_wpa_psk_0110moreap0110_maskCheck").click()
                if(driver.find_element(By.ID, "wifi_wpa_psk_0110moreap0110").get_attribute("value") != "ZYXEL5678901234567890123456789012345678901234567890123456789AB1"):
                    print(f"ONT WiFi {ONT_WiFi_Band_Name[band_num]} Index{index_num+2} Password Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
            except:
                print(f"ONT WiFi {ONT_WiFi_Band_Name[band_num]} Index{index_num+2} Security Mode Enable Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                print(f"ONT WiFi {ONT_WiFi_Band_Name[band_num]} Index{index_num+2} Password Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
    
        
            # Index 2 3 4傳入值測試 第三次
            driver.switch_to.window(driver.window_handles[0])
            mod.Switch_Frame(driver)
            ONT_Con_ONT_WiFi_Band(driver,ONT_WiFi_Band_ID_Request[band_num])
            ONT_Con_ONT_WiFi_Index(driver,ONT_WiFi_Index_Num[index_num])
            ONT_Con_ONT_WiFi_SSID_def_btn(driver,True)
            ONT_Con_ONT_WiFi_SSID_Enable_Mode(driver,"rpOntWifi_RdoSSIDEnale")
            ONT_Con_ONT_WiFi_Apply(driver)
            time.sleep(4)

            # Index 2 3 4切至Web確認 第三次
            driver.switch_to.window(driver.window_handles[1])
            try:
                time.sleep(30)
                driver.refresh()
                driver.find_element(By.ID, "tab_Wireless_General_Tab")
            except:
                time.sleep(2)
                driver.refresh()
                time.sleep(10)
                driver.refresh()
                time.sleep(2)
                try:  
                    driver.refresh()
                    time.sleep(2)
                    driver.find_element(By.ID, "tab_Wireless_General_Tab")
                except:
                    username2_ = driver.find_element(By.ID, "username")
                    username2_.send_keys(newpage_username)
                    password2_ = driver.find_element(By.ID, "userpassword")
                    password2_.send_keys(newpage_password)
                    driver.find_element(By.ID, "h_menu_list").click()
                    time.sleep(0.5)
                    driver.find_element(By.LINK_TEXT, "Network Setting").click()
                    time.sleep(0.5)
                    driver.find_element(By.XPATH, "//div[@id='Wireless']/span").click()
                    time.sleep(2)
            time.sleep(2)
            driver.find_element(By.XPATH, f"//*[@id='wifi_radio_general']/option[{band_num+1}]").click()
            time.sleep(1)
            driver.find_element(By.ID, "tab_Wireless_Guest_Tab").click()
            time.sleep(1)
            driver.find_element(By.ID, f"Network_Wireless_Guest_Edit{index_num+1}").click()
            time.sleep(1)
            if(driver.find_element(By.ID, "ssid_state_MoreAPedit_enable").get_attribute("class") == "switch active "):
                pass
            elif(driver.find_element(By.ID, "ssid_state_MoreAPedit_enable").get_attribute("class") == "switch  "):
                print(f"ONT WiFi {ONT_WiFi_Band_Name[band_num]} Index{index_num+2} SSID Enable Mode Enable WiFi-Off Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
            if(driver.find_element(By.ID, "wifi_hide_ssid_0110moreap0110_label").get_attribute("class") == "custom-control custom-checkbox active "):
                pass
            elif(driver.find_element(By.ID, "wifi_hide_ssid_0110moreap0110_label").get_attribute("class") == "custom-control custom-checkbox  "):
                print(f"ONT WiFi {ONT_WiFi_Band_Name[band_num]} Index{index_num+2} SSID Enable Mode Enable Hide SSID-Off Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
            elif(driver.find_element(By.ID, "wifi_hide_ssid_0110moreap0110_label").get_attribute("class") == "custom-control custom-checkbox  disabled"):
                print(f"ONT WiFi {ONT_WiFi_Band_Name[band_num]} Index{index_num+2} SSID Enable Mode Enable WPS-Fail Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        
    print("Test Finishd",file = open("ONT_Status_Test_report.txt", '+a'))
    print("======================================================================================",file = open("ONT_Status_Test_report.txt", '+a'))

def ONT_Con_ONT_WiFi_Band(driver,id):
    driver.find_element(By.ID, id).click()
    #rpOntWifi_RdoBand2_4g
    #rpOntWifi_RdoBand5g

def ONT_Con_ONT_WiFi_Index(driver,text):
    Select(driver.find_element(By.ID, "rpOntWifi_SltWifiId")).select_by_visible_text(text)

def ONT_Con_ONT_WiFi_SSID_def_btn(driver,request):
    active = driver.find_element(By.ID, "rpOntWifi_ChkDefaultSSID")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()

def ONT_Con_ONT_WiFi_SSID(driver,key):
    input = driver.find_element(By.ID, "rpOntWifi_TextIptSSID")
    input.clear()
    input.send_keys(key)
    
def ONT_Con_ONT_WiFi_SSID_Enable_Mode(driver,id):
    driver.find_element(By.ID, id).click()
    #rpOntWifi_RdoSSIDDisable
    #rpOntWifi_RdoSSIDEnaleBroadcast
    #rpOntWifi_RdoSSIDEnale
    
def ONT_Con_ONT_WiFi_Security_Mode(driver,id):
    driver.find_element(By.ID, id).click()
    #rpOntWifi_RdoSecurityNone
    #rpOntWifi_RdoSecurityWPA2
    #rpOntWifi_RdoSecurityWEP

def ONT_Con_ONT_WiFi_PW_def_btn(driver,request):
    active = driver.find_element(By.ID, "rpOntWifi_ChkDefaultPassword")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()

def ONT_Con_ONT_WiFi_PW(driver,key):
    input = driver.find_element(By.ID, "rpOntWifi_TextIptPassword")
    input.clear()
    input.send_keys(key)

def ONT_Con_ONT_WiFi_Channel(driver,text):
    Select(driver.find_element(By.ID, "rpOntWifi_SltChannel")).select_by_visible_text(text)

def ONT_Con_ONT_WiFi_Bandwidth(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpOntWifi_SltBandwidth']/option[{sel}]")
    select.click()

def ONT_Con_ONT_WiFi_Max_Clients(driver,key):
    input = driver.find_element(By.ID, "rpOntWifi_TextIptMaxClients")
    input.clear()
    input.send_keys(key)

def ONT_Con_ONT_WiFi_Tx_Power(driver,sel):
    select = driver.find_element(By.XPATH, f"//*[@id='rpOntWifi_SltTx']/option[{sel}]")
    select.click()

def ONT_Con_ONT_WiFi_Apply(driver):
    driver.find_element(By.NAME, "rpOntWifi_BtnApply").click()

def ONT_Con_ONT_WiFi_Reset(driver):
    driver.find_element(By.NAME, "rpOntWifi_BtnReset").click()

    # ONT Config -> ONT Misc

def ONT_Con_ONT_Mis_Slot_Pon_Select(driver,slot,pon):
    Select(driver.find_element(By.NAME, "gponSelOltPort")).select_by_visible_text(f"{slot}-{pon}")

def ONT_Con_ONT_Mis_Tem_Select(driver,tem):
    Select(driver.find_element(By.ID, "rpGponOntMisc_ont")).select_by_visible_text(f"{tem}")

def ONT_Con_ONT_Mis_Load(driver):
    driver.find_element(By.NAME, "rpGponOntMisc_btnLoad").click()

# ONT Config > ONT MISC & ONT Web Value Check
def ONT_Con_ONT_Mis_Web_Check(driver,ont_aid,slot,port,aid_num,newpage_username,newpage_password):
    # test_report = open("ONT_Status_Test_report.txt","w+")
    print(f"{ont_aid} ONT Misc Web Check\nTest Start",file = open("ONT_Status_Test_report.txt", '+a'))
    
    # 導向路徑ONT Quick Setup
    driver.switch_to.window(driver.window_handles[0])
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"GPON")
    mod.SubPage_Switch(driver,"ONT Quick Setup")
    mod.Switch_Frame(driver)
    retry = True
    while retry:
        try:
            Slot_Select(driver,slot)
            retry = False
        except:
            retry = True
        time.sleep(0.5)
        if(mod.IsAlert(driver)):
            break
        time.sleep(0.5)
    retry = True
    counter = 0
    while retry and counter <= 20:
        try:
            ONT_Qui_Port_Select(driver,port)
            time.sleep(0.5)
            ONT_Qui_ONT_Qui_Load(driver)
            time.sleep(0.5)
            retry = False
        except:
            counter = counter+1
            retry = True
    driver.find_elements(By.ID, "rpGponOntSetup_ontAid")[aid_num].click()

    # 偵測是否登入，否則登入新分頁
    try:
        driver.switch_to.window(driver.window_handles[1])
        mod.Find_by_id_wait(driver,"card_sysinfo_modelname",10)
    except:
        try:
            driver.switch_to.window(driver.window_handles[1])
            username2_ = driver.find_element(By.ID, "username")
            username2_.send_keys(newpage_username)
            password2_ = driver.find_element(By.ID, "userpassword")
            password2_.send_keys(newpage_password)
            driver.find_element(By.ID, "loginBtn").click()
        except:
            print("ONT Wed Open Fail",file = open("ONT_Status_Test_report.txt", '+a'))
            print("Test Finishd",file = open("ONT_Status_Test_report.txt", '+a'))
            print("======================================================================================",file = open("ONT_Status_Test_report.txt", '+a'))
            return 0

# ONT Misc Server Check
# GPON > ONT Config > ONT Misc > ONT Service Control
# -------------------------start-------------------------

    # ONT Web路徑導向Maintenance > Remote MGMT
    time.sleep(4)
    mod.Find_by_id_wait_click(driver,"h_menu_list",60)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Maintenance").click()
    time.sleep(0.5)
    driver.find_element(By.XPATH, "//div[@id='Remote_MGMT']/span").click()

    # 原頁面路徑導向ONT Misc 17-16-2
    driver.switch_to.window(driver.window_handles[0])
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"ONT Config")
    mod.Switch_Frame(driver)
    mod.Tab_Switch(driver,"ONT Misc")
    retry = True
    while retry:
        try:
            ONT_Con_ONT_Mis_Slot_Pon_Select(driver,slot,port)
            retry = False
        except:
            retry = True
        time.sleep(0.5)
        if(mod.IsAlert(driver)):
            break
        time.sleep(0.5)
    retry = True
    counter = 0
    while retry and counter <= 20:
        try:
            ONT_Con_ONT_Mis_Tem_Select(driver,aid_num+1)
            time.sleep(0.5)
            ONT_Con_ONT_Mis_Load(driver)
            time.sleep(0.5)
            retry = False
        except:
            counter = counter+1
            retry = True

    # 設定測試值及id
    ONT_Service_Input_Value = [1,65535,65536]
    ONT_Service_Check_Value = ["1","65535","65535"]
    ONT_Service_Check_Request = [False,True,True]
    ONT_Web_Service_Check_Text = ["custom-control custom-checkbox  ","custom-control custom-checkbox active ","custom-control custom-checkbox active "]
    ONT_Service_Name = ["FTP","HTTPS","SNMP","SSH","TELNET"]
    ONT_Service_Lan_Id = ["rpOntService_chkFtpLAN","rpOntService_chkHttpsLAN","rpOntService_chkSnmpLAN","rpOntService_chkSshLAN","rpOntService_chkTelnetLAN"]
    ONT_Service_Wan_Id = ["rpOntService_chkFtpWAN","rpOntService_chkHttpsWAN","rpOntService_chkSnmpWAN","rpOntService_chkSshWAN","rpOntService_chkTelnetWAN"]
    ONT_Service_Port_Id = ["rpOntService_iptFtpPort","rpOntService_iptHttpsPort","rpOntService_iptSnmpPort","rpOntService_iptSshPort","rpOntService_iptTelnetPort"]
    ONT_Web_Service_Lan_Id = ["httpsLan_id_2_label","httpsLan_id_1_label","httpsLan_id_5_label","httpsLan_id_4_label","httpsLan_id_3_label"]
    ONT_Web_Service_Wan_Id = ["wan_2_label","wan_1_label","wan_5_label","wan_4_label","wan_3_label"]
    ONT_Web_Service_Port_Id = ["port_2","port_1","port_5","port_4","port_3"]

    # Server傳入值與Web比對
    if_error = False
    ONT_Con_ONT_Mis_Serv_Con(driver,True)
    for service_num in range(5):
        ONT_Con_ONT_Mis_Serv_Def(driver,False)
        for check_time in range(3):
            mod.Find_by_id_wait(driver,ONT_Service_Lan_Id[service_num],30)
            ONT_Con_ONT_Mis_Serv_Lan_Wan(driver,ONT_Service_Lan_Id[service_num],ONT_Service_Check_Request[check_time])
            ONT_Con_ONT_Mis_Serv_Lan_Wan(driver,ONT_Service_Wan_Id[service_num],ONT_Service_Check_Request[check_time])
            ONT_Con_ONT_Mis_Serv_Port(driver,ONT_Service_Port_Id[service_num],ONT_Service_Input_Value[check_time])
            time.sleep(1)
            ONT_Con_ONT_Mis_Serv_Apply(driver)
            time.sleep(2)
            driver.switch_to.window(driver.window_handles[1])
            try:  
                driver.refresh()
                time.sleep(2)
                driver.find_element(By.ID, "httpsLan_id_2_label")
            except:
                time.sleep(2)
                driver.refresh()
                time.sleep(5)
                username2_ = driver.find_element(By.ID, "username")
                username2_.send_keys(newpage_username)
                password2_ = driver.find_element(By.ID, "userpassword")
                password2_.send_keys(newpage_password)
                driver.find_element(By.ID, "loginBtn").click()
                mod.Find_by_id_wait_click(driver,"h_menu_list",50)
                mod.Find_by_link_text_wait_click(driver,"Maintenance",50)
                mod.Find_by_xpath_wait_click(driver,"//div[@id='Remote_MGMT']/span",50)
                time.sleep(0.5)
            mod.Find_by_id_wait(driver,ONT_Web_Service_Lan_Id[service_num],50)
            if(driver.find_element(By.ID, ONT_Web_Service_Lan_Id[service_num]).get_attribute("class") != ONT_Web_Service_Check_Text[check_time]):
                print(f"ONT Service {ONT_Service_Name[service_num]} LAN",ONT_Service_Check_Request[check_time],"Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                if_error = True
            if(driver.find_element(By.ID, ONT_Web_Service_Wan_Id[service_num]).get_attribute("class") != ONT_Web_Service_Check_Text[check_time]):
                print(f"ONT Service {ONT_Service_Name[service_num]} WAN",ONT_Service_Check_Request[check_time],"Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                if_error = True
            if(driver.find_element(By.ID, ONT_Web_Service_Port_Id[service_num]).get_attribute("value") != ONT_Service_Check_Value[check_time]):
                print(f"ONT Service {ONT_Service_Name[service_num]} Port",ONT_Service_Input_Value[check_time],"Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                if_error = True
            driver.switch_to.window(driver.window_handles[0])
            mod.Switch_Frame(driver)

        # 重設為預設值
        ONT_Con_ONT_Mis_Serv_Lan_Wan(driver,ONT_Service_Lan_Id[service_num],True)
        ONT_Con_ONT_Mis_Serv_Lan_Wan(driver,ONT_Service_Wan_Id[service_num],False)
        ONT_Con_ONT_Mis_Serv_Def(driver,True)
        time.sleep(1)
        ONT_Con_ONT_Mis_Serv_Apply(driver)

    if(if_error == False):
        print("ONT Service Test Pass",file = open("ONT_Status_Test_report.txt", '+a'))
# -------------------------end-------------------------

# ONT Misc Firewall Check
# GPON > ONT Config > ONT Misc > ONT Firewall Control
# -------------------------start-------------------------
    
    # ONT Web路徑導向Security > Firewall
    driver.switch_to.window(driver.window_handles[1])
    try:  
        driver.find_element(By.ID, "h_menu_list").click()
        time.sleep(0.5)
        driver.find_element(By.LINK_TEXT, "Security").click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, "//div[@id='Firewall']/span").click()
    except:
        time.sleep(2)
        driver.refresh()
        time.sleep(2)
        username2_ = driver.find_element(By.ID, "username")
        username2_.send_keys(newpage_username)
        password2_ = driver.find_element(By.ID, "userpassword")
        password2_.send_keys(newpage_password)
        driver.find_element(By.ID, "loginBtn").click()
        mod.Find_by_id_wait_click(driver,"h_menu_list",50)
        mod.Find_by_link_text_wait_click(driver,"Security",50)
        mod.Find_by_xpath_wait_click(driver,"//div[@id='Firewall']/span",50)

    # 設定測試值及id
    ONT_Con_ONT_Mis_Fire_IPv4_Request = [False,True,False,True]
    ONT_Con_ONT_Mis_Fire_IPv6_Request = [False,False,True,True]
    ONT_Con_ONT_Mis_Fire_Lev_Request_Name = ["Low","Medium","High","Medium"]
    ONT_Con_ONT_Mis_Fire_Lev_Request_id = ["rpOntFirewall_RdoLevelLow","rpOntFirewall_RdoLevelMed","rpOntFirewall_RdoLevelHigh","rpOntFirewall_RdoLevelMed"]
    ONT_Con_ONT_Mis_Fire_Lev_Request_Num = [1,2,3,2]
    ONT_Web_Firewall_IPv4_Check_Text = ["switch  ","switch active ","switch  ","switch active "]
    ONT_Web_Firewall_IPv6_Check_Text = ["switch  ","switch  ","switch active ","switch active "]

    # Firewall傳入值與Web比對
    if_error = False
    driver.switch_to.window(driver.window_handles[0])
    mod.Switch_Frame(driver)
    ONT_Con_ONT_Mis_Fire_Con(driver,True)
    for check_time in range(4):
        driver.switch_to.window(driver.window_handles[0])
        mod.Switch_Frame(driver)
        ONT_Con_ONT_Mis_Fire_Ena_IPv4(driver,ONT_Con_ONT_Mis_Fire_IPv4_Request[check_time])
        ONT_Con_ONT_Mis_Fire_Ena_IPv6(driver,ONT_Con_ONT_Mis_Fire_IPv6_Request[check_time])
        ONT_Con_ONT_Mis_Fire_Lev(driver,ONT_Con_ONT_Mis_Fire_Lev_Request_id[check_time])
        time.sleep(1)
        ONT_Con_ONT_Mis_Fire_Apply(driver)
        time.sleep(2)

        driver.switch_to.window(driver.window_handles[1])
        try:  
            driver.refresh()
            time.sleep(2)
            driver.find_element(By.ID, "v_g_enable4")
        except:
            time.sleep(2)
            driver.refresh()
            time.sleep(2)
            username2_ = driver.find_element(By.ID, "username")
            username2_.send_keys(newpage_username)
            password2_ = driver.find_element(By.ID, "userpassword")
            password2_.send_keys(newpage_password)
            driver.find_element(By.ID, "loginBtn").click()
            mod.Find_by_id_wait_click(driver,"h_menu_list",50)
            mod.Find_by_link_text_wait_click(driver,"Maintenance",50)
            mod.Find_by_xpath_wait_click(driver,"//div[@id='Remote_MGMT']/span",50)
        time.sleep(2)

        if(driver.find_element(By.ID, "v_g_enable4").get_attribute("class") != ONT_Web_Firewall_IPv4_Check_Text[check_time]):
            print("ONT Firewall IPv4",ONT_Con_ONT_Mis_Fire_IPv4_Request[check_time],"Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
            if_error = True
        if(driver.find_element(By.ID, "v_g_enable6").get_attribute("class") != ONT_Web_Firewall_IPv6_Check_Text[check_time]):
            print("ONT Firewall IPv6",ONT_Con_ONT_Mis_Fire_IPv6_Request[check_time],"Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
            if_error = True
        if(driver.find_element(By.XPATH, f"//div[@id='l_g_firewallrange']/div/div[{ONT_Con_ONT_Mis_Fire_Lev_Request_Num[check_time]}]").get_attribute("class") != "label active"):
            print("ONT Firewall Level",ONT_Con_ONT_Mis_Fire_Lev_Request_Name[check_time],"Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
            if_error = True

    driver.switch_to.window(driver.window_handles[0])
    mod.Switch_Frame(driver)
    ONT_Con_ONT_Mis_Fire_Con(driver,False)
    ONT_Con_ONT_Mis_Fire_Apply(driver)
    if(if_error == False):
        print("ONT Firewall Test Pass",file = open("ONT_Status_Test_report.txt", '+a'))

# -------------------------end-------------------------

# ONT Misc UPnP Check
# GPON > ONT Config > ONT Misc > ONT UPnP Control
# -------------------------start-------------------------

    # ONT Web路徑導向Network Setting > Home Networking > UPnP
    driver.switch_to.window(driver.window_handles[1])
    try:
        mod.Find_by_id_wait_click(driver,"h_menu_list",50)
        mod.Find_by_link_text_wait_click(driver,"Network Setting",50)
        mod.Find_by_xpath_wait_click(driver,"//div[@id='Home_Networking']/span",50)
        mod.Find_by_id_wait_click(driver,"tab_Network_Home_Networking_UPnP_Tab",50)
    except:
        time.sleep(2)
        driver.refresh()
        time.sleep(2)
        username2_ = driver.find_element(By.ID, "username")
        username2_.send_keys(newpage_username)
        password2_ = driver.find_element(By.ID, "userpassword")
        password2_.send_keys(newpage_password)
        driver.find_element(By.ID, "loginBtn").click()
        time.sleep(2)
        mod.Find_by_id_wait_click(driver,"h_menu_list",50)
        mod.Find_by_link_text_wait_click(driver,"Network Setting",50)
        mod.Find_by_xpath_wait_click(driver,"//div[@id='Home_Networking']/span",50)
        mod.Find_by_id_wait_click(driver,"tab_Network_Home_Networking_UPnP_Tab",50)

    # 設定測試值及id
    ONT_Con_ONT_Mis_UPnP_Ena_Request = [True,False]
    ONT_Con_ONT_Mis_UPnP_Check_Text = ["switch active ","switch  "]

    # UPnP傳入值與Web比對
    if_error = False
    driver.switch_to.window(driver.window_handles[0])
    mod.Switch_Frame(driver)
    ONT_Con_ONT_Mis_UPnP_Con(driver,True)
    for check_time in range(2):
        driver.switch_to.window(driver.window_handles[0])
        mod.Switch_Frame(driver)
        ONT_Con_ONT_Mis_UPnP_Enable(driver,ONT_Con_ONT_Mis_UPnP_Ena_Request[check_time])
        time.sleep(1)
        ONT_Con_ONT_Mis_UPnP_Apply(driver)
        time.sleep(2)

        driver.switch_to.window(driver.window_handles[1])
        try:  
            driver.refresh()
            time.sleep(2)
            driver.find_element(By.ID, "tab_Network_Home_Networking_UPnP_Tab").click()
            time.sleep(0.5)
            driver.find_element(By.ID, "upnp_enable_radio")
        except:
            time.sleep(2)
            driver.refresh()
            time.sleep(2)
            username2_ = driver.find_element(By.ID, "username")
            username2_.send_keys(newpage_username)
            password2_ = driver.find_element(By.ID, "userpassword")
            password2_.send_keys(newpage_password)
            driver.find_element(By.ID, "loginBtn").click()
            time.sleep(2)
            mod.Find_by_id_wait_click(driver,"h_menu_list",50)
            mod.Find_by_link_text_wait_click(driver,"Network Setting",50)
            mod.Find_by_xpath_wait_click(driver,"//div[@id='Home_Networking']/span",50)
            mod.Find_by_id_wait_click(driver,"tab_Network_Home_Networking_UPnP_Tab",50)
        time.sleep(2)

        if(driver.find_element(By.ID, "upnp_enable_radio").get_attribute("class") != ONT_Con_ONT_Mis_UPnP_Check_Text[check_time] or driver.find_element(By.ID, "upnp_natt_enable_radio").get_attribute("class") != ONT_Con_ONT_Mis_UPnP_Check_Text[check_time]):
            print("ONT UPnP",ONT_Con_ONT_Mis_UPnP_Ena_Request[check_time],"Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
            if_error = True

    driver.switch_to.window(driver.window_handles[0])
    mod.Switch_Frame(driver)
    ONT_Con_ONT_Mis_UPnP_Con(driver,False)
    ONT_Con_ONT_Mis_UPnP_Apply(driver)
    if(if_error == False):
        print("ONT UPnP Test Pass",file = open("ONT_Status_Test_report.txt", '+a'))

# -------------------------end-------------------------

# ONT Misc DMZ Check
# GPON > ONT Config > ONT Misc > ONT DMZ Control
# -------------------------start-------------------------

    # ONT Web路徑導向Network Setting > NAT > DMZ
    driver.switch_to.window(driver.window_handles[1])
    try:
        mod.Find_by_id_wait_click(driver,"h_menu_list",50)
        mod.Find_by_link_text_wait_click(driver,"Network Setting",50)
        mod.Find_by_xpath_wait_click(driver,"//div[@id='NAT']/span",50)
        mod.Find_by_id_wait_click(driver,"tab_Network_NAT_DMZ_Tab",50)
    except:
        time.sleep(2)
        driver.refresh()
        time.sleep(2)
        username2_ = driver.find_element(By.ID, "username")
        username2_.send_keys(newpage_username)
        password2_ = driver.find_element(By.ID, "userpassword")
        password2_.send_keys(newpage_password)
        driver.find_element(By.ID, "loginBtn").click()
        time.sleep(2)
        mod.Find_by_id_wait_click(driver,"h_menu_list",50)
        mod.Find_by_link_text_wait_click(driver,"Network Setting",50)
        mod.Find_by_xpath_wait_click(driver,"//div[@id='NAT']/span",50)
        mod.Find_by_id_wait_click(driver,"tab_Network_NAT_DMZ_Tab",50)

    # 設定測試值及id
    ONT_Con_ONT_Mis_DMZ_Request = ["10.10.10.10","10.10.10.254"]
    ONT_Web_DMZ_Check_IP = ["10","254"]

    # DMZ傳入值與Web比對
    if_error = False
    driver.switch_to.window(driver.window_handles[0])
    mod.Switch_Frame(driver)
    ONT_Con_ONT_Mis_DMZ_Con(driver,True)
    for check_time in range(2):
        driver.switch_to.window(driver.window_handles[0])
        mod.Switch_Frame(driver)
        ONT_Con_ONT_Mis_DMZ_IP(driver,ONT_Con_ONT_Mis_DMZ_Request[check_time])
        time.sleep(1)
        ONT_Con_ONT_Mis_DMZ_Apply(driver)
        time.sleep(2)

        driver.switch_to.window(driver.window_handles[1])
        try:  
            driver.refresh()
            time.sleep(2)
            driver.find_element(By.ID, "tab_Network_NAT_DMZ_Tab").click()
            time.sleep(0.5)
            driver.find_element(By.ID, "a_dmz_addr_1")
        except:
            time.sleep(2)
            driver.refresh()
            time.sleep(2)
            username2_ = driver.find_element(By.ID, "username")
            username2_.send_keys(newpage_username)
            password2_ = driver.find_element(By.ID, "userpassword")
            password2_.send_keys(newpage_password)
            driver.find_element(By.ID, "loginBtn").click()
            time.sleep(2)
            mod.Find_by_id_wait_click(driver,"h_menu_list",50)
            mod.Find_by_link_text_wait_click(driver,"Network Setting",50)
            mod.Find_by_xpath_wait_click(driver,"//div[@id='NAT']/span",50)
            mod.Find_by_id_wait_click(driver,"tab_Network_NAT_DMZ_Tab",50)
        time.sleep(2)

        if(driver.find_element(By.ID, "a_dmz_addr_1").get_attribute("value") != "10" or driver.find_element(By.ID, "a_dmz_addr_2").get_attribute("value") != "10" or driver.find_element(By.ID, "a_dmz_addr_3").get_attribute("value") != "10" or driver.find_element(By.ID, "a_dmz_addr_4").get_attribute("value") != ONT_Web_DMZ_Check_IP[check_time]):
            print("ONT DMZ",ONT_Con_ONT_Mis_DMZ_Request[check_time],"Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
            if_error = True

    if(if_error == False):
        print("ONT DMZ Test Pass",file = open("ONT_Status_Test_report.txt", '+a'))

    # Reset DMZ
    driver.switch_to.window(driver.window_handles[0])
    mod.Switch_Frame(driver)
    ONT_Con_ONT_Mis_DMZ_IP(driver,"")
    time.sleep(1)
    ONT_Con_ONT_Mis_DMZ_Con(driver,False)
    ONT_Con_ONT_Mis_DMZ_Apply(driver)

# -------------------------end-------------------------

# ONT Misc ACS Check
# GPON > ONT Config > ONT Misc > ONT ACS Control
# -------------------------start-------------------------

    # ONT Web路徑導向Maintenance > TR069 Client
    driver.switch_to.window(driver.window_handles[1])
    try:
        mod.Find_by_id_wait_click(driver,"h_menu_list",50)
        mod.Find_by_link_text_wait_click(driver,"Maintenance",50)
        mod.Find_by_xpath_wait_click(driver,"//div[@id='TR-069_Client']/span",50)
    except:
        time.sleep(2)
        driver.refresh()
        time.sleep(2)
        username2_ = driver.find_element(By.ID, "username")
        username2_.send_keys(newpage_username)
        password2_ = driver.find_element(By.ID, "userpassword")
        password2_.send_keys(newpage_password)
        driver.find_element(By.ID, "loginBtn").click()
        mod.Find_by_id_wait_click(driver,"h_menu_list",50)
        mod.Find_by_link_text_wait_click(driver,"Maintenance",50)
        mod.Find_by_xpath_wait_click(driver,"//div[@id='TR-069_Client']/span",50)

    # 設定測試值及id
    ONT_Con_ONT_Mis_ACS_Request = ["10","9","@","1000000","1000001"]
    ONT_Web_ACS_Check_Int = ["10","10","10","1000000","1000000"]

    # ACS傳入值與Web比對
    if_error = False
    driver.switch_to.window(driver.window_handles[0])
    mod.Switch_Frame(driver)
    ONT_Con_ONT_Mis_ACS_Con(driver,True)
    ONT_Con_ONT_Mis_ACS_Ser_Ena(driver,True)
    ONT_Con_ONT_Mis_ACS_Username(driver,"1 23456789012345678901234567890123456789username50")
    ONT_Con_ONT_Mis_ACS_Password(driver,"1 23456789012345678901234567890123456789username50")
    ONT_Con_ONT_Mis_ACS_URL(driver,"http://12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123sssssss45678901234567890123456789012.io:10301/")
    ONT_Con_ONT_Mis_ACS_Inf(driver,True)
    ONT_Con_ONT_Mis_ACS_Apply(driver)
    time.sleep(2)

    driver.switch_to.window(driver.window_handles[1])
    try:  
        driver.refresh()
        time.sleep(2)
        driver.find_element(By.ID, "v_69_username")
    except:
        time.sleep(2)
        driver.refresh()
        time.sleep(2)
        username2_ = driver.find_element(By.ID, "username")
        username2_.send_keys(newpage_username)
        password2_ = driver.find_element(By.ID, "userpassword")
        password2_.send_keys(newpage_password)
        driver.find_element(By.ID, "loginBtn").click()
        mod.Find_by_id_wait_click(driver,"h_menu_list",50)
        mod.Find_by_link_text_wait_click(driver,"Maintenance",50)
        mod.Find_by_xpath_wait_click(driver,"//div[@id='TR-069_Client']/span",50)
    time.sleep(2)

    if(driver.find_element(By.ID, "v_69_username").get_attribute("value") != "1 23456789012345678901234567890123456789username50"):
        print("ONT ACS Username Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        if_error = True
    if(driver.find_element(By.ID, "v_69_password").get_attribute("value") != "********"):
        print("ONT ACS Password Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        if_error = True
    if(driver.find_element(By.ID, "v_69_url").get_attribute("value") != "http://12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123sssssss45678901234567890123456789012.io:10301/"):
        print("ONT ACS URL Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        if_error = True
    if(driver.find_element(By.ID, "TR069Client.inform").get_attribute("class") != "switch active "):
        print("ONT ACS Inform Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        if_error = True

    for check_time in range(5):
        driver.switch_to.window(driver.window_handles[0])
        mod.Switch_Frame(driver)
        ONT_Con_ONT_Mis_ACS_Int(driver,ONT_Con_ONT_Mis_ACS_Request[check_time])
        time.sleep(1)
        ONT_Con_ONT_Mis_ACS_Apply(driver)
        time.sleep(2)

        driver.switch_to.window(driver.window_handles[1])
        try:  
            driver.refresh()
            time.sleep(2)
            driver.find_element(By.ID, "v_69_inform_inv")
        except:
            time.sleep(2)
            driver.refresh()
            time.sleep(2)
            username2_ = driver.find_element(By.ID, "username")
            username2_.send_keys(newpage_username)
            password2_ = driver.find_element(By.ID, "userpassword")
            password2_.send_keys(newpage_password)
            driver.find_element(By.ID, "loginBtn").click()
            mod.Find_by_id_wait_click(driver,"h_menu_list",50)
            mod.Find_by_link_text_wait_click(driver,"Maintenance",50)
            mod.Find_by_xpath_wait_click(driver,"//div[@id='TR-069_Client']/span",50)
        time.sleep(2)

        if(driver.find_element(By.ID, "v_69_inform_inv").get_attribute("value") != ONT_Web_ACS_Check_Int[check_time]):
            print("ONT ACS Inform Interval",ONT_Con_ONT_Mis_ACS_Request[check_time],"Test Fail",file = open("ONT_Status_Test_report.txt", '+a'))
            if_error = True

    if(if_error == False):
        print("ONT ACS Test Pass",file = open("ONT_Status_Test_report.txt", '+a'))

    # Reset ACS
    driver.switch_to.window(driver.window_handles[0])
    mod.Switch_Frame(driver)
    ONT_Con_ONT_Mis_ACS_Ser_Ena(driver,False)
    ONT_Con_ONT_Mis_ACS_Inf(driver,False)
    ONT_Con_ONT_Mis_ACS_Int(driver,"86400")
    ONT_Con_ONT_Mis_ACS_Con(driver,False)
    time.sleep(1)
    ONT_Con_ONT_Mis_ACS_Apply(driver)

# -------------------------end-------------------------

    print("Test Finishd",file = open("ONT_Status_Test_report.txt", '+a'))
    print("======================================================================================",file = open("ONT_Status_Test_report.txt", '+a'))

def ONT_Con_ONT_Mis_Serv_Con(driver,request):
    active = driver.find_element(By.ID, "rpOntService_chkControl")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()

def ONT_Con_ONT_Mis_Serv_Def(driver,request):
    active = driver.find_element(By.ID, "rpOntService_chkDefaultPort")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()

def ONT_Con_ONT_Mis_Serv_Lan_Wan(driver,id,request):
    active = driver.find_element(By.ID, id)
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()

def ONT_Con_ONT_Mis_Serv_Port(driver,id,key):
    input = driver.find_element(By.ID, id)
    input.clear()
    input.send_keys(key)

def ONT_Con_ONT_Mis_Serv_FTP_LAN(driver,request):
    active = driver.find_element(By.ID, "rpOntService_chkFtpLAN")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()
            
def ONT_Con_ONT_Mis_Serv_FTP_WAN(driver,request):
    active = driver.find_element(By.ID, "rpOntService_chkFtpWAN")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()

def ONT_Con_ONT_Mis_Serv_FTP_Port(driver,key):
    input = driver.find_element(By.ID, "rpOntService_iptFtpPort")
    input.clear()
    input.send_keys(key)

def ONT_Con_ONT_Mis_Serv_HTTPS_LAN(driver,request):
    active = driver.find_element(By.ID, "rpOntService_chkHttpsLAN")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()
            
def ONT_Con_ONT_Mis_Serv_HTTPS_WAN(driver,request):
    active = driver.find_element(By.ID, "rpOntService_chkHttpsWAN")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()

def ONT_Con_ONT_Mis_Serv_HTTPS_Port(driver,key):
    input = driver.find_element(By.ID, "rpOntService_iptHttpsPort")
    input.clear()
    input.send_keys(key)

def ONT_Con_ONT_Mis_Serv_SNMP_LAN(driver,request):
    active = driver.find_element(By.ID, "rpOntService_chkSnmpLAN")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()
            
def ONT_Con_ONT_Mis_Serv_SNMP_WAN(driver,request):
    active = driver.find_element(By.ID, "rpOntService_chkSnmpWAN")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()

def ONT_Con_ONT_Mis_Serv_SNMP_Port(driver,key):
    input = driver.find_element(By.ID, "rpOntService_iptSnmpPort")
    input.clear()
    input.send_keys(key)

def ONT_Con_ONT_Mis_Serv_SSH_LAN(driver,request):
    active = driver.find_element(By.ID, "rpOntService_chkSshLAN")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()
            
def ONT_Con_ONT_Mis_Serv_SSH_WAN(driver,request):
    active = driver.find_element(By.ID, "rpOntService_chkSshWAN")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()

def ONT_Con_ONT_Mis_Serv_SSH_Port(driver,key):
    input = driver.find_element(By.ID, "rpOntService_iptSshPort")
    input.clear()
    input.send_keys(key)

def ONT_Con_ONT_Mis_Serv_TELNET_LAN(driver,request):
    active = driver.find_element(By.ID, "rpOntService_chkTelnetLAN")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()
            
def ONT_Con_ONT_Mis_Serv_TELNET_WAN(driver,request):
    active = driver.find_element(By.ID, "rpOntService_chkTelnetWAN")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()

def ONT_Con_ONT_Mis_Serv_TELNET_Port(driver,key):
    input = driver.find_element(By.ID, "rpOntService_iptTelnetPort")
    input.clear()
    input.send_keys(key)

def ONT_Con_ONT_Mis_Serv_Apply(driver):
    btn = driver.find_element(By.NAME, "rpOntService_BtnApply")
    btn.click()

        # ONT Config -> ONT Misc -> ONT Firewall Control

def ONT_Con_ONT_Mis_Fire_Con(driver,request):
    active = driver.find_element(By.NAME, "rpOntFirewall_ChkControl")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()

def ONT_Con_ONT_Mis_Fire_Ena_IPv4(driver,request):
    active = driver.find_element(By.ID, "rpOntFirewall_ChkIPv4")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()

def ONT_Con_ONT_Mis_Fire_Ena_IPv6(driver,request):
    active = driver.find_element(By.ID, "rpOntFirewall_ChkIPv6")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()
            
def ONT_Con_ONT_Mis_Fire_Lev(driver,id):
    btn = driver.find_element(By.ID, id)
    btn.click()

def ONT_Con_ONT_Mis_Fire_Lev_Low(driver):
    btn = driver.find_element(By.ID, "rpOntFirewall_RdoLevelLow")
    btn.click()

def ONT_Con_ONT_Mis_Fire_Lev_Med(driver):
    btn = driver.find_element(By.ID, "rpOntFirewall_RdoLevelMed")
    btn.click()

def ONT_Con_ONT_Mis_Fire_Lev_High(driver):
    btn = driver.find_element(By.ID, "rpOntFirewall_RdoLevelHigh")
    btn.click()

def ONT_Con_ONT_Mis_Fire_Apply(driver):
    btn = driver.find_element(By.NAME, "rpOntFirewall_BtnApply")
    btn.click()

        # ONT Config -> ONT Misc -> ONT UPnP Control

def ONT_Con_ONT_Mis_UPnP_Con(driver,request):
    active = driver.find_element(By.NAME, "rpOntUPnP_ChkControl")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()

def ONT_Con_ONT_Mis_UPnP_Enable(driver,request):
    active = driver.find_element(By.ID, "rpOntUPnP_ChkEnable")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()

def ONT_Con_ONT_Mis_UPnP_Apply(driver):
    btn = driver.find_element(By.NAME, "rpOntUPnP_BtnApply")
    btn.click()

        # ONT Config -> ONT Misc -> ONT DMZ Control

def ONT_Con_ONT_Mis_DMZ_Con(driver,request):
    active = driver.find_element(By.NAME, "rpOntDmz_ChkControl")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()

def ONT_Con_ONT_Mis_DMZ_IP(driver,key):
    input = driver.find_element(By.ID, "rpOntDmz_TxtIpAddress")
    input.clear()
    input.send_keys(key)

def ONT_Con_ONT_Mis_DMZ_Apply(driver):
    btn = driver.find_element(By.NAME, "rpOntDmz_BtnApply")
    btn.click()

        # ONT Config -> ONT Misc -> ONT ACS Control

def ONT_Con_ONT_Mis_ACS_Con(driver,request):
    active = driver.find_element(By.NAME, "rpOntAcs_ChkControl")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()

def ONT_Con_ONT_Mis_ACS_Ser_Ena(driver,request):
    active = driver.find_element(By.ID, "rpOntAcs_ChkServer")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()

def ONT_Con_ONT_Mis_ACS_Inf(driver,request):
    active = driver.find_element(By.ID, "rpOntAcs_ChkInform")
    if(active.is_selected() == True):
        if(request == False):
            active.click()
    else:
        if(request == True):
            active.click()

def ONT_Con_ONT_Mis_ACS_Username(driver,key):
    input = driver.find_element(By.ID, "rpOntAcs_TextIptUsername")
    input.clear()
    input.send_keys(key)

def ONT_Con_ONT_Mis_ACS_Password(driver,key):
    input = driver.find_element(By.ID, "rpOntAcs_TextIptPasseord")
    input.clear()
    input.send_keys(key)

def ONT_Con_ONT_Mis_ACS_URL(driver,key):
    input = driver.find_element(By.ID, "rpOntAcs_TextIptUrl")
    input.clear()
    input.send_keys(key)

def ONT_Con_ONT_Mis_ACS_Int(driver,key):
    input = driver.find_element(By.ID, "rpOntAcs_TextIptInterval")
    input.clear()
    input.send_keys(key)

def ONT_Con_ONT_Mis_ACS_Apply(driver):
    btn = driver.find_element(By.NAME, "rpOntAcs_BtnApply")
    btn.click()


# ONT Quick Setup

# 
def ONT_Qui_Port_Select(driver,port):
    select = driver.find_element(By.XPATH, f"//*[@id='lctbl_selPort']/option[{port}]")
    select.click()

def ONT_Qui_Next(driver):
    btn = driver.find_element(By.ID, "btnNextPage")
    btn.click()

def ONT_Qui_Page_Total(driver):
    value = int(driver.find_element(By.ID, "pageTotal").get_attribute("textContent"))
    return value

def ONT_Qui_Check(driver,ont_aid,ont_sn,ont_password,slot,port,aid_num,newpage_username,newpage_password):
    # test_report = open("ONT_Status_Test_report.txt","w+")
    print(f"AID={ont_aid} SN={ont_sn} Password={ont_password}\nTest Start",file = open("ONT_Status_Test_report.txt", '+a'))
    
    # 將網頁中ONT AID的"ont-"移除
    characters = "ont-"
    for i in range(len(characters)):
        ont_aid = ont_aid.replace(characters[i],"")
    
# ONT Quick Setup Check
# GPON > ONT Quick Setup Check > ONT Quick Setup Check
# -------------------------start-------------------------
    
    # 導向路徑ONT Quick Setup
    driver.switch_to.window(driver.window_handles[0])
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"GPON")
    mod.SubPage_Switch(driver,"ONT Quick Setup")
    mod.Switch_Frame(driver)
    retry = True
    while retry:
        try:
            Slot_Select(driver,slot)
            retry = False
        except:
            retry = True
        time.sleep(0.5)
        if(mod.IsAlert(driver)):
            break
        time.sleep(0.5)
    retry = True
    counter = 0
    while retry and counter <= 20:
        try:
            ONT_Qui_Port_Select(driver,port)
            time.sleep(0.5)
            ONT_Qui_ONT_Qui_Load(driver)
            time.sleep(0.5)
            retry = False
        except:
            counter = counter+1
            retry = True

    # 測試ONT Quick Setup中的ont aid、sn、active、password是否符合txt檔
    retry = True
    now_page = 1
    while retry:
        characters = "ont-"
        now_aid = driver.find_elements(By.CLASS_NAME, "rpGponOntSetup_ontAid")[aid_num].get_attribute("textContent")
        for i in range(len(characters)):
            now_aid = now_aid.replace(characters[i],"")
        if(now_aid == ont_aid):
            retry = False
            if(driver.find_elements(By.CLASS_NAME, "rpGponOntSetup_txtSn")[aid_num].get_attribute("value") == ont_sn):
                if(driver.find_elements(By.CLASS_NAME, "rpGponOntSetup_txtPw")[aid_num].get_attribute("value") == ont_password):
                    if(driver.find_elements(By.NAME, "rpGponOntSetup_chkActive")[aid_num].is_selected() == True):
                        print("-ONT Quick Setup- Pass",file = open("ONT_Status_Test_report.txt", '+a'))
                    else:
                        print("-ONT Quick Setup- Active Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                else:
                    print("-ONT Quick Setup- ONT Password Incorrect",file = open("ONT_Status_Test_report.txt", '+a'))
            else:
                print("-ONT Quick Setup- ONT SN Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
        else:
            if(now_page < ONT_Qui_Page_Total(driver)):
                ONT_Qui_Next(driver)
                time.sleep(1)
            else:
                retry = False
                print ("-ONT Quick Setup- ONT AID Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
# -------------------------end-------------------------

# Status Check
# Gpon > ONT Quick Setup Check > Status
# -------------------------start-------------------------

    # 導向路徑Status
    mod.Tab_Switch(driver,"Status")
    retry = True
    while retry:
        try:
            Slot_Select(driver,slot)
            retry = False
        except:
            retry = True
        time.sleep(0.5)
        if(mod.IsAlert(driver)):
            break
        time.sleep(0.5)
    retry = True
    counter = 0
    while retry and counter <= 20:
        try:
            ONT_Qui_Port_Select(driver,port)
            time.sleep(0.5)
            ONT_Qui_Sta_Load(driver)
            time.sleep(0.5)
            retry = False
        except:
            counter = counter+1
            retry = True

    # 測試Status中的ont aid、sn、IS、password是否符合txt檔
    retry = True
    now_page = 1
    while retry:
        row_num = 0
        retry_2 = True
        while retry_2:
            try:
                characters = "ont-"
                now_aid = driver.find_elements(By.CLASS_NAME, "td-table-content.rpGponOntStatus_ontAid")[row_num].get_attribute("textContent")
                for i in range(len(characters)):
                    now_aid = now_aid.replace(characters[i],"")
                if(now_aid == ont_aid):
                    retry = False
                    retry_2 = False
                    if(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_actSn")[row_num].get_attribute("textContent") == ont_sn):
                        if(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_actPw")[row_num].get_attribute("textContent") == "DEFAULT"):
                            if(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_actStatus")[row_num].get_attribute("textContent") == "IS"):
                                print("-Status- Pass",file = open("ONT_Status_Test_report.txt", '+a'))
                            else:
                                print("-Status- IS Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                        else:
                            print("-Status- Password Incorrect",file = open("ONT_Status_Test_report.txt", '+a'))
                    else:
                        print("-Status- ONT SN Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
                else:
                    if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                        row_num = row_num+1
                    else:
                        retry_2 = False
            except:
                if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                    row_num = row_num+1
                else:
                    retry_2 = False
        if(now_page < ONT_Qui_Page_Total(driver)):
            ONT_Qui_Next(driver)
            time.sleep(1)
            now_page = now_page+1
        else:
            retry = False
            print ("-Status- ONT Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
    
# -------------------------end-------------------------

# New Page Check
# Gpon > ONT Quick Setup Check > ONT Quick Setup Check > ONT AID
# -------------------------start-------------------------
    
    # 讀取Status中的version和model name
    ont_version = ""
    if(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_image1")[aid_num].get_attribute("textContent") == "V 1"):
        ont_version = driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_version1")[aid_num].get_attribute("textContent")
    elif(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_image2")[aid_num].get_attribute("textContent") == "V 2"):
        ont_version = driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_version2")[aid_num].get_attribute("textContent")
    ont_model_name = driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_vendor2")[aid_num].get_attribute("textContent")
    
    # 打開ONT新分頁
    mod.Tab_Switch(driver,"ONT Quick Setup")
    while retry:
        try:
            Slot_Select(driver,slot)
            retry = False
        except:
            retry = True
        time.sleep(0.5)
        if(mod.IsAlert(driver)):
            break
        time.sleep(0.5)
    retry = True
    counter = 0
    while retry and counter <= 20:
        try:
            ONT_Qui_Port_Select(driver,port)
            time.sleep(0.5)
            ONT_Qui_ONT_Qui_Load(driver)
            time.sleep(0.5)
            retry = False
        except:
            counter = counter+1
            retry = True
    driver.find_elements(By.ID, "rpGponOntSetup_ontAid")[aid_num].click()

    try:
        # 登入新分頁
        driver.switch_to.window(driver.window_handles[1])
        username2_ = driver.find_element(By.ID, "username")
        username2_.send_keys(newpage_username)
        password2_ = driver.find_element(By.ID, "userpassword")
        password2_.send_keys(newpage_password)
        driver.find_element(By.ID, "loginBtn").click()
        time.sleep(2)
        newpage_ont_model_name = driver.find_element(By.ID, "card_sysinfo_modelname").get_attribute("textContent")
        newpage_ont_version = driver.find_element(By.ID, "card_sysinfo_fwversion").get_attribute("textContent")

         # 去掉version中的".()"
        characters = ".()"
        for i in range(len(characters)):
            newpage_ont_version = newpage_ont_version.replace(characters[i],"")
            
        # 比對version和model name是否與Status中的相同
        if(ont_model_name == newpage_ont_model_name and ont_version == newpage_ont_version):
            print("-Newpage- Pass",file = open("ONT_Status_Test_report.txt", '+a'))
    except:
        print("-Newpage- Fail",file = open("ONT_Status_Test_report.txt", '+a'))
# -------------------------end-------------------------
    print("Test Finished",file = open("ONT_Status_Test_report.txt", '+a'))
    print("======================================================================================",file = open("ONT_Status_Test_report.txt", '+a'))
    # test_report.close()

def OLT_Qui_Reg_Loop(driver,ont_aid,ont_sn,ont_password,slot,port,loop,ont_sn_1_1,url,username,password):
    # test_report = open("ONT_Status_Test_report.txt","w+")
    print(f"{ont_aid} ONT Register Loop\nTest Start",file = open("ONT_Status_Test_report.txt", '+a'))
    for times in range(loop):
        try:
            print("---",times+1,"--- Test",file = open("ONT_Status_Test_report.txt", '+a'))

# OLT Register
# GPON > ONT Quick Setup Check > Unregistered
# -------------------------start-------------------------
    
            # 導向路徑Unregistered
            driver.switch_to.window(driver.window_handles[0])
            mod.Switch_Default(driver)
            mod.Page_Switch(driver,"GPON")
            mod.SubPage_Switch(driver,"ONT Quick Setup")
            mod.Switch_Frame(driver)
            time.sleep(1)
            mod.Tab_Switch(driver,"Unregistered")
            retry = True
            counter = 0
            while retry and counter <= 25:
                try:
                    Slot_Select(driver,slot)
                    retry = False
                except:
                    counter = counter+1
                    retry = True
                time.sleep(0.5)
                if(mod.IsAlert(driver)):
                    break
                if(counter == 26):
                    driver.find_element(By.ID, "dontexist")
                time.sleep(0.5)
            retry = True
            counter = 0
            while retry and counter <= 20:
                try:
                    ONT_Qui_Port_Select(driver,port)
                    time.sleep(0.5)
                    ONT_Qui_Unr_Load(driver)
                    time.sleep(1)
                    ONT_Qui_Unr_Load(driver)
                    time.sleep(0.5)
                    retry = False
                except:
                    counter = counter+1
                    retry = True
                if(counter == 21):
                    driver.find_element(By.ID, "dontexist")

            # 尋找sn與pw符合的OLT
            retry = True
            if ONT_Qui_Sta_SN_Num(driver) == 0:
                retry = False
                print("-Unregister- SN Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
            now_page = 1
            while retry:
                row_num = 0
                retry_2 = True
                while retry_2:
                    if (driver.find_elements(By.CLASS_NAME, "rpGponOntUnreg_sn")[row_num].get_attribute("value") == ont_sn):
                        retry = False
                        retry_2 = False
                        if (driver.find_elements(By.CLASS_NAME, "rpGponOntUnreg_pw")[row_num].get_attribute("value") == ont_password):
                            Select(driver.find_elements(By.CLASS_NAME, "rpGponOntUnreg_sltPortTemp")[row_num]).select_by_visible_text(f"pon-{slot}-{port}")
                            Select(driver.find_elements(By.CLASS_NAME, "rpGponOntUnreg_sltOntTemp")[row_num]).select_by_visible_text(f"Template-{slot}-{port}-128")
                            ONT_Qui_Unr_Reg(driver,row_num,True)
                            ONT_Qui_Unr_Apply(driver)
                        else:
                            print("-Unregister- Password Incorrect",file = open("ONT_Status_Test_report.txt", '+a'))
                    elif (retry_2 and row_num < ONT_Qui_Sta_SN_Num(driver)-1):
                        row_num = row_num+1
                    else:
                        retry_2 = False
                if(retry and now_page < ONT_Qui_Page_Total(driver)):
                    ONT_Qui_Next(driver)
                    time.sleep(1)
                    now_page = now_page+1
                elif(retry):
                    print("-Unregister- SN Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
                    retry = False
            time.sleep(15)
# -------------------------end-------------------------

# Status value Check
# Gpon > ONT Quick Setup Check > Status
# -------------------------start-------------------------

            # 導向路徑Status
            mod.Tab_Switch(driver,"Status")
            retry = True
            counter = 0
            while retry and counter <= 25:
                try:
                    Slot_Select(driver,slot)
                    retry = False
                except:
                    counter = counter+1
                    retry = True
                time.sleep(0.5)
                if(mod.IsAlert(driver)):
                    break
                if(counter == 26):
                    driver.find_element(By.ID, "dontexist")
                time.sleep(0.5)
            retry = True
            counter = 0
            while retry and counter <= 20:
                try:
                    ONT_Qui_Port_Select(driver,port)
                    time.sleep(0.5)
                    ONT_Qui_Sta_Load(driver)
                    time.sleep(1)
                    ONT_Qui_Sta_Load(driver)
                    time.sleep(0.5)
                    retry = False
                except:
                    counter = counter+1
                    retry = True
                if(counter == 21):
                    driver.find_element(By.ID, "dontexist")

            # 測試Status中的sn、IS、password是否符合txt檔
            retry = True
            now_page = 1
            while retry:
                row_num = 0
                retry_2 = True
                while retry_2:
                    try:   
                        if(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_actSn")[row_num].get_attribute("textContent") == ont_sn):
                            retry = False
                            retry_2 = False
                            if(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_actPw")[row_num].get_attribute("textContent") == "DEFAULT"):
                                if(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_actStatus")[row_num].get_attribute("textContent") == "IS"):
                                    print("-Status- Pass",file = open("ONT_Status_Test_report.txt", '+a'))
                                else:
                                    print("-Status- IS Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                            else:
                                print("-Status- Password Incorrect",file = open("ONT_Status_Test_report.txt", '+a'))
                        else:
                            if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                                row_num = row_num+1
                            else:
                                retry_2 = False
                    except:
                        if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                            row_num = row_num+1
                        else:
                            retry_2 = False
                if(retry and now_page < ONT_Qui_Page_Total(driver)):
                    ONT_Qui_Next(driver)
                    time.sleep(1)
                    now_page = now_page+1
                elif(retry):
                    retry = False
                    print ("-Status- ONT Not Found",file = open("ONT_Status_Test_report.txt", '+a'))

            # 測試Status中的 sn = ont 1-1 Status是否為IS
            retry = True
            now_page = 1
            while retry:
                row_num = 0
                retry_2 = True
                while retry_2:
                    try:   
                        if(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_actSn")[row_num].get_attribute("textContent") == ont_sn_1_1):
                            retry = False
                            retry_2 = False
                            if(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_actStatus")[row_num].get_attribute("textContent") == "IS"):
                                print("-Status ONT 1-1- Pass",file = open("ONT_Status_Test_report.txt", '+a'))
                            else:
                                print("-Status ONT 1-1- IS Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                        else:
                            if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                                row_num = row_num+1
                            else:
                                retry_2 = False
                    except:
                        if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                            row_num = row_num+1
                        else:
                            retry_2 = False
                if(retry and now_page < ONT_Qui_Page_Total(driver)):
                    ONT_Qui_Next(driver)
                    time.sleep(1)
                    now_page = now_page+1
                elif(retry):
                    retry = False
                    print ("-Status ONT 1-1- SN Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
# -------------------------end-------------------------

# ONT Quick Setup Value Check
# GPON > ONT Quick Setup Check > ONT Quick Setup Check
# -------------------------start-------------------------
    
            # 導向路徑ONT Quick Setup
            mod.Switch_Default(driver)
            mod.SubPage_Switch(driver,"ONT Quick Setup")
            mod.Switch_Frame(driver)
            retry = True
            counter = 0
            while retry and counter <= 25:
                try:
                    Slot_Select(driver,slot)
                    retry = False
                except:
                    retry = True
                time.sleep(0.5)
                if(mod.IsAlert(driver)):
                    break
                if(counter == 26):
                    driver.find_element(By.ID, "dontexist")
                time.sleep(0.5)
            retry = True
            counter = 0
            while retry and counter <= 20:
                try:
                    ONT_Qui_Port_Select(driver,port)
                    time.sleep(0.5)
                    ONT_Qui_ONT_Qui_Load(driver)
                    time.sleep(0.5)
                    retry = False
                except:
                    counter = counter+1
                    retry = True
                if(counter == 21):
                    driver.find_element(By.ID, "dontexist")

            # 測試ONT Quick Setup中的sn、active、password是否符合txt檔
            retry = True
            now_page = 1
            while retry:
                row_num = 0
                retry_2 = True
                while retry_2:
                    try:
                        if(driver.find_elements(By.CLASS_NAME, "rpGponOntSetup_txtSn")[row_num].get_attribute("value") == ont_sn):
                            retry = False
                            retry_2 = False
                            if(driver.find_elements(By.CLASS_NAME, "rpGponOntSetup_txtPw")[row_num].get_attribute("value") == ont_password):
                                if(driver.find_elements(By.NAME, "rpGponOntSetup_chkActive")[row_num].is_selected() == True):
                                    print("-ONT Quick Setup- Pass",file = open("ONT_Status_Test_report.txt", '+a'))
                                    Select(driver.find_elements(By.CLASS_NAME, "rpGponOntSetup_sltAction")[row_num]).select_by_visible_text("Delete")
                                    ONT_Qui_ONT_Qui_Apply(driver)
                                else:
                                    print("-ONT Quick Setup- Active Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                            else:
                                print("-ONT Quick Setup- ONT Password Incorrect",file = open("ONT_Status_Test_report.txt", '+a'))
                        else:
                            if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                                row_num = row_num+1
                            else:
                                retry_2 = False
                    except:
                        if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                            row_num = row_num+1
                        else:
                            retry_2 = False
                if(retry and now_page < ONT_Qui_Page_Total(driver)):
                    ONT_Qui_Next(driver)
                    time.sleep(1)
                    now_page = now_page+1
                elif(retry):
                    retry = False
                    print ("-ONT Quick Setup- ONT Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
# -------------------------end-------------------------
        except:
            time.sleep(5)
            from selenium import webdriver
            driver = webdriver.Chrome()
            driver.get(url) # 連上網頁
            mod.Login(driver,username,password) # 登入
            time.sleep(1)
            print("-----Open New Page-----",file = open("ONT_Status_Test_report.txt", '+a'))
        time.sleep(2)
    print("Test Finished",file = open("ONT_Status_Test_report.txt", '+a'))
    print("======================================================================================",file = open("ONT_Status_Test_report.txt", '+a'))

def OLT_Qui_Reg_Method_Check(driver,ont_aid,ont_sn,ont_password,slot,port,ont_sn_1_1,url,username,password):
    # test_report = open("ONT_Status_Test_report.txt","w+")
    print(f"{ont_aid} ONT Register Method Check\nTest Start",file = open("ONT_Status_Test_report.txt", '+a'))

# ONT Quick Setup 刪除ONT
# GPON > ONT Quick Setup > ONT Quick Setup
# -------------------------start-------------------------

    # 導向路徑ONT Quick Setup
    driver.switch_to.window(driver.window_handles[0])
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"GPON")
    mod.SubPage_Switch(driver,"ONT Quick Setup")
    mod.Switch_Frame(driver)
    retry = True
    counter = 0
    while retry and counter <= 25:
        try:
            Slot_Select(driver,slot)
            retry = False
        except:
            retry = True
        time.sleep(0.5)
        if(mod.IsAlert(driver)):
            break
        if(counter == 26):
            driver.find_element(By.ID, "dontexist")
        time.sleep(0.5)
    retry = True
    counter = 0
    while retry and counter <= 20:
        try:
            ONT_Qui_Port_Select(driver,port)
            time.sleep(0.5)
            ONT_Qui_ONT_Qui_Load(driver)
            time.sleep(0.5)
            retry = False
        except:
            counter = counter+1
            retry = True
        if(counter == 21):
            driver.find_element(By.ID, "dontexist")

    # 用sn尋找ONT並刪除
    retry = True
    now_page = 1
    while retry:
        row_num = 0
        retry_2 = True
        while retry_2:
            try:
                if(driver.find_elements(By.CLASS_NAME, "rpGponOntSetup_txtSn")[row_num].get_attribute("value") == ont_sn):
                    retry = False
                    retry_2 = False
                    Select(driver.find_elements(By.CLASS_NAME, "rpGponOntSetup_sltAction")[row_num]).select_by_visible_text("Delete")
                    print("-ONT1-2 Delete- Success",file = open("ONT_Status_Test_report.txt", '+a'))
                    ONT_Qui_ONT_Qui_Apply(driver)
                else:
                    if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                        row_num = row_num+1
                    else:
                        retry_2 = False
            except:
                if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                    row_num = row_num+1
                else:
                    retry_2 = False
        if(retry and now_page < ONT_Qui_Page_Total(driver)):
            ONT_Qui_Next(driver)
            time.sleep(1)
            now_page = now_page+1
        elif(retry):
            retry = False
            print ("-ONT1-2 Delete- SN Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
# -------------------------end-------------------------

# OLT Registration 設為A
# GPON > OLT Registration
# -------------------------start-------------------------

    # 導向路徑OLT Registration
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"OLT Registration")
    mod.Switch_Frame(driver)
    retry = True
    counter = 0
    while retry and counter <= 25:
        try:
            Slot_Select(driver,slot)
            time.sleep(0.5)
            OLT_Reg_OLT_Reg_Load(driver)
            retry = False
        except:
            retry = True
        time.sleep(0.5)
        if(mod.IsAlert(driver)):
            break
        if(counter == 26):
            driver.find_element(By.ID, "dontexist")
        time.sleep(0.5)
    driver.find_elements(By.XPATH, f"//*[@id='rpGponPortReg_sltReg']/option[1]")[int(port)-1].click()
    OLT_Reg_OLT_Reg_Apply(driver)
    print ("-OLT Reg A- Success",file = open("ONT_Status_Test_report.txt", '+a'))

# -------------------------end-------------------------

# OLT Register 註冊ONT
# GPON > ONT Quick Setup > Unregistered
# -------------------------start-------------------------

    # 導向路徑Unregistered
    mod.Switch_Default(driver)
    # mod.Page_Switch(driver,"GPON")
    mod.SubPage_Switch(driver,"ONT Quick Setup")
    mod.Switch_Frame(driver)
    time.sleep(1)
    mod.Tab_Switch(driver,"Unregistered")
    retry = True
    counter = 0
    while retry and counter <= 25:
        try:
            Slot_Select(driver,slot)
            retry = False
        except:
            counter = counter+1
            retry = True
        time.sleep(0.5)
        if(mod.IsAlert(driver)):
            break
        if(counter == 26):
            driver.find_element(By.ID, "dontexist")
        time.sleep(0.5)
    retry = True
    counter = 0
    while retry and counter <= 20:
        try:
            time.sleep(10)
            ONT_Qui_Port_Select(driver,port)
            time.sleep(0.5)
            ONT_Qui_Unr_Load(driver)
            time.sleep(1)
            ONT_Qui_Unr_Load(driver)
            time.sleep(0.5)
            retry = False
        except:
            counter = counter+1
            retry = True
        if(counter == 21):
            driver.find_element(By.ID, "dontexist")

    # 尋找sn與pw符合的OLT
    retry = True
    if ONT_Qui_Sta_SN_Num(driver) == 0:
        retry = False
        print("-ONT Register- SN Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
    now_page = 1
    while retry:
        row_num = 0
        retry_2 = True
        while retry_2:
            if (driver.find_elements(By.CLASS_NAME, "rpGponOntUnreg_sn")[row_num].get_attribute("value") == ont_sn):
                retry = False
                retry_2 = False
                Select(driver.find_elements(By.CLASS_NAME, "rpGponOntUnreg_sltPortTemp")[row_num]).select_by_visible_text(f"pon-{slot}-{port}")
                Select(driver.find_elements(By.CLASS_NAME, "rpGponOntUnreg_sltOntTemp")[row_num]).select_by_visible_text(f"Template-{slot}-{port}-128")
                ONT_Qui_Unr_Reg(driver,row_num,True)
                ONT_Qui_Unr_Apply(driver)
                print("-ONT Register- Success",file = open("ONT_Status_Test_report.txt", '+a'))
            elif (retry_2 and row_num < ONT_Qui_Sta_SN_Num(driver)-1):
                row_num = row_num+1
            else:
                retry_2 = False
        if(retry and now_page < ONT_Qui_Page_Total(driver)):
            ONT_Qui_Next(driver)
            time.sleep(1)
            now_page = now_page+1
        elif(retry):
            print("-ONT Register- SN Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
            retry = False
# -------------------------end-------------------------

# Status value Check 確認ont1-2和1-1的IS
# Gpon > ONT Quick Setup > Status
# -------------------------start-------------------------

    # 導向路徑Status
    time.sleep(60)
    mod.Tab_Switch(driver,"Status")
    retry = True
    counter = 0
    while retry and counter <= 25:
        try:
            Slot_Select(driver,slot)
            retry = False
        except:
            counter = counter+1
            retry = True
        time.sleep(0.5)
        if(mod.IsAlert(driver)):
            break
        if(counter == 26):
            driver.find_element(By.ID, "dontexist")
        time.sleep(0.5)
    retry = True
    counter = 0
    while retry and counter <= 20:
        try:
            ONT_Qui_Port_Select(driver,port)
            time.sleep(0.5)
            ONT_Qui_Sta_Load(driver)
            time.sleep(1)
            ONT_Qui_Sta_Load(driver)
            time.sleep(0.5)
            retry = False
        except:
            counter = counter+1
            retry = True
        if(counter == 21):
            driver.find_element(By.ID, "dontexist")

    # 測試Status中的sn、IS、password是否符合txt檔
    retry = True
    now_page = 1
    while retry:
        row_num = 0
        retry_2 = True
        while retry_2:
            try:   
                if(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_actSn")[row_num].get_attribute("textContent") == ont_sn):
                    retry = False
                    retry_2 = False
                    if(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_actStatus")[row_num].get_attribute("textContent") == "IS"):
                        print("-ONT 1-2 Check- Pass",file = open("ONT_Status_Test_report.txt", '+a'))
                    else:
                        print("-ONT 1-2 Check- IS Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                else:
                    if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                        row_num = row_num+1
                    else:
                        retry_2 = False
            except:
                if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                    row_num = row_num+1
                else:
                    retry_2 = False
        if(retry and now_page < ONT_Qui_Page_Total(driver)):
            ONT_Qui_Next(driver)
            time.sleep(1)
            now_page = now_page+1
        elif(retry):
            retry = False
            print ("-ONT 1-2 Check- SN Not Found",file = open("ONT_Status_Test_report.txt", '+a'))

    # 測試Status中的 sn = ont 1-1 Status是否為IS
    retry = True
    now_page = 1
    while retry:
        row_num = 0
        retry_2 = True
        while retry_2:
            try:   
                if(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_actSn")[row_num].get_attribute("textContent") == ont_sn_1_1):
                    retry = False
                    retry_2 = False
                    if(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_actStatus")[row_num].get_attribute("textContent") == "IS"):
                        print("-ONT 1-1 Check- Pass",file = open("ONT_Status_Test_report.txt", '+a'))
                    else:
                        print("-ONT 1-1 Check- IS Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                else:
                    if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                        row_num = row_num+1
                    else:
                        retry_2 = False
            except:
                if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                    row_num = row_num+1
                else:
                    retry_2 = False
        if(retry and now_page < ONT_Qui_Page_Total(driver)):
            ONT_Qui_Next(driver)
            time.sleep(1)
            now_page = now_page+1
        elif(retry):
            retry = False
            print ("-ONT 1-1 Check- SN Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
# -------------------------end-------------------------

# OLT Registration 設為C
# GPON > OLT Registration
# -------------------------start-------------------------

    # 導向路徑OLT Registration
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"OLT Registration")
    mod.Switch_Frame(driver)
    retry = True
    counter = 0
    while retry and counter <= 25:
        try:
            Slot_Select(driver,slot)
            time.sleep(0.5)
            OLT_Reg_OLT_Reg_Load(driver)
            retry = False
        except:
            retry = True
        time.sleep(0.5)
        if(mod.IsAlert(driver)):
            break
        if(counter == 26):
            driver.find_element(By.ID, "dontexist")
        time.sleep(0.5)
    driver.find_elements(By.XPATH, f"//*[@id='rpGponPortReg_sltReg']/option[2]")[int(port)-1].click()
    OLT_Reg_OLT_Reg_Apply(driver)
    print ("-OLT Reg C- Success",file = open("ONT_Status_Test_report.txt", '+a'))

# -------------------------end-------------------------

# ONT Quick Setup 刪除ONT
# GPON > ONT Quick Setup > ONT Quick Setup
# -------------------------start-------------------------

    # 導向路徑ONT Quick Setup
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"ONT Quick Setup")
    mod.Switch_Frame(driver)
    retry = True
    counter = 0
    while retry and counter <= 25:
        try:
            Slot_Select(driver,slot)
            retry = False
        except:
            retry = True
        time.sleep(0.5)
        if(mod.IsAlert(driver)):
            break
        if(counter == 26):
            driver.find_element(By.ID, "dontexist")
        time.sleep(0.5)
    retry = True
    counter = 0
    while retry and counter <= 20:
        try:
            ONT_Qui_Port_Select(driver,port)
            time.sleep(0.5)
            ONT_Qui_ONT_Qui_Load(driver)
            time.sleep(0.5)
            retry = False
        except:
            counter = counter+1
            retry = True
        if(counter == 21):
            driver.find_element(By.ID, "dontexist")

    # 用sn尋找ONT並刪除
    retry = True
    now_page = 1
    while retry:
        row_num = 0
        retry_2 = True
        while retry_2:
            try:
                if(driver.find_elements(By.CLASS_NAME, "rpGponOntSetup_txtSn")[row_num].get_attribute("value") == ont_sn):
                    retry = False
                    retry_2 = False
                    Select(driver.find_elements(By.CLASS_NAME, "rpGponOntSetup_sltAction")[row_num]).select_by_visible_text("Delete")
                    print("-ONT1-2 Delete- Success",file = open("ONT_Status_Test_report.txt", '+a'))
                    ONT_Qui_ONT_Qui_Apply(driver)
                else:
                    if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                        row_num = row_num+1
                    else:
                        retry_2 = False
            except:
                if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                    row_num = row_num+1
                else:
                    retry_2 = False
        if(retry and now_page < ONT_Qui_Page_Total(driver)):
            ONT_Qui_Next(driver)
            time.sleep(1)
            now_page = now_page+1
        elif(retry):
            retry = False
            print ("-ONT1-2 Delete- SN Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
# -------------------------end-------------------------
    
# ONT Quick Setup 17-16-123 Config ONT1-2 的 SN
# GPON > ONT Quick Setup
# -------------------------start-------------------------
 
    # 導向路徑ONT Quick Setup
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"ONT Quick Setup")
    mod.Switch_Frame(driver)

    # Load Slot & Pon
    retry = True
    counter = 0
    while retry and counter <= 25:
        try:
            Slot_Select(driver,slot)
            retry = False
        except:
            retry = True
        time.sleep(0.5)
        if(mod.IsAlert(driver)):
            break
        if(counter == 26):
            driver.find_element(By.ID, "dontexist")
        time.sleep(0.5)
    retry = True
    counter = 0
    while retry and counter <= 20:
        try:
            ONT_Qui_Port_Select(driver,port)
            time.sleep(0.5)
            ONT_Qui_ONT_Qui_Load(driver)
            time.sleep(0.5)
            retry = False
        except:
            counter = counter+1
            retry = True
        if(counter == 21):
            driver.find_element(By.ID, "dontexist")

    ONT_Qui_Next(driver)
    time.sleep(1)
    ONT_Qui_Next(driver)
    time.sleep(1)
    ONT_Qui_Next(driver)
    time.sleep(1)
    ONT_Qui_ONT_Qui_Active(driver,27,True)
    ONT_Qui_ONT_Qui_SN_Input(driver,27,ont_sn)
    Select(driver.find_elements(By.CLASS_NAME, "rpGponOntSetup_sltPort")[26]).select_by_visible_text(f"pon-{slot}-{port}")
    Select(driver.find_elements(By.CLASS_NAME, "rpGponOntSetup_sltOntTemp")[26]).select_by_visible_text(f"Template-{slot}-{port}-128")
    Select(driver.find_elements(By.CLASS_NAME, "rpGponOntSetup_sltAction")[26]).select_by_visible_text("Add")
    ONT_Qui_ONT_Qui_Apply(driver)
    print ("-ONT1-2 SN Config 17-16-123- Success",file = open("ONT_Status_Test_report.txt", '+a'))

# -------------------------end-------------------------

# Status value Check 17-16-123 確認ont1-2和1-1的IS
# Gpon > ONT Quick Setup > Status
# -------------------------start-------------------------

    # 導向路徑Status
    time.sleep(20)
    mod.Tab_Switch(driver,"Status")
    retry = True
    counter = 0
    while retry and counter <= 25:
        try:
            Slot_Select(driver,slot)
            retry = False
        except:
            counter = counter+1
            retry = True
        time.sleep(0.5)
        if(mod.IsAlert(driver)):
            break
        if(counter == 26):
            driver.find_element(By.ID, "dontexist")
        time.sleep(0.5)
    retry = True
    counter = 0
    while retry and counter <= 20:
        try:
            ONT_Qui_Port_Select(driver,port)
            time.sleep(0.5)
            ONT_Qui_Sta_Load(driver)
            time.sleep(1)
            ONT_Qui_Sta_Load(driver)
            time.sleep(0.5)
            retry = False
        except:
            counter = counter+1
            retry = True
        if(counter == 21):
            driver.find_element(By.ID, "dontexist")

    # 測試Status中的sn、IS、password是否符合txt檔
    retry = True
    now_page = 1
    while retry:
        row_num = 0
        retry_2 = True
        while retry_2:
            try:
                if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpGponOntStatus_ontAid")[row_num].get_attribute("textContent") == "ont-17-16-123"):
                    retry = False
                    retry_2 = False
                    if(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_actSn")[row_num].get_attribute("textContent") == ont_sn):
                        if(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_actStatus")[row_num].get_attribute("textContent") == "IS"):
                            print("-ONT 1-2 Check- Pass",file = open("ONT_Status_Test_report.txt", '+a'))
                        else:
                            print("-ONT 1-2 Check- IS Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                    else:
                        print("-ONT 1-2 Check- SN Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
                else:
                    if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                        row_num = row_num+1
                    else:
                        retry_2 = False
            except:
                if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                    row_num = row_num+1
                else:
                    retry_2 = False
        if(retry and now_page < ONT_Qui_Page_Total(driver)):
            ONT_Qui_Next(driver)
            time.sleep(1)
            now_page = now_page+1
        elif(retry):
            retry = False
            print ("-ONT 1-2 Check- AID Not Found",file = open("ONT_Status_Test_report.txt", '+a'))

    # 測試Status中的 sn = ont 1-1 Status是否為IS
    retry = True
    now_page = 1
    while retry:
        row_num = 0
        retry_2 = True
        while retry_2:
            try:   
                if(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_actSn")[row_num].get_attribute("textContent") == ont_sn_1_1):
                    retry = False
                    retry_2 = False
                    if(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_actStatus")[row_num].get_attribute("textContent") == "IS"):
                        print("-ONT 1-1 Check- Pass",file = open("ONT_Status_Test_report.txt", '+a'))
                    else:
                        print("-ONT 1-1 Check- IS Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                else:
                    if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                        row_num = row_num+1
                    else:
                        retry_2 = False
            except:
                if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                    row_num = row_num+1
                else:
                    retry_2 = False
        if(retry and now_page < ONT_Qui_Page_Total(driver)):
            ONT_Qui_Next(driver)
            time.sleep(1)
            now_page = now_page+1
        elif(retry):
            retry = False
            print ("-ONT 1-1 Check- SN Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
# -------------------------end-------------------------

# ONT Quick Setup 刪除ONT
# GPON > ONT Quick Setup > ONT Quick Setup
# -------------------------start-------------------------

    # 導向路徑ONT Quick Setup
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"ONT Quick Setup")
    mod.Switch_Frame(driver)
    retry = True
    counter = 0
    while retry and counter <= 25:
        try:
            Slot_Select(driver,slot)
            retry = False
        except:
            retry = True
        time.sleep(0.5)
        if(mod.IsAlert(driver)):
            break
        if(counter == 26):
            driver.find_element(By.ID, "dontexist")
        time.sleep(0.5)
    retry = True
    counter = 0
    while retry and counter <= 20:
        try:
            ONT_Qui_Port_Select(driver,port)
            time.sleep(0.5)
            ONT_Qui_ONT_Qui_Load(driver)
            time.sleep(0.5)
            retry = False
        except:
            counter = counter+1
            retry = True
        if(counter == 21):
            driver.find_element(By.ID, "dontexist")

    # 用sn尋找ONT並刪除
    retry = True
    now_page = 1
    while retry:
        row_num = 0
        retry_2 = True
        while retry_2:
            try:
                if(driver.find_elements(By.CLASS_NAME, "rpGponOntSetup_txtSn")[row_num].get_attribute("value") == ont_sn):
                    retry = False
                    retry_2 = False
                    Select(driver.find_elements(By.CLASS_NAME, "rpGponOntSetup_sltAction")[row_num]).select_by_visible_text("Delete")
                    print("-ONT1-2 Delete- Success",file = open("ONT_Status_Test_report.txt", '+a'))
                    ONT_Qui_ONT_Qui_Apply(driver)
                else:
                    if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                        row_num = row_num+1
                    else:
                        retry_2 = False
            except:
                if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                    row_num = row_num+1
                else:
                    retry_2 = False
        if(retry and now_page < ONT_Qui_Page_Total(driver)):
            ONT_Qui_Next(driver)
            time.sleep(1)
            now_page = now_page+1
        elif(retry):
            retry = False
            print ("-ONT1-2 Delete- SN Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
# -------------------------end-------------------------
    
# ONT Quick Setup 17-16-122 Config ONT1-2 的 Password
# GPON > ONT Quick Setup
# -------------------------start-------------------------
 
    # 導向路徑ONT Quick Setup
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"ONT Quick Setup")
    mod.Switch_Frame(driver)

    # Load Slot & Pon
    retry = True
    counter = 0
    while retry and counter <= 25:
        try:
            Slot_Select(driver,slot)
            retry = False
        except:
            retry = True
        time.sleep(0.5)
        if(mod.IsAlert(driver)):
            break
        if(counter == 26):
            driver.find_element(By.ID, "dontexist")
        time.sleep(0.5)
    retry = True
    counter = 0
    while retry and counter <= 20:
        try:
            ONT_Qui_Port_Select(driver,port)
            time.sleep(0.5)
            ONT_Qui_ONT_Qui_Load(driver)
            time.sleep(0.5)
            retry = False
        except:
            counter = counter+1
            retry = True
        if(counter == 21):
            driver.find_element(By.ID, "dontexist")

    ONT_Qui_Next(driver)
    time.sleep(1)
    ONT_Qui_Next(driver)
    time.sleep(1)
    ONT_Qui_Next(driver)
    time.sleep(1)
    ONT_Qui_ONT_Qui_Active(driver,26,True)
    ONT_Qui_ONT_Qui_PW_Input(driver,26,ont_password)
    Select(driver.find_elements(By.CLASS_NAME, "rpGponOntSetup_sltPort")[25]).select_by_visible_text(f"pon-{slot}-{port}")
    Select(driver.find_elements(By.CLASS_NAME, "rpGponOntSetup_sltOntTemp")[25]).select_by_visible_text(f"Template-{slot}-{port}-128")
    Select(driver.find_elements(By.CLASS_NAME, "rpGponOntSetup_sltAction")[25]).select_by_visible_text("Add")
    ONT_Qui_ONT_Qui_Apply(driver)
    print ("-ONT1-2 PW Config 17-16-122- Success",file = open("ONT_Status_Test_report.txt", '+a'))

# -------------------------end-------------------------

# Status value Check 17-16-122 確認 ont1-2和1-1的IS
# Gpon > ONT Quick Setup > Status
# -------------------------start-------------------------

    # 導向路徑Status
    time.sleep(30)
    mod.Tab_Switch(driver,"Status")
    retry = True
    counter = 0
    while retry and counter <= 25:
        try:
            Slot_Select(driver,slot)
            retry = False
        except:
            counter = counter+1
            retry = True
        time.sleep(0.5)
        if(mod.IsAlert(driver)):
            break
        if(counter == 26):
            driver.find_element(By.ID, "dontexist")
        time.sleep(0.5)
    retry = True
    counter = 0
    while retry and counter <= 20:
        try:
            ONT_Qui_Port_Select(driver,port)
            time.sleep(0.5)
            ONT_Qui_Sta_Load(driver)
            time.sleep(1)
            ONT_Qui_Sta_Load(driver)
            time.sleep(0.5)
            retry = False
        except:
            counter = counter+1
            retry = True
        if(counter == 21):
            driver.find_element(By.ID, "dontexist")

    # 測試Status中的sn、IS、password是否符合txt檔
    retry = True
    now_page = 1
    while retry:
        row_num = 0
        retry_2 = True
        while retry_2:
            try:
                if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpGponOntStatus_ontAid")[row_num].get_attribute("textContent") == "ont-17-16-122"):
                    retry = False
                    retry_2 = False
                    if(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_actPw")[row_num].get_attribute("textContent") == ont_password):
                        if(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_actStatus")[row_num].get_attribute("textContent") == "IS"):
                            print("-ONT 1-2 Check- Pass",file = open("ONT_Status_Test_report.txt", '+a'))
                        else:
                            print("-ONT 1-2 Check- IS Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                    else:
                        print("-ONT 1-2 Check- PW Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
                else:
                    if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                        row_num = row_num+1
                    else:
                        retry_2 = False
            except:
                if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                    row_num = row_num+1
                else:
                    retry_2 = False
        if(retry and now_page < ONT_Qui_Page_Total(driver)):
            ONT_Qui_Next(driver)
            time.sleep(1)
            now_page = now_page+1
        elif(retry):
            retry = False
            print ("-ONT 1-2 Check- AID Not Found",file = open("ONT_Status_Test_report.txt", '+a'))

    # 測試Status中的 sn = ont 1-1 Status是否為IS
    retry = True
    now_page = 1
    while retry:
        row_num = 0
        retry_2 = True
        while retry_2:
            try:   
                if(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_actSn")[row_num].get_attribute("textContent") == ont_sn_1_1):
                    retry = False
                    retry_2 = False
                    if(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_actStatus")[row_num].get_attribute("textContent") == "IS"):
                        print("-ONT 1-1 Check- Pass",file = open("ONT_Status_Test_report.txt", '+a'))
                    else:
                        print("-ONT 1-1 Check- IS Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                else:
                    if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                        row_num = row_num+1
                    else:
                        retry_2 = False
            except:
                if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                    row_num = row_num+1
                else:
                    retry_2 = False
        if(retry and now_page < ONT_Qui_Page_Total(driver)):
            ONT_Qui_Next(driver)
            time.sleep(1)
            now_page = now_page+1
        elif(retry):
            retry = False
            print ("-ONT 1-1 Check- SN Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
# -------------------------end-------------------------

# OLT Registration 設為C-autolock
# GPON > OLT Registration
# -------------------------start-------------------------

    # 導向路徑OLT Registration
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"OLT Registration")
    mod.Switch_Frame(driver)
    retry = True
    counter = 0
    while retry and counter <= 25:
        try:
            Slot_Select(driver,slot)
            time.sleep(0.5)
            OLT_Reg_OLT_Reg_Load(driver)
            retry = False
        except:
            retry = True
        time.sleep(0.5)
        if(mod.IsAlert(driver)):
            break
        if(counter == 26):
            driver.find_element(By.ID, "dontexist")
        time.sleep(0.5)
    driver.find_elements(By.XPATH, f"//*[@id='rpGponPortReg_sltReg']/option[3]")[int(port)-1].click()
    OLT_Reg_OLT_Reg_Apply(driver)
    print ("-OLT Reg C-autolock- Success",file = open("ONT_Status_Test_report.txt", '+a'))

# -------------------------end-------------------------

# ONT Quick Setup 刪除ONT
# GPON > ONT Quick Setup > ONT Quick Setup
# -------------------------start-------------------------

    # 導向路徑ONT Quick Setup
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"ONT Quick Setup")
    mod.Switch_Frame(driver)
    retry = True
    counter = 0
    while retry and counter <= 25:
        try:
            Slot_Select(driver,slot)
            retry = False
        except:
            retry = True
        time.sleep(0.5)
        if(mod.IsAlert(driver)):
            break
        if(counter == 26):
            driver.find_element(By.ID, "dontexist")
        time.sleep(0.5)
    retry = True
    counter = 0
    while retry and counter <= 20:
        try:
            ONT_Qui_Port_Select(driver,port)
            time.sleep(0.5)
            ONT_Qui_ONT_Qui_Load(driver)
            time.sleep(0.5)
            retry = False
        except:
            counter = counter+1
            retry = True
        if(counter == 21):
            driver.find_element(By.ID, "dontexist")

    # 用sn尋找ONT並刪除
    retry = True
    now_page = 1
    while retry:
        row_num = 0
        retry_2 = True
        while retry_2:
            try:
                if(driver.find_elements(By.CLASS_NAME, "rpGponOntSetup_txtSn")[row_num].get_attribute("value") == ont_sn):
                    retry = False
                    retry_2 = False
                    Select(driver.find_elements(By.CLASS_NAME, "rpGponOntSetup_sltAction")[row_num]).select_by_visible_text("Delete")
                    print("-ONT1-2 Delete- Success",file = open("ONT_Status_Test_report.txt", '+a'))
                    ONT_Qui_ONT_Qui_Apply(driver)
                else:
                    if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                        row_num = row_num+1
                    else:
                        retry_2 = False
            except:
                if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                    row_num = row_num+1
                else:
                    retry_2 = False
        if(retry and now_page < ONT_Qui_Page_Total(driver)):
            ONT_Qui_Next(driver)
            time.sleep(1)
            now_page = now_page+1
        elif(retry):
            retry = False
            print ("-ONT1-2 Delete- SN Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
# -------------------------end-------------------------
    
# ONT Quick Setup 17-16-121 Config ONT1-2 的 Password
# GPON > ONT Quick Setup
# -------------------------start-------------------------
 
    # 導向路徑ONT Quick Setup
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"ONT Quick Setup")
    mod.Switch_Frame(driver)

    # Load Slot & Pon
    retry = True
    counter = 0
    while retry and counter <= 25:
        try:
            Slot_Select(driver,slot)
            retry = False
        except:
            retry = True
        time.sleep(0.5)
        if(mod.IsAlert(driver)):
            break
        if(counter == 26):
            driver.find_element(By.ID, "dontexist")
        time.sleep(0.5)
    retry = True
    counter = 0
    while retry and counter <= 20:
        try:
            ONT_Qui_Port_Select(driver,port)
            time.sleep(0.5)
            ONT_Qui_ONT_Qui_Load(driver)
            time.sleep(0.5)
            retry = False
        except:
            counter = counter+1
            retry = True
        if(counter == 21):
            driver.find_element(By.ID, "dontexist")

    ONT_Qui_Next(driver)
    time.sleep(1)
    ONT_Qui_Next(driver)
    time.sleep(1)
    ONT_Qui_Next(driver)
    time.sleep(1)
    ONT_Qui_ONT_Qui_Active(driver,25,True)
    ONT_Qui_ONT_Qui_SN_Input(driver,25,ont_sn)
    Select(driver.find_elements(By.CLASS_NAME, "rpGponOntSetup_sltPort")[24]).select_by_visible_text(f"pon-{slot}-{port}")
    Select(driver.find_elements(By.CLASS_NAME, "rpGponOntSetup_sltOntTemp")[24]).select_by_visible_text(f"Template-{slot}-{port}-128")
    Select(driver.find_elements(By.CLASS_NAME, "rpGponOntSetup_sltAction")[24]).select_by_visible_text("Add")
    ONT_Qui_ONT_Qui_Apply(driver)
    print ("-ONT1-2 PW Config 17-16-121- Success",file = open("ONT_Status_Test_report.txt", '+a'))

# -------------------------end-------------------------

# Status value Check 17-16-121 確認 ont1-2和1-1的IS
# Gpon > ONT Quick Setup > Status
# -------------------------start-------------------------

    # 導向路徑Status
    time.sleep(40)
    mod.Tab_Switch(driver,"Status")
    retry = True
    counter = 0
    while retry and counter <= 25:
        try:
            Slot_Select(driver,slot)
            retry = False
        except:
            counter = counter+1
            retry = True
        time.sleep(0.5)
        if(mod.IsAlert(driver)):
            break
        if(counter == 26):
            driver.find_element(By.ID, "dontexist")
        time.sleep(0.5)
    retry = True
    counter = 0
    while retry and counter <= 20:
        try:
            ONT_Qui_Port_Select(driver,port)
            time.sleep(0.5)
            ONT_Qui_Sta_Load(driver)
            time.sleep(1)
            ONT_Qui_Sta_Load(driver)
            time.sleep(0.5)
            retry = False
        except:
            counter = counter+1
            retry = True
        if(counter == 21):
            driver.find_element(By.ID, "dontexist")

    # 測試Status中的sn、IS、password是否符合txt檔
    retry = True
    now_page = 1
    while retry:
        row_num = 0
        retry_2 = True
        while retry_2:
            try:
                if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpGponOntStatus_ontAid")[row_num].get_attribute("textContent") == "ont-17-16-121"):
                    retry = False
                    retry_2 = False
                    if(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_actPw")[row_num].get_attribute("textContent") == ont_password):
                        if(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_actStatus")[row_num].get_attribute("textContent") == "IS"):
                            print("-ONT 1-2 Check- Pass",file = open("ONT_Status_Test_report.txt", '+a'))
                        else:
                            print("-ONT 1-2 Check- IS Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                    else:
                        print("-ONT 1-2 Check- PW Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
                else:
                    if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                        row_num = row_num+1
                    else:
                        retry_2 = False
            except:
                if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                    row_num = row_num+1
                else:
                    retry_2 = False
        if(retry and now_page < ONT_Qui_Page_Total(driver)):
            ONT_Qui_Next(driver)
            time.sleep(1)
            now_page = now_page+1
        elif(retry):
            retry = False
            print ("-ONT 1-2 Check- AID Not Found",file = open("ONT_Status_Test_report.txt", '+a'))

    # 測試Status中的 sn = ont 1-1 Status是否為IS
    retry = True
    now_page = 1
    while retry:
        row_num = 0
        retry_2 = True
        while retry_2:
            try:   
                if(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_actSn")[row_num].get_attribute("textContent") == ont_sn_1_1):
                    retry = False
                    retry_2 = False
                    if(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_actStatus")[row_num].get_attribute("textContent") == "IS"):
                        print("-ONT 1-1 Check- Pass",file = open("ONT_Status_Test_report.txt", '+a'))
                    else:
                        print("-ONT 1-1 Check- IS Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                else:
                    if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                        row_num = row_num+1
                    else:
                        retry_2 = False
            except:
                if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                    row_num = row_num+1
                else:
                    retry_2 = False
        if(retry and now_page < ONT_Qui_Page_Total(driver)):
            ONT_Qui_Next(driver)
            time.sleep(1)
            now_page = now_page+1
        elif(retry):
            retry = False
            print ("-ONT 1-1 Check- SN Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
# -------------------------end-------------------------

# ONT Quick Setup 刪除ONT
# GPON > ONT Quick Setup > ONT Quick Setup
# -------------------------start-------------------------

    # 導向路徑ONT Quick Setup
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"ONT Quick Setup")
    mod.Switch_Frame(driver)
    retry = True
    counter = 0
    while retry and counter <= 25:
        try:
            Slot_Select(driver,slot)
            retry = False
        except:
            retry = True
        time.sleep(0.5)
        if(mod.IsAlert(driver)):
            break
        if(counter == 26):
            driver.find_element(By.ID, "dontexist")
        time.sleep(0.5)
    retry = True
    counter = 0
    while retry and counter <= 20:
        try:
            ONT_Qui_Port_Select(driver,port)
            time.sleep(0.5)
            ONT_Qui_ONT_Qui_Load(driver)
            time.sleep(0.5)
            retry = False
        except:
            counter = counter+1
            retry = True
        if(counter == 21):
            driver.find_element(By.ID, "dontexist")

    # 用sn尋找ONT並刪除
    retry = True
    now_page = 1
    while retry:
        row_num = 0
        retry_2 = True
        while retry_2:
            try:
                if(driver.find_elements(By.CLASS_NAME, "rpGponOntSetup_txtSn")[row_num].get_attribute("value") == ont_sn):
                    retry = False
                    retry_2 = False
                    Select(driver.find_elements(By.CLASS_NAME, "rpGponOntSetup_sltAction")[row_num]).select_by_visible_text("Delete")
                    print("-ONT1-2 Delete- Success",file = open("ONT_Status_Test_report.txt", '+a'))
                    ONT_Qui_ONT_Qui_Apply(driver)
                else:
                    if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                        row_num = row_num+1
                    else:
                        retry_2 = False
            except:
                if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                    row_num = row_num+1
                else:
                    retry_2 = False
        if(retry and now_page < ONT_Qui_Page_Total(driver)):
            ONT_Qui_Next(driver)
            time.sleep(1)
            now_page = now_page+1
        elif(retry):
            retry = False
            print ("-ONT1-2 Delete- SN Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
# -------------------------end-------------------------

# OLT Registration 設為E
# GPON > OLT Registration
# -------------------------start-------------------------

    # 導向路徑OLT Registration
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"OLT Registration")
    mod.Switch_Frame(driver)
    retry = True
    counter = 0
    while retry and counter <= 25:
        try:
            Slot_Select(driver,slot)
            time.sleep(0.5)
            OLT_Reg_OLT_Reg_Load(driver)
            retry = False
        except:
            retry = True
        time.sleep(0.5)
        if(mod.IsAlert(driver)):
            break
        if(counter == 26):
            driver.find_element(By.ID, "dontexist")
        time.sleep(0.5)
    driver.find_elements(By.XPATH, f"//*[@id='rpGponPortReg_sltReg']/option[5]")[int(port)-1].click()
    OLT_Reg_OLT_Reg_Apply(driver)
    print ("-OLT Reg E- Success",file = open("ONT_Status_Test_report.txt", '+a'))

# -------------------------end-------------------------

# Status value Check 確認 ont1-2和1-1的IS
# Gpon > ONT Quick Setup > Status
# -------------------------start-------------------------

    # 導向路徑Status
    time.sleep(90)
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"ONT Quick Setup")
    mod.Switch_Frame(driver)
    time.sleep(1)
    mod.Tab_Switch(driver,"Status")
    retry = True
    counter = 0
    while retry and counter <= 25:
        try:
            Slot_Select(driver,slot)
            retry = False
        except:
            counter = counter+1
            retry = True
        time.sleep(0.5)
        if(mod.IsAlert(driver)):
            break
        if(counter == 26):
            driver.find_element(By.ID, "dontexist")
        time.sleep(0.5)
    retry = True
    counter = 0
    while retry and counter <= 20:
        try:
            ONT_Qui_Port_Select(driver,port)
            time.sleep(0.5)
            ONT_Qui_Sta_Load(driver)
            time.sleep(1)
            ONT_Qui_Sta_Load(driver)
            time.sleep(0.5)
            retry = False
        except:
            counter = counter+1
            retry = True
        if(counter == 21):
            driver.find_element(By.ID, "dontexist")

    # 測試Status中的sn、IS、password是否符合txt檔
    retry = True
    now_page = 1
    while retry:
        row_num = 0
        retry_2 = True
        while retry_2:
            try:
                if(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_actSn")[row_num].get_attribute("textContent") == ont_sn):
                    retry = False
                    retry_2 = False
                    if(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_actStatus")[row_num].get_attribute("textContent") == "IS"):
                        print("-ONT 1-2 Check- Pass",file = open("ONT_Status_Test_report.txt", '+a'))
                    else:
                        print("-ONT 1-2 Check- IS Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                else:
                    if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                        row_num = row_num+1
                    else:
                        retry_2 = False
            except:
                if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                    row_num = row_num+1
                else:
                    retry_2 = False
        if(retry and now_page < ONT_Qui_Page_Total(driver)):
            ONT_Qui_Next(driver)
            time.sleep(1)
            now_page = now_page+1
        elif(retry):
            retry = False
            print ("-ONT 1-2 Check- SN Not Found",file = open("ONT_Status_Test_report.txt", '+a'))

    # 測試Status中的 sn = ont 1-1 Status是否為IS
    retry = True
    now_page = 1
    while retry:
        row_num = 0
        retry_2 = True
        while retry_2:
            try:   
                if(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_actSn")[row_num].get_attribute("textContent") == ont_sn_1_1):
                    retry = False
                    retry_2 = False
                    if(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_actStatus")[row_num].get_attribute("textContent") == "IS"):
                        print("-ONT 1-1 Check- Pass",file = open("ONT_Status_Test_report.txt", '+a'))
                    else:
                        print("-ONT 1-1 Check- IS Fail",file = open("ONT_Status_Test_report.txt", '+a'))
                else:
                    if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                        row_num = row_num+1
                    else:
                        retry_2 = False
            except:
                if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                    row_num = row_num+1
                else:
                    retry_2 = False
        if(retry and now_page < ONT_Qui_Page_Total(driver)):
            ONT_Qui_Next(driver)
            time.sleep(1)
            now_page = now_page+1
        elif(retry):
            retry = False
            print ("-ONT 1-1 Check- SN Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
# -------------------------end-------------------------

# ONT Quick Setup 刪除ONT
# GPON > ONT Quick Setup > ONT Quick Setup
# -------------------------start-------------------------

    # 導向路徑ONT Quick Setup
    mod.Switch_Default(driver)
    mod.SubPage_Switch(driver,"ONT Quick Setup")
    mod.Switch_Frame(driver)
    retry = True
    counter = 0
    while retry and counter <= 25:
        try:
            Slot_Select(driver,slot)
            retry = False
        except:
            retry = True
        time.sleep(0.5)
        if(mod.IsAlert(driver)):
            break
        if(counter == 26):
            driver.find_element(By.ID, "dontexist")
        time.sleep(0.5)
    retry = True
    counter = 0
    while retry and counter <= 20:
        try:
            ONT_Qui_Port_Select(driver,port)
            time.sleep(0.5)
            ONT_Qui_ONT_Qui_Load(driver)
            time.sleep(0.5)
            retry = False
        except:
            counter = counter+1
            retry = True
        if(counter == 21):
            driver.find_element(By.ID, "dontexist")

    # 用sn尋找ONT並刪除
    retry = True
    now_page = 1
    while retry:
        row_num = 0
        retry_2 = True
        while retry_2:
            try:
                if(driver.find_elements(By.CLASS_NAME, "rpGponOntSetup_txtSn")[row_num].get_attribute("value") == ont_sn):
                    retry = False
                    retry_2 = False
                    Select(driver.find_elements(By.CLASS_NAME, "rpGponOntSetup_sltAction")[row_num]).select_by_visible_text("Delete")
                    print("-ONT1-2 Delete- Success",file = open("ONT_Status_Test_report.txt", '+a'))
                    ONT_Qui_ONT_Qui_Apply(driver)
                else:
                    if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                        row_num = row_num+1
                    else:
                        retry_2 = False
            except:
                if(row_num < ONT_Qui_Sta_SN_Num(driver)):
                    row_num = row_num+1
                else:
                    retry_2 = False
        if(retry and now_page < ONT_Qui_Page_Total(driver)):
            ONT_Qui_Next(driver)
            time.sleep(1)
            now_page = now_page+1
        elif(retry):
            retry = False
            print ("-ONT1-2 Delete- SN Not Found",file = open("ONT_Status_Test_report.txt", '+a'))
# -------------------------end-------------------------

    print("Test Finished",file = open("ONT_Status_Test_report.txt", '+a'))
    print("======================================================================================",file = open("ONT_Status_Test_report.txt", '+a'))

def ONT_Qui_open_IP_Address_by_SN(driver,sn,newpage_username,newpage_password):
    
# ONT Quick Setup 用 SN 找 AID
# GPON > ONT Quick Setup > ONT Quick Setup
# -------------------------start-------------------------
    
    # 導向路徑ONT Quick Setup
    driver.switch_to.window(driver.window_handles[0])
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"GPON")
    mod.SubPage_Switch(driver,"ONT Quick Setup")
    mod.Switch_Frame(driver)

    # 搜尋符合的sn
    if_find = False
    ont_aid = ""
    for slot in range(Get_Max_Slot(driver)):
        if(if_find == False):
            retry = True
            while retry:
                try:
                    Slot_Select(driver,slot+1)
                    retry = False
                except:
                    retry = True
                time.sleep(0.5)
            if(mod.IsAlert(driver)):
                time.sleep(0.5)
            else:
                time.sleep(0.5)
                for port in range(Get_Max_Port(driver)):
                    if(if_find == False):
                        retry = True
                        counter = 0
                        while retry and counter <= 20:
                            try:
                                ONT_Qui_Port_Select(driver,port+1)
                                time.sleep(0.5)
                                ONT_Qui_ONT_Qui_Load(driver)
                                time.sleep(0.5)
                                retry = False
                            except:
                                counter = counter+1
                                retry = True
                        retry_2 = True
                        now_page = 1
                        while retry_2:
                            for index in range(driver.find_elements(By.CLASS_NAME, "listOnt").__len__()):
                                if(driver.find_elements(By.ID, "rpGponOntSetup_txtSn")[index].get_attribute("value") == sn):
                                    ont_aid = driver.find_elements(By.ID, "rpGponOntSetup_ontAid")[index].get_attribute("textContent")
                                    if_find = True
                                    retry_2 = False
                            if(if_find == False and now_page < ONT_Qui_Page_Total(driver)):
                                try:
                                    ONT_Qui_Next(driver)
                                    time.sleep(1)
                                    now_page = now_page+1
                                except:
                                    pass
                            else:
                                retry_2 = False
    if(if_find == False):
        print("SN NOT FOUND")
        return

    # 切換至WAN尋找IP Address
    slot = ont_aid.split("-")[1]
    port = ont_aid.split("-")[2]
    mod.Tab_Switch(driver,"Wan")
    retry = True
    while retry:
        try:
            Slot_Select(driver,slot)
            retry = False
        except:
            retry = True
        time.sleep(0.5)
        if(mod.IsAlert(driver)):
            break
        time.sleep(0.5)
    retry = True
    counter = 0
    while retry and counter <= 20:
        try:
            ONT_Qui_Port_Select(driver,port)
            time.sleep(0.5)
            ONT_Qui_Wan_Load(driver)
            time.sleep(0.5)
            retry = False
        except:
            counter = counter+1
            retry = True
    if(driver.find_elements(By.CLASS_NAME, "listWan").__len__() == 0):
        pass
    else:
        for index in range(driver.find_elements(By.CLASS_NAME, "listWan").__len__()):
            if(driver.find_elements(By.CLASS_NAME, "td-table-content.rpGponOntWan_ontAid")[index].get_attribute("textContent") == ont_aid):
                ip_address = driver.find_elements(By.CLASS_NAME, "td-table-content.rpGponOntWan_ipaddr")[index].get_attribute("textContent")
                break
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(f"http://{ip_address}/")

    
    # 登入新分頁
    try:
        username2_ = driver.find_element(By.ID, "username")
        username2_.send_keys(newpage_username)
        password2_ = driver.find_element(By.ID, "userpassword")
        password2_.send_keys(newpage_password)
        driver.find_element(By.ID, "loginBtn").click()
        time.sleep(2)
        newpage_ont_model_name = driver.find_element(By.ID, "card_sysinfo_modelname").get_attribute("textContent")
        newpage_ont_version = driver.find_element(By.ID, "card_sysinfo_fwversion").get_attribute("textContent")
    except:
        print("New Web Open Fail")

 
# -------------------------end-------------------------

# ONT Quick Setup -> ONT Quick Setup

def ONT_Qui_ONT_Qui_Load(driver):
    btn = driver.find_element(By.NAME, "rpGponOntSetup_btnLoad")
    btn.click()

def ONT_Qui_ONT_Qui_Next(driver):
    btn = driver.find_element(By.ID, "btnNextPage")
    btn.click()

def ONT_Qui_ONT_Qui_Active(driver,index,request):
    check_box = driver.find_elements(By.NAME, "rpGponOntSetup_chkActive")[index-1]
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ONT_Qui_ONT_Qui_SN_Input(driver,index,sn_num):
    input = driver.find_elements(By.NAME, "rpGponOntSetup_txtSn")[index-1]
    input.clear()
    input.send_keys(sn_num)

def ONT_Qui_ONT_Qui_PW_Input(driver,index,password):
    input = driver.find_elements(By.NAME, "rpGponOntSetup_txtPw")[index-1]
    input.clear()
    input.send_keys(password)

def ONT_Qui_ONT_Qui_Apply(driver):
    btn = driver.find_element(By.NAME, "rpGponOntSetup_btnApply")
    btn.click()

def ONT_Qui_ONT_Qui_ONT_Web_Login(driver,slot,port,aid_num,newpage_username,newpage_password):
    
    # 導向路徑ONT Quick Setup
    driver.switch_to.window(driver.window_handles[0])
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"GPON")
    mod.SubPage_Switch(driver,"ONT Quick Setup")
    mod.Switch_Frame(driver)
    retry = True
    while retry:
        try:
            Slot_Select(driver,slot)
            retry = False
        except:
            retry = True
        time.sleep(0.5)
        if(mod.IsAlert(driver)):
            break
        time.sleep(0.5)
    retry = True
    counter = 0
    while retry and counter <= 20:
        try:
            ONT_Qui_Port_Select(driver,port)
            time.sleep(0.5)
            ONT_Qui_ONT_Qui_Load(driver)
            time.sleep(0.5)
            retry = False
        except:
            counter = counter+1
            retry = True
    driver.find_elements(By.ID, "rpGponOntSetup_ontAid")[aid_num].click()

    # 登入新分頁
    try:
        driver.switch_to.window(driver.window_handles[1])
        username2_ = driver.find_element(By.ID, "username")
        username2_.send_keys(newpage_username)
        password2_ = driver.find_element(By.ID, "userpassword")
        password2_.send_keys(newpage_password)
        driver.find_element(By.ID, "loginBtn").click()
        time.sleep(2)
    except:
        print("ONT Wed Open Fail",file = open("ONT_Status_Test_report.txt", '+a'))
        return 0

def ONT_Qui_ONT_Qui_Check(driver,ont_aid,ont_sn,ont_password,slot,port):
    retry = True
    
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"GPON")
    mod.SubPage_Switch(driver,"ONT Quick Setup")
    mod.Switch_Frame(driver)
    # mod.Tab_Switch(driver,"ONT Quick Setup")
    while retry:
        try:
            Slot_Select(driver,slot)
            retry = False
        except:
            retry = True
        time.sleep(0.2)
        if(mod.IsAlert(driver)):
            break
        time.sleep(0.2)
    retry = True
    counter = 0
    while retry and counter <= 10:
        try:
            ONT_Qui_Port_Select(driver,port)
            ONT_Qui_ONT_Qui_Load(driver)
            retry = False
        except:
            counter = counter+1
            retry = True
    retry = True
    while retry:
        try:
            for sn_num in range(ONT_Qui_Sta_SN_Num(driver)):
                if(driver.find_elements(By.CLASS_NAME, "rpGponOntSetup_ontAid")[sn_num].get_attribute("textContent") == ont_aid):
                    retry = False
                    if(driver.find_elements(By.CLASS_NAME, "rpGponOntSetup_txtSn")[sn_num].get_attribute("value") == ont_sn):
                        if(driver.find_elements(By.CLASS_NAME, "rpGponOntSetup_txtPw")[sn_num].get_attribute("value") == ont_password):
                            print(f"ONT Quick Setup AID={ont_aid} SN={ont_sn} Password={ont_password}",True,file = open("ONT_Status_Test_report.txt", '+a'))
                            return True
        except:
            try:
                ONT_Qui_Next(driver)
                time.sleep(1)
                retry = True
            except:
                retry = False
                print (f"AID={ont_aid} SN={ont_sn} Password={ont_password} Not Found",file = open("ONT_Status_Test_report.txt", '+a'))

# ONT Quick Setup -> Status

# 
def ONT_Qui_Sta_Load(driver):
    btn = driver.find_element(By.NAME, "rpGponOntStatus_btnLoad")
    btn.click()

def ONT_Qui_Sta_SN_Num(driver):
    num = driver.find_elements(By.CLASS_NAME, "td-table-content.i1").__len__()
    return num

#
def ONT_Qui_Sta_Check(driver,ont_aid,ont_sn,ont_password,slot,port):
    retry = True
    
    mod.Switch_Default(driver)
    mod.Page_Switch(driver,"GPON")
    mod.SubPage_Switch(driver,"ONT Quick Setup")
    mod.Switch_Frame(driver)
    mod.Tab_Switch(driver,"Status")
    while retry:
        try:
            Slot_Select(driver,slot)
            retry = False
        except:
            retry = True
        time.sleep(0.2)
        if(mod.IsAlert(driver)):
            break
        # elif(driver.find_element(By.XPATH, f"//*[@id='lctbl_selPort']/option[{port+1}]")):
        time.sleep(0.2)
    retry = True
    counter = 0
    while retry and counter <= 10:
        try:
            ONT_Qui_Port_Select(driver,port)
            ONT_Qui_Sta_Load(driver)
            retry = False
        except:
            counter = counter+1
            # print(slot+1,"-",port+1," ",counter)
            retry = True
    retry = True
    while retry:
        try:
            for sn_num in range(ONT_Qui_Sta_SN_Num(driver)):
                if(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_actSn")[sn_num].get_attribute("textContent") == ont_sn):
                    retry = False
                    if(driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_actStatus")[sn_num].get_attribute("textContent") == "IS" and driver.find_elements(By.CLASS_NAME, "div-row-begin-center.rpGponOntStatus_actPw")[sn_num].get_attribute("textContent") == "DEFAULT"):
                        print(f"Status AID={ont_aid} SN={ont_sn} Password={ont_password}",True,file = open("ONT_Status_Test_report.txt", '+w'))
                        return True
                    else:
                        print(f"Status AID={ont_aid} SN={ont_sn} Password={ont_password}",False,file = open("ONT_Status_Test_report.txt", '+w'))
                        return False
        except:
            try:
                ONT_Qui_Next(driver)
                time.sleep(1)
            except:
                retry = False
    print (f"AID={ont_aid} SN={ont_sn} Password={ont_password} Not Found",file = open("ONT_Status_Test_report.txt", '+w'))

# ONT Quick Setup -> Wan

def ONT_Qui_Wan_Load(driver):
    btn = driver.find_element(By.NAME, "rpGponOntWan_btnLoad")
    btn.click()

# ONT Quick Setup -> Unregistered

def ONT_Qui_Unr_Load(driver):
    btn = driver.find_element(By.NAME, "rpGponOntUnreg_btnLoad")
    btn.click()

def ONT_Qui_Unr_Tem_Pon(driver,row_num,sel):
    select = driver.find_elements(By.XPATH, f"//*[@id='rpGponOntUnreg_sltPortTemp']/option[{sel}]")[row_num]
    select.click()

def ONT_Qui_Unr_Tem_Tem(driver,row_num,sel):
    select = driver.find_elements(By.XPATH, f"//*[@id='rpGponOntUnreg_sltOntTemp']/option[{sel}]")[row_num]
    select.click()

def ONT_Qui_Unr_Reg(driver,row_num,request):
    check_box = driver.find_elements(By.NAME, "rpGponOntUnreg_chkReg")[row_num]
    if(check_box.is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()

def ONT_Qui_Unr_Apply(driver):
    driver.find_element(By.ID, "rpGponOntUnreg_btnApply").click()

# ONT Model

def ONT_Model_Name(driver,name):
    input = driver.find_element(By.ID, "rpGponOntModel_addName")
    input.clear()
    input.send_keys(name)

def ONT_Model_ID(driver,key):
    input = driver.find_element(By.ID, "rpGponOntModel_modelId")
    input.clear()
    input.send_keys(key)

def ONT_Model_VV(driver,key):
    input = driver.find_element(By.ID, "rpGponOntModel_vendorVersion")
    input.clear()
    input.send_keys(key)

def ONT_Model_SV(driver,key):
    input = driver.find_element(By.ID, "rpGponOntModel_softwareVersion")
    input.clear()
    input.send_keys(key)

def ONT_Model_Card1(driver,key):
    input = driver.find_element(By.ID, "rpGponOntModel_card1")
    input.clear()
    input.send_keys(key)

def ONT_Model_Card2(driver,key):
    input = driver.find_element(By.ID, "rpGponOntModel_card2")
    input.clear()
    input.send_keys(key)

def ONT_Model_Card3(driver,key):
    input = driver.find_element(By.ID, "rpGponOntModel_card3")
    input.clear()
    input.send_keys(key)

def ONT_Model_Card4(driver,key):
    input = driver.find_element(By.ID, "rpGponOntModel_card4")
    input.clear()
    input.send_keys(key)

def ONT_Model_Card5(driver,key):
    input = driver.find_element(By.ID, "rpGponOntModel_card5")
    input.clear()
    input.send_keys(key)
    
def ONT_Model_Apply_Up(driver):
    btn = driver.find_element(By.ID, "rpGponOntModel_btnAdd")
    btn.click()
    
def ONT_Model_Apply_Down(driver):
    btn = driver.find_element(By.ID, "rpGponOntModel_btnDel")
    btn.click()

# File Transfer

def File_Transfer_ONT(driver,slot,pon,aid):
    slot = int(slot)
    pon = int(pon)
    aid = int(aid)+1
    time.sleep(1)
    Select(driver.find_element(By.ID, "gponSelOltPort")).select_by_visible_text(f"{slot}-{pon}")
    time.sleep(1)
    if(aid <= 32):
        driver.find_element(By.XPATH, f"//*[@id='rpGponFileTransfer_selRange']/option[1]")
    elif(aid <= 64):
        driver.find_element(By.XPATH, f"//*[@id='rpGponFileTransfer_selRange']/option[2]")
    elif(aid <= 96):
        driver.find_element(By.XPATH, f"//*[@id='rpGponFileTransfer_selRange']/option[3]")
    else:
        driver.find_element(By.XPATH, f"//*[@id='rpGponFileTransfer_selRange']/option[4]")
    time.sleep(3)
    Select(driver.find_element(By.ID, "rpGponFileTransfer_selONT")).select_by_visible_text(f"ont-{slot}-{pon}-{aid}")

def File_Transfer_LFN(driver,key):
    input = driver.find_element(By.ID, "rpGponFileTransfer_iptLocalFileName")
    input.clear()
    input.send_keys(key)

def File_Transfer_URI(driver,key):
    input = driver.find_element(By.ID, "rpGponFileTransfer_iptURI")
    input.clear()
    input.send_keys(key)

def File_Transfer_UN(driver,key):
    input = driver.find_element(By.ID, "rpGponFileTransfer_iptUsername")
    input.clear()
    input.send_keys(key)

def File_Transfer_PW(driver,key):
    input = driver.find_element(By.ID, "rpGponFileTransfer_iptPassword")
    input.clear()
    input.send_keys(key)
    
def File_Transfer_Upload(driver):
    btn = driver.find_element(By.ID, "rpGponFileTransfer_btnUploadAdd")
    btn.click()
    
def File_Transfer_Download(driver):
    btn = driver.find_element(By.ID, "rpGponFileTransfer_btnDownloadAdd")
    btn.click()
