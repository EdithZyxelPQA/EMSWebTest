import re
import time

import pytest
from pytest_assume.plugin import assume
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from libs.browser import create_browser
from libs.device_cli import run_console_commands
from libs.ems_tables import navigate_to, table_rows, total_data
from libs.ems_ui import login_ems


EXPECTED_DOWN_STATUS = "Device Not Responding"


@pytest.mark.ems
@pytest.mark.selenium
@pytest.mark.node
class TestEMS17214DeviceStatusDown:
    driver = None

    @pytest.fixture(autouse=True)
    def setup_browser(self):
        print("EMS1-7214: create browser", flush=True)
        self.driver = create_browser(self.browser, self.downloadpath)
        print("EMS1-7214: browser created", flush=True)
        self.driver.implicitly_wait(self.waitTime)
        self.driver.set_page_load_timeout(60)
        print("EMS1-7214: maximize browser", flush=True)
        self.driver.maximize_window()
        print("EMS1-7214: browser ready", flush=True)
        yield
        if self.driver:
            self.driver.quit()
            self.driver = None

    def test_EMS1_7214_deviceStatusDown(self):
        if not self._is_supported_device():
            pytest.skip("EMS1-7214 supports only NeoX and IES devices.")

        disabled = False
        print("EMS1-7214: login EMS")
        self._open_ems()
        login_ems(self.driver, self.emsUsr, self.emsPwd)

        try:
            print("EMS1-7214: verify device status is Up")
            current_status = self._current_device_status()
            if current_status != "Up":
                print(f"EMS1-7214: initial device status is {current_status}; enable all uplink ports first")
                self._set_uplink_ports(enable=True, verify=True)
            self._wait_device_status("Up", timeout=600)

            print("EMS1-7214: disable uplink ports by console")
            self._set_uplink_ports(enable=False)
            disabled = True

            print("EMS1-7214: wait device status Down")
            self._wait_device_status("Down", timeout=600)

            print("EMS1-7214: wait 60 seconds before inventory/dashboard checks")
            time.sleep(60)
            self._check_inventory_down_pages()
            self._check_dashboard_down_status()
        finally:
            if disabled:
                print("EMS1-7214: restore uplink ports by console")
                self._set_uplink_ports(enable=True, verify=True)
                print("EMS1-7214: wait device status back to Up")
                self._wait_device_status("Up", timeout=600)

    def _set_uplink_ports(self, enable, verify=False):
        action = "enable" if enable else "disable"
        interface_type = "nni" if "NeoX" in self.dutType else "genni"
        interface_command = f"interface {interface_type} *"
        if not self.dutConsolePort:
            raise RuntimeError("Console port is required for EMS1-7214 because disabling uplink may break in-band access.")
        commands = ["configure", interface_command, action, "exit", "exit"]
        if verify:
            commands.append(f"show interface {interface_type} * config")
        output = run_console_commands(
            self.dutConsolePort,
            self.dutConsoleBaudrate,
            self.dutConsoleName,
            self.dutConsolePwd,
            commands,
            timeout=90,
        )
        with assume:
            assert "% Invalid" not in output and "Unknown command" not in output, output
        if verify:
            active_statuses = _interface_active_statuses(output)
            with assume:
                assert active_statuses and all(status == "Yes" for status in active_statuses.values()), active_statuses

    def _open_ems(self):
        try:
            self.driver.get(self.emsURL)
        except TimeoutException:
            print("EMS1-7214: EMS page load timeout; continue with current page", flush=True)

    def _current_device_status(self):
        self._filter_device()
        rows = table_rows(self.driver, "dev_inventory_div")
        row = _single_row_for_ip(rows, self.dutIp)
        return _first_value(row, ["DevStatus", "Operational Status", "OperationStatus", "Status"])

    def _wait_device_status(self, expected_status, timeout):
        self._filter_device()
        end_time = time.time() + timeout
        last_status = ""
        while time.time() < end_time:
            rows = table_rows(self.driver, "dev_inventory_div")
            try:
                row = _single_row_for_ip(rows, self.dutIp)
            except AssertionError:
                last_status = f"rows={rows}"
                self._refresh()
                time.sleep(5)
                continue
            status = _first_value(row, ["DevStatus", "Operational Status", "OperationStatus", "Status"])
            last_status = f"{status}, row={row}"
            if status == expected_status:
                return row
            self._refresh()
            time.sleep(5)
        raise AssertionError(f"Device status did not become {expected_status}. Last status: {last_status}")

    def _check_inventory_down_pages(self):
        print("EMS1-7214: check Inventory/Card")
        self._filter_card()
        self._assume_rows_status(
            "Inventory/Card",
            table_rows(self.driver, "card_inventory_div"),
            ["OperationStatus", "Operation Status"],
            require_rows=True,
        )

        for page_name, filter_method, should_exist in self._port_pages_to_check():
            print(f"EMS1-7214: check Inventory/Port/{page_name}")
            filter_method()
            rows = table_rows(self.driver, "port_inventory_div")
            self._assume_rows_status(
                f"Inventory/Port/{page_name}",
                rows,
                ["portOperationStatus", "OperationStatus", "Operation Status"],
                require_rows=should_exist,
            )

        print("EMS1-7214: check Inventory/ONT")
        self._filter_ont()
        self._assume_rows_status(
            "Inventory/ONT",
            table_rows(self.driver, "ont_inventory_div"),
            ["OntOperationStatus", "OperationStatus", "Operation Status"],
            require_rows=False,
        )

    def _check_dashboard_down_status(self):
        print("EMS1-7214: check Dashboard/ONT Status")
        status_count = self._dashboard_status_link_count("ontStatus")
        for index in range(1, status_count + 1):
            navigate_to(self.driver, "Dashboard")
            status_link = self.driver.find_element(
                By.XPATH,
                f"(//div[@id='ontStatus']//a[string-length(normalize-space()) > 0])[{index}]",
            )
            status_text = status_link.text.strip()
            status_link.click()
            time.sleep(2)
            self._select_dashboard_device_if_present()
            with assume:
                assert total_data(self.driver, "All_ontStatusTable") == 0, f"ONT Status {status_text or index}"

        print("EMS1-7214: check Dashboard/Ethernet Access Port Status")
        if self._has_ethernet_access_card():
            navigate_to(self.driver, "Dashboard")
            self.driver.find_element(By.CSS_SELECTOR, "#gePortStatusList a[data-value='99']").click()
            time.sleep(3)
            rows = _try_table_rows(self.driver, "All_gePortStatusTable")
            with assume:
                assert any(self.dutIp in row.values() for row in rows), rows

    def _dashboard_status_link_count(self, status_id):
        navigate_to(self.driver, "Dashboard")
        return len(
            self.driver.find_elements(
                By.XPATH,
                f"//div[@id='{status_id}']//a[string-length(normalize-space()) > 0]",
            )
        )

    def _filter_device(self):
        navigate_to(self.driver, "Inventory", "Device")
        self._open_filter()
        _click_if_present(self.driver, By.ID, "inventory_device_clear_btn")
        _type_if_present(self.driver, By.ID, "ip1", self.dutIp)
        _click_if_present(self.driver, By.ID, "inventory_device_btn")
        _wait_table(self.driver, "dev_inventory_div")

    def _filter_card(self):
        navigate_to(self.driver, "Inventory", "Card")
        self._open_filter()
        _click_if_present(self.driver, By.ID, "inventory_slot_clear_btn")
        _type_if_present(self.driver, By.ID, "deviceName2", self.dutName)
        _type_if_present(self.driver, By.ID, "ip2", self.dutIp)
        _click_if_present(self.driver, By.ID, "inventory_slot_btn")
        _wait_table(self.driver, "card_inventory_div")

    def _filter_all_ports(self):
        navigate_to(self.driver, "Inventory", "Port")
        _click_if_present(self.driver, By.ID, "AllPort")
        self._filter_port_page("all", clear_id="inventory_allport_clear_btn", button_id="inventory_allport_btn")

    def _filter_network_ports(self):
        navigate_to(self.driver, "Inventory", "Port")
        _click_if_present(self.driver, By.LINK_TEXT, "Network Port")
        self._filter_port_page("network")

    def _filter_ethernet_ports(self):
        navigate_to(self.driver, "Inventory", "Port")
        _click_if_present(self.driver, By.LINK_TEXT, "Ethernet Access Port")
        self._filter_port_page("ethernet")

    def _filter_gpon_ports(self):
        navigate_to(self.driver, "Inventory", "Port")
        _click_if_present(self.driver, By.LINK_TEXT, "GPON Port")
        self._filter_port_page("pon")

    def _filter_xpon_ports(self):
        navigate_to(self.driver, "Inventory", "Port")
        _click_if_present(self.driver, By.LINK_TEXT, "xPON Port")
        self._filter_port_page("xpon")

    def _filter_port_page(self, suffix, clear_id=None, button_id=None):
        self._open_filter()
        _click_if_present(self.driver, By.ID, clear_id or f"inventory_{suffix}_clear_btn")
        _type_if_present(self.driver, By.ID, f"deviceName_{suffix}", self.dutName)
        _type_if_present(self.driver, By.ID, f"ip_{suffix}", self.dutIp)
        _click_if_present(self.driver, By.ID, button_id or f"inventory_{suffix}_btn")
        _wait_table(self.driver, "port_inventory_div")

    def _filter_ont(self):
        navigate_to(self.driver, "Inventory", "ONT")
        self._open_filter()
        _click_if_present(self.driver, By.ID, "inventory_allont_clear_btn")
        _type_if_present(self.driver, By.ID, "deviceName_Allont", self.dutName)
        _type_if_present(self.driver, By.ID, "ip_Allont", self.dutIp)
        _click_if_present(self.driver, By.ID, "inventory_allont_btn")
        _wait_table(self.driver, "ont_inventory_div")

    def _port_pages_to_check(self):
        return [
            ("All Ports", self._filter_all_ports, True),
            ("Network Port", self._filter_network_ports, True),
            ("Ethernet Access Port", self._filter_ethernet_ports, self._has_ethernet_access_card()),
            ("GPON Port", self._filter_gpon_ports, self._has_gpon_card()),
            ("xPON Port", self._filter_xpon_ports, self._has_xpon_card()),
        ]

    def _assume_rows_status(self, page_name, rows, status_keys, require_rows):
        matched_rows = [row for row in rows if row.get("IPAddress") == self.dutIp or row.get("DevName") == self.dutName]
        if require_rows:
            with assume:
                assert matched_rows, f"{page_name} should have rows for {self.dutName}/{self.dutIp}. rows={rows}"
        for row in matched_rows:
            status = _first_value(row, status_keys)
            with assume:
                assert status == EXPECTED_DOWN_STATUS, f"{page_name} row status={status}, row={row}"

    def _open_filter(self):
        _click_if_present(self.driver, By.CSS_SELECTOR, "#i_action_filter > a")

    def _refresh(self):
        _click_if_present(self.driver, By.CSS_SELECTOR, "#i_action_refresh > a")

    def _select_dashboard_device_if_present(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, ".comboTreeArrowBtnImg").click()
            label = self.driver.find_element(By.XPATH, f"//label[contains(.,'{self.dutNodeName}')]")
            label.click()
            time.sleep(2)
        except NoSuchElementException:
            pass

    def _click_dashboard_status(self, section_title, status_text):
        navigate_to(self.driver, "Dashboard")
        candidates = self.driver.find_elements(
            By.XPATH,
            f"//*[normalize-space()='{section_title}']/ancestor::div[contains(@class,'panel') or contains(@class,'box')][1]"
            f"//*[normalize-space()='{status_text}']/following::a[1]",
        )
        if not candidates:
            candidates = self.driver.find_elements(By.XPATH, f"//div[contains(.,'{section_title}')]//a[normalize-space()='{status_text}']")
        with assume:
            assert candidates, f"Cannot find Dashboard/{section_title} status {status_text}"
        if candidates:
            candidates[0].click()
            time.sleep(3)

    def _has_ethernet_access_card(self):
        return any("GLC" in _card_text(key, card) or "NXA" in _card_text(key, card) for key, card in self.dutCardInfo.items())

    def _has_gpon_card(self):
        return "OLT" in self.dutType or any("OLC3416-42A" in _card_text(key, card) for key, card in self.dutCardInfo.items())

    def _has_xpon_card(self):
        return any(
            token in _card_text(key, card)
            for key, card in self.dutCardInfo.items()
            for token in ["OLC3146B", "OLC3416B", "OLC3816", "NXP"]
        )

    def _is_supported_device(self):
        return "NeoX" in self.dutType or "IES" in self.dutType


