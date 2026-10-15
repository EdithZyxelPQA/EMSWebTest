import re

from libs.device_cli import run_ssh_commands


def show_xont_config(host, username, password, slot_id, port_id, ont_id):
    aid = f"{slot_id}-{port_id}-{ont_id}"
    return run_ssh_commands(
        host,
        username,
        password,
        [f"show interface remote xont {aid} config"],
        timeout=120,
    )


def assert_qos_vlan_translation(output, service_count=32):
    normalized_lines = [_normalize(line) for line in output.splitlines()]
    missing = []
    for index in range(1, service_count + 1):
        vlan = 200 + index
        svlan = 300 + index
        cvlan = 400 + index
        if not _has_service_vlan_line(normalized_lines, index, vlan, svlan, cvlan):
            missing.append(f"service{index}: vlan={vlan}, svlan={svlan}, cvlan={cvlan}")
    if missing:
        raise AssertionError(
            "Cannot verify xONT QoS VLAN translation in CLI output. Missing: "
            + "; ".join(missing)
            + "\nCLI output:\n"
            + output
        )


def _has_service_vlan_line(lines, service_index, vlan, svlan, cvlan):
    service_patterns = [f"service{service_index}", f"service {service_index}", str(service_index)]
    for line in lines:
        if not any(pattern in line for pattern in service_patterns):
            continue
        numbers = re.findall(r"\d+", line)
        if {str(vlan), str(svlan), str(cvlan)}.issubset(numbers):
            return True
    return False


def _normalize(text):
    return re.sub(r"\s+", " ", text.strip().lower())
