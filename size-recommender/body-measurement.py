import cv2
from cvzone.PoseModule import PoseDetector
import math
import time

# Initialize the model and webcam 
detector = PoseDetector()
cap = cv2.VideoCapture(0)

# Initialize variables
initial_pose = None  # Time when the pose is first detected
measurement_list = []  # List to store measurements
stable_pose = False  # Flag to check whether the pose is stable

# Threshold for detecting significant movement
movement_threshold = 200  # To determine significant movement (sensitivity) --> higher more sensitive
previous_landmarks = None  # To compare previous and current landmarks for movement

while True:
    ret, img = cap.read()
    if not ret:
        print ("Failed to grab frame") #Debugging purposes
        break

    # Detect pose
    img = detector.findPose(img)
    lmList, bbox = detector.findPosition(img, draw=True)  # Get landmarks

    if lmList:
        # Get coordinates of important landmarks for shirt and pants sizing
        left_shoulder = lmList[11][:2]  # (x, y) of left shoulder
        right_shoulder = lmList[12][:2]  # (x, y) of right shoulder
        left_hip = lmList[23][:2]  # (x, y) of left hip
        right_hip = lmList[24][:2]  # (x, y) of right hip
        left_ankle = lmList[27][:2]  # (x, y) of left ankle
        right_ankle = lmList[28][:2]  # (x, y) of right ankle

        # Measure shoulder width for shirt sizing
        shoulder_width = math.dist(left_shoulder, right_shoulder)

        # Measure torso height (shoulder to hip) for shirt length
        torso_height = math.dist(left_shoulder, left_hip)

        # Measure hip width (hip to hip) for pants sizing
        hip_width = math.dist(left_hip, right_hip)

        # Measure full leg length (hip to ankle) for pants inseam
        left_leg_length = math.dist(left_hip, left_ankle)
        right_leg_length = math.dist(right_hip, right_ankle)

        # Display measurements for shirt and pants sizing
        cv2.putText(img, f"Shoulder Width: {shoulder_width:.2f} px", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(img, f"Torso Height: {torso_height:.2f} px", (50, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(img, f"Hip Width: {hip_width:.2f} px", (50, 110),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(img, f"Left Leg Length: {left_leg_length:.2f} px", (50, 140),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(img, f"Right Leg Length: {right_leg_length:.2f} px", (50, 170),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Check for movement if previous landmarks exist
        if previous_landmarks is not None:
            # Calculate the Euclidean distance between current and previous landmarks
            movement = 0
            for i in range(11, 29):  # We are interested in the body landmarks
                current_landmark = lmList[i][:2]
                previous_landmark = previous_landmarks[i][:2]
                movement += math.dist(current_landmark, previous_landmark)

            # If the movement is smaller than the threshold, we consider the pose stable
            if movement < movement_threshold:
                if initial_pose is None:
                    initial_pose = time.time()  # Start the timer if the pose is stable
            else:
                initial_pose = None  # Reset the timer if there's movement

        previous_landmarks = lmList  # Update previous landmarks

        # If pose is stable for 3 seconds, save the measurements and close the camera
        if initial_pose and time.time() - initial_pose >= 3:
            MList = [
                shoulder_width,
                torso_height,
                hip_width,
                left_leg_length,
                right_leg_length
            ]
            print("Measurements saved:", MList)
            break  # Exit the loop to close the camera

    # Show the image
    cv2.imshow("Body Measurement for Shirt and Pants", img)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()




