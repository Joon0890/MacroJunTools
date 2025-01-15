from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from MacroJun.Utiles.utiles.chrome import scroll_into_view

def initialize_articles(browser: webdriver.Chrome):
    """Retrieves the list of articles on the current page."""
    return browser.find_elements(By.XPATH, "//article[@class='list']")

def navigate(browser: webdriver.Chrome, direction):
    """Navigates to the next or previous page."""
    button = browser.find_element(By.LINK_TEXT, direction)
    scroll_into_view(browser, button)
    button.click(); sleep(1)



