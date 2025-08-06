import streamlit as st
from streamlit.components.v1 import html
from urllib.parse import urlparse
from google.cloud import firestore
from pytube import YouTube
from streamlit_google_auth import Authenticate
import tempfile
import json

firebase_creds = {
    "type": "service_account",
  "project_id": st.secrets['firebase']['project_id'],
  "private_key_id": st.secrets['firebase']['private_key_id'],
  "private_key": st.secrets['firebase']['private_key'],
  "client_email": st.secrets['firebase']['client_email'],
  "client_id": st.secrets['firebase']['client_id'],
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40live-tv-channels-9e23c.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

#db = firestore.Client.from_service_account_json('firebase_credentials.json')
with tempfile.NamedTemporaryFile(suffix='.json', mode='w', delete=False) as tmp:
                json.dump(firebase_creds, tmp)
                tmp_path = tmp.name
db = firestore.Client.from_service_account_json(tmp_path)

    
def is_valid_youtube_url(url):
    parsed = urlparse(url)
    return parsed.netloc in ['www.youtube.com', 'youtube.com', 'youtu.be']

def add_channels():
    if 'connected' not in st.session_state:
        st.write("User is not logged in, cannot add channels.")
        return
    
    st.session_state.channels = []

    if 'user_info' in st.session_state:
        user_email = st.session_state['user_email']
    else:
        user_email= "test"
    user_ref = db.collection(user_email)

    for doc in user_ref.stream():
        st.session_state.channels.append(doc.to_dict())
    st.header("Channel Management")


    # Add new channel
    channel_name = st.text_input("Channel Name")
    channel_url = st.text_input("Channel URL")

    channel = { "name": channel_name, "url": channel_url}

    if st.button("Add Channel") and channel_name and channel_url:
        st.write(channel["name"])
        if is_valid_youtube_url(channel_url):
            if channel not in st.session_state.channels:
                yt = YouTube(channel['url'])
                video_id = yt.video_id
                st.session_state.channels.append(channel)
                doc_ref = db.collection(st.session_state['user_email']).document(video_id)
                doc_ref.set({
                    'id': video_id,
                    'name': channel["name"],
                    'url': channel["url"],
                
                })
                st.success("Channel added!")
            else:
                st.warning("Channel already exists in the list")
        else:
            st.error("Please enter a valid YouTube URL")

    for i, channel in enumerate(st.session_state.channels):
        #video_id = st.session_state.channels[i]['id']
        col1, col2 = st.columns([1,1])  # Adjust ratios as needed
        with col1:
            st.write(st.session_state.channels[i]['name'])
        with col2:
            if st.button("🗑️", key=f"delete_{i}"):
                video_id = st.session_state.channels[i]['id']
                user_ref = db.collection(st.session_state['user_email'])
                user_ref.document(video_id).delete()
                del st.session_state.channels[i]
                st.success("Channel removed!")
                st.rerun()
        st.divider()
       


#if not st.user.is_logged_in:
if 'user_name' in st.session_state:
    add_channels() 
else:
    st.subheader("You are not logged in")
    st.write("You must log in to Add Channel!")
    st.markdown("[Sign In](/Sign_in)")
