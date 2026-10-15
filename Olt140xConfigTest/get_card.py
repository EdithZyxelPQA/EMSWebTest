import time
import selenium_module as mod


def get_card_case(driver,glc_port,pon_x_1_aid,pon_1_aid,file_name=''):
    MSC_card = ""
    MSC_slot = ""
    cardtype_case = 0
    list1 = []            # case, slot, port (str each element)
    if_no_card = False
    
    # Home, get active card type ---
    dict1={}
    for test in range(5):
        time.sleep(5) 
        mod.Switch_Default(driver)
        mod.Page_Switch(driver,"Home")
        time.sleep(2)
        mod.Page_Switch(driver,"Home")
        mod.Switch_Frame(driver)
        time.sleep(2)
        for index in range(driver.find_elements('class name',"SysinfoList").__len__()):    

            # WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located(driver.find_elements(By.CLASS_NAME, "td-table-content.SysinfoState")[index]))

            time.sleep(2)
            
            if(driver.find_elements('class name',"td-table-content.SysinfoState")[index].text == "active"):            
                slot_n = driver.find_elements('class name',"td-table-content.i1")[index].text
                cardtype_n = driver.find_elements('class name',"td-table-content.SysinfoCardType.left-wrapper")[index].text
                # dict1[slot_n]=cardtype_n        
                dict1[cardtype_n] = slot_n     

        if(len(dict1) == 0):
            # print(f"no active card",file = open(file_name, '+a'))        
            print(f"no active card")        
            if_no_card = True
            # test_report.close()
            # driver.quit()    
            # exit
            print(f"no active card")
            print(f"Get Active Card Fail. Retry?")
            # raise Exception ("Get Active Card Fail. Retry?")
            input("...")
        else:
            break
        if(test == 4):
            raise Exception ("Get Active Card Fail. Retry?")
        
    print(f"dict1:{dict1}")

    print(dict1.keys())
    for i in dict1.keys():
        # print("....")
        # print("i:"+i)
        # =
        
        # CASE 1
        # (GLC)
        if(("GLC1440X" in i) or ("GLC1540X" in i)):                                                                           # GLC
            cardtype_case = 1
            # print("in case (1) GLC1440X, GLC1540X")        
            # print('{:>20}'.format(f"{i} slot:{dict1[i]},"))
            # print(f"slot:{dict1[i]} {i}, in case (1) GLC1440X, GLC1540X",file = open(file_name, '+a'))        
            print(f"slot:{dict1[i]} {i}, in case (1) GLC1440X, GLC1540X")        
            temp = "1," + dict1[i]
            temp = temp + "," + glc_port

        # CASE 2
        # (XPON)
        elif(("OLC3416B" in i) or ("OLC3708" in i) or ("OLC3816" in i)):                                                      # XPON ?
            cardtype_case = 2
            # print("in case (2) OLC3416B, OLC3708, OLC3816")         
            # print(f"slot:{dict1[i]} {i}, in case (2) OLC3416B, OLC3708, OLC3816",file = open(file_name, '+a'))                  
            print(f"slot:{dict1[i]} {i}, in case (2) OLC3416B, OLC3708, OLC3816")                  
            temp = "2," + dict1[i]
            if(("OLC3708" in i) and (int(pon_x_1_aid) > 8)):
                temp = temp + "," + '8'
            else:
                temp = temp + "," + pon_x_1_aid

        # CASE 3
        # (GPON)
        elif("OLC3416" in i):                                                                                                 # GPON ?
            cardtype_case = 3
            # print("in case (3) OLC3416")              
            # print(f"slot:{dict1[i]} {i}, in case (3) OLC3416",file = open(file_name, '+a'))        
            print(f"slot:{dict1[i]} {i}, in case (3) OLC3416")        
            temp = "3," + dict1[i] + "," + pon_1_aid
            
        # CASE 4           
        # (MSC)                                          
        elif("MSC" in i):                                                                                                     # MSC
            cardtype_case = 4
            print(f"slot:{dict1[i]} {i}, in case (4) MSC")        
            temp = "4," + dict1[i] + "," + pon_1_aid
            MSC_card = i
            MSC_slot = dict1[i] 

        else:        
            cardtype_case = 5
            # print("not in any case")        
            # print(f"slot:{dict1[i]} {i}, not in any case",file = open(file_name, '+a'))        
            print(f"slot:{dict1[i]} {i}, not in any case")        
            temp = "5," + dict1[i] + "," + "0"
                
        
        temp = temp + "," + i

        list1.append(temp)
            
    print(f"list1:{list1}")
    list1.append(MSC_card)
    list1.append(MSC_slot)
    print(f"list1:{list1}")
    return list1

def print_case(my_list,file_name):
    set_file_name(file_name)
    printf("======================================================================================")
    for item in my_list:
        try:
            case = item.split(",")[0]
            slot = item.split(",")[1]
            port = item.split(",")[2]
            type = item.split(",")[3]
            match case:            
                case "1":
                    printf(f"slot:{slot} port:{port} type:{type}, in case (1) (GLC1440X, GLC1540X)")
                case "2":
                    printf(f"slot:{slot} port:{port} type:{type}, in case (2) (OLC3416B, OLC3708, OLC3816)")
                case "3":
                    printf(f"slot:{slot} port:{port} type:{type}, in case (3) (OLC3416)")
                case "4":
                    printf(f"slot:{slot} port:{port} type:{type}, in case (4) (MSC)")
                case _:                
                    printf(f"slot:{slot} port:{port} type:{type}, not in any case")
        except:
            pass
    printf("======================================================================================")

def printf(str):
    print(str,file = open(file_name, '+a'))   

def set_file_name(file):
    global file_name
    file_name = file

# def get_file_name(file):
#     return file