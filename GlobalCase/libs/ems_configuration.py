import re
import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


SUCCESS_PATTERN = re.compile(r"(success|successful|complete|completed)", re.IGNORECASE)
ERROR_PATTERN = re.compile(
    r"(invalid|error|fail|failed|wrong|format|illegal|must|range|not allow|please input valid)",
    re.IGNORECASE,
)


def open_ip_name_server_page(driver, dut_node_name, timeout=180):
    driver.switch_to.default_content()
    _click_top_menu(driver, "Provision", timeout)
    _click_top_menu(driver, "Configuration", timeout)
    _select_configuration_device(driver, dut_node_name, timeout)
    _switch_to_config_frame(driver, timeout)
    _open_config_menu(driver, "System", "IP Name Server", timeout)


def open_port_speed_page(driver, dut_node_name, port_page, timeout=180):
    driver.switch_to.default_content()
    _click_top_menu(driver, "Provision", timeout)
    _click_top_menu(driver, "Configuration", timeout)
    _select_configuration_device(driver, dut_node_name, timeout)
    _switch_to_config_frame(driver, timeout)
    _open_config_menu(driver, "Port", port_page, timeout)


def select_port_for_speed(driver, port_page, slot_id, port_id, timeout=30):
    prefix = _port_prefix(port_page)
    slot_select = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, f"port_{prefix}_slot_combobox"))
    )
    _select_by_value_or_text(slot_select, slot_id)
    time.sleep(1)
    port_select = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, f"port_{prefix}_port_combobox"))
    )
    _select_by_value_or_text(port_select, port_id)
    time.sleep(1)


def port_speed_options(driver, port_page, timeout=30):
    speed_select = _port_speed_select(driver, port_page, timeout)
    options = []
    for option in Select(speed_select).options:
        label = option.text.strip()
        value = (option.get_attribute("value") or "").strip()
        if not label or label in {"--", "Select", "Please Select"}:
            continue
        if option.get_attribute("disabled"):
            continue
        options.append((label, value))
    return options


def current_port_speed(driver, port_page, timeout=30):
    speed_select = _port_speed_select(driver, port_page, timeout)
    selected = Select(speed_select).first_selected_option
    return selected.text.strip(), (selected.get_attribute("value") or "").strip()


def _port_auto_nego_select(driver, timeout=30):
    # The "Auto-Nego" dropdown of the port page (looked up by its label)
    return WebDriverWait(driver, timeout).until(lambda d: next((
        e for e in d.find_elements(
            By.XPATH,
            "//*[normalize-space(text())='Auto-Nego']/following::select[1]",
        ) if e.is_displayed()), False))


def current_port_auto_nego(driver, timeout=30):
    try:
        return Select(_port_auto_nego_select(driver, timeout)).first_selected_option.text.strip()
    except TimeoutException:
        return None


def port_speed_needs_auto_nego_disabled(speed_label):
    # IES: "Error: Auto-nego should be disable in speed=2.5G !" - fixed speeds above 1G
    # (2.5G / 10G) can only be set with auto-negotiation disabled
    text = (speed_label or "").lower()
    return text.startswith("2.5g") or text.startswith("10g")


def apply_port_speed(driver, port_page, speed_label, timeout=60, auto_nego=None):
    # auto_nego: "Enable" / "Disable" to set the Auto-Nego dropdown in the same Apply
    speed_select = _port_speed_select(driver, port_page, timeout)
    select = Select(speed_select)
    if auto_nego:
        Select(_port_auto_nego_select(driver)).select_by_visible_text(auto_nego)
    select.select_by_visible_text(speed_label)
    selected = select.first_selected_option
    selected_value = (selected.get_attribute("value") or "").strip()
    driver.find_element(By.ID, f"port_{_port_prefix(port_page)}_apply_btn").click()
    return wait_apply_success(driver, timeout=timeout), selected_value


def set_ip_name_servers(driver, first_value, second_value):
    first_input, second_input = _name_server_inputs(driver)
    _replace_value(first_input, first_value)
    _replace_value(second_input, second_value)


def apply_ip_name_server(driver, timeout=30):
    _click_apply(driver, timeout)
    time.sleep(1)
    return _visible_message_text(driver)


def wait_apply_success(driver, timeout=90):
    end_time = time.time() + timeout
    last_message = ""
    while time.time() < end_time:
        last_message = _visible_message_text(driver)
        if SUCCESS_PATTERN.search(last_message):
            _close_message_if_present(driver)
            return last_message
        if _message_dialog_button(driver):
            _close_message_if_present(driver)
            return last_message or "Success dialog was displayed."
        time.sleep(1)
    raise AssertionError(f"Did not see successful apply message. Last message: {last_message!r}")


