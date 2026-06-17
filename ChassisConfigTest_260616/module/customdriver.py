# Wrap? selenium's method


from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.service import Service as ChromeService 
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
import time



def Wait_Block(driver):
    try:
        if_block = True
        count = 0
        time.sleep(0.1) # time.sleep(0.2)
        while((if_block == True) and (count < 300)):  # 10
            if("block" in driver.find_element(By.ID,"configure_loader").get_attribute("style")):
                time.sleep(0.5)                    
                count = count + 1     
            else:
                if_block = False
        time.sleep(0.1)
    except:
        pass

def _try_recover_renderer(driver, wait_sec=5):
    """
    When a TimeoutException (renderer timeout) occurs, attempt a lightweight
    recovery: navigate to about:blank and wait briefly so Chrome can free
    renderer resources before the next real operation.
    """
    try:
        driver.execute_script("window.stop();")
    except Exception:
        pass
    try:
        # Navigate to blank page to clear renderer state
        driver.get("about:blank")
        time.sleep(wait_sec)
    except Exception:
        pass

class CustomDriver(webdriver.Chrome): 

    def __init__(self,time_sleep=0):
        self.time_sleep = time_sleep
        # super(CustomDriver, self).__init__(service=ChromeService(ChromeDriverManager().install()))  ### webdriver_manager had some issues
        # super(CustomDriver, self).__init__(service=ChromeService())        

        try:  
            super(CustomDriver, self).__init__(service=ChromeService())           
        except:
            import module.update_my_chromedriver
            super(CustomDriver, self).__init__(service=ChromeService())   
            # try:
            #     # update chromedriver to 'drivers' folder
            #     import module.update_my_chromedriver
            #     super(CustomDriver, self).__init__(service=ChromeService())     
            # except:
            #     # webdriver-manager package                   
            #     # super(CustomDriver, self).__init__(service=ChromeService(ChromeDriverManager().install()))  ### webdriver_manager had some issues
            #     pass

    def find_element(self, by=By.ID, value=None) -> WebElement:  
        
        # Wait_Block(self)      
        
        time.sleep(self.time_sleep)
        for i in range(3):
            try:
                super().find_element(by, value)
                break
            except TimeoutException:
                # Renderer timeout: attempt recovery before retrying
                print(f'!find_element renderer timeout ({i}), attempting recovery...')
                _try_recover_renderer(self, wait_sec=3)
            except Exception:
                time.sleep(1) 
                # print(f'!element ({i}) ',by,' ',value)

        return super().find_element(by, value)
    
    def find_elements(self, by=By.ID, value=None) -> WebElement:        
        time.sleep(self.time_sleep)
        for i in range(3):
            try:
                super().find_elements(by, value)
                break
            except TimeoutException:
                # Renderer timeout: attempt recovery before retrying
                print(f'!find_elements renderer timeout ({i}), attempting recovery...')
                _try_recover_renderer(self, wait_sec=3)
            except Exception:
                time.sleep(1) 
                # print(f'!element ({i}) ',by,' ',value)
                
        return super().find_elements(by, value)