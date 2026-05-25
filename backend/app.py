"""FastAPI Backend for Object Detection & Tracking"""
import cv2
import time
import numpy as np
import tempfile
import os
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse, FileResponse, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="VisionScan API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import after FastAPI setup
try:
    from detector import ObjectDetector
    from tracker import ObjectTracker
    detector = ObjectDetector(model_name="yolov8n.pt", conf_threshold=0.5)
    tracker = ObjectTracker()
    print("[INFO] Models loaded successfully")
except Exception as e:
    print(f"[ERROR] Failed to load models: {e}")
    detector = None
    tracker = None

# Global state
class AppState:
    def __init__(self):
        self.camera_active = False
        self.cap = None
        self.stats = {"fps": 0, "total_objects": 0, "object_counts": {}, "tracked_objects": [], "camera_status": "stopped"}

app_state = AppState()

@app.get("/")
def root():
    return {"message": "VisionScan API", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": time.time()}

@app.post("/start_camera")
def start_camera():
    try:
        if not app_state.camera_active:
            app_state.cap = cv2.VideoCapture(0)
            app_state.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            app_state.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            
            if not app_state.cap.isOpened():
                app_state.cap = None
                print("[ERROR] Camera not found")
                return {"status": "error", "message": "Camera not found"}
            
            app_state.camera_active = True
            app_state.stats["camera_status"] = "running"
            print("[INFO] Camera started")
            return {"status": "started", "message": "Camera started successfully"}
        return {"status": "already_running", "message": "Camera is already running"}
    except Exception as e:
        print(f"[ERROR] start_camera: {e}")
        return {"status": "error", "message": str(e)}

@app.post("/stop_camera")
def stop_camera():
    try:
        if app_state.camera_active:
            app_state.camera_active = False
            if app_state.cap:
                app_state.cap.release()
            app_state.stats["camera_status"] = "stopped"
            print("[INFO] Camera stopped")
            return {"status": "stopped", "message": "Camera stopped successfully"}
        return {"status": "already_stopped", "message": "Camera is not running"}
    except Exception as e:
        print(f"[ERROR] stop_camera: {e}")
        return {"status": "error", "message": str(e)}

def generate_frames():
    frame_count = 0
    start_time = time.time()
    
    while app_state.camera_active:
        try:
            if app_state.cap is None or not app_state.cap.isOpened():
                app_state.camera_active = False
                break
                
            ret, frame = app_state.cap.read()
            if not ret:
                app_state.camera_active = False
                break
            
            if detector is None:
                app_state.camera_active = False
                break
            
            detections = detector.detect(frame)
            tracks = tracker.update(detections, frame) if tracker else []
            
            if tracks:
                frame = tracker.draw_tracks(frame, tracks)
                n_objects = len(tracks)
            elif detections:
                frame = detector.draw_detections(frame, detections)
                n_objects = len(detections)
            else:
                n_objects = 0
            
            frame_count += 1
            elapsed = time.time() - start_time
            fps = frame_count / elapsed if elapsed > 0 else 0
            
            cv2.rectangle(frame, (0, 0), (frame.shape[1], 35), (10, 10, 10), -1)
            cv2.putText(frame, f"FPS: {fps:.1f}", (10, 23), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 120), 2)
            cv2.putText(frame, f"Objects: {n_objects}", (150, 23), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 210, 255), 2)
            
            object_counts = {}
            for track in tracks:
                label = track.get("label", "unknown")
                object_counts[label] = object_counts.get(label, 0) + 1
            
            app_state.stats.update({
                "fps": round(fps, 1),
                "total_objects": n_objects,
                "object_counts": object_counts,
                "tracked_objects": tracks[:10],
                "camera_status": "running"
            })
            
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        except Exception as e:
            print(f"[ERROR] generate_frames: {e}")
            app_state.camera_active = False
            break

@app.get("/video_feed")
def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/stats")
def get_stats():
    return app_state.stats

