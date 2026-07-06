import re
import time
from io import BytesIO

from PIL import Image
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from libs.ems_tables import navigate_to

def open_current_page(driver):
    current_content = driver.find_elements(By.ID, "content_Demand")
    if current_content and current_content[0].is_displayed():
        return
    print("Performance helper: open Performance/Current", flush=True)
    navigate_to(driver, "Performance", "Current")
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "content_Demand")))


def close_all_current_charts(driver, timeout=300):
    open_current_page(driver)
    end_time = time.time() + timeout
    while time.time() < end_time:
        _confirm_if_present(driver, timeout=1)
        chart_count = _scroll_current_page_to_bottom_and_count_charts(driver)
        if chart_count == 0:
            print("Performance helper: no charts to close", flush=True)
            return

        print(f"Performance helper: found {chart_count} chart(s), close by pm_ xpath loop", flush=True)
        _close_charts_by_pm_xpath_loop(driver, chart_count)

        remaining = _current_chart_container_count(driver)
        if remaining == 0:
            print("Performance helper: all charts are closed", flush=True)
            return
        print(f"Performance helper: {remaining} chart(s) remain after clicking {chart_count} X icon(s)", flush=True)
    raise TimeoutError("Performance/Current charts were not closed before timeout.")


def open_create_demand(driver):
    print("Performance helper: open Create Demand dialog", flush=True)
    last_error = None
    for attempt in range(1, 4):
        try:
            open_current_page(driver)
            _confirm_if_present(driver, timeout=0)
            create_icon = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#i_action_create_demand > a"))
            )
            print(f"Performance helper: click Create Demand icon attempt={attempt}/3", flush=True)
            if not _dispatch_frontend_mouse_click(driver, create_icon):
                ActionChains(driver).move_to_element(create_icon).pause(0.1).click(create_icon).perform()
            WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "create_demand_background")))
            print("Performance helper: Create Demand dialog is open", flush=True)
            return
        except TimeoutException as exc:
            last_error = exc
            print(f"Performance helper: Create Demand dialog did not open attempt={attempt}/3", flush=True)
            _confirm_if_present(driver, timeout=0)
            try:
                close_create_demand(driver)
            except Exception:
                pass
            try:
                driver.refresh()
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "content_Demand")))
            except Exception:
                pass
    raise last_error


def close_create_demand(driver):
    print("Performance helper: close Create Demand dialog", flush=True)
    if not _create_demand_visible(driver):
        print("Performance helper: Create Demand dialog is already closed", flush=True)
        return
    for selector in ["#create_demand_background a.exit", ".alarm_tool_background_create a.exit", "a.exit"]:
        candidates = driver.find_elements(By.CSS_SELECTOR, selector)
        for index, candidate in enumerate(candidates, start=1):
            try:
                if not candidate.is_displayed():
                    continue
                print(f"Performance helper: click Create Demand close selector={selector} index={index}", flush=True)
                try:
                    driver.execute_script(
                        "arguments[0].scrollIntoView({block:'center', inline:'nearest'});",
                        candidate,
                    )
                    time.sleep(0.1)
                except Exception:
                    pass
                candidate.click()
                WebDriverWait(driver, 3).until(
                    EC.invisibility_of_element_located((By.ID, "create_demand_background"))
                )
                return
            except Exception as exc:
                print(
                    f"Performance helper: close selector={selector} index={index} failed: {exc.__class__.__name__}",
                    flush=True,
                )
                try:
                    if _dispatch_frontend_mouse_click(driver, candidate):
                        WebDriverWait(driver, 3).until(
                            EC.invisibility_of_element_located((By.ID, "create_demand_background"))
                        )
                        return
                except Exception:
                    continue
    print("Performance helper: Create Demand dialog close button was not found or dialog already closed", flush=True)


def available_probe_count(driver, timeout=15, expected=None):
    end_time = time.time() + timeout
    last_text = ""
    last_count = None
    while time.time() < end_time:
        text = driver.find_element(By.ID, "create_demand_background").text
        last_text = text
        match = re.search(r"The currently available number of probes is\s*:\s*(\d+)", text)
        if match:
            last_count = int(match.group(1))
            if expected is not None and last_count == expected:
                return last_count
            if expected is None and last_count != 0:
                return last_count
        time.sleep(1)
    if last_count is not None:
        return last_count
    raise AssertionError(f"Cannot find available probe count in Create dialog: {last_text}")


