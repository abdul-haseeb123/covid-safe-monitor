from ultralytics import YOLO
import os

# Load model
model = YOLO("yolo11n.pt")

sample_img = "dataset/images/train/maksssksksss0.png"

results = model.predict(sample_img)


for r in results:
    print(r.boxes)
