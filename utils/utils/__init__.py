if results.pose_landmarks:
    print("POSE DETECTED")
else:
    print("NO POSE")
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

        angle = calculate_angle(hip, knee, ankle)
        print("ANGLE:", angle)  # DEBUG

        h, w, _ = image.shape

        cv2.putText(image, str(int(angle)),
                    tuple(np.multiply(knee, [w, h]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0,255,0), 3)

except Exception as e:
    print("ERROR:", e)