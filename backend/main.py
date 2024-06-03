""" Main script to run the Reddit scrapper and model as server """

import time
from scrapper import RedditClient
from model import Model
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

    print("[INFO] Job started: Running model...")

    model = Model()
    data = model.fit_transform("gaming")
    print(data)
    # save to firebase
    # delete data

    print("[INFO] Job completed: Model run successful!")


if __name__ == "__main__":
    schedule.every().monday.at("12:00").do(scrape_weekly_reddit)
    schedule.every(4).weeks.do(run_monthly_model)

    # Run the jobs immediately for now
    schedule.run_all(delay_seconds=5)

    while True:
        schedule.run_pending()
        time.sleep(1)
