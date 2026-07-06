import json
import os
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace

import pytest


PROJECT_ROOT = Path(__file__).resolve().parent
SESSION_TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def pytest_addoption(parser):
    parser.addoption("--cmdopt", action="store", default="NODE1", help="DUT node key from environment_parameter.json")
    parser.addoption(
        "--env-file",
        action="store",
        default=str(PROJECT_ROOT / "environment_parameter.json"),
        help="Path to the EMS test environment JSON file",
    )


def _as_namespace(value):
    if isinstance(value, dict):
        return SimpleNamespace(**{key: _as_namespace(item) for key, item in value.items()})
    if isinstance(value, list):
        return [_as_namespace(item) for item in value]
    return value


def load_env_data(env_file):
    env_path = Path(env_file)
    if not env_path.is_absolute():
        env_path = PROJECT_ROOT / env_path

    with env_path.open(encoding="utf-8") as f:
        return json.load(f), env_path


def build_config_object(node_name, env_file):
    data, env_path = load_env_data(env_file)
    ems = data.get("EMS", {})
    auto_site = data.get("AUTO_SITE", {})
    element = data.get("ELEMENT", {})
    dut_table = data.get("ZYXEL_DUT", {})

    if node_name not in dut_table:
        available_nodes = ", ".join(dut_table.keys()) or "<none>"
        raise pytest.UsageError(
            f"Node '{node_name}' was not found in {env_path}. Available nodes: {available_nodes}"
        )

    dut_data = dut_table[node_name]
    ont_table = dut_data.get("ONT", {})
    exe_service_ont = ont_table.get("exe_provision_ont", "")
    service_ont_data = ont_table.get(exe_service_ont, {}) if exe_service_ont else {}
    upload_path = auto_site.get("upload_path", str(PROJECT_ROOT / "ForUpload"))
    download_path = auto_site.get("download_path", str(PROJECT_ROOT / "download"))
    report_path = auto_site.get("report_path", str(PROJECT_ROOT / "report"))

    config = {
        "projectRoot": str(PROJECT_ROOT),
        "envFile": str(env_path),
        "sessionTimestamp": SESSION_TIMESTAMP,
        "reportTitle": ems.get("report_title", "Web_EMS_NewCase"),
        "waitTime": int(element.get("wait_time", 3)),
        "uploadPath": os.path.abspath(upload_path),
        "downloadpath": os.path.abspath(download_path),
        "reportPath": os.path.abspath(report_path),
        "browser": auto_site.get("browser", "chrome"),
        "emsIp": ems.get("ip", ""),
        "emsURL": ems.get("url", ""),
        "emsVer": ems.get("version", ""),
        "emsUsr": ems.get("login_username", ""),
        "emsPwd": ems.get("login_password", ""),
        "node_name": node_name,
        "dutName": dut_data.get("name", node_name),
        "dutIp": dut_data.get("ip", ""),
        "dutNodeName": dut_data.get("name_display", f"{dut_data.get('name', node_name)}({dut_data.get('ip', '')})"),
        "dutDesc": dut_data.get("description", ""),
        "dutAdminName": dut_data.get("login_username", ""),
        "dutAdminPwd": dut_data.get("login_password", ""),
        "dutConsolePort": dut_data.get("console_port", ""),
        "dutConsoleBaudrate": int(dut_data.get("console_baudrate", 115200)),
        "dutConsoleName": dut_data.get("console_username", dut_data.get("login_username", "")),
        "dutConsolePwd": dut_data.get("console_password", dut_data.get("login_password", "")),
        "dutType": dut_data.get("type", ""),
        "dutSlotCount": dut_data.get("slot_total", ""),
        "dutCardInfo": dut_data.get("CARDINFO", {}),
        "dutGeInfo": dut_data.get("GE", {}),
        "exeServiceOnt": exe_service_ont,
        "serviceOntSN": service_ont_data.get("sn_16", ""),
        "serviceOntPW": service_ont_data.get("pw", ""),
        "serviceOntFlag": service_ont_data.get("flag", ""),
        "serviceOntType": service_ont_data.get("type", ""),
        "serviceOntProfile": service_ont_data.get("service_prf", ""),
        "serviceOntSlotID": service_ont_data.get("slot_id", ""),
        "serviceOntPortID": service_ont_data.get("port_id", ""),
        "serviceOntID": service_ont_data.get("ont_id", ""),
        "raw": _as_namespace(data),
        "dut": _as_namespace(dut_data),
    }
    return SimpleNamespace(**config)


@pytest.fixture(scope="session")
def test_config(request):
    node_name = request.config.getoption("--cmdopt")
    env_file = request.config.getoption("--env-file")
    return build_config_object(node_name, env_file)


@pytest.fixture(autouse=True, scope="class")
def inject_test_config(request, test_config):
    if request.cls is None:
        return

    for key, value in vars(test_config).items():
        setattr(request.cls, key, value)


@pytest.fixture(scope="session", autouse=True)
def create_runtime_dirs(test_config):
    Path(test_config.downloadpath).mkdir(parents=True, exist_ok=True)
    Path(test_config.reportPath).mkdir(parents=True, exist_ok=True)
