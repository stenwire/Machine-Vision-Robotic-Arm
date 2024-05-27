from ultralytics import YOLO
import cv2
import numpy as np

# Load a model
model = YOLO("C:/Users/ASUS/Documents/Portfolio/School/Machine-Vision-Robotic-Arm/red_box_detector/exp/weights/best.pt")  # load a pretrained model

# Predict on an image
results = model.predict("C:/Users/ASUS/Documents/Portfolio/School/Machine-Vision-Robotic-Arm/red_box_detector/test/images/IMG_20240408_153443_963.jpg", save=True)

# Load the image
image = cv2.imread("C:/Users/ASUS/Documents/Portfolio/School/Machine-Vision-Robotic-Arm/red_box_detector/test/images/IMG_20240408_153443_963.jpg")

# Convert BGR to HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define range of red color in HSV
lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])

# Threshold the HSV image to get only red colors
mask = cv2.inRange(hsv, lower_red, upper_red)

cnts = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

for c in cnts:
  area = cv2.contourArea(c)
  cv2.drawContours(image, [c], -1, (0,255,0), 3)
  M = cv2.moments(c)
  cx = int(M["m10"]/M["m00"])
  cy = int(M["m01"]/M["m00"])

  cv2.circle(image, (cx, cy), 7, (255, 255, 255), -1)
  cv2.putText(image, "center", (cx-20, cy-20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)