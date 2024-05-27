import os
import serial
import time
from Kinematics.main import InverseKinematics
from red_box_detector.test.test import detect_box_center as box_detector
from red_box_detector.test.take_snapshot_OG import save_frame_camera_cycle as capture_image
from camera_calibration.camera_calibration import runRemoveDistortion, calculate_XYZ

# Define Arduino serial port and baud rate
arduino_port = '/dev/ttyUSB0'
baud_rate = 115200

no_box = False
countdown = 60


root = os.getcwd()
imgPath = os.path.join(root, 'camera_calibration\images\Screenshot 2024-05-05 083153.png')
# capture_image_path = 'data/temp'
captured_image_path = os.path.join(root, 'Vision/data/temp/capture_image')
image_to_undistort = os.path.join(root, 'Vision/data/temp/image_to_undistort/und_img.jpg')
camera_to_use = 1

model_path = os.path.join(root, 'red_box_detector/exp/weights/best.pt')
save_detect_box_image = os.path.join(root, 'red_box_detector/test/images/results')
image_to_detect_box = os.path.join(root, 'red_box_detector/test/images/IMG_20240408_153443_963.jpg')

link_lengths = [5, 10, 15, 8]  # [base, shoulder-elbow, elbow-wrist, wrist-end_effector]

# comment this out when camera is in use
box_detect_image_path = os.path.join(root, 'cali_images/12.jpg')


def main():
    # image = capture_image(camera_to_use, captured_image_path, 'camera_capture_cycle_main')
    # print("captured image: ", image)
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
    print("IK calculated:", calculate_ik)
    return calculate_ik


def initialize():
    try:
        # Open serial connection to Arduino
        arduino = serial.Serial(arduino_port, baud_rate, timeout=1.0)
        time.sleep(3)
        arduino.reset_input_buffer()
        print("======== Serial connection established with Arduino. ========")

        try:
            while True:
                time.sleep(0.01)
                print(f"Angle are being sent to the arduino: {ik_angles}")
                ik_angles = main()
                # Send angles to Arduino
                arduino_angles = ','.join(map(str, ik_angles))
                arduino_angles += '\n'  # Add newline character as delimiter
                arduino.write(arduino_angles.encode('utf-8'))
                print("Angles sent to Arduino: ", arduino_angles)

                # Logic to recieve message from arduino
                # while arduino.in_waiting <= 0:
                #     time.sleep(0.01)
                # response = arduino.readline().decode('utf-8').rstrip()
                # print(response)

        except Exception as e:
            print("======== Serial connection ended with Arduino. ========", e)
            arduino.close()

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    # initialize() # to run algorithm
    main() # To test algorithm with arduino
