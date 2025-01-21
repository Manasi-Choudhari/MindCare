import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import time
import pygame
import subprocess
import random
from nltk.chat.util import Chat, reflections
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Initialize Pygame for games
pygame.init()

# Example data for AI mood prediction
data = [
    ("I am happy today", "Happy"),
    ("I feel really down", "Sad"),
    ("I'm stressed out", "Stressed"),
    ("I feel very calm", "Calm"),
]
texts, labels = zip(*data)
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)
y = labels
model = MultinomialNB()
model.fit(X, y)


# Function to play background music
def play_music():
    audio_file_path = "C:/MENATL_HEALTH/assets/Futuristic Hacker HUD Interface - Login _ + Free After Effects File.mp3"  # Replace with the path to your audio file
    if os.path.exists(audio_file_path):
        st.markdown(
            f"""<audio autoplay loop>
                <source src="data:audio/mpeg;base64,{get_audio_base64(audio_file_path)}" type="audio/mpeg">
            </audio>""",
            unsafe_allow_html=True,
        )
    else:
        st.warning("Audio file not found! Please check the path.")


# Helper function to convert audio file to base64
def get_audio_base64(file_path):
    import base64
    with open(file_path, "rb") as audio_file:
        return base64.b64encode(audio_file.read()).decode()




# Mood Tracker
def log_mood():
    st.title("🌈 Mood Tracker")
    st.write("Track your emotions and observe trends over time.")
    mood = st.selectbox(
        "How do you feel today?", ["Happy", "Sad", "Stressed", "Anxious", "Calm", "Angry"]
    )
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


# Guided Breathing Exercise
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


# Simple Pygame Game
import streamlit.components.v1 as components

def embedded_game():
    st.title("Relaxing Game 🎮")
    st.write("Play the game to unwind and have some fun!")

    if st.button("Launch Game"):
        # Launch the Pygame script
        subprocess.Popen(["python", "py_game.py"])



# Mental Health Chatbot
def chatbot():
    st.title("🤖 Mental Health Chatbot")
    st.write("Chat with our AI bot to share your feelings.")
    pairs = [
        (r"Hi|Hello", ["Hello! How are you today?"]),
        (r"I'm feeling (.*)", ["I'm sorry to hear that. How can I help you?"]),
        (r"(.*) stress", ["Stress can be overwhelming. Would you like some relaxation tips?"]),
        (r"(.*) help(.*)", ["I'm here to listen. Feel free to share your feelings."]),
        (r"quit", ["Goodbye! Stay strong."]),
    ]
    chat = Chat(pairs, reflections)

    user_input = st.text_input("You: ", "")
    if user_input:
        response = chat.respond(user_input)
        st.write(f"Chatbot: {response}")


# Gratitude Journal
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


# Stress Assessment Quiz
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


# AI Mood Prediction
def predict_mood():
    st.title("🔮 AI Mood Prediction")
    user_input = st.text_input("Describe how you're feeling:", "")
    if user_input:
        prediction = model.predict(vectorizer.transform([user_input]))[0]
        st.write(f"Predicted Mood: {prediction}")
        suggestions = {
            "Happy": "Keep spreading positivity! Try sharing your gratitude in the journal.",
            "Sad": "It's okay to feel this way. Try a guided breathing exercise or talk to someone you trust.",
            "Stressed": "Take a break and relax. Try the breathing exercise or play the relaxing game.",
            "Calm": "Enjoy the peace. Consider writing in your gratitude journal.",
        }
        st.write(suggestions.get(prediction, "Take care of yourself!"))


# Main menu
def main():
    play_music()
    st.sidebar.title("🌟 Mental Health Toolkit")
    options = st.sidebar.radio(
        "Select a Tool:",
        [
            "Mood Tracker",
            "Guided Breathing Exercise",
            "Mental Health Chatbot",
            "Gratitude Journal",
            "Stress Assessment Quiz",
            "AI Mood Prediction",
            "Relaxing Game",
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
        predict_mood()
    elif options == "Relaxing Game":
        embedded_game()


if __name__ == "__main__":
    main()



