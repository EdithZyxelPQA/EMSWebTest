from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def login_ems(driver, username, password):
    user_field = driver.find_element(By.ID, "name")
    user_field.clear()
    user_field.send_keys(username)
    password_field = driver.find_element(By.ID, "passwd")
    password_field.clear()
    password_field.send_keys(password)
    driver.find_element(By.ID, "signin").click()
    WebDriverWait(driver, 180).until(EC.visibility_of_element_located((By.ID, "index_t_userName")))


def logout_ems(driver):
    driver.find_element(By.ID, "index_t_userName").click()
    driver.find_element(By.ID, "index_sign_off").click()
