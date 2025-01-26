import logging
from modules.everytime import move_to_board
from modules.everytime import process_articles
from modules.everytime import AutoLikeManager
from modules.everytime import LoginManager
from modules.everytime import LogManager
from modules.everytime import BrowserContext
from modules.utiles import ChromeDriverManager
from modules.utiles import load_env

def everytime_main(args):
    log_manager = LogManager()

    # .env 파일 및 config.yaml 파일 불러오기
    env_values = load_env()

    # .env에서 민감한 정보 가져오기
    my_id = env_values.get("EVERYTIME_USERNAME")
    my_password = env_values.get("EVERYTIME_PASSWORD")

    print(f"[INFO] Everytime ID: {my_id}, Everytime Password: {my_password}")
    
    if not my_id or not my_password:
        print("[ERROR] Instagram credentials are missing in .env file!")
        return
    
    print("[INFO] Starting Everytime auto-like...")
    
    try:
        manager = ChromeDriverManager.initialize_browser_with_stealth(headless_flag=args.headless)
        manager.get_url(url="https://everytime.kr/", maximize_flag=True, wait=3)

        context = BrowserContext(manager.browser, log_manager)

        LoginManager.create_with_login(context, my_id, my_password)

        move_to_board(context, "자유게시판")
        start_article, page_num = process_articles(context)

        AutoLikeManager.StartAutoLike(context, start_article, page_num)
            
    except KeyboardInterrupt:
        print("[INFO] Program interrupted by user. Exiting gracefully.")
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")

    finally:
        if args.auto_close:
            manager.terminate_process()
