from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from MacroJun.Utiles.utiles.chrome import wait_for_element
from time import sleep

class LoginManager:
    def __init__(self, browser, log_manager):
        self.browser = browser
        self.log_manager = log_manager
        
    def log_in(self, config):
        """Logs in to the website."""
        try: 
            wait_for_element(self.browser, By.CLASS_NAME, 'signin').click()
        except:
            pass

        try:    
            wait_for_element(self.browser, By.XPATH, '/html/body/div[1]/div/form/div[1]/input[1]').send_keys(config["my_id"])
            password_elem = wait_for_element(self.browser, By.XPATH, '/html/body/div[1]/div/form/div[1]/input[2]')
            password_elem.send_keys(config["my_password"])
            wait_for_element(self.browser, By.XPATH, '/html/body/div[1]/div/form/div[2]/label').click()
            password_elem.send_keys(Keys.ENTER)
            sleep(3)
        except Exception as e:
            self.log_manager.log_error("LoginManager", "Error during login", str(e))
