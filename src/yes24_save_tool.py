from src.app.pyautogui.find_location import findPosition
from src.app.pyautogui.auto_clicker import YES24eBOOKAutoSave, get_rectangle_properties
from src.utils.file.save_imagefiles import PDFsave

def run_yes24_save_tool():
    x1, y1 = findPosition()
    x2, y2 = findPosition()

    x_min, y_min, width, height = get_rectangle_properties(x1, y1, x2, y2)
    YES24eBOOKAutoSave(404, x_min, y_min, width, height)
    PDFsave(image_folder="yes24", output_pdf="111.pdf")