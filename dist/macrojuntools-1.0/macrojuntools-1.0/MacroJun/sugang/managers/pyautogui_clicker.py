import pyautogui
import keyboard  # pip install keyboard
import time
import pytesseract
from MacroJun.sugang.autoclick_utils.click_utils import AutoClick
from MacroJun.sugang.autoclick_utils.click_utils import refresh
from MacroJun.sugang.autoclick_utils.click_utils import separate_color

def locate_and_click(image_path, index, confidence=0.95, wait_time=2):
    try:
        locations = list(pyautogui.locateAllOnScreen(image_path, confidence=confidence))

        if locations:
            AutoClick(locations[int(index)])  # Click the last location
            print(f"[INFO] {image_path} clicked.")
            time.sleep(wait_time)
        else:
            print(f"[WARNING] {image_path} not found on the screen.")
    
    except Exception as e:
        print(f"[ERROR] {e}")

def AutoImageClick(search, button, confidence=0.95, wait_time=2, exit_key=b'\x1b'):
    print("[INFO] Starting auto-click. Press Esc to exit.")
    while True:
        # Click the search button
        locate_and_click(confidence=confidence, wait_time=wait_time, **search)

        # Click the action button
        locate_and_click(confidence=confidence, wait_time=wait_time, **button)

        if keyboard.is_pressed('esc'):  # ESC 키 감지
            print("[INFO] Esc key pressed. Exiting.")
            return  # 함수 종료

def AutoLocationClick(target_text:str):    
    while True:
        refresh()
        screenshot = pyautogui.screenshot()
        data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)

        for row in data:
            if target_text in row['text']:
                x = row['left']
                y = row['top']
                width = row['width']
                height = row['height']
                
                center_x = x + width // 2
                center_y = y + height // 2
                print(f'Text "{target_text}" found at ({center_x}, {center_y})')
                
                return AutoClick(center_x, center_y)
            
def AutoColorClick(color:str="b"):
    target_color = separate_color(color)
    while True:
        refresh()
        screen_width, screen_height = pyautogui.size()

        for x in range(screen_width):
            for y in range(screen_height):
                pixel_color = pyautogui.pixel(x, y)
                if pixel_color == target_color:
                    print(f'Target color found at ({x}, {y})')
                    return AutoClick((x, y))
                