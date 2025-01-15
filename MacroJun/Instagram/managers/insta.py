import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

LI_NUMBERRING = "23434334343343433434"

XPATH_LIST = {
    "article": "/html/body/div[contains(@class, 'x1n2onr6 xzkaem6')]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article",
    
    "li": [
        "/html/body/div[contains(@class, 'x1n2onr6 xzkaem6')]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[1]/div/div[1]/div[2]/div/div/div/ul/li[{li_num}]/div/div/div/div/div[1]/img",
        "/html/body/div[contains(@class, 'x1n2onr6 xzkaem6')]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[1]/div/div[1]/div[2]/div/div/div/ul/li[{li_num}]/div/div/div/div/div[1]/div[1]/img",
    ],

    "small_button":
    [
        "/html/body/div[contains(@class, 'x1n2onr6 xzkaem6')]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[1]/div/div[1]/div[2]/div/button[{btn_num}]",
        "/html/body/div[contains(@class, 'x1n2onr6 xzkaem6')]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[1]/div/div[1]/div[2]/div/button",
    ],

    "big_button":
    [
        "/html/body/div[contains(@class, 'x1n2onr6 xzkaem6')]/div[1]/div/div[3]/div/div/div/div/div[1]/div/div/div[2]/button",
        "/html/body/div[contains(@class, 'x1n2onr6 xzkaem6')]/div[1]/div/div[3]/div/div/div/div/div[1]/div/div/div/button"
    ]
}

# 로그인 함수
def login_insta(driver: Chrome, keyword: str, my_id: str, my_password: str):
    """Log in to Instagram."""
    driver.get(f"https://www.instagram.com/explore/tags/{keyword}/")
    time.sleep(2)

    input_id = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')
    input_password = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')
    login_button = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')

    input_id.send_keys(my_id)
    input_password.send_keys(my_password)
    login_button.click()

    print("[INFO] Login successful.")
    time.sleep(5)  


def collect_insta_contents(driver: Chrome, contents_num):
    link_list, video_list = [], []

    print("[INFO] Collecting Instagram contents...")

    elems = driver.find_elements(By.TAG_NAME, "a")
    print(f"[DEBUG] Found {len(elems)} links on the page.")

    for index, elem in enumerate(elems[:3]):
        try:
            svg_tag = elem.find_element(By.TAG_NAME, "svg")
            if svg_tag.get_attribute("aria-label") == "릴스":
                print(f"[INFO] Found '릴스' link at index {index}. Clicking it.")
                elems[1].click()
                break
        except Exception as e:
            print(f"[ERROR] Error processing link at index {index}: {e}")
    else:
        print("[INFO] No '릴스' link found. Clicking the first link.")
        elems[0].click()

    time.sleep(1)
    print("[INFO] Starting to scrape contents...")

    for content_index in range(contents_num):
        print(f"[INFO] Scraping content {content_index + 1} of {contents_num}...")
        for li_num in list(LI_NUMBERRING):
            try:
                try:
                    article = driver.find_element(By.XPATH, XPATH_LIST["article"])
                except:
                    article = driver.find_element(By.XPATH, XPATH_LIST["article"])
                print("[DEBUG] Found article element.")

                try:
                    img_tag = article.find_element(By.XPATH, XPATH_LIST["li"][0].format(li_num=li_num))
                except:
                    img_tag = article.find_element(By.XPATH, XPATH_LIST["li"][1].format(li_num=li_num))

                print(f"[DEBUG] Found image element for li_num {li_num}.")

            except NoSuchElementException:
                current_url = driver.current_url
                video_list.append(current_url)
                print(f"[INFO] Video link: {current_url}")
                break

            else:
                link = img_tag.get_attribute('src')
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

        try:
            driver.find_element(By.XPATH, XPATH_LIST["big_button"][0]).click()
            print("[INFO] Moving to the next post.")
        except:
            driver.find_element(By.XPATH, XPATH_LIST["big_button"][1]).click()
            print("[INFO] Moving to the next post using alternative button.")
        finally:
            time.sleep(3)

    print("[INFO] Finished scraping.")
    print(f"[SUMMARY] Collected {len(link_list)} image links and {len(video_list)} video links.")
    return link_list, video_list
    

    