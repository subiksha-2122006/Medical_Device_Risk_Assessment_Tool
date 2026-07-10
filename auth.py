import streamlit as st

# Temporary users
USERS = {
    "admin": "admin123",
    "student": "student123"
}

def login():

    st.subheader("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if username in USERS and USERS[username] == password:

            st.session_state["logged_in"] = True
            st.session_state["username"] = username

            st.success(
                f"Welcome {username}!"
            )

            st.rerun()

        else:

            st.error(
                "Invalid Username or Password"
            )

def logout():

    st.session_state["logged_in"] = False

    if "username" in st.session_state:
        del st.session_state["username"]

    st.rerun()