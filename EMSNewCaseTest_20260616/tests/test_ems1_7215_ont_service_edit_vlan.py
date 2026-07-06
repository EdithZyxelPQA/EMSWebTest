import pytest

from libs.browser import create_browser
from libs.device_cli import unregister_ont_by_flag
from libs.ems_profiles import (
    delete_profile_if_exists,
    recreate_ont_qos_bandwidth_profile,
    recreate_ont_service_profile,
    recreate_ont_template_vlan_profile,
)
from libs.ems_tables import (
    create_ont_service_with_qos_vlan_translation,
    delete_ont_service_by_template_if_exists,
    delete_ont_service_if_exists,
    filter_inventory_ont_by_sn,
    wait_inventory_ont_id,
    wait_ont_service_success,
)
from libs.ems_ui import login_ems
from libs.ont_service_vlan import assert_qos_vlan_translation, show_xont_config


@pytest.mark.ems
@pytest.mark.selenium
@pytest.mark.node
class TestEMS17215OntServiceEditVlan:
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

    def test_EMS1_7215_ontServiceEditVlan(self):
        if "NeoX" not in self.dutType:
            pytest.skip("EMS1-7215 only supports NeoX devices.")
        if self.serviceOntFlag != "xont":
            pytest.skip("EMS1-7215 only supports xont.")

        sn = self.serviceOntSN
        password = self.serviceOntPW
        slot_id = self.serviceOntSlotID
        port_id = self.serviceOntPortID
        ont_id = self.serviceOntID
        assert sn, "Missing ZYXEL_DUT.<node>.ONT.<exe_provision_ont>.sn_16"
        assert password, "Missing ZYXEL_DUT.<node>.ONT.<exe_provision_ont>.pw"

        print("EMS1-7215: unregister ONT by SSH", flush=True)
        unregister_ont_by_flag(self.dutIp, self.dutAdminName, self.dutAdminPwd, self.serviceOntFlag, sn, password)

        print(f"EMS1-7215: open EMS {self.emsURL}", flush=True)
        self.driver.get(self.emsURL)
        login_ems(self.driver, self.emsUsr, self.emsPwd)

        print("EMS1-7215: delete existing ONT service by SN", flush=True)
        delete_ont_service_if_exists(self.driver, sn)
        print("EMS1-7215: delete existing ONT service by template", flush=True)
        delete_ont_service_by_template_if_exists(self.driver, "$py_OntTempVlan")
        print("EMS1-7215: delete ONT template profile", flush=True)
        delete_profile_if_exists(self.driver, "ONT Template", "$py_OntTempVlan")

        for vlan in range(101, 133):
            print(f"EMS1-7215: recreate ONT Service Profile $py_Service{vlan}_XLAN1", flush=True)
            recreate_ont_service_profile(self.driver, f"$py_Service{vlan}_XLAN1", vlan, "LAN 1")

        print("EMS1-7215: recreate ONT QoS Bandwidth Profile $py_Bandwidth_1G_US", flush=True)
        recreate_ont_qos_bandwidth_profile(self.driver, "$py_Bandwidth_1G_US")
        print("EMS1-7215: recreate ONT QoS Bandwidth Profile $py_Bandwidth_1G_DS", flush=True)
        recreate_ont_qos_bandwidth_profile(self.driver, "$py_Bandwidth_1G_DS")
        print("EMS1-7215: recreate ONT Template Profile $py_OntTempVlan", flush=True)
        recreate_ont_template_vlan_profile(self.driver, "$py_OntTempVlan")

        print("EMS1-7215: confirm no ONT service by SN", flush=True)
        delete_ont_service_if_exists(self.driver, sn)

        print("EMS1-7215: wait Inventory/ONT Unregistered", flush=True)
        filter_inventory_ont_by_sn(self.driver, sn)
        wait_inventory_ont_id(self.driver, sn, lambda found_ont_id: found_ont_id == "Unregistered", timeout=300)

        print("EMS1-7215: create ONT service with template and QoS VLAN translation", flush=True)
        create_ont_service_with_qos_vlan_translation(
            self.driver,
            sn,
            self.dutIp,
            password,
            qos_count=32,
            template_name="$py_OntTempVlan",
        )
        print("EMS1-7215: wait ONT service Success", flush=True)
        wait_ont_service_success(self.driver, sn, timeout=600)

        print("EMS1-7215: wait Inventory/ONT registered", flush=True)
        filter_inventory_ont_by_sn(self.driver, sn)
        inventory_row = wait_inventory_ont_id(
            self.driver,
            sn,
            lambda found_ont_id: found_ont_id != "Unregistered",
            timeout=300,
        )
        actual_ont_id = inventory_row.get("ONT") or ont_id

        print("EMS1-7215: verify xONT config by SSH", flush=True)
        output = show_xont_config(
            self.dutIp,
            self.dutAdminName,
            self.dutAdminPwd,
            slot_id,
            port_id,
            actual_ont_id,
        )
        assert_qos_vlan_translation(output, service_count=32)