def create_interface_current_chart(driver, performance_type, node_name, slot_id, card_type, port_id):
    print(
        f"Performance helper: create chart type={performance_type}, node={node_name}, "
        f"slot={slot_id}, card={card_type}, port={port_id}",
        flush=True,
    )
    Select(driver.find_element(By.ID, "create_performance_select")).select_by_visible_text(performance_type)
    _expand_node_path(driver, node_name)
    card_label = _card_label(driver, slot_id, card_type)
    ActionChains(driver).scroll_to_element(card_label).pause(0.1).move_to_element(card_label).click(card_label).perform()
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "performance_select_port")))
    Select(driver.find_element(By.ID, "performance_select_port")).select_by_visible_text(str(port_id))
    driver.find_element(By.XPATH, "//input[@value='Create' and contains(@class,'button_green')]").click()
    _wait_create_demand_closed(driver, timeout=60)


def create_interface_current_charts_in_open_dialog(driver, performance_type, node_name, slot_id, card_type, port_ids):
    print(
        f"Performance helper: batch create charts type={performance_type}, node={node_name}, "
        f"slot={slot_id}, card={card_type}, ports={port_ids}",
        flush=True,
    )
    _prepare_interface_current_chart_dialog(driver, performance_type, node_name, slot_id, card_type)

    for index, port_id in enumerate(port_ids, start=1):
        if not _create_demand_visible(driver):
            open_create_demand(driver)
            _prepare_interface_current_chart_dialog(driver, performance_type, node_name, slot_id, card_type)
        print(
            f"Performance helper: batch create {performance_type} "
            f"{index}/{len(port_ids)} slot={slot_id}, card={card_type}, port={port_id}",
            flush=True,
        )
        _select_performance_port_like_user(driver, port_id)
        create_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@value='Create' and contains(@class,'button_green')]"))
        )
        ActionChains(driver).move_to_element(create_button).pause(0.2).click(create_button).perform()
        message = _ack_create_message(driver, timeout=1.2)
        if isinstance(message, str) and "No probes are available anymore" in message:
            raise AssertionError(
                "Create Performance chart failed: "
                f"type={performance_type}, index={index}/{len(port_ids)}, "
                f"slot={slot_id}, card={card_type}, port={port_id}, message={message}"
            )


def _prepare_interface_current_chart_dialog(driver, performance_type, node_name, slot_id, card_type):
    last_error = None
    node_ip = _node_ip_from_name(node_name)
    for attempt in range(1, 4):
        try:
            print(
                f"Performance helper: prepare dialog attempt={attempt}/3 "
                f"type={performance_type}, slot={slot_id}, card={card_type}",
                flush=True,
            )
            Select(driver.find_element(By.ID, "create_performance_select")).select_by_visible_text(performance_type)
            print("Performance helper: performance type selected", flush=True)
            time.sleep(1)
            _expand_node_by_ip(driver, node_ip)
            print("Performance helper: node path expanded", flush=True)
            card_label = _card_label_under_node_ip(driver, node_ip, slot_id, card_type, timeout=12)
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", card_label)
            time.sleep(0.5)
            try:
                card_label.click()
            except Exception:
                ActionChains(driver).move_to_element(card_label).pause(0.1).click(card_label).perform()
            time.sleep(1)
            print("Performance helper: card selected", flush=True)
            WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "performance_select_port")))
            print("Performance helper: port selector is visible", flush=True)
            return
        except TimeoutException as exc:
            last_error = exc
            print(
                f"Performance helper: card label not ready, retry dialog prepare "
                f"attempt={attempt}/3 slot={slot_id}, card={card_type}",
                flush=True,
            )
            close_create_demand(driver)
            open_create_demand(driver)
    raise last_error


def _create_demand_visible(driver):
    dialogs = driver.find_elements(By.ID, "create_demand_background")
    return bool(dialogs and dialogs[0].is_displayed())


def _select_performance_port_like_user(driver, port_id):
    port_select = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.ID, "performance_select_port"))
    )
    ActionChains(driver).move_to_element(port_select).click(port_select).perform()
    Select(port_select).select_by_visible_text(str(port_id))
    WebDriverWait(driver, 10).until(
        lambda _: Select(driver.find_element(By.ID, "performance_select_port")).first_selected_option.text.strip() == str(port_id)
    )
    time.sleep(2)


