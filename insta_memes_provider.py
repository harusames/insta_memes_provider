import os
from time import sleep

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


load_dotenv(os.environ.get("SECRETS_FILE"))
driver = webdriver.Chrome()
driver.get("https://www.instagram.com/")

decline_cookies_button = WebDriverWait(driver, 10).until(
    ec.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Decline optional cookies')]"))
)
decline_cookies_button.click()

username_input = WebDriverWait(driver, 10).until(
    ec.presence_of_element_located((By.NAME, "username"))
)
username_input.send_keys(os.environ.get("INSTAGRAM_USERNAME"))

password_input = WebDriverWait(driver, 10).until(
    ec.presence_of_element_located((By.NAME, "password"))
)
password_input.send_keys(os.environ.get("INSTAGRAM_PASSWORD"))

sleep(1)
login_button = WebDriverWait(driver, 10).until(
    ec.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Log in')]"))
)
# test with: document.evaluate(`//*[contains(text(), 'Log in')]`, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue

login_button.click()

WebDriverWait(driver, 10).until(
    ec.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Save Your Login Info?')]"))
)

driver.get(f"https://www.instagram.com/direct/t/{os.environ.get('INSTAGRAM_INSTA_MEMES_PROVIDER_DM_TARGET_ID')}/")

turn_on_notification_not_now_button = WebDriverWait(driver, 10).until(
    ec.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Not Now')]"))
)
turn_on_notification_not_now_button.click()

WebDriverWait(driver, 10).until(
    ec.presence_of_element_located((By.XPATH, f"//*[@aria-label='Messages in conversation with {os.environ.get('INSTAGRAM_INSTA_MEMES_PROVIDER_DM_TARGET_NAME')}']"))
)
anchors_with_preview_area_label = driver.find_elements(By.XPATH, "//a[@aria-label='Preview']")

# TODO:
#  from anchor to like button
#  if post is liked then stop, else:
#  save link to file + replace "reel" with "p" in link + download post
#   get link: ?
#  like post
#  get next post (if none left. then scrollIntoView() on the last one)
print()
