import re
import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def navigate_to(driver, first_menu, second_menu=None, tab_id=None):
    _click_menu_if_inactive(driver, By.LINK_TEXT, first_menu)
    if second_menu:
        _click_menu_if_inactive(driver, By.LINK_TEXT, second_menu)
    if tab_id:
        _click_menu_if_inactive(driver, By.ID, tab_id)


def filter_inventory_ont_by_sn(driver, sn):
    navigate_to(driver, "Inventory", "ONT")
    _click(driver, By.CSS_SELECTOR, "#i_action_filter > a")
    _click(driver, By.ID, "inventory_allont_clear_btn")
    _type(driver, By.ID, "serial_Allont", sn)
    _click(driver, By.ID, "inventory_allont_btn")
    _wait_for_table(driver, "ont_inventory_div")


def filter_inventory_ont_by_slot_port(driver, slot_id, port_id):
    navigate_to(driver, "Inventory", "ONT")
    _click(driver, By.CSS_SELECTOR, "#i_action_filter > a")
    _click(driver, By.ID, "inventory_allont_clear_btn")
    _type(driver, By.ID, "slot_Allont", str(slot_id))
    _type(driver, By.ID, "port_Allont", str(port_id))
    _click(driver, By.ID, "inventory_allont_btn")
    _wait_for_table(driver, "ont_inventory_div")


def available_ont_ids_from_inventory(driver, slot_id, port_id, preferred_ont_id, max_ont_id_attempts=16):
    preferred_ont_id = int(preferred_ont_id)
    candidate_ids = [str(index) for index in range(preferred_ont_id, preferred_ont_id + max_ont_id_attempts)]
    filter_inventory_ont_by_slot_port(driver, slot_id, port_id)
    occupied_ids = set()
    for row in table_rows(driver, "ont_inventory_div"):
        if row.get("Slot") != str(slot_id) or row.get("Port") != str(port_id):
            continue
        ont_id = row.get("ONT", "")
        if ont_id and ont_id not in {"--", "Unregistered"}:
            occupied_ids.add(ont_id)
    available_ids = [ont_id for ont_id in candidate_ids if ont_id not in occupied_ids]
    if not available_ids:
        raise RuntimeError(
            f"No available ONT ID in Inventory/ONT for slot={slot_id}, port={port_id}. "
            f"Checked={candidate_ids}, occupied={sorted(occupied_ids)}"
        )
    return available_ids


def wait_inventory_ont_id(driver, sn, predicate, timeout=300):
    sn_candidates = {sn, sn[-12:]}
    end_time = time.time() + timeout
    last_state = ""
    filter_inventory_ont_by_sn(driver, sn)
    while time.time() < end_time:
        rows = table_rows(driver, "ont_inventory_div")
        matched_rows = [row for row in rows if row.get("sn") in sn_candidates]
        if len(matched_rows) == 1:
            ont_id = matched_rows[0].get("ONT", "")
            last_state = f"ONT ID={ont_id}, row={matched_rows[0]}"
            if _call_inventory_predicate(predicate, ont_id, matched_rows[0]):
                return matched_rows[0]
        else:
            last_state = f"matched rows={len(matched_rows)}, rows={rows}"
        _safe_click(driver, By.ID, "i_action_refresh")
        time.sleep(3)
    raise TimeoutError(f"ONT inventory state did not match before timeout. SN={sn}, last_state={last_state}")


def wait_inventory_description(driver, sn, expected_description, timeout=300):
    return wait_inventory_ont_id(
        driver,
        sn,
        lambda _ont_id, row: row.get("description") == expected_description,
        timeout,
    )


def delete_ont_service_if_exists(driver, sn):
    filter_ont_service_by_sn(driver, sn)
    if total_data(driver, "provision_service_table") < 1:
        return False
    _click(driver, By.XPATH, "//label[@for='myCheckbox_title_provision_service_table']")
    _click(driver, By.CSS_SELECTOR, "#provision_service_delete > a")
    _confirm_message(driver)
    return True


def delete_ont_service_by_template_if_exists(driver, template_name):
    filter_ont_service_by_template(driver, template_name)
    if total_data(driver, "provision_service_table") < 1:
        return False
    _click(driver, By.XPATH, "//label[@for='myCheckbox_title_provision_service_table']")
    _click(driver, By.CSS_SELECTOR, "#provision_service_delete > a")
    _confirm_message(driver)
    return True


def filter_ont_service_by_sn(driver, sn):
    navigate_to(driver, "Provision", "Service", "service_tab_ont")
    _click(driver, By.CSS_SELECTOR, "#provision_service_filter > a")
    _click(driver, By.ID, "provision_service_filter_reset_btn")
    _click(driver, By.XPATH, "//label[@for='provision_filter_ont_sn_checkbox']")
    _type(driver, By.ID, "provision_filter_ont_sn_text", sn)
    _click(driver, By.ID, "provision_service_filter_query_btn")
    _wait_for_table(driver, "provision_service_table")


