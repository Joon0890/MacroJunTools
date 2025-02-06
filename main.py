import argparse
from instagram_scraper import insta_main
from sugang_tool import sugang_main
from everytime_auto import everytime_main
from settings_manage import interactive_config

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

    # 실행
    args = parser.parse_args()

    if args.command == "setting":
        interactive_config()
    elif args.command == "instagram":
        insta_main(args)
    elif args.command == "sugang":
        sugang_main(args)
    elif args.command == "everytime":
        everytime_main(args)
    else:
        parser.print_help()
