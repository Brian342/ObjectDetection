import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth


def auth():
    st.title('Welcome to :grey[WakeApp]')

    choose = st.selectbox('Login/SignUp', ['Login', 'Sign Up'])
    if choose == 'Login':
        email = st.text_input('Email address')
        password = st.text_input('Password', type='password')

        st.button('Login')

    else:
        email = st.text_input('Email address')
        password = st.text_input('Password', type='password')
        user  = st.text_input('Enter your Unique UserName')
        st.button('Create Account')

