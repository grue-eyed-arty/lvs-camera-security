Arturo McGill LVS Coding Assignment
===================================

Overview
--------
This is a simple security system that will monitor the system's webcam for events, and logs said events in JSON files.

Technology/Packages Used
------------------------
* [OpenCV](https://pypi.org/project/opencv-python/)
    * This package provides support for grabbing a video feed from a live capture device such as a camera.    

Assumptions
-----------
* The webcam being used is the only one connected to the host machine. In other words, `CV2.VideoCapture(0)` returns the webcam we care about.
* An "event" is interpreted as movement in the camera stream, such that it is the first motion after an extended period of stillness. 
  * For example, if the camera is looking down an empty hallway, and a cat walks into the frame, and walks around for a while, that whole thing counts as a single event. 
  * However, if the cat falls asleep as doesn't move for some amount of time, then the cat getting up again counts as an event.
  * In other words, an "event" is the start of movement after a baseline of some amount of stillness. This amount is TBD. Likely something to be done in configuration.

Examples
--------
* Both for myself as a developer, and for whoever is reviewing this project, I have includes an Examples folder with example code provided by the developers of the various packges. This is both for just the sake of providing an example, as well as for providing me as the developer a playground to work with.

AI Assistance
-------------
Please refer to the [AI Usage document](AI_Usage.md).