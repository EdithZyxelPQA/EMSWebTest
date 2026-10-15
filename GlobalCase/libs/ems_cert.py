"""EMS1-7240 helpers: swap the EMS HTTPS certificate for one signed by a lab CA and
check the web UI with real certificate validation (no ignore-certificate-errors)."""
import ctypes
import hashlib
import json
import re
import shlex
import socket
import ssl
import subprocess
import time
import urllib.request
from urllib.parse import urlparse

import paramiko
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from libs.ems_configuration import _click_top_menu, _select_configuration_device
from libs.ems_tables import _wait_idle


EMS_HOME = "/opt/ELEMENTVIEW_MASTER"
PFX_PATH = f"{EMS_HOME}/conf/emsauth.pfx"
EMS_BIN = f"{EMS_HOME}/bin"
TOMCAT_HOME = f"{EMS_BIN}/apache-tomcat"
SERVER_XML = f"{TOMCAT_HOME}/conf/server.xml"
CATALINA_OUT = f"{TOMCAT_HOME}/logs/catalina.out"
# The EMS runs two Tomcats: apache-tomcat (WEB Server) and apache-tomcat-RESTful (Inventory Collect Server).
# Only the WEB one may be touched, so match its own conf path, never the shared Bootstrap class name.
TOMCAT_PROCESS = "[a]pache-tomcat/conf/logging.properties"
RESTFUL_TOMCAT_PROCESS = "[a]pache-tomcat-RESTful/conf/logging.properties"
LAB_CA_CN = "EMS Lab CA"

# EMS page levels: 1 = left icon menu, 2 = tab bar, 3 = list beside the content.
# Lists inside the content (users, regions, table rows) are not clicked.
TOP_MENU_CSS = "#Menu_text > li"
LEVEL2_CSS = "#tab_background a"
LEVEL3_CSS = "#content_list a, #Inventory_port_type_list a, #fault_list a"
# Level 4 = inner tabs, walked only under these level-3 pages.
LEVEL4_CSS = "#tab_content .content_Menu a"
LEVEL4_PAGES = {("System Properties", "System Setting"), ("System Properties", "System Storage")}

CERT_ERROR_PATTERN = re.compile(r"ERR_CERT|ERR_SSL|ERR_BAD_SSL", re.IGNORECASE)


# ---------------------------------------------------------------- EMS server
class EmsShell:
    """SSH to the EMS server as the server user and run commands as root through sudo."""

    def __init__(self, host, username, password, sudo_password):
        self.login = (host, username, password)
        self.sudo_password = sudo_password
        self.client = None
        self._connect()

    def _connect(self):
        if self.client:
            self.client.close()
        host, username, password = self.login
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(host, 22, username, password, timeout=30)

    def _exec(self, full, timeout):
        # The lab EMS sometimes drops the SSH session; the command has not started when
        # exec_command fails, so reconnecting and sending it again is safe.
        for attempt in range(1, 4):
            try:
                return self.client.exec_command(full, timeout=timeout)
            except (EOFError, OSError, paramiko.SSHException) as error:
                print(f"[EMS] SSH dropped ({error!r}), reconnect {attempt}/3", flush=True)
                time.sleep(10)
                self._connect()
        return self.client.exec_command(full, timeout=timeout)

    def run(self, command, timeout=180, check=True, quiet=False):
        full = "sudo -S -p '' bash -lc " + shlex.quote(command)
        stdin, stdout, stderr = self._exec(full, timeout)
        stdin.write(self.sudo_password + "\n")
        stdin.flush()
        out = stdout.read().decode("utf-8", errors="ignore")
        err = stderr.read().decode("utf-8", errors="ignore")
        rc = stdout.channel.recv_exit_status()
        print(f"[EMS] # {command}" + ("" if quiet else f"\n{out}{err}".rstrip()), flush=True)
        if check and rc != 0:
            raise AssertionError(f"EMS command failed (rc={rc}): {command}\n{out}{err}")
        return out

    def get_file(self, remote_path, local_path):
        try:
            sftp = self.client.open_sftp()
        except (EOFError, OSError, paramiko.SSHException):
            self._connect()
            sftp = self.client.open_sftp()
        try:
            sftp.get(remote_path, local_path)
        finally:
            sftp.close()

    def close(self):
        self.client.close()


