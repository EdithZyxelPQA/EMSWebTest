from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service as ChromeService 
from selenium.webdriver.edge.service import Service as EdgeService 
from selenium.webdriver.firefox.service import Service as FirefoxService 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager 
import time
import pyautogui


options = webdriver.ChromeOptions()
driver1 = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))

options = webdriver.FirefoxOptions()
driver2 = webdriver.Firefox(options=options,service=FirefoxService(executable_path="C:\AutoTest\Tools\my_web_driver\geckodriver.exe"))  # geckodriver

options = webdriver.EdgeOptions()
driver3 = webdriver.Edge(options=options,service=EdgeService(executable_path="C:\AutoTest\Tools\my_web_driver\msedgedriver.exe"))

drivers = [driver1,driver2,driver3]
username = "admin"
password = "1234"

file_name = f"C:\\AutoTest\\Tools\\finish.txt" # "test_tmp.txt" #
test_report = open(file_name,"w+")

# for i, driver in enumerate(drivers):
for i, driver in enumerate(drivers):
    print(f"------------------------ browser:{driver.name} start ------------------------",file = open(file_name, '+a'))
    try:
        driver.maximize_window()
        # driver.get("http://192.168.169.207")
        # driver.get("http://admin:1234@192.168.169.207")
        driver.get("http://192.168.169.86")

        #------------------add https (click something before log in)------------------------
        try:
            driver.find_element(By.ID, "details-button").click()
            driver.find_element(By.ID, "proceed-link").click()
        except:
            pass
        #-----------------------------------------------------------------------------------
        username_ = driver.find_element(By.NAME, "user")
        username_.clear()
        username_.send_keys(username)
        password_ = driver.find_element(By.NAME, "pass")
        password_.clear()
        password_.send_keys(password)
        try:
            driver.find_element("xpath","//input[@type='submit']").click()
        except:
            pass

        # pyautogui.write("admin")
        # pyautogui.press("tab")
        # pyautogui.write("1234")
        # pyautogui.press("enter")    
        time.sleep(5)

        # after login 
        driver.switch_to.default_content()
        driver.find_element('link text','Maintenance').click()
        driver.find_element('link text','Config Backup').click()
        driver.switch_to.frame(0)
        time.sleep(3) 
        driver.find_element('name','rpMainBackup').click()
        time.sleep(5) 
    except:
        print(f"------------------------         FAIL ------------------------",file = open(file_name, '+a'))
    print(f"------------------------ browser:{driver.name} DONE ------------------------",file = open(file_name, '+a'))
    

