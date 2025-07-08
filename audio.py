import streamlit as st
import base64
import os

def get_audio_base64(file_path):
    with open(file_path, "rb") as audio_file:
        return base64.b64encode(audio_file.read()).decode()

def play_music():
    audio_file_path = "C:/MENATL_HEALTH/hackorbit/peace.mp3"
    if os.path.exists(audio_file_path):
        st.markdown(
            f"""<audio autoplay loop>
                <source src="data:audio/mpeg;base64,{get_audio_base64(audio_file_path)}" type="audio/mpeg">
            </audio>""",
            unsafe_allow_html=True,
        )
    else:
        st.warning("Audio file not found! Please check the path.")