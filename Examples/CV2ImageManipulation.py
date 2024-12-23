# Importing the OpenCV library
import cv2
# Reading the image using imread() function
image = cv2.imread('/Users/arthurmcgill/dev/lvs-camera-security/Examples/image.jpg')
print(len(image))

print(image)


# Extracting the height and width of an image
h, w = image.shape[:2]
# Displaying the height and width
print("Height = {}, Width = {}".format(h, w))

# Extracting RGB values.
# Here we have randomly chosen a pixel
# by passing in 100, 100 for height and width.
(B, G, R) = image[100, 100]

# Displaying the pixel values
print("R = {}, G = {}, B = {}".format(R, G, B))

# We can also pass the channel to extract
# the value for a specific channel
B = image[100, 100, 0]
print("B = {}".format(B))

# We will calculate the region of interest
# by slicing the pixels of the image
roi = image[0 : 200, 200 : 700]
cv2.imshow("ROI", roi)
cv2.waitKey(4000)