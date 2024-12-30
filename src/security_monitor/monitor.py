import numpy as np
import cv2 as cv
import json
import os
from datetime import datetime

#Declare our constants
MOTION_START = "motion_detected"
MOTION_IN_PROGRESS = "motion_in_progress"
MOTION_ENDS = "motion_ends"

def get_camera():
   try:
    return cv.VideoCapture(0)
   except:
       pass #TODO figure out how I want to handle the case of no camera

def filename_as_jpg(dt):
    return str(dt) + ".jpg"

def filepath_as_jpg(dt):
    return video_output_directory + filename_as_jpg(dt)

def write_line_to_error_log(line):
    write_line_to_log(line, error_log)

def write_line_to_event_log(line):
    write_line_to_log(line, event_log)

def write_line_to_capture_log(line):
    write_line_to_log(line, capture_log)

def write_line_to_log(line, log):
    os.makedirs(os.path.dirname(log), exist_ok=True) #This line was AI generated since I wasn't sure how to generate just the dir section of my log path.
    with open(log, 'a+') as log_file:
        log_file.write(line + "\n")

def write_image_to_file_system(timestamp, frame):
    os.makedirs(os.path.dirname(video_output_directory), exist_ok=True)
    cv.imwrite(filepath_as_jpg(timestamp), frame)

def add_frame_to_captures_and_log(timestamp, frame, event_type):
    write_image_to_file_system(timestamp, frame)
    write_line_to_capture_log(create_capture_ndjson_line(timestamp, event_type))

#Since we are using NDJSON to avoid having to read our entire log back into memory everytime,
#we want to stick a newline at the end of every entry.
def create_capture_ndjson_line(timestamp, event_type):
    return json.dumps({
        "filename": filename_as_jpg(timestamp),
        "timestamp": str(timestamp),
        "type": event_type
    })

def process_event(event_frames):
    #This condition is to avoid little flickers that really shouldn't count as an event.
    #The minimum_event_length_in_frames is configurable.
    if(len(event_frames) > minimum_event_length_in_frames):

        first_frame, first_timestamp = event_frames[0]
        last_frame, last_timestamp = event_frames[-1]
        middle_frames = event_frames[1:-1]  #This line and the next was made with AI assistance because list comprehension and splicing can get annoying.
        middle_frames = [frame for i, frame in enumerate(middle_frames) if i % capture_frame_interval == 0]

        #Write first frame to capture log and add image to file system.
        add_frame_to_captures_and_log(first_timestamp, first_frame, MOTION_START)

        #Write every Xth frame to capture log and add image to file system,
        #where X is 'capture_frame_inteval' in the config.
        for middle_frame_tuple in middle_frames:
            middle_frame, middle_timestamp = middle_frame_tuple

            add_frame_to_captures_and_log(middle_timestamp, middle_frame, MOTION_IN_PROGRESS)
            

        #Write last frame to capture log and add image to file system.
        add_frame_to_captures_and_log(last_timestamp, last_frame, MOTION_ENDS)

        #TODO Remove this fun print statement
        print("CAPTURE")


def load_configs():
    try:
        #This is the only file path that is hardcoded since it's whenere the rest of the paths and configs live.
        with open('src/security_monitor/config.json') as config_json:
            config = json.load(config_json)
            try:
                #Since these are configurations we're constantly accesing, we want them global.
                global movement_check_interval_in_frames
                global contour_size_threshold           
                global inactivity_timeout_in_frames     
                global minimum_event_length_in_frames   
                global video_output_directory           
                global include_border_boxes_in_output   
                global error_log     
                global event_log     
                global capture_log        
                global capture_frame_interval 
                global inactivity_timer
                global frame_count
                global event_frames

                movement_check_interval_in_frames = config["movement_check_interval_in_frames"]
                contour_size_threshold            = config["contour_size_threshold"]
                inactivity_timeout_in_frames      = config["inactivity_timeout_in_frames"]
                minimum_event_length_in_frames    = config["minimum_event_length_in_frames"]
                video_output_directory            = config["video_output_directory"]
                include_border_boxes_in_output    = config["include_border_boxes_in_output"]
                error_log                         = config["error_log"]
                event_log                         = config["event_log"]
                capture_log                       = config["capture_log"]
                capture_frame_interval            = config["capture_frame_interval"]
                inactivity_timer = 0
                frame_count = 0
                event_frames = []
                
                #TODO Write success to activity log

            except KeyError as ke:
                #TODO Log error
                print("KeyError getting configuration: " + ke.args[0])
                exit()
            except Exception as e:
                #TODO Log error
                print("Unknown error getting configurations: " + e)
    except FileNotFoundError as fnfe:
        #TODO Log error
        print("Config file not file or incorrect path")
        exit()
    except Exception as e:
        #TODO Log error
        print("Unknown error opening config file: " + str(e))
        exit()



#TODO write to activity log that program has started
load_configs()
cap = get_camera
backSub = cv.createBackgroundSubtractorMOG2()

if not cap.isOpened():
    print("Cannot open camera")
    exit()

#Pretty much all the logic here is stolen from the example. Some of the lines are taken verbatim.

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    #Since we define the amount of time between frames we check in milliseconds,
    #we want to normalize for any possible FPS on the camera.
    if frame_count % movement_check_interval_in_frames == 0:

        # if frame is read correctly ret is True
        if not ret:
            #TODO write an error message not from the example. Handle the error.
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
        #This is optional depending on the 'include_border_boxes_in_output' config.
        if include_border_boxes_in_output:
            for cnt in large_contours:
                # print(cnt.shape)
                x, y, w, h = cv.boundingRect(cnt)
                frame = cv.rectangle(
                    frame, (x, y), (x+w, y+h), (0, 0, 200), 3)

   
    #TODO Clean up unused imshows.
        # Display the resulting frame
        cv.imshow('frame_out_colorful', frame)


        print(frame_count)

    #TODO Write that user has ended the program to actvity log
    if cv.waitKey(25) & 0xFF == ord('q'):
        break

    frame_count += 1

#TODO Maybe have "user exited" happen here instead?
cap.release()
cv.destroyAllWindows()
