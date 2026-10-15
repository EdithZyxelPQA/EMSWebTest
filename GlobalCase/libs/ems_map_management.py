import time

from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from libs.ems_tables import navigate_to


def default_device_settings(config):
    dut = getattr(config, "dut", None)
    return {
        "deviceName": getattr(config, "dutName", ""),
        "description": getattr(config, "dutDesc", ""),
        "deviceIP": getattr(config, "dutIp", ""),
        "userName": getattr(config, "dutAdminName", ""),
        "dev_password": getattr(config, "dutAdminPwd", ""),
        "setCommunity": getattr(config, "dutSet", getattr(dut, "set_community", "")),
        "getCommunity": getattr(config, "dutGet", getattr(dut, "get_community", "")),
        "snmpVersion": getattr(config, "dutSnmpVer", getattr(dut, "snmp_ver", "SNMP V3")),
        "snmpv3level": getattr(config, "dutSnmp3Auth", getattr(dut, "snmp3_auth", "Authentication and privacy")),
        "snmpv3hash": getattr(config, "dutSnmp3Hash", getattr(dut, "snmp3_hash", "SHA")),
        "snmpv3encrypt": getattr(config, "dutSnmp3Encrypt", getattr(dut, "snmp3_encrypt", "AES")),
        "dev_sshPort": "22",
        "geoPosition": getattr(config, "dutAddr", getattr(dut, "geo_position", "")),
    }


def open_map_management(driver):
    navigate_to(driver, "System", "Security")
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.LINK_TEXT, "Map Management"))).click()
    WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.ID, "node_id_0")))


def remember_device_settings_from_edit(driver, dut_ip, fallback_settings):
    open_map_management(driver)
    _select_device_by_ip(driver, dut_ip)
    _click_device_button(driver, 1)
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "deviceName")))

    settings = dict(fallback_settings)
    # Credentials (user/password/communities) are masked or empty in the edit
    # form; reading them back and re-adding the device with them leaves the
    # device "Linked" forever.  Keep the configured credentials instead.
    for field_id in [
        "deviceName",
        "description",
        "deviceIP",
        "snmpVersion",
        "snmpv3level",
        "snmpv3hash",
        "snmpv3encrypt",
        "dev_sshPort",
        "geoPosition",
    ]:
        value = _field_value(driver, field_id)
        if value:
            settings[field_id] = value

    _close_device_form(driver)
    return settings


def delete_device_by_ip(driver, dut_ip):
    open_map_management(driver)
    _select_device_by_ip(driver, dut_ip)
    _click_device_button(driver, 1)
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "deviceName")))
    _click_device_button(driver, 2)
    _accept_alert_if_present(driver, timeout=5)
    _confirm_message(driver)
    time.sleep(10)


def add_device_under_ems(driver, settings):
    open_map_management(driver)
    root_node = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, "node_id_0")))
    ActionChains(driver).move_to_element(root_node).pause(0.2).click(root_node).perform()
    _click_add_device_icon(driver)
    WebDriverWait(driver, 60).until(lambda d: "Create Node" in d.find_element(By.TAG_NAME, "body").text)

    WebDriverWait(driver, 60).until(lambda d: _field_is_editable(d, "deviceIP"))
    _select_if_present(driver, "snmpVersion", settings.get("snmpVersion", "SNMP V3"))
    _select_if_present(driver, "snmpv3level", settings.get("snmpv3level", "Authentication and privacy"))
    _select_if_present(driver, "snmpv3hash", settings.get("snmpv3hash", "SHA"))
    _select_if_present(driver, "snmpv3encrypt", settings.get("snmpv3encrypt", "AES"))

    for field_id in [
        "deviceName",
        "description",
        "deviceIP",
        "userName",
        "dev_password",
        "setCommunity",
        "getCommunity",
        "dev_sshPort",
        "geoPosition",
    ]:
        _set_field_if_present(driver, field_id, settings.get(field_id, ""))

    _click_if_present(driver, By.ID, "geoPositionSearch", timeout=3)
    _click_visible_first_present(
        driver,
        [
            (By.XPATH, "//input[@value='Apply']"),
            (By.XPATH, "//button[normalize-space()='Apply']"),
        ],
        timeout=30,
    )
    _accept_alert_if_present(driver, timeout=5)
    _confirm_message(driver)
    WebDriverWait(driver, 300).until(lambda d: _device_nodes_by_ip(d, settings.get("deviceIP", "")))


