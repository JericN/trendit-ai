import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

app_name = "trenddit"


class FirebaseClient:

    def __init__(self):
        self.firebase = firebase_admin.initialize_app(credentials.Certificate("../credentials/firebase.json"), name=app_name)
        self.db = firestore.client(firebase_admin.get_app(name=app_name))

    def upload_data(self, data: dict, subreddit: str) -> None:
        try:
            doc_ref = self.db.collection(subreddit).add(data)
            print(f"[INFO] Document added to collection {subreddit}")
        except Exception as _:
            print(f"[Error] Failed uploading data for {subreddit}")
