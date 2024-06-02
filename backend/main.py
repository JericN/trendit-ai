""" Main script to run the Reddit scrapper and model as server """

import time
from scrapper import RedditClient
from utils import write_to_csv, read_subreddit_list
import schedule


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
    print("[LOGS] Running model...")


if __name__ == "__main__":
    schedule.every().monday.at("12:00").do(scrape_weekly_reddit)
    schedule.every().weeks.do(run_monthly_model)
    schedule.run_all(delay_seconds=5)
    while True:
        schedule.run_pending()
        time.sleep(1)
