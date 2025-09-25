import argparse
from config import interactive_env
from core import RunEverytimeAutoLike

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Main Entry Point")
    subparsers = parser.add_subparsers(dest="command", help="Sub-command to run")

    # Setting
    setting_parser = subparsers.add_parser("setting", help="Setting config and .env file")

    # Everytime
    everytime_parser = subparsers.add_parser("everytime", help="Run Everytime auto-like")
    everytime_parser.add_argument("--headless", action="store_true", help="Run in headless mode")

    # 실행
    args = parser.parse_args()

    if args.command == "setting":
        interactive_env()
    elif args.command == "everytime":
        RunEverytimeAutoLike(headless=args.headless)
    else:
        parser.print_help()