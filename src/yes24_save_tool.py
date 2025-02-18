from src.app.pyautogui.find_location import findPosition
from src.app.pyautogui.auto_clicker import YES24eBOOKAutoSave
from src.utils.file.save_imagefiles import PDFsave

def run_yes24_save_tool():
    x1, y1 = findPosition()
    x2, y2 = findPosition()

    page = int(input("[INFO] input page num: "))

    YES24eBOOKAutoSave(x1, y1, x2, y2, page)
    PDFsave(image_folder="yes24", output_pdf="111.pdf")