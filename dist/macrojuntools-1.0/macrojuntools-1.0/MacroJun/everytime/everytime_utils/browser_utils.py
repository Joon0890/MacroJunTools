import time, random
from selenium import webdriver
from selenium.webdriver.common.by import By
from MacroJun.utiles.scripts.log_csv import LogManager
from MacroJun.utiles.scripts.transform import selenium_error_transform 

log = LogManager()

def initialize_articles(browser: webdriver.Chrome):
    """Retrieves the list of articles on the current page."""
    return browser.find_elements(By.XPATH, "//article[@class='list']")

def navigate(browser: webdriver.Chrome, direction):
    """Navigates to the next or previous page."""
    global log

    try:
        pagination = browser.find_element(By.XPATH, "//div[@class='pagination']")
        button = pagination.find_element(By.CLASS_NAME, direction)
        scroll_into_view(browser, button)
        button.click()
        time.sleep(random.uniform(1, 2))

    except Exception as e:
        log.log_error("navigate", "Error while navigating", selenium_error_transform(e))

def scroll_into_view(browser: webdriver.Chrome, element):
    """Scrolls the browser to bring the element into view."""
    SCROLL_SCRIPT = "arguments[0].scrollIntoView({ behavior: 'auto', block: 'center', inline: 'center' });"
    browser.execute_script(SCROLL_SCRIPT, element)
    time.sleep(random.uniform(1, 2))