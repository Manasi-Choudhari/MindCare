# -------------------- Imports and Setup --------------------
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import time
import pygame
import random
import base64
import cv2
import numpy as np
import hashlib
from PIL import Image
from tensorflow.keras.models import load_model
import google.generativeai as genai
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

pygame.init()
GEMINI_API_KEY = "AIzaSyBwmRt-EhrKstoWNcdFI3-Bi1lbSuIncCU"
genai.configure(api_key=GEMINI_API_KEY)

# -------------------- Authentication --------------------
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

# -------------------- Audio --------------------
def get_audio_base64(file_path):
    with open(file_path, "rb") as audio_file:
        return base64.b64encode(audio_file.read()).decode()

def play_music():
    audio_file_path = "C:/MENATL_HEALTH/assets/peace.mp3"
    if os.path.exists(audio_file_path):
        st.markdown(
            f"""<audio autoplay loop>
                <source src="data:audio/mpeg;base64,{get_audio_base64(audio_file_path)}" type="audio/mpeg">
            </audio>""",
            unsafe_allow_html=True,
        )
    else:
        st.warning("Audio file not found! Please check the path.")

# -------------------- Mood Tracker --------------------
def log_mood():
    st.title("🌈 Mood Tracker")
    st.write("Track your emotions and observe trends over time.")
    mood = st.selectbox("How do you feel today?", ["Happy", "Sad", "Stressed", "Anxious", "Calm", "Angry"])
    notes = st.text_area("Any additional notes?", "")
    if st.button("Log Mood"):
        df = pd.read_csv("mood_log.csv") if os.path.exists("mood_log.csv") else pd.DataFrame(columns=["Date", "Mood", "Notes"])
        new_entry = {"Date": pd.to_datetime("today").strftime("%Y-%m-%d"), "Mood": mood, "Notes": notes}
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv("mood_log.csv", index=False)
        st.success("Mood logged successfully!")

    if os.path.exists("mood_log.csv"):
        df = pd.read_csv("mood_log.csv")
        df["Date"] = pd.to_datetime(df["Date"])
        mood_count = df.groupby("Mood").size().reset_index(name="Counts")

        st.subheader("Mood Trends")
        col1, col2 = st.columns(2)

        with col1:
            plt.figure(figsize=(5, 3))
            plt.bar(mood_count["Mood"], mood_count["Counts"], color="skyblue")
            plt.title("Mood Distribution")
            plt.ylabel("Frequency")
            st.pyplot(plt)

        with col2:
            st.subheader("Weekly Mood Trends")
            df["Week"] = df["Date"].dt.to_period("W").apply(str)
            weekly_trend = df.groupby(["Week", "Mood"]).size().unstack(fill_value=0)
            st.line_chart(weekly_trend)

# -------------------- Guided Breathing --------------------
def guided_exercise():
    st.title("🌬️ Guided Breathing Exercise")
    st.write("Take a few deep breaths to relax. Follow the instructions below:")
    duration = st.slider("Set the duration for each step (in seconds):", min_value=2, max_value=10, value=4)

    if st.button("Start Breathing Exercise"):
        for i in range(5):
            st.markdown(f"<h3 style='text-align: center;'>Breathe In... {i+1}</h3>", unsafe_allow_html=True)
            time.sleep(duration)
            st.markdown(f"<h3 style='text-align: center;'>Hold... {i+1}</h3>", unsafe_allow_html=True)
            time.sleep(duration)
            st.markdown(f"<h3 style='text-align: center;'>Breathe Out... {i+1}</h3>", unsafe_allow_html=True)
            time.sleep(duration)
        st.success("Exercise Completed! Feel free to try again.")

# -------------------- Chatbot --------------------
def chatbot():
    st.title("🤖 Mental Health Chatbot")
    st.write("Chat with our AI bot to share your feelings.")
    user_input = st.text_input("You: ", "")
    if user_input:
        try:
            model = genai.GenerativeModel("gemini-1.5-pro")
            response = model.generate_content(user_input)
            st.write(f"Chatbot: {response.text}")
        except Exception as e:
            st.error(f"Error: {e}")

# -------------------- Gratitude Journal --------------------
def gratitude_journal():
    st.title("🌻 Gratitude Journal")
    entry = st.text_area("Write something you're grateful for:")
    if st.button("Save Entry"):
        if entry:
            df = pd.read_csv("gratitude_journal.csv") if os.path.exists("gratitude_journal.csv") else pd.DataFrame(columns=["Date", "Entry"])
            new_entry = {"Date": pd.to_datetime("today").strftime("%Y-%m-%d"), "Entry": entry}
            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            df.to_csv("gratitude_journal.csv", index=False)
            st.success("Your gratitude entry has been saved!")

    if os.path.exists("gratitude_journal.csv"):
        df = pd.read_csv("gratitude_journal.csv")
        st.write("### Previous Entries")
        st.write(df)

# -------------------- Stress Quiz --------------------
def stress_quiz():
    st.title("🌡️ Stress Assessment Quiz")
    questions = [
        "Do you feel overwhelmed frequently?",
        "Are you having trouble sleeping?",
        "Do you find it difficult to concentrate?",
        "Do you often feel anxious or irritable?",
    ]
    answers = []
    for question in questions:
        answer = st.radio(question, options=["Yes", "No"], key=question)
        answers.append(answer)

    if st.button("Submit Quiz"):
        score = answers.count("Yes")
        st.write(f"Your Stress Level: {score}/4")
        if score >= 3:
            st.warning("It looks like you're feeling stressed. Consider relaxation techniques or professional help.")
        else:
            st.success("You're managing stress well. Keep up the good work!")

