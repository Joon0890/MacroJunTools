import argparse
from selenium.common.exceptions import NoSuchElementException
from MacroJun.instagram.save_contents.image import save_images
from MacroJun.instagram.save_contents.video import save_videos
from MacroJun.instagram.managers.insta import collect_insta_contents
from MacroJun.instagram.managers.insta import login_insta
from MacroJun.sugang.managers.pyautogui_clicker import AutoImageClick
from MacroJun.sugang.managers.find_location import FindImgLocation
from MacroJun.everytime.managers.articles import ArticleManager
from MacroJun.everytime.managers.autolike import AutoLikeManager
from MacroJun.everytime.managers.login import LoginManager
from MacroJun.utiles.scripts.chrome import ChromeDriverManager
from MacroJun.utiles.scripts.delete_file import remove_duplicate_files
from MacroJun.utiles.scripts.config_loader import ConfigLoader
from MacroJun.utiles.scripts.transform import str_to_bool
from MacroJun.utiles.scripts.json_file import load_json
from MacroJun.utiles.scripts.json_file import save_json
from MacroJun.utiles.scripts.log_csv import LogManager

def insta_main():
    parser = argparse.ArgumentParser(description="Instagram Content Scraper")
    parser.add_argument("--contents", type=int, default=5, help="Number of Instagram posts to scrape")
    parser.add_argument("--keyword", type=str, required=True, help="Instagram tag name")
    parser.add_argument("--desktop", type=str_to_bool, required=True, help="True or False for desktop mode")
    parser.add_argument("--chrome_close", type=str_to_bool, default=True, help="True or False for Chrome closing")
    parser.add_argument("--headless", type=str_to_bool, required=False, help="True or False for headless mode")
    parser.add_argument('--my_id', type=str, required=True, help='Instagram username')
    parser.add_argument('--my_password', type=str, required=True, help='Instagram password')

    args = parser.parse_args()

    with ChromeDriverManager(
        desktop_flags=args.desktop, 
        close_flag=args.chrome_close, 
        headless_flag=args.headless
        ) as manager:

        try:
            login_insta(driver=manager.browser, keyword=args.keyword, my_id=args.my_id, my_password=args.my_password)
            link_list, video_list = collect_insta_contents(driver=manager.browser, contents_num=args.contents)
            
            save_images(link_list)
            save_videos(video_list)

            # 결과 출력
            print("[RESULT] Image Links:")
            for link in link_list:
                print(link)

            print("\n[RESULT] Video Links:")
            for video in video_list:
                print(video)

            print("[INFO] removing duplicate files...")
            remove_duplicate_files()
            print("[INFO] removed duplicate files.")

        except NoSuchElementException:
            print("[ERROR] elements not found. Check the XPath or page structure.")
            raise

        except KeyboardInterrupt:
            print("[INFO] KeyboardInterrupt: Closing instagram tool...")
            raise
        
        except Exception as e:
            print(f"[ERROR] Error While processing: {e}")
            raise

        finally:
            print("[INFO] Program terminated.")


def sugang_main():
    parser = argparse.ArgumentParser(description="Image Location Finder and Auto Click Tool")
    parser.add_argument("--find", action="store_true", help="Image location finding mode")
    parser.add_argument("--auto-click", action="store_true", help="Auto click mode")
    parser.add_argument("--imgpath", type=str, nargs='+', help="Path to the image file")
    parser.add_argument("--confidence", type=float, default=0.95, help="Image detection confidence (default: 0.95)")

    args = parser.parse_args()
    
    try:
        if args.find:
            if not args.imgpath:
                print("[ERROR] You must provide an image path. Use the --imgpath option.")
                return

            # Find image location
            locations = FindImgLocation(args.imgpath)
            if locations:
                save_json(locations)
                print("[INFO] Location information has been saved.")
                
        elif args.auto_click:
            # Use saved location to perform auto click
            locations = load_json()
            print(locations)
            if len(locations) < 1:
                print("[ERROR] At least one location is required. Use the --find option to save a location first.")
                return
            AutoImageClick(*locations)

        else:
            print("[ERROR] You must use one of the following options: --find or --auto-click")
    except KeyboardInterrupt:
        print("[INFO] Program terminated.")


def everytime_main():
    parser = argparse.ArgumentParser(description="Everytime Auto Like click")
    parser.add_argument("--chrome_close", type=str_to_bool, default=True, help="True or False for Chrome closing")
    parser.add_argument("--headless", type=str_to_bool, required=False, help="True or False for headless mode")
    parser.add_argument('--env', type=str, required=True, help='Path to .env file')

    args = parser.parse_args()

    log = LogManager()
    config_like = ConfigLoader(args.env)
    
    with ChromeDriverManager(
        close_flag=args.chrome_close, 
        headless_flag=args.headless
        ) as manager:
        try:
            manager.get_url(url="https://everytime.kr/", maximize_flag=True, wait=3)
            
            login = LoginManager(browser=manager.get_browser(), log_manager=log)
            login.login_everytime(config=config_like)
            
            article = ArticleManager(browser=manager.get_browser(), log_manager=log)
            article.move_to_article(article_name="자유게시판")
            article.find_first_article()
            article.find_article_for_click()
            
            autolike = AutoLikeManager(browser=manager.get_browser(), log_manager=log)
            autolike.like_articles()
        except KeyboardInterrupt:
            raise