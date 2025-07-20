import streamlit as st
import streamlit as st
from streamlit.components.v1 import html
from urllib.parse import urlparse
from google.cloud import firestore
from pytube import YouTube


db = firestore.Client.from_service_account_json('key.json')

def login_screen():
    st.header("This app is private.")
    st.subheader("Please log in.")
    st.button("Log in with Google", on_click=st.login)

if not st.user.is_logged_in:
    login_screen()
else:
    with st.sidebar:
        st.header(f"Welcome, {st.user.name}!")
        st.subheader(f"{st.user.email}!")
    
    #st.button("Log out", on_click=st.logout)

# Initialize session state for channels
if 'channels' not in st.session_state:
    st.session_state.channels = []
    user_ref = db.collection(st.user.email)

    for doc in user_ref.stream():
        st.session_state.channels.append(doc.to_dict()['url'])
        #st.write('{} => {}'.format(doc.id, doc.to_dict()))

def display_youtube_video(video_url):
    try:
        st.video(video_url)
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
            height: calc(100vh / 3 - 20px) !important;
        }
        .stVideo iframe {
            height: 100% !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar for channel management
with st.sidebar:
    st.header("Channel Management")
    
   
    # Add new channel
    new_channel = st.text_input("Add new YouTube channel URL:")
    if st.button("Add Channel") and new_channel:
        if is_valid_youtube_url(new_channel):
            if new_channel not in st.session_state.channels:
                yt = YouTube(new_channel)
                video_id = yt.video_id
                st.session_state.channels.append(new_channel)
                doc_ref = db.collection(st.user.email).document(video_id)
                doc_ref.set({
                    'name': 'Test',
                    'url': new_channel,
                
                })
                st.success("Channel added!")
            else:
                st.warning("Channel already exists in the list")
        else:
            st.error("Please enter a valid YouTube URL")
    
    # Display channels with delete buttons
    st.subheader("Your Channels")
    channels_to_remove = []
    
    for i, channel in enumerate(st.session_state.channels):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(channel)
        with col2:
            if st.button("🗑️", key=f"delete_{i}"):
                channels_to_remove.append(i)
    
    # Remove selected channels
    for i in sorted(channels_to_remove, reverse=True):
        if 0 <= i < len(st.session_state.channels):
            del st.session_state.channels[i]
            user_ref = db.collection(st.user.email)
            yt = YouTube(channels_to_remove[i])
            video_id = yt.video_id
            user_ref.document(video_id).delete()


# Display videos in a responsive grid
cols = st.columns(3)  # 3-column layout

for i, channel in enumerate(st.session_state.channels):
    with cols[i % 3]:
        try:
            display_youtube_video(channel)
            #st.caption(channel)
        except Exception as e:
            st.error(f"Error displaying {channel}: {str(e)}")