# -------------------- AI Mood Prediction --------------------
def ai_mood_prediction():
    st.title("😊 AI-Based Emotion Detection 🎭")
    st.write("Upload an image or use your webcam to detect emotions!")

    MODEL_PATH = "emotion_model.h5"
    model = load_model(MODEL_PATH)
    class_names = ["angry", "disgusted", "fearful", "happy", "neutral", "sad", "surprised"]
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        img_array = np.array(image)
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (48, 48))
            face = np.expand_dims(face, axis=0)
            face = np.expand_dims(face, axis=-1) / 255.0
            prediction = model.predict(face)
            emotion_label = class_names[np.argmax(prediction)]
            cv2.rectangle(img_array, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(img_array, emotion_label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        result_image = Image.fromarray(img_array)
        st.image(result_image, caption=f"Detected Emotion: {emotion_label}", use_column_width=True)

    st.write("OR")
    st.write("Press the button below to start webcam emotion detection!")

    if st.button("Start Webcam"):
        cap = cv2.VideoCapture(0)
        FRAME_WINDOW = st.image([])

        while True:
            ret, frame = cap.read()
            if not ret:
                st.error("Failed to capture video.")
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                face = gray[y:y+h, x:x+w]
                face = cv2.resize(face, (48, 48))
                face = np.expand_dims(face, axis=0)
                face = np.expand_dims(face, axis=-1) / 255.0
                prediction = model.predict(face)
                emotion_label = class_names[np.argmax(prediction)]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, emotion_label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            FRAME_WINDOW.image(frame)

        cap.release()

# -------------------- Community Forum --------------------
def community_page():
    st.title("🗣️ Community Forum")
    st.write("Welcome to the mental health community space. Share thoughts, advice, or supportive messages.")
    name = st.text_input("Your Name")
    message = st.text_area("What's on your mind?")
    if st.button("Post"):
        if name and message:
            df = pd.read_csv("community_posts.csv") if os.path.exists("community_posts.csv") else pd.DataFrame(columns=["Timestamp", "Name", "Message", "Likes"])
            new_post = {
                "Timestamp": pd.to_datetime("now").strftime("%Y-%m-%d %H:%M:%S"),
                "Name": name.strip(),
                "Message": message.strip(),
                "Likes": 0
            }
            df = pd.concat([df, pd.DataFrame([new_post])], ignore_index=True)
            df.to_csv("community_posts.csv", index=False)
            st.success("Message posted!")
            st.rerun()
        else:
            st.warning("Please enter both name and message.")

    posts_df = pd.read_csv("community_posts.csv") if os.path.exists("community_posts.csv") else pd.DataFrame(columns=["Timestamp", "Name", "Message", "Likes"])
    replies_df = pd.read_csv("community_replies.csv") if os.path.exists("community_replies.csv") else pd.DataFrame(columns=["PostTimestamp", "Replier", "Reply"])

    if not posts_df.empty:
        st.subheader("📝 Recent Posts")
        posts_df = posts_df.sort_values(by="Timestamp", ascending=False)

        for idx, row in posts_df.iterrows():
            st.markdown("---")
            st.markdown(f"**{row['Name']}** *({row['Timestamp']})*")
            st.markdown(f"> {row['Message']}")

            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("👍", key=f"like_{idx}"):
                    posts_df.at[idx, "Likes"] += 1
                    posts_df.to_csv("community_posts.csv", index=False)
                    st.rerun()
            with col2:
                st.write(f"Likes: {row['Likes']}")

            post_replies = replies_df[replies_df["PostTimestamp"] == row["Timestamp"]]
            for _, reply in post_replies.iterrows():
                st.markdown(f"↪️ **{reply['Replier']}**: {reply['Reply']}")

            with st.expander("💬 Reply"):
                replier = st.text_input(f"Reply Name {idx}", label_visibility="collapsed", placeholder="Your name")
                reply_text = st.text_area(f"Reply Text {idx}", label_visibility="collapsed", placeholder="Your reply...")
                if st.button(f"Post Reply {idx}"):
                    if replier.strip() and reply_text.strip():
                        new_reply = {
                            "PostTimestamp": row["Timestamp"],
                            "Replier": replier.strip(),
                            "Reply": reply_text.strip()
                        }
                        replies_df = pd.concat([replies_df, pd.DataFrame([new_reply])], ignore_index=True)
                        replies_df.to_csv("community_replies.csv", index=False)
                        st.success("Reply posted!")
                        st.rerun()

# -------------------- Main --------------------
def main():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        login_register()
        return

    play_music()
    st.sidebar.title("🌟 Mental Health Toolkit")
    st.sidebar.markdown(f"Logged in as: **{st.session_state['username']}**")
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.session_state["username"] = ""
        st.rerun()

    options = st.sidebar.radio(
        "Select a Tool:",
        [
            "Mood Tracker",
            "Guided Breathing Exercise",
            "Mental Health Chatbot",
            "Gratitude Journal",
            "Stress Assessment Quiz",
            "AI Mood Prediction",
            "Community Forum"
        ],
    )

    if options == "Mood Tracker":
        log_mood()
    elif options == "Guided Breathing Exercise":
        guided_exercise()
    elif options == "Mental Health Chatbot":
        chatbot()
    elif options == "Gratitude Journal":
        gratitude_journal()
    elif options == "Stress Assessment Quiz":
        stress_quiz()
    elif options == "AI Mood Prediction":
        ai_mood_prediction()
    elif options == "Community Forum":
        community_page()

if __name__ == "__main__":
    main()

