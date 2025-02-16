import xml.etree.ElementTree as ET
import os
from zipfile import ZipFile
import random

def normalize_save_bbox(filepath, dest_path):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    if filepath[-4:] != ".xml":
        raise ValueError("File must be in XML format")
    tree = ET.parse(filepath)
    full_width = float(tree.find("size").find("width").text)
    full_height = float(tree.find("size").find("height").text)
    objects = tree.findall("object")
    
    records = []
    for obj in objects:
        data = [obj.find("name").text, 
                float(obj.find("bndbox").find("xmin").text),
                float(obj.find("bndbox").find("xmax").text),
                float(obj.find("bndbox").find("ymin").text),
                float(obj.find("bndbox").find("ymax").text)]
        records.append(data)

     # Extract values from the input array
    result = ""
    for data in records:
        name = data[0]
        label = 0
        if name == "with_mask":
            label = 0
        elif name == "without_mask":
            label = 1
        else:
            label = 2
        xmin, xmax, ymin, ymax = data[1], data[2], data[3], data[4]

        # Calculate width and height of the bounding box
        width = xmax - xmin
        height = ymax - ymin

        # Calculate center coordinates (xcenter, ycenter)
        xcenter = xmin + (width / 2)
        ycenter = ymin + (height / 2)

        # Normalize coordinates to [0, 1] range
        xcenter_norm = xcenter / full_width
        ycenter_norm = ycenter / full_height
        width_norm = width / full_width  # This will always be 1
        height_norm = height / full_height  # This will always be 1

        # Prepare the output string
        result += f"{label} {xcenter_norm:.6f} {ycenter_norm:.6f} {width_norm:.6f} {height_norm:.6f}\n"

    # Write the output to the text file
    with open(dest_path, 'w') as file:
        file.write(result)

with ZipFile("face-mask-detection.zip", "r") as zip_ref:
    images_list = [x.split("/")[-1] for x in zip_ref.namelist() if x.startswith("images/")]
       
    val_dir = os.path.join(os.getcwd(), "dataset", "images", "val")
    val_dir_labels = os.path.join(os.getcwd(), "dataset", "labels", "val")
    train_dir = os.path.join(os.getcwd(), "dataset", "images", "train")
    train_dir_labels = os.path.join(os.getcwd(), "dataset", "labels", "train")
    tmp_dir = os.path.join(os.getcwd(), "tmp")

    os.makedirs(val_dir, exist_ok=True)
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir_labels, exist_ok=True)
    os.makedirs(train_dir_labels, exist_ok=True)

    # Randomly select 214 images for the val directory
    val_images = random.sample(images_list, 214)

    for image_name in images_list:
        if image_name in val_images:
            zip_ref.extract(f"images/{image_name}", val_dir)

            zip_ref.extract(f"annotations/{image_name[:-3]}xml", tmp_dir)
            normalize_save_bbox(os.path.join(tmp_dir, "annotations", f"{image_name[:-3]}xml"), os.path.join(val_dir_labels, f"{image_name[:-3]}txt"))
        else:
            zip_ref.extract(f"images/{image_name}", train_dir)

            zip_ref.extract(f"annotations/{image_name[:-3]}xml", tmp_dir)
            normalize_save_bbox(os.path.join(tmp_dir, "annotations", f"{image_name[:-3]}xml"), os.path.join(train_dir_labels, f"{image_name[:-3]}txt"))

    print("Data extraction completed!")
    

