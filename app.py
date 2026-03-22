import cv2
import mediapipe as mp
import numpy as np
from utils.angles import calculate_angle

# Initialize mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Start camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Variables
counter = 0
stage = None
angle = 0
correct_reps = 0
feedback = ""

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            print("Camera not working")
            break

        # Flip for mirror view
        frame = cv2.flip(frame, 1)

        # Convert to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        results = pose.process(image)

        # Convert back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Draw skeleton
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

        # ===== LOGIC =====
        try:
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark

                hip = [
                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y
                ]

                knee = [
                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y
                ]

                ankle = [
                    landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y
                ]

                # Calculate angle
                angle = calculate_angle(hip, knee, ankle)

                # Stage logic
                if angle > 165:
                    stage = "up"

                if angle < 90 and stage == "up":
                    stage = "down"
                    counter += 1

                    if feedback == "Good Form":
                        correct_reps += 1

                # Posture check
                if angle < 90:
                    if hip[1] < knee[1]:
                        feedback = "Lean Back!"
                    elif knee[0] > ankle[0]:
                        feedback = "Knees too forward!"
                    else:
                        feedback = "Good Form"
                else:
                    feedback = ""

        except Exception as e:
            print("ERROR:", e)

        # ===== UI =====
        overlay = image.copy()
        cv2.rectangle(overlay, (0, 0), (420, 260), (30, 30, 30), -1)
        image = cv2.addWeighted(overlay, 0.6, image, 0.4, 0)

        # Colors
        GREEN = (0, 255, 0)
        RED = (0, 0, 255)
        CYAN = (255, 255, 0)
        WHITE = (255, 255, 255)

        font = cv2.FONT_HERSHEY_DUPLEX

        # Accuracy
        accuracy = (correct_reps / counter * 100) if counter > 0 else 0

        # Text display
        cv2.putText(image, f'Reps: {counter}', (30, 50), font, 0.9, GREEN, 2)
        cv2.putText(image, f'Stage: {stage}', (30, 90), font, 0.9, WHITE, 2)
        cv2.putText(image, f'Accuracy: {accuracy:.1f}%', (30, 130), font, 0.9, CYAN, 2)

        feedback_color = GREEN if feedback == "Good Form" else RED
        cv2.putText(image, f'Feedback: {feedback}', (30, 170), font, 0.9, feedback_color, 2)

        cv2.putText(image, f'Angle: {int(angle)}', (30, 210), font, 0.9, GREEN, 2)

        cv2.putText(image, "Press Q / ESC to exit", (30, 240),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, WHITE, 1)

        # Show window
        cv2.imshow('AI Workout Tracker', image)

        # Exit control
        key = cv2.waitKey(1)
        if key == ord('q') or key == 27:
            break

# Cleanup
cap.release()
cv2.destroyAllWindows()