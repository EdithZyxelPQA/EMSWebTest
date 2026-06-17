import pytest


def _find_first(driver, locators):
    for by, value in locators:
        elements = driver.find_elements(by, value)
        if elements:
            return elements[0]
    return None


def _login(driver, config, username, password):
    from selenium.webdriver.common.by import By

    driver.get(config["base_url"])

    username_input = _find_first(
        driver,
        [
            (By.ID, "name"),
            (By.NAME, "user"),
            (By.CSS_SELECTOR, "input[type='text']"),
        ],
    )
    password_input = _find_first(
        driver,
        [
            (By.ID, "passwd"),
            (By.NAME, "pass"),
            (By.CSS_SELECTOR, "input[type='password']"),
        ],
    )

    assert username_input is not None, "Username input was not found."
    assert password_input is not None, "Password input was not found."

    username_input.clear()
    username_input.send_keys(username)
    password_input.clear()
    password_input.send_keys(password)

    submit = _find_first(
        driver,
        [
            (By.ID, "signin"),
            (By.CSS_SELECTOR, "input[type='submit']"),
            (By.CSS_SELECTOR, "button[type='submit']"),
            (By.XPATH, "//*[@value='Login' or normalize-space()='Login']"),
        ],
    )
    assert submit is not None, "Login submit control was not found."
    submit.click()


def _is_authenticated(driver, config):
    from selenium.webdriver.common.by import By

    for indicator in config["authenticated_indicators"]:
        if driver.find_elements(By.ID, indicator):
            return True
    page_text = driver.page_source.lower()
    return "logout" in page_text or "ems" in driver.title.lower()


@pytest.mark.ui
def test_empty_login_is_rejected(driver, config, screenshot):
    _login(driver, config, "", "")
    screenshot(driver, "empty_login_result")

    assert not _is_authenticated(driver, config), (
        "Empty credentials unexpectedly reached an authenticated state."
    )


@pytest.mark.ui
def test_valid_login_smoke(driver, config, screenshot):
    _login(driver, config, config["username"], config["password"])
    screenshot(driver, "valid_login_result")

    assert _is_authenticated(driver, config), (
        "Configured credentials did not reach an authenticated EMS state."
    )


@pytest.mark.ui
def test_authenticated_page_is_not_blank(driver, config, screenshot):
    _login(driver, config, config["username"], config["password"])
    screenshot(driver, "authenticated_page")

    source = driver.page_source.strip()
    assert _is_authenticated(driver, config)
    assert len(source) > 500, "Authenticated page source is unexpectedly small."


@pytest.mark.ui
def test_about_dialog_version_if_available(driver, config, screenshot):
    from selenium.webdriver.common.by import By

    _login(driver, config, config["username"], config["password"])
    about = _find_first(
        driver,
        [
            (By.ID, "about"),
            (By.LINK_TEXT, "About"),
            (By.PARTIAL_LINK_TEXT, "About"),
        ],
    )
    if about is None:
        pytest.skip("About control is not available on this EMS page.")

    about.click()
    screenshot(driver, "about_dialog")
    version_text = ""
    for locator in [(By.ID, "emsversion"), (By.CSS_SELECTOR, "[id*='version']")]:
        element = _find_first(driver, [locator])
        if element is not None:
            version_text = element.text.strip()
            break

    assert version_text, "About dialog opened but no EMS version text was found."

