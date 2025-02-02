import re
import time
import random
from functools import wraps
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from modules.everytime.scripts.transform import selenium_error_transform
from modules.everytime.scripts.everytime_utils import navigate
from modules.everytime.scripts.everytime_utils import scroll_into_view
from modules.everytime.scripts.everytime_utils import initialize_articles
from modules.utiles.logging.logger import read_logs
from modules.utiles.logging.logging_utils import GetLogger
from modules.everytime.scripts.exception import exception_handler
from modules.utiles.chromedriver.chrome_manager import ChromeDriverManager

logger = GetLogger()

@exception_handler(logger)
def move_to_board(manager: ChromeDriverManager, board_name: str) -> None:
    """Navigates to the specified article board."""

    logger.info("Navigating to board: %s", board_name)

    try:
        submenu = manager.browser.find_element(By.ID, "submenu")
        a_tags = submenu.find_elements(By.TAG_NAME, "a")
        
        for a_tag in a_tags:
            if a_tag.text == board_name:
                logger.info("Board '%s' found, clicking...", board_name)
                a_tag.click()
                wait_time = random.uniform(2, 5)
                logger.info("Waiting for %s seconds after navigation...", wait_time)
                time.sleep(wait_time)
                return
        
        logger.warning("Board '%s' not found!", board_name)

    except Exception as e:
        logger.error("Error navigating to board '%s': %s", board_name, selenium_error_transform(e))


def __find_first_article(filename, encoding="utf-8", num_lines=None) -> str:
    """Finds the starting article for automation."""

    logger.info("Reading logs to find the starting article...")

    try:
        strLogs: str = read_logs(filename, encoding, num_lines)
        if not strLogs:
            logger.error("Log file is empty or missing.")
            return None
        
        for row in reversed(strLogs.split("\n")):
            match = re.search(r"Article click completed: <([^<>]+)>", row)
            if match:
                start_article = match.group(1)
                logger.info("Found the starting point for likes in logs: %s", start_article)
                return start_article

        logger.warning("No matching articles found in logs.")
            
    except Exception as e:
        logger.error("Error while finding the first article: %s", e)
    
    return None


def __find_article_for_click(browser: Chrome, start_article: str, page_num: int = 3) -> tuple[str, int]:
    """Finds the article to start liking from."""

    logger.info("Searching for starting article: %s", start_article)

    if start_article is not None:
        found = False

        while not found:
            articles = initialize_articles(browser)
            for article in articles:
                scroll_into_view(browser, article)
                if start_article in article.text:
                    logger.info("Found matching article: %s", start_article)
                    found = True
                    break

            if found or page_num >= 10:
                break

            page_num += 1
            logger.info("Moving to page %s...", page_num)
            navigate(browser, "next")

    else:
        logger.info("No starting article found, navigating %s pages forward...", page_num - 1)
        for _ in range(page_num - 1):
            navigate(browser, "next")

    return start_article, page_num


@exception_handler(logger)
def find_starting_point(manager: ChromeDriverManager, filename, encoding="utf-8", num_lines=None) -> "__find_article_for_click":
    """
    Combines find_first_article and find_article_for_click into a single function.
    """

    logger.info("Finding the starting point for auto-liking articles...")

    start_article = __find_first_article(filename, encoding, num_lines)
    if start_article:
        logger.info("Starting article found: %s", start_article)
    else:
        logger.warning("No starting article found, starting from the first available page.")

    return __find_article_for_click(manager.browser, start_article)