def _single_row_for_ip(rows, dut_ip):
    for row in rows:
        if row.get("IPAddress") == dut_ip:
            return row
    raise AssertionError(f"Cannot find device IP {dut_ip}. rows={rows}")


def _first_value(row, keys):
    for key in keys:
        if row.get(key):
            return row[key]
    return ""


def _card_text(key, card):
    return f"{key} {card.get('type', '')} {card.get('port_type', '')}"


def _interface_active_statuses(output):
    statuses = {}
    cleaned = re.sub(r"\x1b\[[0-9;?]*[A-Za-z]", "", output)
    for line in cleaned.splitlines():
        match = re.match(r"\s*(\d+)\s+\|\s+(Yes|No)\b", line)
        if match:
            statuses[match.group(1)] = match.group(2)
    return statuses


def _click_if_present(driver, by, value):
    try:
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((by, value))).click()
        time.sleep(1)
        return True
    except (NoSuchElementException, TimeoutException):
        return False


def _type_if_present(driver, by, value, text):
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, value)))
    except TimeoutException:
        return False
    element.clear()
    element.send_keys(text)
    return True


def _wait_table(driver, table_id):
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, f"{table_id}_body")))


def _try_table_rows(driver, table_id):
    try:
        return table_rows(driver, table_id)
    except (NoSuchElementException, TimeoutException):
        return []


def _status_count(driver, status_id):
    return len(driver.find_elements(By.XPATH, f"//div[@id='{status_id}']/div"))
