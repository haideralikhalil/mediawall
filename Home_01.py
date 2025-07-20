import streamlit as st 

st.set_page_config(
    page_title="Media Wall",   
    page_icon="📺",
    layout="wide"
    )


st.title("Media Wall")
def login_screen():
    st.header("This app is private.")
    st.subheader("Please log in.")
    st.button("Log in with Google", on_click=st.login)

if not st.user.is_logged_in:
    login_screen()
else:
   
    st.header(f"Welcome, {st.user.name}!")
    st.subheader(f"{st.user.email}!")
    
st.sidebar.success("Welcome to Live TV App!")