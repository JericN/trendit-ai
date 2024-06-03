"""Firebase client to interact with the firestore database"""

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class FirebaseClient:
    """Firebase client to interact with the firestore database"""

    def __init__(self, app_name: str):
        self.firebase = firebase_admin.initialize_app(credentials.Certificate("../credentials/firebase.json"), name=app_name)
        self.db = firestore.client(firebase_admin.get_app(name=app_name))

    def upload_data(self, data: dict, subreddit: str) -> None:
        """Uploads data to the firestore database"""
        try:
            _, doc_ref = self.db.collection(subreddit).add(
                {
                    "date": data["date"],
                    "doc_count": data["doc_count"],
                }
            )

            for topic in data["topics"]:
                self.db.collection(subreddit).document(doc_ref.id).collection("topics").add(topic)

            print(f"[INFO] Document added to collection {subreddit}")
        except Exception as _:
            print(f"[Error] Failed uploading data for {subreddit}")
