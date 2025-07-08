import streamlit as st
import google.generativeai as genai

genai.configure(api_key="AIzaSyDooyq1QXrFVDfiA6pkvciTzL-5tHfaIq8")

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