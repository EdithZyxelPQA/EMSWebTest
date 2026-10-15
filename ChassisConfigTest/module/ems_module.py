import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import module.selenium_module as mod
import linecache
import sys as real_sys
import traceback
import io
SUCCESS_TEXT = "uccess"



def Login_EMS(driver,username,password):
    #------------------add https (click something before log in)----
    try:
        driver.find_element('id',"details-button").click()
        driver.find_element('id',"proceed-link").click()
    except:
        pass
    #---------------------------------------------------------------

    count = 0
    if_log = False
    while((if_log == False) and (count < 5) ):
        try:
            driver.find_element(By.ID, "name").clear()
            driver.find_element(By.ID, "name").send_keys(username)
            driver.find_element(By.ID, "passwd").clear()
            driver.find_element(By.ID, "passwd").send_keys(password)            
            driver.find_element(By.ID, "signin").click() 
            time.sleep(1)
            driver.find_element(By.ID, "index_t_userName")
            if_log = True           
        except:
            try:
                driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div/div/div[3]/button").click()
                time.sleep(1)
                # s
                driver.find_element(By.ID, "passwd").clear()
                driver.find_element(By.ID, "passwd").send_keys(password)                
                driver.find_element(By.ID, "signin").click()
                time.sleep(1)
                driver.find_element(By.ID, "index_t_userName")
                if_log = True
            except:
                pass
        count = count + 1


def Click(driver,type,ele):
    driver.find_element(type,ele).click()

def Input_text(driver,type,ele,value):
    driver.find_element(type,ele).send_keys(Keys.CONTROL + 'a')
    driver.find_element(type,ele).send_keys(value)

def Page_Switch(driver,name):
    page = driver.find_element(By.LINK_TEXT,name)
    page.click()

def SubPage_Switch(driver,name):
    subpage = driver.find_element(By.LINK_TEXT,name)
    subpage.click()

def Tab_Switch(driver,name):
    tab = driver.find_element(By.LINK_TEXT,name)
    tab.click()

# def Switch_Frame(driver):
#     driver.switch_to.frame(0)

# def Switch_Default(driver):
#     driver.switch_to.default_content()
    
def Scroll(driver,element,direction='Top',move=200,symbol='+'):
    move = str(move)
    if(direction == 'Left'):
        symbol = '-'
    driver.execute_script(f'arguments[0].scroll{direction} = arguments[0].scroll{direction} {symbol} {move};',element)

    


def Checkbox_EMS(driver,ele_id,request,index=''): # for ems check box
    index = str(index)
    check_box = driver.find_element(By.XPATH,f'//*[@for="{ele_id}{index}"]')
    if(driver.find_element(By.XPATH,f'//*[@id="{ele_id}{index}"]').is_selected() == True):
        if(request == False):
            check_box.click()
    else:
        if(request == True):
            check_box.click()    

def Radio(driver, element_id, index=''): # Multiple Choice
    driver.find_element(By.XPATH,f'//*[@for="{element_id}{index}"]').click()

def NextPage_Click(driver,index=''):
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, f"btnNextPage{index}"))).click()
    # driver.find_element(By.ID,f"btnNextPage{index}").click()

def PrevPage_Click(driver,index=''):
    driver.find_element(By.ID,f"btnPrevPage{index}").click()

def alert_accept(driver,timeout=10):
    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="message_diag"]/div/div/div[3]/button'))).click()  #* modify 20230803            
        return True
    except:
        return False
        pass

def Wait_Block(driver):
    try:
        if_block = True
        count = 0
        time.sleep(1) # time.sleep(0.2)
        while((if_block == True) and (count < 300)):  # 10
            if("block" in driver.find_element(By.ID,"configure_loader").get_attribute("style")):
                time.sleep(0.5)                    
                count = count + 1     
            else:
                if_block = False
        time.sleep(0.1)
    except:
        pass

def get_ems_alert_msg(driver):
    msg = driver.find_element(By.ID,"message_text").text
    msg = msg.replace("\n"," ")    
    return msg
    
def alert_accept_text(driver, timeout=10):  # 60
    
    # wait
    Wait_Block(driver)
    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.ID,"message_text")))                                          #* modify 20230802
        msg = get_ems_alert_msg(driver)
        alert_accept(driver)   
    except:
        msg = f'timeout {timeout}s no msg'

    # try:                      # Add
    #     Close(driver)
    # except:
    #     pass
          
    return (msg + ' ')

def alert_accept_text_2(driver,  file_name, timeout=10):
    
    # if msg, print

    Wait_Block(driver)
    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.ID,"message_text")))
        msg = get_ems_alert_msg(driver)
        alert_accept(driver)   
        print(f"             msg:{msg}",file = open(file_name, '+a'))
    except:
        # msg = f'timeout {timeout}s no msg'
        pass
          
    # return (msg + ' ')

def if_msg_not_success(msg):
    # no SUCCESS_TEXT
    # no timeout no msg
    # if((SUCCESS_TEXT not in msg) and ("no msg" not in msg)):
    # if((SUCCESS_TEXT not in msg) or ("no msg" not in msg)):
    
    if("Did not change anything" in msg):
        return False
    
    if((SUCCESS_TEXT in msg) and ("no msg" not in msg)):
        return False
    else:
        return True
    

# Click 'OK', it will show 'value format error while use .clear() on text input'
def Click_OK_format_error(driver):
    try:
        driver.find_element(By.XPATH,'//*[@id="message_diag"]/div/div/div[3]/button').click()      # OK
    except:
        pass    

def Clear_Input_text(driver,ele):
    # fire keyboard event to clear text (Ctrl + Backspace)
    driver.find_element('css_selector',ele).send_keys(u'\ue009' + u'\ue003')




def OK(driver):
    try:
        driver.find_element(By.ID,'popupCallBack').click()
    except:
        
        try:
            driver.find_element(By.XPATH,'//*[@id="message_diag"]/div/div/div[3]/button').click()
        except:
            pass

def Close(driver):
    driver.find_element(By.ID,'popupClose').click()

def Close2(driver):
    try:
        driver.find_element(By.ID,'popupClose').click()
    except:
        pass