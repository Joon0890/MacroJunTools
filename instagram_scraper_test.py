import logging
from modules.instagram import save_images
from modules.instagram import save_videos
from modules.instagram import login_insta
from modules.instagram import collect_contents
from modules.utiles import ChromeDriverManager
from modules.utiles import remove_duplicate_files
from modules.utiles import load_config, load_env

def insta_main():
    
    try:
        manager = ChromeDriverManager()
        manager.start(headless=False, url="https://www.instagram.com/p/C7rtyvIgbAB/")

        link_list, video_list = collect_contents(manager.browser,contents_num=1)

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

insta_main()