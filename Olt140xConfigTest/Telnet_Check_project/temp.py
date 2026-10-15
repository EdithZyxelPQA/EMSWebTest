import json
import datetime
import time
import random
import os
import telnetlib
import paramiko
import ftplib
from contextlib import closing
 
JSON_file = 'd:/192.168.169.86_01.json'

def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True

def is_json_f(file):
    try:
        with open(file) as f:
            # data = json.load(f)
            # json.loads(f)
            json.load(f)
    except ValueError:
        return False
    return True

# data = {
#     'name' : 'ACME',
#     'shares' : 100,
#     'price' : 542.23
# }
 
# json_str = json.dumps(data)

def prin():
    print (is_json_f(JSON_file))
    print (is_json_f('D:\zh_memo\Telnet_Check_project\data.json'))

def test():
    with open(JSON_file) as f:
        data = json.load(f,strict=False)
        print(data)
def dump():
    with open(JSON_file) as f:
        json.dump(f)

# prin()
# test()  # open wrd



# with open('n.json') as f:
#     json.load(f)

# f = open('input.txt','r')
# line = f.readline().replace('\n','')
# while(line):
#     print(line)
#     line = f.readline().replace('\n','')

# -----------------------------------------------------------------------------------

# fetch data ==========================
with open('data.json') as f:
    data0 = json.load(f)
telnet_ip = data0['telnet_ip']
username = data0['username']
password = data0['password']
ssh_ip = data0['ssh_ip']
ssh_password = data0['ssh_password']

with open('data_cardtype_list.json') as f:
    dict_cardtype = json.load(f)
dict_rate = {"1g-full":"1000"}
# output command ======================
# set_up_file = open("output_command.txt",'r')
# lines_env = set_up_file.readlines()
# set_up_file.close()
time1 = f'{str(datetime.datetime.now()).split(":")[0]}{str(datetime.datetime.now()).split(":")[1]}'
output_file = f'output_command_{time1}.txt'
file0 = open(output_file,'w+')
# load json ===========================
print('00')
with open(JSON_file) as f:
    data = json.load(f,strict=False)
#     print(data)

print( data['ipconf']['iplist'])
print( data['ipconf']['iplist'][0]['interface'])





# Telent and Check ======================
def f(com,tnet_hndl,output_file):
    print(com,file = open(output_file, '+a'))  # print command
    tnet_hndl.write(com.encode('utf-8') + b"\n")
    s = str(tnet_hndl.read_until(b"# "))
    list_1 = s.split('\\r\\n')
    for i in list_1:
        print (':',i,file = open(output_file, '+a'))  # print return data
    return s

host_ip = telnet_ip
tnet_hndl = telnetlib.Telnet(host_ip)
print (tnet_hndl.read_until(b"login: "),file = open(output_file, '+a'))
tnet_hndl.write(username.encode('ascii') + b"\n")
print (tnet_hndl.read_until(b"Password: "),file = open(output_file, '+a'))
tnet_hndl.write(password.encode('ascii') + b"\n")
print (tnet_hndl.read_until(b"# "),file = open(output_file, '+a'))



def onelinetry(com,content,print_t,tnet_hndl,output_file,t_file):
    print(com,file = open(output_file, '+a'))  # print command
    tnet_hndl.write(com.encode('ascii') + b"\n")
    s = str(tnet_hndl.read_until(b"# "))
    list_1 = s.split('\\r\\n')
    for i in list_1:
        print (':',i,file = open(output_file, '+a'))  # print return data
    # return list_1
    # return s
    if(content not in s):  # (value)
        print (f'bootfwversion Test Fail ({content})',file = open(t_file, '+a'))
    else:
        print (f'bootfwversion Test Pass ({content})',file = open(t_file, '+a'))

def printReturnMsg(msg,keyword,file_name):
    # get list
    my_list = msg.split('\\r\\n')
    if_find = False
    for i in my_list:
        if keyword in i:
            if_find = True
            print (i,file = open(file_name, '+a'))            
            break
    if(if_find == False):
        print (f'Not Found "{keyword}"',file = open(file_name, '+a'))            

# Test Start ===================================================== 
t_file = f'test_{time1}.txt'
file = open(t_file,'w+')

