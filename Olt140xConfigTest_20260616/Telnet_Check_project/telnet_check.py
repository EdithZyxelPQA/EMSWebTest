# pip install paramiko
import random
import os
import telnetlib
import time
import datetime
import json
import paramiko
import ftplib
from contextlib import closing

# START Main Func ====================================================================================================


# output_file = f'output_{str(datetime.datetime.now()).split(":")[0]}{str(datetime.datetime.now()).split(":")[1]}.txt'
output_file = f'output_command.txt'
file = open(output_file,'w+')


# fetch data ======================
with open('data.json') as f:
    data = json.load(f)
telnet_ip = data['telnet_ip']
username = data['username']
password = data['password']
ssh_ip = data['ssh_ip']
ssh_password = data['ssh_password']
# =================================

# Telnet -----------------------------------------------------------------------------------------
print('Telnet')
host_ip = telnet_ip  
cmd1 = ['location "L_Zyxel_EM_PQA_4F_IES5206_OLC3708-43A_OLC3416-42_IES4204QA_GLC1440X-55_OLC3416-42_CecilyChi_DUT_systemLocation_2023_@auto_end !"',
       'contact "C_Zyxel_EM_PQA_4F_IES5206_OLC3708-43A_OLC3416-42_IES4204QA_GLC1440X-55_OLC3416-42_CecilyChi_DUT_systemContact_2022_@auto_end !"',
       'exit',
       '',
       
       #
       
       'in genni 1',
       'name "xxxxxxxxxxxxxxxGenni_name_31 x"',
       'exit',
       'in gpon 10-16',
       'name "xxxxxxxxxxxxxxxxGPON_name_31 x"',
       'tel "xxxxxxxxxxxxxxxxxGPON_tel_31 x"',
       'exit',
       'in ge 16-1',
       'name "xxxxxxxxxxxxxxxxxxGe_name_31 x"',
       'tel "xxxxxxxxxxxxxxxxxxxGe_tel_31 x"',
       'exit',
       'in xpon 17-1',
       'name "xxxxxxxxxxxxxxxxXPON_name_31 x"',
       'exit',
       'xpon uni-profile wanip',
       'port veip tag-oper-id 1',
       'uniport-list 1',
       'filter uni-vlan 7',
       'vlan 7',
       'exit',
       'exit',
       'xpon ont-profile wanip',
       'ontServiceControl http enable ALL',
       'ontWan 1',
       'default',
       'enable',
       'ip nat',
       'ip dynamic',
       'vlan 7 priority 7 mvlan 7',
       'exit',
       'exit',
       'xpon qos bwprof 1G',
       'sir 0 air 0 pir 1000000',
       'exit',
       'xpon service-profile wanip',
       'mode veip',
       'port lan 1',
       'vlan 7',
       'mapper-pbit 0,1,2,3,4,5,6,7',
       'exit',
       'xpon template wanip',
       'service 1 service-profile wanip shared-priority 7 usbwprof 1G dsbwprof 1G',
       'tcont 1 services 1',
       'uni-profile wanip',
       'ont-profile wanip',
       'exit',
       'in remote x 17-1-128',
       'sn ZYYG4B5DB78F',
       'reg DEFAULT',
       'des "xxxxxxxxxxxxxxxxxXONT_des_31 x"',
       'temp wanip',
       'no inac',
       'exit',
       
       
       
       #
       'linux supervisor',
       'cd /tmp/emsUpload/',
       'ls',
       'cat dev_data',
       'cat perf_data',
       'cat dev.log',
       'exit',
       'linux supervisor',
       'cd /home/admin',
       'snmpset -v 2c -c public 192.168.169.86 1.3.6.1.4.1.890.1.5.13.13.16.21.1.0 s "192.168.169.86"',
       'snmpset -v 2c -c public 192.168.169.86 1.3.6.1.4.1.890.1.5.13.13.16.21.2.0 s "https://192.168.128.8/RESTfulServer/Server/DevicePollerDebug/"',
       'snmpset -v 2c -c public 192.168.169.86 1.3.6.1.4.1.890.1.5.13.13.16.21.2.0 s "https://192.168.128.8/RESTfulServer/Server/DevicePoller/"'
       ]
