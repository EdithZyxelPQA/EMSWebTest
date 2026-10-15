"""EMS1-7245 helpers: open EMS by hostname (browser-side mapping, no server change) and check the Map device page.

The hostname is mapped to the EMS IP with Chrome/Edge `--host-resolver-rules`, so no hosts file or certificate
change is needed. Certificate errors are ignored (the EMS default certificate is expired, see BUG-4), so these
helpers only look at whether pages and data load.
"""
import json
import time
from urllib.parse import urlparse

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from libs.ems_map import _device_node, _expand_map_tree_until_device_visible
from libs.ems_tables import navigate_to

DATA_GATHERING = "Data gathering"
# EMS DB APIs the Map device page calls to show device data (seen with IP access).
DEVICE_DATA_APIS = (
    "getDeviceState", "getHardwareState", "getPowerConsumption", "getAlarmStatus",
    "getActiveAlarmTypeCount", "getAllOntInventoryInfo", "getNetwork",
)


def create_hostname_browser(browser_name, download_path, hostname, ems_ip, extra_rules=""):
    """Chrome/Edge where `hostname` resolves to `ems_ip`, certificate errors ignored, network + console logging on.

    `extra_rules` adds more host-resolver rules, e.g. "MAP maps.googleapis.com ~NOTFOUND" to make a host unreachable.
    """
    use_edge = browser_name.lower() == "edge"
    options = webdriver.EdgeOptions() if use_edge else webdriver.ChromeOptions()
    options.add_argument("ignore-certificate-errors")
    rules = f"MAP {hostname} {ems_ip}" + (f", {extra_rules}" if extra_rules else "")
    options.add_argument(f"--host-resolver-rules={rules}")
    options.add_experimental_option(
        "prefs",
        {"download.default_directory": download_path, "download.prompt_for_download": False, "download.directory_upgrade": True},
    )
    options.set_capability("ms:loggingPrefs" if use_edge else "goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"})
    options.add_experimental_option("perfLoggingPrefs", {"enableNetwork": True, "enablePage": False})
    return webdriver.Edge(options=options) if use_edge else webdriver.Chrome(options=options)


GOOGLE_MAPS_UNREACHABLE = "MAP maps.googleapis.com ~NOTFOUND, MAP maps.gstatic.com ~NOTFOUND"
INVALID_MAPS_KEY = "AIzaSyINVALID-KEY-FOR-EMS-TEST-0000000000"


def use_invalid_maps_key(driver):
    """Make this browser load Google Maps with an invalid API key (client side only, EMS settings untouched).

    Must be called before the EMS page is opened: it rewrites the key= value of any Google Maps script URL.
    """
    script = (
        "(() => {"
        " const d = Object.getOwnPropertyDescriptor(HTMLScriptElement.prototype, 'src');"
        " Object.defineProperty(HTMLScriptElement.prototype, 'src', {"
        "  set(v) { if (typeof v === 'string' && v.includes('maps.googleapis.com'))"
        f"   v = v.replace(/key=[^&]+/, 'key={INVALID_MAPS_KEY}'); d.set.call(this, v); }},"
        "  get() { return d.get.call(this); }, configurable: true });"
        "})();"
    )
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})


def drain_requests(driver):
    """Request URLs seen since the last call (performance log)."""
    urls = []
    try:
        entries = driver.get_log("performance")
    except WebDriverException:
        return urls
    for entry in entries:
        message = json.loads(entry["message"])["message"]
        if message.get("method") == "Network.requestWillBeSent":
            urls.append(message["params"]["request"]["url"])
    return urls


def console_errors(driver):
    """SEVERE console messages since the last call."""
    try:
        return [e["message"] for e in driver.get_log("browser") if e.get("level") == "SEVERE"]
    except WebDriverException:
        return []


def _status_text(driver):
    pages = [e for e in driver.find_elements(By.ID, "status_page") if e.is_displayed()]
    return pages[0].text if pages else ""


