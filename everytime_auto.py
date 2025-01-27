import logging
from modules.everytime import move_to_board
from modules.everytime import process_articles
from modules.everytime import AutoLikeManager
from modules.everytime import LoginManager
from modules.everytime import CustomLogging
from modules.everytime import BrowserContext
from modules.utiles import ChromeDriverManager
from modules.utiles import load_env

def everytime_main(args):
    logger = CustomLogging("DualLogger")
    logger.addHandler("app.log")

    # .env 파일 및 config.yaml 파일 불러오기
    env_values = load_env()

    # .env에서 민감한 정보 가져오기
    my_id = env_values.get("EVERYTIME_USERNAME")
    my_password = env_values.get("EVERYTIME_PASSWORD")

    logger.info(f"Everytime ID, Password: {my_id, my_password}")
    
    if not my_id or not my_password:
        logger.error("Instagram credentials are missing in .env file!")
        raise
    
    logger.info("Starting Everytime auto-like...")
    
    try:
        manager = ChromeDriverManager()
        manager.start(headless_flag=args.headless, url="https://everytime.kr/")

        context = BrowserContext(manager.browser, logger)

        LoginManager.create_with_login(context, my_id, my_password)

        move_to_board(context, "자유게시판")
        start_article, page_num = process_articles(context)

        AutoLikeManager.StartAutoLike(context, start_article, page_num)
            
    except KeyboardInterrupt:
        logger.info("Program interrupted by user. Exiting gracefully.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

    finally:
        if args.auto_close:
            manager.stop()