def https_connector(server_xml_text, port):
    """Return the attributes (lower-case keys) of the active Connector on `port`, nested Certificate included."""
    text = re.sub(r"<!--.*?-->", "", server_xml_text, flags=re.DOTALL)
    for match in re.finditer(r"<Connector\b(?:[^>]*?/>|[^>]*?>.*?</Connector>)", text, flags=re.DOTALL):
        block = match.group(0)
        attrs = {k.lower(): v for k, v in re.findall(r'(\w+)\s*=\s*"([^"]*)"', block)}
        if attrs.get("port") == str(port):
            return attrs
    raise AssertionError(f"No active Connector with port {port} in {SERVER_XML}")


def connector_keystore(attrs):
    def pick(*names):
        return next((attrs[n] for n in names if n in attrs), None)

    return {
        "file": pick("certificatekeystorefile", "keystorefile"),
        "type": pick("certificatekeystoretype", "keystoretype"),
        "password": pick("certificatekeystorepassword", "keystorepass"),
    }


def pfx_cert_command(pfx_path, password, x509_args):
    """Shell pipeline that prints details of the leaf certificate in a PKCS12 file (OpenSSL 1.1 and 3.x)."""
    pfx = shlex.quote(pfx_path)
    pw = shlex.quote(f"pass:{password}")
    extract = (
        f"(openssl pkcs12 -in {pfx} -nokeys -clcerts -passin {pw} 2>/dev/null"
        f" || openssl pkcs12 -legacy -in {pfx} -nokeys -clcerts -passin {pw} 2>/dev/null)"
    )
    return f"{extract} | openssl x509 {x509_args}"


def tomcat_user(shell):
    out = shell.run(f"ps -eo user:32,args | grep '{TOMCAT_PROCESS}' | awk '{{print $1}}' | head -1", check=False)
    return out.strip() or "root"


def _pids(shell, pattern):
    return shell.run(f"pgrep -f '{pattern}'", check=False).split()


def _restart_web_once(shell, as_user, timeout):
    """One shutdown.sh / startup.sh of the WEB Tomcat; return the first catalina.out line written by it."""
    start_line = int((shell.run(f"wc -l < {CATALINA_OUT} 2>/dev/null || echo 0", check=False).strip() or "0"))
    # Same working directory as emsstop/emsstart: EMS resolves ../conf from it.
    shell.run(as_user(f"cd {EMS_BIN} && apache-tomcat/bin/shutdown.sh"), check=False)
    time.sleep(10)
    deadline = time.time() + 120
    while web_pids := _pids(shell, TOMCAT_PROCESS):
        if time.time() > deadline:
            # Only the WEB Tomcat PIDs found above; never a name-wide pkill.
            shell.run(f"kill {' '.join(web_pids)}", check=False)
            time.sleep(15)
            break
        time.sleep(5)
    assert not _pids(shell, TOMCAT_PROCESS), "WEB Tomcat still running after shutdown.sh"
    shell.run(as_user(f"cd {EMS_BIN} && apache-tomcat/bin/startup.sh") + " </dev/null >/dev/null 2>&1")

    deadline = time.time() + timeout
    while time.time() < deadline:
        total = int((shell.run(f"wc -l < {CATALINA_OUT}", check=False).strip() or "0"))
        first = start_line + 1 if total >= start_line else 1  # log rotated during restart
        if "Server startup in" in shell.run(f"tail -n +{first} {CATALINA_OUT}", check=False, quiet=True):
            return first
        time.sleep(15)
    raise AssertionError(f"Tomcat did not log 'Server startup in' within {timeout}s")


