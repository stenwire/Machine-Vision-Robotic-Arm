import os
from Kinematics.main import InverseKinematics
from red_box_detector.test.test import detect_box_center as box_detector
from red_box_detector.test.take_snapshot_OG import save_frame_camera_cycle as capture_image
from camera_calibration.camera_calibration import runRemoveDistortion, calculate_XYZ

'''
@TODO:
take snapshot
undistort image
detect object center and diameter
calculate xyz using calibration parameters and object center and diameter
send xyz to IK to solve for angles
send angles to arduino
'''

no_box = False
countdown = 60

# image = capture_image.save_frame_camera_cycle(0, 'data/temp', 'camera_capture_cycle_main', 30)
# print(len(image))
root = os.getcwd()
imgPath = os.path.join(root, 'camera_calibration\images\Screenshot 2024-05-05 083153.png')
# capture_image_path = 'data/temp'
captured_image_path = os.path.join(root, 'Vision/data/temp/capture_image')
image_to_undistort = os.path.join(root, 'Vision/data/temp/image_to_undistort/und_img.jpg')
camera_to_use = 0

model_path = os.path.join(root, 'red_box_detector/exp/weights/best.pt')
save_detect_box_image = os.path.join(root, 'red_box_detector/test/images/results')
image_to_detect_box = os.path.join(root, 'red_box_detector/test/images/IMG_20240408_153443_963.jpg')

link_lengths = [5, 10, 15, 8]  # [base, shoulder-elbow, elbow-wrist, wrist-end_effector]

# comment this out when camera is in use
box_detect_image_path = os.path.join(root, 'red_box_detector/test/images/IMG_20240408_153443_963.jpg')

def main():
  try:
    image = capture_image(camera_to_use, captured_image_path, 'camera_capture_cycle_main', 30)
    print("captured image: ", image)
    calibration_data = runRemoveDistortion(imgPath)
    _, camMatrix, _ = calibration_data
    print("calibration_data: ", camMatrix)
    detect_box = box_detector(box_detect_image_path, save_detect_box_image, model_path)
    print("detect_box: ", detect_box)
    fx = camMatrix[0, 0]
    fy = camMatrix[1, 1]
    px = camMatrix[0, 2]
    py = camMatrix[1, 2]
    x = detect_box["cx"]
    y = detect_box["cy"]
    d_pix = detect_box["diameter"]
    calculate_xyz = calculate_XYZ(fx, fy, px, py, d_pix, x, y)
    print("calculate_xyz: ", calculate_xyz)
    target_position = [calculate_xyz["X"], calculate_xyz["Y"], calculate_xyz["Z"]]
    print("target_position: ", target_position)
    i_ken = InverseKinematics()
    calculate_ik = i_ken.calculate(link_lengths, target_position)
    print(calculate_ik)
    return(calculate_ik)
    # send ANGLES to Arduino

  except Exception as e:
    print("The error is: ",e)
    return(e)



main()


# while True:
#   image = capture_image.save_frame_camera_cycle(0, 'data/temp', 'camera_capture_cycle', 30)
#   print
  # if (image):
  #   box = box_detector.detect_box_center()
  # if box == "no box":
  #   no_box = True
  # if no_box == True:
  #   count = 0
  #   for (i in range(0, countdown)):
  #     count++
  #   if count == countdown:
  #     return false