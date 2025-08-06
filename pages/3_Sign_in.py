import streamlit as st
from streamlit_google_auth import Authenticate
import tempfile
import json

google_creds = {
    "web":
        {
        "client_id": st.secrets['google_oauth_web']['client_id'],
         "project_id":st.secrets['google_oauth_web']['project_id'],
         "auth_uri":"https://accounts.google.com/o/oauth2/auth",
         "token_uri":"https://oauth2.googleapis.com/token",
         "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
         "client_secret":st.secrets['google_oauth_web']['client_secret'],
         "redirect_uris":["http://localhost:8501/Sign_in"],
         "javascript_origins":["http://localhost:8501"]
        }
    }


#st.title('Streamlit Google Auth')
if 'user_name' in st.session_state:
    st.title('Sign Out')
else:
    st.title("Sign In")
    st.write("You are not logged in, please log in to continue.")    
    
def login_screen():
    if 'connected' not in st.session_state:
        with tempfile.NamedTemporaryFile(suffix='.json', mode='w', delete=False) as tmp:
                json.dump(google_creds, tmp)
                tmp_path = tmp.name
                
        authenticator = Authenticate(
            #secret_credentials_path = 'google_credentials.json',
            secret_credentials_path=tmp_path,
            
            cookie_name='my_cookie_name',
            cookie_key='this_is_secret',
            redirect_uri = 'http://localhost:8501/Sign_in',
        )
        st.session_state["authenticator"] = authenticator

    # Catch the login event
    st.session_state["authenticator"].check_authentification()
   
    # Create the login button
    st.session_state["authenticator"].login()
  
    if st.session_state['connected']:
        st.session_state['user_name'] = st.session_state['user_info'].get('name')
        st.session_state['user_email'] = st.session_state['user_info'].get('email')
        #st.image(st.session_state['user_info'].get('picture'))
        st.write('Hello, '+ st.session_state['user_name'] + ': ' + st.session_state['user_email'])
        if st.button('Log out'):
            del st.session_state.connected, st.session_state.user_name, st.session_state.user_email
            st.session_state["authenticator"].logout()
        
    
login_screen()



