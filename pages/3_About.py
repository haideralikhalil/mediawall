import streamlit as st 
from st_social_media_links import SocialMediaIcons
st.header("Media Wall")
st.subheader("Developed By Haider Ali")

social_media_links = [
    "https://www.linkedin.com/in/haiderkhalil",
    "https://www.medium.com/@haiderkhalil",
    "https://www.x.com/haiderhalil",
    "https://www.facebook.com/haideralikhalil",
    "https://www.youtube.com/@towncoder",
    "https://www.github.com/haideralikhalil",
    "https://wa.me/00923219032716"
]
social_media_icons = SocialMediaIcons(social_media_links)

social_media_icons.render()  
st.divider()
st.video("https://youtu.be/ZlLtP16jIM4") 
st.image("haider.png", width=400, caption="Haider Ali Khalil"  )      