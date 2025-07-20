import streamlit as st 

if st.user.is_logged_in:
    st.subheader(f"Welcome, {st.user.name}!")
    if(st.button("Logout")):
        st.logout()
else:
    st.header("Only Registered Users can add channels.")
    st.button("Log in with Google", on_click=st.login)
