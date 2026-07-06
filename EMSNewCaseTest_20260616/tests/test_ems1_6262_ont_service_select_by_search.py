import pytest

from libs.browser import create_browser
from libs.device_cli import unregister_ont_by_flag
from libs.ems_tables import (
    create_ont_service_by_select_sn,
    delete_ont_service_if_exists,
    filter_inventory_ont_by_sn,
    wait_inventory_description,
    wait_inventory_ont_id,
    wait_ont_service_success,
)
from libs.ems_ui import login_ems


@pytest.mark.ems
@pytest.mark.selenium
@pytest.mark.node
class TestEMS16262OntServiceSelectBySearch:
    driver = None
    service_description = "testSearchUnregistered"

    @pytest.fixture(autouse=True)
    def setup_browser(self):
        self.driver = create_browser(self.browser, self.downloadpath)
        self.driver.implicitly_wait(self.waitTime)
        self.driver.maximize_window()
        yield
        if self.driver:
            self.driver.quit()
            self.driver = None

    def test_EMS1_6262_ontServiceSelectBySearch(self):
        sn = self.serviceOntSN
        password = self.serviceOntPW
        flag = self.serviceOntFlag
        assert sn, "Missing ZYXEL_DUT.<node>.ONT.<exe_provision_ont>.sn_16"
        assert password, "Missing ZYXEL_DUT.<node>.ONT.<exe_provision_ont>.pw"
        assert flag, "Missing ZYXEL_DUT.<node>.ONT.<exe_provision_ont>.flag"

        unregister_ont_by_flag(self.dutIp, self.dutAdminName, self.dutAdminPwd, flag, sn, password)

        self.driver.get(self.emsURL)
        login_ems(self.driver, self.emsUsr, self.emsPwd)

        filter_inventory_ont_by_sn(self.driver, sn)
        wait_inventory_ont_id(self.driver, sn, lambda ont_id: ont_id == "Unregistered")

        delete_ont_service_if_exists(self.driver, sn)
        create_ont_service_by_select_sn(self.driver, sn, self.dutIp, password, self.service_description)
        wait_ont_service_success(self.driver, sn)

        filter_inventory_ont_by_sn(self.driver, sn)
        wait_inventory_ont_id(self.driver, sn, lambda ont_id: ont_id != "Unregistered")
        wait_inventory_description(self.driver, sn, self.service_description)