def Find_title(out,title,type=0):
    my_list = out.split('\\r\\n')
    for i in my_list: ### only return the first match one
        if(f'{title}' in i):
            temp = i.split(f'{title}')[1]
            if(type == 1):
                temp = temp.split()[2].split('\\')[0]
            return temp
            break
    return None

try:
    out = f('config',tnet_hndl,output_file)
    out = f('in genni 1',tnet_hndl,output_file)
    out = f('name "xxxxxxxxxxxxxxxname_31 x"',tnet_hndl,output_file)
    out = f('exit',tnet_hndl,output_file)
    out = f('exit',tnet_hndl,output_file)

    out = f('show version',tnet_hndl,output_file)
    my_list = out.split('\\r\\n')
    if_find = False
    for i in my_list:
        if('running image : ' in i):
            temp = i.split('running image : ')[1]
            if_find = True
            break
    # temp = out.split('\\r\\n')[1].split()[3]
    if(if_find == False):
        print ('"running image : " Not Found in return msg Test Fail ',file = open(t_file, '+a'))
    elif(data['bootfwversion'] != temp):       
        print (f"bootfwversion Test Fail ({data['bootfwversion']}!={temp})",file = open(t_file, '+a'))
    else:
        print (f"bootfwversion Test Pass ({data['bootfwversion']})",file = open(t_file, '+a'))

    out = f('show lc status < MSC >',tnet_hndl,output_file)
    out = f('show lcman status 17',tnet_hndl,output_file)
    my_list = out.split('\\r\\n')
    if_find = False
    for i in my_list:        
        index = i.find('image 1 version:') + 17
        if(index > 16):
            if_find = True
            target = i[index:]
            break    
    if(if_find == False):
        print ('image 1 version Not Found in return msg Test Fail ',file = open(t_file, '+a'))
    elif(data['fwimage1version'] != target):                              ###
        print (f"image 1 version Test Fail ({data['fwimage1version']}!={target})",file = open(t_file, '+a'))
    else:
        print (f"image 1 version Test Pass ({data['fwimage1version']})",file = open(t_file, '+a'))    
    if_find = False
    for i in my_list:        
        index = i.find('image 2 version:') + 17
        if(index > 16):
            if_find = True
            target = i[index:]
            break    
    if(if_find == False):
        print ('image 2 version Not Found in return msg Test Fail ',file = open(t_file, '+a'))
    elif(data['fwimage2version'] != target):                              ###
        print (f"image 2 version Test Fail ({data['fwimage2version']}!={target})",file = open(t_file, '+a'))
    else:
        print (f"image 2 version Test Pass ({data['fwimage2version']})",file = open(t_file, '+a'))

    out = f('show system',tnet_hndl,output_file)
    temp = Find_title(out,'Location: ')
    if(temp == None):
        print ('"Location: " Not Found in return msg Test Fail ',file = open(t_file, '+a'))
    elif(data['location'] not in temp):
        print (f'location Test Fail ({data["location"]}!={temp})',file = open(t_file, '+a'))
    else:
        print (f"location Test Pass ({data['location']})",file = open(t_file, '+a'))
    temp = Find_title(out,'Contact: ')
    if(temp == None):
        print ('"Contact: " Not Found in return msg Test Fail ',file = open(t_file, '+a'))
    elif(data['contact'] not in temp):
        print (f'contact Test Fail ([{data["contact"]}!={temp})',file = open(t_file, '+a'))
    else:
        print (f"contact Test Pass ({data['contact']})",file = open(t_file, '+a'))
    # if(data['macaddress'] not in temp):
    #     print ('MAC address Test Fail ', printReturnMsg(out,'MAC address',t_file),file = open(t_file, '+a'))
    temp = Find_title(out,'MAC address: ')
    if(temp == None):
        print ('"MAC address: " Not Found in return msg Test Fail ',file = open(t_file, '+a'))
    elif(data['macaddress'] not in temp):
        print (f'macaddress Test Fail ({data["macaddress"]}!={temp})',file = open(t_file, '+a'))
    else:
        print (f"MAC address Test Pass ({data['macaddress']})",file = open(t_file, '+a'))
 
    out = f('show snmp',tnet_hndl,output_file)              ###
    my_list = out.split('\\r\\n')
    if_find = False
    for i in my_list:
        index = i.find('trap community:') + 16
        if(index > 15):
            if_find = True
            target = i[index:]
            break    
    if(if_find == False):
        target = 'Not Found "trap community"'
    if(data['trapcommunity'] not in target):
        print (f"trap community Test Fail ({data['trapcommunity']}!={target})",file = open(t_file, '+a'))
    else:
        print (f"trap community Test Pass ({target})",file = open(t_file, '+a'))

    out = f('show ip',tnet_hndl,output_file)              ###
    my_list = out.split('\\r\\n')[4].split()
    if(data['ipconf']['iplist'][0]['interface'] != my_list[0]):
        print (f"interface Test Fail ({data['ipconf']['iplist'][0]['interface']}!={my_list[0]})",file = open(t_file, '+a'))
    else:
        print (f"interface Test Pass ({my_list[0]})",file = open(t_file, '+a'))
    if(data['ipconf']['iplist'][0]['ip'] != my_list[1]):
        print (f"ip Test Fail ({data['ipconf']['iplist'][0]['ip']}!={my_list[1]})",file = open(t_file, '+a'))
    else:
        print (f"ip Test Pass ({my_list[1]})",file = open(t_file, '+a'))
    if(data['ipconf']['iplist'][0]['mask'] != my_list[2]):
        print (f"mask Test Fail ({data['ipconf']['iplist'][0]['mask']}!={my_list[2]})",file = open(t_file, '+a'))
    else:
        print (f"mask Test Pass ({my_list[2]})",file = open(t_file, '+a'))
    if(data['ipconf']['iplist'][0]['gateway'] != my_list[3]):
        print (f"gateway Test Fail ({data['ipconf']['iplist'][0]['gateway']}!={my_list[3]})",file = open(t_file, '+a'))
    else:
        print (f"gateway Test Pass ({my_list[3]})",file = open(t_file, '+a'))
    if(str(data['ipconf']['iplist'][0]['vid']) != str(my_list[4])):
        print (f"vid Test Fail ({data['ipconf']['iplist'][0]['vid']}!={my_list[4]})",file = open(t_file, '+a'))
    else:
        print (f"vid Test Pass ({my_list[4]})",file = open(t_file, '+a'))
    
    out = f('show lc st 17',tnet_hndl,output_file)              ###
    temp = out.split('\\r\\n')[1].split('slot')
    if(str(data['slotinfo'][16]['slot']) not in str(temp)):
        print (f"slot 17 Test Fail ({data['slotinfo'][16]['slot']}!={temp})",file = open(t_file, '+a'))
    else:
        print (f"slot 17 Test Pass ({data['slotinfo'][16]['slot']})",file = open(t_file, '+a'))
    # temp = out.split('\\r\\n')[2].split()[2]
    temp = Find_title(out,'name  : ')
    if(temp == None):
        print ('"name  : " Not Found in return msg Test Fail ',file = open(t_file, '+a'))
    elif(str(data['slotinfo'][16]['type']) not in str(dict_cardtype[temp.lower()])):
        print (f"name Test Fail ({data['slotinfo'][16]['type']}!={dict_cardtype[temp.lower()]} {temp})",file = open(t_file, '+a'))
    else:
        print (f"name Test Pass ({data['slotinfo'][16]['type']} {temp})",file = open(t_file, '+a'))
    # temp = out.split('\\r\\n')[18].split()[3]
    temp = Find_title(out,'hardware version        : ')
    if(temp == None):
        print ('"hardware version        : " Not Found in return msg Test Fail ',file = open(t_file, '+a'))
    elif(str(data['slotinfo'][16]['hwversion']) not in str(temp)):
        print (f"hardware version Test Fail ({data['slotinfo'][16]['hwversion']}!={temp})",file = open(t_file, '+a'))
    else:
        print (f"hardware version Test Pass ({data['slotinfo'][16]['hwversion']})",file = open(t_file, '+a'))
    # temp = out.split('\\r\\n')[20].split()[3]
    temp = Find_title(out,'firmware version        : ')
    if(temp == None):
        print ('"firmware version        : " Not Found in return msg Test Fail ',file = open(t_file, '+a'))
    elif(str(data['slotinfo'][16]['fwversion']) not in str(temp)):
        print (f"firmware version Test Fail ({data['slotinfo'][16]['fwversion']}!={temp})",file = open(t_file, '+a'))
    else:
        print (f"firmware version Test Pass ({data['slotinfo'][16]['fwversion']})",file = open(t_file, '+a'))
    # temp = out.split('\\r\\n')[19].split()[4]
    temp = Find_title(out,'hardware serial number  : ')
    if(temp == None):
        print ('"hardware serial number  : " Not Found in return msg Test Fail ',file = open(t_file, '+a'))
    elif(str(data['slotinfo'][16]['serialnumber']) not in str(temp)):
        print (f"hardware serial number Test Fail ({data['slotinfo'][16]['serialnumber']}!={temp})",file = open(t_file, '+a'))
    else:
        print (f"hardware serial number Test Pass ({data['slotinfo'][16]['serialnumber']})",file = open(t_file, '+a'))
    print (f"...operstatus...",file = open(t_file, '+a'))
    print (f"...adminstate...",file = open(t_file, '+a'))
    print (f"...alarmstate...",file = open(t_file, '+a'))
    
    # GENNI
    out = f('show lc status < MSC >',tnet_hndl,output_file)     
    slot = '9' #????           ###
    out = f(f'show lcman status {slot}',tnet_hndl,output_file)  ####  MSC slot
    # temp = out.split('\\r\\n')[2].split()[2]
    temp = Find_title(out,'name  : ')
    if(temp == None):
        print ('"name  : " Not Found in return msg Test Fail ',file = open(t_file, '+a'))
    elif(str(data['portinfo'][0]['name']) != str(dict_cardtype[temp.lower()])):
        print (f"name Test Fail ({data['portinfo'][0]['name']}!={dict_cardtype[temp.lower()]} {temp})",file = open(t_file, '+a'))
    else:
        print (f"name Test Pass ({str(data['portinfo'][0]['name'])})",file = open(t_file, '+a'))
    
    out = f('show interface genni 1 status',tnet_hndl,output_file)          ###
    temp = out.split('\\r\\n')[4].split()[0]
    if(str(data['portinfo'][0]['port']) not in str(temp)):
        print (f"port Test Fail ({data['portinfo'][0]['port']}!={temp})",file = open(t_file, '+a'))
    else:
        print (f"port Test Pass ({data['portinfo'][0]['port']})",file = open(t_file, '+a'))
    print (f"...type...",file = open(t_file, '+a'))
    temp = out.split('\\r\\n')[4].split()[2]
    if(str(data['portinfo'][0]['operstatus']) not in str(temp)):
        print (f"operstatus Test Fail ({data['portinfo'][0]['operstatus']}!={temp})",file = open(t_file, '+a'))
    else:
        print (f"operstatus Test Pass ({data['portinfo'][0]['operstatus']})",file = open(t_file, '+a'))
    temp = out.split('\\r\\n')[4].split()[3]
    if(str(data['portinfo'][0]['rate']) not in str(dict_rate[temp])):
        print (f"rate Test Fail ({data['portinfo'][0]['rate']}!={dict_rate[temp]})",file = open(t_file, '+a'))
    else:
        print (f"rate Test Pass ({data['portinfo'][0]['rate']})",file = open(t_file, '+a'))
    
    
    out = f('show ru interface genni 1',tnet_hndl,output_file)              ###
    print (f"...name...",file = open(t_file, '+a'))
    print (f"...adminstate...",file = open(t_file, '+a'))
    print (f"...linetemplate...",file = open(t_file, '+a'))
    print (f"...alarmtemplate...",file = open(t_file, '+a'))
    print (f"...upstreamrate...",file = open(t_file, '+a'))
    print (f"...downstreamrate...",file = open(t_file, '+a'))
    print (f"...rate...",file = open(t_file, '+a'))
    print (f"...fiberstatus...",file = open(t_file, '+a'))
    
    slot = '17'
    port='1'
    ont = '128'
    out = f('sh in remote x 17-1-128 status',tnet_hndl,output_file) 
    temp = Find_title(out,'AID',1)             ###
    if(str(data['xontinfo'][0]['slot']) != temp.split('-')[0]):
        print (f"slot Test Fail ({data['xontinfo'][0]['slot']}!={temp.split('-')[0]})",file = open(t_file, '+a'))
    else:
        print (f"slot Test Pass ({data['xontinfo'][0]['slot']})",file = open(t_file, '+a'))
    if(str(data['xontinfo'][0]['port']) != temp.split('-')[1]):
        print (f"port Test Fail ({data['xontinfo'][0]['port']}!={temp.split('-')[1]})",file = open(t_file, '+a'))
    else:
        print (f"port Test Pass ({data['xontinfo'][0]['port']})",file = open(t_file, '+a'))
    if(str(data['xontinfo'][0]['ontid']) != temp.split('-')[2]):
        print (f"ontid Test Fail ({data['xontinfo'][0]['ontid']}!={temp.split('-')[2]})",file = open(t_file, '+a'))
    else:
        print (f"ontid Test Pass ({data['xontinfo'][0]['ontid']})",file = open(t_file, '+a'))
    # sn, pw, ontstate vendorid vendorversion bootversion
    temp = Find_title(out,'SN',1)
    if(temp == None):
        print ('"SN" Not Found in return msg Test Fail ',file = open(t_file, '+a'))
    elif(str(data['xontinfo'][0]['sn']) != str(temp)):
        print (f"sn Test Fail ({data['xontinfo'][0]['sn']}!={temp})",file = open(t_file, '+a'))
    else:
        print (f"sn Test Pass ({str(data['xontinfo'][0]['sn'])})",file = open(t_file, '+a'))
    print (f"...pw...",file = open(t_file, '+a'))
    temp = Find_title(out,'Status',1)
    if(temp == None):
        print ('"Status" Not Found in return msg Test Fail ',file = open(t_file, '+a'))
    elif(str(data['xontinfo'][0]['ontstate']) != str(temp)):
        print (f"ontstate Test Fail ({data['xontinfo'][0]['ontstate']}!={temp})",file = open(t_file, '+a'))
    else:
        print (f"ontstate Test Pass ({str(data['xontinfo'][0]['ontstate'])})",file = open(t_file, '+a'))
    temp = Find_title(out,'Vendor ID',1)
    if(temp == None):
        print ('"Vendor ID" Not Found in return msg Test Fail ',file = open(t_file, '+a'))
    elif(str(data['xontinfo'][0]['vendorid']) != str(temp)):
        print (f"vendorid Test Fail ({data['xontinfo'][0]['vendorid']}!={temp})",file = open(t_file, '+a'))
    else:
        print (f"vendorid Test Pass ({str(data['xontinfo'][0]['vendorid'])})",file = open(t_file, '+a'))
    temp = Find_title(out,'Vendor version',1)
    if(temp == None):
        print ('"Vendor version" Not Found in return msg Test Fail ',file = open(t_file, '+a'))
    elif(str(data['xontinfo'][0]['vendorversion']) != str(temp)):
        print (f"vendorversion Test Fail ({data['xontinfo'][0]['vendorversion']}!={temp})",file = open(t_file, '+a'))
    else:
        print (f"vendorversion Test Pass ({str(data['xontinfo'][0]['vendorversion'])})",file = open(t_file, '+a'))
    print (f"...bootversion...",file = open(t_file, '+a'))


    out = f('sh in remote x 17-1-128 config',tnet_hndl,output_file)              ###
    
    out = f('sh in remote x 17-1-128 wan-status',tnet_hndl,output_file)              ###
    

except Exception as e:
    tnet_hndl.close() 
    print(e)
    raise Exception
# out = f('show lc st 17',tnet_hndl,output_file)              ###
# data['slotinfo'][16]['slot']
# data['slotinfo'][16]['type']
# data['slotinfo'][16]['operstatus']
# data['slotinfo'][16]['adminstate']
# data['slotinfo'][16]['alarmstate']
# data['slotinfo'][16]['hwversion']
# data['slotinfo'][16]['fwversion']
# data['slotinfo'][16]['serialnumber']


try:
    tnet_hndl.close()
except Exception as e:
    print(e)
    raise Exception