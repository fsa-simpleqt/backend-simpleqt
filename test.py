import os
from dotenv import load_dotenv

import firebase_admin
from firebase_admin import credentials, storage, db

from app.modules.question_retrieval.models.get_question import get_question


if __name__ == "__main__":
    # storageBucket = "fsa-firebase-tutorial.appspot.com"
    # databaseURL = "https://fsa-firebase-tutorial-default-rtdb.asia-southeast1.firebasedatabase.app/"

    # cred = credentials.Certificate('credentials\\fsa-firebase-database.json')
    # # firebase_admin.initialize_app(cred, {
    # #     'storageBucket': storageBucket,
    # #     'databaseURL': databaseURL
    # # })
    get_question("hihi")

