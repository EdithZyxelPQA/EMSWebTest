"""Run only the three shared VoIP setup helpers twice to check reuse."""
import datetime
import os
from pathlib import Path
import re
import time

from module.customdriver import CustomDriver
import module.ems_test_module as ems
import module.selenium_module as mod
from module.variable_module import ems_url, username, ems_password


def main():
    os.chdir(Path(__file__).resolve().parent)
    report_dir = Path('Report')
    report_dir.mkdir(exist_ok=True)
    report = report_dir / f"Web_EMS_VoIP_Retest_{datetime.datetime.now():%Y%m%d_%H%M%S}.txt"
    report.write_text('EMS shared VoIP setup/reuse retest\n', encoding='utf-8')
    file_name = str(report.resolve())
    print(f'Report: {file_name}', flush=True)
    ems.parameter_add('file_name', file_name)
    ems.get_file_name(file_name)
    driver = None
    failures = 0
    try:
        driver = CustomDriver(time_sleep=0)
        driver.set_window_size(1920, 1080)
        driver.get(ems_url)
        time.sleep(5)
        mod.Login_EMS(driver, username, ems_password)
        time.sleep(5)
        for round_number in (1, 2):
            for name, action in (
                ('SIP', ems.Create_ONT_VoIP_Sip_Profile),
                ('Common', ems.Create_ONT_VoIP_Common_Profile),
                ('Dial Plan', ems.Create_ONT_VoIP_Dial_Plan_Profile),
            ):
                print(f'Round {round_number}: {name}', flush=True)
                offset = report.stat().st_size
                try:
                    action(driver, username, ems_password, file_name)
                    segment = report.read_bytes()[offset:].decode('utf-8', errors='replace')
                    passed = bool(re.search(r'(Create|Reuse) Pass', segment)) and not re.search(r'\bFail\b', segment)
                except Exception as exc:
                    passed = False
                    with report.open('a', encoding='utf-8') as log:
                        print(f'{name} exception: {exc}', file=log)
                failures += not passed
                result = f'Round {round_number} {name}: Result {"Pass" if passed else "Fail"}'
                print(result, flush=True)
                with report.open('a', encoding='utf-8') as log:
                    print(result, file=log)
    finally:
        if driver is not None:
            driver.quit()
    print(f'Completed: {failures} failed checks', flush=True)
    return int(failures > 0)


if __name__ == '__main__':
    raise SystemExit(main())
