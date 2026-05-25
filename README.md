# VisionScan - Real-Time Object Detection & Tracking

A full-stack web application I built for real-time object detection and tracking using YOLOv8 and Deep SORT. This project combines a React frontend with a FastAPI backend to deliver a smooth, interactive experience for detecting and tracking objects in live video feeds.

## What This Project Does

I created VisionScan to solve the problem of tracking multiple objects in real-time. Whether you're working with webcam feeds or video files, this application:

- Detects objects in real-time using YOLOv8 (the nano model for speed)
- Tracks multiple objects simultaneously with stable IDs across frames
- Displays live statistics like FPS, object counts, and confidence scores
- Provides a clean, modern dashboard to interact with everything
- Offers a RESTful API for programmatic access

## Tech Stack

**Frontend:**
- React 18 with Vite (fast development experience)
- Tailwind CSS for styling (though I customized it heavily)
- Axios for API calls
- Modern ES6+ JavaScript

**Backend:**
- Python 3.8+ with FastAPI (incredibly fast and easy to work with)
- OpenCV for video processing
- YOLOv8 from Ultralytics (state-of-the-art detection)
- Deep SORT for object tracking
- PyTorch as the deep learning backbone

## Project Structure

```
Object Detection Tracking/
├── backend/
│   ├── app.py              # Main FastAPI application
│   ├── detector.py         # YOLOv8 detection logic
│   ├── tracker.py          # Deep SORT tracking logic
│   ├── requirements.txt    # Python dependencies
│   └── models/             # Model storage
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   ├── App.css         # Styling
│   │   ├── main.jsx        # Entry point
│   │   └── index.css       # Global styles
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── tsconfig.json
│
└── README.md
```

## Getting Started

### Prerequisites

You'll need:
- Python 3.8 or higher
- Node.js 18 or higher
- A webcam (optional, for live detection)
- 4GB+ RAM recommended

### Installation

**Step 1: Clone the repository**
```bash
git clone https://github.com/HarshaKurasala/Object-detection-Tracking.git
cd "Object Detection Tracking"
```

**Step 2: Set up the backend**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

**Step 3: Set up the frontend**
```bash
cd ../frontend
npm install
```

### Running the Application

**Terminal 1 - Start the backend:**
```bash
cd backend
venv\Scripts\activate
python app.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2 - Start the frontend:**
```bash
cd frontend
npm run dev
```

You should see:
```
VITE v5.0.0  ready in 234 ms
➜  Local:   http://localhost:5173/
```

**Open your browser to:** `http://localhost:5173`

## How to Use

### Webcam Detection
1. Click the "Webcam" tab
2. Hit "Start Camera" to begin live detection
3. Watch objects get detected and tracked in real-time
4. View live statistics on the right panel

### Image Detection
1. Click the "Image" tab
2. Upload an image file
3. The system processes it and shows detections with bounding boxes

### Video Processing
1. Click the "Video" tab
2. Upload a video file
3. Wait for processing (depends on video length)
4. Download the processed video with tracking overlays

## API Endpoints

I built a clean REST API for programmatic access:

**Health Check**
```
GET /health
```

**Camera Control**
```
POST /start_camera
POST /stop_camera
```

**Video Stream**
```
GET /video_feed
```

**Statistics**
```
GET /stats
```

**File Processing**
```
POST /upload_video
POST /detect_image
```

## Configuration

You can customize the detection behavior by editing `backend/app.py`:

```python
# Change the model (options: yolov8n, yolov8s, yolov8m, yolov8l, yolov8x)
detector = ObjectDetector(model_name="yolov8n.pt", conf_threshold=0.5)

# Adjust video resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
```

## Troubleshooting

**Camera not starting?**
- Check if another app is using your webcam
- Try restarting the backend server
- Grant camera permissions to Python

**Slow performance?**
- The nano model (yolov8n) is already optimized for speed
- Try reducing video resolution
- Close other applications
- Consider using GPU if available

**Port already in use?**
- Change the port in `backend/app.py`: `uvicorn.run(app, host="0.0.0.0", port=8001)`
- Or in `frontend/vite.config.js`: `port: 5174`

**Module not found errors?**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
npm install --legacy-peer-deps
```

## What I Learned Building This

- How to integrate YOLOv8 for real-time detection
- Deep SORT tracking algorithm and its implementation
- Building responsive UIs with React and Vite
- Creating high-performance APIs with FastAPI
- Video processing with OpenCV
- Managing state in full-stack applications

## Future Ideas

I'm thinking about adding:
- GPU acceleration support (CUDA)
- Multi-camera support
- Database storage for tracking history
- Real-time alerts
- Video export with annotations
- Mobile app version
- Custom model training interface

## Challenges I Faced

1. **Video Codec Issues** - Spent time figuring out the right codec (MJPG works best)
2. **Tracking Stability** - Fine-tuning Deep SORT parameters for smooth tracking
3. **Performance** - Optimizing frame processing to maintain good FPS
4. **State Management** - Handling global state safely in the backend

## License

MIT License - feel free to use this for your own projects

## Acknowledgments

- Ultralytics for the amazing YOLOv8 model
- The Deep SORT community
- React and FastAPI communities for excellent frameworks

---

**Built with ❤️ during my internship at CodeAlpha**

Feel free to reach out if you have questions or suggestions!
