import time, random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoSuchElementException
from MacroJun.utiles.scripts.log_csv import LogManager
from MacroJun.utiles.scripts.transform import selenium_error_transform
from MacroJun.everytime.everytime_utils.browser_utils import navigate
from MacroJun.everytime.everytime_utils.browser_utils import scroll_into_view
from MacroJun.everytime.everytime_utils.browser_utils import initialize_articles

class AutoLikeManager:
    def __init__(self, browser: webdriver.Chrome, log_manager: LogManager):
        self.browser = browser
        self.log_manager = log_manager

    def like_articles(self):
        while True:
            try:
                changed_name = None
                articles = initialize_articles(self.browser)
                art_list = [article.text.split('\n')[0] for article in articles]
                print(f"[Art List]: {art_list}, [Changed Name]: {changed_name}")
                while art_list:
                    articles = initialize_articles(self.browser)
                    first_article = articles[0].find_element(By.TAG_NAME, "h2").text
                    if changed_name == first_article:
                        break

                    print(f"[First Article]: {first_article}, [Articles Count]: {len(articles)}, [Art List Count]: {len(art_list)}")
                    
                    for realname in reversed(art_list):
                        for article in reversed(articles):
                            changed_name = article.find_element(By.TAG_NAME, "h2").text
                            if changed_name == realname:
                                print(f"[Article Name]: {changed_name}")
                                self._handle_article_like(article, realname, art_list)
                                break
                        break

                    if len(art_list) == 0:
                        articles = initialize_articles(self.browser)
                        for art in articles:
                            if str(art.text.split('\n')[0]) == changed_name:
                                break
                            else:
                                art_list.append(str(art.text.split('\n')[0]))
            except KeyboardInterrupt:
                raise

            except Exception as e:
                self.log_manager.log_error("like_articles", "General error", selenium_error_transform(e))
                pass
            
            else:
                self.log_manager.log_info("like_articles", "20 articles clicked successfully")
                try:
                    navigate(self.browser, "prev")
                except NoSuchElementException:
                    self.log_manager.log_info("like_articles", "No 'prev' button found, task completed.")
                    return
                except Exception as e:
                    self.log_manager.log_error("like_articles", "Unexpected error in navigate", selenium_error_transform(e))
                    return

    def _handle_article_like(self, article, realname, art_list):
        """Handles the liking of an individual article."""
        scroll_into_view(self.browser, article)
        article.click()
        time.sleep(random.uniform(2, 5))

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
            alert.accept() 
            
            time.sleep(random.uniform(0.5, 1.5))
            alert.accept() 
            time.sleep(random.uniform(0.5, 1.5))

        except:
            pass

        finally:
            self.browser.back()
            time.sleep(random.uniform(0.5, 1.5))