def open_map_device(driver, node_name, node_ip, timeout=60):
    """Open Map, select the device and wait for its data. Never raises; returns a result dict.

    loaded       : True when the Power Meter chart is shown and no "Data gathering..." remains on the device page
    gathering    : number of "Data gathering..." texts still shown after `timeout`
    db_apis      : EMS DB API names requested while the page loaded
    console      : console errors while the page loaded (e.g. Google Maps RefererNotAllowedMapError)
    """
    drain_requests(driver)
    console_errors(driver)
    result = {"loaded": False, "gathering": -1, "db_apis": [], "console": [], "error": ""}
    try:
        navigate_to(driver, "Map")
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "navMenuTree")))
        navside = driver.find_element(By.ID, "navside")
        if "hidden" in (navside.get_attribute("class") or ""):
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "navside_icon"))).click()
        _expand_map_tree_until_device_visible(driver, node_name, node_ip)
        device = _device_node(driver, node_name, node_ip)
        driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'nearest'});", device)
        time.sleep(0.5)
        ActionChains(driver).move_to_element(device).pause(0.2).click(device).perform()
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "status_page")))

        def data_shown(d):
            power = [e for e in d.find_elements(By.ID, "map_char_powermeter") if e.is_displayed()]
            return bool(power) and DATA_GATHERING not in _status_text(d)

        try:
            WebDriverWait(driver, timeout, poll_frequency=3).until(data_shown)
            result["loaded"] = True
        except TimeoutException:
            pass
        result["gathering"] = _status_text(driver).count(DATA_GATHERING)
    except Exception as error:
        result["error"] = f"{type(error).__name__}: {(str(error).strip().splitlines() or [''])[0]}"
    urls = drain_requests(driver)
    result["db_apis"] = sorted({urlparse(u).path.rstrip("/").split("/")[-1] for u in urls if "/netatlasems/DB/" in u})
    result["console"] = console_errors(driver)
    return result


# EMS DB APIs the Map > EMS (root node, geographic map) page calls to list the devices on the map.
MAP_ROOT_APIS = ("getAllDevInfo", "getAllInfo")
_MAP_ROOT_PROBE = r"""
const vis = e => !!e && e.offsetParent !== null;
const sel = document.querySelector('#navMenuTree li.node-navMenuTree.node-selected');
const gm = document.querySelector('#geomap .gm-style');
return {
  root_selected: !!sel && sel.getAttribute('data-nodeid') === '0',
  geomap_shown: vis(document.getElementById('topology_geomap_page')) && vis(document.getElementById('geomap')),
  google_map: vis(gm),
  markers: gm ? gm.querySelectorAll('img[src*="marker"], [role=button], gmp-advanced-marker').length : 0,
  map_error: [...document.querySelectorAll('#geomap .gm-err-message')].map(e => e.innerText.trim()).slice(0, 1),
};
"""


def open_map_root(driver, wait_seconds=20):
    """Open Map (EMS root node is selected by default) and read the geographic map state. Never raises.

    root_selected : the EMS root node (data-nodeid 0) is the selected tree node
    geomap_shown  : the geographic map page (#topology_geomap_page / #geomap) is shown
    google_map    : Google Maps drew the map; markers = device markers on it
    map_error     : Google Maps error text in the map area (expected when the key is rejected)
    db_apis       : EMS DB API names requested while the page loaded
    """
    drain_requests(driver)
    console_errors(driver)
    result = {"root_selected": False, "geomap_shown": False, "google_map": False, "markers": 0,
              "map_error": [], "db_apis": [], "console": [], "error": ""}
    try:
        navigate_to(driver, "Map")
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "navMenuTree")))
        time.sleep(wait_seconds)
        result.update(driver.execute_script(_MAP_ROOT_PROBE))
    except Exception as error:
        result["error"] = f"{type(error).__name__}: {(str(error).strip().splitlines() or [''])[0]}"
    urls = drain_requests(driver)
    result["db_apis"] = sorted({urlparse(u).path.rstrip("/").split("/")[-1] for u in urls if "/netatlasems/DB/" in u})
    result["console"] = console_errors(driver)
    return result
