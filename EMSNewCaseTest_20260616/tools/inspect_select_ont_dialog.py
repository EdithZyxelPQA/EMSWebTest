import sys
from pathlib import Path

from selenium.webdriver.common.by import By

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from libs.browser import create_browser
from libs.ems_tables import navigate_to
from libs.ems_ui import login_ems
from conftest import build_config_object


def main():
    cfg = build_config_object("192.168.168.85", "environment_parameter.json")
    driver = create_browser(cfg.browser, cfg.downloadpath)
    try:
        driver.implicitly_wait(cfg.waitTime)
        driver.maximize_window()
        driver.get(cfg.emsURL)
        login_ems(driver, cfg.emsUsr, cfg.emsPwd)
        navigate_to(driver, "Provision", "Service", "service_tab_ont")
        driver.find_element(By.CSS_SELECTOR, "#provision_service_create > a").click()
        driver.find_element(By.XPATH, "//input[@value='Select ONT']").click()

        print("INPUTS")
        for element in driver.find_elements(By.XPATH, "//div[@id='modal_select_ont']//input"):
            print(
                {
                    "id": element.get_attribute("id"),
                    "name": element.get_attribute("name"),
                    "type": element.get_attribute("type"),
                    "value": element.get_attribute("value"),
                    "checked": element.get_attribute("checked"),
                }
            )

        print("BUTTONS")
        for element in driver.find_elements(By.XPATH, "//div[@id='modal_select_ont']//button|//div[@id='modal_select_ont']//a"):
            print(
                {
                    "id": element.get_attribute("id"),
                    "class": element.get_attribute("class"),
                    "text": element.text,
                }
            )

        print("TABLE TEXT")
        table = driver.find_element(By.ID, "provision_select_ont_table")
        print(table.text)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
