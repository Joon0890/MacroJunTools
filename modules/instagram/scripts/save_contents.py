import os
import instaloader
import requests
from datetime import datetime

def save_videos(username, article_id, video_list, output_path):
    # Instaloader 인스턴스 생성
    instaloading = instaloader.Instaloader()

    # 저장 디렉토리 설정
    current_directory = os.getcwd()
    save_directory = os.path.join(current_directory, output_path)
    os.makedirs(save_directory, exist_ok=True)

    for video in video_list:
        try:
            # URL에서 shortcode 추출
            if "/p/" in video:
                post_url = video.split("/p/")[1].split('/')[0]
            else:
                print(f"Invalid URL format: {video}")
                continue

            # 게시물 불러오기
            post = instaloader.Post.from_shortcode(instaloading.context, post_url)

            # 다중 슬라이드(동영상 포함) 처리
            print(f"Downloading content from: {video}")
            for idx, node in enumerate(post.get_sidecar_nodes(), start=1):
                if node.is_video:
                    current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f")
                    video_path = os.path.join(
                        save_directory, f"{username}_{article_id}_{current_date}.mp4"
                    )
                    instaloading.download_pic(video_path, node.video_url, post.date_utc)
                    print(f"Video saved to {video_path}")
                else:
                    print(f"Skipped non-video content in slide {idx}")

            # 단일 동영상 처리
            if post.is_video:
                current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f")
                video_path = os.path.join(
                    save_directory, f"{username}_{article_id}_{current_date}.mp4"
                )
                instaloading.download_pic(video_path, post.video_url, post.date_utc)
                print(f"Video saved to {video_path}")

        except Exception as e:
            print(f"Failed to process {video}. Error: {e}")

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

def save_images(username, article_id, image_list, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)  # 디렉토리가 존재하지 않으면 생성

    for image_url in image_list:
        try:
            # 현재 날짜와 시간 포맷
            current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f")
            # 이미지 이름 생성
            image_name = f"{username}_{article_id}_{current_date}.jpg"

            # 저장 경로 설정
            save_path = os.path.join(output_path, image_name)

            download_image(image_url, save_path)
            print(f"Downloaded to {save_path}")
        except Exception as e:
            print(f"Failed to process {image_url}. Error: {e}")

def save_img_video(username, article_id, image_list, video_list, output_path="D:/insta_download"):
    save_images(username, article_id, image_list, output_path)
    save_videos(username, article_id, video_list, output_path)