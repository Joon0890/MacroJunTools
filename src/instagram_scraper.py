from src.app.instagram.save_contents import save_img_video
from src.app.instagram.insta_collector_new import collect_contents_new
from src.utils.chrome_manager import ChromeDriverManager
from src.utils.file.delete_file import remove_duplicate_files
from src.utils.file.env_utils import load_env

def run_instagram_scraper(headless, save_path):
    # .env 파일 및 config.yaml 파일 불러오기
    env_values = load_env()

    # .env에서 민감한 정보 가져오기
    my_id = env_values.get("INSTAGRAM_USERNAME")
    my_password = env_values.get("INSTAGRAM_PASSWORD")
    if not my_id or not my_password:
        print("Instagram credentials are missing in .env file!")
        return
    
    print("Starting Instagram scraper...")
    
    URL_INPUT = input("[INFO] INPUT INSTAGRAM URL: ")

    try:
        manager = ChromeDriverManager()
        manager.start(headless=headless, url=URL_INPUT)

        username, article_id, image_list, video_list = collect_contents_new(manager.browser)

        save_img_video(username, article_id, image_list, video_list, output_path=save_path)

        remove_duplicate_files(folder_path=save_path)

    except Exception as e:
        print(f"Error occurred in Instagram scraper: {e}")

    finally:
        if manager:
            manager.stop()
