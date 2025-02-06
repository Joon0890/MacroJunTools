from modules.utiles import ChromeDriverManager
from modules.utiles import remove_duplicate_files
from modules.utiles import load_config, load_env
from modules.instagram import save_img_video
from modules.instagram import collect_contents_new
from modules.instagram import login_insta
from modules.utiles import ChromeDriverManager
from modules.utiles import remove_duplicate_files

def insta_main(args):
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
        manager.start(headless=args.headless, url=URL_INPUT)

        username, article_id, image_list, video_list = collect_contents_new(manager.browser)

        save_img_video(username, article_id, image_list, video_list, output_path=args.save_path)

        remove_duplicate_files(folder_path=args.save_path)

    except Exception as e:
        print(f"Error occurred in Instagram scraper: {e}")
