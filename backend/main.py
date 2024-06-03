""" Main script to run the Reddit scrapper and model as server """

import time
import calendar
from datetime import datetime, date
from scrapper import RedditClient
from model import Model
from firebase import FirebaseClient
from utils import write_to_csv, read_subreddit_list
import schedule
from pprint import pprint


def is_last_day_of_month():
    """Check if today is the last day of the month"""

    today = date.today()
    last_day = calendar.monthrange(today.year, today.month)[1]
    return today.day == last_day


def scrape_weekly_reddit():
    """Scrape Reddit for weekly posts and write to CSV"""

    print("[INFO] Job started: Scraping Reddit!")
    reddit = RedditClient()
    subreddits = read_subreddit_list()

    # Scrape each subreddit and write to CSV
    for index, subreddit in enumerate(subreddits, start=1):
        print(f"[INFO] ({index}/{len(subreddits)}) Scraping {subreddit}...")
        weekly_posts = reddit.get_weekly_posts(subreddit)
        write_to_csv(weekly_posts, f"./data/{subreddit}.csv")

    print("[INFO] Job completed: Scraping successful!")


def run_monthly_model():
    """Run the model on the scraped data"""

    if is_last_day_of_month():
        print("[INFO] Job skipped: Not the last day of the month.")
        return

    print("[INFO] Job started: Running model...")

    model = Model()
    firebase = FirebaseClient()

    subreddits = read_subreddit_list()
    for index, subreddit in enumerate(subreddits, start=1):
        print(f"[INFO] ({index}/{len(subreddits)}) Running model for {subreddit}...")
        data = model.generate_monthly_result(subreddit)
        pprint(data)
        firebase.upload_data(data, subreddit)
    # delete data

    print("[INFO] Job completed: Model run successful!")


if __name__ == "__main__":
    # schedule.every().monday.at("12:00").do(scrape_weekly_reddit)
    schedule.every().day.at("12:00").do(run_monthly_model)

    # Run the jobs immediately for now
    schedule.run_all(delay_seconds=5)

    while True:
        schedule.run_pending()
        time.sleep(1)
