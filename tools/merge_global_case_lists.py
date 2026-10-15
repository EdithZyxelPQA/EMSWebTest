"""Merge the four legacy GlobalCase list files without altering their content."""

from __future__ import annotations

import sys
from pathlib import Path


def merge(source_paths: list[Path], output_path: Path) -> None:
    sections = []
    for path in source_paths:
        content = path.read_text(encoding="utf-8-sig").strip()
        if path.name == "Web_EMS_NewCase.list":
            configuration_cases = (
                "[EMS1-7212]ipNameServer",
                "[EMS1-4538]portSpeedSelection",
            )
            for configuration_case in configuration_cases:
                content = content.replace(f"\n{configuration_case}", "")
            configuration_section = (
                "======== Configuration on EMS Web ========\n"
                + "\n".join(configuration_cases)
                + "\n\n"
            )
            content = content.replace(
                "======== Performance on EMS Web ========",
                configuration_section + "======== Performance on EMS Web ========",
                1,
            )
        if path.name == "Web_EMS_Unicase.list":
            content = content.replace(
                "[EMS1-3496]alarmActive",
                "[EMS1-3496]alarmActive\n"
                "[EMS1-4907]loginSuccessAlarm\n"
                "[EMS1-6238]clearAlarmGeneratedAccessLog\n"
                "[EMS1-5178]alarmFilterTimeReset",
                1,
            )
            content = content.replace(
                "[EMS1-3495]mapTreeNode",
                "[EMS1-3495]mapTreeNode\n[EMS1-3906]treeNodeOrder",
                1,
            )
            content = content.replace(
                "[EMS1-4365]mapDeviceImage",
                "[EMS1-4361]availabilityDevicePanelLink\n"
                "[EMS1-4365]mapDeviceImage",
                1,
            )
            content = content.replace(
                "[EMS1-4369]alarmStatus",
                "[EMS1-4369]alarmStatus\n"
                "[EMS1-6147]alarmStatusExport\n"
                "[EMS1-6156]deviceDashboardAlarmStatus\n"
                "[EMS1-6144]deviceDashboardAlarmAck\n"
                "[EMS1-6145]deviceDashboardAlarmClear\n"
                "[EMS1-4362_4398]deviceHwMonitor",
                1,
            )
            content = content.replace(
                "[EMS1-4507]ontInfo",
                "[EMS1-7049]transceiverFilter\n"
                "[EMS1-7051]transceiverExport\n"
                "[EMS1-7072]transceiverInfo\n"
                "[EMS1-4507]ontInfo",
                1,
            )
            content = content.replace(
                "[EMS1-5931]deleteResultLog",
                "[EMS1-5931]deleteResultLog\n"
                "[EMS1-6317]fwManagementAccessLog\n"
                "[EMS1-6318]deleteScheduleLogAccessLog",
                1,
            )
            content = content.replace(
                "[EMS1-6068]dashboardAlarmClear",
                "[EMS1-6068]dashboardAlarmClear\n[EMS1-6201]dashboardAlarmAckClearLog",
                1,
            )
            content = content.replace(
                "[EMS1-6078]ontDashboardAlarmStatus",
                "[EMS1-6078]ontDashboardAlarmStatus\n[EMS1-6079]ontDashboardDdmi",
                1,
            )
            content = content.replace(
                "[EMS1-5037]mapTreeFold",
                "[EMS1-5037]mapTreeFold\n[EMS1-5105]navsideIconIts\n[EMS1-6123]cardTreeFold",
                1,
            )
            content = content.replace(
                "[EMS1-4439]remoteControlReset",
                "[EMS1-4439]remoteControlReset\n[EMS1-5180]hostnameRemoteControlIts",
                1,
            )
            content = content.replace(
                "[EMS1-4368]ontStatusPage",
                "[EMS1-4368]ontStatusPage\n"
                "[EMS1-6107]ontDashboardOntStatusFromMapDevice\n"
                "[EMS1-6172]ontDashboardRunScriptFromMapDevice\n"
                "[EMS1-6108]ontDashboardAlarmStatusFromMapDevice\n"
                "[EMS1-6171]ontDashboardRebootFromMapDevice\n"
                "[EMS1-6109]ontDashboardDdmiFromMapDevice",
                1,
            )
        sections.append(content)
    output_path.write_text("\r\n\r\n".join(sections) + "\r\n", encoding="utf-8", newline="")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        raise SystemExit("usage: merge_global_case_lists.py <source.list>... <output.list>")
    merge([Path(value) for value in sys.argv[1:-1]], Path(sys.argv[-1]))