def restart_tomcat(shell, run_user, ems_port, verify=None, attempts=3, timeout=900):
    """Restart only the WEB Tomcat until the web app really works; return the catalina.out lines of the good start.

    The EMS services open a new MySQL connection per query, so connection peaks briefly pass max_connections.
    If that happens while the web app initialises its topology/user-access data, the init is never retried
    (myTopo stays null) and pages such as Alarm stay empty. Such a start is detected and the WEB Tomcat is
    restarted again. `verify()` (e.g. log in and read Alarm) returns a list of problems; it also triggers the
    lazy init, so the log is read after it.
    """
    def as_user(cmd):
        return cmd if run_user == "root" else f"su -s /bin/bash {shlex.quote(run_user)} -c {shlex.quote(cmd)}"

    restful_before = _pids(shell, RESTFUL_TOMCAT_PROCESS)
    for attempt in range(1, attempts + 1):
        first = _restart_web_once(shell, as_user, timeout)
        listen = shell.run(f"ss -tln 'sport = :{ems_port}'", check=False)
        assert "LISTEN" in listen, f"Port {ems_port} is not listening after Tomcat restart:\n{listen}"
        restful_after = _pids(shell, RESTFUL_TOMCAT_PROCESS)
        assert restful_after == restful_before, (
            f"Inventory Collect Server (apache-tomcat-RESTful) changed during WEB Tomcat restart: {restful_before} -> {restful_after}"
        )
        time.sleep(30)
        problems = verify() if verify else []
        new_log = shell.run(f"tail -n +{first} {CATALINA_OUT}", check=False, quiet=True)
        init_errors = {
            pattern: new_log.count(pattern)
            for pattern in ("Too many connections", "TopoTreeControlInterface.myTopo", "SQLNonTransientConnectionException")
            if new_log.count(pattern)
        }
        if init_errors:
            problems.append(f"DB init errors in catalina.out {init_errors}")
        print(f"[EMS] WEB Tomcat restart {attempt}/{attempts}: {'OK' if not problems else problems}", flush=True)
        if not problems:
            return new_log
    raise AssertionError(
        f"WEB Tomcat did not come up working after {attempts} restarts: {problems}. EMS pages may be empty; "
        f"restart only the WEB Tomcat again (cd {EMS_BIN} && apache-tomcat/bin/shutdown.sh, then apache-tomcat/bin/startup.sh)"
    )


def web_ready_problems(browser_name, download_path, ems_url, username, password, timeout=90):
    """Log in with a browser that ignores certificate errors and check that Alarm > Active shows data."""
    from libs.browser import close_browser
    from libs.ems_ui import login_ems

    parsed = urlparse(ems_url)
    try:
        wait_https_ready(parsed.hostname, parsed.port or 443)
    except AssertionError as error:
        return [str(error)]
    driver = create_cert_browser(browser_name, download_path, ignore_cert_errors=True)
    try:
        driver.implicitly_wait(10)
        driver.get(ems_url)
        login_ems(driver, username, password)
        time.sleep(5)
        driver.find_element(By.CSS_SELECTOR, "#i_menu_alarm > a").click()
        try:
            rows = WebDriverWait(driver, timeout, poll_frequency=3).until(
                lambda d: d.execute_script("return document.querySelectorAll('#alarm_activeAlarmTable_body tbody tr').length;")
            )
        except TimeoutException:
            return [f"Alarm > Active stays empty {timeout}s after login (web app data init failed)"]
        print(f"[EMS] web check: login OK, Alarm > Active {rows} rows", flush=True)
        return []
    except Exception as error:
        return [f"web check failed: {type(error).__name__}: {(str(error).strip().splitlines() or [''])[0]}"]
    finally:
        close_browser(driver)


