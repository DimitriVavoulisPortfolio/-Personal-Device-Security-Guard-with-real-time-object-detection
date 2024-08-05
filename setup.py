import sys
import subprocess
import os
import urllib.request

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

print("Setting up Object Detection application...")

# Check and install required packages
required_packages = ['opencv-python', 'numpy']
for package in required_packages:
    try:
        __import__(package)
        print(f"{package} is already installed.")
    except ImportError:
        print(f"{package} not found. Installing...")
        install_package(package)

# Create a directory for downloads if it doesn't exist
script_dir = os.path.dirname(os.path.abspath(__file__))
download_dir = os.path.join(script_dir, "yolo_files")
os.makedirs(download_dir, exist_ok=True)
print(f"Created directory for YOLO files: {download_dir}")

# Define YOLO files and their URLs
yolo_files = {
    "yolov3.weights": "https://pjreddie.com/media/files/yolov3.weights",
    "yolov3.cfg": "https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg",
    "yolov3-tiny.weights": "https://pjreddie.com/media/files/yolov3-tiny.weights",
    "yolov3-tiny.cfg": "https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3-tiny.cfg",
    "coco.names": "https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names"
}

# Download YOLO files if they don't exist
for file_name, url in yolo_files.items():
    file_path = os.path.join(download_dir, file_name)
    if not os.path.exists(file_path):
        print(f"Downloading {file_name}...")
        urllib.request.urlretrieve(url, file_path)
        print(f"{file_name} downloaded successfully.")
    else:
        print(f"{file_name} already exists.")

print("\nSetup completed successfully!")
print("You can now run the object detection application by running 'object_detection_app.py'")
input("Press Enter to exit...")