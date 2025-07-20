import streamlit as st

# Function to display YouTube video using Pytube
def display_youtube_video(video_url):
    try:
        st.video(video_url)
    except Exception as e:
        st.error(f"An error occurred: {e}")


# Define YouTube video URLs (you can replace these with your desired video URLs)
channels = [
    {"id": "123", "name": "GEO", "url": "https://www.youtube.com/watch?v=Z7B6CZJLEtI?autoplay=1"}
]
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

# Display videos in a 3-column grid
col1, col2, col3 = st.columns(3)

with col1:
    display_youtube_video(channels[0])

with col2:
    display_youtube_video(channels[1])

with col3:
    display_youtube_video(channels[2])

with col1:
    display_youtube_video(channels[3])

with col2:
    display_youtube_video(channels[4])

with col3:
    display_youtube_video(channels[5])