def assert_apply_rejected(driver, timeout=15):
    end_time = time.time() + timeout
    last_message = ""
    while time.time() < end_time:
        last_message = _visible_message_text(driver)
        if ERROR_PATTERN.search(last_message):
            _close_message_if_present(driver)
            return last_message
        time.sleep(0.5)

    validation_text = driver.execute_script(
        """
        const invalid = Array.from(document.querySelectorAll('input,select,textarea'))
          .filter((el) => !el.checkValidity())
          .map((el) => el.validationMessage || el.getAttribute('title') || el.id || el.name)
          .filter(Boolean);
        return invalid.join("\\n");
        """
    )
    if validation_text:
        return validation_text

    raise AssertionError(f"Apply was not rejected with a visible error. Last message: {last_message!r}")


def _click_top_menu(driver, label, timeout):
    element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.LINK_TEXT, label)))
    if element.get_attribute("className") == "":
        element.click()
        time.sleep(3)


def _select_configuration_device(driver, dut_node_name, timeout):
    node_xpath = f"//*[@id='navMenuTree']/ul/li[normalize-space(.)={_xpath_literal(dut_node_name)}]"
    node = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, node_xpath)))
    class_name = node.get_attribute("className") or ""
    if "node-selected" not in class_name and "active" not in class_name:
        node.click()
        time.sleep(3)


def _switch_to_config_frame(driver, timeout):
    driver.switch_to.default_content()
    WebDriverWait(driver, timeout).until(lambda d: len(d.find_elements(By.TAG_NAME, "iframe")) > 0)
    driver.switch_to.frame(0)


def _open_config_menu(driver, main_label, sub_label, timeout):
    main = _first_visible(
        driver,
        [
            (By.LINK_TEXT, main_label),
            (By.XPATH, f"//*[@id='config_menu']//*[normalize-space(.)={_xpath_literal(main_label)}]"),
        ],
        timeout,
    )
    sub_locators = [
        (By.LINK_TEXT, sub_label),
        (By.XPATH, f"//*[@id='config_menu']//*[normalize-space(.)={_xpath_literal(sub_label)}]"),
    ]
    sub = _try_first_visible(driver, sub_locators, timeout=2)
    if sub is None:
        _safe_click(driver, main)
        time.sleep(1)
        sub = _first_visible(driver, sub_locators, timeout)
    _safe_click(driver, sub)
    time.sleep(3)


def _try_first_visible(driver, locators, timeout):
    try:
        return _first_visible(driver, locators, timeout)
    except TimeoutException:
        return None


def _port_prefix(port_page):
    if port_page in {"NNI", "GENNI"}:
        return "genni"
    if port_page == "GE":
        return "ge"
    raise ValueError(f"Unsupported port page: {port_page!r}")


def _port_speed_select(driver, port_page, timeout):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, f"port_{_port_prefix(port_page)}_speed_combobox"))
    )


def _select_by_value_or_text(select_element, value):
    select = Select(select_element)
    value = str(value)
    try:
        select.select_by_value(value)
        return
    except NoSuchElementException:
        pass
    select.select_by_visible_text(value)


def _following_config_panel(driver, main_label):
    try:
        return driver.find_element(
            By.XPATH,
            f"//*[@id='config_menu']/div[normalize-space(.)={_xpath_literal(main_label)}]/following-sibling::div[1]",
        )
    except NoSuchElementException:
        return None


def _name_server_inputs(driver):
    with _temporary_implicit_wait(driver, 0):
        first = _first_visible_by_id_or_name(
            driver,
            [
                "ip_name_server_primary_text",
                "ip_nameserver_primary_text",
                "system_ip_name_server_primary_text",
                "system_ip_nameserver_primary_text",
                "ipNameServer1",
                "ip_nameserver1",
                "nameserver1",
            ],
        )
        second = _first_visible_by_id_or_name(
            driver,
            [
                "ip_name_server_secondary_text",
                "ip_nameserver_secondary_text",
                "system_ip_name_server_secondary_text",
                "system_ip_nameserver_secondary_text",
                "ipNameServer2",
                "ip_nameserver2",
                "nameserver2",
            ],
        )
        candidates = [
            element
            for element in driver.find_elements(By.XPATH, "//input[not(@type='hidden') and not(@disabled)]")
            if element.is_displayed()
        ]
        ip_like_inputs = []
        for element in candidates:
            identity = " ".join(
                filter(
                    None,
                    [
                        element.get_attribute("id"),
                        element.get_attribute("name"),
                        element.get_attribute("placeholder"),
                        element.get_attribute("title"),
                    ],
                )
            ).lower()
            if "name" in identity or "server" in identity or "dns" in identity or "ip" in identity:
                ip_like_inputs.append(element)

    if first is not None and second is not None:
        return first, second
    if len(ip_like_inputs) >= 2:
        return ip_like_inputs[0], ip_like_inputs[1]
    if len(candidates) >= 2:
        return candidates[0], candidates[1]
    raise NoSuchElementException("Could not locate two IP Name Server input fields.")


