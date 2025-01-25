import logging
from modules.utiles import ChromeDriverManager
from modules.utiles import load_env, load_config
from modules.everytime import ArticleManager
from modules.everytime import AutoLikeManager
from modules.everytime import LoginManager
from modules.utiles import LogManager

def everytime_main(args):
    # .env 파일 및 config.yaml 파일 불러오기
    env_values = load_env()
    config = load_config()

    # .env에서 민감한 정보 가져오기
    my_id = env_values.get("EVERYTIME_USERNAME")
    my_password = env_values.get("EVERYTIME_PASSWORD")
    if not my_id or not my_password:
        logging.error("Instagram credentials are missing in .env file!")
        return

    # config.yaml에서 설정값 가져오기
    headless = config.get("everytime", {}).get("headless", True)
    chrome_close = config.get("everytime", {}).get("chrome_close", True)
    
    logging.info("Starting Everytime auto-like...")
    with ChromeDriverManager(close_flag=chrome_close, headless_flag=headless) as manager:
        log = LogManager()

        manager.get_url(url="https://everytime.kr/", maximize_flag=True, wait=3)

        login = LoginManager(manager.get_browser(), log)
        login.login_everytime(my_id, my_password)

        article = ArticleManager(manager.get_browser(), log)
        article.move_to_article("자유게시판")
        article.find_first_article()
        article.find_article_for_click()

        autolike = AutoLikeManager(manager.get_browser(), log)
        autolike.like_articles()
