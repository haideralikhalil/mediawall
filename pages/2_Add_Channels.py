import streamlit as st
import streamlit as st
from streamlit.components.v1 import html
from urllib.parse import urlparse
from google.cloud import firestore
from pytube import YouTube


db = firestore.Client.from_service_account_json('key.json')

def login_screen():
    st.header("Only Registered Users can add channels.")
    st.button("Log in with Google", on_click=st.login)
    
def is_valid_youtube_url(url):
    parsed = urlparse(url)
    return parsed.netloc in ['www.youtube.com', 'youtube.com', 'youtu.be']

if not st.user.is_logged_in:
    login_screen()
    st.stop()
 
# Initialize session state for channels
if 'channels' not in st.session_state:
    st.session_state.channels = []
st.session_state.channels = []

user_ref = db.collection(st.user.email)

for doc in user_ref.stream():
    st.session_state.channels.append(doc.to_dict())
    #st.write('{} => {}'.format(doc.id, doc.to_dict()))
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
            doc_ref = db.collection(st.user.email).document(video_id)
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


#channels_to_remove = []
#st.session_state.channels=[]
#st.write(st.session_state.channels)
for i, channel in enumerate(st.session_state.channels):
   
    #st.write(channel)
    st.write(f"**{channel['name']}** {channel['url']}")
    #st.write(channel['url'])
    if st.button("🗑️", key=f"delete_{i}"):
        #channels_to_remove.append(i)
        #st.write(st.session_state.channels[i])
        video_id = st.session_state.channels[i]['id']
        user_ref = db.collection(st.user.email)
        user_ref.document(video_id).delete()
        del st.session_state.channels[i]
        st.success("Channel removed!")
        st.rerun()
