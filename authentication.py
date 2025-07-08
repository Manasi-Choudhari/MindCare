import streamlit as st
import pandas as pd
import hashlib
import os

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_login(username, password):
    if os.path.exists("users.csv"):
        df = pd.read_csv("users.csv")
        hashed = hash_password(password)
        return any((df["username"] == username) & (df["password"] == hashed))
    return False

def register_user(username, password):
    hashed = hash_password(password)
    df = pd.read_csv("users.csv") if os.path.exists("users.csv") else pd.DataFrame(columns=["username", "password"])
    if username in df["username"].values:
        return False
    df = pd.concat([df, pd.DataFrame([{"username": username, "password": hashed}])], ignore_index=True)
    df.to_csv("users.csv", index=False)
    return True

def login_register():
    st.title("🔐 Login / Register")
    choice = st.radio("Login or Register?", ["Login", "Register"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Login":
        if st.button("Login"):
            if check_login(username, password):
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.success(f"Welcome {username}!")
                st.rerun()
            else:
                st.error("Invalid credentials.")
    else:
        if st.button("Register"):
            if register_user(username, password):
                st.success("Registration successful! Please log in.")
            else:
                st.warning("Username already exists.")