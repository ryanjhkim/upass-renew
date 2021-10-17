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


def get_headless_chrome_opts():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    return chrome_options


def init_driver_headless():
    chrome_options = get_headless_chrome_opts()
    driver = webdriver.Chrome(options=chrome_options)
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


def restart_driver(driver):
    driver.quit()
    time.sleep(10)
    return init_driver_headless()


def request_upass(driver):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "chk_1"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "requestButton"))).click()


if __name__ == '__main__':
    users = load_yaml()
    headless_chrome = init_driver_headless()
    for user in users:
        username = users[user]['USERNAME']
        password = users[user]['PASSWORD']
        upass_select_school(headless_chrome)
        login_ubc(headless_chrome, username, password)
        time.sleep(30)
        request_upass(headless_chrome)
        print(f"Successfully requested U-Pass for {username}")
        headless_chrome = restart_driver(headless_chrome)

