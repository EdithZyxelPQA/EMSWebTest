import telnetlib
import inspect
import time
try:
    from loguru import logger
except ImportError:  # Python311 used for ChassisConfigTest has no loguru
    import logging
    logger = logging.getLogger("telnet_module")

def Run_Telnet_Func( title="", msg="", cmd=""):

    # _url_ip = variables_module.url_ip
    # ========================= Telnet ================================

    def Input_cmd_func(input_cmd_file_name):
        # Get command from txt
        f = open(input_cmd_file_name,'r', encoding="utf-8")
        My_List = []
        done = 0
        while (not done):
            aline = f.readline()
            if(aline!=''):
                My_List.append(aline.strip())
            else:
                done = 1
        return My_List

    def Telnet_func(host_ip,My_List,output_file, _type=0):	

        # print(f"\n====================== START ======================\n",file = open(output_file, '+a'))  

        def wait_for_specific_words(tn,words):
            while True:
                output = tn.read_until(b"\n").decode("utf-8")
                output = str(output)
                for word in words:
                    if(word.decode("utf-8") in output):
                        break
        wordds = [b"# ",b"-- more --, next page: Space, continue: c, quit: ESC"]


        username = 'admin'
        password = '1234'
        # print('- - - - - - - - - - - - - - - - - - - - - - - - - -',file = open(output_file, '+a'))
        # print(f'>>> Telnet {host_ip}',file = open(output_file, '+a'))
        logger.info(f"Telnet {host_ip}")
        tnet_hndl = telnetlib.Telnet(host_ip)
        if(_type==1):
            # print(tnet_hndl.read_until(b"User name: "),file = open(output_file, '+a'))
            tnet_hndl.read_until(b"User name: ")
            tnet_hndl.write(username.encode('ascii') + b"\n")
        else:
            # print(tnet_hndl.read_until(b"login: "),file = open(output_file, '+a')) # for IES52xx
            tnet_hndl.read_until(b"login: ")
            tnet_hndl.write(username.encode('ascii') + b"\n")
        # print(tnet_hndl.read_until(b"Password: "),file = open(output_file, '+a'))
        tnet_hndl.read_until(b"Password: ")
        tnet_hndl.write(password.encode('ascii') + b"\n")
        # print(tnet_hndl.read_until(b"# "),file = open(output_file, '+a'))
        tnet_hndl.read_until(b"# ")
        list_1 = ["(no resp)"]
        for cmd in My_List:

            logger.info(f'[Telnet] "{cmd}"')
            # cmd = cmd.decode('utf-8', errors='ignore') if isinstance(cmd, (bytes, bytearray)) else str(cmd)

            if((cmd=="c")or(cmd=="y")):
                cmd = bytes(cmd, encoding='UTF-8')
                tnet_hndl.write(cmd)
            else:
                cmd = bytes(cmd, encoding='UTF-8')
                tnet_hndl.write(cmd + b"\n")
            # if ((cmd == "admin" or cmd == "1234") or cmd == "li supervisor") or "lcman debug " in cmd:
            # if cmd in {b"admin", b"1234", b"li supervisor"} or cmd.startswith(b"lcman debug "):
            #     pass
            # else:                
            #     print(cmd,file = open(output_file, '+a'))  # print command

            time.sleep(0) # 1 # 0.3

            # print('- - - - - - - - - - - - - - - - - - - - - - - - - -',file = open(output_file, '+a'))
            if_find = False
            for i in range(3):
                set_timeout = 5
                if(i>0):
                    set_timeout = 20
                for wor in wordds:
                    # print(f'start read until {wor}')
                    try:
                        # list_1 = str(tnet_hndl.read_until(wor,timeout=10)).split('\\r\\n')
                        list_1 = str(tnet_hndl.read_until(wor,timeout=set_timeout)).split('\\r\\n')
                        if_find = True
                        # print(f'read until {wor} pass')
                        break
                    except ConnectionResetError as e:
                        print(f'{cmd} //read until {wor} fail ({i+1}t)')
                        print('timeout occurred')
                        continue
                if(if_find == True):
                    break
            if(if_find == False):
                print(f"'{cmd}' //read until all words fail",file = open(output_file, '+a'))

            list_1.pop(0) ### delete the first line
            if cmd == b"admin" or cmd == b"1234":
                pass
            elif b"li supervisor" not in cmd and b"lcman debug " not in cmd:
                for i in list_1:
                    # print(f':{i}',file = open(output_file, '+a'))  # print return data
                    logger.info(f':{i}')

                # print('\n',file = open(output_file, '+a'))
                # print('- - - - - - - - - - - - - - - - - - - - - - - - - -',file = open(output_file, '+a'))
        tnet_hndl.close()
        return list_1

        # print(f"\n====================== DONE. ======================\n",file = open(output_file, '+a'))  

    My_List = []  
    if isinstance(cmd,list):
        My_List = cmd
    else:
        telnet_command = f"""
        {cmd}
        """
        for line in telnet_command.strip().split("\n"):
            My_List.append(line.strip())

    output_file = 'telnet_log.log'
    # output_file_f = open('Output/telnet_log.txt',"w+")
    # print(f"[MSAN-{title}]",file = open(output_file, '+a'))
    print(f"{title}",file = open(output_file, '+a'))
    msg = msg.replace("\n","\n         ")
    print(f"Message: {msg}",file = open(output_file, '+a'))



    # # 取得 frame 資訊
    # frame_info = inspect.stack()[1]  # [0] 是自己，[1] 是呼叫處     
    # filename = frame_info.filename                                                                                                                                                                                                                                     
    # lineno = frame_info.lineno
    # function_name = frame_info.function
    # print(f"* Now inside function: {function_name} () @ {filename}:{lineno}",file = open(output_file, '+a'))
    # logger.info(f"* Now inside function: {function_name} () @ {filename}:{lineno}")
    # # 取得前幾行程式碼
    # print("Previous 10 lines of code:",file = open(output_file, '+a'))
    # start = max(1, lineno - 10)
    # for i in range(start, lineno + 1):
    #     code_line = linecache.getline(filename, i).rstrip()
    #     print(f"{i}: {code_line}",file = open(output_file, '+a'))
    _url_ip="192.168.169.88"
    resp = Telnet_func(_url_ip,My_List,output_file, _type=0)


