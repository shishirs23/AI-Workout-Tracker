import streamlit as st
import cv2
import mediapipe as mp

st.title("💪 AI Workout Tracker")

run = st.checkbox('Start Camera')

FRAME_WINDOW = st.image([])

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

cap = cv2.VideoCapture(0)

while run:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    if results.pose_landmarks:
        mp.solutions.drawing_utils.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

    FRAME_WINDOW.image(frame)

cap.release()