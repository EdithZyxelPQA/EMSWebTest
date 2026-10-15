"""Make basic Selenium actions tolerate a slow EMS web UI.

The EMS pages draw asynchronously and show a loading overlay ("loadind_*",
"configure_loader*") while busy.  Many cases call
``driver.find_element(...).click()`` right after a fixed ``time.sleep``, which
fails whenever the screen is slower than expected.  ``install()`` patches the
Selenium classes once so that:

* click / send_keys / clear first wait for the loading overlay to disappear
  and retry for a while when the element is covered or not interactable yet
  (a not-interactable element is scrolled into view first; for an <option>,
  e.g. from Select, its <select> is scrolled);
* Select.select_by_* retries while the options are reloaded (stale options or
  the wanted option not there yet), looking the <select> up again;
* find_element keeps looking for a while for menu links (LINK_TEXT) or while
  the page is still loading.

Other lookups keep their original behaviour so "element absent" checks are not
slowed down.
"""

import time

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    InvalidElementStateException,
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select

ACTION_RETRY_SECONDS = 30
FIND_RETRY_SECONDS = 15
SHORT_FIND_RETRY_SECONDS = 6
OVERLAY_WAIT_SECONDS = 120

_LOADING_OVERLAY_JS = """
return Array.from(document.querySelectorAll("[id^='loadind'], [id^='configure_loader']")).some(function (e) {
    var s = window.getComputedStyle(e);
    return s.display !== 'none' && s.visibility !== 'hidden' && e.getClientRects().length > 0;
});
"""

_installed = False
_originalClick = WebElement.click
_originalSendKeys = WebElement.send_keys
_originalClear = WebElement.clear
_originalFindElement = WebDriver.find_element
_originalSelect = {
    name: getattr(Select, name)
    for name in ("select_by_visible_text", "select_by_value", "select_by_index")
}


def _isLoading(driver):
    try:
        return bool(_originalExecuteScript(driver, _LOADING_OVERLAY_JS))
    except Exception:
        return False


def _originalExecuteScript(driver, script, *args):
    return WebDriver.execute_script(driver, script, *args)


def _waitIdle(driver, timeout=OVERLAY_WAIT_SECONDS):
    endTime = time.monotonic() + timeout
    while _isLoading(driver) and time.monotonic() < endTime:
        time.sleep(0.5)


_SCROLL_INTO_VIEW_JS = """
var e = arguments[0];
var target = (e.tagName === "OPTION") ? (e.closest("select") || e) : e;
target.scrollIntoView({block: "center", inline: "nearest"});
"""


def _scrollIntoView(driver, element):
    # An element below the visible part of a scrolling form (e.g. a profile form) is
    # "not interactable"; Select clicks <option>, so scroll its <select> into view.
    try:
        _originalExecuteScript(driver, _SCROLL_INTO_VIEW_JS, element)
    except Exception:
        pass


def _retryAction(element, action, *args):
    driver = element._parent
    _waitIdle(driver)
    endTime = time.monotonic() + ACTION_RETRY_SECONDS
    while True:
        try:
            return action(element, *args)
        except (ElementClickInterceptedException, ElementNotInteractableException, InvalidElementStateException) as exc:
            if time.monotonic() >= endTime:
                raise
            if isinstance(exc, ElementNotInteractableException):
                _scrollIntoView(driver, element)
            time.sleep(0.5)
            _waitIdle(driver)
        except StaleElementReferenceException:
            # The page was redrawn after the element was found: look it up again
            locator = getattr(element, "_patienceLocator", None)
            if locator is None or time.monotonic() >= endTime:
                raise
            time.sleep(0.5)
            _waitIdle(driver)
            try:
                element = _findElement(driver, *locator)
            except NoSuchElementException:
                raise


def _click(self):
    return _retryAction(self, _originalClick)


def _sendKeys(self, *value):
    return _retryAction(self, _originalSendKeys, *value)


def _clear(self):
    return _retryAction(self, _originalClear)


def _remember(element, by, value):
    try:
        element._patienceLocator = (by, value)
    except Exception:
        pass
    return element


def _findElement(self, by=By.ID, value=None):
    try:
        return _remember(_originalFindElement(self, by, value), by, value)
    except NoSuchElementException:
        pass
    # Menu links and lookups during loading get the long retry; other lookups a
    # short one so that "element is absent" checks are not slowed down much.
    longRetry = by in (By.LINK_TEXT, By.PARTIAL_LINK_TEXT) or _isLoading(self)
    endTime = time.monotonic() + (FIND_RETRY_SECONDS if longRetry else SHORT_FIND_RETRY_SECONDS)
    while True:
        _waitIdle(self)
        try:
            return _remember(_originalFindElement(self, by, value), by, value)
        except NoSuchElementException:
            if time.monotonic() >= endTime:
                raise
            time.sleep(0.5)


def _patientSelect(name):
    original = _originalSelect[name]

    def select(self, value):
        # Choosing one dropdown can make the page reload the options of another one (e.g. the
        # bandwidth profiles after a T-cont is chosen): the options read by Select go stale, or
        # the wanted option is not there yet.  Wait, look the <select> up again and retry.
        endTime = time.monotonic() + ACTION_RETRY_SECONDS
        while True:
            try:
                return original(self, value)
            except (StaleElementReferenceException, NoSuchElementException):
                if time.monotonic() >= endTime:
                    raise
                time.sleep(0.5)
                driver = self._el._parent
                _waitIdle(driver)
                locator = getattr(self._el, "_patienceLocator", None)
                if locator is not None:
                    try:
                        self._el = _findElement(driver, *locator)
                    except NoSuchElementException:
                        pass

    select.__name__ = name
    return select


def install():
    global _installed
    if _installed:
        return
    WebElement.click = _click
    WebElement.send_keys = _sendKeys
    WebElement.clear = _clear
    WebDriver.find_element = _findElement
    for name in _originalSelect:
        setattr(Select, name, _patientSelect(name))
    _installed = True
