import cv2
import mediapipe as mp #MediaPipe Pose is a pre-built AI model from Google that can find the position of a person’s body in any image or video.
from mabu import analyze_mabu

mp_drawing = mp.solutions.drawing_utils #This module contains functions to draw the pose landmarks on the image.

# Load an image (replace the filename later with your own)
image_path = "../Mabu_high.webp"
img = cv2.imread(image_path)


if img is None:
    print("❌ Image not found!")
else:
    # Convert image to RGB (MediaPipe needs RGB instead of BGR)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Run MediaPipe
    with mp.solutions.pose.Pose(static_image_mode=True) as pose:
        results = pose.process(img_rgb)


    # Evaluate pose using the new wrapper
    feedback_report = analyze_mabu(results)

    if not results or not results.pose_landmarks:
        print("⚠️ No pose detected — skipping drawing.")
    else:
        # Draw landmarks (skeleton)
        mp_drawing.draw_landmarks(
            img, 
            results.pose_landmarks, 
            mp.solutions.pose.POSE_CONNECTIONS
        )

    print("\n=== MABU EVALUATION REPORT ===")
    for key, value in feedback_report.items():
        print(f"{key}: {value}")

    # Show the image in a window
    cv2.imshow("Wushu Pose - Detected", img)
    cv2.waitKey(0) #Wait for a key press to close the window
    cv2.destroyAllWindows() #Close the window after key press





        

        

   
