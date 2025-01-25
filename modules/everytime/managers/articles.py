import re
import time, random
from selenium import webdriver
from selenium.webdriver.common.by import By
from modules.everytime.utiles.log_csv import LogManager
from modules.everytime.utiles.transform import selenium_error_transform
from modules.everytime.utiles.everytime_utils import navigate
from modules.everytime.utiles.everytime_utils import scroll_into_view
from modules.everytime.utiles.everytime_utils import initialize_articles

class ArticleManager:
    def __init__(self, browser: webdriver.Chrome, log_manager: LogManager):
        self.browser = browser
        self.log_manager = log_manager
        self.start_article = None
        self.page_num = 1

    def move_to_article(self, article_name):
        """Navigates to the specified article board."""
        try:
            group_lis = self.browser.find_element(By.XPATH, "//div[@id='submenu']").find_elements(By.TAG_NAME, "li")
            for li in group_lis:
                a_tag = li.find_element(By.TAG_NAME, "a")
                if a_tag.text == article_name:
                    a_tag.click()
                    time.sleep(random.uniform(2, 5))
                    return
        except Exception as e:
            self.log_manager.log_error("move_to_article", "Error while navigating the article", selenium_error_transform(e))

    def find_first_article(self):
        """Finds the starting article for automation."""
        try:
            rows = self.log_manager.read_log()
            for row in reversed(rows):
                if len(row) > 2:
                    match = re.search(r"^<(.*?)>$", row[4])
                    if match:
                        self.start_article = match.group(1)
                        print(f"[First Article]: {self.start_article}")
                        self.log_manager.log_info(
                            "find_first_article", 
                            "Found the starting point for likes in the CSV file.", 
                            f"<{self.start_article}>"
                            )
                        return
        except Exception:
            self.log_manager.log_error("find_first_article", "Error while finding the first article")

    def find_article_for_click(self):
        """Finds the article to start liking from."""
        try:
            if self.start_article is not None:
                found = False
                while not found:
                    articles = initialize_articles(self.browser)
                    for index, article in enumerate(articles):
                        scroll_into_view(self.browser, article)
                        if self.start_article in article.text:
                            found = True
                            self.art_index = index
                            break

                    if found or self.page_num >= 10:
                        break

                    self.page_num += 1
                    navigate(self.browser, "next")
            else:
                self.page_num = 2
                for k in range(self.page_num - 1):
                    navigate(self.browser, "next")
        
        except KeyboardInterrupt:
            raise

        except Exception as e:
            self.log_manager.log_error("find_article_for_click", "Error while finding the first article for click", selenium_error_transform(e))
            raise

        else: 
            self.log_manager.log_info("find_article_for_click", "Initial article navigation completed for clicking")
            return
