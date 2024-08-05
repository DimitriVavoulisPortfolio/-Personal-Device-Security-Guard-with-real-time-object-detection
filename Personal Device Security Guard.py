import cv2
import numpy as np
import os
from datetime import datetime
import traceback
import time

def main():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        yolo_dir = os.path.join(script_dir, "yolo_files")
        
        download_dir = os.path.join(os.path.expanduser("~"), "Downloads", "object_detection_results")
        os.makedirs(download_dir, exist_ok=True)

        use_tiny = input("Use YOLOv3-tiny for faster processing? (y/n): ").lower() == 'y'

        if use_tiny:
            weights_path = os.path.join(yolo_dir, "yolov3-tiny.weights")
            cfg_path = os.path.join(yolo_dir, "yolov3-tiny.cfg")
        else:
            weights_path = os.path.join(yolo_dir, "yolov3.weights")
            cfg_path = os.path.join(yolo_dir, "yolov3.cfg")

        names_path = os.path.join(yolo_dir, "coco.names")

        if not all(os.path.exists(f) for f in [weights_path, cfg_path, names_path]):
            raise FileNotFoundError("YOLO files are missing. Please run setup.py first.")

        print("Loading YOLO model...")
        net = cv2.dnn.readNet(weights_path, cfg_path)
        
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

        with open(names_path, "r") as f:
            classes = [line.strip() for line in f.readlines()]
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
        print("YOLO model loaded successfully.")

        print("Initializing camera...")
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        if not cap.isOpened():
            raise Exception("Could not open video capture. Make sure a camera is connected and not in use by another application.")

        ret, frame = cap.read()
        if not ret:
            raise Exception("Failed to capture frame from camera. The camera may be in use by another application.")

        print("Camera initialized successfully.")
        print("Object detection is running. Press 'q' to quit.")

        frame_count = 0
        start_time = time.time()
        previous_objects = set()

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame. Retrying...")
                time.sleep(1)
                continue
            
            frame_count += 1
            if frame_count % 2 != 0:  # Process every other frame
                continue

            height, width = frame.shape[:2]

            blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
            net.setInput(blob)
            outs = net.forward(output_layers)

            class_ids = []
            confidences = []
            boxes = []
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5:
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)
                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
            
            current_objects = set()
            font = cv2.FONT_HERSHEY_PLAIN
            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    label = str(classes[class_ids[i]])
                    current_objects.add(label)
                    color = (0, 255, 0)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, label, (x, y + 30), font, 2, color, 2)

            # Check for changes in detected objects
            if current_objects != previous_objects:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"snapshot_{timestamp}.jpg"
                filepath = os.path.join(download_dir, filename)
                cv2.imwrite(filepath, frame)
                print(f"Change detected! Snapshot saved as {filepath}")
                print(f"Previous objects: {previous_objects}")
                print(f"Current objects: {current_objects}")
                previous_objects = current_objects.copy()

            cv2.imshow('Object Detection', frame)
            
            if frame_count % 30 == 0:
                end_time = time.time()
                fps = 30 / (end_time - start_time)
                print(f"FPS: {fps:.2f}")
                start_time = time.time()

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Traceback:")
        print(traceback.format_exc())
        print("\nPress Enter to exit...")
        input()

if __name__ == "__main__":
    main()