def bulk_config(ip, cmds, username="admin", password="1234", timeout=15):
    """Run many config-mode commands quickly over one telnet session.
    Returns (error_list, elapsed_sec); error_list holds (cmd, output) for commands whose output looks like an error."""
    start = time.time()
    tn = telnetlib.Telnet(ip, timeout=timeout)
    tn.read_until(b"login: ", timeout)
    tn.write(username.encode('ascii') + b"\n")
    tn.read_until(b"Password: ", timeout)
    tn.write(password.encode('ascii') + b"\n")
    tn.read_until(b"# ", timeout)
    tn.write(b"configure\n")
    tn.read_until(b"(config)# ", timeout)
    errors = []
    for cmd in cmds:
        tn.write(cmd.encode('ascii') + b"\n")
        out = tn.read_until(b"(config)# ", timeout).decode("utf-8", errors="ignore")
        if not out.endswith("(config)# "):
            errors.append((cmd, "timeout: " + out[-200:]))
        elif "%" in out or "rror" in out or "nvalid" in out or "full" in out:
            errors.append((cmd, out.strip()[-200:]))
    tn.write(b"exit\n")
    tn.read_until(b"# ", timeout)
    tn.write(b"exit\n")
    tn.close()
    elapsed = time.time() - start
    logger.info(f"[Telnet] bulk_config {ip}: {len(cmds)} cmds, {len(errors)} errors, {elapsed:.0f}s")
    return errors, elapsed


