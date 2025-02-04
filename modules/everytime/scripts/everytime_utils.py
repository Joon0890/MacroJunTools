import time, random
from enum import Enum
from typing import Optional
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement   
from modules.utiles.logging.logging_utils import GetLogger

logger = GetLogger()

class ScrollBehavior(Enum):
    AUTO = "arguments[0].scrollIntoView({ behavior: 'auto', block: 'center', inline: 'center' });"
    SMOOTH = "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });"
    END = "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'end' });"

def initialize_articles(browser: Chrome):
    return browser.find_elements(By.XPATH, "//article[@class='list']")

def navigate(
    browser: Chrome, 
    direction: str, 
    wait_time: Optional[int] = None
) -> None:
    """Navigates to the next or previous page."""
    if wait_time is None:  # 호출될 때마다 새로운 랜덤 값 설정
        wait_time = random.uniform(1, 2)

    if direction not in {"prev", "next"}:
        logger.error("Invalid direction '%s'. Expected 'prev' or 'next'.", direction)
        raise ValueError(f"Invalid direction '{direction}'. Expected 'prev' or 'next'.")

    pagination = browser.find_element(By.CLASS_NAME, "pagination")
    button = pagination.find_element(By.CLASS_NAME, direction)
    scroll_into_view(browser, button)
    button.click()
    time.sleep(wait_time)
    
def scroll_into_view(
    browser: Chrome, 
    element: WebElement,
    scroll_script: str = ScrollBehavior.AUTO.value,  
    wait_time: Optional[int] = None
) -> None:
    """Scrolls the browser to bring the element into view."""
    if wait_time is None:  # 호출될 때마다 새로운 랜덤 값 설정
        wait_time = random.uniform(1, 2)
    
    browser.execute_script(scroll_script, element)
    time.sleep(wait_time)