def interface_port_options(driver, performance_type, node_name, slot_id, card_type):
    print(
        f"Performance helper: get port options type={performance_type}, node={node_name}, "
        f"slot={slot_id}, card={card_type}",
        flush=True,
    )
    _prepare_interface_current_chart_dialog(driver, performance_type, node_name, slot_id, card_type)
    ports = [
        option.text.strip()
        for option in driver.find_element(By.ID, "performance_select_port").find_elements(By.TAG_NAME, "option")
        if option.text.strip()
    ]
    print(f"Performance helper: found port options {ports}", flush=True)
    return ports


def refresh_current_page(driver):
    open_current_page(driver)
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#i_action_refresh > a"))).click()
    time.sleep(0.5)


def wait_for_chart(driver, expected_title, excluded_values=None, timeout=240):
    excluded_values = {str(value) for value in (excluded_values or [])}
    end_time = time.time() + timeout
    last_text = ""
    while time.time() < end_time:
        refresh_current_page(driver)
        values = [
            value
            for value in canvas_numeric_values(driver)
            if _numeric_token(value) not in excluded_values and value not in excluded_values
        ]
        last_text = f"values={values}"
        if values:
            return values
        time.sleep(10)
    raise AssertionError(f"Performance chart did not expose numeric canvas values. title={expected_title}, last_state={last_text}")


def wait_for_all_charts_with_values(driver, expected_count, excluded_values=None, timeout=300):
    excluded_values = {str(value) for value in (excluded_values or [])}
    end_time = time.time() + timeout
    last_values = []
    while time.time() < end_time:
        refresh_current_page(driver)
        frame_values = []
        for values in canvas_numeric_values_by_frame(driver):
            filtered_values = [
                value
                for value in values
                if _numeric_token(value) not in excluded_values and value not in excluded_values
            ]
            if filtered_values:
                frame_values.append(filtered_values)
        last_values = frame_values
        print(
            f"Performance helper: charts with canvas values {len(frame_values)}/{expected_count}",
            flush=True,
        )
        if len(frame_values) >= expected_count:
            return frame_values
        time.sleep(10)
    raise AssertionError(
        f"Not all Performance charts exposed canvas values. expected={expected_count}, actual={len(last_values)}, values={last_values}"
    )


def wait_for_all_charts_rendered(driver, expected_count, timeout=300):
    end_time = time.time() + timeout
    last_count = 0
    while time.time() < end_time:
        refresh_current_page(driver)
        rendered_count = rendered_canvas_count_by_frame(driver)
        last_count = rendered_count
        print(
            f"Performance helper: rendered canvas charts {rendered_count}/{expected_count}",
            flush=True,
        )
        if rendered_count >= expected_count:
            return rendered_count
        time.sleep(10)
    raise AssertionError(
        f"Not all Performance charts rendered canvas data. expected={expected_count}, actual={last_count}"
    )


def wait_for_all_charts_with_visual_data(driver, expected_count, timeout=300):
    end_time = time.time() + timeout
    last_state = []
    while time.time() < end_time:
        refresh_current_page(driver)
        states = chart_visual_data_states_across_page(driver, expected_count)
        passed = [
            state for state in states
            if state["has_line_or_point"] and state["has_numeric_value"]
        ]
        last_state = states
        print(
            f"Performance helper: charts with line/point and numeric values "
            f"{len(passed)}/{expected_count}; states={states}",
            flush=True,
        )
        if len(passed) >= expected_count:
            return states
        time.sleep(10)
    raise AssertionError(
        "Not all Performance charts exposed line/point data and numeric values. "
        f"expected={expected_count}, actual={len([s for s in last_state if s['has_line_or_point'] and s['has_numeric_value']])}, "
        f"states={last_state}"
    )


def current_chart_count(driver):
    open_current_page(driver)
    return _current_chart_container_count(driver)


def current_iframe_count(driver):
    open_current_page(driver)
    return len([frame for frame in driver.find_elements(By.TAG_NAME, "iframe") if frame.is_displayed()])


def _visible_chart_close_buttons(driver):
    return [button for button in _chart_close_buttons(driver) if _is_clickable_chart_close_icon(driver, button)]


def _chart_close_buttons(driver):
    return driver.find_elements(By.XPATH, "//*[@class='icon exitBlock']")


def _pm_chart_close_buttons(driver):
    return driver.find_elements(By.XPATH, "//*[starts-with(@id,'pm_')]/div[1]/div[1]/div[contains(@class,'exitBlock')]")


