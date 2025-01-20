import os
import requests
from datetime import datetime

def download_image(image_url, save_path):
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(save_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Image saved to {save_path}")
        else:
            print(f"Failed to download {image_url}: HTTP {response.status_code}")
    except Exception as e:
        print(f"Error downloading {image_url}: {e}")

def save_images(link_list, output_path="D:/insta_download", keyword=""):
    img_num = 1
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)  # 디렉토리가 존재하지 않으면 생성

    for image_url in link_list:
        try:
            # 현재 날짜와 시간 포맷
            current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            # 이미지 이름 생성
            if len(keyword)==0:
                image_name = f"{current_date}_{img_num}.jpg"
            else:
                image_name = f"{keyword}_{current_date}_{img_num}.jpg"
            img_num += 1

            # 저장 경로 설정
            save_path = os.path.join(output_path, image_name)

            # 이미지 다운로드
            print(f"Downloading video from {image_url}...")
            download_image(image_url, save_path)
            print(f"Downloaded to {save_path}")
        except Exception as e:
            print(f"Failed to process {image_url}. Error: {e}")
