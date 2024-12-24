To-Do
=============
1) ~~Figure out how to get my camera stream going and how to process each individual.~~
   * Taken care of by OpenCV
2) ~~Figure out exactly what an "event" means. Leaning towards it being any amount of movement after some baseline amount of stillness.~~
   * First frame with large contours of any sort after nothing.
3) Figure out A) how much tolerance there should be for stillness (ie we don't want random noise counted as an event), and B) figure out how long an event goes on for. 
4) Figure out which frame is best to capture for an event. Maybe the middle of the event? Or maybe only look at a frame every 10 second, and if it's different from the one before, it's its own event and should be tracked?
5) Figure out how to do config files.
6) Make a requirements.txt file to quickly install dependencies. (Do at end with `pip freeze > requirements.txt`)
7) Add exception handling for missing configurations
8) Find a less ugly way to close the program (keyboard module doesn't work on mac).
9) Figure out how to have the webcam stream to an HTTP server, then have my program read from that server.