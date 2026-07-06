import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from libs.ems_tables import navigate_to, table_rows


def ensure_ont_service_profile(driver, profile_name, vlan, uni_port="XLAN 1"):
    if profile_exists(driver, "ONT Service Profile", profile_name):
        return
    open_create_profile(driver, "ONT Service Profile", profile_name)
    _type(driver, By.ID, "ont_service_vlan_text", str(vlan))
    _click_label_contains(driver, "Bridge")
    _click_label_contains(driver, "XLAN")
    _select_visible_text_fuzzy(driver.find_element(By.ID, "ont_service_lan_combobox"), uni_port)
    save_profile(driver)


def recreate_ont_service_profile(driver, profile_name, vlan, uni_port="XLAN 1"):
    delete_profile_if_exists(driver, "ONT Service Profile", profile_name)
    ensure_ont_service_profile(driver, profile_name, vlan, uni_port)


def ensure_ont_qos_bandwidth_profile(driver, profile_name, pir="1024000"):
    if profile_exists(driver, "ONT QoS Bandwidth Profile", profile_name):
        return
    open_create_profile(driver, "ONT QoS Bandwidth Profile", profile_name)
    for name, value in {
        "bwprofile_sir": "0",
        "bwprofile_air": "0",
        "bwprofile_pir": pir,
        "bwprofile_gpon_sir": "0",
        "bwprofile_gpon_air": "0",
        "bwprofile_gpon_pir": pir,
    }.items():
        _type(driver, By.NAME, name, value)
    save_profile(driver)


def recreate_ont_qos_bandwidth_profile(driver, profile_name, pir="1024000"):
    delete_profile_if_exists(driver, "ONT QoS Bandwidth Profile", profile_name)
    ensure_ont_qos_bandwidth_profile(driver, profile_name, pir)


def ensure_ont_template_vlan_profile(
    driver,
    profile_name="$py_OntTempVlan",
    service_profile_prefix="$py_Service",
    us_bandwidth_profile="$py_Bandwidth_1G_US",
    ds_bandwidth_profile="$py_Bandwidth_1G_DS",
):
    if profile_exists(driver, "ONT Template", profile_name):
        return
    open_create_profile(driver, "ONT Template", profile_name)

    for index in range(1, 33):
        vlan = 100 + index
        _ensure_checkbox_checked(driver, f"ont_template_service_enable_checkbox{index}")
        _select_profile(driver, f"ont_template_service_combobox{index}", f"{service_profile_prefix}{vlan}_XLAN1")
        Select(driver.find_element(By.ID, f"ont_template_service_shared_combobox{index}")).select_by_visible_text(
            str((index - 1) % 8)
        )
        _select_profile(driver, f"ont_template_service_us_bw_combobox{index}", us_bandwidth_profile)
        _select_profile(driver, f"ont_template_service_ds_bw_combobox{index}", ds_bandwidth_profile)

    for index in range(1, 9):
        _ensure_checkbox_checked(driver, f"ont_template_tcont_enable_checkbox{index}")
        service_select = Select(driver.find_element(By.ID, f"ont_template_tcont_combobox{index}"))
        for service_index in range((index - 1) * 4 + 1, index * 4 + 1):
            service_select.select_by_visible_text(str(service_index))
        _select_profile(driver, f"ont_template_tcont_us_bw_combobox{index}", us_bandwidth_profile)
        _select_profile(driver, f"ont_template_tcont_ds_bw_combobox{index}", ds_bandwidth_profile)
        Select(driver.find_element(By.ID, f"ont_template_tcont_type_combobox{index}")).select_by_visible_text("Best-Effort")

    save_profile(driver)


def recreate_ont_template_vlan_profile(
    driver,
    profile_name="$py_OntTempVlan",
    service_profile_prefix="$py_Service",
    us_bandwidth_profile="$py_Bandwidth_1G_US",
    ds_bandwidth_profile="$py_Bandwidth_1G_DS",
):
    delete_profile_if_exists(driver, "ONT Template", profile_name)
    ensure_ont_template_vlan_profile(
        driver,
        profile_name,
        service_profile_prefix,
        us_bandwidth_profile,
        ds_bandwidth_profile,
    )


