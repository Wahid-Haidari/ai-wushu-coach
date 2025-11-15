import math
import mediapipe as mp
mp_pose = mp.solutions.pose

#Calculate angle between three points _____________________________________________
def calculate_angle(a, b, c):
    a = [a.x, a.y]
    b = [b.x, b.y]
    c = [c.x, c.y]

    ab = [a[0]-b[0], a[1]-b[1]]
    cb = [c[0]-b[0], c[1]-b[1]]

    dot_product = ab[0]*cb[0] + ab[1]*cb[1]
    magnitude = math.sqrt((ab[0]**2 + ab[1]**2) * (cb[0]**2 + cb[1]**2))

    if magnitude == 0:
        return None

    angle = math.degrees(math.acos(dot_product / magnitude))
    return angle



# Evaluate knee angle and provide feedback ________________________________________
def evaluate_knee_angle(left_hip, left_knee, left_ankle):
    """Returns knee angle AND a coaching feedback string."""
    
    angle = calculate_angle(left_hip, left_knee, left_ankle)
    
    if angle is None:
        return angle, "⚠️ Could not calculate knee angle."

    # Generate feedback
    if angle > 123:
        feedback = "🟡 Try lowering your stance a bit more."
    elif angle < 80:
        feedback = "🟡 You might be bending too low or leaning."
    else:
        feedback = "✅ Nice Knee angle!"

    return angle, feedback




# Evaluate how deep one side of a stance is ___________________________________________________________
def evaluate_side_depth(hip, knee):
    #  if left_knee_y == 0:
    #     return None, "⚠️ Could not calculate depth ratio."
     
    
    hip_height = hip.y
    knee_height = knee.y
    depth_ratio = hip_height / knee_height
    is_correct_depth = False
    print(f"Hip-to-knee depth ratio: {depth_ratio:.2f}")

    if depth_ratio > 0.95:
        feedback = "⚠️ Stance is too high — lower your hips."  
        
    elif depth_ratio < 0.75:
        feedback = "⚠️ You may be squatting too deep or leaning forward."
    else:
        feedback = "✅ Good stance depth!"
        is_correct_depth = True
    return is_correct_depth, feedback


# Evaluate symmetry between left and right knees ________________________________________
def evaluate_symmetry(left_knee, right_knee):
    diff = abs(left_knee.y - right_knee.y)

    if diff < 0.03:
        return True, "✅ Knees are symmetrical."
    elif diff < 0.07:
        return False, "🟡 Slight asymmetry — balance your stance."
    else:
        return False, "⚠️ Significant imbalance — your weight is shifted."


# Evaluate stance width based on knee and shoulder positions ________________________________________
def evaluate_stance_width(left_knee, right_knee, left_shoulder, right_shoulder):
    knee_width = abs(left_knee.x - right_knee.x)
    shoulder_width = abs(left_shoulder.x - right_shoulder.x)

    ratio = knee_width / shoulder_width
    print(f"Stance width ratio: {ratio:.2f}")

    if ratio < 1.4:
        return False, "⚠️ Stance too narrow."
    elif ratio > 2.6:
        return False, "⚠️ Stance too wide."
    else:
        return True, "✅ Good stance width."

# Evaluate torso alignment based on shoulder and hip midpoints ________________________________________
def evaluate_torso_alignment(left_shoulder, right_shoulder, left_hip, right_hip):
    shoulder_mid = (left_shoulder.x + right_shoulder.x) / 2
    hip_mid = (left_hip.x + right_hip.x) / 2

    diff = abs(shoulder_mid - hip_mid)

    if diff < 0.03:
        return True, "✅ Torso centered."
    elif diff < 0.07:
        return False, "🟡 Slight torso lean."
    else:
        return False, "⚠️ Torso leaning — straighten your back."
    

# Main evaluation function that processes an image and returns feedback ___________________________
def analyze_mabu(results):
    """
    Takes MediaPipe results and returns a feedback report dict.
    Does NOT process images. Only evaluates landmarks.
    """

    feedback_report = {}

    if not results or not results.pose_landmarks:
        feedback_report["pose"] = "⚠️ No pose detected. Try a clearer image."
        return feedback_report

    feedback_report["pose"] = "✅ Pose detected!"

    # Extract landmarks
    lm = results.pose_landmarks.landmark
    left_hip = lm[mp_pose.PoseLandmark.LEFT_HIP]
    left_knee = lm[mp_pose.PoseLandmark.LEFT_KNEE]
    left_ankle = lm[mp_pose.PoseLandmark.LEFT_ANKLE]

    right_hip = lm[mp_pose.PoseLandmark.RIGHT_HIP]
    right_knee = lm[mp_pose.PoseLandmark.RIGHT_KNEE]
    right_ankle = lm[mp_pose.PoseLandmark.RIGHT_ANKLE]

    left_shoulder = lm[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER]

    # Knee angles
    _, fb_left = evaluate_knee_angle(left_hip, left_knee, left_ankle)
    _, fb_right = evaluate_knee_angle(right_hip, right_knee, right_ankle)
    feedback_report["left_knee_angle"] = fb_left
    feedback_report["right_knee_angle"] = fb_right

    # Depth
    _, depthL_msg = evaluate_side_depth(left_hip, left_knee)
    _, depthR_msg = evaluate_side_depth(right_hip, right_knee)
    feedback_report["left_depth"] = depthL_msg
    feedback_report["right_depth"] = depthR_msg

    # Symmetry
    _, sym_msg = evaluate_symmetry(left_knee, right_knee)
    feedback_report["symmetry"] = sym_msg

    # Width
    _, width_msg = evaluate_stance_width(left_knee, right_knee, left_shoulder, right_shoulder)
    feedback_report["stance_width"] = width_msg

    # Torso alignment
    _, torso_msg = evaluate_torso_alignment(left_shoulder, right_shoulder, left_hip, right_hip)
    feedback_report["torso_alignment"] = torso_msg

    return feedback_report
