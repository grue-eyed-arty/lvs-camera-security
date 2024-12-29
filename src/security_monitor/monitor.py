import numpy as np
import cv2 as cv
import json
import os
from datetime import datetime

#Declare our constants
MOTION_START = "motion_detected"
MOTION_IN_PROGRESS = "motion_in_progress"
MOTION_ENDS = "motion_ends"

def filename_as_jpg(dt):
    return str(dt) + ".jpg"

def filepath_as_jpg(dt):
    return video_output_directory + filename_as_jpg(dt)


#Since we are using NDJSON to avoid having to read our entire log back into memory everytime,
#we want to stick a newline at the end of every entry.
def create_json_line(timestamp, event_type):
    return json.dumps({
        "filename": filename_as_jpg(timestamp),
        "timestamp": str(timestamp),
        "type": event_type
    }) + "\n"

def process_event(event_frames):

    os.makedirs(video_output_directory, exist_ok=True)

    #This is to avoid little flickers that really shouldn't count as an event.
    #The minimum_event_length_in_frames is configurable.
    if(len(event_frames) > minimum_event_length_in_frames):

        first_frame, first_timestamp = event_frames[0]
        last_frame, last_timestamp = event_frames[-1]

        
       #Add three images to the images directory.
        
     #   cv.imwrite(filepath_as_jpg(middle_timestamp), middle_frame)
        

        #Write data about the above to the 
        with open(capture_logging_directory, 'a+') as capture_log:
            #Log the start of motion
            cv.imwrite(filepath_as_jpg(first_timestamp), first_frame)
            capture_log.write(create_json_line(first_timestamp, MOTION_START))
            
            
            #Here we're only looking at the frames in the middle of the action. This means we disregard the first and last frames.
            middle_frames = event_frames[1:-1]  #This line and the next was made with AI assistance because list comprehension and splicing can get annoying.
            middle_frames = [frame for i, frame in enumerate(middle_frames) if i % capture_frame_interval == 0]
            for middle_frame_tuple in middle_frames:
                middle_frame, middle_timestamp = middle_frame_tuple
                cv.imwrite(filepath_as_jpg(middle_timestamp), middle_frame)
                capture_log.write(create_json_line(middle_timestamp, MOTION_IN_PROGRESS))

            
            #Log the end of motion
            cv.imwrite(filepath_as_jpg(last_timestamp), last_frame)
            capture_log.write(create_json_line(last_timestamp, MOTION_ENDS))

    #TODO Remove this fun print statement
    print("CAPTURE")


        

try:
    with open('src/security_monitor/config.json') as config_json:
        config = json.load(config_json)
        try:
            movement_check_interval_in_frames = config["movement_check_interval_in_frames"]
            contour_size_threshold            = config["contour_size_threshold"]
            inactivity_timeout_in_frames      = config["inactivity_timeout_in_frames"]
            minimum_event_length_in_frames    = config["minimum_event_length_in_frames"]
            video_output_directory            = config["video_output_directory"]
            include_border_boxes_in_output    = config["include_border_boxes_in_output"]
            error_logging_directory           = config["error_logging_directory"]
            capture_logging_directory         = config["capture_logging_directory"]
            capture_frame_interval            = config["capture_frame_interval"]

        except KeyError as ke:
            print("KeyError getting configuration: " + ke.args[0])
            exit()
        except Exception as e:
            print("Unknown error getting configurations: " + e)
except FileNotFoundError as fnfe:
    print("Config file not file or incorrect path")
    exit()
except Exception as e:
    print("Unknown error opening config file: " + str(e))
    exit()



cap = cv.VideoCapture(0)
fps = int(cap.get(cv.CAP_PROP_FPS))
backSub = cv.createBackgroundSubtractorMOG2()

if not cap.isOpened():
    print("Cannot open camera")
    exit()


#Pretty much all the logic here is stolen from the example.
inactivity_timer = 0
frame_count = 0
event_frames = []
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

        #Logically equivalent to "if movement detected"
        if(large_contours):
            event_frames.append((frame, datetime.now()))
        elif event_frames: #We only want this "wait for a bit then process" logic to keep in if we've been seeing motion
            #If it's been less than movement frame inactivity timeout, we keep adding to the event.
            #Otherwise, we assume the event is over, process the event, and start over.
            if(inactivity_timer < inactivity_timeout_in_frames):
                event_frames.append((frame, datetime.now())) #We want to keep track of the timestamp of each frame
                inactivity_timer += 1
            else:
                process_event(event_frames)
                event_frames = []
                inactivity_timer = 0

        
        #This block of code paints the contours on top of the original video. 

        if include_border_boxes_in_output:
            for cnt in large_contours:
                # print(cnt.shape)
                x, y, w, h = cv.boundingRect(cnt)
                frame = cv.rectangle(
                    frame, (x, y), (x+w, y+h), (0, 0, 200), 3)

   
    #TODO Clean up unused imshows.
        # Display the resulting frame
    #    cv.imshow('masked', background_masked_frame)
    #    cv.imshow('background_masked_shadows_removed', background_masked_shadows_removed_frame)
    #    cv.imshow('background_masked_shadows_removed_and_eroded', background_masked_shadows_removed_and_eroded_frame)
    #    cv.imshow('frame_out_raw', frame_out_raw)
        cv.imshow('frame_out_colorful', frame)

        #The way I'm doing my framerates seem to be breaking this functionality?
        # if cv.waitKey(25) & 0xFF == ord('q'):
        #     break

        print(frame_count)

    if cv.waitKey(25) & 0xFF == ord('q'):
        break

    frame_count += 1

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
