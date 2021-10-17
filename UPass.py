from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import yaml

SCHOOL_SELECT_ID = "PsiId"
SCHOOL_SELECT_SUBMIT_ID = "goButton"


def load_yaml():
    with open("config.yaml", "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def init_driver():
    driver = webdriver.Chrome()
    return driver


def upass_select_school(driver):
    driver.get('https://upassbc.translink.ca/')
    school_selector = Select(driver.find_element_by_id(SCHOOL_SELECT_ID))
    school_selector.select_by_index(9)

    go_btn = driver.find_element_by_id(SCHOOL_SELECT_SUBMIT_ID)
    go_btn.submit()


def login_ubc(driver, username, password):
    _username = driver.find_element_by_id("username")
    _password = driver.find_element_by_id("password")

    _username.send_keys(username)
    _password.send_keys(password)

    login_btn = driver.find_element_by_name("_eventId_proceed")
    login_btn.click()


def restart_driver():
    time.sleep(10)
    return init_driver()


def request_upass(driver):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "chk_1"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "requestButton"))).click()


if __name__ == '__main__':
    users = load_yaml()
    driver = init_driver()

    for user in users:
        username = user['USERNAME']
        password = user['PASSWORD']
        upass_select_school(driver)
        login_ubc(driver, username, password)
        request_upass(driver)
        driver = restart_driver()

