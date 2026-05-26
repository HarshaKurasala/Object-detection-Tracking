"""YOLOv8 Object Detector"""
import cv2
import numpy as np
from ultralytics import YOLO

class ObjectDetector:
    # Constructor to initialize the YOLOv8 object detection model
    # Parameters: model_name - YOLOv8 model variant to load
    #           conf_threshold - minimum confidence score for detections (0.0-1.0)
    def __init__(self, model_name="yolov8n.pt", conf_threshold=0.5):
        self.model = YOLO(model_name)
        self.conf_threshold = conf_threshold
        
    # Main detection method - runs YOLOv8 inference on a frame
    # Parameter: frame - input image (numpy array in BGR format)
    # Returns: list of detection dictionaries with bounding boxes, confidence, and class labels
    def detect(self, frame):
        try:
            results = self.model(frame, conf=self.conf_threshold, verbose=False)
            detections = []
            
            if results and len(results) > 0:
                result = results[0]
                if result.boxes is not None and len(result.boxes) > 0:
                    for box in result.boxes:
                        try:
                            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                            conf = float(box.conf[0])
                            cls_id = int(box.cls[0])
                            label = self.model.names[cls_id]
                            
                            detections.append({
                                "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                                "conf": conf,
                                "label": label,
                                "class_id": cls_id
                            })
                        except Exception as e:
                            print(f"[ERROR] Processing box: {e}")
                            continue
            
            return detections
        except Exception as e:
            print(f"[ERROR] Detection failed: {e}")
            return []
    
    # Draws detection bounding boxes and labels on the frame
    # Parameters: frame - input image
    #            detections - list of detection dictionaries from detect() method
    # Returns: annotated frame with drawn boxes and labels
    def draw_detections(self, frame, detections):
        try:
            if not detections:
                return frame
                
            for det in detections:
                try:
                    x1, y1, x2, y2 = det["x1"], det["y1"], det["x2"], det["y2"]
                    color = self._get_color(det["class_id"])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    
                    label = f"{det['label']} {det['conf']:.2f}"
                    self._put_label(frame, label, x1, y1, color)
                except Exception as e:
                    print(f"[ERROR] Drawing detection: {e}")
                    continue
            
            return frame
        except Exception as e:
            print(f"[ERROR] draw_detections: {e}")
            return frame
    
    # Helper method to assign consistent colors to different object classes
    # Parameter: class_id - the class identifier from YOLO model
    # Returns: BGR color tuple (B, G, R) for consistent visualization
    def _get_color(self, class_id):
        colors = [
            (255, 56, 56), (255, 157, 51), (255, 225, 51), (99, 226, 87),
            (45, 211, 153), (56, 185, 255), (69, 83, 255), (209, 34, 255),
            (255, 72, 186), (160, 237, 87), (71, 193, 193), (255, 142, 203)
        ]
        return colors[int(class_id) % len(colors)]
    
    # Helper method to draw text labels on frames with background rectangle
    # Parameters: frame - image to draw on
    #            text - label text to display
    #            x, y - position for label placement
    #            color - BGR color tuple for the rectangle background
    def _put_label(self, frame, text, x, y, color):
        try:
            (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            y0 = max(y, th + 10)
            cv2.rectangle(frame, (x, y0 - th - 6), (x + tw + 4, y0), color, -1)
            cv2.putText(frame, text, (x + 2, y0 - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        except Exception as e:
            print(f"[ERROR] _put_label: {e}")
