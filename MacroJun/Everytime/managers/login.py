import time, random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from MacroJun.utiles.scripts.log_csv import LogManager
from MacroJun.utiles.scripts.transform import selenium_error_transform

class LoginManager:
    def __init__(self, browser: webdriver.Chrome, log_manager: LogManager):
        self.browser = browser
        self.log_manager = log_manager
        self.log_manager.log_info("LoginManager", "The program starts and attempts to login.")
        
    def login_everytime(self, config):
        """Logs in to the website."""
        try:    
            try: 
                self.browser.find_element(By.CLASS_NAME, 'signin').click()
            except:
                pass
            
            self.browser.find_element(By.XPATH, '/html/body/div[1]/div/form/div[1]/input[1]').send_keys(config["my_id"])
            password_elem = self.browser.find_element(By.XPATH, '/html/body/div[1]/div/form/div[1]/input[2]')
            password_elem.send_keys(config["my_password"])
            self.browser.find_element(By.XPATH, '/html/body/div[1]/div/form/div[2]/label').click()
            password_elem.send_keys(Keys.ENTER)
            time.sleep(random.uniform(2, 5))
            
        except KeyboardInterrupt:
            raise
        
        except Exception as e:
            self.log_manager.log_error("LoginManager", "Error during login", selenium_error_transform(e))
            pass    
        
        else:
            self.log_manager.log_info("LoginManager", "completed login successfully.")