from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import Select

def Login(driver,username,password):
   
    #------------------add https (click something before log in)----
    try:
        driver.find_element('id',"details-button").click()
        driver.find_element('id',"proceed-link").click()
    except:
        pass
    #---------------------------------------------------------------

    # try:
    #     driver.find_element(By.ID, "name").clear()
    #     driver.find_element(By.ID, "name").send_keys(username)
    #     # driver.find_element(By.ID, "passwd").clear()
    #     driver.find_element(By.ID, "passwd").send_keys(password)
    #     # pyautogui.press("enter")
    # except:
    #     pass

    try:
        username_ = driver.find_element(By.NAME, "user")
        username_.clear()
        username_.send_keys(username)
        password_ = driver.find_element(By.NAME, "pass")
        password_.clear()
        password_.send_keys(password)
        driver.find_element('xpath',f'//*[@value="Login"]').click()
        driver.find_element('xpath',f'//*[@value="Login"]').click()
    except:
        pass

def Login_EMS(driver,username,password):

    try:
        driver.find_element('id',"index_t_userName")
        return
    except:
        pass

    # try:
    #     driver.find_element(By.ID, "name").clear()
    #     driver.find_element(By.ID, "name").send_keys(username)
    #     driver.find_element(By.ID, "passwd").clear()
    #     driver.find_element(By.ID, "passwd").send_keys("Pqa1234!!")
    #     # pyautogui.press("enter")
    #     driver.find_element(By.ID, "signin").click()
    # except:
    #     try:
    #         driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div/div/div[3]/button").click()
    #         driver.find_element(By.ID, "name").clear()
    #         driver.find_element(By.ID, "name").send_keys(username)
    #         driver.find_element(By.ID, "passwd").clear()
    #         driver.find_element(By.ID, "passwd").send_keys("Pqa1234!!")
    #         # pyautogui.press("enter")
    #         driver.find_element(By.ID, "signin").click()
    #     except:
    #         pass
    
    # try:
    # except:
    #     pass

    #------------------add https (click something before log in)----
    try:
        driver.find_element('id',"details-button").click()
        driver.find_element('id',"proceed-link").click()
    except:
        pass
    #---------------------------------------------------------------

    count = 0
    if_log = False
    # while((if_log == False) and (count < 5) ):
    while((if_log == False) and (count < 3) ):
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

def Page_Switch(driver,name):
    page = driver.find_element(By.LINK_TEXT, name)
    page.click()

def SubPage_Switch(driver,name):
    subpage = driver.find_element(By.LINK_TEXT, name)
    subpage.click()

def Tab_Switch(driver,name):
    tab = driver.find_element(By.LINK_TEXT, name)
    tab.click()

def Switch_Frame(driver):
    driver.switch_to.frame(0)

def Switch_Specific_Frame(driver,num):
    driver.switch_to.frame(num)

def Switch_Default(driver):
    driver.switch_to.default_content()

def Re_Login(driver,username,password):
    driver.switch_to.default_content()
    username_alert = driver.find_element(By.ID, "lg_user")
    username_alert.send_keys(username)
    password_alert = driver.find_element(By.ID, "lg_pass")
    password_alert.send_keys(password)
    login_alert = driver.find_element(By.ID, "userLogin")
    login_alert.click()

def IsAlert(driver):
    try:
        driver.find_element(By.XPATH, "//div[@id='toast-container']/div")
        return True
    except:
        return False

def Find_by_id_wait_click(driver,id,sec):
    if_find = False
    counter = 0
    while if_find == False and counter < sec:
        try:
            driver.find_element(By.ID, id).click()
            if_find = True
            return
        except:
            counter = counter+1
            time.sleep(1)
    driver.find_element(By.ID, id).click()

def Find_by_id_wait(driver,id,sec):
    if_find = False
    counter = 0
    while if_find == False and counter < sec:
        try:
            driver.find_element(By.ID, id)
            if_find = True
            return
        except:
            counter = counter+1
            time.sleep(1)
    driver.find_element(By.ID, id)

def Find_by_xpath_wait_click(driver,xpath,sec):
    if_find = False
    counter = 0
    while if_find == False and counter < sec:
        try:
            driver.find_element(By.XPATH, xpath).click()
            if_find = True
            return
        except:
            counter = counter+1
            time.sleep(1)
    driver.find_element(By.XPATH, xpath).click()

