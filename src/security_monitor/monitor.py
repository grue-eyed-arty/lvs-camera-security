import numpy as np
import cv2 as cv
import json
import helpers

try:
    with open('src/security_monitor/config.json') as config_json:
        config = json.load(config_json)
        try:
            movement_check_interval_in_frames = config["movement_check_interval_in_frames"]
            contour_size_threshold = config["contour_size_threshold"]
        except KeyError as ke:
            print("KeyError getting configuration: " + ke.args[0])
            exit()
        except Exception as e:
            print("Unknown error getting configurations: " + e)
except FileNotFoundError as fnfe:
    print("Config file not file or incorrect path")
    exit()
except Exception as e:
    print("Unknown error opening config file")
    exit()



cap = cv.VideoCapture(0)
fps = int(cap.get(cv.CAP_PROP_FPS))
backSub = cv.createBackgroundSubtractorMOG2()

if not cap.isOpened():
    print("Cannot open camera")
    exit()


#Pretty much all the logic here is stolen from the example.
frame_count = 0
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    #Since we define the amount of time between frames we check in milliseconds,
    #we want to normalize for any possible FPS on the camera.
    if frame_count % movement_check_interval_in_frames == 0:

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


        #Find contours. This is useless by itself since it's way too fine grain.
        #But it's necessary for the next step of finding large contours.
        contours, hierarchy = cv.findContours(
            background_masked_shadows_removed_and_eroded_frame, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        
        #This limits the contours to only be bigger ones.
        #contour_size_threshold can be adjusted for sensitivituy. Defined in config.json.
        large_contours = [
            cnt for cnt in contours if cv.contourArea(cnt) > contour_size_threshold]
        
        # if(not large_contours):
        #     print("EMPTY")
        # else:
        #     print(large_contours)
        
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
        
   
    #TODO Clean up unused imshows.
        # Display the resulting frame
    #    cv.imshow('masked', background_masked_frame)
    #    cv.imshow('background_masked_shadows_removed', background_masked_shadows_removed_frame)
    #    cv.imshow('background_masked_shadows_removed_and_eroded', background_masked_shadows_removed_and_eroded_frame)
    #    cv.imshow('frame_out_raw', frame_out_raw)
        cv.imshow('frame_out_colorful', frame_out_colorful)

        if cv.waitKey(25) & 0xFF == ord('q'):
            break

        print(frame_count)

    frame_count += 1

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
