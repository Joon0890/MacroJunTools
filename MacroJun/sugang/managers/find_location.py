import pyautogui
    
def FindImgLocation(image_paths: str, confidence: float=0.95):
    choice_list = []
    
    for image_path in image_paths:
        search_locations = list(pyautogui.locateAllOnScreen(image_path, confidence=confidence))

        if not search_locations:
            print("[INFO] No image found on the screen.")
            return False

        print("[INFO] Found the image at the following locations:")
        for i, location in enumerate(search_locations):
            print(f"[INFO] [{i + 1}] Location: [Left: {location.left}, Top: {location.top}, Width: {location.width}, Height: {location.height}]")

        choice = input("[INPUT] Enter the number of the image to select: ")

        if choice.isdigit() and 0 < int(choice) <= len(search_locations):
            selected_index = int(choice) - 1
            selected_location = search_locations[selected_index]
            center_x = int(selected_location.left + selected_location.width // 2)
            center_y = int(selected_location.top + selected_location.height // 2)

            pyautogui.position(center_x, center_y)
            print(f"[SUCCESS] Positioned on item [{choice}]: [Center X: {center_x}, Center Y: {center_y}]")
            choice_list.append({"image_path": image_path, "index": selected_index})

        else:
            print("[WARNING] Invalid input. Please enter a valid number or type 'exit'.")
            
    return choice_list

