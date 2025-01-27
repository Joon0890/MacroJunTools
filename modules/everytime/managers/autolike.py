import time, random
from typing import List 
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from modules.everytime.utiles.context import return_comtext_instance
from modules.everytime.utiles.transform import selenium_error_transform
from modules.everytime.utiles.everytime_utils import navigate
from modules.everytime.utiles.everytime_utils import scroll_into_view
from modules.everytime.utiles.everytime_utils import initialize_articles

def create_art_list(articles: List[WebElement], comparison_str: str):
    art_list = []

    for article in articles:
        if comparison_str == article.text.split('\n')[0]:
            break
        art_list.append(article.text.split('\n')[0])

    return art_list

def return_title_of_article(article: Chrome):
    return article.find_element(By.TAG_NAME, "h2").text

class AutoLikeManager:
    def __init__(self, context):
        self.context = context
        self.browser, self.logger = return_comtext_instance(context)

    @classmethod
    def StartAutoLike(cls, context, start_article, page_num):
        """팩토리 메서드: 인스턴스를 생성하고 로그인을 실행"""
        instance = cls(context)
        instance.__like_articles(start_article, page_num)
        return instance
    
    def __like_articles(self, start_article, page_num, changed_name = None):
        for index in range(page_num):
            try:
                articles = initialize_articles(self.browser)
                art_list = create_art_list(articles, start_article)
            
                self.logger.debug(f"[Art List]: {art_list}")

                while art_list:
                    articles = initialize_articles(self.browser)

                    first_article = return_title_of_article(articles[0])
                    if changed_name == first_article:
                        break

                    self.logger.debug(f"[First Article]: {first_article}, [Articles Count]: {len(articles)}, [Art List Count]: {len(art_list)}")
                    
                    for realname in reversed(art_list):
                        for article in reversed(articles):
                            changed_name = return_title_of_article(article)
                            if changed_name == realname:
                                print(f"[Article Name]: {changed_name}")
                                self.__handle_article_like(article, realname, art_list)
                                break
                        break

                    if len(art_list) == 0:
                        articles = initialize_articles(self.browser)
                        art_list = create_art_list(articles, changed_name)

            except KeyboardInterrupt:
                raise

            except Exception as e:
                self.logger.error(f"General error: {selenium_error_transform(e)}")
                pass
            
            else:
                self.logger.info(f"20 articles clicked successfully in {page_num-index} page")
                try:
                    navigate(self.browser, "prev")

                except NoSuchElementException:
                    self.logger.debug("No 'prev' button found, task completed.")
                    return
                
                except Exception as e:
                    self.logger.error(f"Unexpected error in navigate: {selenium_error_transform(e)}")
                    raise

    def __handle_article_like(self, article: WebElement, realname, art_list: List):
        """Handles the liking of an individual article."""
        scroll_into_view(self.browser, article)
        article.click()
        time.sleep(random.uniform(2, 5))

        article_name = self.browser.find_element(By.XPATH, "//h2[@class='large']").text
        self.logger.info(f"Article click completed <{article_name}>")
        self.__like_button_click()

        art_list.remove(realname)

    def __like_button_click(self):
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