def wait_https_ready(ip, port, timeout=600):
    """Wait until the EMS web app answers again (certificate not checked here)."""
    ctx = ssl._create_unverified_context()
    url = f"https://{ip}:{port}/netatlasems/"
    deadline = time.time() + timeout
    last_error = None
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=15, context=ctx) as resp:
                if resp.status < 500:
                    return
        except Exception as error:
            last_error = error
        time.sleep(10)
    raise AssertionError(f"EMS web {url} not ready within {timeout}s: {last_error}")


def server_cert(ip, port, server_name=None, cafile=None):
    """TLS handshake with the EMS. With `cafile` the chain and host/IP are verified by Python's ssl."""
    if cafile:
        ctx = ssl.create_default_context(cafile=cafile)
    else:
        ctx = ssl._create_unverified_context()
    with socket.create_connection((ip, port), timeout=15) as sock:
        with ctx.wrap_socket(sock, server_hostname=server_name or ip) as tls:
            return tls.getpeercert(binary_form=True), tls.getpeercert()


def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()


# ---------------------------------------------------------------- Windows client
def is_windows_admin():
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def _powershell(command):
    result = subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", command],
        capture_output=True, text=True, timeout=120,
    )
    print(f"[PC] PS> {command}\n{result.stdout}{result.stderr}".rstrip(), flush=True)
    return result


def pem_thumbprint(pem_path):
    with open(pem_path, encoding="ascii") as f:
        der = ssl.PEM_cert_to_DER_cert(f.read())
    return hashlib.sha1(der).hexdigest().upper()


def import_lab_ca(pem_path):
    _powershell(f"Import-Certificate -FilePath '{pem_path}' -CertStoreLocation Cert:\\LocalMachine\\Root | Out-Null")
    return pem_thumbprint(pem_path)


def lab_ca_count(store="LocalMachine"):
    result = _powershell(
        f"@(Get-ChildItem Cert:\\{store}\\Root | Where-Object {{ $_.Subject -eq 'CN={LAB_CA_CN}' }}).Count"
    )
    return int((result.stdout.strip() or "0").splitlines()[-1])


def remove_lab_ca():
    _powershell(
        f"Get-ChildItem Cert:\\LocalMachine\\Root | Where-Object {{ $_.Subject -eq 'CN={LAB_CA_CN}' }} | Remove-Item"
    )
    return lab_ca_count()


# ---------------------------------------------------------------- browser
def create_cert_browser(browser_name, download_path, host_rules=None, ignore_cert_errors=False):
    """Chrome/Edge with the performance log on. Firefox cannot map hosts or read the Windows store, so Chrome is used instead."""
    use_edge = browser_name.lower() == "edge"
    options = webdriver.EdgeOptions() if use_edge else webdriver.ChromeOptions()
    if ignore_cert_errors:
        options.add_argument("ignore-certificate-errors")
    if host_rules:
        options.add_argument(f"--host-resolver-rules={host_rules}")
    options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": download_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
        },
    )
    options.set_capability("ms:loggingPrefs" if use_edge else "goog:loggingPrefs", {"performance": "ALL"})
    # Network events only: page/timeline events on big tables make the renderer run out of memory.
    options.add_experimental_option("perfLoggingPrefs", {"enableNetwork": True, "enablePage": False})
    return webdriver.Edge(options=options) if use_edge else webdriver.Chrome(options=options)


