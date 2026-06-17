from selenium.webdriver.common.by import By


def login_ems(driver, username, password):
    driver.find_element(By.ID, "login_username").send_keys(username)
    driver.find_element(By.ID, "login_password").send_keys(password)
    driver.find_element(By.ID, "login_button").click()


def logout_ems(driver):
    driver.find_element(By.ID, "index_t_userName").click()
    driver.find_element(By.ID, "index_logout").click()

