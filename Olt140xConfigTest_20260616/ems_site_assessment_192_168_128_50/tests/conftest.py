import json
import os
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _as_bool(value):
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


@pytest.fixture(scope="session")
def config():
    with (PROJECT_ROOT / "config.json").open("r", encoding="utf-8") as file_obj:
        data = json.load(file_obj)

    data["base_url"] = os.getenv("EMS_BASE_URL", data["base_url"]).rstrip("/") + "/"
    data["username"] = os.getenv("EMS_USERNAME", data["username"])
    data["password"] = os.getenv("EMS_PASSWORD", data["password"])
    data["browser"] = os.getenv("EMS_BROWSER", data["browser"]).lower()
    data["headless"] = _as_bool(os.getenv("EMS_HEADLESS", data["headless"]))
    data["artifacts_path"] = PROJECT_ROOT / data["artifacts_dir"]
    data["artifacts_path"].mkdir(parents=True, exist_ok=True)
    return data


@pytest.fixture(scope="session")
def http_session(config):
    requests = pytest.importorskip("requests")
    urllib3 = pytest.importorskip("urllib3")

    if not config["verify_tls"]:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    session = requests.Session()
    session.verify = config["verify_tls"]
    return session


@pytest.fixture
def driver(config):
    selenium = pytest.importorskip("selenium")
    from selenium import webdriver

    if config["browser"] != "chrome":
        pytest.skip(f"Unsupported browser configured for this suite: {config['browser']}")

    options = webdriver.ChromeOptions()
    options.accept_insecure_certs = True
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1440,1000")
    if config["headless"]:
        options.add_argument("--headless=new")

    browser = webdriver.Chrome(options=options)
    browser.set_page_load_timeout(config["timeout_seconds"])
    browser.implicitly_wait(2)
    yield browser
    browser.quit()


@pytest.fixture
def screenshot(config):
    def capture(driver, name):
        path = config["artifacts_path"] / f"{name}.png"
        driver.save_screenshot(str(path))
        return path

    return capture

