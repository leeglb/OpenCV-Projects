import cv2  
import mediapipe as mp  
import random 
import time 
from datetime import datetime



#creating venv: python3.10 -m venv venv 

#./venv/Scripts/activate --> windows 
#source venv/bin/activate --> mac 

action_value = ""
RPS_list = ["Rock", "Paper", "Scissors"] 
RPS_random = ""

# ------------------

# Time Variables 

game_started = False

DURATION = 3.5

countdown = 0.0

# ------------------

# ------------------

# Score Variables

ai_score = 0 

player_score = 0 

# ------------------

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


cap = cv2.VideoCapture(0)

WINDOW_NAME = "MediaPipe Hands" 
cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

with mp_hands.Hands(
        min_detection_confidence=0.5,  
        min_tracking_confidence=0.5  
) as hands:
    while cap.isOpened():  
        success, image = cap.read()  
        if not success:  
            print("Ignoring empty camera frame.")
            continue

        
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        
        image.flags.writeable = False
        results = hands.process(image)  

        
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        
        image_height, image_width, _ = image.shape

        
        if results.multi_hand_landmarks:
            for hand_landmarks, handed in zip(results.multi_hand_landmarks, results.multi_handedness):
                    
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                which_hand = handed.classification[0].label
                
                fin = ''

                current_action = ""
                
                if which_hand == 'Right':

                    if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x > \
                    hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x:
                        val0 = 0
                        thumb_value = 0
                    else: 
                        val0 = 1
                        fin += 'Thumb '
                        thumb_value = 1

                else:
                    if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x < \
                    hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x:
                        val0 = 0
                        thumb_value = 0 
                    else: 
                        val0 = 1
                        fin += 'Thumb '  
                        thumb_value = 1
                
                if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y > \
                hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y:
                    val1 = 0  
                    index_value = 0 
                else:
                    val1 = 1 
                    fin += 'Index '  
                    index_value = 3
                    
                
                if hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y > \
                hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y:
                    val2 = 0 
                    middle_value = 0 
                else:
                    val2 = 1  
                    fin += 'Middle '
                    middle_value = 5  

                
                if hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y > \
                hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y:
                    val3 = 0  
                    ring_value = 0 
                else:
                    val3 = 1  
                    fin += 'Ring ' 
                    ring_value = 7  

                
                if hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y > \
                hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].y:
                    val4 = 0  
                    pinky_value = 0 
                else:
                    val4 = 1  
                    fin += 'Pinky ' 
                    pinky_value = 9

                
                val = val0 + val1 + val2 + val3 + val4

                finger_values = thumb_value + index_value + middle_value + ring_value + pinky_value
                

                # rock = 0 
                # scissors = 3 + 5 = 8
                # paper = 1 + 3 + 5 + 7 + 9 = 25
                
                while True: 


                    if finger_values == 25: 

                        current_action = "Paper"

                    elif finger_values == 8:

                        current_action = "Scissors"

                    elif finger_values == 0:

                        current_action = "Rock"

                    break 

                if game_started: 

                    time_remaining = int(countdown - time.time())

                    if time_remaining >= 0: 

                        cv2.putText(image, str(time_remaining), (20, 300), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)

                        if time_remaining <= 0: 

                            match current_action: 

                                case "Rock":

                                    if RPS_random == "Rock":

                                        cv2.putText(image, "Tie", (20, 450), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)

                                    elif RPS_random == "Scissors":

                                        cv2.putText(image, "You Win!", (20, 450), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
                                        
                                        player_score += 1 

                                    elif RPS_random == "Paper": 

                                        cv2.putText(image, "You Lost!", (20, 450), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
                                        
                                        ai_score += 1

                                case "Paper":

                                    if RPS_random == "Rock":

                                        cv2.putText(image, "You Win!", (20, 450), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
                                        
                                        player_score += 1 

                                    elif RPS_random == "Scissors":

                                        cv2.putText(image, "You Lost!", (20, 450), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
                                        
                                        ai_score += 1

                                    elif RPS_random == "Paper": 

                                        cv2.putText(image, "Tie", (20, 450), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)


                                case "Scissors":

                                    if RPS_random == "Rock":

                                        cv2.putText(image, "You Lost!", (20, 450), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
                                        
                                        ai_score += 1 

                                    elif RPS_random == "Scissors":

                                        cv2.putText(image, "Tie!", (20, 450), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)

                                    elif RPS_random == "Paper": 

                                        cv2.putText(image, "You Win!", (20, 450), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
                                        
                                        player_score += 1 

                    else: 

                        game_started = False




                fps = str(val) + ' fingers'
                # cv2.putText(image, fps, (20, 40), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)

                # cv2.putText(image, fin, (20, 200), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)

                cv2.putText(image, "Current Action: " + current_action, (20, 1050), cv2.FONT_HERSHEY_DUPLEX, 2.5, (255, 255, 255), 2)
                
                cv2.putText(image, "Current Player Score: " + str(player_score), (20, 100), cv2.FONT_HERSHEY_DUPLEX, 2.5, (255, 255, 255), 2)
                cv2.putText(image, "Current Computer Score: " + str(ai_score), (20, 1500), cv2.FONT_HERSHEY_DUPLEX, 2.5, (255, 255, 255), 2)
                #cv2.putText(image, RPS_random, (20, 500), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)

                
       
        cv2.imshow(WINDOW_NAME, image)
        
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            
            break
        
        if key == ord('s'):

            game_started = True 

            RPS_random = random.choice(RPS_list)

            countdown = time.time() + DURATION

cap.release()

    


