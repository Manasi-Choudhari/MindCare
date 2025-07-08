import streamlit as st
import cv2
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model

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