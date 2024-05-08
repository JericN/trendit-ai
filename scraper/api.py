""" This module is responsible for authenticating the Reddit API. """

import requests
from os import getenv
from requests import auth


def get_access_token():
    """Get and print access token from Reddit API."""

    client_auth = auth.HTTPBasicAuth(
        getenv("CLIENT_ID"), getenv("CLIENT_SECRET")
    )

    post_data = {
        "grant_type": "password",
        "username": getenv("REDDIT_USERNAME"),
        "password": getenv("REDDIT_PASSWORD"),
    }

    headers = {"User-Agent": getenv("USER_AGENT")}

    response = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=client_auth,
        data=post_data,
        headers=headers,
        timeout=10,
    )

    print(response.json())


def get_auth_header():
    """ Get the authorization header for Reddit API. """
    return {
        "Authorization": f"{getenv("TOKEN_TYPE")} {getenv("ACCESS_TOKEN")}",
        "User-Agent": getenv("USER_AGENT"),
    }

def get_posts(subreddit, after=None, limit=100):
    """ Get the latest posts from a subreddit. """
    after = None if after == 'initial' else after

    api_url = f"https://oauth.reddit.com/r/{subreddit}/new"
    headers = get_auth_header()
    params = {"limit": limit, "after": after}

    response = requests.get(
        api_url,
        headers=headers,
        params=params,
        timeout=10,
    )

    response.raise_for_status()
    response_json = response.json()
    
    return response_json["data"]
