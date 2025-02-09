from modules.pyautogui.image_click import AutoImageClick
from modules.pyautogui.find_location import FindImgLocation
from modules.json_file import save_json, load_json

def run_sugang_tool(auto_click, imgpath, confidence, wait_time):
    if imgpath:
        locations = FindImgLocation(imgpath, confidence)
        if locations:
            save_json(locations)
            print("Location information saved.")
    elif auto_click:
        locations = load_json()
        if not locations:
            print("No locations found. Use --find option first.")
            return
        AutoImageClick(*locations, confidence, wait_time)
    else:
        print("You must specify --find or --auto-click option.")