def _close_charts_by_pm_xpath_loop(driver, chart_count):
    close_xpath = "//*[starts-with(@id,'pm_')]/div[1]/div[1]/div[contains(@class,'exitBlock')]"
    for index in range(chart_count):
        before_count = len(_chart_containers(driver))
        print(f"Performance helper: pm_ close loop {index + 1}/{chart_count}", flush=True)
        button = driver.find_element(By.XPATH, close_xpath)
        try:
            driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'nearest'});", button)
            time.sleep(0.2)
        except Exception:
            pass
        button = driver.find_element(By.XPATH, close_xpath)
        button.click()
        _confirm_if_present(driver, timeout=0)
        WebDriverWait(driver, 5).until(lambda _: len(_chart_containers(driver)) < before_count)


def _chart_containers(driver):
    return driver.find_elements(By.XPATH, "//*[starts-with(@id,'pm_')]")


def _current_chart_container_count(driver):
    containers = _chart_containers(driver)
    if containers:
        return len(containers)
    return len(_chart_close_buttons(driver))


def _click_chart_close_icon(driver, button):
    if _dispatch_frontend_mouse_click(driver, button):
        return True
    for attempt in range(3):
        try:
            ActionChains(driver).move_to_element(button).click(button).perform()
            return True
        except Exception:
            pass
        try:
            image = button.find_element(By.TAG_NAME, "img")
            ActionChains(driver).move_to_element(image).click(image).perform()
            return True
        except Exception:
            pass
        try:
            width = max(1, int(button.size.get("width", 1)) // 2)
            height = max(1, int(button.size.get("height", 1)) // 2)
            ActionChains(driver).move_to_element_with_offset(button, width - 1, height - 1).click().perform()
            return True
        except Exception:
            if attempt == 2:
                try:
                    button.click()
                    return True
                except Exception:
                    return False
    return False


def _dispatch_frontend_mouse_click(driver, element):
    try:
        rect = driver.execute_script(
            "const r = arguments[0].getBoundingClientRect(); return {x:r.left,y:r.top,width:r.width,height:r.height};",
            element,
        )
        x = rect["x"] + rect["width"] / 2
        y = rect["y"] + rect["height"] / 2
        if x < 0 or y < 0 or rect["width"] <= 0 or rect["height"] <= 0:
            return False
        driver.execute_cdp_cmd("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": x, "y": y})
        driver.execute_cdp_cmd(
            "Input.dispatchMouseEvent",
            {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1},
        )
        driver.execute_cdp_cmd(
            "Input.dispatchMouseEvent",
            {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1},
        )
        return True
    except Exception:
        return False


def _batch_close_visible_chart_icons(driver, planned_count):
    closed_attempts = 0
    body = driver.find_element(By.TAG_NAME, "body")
    ActionChains(driver).move_to_element(body).click().send_keys(Keys.END).perform()
    time.sleep(0.2)
    stagnant_pages = 0
    for page_index in range(max(12, planned_count + 2)):
        visible_buttons = _visible_pm_chart_close_buttons_bottom_right_first(driver)
        close_method = "pm"
        if not visible_buttons:
            visible_buttons = _visible_chart_close_buttons_bottom_right_first(driver)
            close_method = "exitBlock"
        if visible_buttons:
            print(
                f"Performance helper: batch page {page_index + 1}, "
                f"click {len(visible_buttons)} visible {close_method} close icon(s) from bottom-right",
                flush=True,
            )
            for button in visible_buttons:
                if not _dispatch_frontend_mouse_click(driver, button):
                    try:
                        button.click()
                    except Exception:
                        _click_chart_close_icon(driver, button)
                closed_attempts += 1
                _confirm_if_present(driver, timeout=0)
            stagnant_pages = 0
        else:
            stagnant_pages += 1
            if stagnant_pages >= 2:
                break
        ActionChains(driver).send_keys(Keys.PAGE_UP).perform()
        time.sleep(0.15)
    print(f"Performance helper: batch close attempted {closed_attempts}/{planned_count}", flush=True)


def _visible_pm_chart_close_buttons_bottom_right_first(driver):
    buttons = [button for button in _pm_chart_close_buttons(driver) if _is_clickable_chart_close_icon(driver, button)]
    buttons.sort(key=lambda button: _button_screen_position(driver, button), reverse=True)
    return buttons


def _visible_chart_close_buttons_bottom_right_first(driver):
    buttons = _visible_chart_close_buttons(driver)
    buttons.sort(key=lambda button: _button_screen_position(driver, button), reverse=True)
    return buttons


def _button_screen_position(driver, button):
    try:
        rect = button.rect
        return (round(rect.get("y", 0), 1), round(rect.get("x", 0), 1))
    except Exception:
        return (0, 0)


def _is_clickable_chart_close_icon(driver, element):
    try:
        if not element.is_displayed():
            return False
        size = element.size
        if size.get("width", 0) <= 0 or size.get("height", 0) <= 0:
            return False
        rect = driver.execute_script(
            "const r = arguments[0].getBoundingClientRect(); return {x:r.x,y:r.y,width:r.width,height:r.height};",
            element,
        )
        viewport_width = driver.execute_script("return window.innerWidth || document.documentElement.clientWidth || 1200;")
        viewport_height = driver.execute_script("return window.innerHeight || document.documentElement.clientHeight || 800;")
        return (
            rect["width"] > 0
            and rect["height"] > 0
            and rect["x"] >= 0
            and rect["y"] >= 0
            and rect["x"] < viewport_width
            and rect["y"] < viewport_height
        )
    except Exception:
        return False


def _element_viewport_sort_key(driver, element):
    try:
        rect = driver.execute_script(
            "const r = arguments[0].getBoundingClientRect(); return {x:r.x,y:r.y,width:r.width,height:r.height};",
            element,
        )
        viewport_height = driver.execute_script("return window.innerHeight || document.documentElement.clientHeight || 800;")
        in_view = 0 <= rect["y"] <= viewport_height
        return (0 if in_view else 1, max(0, rect["y"]), max(0, rect["x"]))
    except Exception:
        return (2, 0, 0)


def _short_outer_html(driver, element, limit=500):
    try:
        html = driver.execute_script("return arguments[0].outerHTML;", element)
        return re.sub(r"\s+", " ", html or "")[:limit]
    except Exception as exc:
        return f"<unavailable: {exc}>"


def _element_debug(driver, element):
    try:
        info = driver.execute_script(
            """
            const e = arguments[0];
            const r = e.getBoundingClientRect();
            return {
                tag: e.tagName,
                id: e.id,
                className: e.className,
                text: e.innerText || e.textContent || '',
                title: e.getAttribute('title'),
                href: e.getAttribute('href'),
                onclick: e.getAttribute('onclick'),
                rect: {x: r.x, y: r.y, width: r.width, height: r.height},
                outerHTML: e.outerHTML,
                ancestors: (() => {
                    const list = [];
                    let node = e;
                    for (let i = 0; node && i < 8; i += 1, node = node.parentElement) {
                        list.push({
                            tag: node.tagName,
                            id: node.id,
                            className: node.className,
                            onclick: node.getAttribute && node.getAttribute('onclick')
                        });
                    }
                    return list;
                })()
            };
            """,
            element,
        )
        html = re.sub(r"\s+", " ", info.get("outerHTML") or "")[:500]
        return (
            f"tag={info.get('tag')} id={info.get('id')} class={info.get('className')} "
            f"title={info.get('title')} href={info.get('href')} onclick={info.get('onclick')} "
            f"rect={info.get('rect')} text={info.get('text')!r} ancestors={info.get('ancestors')} html={html}"
        )
    except Exception as exc:
        return f"<unavailable: {exc}>"


def _confirm_if_present(driver, timeout=0):
    end_time = time.time() + timeout
    try:
        WebDriverWait(driver, min(timeout, 1) if timeout else 0.1).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert_text = alert.text
        alert.accept()
        print(f"Performance helper: accepted browser alert text={alert_text!r}", flush=True)
        return alert_text or True
    except TimeoutException:
        pass

    while True:
        for locator in [
            (By.ID, "confirm_yes_button"),
            (By.CSS_SELECTOR, "#message_diag .button"),
            (By.XPATH, "//button[normalize-space()='Yes']"),
            (By.XPATH, "//button[normalize-space()='OK']"),
            (By.XPATH, "//input[@type='button' and (@value='Yes' or @value='OK')]"),
            (By.XPATH, "//input[@type='submit' and (@value='Yes' or @value='OK')]"),
            (By.XPATH, "//*[contains(@class,'modal') and not(contains(@style,'display: none'))]//button[normalize-space()='OK' or normalize-space()='Yes']"),
            (By.XPATH, "//*[contains(@class,'modal') and not(contains(@style,'display: none'))]//input[@value='OK' or @value='Yes']"),
        ]:
            for element in driver.find_elements(*locator):
                if element.is_displayed() and element.is_enabled():
                    message_text = _visible_dialog_text(driver, element)
                    print(
                        f"Performance helper: confirm dialog with locator={locator}, text={message_text!r}",
                        flush=True,
                    )
                    element.click()
                    return message_text or True
        if time.time() >= end_time:
            return False
        time.sleep(0.2)


def _visible_dialog_text(driver, button_element):
    candidates = []
    for locator in [
        (By.ID, "message_diag"),
        (By.CSS_SELECTOR, ".modal"),
        (By.CSS_SELECTOR, "[role='dialog']"),
        (By.XPATH, "//*[contains(normalize-space(.), 'No probes are available anymore')]"),
        (By.XPATH, "//*[contains(normalize-space(.), 'Message')]"),
    ]:
        try:
            candidates.extend(driver.find_elements(*locator))
        except Exception:
            pass
    try:
        candidates.extend(button_element.find_elements(By.XPATH, "./ancestor::*[self::div or self::table]"))
    except Exception:
        pass

    texts = []
    for candidate in candidates:
        try:
            if candidate.is_displayed():
                text = re.sub(r"\s+", " ", candidate.text or "").strip()
                if text and len(text) < 2000:
                    texts.append(text)
        except Exception:
            continue
    if texts:
        texts.sort(key=len, reverse=True)
        return texts[0]
    try:
        return (button_element.text or "").strip()
    except Exception:
        return ""


def _ack_create_message(driver, timeout=8):
    end_time = time.time() + timeout
    while time.time() < end_time:
        message = _confirm_if_present(driver, timeout=0)
        if message:
            return message
        time.sleep(0.1)
    return None


def _wait_create_demand_closed(driver, timeout=60):
    end_time = time.time() + timeout
    while time.time() < end_time:
        _confirm_if_present(driver, timeout=0)
        dialogs = driver.find_elements(By.ID, "create_demand_background")
        if not dialogs or not dialogs[0].is_displayed():
            return
        time.sleep(0.2)
    raise TimeoutException("Create Demand dialog did not close before timeout.")


def _expand_node_path(driver, node_name):
    _expand_tree_label(driver, "EMS")
    node_label = _label_by_text(driver, node_name)
    arrow = node_label.find_element(By.XPATH, "../div[contains(@class,'arrow')]")
    if "collapsed" in arrow.get_attribute("class"):
        arrow.click()
        WebDriverWait(driver, 10).until(lambda _: "collapsed" not in arrow.get_attribute("class"))


def _expand_node_by_ip(driver, node_ip):
    _expand_tree_label(driver, "EMS")
    node_label = _node_label_by_ip(driver, node_ip)
    arrow = node_label.find_element(By.XPATH, "../div[contains(@class,'arrow')]")
    if "collapsed" in arrow.get_attribute("class"):
        arrow.click()
        WebDriverWait(driver, 10).until(lambda _: "collapsed" not in arrow.get_attribute("class"))
    time.sleep(1)


def _expand_tree_label(driver, label_text):
    label = _label_by_text(driver, label_text)
    arrow = label.find_element(By.XPATH, "../div[contains(@class,'arrow')]")
    if "collapsed" in arrow.get_attribute("class"):
        arrow.click()
        WebDriverWait(driver, 10).until(lambda _: "collapsed" not in arrow.get_attribute("class"))


def _label_by_text(driver, label_text):
    return WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, f"//*[@id='tree_demand']//label[normalize-space()='{label_text}']"))
    )


