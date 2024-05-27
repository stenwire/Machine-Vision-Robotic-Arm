import time
import cv2

#The duration in seconds for the video captured
capture_duration=60

#Create an object to read from camera
cap=cv2.VideoCapture(1)

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

while(int(time.time()-start_time) < capture_duration):
    
    ret,frame=cap.read()
    if ret==True:
        result.write(frame)
        cv2.imshow("OpenCVCam", frame)
        
        #Press Q to stop the process
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

#When everything is done, release the video capture and videi write objects
cap.release()
result.release()
cv2.destroyAllWindows()