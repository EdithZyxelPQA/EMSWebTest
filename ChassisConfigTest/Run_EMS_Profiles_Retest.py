"""Rerun only the profile groups that failed in Run_EMS_Profiles_1.py.

Usage: python Run_EMS_Profiles_Retest.py [--ems <IP>] [ems_test_module function names ...]
With no function names, runs the default RETEST list below.
--ems overrides the EMS url/ip in ENV/ENV_WEB.json for this run (see module/variable_module.py).
"""
import datetime
import os
from pathlib import Path
import sys
import time

from module.customdriver import CustomDriver
import module.ems_profile_module as e_pro
import module.ems_test_module as ems
import module.selenium_module as mod
from module.variable_module import ems_url, username, ems_password, ems_tag


RETEST = (
    ems.Create_zzz_profile_for_Sort_test,  # Sort cases need the zzz profiles
    ems.ONT_Multicast_Profile,             # EMS1-5624, EMS1-5626
    ems.ONT_VoIP_SIP_Profile,              # EMS1-5666, EMS1-5670
    ems.ONT_VoIP_Common_Profile,           # EMS1-3629, EMS1-5676
    ems.Weight_Profile,                    # EMS1-5788
)


def Cleanup_Multicast_SIP(driver, ems_url, username, ems_password, file_name):
    """Delete the profiles ONT_Multicast_Profile / ONT_VoIP_SIP_Profile create, so they start clean."""
    driver.get(ems_url)
    time.sleep(5)
    mod.Login_EMS(driver, username, ems_password)
    time.sleep(5)
    print(f"             [Profile] (Cleanup Multicast / SIP profiles)", file=open(file_name, '+a'))
    for name, page in (
        ('!!!AutoTest_DoNotDelete_mul_SFU', 'ONT Multicast Profile'),
        ('!!!AutoTest_DoNotDelete_mul_HGU', 'ONT Multicast Profile'),
        ('zzzzzzzzzzzzzzzzzzzzzzzzzzzzzz', 'ONT Multicast Profile'),
        ('!!!AutoTest_DoNotDelete_xxxxxxx', 'IGMP Group Privilege Profile'),  # after Multicast, which references it
        ('sip_profile_SFU', 'ONT VoIP SIP Profile'),
        ('sip_profile_HGU', 'ONT VoIP SIP Profile'),
        ('zzzzzzzzzzzzzzz', 'ONT VoIP SIP Profile'),
    ):
        ems.Delete_Profile_Test(driver, name, page, file_name)
    print(f"             [Profile] (Cleanup finished)", file=open(file_name, '+a'))


def Cleanup_Template_GE_Sec_Alarm_Rate_Shaping(driver, ems_url, username, ems_password, file_name):
    """Delete the profiles the ONT Template / GE Template / Security / Alarm / Rate Limit / Shaping tests create
    (names from EMS_delete_profiles). Templates first, since they reference the other profiles."""
    driver.get(ems_url)
    time.sleep(5)
    mod.Login_EMS(driver, username, ems_password)
    time.sleep(5)
    zzz = 'zzzzzzzzzzzzzzzzzzzzzzzzzzzzzz'
    igmp = '!!!AutoTest_DoNotDelete_xxxxxxx'
    print(f"             [Profile] (Cleanup Template/GE/Security/Alarm/Rate Limit/Shaping profiles)", file=open(file_name, '+a'))
    for name, page in (
        ('!!!Auto_DoNotDelete_templat_SFU', 'ONT Template'),
        (zzz, 'ONT Template'),
        ('ＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺ', 'ONT Template'),
        ('!!!GE_template_vlan_trunk_xxxxx', 'GE Template'),
        ('!!!GE_template_vlan_tls_xxxxx', 'GE Template'),
        ('!!!GE_template_vlan_translation', 'GE Template'),
        (zzz, 'GE Template'),
        ('!!!Auto_DoNotDelete_security_xx', 'ONT Security Profile'),
        ('!!!Auto_DoNotDelete_security__m', 'ONT Security Profile'),
        (zzz, 'ONT Security Profile'),
        ('!!!Auto_create_alarm_profile_xx', 'ONT Alarm Profile'),
        ('!!!Auto_create_alarm_profile__m', 'ONT Alarm Profile'),
        (zzz, 'ONT Alarm Profile'),
        (igmp, 'Rate Limit Profile'),
        (zzz, 'Rate Limit Profile'),
        (igmp, 'Shaping Profile'),
        (zzz, 'Shaping Profile'),
    ):
        _delete_with_retry(driver, name, page, file_name)
    print(f"             [Profile] (Cleanup finished)", file=open(file_name, '+a'))


@ems.retry(max_retries=3)
def Sort_Sec_Rate_Shaping(driver, ems_url, username, ems_password, file_name):
    """Recreate the zzz profiles (same way as Create_zzz_profile_for_Sort_test) on Security / Rate Limit / Shaping,
    then run only their SORT cases (EMS1-5650 / 5766 / 5777)."""
    zzz = 'zzzzzzzzzzzzzzzzzzzzzzzzzzzzzz'
    driver.get(ems_url)
    time.sleep(5)
    mod.Login_EMS(driver, username, ems_password)
    time.sleep(5)
    ems.Create_ONT_Security_Profile(driver, ems_url, username, ems_password, file_name, zzz)
    for page in ('Rate Limit Profile', 'Shaping Profile'):
        e_pro.Profile_Path(driver, page)
        time.sleep(3)
        e_pro.New_Profile(driver)
        e_pro.Profile_Name(driver, zzz)
        e_pro.Save(driver)
        msg = ems.alert_accept_text_no_block(driver)
        print(f"             [Setup] create {page} {zzz}: msg:{msg}", file=open(file_name, '+a'))
    ems.Profile_Sort_Test(driver, '[EMS1-5650]', 'ONT Security Profile', file_name, profile_name=zzz)
    ems.Profile_Sort_Test(driver, '[EMS1-5766]', 'Rate Limit Profile', file_name, profile_name=zzz)
    ems.Profile_Sort_Test(driver, '[EMS1-5777]', 'Shaping Profile', file_name, profile_name=zzz)