def _node_label_by_ip(driver, node_ip, timeout=30):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//*[@id='tree_demand']//label[contains(normalize-space(.),'({node_ip})')]")
        )
    )


def _card_label(driver, slot_id, card_type, timeout=30):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//*[@id='tree_demand']//label[normalize-space()='{slot_id} - {card_type}']")
        )
    )


def _card_label_under_node_ip(driver, node_ip, slot_id, card_type, timeout=30):
    slot_prefix = f"{slot_id} - "
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//*[@id='tree_demand']//label[contains(normalize-space(.),"
                f"'({node_ip})')]/../ul/li[contains(normalize-space(.),"
                f"'{slot_prefix}') and contains(normalize-space(.),'{card_type}')]/label",
            )
        )
    )


def _node_ip_from_name(node_name):
    match = re.search(r"\((\d+\.\d+\.\d+\.\d+)\)", node_name or "")
    return match.group(1) if match else node_name


def canvas_numeric_values(driver):
    values = []
    for frame_values in canvas_numeric_values_by_frame(driver):
        values.extend(frame_values)
    return _unique_preserve_order(values)


def canvas_numeric_values_by_frame(driver):
    frame_values = []
    frames = driver.find_elements(By.TAG_NAME, "iframe")
    for frame in frames:
        try:
            driver.switch_to.frame(frame)
            frame_values.append(_unique_preserve_order(_canvas_numeric_values_in_current_frame(driver)))
        finally:
            driver.switch_to.default_content()
    return frame_values


