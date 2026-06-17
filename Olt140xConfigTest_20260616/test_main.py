import pytest
import json
from customdriver import CustomDriver
from ems_test_module import test_1
from ems_test_module import test_2
from ems_test_module import *
import time
import selenium_module as mod

with open('ENV_j.json', 'r') as f:
    d = json.load(f)

if(True):

    url = d['url']
    url_ip = url.split("/")[2] 
    username = d['username']
    password = d['password']
    loop = int(d['loop']) 

    #Card
    msc_slot = d['Card']['MSC_slot']
    msc_port = d['Card']['MSC_port']
    glc_slot = d['Card']['GLC_slot']
    glc_port = d['Card']['GLC_port']

    #Gpon
    slot_1_aid = d['Gpon']['Slot_1_aid']
    pon_1_aid = d['Gpon']['Pon_1_aid']
    ont_1_1 = d['Gpon']['Ont_1_1']
    ont_1_2 = d['Gpon']['Ont_1_2']
    ont_1_1_aid = d['Gpon']['Ont_1_1_aid']
    ont_1_2_aid = d['Gpon']['Ont_1_2_aid']

    slot_2_aid = d['Gpon']['Slot_2_aid']
    pon_2_aid = d['Gpon']['Pon_2_aid']
    ont_2_1 = d['Gpon']['Ont_2_1']
    ont_2_2 = d['Gpon']['Ont_2_2']
    ont_2_1_aid = d['Gpon']['Ont_2_1_aid']
    ont_2_2_aid = d['Gpon']['Ont_2_2_aid']

    ont_1_1_sn = d['Gpon']['ONT']['ONT_1_1_SN']
    ont_1_1_pw = d['Gpon']['ONT']['ONT_1_1_PW']
    ont_1_1_ont_USER = d['Gpon']['ONT']['ONT_1_1_ont_USER']
    ont_1_1_ont_PW = d['Gpon']['ONT']['ONT_1_1_ont_PW']

    ont_1_2_sn = d['Gpon']['ONT']['ONT_1_2_SN']
    ont_1_2_pw = d['Gpon']['ONT']['ONT_1_2_PW']
    ont_1_2_ont_USER = d['Gpon']['ONT']['ONT_1_2_ont_USER']
    ont_1_2_ont_PW = d['Gpon']['ONT']['ONT_1_2_ont_PW']

    ont_2_1_sn = d['Gpon']['ONT']['ONT_2_1_SN']
    ont_2_1_pw = d['Gpon']['ONT']['ONT_2_1_PW']
    ont_2_1_ont_USER = d['Gpon']['ONT']['ONT_2_1_ont_USER']
    ont_2_1_ont_PW = d['Gpon']['ONT']['ONT_2_1_ont_PW']

    ont_2_2_sn = d['Gpon']['ONT']['ONT_2_2_SN']
    ont_2_2_pw = d['Gpon']['ONT']['ONT_2_2_PW']
    ont_2_2_ont_USER = d['Gpon']['ONT']['ONT_2_2_ont_USER']
    ont_2_2_ont_PW = d['Gpon']['ONT']['ONT_2_2_ont_PW']

    #Xpon
    slot_x_1_aid = d['Xpon']['Slot_x_1_aid']
    pon_x_1_aid = d['Xpon']['Pon_x_1_aid']
    ont_x_1_1 = d['Xpon']['Ont_x_1_1']
    ont_x_1_2 = d['Xpon']['Ont_x_1_2']
    ont_x_1_1_aid = d['Xpon']['Ont_x_1_1_aid']
    ont_x_1_2_aid = d['Xpon']['Ont_x_1_2_aid']

    slot_x_2_aid = d['Xpon']['Slot_x_2_aid']
    pon_x_2_aid = d['Xpon']['Pon_x_2_aid']
    ont_x_2_1 = d['Xpon']['Ont_x_2_1']
    ont_x_2_2 = d['Xpon']['Ont_x_2_2']
    ont_x_2_1_aid = d['Xpon']['Ont_x_2_1_aid']
    ont_x_2_2_aid = d['Xpon']['Ont_x_2_2_aid']

    ont_x_1_1_sn = d['Xpon']['ONT']['ONT_x_1_1_SN']
    ont_x_1_1_pw = d['Xpon']['ONT']['ONT_x_1_1_PW']
    ont_x_1_1_ont_USER = d['Xpon']['ONT']['ONT_x_1_1_ont_USER']
    ont_x_1_1_ont_PW = d['Xpon']['ONT']['ONT_x_1_1_ont_PW']

    ont_x_1_2_sn = d['Xpon']['ONT']['ONT_x_1_2_SN']
    ont_x_1_2_pw = d['Xpon']['ONT']['ONT_x_1_2_PW']
    ont_x_1_2_ont_USER = d['Xpon']['ONT']['ONT_x_1_2_ont_USER']
    ont_x_1_2_ont_PW = d['Xpon']['ONT']['ONT_x_1_2_ont_PW']

    ont_x_2_1_sn = d['Xpon']['ONT']['ONT_x_2_1_SN']
    ont_x_2_1_pw = d['Xpon']['ONT']['ONT_x_2_1_PW']
    ont_x_2_1_ont_USER = d['Xpon']['ONT']['ONT_x_2_1_ont_USER']
    ont_x_2_1_ont_PW = d['Xpon']['ONT']['ONT_x_2_1_ont_PW']

    ont_x_2_2_sn = d['Xpon']['ONT']['ONT_x_2_2_SN']
    ont_x_2_2_pw = d['Xpon']['ONT']['ONT_x_2_2_PW']
    ont_x_2_2_ont_USER = d['Xpon']['ONT']['ONT_x_2_2_ont_USER']
    ont_x_2_2_ont_PW = d['Xpon']['ONT']['ONT_x_2_2_ont_PW']

    # service_mode_x_1 = lines[104].split("'")[1]
    service_mode_x_1 = ''

    # snmp_get = lines[110].split("=")[1]
    snmp_get = ''
    snmp_set = '' #lines[111].split("=")[1]
    snmp_version = '' #lines[112].split("=")[1]

    GLC1440_slot = '' #lines[114].split("'")[1]
    GLC1440_port = glc_port# '' #lines[115].split("'")[1]

    GLC1540_slot = '' #lines[117].split("'")[1]
    GLC1540_port = glc_port#'' #lines[118].split("'")[1]

    OLC3416_42_slot = '' #lines[120].split("'")[1]
    OLC3416_42_port =  pon_1_aid #'' #lines[121].split("'")[1]

    OLC3416B_slot = '' #lines[123].split("'")[1]
    OLC3416B_port = pon_x_1_aid#'' #lines[124].split("'")[1]

    OLC3816_port = pon_x_1_aid

    OLC3708_port = pon_x_1_aid
    if(int(pon_x_1_aid) > 8):
        OLC3708_port = "8"

    ont_1_1 = int(ont_1_1)-1
    ont_1_2 = int(ont_1_2)-1
    ont_2_1 = int(ont_2_1)-1
    ont_2_2 = int(ont_2_2)-1

    ems_password = "Pqa1234!!"

file_name = 'temp_test_1204.txt'
open(file_name,"w+")

# # # # # TEMP # # # # # 
list1:['2,1,0,OLC3816-IA', '1,2,39,GLC1540X-55A', '4,4,0,MSC1240QA']
MSC_card  = '4'
# # # # # TEMP # # # # # 

# @pytest.fixture
def test_just_t():
    # test_1(False)
    # test_1()
    # test_2()

    # SET
    slot = '2'
    port = '2'
    output_id = '1234'
    

    driver = CustomDriver()
    
    driver.get(url) # 連上網頁
    mod.Login(driver,username,password) # 登入
    case_test_1(driver,url,slot,port,output_id,username,password,file_name)
    Multicast_VLAN_Mode(driver,url,MSC_card,username,password,file_name)

test_just_t()
