""" This is the main script that routes the arguments to the correct function """

import argparse
from dotenv import load_dotenv
from scraper.main import run_reddit_scraper  # Import the function from script/main.py

load_dotenv()


def main():
    """Main function that routes the arguments to the correct function"""

    parser = argparse.ArgumentParser(
        description="This is a python scraper and machine learning model."
    )

    parser.add_argument("-s", "--scraper", action="store_true", help="Run the scraper")
    parser.add_argument("-m", "--model", action="store_true", help="Run the model")
    args = parser.parse_args()

    if args.scraper:
        run_reddit_scraper()
    if args.model:
        print("Goodbye World!")


if __name__ == "__main__":
    main()
