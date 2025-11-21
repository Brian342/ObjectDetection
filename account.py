import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

cred = credentials.Certificate('wakeapp-51082-fb1600eb10dc.json')
firebase_admin.initialize_app(cred)


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
        userName = st.text_input('Enter your Unique UserName')

        if st.button('Create Account'):
            user = auth.create_user(email=email, password=password, uid=userName)

            st.success('Account Created Successfully!')
            st.markdown('please Login Using Your Email and Password!')
            st.balloons()

