"""A module for fetching posts from Reddit using the PRAW library"""

from os import getenv
from datetime import datetime, timedelta
from typing import Dict, Any
from praw import Reddit
from dotenv import load_dotenv
import pandas as pd

# reddit attribute names to preferred names
attributes: Dict[str, str] = {
    "subreddit": "subreddit",
    "name": "id",
    "created_utc": "timestamp",
    "permalink": "permalink",
    "link_flair_text": "tag",
    "title": "title",
    "selftext": "body",
    "num_comments": "comments",
    "score": "score",
}


class RedditClient:
    """A class for interacting with the Reddit API to fetch posts"""

    def __init__(self) -> None:
        """Initializes the RedditClient"""
        load_dotenv()
        self.reddit = Reddit(
            client_id=getenv("CLIENT_ID"),
            client_secret=getenv("CLIENT_SECRET"),
            user_agent=getenv("USER_AGENT"),
        )

    def _get_relevant_data(self, submission: Any) -> Dict[str, Any]:
        """Extracts relevant attributes from a submission object"""
        return {key: getattr(submission, key, "") for key in attributes}

    def get_new_posts(self, subreddit_name: str, limit: int = 5) -> pd.DataFrame:
        """Fetches new posts from a specified subreddit"""
        subreddit = self.reddit.subreddit(subreddit_name)
        top_posts = subreddit.new(limit=limit)
        post_dicts = [self._get_relevant_data(post) for post in top_posts]
        post_df = pd.DataFrame(post_dicts, columns=attributes)
        post_df.columns = list(attributes.values())
        return post_df

    def get_weekly_posts(self, subreddit_name: str) -> pd.DataFrame:
        """Fetches posts from the past week from a specified subreddit"""
        subreddit = self.reddit.subreddit(subreddit_name)
        cutoff_date = datetime.now() - timedelta(days=7)
        posts_df = pd.DataFrame(columns=attributes)

        for submission in subreddit.new(limit=10000):
            data = self._get_relevant_data(submission)
            submission_date = datetime.fromtimestamp(data["created_utc"])
            if submission_date < cutoff_date:
                break
            posts_df = pd.concat([posts_df if not posts_df.empty else None, pd.DataFrame([data])])

        posts_df.columns = list(attributes.values())
        posts_df.reset_index(drop=True, inplace=True)
        return posts_df