_ZZZ = 'zzzzzzzzzzzzzzzzzzzzzzzzzzzzzz'
SORT_CASES = (  # (case id, page, zzz name) - the Sort cases whose zzz is made by my_create_zzz_profile
    ('EMS1-5777', 'Shaping Profile', _ZZZ),
    ('EMS1-5660', 'ONT ONT Profile', _ZZZ),
    ('EMS1-3636', 'ONT Template', 'ＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺＺ'),
    ('EMS1-5788', 'Weight Profile', _ZZZ),
    ('EMS1-5744', 'GE Template', _ZZZ),
)


def Sort_With_zzz(driver, ems_url, username, ems_password, file_name, cases=SORT_CASES):
    """For each (case, page, zzz): create zzz if missing (same steps as my_create_zzz_profile), then run that Sort case.
    Each page is retried on its own, so one slow page does not skip the others (unlike Create_zzz_profile_for_Sort_test)."""
    for case, page, zzz in cases:
        for attempt in range(3):
            try:
                driver.get(ems_url)
                time.sleep(5)
                mod.Login_EMS(driver, username, ems_password)
                time.sleep(5)
                e_pro.Profile_Path(driver, page)
                time.sleep(3)
                if not e_pro.Profile_Name_Search_only(driver, zzz):
                    e_pro.New_Profile(driver)
                    e_pro.Profile_Name(driver, zzz)
                    e_pro.Save(driver)
                    print(f"             [Setup] create {page} zzz: msg:{ems.alert_accept_text_no_block(driver)}", file=open(file_name, '+a'))
                ems.Profile_Sort_Test(driver, f'[{case}]', page, file_name, profile_name=zzz)
                break
            except Exception as exc:
                print(f"             [Setup] {case} {page}: {type(exc).__name__} (attempt {attempt + 1})", file=open(file_name, '+a'))
                time.sleep(5)


def _delete_with_retry(driver, name, page, file_name, attempts=2):
    # slow EMS pages (loading overlay) can make one lookup miss; retry once after a pause
    for attempt in range(attempts):
        try:
            return ems.Delete_Profile_Test(driver, name, page, file_name)
        except Exception as exc:
            print(f"             [Cleanup] {page} {name}: {type(exc).__name__} (attempt {attempt + 1})", file=open(file_name, '+a'))
            time.sleep(5)


def _function_names(args):
    # drop "--ems <IP>" / "--ems=<IP>" (handled by variable_module); the rest are function names
    names, skip = [], False
    for arg in args:
        if skip:
            skip = False
        elif arg == "--ems":
            skip = True
        elif not arg.startswith("--ems="):
            names.append(arg)
    return names


def main():
    retest = [globals().get(name) or getattr(ems, name) for name in _function_names(sys.argv[1:])] or RETEST
    os.chdir(Path(__file__).resolve().parent)
    Path('Report').mkdir(exist_ok=True)
    # EMS_FIND_WAIT: seconds to sleep before each find_element (slow pages, e.g. 1700+ SIP profiles)
    driver = CustomDriver(time_sleep=float(os.environ.get('EMS_FIND_WAIT', '0')))
    try:
        driver.set_window_size(1920, 1080)
        driver.get(ems_url)
        time.sleep(5)
        mod.Login_EMS(driver, username, ems_password)
        time.sleep(5)
        driver.find_element('id', 'helpMenu').click()
        driver.find_element('id', 'about_ems_button').click()
        time.sleep(3)
        emsversion = ""
        for _ in range(30):   # About dialog fills the version asynchronously
            emsversion = driver.find_element('id', 'emsversion').text.split("\n")[0].strip()
            if emsversion:
                break
            time.sleep(1)
        driver.find_element('xpath', '//*[@type="button" and @class="button button_green"]').click()

        file_name = f"Report/Web_EMS_Profiles_Retest_{emsversion}_{ems_tag}_{datetime.datetime.now():%Y-%m-%d %H%M}.txt"
        ems.parameter_add("file_name", file_name)
        ems.get_file_name(file_name)
        with open(file_name, 'w', encoding='utf-8') as f:
            print("EMS Web Auto Report (Profile retest)", file=f)
            print(datetime.datetime.now(), file=f)
            print(f"EMS Web IP:{ems_url}  \nEMS Version:{emsversion} ", file=f)
            print("=" * 86, file=f)
        print(f'Report: {file_name}', flush=True)

        start = time.time()
        for action in retest:
            print(f'Running {action.__name__}', flush=True)
            action(driver, ems_url, username, ems_password, file_name)
        total = time.time() - start
        print(f'Profile Retest   Total time: {int(total/3600)} hr {int(total/60%60)} min {int(total%60)} sec',
              file=open(file_name, '+a'))
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
