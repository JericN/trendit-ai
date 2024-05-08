""" This module is responsible for authenticating the Reddit API. """

from os import getenv
import requests
import requests.auth


def get_access_token():
    """Get and print access token from Reddit API."""

    client_auth = requests.auth.HTTPBasicAuth(
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
