import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

LI_NUMBERRING = "23434334343343433434"

XPATH_LIST = {
    "div": "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[1]/div[contains(@class, 'x1lliihq xh8yej3')]",
    
    "li": [
        "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[1]/div/div/div/div/div[1]/div/div[1]/div[2]/div/div/div/ul/li[{li_num}]/div/div/div/div/div[1]/img",
        "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[1]/div/div/div/div/div[1]/div/div[1]/div[2]/div/div/div/ul/li[{li_num}]/div/div/div/div/div[1]/div[1]/img"
    ],

    "small_button":
    [
        "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[1]/div/div/div/div/div[1]/div/div[1]/div[2]/div/button[{btn_num}]",
        "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[1]/div/div/div/div/div[1]/div/div[1]/div[2]/div/button",
    ]
}

def collect_contents_new(driver: Chrome):
    link_list, video_list = [], []

    print("[INFO] Starting to scrape contents...")

    for li_num in list(LI_NUMBERRING):
        try:
            try:
                link = driver.find_element(By.XPATH, XPATH_LIST["li"][0].format(li_num=li_num)).get_attribute('src')
            except:
                link = driver.find_element(By.XPATH, XPATH_LIST["li"][1].format(li_num=li_num)).get_attribute('src')

            print(f"[DEBUG] Found image element for li_num {li_num}.")

        except NoSuchElementException:
            current_url = driver.current_url
            video_list.append(current_url)
            print(f"[INFO] Video link: {current_url}")
            break

        else:
            link_list.append(link)
            print(f"[INFO] Image link: {link}")

        finally:
            try:
                try:
                    next_button = driver.find_element(By.XPATH, XPATH_LIST["small_button"][0].format(btn_num=2))
                except:
                    next_button = driver.find_element(By.XPATH, XPATH_LIST["small_button"][1])

            except Exception as e:
                print(f"[ERROR] Error clicking next button: {e}")
                break

            else:
                if next_button.get_attribute("aria-label") == "돌아가기":
                    print("[INFO] End of post reached.")
                    break
                else:
                    next_button.click()
                    time.sleep(1)
                    print("[INFO] Next slide clicked.")

    print("[INFO] Finished scraping.")
    print(f"[SUMMARY] Collected {len(link_list)} image links and {len(video_list)} video links.")
    return link_list, video_list
    

    