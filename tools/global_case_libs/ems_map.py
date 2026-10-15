import time
from datetime import datetime, timedelta

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from libs.ems_performance import chartjs_datasets
from libs.ems_tables import navigate_to


def map_tree_node_order_groups(driver):
    """Expand the Map tree and return each sibling group's node names in UI order."""
    navigate_to(driver, "Map")
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "navMenuTree")))
    navside = driver.find_element(By.ID, "navside")
    if "hidden" in (navside.get_attribute("class") or ""):
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, "navside_icon"))
        ).click()
        WebDriverWait(driver, 30).until(
            lambda current: "hidden" not in (
                current.find_element(By.ID, "navside").get_attribute("class") or ""
            )
        )

    # Expanding a submap can add another level of plus icons. Re-query after
    # every click so stale elements from the previous tree state are not used.
    for _ in range(500):
        collapsed = [
            icon
            for icon in driver.find_elements(
                By.CSS_SELECTOR,
                "#navMenuTree li.node-navMenuTree > .expand-icon.oi-plus",
            )
            if icon.is_displayed()
            and driver.execute_script(
                r"""
const li = arguments[0].parentElement;
if (!li) return false;
const clone = li.cloneNode(true);
clone.querySelectorAll('ul').forEach((child) => child.remove());
const name = (clone.innerText || clone.textContent || '').trim();
const deviceIcon = li.querySelector(
  ':scope > .node-icon[class*="icon-dev"], :scope > span[class*="icon-dev"]'
);
return !deviceIcon && !/\(\d{1,3}(?:\.\d{1,3}){3}\)/.test(name);
""",
                icon,
            )
        ]
        if not collapsed:
            break
        icon = collapsed[0]
        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center', inline:'nearest'});", icon
        )
        ActionChains(driver).move_to_element(icon).pause(0.05).click(icon).perform()
        time.sleep(0.15)
    else:
        raise AssertionError("Map tree expansion exceeded 500 nodes")

    groups = driver.execute_script(
        r"""
const root = document.getElementById('navMenuTree');
if (!root) return [];

function ownName(li) {
  const clone = li.cloneNode(true);
  clone.querySelectorAll('ul').forEach((child) => child.remove());
  return (clone.innerText || clone.textContent || '')
    .replace(/[\r\n\t]+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function parentPath(ul) {
  const owner = ul.parentElement && ul.parentElement.closest('li.node-navMenuTree');
  return owner ? ownName(owner) : 'ROOT';
}

function isDevice(li) {
  const deviceIcon = li.querySelector(
    ':scope > .node-icon[class*="icon-dev"], :scope > span[class*="icon-dev"]'
  );
  return Boolean(deviceIcon) || /\(\d{1,3}(?:\.\d{1,3}){3}\)/.test(ownName(li));
}

const result = [];
for (const ul of root.querySelectorAll('ul')) {
  const owner = ul.parentElement && ul.parentElement.closest('li.node-navMenuTree');
  // A UL owned by a device contains cards/ports. EMS1-3906 checks only
  // Submap and Device nodes, so device descendants are deliberately excluded.
  if (owner && isDevice(owner)) continue;
  const children = Array.from(ul.children).filter(
    (child) => child.matches('li.node-navMenuTree') && child.offsetParent !== null
  ).filter((child) => !isDevice(child));
  let names = children.map(ownName).filter(Boolean);
  if (parentPath(ul) === 'ROOT') {
    // EMS is the fixed tree root, not a sortable Submap sibling.
    names = names.filter((name) => name !== 'EMS');
  }
  if (names.length > 1) result.push({parent: parentPath(ul), names});
}
return result;
"""
    )
    return groups


def map_tree_node_order_key(value):
    """EMS order: special characters, digits, lowercase, uppercase, then Chinese."""
    text = str(value).strip()
    first = text[0] if text else ""
    codepoint = ord(first) if first else -1
    if first.isascii() and not first.isalnum():
        category = 0
    elif first.isascii() and first.isdigit():
        category = 1
    elif first.isascii() and first.isalpha():
        category = 2
    elif 0x3400 <= codepoint <= 0x9FFF:
        category = 3
    else:
        category = 4

    # EMS displays alphabetic names in case-insensitive dictionary order.
    # If two names are otherwise identical, lowercase precedes uppercase.
    case_tiebreaker = tuple(
        0 if character.islower() else 1 if character.isupper() else 0
        for character in text
    )
    return category, text.casefold(), case_tiebreaker, text


