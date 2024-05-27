import cv2
import os
import datetime
import time


# def save_frame_camera_cycle(device_num, dir_path, basename, cycle, ext='jpg', delay=1, window_name='frame'):
#     cap = cv2.VideoCapture(device_num)

#     if not cap.isOpened():
#         return

#     os.makedirs(dir_path, exist_ok=True)
#     base_path = os.path.join(dir_path, basename)

#     # Width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     # Height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     print("Width=", cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     print("Height=",cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#     n = 0
#     while True:
#         ret, frame = cap.read()
#         # cv2.imshow(window_name, frame)
#         # if cv2.waitKey(delay) & 0xFF == ord('q'):
#         #     break
#         n += 1
#         if n == cycle:
#             img_path = '{}_{}.{}'.format(base_path, datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'), ext)
#             cv2.imwrite(img_path,frame)
#             break

#     print(f"image is saved to: {img_path}")
#     return img_path
#     # cv2.destroyWindow(window_name)

# if __name__ == "__main__":
#     root = os.getcwd()
#     imgPath = os.path.join(root, 'data/temp')
#     save_frame_camera_cycle(1, imgPath, 'camera_capture_cycle_main', 30)
    # save_frame_camera_cycle()


# =========================================================================

#The duration in seconds for the video captured
# capture_duration=10
# ext='jpg'
# delay=1,
# window_name='frame'

# #Create an object to read from camera
# cap=cv2.VideoCapture(1)

# cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('U','Y','V','Y'))
# cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
# print("Width=", cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# print("Height=",cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# #we check if the camera is opened previously or not
# if (cap.isOpened()==False):
#     print("Error reading video file")

# Width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# Height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


# # VideoWriter object will create a frame of the above defined output is stored in 'output.avi' file.
# result = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc(*'MJPG'),30,(640,480))

# start_time = time.time()
# root = os.getcwd()
# base_path = os.path.join(root, 'data/temp')

# while(int(time.time()-start_time) < capture_duration):
    
#     ret,frame=cap.read()
#     if ret==True:
#         img_path = '{}_{}.{}'.format(base_path, datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'), ext)
#         cv2.imwrite(img_path,frame)
#         result.write(frame)
#         cv2.imshow("OpenCVCam", frame)
        
#         #Press Q to stop the process
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     else:
#         break

# print(f"image is saved to: {img_path}")
# # return img_path

# #When everything is done, release the video capture and videi write objects
# cap.release()
# result.release()
# cv2.destroyAllWindows()

def save_frame_camera_cycle(device_num, dir_path, basename):
    capture_duration=10
    ext='jpg'
    delay=1,
    window_name='frame'

    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)

    #Create an object to read from camera
    cap=cv2.VideoCapture(device_num)

    cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('U','Y','V','Y'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
    print("Width=", cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    print("Height=",cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    #we check if the camera is opened previously or not
    if (cap.isOpened()==False):
        print("Error reading video file")

    Width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    Height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


    # VideoWriter object will create a frame of the above defined output is stored in 'output.avi' file.
    result = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc(*'MJPG'),30,(640,480))

    start_time = time.time()
    # root = os.getcwd()
    # base_path = os.path.join(root, 'data/temp')

    while(int(time.time()-start_time) < capture_duration):
        
        ret,frame=cap.read()
        if ret==True:
            img_path = '{}_{}.{}'.format(base_path, datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'), ext)
            cv2.imwrite(img_path,frame)
            result.write(frame)
            cv2.imshow("OpenCVCam", frame)
            
            #Press Q to stop the process
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    result.release()
    cv2.destroyAllWindows()

    print(f"image is saved to: {img_path}")
    return img_path

    #When everything is done, release the video capture and videi write objects
    # cap.release()
    # result.release()
    # cv2.destroyAllWindows()

if __name__=="__main__":
    save_frame_camera_cycle()
    # save_frame_camera_cycle(1, saveImgPath, 'camera_capture_cycle_main')