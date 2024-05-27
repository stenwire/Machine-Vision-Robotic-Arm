import cv2
import numpy as np

# Load the image (replace 'red_cube.jpg' with your image file)
image = cv2.imread('C:/Users/ASUS/Documents/Portfolio/School/Machine-Vision-Robotic-Arm/red_box_detector/test/images/IMG_20240408_153443_963.jpg')

# Convert to HSV color space
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define the lower and upper bounds for red color (adjust as needed)
lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])

# Create a binary mask for red regions
red_mask = cv2.inRange(hsv_image, lower_red, upper_red)

# Find contours in the mask
contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Assuming the largest contour corresponds to the red cube
if contours:
    largest_contour = max(contours, key=cv2.contourArea)
    (x, y), radius = cv2.minEnclosingCircle(largest_contour)
    center = (int(x), int(y))
    diameter = int(2 * radius)
    width = diameter  # Assuming the cube is a perfect circle

    print(f"Center (x, y): {center}")
    print(f"Diameter: {diameter}")
    print(f"Width: {width}")
else:
    print("No red cube found in the image.")

# Display the segmented red regions (optional)
cv2.imshow("Red Cube Segmentation", red_mask)
cv2.waitKey(0)
cv2.destroyAllWindows()