def rendered_canvas_count_by_frame(driver):
    rendered_count = 0
    frames = driver.find_elements(By.TAG_NAME, "iframe")
    for frame in frames:
        try:
            driver.switch_to.frame(frame)
            if _frame_has_rendered_canvas(driver):
                rendered_count += 1
        finally:
            driver.switch_to.default_content()
    return rendered_count


def chart_visual_data_states(driver):
    states = []
    frames = driver.find_elements(By.TAG_NAME, "iframe")
    for frame_index, frame in enumerate(frames, start=1):
        try:
            driver.switch_to.frame(frame)
            states.append(_frame_visual_data_state(driver, frame_index))
        finally:
            driver.switch_to.default_content()
    return states


def chart_visual_data_states_across_page(driver, expected_count):
    open_current_page(driver)
    _scroll_current_page_to_bottom_and_count_charts(driver)
    states_by_frame = {}
    body = driver.find_element(By.TAG_NAME, "body")
    ActionChains(driver).move_to_element(body).click().send_keys(Keys.HOME).perform()
    time.sleep(0.5)
    max_steps = max(8, expected_count + 2)
    for step_index in range(max_steps):
        for state in chart_visual_data_states(driver):
            key = _chart_state_key(state)
            previous = states_by_frame.get(key)
            if previous is None or _chart_state_score(state) > _chart_state_score(previous):
                states_by_frame[key] = state
        passed_count = len([
            state for state in states_by_frame.values()
            if state["has_line_or_point"] and state["has_numeric_value"]
        ])
        if passed_count >= expected_count:
            break
        ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(0.5)
    ActionChains(driver).send_keys(Keys.HOME).perform()
    return list(states_by_frame.values())


