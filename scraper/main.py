"""Main module for the scraper package."""


from os import getenv, path, remove
from datetime import datetime
import requests
import requests.auth
import pandas as pd
import numpy as np
from pprint import pprint
from time import sleep


SUBREDDIT = "peyups"
OUTPUT_DIR = "data.csv"
COMMENT_DIR = "comments.csv"

def get_auth_header():
    """ Get the authorization header for Reddit API. """
    return {
        "Authorization": f"{getenv("TOKEN_TYPE")} {getenv("ACCESS_TOKEN")}",
        "User-Agent": getenv("USER_AGENT"),
    }

# def fetch_reddit_comments_on():
#     """ Fetch the latest N posts from a subreddit. """
#     if path.exists(OUTPUT_DIR):
#         remove(OUTPUT_DIR)

#     headers = get_auth_header()

def fetch_reddit_posts(count: int)->list:
    """ Fetch the latest N posts from a subreddit. """
    if path.exists(COMMENT_DIR):
        remove(COMMENT_DIR)

    headers = get_auth_header()

    after = None
    for i in range(count):
        print(f"Fetching slice {i+1} of {count}")
        response = requests.get(
            f"https://oauth.reddit.com/r/{SUBREDDIT}/hot",
            headers=headers,
            timeout=10,
            params={"limit": 100, "after": after},
        )
        res_json = response.json()
        after = res_json["data"]["after"]

        df = pd.DataFrame()
        for post in res_json["data"]["children"]:
            data = post["data"]
            for key in data.keys():
                data[key] = [data[key]]
            ndf = pd.DataFrame(data)
            df = pd.concat([df, ndf], ignore_index=True)
        df.to_csv(OUTPUT_DIR, mode='a', index=False, header=True if i == 0 else False)


def reddit_api():
    """ Get the latest posts from a subreddit. """
    fetch_reddit_posts(10)


def run_reddit_scraper():
    reddit_api()
