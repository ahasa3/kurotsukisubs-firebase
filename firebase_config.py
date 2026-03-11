import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import json

firebase_key = json.loads(os.environ.get("FIREBASE_KEY"))

cred = credentials.Certificate(firebase_key)
firebase_admin.initialize_app(cred)

db = firestore.client()