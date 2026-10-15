import base64
import ftplib
import json
import re
import time
from io import BytesIO
from pathlib import Path

import paramiko
import telnetlib
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


MIB_FIELDS = {
    "dev_uuid": 1,
    "dev_path": 2,
    "perf_uuid": 5,
    "perf_path": 6,
}


POWER_IMAGE_PROFILES = {
    "neox-03": {
        "mode": "DC",
        "led_centres": [(0.661, 0.934), (0.976, 0.934)],
        "green_pixel_minimum": 40,
    },
    "neox-06": {
        "mode": "DC",
        "led_centres": [(0.661, 0.961), (0.966, 0.961)],
    },
    "ies5206": {
        "mode": "DC",
        "led_centres": [(0.360, 0.234), (0.968, 0.234)],
    },
    "ies4204": {
        "mode": "DC",
        "led_centres": [(0.723, 0.208), (0.868, 0.208)],
    },
}


def capture_restful_debug_files(config, report_dir, timeout=180):
    report_dir = Path(report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)
    uuid_dev = f"{config.dutIp}_dev"
    uuid_perf = f"{config.dutIp}_perf"
    debug_values = {
        "dev_uuid": uuid_dev,
        "dev_path": f"https://{config.emsIp}/RESTfulServer/Server/DevicePollerDebug/",
        "perf_uuid": uuid_perf,
        "perf_path": f"https://{config.emsIp}/RESTfulServer/Server/PerformanceDebug/",
    }

    session = _open_device_linux(config)
    originals = {}
    try:
        for name, suffix in MIB_FIELDS.items():
            originals[name] = _snmp_get(session, config, _mib_oid(config, suffix))
        try:
            for name, suffix in MIB_FIELDS.items():
                _snmp_set(session, config, _mib_oid(config, suffix), debug_values[name])
            paths = _download_ems_debug_files(
                config,
                [uuid_dev, uuid_perf],
                report_dir,
                timeout,
            )
        finally:
            restore_errors = []
            for name, suffix in MIB_FIELDS.items():
                try:
                    _snmp_set(session, config, _mib_oid(config, suffix), originals[name])
                except Exception as error:
                    restore_errors.append(f"{name}: {error}")
            if restore_errors:
                raise AssertionError(
                    "Failed to restore RESTful upload MIB values: "
                    + "; ".join(restore_errors)
                )
    finally:
        session.close()

    with paths[uuid_dev].open(encoding="utf-8", errors="ignore") as stream:
        dev_data = json.load(stream)
    with paths[uuid_perf].open(encoding="utf-8", errors="ignore") as stream:
        perf_data = json.load(stream)
    return dev_data, perf_data, paths, originals


