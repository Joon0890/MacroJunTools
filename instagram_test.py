from modules.instagram import save_images, save_videos
from modules.instagram import collect_contents_new
from modules.utiles import ChromeDriverManager

try:
    manager = ChromeDriverManager()
    manager.start(headless=False, url="https://www.instagram.com/p/C7ggZ6MPzsK/")

    link_list, video_list = collect_contents_new(manager.browser)

    print("\n\n\n")
    print("Image Links:")
    for link in link_list:
        print(link)

    print("Video Links:")
    for video in video_list:
        print(video)

    print("Removing duplicate files...")

except Exception as e:
    print(f"Error occurred in Instagram scraper: {e}")

finally:
    if manager:
        manager.stop()