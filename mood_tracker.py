import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

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