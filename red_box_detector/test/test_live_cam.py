import cv2
from ultralytics import YOLO

# Load a model
model = YOLO("C:/Users/ASUS/Documents/Portfolio/School/Machine-Vision-Robotic-Arm/red_box_detector/exp/weights/best.pt")  # load a pretrained model (recommended for training)

# Open the default camera (typically the first one)
cap = cv2.VideoCapture(0)

# Set resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) # Height

# Set frame rate
frame_rate = 25 # Adjust as needed
cap.set(cv2.CAP_PROP_FPS, frame_rate)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # Resize frame if needed (optional)
    # frame = cv2.resize(frame, (640, 480))
    
    # Predict on the frame
    results = model(frame)  # predict on the frame
    
    for r in results:
        # Concatenate coordinates into a single string
        coordinates_text = ""
        for box in r.boxes.xyxy:
            x, y = int(box[0]), int(box[1])
            coordinates_text += f'({x},{y})\n'
        
        # Display coordinates on the frame
        cv2.putText(frame, coordinates_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Display the resulting frame
    cv2.imshow('frame', frame)
    
    # Check for 'q' key pressed to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
