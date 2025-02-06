from modules.instagram import save_img_video
from modules.instagram import collect_contents_new
from modules.utiles import ChromeDriverManager
from modules.utiles import remove_duplicate_files

URL_INPUT = input("[INFO] INPUT INSTAGRAM URL: ")

try:
    manager = ChromeDriverManager()
    manager.start(headless=False, url=URL_INPUT)

    username, article_id, image_list, video_list = collect_contents_new(manager.browser)

    save_img_video(username, article_id, image_list, video_list, output_path="D:/DOWNLOAD")

    remove_duplicate_files(folder_path="D:/DOWNLOAD")

except Exception as e:
    print(f"Error occurred in Instagram scraper: {e}")

finally:
    if manager:
        manager.stop()
