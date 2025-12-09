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
    st.info()

# Initialize the app with the credentials
firebase_admin.initialize_app(cred)


def credential():
    st.title('Welcome to :blue[WakeApp]')

    choose = st.selectbox('Login/SignUp', ['Login', 'Sign Up'])

    def validate():
        try:
            user = auth.get_user_by_email(email)
            # print(user.uid)
            st.write("Login Successful")

        except:
            st.warning('Login Failed')

    if choose == 'Login':
        email = st.text_input('Email address')
        password = st.text_input('Password', type='password')

        st.button('Login', on_click=validate)

    else:
        email = st.text_input('Email address')
        password = st.text_input('Password', type='password')
        userName = st.text_input('Enter your Unique UserName')

        if st.button('Create Account'):
            user = auth.create_user(email=email, password=password, uid=userName)

            st.success('Account Created Successfully!')
            st.markdown('please Login Using Your Email and Password!')
            st.balloons()
