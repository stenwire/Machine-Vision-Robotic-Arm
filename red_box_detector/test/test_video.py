import cv2
from ultralytics import YOLO

# Load a model
model = YOLO("C:/Users/ASUS/Documents/Portfolio/School/Machine-Vision-Robotic-Arm/red_box_detector/exp/weights/best.pt")  # load a pretrained model (recommended for training)

# Open the video file
video_path = "c:/Users/ASUS/Documents/Portfolio/School/Machine-Vision-Robotic-Arm/red_box_detector/test/videos/VID_20240408_153553.mp4"
cap = cv2.VideoCapture(video_path)

# Get the video's frame width and height
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create VideoWriter object to save the modified video
out = cv2.VideoWriter('output_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (frame_width, frame_height))

while(cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break

    # Perform object detection
    results = model(frame)

    # Concatenate coordinates into a single string
    coordinates_text = ""
    for r in results:
        for box in r.boxes.xyxy:
            x, y = int(box[0]), int(box[1])
            coordinates_text += f'({x},{y})\n'

    # Display coordinates on the frame
    cv2.putText(frame, coordinates_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Write the modified frame to the output video
    out.write(frame)

    # Display the frame
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
