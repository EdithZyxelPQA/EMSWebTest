"""EMS1-7243 helpers: temporarily exhaust the EMS MySQL connections and check how EMS Web behaves.

These functions run read/stress commands on the EMS server over SSH (as the DB root). They occupy
MySQL connections with `select sleep(...)` sessions that end by themselves, and also release them
explicitly. Nothing changes max_connections or any EMS configuration.
"""
import shlex
import time

from selenium.webdriver.common.by import By

from libs.ems_cert import NetworkLog, create_cert_browser
from libs.ems_ui import login_ems
from libs.browser import close_browser

HOG_MARKER = "ems1_7243_hog"
# DB APIs that normally return data; an empty 200 body from these is the BUG-1 defect.
EMPTY_BODIES = ("[]", "{}", "")
MONITORED_APIS = ("getLatestHealth", "getAlarmStatus", "getActiveAlarmTypeCount")


def _mysql(db_user, db_pw):
    return f"MYSQL_PWD={shlex.quote(db_pw)} mysql -u{shlex.quote(db_user)}"


def db_threads_connected(shell, db_user, db_pw):
    """Current MySQL Threads_connected, or -1 when MySQL refuses the query (connections full)."""
    out = shell.run(f"{_mysql(db_user, db_pw)} -N -e \"show global status like 'Threads_connected'\" 2>/dev/null", check=False, quiet=True)
    parts = out.split()
    return int(parts[-1]) if parts and parts[-1].isdigit() else -1


def db_max_connections(shell, db_user, db_pw):
    out = shell.run(f"{_mysql(db_user, db_pw)} -N -e \"show variables like 'max_connections'\" 2>/dev/null", check=False, quiet=True)
    parts = out.split()
    return int(parts[-1]) if parts and parts[-1].isdigit() else 151


def connection_errors(shell, db_user, db_pw):
    out = shell.run(f"{_mysql(db_user, db_pw)} -N -e \"show global status like 'Connection_errors_max_connections'\" 2>/dev/null", check=False, quiet=True)
    parts = out.split()
    return int(parts[-1]) if parts and parts[-1].isdigit() else -1


def hold_db_connections(shell, db_user, db_pw, leave_free=2, seconds=180):
    """Open sleeping MySQL sessions so that only `leave_free` connections stay free. Returns the count opened.

    The sessions carry HOG_MARKER and end by themselves after `seconds`; release_db_connections ends them early.
    """
    limit = db_max_connections(shell, db_user, db_pw)
    cur = db_threads_connected(shell, db_user, db_pw)
    if cur < 0:
        cur = 2
    n = limit - cur - leave_free
    if n < 1:
        n = 1
    shell.run(
        f"for i in $(seq 1 {n}); do (MYSQL_PWD={shlex.quote(db_pw)} setsid mysql -u{shlex.quote(db_user)} "
        f"-e 'select sleep({seconds}) /*{HOG_MARKER}*/' </dev/null >/dev/null 2>&1 &); done; sleep 3",
        check=False, quiet=True,
    )
    return n


def release_db_connections(shell, db_user, db_pw):
    """Stop the hog client processes and KILL any remaining hog sessions in MySQL."""
    pfx = _mysql(db_user, db_pw)
    shell.run(
        f"pkill -f '{HOG_MARKER}' 2>/dev/null; "
        f"for id in $({pfx} -N -e \"select id from information_schema.processlist "
        f"where info like '%{HOG_MARKER}%' and info not like '%information_schema%'\" 2>/dev/null); "
        f"do {pfx} -e \"KILL $id\" 2>/dev/null; done; true",
        check=False, quiet=True,
    )
    time.sleep(3)


def hog_processes_left(shell):
    # Count only mysql client processes (command line starts with "mysql"); anchoring avoids matching
    # the shell that runs this grep, whose own command line also contains the marker text.
    out = shell.run(f"ps -eo args | grep -c '^mysql .*{HOG_MARKER}' || echo 0", check=False, quiet=True)
    try:
        return int(out.strip().splitlines()[-1])
    except (ValueError, IndexError):
        return -1


def open_logged_in_browser(browser_name, download_path, ems_url, username, password, wait_time):
    """A Chrome/Edge browser (certificate errors ignored) logged in to EMS, with a NetworkLog attached."""
    driver = create_cert_browser(browser_name, download_path, ignore_cert_errors=True)
    driver.implicitly_wait(wait_time)
    driver.maximize_window()
    net = NetworkLog(driver)
    driver.get(ems_url)
    login_ems(driver, username, password)
    time.sleep(5)
    return driver, net


def collect_db_api_results(driver, net, since):
    """Return the EMS DB-API responses seen since `since`: [{name, status, empty, body_len}].

    `empty` is True when a monitored API returns HTTP 200 with an empty JSON body (the BUG-1 defect).
    Requires a Chrome/Edge driver (uses CDP Network.getResponseBody).
    """
    net.drain()
    results = []
    for message in net.events[since:]:
        if message["method"] != "Network.responseReceived":
            continue
        response = message["params"]["response"]
        url = response.get("url", "")
        if "/netatlasems/DB/" not in url:
            continue
        name = url.split("?")[0].rstrip("/").split("/")[-1]
        try:
            body = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": message["params"]["requestId"]}).get("body", "")
        except Exception:
            body = None
        empty = (
            name in MONITORED_APIS
            and response.get("status") == 200
            and body is not None
            and body.strip() in EMPTY_BODIES
        )
        results.append({"name": name, "status": response.get("status"), "empty": empty, "body_len": len(body) if body else 0})
    return results


