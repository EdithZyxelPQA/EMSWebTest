# global url,url_ip,username,password,loop
# global msc_slot,msc_port,glc_slot,glc_port
# global slot_1_aid,msc_port,glc_slot,glc_port

global msc_card_type 
msc_card_type = 'default'




# set_up_file = open("ENV/ENV_WEB.txt",'r')
# lines = set_up_file.readlines()
# set_up_file.close()
# url = lines[0].split("=")[1]
# url_ip = url.split("/")[2] 
# username = lines[1].split("=")[1]
# password = lines[2].split("=")[1]
# loop = int(lines[3].split("'")[1])

# #Card
# msc_slot = lines[6].split("'")[1]
# msc_port = lines[7].split("'")[1]
# glc_slot = lines[8].split("'")[1]
# glc_port = lines[9].split("'")[1]

# #Gpon
# slot_1_aid = lines[12].split("'")[1]
# pon_1_aid = lines[13].split("'")[1]
# ont_1_1 = lines[16].split("'")[1]
# ont_1_2 = lines[17].split("'")[1]
# ont_1_1_aid = lines[19].split("'")[1]
# ont_1_2_aid = lines[20].split("'")[1]

# slot_2_aid = lines[24].split("'")[1]
# pon_2_aid = lines[25].split("'")[1]
# ont_2_1 = lines[28].split("'")[1]
# ont_2_2 = lines[29].split("'")[1]
# ont_2_1_aid = lines[31].split("'")[1]
# ont_2_2_aid = lines[32].split("'")[1]

# ont_1_1_sn = lines[36].split("'")[1]
# ont_1_1_pw = lines[37].split("'")[1]
# ont_1_1_ont_USER = lines[38].split("=")[1]
# ont_1_1_ont_PW = lines[39].split("=")[1]

# ont_1_2_sn = lines[41].split("'")[1]
# ont_1_2_pw = lines[42].split("'")[1]
# ont_1_2_ont_USER = lines[43].split("=")[1]
# ont_1_2_ont_PW = lines[44].split("=")[1]

# ont_2_1_sn = lines[46].split("'")[1]
# ont_2_1_pw = lines[47].split("'")[1]
# ont_2_1_ont_USER = lines[48].split("=")[1]
# ont_2_1_ont_PW = lines[49].split("=")[1]

# ont_2_2_sn = lines[51].split("'")[1]
# ont_2_2_pw = lines[52].split("'")[1]
# ont_2_2_ont_USER = lines[53].split("=")[1]
# ont_2_2_ont_PW = lines[54].split("=")[1]

# #Xpon
# slot_x_1_aid = lines[58].split("'")[1]
# pon_x_1_aid = lines[59].split("'")[1]
# ont_x_1_1 = lines[62].split("'")[1]
# ont_x_1_2 = lines[63].split("'")[1]
# ont_x_1_1_aid = lines[65].split("'")[1]
# ont_x_1_2_aid = lines[66].split("'")[1]

# slot_x_2_aid = lines[70].split("'")[1]
# pon_x_2_aid = lines[71].split("'")[1]
# ont_x_2_1 = lines[74].split("'")[1]
# ont_x_2_2 = lines[75].split("'")[1]
# ont_x_2_1_aid = lines[77].split("'")[1]
# ont_x_2_2_aid = lines[78].split("'")[1]

# ont_x_1_1_sn = lines[82].split("'")[1]
# ont_x_1_1_pw = lines[83].split("'")[1]
# ont_x_1_1_ont_USER = lines[84].split("=")[1]
# ont_x_1_1_ont_PW = lines[85].split("=")[1]

# ont_x_1_2_sn = lines[87].split("'")[1]
# ont_x_1_2_pw = lines[88].split("'")[1]
# ont_x_1_2_ont_USER = lines[89].split("=")[1]


# ont_x_1_2_ont_PW = lines[90].split("=")[1]

# ont_x_2_1_sn = lines[92].split("'")[1]
# ont_x_2_1_pw = lines[93].split("'")[1]
# ont_x_2_1_ont_USER = lines[94].split("=")[1]
# ont_x_2_1_ont_PW = lines[95].split("=")[1]

# ont_x_2_2_sn = lines[97].split("'")[1]
# ont_x_2_2_pw = lines[98].split("'")[1]
# ont_x_2_2_ont_USER = lines[99].split("=")[1]
# ont_x_2_2_ont_PW = lines[100].split("=")[1]


# # service_mode_x_1 = lines[104].split("'")[1]
# service_mode_x_1 = ''