def ensure_device_exists(driver, settings):
    dut_ip = settings.get("deviceIP", "")
    open_map_management(driver)
    time.sleep(3)
    open_map_management(driver)
    if _device_nodes_by_ip(driver, dut_ip):
        return
    add_device_under_ems(driver, settings)


def update_device_settings_by_ip(driver, dut_ip, settings):
    open_map_management(driver)
    _select_device_by_ip(driver, dut_ip)
    _click_device_button(driver, 1)
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "deviceName")))

    _select_if_present(driver, "snmpVersion", settings.get("snmpVersion", "SNMP V3"))
    _select_if_present(driver, "snmpv3level", settings.get("snmpv3level", "Authentication and privacy"))
    _select_if_present(driver, "snmpv3hash", settings.get("snmpv3hash", "SHA"))
    _select_if_present(driver, "snmpv3encrypt", settings.get("snmpv3encrypt", "AES"))

    for field_id in [
        "deviceName",
        "description",
        "deviceIP",
        "userName",
        "dev_password",
        "setCommunity",
        "getCommunity",
        "dev_sshPort",
        "geoPosition",
    ]:
        _set_field_if_present(driver, field_id, settings.get(field_id, ""))

    _click_visible_first_present(
        driver,
        [
            (By.XPATH, "//input[@value='Save']"),
            (By.XPATH, "//button[normalize-space()='Save']"),
            (By.XPATH, "//input[@value='Apply']"),
            (By.XPATH, "//button[normalize-space()='Apply']"),
        ],
        timeout=30,
    )
    _accept_alert_if_present(driver, timeout=10)
    _confirm_message(driver)


def _select_device_by_ip(driver, dut_ip):
    nodes = _device_nodes_by_ip(driver, dut_ip)
    if not nodes:
        raise AssertionError(f"Cannot find device in Map Management. IP={dut_ip}")
    node = nodes[0]
    driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'nearest'});", node)
    node.click()
    time.sleep(0.5)


def _device_nodes_by_ip(driver, dut_ip):
    if not dut_ip:
        return []
    preferred_xpath = f"//small[contains(normalize-space(.), '({dut_ip})')]"
    preferred_nodes = [element for element in driver.find_elements(By.XPATH, preferred_xpath) if _is_displayed(element)]
    if preferred_nodes:
        return preferred_nodes
    fallback_xpath = f"//*[contains(normalize-space(.), '{dut_ip}')]"
    return [element for element in driver.find_elements(By.XPATH, fallback_xpath) if _is_displayed(element)]


def _click_device_button(driver, index):
    selector = f".device_button:nth-child({index})"

    def visible_enabled_button(_):
        for button in driver.find_elements(By.CSS_SELECTOR, selector):
            try:
                if button.is_displayed() and button.is_enabled():
                    return button
            except Exception:
                continue
        return False

    button = WebDriverWait(driver, 30).until(visible_enabled_button)
    driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'nearest'});", button)
    button.click()


