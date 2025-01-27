import time, random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from modules.everytime.utiles.log_manager import CustomLogging
from modules.everytime.utiles.context import return_comtext_instance
from modules.everytime.utiles.transform import selenium_error_transform

class LoginManager:
    def __init__(self, context):
        self.context = context
        self.browser, self.logger = return_comtext_instance(context)
        self.logger.info("The program starts and attempts to login")
        
    @classmethod
    def create_with_login(cls, context, my_id, my_password):
        """팩토리 메서드: 인스턴스를 생성하고 로그인을 실행"""
        instance = cls(context)
        instance.__login_everytime(my_id, my_password)
        return instance
    
    def __login_everytime(self, my_id, my_password):
        """Logs in to the website."""
        try:    
            if my_id is None or my_password is None:
                self.logger.error("Everytime ID and Password is None")
                return  
            try: 
                self.browser.find_element(By.CLASS_NAME, 'signin').click()
            except:
                pass
            
            self.browser.find_element(By.XPATH, '/html/body/div[1]/div/form/div[1]/input[1]').send_keys(my_id)
            password_elem = self.browser.find_element(By.XPATH, '/html/body/div[1]/div/form/div[1]/input[2]')
            password_elem.send_keys(my_password)
            self.browser.find_element(By.XPATH, '/html/body/div[1]/div/form/div[2]/label').click()
            password_elem.send_keys(Keys.ENTER)
            time.sleep(random.uniform(2, 5))
            
        except KeyboardInterrupt:
            raise
        
        except NoSuchElementException:
            return

        except Exception as e:
            self.logger.error(f"Error during login: {selenium_error_transform(e)}")
            raise 
        
        else:
            self.logger.info("completed login successfully")
            return 