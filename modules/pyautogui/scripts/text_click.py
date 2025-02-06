import pyautogui
import pytesseract
from modules.pyautogui.utiles.autoclick_utils import AutoClick
from modules.pyautogui.utiles.autoclick_utils import refresh

def take_screenshot():
    """화면을 캡처하여 반환합니다."""
    return pyautogui.screenshot()

def extract_text_data(image):
    """이미지에서 텍스트 데이터를 추출합니다."""
    return pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

def find_text_position(data, target_text):
    """지정된 텍스트의 중심 좌표를 반환합니다."""
    for i, text in enumerate(data['text']):
        if target_text in text:
            x = data['left'][i]
            y = data['top'][i]
            width = data['width'][i]
            height = data['height'][i]
            
            center_x = x + width // 2
            center_y = y + height // 2
            return center_x, center_y
    return None

def AutoTextClick(target_text):
    """텍스트를 찾고 클릭합니다."""
    while True:
        refresh()
        screenshot = take_screenshot()
        data = extract_text_data(screenshot)
        position = find_text_position(data, target_text)
        if position:
            print(f'Text "{target_text}" found at {position}')
            AutoClick(*position)
            break

        