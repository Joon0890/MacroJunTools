from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="MacroJunTools",  # 패키지 이름
    version="1.0",
    description="Automation tools for Instagram, AutoClick, and more",
    author="Your Name",
    packages=find_packages(include=["MacroJun", "MacroJun.*"]),  # MacroJun 및 서브 디렉토리 포함
    install_requires=required,
    entry_points={
        "console_scripts": [
            "instagram=MacroJun.main:insta_main",  # Instagram 툴 실행
            "sugang=MacroJun.main:sugang_main",         # AutoClick 실행
            "everytime=MacroJun.main:everytime_main",         # Everytime 실행
        ],
    },
)
