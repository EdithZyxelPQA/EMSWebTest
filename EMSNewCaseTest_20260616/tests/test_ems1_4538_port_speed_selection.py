import re

import pytest
from pytest_assume.plugin import assume
from selenium.common.exceptions import NoSuchElementException

from libs.browser import create_browser
from libs.device_cli import run_ssh_command
from libs.ems_configuration import (
    apply_port_speed,
    current_port_speed,
    open_port_speed_page,
    port_speed_options,
    select_port_for_speed,
)
from libs.ems_ui import login_ems


@pytest.mark.ems
@pytest.mark.selenium
@pytest.mark.node
class TestEMS14538PortSpeedSelection:
    driver = None

    @pytest.fixture(autouse=True)
    def setup_browser(self):
        self.driver = create_browser(self.browser, self.downloadpath)
        self.driver.implicitly_wait(self.waitTime)
        self.driver.maximize_window()
        yield
        if self.driver:
            self.driver.quit()
            self.driver = None

    def test_EMS1_4538_portSpeedSelection(self):
        if not self._is_supported_device():
            pytest.skip("EMS1-4538 supports only NeoX and IES devices.")

        print("EMS1-4538: login EMS")
        self.driver.get(self.emsURL)
        login_ems(self.driver, self.emsUsr, self.emsPwd)

        main_page, main_card = self._main_port_target()
        ge_cards = self._ge_port_targets()
        if main_card is None and not ge_cards:
            pytest.skip("No NXC/MSC/GLC card information is available for EMS1-4538.")

        if main_card is not None:
            self._exercise_port_page(main_page, main_card, self._main_show_command(main_page, main_card))

        for card in ge_cards:
            self._exercise_port_page("GE", card, self._ge_show_command(card))

    def _exercise_port_page(self, port_page, card, show_command):
        slot_id = str(card["slot_id"])
        port_id = str(card["port_id"])
        card_type = card.get("type", "")

        print(f"EMS1-4538: open Port/{port_page} for {card_type} slot {slot_id} port {port_id}")
        open_port_speed_page(self.driver, self.dutNodeName, port_page)
        select_port_for_speed(self.driver, port_page, slot_id, port_id)
        original_speed_label, original_speed_value = current_port_speed(self.driver, port_page)
        options = port_speed_options(self.driver, port_page)
        assert options, f"No speed options found on Port/{port_page}."
        self._assert_detect_option_for_nxc_nxa(card_type, port_page, slot_id, port_id, options)

        try:
            for speed_label, _speed_value in options:
                print(f"EMS1-4538: set Port/{port_page} {slot_id}-{port_id} Speed={speed_label}")
                try:
                    success_message, selected_value = apply_port_speed(self.driver, port_page, speed_label)
                except NoSuchElementException as exc:
                    with assume:
                        assert False, (
                            f"Port/{port_page} {card_type} slot {slot_id} port {port_id} "
                            f"Speed option disappeared before apply: {speed_label}. Error: {exc}"
                        )
                    continue
                assert "Success" in success_message

                output = run_ssh_command(
                    self.dutIp,
                    self.dutAdminName,
                    self.dutAdminPwd,
                    show_command,
                )
                self._assert_speed_visible_in_cli(output, speed_label, selected_value, show_command)
        finally:
            self._restore_original_speed(
                port_page,
                card_type,
                slot_id,
                port_id,
                show_command,
                original_speed_label,
                original_speed_value,
            )

    def _main_port_target(self):
        if "NeoX" in self.dutType:
            return "NNI", self._card_by_key_or_type("NXC")
        if "IES" in self.dutType:
            return "GENNI", self._card_by_key_or_type("MSC")
        return None, None

    def _ge_port_targets(self):
        targets = []
        for key, card in self.dutCardInfo.items():
            card_text = f"{key} {card.get('type', '')}"
            port_type = card.get("port_type", "")
            if "NeoX" in self.dutType and ("Ethernet Access" in port_type or "NXA" in card_text):
                targets.append(card)
            elif "IES" in self.dutType and "GLC" in card_text:
                targets.append(card)
        return targets

    def _main_show_command(self, port_page, card):
        port_id = card["port_id"]
        if port_page == "NNI":
            return f"show interface nni {port_id} config"
        return f"show interface genni {port_id} config"

    def _ge_show_command(self, card):
        return f"show interface ge {card['slot_id']}-{card['port_id']} config"

    def _card_by_key_or_type(self, token):
        for key, card in self.dutCardInfo.items():
            if token in f"{key} {card.get('type', '')}":
                return card
        return None

    def _is_supported_device(self):
        return "NeoX" in self.dutType or "IES" in self.dutType

    def _assert_detect_option_for_nxc_nxa(self, card_type, port_page, slot_id, port_id, options):
        if "NXC" not in card_type and "NXA" not in card_type:
            return

        labels = [label for label, _value in options]
        with assume:
            assert any(label.strip().lower() == "detect" for label in labels), (
                f"Port/{port_page} {card_type} slot {slot_id} port {port_id} "
                f"Speed options must include Detect. Actual options: {labels}"
            )

    def _restore_original_speed(
        self,
        port_page,
        card_type,
        slot_id,
        port_id,
        show_command,
        original_speed_label,
        original_speed_value,
    ):
        current_label, current_value = current_port_speed(self.driver, port_page)
        if current_label == original_speed_label or current_value == original_speed_value:
            return

        print(
            f"EMS1-4538: restore Port/{port_page} {slot_id}-{port_id} "
            f"Speed={original_speed_label}"
        )
        try:
            success_message, selected_value = apply_port_speed(self.driver, port_page, original_speed_label)
        except NoSuchElementException as exc:
            with assume:
                assert False, (
                    f"Port/{port_page} {card_type} slot {slot_id} port {port_id} "
                    f"could not restore original Speed={original_speed_label}. Error: {exc}"
                )
            return
        assert "Success" in success_message

        output = run_ssh_command(
            self.dutIp,
            self.dutAdminName,
            self.dutAdminPwd,
            show_command,
        )
        self._assert_speed_visible_in_cli(output, original_speed_label, selected_value, show_command)

    def _assert_speed_visible_in_cli(self, output, speed_label, selected_value, show_command):
        cli_text = _normalize_speed_text(output)
        candidates = _speed_candidates(speed_label, selected_value)
        if any(candidate and candidate in cli_text for candidate in candidates):
            return
        raise AssertionError(
            f"Speed {speed_label!r} was not found after '{show_command}'. "
            f"Candidates={sorted(candidates)} Output:\n{output}"
        )


def _speed_candidates(label, value):
    candidates = {_normalize_speed_text(label), _normalize_speed_text(value)}
    text = label.lower()
    value_text = value.lower()

    if "auto" in text or value_text == "auto":
        candidates.add("auto")
    for base in ("10m", "100m", "1g", "2.5g", "5g", "10g", "25g", "40g", "100g"):
        if base in text or base in value_text:
            candidates.add(base)
            if "full" in text or "full" in value_text:
                candidates.add(base + "full")
            if "half" in text or "half" in value_text:
                candidates.add(base + "half")
    match = re.search(r"(\d+(?:\.\d+)?[gm])(?:-\d+x)?(?:-[a-z]+)?-(?:full|half)", text)
    if match:
        candidates.add(_normalize_speed_text(text.rsplit("-", 1)[0]))
    return {candidate for candidate in candidates if candidate}


def _normalize_speed_text(value):
    return re.sub(r"[^a-z0-9]+", "", str(value).lower())