print('1')    
tnet_hndl = telnetlib.Telnet(host_ip)
print (tnet_hndl.read_until(b"login: "),file = open(output_file, '+a'))
tnet_hndl.write(username.encode('ascii') + b"\n")
print (tnet_hndl.read_until(b"Password: "),file = open(output_file, '+a'))
tnet_hndl.write(password.encode('ascii') + b"\n")
print (tnet_hndl.read_until(b"# "),file = open(output_file, '+a'))
tnet_hndl.write(b"config" + b"\n")
print (tnet_hndl.read_until(b"# "),file = open(output_file, '+a'))
for com in cmd1:    
    print(com,file = open(output_file, '+a'))  # print command
    com = bytes(com, encoding='UTF-8')
    # tnet_hndl.write(com.encode('ascii') + b"\n")
    tnet_hndl.write(com + b"\n")
    # print (':',str(tnet_hndl.read_until(b"# ")).split('\\r\\n')[1],file = open(output_file, '+a'))  # print return data
    list_1 = str(tnet_hndl.read_until(b"# ")).split('\\r\\n')
    for i in list_1:
        print (':',i,file = open(output_file, '+a'))  # print return data
tnet_hndl.close()

# Ssh ------------------------------------------------------------------------------------
print('SSH')
print('\nSSH\n',file = open(output_file, '+a')) 
# cmd = ['cd /opt/ELEMENTVIEW_MASTER/bin/',
#        'ls'           
#        ]
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=ssh_ip, username=username, password=ssh_password)


# com = 'sudo su'
def channel_exe(channel, cmd, t=0.2):
    channel.send(cmd)
    channel.send('\n')
    import time
    time.sleep(t)
    resp = channel.recv(9999).decode("utf8")
    print(cmd)
    print(resp)
    return resp

channel_ssh = ssh.invoke_shell()

com = f'cd /opt/ELEMENTVIEW_MASTER/bin/'
channel_exe(channel_ssh, com)
com = f'ls'
channel_exe(channel_ssh, com)
com = 'sudo su'
if(f"password for {username}" in channel_exe(channel_ssh, com)):
    print('111')
    com = ssh_password
    channel_exe(channel_ssh, com)
    print('111')
com = f'chmod 777 {telnet_ip}'
channel_exe(channel_ssh, com)
com = f'ls'
channel_exe(channel_ssh, com)

# channel_ssh.close()

# ssh.close()



# Ftp -----------------------------------------------------------------------------
print('FTP')
print ('\nFTP\n',file = open(output_file, '+a'))
count = 0
if_pass = False
while((if_pass == False) and count < 1):
    with closing(ftplib.FTP(ssh_ip)) as ftp:

        
        try:
            # ftp.set_debuglevel(2)
            ftp.login(username,ssh_password)
            
            # ftp.cwd('opt/ELEMENTVIEW_MASTER/bin/192.168.169.86')
            ftp.cwd('/opt/ELEMENTVIEW_MASTER/bin')
            # ftp.cwd('/opt')
            # ftp.retrlines('LIST')
            # ftp.cwd('ELEMENTVIEW_MASTER')
            # ftp.retrlines('LIST')
            # ftp.cwd('bin')
            ftp.retrlines('LIST')
            # ftp.cwd('192.168.169.86')

            
            # localfile = open('d:/'+telnet_ip+'','wb')    # 本地端要儲存的檔案
            localfile = open('d:/'+telnet_ip+'.json','wb')    # 本地端要儲存的檔案
            # localfile = open('d:/'+telnet_ip+'.txt','wb')    # 本地端要儲存的檔案
            ftp.retrbinary('RETR ' + telnet_ip, localfile.write)    # 下載檔案

            # ftp.sendcmd(f'get {telnet_ip} d:/{telnet_ip}.json')   /// X
        except ftplib.error_perm as error:
            print ('*** ftp Fail ***   ',error,file = open(output_file, '+a'))
            print (error)

        # try:    
        #     ftp.login(username,ssh_password)
        #     # ftp.retrlines('LIST')
        #     # print(ftp.pwd())
        #     # ftp.cwd(ftp.pwd()+'/'+'opt/ELEMENTVIEW_MASTER/bin/')
        #     # print('pwd:',ftp.pwd())
        #     # ftp.retrlines('LIST')
        #     # # ftp.cwd('Templates')
        #     # ftp.cwd('../')
        #     # ftp.retrlines('LIST')
        #     # ftp.cwd('../')
        #     # ftp.retrlines('LIST')
        
        #     # ftp.cwd(ftp.pwd()+'/'+'opt/ELEMENTVIEW_MASTER/bin/')
        #     # ftp.retrlines('LIST')

        #     ftp.cwd('/opt/ELEMENTVIEW_MASTER/bin/192.168.169.86')
        #     print(ftp.retrlines('LIST'))

        #     # cd opt/ELEMENTVIEW_MASTER/bin/   //// get opt/ELEMENTVIEW_MASTER/bin/192.168.169.86 d:/192.168.169.86.txt
        #     msg = ftp.sendcmd(f'get {telnet_ip} d:/{telnet_ip}.json')
        #     # msg = ftp.sendcmd(f'get opt/ELEMENTVIEW_MASTER/bin/{telnet_ip} d:/{telnet_ip}.json')
        #     print(msg)
        #     if_pass = True
        #     break
            
        # except ftplib.error_perm as error:
        #     print ('*** ftp Fail ***   ',error,file = open(output_file, '+a'))
        #     print (error)


        

    try:
        ftp.quit()
    except:
        pass
    try:
        ftp.close()
    except:
        pass

    count += 1

