import streamlit as st
import streamlit as st
from streamlit.components.v1 import html
from urllib.parse import urlparse
from google.cloud import firestore
from pytube import YouTube

st.set_page_config(
    page_title="Media Wall",   
    page_icon="📺",
    layout="wide"
    )

channels = []

db = firestore.Client.from_service_account_json('key.json')
# Initialize session state for channels

def get_channels_from_db():
    user_ref = db.collection(st.user.email)
    for doc in user_ref.stream():
        channel = {
            "name": doc.to_dict().get('name'),
            "url": doc.to_dict().get('url')
        }
        st.session_state.channels.append(channel)
    

if 'channels' not in st.session_state:
    st.session_state.channels = []
    if st.user.is_logged_in:
        get_channels_from_db()
    else:
        st.session_state.channels = [
                {"name": "DW News", "url": "https://www.youtube.com/watch?v=LuKwFajn37U"},
                {"name": "GEO News", "url": "https://www.youtube.com/watch?v=O3DPVlynUM0"},
                {"name": "ARY TV", "url": "https://www.youtube.com/watch?v=RqUZ2Fv9l8w"},
                {"name": "AAJ News", "url": "https://www.youtube.com/watch?v=2Gub8-cSH9c"},
                {"name": "SAMAA", "url": "https://www.youtube.com/watch?v=fB6Z4q01uFU"},
                {"name": "Aljazeera", "url": "https://www.youtube.com/watch?v=gCNeDWCI0vo"},
            ]
    
def display_youtube_video(channel):
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
            #st.caption(channel)
        except Exception as e:
            st.error(f"Error displaying {channel}: {str(e)}")

