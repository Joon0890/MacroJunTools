import logging
from modules.pyautogui import AutoImageClick
from modules.pyautogui import FindImgLocation
from modules.utiles import save_json, load_json
from modules.utiles import load_config

def sugang_main(args):
    # .env 파일 및 config.yaml 파일 불러오기
    config = load_config()

    # config.yaml에서 설정값 가져오기
    imgpath = config.get("sugang", {}).get("imgpath", "")
    confidence = config.get("sugang", {}).get("confidence", 0.95)

    if args.find:
        if not imgpath:
            logging.error("Image path is required. Use --imgpath option.")
            return

        locations = FindImgLocation(imgpath, confidence)
        if locations:
            save_json(locations)
            logging.info("Location information saved.")
    elif args.auto_click:
        locations = load_json()
        if not locations:
            logging.error("No locations found. Use --find option first.")
            return
        AutoImageClick(*locations)
    else:
        logging.error("You must specify --find or --auto-click option.")