class NetworkLog:
    """Requests seen by the browser, kept across page loads like DevTools "Preserve log"."""

    def __init__(self, driver):
        self.driver = driver
        self.events = []
        self.urls = {}

    def drain(self):
        try:
            entries = self.driver.get_log("performance")
        except WebDriverException:
            return
        for entry in entries:
            message = json.loads(entry["message"])["message"]
            method = message.get("method")
            params = message.get("params", {})
            if method == "Network.requestWillBeSent":
                self.urls[params.get("requestId")] = params.get("request", {}).get("url", "")
            elif method in ("Network.responseReceived", "Network.loadingFailed"):
                self.events.append(message)

    def mark(self):
        self.drain()
        return len(self.events)

    def cert_failures(self, host, since=0):
        """Requests to `host` that failed on TLS or were delivered insecurely."""
        self.drain()
        failures = []
        for message in self.events[since:]:
            params = message["params"]
            if message["method"] == "Network.loadingFailed":
                url = self.urls.get(params.get("requestId"), "")
                error = params.get("errorText", "")
                if urlparse(url).hostname == host and CERT_ERROR_PATTERN.search(error):
                    failures.append(f"{url} -> {error}")
            else:
                response = params.get("response", {})
                url = response.get("url", "")
                if url.startswith("https://") and urlparse(url).hostname == host and response.get("securityState") == "insecure":
                    failures.append(f"{url} -> securityState insecure")
        return failures

    def failed_requests(self, since=0):
        """Every failed or HTTP-error request (any host) since `since`, for diagnosing a page that did not load."""
        self.drain()
        failed = []
        for message in self.events[since:]:
            params = message["params"]
            if message["method"] == "Network.loadingFailed":
                error = params.get("errorText", "")
                if error != "net::ERR_ABORTED":
                    failed.append(f"{self.urls.get(params.get('requestId'), '')} -> {error}")
            else:
                response = params.get("response", {})
                if response.get("status", 0) >= 400:
                    failed.append(f"{response.get('url', '')} -> HTTP {response.get('status')}")
        return failed

    def document_response(self, host):
        """Last top-level document response from `host` (the EMS page in the address bar)."""
        self.drain()
        for message in reversed(self.events):
            params = message["params"]
            if message["method"] == "Network.responseReceived" and params.get("type") == "Document":
                response = params.get("response", {})
                if urlparse(response.get("url", "")).hostname == host:
                    return response
        return None


def cert_warning_shown(driver):
    """Chrome/Edge certificate interstitial ("Your connection is not private")."""
    driver.implicitly_wait(0)
    try:
        return bool(driver.find_elements(By.ID, "details-button")) and not driver.find_elements(By.ID, "name")
    finally:
        driver.implicitly_wait(10)


def _visible_link_texts(driver, css):
    return driver.execute_script(
        "return Array.from(document.querySelectorAll(arguments[0]))"
        ".filter(a => a.offsetParent !== null && a.innerText.trim()).map(a => a.innerText.trim());",
        css,
    )


def _click_link(driver, css, text):
    for element in driver.find_elements(By.CSS_SELECTOR, css):
        try:
            if element.is_displayed() and element.text.strip() == text:
                driver.execute_script("arguments[0].click();", element)
                time.sleep(2)
                _wait_idle(driver)
                return True
        except StaleElementReferenceException:
            continue
    return False


def _walk_level(driver, css, path, on_page, children=None):
    """Click each visible link of a level, check the page, then walk its children (if any)."""
    for text in _visible_link_texts(driver, css):
        if not _click_link(driver, css, text):
            on_page(path + [text], f"cannot click {text}")
            continue
        on_page(path + [text])
        if children:
            children(path + [text])


def walk_all_pages(driver, on_page):
    """Open every level-1 menu, level-2 tab, level-3 list item and the listed level-4 tabs; call on_page(path) on each."""
    driver.switch_to.default_content()
    tops = driver.execute_script(
        "return Array.from(document.querySelectorAll(arguments[0])).map(li => [li.id, li.innerText.trim()]);",
        TOP_MENU_CSS,
    )
    assert tops, "EMS top menu not found"
    for li_id, top in tops:
        driver.switch_to.default_content()
        driver.find_element(By.CSS_SELECTOR, f"#{li_id} > a").click()
        time.sleep(2)
        _wait_idle(driver)
        on_page([top])
        level2 = _visible_link_texts(driver, LEVEL2_CSS) or [None]
        for tab in level2:
            path = [top]
            if tab:
                path = [top, tab]
                if not _click_link(driver, LEVEL2_CSS, tab):
                    on_page(path, f"cannot click tab {tab}")
                    continue
                on_page(path)
            def level4(level3_path):
                if tuple(level3_path[-2:]) in LEVEL4_PAGES:
                    _walk_level(driver, LEVEL4_CSS, level3_path, on_page)

            _walk_level(driver, LEVEL3_CSS, path, on_page, level4)
    return [top for _, top in tops]


