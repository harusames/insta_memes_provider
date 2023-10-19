import os
from time import sleep

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


driver = webdriver.Chrome()

find_scrollbar = """
function findScrollableDescendant(element) {
    if (element) {
        const styles = window.getComputedStyle(element);
        if (styles.getPropertyValue('overflow-y') === 'scroll') {
            return element;
        }

        for (let i = 0; i < element.children.length; i++) {
            const childResult = findScrollableDescendant(element.children[i]);
            if (childResult) {
                return childResult;
            }
        }
    }

    return null;
}
const xpath = `//div[contains(@aria-label, 'Messages in conversation with')]`;
const parent = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
return findScrollableDescendant(parent)"""
scroll_size = 500


def prepare():
    load_dotenv(os.environ.get("SECRETS_FILE"))
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
        # ec.presence_of_element_located((By.XPATH, f"//div[@aria-label='Messages in conversation with {os.environ.get('INSTAGRAM_INSTA_MEMES_PROVIDER_DM_TARGET_NAME')}']"))
        ec.presence_of_element_located((By.XPATH, "//div[contains(@aria-label, 'Messages in conversation with')]"))
    )


links = []


prepare()

anchors = lambda: driver.find_elements(By.XPATH, "//a[@aria-label='Preview']")
anchors_size = lambda: len(anchors())

latest_post_reverse_index = 1
while latest_post_reverse_index <= anchors_size():
    print(f"latest_post_reverse_index: {latest_post_reverse_index}")
    # TODO: change this to javascript and provide index as arguments[0] because current trials at index 2
    anchor = lambda: anchors()[-latest_post_reverse_index]
    # ancestor = lambda: anchor().find_element(By.XPATH, './ancestor::div[@role="button" and @aria-label="Double tap to like"]')
    # descendant = lambda: next(iter(ancestor().find_elements(By.XPATH, './/span[contains(text(), "❤️")]')), None)

    # anchor_v = anchor()
    # ancestor_v = anchor_v.find_element(By.XPATH, './ancestor::div[@role="button" and @aria-label="Double tap to like"]')
    # descendant_v = next(iter(ancestor_v.find_elements(By.XPATH, './/span[contains(text(), "❤️")]')), None)

    # if descendant():
    # if next(iter(anchors()[-latest_post_reverse_index].find_elements(By.XPATH, './ancestor::div[@role="button" and @aria-label="Double tap to like"]/.//span[contains(text(), "❤️")]')), None):
    # if descendant_v:
    if next(iter(driver.find_elements(By.XPATH, "//a[@aria-label='Preview']")[-latest_post_reverse_index].find_element(By.XPATH, './ancestor::div[@role="button" and @aria-label="Double tap to like"]').find_elements(By.XPATH, './/span[contains(text(), "❤️")]')), None):
        break
    else:
        latest_post_reverse_index += 1
        driver.execute_script("arguments[0].scrollIntoView();", anchors()[0])
        driver.execute_script(f"{find_scrollbar}.scrollTop -= {1000}")
        # driver.find_element_by_xpath('//div[@aria-label="abc"]//*[contains(@style, "overflow-y: scroll")]')
        # driver.find_element_by_xpath('//div[@aria-label="Messages in conversation with {os.environ.get('INSTAGRAM_INSTA_MEMES_PROVIDER_DM_TARGET_NAME')}"]//*[contains(@style, "overflow-y: scroll")]')
        # driver.find_element_by_xpath(f'//div[@aria-label="Messages in conversation with {os.environ.get("INSTAGRAM_INSTA_MEMES_PROVIDER_DM_TARGET_NAME")}"]//*[contains(@style, "overflow-y: scroll")]')
        # driver.find_elements(By.XPATH, f'//div[@aria-label="Messages in conversation with {os.environ.get("INSTAGRAM_INSTA_MEMES_PROVIDER_DM_TARGET_NAME")}"]//*[contains(@style, "overflow-y: scroll")]') # returns 0
        # driver.find_elements(By.XPATH, f'//div[@aria-label="Messages in conversation with {os.environ.get("INSTAGRAM_INSTA_MEMES_PROVIDER_DM_TARGET_NAME")}"]') # works
        # driver.find_elements(By.XPATH, "//div[contains(@style, 'height')]")[0] # works

        # document.evaluate("//div[contains(@aria-label, 'Messages in conversation with')]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue

        # document.evaluate(`//div[contains(@aria-label, 'Messages in conversation with')]`, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue # works
        # driver.execute_script("document.evaluate(`//div[contains(@aria-label, 'Messages in conversation with')]`, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue")

        # driver.execute_script("return document.evaluate(`//div[contains(@aria-label, 'Messages in conversation with')]`, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue")
        driver.implicitly_wait(1)



while True:
    anchors_with_preview_area_label = driver.find_elements(By.XPATH, "//a[@aria-label='Preview']")
    for anchor in anchors_with_preview_area_label:
        ancestor_button = anchor.find_element(By.XPATH, './ancestor::div[@role="button" and @aria-label="Double tap to like"]')
        try:
            descendant_span = ancestor_button.find_element(By.XPATH, './/span[contains(text(), "❤️")]')
            print("found 1st liked")
        except NoSuchElementException:
            # ancestor_button.click()
            sleep(1)
        # driver.execute_script("arguments[0].scrollIntoView();", anchors_with_preview_area_label[0])
        # list(map(lambda e: e.get_attribute('href'), driver.find_elements(By.XPATH, "//a[@aria-label='Preview']")))
        # driver.find_elements(By.XPATH, "//a[@aria-label='Preview']")[0].find_element(By.XPATH, './ancestor::div[@role="button" and @aria-label="Double tap to like"]').find_element(By.XPATH, './/span[contains(text(), "❤️")]')
        # links.append(anchor.get_attribute("href"))
    driver.execute_script("arguments[0].scrollIntoView();", anchors_with_preview_area_label[0])
    driver.implicitly_wait(1)
    # sleep(1)


anchors_with_preview_area_label = driver.find_elements(By.XPATH, "//a[@aria-label='Preview']")

# like: span that contains ❤️
# common parent: div with role button with ari-label="Double tap to like"

# TODO:
#  from anchor to like button
#  if post is liked then stop, else:
#  save link to file + replace "reel" with "p" in link + download post
#   get link: ?
#  like post
#  get next post (if none left. then scrollIntoView() on the last one)
print()
