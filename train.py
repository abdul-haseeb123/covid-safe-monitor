from ultralytics import YOLO

# Load a pretrained YOLO model (recommended for training)
model = YOLO("yolo11n-pose.pt")

results = model.predict(source="sample-videos/saboor-walk.mp4", save=True)



