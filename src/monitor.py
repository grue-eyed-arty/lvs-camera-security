import numpy as np
import cv2 as cv


cap = cv.VideoCapture(0)
backSub = cv.createBackgroundSubtractorMOG2()

if not cap.isOpened():
    print("Cannot open camera")
    exit()


#Pretty much all the logic here is stolen from the example.
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    #This masks out the background
    background_masked_frame = backSub.apply(frame)

    #Remove shadows
    retval, background_masked_shadows_removed_frame = cv.threshold(
    background_masked_frame, 180, 255, cv.THRESH_BINARY)

    #Not quite sure what the kernel is but this "erodes" removing most of the digital dandruff.
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
    background_masked_shadows_removed_and_eroded_frame = cv.morphologyEx(background_masked_shadows_removed_frame, cv.MORPH_OPEN, kernel)


    # Find contours. This is useless by itself since it's way too fine grain.
    contours, hierarchy = cv.findContours(
        background_masked_shadows_removed_and_eroded_frame, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    #This limits the contours to only be bigger ones.
    #min_contour_area can be adjusted for sensitivity
    min_contour_area = 10000  
    large_contours = [
        cnt for cnt in contours if cv.contourArea(cnt) > min_contour_area]
    
    #This block of code paints the contours on top of the original video. 
    frame_out_colorful = frame.copy()
    for cnt in large_contours:
        # print(cnt.shape)
        x, y, w, h = cv.boundingRect(cnt)
        frame_out_colorful = cv.rectangle(
            frame, (x, y), (x+w, y+h), (0, 0, 200), 3)

    #This block of code paints the contours on top of our mask.
    frame_out_raw = cv.cvtColor(background_masked_shadows_removed_and_eroded_frame, cv.COLOR_GRAY2BGR)   
    for cnt in large_contours:
        # print(cnt.shape)
        x, y, w, h = cv.boundingRect(cnt)
        frame_out_raw = cv.rectangle(
            frame_out_raw, (x, y), (x+w, y+h), (0, 0, 200), 3)
    


    # Display the resulting frame
#    cv.imshow('masked', background_masked_frame)
#    cv.imshow('background_masked_shadows_removed', background_masked_shadows_removed_frame)
#    cv.imshow('background_masked_shadows_removed_and_eroded', background_masked_shadows_removed_and_eroded_frame)
    cv.imshow('frame_out_colorful', frame_out_colorful)
    cv.imshow('frame_out_raw', frame_out_raw)
    if cv.waitKey(1) == ord('q'):
        break


# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
