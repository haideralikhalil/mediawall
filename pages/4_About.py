import streamlit as st 
from st_social_media_links import SocialMediaIcons
st.header("Media Wall")
st.write("Manage and display Live YouTube channels.")

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


st.video("https://www.youtube.com/watch?v=-kyxxdKe9uA") 
st.write("Developed By Haider Ali")
social_media_icons.render()  
st.image("haider.png", width=400, caption="Haider Ali Khalil"  )      