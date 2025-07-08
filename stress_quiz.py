import streamlit as st

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