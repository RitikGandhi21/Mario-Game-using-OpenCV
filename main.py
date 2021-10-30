
import cv2 
import mediapipe as mp
from controls import *
import threading

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


cap = cv2.VideoCapture(0)

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence= 0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False 

        
        results = pose.process(image)

        
        image.flags.writeable = True 
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


        try:
            landmarks = results.pose_landmarks.landmark

            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

            mid_point_of_shoulder = [ (left_shoulder[0] * 1000 + right_shoulder[0] * 1000)//2, 
                                    (left_shoulder[1] * 1000 + right_shoulder[1] * 1000)//2 ]

            

            left_threshold = 450
            right_threshold = 575
            top_threshold = 420

            
            if int(mid_point_of_shoulder[0]) < int(left_threshold):
                t1 = threading.Thread(target=move_left)
                t1.start()

            if int(mid_point_of_shoulder[0]) > int(right_threshold):
                
                t2 = threading.Thread(target=move_right)
                t2.start()               
                

            
            if int(mid_point_of_shoulder[1]) < int(top_threshold):
                jump()
                

            else:
                do_nothing()

        
        
        except Exception as e : 
            print("enter exception", e)
            do_nothing()

        
        cv2.imshow('Cam Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()        
