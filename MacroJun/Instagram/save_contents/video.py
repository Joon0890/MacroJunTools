import os
import instaloader

def save_videos(video_list, output_path="insta_download"):
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
                    video_path = os.path.join(
                        save_directory, f"{post.date_utc.strftime('%Y-%m-%d_%H-%M-%S')}_video{idx}.mp4"
                    )
                    instaloading.download_pic(video_path, node.video_url, post.date_utc)
                    print(f"Video saved to {video_path}")
                else:
                    print(f"Skipped non-video content in slide {idx}")

            # 단일 동영상 처리
            if post.is_video:
                video_path = os.path.join(
                    save_directory, f"{post.date_utc.strftime('%Y-%m-%d_%H-%M-%S')}.mp4"
                )
                instaloading.download_pic(video_path, post.video_url, post.date_utc)
                print(f"Video saved to {video_path}")

        except Exception as e:
            print(f"Failed to process {video}. Error: {e}")