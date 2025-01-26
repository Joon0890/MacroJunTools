import logging
from modules.instagram import save_images
from modules.instagram import save_videos
from modules.instagram import login_insta
from modules.instagram import collect_contents
from modules.utiles import ChromeDriverManager
from modules.utiles import remove_duplicate_files
from modules.utiles import load_config, load_env

def insta_main(args):
    # .env 파일 및 config.yaml 파일 불러오기
    env_values = load_env()
    config = load_config()

    # .env에서 민감한 정보 가져오기
    my_id = env_values.get("INSTAGRAM_USERNAME")
    my_password = env_values.get("INSTAGRAM_PASSWORD")
    if not my_id or not my_password:
        logging.error("Instagram credentials are missing in .env file!")
        return

    # config.yaml에서 설정값 가져오기
    scrape_limit = config.get("instagram", {}).get("scrape_limit", 5)

    if not args.keyword:
        logging.error("Instagram keyword is missing in config.yaml!")
        return
    
    logging.info("Starting Instagram scraper...")
    with ChromeDriverManager(close_flag=args.chrome_close, headless_flag=False) as manager:
        try:
            login_insta(manager.browser, args.keyword, my_id, my_password)
            link_list, video_list = collect_contents(manager.browser, scrape_limit)

            save_images(link_list)
            save_videos(video_list)

            logging.info("Image Links:")
            for link in link_list:
                logging.info(link)

            logging.info("Video Links:")
            for video in video_list:
                logging.info(video)

            logging.info("Removing duplicate files...")
            remove_duplicate_files()
        except Exception as e:
            logging.error(f"Error occurred in Instagram scraper: {e}")
