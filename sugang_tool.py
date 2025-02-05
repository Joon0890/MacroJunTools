import logging
from modules.pyautogui import AutoImageClick
from modules.pyautogui import FindImgLocation
from modules.utiles import save_json, load_json
from modules.utiles import load_config

def sugang_main(args):
    if args.imgpath:
        locations = FindImgLocation(args.imgpath, args.confidence)
        if locations:
            save_json(locations)
            logging.info("Location information saved.")
    elif args.auto_click:
        locations = load_json()
        if not locations:
            logging.error("No locations found. Use --find option first.")
            return
        AutoImageClick(*locations, args.confidence, args.wait_time)
    else:
        logging.error("You must specify --find or --auto-click option.")
