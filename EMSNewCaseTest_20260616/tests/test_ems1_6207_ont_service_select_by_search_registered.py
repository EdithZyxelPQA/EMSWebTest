import pytest

from libs.browser import create_browser
from libs.device_cli import register_ont_by_flag, unregister_ont_by_flag
from libs.ems_tables import (
    available_ont_ids_from_inventory,
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
class TestEMS16207OntServiceSelectBySearchRegistered:
    driver = None
    service_description = "testSearchRegistered"

    @pytest.fixture(autouse=True)
    def setup_browser(self):
        self.driver = create_browser(self.browser, self.downloadpath)
        self.driver.implicitly_wait(self.waitTime)
        self.driver.maximize_window()
        yield
        if self.driver:
            self.driver.quit()
            self.driver = None

    def test_EMS1_6207_ontServiceSelectBySearchRegistered(self):
        sn = self.serviceOntSN
        password = self.serviceOntPW
        flag = self.serviceOntFlag
        assert sn, "Missing ZYXEL_DUT.<node>.ONT.<exe_provision_ont>.sn_16"
        assert password, "Missing ZYXEL_DUT.<node>.ONT.<exe_provision_ont>.pw"
        assert flag, "Missing ZYXEL_DUT.<node>.ONT.<exe_provision_ont>.flag"

        self.driver.get(self.emsURL)
        login_ems(self.driver, self.emsUsr, self.emsPwd)
        delete_ont_service_if_exists(self.driver, sn)

        unregister_ont_by_flag(self.dutIp, self.dutAdminName, self.dutAdminPwd, flag, sn, password)
        candidate_ont_ids = available_ont_ids_from_inventory(
            self.driver,
            self.serviceOntSlotID,
            self.serviceOntPortID,
            self.serviceOntID,
        )
        registered_ont = register_ont_by_flag(
            self.dutIp,
            self.dutAdminName,
            self.dutAdminPwd,
            flag,
            self.serviceOntSlotID,
            self.serviceOntPortID,
            self.serviceOntID,
            sn,
            password,
            candidate_ont_ids=candidate_ont_ids,
        )

        filter_inventory_ont_by_sn(self.driver, sn)
        wait_inventory_ont_id(self.driver, sn, lambda ont_id: ont_id == registered_ont.ont_id)

        create_ont_service_by_select_sn(self.driver, sn, self.dutIp, password, self.service_description)
        wait_ont_service_success(self.driver, sn)

        filter_inventory_ont_by_sn(self.driver, sn)
        wait_inventory_ont_id(self.driver, sn, lambda ont_id: ont_id != "Unregistered")
        wait_inventory_description(self.driver, sn, self.service_description)
