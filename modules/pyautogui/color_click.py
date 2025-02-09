import pyautogui
from modules.pyautogui.autoclick_utils import AutoClick

def separate_color(color: str):
    color_map = {
        "r": (255, 0, 0),   # 빨간색
        "g": (0, 255, 0),   # 초록색
        "b": (0, 0, 255),   # 파란색
        "w": (255, 255, 255),  # 흰색
        "k": (0, 0, 0)     # 검정색
    }
    return color_map.get(color.lower(), (0, 0, 0))  # 기본값: 검정색

def find_color_on_screen(target_color):
    screen_width, screen_height = pyautogui.size()
    for x in range(screen_width):
        for y in range(screen_height):
            if pyautogui.pixel(x, y) == target_color:
                return x, y
    return None

def AutoColorClick(color: str = "b"):
    target_color = separate_color(color)
    while True:
        position = find_color_on_screen(target_color)
        if position:
            print(f"Target color found at {position}")
            AutoClick(position)
            break

                