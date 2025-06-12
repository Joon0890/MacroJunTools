import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

# 로그인 함수
def login_insta(driver: Chrome, my_id: str, my_password: str):
    """Log in to Instagram."""
    try:
        driver.get(f"https://www.instagram.com/")
        time.sleep(2)

        input_id = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')
        input_password = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')
        login_button = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')

        input_id.send_keys(my_id)
        input_password.send_keys(my_password)
        login_button.click()

        print("[INFO] Login successful.")
        time.sleep(5)  
    
    except:
        pass