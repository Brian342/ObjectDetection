import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth

if not firebase_admin._apps:
    cred = credentials.Certificate('wakeapp-51082-fb1600eb10dc.json')
    firebase_admin.initialize_app(cred, {
        "projectId": "wakeapp-51082",
    })


def authentication():
    st.title('Welcome to :grey[WakeApp]')

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

        st.button('Login', on_click=validate())

    else:
        email = st.text_input('Email address')
        password = st.text_input('Password', type='password')
        userName = st.text_input('Enter your Unique UserName')

        if st.button('Create Account'):
            user = auth.create_user(email=email, password=password, uid=userName)

            st.success('Account Created Successfully!')
            st.markdown('please Login Using Your Email and Password!')
            st.balloons()
