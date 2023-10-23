import os
from time import sleep

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from lib import read_file


def prepare():
    _driver = webdriver.Chrome()
    load_dotenv(os.environ.get("SECRETS_FILE"))
    _driver.get("https://www.instagram.com/")

    decline_cookies_button = WebDriverWait(_driver, 10).until(
        ec.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Decline optional cookies')]"))
    )
    decline_cookies_button.click()

    username_input = WebDriverWait(_driver, 10).until(
        ec.presence_of_element_located((By.NAME, "username"))
    )
    username_input.send_keys(os.environ.get("INSTAGRAM_USERNAME"))

    password_input = WebDriverWait(_driver, 10).until(
        ec.presence_of_element_located((By.NAME, "password"))
    )
    password_input.send_keys(os.environ.get("INSTAGRAM_PASSWORD"))

    sleep(1)
    login_button = WebDriverWait(_driver, 10).until(
        ec.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Log in')]"))
    )
    # test with: document.evaluate(`//*[contains(text(), 'Log in')]`, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue

    login_button.click()

    WebDriverWait(_driver, 10).until(
        ec.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Save Your Login Info?')]"))
    )

    _driver.get(f"https://www.instagram.com/direct/t/{os.environ.get('INSTAGRAM_INSTA_MEMES_PROVIDER_DM_TARGET_ID')}/")

    turn_on_notification_not_now_button = WebDriverWait(_driver, 10).until(
        ec.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Not Now')]"))
    )
    turn_on_notification_not_now_button.click()

    WebDriverWait(_driver, 10).until(
        # ec.presence_of_element_located((By.XPATH, f"//div[@aria-label='Messages in conversation with {os.environ.get('INSTAGRAM_INSTA_MEMES_PROVIDER_DM_TARGET_NAME')}']"))
        ec.presence_of_element_located((By.XPATH, "//div[contains(@aria-label, 'Messages in conversation with')]"))
    )

    return _driver


script = read_file(os.path.join(os.path.dirname(__file__), "insta_memes_provider.js"))
driver = prepare()
driver.set_script_timeout(5 * 60)

response = driver.execute_script(f"{script} return response;")
# TODO: save links_as_text, logs, errors
# TODO: call downloader with links_as_text

print()
