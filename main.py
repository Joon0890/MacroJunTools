import argparse
from config import interactive_env
from core import (
    RunEverytimeAutoLike, 
    run_instagram_scraper, 
    run_sugang_tool, 
    run_yes24_save_tool
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Main Entry Point")
    subparsers = parser.add_subparsers(dest="command", help="Sub-command to run")

    # Setting
    setting_parser = subparsers.add_parser("setting", help="Setting config and .env file")

    # Instagram
    insta_parser = subparsers.add_parser("instagram", help="Run Instagram scraper")
    insta_parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    insta_parser.add_argument("--save-path", type=str, required=False, help="Run in headless mode")

    # Sugang
    sugang_parser = subparsers.add_parser("sugang", help="Run Sugang Tool")
    sugang_parser.add_argument("--auto-click", action="store_true", help="Auto-click mode")
    sugang_parser.add_argument("--imgpath", type=str, nargs='+', help="Path to image files")
    sugang_parser.add_argument("--confidence", type=float, default=0.95, help="Image detection confidence")
    sugang_parser.add_argument("--wait-time", type=float, default=1, help="Image detection confidence")

    # Everytime
    everytime_parser = subparsers.add_parser("everytime", help="Run Everytime auto-like")
    everytime_parser.add_argument("--headless", action="store_true", help="Run in headless mode")

    yes24_parser = subparsers.add_parser("yes24", help="Run YES24 ebook auto save")

    # 실행
    args = parser.parse_args()

    if args.command == "setting":
        interactive_env()
    elif args.command == "instagram":
        run_instagram_scraper(headless=args.headless, save_path=args.save_path)
    elif args.command == "everytime":
        RunEverytimeAutoLike(headless=args.headless)
    elif args.command == "sugang":
        run_sugang_tool(auto_click=args.auto_click, imgpath=args.imgpath, confidence=args.confidence, wait_time=args.wait_time)
    elif args.command == "yes24":
        run_yes24_save_tool()
    else:
        parser.print_help()