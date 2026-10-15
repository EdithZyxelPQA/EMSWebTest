import re
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from libs.ems_tables import navigate_to, table_rows_all_pages, total_data, wait_table_total_stable


GE_PORT_STATUS_TABLE = "All_gePortStatusTable"
DEVICE_STATUS_TABLE = "All_devStatusTable"
ONT_STATUS_TABLE = "All_ontStatusTable"


def open_dashboard(driver):
    if "netatlasems/index" in driver.current_url and "#" in driver.current_url:
        driver.get(driver.current_url.split("#", 1)[0] + "#")
    navigate_to(driver, "Dashboard")
    WebDriverWait(driver, 60).until(
        lambda d: d.find_elements(By.ID, "gePortStatusList") or d.find_elements(By.ID, "devStatus")
    )
    time.sleep(2)


def device_status_names(driver):
    open_dashboard(driver)
    names = []
    for index in range(1, len(driver.find_elements(By.CSS_SELECTOR, "#devStatus > div")) + 1):
        name = _device_status_name_from_index(index)
        if name and name not in names:
            names.append(name)
    return names


def click_device_status(driver, status_name):
    open_dashboard(driver)
    status_index = _device_status_index(status_name)
    status_block = driver.find_element(By.XPATH, f"//div[@id='devStatus']/div[{status_index}]")
    count = _status_count(status_block)
    try:
        click_target = status_block.find_element(By.XPATH, "./div[2]/a")
    except NoSuchElementException:
        click_target = status_block.find_element(By.TAG_NAME, "a")
    click_target.click()
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, f"{DEVICE_STATUS_TABLE}_body")))
    time.sleep(2)
    return count


def device_status_table_total(driver):
    return total_data(driver, DEVICE_STATUS_TABLE)


def ethernet_access_status_names(driver):
    open_dashboard(driver)
    names = []
    for element in driver.find_elements(By.CSS_SELECTOR, "#gePortStatusList > div"):
        status = _status_name_from_text(element.text)
        if status and status not in names:
            names.append(status)
    return names


def click_ethernet_access_status(driver, status_name):
    open_dashboard(driver)
    status_block = _status_block(driver, status_name)
    count = _status_count(status_block)
    try:
        click_target = status_block.find_element(By.TAG_NAME, "a")
    except NoSuchElementException:
        click_target = status_block
    click_target.click()
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, f"{GE_PORT_STATUS_TABLE}_body")))
    time.sleep(2)
    wait_table_total_stable(driver, GE_PORT_STATUS_TABLE)
    return count


def ethernet_access_status_table_total(driver):
    return total_data(driver, GE_PORT_STATUS_TABLE)


def ethernet_access_status_rows_all_pages(driver):
    return table_rows_all_pages(driver, GE_PORT_STATUS_TABLE)


def ont_status_entries(driver):
    return dashboard_status_entries(driver, "ontStatus")


def click_ont_status(driver, entry):
    return click_dashboard_status_entry(driver, "ontStatus", entry, ONT_STATUS_TABLE)


def ethernet_access_status_entries(driver):
    return dashboard_status_entries(driver, "gePortStatusList")


def click_ethernet_access_status_entry(driver, entry):
    return click_dashboard_status_entry(driver, "gePortStatusList", entry, GE_PORT_STATUS_TABLE)


def dashboard_status_entries(driver, status_id):
    open_dashboard(driver)
    entries = []
    links = driver.find_elements(By.XPATH, f"//div[@id='{status_id}']//a[string-length(normalize-space()) > 0]")
    for index, link in enumerate(links, start=1):
        container_text = _status_container_text(link)
        status_name = _status_name_from_text(container_text) or _clean_status_label(container_text) or f"{status_id} #{index}"
        entries.append({"index": index, "name": status_name})
    return entries


def click_dashboard_status_entry(driver, status_id, entry, table_id):
    open_dashboard(driver)
    status_link = driver.find_element(
        By.XPATH,
        f"(//div[@id='{status_id}']//a[string-length(normalize-space()) > 0])[{entry['index']}]",
    )
    count = _link_count(status_link)
    status_link.click()
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, f"{table_id}_body")))
    time.sleep(2)
    return count


def row_operation_status(row):
    for key in ["portOperationStatus", "OperationStatus", "Operation Status"]:
        if row.get(key):
            return row[key]
    return ""


def _status_block(driver, status_name):
    candidates = []
    for element in driver.find_elements(By.CSS_SELECTOR, "#gePortStatusList > div"):
        if _status_name_from_text(element.text) == status_name:
            candidates.append(element)
    if candidates:
        return candidates[0]

    data_value = {"Up": "1", "Down": "2", "Device Not Responding": "99"}.get(status_name)
    if data_value:
        return driver.find_element(By.CSS_SELECTOR, f"#gePortStatusList a[data-value='{data_value}']").find_element(
            By.XPATH, "./ancestor::div[contains(@class,'dashboard') or parent::div[@id='gePortStatusList']][1]"
        )
    raise NoSuchElementException(f"Cannot find Ethernet Access Port Status block: {status_name}")


def _device_status_index(status_name):
    status_map = {
        "In Service": 1,
        "Linked": 2,
        "Disconnected": 3,
    }
    if status_name not in status_map:
        raise NoSuchElementException(f"Cannot find Device Status block: {status_name}")
    return status_map[status_name]


def _device_status_name_from_index(index):
    names = {
        1: "In Service",
        2: "Linked",
        3: "Disconnected",
    }
    return names.get(index, "")


def _status_name_from_text(text):
    normalized = " ".join((text or "").split())
    if "Device Not Responding" in normalized:
        return "Device Not Responding"
    if "In Service" in normalized:
        return "In Service"
    if "Linked" in normalized:
        return "Linked"
    if "Disconnected" in normalized:
        return "Disconnected"
    if "Unregistered" in normalized:
        return "Unregistered"
    if "Inactive" in normalized:
        return "Inactive"
    if re.search(r"\bDown\b", normalized):
        return "Down"
    if re.search(r"\bUp\b", normalized):
        return "Up"
    return ""


def _status_count(element):
    text = element.text or ""
    numbers = re.findall(r"\d+", text)
    if numbers:
        return int(numbers[-1])
    try:
        value = element.find_element(By.TAG_NAME, "a").text
    except NoSuchElementException:
        value = ""
    numbers = re.findall(r"\d+", value)
    return int(numbers[-1]) if numbers else 0


def _link_count(link):
    text = " ".join((link.text or "").split())
    match = re.fullmatch(r"\d+", text)
    if match:
        return int(text)
    numbers = re.findall(r"\d+", text)
    return int(numbers[-1]) if numbers else _status_count(link)


def _status_container_text(link):
    for xpath in [
        "./ancestor::div[parent::div[@id='ontStatus'] or parent::div[@id='gePortStatusList']][1]",
        "./ancestor::div[1]",
    ]:
        try:
            text = link.find_element(By.XPATH, xpath).text
            if text:
                return text
        except NoSuchElementException:
            continue
    return link.text


def _clean_status_label(text):
    normalized = " ".join((text or "").split())
    label = re.sub(r"\b\d+\b", "", normalized).strip()
    return " ".join(label.split())
