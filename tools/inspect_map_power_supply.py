import json
import sys
import base64
from io import BytesIO
from pathlib import Path

from PIL import Image
from selenium.webdriver.common.by import By


ROOT = Path(__file__).resolve().parents[1] / "GlobalCase"
sys.path.insert(0, str(ROOT))

from libs.browser import close_browser, create_browser
from libs.ems_map import open_map_device_status
from libs.ems_ui import login_ems


def safe(value):
    return (value or "").encode("ascii", "backslashreplace").decode("ascii")


def main():
    node = sys.argv[1] if len(sys.argv) > 1 else "192.168.168.85"
    with (ROOT / "environment_parameter.json").open(encoding="utf-8") as stream:
        data = json.load(stream)
    ems = data["EMS"]
    dut = data["ZYXEL_DUT"][node]
    driver = create_browser(data["AUTO_SITE"].get("browser", "chrome"), str(ROOT / "download"))
    driver.implicitly_wait(3)
    driver.maximize_window()
    try:
        driver.get(ems["url"])
        login_ems(driver, ems["login_username"], ems["login_password"])
        try:
            open_map_device_status(driver, dut["name_display"], dut["ip"])
        except AssertionError:
            tree = driver.find_elements(By.ID, "navMenuTree")
            print(f"map-tree-text={safe(tree[0].text) if tree else '<missing>'!r}", flush=True)
            filters = driver.find_elements(By.XPATH, "//*[@placeholder='Filter string here ...']")
            print(
                f"map-filter-values={[safe(item.get_attribute('value')) for item in filters]!r}",
                flush=True,
            )
            raise
        selectors = [
            "[id*='power' i]", "[class*='power' i]", "[id*='psu' i]",
            "[class*='psu' i]", "#status_page img", "#status_page svg *",
            "#status_page canvas", "#status_page [style*='background-image']",
            "#status_page map", "#status_page area",
        ]
        seen = set()
        for selector in selectors:
            for element in driver.find_elements(By.CSS_SELECTOR, selector):
                key = (element.tag_name, element.get_attribute("id"), element.get_attribute("class"))
                if key in seen:
                    continue
                seen.add(key)
                print(
                    f"selector={selector!r} tag={element.tag_name!r} "
                    f"id={safe(element.get_attribute('id'))!r} "
                    f"class={safe(element.get_attribute('class'))!r} "
                    f"src={(safe(element.get_attribute('src'))[:120] + '...')!r} "
                    f"style={safe(element.get_attribute('style'))!r} "
                    f"title={safe(element.get_attribute('title'))!r} "
                    f"usemap={safe(element.get_attribute('usemap'))!r} "
                    f"coords={safe(element.get_attribute('coords'))!r} "
                    f"shape={safe(element.get_attribute('shape'))!r} "
                    f"text={safe(element.text)[:200]!r}",
                    flush=True,
                )
        sources = driver.execute_script(
            "return Array.from(document.querySelectorAll('#status_page img'))"
            ".map(image => image.src || '')"
            ".filter(source => source.startsWith('data:image/'));"
        )
        images = []
        for source in sources:
            try:
                images.append(
                    Image.open(BytesIO(base64.b64decode(source.split(",", 1)[1]))).convert("RGB")
                )
            except Exception:
                continue
        image = max(images, key=lambda candidate: candidate.width * candidate.height)
        width, height = image.size
        green = set()
        for y in range(height):
            for x in range(width):
                red, channel_green, blue = image.getpixel((x, y))
                if channel_green >= 90 and channel_green >= red * 1.35 and channel_green >= blue * 1.20:
                    green.add((x, y))
        components = []
        while green:
            seed = green.pop()
            stack = [seed]
            points = [seed]
            while stack:
                x, y = stack.pop()
                for neighbour in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                    if neighbour in green:
                        green.remove(neighbour)
                        stack.append(neighbour)
                        points.append(neighbour)
            if len(points) >= 4:
                xs = [point[0] for point in points]
                ys = [point[1] for point in points]
                components.append((len(points), min(xs), min(ys), max(xs), max(ys)))
        print(f"image-size={width}x{height}", flush=True)
        for component in sorted(components, reverse=True)[:100]:
            print(f"green-component={component}", flush=True)
    finally:
        close_browser(driver)


if __name__ == "__main__":
    main()