def _scroll_current_page_to_bottom_and_count_charts(driver, stable_rounds=2, max_steps=30):
    body = driver.find_element(By.TAG_NAME, "body")
    ActionChains(driver).move_to_element(body).click().send_keys(Keys.HOME).perform()
    time.sleep(0.3)
    last_count = -1
    stable_count = 0
    for step in range(max_steps):
        pm_count = len(_chart_containers(driver))
        exit_count = len(_chart_close_buttons(driver))
        current_count = max(pm_count, exit_count)
        print(
            f"Performance helper: scroll count step={step}, pm={pm_count}, exitBlock={exit_count}",
            flush=True,
        )
        if current_count == last_count:
            stable_count += 1
        else:
            stable_count = 0
            last_count = current_count
        if stable_count >= stable_rounds:
            break
        ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(0.4)
    return max(last_count, 0)


def _chart_state_key(state):
    title = state.get("title") or ""
    if title:
        return title
    values = ",".join(state.get("numeric_values", []))
    return f"{state.get('frame')}:{values}:{state.get('canvas_count')}"


def _chart_state_score(state):
    return int(state["has_line_or_point"]) + int(state["has_numeric_value"]) + len(state.get("numeric_values", []))


def _frame_visual_data_state(driver, frame_index):
    canvases = [
        canvas
        for canvas in driver.find_elements(By.TAG_NAME, "canvas")
        if canvas.is_displayed() and canvas.size.get("width", 0) > 20 and canvas.size.get("height", 0) > 20
    ]
    has_line_or_point = any(_canvas_screenshot_has_content(canvas) for canvas in canvases)
    numeric_values = _unique_preserve_order(_canvas_numeric_values_from_canvases(driver, canvases))
    return {
        "frame": frame_index,
        "title": _frame_title_text(driver),
        "canvas_count": len(canvases),
        "has_line_or_point": has_line_or_point,
        "has_numeric_value": bool(numeric_values),
        "numeric_values": numeric_values[:5],
    }