def latest_health_value(results):
    """The y value reported by getLatestHealth in a result list, or None."""
    for r in reversed(results):
        if r["name"] == "getLatestHealth" and r["status"] == 200 and r["body_len"] > 2:
            return True
    return False


def open_dashboard_and_collect(driver, net):
    """Click Dashboard, wait, and return the DB-API results for that load."""
    since = net.mark()
    driver.switch_to.default_content()
    driver.find_element(By.CSS_SELECTOR, "#i_menu_dashboard > a").click()
    time.sleep(12)
    return collect_db_api_results(driver, net, since)


def open_alarm_and_collect(driver, net):
    """Click Alarm, wait, and return the DB-API results for that load."""
    since = net.mark()
    driver.switch_to.default_content()
    driver.find_element(By.CSS_SELECTOR, "#i_menu_alarm > a").click()
    time.sleep(12)
    return collect_db_api_results(driver, net, since)


# ---------------------------------------------------------------------------
# EMS1-7244 helpers: read-only observation of DB connection stability (BUG-2).
# These add no load and change nothing on the server.
# ---------------------------------------------------------------------------
EMS_HOME = "/opt/ELEMENTVIEW_MASTER"
WEB_CLASSES = f"{EMS_HOME}/bin/apache-tomcat/webapps/netatlasems/WEB-INF/classes/com/zyxel/netatlasems/web"
POOL_LIB_PATTERN = "bonecp|hikari|c3p0|dbcp|druid|tomcat-jdbc"


def sample_connection_churn(shell, db_user, db_pw, seconds=60):
    """Return connection churn over `seconds`: new connections/sec vs. concurrent Threads_connected.

    A low rate with stable Threads_connected means connections are reused (pool). A high rate (tens/sec)
    while only a few are concurrent means a new connection is opened per query (no pool).
    """
    m = _mysql(db_user, db_pw) + " -N"  # -N: value only, no column header
    conn_q = "select variable_value from performance_schema.global_status where variable_name='Connections'"
    c0 = shell.run(f'{m} -e "{conn_q}" 2>/dev/null', check=False, quiet=True).strip()
    loop = (
        f'for i in $(seq 1 {seconds}); do '
        f'{m} -e "select variable_value from performance_schema.global_status where variable_name=\'Threads_connected\'" 2>/dev/null; '
        'sleep 1; done'
    )
    sampled = shell.run(loop, timeout=seconds + 60, check=False, quiet=True)
    c1 = shell.run(f'{m} -e "{conn_q}" 2>/dev/null', check=False, quiet=True).strip()
    tcs = [int(x) for x in sampled.split() if x.isdigit()]
    new_total = int(c1) - int(c0) if c0.isdigit() and c1.isdigit() else -1
    return {
        "new_per_sec": round(new_total / seconds, 1) if new_total >= 0 else -1,
        "threads_max": max(tcs) if tcs else -1,
        "threads_avg": sum(tcs) // len(tcs) if tcs else -1,
        "max_connections": db_max_connections(shell, db_user, db_pw),
    }


def pool_evidence(shell):
    """Whether a DB connection pool is installed/used (read-only)."""
    jars = shell.run(f"ls {EMS_HOME}/lib 2>/dev/null | grep -iE '{POOL_LIB_PATTERN}' || true", check=False, quiet=True).split()
    cm = shell.run(f"strings -n 5 {WEB_CLASSES}/common/ConnectionManager.class 2>/dev/null | grep -iE 'DataSource|DriverManager|pool' | sort -u", check=False, quiet=True)
    provider = shell.run(f"grep -E 'provider_class' {EMS_HOME}/conf/hibernate.cfg.xml 2>/dev/null | grep -v '<!--' || true", check=False, quiet=True).strip()
    return {
        "pool_jars": jars,
        "connmgr_uses_driver_manager": "DriverManager" in cm,
        "connmgr_uses_datasource": "DataSource" in cm,
        "hibernate_pool_provider_active": bool(provider),
    }


def count_log_occurrences(shell):
    """Current count of 'Too many connections' and alarm 'save to db fail' lines in the service logs."""
    logs = f"{EMS_HOME}/logs"
    too_many = shell.run(f"grep -h 'Too many connections' {logs}/*.log 2>/dev/null | wc -l", check=False, quiet=True).strip()
    save_fail = shell.run(f"grep -h 'save to db fail' {logs}/alarmServer.log 2>/dev/null | wc -l", check=False, quiet=True).strip()
    return int(too_many or 0), int(save_fail or 0)


def monitor_peak_and_errors(shell, db_user, db_pw, seconds, interval=5):
    """Over `seconds`, return the peak Threads_connected seen."""
    m = _mysql(db_user, db_pw) + " -N"
    steps = max(1, seconds // interval)
    loop = (
        f'for i in $(seq 1 {steps}); do '
        f'{m} -e "select variable_value from performance_schema.global_status where variable_name=\'Threads_connected\'" 2>/dev/null; '
        f'sleep {interval}; done'
    )
    sampled = shell.run(loop, timeout=seconds + 60, check=False, quiet=True)
    tcs = [int(x) for x in sampled.split() if x.isdigit()]
    return max(tcs) if tcs else -1
