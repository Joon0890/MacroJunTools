from typing import Optional
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from modules.utiles.logging.logging_utils import GetLogger
from modules.everytime.scripts.exception import exception_handler
from modules.utiles.chromedriver.chrome_manager import ChromeDriverManager

logger = GetLogger()

@exception_handler(logger)
def login_everytime(
    manager: ChromeDriverManager, 
    my_id: Optional[str], 
    my_password: Optional[str]
) -> Optional[bool]:
    """Logs in to the website."""

    if not my_id or not my_password:
        logger.error("Everytime ID and Password are None")
        raise ValueError("Everytime credentials are missing")

    logger.info("Attempting to log in with ID: %s", my_id)

    logger.info("current url: %s", manager.browser.current_url)

    logger.info("page source: %s", manager.browser.page_source)

    try:
        if manager.browser.find_element(By.ID, "submenu"):
            logger.info("Already logged in, skipping login process.")
            return False
    except NoSuchElementException:
        logger.info("Not logged in, proceeding with login.")

    try:
        signin_button = manager.browser.find_element(By.CLASS_NAME, "signin")
        logger.info("Sign-in button found, clicking...")
        signin_button.click()
    except NoSuchElementException:
        logger.warning("Sign-in button not found, skipping...")

    logger.info("Locating login form...")
    login_form = manager.browser.find_element(By.TAG_NAME, "form")

    id_elem = login_form.find_element(By.NAME, "id")
    password_elem = login_form.find_element(By.NAME, "password")
    keep_checkbox = login_form.find_element(By.CLASS_NAME, "keep")

    logger.info("Entering credentials...")
    id_elem.send_keys(my_id)
    password_elem.send_keys(my_password)

    logger.info("Checking 'Keep me logged in' checkbox...")
    keep_checkbox.click()

    logger.info("Submitting login form...")
    password_elem.send_keys(Keys.ENTER)

    sleep_time = random.uniform(2, 5)
    logger.info("Waiting for %s seconds after login attempt...", sleep_time)
    time.sleep(sleep_time)

    logger.info("Login process completed successfully.")
    return True


    
    
    

