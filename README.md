Arturo McGill LVS Coding Assignment
===================================

Overview
--------
This is a simple security system that will monitor the system's webcam for events, and logs said events in JSON files.

Technology and Resources Packages Used
------------------------
* [OpenCV](https://pypi.org/project/opencv-python/)
    * This package provides support for grabbing a video feed from a live capture device such as a camera.

* https://github.com/spmallick/learnopencv/tree/master/Moving-Object-Detection-with-OpenCV
  * This repo is a great resoruce for seeing real example usage of the OpenCV project.  

Assumptions
-----------
* The webcam being used is the only one connected to the host machine. In other words, `CV2.VideoCapture(0)` returns the webcam we care about.
* The webcam is mounted in one place and is not moving.
* The webcam will be seeing a view form a corner of a room or hallway and we are looking for people or animals walking around.
* An "event" is interpreted as any significant movement beyond baseline noise in our image. 
  * Since we are tracking the "type" of event, but what a "type" means is pretty ambiguous and this is a very basic security system, each "event" will be split into three types of event events that are logged. One for motion detected, one for the end of the motion (aka return to baseline), and one for everything in between. The amount of "log every X frames of motion" is a configurable of value in the config.
  * There is probably a smarter way to determine which frame should be captured for the purposes of capturing the most info about what's going on, but giving time constraints and the scope of the project, "the middle frame" seems like a reasonable heuristic.
  * CORRECTION: I have found a smarter way. We're just going to be recording every Xth frame, where X is defined in the config. 
* Since the camera is facing into a room or hallway, we are okay with it being "oversensitive" to pick up movements down the hall. Of course this sensitivity can be corrected by just changing the area value in our config.
* Newline Delimited JSON (NDJSON) satisfes the requirement of being "JSON" for the event tracking and the error tracking and the activity tracking. I am going with this approach since we never actually need to do anything with either of these JSONs so, this avoids wasting time loading them into memory. Instead we just concat to the end.
* Logging an error never throws an error itself. This is to avoid the hellish despair of trying to log an error from an error logging an error from an error logging an error for an error logging an error ad infinitum.
* The requirements say that "Activities" should be tracked. In lieu of anything else to track, I am assuming that it is fine to just track "the user started the system" and "the user gracefully exited the system".

Elaborations/Notes
------------
* One thing to note is that instead of an approach of "check the feed every 3 seconds", or "check the feed every 0.5 seconds", or so on, the checking interval is done in number of frames. This does mean that different FPS cameras will need different configurations. However, this approach was taken as makes the code cleaner and also makes it simpler to define the intervals of inactivity that will separate one event from the next.
* Both for myself as a developer, and for whoever is reviewing this project, I have includes an Examples folder with example code provided by the developers of the various packges. This is both for just the sake of providing an example, as well as for providing me as the developer a playground to work with. Some of the example code is kept in tact, somee of it is marked up by me for the sake of experimentation and learning. 

AI Assistance
-------------
Please refer to the [AI Usage document](AI_Usage.md).