def _click_add_device_icon(driver):
    icon = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "i_action_create_device")))

    def icon_is_visible(_):
        return icon if icon.is_displayed() else False

    WebDriverWait(driver, 30).until(icon_is_visible)
    rect = driver.execute_script(
        "const r = arguments[0].getBoundingClientRect(); return {x:r.x,y:r.y,width:r.width,height:r.height};",
        icon,
    )
    if rect.get("width", 0) > 1 and rect.get("height", 0) > 1:
        x = rect["x"] + rect["width"] / 2
        y = rect["y"] + rect["height"] / 2
    else:
        x = driver.execute_script("return window.innerWidth - 55;")
        y = 195
    driver.execute_cdp_cmd("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": x, "y": y})
    driver.execute_cdp_cmd("Input.dispatchMouseEvent", {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1})
    driver.execute_cdp_cmd("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1})


def _field_value(driver, field_id):
    try:
        element = driver.find_element(By.ID, field_id)
        if element.tag_name.lower() == "select":
            from selenium.webdriver.support.select import Select

            selected = Select(element).first_selected_option
            return (selected.text or "").strip()
        return (element.get_attribute("value") or element.text or "").strip()
    except Exception:
        return ""


def _set_field_if_present(driver, field_id, value):
    try:
        field = driver.find_element(By.ID, field_id)
    except Exception:
        return False
    if not field.is_enabled():
        return False
    if value is None:
        value = ""
    try:
        field.clear()
    except Exception:
        pass
    field.send_keys(str(value))
    return True


def _select_if_present(driver, field_id, visible_text):
    try:
        field = driver.find_element(By.ID, field_id)
    except Exception:
        return False
    if not field.is_displayed() or not field.is_enabled():
        return False
    from selenium.webdriver.support.select import Select

    selector = Select(field)
    expected = str(visible_text or "").strip()
    for option in selector.options:
        if option.text.strip() == expected:
            selector.select_by_visible_text(option.text)
            return True
    return False


def _field_is_editable(driver, field_id):
    try:
        field = driver.find_element(By.ID, field_id)
        return field.is_displayed() and field.is_enabled() and not field.get_attribute("readonly")
    except Exception:
        return False


def _close_device_form(driver):
    _click_first_present(
        driver,
        [
            (By.XPATH, "//button[normalize-space()='Cancel']"),
            (By.XPATH, "//input[@value='Cancel']"),
            (By.CSS_SELECTOR, ".modal-header .close"),
            (By.CSS_SELECTOR, ".close"),
        ],
        timeout=5,
        raise_on_missing=False,
    )
    _accept_alert_if_present(driver, timeout=2)


def _confirm_message(driver):
    WebDriverWait(driver, 180).until(EC.presence_of_element_located((By.ID, "message_text")))
    message = driver.find_element(By.ID, "message_text").text.strip()
    if message and "success" not in message.lower() and "operation success" not in message.lower():
        raise AssertionError(f"Unexpected Map Management message: {message}")
    _click_first_present(
        driver,
        [
            (By.CSS_SELECTOR, "#message_diag .button"),
            (By.XPATH, "//*[@id='message_diag']//button[normalize-space()='OK']"),
            (By.XPATH, "//*[@id='message_diag']//input[@value='OK']"),
            (By.XPATH, "//*[@id='message_diag']//*[contains(@class,'button')]"),
            (By.XPATH, "//*[contains(@class,'button') and (normalize-space()='OK' or @value='OK')]"),
        ],
        timeout=30,
    )


def _accept_alert_if_present(driver, timeout=5):
    try:
        WebDriverWait(driver, timeout).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print(f"Map Management helper: accept alert: {alert.text}", flush=True)
        alert.accept()
        return True
    except (NoAlertPresentException, TimeoutException):
        return False


def _click_if_present(driver, by, value, timeout=5):
    try:
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value))).click()
        return True
    except TimeoutException:
        return False


def _click_first_present(driver, locators, timeout=10, raise_on_missing=True):
    end_time = time.time() + timeout
    last_error = None
    while time.time() < end_time:
        for by, value in locators:
            try:
                WebDriverWait(driver, 1).until(EC.element_to_be_clickable((by, value))).click()
                return True
            except Exception as exc:
                last_error = exc
                if _accept_alert_if_present(driver, timeout=1):
                    return True
        time.sleep(0.2)
    if raise_on_missing:
        raise TimeoutException(f"Cannot click any locator from {locators}. last_error={last_error}")
    return False


def _click_visible_first_present(driver, locators, timeout=10, raise_on_missing=True):
    end_time = time.time() + timeout
    last_error = None
    while time.time() < end_time:
        for by, value in locators:
            try:
                for element in driver.find_elements(by, value):
                    if element.is_displayed() and element.is_enabled():
                        target = element
                        if element.tag_name.lower() == "a" and element.get_attribute("title"):
                            parent = driver.execute_script("return arguments[0].parentElement;", element)
                            if parent is not None and parent.is_displayed():
                                target = parent
                        driver.execute_script(
                            "arguments[0].scrollIntoView({block:'center', inline:'nearest'});",
                            target,
                        )
                        ActionChains(driver).move_to_element(target).pause(0.2).click(target).perform()
                        if element.tag_name.lower() == "a" and element.get_attribute("title") == "Add":
                            time.sleep(0.5)
                            driver.execute_script("arguments[0].click();", element)
                        return True
            except Exception as exc:
                last_error = exc
        time.sleep(0.2)
    if raise_on_missing:
        raise TimeoutException(f"Cannot click visible locator from {locators}. last_error={last_error}")
    return False


def _is_displayed(element):
    try:
        return element.is_displayed()
    except Exception:
        return False
