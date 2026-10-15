# Wrap? selenium's method


from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
from pathlib import Path

# EMS loading overlays: 'loadind_1' (current EMS web), 'configure_loader' (older pages, see Wait_Block)
LOADING_OVERLAY_IDS = ("loadind_1", "configure_loader")



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

def _wait_page_ready(driver, by, value, overlay_timeout, element_timeout):
    """
    Wait until no EMS loading overlay is displayed, then until (by, value) is present.
    Uses WebDriver.find_elements directly so it never re-enters CustomDriver.find_element.
    Never raises: on timeout the normal find_element/find_elements path runs as before.
    """
    def overlay_shown():
        for overlay_id in LOADING_OVERLAY_IDS:
            for e in WebDriver.find_elements(driver, By.ID, overlay_id):
                try:
                    if e.is_displayed():
                        return True
                except WebDriverException:   # stale: overlay re-rendered
                    return True
        return False

    try:
        end = time.time() + overlay_timeout
        while overlay_shown() and time.time() < end:
            time.sleep(0.3)
        end = time.time() + element_timeout
        while not WebDriver.find_elements(driver, by, value) and time.time() < end:
            time.sleep(0.3)
    except Exception:
        pass

def wait_loading_done(driver, timeout=30, settle=0.5):
    """
    Wait until no EMS loading overlay is displayed (max timeout s). Call right after an action that reloads part of
    the page (sort click, New, Save...) so the next step does not read the old table / form. Never raises.
    """
    time.sleep(settle)   # the overlay appears shortly after the click
    _wait_page_ready(driver, By.TAG_NAME, "body", timeout, 0)

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

    def __init__(self,time_sleep=0, wait_page_ready=True, overlay_timeout=30, element_timeout=10, elements_timeout=5):
        self.time_sleep = time_sleep
        # Before each find: wait for the EMS loading overlay to go away (max overlay_timeout s), then for the element
        # (max element_timeout s for find_element, elements_timeout s for find_elements). Slow EMS (e.g. 128.100)
        # otherwise hits "element click intercepted ... loadind_1" / "no such element" and whole groups get skipped.
        self.wait_page_ready = wait_page_ready
        self.overlay_timeout = overlay_timeout
        self.element_timeout = element_timeout
        self.elements_timeout = elements_timeout
        # super(CustomDriver, self).__init__(service=ChromeService(ChromeDriverManager().install()))  ### webdriver_manager had some issues
        # super(CustomDriver, self).__init__(service=ChromeService())        

        driver_path = Path(__file__).resolve().parent.parent / 'drivers' / 'chromedriver.exe'
        try:
            service = ChromeService(executable_path=str(driver_path)) if driver_path.is_file() else ChromeService()
            super(CustomDriver, self).__init__(service=service)
        except WebDriverException:
            from module.update_my_chromedriver import Update_Chromedriver3
            Update_Chromedriver3(str(driver_path.parent))
            super(CustomDriver, self).__init__(service=ChromeService(executable_path=str(driver_path)))
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
        if self.wait_page_ready:
            _wait_page_ready(self, by, value, self.overlay_timeout, self.element_timeout)
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
        if self.wait_page_ready:
            _wait_page_ready(self, by, value, self.overlay_timeout, self.elements_timeout)
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
