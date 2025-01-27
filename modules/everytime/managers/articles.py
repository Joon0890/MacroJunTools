import re
import time, random
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from modules.everytime.utiles.log_manager import read_logs
from modules.everytime.utiles.log_manager import CustomLogging
from modules.everytime.utiles.context import return_comtext_instance
from modules.everytime.utiles.transform import selenium_error_transform
from modules.everytime.utiles.everytime_utils import navigate
from modules.everytime.utiles.everytime_utils import scroll_into_view
from modules.everytime.utiles.everytime_utils import initialize_articles

def move_to_board(context, board_name):
    """Navigates to the specified article board."""
    browser, logger = return_comtext_instance(context)
    try:
        group_lis = browser.find_element(By.XPATH, "//div[@id='submenu']").find_elements(By.TAG_NAME, "li")
        for li in group_lis:
            a_tag = li.find_element(By.TAG_NAME, "a")
            if a_tag.text == board_name:
                a_tag.click()
                time.sleep(random.uniform(2, 5))
                return
    except Exception as e:
        logger.error(f"Error while navigating the board: {selenium_error_transform(e)}") 

def process_articles(context):
    """
    find_first_article와 find_article_for_click을 한 번에 처리하는 함수
    """
    start_article = __find_first_article(context)
    return __find_article_for_click(context, start_article)

def __find_first_article(context) -> str:
    """Finds the starting article for automation."""
    _, logger = return_comtext_instance(context)
    try:
        strLogs = read_logs()
        for row in strLogs.split("\n"):
            match = re.search(r"\[First Article\] :(.*?)", row)
            if match:
                start_article = match.group(1)
                print(f"[First Article]: {start_article}")
                logger.info(f"Found the starting point for likes in the CSV file")
                logger.debug(f"[First Article] :{start_article}")
                return start_article
            
    except Exception:
        logger.error("Error while finding the first article")
        return None
    
def __find_article_for_click(context, start_article, page_num=1):
    """Finds the article to start liking from."""
    browser, logger = return_comtext_instance(context)
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
        logger.error(f"Error while finding the first article for click: {selenium_error_transform(e)}", )
        raise

    else: 
        logger.info("Initial article navigation completed for clicking")
        return start_article, page_num
