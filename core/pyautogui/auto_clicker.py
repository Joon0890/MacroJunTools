import os
import time
import pyautogui
from core.pyautogui.autoclick_utils import is_pressed

def CanvasAutoSave(page, save_folder="canva_file", index=0):
    print("[INFO] Starting program...")
    time.sleep(10)

    pyautogui.press("f11")
    print("[INFO] Pressed f11 and please wait...")
    time.sleep(5)
        
    for index in range(page):
        try:        
            pyautogui.screenshot(
                imageFilename=f"{save_folder}/screenshot_{index}.jpg"
                )
            print(f"[INFO] Screenshot and save screenshot_{index}.jpg")

        except Exception as e:
            print(f"[ERROR] error while sliding: {e}")
        
        else:     
            pyautogui.press("right")
            print("[INFO] complete slide")
            time.sleep(2)
        
        finally:
            if is_pressed():
                break

def YES24eBOOKAutoSave(x1, y1, x2, y2, page, save_folder="yes24"):
    """
    YES24의 eBook 뷰어와 같은 일부 애플리케이션은 
    UI 렌더링 방식이 일반적인 화면 요소와 다르기 때문에, 
    관리자 권한으로 실행해야 pyautogui의 클릭 이벤트를
    원활하게 해결 가능
    """

    if not os.path.exists(save_folder):
        os.makedirs(save_folder, exist_ok=True)

    def get_rectangle_properties(x1, y1, x2, y2):
        x_min = min(x1, x2)
        y_min = min(y1, y2)
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        
        return x_min, y_min, width, height

    x_min, y_min, width, height = get_rectangle_properties(x1, y1, x2, y2)

    print("[INFO] Starting program...")

    try:
        for index in range(page):
            try:        
                if is_pressed():
                    break
                save1 = pyautogui.screenshot(region=(x_min, y_min, width, height))
                save1.save(f"{save_folder}/screenshot_{index}.png")
                print(f"[INFO] Screenshot and save screenshot_{index}.jpg")

            except Exception as e:
                print(f"[ERROR] error while sliding: {e}")
            
            else:     
                pyautogui.click(x=1868, y=584)
                print("[INFO] complete slide")
                time.sleep(1)
                
    except KeyboardInterrupt:
        pass



