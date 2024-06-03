"""Model class for the BERTopic model"""

from utils import read_subreddit_posts

import pandas as pd
from os import getenv
from dotenv import load_dotenv
import re
from datetime import datetime
from typing import List, Dict

# OpenAI Library
import torch
import tiktoken
from openai import OpenAI as OpenAI_client
from umap import UMAP
from hdbscan import HDBSCAN
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired, OpenAI, PartOfSpeech
from bertopic.vectorizers import ClassTfidfTransformer

PROMPT = """
You are a helpful, respectful and honest assistant for labeling topics.

Given this example input:
I have a topic that contains the following documents:
 - Traditional diets in most cultures were primarily plant-based with a little meat on top, but with the rise of industrial style meat production and factory farming, meat has become a staple food.
 - Meat, but especially beef, is the word food in terms of emissions.
 - Eating meat doesn't make you a bad person, not eating meat doesn't make you a good one.
The topic is described by the following keywords: 'meat, beef, eat, eating, emissions, steak, food, health, processed, chicken'.
Based on the information about the topic above, please create a short but broad and highly encompassing label of this topic, focus on the keywords. Make sure you to only return the label and nothing more.

Your reply as the assistant is:
topic: Environmental impacts of eating meat.

Given the example above, now do this:
I have a topic that contains the following documents:
[DOCUMENTS]
The topic is described by the following keywords: [KEYWORDS]

Based on the information above, extract a short yet highly encompassing topic label of at most 10 words. Make sure it is in the following format:
topic: <topic label>
"""


class Model:
    """Model class for the BERTopic model"""

    def _init_embedding_layer(self):
        return SentenceTransformer("thenlper/gte-small", trust_remote_code=True)

    def _init_dimensionality_reduction_layer(self):
        return UMAP(n_neighbors=5, n_components=3, min_dist=0.0, metric="cosine", random_state=21522)

    def _init_clustering_layer(self):
        return HDBSCAN(min_cluster_size=15, min_samples=1, metric="euclidean", cluster_selection_method="leaf", prediction_data=True)

    def _init_vectorizer_layer(self):
        return CountVectorizer(stop_words="english", min_df=2, ngram_range=(1, 2))

    def _init_topic_representation_layer(self):
        return ClassTfidfTransformer(reduce_frequent_words=True)

    def _init_topic_finetuning_layer(self, openai_client):
        keybert_model = KeyBERTInspired(top_n_words=10)
        pos_model = PartOfSpeech(top_n_words=10, model="en_core_web_sm")
        openai_tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")
        openai_model = OpenAI(openai_client, model="gpt-3.5-turbo", exponential_backoff=True, chat=True, prompt=PROMPT, nr_docs=10, doc_length=200, tokenizer=openai_tokenizer)
        return {
            "KeyBERT": keybert_model,
            "POS": pos_model,
            "OpenAI": [pos_model, openai_model],
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

        return (data, data["title"], data["doc"])

    def _change_topic_labels(self):
        chatgpt_topic_labels = {topic: " | ".join(list(zip(*values))[0]) for topic, values in self.model.topic_aspects_["OpenAI"].items()}
        chatgpt_topic_labels[-1] = "Outlier Topic"
        self.model.set_topic_labels(chatgpt_topic_labels)

    def _extract_rep_docs(self, docs, n=10) -> pd.DataFrame:
        documents = pd.DataFrame({"Document": docs, "ID": range(len(docs)), "Topic": self.model.topics_})
        repr_docs, a, b, c = self.model._extract_representative_docs(c_tf_idf=self.model.c_tf_idf_, documents=documents, topics=self.model.topic_representations_, nr_repr_docs=n)
        return repr_docs

    def _get_topics_data(self, data: pd.DataFrame, repdocs: pd.DataFrame) -> List[Dict]:
        base_url = "https://www.reddit.com"
        all_topics_data = []
        num_topics = min(10, len(self.model.get_topic_info()) - 1)

        for i in range(num_topics):
            topics = self.model.get_topic(i, full=True)
            label = topics["OpenAI"][0][0]
            keywords = [topics["POS"][j][0] for j in range(10)]
            doc_count = self.model.get_topic_freq(i)
            rep_docs = [{"content": data.loc[data["doc"] == doc, "title"].values[0], "url": base_url + data.loc[data["doc"] == doc, "permalink"].values[0]} for doc in repdocs[i]]

            # Append the topic data to the results list
            topic_data = {"label": label, "keywords": keywords, "doc_count": doc_count, "rep_docs": rep_docs}
            all_topics_data.append(topic_data)

        return all_topics_data

    def generate_monthly_result(self, subreddit: str) -> Dict:
        """Fit the model on the scraped data"""
        # if subreddit is funny&gaming, split this and read the data and combine
        if "&" in subreddit:
            subreddits = subreddit.split("&")
            data = pd.concat([read_subreddit_posts(subreddit) for subreddit in subreddits])
        else:
            data = read_subreddit_posts(subreddit)
        print("[MODEL] Preprocessing data")
        data, titles, docs = self._preprocess_data(data)

        print("[MODEL] Fitting model")
        topics, probs = self.model.fit_transform(docs)

        print("[MODEL] Changing topic labels")
        self._change_topic_labels()

        print("[MODEL] Extracting representative documents")
        repr_docs = self._extract_rep_docs(docs)

        print("[MODEL] Getting results")
        topics_data = self._get_topics_data(data, repr_docs)

        date = "May 2024"
        doc_count = len(data)

        return {"date": date, "doc_count": doc_count, "topics": topics_data}
