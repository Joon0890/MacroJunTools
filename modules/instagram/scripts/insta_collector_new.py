import time
from typing import Optional
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

LI_NUMBERRING = "23333333333333333333"

def get_XPATH_format(
    li_num: Optional[int] = None
) -> str:
    if li_num:
        return [
            f"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[1]/div/div/div/div/div[1]/div/div[1]/div[2]/div/div/div/ul/li[{li_num}]/div/div/div/div/div[1]/img",
            f"/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div[1]/div/div[1]/div/div/div/div/div[1]/div/div[1]/div[2]/div/div/div/ul/li[{li_num}]/div/div/div/div/div[1]/div[1]/img"
        ]
    
def collect_contents_new(driver: Chrome):
    image_list, video_list = [], []

    print("[INFO] Starting to scrape contents...")
    
    username = driver.find_element(By.CSS_SELECTOR, "span._ap3a._aaco._aacw._aacx._aad7._aade").text
    article_id = driver.current_url.split("p/")[-1].replace("/", "")

    for li_num in list(LI_NUMBERRING):
        try:
            try:
                link = driver.find_element(By.XPATH, get_XPATH_format(li_num=li_num)[0]).get_attribute('src')
            except NoSuchElementException:
                link = driver.find_element(By.XPATH, get_XPATH_format(li_num=li_num)[1]).get_attribute('src')

            print(f"[DEBUG] Found image element for li_num {li_num}.")

            image_list.append(link)
            print(f"[INFO] Image link: {link}\n\n")

        except NoSuchElementException:
            current_url = driver.current_url
            video_list.append(current_url)
            print(f"[INFO] Video link: {current_url}\n\n")
            break

        try:
            button_next = driver.find_element(By.CSS_SELECTOR, "button[aria-label='다음']")
            button_next.click()
            time.sleep(1)
            print("[INFO] Next slide clicked.")

        except NoSuchElementException:
            print("[INFO] End of post reached.")
            break
                    
    print("[INFO] Finished scraping.")
    print(f"[SUMMARY] Collected {len(image_list)} image links and {len(video_list)} video links.")
    return username, article_id, image_list, video_list
    

    