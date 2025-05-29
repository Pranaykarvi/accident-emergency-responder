import pyrebase
import streamlit as st
import webbrowser

from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env

firebaseConfig = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
    "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID"),
}



firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

def login(email: str, password: str):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return user
    except Exception:
        return None

def signup(email: str, password: str):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        send_verification_email(user)
        return user
    except Exception:
        return None

def send_verification_email(user):
    try:
        auth.send_email_verification(user['idToken'])
    except Exception:
        pass

def login_ui():
    st.subheader("Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        user = login(email, password)
        if user:
            st.success(f"Logged in as {email}")
            st.session_state["user"] = user
            st.session_state["auth_method"] = "email"
            st.rerun()  # <- updated here
        else:
            st.error("Login failed: Check your credentials.")

def signup_ui():
    st.subheader("Sign Up")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")

    if st.button("Sign Up"):
        user = signup(email, password)
        if user:
            st.success("User created! Verification email sent.")
        else:
            st.error("Signup failed. Try again.")

# def google_login_ui():
#     st.subheader("Login with Google")

#     if st.button("Login with Google"):
#         google_auth_url = f"https://{firebaseConfig['authDomain']}/__/auth/handler"
#         st.info("Opening Google login page in your browser...")
#         webbrowser.open(google_auth_url)
#         st.write("After logging in with Google, copy the ID token from the browser console and paste below.")

#     id_token = st.text_input("Paste your Google ID Token here:")

#     if id_token:
#         try:
#             user = auth.sign_in_with_custom_token(id_token)
#             st.success("Google login successful!")
#             st.session_state["user"] = user
#             st.session_state["auth_method"] = "google"
#             st.experimental_rerun()
#         except Exception as e:
#             st.error(f"Google authentication failed: {e}")

def logout():
    if st.sidebar.button("Logout"):
        st.session_state.pop("user", None)
        st.session_state.pop("auth_method", None)
        st.experimental_rerun()

def is_logged_in():
    return "user" in st.session_state
