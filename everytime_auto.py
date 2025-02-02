import sys
from modules.everytime import move_to_board
from modules.everytime import find_starting_point
from modules.everytime import login_everytime
from modules.everytime import StartAutoLike
from modules.utiles import GetLogger
from modules.utiles import ChromeDriverManager
from modules.utiles import load_env
from selenium.common.exceptions import WebDriverException, NoSuchWindowException, NoSuchElementException
            
def everytime_main(args):
    logger = GetLogger("everytime_autoLike.log")

    # .env 파일 및 config.yaml 파일 불러오기
    env_values = load_env()

    # .env에서 민감한 정보 가져오기
    my_id = env_values.get("EVERYTIME_USERNAME")
    my_password = env_values.get("EVERYTIME_PASSWORD")
    
    logger.info("Everytime ID, Password: %s, %s", my_id, my_password)
    
    if not my_id or not my_password:
        logger.error("Instagram credentials are missing in .env file!")
        raise
    
    logger.info("Starting Everytime auto-like...")
    
    try:
        manager = ChromeDriverManager()
        manager.start(headless=args.headless, url="https://everytime.kr/")
        
        # 크롬이 종료되었을 경우 예외 처리
        if not manager.browser:
            logger.error("Chrome browser failed to start.")
            raise SystemExit("Chrome browser failed to start.")

        login_everytime(manager, my_id, my_password)

        move_to_board(manager, "자유게시판")
        start_article, page_num = find_starting_point(manager, "everytime_autoLike.log")

        logger.info("Starting from article: %s, page number: %s", start_article, page_num)

        StartAutoLike(manager, start_article, page_num)

    except NoSuchElementException as e:
        logger.info("Element not found: %s. The task is complete.", e)
        if manager:
            manager.stop()
        logger.info("Exiting program as there are no more elements to process.")
        sys.exit(0)  # 정상 종료


