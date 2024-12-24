import math

#Some of these helper functions are for calculations,
#others are just for clarity and abstraction.

#AI generated since dimensional analysis is annoying.
def calculate_frames(fps, milliseconds):
    frame_duration_ms = 1000 / fps
    return math.floor(milliseconds / frame_duration_ms)

def movement_detected(large_contours):
    return len(large_contours) > 0