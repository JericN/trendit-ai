"""Utility functions for the server"""

from os import path
import pandas as pd


def write_to_csv(data: pd.DataFrame, file_path: str) -> None:
    """Writes data to a CSV file, appending if the file already exists"""
    if path.isfile(file_path) and path.getsize(file_path) > 0:
        data.to_csv(file_path, mode="a", index=False, header=False)
    else:
        data.to_csv(file_path, mode="a", index=False, header=True)


def read_subreddit_list() -> list[str]:
    """Reads a list of subreddits from a file"""
    with open("subreddits.txt", "r", encoding="utf-8") as file:
        return [sub.strip() for sub in file.readlines()]


# FIXME: only read the post last month
def read_subreddit_posts(subreddit: str) -> pd.DataFrame:
    """Reads posts from a CSV file"""
    return pd.read_csv(f"./data/{subreddit}.csv")
