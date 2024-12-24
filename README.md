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


Examples
--------
* Both for myself as a developer, and for whoever is reviewing this project, I have includes an Examples folder with example code provided by the developers of the various packges. This is both for just the sake of providing an example, as well as for providing me as the developer a playground to work with. Some of the example code is kept in tact, somee of it is marked up by me for the sake of experimentation and learning.

AI Assistance
-------------
Please refer to the [AI Usage document](AI_Usage.md).