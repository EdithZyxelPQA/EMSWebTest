from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import Select


def _wait_until(action, timeout=10, interval=1):
    last_error = None
    attempts = max(1, int(timeout))
    for attempt in range(attempts):
        try:
            return action()
        except Exception as error:
            last_error = error
            if attempt < attempts - 1:
                time.sleep(interval)
    if last_error is not None:
        raise last_error

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

def Switch_Default(driver):
    driver.switch_to.default_content()

def Switch_Specific_Frame(driver,num):
    driver.switch_to.frame(num)

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
    _wait_until(lambda: driver.find_element(By.ID, id).click(), sec)

def Find_by_id_wait(driver,id,sec):
    return _wait_until(lambda: driver.find_element(By.ID, id), sec)

def Find_by_xpath_wait_click(driver,xpath,sec):
    _wait_until(lambda: driver.find_element(By.XPATH, xpath).click(), sec)

def Find_by_link_text_wait_click(driver,link_text,sec):
    _wait_until(lambda: driver.find_element(By.LINK_TEXT, link_text).click(), sec)

def Find_by_class_name_wait_click(driver,class_name,sec):
    _wait_until(lambda: driver.find_element(By.CLASS_NAME, class_name).click(), sec)



# # # Add    FW Web (input, click, select, checkbox) --------------------------------------------

def Find_ele_wait_input(driver,element_type,element_content,value,timeout=10): # default wait 10s
    def action():
        element = driver.find_element(element_type,element_content)
        element.clear()
        element.send_keys(value)
    _wait_until(action, timeout)

def Find_eles_wait_input(driver,element_type,element_content,index,value,timeout=10): # default wait 10s

    index = int(index) - 1
    def action():
        element = driver.find_elements(element_type,element_content)[index]
        element.clear()
        element.send_keys(value)
    _wait_until(action, timeout)

def Find_ele_wait_click(driver,element_type,element_content,timeout=10): # default wait 10s
    _wait_until(lambda: driver.find_element(element_type,element_content).click(), timeout)

def Find_eles_wait_click(driver,element_type,element_content,index,timeout=10): # default wait 10s
    index = int(index) - 1
    _wait_until(lambda: driver.find_elements(element_type,element_content)[index].click(), timeout)

def Find_ele_wait_select(driver,element_type,element_content,text,timeout=10): # default wait 10s

    def action():
        ele = driver.find_element(element_type,element_content)
        Select(ele).select_by_visible_text(text)
    _wait_until(action, timeout)

def Find_eles_wait_select(driver,element_type,element_content,index,text,timeout=10): # default wait 10s
    index = int(index) - 1
    def action():
        ele = driver.find_elements(element_type,element_content)[index]
        Select(ele).select_by_visible_text(text)
    _wait_until(action, timeout)

def Find_ele_wait_checkbox(driver,request,element_type,element_content,timeout=10):
    def action():
        checkbox = driver.find_element(element_type,element_content)
        if checkbox.is_selected() != request:
            checkbox.click()
    _wait_until(action, timeout)

def Find_eles_wait_checkbox(driver,request,index,element_type,element_content,timeout=10):
    index = int(index) - 1
    def action():
        checkbox = driver.find_elements(element_type,element_content)[index]
        if checkbox.is_selected() != request:
            checkbox.click()
    _wait_until(action, timeout)
