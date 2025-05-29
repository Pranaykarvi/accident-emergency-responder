# src/utils/download_dataset.py

from roboflow import Roboflow
import shutil
import os

def download_dataset():
    # Initialize Roboflow with your private API key
    rf = Roboflow(api_key="KPw0WjS0xPqm5rEJ1ptP")
    
    # Access the project and version
    project = rf.workspace("accident-detection-model").project("accident-detection-model")
    dataset = project.version(2).download("yolov8")  # Change format if you want (e.g., "yolov5")

    # Define target folder (datasets/labeled relative to this script)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.abspath(os.path.join(current_dir, "../../datasets/labeled"))

    # Remove old labeled dataset folder if exists
    if os.path.exists(target_dir):
        print(f"Removing old dataset folder: {target_dir}")
        shutil.rmtree(target_dir)

    # Move downloaded dataset folder to target_dir
    print(f"Moving downloaded dataset from {dataset.location} to {target_dir}")
    shutil.move(dataset.location, target_dir)

    print(f"Dataset downloaded and moved to: {target_dir}")

if __name__ == "__main__":
    download_dataset()
