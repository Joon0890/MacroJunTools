import time
import random
from typing import Optional
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait as WW
from selenium.webdriver.support import expected_conditions as EC
from core.everytime.exception import exception_handler
from core.utils.custom_logging import CustomLogging

@exception_handler
def login_everytime(
    browser: Chrome, 
    logger: CustomLogging,
    my_id: Optional[str], 
    my_password: Optional[str],
    wait_time: Optional[int] = None
) -> Optional[bool]:
    """Logs in to the website."""
    
    if wait_time is None:  # 호출될 때마다 새로운 랜덤 값 설정
        wait_time = random.uniform(2, 5)

    if not my_id or not my_password:
        logger.error("Everytime ID and Password are None")
        raise ValueError("Everytime credentials are missing")

    print("Attempting to log in with ID: %s", my_id)

    try:
        if browser.find_element(By.CSS_SELECTOR, "div#submenu"):
            print("Already logged in, skipping login process.")
            return False
    except NoSuchElementException:
        print("Not logged in, proceeding with login.")

    try:
        signin_button = WW(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.signin")))
        signin_button.click()
        print("Sign-in button found, clicking...")
    except NoSuchElementException:
        print("Sign-in button not found, skipping...")

    print("Locating login form...")
    login_form = WW(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "form[method='post']")))

    id_elem = login_form.find_element(By.NAME, "id")
    password_elem = login_form.find_element(By.NAME, "password")
    keep_checkbox = login_form.find_element(By.CLASS_NAME, "keep")

    id_elem.send_keys(my_id)
    password_elem.send_keys(my_password)
    keep_checkbox.click()
    password_elem.send_keys(Keys.ENTER)

    print("Login process completed successfully.")
    return True


    
    
    

