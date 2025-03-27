
import torch
import cv2
import os

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # Use 'yolov5s', 'yolov5m', 'yolov5l', or 'yolov5x'

inputPath = os.getcwd() + "/test_images/"
outputPath = os.getcwd() + "/output_images/"

def detectVehicles(filename):
    global model, inputPath, outputPath
    img_path = inputPath + filename
    img = cv2.imread(img_path)

    # Perform inference
    results = model(img)

    # Filter results for vehicles
    vehicle_labels = ["car", "bus", "truck", "motorcycle", "bicycle"]
    detections = results.pandas().xyxy[0]  # Get predictions as a pandas DataFrame
    for _, row in detections.iterrows():
        if row['name'] in vehicle_labels:
            # Draw bounding box and label
            top_left = (int(row['xmin']), int(row['ymin']))
            bottom_right = (int(row['xmax']), int(row['ymax']))
            label = row['name']
            img = cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 3)
            img = cv2.putText(img, label, top_left, cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)

    # Save the output image
    outputFilename = outputPath + "output_" + filename
    cv2.imwrite(outputFilename, img)
    print('Output image stored at:', outputFilename)

# Process all images in the input folder
if not os.path.exists(outputPath):
    os.makedirs(outputPath)

for filename in os.listdir(inputPath):
    if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
        detectVehicles(filename)

print("Done!")