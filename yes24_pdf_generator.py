from modules.pyautogui.find_location import findPosition
from modules.pyautogui.auto_clicker import YES24eBOOKAutoSave, get_rectangle_properties
from modules.save_imagefiles import PDFsave

if __name__=='__main__':
    #x1, y1 = findPosition()
    #x2, y2 = findPosition()
#
    #x_min, y_min, width, height = get_rectangle_properties(x1, y1, x2, y2)
    #YES24eBOOKAutoSave(404, x_min, y_min, width, height)
    PDFsave(image_folder="yes24", output_pdf="111.pdf")