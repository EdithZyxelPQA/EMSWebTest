# Wrap? selenium's method


from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.service import Service as ChromeService 
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time

my_chromedriver_path  = "chromedriver.exe"

class CustomDriver(webdriver.Chrome): 

    def __init__(self,time_sleep=0, retries=3, retry_interval=1):
        self.time_sleep = time_sleep
        self.retries = retries
        self.retry_interval = retry_interval
        # super(CustomDriver, self).__init__(service=ChromeService(ChromeDriverManager().install()))  ### webdriver_manager had some issues
        # super(CustomDriver, self).__init__(service=ChromeService(executable_path=my_chromedriver_path))  
        # 
        # 
        try:  
            super(CustomDriver, self).__init__(service=ChromeService())           
        except WebDriverException as first_error:
            try:
                # update chromedriver to 'drivers' folder
                import module.update_my_chromedriver
                super(CustomDriver, self).__init__(service=ChromeService())     
            except Exception as second_error:
                # webdriver-manager package                   
                # super(CustomDriver, self).__init__(service=ChromeService(ChromeDriverManager().install()))  ### webdriver_manager had some issues
                raise RuntimeError("Unable to start Chrome WebDriver") from second_error
      
    def _retry_find(self, finder, *args):
        time.sleep(self.time_sleep)
        last_error = None
        for attempt in range(self.retries):
            try:
                return finder(*args)
            except WebDriverException as error:
                last_error = error
                if attempt < self.retries - 1:
                    time.sleep(self.retry_interval)
        raise last_error

    def find_element(self, by=By.ID, value=None) -> WebElement:        
        return self._retry_find(super().find_element, by, value)
    
    def find_elements(self, by=By.ID, value=None) -> list[WebElement]:        
        return self._retry_find(super().find_elements, by, value)
