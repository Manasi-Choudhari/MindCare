import streamlit as st
import time

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