# # snmp_get = lines[110].split("=")[1]
# snmp_get = ''
# snmp_set = '' #lines[111].split("=")[1]
# snmp_version = '' #lines[112].split("=")[1]

# ont_1_1 = int(ont_1_1)-1
# ont_1_2 = int(ont_1_2)-1
# ont_2_1 = int(ont_2_1)-1
# ont_2_2 = int(ont_2_2)-1

# ems_password = "Pqa1234!!"
# test_retry_num = 3




# # # # # # #

import json

env_file = "ENV/ENV_WEB.json"

with open(env_file, 'r') as f:
    d = json.load(f)

url = d["ZYXEL_DUT"]["NODE1"]["url"]
url_ip = url.split("/")[2]   
username = d['ZYXEL_DUT']['NODE1']["login_username"]
password = d['ZYXEL_DUT']['NODE1']["login_password"]
login_username = d['ZYXEL_DUT']['NODE1']["login_username"]
login_password = d['ZYXEL_DUT']['NODE1']["login_password"]
default_username = d['ZYXEL_DUT']['NODE1']["default_username"]
default_password = d['ZYXEL_DUT']['NODE1']["default_password"]
loop = d["LOOP"]["count"]

# EMS
ems_url = d["EMS"]["url"]
ems_username = d["EMS"]["login_username"]
ems_password = d["EMS"]["login_password"]

#Card
msc_slot = d["ZYXEL_DUT"]["NODE1"]["CARDINFO"]["MSC"]["slot_id"]
msc_port = d["ZYXEL_DUT"]["NODE1"]["CARDINFO"]["MSC"]["port_id"]
glc_slot = d["ZYXEL_DUT"]["NODE1"]["CARDINFO"]["GLC1440X"]["slot_id"] #/ d["ZYXEL_DUT"]["NODE1"]["CARDINFO"]["GLC1540X"]["slot_id"]
glc_port = d["ZYXEL_DUT"]["NODE1"]["CARDINFO"]["GLC1440X"]["port_id"] #/["GLC1540X"]["port_id"]
OLT_Port = d["ZYXEL_DUT"]["NODE1"]["CARDINFO"]["OLT140x"]["port_id"]
OLT_Eth_Port = d["ZYXEL_DUT"]["NODE1"]["CARDINFO"]["OLT140x"]["eth_port_id"]

#Xpon
slot_x_1_aid = d["ZYXEL_DUT"]["NODE1"]["ONTINFO"]["XPON"]["ONT1"]["slot_id"]
pon_x_1_aid = d["ZYXEL_DUT"]["NODE1"]["ONTINFO"]["XPON"]["ONT1"]["port_id"]
ont_x_1_1 = d["ZYXEL_DUT"]["NODE1"]["ONTINFO"]["XPON"]["ONT1"]["ont_id"]
ont_x_1_2 = "d['Xpon']['Ont_x_1_2']"         ## not sure if use
ont_x_1_1_aid = f'{slot_x_1_aid}-{pon_x_1_aid}-{ont_x_1_1}'
ont_x_1_2_aid = "d['Xpon']['Ont_x_1_2_aid']" ##


ont_x_1_1_sn_12 = d["ZYXEL_DUT"]["NODE1"]["ONTINFO"]["XPON"]["ONT1"]["sn_12"]
ont_x_1_1_sn = d["ZYXEL_DUT"]["NODE1"]["ONTINFO"]["XPON"]["ONT1"]["sn_16"]
ont_x_1_1_pw = d["ZYXEL_DUT"]["NODE1"]["ONTINFO"]["XPON"]["ONT1"]["pw"]
ont_x_1_1_ont_USER = d["ZYXEL_DUT"]["NODE1"]["ONTINFO"]["XPON"]["ONT1"]["ont_user"]
ont_x_1_1_ont_PW = d["ZYXEL_DUT"]["NODE1"]["ONTINFO"]["XPON"]["ONT1"]["ont_pw"]

ont_x_1_2_sn_12 = "d['Xpon']['ONT']['ONT_x_1_2_SN_12']"   ##
ont_x_1_2_sn = "d['Xpon']['ONT']['ONT_x_1_2_SN']"             ## use
ont_x_1_2_pw = "d['Xpon']['ONT']['ONT_x_1_2_PW']"             ## 
ont_x_1_2_ont_USER = "d['Xpon']['ONT']['ONT_x_1_2_ont_USER']" ##
ont_x_1_2_ont_PW = "d['Xpon']['ONT']['ONT_x_1_2_ont_PW']"     ##


test_retry_num = 3