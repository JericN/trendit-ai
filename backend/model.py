"""Model class for the BERTopic model"""

from utils import read_subreddit_posts

import pandas as pd
from os import getenv
from dotenv import load_dotenv
import re

# OpenAI Library
import torch
import tiktoken
from openai import OpenAI as OpenAI_client
from umap import UMAP
from hdbscan import HDBSCAN
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired, OpenAI
from bertopic.vectorizers import ClassTfidfTransformer

PROMPT = """
You are a helpful, respectful and honest assistant for labeling topics.

Given this example input:
I have a topic that contains the following documents:
 - Traditional diets in most cultures were primarily plant-based with a little meat on top, but with the rise of industrial style meat production and factory farming, meat has become a staple food.
 - Meat, but especially beef, is the word food in terms of emissions.
 - Eating meat doesn't make you a bad person, not eating meat doesn't make you a good one.
The topic is described by the following keywords: 'meat, beef, eat, eating, emissions, steak, food, health, processed, chicken'.
Based on the information about the topic above, please create a short label of this topic. Make sure you to only return the label and nothing more.

Your reply as the assistant is:
topic: Environmental impacts of eating meat.

Given the example above, now do this:
I have a topic that contains the following documents:
[DOCUMENTS]
The topic is described by the following keywords: [KEYWORDS]

Based on the information above, extract a short but highly descriptive topic label of at most 10 words. Make sure it is in the following format:
topic: <topic label>
"""


class Model:
    """Model class for the BERTopic model"""

    def _init_embedding_layer(self):
        return SentenceTransformer("thenlper/gte-small", trust_remote_code=True)

    def _init_dimensionality_reduction_layer(self):
        return UMAP(n_neighbors=5, n_components=3, min_dist=0.0, metric="cosine", random_state=21522)

    def _init_clustering_layer(self):
        return HDBSCAN(min_cluster_size=20, min_samples=1, metric="euclidean", cluster_selection_method="leaf", prediction_data=True)

    def _init_vectorizer_layer(self):
        return CountVectorizer(stop_words="english", min_df=2, ngram_range=(1, 2))

    def _init_topic_representation_layer(self):
        return ClassTfidfTransformer(reduce_frequent_words=True)

    def _init_topic_finetuning_layer(self, openai_client):
        keybert_model = KeyBERTInspired(top_n_words=10)
        openai_tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")
        openai_model = OpenAI(openai_client, model="gpt-3.5-turbo", exponential_backoff=True, chat=True, prompt=PROMPT, nr_docs=10, doc_length=200, tokenizer=openai_tokenizer)
        return {
            "KeyBERT": keybert_model,
            "OpenAI": [keybert_model, openai_model],
        }

    def __init__(self):
        load_dotenv()
        openai_client = OpenAI_client(api_key=getenv("OPENAI_API_KEY"))

        self.model = BERTopic(
            embedding_model=self._init_embedding_layer(),
            umap_model=self._init_dimensionality_reduction_layer(),
            hdbscan_model=self._init_clustering_layer(),
            vectorizer_model=self._init_vectorizer_layer(),
            ctfidf_model=self._init_topic_representation_layer(),
            representation_model=self._init_topic_finetuning_layer(openai_client),
            top_n_words=10,
            verbose=True,
        )

        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful, respectful and honest assistant for labeling topics from reddit posts."},
                {"role": "user", "content": "Hello! are you ready?"},
            ],
        )

        print("[MODEL] ", response.choices[0].message.content)

    def _preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Import the scraped data"""

        data.fillna("", inplace=True)
        data["doc"] = data.apply(lambda row: f"{row['title']} {row['body']}", axis=1)
        data["doc"] = data["doc"].str.replace(r"(http|www)\S+", "", regex=True)
        data["doc"] = data["doc"].str.replace(r" +", " ")
        data["doc"] = data["doc"].str.strip()

        return (data["title"], data["doc"])

    def fit_transform(self, subreddit: str) -> pd.DataFrame:
        """Fit the model on the scraped data"""

        data = read_subreddit_posts(subreddit)
        print(data)
        titles, docs = self._preprocess_data(data)
        topics, probs = self.model.fit_transform(docs)
        print(topics)
        print(probs)
        print(self.model.get_topic_info())
        return self.model.get_topic_info()
