from ultralytics import YOLO
from PIL import Image
import cv2

# Load a model
model = YOLO("C:/Users/ASUS/Documents/Portfolio/School/Machine-Vision-Robotic-Arm/red_box_detector/exp/weights/best.pt")  # load a pretrained model (recommended for training)

img_src = model("c:/Users/ASUS/Documents/Portfolio/School/Machine-Vision-Robotic-Arm/red_box_detector/test/images/IMG_20240408_153443_963.jpg")  # predict on an image

for r in img_src:
    im_array = r.plot()  # plot a BGR numpy array of predictions
    im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
    img = cv2.cvtColor(im_array[..., ::-1], cv2.COLOR_BGR2RGB) # Open-CV reads images as BGR, we convert it to RGB

    # Concatenate coordinates into a single string
    coordinates_text = ""
    for box in r.boxes.xyxy:
        x, y = int(box[0]), int(box[1])
        coordinates_text += f'({x},{y})-'
    
    # Display coordinates on the image
    cv2.putText(img, coordinates_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    cv2.imshow("Image", img)  # provide a window name along with the image matrix
    cv2.waitKey(0)  # wait for any key to be pressed
    cv2.destroyAllWindows()  # close all OpenCV windows
