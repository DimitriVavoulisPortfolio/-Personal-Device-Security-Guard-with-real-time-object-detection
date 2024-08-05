# Personal Device Security Guard

## Author
Dimitri Vavoulis

## Overview
This project implements an innovative security system for personal devices, acting as a virtual guard dog when you're away from your computer or smartphone. Utilizing advanced computer vision techniques, it transforms your device's camera into a vigilant security monitor, alerting you to any unexpected activity in its vicinity.

## Key Security Features
- Continuous Monitoring: Keeps watch over your device's surroundings when you're away.
- Intelligent Change Detection: Automatically identifies new objects or people entering the monitored area.
- Snapshot Evidence: Captures and saves images when changes are detected, providing a visual record of any potential security breaches.
- Privacy-Focused: Operates locally on your device, ensuring your security footage remains private.

## Technical Specifications
- Real-time object detection using the YOLO (You Only Look Once) algorithm
- Support for both YOLOv3 (high accuracy) and YOLOv3-tiny (faster processing) models
- FPS (Frames Per Second) monitoring for optimal performance
- Customizable detection sensitivity to minimize false alarms

## Project Structure
1. `setup.py`: Initial configuration script that:
   - Installs necessary dependencies
   - Downloads required YOLO model files
   - Prepares the security environment

2. `Personal_Device_Security_Guard.py`: Core security application that:
   - Activates your device's camera
   - Processes the video feed in real-time
   - Detects and analyzes changes in the monitored area
   - Automatically captures and stores security snapshots
   - Provides a live feed with highlighted detected objects (when actively monitored)

## Technologies Employed
- Python: Core programming language
- OpenCV (cv2): For image processing and camera interfacing
- NumPy: For efficient numerical operations
- YOLO (YOLOv3 and YOLOv3-tiny): State-of-the-art object detection models

## Setup and Deployment
1. Execute `setup.py` to configure the security environment.
2. Run `Personal_Device_Security_Guard.py` to activate the security system.
3. Select your preferred model: YOLOv3 (higher security, more resource-intensive) or YOLOv3-tiny (faster, ideal for less powerful devices).
4. The system will begin monitoring, saving snapshots of any detected changes.
5. To deactivate, press 'q' in the application window.

## Performance Optimization
- Adaptable to various hardware configurations
- YOLOv3-tiny option available for resource-constrained devices
- GPU acceleration support for enhanced performance on compatible systems

## Future Security Enhancements
- Remote monitoring and alert system integration
- Custom object recognition for personalized security (e.g., recognizing specific individuals)
- Integration with smart home security systems

This project demonstrates expertise in computer vision, real-time data processing, and creating practical security solutions. It showcases the ability to develop sophisticated, user-centric security applications for personal devices.