def profile_exists(driver, profile_type, profile_name):
    open_profile_list(driver, profile_type)
    rows = table_rows(driver, "profile_table")
    return any(row.get("Name") == profile_name for row in rows)


def delete_profile_if_exists(driver, profile_type, profile_name):
    print(f"EMS profile: delete if exists type={profile_type}, name={profile_name}", flush=True)
    open_profile_list(driver, profile_type)
    row_xpath = (
        f"//table[@id='profile_table_body']/tbody/tr[td[normalize-space()={xpath_literal(profile_name)}]"
        f" or td[contains(normalize-space(), {xpath_literal(profile_name)})]]"
    )
    try:
        row = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, row_xpath)))
    except TimeoutException:
        print(f"EMS profile: not found type={profile_type}, name={profile_name}", flush=True)
        return False
    checkbox_label = row.find_element(By.XPATH, ".//label")
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", checkbox_label)
    checkbox_label.click()
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#i_action_delete > a"))).click()
    _confirm_message(driver)
    print(f"EMS profile: delete requested type={profile_type}, name={profile_name}", flush=True)
    return True


def open_profile_list(driver, profile_type):
    navigate_to(driver, "Provision", "Profile")
    Select(WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "profile_filtertype")))).select_by_visible_text(
        profile_type
    )
    time.sleep(3)


def open_create_profile(driver, profile_type, profile_name):
    print(f"EMS profile: create type={profile_type}, name={profile_name}", flush=True)
    open_profile_list(driver, profile_type)
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#i_action_create_collector > a"))).click()
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "profile_name")))
    _type(driver, By.ID, "profile_name", profile_name)


def save_profile(driver):
    print("EMS profile: save", flush=True)
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Save']"))).click()
    _confirm_message(driver)


def _type(driver, by, value, text):
    element = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((by, value)))
    element.send_keys(Keys.CONTROL + "a")
    element.send_keys(Keys.DELETE)
    element.send_keys(str(text))


def _click_label_contains(driver, text):
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, f"//label[contains(normalize-space(), {xpath_literal(text)})]"))
    ).click()
    time.sleep(1)


def _select_profile(driver, select_id, profile_name):
    element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, select_id)))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    Select(element).select_by_visible_text(profile_name)
    time.sleep(0.5)


def _select_visible_text_fuzzy(element, expected_text):
    selector = Select(element)
    expected_normalized = _normalize_option_text(expected_text)
    for option in selector.options:
        if _normalize_option_text(option.text) == expected_normalized:
            selector.select_by_visible_text(option.text)
            return
    expected_tokens = [token for token in re_split_text(expected_text) if token]
    for option in selector.options:
        option_normalized = _normalize_option_text(option.text)
        if all(token in option_normalized for token in expected_tokens):
            selector.select_by_visible_text(option.text)
            return
    available = [option.text for option in selector.options]
    raise NoSuchElementException(f"Cannot select {expected_text!r}; available options={available}")


def _normalize_option_text(text):
    return "".join(str(text).lower().split())


def re_split_text(text):
    return [part.lower() for part in str(text).replace("-", " ").replace("_", " ").split()]


def _ensure_checkbox_checked(driver, checkbox_id):
    checkbox = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, checkbox_id)))
    if checkbox.is_selected():
        return
    label = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, f"//label[@for={xpath_literal(checkbox_id)}]"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", label)
    label.click()
    time.sleep(0.5)


def _confirm_message(driver):
    try:
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#message_diag .button"))).click()
        time.sleep(3)
    except TimeoutException:
        pass


def xpath_literal(text):
    if "'" not in text:
        return f"'{text}'"
    if '"' not in text:
        return f'"{text}"'
    parts = text.split("'")
    return "concat(" + ", \"'\", ".join(f"'{part}'" for part in parts) + ")"
