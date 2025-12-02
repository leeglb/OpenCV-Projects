import cv2
import courier 
from courier.client import Courier 
from ultralytics import YOLO
from playsound3 import playsound
from datetime import datetime 

# Video Capture Parameters

cap = cv2.VideoCapture(1)
assert cap.isOpened(), "Error opening camera"

"""
Model Paramaters: 
"""

model = YOLO("yolov8n.pt")

# Global Parameters: 

alarm_activated = False 

while True:
    success, frame = cap.read()
    if not success:
        print("Failed to read frame from camera.")
        break

    current_datetime = datetime.now()
    
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    
    results = model.predict(source=frame, classes=[0])
   
    annotated_frame = results[0].plot()
    
    cv2.putText(annotated_frame, f"Current Time: {formatted_datetime}", (0, 100), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
    
    # Alarm System Function 
    
    print(current_datetime.second)

    if alarm_activated:  
        
        playsound("/Users/galbraithlee/Desktop/OpenCV-Projects/Intruder Alert Warning System.mp3")
        
    else: 
        
        alarm_activated = False 


    key = cv2.waitKey(1) & 0xFF
    
    audio_key = cv2.waitKey(30) & 0xFF
    
    if key == ord('q'):
        
        break
    
    if audio_key == ord('s'):
        
        alarm_activated = True 
        
        
    cv2.imshow("Detections", annotated_frame)

cap.release()
cv2.destroyAllWindows()
