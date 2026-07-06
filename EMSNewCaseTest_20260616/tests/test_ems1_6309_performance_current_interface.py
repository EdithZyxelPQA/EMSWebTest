import time

import pytest
from selenium.common.exceptions import TimeoutException

from libs.browser import create_browser
from libs.ems_performance import (
    available_probe_count,
    close_all_current_charts,
    close_create_demand,
    create_interface_current_charts_in_open_dialog,
    interface_port_options,
    open_create_demand,
    refresh_current_page,
    wait_for_all_charts_with_visual_data,
)
from libs.ems_ui import login_ems


@pytest.mark.ems
@pytest.mark.selenium
@pytest.mark.node
class TestEMS16309PerformanceCurrentInterface:
    driver = None

    @pytest.fixture(autouse=True)
    def setup_browser(self):
        print("EMS1-6309: create browser", flush=True)
        self.driver = create_browser(self.browser, self.downloadpath)
        self.driver.implicitly_wait(self.waitTime)
        self.driver.set_page_load_timeout(60)
        print("EMS1-6309: maximize browser", flush=True)
        self.driver.maximize_window()
        print("EMS1-6309: browser ready", flush=True)
        yield
        if self.driver:
            self.driver.quit()
            self.driver = None

    def test_EMS1_6309_peformanceCurrentInterface(self):
        cards = self._interface_cards()
        if not cards:
            pytest.skip("EMS1-6309 requires interface cards in environment_parameter.json CARDINFO.")

        print("EMS1-6309: login EMS", flush=True)
        self._open_ems()
        login_ems(self.driver, self.emsUsr, self.emsPwd)

        print("EMS1-6309: close all existing Performance/Current charts", flush=True)
        close_all_current_charts(self.driver)

        try:
            for card_index, card in enumerate(cards, start=1):
                print(
                    f"EMS1-6309: test card {card_index}/{len(cards)} "
                    f"slot={card['slot_id']} card={card['type']}",
                    flush=True,
                )
                for performance_type in ["Interface(Accumulation)", "Interface(Rate)"]:
                    targets = self._discover_card_targets(performance_type, card)
                    self._create_and_verify_card_ports(performance_type, targets)
                    print(
                        f"EMS1-6309: close all {performance_type} charts "
                        f"for slot={card['slot_id']} card={card['type']}",
                        flush=True,
                    )
                    close_all_current_charts(self.driver)
        finally:
            print("EMS1-6309: close all Performance/Current charts", flush=True)
            close_all_current_charts(self.driver)

    def _discover_card_targets(self, performance_type, card):
        print(
            f"EMS1-6309: discover ports for {performance_type} "
            f"slot={card['slot_id']} card={card['type']}",
            flush=True,
        )
        targets = []
        open_create_demand(self.driver)
        try:
            ports = interface_port_options(
                self.driver,
                performance_type,
                self.dutNodeName,
                card["slot_id"],
                card["type"],
            )
        finally:
            close_create_demand(self.driver)
        print(
            f"EMS1-6309: selectable ports for slot={card['slot_id']} card={card['type']}: {ports}",
            flush=True,
        )
        for port_id in ports:
            targets.append({**card, "port_id": port_id})
        assert targets, (
            f"No Performance/Current port options found for {performance_type} "
            f"slot={card['slot_id']} card={card['type']}"
        )
        print(f"EMS1-6309: {performance_type} targets={self._target_names(performance_type, targets)}", flush=True)
        return targets

    def _create_and_verify_card_ports(self, performance_type, targets):
        print(f"EMS1-6309: check available probes for {performance_type}", flush=True)
        open_create_demand(self.driver)
        try:
            available = available_probe_count(self.driver)
            print(
                f"EMS1-6309: available probes for {performance_type}: {available}, required={len(targets)}",
                flush=True,
            )
            assert available >= len(targets), (
                f"available probes should be enough for card ports. available={available}, required={len(targets)}"
            )
        finally:
            close_create_demand(self.driver)

        print(f"EMS1-6309: batch create {len(targets)} {performance_type} charts", flush=True)
        open_create_demand(self.driver)
        try:
            first_target = targets[0]
            create_interface_current_charts_in_open_dialog(
                self.driver,
                performance_type,
                self.dutNodeName,
                first_target["slot_id"],
                first_target["type"],
                [target["port_id"] for target in targets],
            )
        finally:
            close_create_demand(self.driver)

        print(f"EMS1-6309: refresh and wait 30 seconds for {performance_type} chart data", flush=True)
        refresh_current_page(self.driver)
        time.sleep(30)
        print(f"EMS1-6309: verify canvas line/point and numeric values for {performance_type}", flush=True)
        chart_states = wait_for_all_charts_with_visual_data(
            self.driver,
            expected_count=len(targets),
            timeout=360,
        )
        print(f"EMS1-6309: {performance_type} chart visual states: {chart_states}", flush=True)

    def _interface_cards(self):
        cards = []
        for card in self.dutCardInfo.values():
            card_type = card.get("type", "")
            port_type = card.get("port_type", "")
            if any(token in f"{card_type} {port_type}" for token in ["NXC", "NXA", "NXP", "MSC", "GLC", "OLC"]):
                cards.append({"slot_id": str(card["slot_id"]), "type": card_type})
        return cards

    def _target_names(self, performance_type, targets):
        return [
            f"{performance_type} : {self.dutNodeName} - {target['type']}({target['slot_id']}) - "
            f"{target['port_id']}, Polling : 1 Minutes"
            for target in targets
        ]

    def _open_ems(self):
        try:
            self.driver.get(self.emsURL)
        except TimeoutException:
            print("EMS1-6309: EMS page load timeout; continue with current page", flush=True)