class Telnet():
    def __init__(self,ip="192.168.169.88", username="admin", password="1234"):
        logger.info(f"[Telnet] Host IP {ip}")
        self.host_ip = ip #"192.168.169.81" if ip == None else ip
        self.username = username #"admin" if username == None else username
        self.password = password # "1234" if password == None else password
        self.tnet = telnetlib.Telnet(self.host_ip)
        self.login()

    def login(self):
        # pass

        _type = 0
        if(_type==1):
            self.tnet.read_until(b"User name: ")
            self.tnet.write(self.username.encode('ascii') + b"\n")
        else:
            self.tnet.read_until(b"login: ")
            self.tnet.write(self.username.encode('ascii') + b"\n")
        self.tnet.read_until(b"Password: ")
        self.tnet.write(self.password.encode('ascii') + b"\n")
        self.tnet.read_until(b"# ")        

    def send(self, cmd, if_set_timeout=1):
        wordds = [b"# ",b"-- more --, next page: Space, continue: c, quit: ESC"]
        list_1 = ["(no resp)"]
        if if_set_timeout == 0:
            logger.info(f'[Telnet] "{cmd}" (no wait #)')
        else:
            logger.info(f'[Telnet] "{cmd}"')
        # cmd = cmd.decode('utf-8', errors='ignore') if isinstance(cmd, (bytes, bytearray)) else str(cmd)
        if((cmd=="c")or(cmd=="y")):
            cmd = bytes(cmd, encoding='UTF-8')
            self.tnet.write(cmd)
        else:
            cmd = bytes(cmd, encoding='UTF-8')
            self.tnet.write(cmd + b"\n")

        if_find = False
        # for i in range(3):
        #     set_timeout = 5
        #     if(i>0):
        #         set_timeout = 120 #20
        #     for wor in wordds:
        #         try:
        #             list_1 = str(self.tnet.read_until(wor,timeout=set_timeout)).split('\\r\\n')
        #             if_find = True
        #             # print(f'read until {wor} pass')
        #             logger.debug(f'[Telnet] read until {wor} pass')
                    
        #             logger.debug(f'[Telnet] resp')
        #             for i in list_1:
        #                 logger.debug(f'[Telnet]     :{i}')
                        

        #             break
        #         except ConnectionResetError as e:
        #             logger.warning(f'[Telnet] {cmd} //read until {wor} fail ({i+1}t), timeout occurred')
        #             continue
        #     if(if_find == True):
        #         break
        # if(if_find == False):
        #     logger.error(f"'[Telnet] {cmd}' //read until all words fail")
        for i in range(3):
            set_timeout = 5
            if(i>0):
                set_timeout = 120 #20
            for wor in wordds:
                try:
                    data = self.tnet.read_until(wor, timeout=set_timeout)
                    text = data.decode("utf-8", errors="ignore")

                    # 💡 把讀到的內容同步到 list_1
                    list_1 = text.split('\r\n')

                    if if_set_timeout != 0:
                        if data.endswith(wor):
                            # ✅ 真的讀到 # 或 -- more --
                            if_find = True
                            logger.debug(f'[Telnet] read until {wor!r} pass')
                        else:
                            # ❌ timeout：沒有找到 wor，只是把目前 buffer 交出來
                            logger.warning(f'[Telnet] timeout before {wor!r}, got (len={len(data)}): {text!r}')
                            continue  # 換下一個 wor 或下一輪 i
                    else:
                        if_find = True
                        break

                    logger.debug('[Telnet] resp')
                    for line in text.split('\r\n'):
                        logger.debug(f'[Telnet]     :{line}')
                    break  # 離開 for wor
                except ConnectionResetError:
                    logger.warning(f'[Telnet] {cmd} //read until {wor!r} fail ({i+1}t), connection reset')
                    continue
                except Exception as e:
                    logger.error(f'[Telnet] Exception:{e}')
                    break
            if if_find:
                break
        if(if_find == False):
            logger.error(f"'[Telnet] {cmd}' //read until all words fail")

        # list_1.pop(0) ### delete the first line
        # # if cmd == b"admin" or cmd == b"1234":
        # #     pass
        # # elif b"li supervisor" not in cmd and b"lcman debug " not in cmd:

        if list_1 and list_1[0] == "(no resp)":
            # 真的沒東西
            list_1 = []
        elif list_1:
            # 刪掉第一行（通常是 echo 或 prompt）
            list_1.pop(0)

        string=""
        for i in list_1:
            string += i + ""
            # logger.info(f'[Telnet] :{i}')
        if len(list_1) != 0:
            logger.info(f'[Telnet] resp:\n{string}')
        return list_1


    def close(self):
        self.tnet.close()
        logger.info("[Telnet] Close Telnet.")