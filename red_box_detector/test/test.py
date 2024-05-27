from typing import Any
from ultralytics import YOLO
from PIL import Image
import cv2
import os


# save_dir = os.path.join(root, 'red_box_detector/test/images/results')
def detect_box_center(image_path: str, save_dir: str, model_path: str) -> dict[str, Any] | None:

    model = YOLO(model_path)  # load a pretrained model
    results = model(image_path)  # predict on an image

    r = results[0]
    print(len(r))

    os.makedirs(save_dir, exist_ok=True)

    if len(r) == 1:
        im_array = r.plot()  # plot a BGR numpy array of predictions
        im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
        img = cv2.cvtColor(im_array[..., ::-1], cv2.COLOR_BGR2RGB)  # Open-CV reads images as BGR, we convert it to RGB

        # Extract bounding box coordinates
        x1, y1, x2, y2 = r.boxes.xyxy[0]  # Assuming only one prediction per image

        # Calculate the center coordinates
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2

        # Calculate the diameter (Euclidean distance)
        diameter = ((x2 - x1)**2 + (y2 - y1)**2)**0.5

        # Display the center and diameter on the image
        cv2.putText(img, f"Center: ({cx:.2f}, {cy:.2f})", (int(cx) + 90, int(cy) + 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), )  # Green dot
        cv2.putText(img, f"Diameter: {diameter:.2f} pixels", (int(cx)+ 90, int(cy) + 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        cv2.circle(img, (int(cx), int(cy)), 6, (0, 255, 0), 3)

        # Save the modified image
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, "modified_image.png")
        cv2.imwrite(save_path, img)

        print({"cx": int(cx), "cy": int(cy), "save_path": save_path})
        detect_box = {"cx": int(cx), "cy": int(cy), "save_path": save_path}
        print(detect_box["cx"])
        return ({"cx": int(cx), "cy": int(cy), "diameter": int(diameter), "save_path": save_path})

        # Show the modified image
        # cv2.imshow("Image with Center and Diameter", img)
        # cv2.waitKey(0)  # wait for any key to be pressed
        # cv2.destroyAllWindows()  # close all OpenCV windows

    else:
        print("No Red Box Detected")
        return None

if __name__ == "__main__":
#     '''
#     Uncomment the commented code below to test this function
#     '''
    root = os.getcwd()
    model_path = os.path.join(root, 'red_box_detector/exp/weights/best.pt')
    save_dir = os.path.join(root, 'red_box_detector/test/images/results')
    image_path = os.path.join(root, 'cali_images/4.jpg')
    print("image_path: ", save_dir)
    result = detect_box_center(image_path, save_dir, model_path)
    if result:
        print(f"Image saved in {result}")
    # detect_box_center()