def Find_by_link_text_wait_click(driver,link_text,sec):
    if_find = False
    counter = 0
    while if_find == False and counter < sec:
        try:
            driver.find_element(By.LINK_TEXT, link_text).click()
            if_find = True
            return
        except:
            counter = counter+1
            time.sleep(1)
    driver.find_element(By.LINK_TEXT, link_text).click()

def Find_by_class_name_wait_click(driver,class_name,sec):
    if_find = False
    counter = 0
    while if_find == False and counter < sec:
        try:
            driver.find_element(By.CLASS_NAME, class_name).click()
            if_find = True
            return
        except:
            counter = counter+1
            time.sleep(1)
    driver.find_element(By.CLASS_NAME, class_name).click()



# # # Add    FW Web (input, click, select, checkbox) --------------------------------------------

def Find_ele_wait_input(driver,element_type,element_content,value,timeout=10): # default wait 10s
    if_find = False
    counter = 0
    while if_find == False and counter < timeout:
        try:
            input = driver.find_element(element_type,element_content)
            input.clear()
            input.send_keys(value)
            if_find = True
            return
        except:
            counter = counter+1
            time.sleep(1)
    input = driver.find_element(element_type,element_content)       # need?
    input.clear()
    input.send_keys(value)

def Find_eles_wait_input(driver,element_type,element_content,index,value,timeout=10): # default wait 10s

    index = int(index) - 1
    if_find = False
    counter = 0
    while if_find == False and counter < timeout:
        try:
            input = driver.find_elements(element_type,element_content)[index]
            input.clear()
            input.send_keys(value)
            if_find = True
            return
        except:
            counter = counter+1
            time.sleep(1)
    input = driver.find_elements(element_type,element_content)[index]       # need?
    input.clear()
    input.send_keys(value)

def Find_ele_wait_click(driver,element_type,element_content,timeout=10): # default wait 10s
    if_find = False
    counter = 0
    while if_find == False and counter < timeout:
        try:
            driver.find_element(element_type,element_content).click()
            if_find = True
            return
        except:
            counter = counter+1
            time.sleep(1)
    driver.find_element(element_type,element_content).click()       # need?

def Find_eles_wait_click(driver,element_type,element_content,index,timeout=10): # default wait 10s
    index = int(index) - 1
    if_find = False
    counter = 0
    while if_find == False and counter < timeout:
        try:
            driver.find_elements(element_type,element_content)[index].click()
            if_find = True
            return
        except:
            counter = counter+1
            time.sleep(1)
    driver.find_elements(element_type,element_content)[index].click()       # need?

def Find_ele_wait_select(driver,element_type,element_content,text,timeout=10): # default wait 10s

    if_find = False
    counter = 0
    while if_find == False and counter < timeout:
        try:
            ele = driver.find_element(element_type,element_content)
            Select(ele).select_by_visible_text(text)
            if_find = True
            return
        except:
            counter = counter+1
            time.sleep(1)
    # ele = driver.find_element(element_type,element_content)      # need?
    # Select(ele).select_by_visible_text(text)

def Find_eles_wait_select(driver,element_type,element_content,index,text,timeout=10): # default wait 10s
    index = int(index) - 1
    if_find = False
    counter = 0
    while if_find == False and counter < timeout:
        try:
            ele = driver.find_elements(element_type,element_content)[index]
            Select(ele).select_by_visible_text(text)
            if_find = True
            return
        except:
            counter = counter+1
            time.sleep(1)

def Find_ele_wait_checkbox(driver,request,element_type,element_content,timeout=10):
    if_find = False
    counter = 0
    while if_find == False and counter < timeout:
        try:

            checkbox = driver.find_element(element_type,element_content)
            if(checkbox.is_selected() == True):
                if(request == False):
                    Find_ele_wait_click(driver,element_type,element_content)
            else:
                if(request == True):
                    Find_ele_wait_click(driver,element_type,element_content)

            if_find = True
            return
        except:
            counter = counter+1
            time.sleep(1)

def Find_eles_wait_checkbox(driver,request,index,element_type,element_content,timeout=10):
    index = int(index) - 1
    if_find = False
    counter = 0
    while if_find == False and counter < timeout:
        try:

            checkbox = driver.find_elements(element_type,element_content)[index]
            if(checkbox.is_selected() == True):
                if(request == False):
                    Find_eles_wait_click(driver,element_type,element_content,index)
            else:
                if(request == True):
                    Find_eles_wait_click(driver,element_type,element_content,index)

            if_find = True
            return
        except:
            counter = counter+1
            time.sleep(1)