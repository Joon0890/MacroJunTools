from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from MacroJun.Everytime.everytime_utils.browser_utils import navigate
from MacroJun.Everytime.everytime_utils.browser_utils import initialize_articles
from MacroJun.Utiles.utiles.chrome import scroll_into_view

class AutoLikeManager:
    def __init__(self, browser, log_manager):
        self.browser = browser
        self.log_manager = log_manager
        self.page_num = 1

    def like_articles(self):
        """Performs the auto-like functionality."""
        for _ in range(self.page_num):
            try:
                changed_name = None
                articles = initialize_articles(self.browser)
                art_list = [article.text.split('\n')[0] for article in articles]
                print(art_list, changed_name)
                while art_list:
                    articles = initialize_articles(self.browser)
                    first_article = articles[0].find_element(By.TAG_NAME, "h2").text
                    print(first_article, len(articles), len(art_list))
                    if changed_name == first_article:
                        break

                    for realname in reversed(art_list):
                        for article in reversed(articles):
                            changed_name = article.find_element(By.TAG_NAME, "h2").text
                            print(changed_name, realname)
                            if changed_name == realname:
                                self._handle_article_like(article, realname, art_list)
                                break
                        break

                    if len(art_list) == 0:
                        for art in articles:
                            if str(art.text.split('\n')[0]) == changed_name:
                                break
                            else:
                                art_list.append(str(art.text.split('\n')[0]))

                self.log_manager.log_info("like_articles", "20 articles clicked successfully", f"completed {self.page_num} page.")
                navigate(self.browser, "이전")
            except Exception as e:
                self.log_manager.log_error("like_articles", "General error", str(e))

        return self.log_manager.log_info("run", "Task completed")

    def _handle_article_like(self, article, realname, art_list):
        """Handles the liking of an individual article."""
        scroll_into_view(self.browser, article); sleep(1)
        article.click(); sleep(3)

        article_name = self.browser.find_element(By.XPATH, "//h2[@class='large']").text
        self.log_manager.log_info("handle_article_like", "Article click completed", f"<{article_name}>")
        self._like_button_click()

        art_list.remove(realname)

    def _like_button_click(self):
        """Clicks the like button and handles potential alerts."""
        like_button = self.browser.find_element(By.CLASS_NAME, "posvote")
        scroll_into_view(self.browser, like_button)
        like_button.click()

        try:
            alert = Alert(self.browser); 
            alert.accept(); sleep(1)
            alert.accept(); sleep(1)
        except:
            pass
        finally:
            self.browser.back(); sleep(1)