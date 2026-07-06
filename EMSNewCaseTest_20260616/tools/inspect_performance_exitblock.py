import argparse
import json
import sys
import time
from pathlib import Path

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from libs.browser import create_browser
from libs.ems_performance import create_interface_current_chart, interface_port_options, open_create_demand
from libs.ems_tables import navigate_to
from libs.ems_ui import login_ems


def load_config(node_name):
    with (ROOT / "environment_parameter.json").open(encoding="utf-8") as f:
        data = json.load(f)
    ems = data["EMS"]
    dut = data["ZYXEL_DUT"][node_name]
    return {
        "ems_url": ems["url"],
        "ems_user": ems["login_username"],
        "ems_password": ems["login_password"],
        "browser": data["AUTO_SITE"].get("browser", "chrome"),
        "download_path": str((ROOT / data["AUTO_SITE"].get("download_path", "download")).resolve()),
        "node_name": dut.get("name_display", node_name),
        "cards": dut.get("CARDINFO", {}),
    }


def exitblock_snapshot(driver, label):
    icons = driver.find_elements(By.XPATH, "//*[@class='icon exitBlock']")
    rows = []
    for index, icon in enumerate(icons, start=1):
        rect = icon.rect
        rows.append(
            {
                "index": index,
                "displayed": icon.is_displayed(),
                "onclick": icon.get_attribute("onclick"),
                "rect": {
                    "x": round(rect.get("x", 0), 1),
                    "y": round(rect.get("y", 0), 1),
                    "width": round(rect.get("width", 0), 1),
                    "height": round(rect.get("height", 0), 1),
                },
            }
        )
    print(f"{label}: count={len(icons)}")
    for row in rows:
        print(f"  {row}")
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cmdopt", default="192.168.168.85")
    parser.add_argument("--steps", type=int, default=10)
    parser.add_argument("--create-charts", type=int, default=0)
    parser.add_argument("--performance-type", default="Interface(Accumulation)")
    args = parser.parse_args()

    cfg = load_config(args.cmdopt)
    driver = create_browser(cfg["browser"], cfg["download_path"])
    driver.implicitly_wait(3)
    driver.maximize_window()

    try:
        driver.get(cfg["ems_url"])
        login_ems(driver, cfg["ems_user"], cfg["ems_password"])
        navigate_to(driver, "Performance", "Current")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "content_Demand")))

        if args.create_charts:
            card = first_interface_card(cfg["cards"])
            print(
                f"create_charts: type={args.performance_type}, slot={card['slot_id']}, "
                f"card={card['type']}, requested={args.create_charts}"
            )
            open_create_demand(driver)
            ports = interface_port_options(
                driver,
                args.performance_type,
                cfg["node_name"],
                card["slot_id"],
                card["type"],
            )
            close_create_dialog(driver)
            print(f"available_ports={ports}")
            for index, port_id in enumerate(ports[: args.create_charts], start=1):
                print(f"create_chart {index}/{args.create_charts}: port={port_id}")
                open_create_demand(driver)
                create_interface_current_chart(
                    driver,
                    args.performance_type,
                    cfg["node_name"],
                    card["slot_id"],
                    card["type"],
                    port_id,
                )
                time.sleep(0.5)

        body = driver.find_element(By.TAG_NAME, "body")
        ActionChains(driver).move_to_element(body).click().send_keys(Keys.HOME).perform()
        time.sleep(1)
        previous_onclicks = None

        for step in range(args.steps + 1):
            rows = exitblock_snapshot(driver, f"step={step}")
            onclicks = [row["onclick"] for row in rows]
            if previous_onclicks is not None:
                print(f"  changed_from_previous={onclicks != previous_onclicks}")
            previous_onclicks = onclicks
            ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(1)
    finally:
        driver.quit()


def first_interface_card(cards):
    for card in cards.values():
        card_type = card.get("type", "")
        port_type = card.get("port_type", "")
        if any(token in f"{card_type} {port_type}" for token in ["NXC", "NXA", "NXP", "MSC", "GLC", "OLC"]):
            return {"slot_id": str(card["slot_id"]), "type": card_type}
    raise RuntimeError("No interface card found in environment_parameter.json.")


def close_create_dialog(driver):
    for selector in ["#create_demand_background a.exit", ".alarm_tool_background_create a.exit", "a.exit"]:
        for candidate in driver.find_elements(By.CSS_SELECTOR, selector):
            if candidate.is_displayed():
                ActionChains(driver).move_to_element(candidate).click(candidate).perform()
                WebDriverWait(driver, 10).until(
                    EC.invisibility_of_element_located((By.ID, "create_demand_background"))
                )
                return


if __name__ == "__main__":
    main()
