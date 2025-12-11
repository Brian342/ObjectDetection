import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, _apps, exceptions
import json
import os

LOCAL_KEY_PATH = "wakeapp-51082-firebase-adminsdk-fbsvc-97a897121b.json"

if "FIREBASE_SERVICE_ACCOUNT_JSON" in st.secrets:
    st.info("Using Streamlit Secrets for Firebase Connection.")
    try:
        service_account_info = json.loads(st.secrets["FIREBASE_SERVICE_ACCOUNT_JSON"])
        cred = credentials.Certificate(service_account_info)
    except Exception as e:
        st.error(f"Error loading JSON from secrets. Check your .streamlit/secrets.toml file. Error: {e}")
        st.stop()
else:
    st.info("Using Local file path for Firebase Connection")
    try:
        cred = credentials.Certificate(LOCAL_KEY_PATH)
    except FileNotFoundError:
        st.error(f"FATAL ERROR: Local key file not found at {LOCAL_KEY_PATH}. Ensure the path is correct.")
        st.stop()

# Initialize the app with the credentials
if not _apps:
    try:
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Firebase Initialization Failed: {e}")
        st.stop()


def credential():
    st.title('Welcome to :blue[WakeApp]')

    choose = st.selectbox('Login/SignUp', ['Login', 'Sign Up'])

    if choose == 'Login':
        email = st.text_input('Email address', key='login_email')
        password = st.text_input('Password', type='password', key='login_password')

        if st.button('Login'):
            if not email or not password:
                st.warning("Email and Password are required.")
                return

            try:
                # This checks existence, not password validity!
                auth.get_user_by_email(email)
                st.success("Login Successful (User found in database)!")
            except firebase_admin.exceptions.NotFoundError:
                st.error('Login Failed: User not found.')
            except Exception as e:
                st.error(f'Login Failed due to an error: {e}')

    else:  # Sign Up
        email = st.text_input('Email address', key='signup_email')
        password = st.text_input('Password', type='password', key='signup_password')
        userName = st.text_input('Enter your Unique UserName', key='signup_username')

        if st.button('Create Account'):
            if not all([email, password, userName]):
                st.warning("All fields are required to create an account.")
                return

            try:
                # Auth.create_user handles the signup
                auth.create_user(email=email, password=password, uid=userName)

                st.success('Account Created Successfully!')
                st.markdown('Please Login Using Your Email and Password!')
                st.balloons()

            except firebase_admin.exceptions.EmailAlreadyExistsError:
                st.error("Account Creation Failed: This email address is already in use.")
            except firebase_admin.exceptions.InvalidPasswordError:
                st.error("Account Creation Failed: Password must be at least 6 characters long.")
            except Exception as e:
                st.error(f"Account Creation Failed: {e}")