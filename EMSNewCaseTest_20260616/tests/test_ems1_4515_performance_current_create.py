import time

import pytest
from pytest_assume.plugin import assume
from selenium.common.exceptions import TimeoutException

from libs.browser import create_browser
from libs.ems_performance import (
    available_probe_count,
    close_all_current_charts,
    create_interface_current_chart,
    current_iframe_count,
    open_create_demand,
    wait_for_chart,
)
from libs.ems_ui import login_ems


@pytest.mark.ems
@pytest.mark.selenium
@pytest.mark.node
class TestEMS14515PerformanceCurrentCreate:
    driver = None

    @pytest.fixture(autouse=True)
    def setup_browser(self):
        print("EMS1-4515: create browser", flush=True)
        self.driver = create_browser(self.browser, self.downloadpath)
        self.driver.implicitly_wait(self.waitTime)
        self.driver.set_page_load_timeout(60)
        print("EMS1-4515: maximize browser", flush=True)
        self.driver.maximize_window()
        print("EMS1-4515: browser ready", flush=True)
        yield
        if self.driver:
            self.driver.quit()
            self.driver = None

    def test_EMS1_4515_peformanceCurrentCreate(self):
        nxc = self.dutCardInfo.get("NXC")
        if not nxc:
            pytest.skip("EMS1-4515 requires an NXC card in environment_parameter.json.")

        slot_id = str(nxc["slot_id"])
        card_type = nxc["type"]
        port_id = str(nxc["port_id"])
        title_base = f"{self.dutNodeName} - {card_type}({slot_id}) - {port_id}, Polling : 1 Minutes"

        print("EMS1-4515: login EMS")
        self._open_ems()
        login_ems(self.driver, self.emsUsr, self.emsPwd)

        print("EMS1-4515: close all existing Performance/Current charts")
        close_all_current_charts(self.driver)

        try:
            print("EMS1-4515: create Interface(Accumulation) chart")
            open_create_demand(self.driver)
            first_available = available_probe_count(self.driver)
            assert first_available >= 100, f"available probes should be >= 100 after closing charts, got {first_available}"
            create_interface_current_chart(
                self.driver,
                "Interface(Accumulation)",
                self.dutNodeName,
                slot_id,
                card_type,
                port_id,
            )
            accumulation_title = f"Interface(Accumulation) : {title_base}"
            time.sleep(120)
            assert current_iframe_count(self.driver) >= 1
            accumulation_values = wait_for_chart(self.driver, accumulation_title, excluded_values={slot_id, port_id, "1"})
            print(f"EMS1-4515: Interface(Accumulation) canvas values: {accumulation_values}")

            print("EMS1-4515: create Interface(Rate) chart")
            open_create_demand(self.driver)
            second_available = available_probe_count(self.driver, timeout=60, expected=first_available - 1)
            assert second_available == first_available - 1, (
                f"available probes should decrease by 1. first={first_available}, second={second_available}"
            )
            create_interface_current_chart(
                self.driver,
                "Interface(Rate)",
                self.dutNodeName,
                slot_id,
                card_type,
                port_id,
            )
            rate_title = f"Interface(Rate) : {title_base}"
            time.sleep(120)
            assert current_iframe_count(self.driver) >= 2
            rate_values = wait_for_chart(self.driver, rate_title, excluded_values={slot_id, port_id, "1"})
            print(f"EMS1-4515: Interface(Rate) canvas values: {rate_values}")
        finally:
            print("EMS1-4515: close all created Performance/Current charts")
            close_all_current_charts(self.driver)

    def _open_ems(self):
        try:
            self.driver.get(self.emsURL)
        except TimeoutException:
            print("EMS1-4515: EMS page load timeout; continue with current page", flush=True)
