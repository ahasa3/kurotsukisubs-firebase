import pyrebase
config = {
    "apiKey": "AIzaSyCVgnAcgG_4ak4FggEP5r-6JDki24lXDj0",
    "authDomain": "kurotsukisubs.firebaseapp.com",
    "projectId": "kurotsukisubs",
    "storageBucket": "kurotsukisubs.firebasestorage.app",
    "messagingSenderId": "688490137077",
    "appId": "1:688490137077:web:089ab14ab5a5a18f7e0cbc",
    "databaseURL": "https://kurotsukisubs-default-rtdb.asia-southeast1.firebasedatabase.app"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

post1 = database.child("1").get().val()
for i in post1:
    print(post1[i])