"""Main module for the scraper package."""

from os import path, remove
import pandas as pd
from scraper.api import get_posts, get_access_token


SUBREDDIT = "Artificial"
OUTPUT_DIR = "./data/data.csv"
COMMENT_DIR = "comments.csv"

attributes = [
    "subreddit",
    "name",
    "created_utc",
    "permalink",
    "author_fullname",
    "link_flair_text",
    "title",
    "selftext",
    "num_comments",
    "score",
]

# subreddit	id	timestamp	permalink	author	tag	title	body	comments	score

new_attributes = [
    "subreddit",
    "id",
    "timestamp",
    "permalink",
    "author",
    "tag",
    "title",
    "body",
    "comments",
    "score",
]


def get_relevant_data(post):
    """Convert a post to a DataFrame."""
    data = {key: [post["data"].get(key, "")] for key in attributes}
    return pd.DataFrame(data)


def fetch_reddit_posts(subreddit, header=False, count=11) -> list:
    """Fetch the latest N posts from a subreddit."""

    paging = "initial"
    data_list = []
    for i in range(count):

        # break if no more posts are available
        if paging is None:
            break

        print(f"Fetching {i*100}th data of {subreddit}...")

        # get the latest posts
        posts = get_posts(subreddit=subreddit, after=paging)
        # update the paging token
        paging = posts.get("after")

        # iterate over the posts
        for post in posts.get("children", []):
            ndf = get_relevant_data(post)
            data_list.append(ndf)

    # Concatenate all DataFrame fragments
    df = pd.concat(data_list, ignore_index=True)
    df.columns = new_attributes
    df.to_csv(OUTPUT_DIR, mode="a", index=False, header=header)


def reddit_api():
    """Get the latest posts from a subreddit."""

    if path.exists(OUTPUT_DIR):
        remove(OUTPUT_DIR)

    fetch_reddit_posts(subreddit="ArtificialInteligence", header=True)
    fetch_reddit_posts("learnmachinelearning")
    fetch_reddit_posts("MachineLearning")
    fetch_reddit_posts("artificial")
    fetch_reddit_posts("deeplearning")
    fetch_reddit_posts("OpenAI")


def run_reddit_scraper():
    """Run the Reddit scraper."""
    reddit_api()
    # get_access_token()
