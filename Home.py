import streamlit as st
from streamlit.components.v1 import html
from urllib.parse import urlparse
from google.cloud import firestore
from pytube import YouTube
from google.cloud import firestore
from google.oauth2 import service_account
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

st.set_page_config(
    page_title="Media Wall",   
    page_icon="📺",
    layout="wide"
    )

if 'user_name' in st.session_state:
    st.sidebar.subheader(st.session_state['user_name'])
else:
    st.sidebar.subheader("Logged in as Guest")

channels = []
with tempfile.NamedTemporaryFile(suffix='.json', mode='w', delete=False) as tmp:
                json.dump(firebase_creds, tmp)
                tmp_path = tmp.name
db = firestore.Client.from_service_account_json(tmp_path)

def get_channels_from_db(collection_name="default"):
    st.session_state.channels = []
    user_ref = db.collection(collection_name)
    for doc in user_ref.stream():
        channel = {
            "name": doc.to_dict().get('name'),
            "url": doc.to_dict().get('url')
        }
        st.session_state.channels.append(channel)

if 'user_name' in st.session_state:
    get_channels_from_db(st.session_state['user_email'])
else:
    get_channels_from_db()

def display_youtube_video(channel):
    try:
        url = channel['url']
        video_id = url.split("v=")[1].split("&")[0]
        embed_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1"
        st.video(embed_url)
    except Exception as e:
        st.error(f"An error occurred: {e}")

def display_youtube_video_01(channel):
    try:
        st.video(channel['url'])
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Function to validate YouTube URL
def is_valid_youtube_url(url):
    parsed = urlparse(url)
    return parsed.netloc in ['www.youtube.com', 'youtube.com', 'youtu.be']

st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
        .stVideo {
            border-radius: 10px;
            height: calc(100vh / 3 - 5px) !important;
        }
        .stVideo iframe {
            height: 100% !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Display videos in a responsive grid
cols = st.columns(3)  # 3-column layout

for i, channel in enumerate(st.session_state.channels):
    with cols[i % 3]:
        try:
            display_youtube_video(channel)
        except Exception as e:
            st.error(f"Error displaying {channel}: {str(e)}")

