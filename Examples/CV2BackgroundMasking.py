#Taken from https://learnopencv.com/moving-object-detection-with-opencv/#aioseo-what-is-moving-object-detection
import cv2
import gradio as gr
import numpy as np
import matplotlib.pyplot as plt

# cap = cv2.VideoCapture(0)
# backSub = cv2.createBackgroundSubtractorMOG2()
# if not cap.isOpened():
#     print("Error opening video file")
#     while cap.isOpened():
#         # Capture frame-by-frame
#           ret, frame = cap.read()
#           if ret:
#             # Apply background subtraction
#             fg_mask = backSub.apply(frame)


cap = cv2.VideoCapture(0)
backSub = cv2.createBackgroundSubtractorMOG2()
while True:
        # Capture frame-by-frame
    ret, frame = cap.read()
 
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv2.imshow('masked', backSub.apply(frame)) #OH HELL YES, THIS WORKS
    if cv2.waitKey(1) == ord('q'):
        break
