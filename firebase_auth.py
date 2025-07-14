import pyrebase

firebase_config = {
    "apiKey": "AIzaSyDjdnzGt_qkyruXZCt4PfWYBd4Db35YLAo",
    "authDomain": "wellness-hub-e546c.firebaseapp.com",
    "databaseURL": "https://wellness-hub-e546c-default-rtdb.firebaseio.com",
    "projectId": "wellness-hub-e546c",
    "storageBucket": "wellness-hub-e546c.appspot.com",
    "messagingSenderId": "130696041295",
    "appId": "1:130696041295:web:bb371bf9807f4391d5ab3a",
    "measurementId": "G-Q1YZZ5TCKE"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()

# Login User
def login_user(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return user
    except:
        return None

# Create Account
def create_account(email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        return user
    except:
        return None

# (Optional) Save and Load User Data
def save_user_data(user_email, section, data, user):
    safe_email = user_email.replace(".", "_")
    if user:
        db.child("users").child(safe_email).child(section).push(data, user['idToken'])
    else:
        db.child("users").child(safe_email).child(section).push(data)


def get_user_data(user_email, section, user):
    safe_email = user_email.replace(".", "_")
    result = db.child("users").child(safe_email).child(section).get(user['idToken'])
    return result.val() if result.each() else []