def open_map_device_status(driver, node_name, node_ip):
    navigate_to(driver, "Map")
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "navMenuTree")))
    navside = driver.find_element(By.ID, "navside")
    if "hidden" in (navside.get_attribute("class") or ""):
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "navside_icon"))).click()
        WebDriverWait(driver, 30).until(
            lambda d: "hidden" not in (d.find_element(By.ID, "navside").get_attribute("class") or "")
        )
    _expand_map_tree_until_device_visible(driver, node_name, node_ip)
    device = _device_node(driver, node_name, node_ip)
    driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'nearest'});", device)
    time.sleep(0.5)
    ActionChains(driver).move_to_element(device).pause(0.2).click(device).perform()
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "status_page")))
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "map_char_powermeter")))
    active_status_tabs = driver.find_elements(By.XPATH, "//a[contains(@class,'active') and normalize-space()='Status']")
    assert active_status_tabs, "Map device page should open on Status tab."


def power_meter_chart_data(driver):
    result = driver.execute_script(
        r"""
const canvas = document.getElementById('map_char_powermeter');
if (!canvas) {
  return {ok: false, error: 'map_char_powermeter canvas not found'};
}
let chart = null;
if (window.Chart && typeof window.Chart.getChart === 'function') {
  chart = window.Chart.getChart(canvas);
}
if (!chart && canvas.__chartist__) {
  chart = canvas.__chartist__;
}
if (!chart && window.Chart && window.Chart.instances) {
  const instances = window.Chart.instances;
  const values = Array.isArray(instances) ? instances : Object.values(instances);
  chart = values.find((item) => item && item.canvas === canvas);
}
if (!chart) {
  return {ok: false, error: 'Chart.js instance not found'};
}
const labels = (chart.data && chart.data.labels) || [];
const datasets = (chart.data && chart.data.datasets) || [];
const points = [];
for (const dataset of datasets) {
  const label = dataset.label || '';
  const data = dataset.data || [];
  for (let index = 0; index < data.length; index++) {
    const rawPoint = data[index];
    const rawValue = rawPoint && typeof rawPoint === 'object' ? rawPoint.y : rawPoint;
    const value = Number(rawValue);
    const timestamp = rawPoint && typeof rawPoint === 'object' && rawPoint.x !== undefined
      ? rawPoint.x
      : labels[index];
    if (Number.isFinite(value)) {
      points.push({label, timestamp: String(timestamp), value});
    }
  }
}
return {ok: true, labels: labels.map((item) => String(item)), datasetCount: datasets.length, points};
"""
    )
    if not result.get("ok"):
        raise AssertionError(f"Cannot read Power Meter Chart.js data: {result}")
    points = result.get("points", [])
    assert points, f"Power Meter chart should expose numeric data. result={result}"
    return points


def assert_power_meter_points_valid(points, now=None):
    now = now or datetime.now()
    assert len(points) <= 96, f"Power Meter point count should be <= 96. count={len(points)}"
    parsed = []
    for point in points:
        timestamp = _parse_chart_timestamp(point.get("timestamp", ""), now)
        value = float(point["value"])
        assert value > 0, f"Power Meter value should be > 0. point={point}"
        parsed.append({**point, "parsed_timestamp": timestamp})
    latest = max(parsed, key=lambda item: item["parsed_timestamp"])
    assert latest["parsed_timestamp"] <= now + timedelta(minutes=5), (
        f"Latest Power Meter timestamp should not be in the future. latest={latest}, now={now}"
    )
    print(f"EMS1-7071: latest Power Meter data: {latest}", flush=True)
    return latest


def ont_dashboard_ddmi_chart_data(driver):
    canvases = driver.execute_script(
        r"""
const selected = new Set();
for (const canvas of document.querySelectorAll('canvas')) {
  let current = canvas;
  for (let depth = 0; current && depth < 6; depth++, current = current.parentElement) {
    const identity = `${current.id || ''} ${current.className || ''}`.toLowerCase();
    if (identity.includes('ddmi')) {
      selected.add(canvas);
      break;
    }
  }
}

if (!selected.size) {
  const headings = Array.from(document.querySelectorAll('h1,h2,h3,h4,h5,h6,legend,label,span,div'))
    .filter((element) => /^ddmi(?:\s|$)/i.test((element.textContent || '').trim()));
  for (const heading of headings) {
    let container = heading.parentElement;
    for (let depth = 0; container && depth < 5; depth++, container = container.parentElement) {
      const canvases = container.querySelectorAll('canvas');
      if (canvases.length) {
        canvases.forEach((canvas) => selected.add(canvas));
        break;
      }
    }
  }
}
return Array.from(selected);
"""
    )
    charts = chartjs_datasets(driver, canvases)
    assert charts, (
        "ONT Dashboard DDMI Chart.js data not found. "
        f"selected_canvas_count={len(canvases)}"
    )
    return charts


