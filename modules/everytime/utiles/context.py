from selenium.webdriver import Chrome
from modules.everytime.utiles.log_manager import CustomLogging

class BrowserContext:
    def __init__(self, browser, logger):
        self.browser = browser
        self.logger = logger

def return_comtext_instance(context: BrowserContext) -> tuple["Chrome", "CustomLogging"]:
    browser = context.browser
    logger = context.logger
    return browser, logger