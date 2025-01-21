import time, random
from MacroJun.utiles import LogManager
from MacroJun.utiles import ConfigLoader
from MacroJun.everytime import LoginManager
from MacroJun.everytime import ArticleManager
from MacroJun.everytime import AutoLikeManager
from MacroJun.utiles import ChromeDriverManager

log = LogManager()
config_like = ConfigLoader("secrets/.env.Like")

with ChromeDriverManager(headless_flag=False) as manager:
    manager.get_url(url="https://everytime.kr/", maximize_flag=True)

    login = LoginManager(browser=manager.get_browser(), log_manager=log)
    login.login_everytime(config=config_like)

    time.sleep(random.uniform(2, 5))

    article = ArticleManager(browser=manager.get_browser(), log_manager=log)
    article.move_to_article(article_name="자유게시판")
    article.find_first_article()
    article.find_article_for_click()

    autolike = AutoLikeManager(browser=manager.get_browser(), log_manager=log)
    autolike.like_articles()