import pyautogui
import time
from src.app.pyautogui.autoclick_utils import AutoClick
from src.app.pyautogui.autoclick_utils import is_pressed

def find_all_locations(image_path, confidence=0.95):
    return list(pyautogui.locateAllOnScreen(image_path, confidence=confidence))

def locate_and_click(image_path, index, confidence=0.95, wait_time=2):
    try:
        locations = find_all_locations(image_path, confidence)

        if locations:
            AutoClick(locations[int(index)])  # Click the last location
            print(f"[INFO] {image_path} clicked.")
            time.sleep(wait_time)
        else:
            print(f"[WARNING] {image_path} not found on the screen.")
    
    except Exception as e:
        print(f"[ERROR] {e}")

def AutoImageClick(search, button, confidence=0.95, wait_time=2):
    print("[INFO] Starting auto-click. Press Esc to exit.")
    while True:
        # Click the search button
        locate_and_click(confidence=confidence, wait_time=wait_time, **search)

        # Click the action button
        locate_and_click(confidence=confidence, wait_time=wait_time, **button)
        
        if is_pressed():
            break



                