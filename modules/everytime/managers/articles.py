import re
import time, random
from selenium.webdriver.common.by import By
from modules.everytime.utiles.transform import selenium_error_transform
from modules.everytime.utiles.everytime_utils import navigate
from modules.everytime.utiles.everytime_utils import scroll_into_view
from modules.everytime.utiles.everytime_utils import initialize_articles

def __return_comtext_instance(context):
    browser = context.browser
    log_manager = context.log_manager
    return browser, log_manager

def move_to_board(context, board_name):
    """Navigates to the specified article board."""
    browser, log_manager = __return_comtext_instance(context)
    try:
        group_lis = browser.find_element(By.XPATH, "//div[@id='submenu']").find_elements(By.TAG_NAME, "li")
        for li in group_lis:
            a_tag = li.find_element(By.TAG_NAME, "a")
            if a_tag.text == board_name:
                a_tag.click()
                time.sleep(random.uniform(2, 5))
                return
    except Exception as e:
        log_manager.log_error("move_to_board", "Error while navigating the board", selenium_error_transform(e))

def process_articles(context):
    """
    find_first_article와 find_article_for_click을 한 번에 처리하는 함수
    """
    start_article = __find_first_article(context)
    return __find_article_for_click(context, start_article)

def __find_first_article(context) -> str:
    """Finds the starting article for automation."""
    _, log_manager = __return_comtext_instance(context)
    try:
        rows = log_manager.read_log()
        for row in reversed(rows):
            if len(row) > 2:
                match = re.search(r"^<(.*?)>$", row[4])
                if match:
                    start_article = match.group(1)
                    print(f"[First Article]: {start_article}")
                    log_manager.log_info(
                        "find_first_article", 
                        "Found the starting point for likes in the CSV file.", 
                        f"<{start_article}>"
                        )
                    return start_article
    except Exception:
        log_manager.log_error("find_first_article", "Error while finding the first article")
        return None
    
def __find_article_for_click(context, start_article, page_num=1):
    """Finds the article to start liking from."""
    browser, log_manager = __return_comtext_instance(context)
    try:
        if start_article is not None:
            found = False
            while not found:
                articles = initialize_articles(browser)
                for index, article in enumerate(articles):
                    scroll_into_view(browser, article)
                    if start_article in article.text:
                        found = True
                        art_index = index
                        break

                if found or page_num >= 10:
                    break

                page_num += 1
                navigate(browser, "next")
        else:
            page_num = 3
            for k in range(page_num - 1):
                navigate(browser, "next")
    
    except KeyboardInterrupt:
        raise

    except Exception as e:
        log_manager.log_error("find_article_for_click", "Error while finding the first article for click", selenium_error_transform(e))
        raise

    else: 
        log_manager.log_info("find_article_for_click", "Initial article navigation completed for clicking")
        return start_article, page_num