_CONTENT_JS = r"""
const root = document.getElementById('div_background_other') || document.body;
const tabs = Array.from(root.querySelectorAll('[id^="tab_content_"]')).filter(e => e.offsetParent !== null);
const targets = tabs.length ? tabs : [root];
return targets.map(e => ({
  id: e.id,
  text: e.innerText.trim().length,
  widgets: e.querySelectorAll('table,svg,canvas,iframe,input,select,img').length
}));"""


def _visible_message(driver):
    for element in driver.find_elements(By.CSS_SELECTOR, "#message_diag #message_text, #message_text"):
        try:
            if element.is_displayed() and element.text.strip():
                return element.text.strip()
        except StaleElementReferenceException:
            continue
    return ""


def frame_states(driver, wait_seconds=30):
    """[(src, location.href, element count)] of visible iframes that have a src; waits for their body."""
    driver.switch_to.default_content()
    states = []
    for frame in driver.find_elements(By.TAG_NAME, "iframe"):
        try:
            src = frame.get_attribute("src") or ""
            if not frame.is_displayed() or not src.startswith("http"):
                continue
        except StaleElementReferenceException:
            continue
        href, count = src, 0
        deadline = time.time() + wait_seconds
        while time.time() < deadline:
            try:
                driver.switch_to.frame(frame)
                href = driver.execute_script("return location.href;")
                count = driver.execute_script("return document.body ? document.body.querySelectorAll('*').length : 0;")
            except WebDriverException:
                pass
            finally:
                driver.switch_to.default_content()
            if count > 0 or href.startswith("chrome-error"):
                break
            time.sleep(2)
        states.append((src, href, count))
    return states


def check_page(driver, net, address_host, since=0):
    """Problems of the current page: cert warning, insecure/failed requests, blank content, error message, bad frames."""
    problems = []
    driver.switch_to.default_content()
    current = urlparse(driver.current_url)
    if current.scheme != "https" or current.hostname != address_host:
        problems.append(f"address bar is {driver.current_url}, expected https://{address_host}")
    if cert_warning_shown(driver):
        problems.append("certificate warning page shown")
    content = driver.execute_script(_CONTENT_JS)
    if not any(part["text"] or part["widgets"] for part in content):
        problems.append(f"blank content {content}")
    message = _visible_message(driver)
    if message:
        problems.append(f"message dialog: {message}")
    for src, href, count in frame_states(driver):
        if href.startswith("chrome-error"):
            problems.append(f"frame {src} shows browser error page")
        elif count == 0:
            problems.append(f"frame {src} is blank")
        if urlparse(href).hostname != address_host:
            problems.append(f"frame host {urlparse(href).hostname} != address bar host {address_host} ({href})")
    problems += [f"cert/insecure request: {f}" for f in net.cert_failures(address_host, since)]
    return problems


def open_dut_configuration(driver, dut_node_name, timeout=180):
    """Provision > Configuration, select the DUT and return the configuration frame URL once it has content."""
    driver.switch_to.default_content()
    _click_top_menu(driver, "Provision", timeout)
    _click_top_menu(driver, "Configuration", timeout)
    _select_configuration_device(driver, dut_node_name, timeout)

    def loaded(_):
        for src, href, count in frame_states(driver, wait_seconds=5):
            if count > 0 or href.startswith("chrome-error"):
                return href
        return False

    try:
        return WebDriverWait(driver, timeout, poll_frequency=3).until(loaded)
    except TimeoutException:
        raise AssertionError(f"Configuration frame of {dut_node_name} did not load within {timeout}s")