def _first_visible_by_id_or_name(driver, names):
    for name in names:
        for by in (By.ID, By.NAME):
            try:
                element = driver.find_element(by, name)
            except NoSuchElementException:
                continue
            if element.is_displayed() and element.is_enabled():
                return element
    return None


class _temporary_implicit_wait:
    def __init__(self, driver, seconds):
        self.driver = driver
        self.seconds = seconds
        self.original = None

    def __enter__(self):
        self.original = self.driver.timeouts.implicit_wait
        self.driver.implicitly_wait(self.seconds)

    def __exit__(self, exc_type, exc, traceback):
        self.driver.implicitly_wait(self.original)


def _replace_value(element, value):
    element.click()
    element.clear()
    element.send_keys(value)


def _click_apply(driver, timeout):
    candidates = [
        (By.XPATH, "//input[@value='Apply' or @value='Save']"),
        (By.XPATH, "//button[normalize-space(.)='Apply' or normalize-space(.)='Save']"),
        (By.CSS_SELECTOR, ".button_green"),
        (By.ID, "ip_name_server_apply_btn"),
        (By.ID, "ip_nameserver_apply_btn"),
        (By.ID, "system_ip_name_server_apply_btn"),
    ]
    _first_clickable(driver, candidates, timeout, per_locator_timeout=1).click()


def _visible_message_text(driver):
    texts = []
    selectors = [
        (By.ID, "message_text"),
        (By.CSS_SELECTOR, "#message_diag"),
        (By.CSS_SELECTOR, ".bootbox-body"),
        (By.CSS_SELECTOR, ".alert"),
        (By.CSS_SELECTOR, ".error"),
        (By.CSS_SELECTOR, ".invalid-feedback"),
    ]
    with _temporary_implicit_wait(driver, 0):
        for by, value in selectors:
            for element in driver.find_elements(by, value):
                if element.is_displayed():
                    text = element.text.strip()
                    if text:
                        texts.append(text)
    return "\n".join(texts)


def _message_dialog_button(driver):
    with _temporary_implicit_wait(driver, 0):
        for by, value in [
            (By.CSS_SELECTOR, "#message_diag .button"),
            (By.CSS_SELECTOR, "#message_diag button"),
            (By.XPATH, "//button[normalize-space(.)='OK']"),
            (By.XPATH, "//input[@value='OK']"),
        ]:
            for element in driver.find_elements(by, value):
                if element.is_displayed() and element.is_enabled():
                    return element
    return None


def _close_message_if_present(driver):
    button = _message_dialog_button(driver)
    if button is not None:
        button.click()
        time.sleep(1)


def _first_present(driver, locators, timeout):
    last_error = None
    for locator in locators:
        try:
            return WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))
        except TimeoutException as exc:
            last_error = exc
    raise last_error


def _first_visible(driver, locators, timeout):
    last_error = None
    end_time = time.time() + timeout
    with _temporary_implicit_wait(driver, 0):
        while time.time() < end_time:
            for locator in locators:
                try:
                    elements = driver.find_elements(*locator)
                except TimeoutException as exc:
                    last_error = exc
                    continue
                for element in elements:
                    if element.is_displayed():
                        return element
            time.sleep(0.5)
    if last_error:
        raise last_error
    raise TimeoutException(f"Could not find visible element from locators: {locators!r}")


def _safe_click(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    try:
        element.click()
    except Exception:
        driver.execute_script("arguments[0].click();", element)


def _first_clickable(driver, locators, timeout, per_locator_timeout=None):
    last_error = None
    end_time = time.time() + timeout
    for locator in locators:
        wait_time = per_locator_timeout or timeout
        wait_time = min(wait_time, max(0.1, end_time - time.time()))
        try:
            return WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable(locator))
        except TimeoutException as exc:
            last_error = exc
        if time.time() >= end_time:
            break
    raise last_error


def _xpath_literal(value):
    if "'" not in value:
        return f"'{value}'"
    if '"' not in value:
        return f'"{value}"'
    return "concat(" + ", \"'\", ".join(f"'{part}'" for part in value.split("'")) + ")"
