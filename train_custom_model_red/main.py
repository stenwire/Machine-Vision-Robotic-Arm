from ultralytics import YOLO

# Load a pre-trained model (transfer learning)
model = YOLO("yolov8m.yaml", verbose=True)  # Load a pre-trained model

# Configure training parameters
model.train(
    data="c:/Users/ASUS/Documents/Portfolio/School/Machine-Vision-Robotic-Arm/train_custom_model_red/config.yaml",
    epochs=100,  # Increase the number of epochs
    imgsz=640,  # Set the input image size
    batch=16,  # Set the batch size
    workers=4,  # Set the number of worker processes
    project="red_box_detector",  # Set the project name for saving results
    name="exp",  # Set the experiment name
    exist_ok=True,  # Allow overwriting existing directories
)

# Evaluate model performance on the validation set
metrics = model.val()
metrics.metric_names  # List of available metrics
metrics.ap  # Average Precision (AP)

# Export the model to ONNX format
path = model.export(format="onnx")