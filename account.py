import firebase_admin
import streamlit as st
from firebase_admin import auth

if not firebase_admin._apps:
    # os.environ["GOOGLE_CLOUD_PROJECT"] = "wakeapp-51082"
    # cred = credentials.Certificate('/Users/briankimanzi/Documents/programmingLanguages/PythonProgramming/ObjectDetection/wakeapp-51082-a620b5257b0c.json')
    firebase_admin.initialize_app(options={"project_id": "wakeapp-51082"})


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
