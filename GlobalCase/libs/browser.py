from selenium import webdriver


def create_browser(browser_name, download_path, incognito=False):
    browser = browser_name.lower()

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("ignore-certificate-errors")
        if incognito:
            options.add_argument("--incognito")
        options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": download_path,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
            },
        )
        return webdriver.Chrome(options=options)

    if browser == "edge":
        options = webdriver.EdgeOptions()
        options.add_argument("ignore-certificate-errors")
        if incognito:
            options.add_argument("--inprivate")
        options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": download_path,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
            },
        )
        return webdriver.Edge(options=options)

    if browser == "firefox":
        options = webdriver.FirefoxOptions()
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.dir", download_path)
        if incognito:
            options.set_preference("browser.privatebrowsing.autostart", True)
        return webdriver.Firefox(options=options)

    raise ValueError(f"Unsupported browser: {browser_name}")


def close_browser(driver):
    if not driver:
        return

    try:
        for handle in list(driver.window_handles):
            try:
                driver.switch_to.window(handle)
                driver.close()
            except Exception:
                pass
    except Exception:
        pass

    try:
        driver.quit()
    except Exception:
        pass

    try:
        process = getattr(getattr(driver, "service", None), "process", None)
        if process and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except Exception:
                process.kill()
    except Exception:
        pass