def assert_ont_dashboard_ddmi_charts_valid(charts, max_points=96):
    validated_datasets = 0
    for chart in charts:
        for dataset in chart.get("datasets", []):
            points = dataset.get("points", [])
            assert 1 <= len(points) <= max_points, (
                f"DDMI data point count should be between 1 and {max_points}. "
                f"count={len(points)}, chart={chart.get('canvasId')}, dataset={dataset.get('label')}"
            )
            valued_points = [point for point in points if point.get("value") is not None]
            assert valued_points, (
                f"DDMI dataset should contain at least one numeric value. "
                f"chart={chart.get('canvasId')}, dataset={dataset.get('label')}, points={points}"
            )
            validated_datasets += 1
    assert validated_datasets, f"DDMI charts should contain at least one dataset. charts={charts}"
    return validated_datasets


def _expand_map_tree_until_device_visible(driver, node_name, node_ip):
    for _ in range(6):
        if _device_nodes(driver, node_name, node_ip):
            return
        icons = [
            icon for icon in driver.find_elements(By.CSS_SELECTOR, "#navMenuTree .expand-icon.oi-plus")
            if icon.is_displayed()
        ]
        if not icons:
            break
        for icon in icons[:20]:
            try:
                driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'nearest'});", icon)
                time.sleep(0.1)
                ActionChains(driver).move_to_element(icon).pause(0.1).click(icon).perform()
                time.sleep(0.2)
            except Exception:
                continue
    if not _device_nodes(driver, node_name, node_ip):
        filters = driver.find_elements(
            By.XPATH,
            "//*[@id='navMenuTree']/preceding::*[@placeholder='Filter string here ...'][1]",
        )
        if not filters:
            filters = driver.find_elements(By.XPATH, "//*[@placeholder='Filter string here ...']")
        if filters and node_ip:
            field = filters[0]
            field.clear()
            field.send_keys(node_ip)
            buttons = driver.find_elements(
                By.XPATH,
                "//*[@placeholder='Filter string here ...']/following::*[normalize-space()='Filter'][1]",
            )
            if buttons:
                buttons[0].click()
                time.sleep(2)
                for _ in range(4):
                    if _device_nodes(driver, node_name, node_ip):
                        break
                    icons = [
                        icon for icon in driver.find_elements(
                            By.CSS_SELECTOR, "#navMenuTree .expand-icon.oi-plus"
                        )
                        if icon.is_displayed()
                    ]
                    if not icons:
                        break
                    for icon in icons[:20]:
                        try:
                            driver.execute_script(
                                "arguments[0].scrollIntoView({block:'center', inline:'nearest'});",
                                icon,
                            )
                            ActionChains(driver).move_to_element(icon).pause(0.1).click(icon).perform()
                            time.sleep(0.3)
                        except Exception:
                            continue
    if not _device_nodes(driver, node_name, node_ip):
        raise AssertionError(f"Cannot find DUT in Map tree. node_name={node_name}, node_ip={node_ip}")


def _device_node(driver, node_name, node_ip):
    nodes = _device_nodes(driver, node_name, node_ip)
    if not nodes:
        raise AssertionError(f"Cannot find DUT in Map tree. node_name={node_name}, node_ip={node_ip}")
    return nodes[0]


def _device_nodes(driver, node_name, node_ip):
    needles = [node_name, node_ip]
    nodes = []
    for needle in [item for item in needles if item]:
        xpath = (
            "//*[@id='navMenuTree']//li[contains(@class,'node-navMenuTree') "
            f"and contains(normalize-space(.), {xpath_literal(needle)})]"
        )
        for element in driver.find_elements(By.XPATH, xpath):
            try:
                if element.is_displayed() and element not in nodes:
                    nodes.append(element)
            except Exception:
                continue
    return nodes


def _parse_chart_timestamp(value, now):
    text = str(value).strip()
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y/%m/%d %H:%M",
        "%H:%M:%S",
        "%H:%M",
    ]
    for fmt in formats:
        try:
            parsed = datetime.strptime(text, fmt)
            if fmt.startswith("%H"):
                return now.replace(hour=parsed.hour, minute=parsed.minute, second=getattr(parsed, "second", 0), microsecond=0)
            return parsed
        except ValueError:
            continue
    try:
        numeric = float(text)
    except ValueError as exc:
        raise AssertionError(f"Cannot parse Power Meter timestamp: {text}") from exc
    if numeric > 10_000_000_000:
        return datetime.fromtimestamp(numeric / 1000)
    return datetime.fromtimestamp(numeric)


def xpath_literal(text):
    if "'" not in text:
        return f"'{text}'"
    if '"' not in text:
        return f'"{text}"'
    parts = text.split("'")
    return "concat(" + ", \"'\", ".join(f"'{part}'" for part in parts) + ")"
