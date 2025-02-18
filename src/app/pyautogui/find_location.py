import time
import pyautogui
from src.app.pyautogui.image_click import find_all_locations
from src.app.pyautogui.autoclick_utils import is_pressed

def display_search_results(locations):
    """
    탐색 결과를 화면에 출력합니다.
    """
    if not locations:
        print("[INFO] No image found on the screen.")
        return False

    print("[INFO] Found the image at the following locations:")
    for i, location in enumerate(locations):
        print(f"[INFO] [{i + 1}] Location: [Left: {location.left}, Top: {location.top}, Width: {location.width}, Height: {location.height}]")
    return True

def get_user_choice(locations):
    """
    사용자로부터 선택 입력을 받습니다.
    """
    while True:
        choice = input("[INPUT] Enter the number of the image to select: ")
        if choice.isdigit() and 0 < int(choice) <= len(locations):
            return int(choice) - 1  # 0-based index
        elif choice.lower() == 'exit':
            return None
        else:
            print("[WARNING] Invalid input. Please enter a valid number or type 'exit'.")

def process_image_search(image_path, confidence=0.95):
    """
    단일 이미지 경로에 대해 탐색을 수행하고 결과를 처리합니다.
    """
    search_locations = find_all_locations(image_path, confidence)
    if not display_search_results(search_locations):
        return None

    selected_index = get_user_choice(search_locations)
    if selected_index is None:
        print("[INFO] Exiting selection process.")
        return None

    selected_location = search_locations[selected_index]
    center_x = int(selected_location.left + selected_location.width // 2)
    center_y = int(selected_location.top + selected_location.height // 2)

    pyautogui.moveTo(center_x, center_y)
    print(f"[SUCCESS] Positioned on item [{selected_index + 1}]: [Center X: {center_x}, Center Y: {center_y}]")
    return {"image_path": image_path, "index": selected_index}

def FindImgLocation(image_paths, confidence=0.95):
    """
    여러 이미지 경로에 대해 탐색 및 선택 작업을 수행합니다.
    """
    choice_list = []
    for image_path in image_paths:
        result = process_image_search(image_path, confidence)
        if result:
            choice_list.append(result)
    return choice_list

def findPosition():
    print("Press ESC to exit.")
    try:
        while True:
            # Get the current mouse position
            current_position = pyautogui.position()
            print(f"Current mouse position: x={current_position.x}, y={current_position.y}", end="\r")
            time.sleep(0.1)  # Update every 0.1 seconds
            if is_pressed():
                return current_position.x, current_position.y
    except KeyboardInterrupt:
        print("\nForcing program termination.")

