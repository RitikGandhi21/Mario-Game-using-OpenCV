
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

            # # if x co-ordinate passes right threshold move right
            if int(mid_point_of_shoulder[0]) > int(right_threshold):
                # for i in range(400):
                #     move_right() 
                t2 = threading.Thread(target=move_right)
                t2.start()               
                

            # # if y co-ordinate passes aboe the top threshold move up
            if int(mid_point_of_shoulder[1]) < int(top_threshold):
                jump()
                #print("jump")

            else:
                do_nothing()

        
        
        except Exception as e : 
            print("enter exception", e)
            do_nothing()

        # rendering the detections
        # to show the acutal lines on the body
        # mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
        #                                   mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
        #                                   mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
        #                                   )
        cv2.imshow('Cam Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()        