def _frame_title_text(driver):
    text = driver.find_element(By.TAG_NAME, "body").text
    for line in text.splitlines():
        if "Interface(" in line and "Polling" in line:
            return line.strip()
    return ""


def _frame_has_rendered_canvas(driver):
    canvases = [
        canvas
        for canvas in driver.find_elements(By.TAG_NAME, "canvas")
        if canvas.is_displayed() and canvas.size.get("width", 0) > 20 and canvas.size.get("height", 0) > 20
    ]
    return any(_canvas_screenshot_has_content(canvas) for canvas in canvases)


def _canvas_screenshot_has_content(canvas):
    image = Image.open(BytesIO(canvas.screenshot_as_png)).convert("RGB")
    width, height = image.size
    if width <= 20 or height <= 20:
        return False
    step_x = max(1, width // 40)
    step_y = max(1, height // 25)
    sampled = []
    for y in range(0, height, step_y):
        for x in range(0, width, step_x):
            sampled.append(image.getpixel((x, y)))
    if not sampled:
        return False
    unique_colors = set(sampled)
    non_background = [
        pixel
        for pixel in sampled
        if not (pixel[0] > 245 and pixel[1] > 245 and pixel[2] > 245)
    ]
    return len(unique_colors) >= 8 and len(non_background) >= max(20, len(sampled) // 50)


def _canvas_numeric_values_in_current_frame(driver):
    canvases = [
        canvas
        for canvas in driver.find_elements(By.TAG_NAME, "canvas")
        if canvas.is_displayed() and canvas.size.get("width", 0) > 20 and canvas.size.get("height", 0) > 20
    ]
    return _canvas_numeric_values_from_canvases(driver, canvases)


def _canvas_numeric_values_from_canvases(driver, canvases):
    values = []
    for canvas in canvases:
        width = int(canvas.size.get("width", 0))
        height = int(canvas.size.get("height", 0))
        sample_points = [
            (int(width * (x_ratio - 0.5)), int(height * (y_ratio - 0.5)))
            for x_ratio, y_ratio in ((0.2, 0.35), (0.35, 0.5), (0.5, 0.5), (0.65, 0.5), (0.8, 0.65))
        ]
        for x_offset, y_offset in sample_points:
            try:
                ActionChains(driver).move_to_element_with_offset(canvas, x_offset, y_offset).perform()
                time.sleep(0.08)
                point_values = _extract_performance_numbers(driver.find_element(By.TAG_NAME, "body").text)
                if point_values:
                    values.extend(point_values)
                    break
            except Exception:
                continue
    return values


def _has_visible_canvas(driver):
    for canvas in driver.find_elements(By.TAG_NAME, "canvas"):
        size = canvas.size
        if canvas.is_displayed() and size.get("width", 0) > 20 and size.get("height", 0) > 20:
            return True
    return False


def _extract_performance_numbers(text):
    values = []
    for match in re.finditer(r"(?<![\w.-])[-+]?\d+(?:\.\d+)?\s*(?:bps|Bps|Kbps|Mbps|Gbps|pps|%|packets|bytes)?(?![\w.-])", text):
        value = match.group(0).strip()
        if _is_performance_value(value):
            values.append(value)
    return values


def _is_performance_value(value):
    number = re.match(r"[-+]?\d+(?:\.\d+)?", value)
    if not number:
        return False
    numeric = float(number.group(0))
    if numeric < 0:
        return False
    if any(unit in value for unit in ["bps", "Bps", "Kbps", "Mbps", "Gbps", "pps", "%", "packets", "bytes"]):
        return True
    return 0 <= numeric <= 10_000_000


def _numeric_token(value):
    match = re.match(r"[-+]?\d+(?:\.\d+)?", value)
    return match.group(0) if match else value


def _unique_preserve_order(values):
    seen = set()
    unique_values = []
    for value in values:
        if value not in seen:
            seen.add(value)
            unique_values.append(value)
    return unique_values


def xpath_literal(text):
    if "'" not in text:
        return f"'{text}'"
    if '"' not in text:
        return f'"{text}"'
    parts = text.split("'")
    return "concat(" + ", \"'\", ".join(f"'{part}'" for part in parts) + ")"