def filter_ont_service_by_template(driver, template_name):
    navigate_to(driver, "Provision", "Service", "service_tab_ont")
    _click(driver, By.CSS_SELECTOR, "#provision_service_filter > a")
    _click(driver, By.ID, "provision_service_filter_reset_btn")
    _click(driver, By.XPATH, "//label[@for='provision_filter_ont_template_checkbox']")
    _type(driver, By.ID, "provision_filter_ont_template_text", template_name)
    _click(driver, By.ID, "provision_service_filter_query_btn")
    _wait_for_table(driver, "provision_service_table")


def create_ont_service_by_select_sn(driver, sn, dut_ip=None, password=None, description=None, template_name=None):
    navigate_to(driver, "Provision", "Service", "service_tab_ont")
    _click(driver, By.CSS_SELECTOR, "#provision_service_create > a")
    _click(driver, By.XPATH, "//input[@value='Select ONT']")
    search_select_ont_dialog(driver, sn, dut_ip, password)
    _click(driver, By.CSS_SELECTOR, "#modal_select_ont .modal-footer > .button")
    edit_new_ont_service_row(driver)
    _ensure_checked(driver, By.XPATH, "//label[@for='provision_service_active_checkbox']")
    if description:
        _type(driver, By.ID, "provision_service_desc_text", description)
    if template_name:
        Select(driver.find_element(By.ID, "provision_service_onttemplate_combbox")).select_by_visible_text(template_name)
    _click(driver, By.ID, "provision_save_service_btn")
    _click(driver, By.XPATH, "//input[@value='Save']")
    _confirm_message(driver)


def create_ont_service_with_qos_vlan_translation(driver, sn, dut_ip=None, password=None, qos_count=32, template_name=None):
    navigate_to(driver, "Provision", "Service", "service_tab_ont")
    _click(driver, By.CSS_SELECTOR, "#provision_service_create > a")
    _click(driver, By.XPATH, "//input[@value='Select ONT']")
    search_select_ont_dialog(driver, sn, dut_ip, password)
    _click(driver, By.CSS_SELECTOR, "#modal_select_ont .modal-footer > .button")
    edit_new_ont_service_row(driver)
    _ensure_checked(driver, By.XPATH, "//label[@for='provision_service_active_checkbox']")
    if template_name:
        Select(driver.find_element(By.ID, "provision_service_onttemplate_combbox")).select_by_visible_text(template_name)
    add_service_qos_vlan_translation_rows(driver, qos_count)
    _click(driver, By.ID, "provision_save_service_btn")
    _click(driver, By.XPATH, "//input[@value='Save']")
    _confirm_message(driver)


def add_service_qos_vlan_translation_rows(driver, qos_count=32):
    for index in range(1, qos_count + 1):
        _click(driver, By.ID, "provision_service_profile_qos_table_new")
        Select(driver.find_element(By.ID, "provision_service_qos_tcont_combbox")).select_by_visible_text(
            f"service{index}"
        )
        _type(driver, By.ID, "provision_service_qos_vlan_text", str(200 + index))
        _type(driver, By.ID, "provision_service_qos_svlan_text", str(300 + index))
        _type(driver, By.ID, "provision_service_qos_cvlan_text", str(400 + index))
        _click(driver, By.CSS_SELECTOR, "#modal_provision_service_qos .button")


def wait_ont_service_success(driver, sn, timeout=300):
    end_time = time.time() + timeout
    last_state = ""
    filter_ont_service_by_sn(driver, sn)
    while time.time() < end_time:
        rows = table_rows(driver, "provision_service_table")
        if len(rows) == 1:
            status = rows[0].get("state", "")
            last_state = f"state={status}, row={rows[0]}"
            if status == "Success":
                return rows[0]
        else:
            last_state = f"rows={rows}"
        _safe_click(driver, By.ID, "provision_service_refresh")
        time.sleep(3)
    raise TimeoutError(f"ONT service did not become Success before timeout. SN={sn}, last_state={last_state}")


def _call_inventory_predicate(predicate, ont_id, row):
    try:
        return predicate(ont_id, row)
    except TypeError:
        return predicate(ont_id)


def search_select_ont_dialog(driver, sn, dut_ip=None, password=None):
    _click(driver, By.XPATH, "//label[@for='provision_select_ont_sn_checkbox']")
    for candidate_sn in [sn, sn[-12:]]:
        _type(driver, By.ID, "provision_select_ont_sn_text", candidate_sn)
        if _search_and_select_ont(driver, sn, password):
            return

    if dut_ip:
        _click(driver, By.XPATH, "//label[@for='provision_select_ont_ip_checkbox']")
        _type(driver, By.ID, "provision_select_ont_ip_text", dut_ip)
        if _search_and_select_ont(driver, sn, password):
            return

    select_ont_from_select_dialog(driver, sn, password, raise_on_missing=True)


