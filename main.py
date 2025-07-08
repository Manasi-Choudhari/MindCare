import streamlit as st
from authentication import login_register
from audio import play_music
from mood_tracker import log_mood
from breathing_exercise import guided_exercise
from chatbot import chatbot
from gratitude_journal import gratitude_journal
from stress_quiz import stress_quiz
from ai_mood_prediction import ai_mood_prediction
from community import community_page

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