import time
import random
from typing import List
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from modules.everytime.scripts.transform import selenium_error_transform
from modules.everytime.scripts.everytime_utils import navigate
from modules.everytime.scripts.everytime_utils import scroll_into_view
from modules.everytime.scripts.everytime_utils import initialize_articles
from modules.utiles.logging.logging_utils import GetLogger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from modules.everytime.scripts.exception import exception_handler
from modules.utiles.chromedriver.chrome_manager import ChromeDriverManager

logger = GetLogger()

def __create_art_list(articles: List[WebElement], comparison_str: str) -> List[str]:
    """Generates a list of article titles, stopping at the comparison string."""
    logger.info("Creating article list, stopping at: %s", comparison_str)

    art_list = []
    for article in articles:
        title = article.text.split('\n')[0]
        if comparison_str == title:
            break
        art_list.append(title)

    logger.info("Generated article list with %s articles", len(art_list))
    return art_list

def __return_title_of_article(article: WebElement) -> str:
    """Returns the title of the given article."""
    title = article.find_element(By.TAG_NAME, "h2").text
    logger.debug("Retrieved article title: %s", title)
    return title

def __Alert_click(browser: Chrome) -> None:
    """Handles potential alerts after clicking like button."""
    try:
        alert = Alert(browser)
        logger.info("Alert detected, accepting...")
        alert.accept()

        time.sleep(random.uniform(0.5, 1.5))
        alert.accept()
        time.sleep(random.uniform(0.5, 1.5))

    except:
        logger.warning("No alert found.")
        pass

    finally:
        logger.info("Returning to the previous page.")
        browser.back()
        time.sleep(random.uniform(0.5, 1.5))

def __like_button_click(browser: Chrome) -> None:
    """Clicks the like button and handles potential alerts."""
    try:
        like_button = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "posvote"))
        )
        scroll_into_view(browser, like_button)
        like_button.click()

        logger.info("Like button clicked.")
        __Alert_click(browser)
    except Exception as e:
        logger.error("Failed to click like button: %s", e)

def __handle_article_like(browser: Chrome, article: WebElement, realname, art_list: List) -> None:
    """Handles the liking of an individual article."""
    logger.info("Processing article: %s", realname)

    scroll_into_view(browser, article)
    article.click()
    wait_time = random.uniform(2, 5)
    logger.info("Clicked on article. Waiting for %s seconds before proceeding.", wait_time)
    time.sleep(wait_time)

    article_name = browser.find_element(By.XPATH, "//h2[@class='large']").text
    logger.info("Article click completed: <%s>", article_name)
    __like_button_click(browser)

    art_list.remove(realname)
    logger.info("Removed %s from article list. Remaining articles: %s", realname, len(art_list))

def __Auto_articles_like(browser: Chrome, art_list: List[str], changed_name: str = None) -> None:
    """Iterates through articles and likes them."""
    while art_list:
        articles = initialize_articles(browser)

        first_article = __return_title_of_article(articles[0])
        if changed_name == first_article:
            logger.info("First article unchanged, stopping auto-like.")
            break

        logger.debug(
            "[First Article]: %s, [Articles Count]: %s, [Art List Count]: %s",
            first_article, len(articles), len(art_list)
        )

        for article in reversed(articles):
            changed_name = __return_title_of_article(article)
            if changed_name in art_list:
                __handle_article_like(browser, article, changed_name, art_list)
                break  # 한 번 클릭하면 루프 종료

        if len(art_list) == 0:
            articles = initialize_articles(browser)
            art_list = __create_art_list(articles, changed_name)

def __like_articles(browser: Chrome, start_article: str, page_num: int) -> None:
    """Likes articles from the starting point, navigating pages if necessary."""
    logger.info("Starting auto-like from article: %s, across %s pages", start_article, page_num)

    for index in range(page_num):
        articles = initialize_articles(browser)
        art_list = __create_art_list(articles, start_article)

        logger.debug("[Art List]: %s", ', '.join(art_list))

        __Auto_articles_like(browser, art_list)

        remaining_pages = page_num - index
        logger.info("20 articles clicked successfully, remaining pages: %s", remaining_pages)

        navigate(browser, "prev")

@exception_handler(logger)
def StartAutoLike(manager: ChromeDriverManager, start_article: str, page_num: int) -> None:
    """Factory method: Initializes auto-liking process."""
    logger.info("Initializing auto-like process for article: %s with %s pages", start_article, page_num)
    return __like_articles(manager.browser, start_article, page_num)
