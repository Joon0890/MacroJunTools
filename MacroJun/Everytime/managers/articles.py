from MacroJun.Everytime.everytime_utils.browser_utils import scroll_into_view
from MacroJun.Everytime.everytime_utils.browser_utils import navigate
from MacroJun.Everytime.everytime_utils.browser_utils import initialize_articles
import re

class ArticleManager:
    def __init__(self, browser, log_manager):
        self.browser = browser
        self.log_manager = log_manager
        self.start_article = None
        self.page_num = 1

    def move_to_article(self, url="https://everytime.kr/389115"):
        """Navigates to the specified article board."""
        try:
            self.browser.get(url)
        except Exception as e:
            self.log_manager.log_error("move_to_article", "Error while navigating the article", str(e))

    def find_first_article(self):
        """Finds the starting article for automation."""
        try:
            rows = self.log_manager.read_log()
            for row in reversed(rows):
                if len(row) > 2:
                    match = re.search(r"<(.*?)>", row[4])
                    if match:
                        self.start_article = match.group(1)
                        self.log_manager.log_info(
                            "find_first_article", 
                            "Found the starting point for likes in the CSV file.", 
                            f"<{self.start_article}>"
                            )
                        break
        except Exception:
            self.log_manager.log_error("find_first_article", "Error while finding the first article.")

    def find_article_for_click(self):
        """Finds the article to start liking from."""
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
                navigate(self.browser, "다음")
        else:
            self.page_num = 2
            for k in range(self.page_num - 1):
                navigate(self.browser, "다음")

        return self.log_manager.log_info(
                "find_article_for_click", 
                "Initial article navigation completed for clicking."
                )
