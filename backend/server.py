import base64 
import cv2
import numpy as np
import mediapipe as mp


from fastapi import FastAPI, UploadFile, File
from mabu import analyze_mabu
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()


# Set up CORS (Cross-Origin Resource Sharing) middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/analyze")
async def analyze_pose(file: UploadFile = File(...)):
    # Read uploaded image bytes
    contents = await file.read()

    #This line takes the raw file bytes (contents of the uploaded image) and turns them into a NumPy array so OpenCV can read it like an image.
    # Convert bytes → NumPy array → OpenCV image
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        return {"error": "Could not read image"}
    
    # Convert to RGB for MediaPipe
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Run MediaPipe Pose
    with mp.solutions.pose.Pose(static_image_mode=True) as pose:
        results = pose.process(img_rgb)

    # Analyze using your mabu.py logic
    feedback = analyze_mabu(results)


    # Draw landmarks on the image before encoding
    if results.pose_landmarks:
        mp.solutions.drawing_utils.draw_landmarks(
            img,
            results.pose_landmarks,
            mp.solutions.pose.POSE_CONNECTIONS
        )

    # Encode processed image as JPEG
    _, buffer = cv2.imencode(".jpg", img)
    img_base64 = base64.b64encode(buffer).decode("utf-8")

    # Add image to feedback
    feedback["image"] = img_base64

    return feedback


@app.get("/")
def root():
    return {"message": "AI Wushu Coach API is running"}
