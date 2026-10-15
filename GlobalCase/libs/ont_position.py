"""Resolve the real ONT ID of the configured ONTs from the DUT CLI.

ZYXEL_DUT.<node>.ONT.<ONTx>.ont_id is a fixed value, but the device assigns
the lowest free ONT ID whenever a case re-provisions an ONT through EMS, so
the ONT can move (e.g. 8-16-2 -> 8-16-1).  Every later case that uses the
configured ID then fails.  ``refresh_ont_positions`` looks the ONTs up by SN
(``show interface xpon <slot>-<port> ontstatus``) and updates the config
object in place before each case.
"""

import re

from libs.device_cli import run_telnet_commands

_ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]|\[J")
_AID_LINE = re.compile(r"^\s*(\d+)-(\d+)-(\d+)\s*\|")
_SN_LINE = re.compile(r"^\s*\|\s*([0-9A-Za-z]{12,16})\b")


def sn16_to_cli(sn16):
    """5A5958458CACE174 -> ZYXE8CACE174 (CLI 'normal' SN style)."""
    try:
        return bytes.fromhex(sn16[:8]).decode("ascii") + sn16[8:]
    except (ValueError, UnicodeDecodeError):
        return sn16


def _parse_ontstatus(output):
    """Return {cli_sn: (slot, port, ont_id)} from 'show interface xpon x-y ontstatus'."""
    positions = {}
    pending = None
    for raw in _ANSI.sub("", output).splitlines():
        aid = _AID_LINE.match(raw)
        if aid:
            pending = aid.groups()
            continue
        sn = _SN_LINE.match(raw)
        if sn and pending:
            positions[sn.group(1).upper()] = pending
            pending = None
    return positions


def refresh_ont_positions(config):
    if "NeoX" not in str(getattr(config, "dutType", "")):
        return
    ports = sorted({(str(s), str(p)) for s, p in zip(config.ontSlotIDList, config.ontPortIDList)})
    commands = [f"show interface xpon {slot}-{port} ontstatus" for slot, port in ports]
    try:
        output = run_telnet_commands(config.dutIp, config.dutAdminName, config.dutAdminPwd, commands, timeout=30)
    except Exception as exc:
        print(f"ONT position lookup skipped: {exc!r}", flush=True)
        return
    positions = _parse_ontstatus(output)

    for index, sn16 in enumerate(config.ontSNList):
        found = positions.get(sn16_to_cli(sn16).upper()) or positions.get(sn16.upper())
        if not found:
            continue
        actual_id = found[2]
        if str(config.ontOntIDList[index]) != actual_id:
            print(
                f"ONT{index + 1} sn={sn16} is at {found[0]}-{found[1]}-{actual_id} "
                f"(config ont_id={config.ontOntIDList[index]}); use the actual ID",
                flush=True,
            )
            config.ontOntIDList[index] = actual_id
        if sn16 == getattr(config, "serviceOntSN", None) and config.ontInfo:
            config.ontInfo[2] = actual_id
            config.serviceOntID = actual_id
        if "ONT" + str(index + 1) == getattr(config, "exeUpgradeONT", None):
            config.upgradeOntOntID = actual_id
