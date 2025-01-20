import pyautogui
import time

def refresh(interval = 0.1):
    pyautogui.press('f5')
    time.sleep(interval)
    return 

def separate_color(color):
    if color=="b":
        return (0, 0, 255)  
    elif color=="r":
        return (255, 0, 0)
    elif color=="g":
        return (0, 255, 0)
    
def AutoClick(location=None, x=None, y=None, interval=0.1, refresh_flag=False):
    # Box 객체인지 확인하고 좌표 추출
    if location is not None:
        if hasattr(location, 'left') and hasattr(location, 'top'):
            x = int(location.left + location.width // 2)  # 중심 x 좌표
            y = int(location.top + location.height // 2)  # 중심 y 좌표
        elif isinstance(location, (list, tuple)) and len(location) == 2:
            x, y = map(int, location)  # 좌표 리스트나 튜플 처리
        else:
            raise ValueError(f"Invalid location format: {location}")
    
    # 좌표 유효성 검사
    if x is None or y is None:
        raise ValueError("Coordinates (x, y) must be provided or derived from location.")
    
    screen_width, screen_height = pyautogui.size()
    if not (0 <= x < screen_width and 0 <= y < screen_height):
        raise ValueError(f"Coordinates ({x}, {y}) are out of screen bounds.")
    
    # Refresh 플래그 처리
    if refresh_flag:
        refresh()
    
    # 클릭 실행
    print(f"[INFO] Clicking at ({x}, {y}) with interval={interval}")
    pyautogui.click(x, y)
    time.sleep(interval)
    return