@app.post("/detect_image")
async def detect_image(file: UploadFile = File(...), threshold: float = Form(0.5), show_labels: bool = Form(True)):
    output_path = None
    try:
        if detector is None:
            return {"error": "Detector not initialized"}
        
        # Validate file extension
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp'}
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in allowed_extensions:
            return {"error": f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"}
        
        print(f"[INFO] Detecting image: {file.filename}")
        contents = await file.read()
        
        if not contents:
            return {"error": "Empty file"}
        
        nparr = np.frombuffer(contents, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            print("[ERROR] Invalid image format")
            return {"error": "Invalid image format"}
        
        print(f"[INFO] Image shape: {frame.shape}")
        
        detector.conf_threshold = float(threshold)
        detections = detector.detect(frame)
        print(f"[INFO] Detected {len(detections)} objects")
        
        if show_labels:
            frame = detector.draw_detections(frame, detections)
        else:
            for det in detections:
                x1, y1, x2, y2 = det["x1"], det["y1"], det["x2"], det["y2"]
                color = detector._get_color(det["class_id"])
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        
        output_path = tempfile.mktemp(suffix='.jpg')
        success = cv2.imwrite(output_path, frame)
        if not success:
            print("[ERROR] Failed to save image")
            return {"error": "Failed to save image"}
        
        print("[INFO] Image detection complete")
        return FileResponse(output_path, media_type="image/jpeg", filename="detected_output.jpg")
    except Exception as e:
        print(f"[ERROR] detect_image: {e}")
        if output_path and os.path.exists(output_path):
            try:
                os.unlink(output_path)
            except:
                pass
        return {"error": str(e)}

@app.post("/process_video")
async def process_video(file: UploadFile = File(...), threshold: float = Form(0.5), show_labels: bool = Form(True)):
    input_path = None
    output_path = None
    try:
        if detector is None or tracker is None:
            return {"error": "Models not initialized"}
        
        # Validate file extension
        allowed_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm'}
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in allowed_extensions:
            return {"error": f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"}
        
        print(f"[INFO] Processing video: {file.filename}")
        contents = await file.read()
        
        if not contents:
            return {"error": "Empty file"}
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.avi') as tmp_in:
            tmp_in.write(contents)
            input_path = tmp_in.name
        
        print(f"[INFO] Video saved to: {input_path}")
        
        output_path = tempfile.mktemp(suffix='.avi')
        detector.conf_threshold = float(threshold)
        video_tracker = ObjectTracker()
        
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            print("[ERROR] Failed to open video")
            return {"error": "Failed to open video file"}
        
        fps_in = cap.get(cv2.CAP_PROP_FPS) or 25
        W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        print(f"[INFO] Video: {W}x{H} @ {fps_in} fps, {total_frames} frames")
        
        if W == 0 or H == 0:
            cap.release()
            print("[ERROR] Invalid video dimensions")
            return {"error": "Invalid video dimensions"}
        
        writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'MJPG'), fps_in, (W, H))
        
        frame_count = 0
        start_time = time.time()
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            detections = detector.detect(frame)
            tracks = video_tracker.update(detections, frame)
            
            if tracks and show_labels:
                frame = video_tracker.draw_tracks(frame, tracks)
            elif detections and show_labels:
                frame = detector.draw_detections(frame, detections)
            elif tracks:
                for track in tracks:
                    x1, y1, x2, y2 = track["box"]
                    color = video_tracker._get_color(track["tid"])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            elif detections:
                for det in detections:
                    x1, y1, x2, y2 = det["x1"], det["y1"], det["x2"], det["y2"]
                    color = detector._get_color(det["class_id"])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            elapsed = time.time() - start_time
            fps = frame_count / elapsed if elapsed > 0 else 0
            n_objects = len(tracks) if tracks else len(detections)
            
            cv2.rectangle(frame, (0, 0), (W, 35), (10, 10, 10), -1)
            cv2.putText(frame, f"FPS: {fps:.1f}", (10, 23), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 120), 2)
            cv2.putText(frame, f"Objects: {n_objects}", (150, 23), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 210, 255), 2)
            
            writer.write(frame)
            frame_count += 1
            
            if frame_count % 30 == 0:
                print(f"[INFO] Processed {frame_count}/{total_frames} frames")
        
        cap.release()
        writer.release()
        
        print(f"[INFO] Video processing complete: {frame_count} frames")
        
        if input_path and os.path.exists(input_path):
            try:
                os.unlink(input_path)
            except Exception as e:
                print(f"[WARNING] Failed to delete input file: {e}")
        
        if not os.path.exists(output_path):
            print("[ERROR] Output video file not created")
            return {"error": "Failed to create output video"}
        
        print(f"[INFO] Returning video file: {output_path}")
        
        # Read file and return as blob
        with open(output_path, 'rb') as f:
            video_data = f.read()
        
        # Clean up temp file
        try:
            os.unlink(output_path)
        except Exception as e:
            print(f"[WARNING] Failed to delete output file: {e}")
        
        return Response(content=video_data, media_type="video/x-msvideo", headers={"Content-Disposition": "attachment; filename=tracked_output.avi"})
    except Exception as e:
        print(f"[ERROR] process_video: {e}")
        if input_path and os.path.exists(input_path):
            try:
                os.unlink(input_path)
            except Exception as ex:
                print(f"[WARNING] Failed to delete input file: {ex}")
        if output_path and os.path.exists(output_path):
            try:
                os.unlink(output_path)
            except Exception as ex:
                print(f"[WARNING] Failed to delete output file: {ex}")
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    print("\n[INFO] Starting VisionScan API on http://localhost:8000\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