def power_supply_image_states(
    driver,
    dut_type,
    power_entries,
    report_path,
    image_selector="#status_page img",
):
    profile = POWER_IMAGE_PROFILES.get((dut_type or "").strip().casefold())
    if profile is None:
        return None, f"No Power Supply image profile for device type {dut_type!r}"
    if len(power_entries) != len(profile["led_centres"]):
        raise AssertionError(
            f"{dut_type} profile has {len(profile['led_centres'])} Power Supply positions, "
            f"but hwinfo.power has {len(power_entries)} entries"
        )

    image = _device_image(driver, image_selector)
    report_path = Path(report_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(report_path)
    radius = max(7, int(min(image.size) * 0.015))
    states = []
    for index, (relative_x, relative_y) in enumerate(profile["led_centres"]):
        centre_x = round(relative_x * image.width)
        centre_y = round(relative_y * image.height)
        green_pixels = 0
        sampled_pixels = 0
        for y in range(max(0, centre_y - radius), min(image.height, centre_y + radius + 1)):
            for x in range(max(0, centre_x - radius), min(image.width, centre_x + radius + 1)):
                red, green, blue = image.getpixel((x, y))[:3]
                sampled_pixels += 1
                if green >= 90 and green >= red * 1.35 and green >= blue * 1.20:
                    green_pixels += 1
        states.append({
            "index": index,
            "mode": profile["mode"],
            "centre": (centre_x, centre_y),
            "green_pixels": green_pixels,
            "sampled_pixels": sampled_pixels,
            "is_up": green_pixels >= profile.get("green_pixel_minimum", 10),
        })
    return states, None


def _device_image(driver, image_selector):
    sources = WebDriverWait(driver, 60).until(
        lambda current_driver: current_driver.execute_script(
            "return Array.from(document.querySelectorAll(arguments[0]))"
            ".map(image => image.src || '')"
            ".filter(source => source.startsWith('data:image/'));",
            image_selector,
        )
    )
    decoded = []
    for source in sources:
        try:
            image = Image.open(BytesIO(base64.b64decode(source.split(",", 1)[1]))).convert("RGB")
            decoded.append(image)
        except Exception:
            continue
    assert decoded, f"No readable equipment image found by selector {image_selector!r}"
    return max(decoded, key=lambda image: image.width * image.height)


def _mib_oid(config, suffix):
    if "neox" in (config.dutType or "").casefold():
        base = "1.3.6.1.4.1.890.1.5.19.1.16.21"
    else:
        base = "1.3.6.1.4.1.890.1.5.13.13.16.21"
    return f"{base}.{suffix}.0"


def _snmp_options(config):
    if getattr(config, "_power_snmp_force_v2", False):
        return f"-v 2c -c {_shell_quote(config.dutGet)}"
    version = re.sub(r".*V", "", config.dutSnmpVer, flags=re.DOTALL)
    if version == "3":
        levels = {
            "No authentication and no privacy": "noAuthNoPriv",
            "Authentication and no privacy": "authNoPriv",
            "Authentication and privacy": "authPriv",
        }
        level = levels[config.dutSnmp3Auth]
        return (
            f"-v 3 -u {config.dutAdminName} -l {level} "
            f"-a {config.dutSnmp3Hash} -A {_shell_quote(config.dutAdminPwd)} "
            f"-x {config.dutSnmp3Encrypt} -X {_shell_quote(config.dutAdminPwd)}"
        )
    return f"-v {version} -c {_shell_quote(config.dutGet)}"


def _open_device_linux(config):
    session = telnetlib.Telnet(config.dutIp, port=23, timeout=50)
    session.read_until(b" login:", timeout=50)
    session.write(config.dutAdminName.encode("ascii") + b"\n")
    session.read_until(b"Password:", timeout=50)
    session.write(config.dutAdminPwd.encode("ascii") + b"\n")
    session.read_until(b"#", timeout=50)
    session.write(b"linux supervisor\n")
    session.read_until(b"#", timeout=50)
    return session


def _linux_command(session, command):
    session.write(command.encode("ascii") + b"\n")
    output = session.read_until(b"#", timeout=60).decode("utf-8", errors="ignore")
    if re.search(r"(?:No Such|Timeout|Error|Invalid|not found)", output, re.I):
        raise AssertionError(f"Command failed: {command}; output={output}")
    return output


def _snmp_get(session, config, oid):
    command = f"snmpget -m '' -Oqv {_snmp_options(config)} {config.dutIp} {oid}"
    try:
        output = _linux_command(session, command)
    except AssertionError as configured_error:
        if getattr(config, "_power_snmp_force_v2", False):
            raise
        config._power_snmp_force_v2 = True
        fallback = f"snmpget -m '' -Oqv {_snmp_options(config)} {config.dutIp} {oid}"
        try:
            output = _linux_command(session, fallback)
        except AssertionError:
            config._power_snmp_force_v2 = False
            raise configured_error
    candidates = []
    for line in output.splitlines():
        value = line.strip()
        if not value or "snmpget" in value or value.endswith("#"):
            continue
        candidates.append(value)
    assert candidates, f"Cannot parse SNMP value for {oid}: {output}"
    value = candidates[-1]
    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    return value


def _snmp_set(session, config, oid, value):
    options = _snmp_options(config).replace(
        f"-c {_shell_quote(config.dutGet)}", f"-c {_shell_quote(config.dutSet)}"
    )
    command = (
        f"snmpset -m '' -Oqv {options} {config.dutIp} {oid} s {_shell_quote(value)}"
    )
    _linux_command(session, command)


def _download_ems_debug_files(config, names, report_dir, timeout):
    deadline = time.monotonic() + timeout
    last_error = None
    while time.monotonic() < deadline:
        try:
            _make_ems_files_readable(config, names)
            paths = {}
            ftp = ftplib.FTP()
            ftp.set_pasv(False)
            ftp.connect(config.emsIp, 21, timeout=30)
            ftp.login(config.emsSrvUsr, config.emsSrvPwd)
            ftp.cwd("/opt/ELEMENTVIEW_MASTER/bin/")
            for name in names:
                target = report_dir / f"EMS1-4903_{name}.json"
                with target.open("wb") as stream:
                    ftp.retrbinary(f"RETR {name}", stream.write)
                assert target.stat().st_size > 0, f"Downloaded file is empty: {name}"
                paths[name] = target
            ftp.quit()
            return paths
        except Exception as error:
            last_error = error
            time.sleep(10)
    raise AssertionError(
        f"Cannot download EMS RESTful debug files {names} within {timeout}s: {last_error}"
    )


def _make_ems_files_readable(config, names):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(config.emsIp, 22, config.emsSrvUsr, config.emsSrvPwd, timeout=30)
    shell = client.invoke_shell()
    commands = [
        "sudo su",
        config.emsSuPwd,
        "cd /opt/ELEMENTVIEW_MASTER/bin",
        "chmod 777 " + " ".join(names),
    ]
    output = ""
    try:
        for command in commands:
            shell.send(command + "\n")
            time.sleep(2)
            while shell.recv_ready():
                output += shell.recv(65535).decode("utf-8", errors="ignore")
    finally:
        client.close()
    if re.search(r"(?:No such file|Permission denied)", output, re.I):
        raise AssertionError(output)


def _shell_quote(value):
    return '"' + str(value).replace("\\", "\\\\").replace('"', '\\"') + '"'
