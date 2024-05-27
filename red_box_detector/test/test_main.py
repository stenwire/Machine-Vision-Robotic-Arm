import cv2
import datetime
import os
from ultralytics import YOLO
from PIL import Image

def capture_first_frame(device_num, dir_path, basename, cycle, ext='jpg', delay=1, window_name='frame'):
  cap = cv2.VideoCapture(device_num)

  if not cap.isOpened():
      return

  os.makedirs(dir_path, exist_ok=True)
  base_path = os.path.join(dir_path, basename)

  n = 0
  while True:
      ret, frame = cap.read()
      cv2.imshow(window_name, frame)
      if cv2.waitKey(delay) & 0xFF == ord('q'):
          break
      if n == cycle:
          cv2.imwrite('{}_{}.{}'.format((base_path), ext), frame)
          return False
      n += 1

  cv2.destroyWindow(window_name)


def count_objects():
    model = YOLO("C:/Users/ASUS/Documents/Portfolio/School/Machine-Vision-Robotic-Arm/red_box_detector/exp/weights/best.pt")  # load a pretrained model (recommended for training)

    img_path = os.path.join("data/temp/first_frame/first_frame.jpg")
    image = cv2.imread(filename=img_path)
    results = model(image)

    count = 0  # Initialize count for detected boxes

    for r in results:
        print(r.boxes)

    for r in results:
        for detection in r:
          count += 1
    print("Number of detected boxes:", count)


    for r in results:
      im_array = r.plot()  # plot a BGR numpy array of predictions
      im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
      img = cv2.cvtColor(im_array[..., ::-1], cv2.COLOR_BGR2RGB) # Open-CV reads images as BGR, we convert it to RGB
      cv2.imshow("Counting Objects", img)  # provide a window name along with the image matrix
      cv2.waitKey(0)  # wait for any key to be pressed
      cv2.destroyAllWindows()  # close all OpenCV windows

    return count

def save_frame_camera_cycle(device_num, dir_path, basename, cycle, ext='jpg', delay=1, window_name='frame'):
    cap = cv2.VideoCapture(device_num)

    if not cap.isOpened():
        return

    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)

    n = 0
    while True:
        ret, frame = cap.read()
        cv2.imshow(window_name, frame)
        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break
        if n == cycle:
            n = 0
            cv2.imwrite('{}_{}.{}'.format(base_path, datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'), ext), frame)
        n += 1

    cv2.destroyWindow(window_name)




# capture_first_frame(0, 'data/temp/first_frame', 'first_frame', 3)
count_objects()