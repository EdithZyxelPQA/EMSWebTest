"""Run one selected case against ENV_WEB_168_84.json without a full-device reset."""
import json
import os
from pathlib import Path
from datetime import datetime
import traceback
import time
import argparse
import inspect
import re

CASE_NAMES = ['Basic_IP', 'Basic_Port', 'IP_Static', 'IP_DHCP', 'Advanced_VLAN',
    'Advanced_Static', 'Advanced_Filtering', 'Advanced_Broadcast', 'Advanced_Link',
    'Advanced_Port', 'Advanced_Classifier', 'Advanced_Policy', 'Advanced_Queqe',
    'Advanced_VLANStacking', 'Advanced_Multicast', 'Advanced_IP', 'Advanced_Loop',
    'Advanced_PPPoE', 'GPON_OLT', 'Configure_Save']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', choices=CASE_NAMES, default='Basic_IP')
    case = parser.parse_args().case
    root = Path(__file__).resolve().parent
    os.chdir(root)
    os.environ['SE_SKIP_DRIVER_IN_PATH'] = 'true'
    from customdriver import CustomDriver
    import selenium_module as mod
    import ems_test_module_OLT1408 as cases

    cfg = json.loads((root / 'ENV/ENV_WEB_168_84.json').read_text(encoding='utf-8-sig'))
    output = root / 'Output'
    output.mkdir(exist_ok=True)
    log = output / (case + '_rerun_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.txt')
    log.write_text(f"Case: {case}\nEMS: {cfg['EMS']['url']}\nDevice: {cfg['ZYXEL_DUT']['NODE1']['url']}\n", encoding='utf-8')
    print(f'Log: {log}', flush=True)
    driver = None
    status = 1
    try:
        driver = CustomDriver()
        driver.maximize_window()
        from urllib.parse import urlsplit, quote
        node = cfg['ZYXEL_DUT']['NODE1']
        host = urlsplit(node['url']).netloc
        driver.get(f"http://{quote(node['login_username'], safe='')}:{quote(node['login_password'], safe='')}@{host}")
        time.sleep(5)
        mod.Switch_Default(driver)
        mod.Switch_Specific_Frame(driver, 3)
        mod.Switch_Default(driver)
        driver.get(cfg['EMS']['url'])
        mod.Login_EMS(driver, cfg['EMS']['login_username'], cfg['EMS']['login_password'])
        time.sleep(5)
        cases.get_file_name(str(log))
        ports = node['CARDINFO']['OLT140x']
        pon = ports['port_id']
        offset = 8 if ports['type'].startswith('OLT1408') else 4
        eth = int(ports['eth_port_id']) - offset
        values = dict(driver=driver, url=node['url'], ems_url=cfg['EMS']['url'],
            file_name=str(log), username=node['login_username'], password=node['login_password'],
            url_ip=host, Pon_Name=f'PON {pon}', Eth_Name=f'ETH {eth}',
            Pon_Name_L=f'pon-{pon}', Eth_Name_L=f'eth-{eth}',
            OLT_Port=pon, OLT_Eth_Port=ports['eth_port_id'])
        func = getattr(cases, case).__wrapped__
        func(**{name: values[name] for name in inspect.signature(func).parameters})
        content = log.read_text(encoding='utf-8', errors='replace')
        status = 1 if re.search(r'\b(fail|failed|error|exception)\b', content, re.I) or not re.search(r'\bpass\b', content, re.I) else 0
        with log.open('a', encoding='utf-8') as stream:
            stream.write('\nRunner: ' + ('FAIL' if status else 'COMPLETED') + '\n')
    except Exception:
        with log.open('a', encoding='utf-8') as stream:
            stream.write('\nRunner: ERROR\n' + traceback.format_exc())
        print(f'{case} stopped with an error; see log.', flush=True)
    finally:
        if driver:
            try:
                driver.save_screenshot(str(log.with_suffix('.png')))
            except Exception:
                pass
            driver.quit()
    print(f'Result: {status}; Log: {log}', flush=True)
    return status


if __name__ == '__main__':
    raise SystemExit(main())