def _search_and_select_ont(driver, sn, password=None, timeout=180):
    end_time = time.time() + timeout
    while time.time() < end_time:
        _click_select_ont_search(driver)
        time.sleep(5)
        if select_ont_from_select_dialog(driver, sn, password, raise_on_missing=False):
            return True
    return False


def _click_select_ont_search(driver):
    search_locators = [
        (By.ID, "provision_select_ont_search_btn"),
        (By.ID, "provision_select_ont_search_ont_btn"),
        (By.ID, "provision_select_ont_search_registered_ont_btn"),
        (By.XPATH, "//div[@id='modal_select_ont']//input[@value='Search']"),
        (By.XPATH, "//div[@id='modal_select_ont']//input[@value='Search ONT']"),
        (By.XPATH, "//div[@id='modal_select_ont']//button[normalize-space()='Search']"),
        (By.XPATH, "//div[@id='modal_select_ont']//a[normalize-space()='Search']"),
    ]
    for by, value in search_locators:
        try:
            _click(driver, by, value)
            return
        except TimeoutException:
            continue
    raise NoSuchElementException("Cannot find Select ONT Search button")


def select_ont_from_select_dialog(driver, sn, password=None, raise_on_missing=True):
    table_id = "provision_select_ont_table"
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, table_id)))
    rows = driver.find_elements(By.XPATH, f"//div[@id='{table_id}']/div")
    header = rows[0].find_elements(By.XPATH, "./div")
    sn_col = _div_col_index(header, "SN")
    password_col = _div_col_index(header, "Password") if password else None
    seen_rows = []
    for index, row in enumerate(rows[1:], start=1):
        cols = row.find_elements(By.XPATH, "./div")
        values = [col.text.strip() for col in cols]
        seen_rows.append(values)
        sn_matched = len(cols) >= sn_col and cols[sn_col - 1].text.strip() in {sn, sn[-12:]}
        password_matched = password_col is None or (
            len(cols) >= password_col and cols[password_col - 1].text.strip() == password
        )
        if sn_matched and password_matched:
            _click(driver, By.XPATH, f"//label[@for='provision_select_ont_table_checkbox{index}']")
            return True
    if raise_on_missing:
        raise NoSuchElementException(f"Cannot find ONT SN in Select ONT dialog: {sn}; rows={seen_rows}")
    return False


def edit_new_ont_service_row(driver):
    cell = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//td[contains(., '{}')]"))
    )
    cell.click()
    time.sleep(2)
    highlighted = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".highlight-selected"))
    )
    highlighted.click()
    time.sleep(2)
    highlighted.click()
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "provision_service_active_checkbox"))
    )


def table_rows(driver, table_id):
    _wait_for_table(driver, table_id)
    headers = _table_headers(driver, table_id)
    rows = []
    for tr in driver.find_elements(By.XPATH, f"//table[@id='{table_id}_body']/tbody/tr"):
        cells = tr.find_elements(By.XPATH, "./td")
        if not cells:
            continue
        rows.append({headers[index]: cell.text.strip() for index, cell in enumerate(cells[: len(headers)])})
    return rows


def total_data(driver, table_id):
    try:
        text = driver.find_element(By.ID, f"table_total_data_{table_id}").text
    except NoSuchElementException:
        return len(table_rows(driver, table_id))
    match = re.search(r"(\d+)", text)
    return int(match.group(1)) if match else 0


def _table_headers(driver, table_id):
    headers = []
    for th in driver.find_elements(By.XPATH, f"//table[@id='{table_id}_head']/thead/tr/th"):
        headers.append(th.get_attribute("name") or th.text.strip())
    return headers


def _div_col_index(header_cells, title):
    for index, cell in enumerate(header_cells, start=1):
        if cell.text.strip() == title:
            return index
    raise NoSuchElementException(f"Cannot find column title: {title}")


def _click_menu_if_inactive(driver, by, value):
    element = driver.find_element(by, value)
    if element.get_attribute("className") == "":
        element.click()
        time.sleep(3)


def _type(driver, by, value, text):
    element = driver.find_element(by, value)
    element.send_keys(Keys.CONTROL + "a")
    element.send_keys(Keys.DELETE)
    element.send_keys(text)



def _click(driver, by, value):
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((by, value))).click()
    time.sleep(1)


def _safe_click(driver, by, value):
    try:
        driver.find_element(by, value).click()
    except NoSuchElementException:
        pass


def _ensure_checked(driver, by, value):
    _click(driver, by, value)


def _confirm_message(driver):
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#message_diag .button"))).click()
    time.sleep(3)


def _wait_for_table(driver, table_id):
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, f"{table_id}_body")))