channel_ssh.close()
ssh.close()    


# Check file ---------------------------------------------------------------------
# output_file = f'output_{str(datetime.datetime.now()).split(":")[0]}{str(datetime.datetime.now()).split(":")[1]}.txt'
# file = open(output_file,'w+')
# set_up_file = open(f'd:/{telnet_ip}.txt','r')
# lines = set_up_file.readlines()
# set_up_file.close()
# location = lines[4].split('"')[3]
# contact = lines[4].split('"')[3]
# if(location != cmd1[0].split('"')[1]):
#     print('fail')



# Telnet -------------------------------------------------------------------------
# cmd2 = ['show version',
#        'show lc status < MSC >',
#        'show system',
#        'show snmp',
#        'show ip',
#        'show lc st 17',

#        'show lc status < MSC >',
#        'show interface genni 1 status',
#        'show ru interface genni 1']
# tnet_hndl = telnetlib.Telnet(host_ip)
# print (tnet_hndl.read_until(b"login: "),file = open(output_file, '+a'))
# tnet_hndl.write(username.encode('ascii') + b"\n")
# print (tnet_hndl.read_until(b"Password: "),file = open(output_file, '+a'))
# tnet_hndl.write(password.encode('ascii') + b"\n")
# print (tnet_hndl.read_until(b"# "),file = open(output_file, '+a'))
# for com in cmd2:    
#     print(com,file = open(output_file, '+a'))  # print command
#     tnet_hndl.write(com.encode('ascii') + b"\n")
#     list_1 = str(tnet_hndl.read_until(b"# ")).split('\\r\\n')
#     for i in list_1:
#         print (':',i,file = open(output_file, '+a'))  # print return data
# tnet_hndl.close()

# Check file -------------------------------------------------------------------------------

# with open(f'd:/192.168.169.86.json') as f:
#     json.load(f)
# with open(f'd:/192.168.169.86.json') as f:
#     data = json.load(f)
#     print(data)
# import sys
# sys.path.append(r'D:\\zh_memo\\Telnet_Check_project\\temp.py')
# import temp
# temp.dump()
# temp.prin()
# temp.test()


# with open(f'd:/192.168.169.86_test.json') as f:
#         data = json.load(f,strict=False)
#         print(data)

# # // text file to json file
# f = open('d:/192.168.169.86.txt','r')
# f_txt = f.read()
# f.close()
# # print(f_txt)

# print('0 lines')
# with open('d:/192.168.169.86.json','w') as f:
#     json.dump(f_txt, f, indent = 4)
#     # data = json.load(f,strict=False)
#     # print(data)

print('00')

# if_pass = False
# count = 0
# while(if_pass==False and count < 4):
#     try:
#         with open('d:/192.168.169.86_7.json') as f:
#             data = json.load(f,strict=False)
#             print(data)
#         if_pass = True
#         break
#     except:
#         count +=1

print('11')
# import temp


# with open('d:/192.168.169.86.json') as f:
#         data = json.load(f,strict=False)
#         print(data)


# set_up_file = open(f'd:/{telnet_ip}.txt','r')
# lines = set_up_file.readlines()
# set_up_file.close()
# location = lines[4].split('"')[3]
# contact = lines[4].split('"')[3]





# file.close()




# test...
# JSON_file = 
# with open(JSON_file) as f:
#     data = json.load(f,strict=False)