import pytest

from libs.browser import create_browser
from libs.device_cli import run_ssh_command, run_ssh_commands
from libs.ems_configuration import (
    apply_ip_name_server,
    assert_apply_rejected,
    open_ip_name_server_page,
    set_ip_name_servers,
    wait_apply_success,
)
from libs.ems_ui import login_ems


@pytest.mark.ems
@pytest.mark.selenium
@pytest.mark.node
class TestEMS17212IpNameServer:
    driver = None
    illegal_special = "@#$%.abc"
    illegal_ip_format = "999.999.999.999"
    valid_first = "8.8.8.8"
    valid_second = "168.95.1.1"

    @pytest.fixture(autouse=True)
    def setup_browser(self):
        self.driver = create_browser(self.browser, self.downloadpath)
        self.driver.implicitly_wait(self.waitTime)
        self.driver.maximize_window()
        yield
        if "NeoX" in self.dutType:
            self._clear_ip_nameserver_for_current_dut_bug()
        if self.driver:
            self.driver.quit()
            self.driver = None

    def test_EMS1_7212_ipNameServer(self):
        if "NeoX" not in self.dutType:
            pytest.skip("EMS1-7212 IP Name Server is supported only on NeoX devices.")

        self._clear_ip_nameserver_for_current_dut_bug()

        print("EMS1-7212: login EMS")
        self.driver.get(self.emsURL)
        login_ems(self.driver, self.emsUsr, self.emsPwd)
        print("EMS1-7212: open IP Name Server page")
        open_ip_name_server_page(self.driver, self.dutNodeName)

        print("EMS1-7212: apply two invalid values")
        set_ip_name_servers(self.driver, self.illegal_special, self.illegal_ip_format)
        apply_ip_name_server(self.driver)
        assert_apply_rejected(self.driver)
        print("EMS1-7212: verify invalid values were not applied")
        output = self._show_ip_nameserver()
        assert self.illegal_special not in output
        assert self.illegal_ip_format not in output

        print("EMS1-7212: apply first valid and second invalid value")
        set_ip_name_servers(self.driver, self.valid_first, self.illegal_ip_format)
        apply_ip_name_server(self.driver)
        assert_apply_rejected(self.driver)
        print("EMS1-7212: verify second invalid value was not applied")
        output = self._show_ip_nameserver()
        assert self.illegal_ip_format not in output

        print("EMS1-7212: apply final valid values")
        set_ip_name_servers(self.driver, self.valid_first, self.valid_second)
        apply_ip_name_server(self.driver)
        success_message = wait_apply_success(self.driver)
        assert "Success" in success_message
        print("EMS1-7212: verify final valid values by SSH")
        output = self._show_ip_nameserver()
        assert self.valid_first in output
        assert self.valid_second in output

    def _clear_ip_nameserver_for_current_dut_bug(self):
        # WORKAROUND for current DUT bug:
        # The DUT may keep stale IP name server entries that affect EMS validation/apply.
        # TODO: Remove this pre-clean/post-clean after the DUT bug is fixed and restore normal test setup.
        run_ssh_commands(
            self.dutIp,
            self.dutAdminName,
            self.dutAdminPwd,
            ["configure", "no ip nameserver 1", "no ip nameserver 2"],
        )

    def _show_ip_nameserver(self):
        return run_ssh_command(
            self.dutIp,
            self.dutAdminName,
            self.dutAdminPwd,
            "show ip nameserver",
        )
