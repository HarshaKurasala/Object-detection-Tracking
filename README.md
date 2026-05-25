# 🎯 Real-Time Object Detection & Tracking Application

An AI-powered full-stack application for real-time object detection and tracking using YOLOv8, Deep SORT, and modern web technologies.

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [API Endpoints](#-api-endpoints)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### Core Capabilities
- ✅ **Real-Time Webcam Detection** - Live object detection from webcam feed
- ✅ **Video File Processing** - Upload and process video files
- ✅ **Multi-Object Tracking** - Track multiple objects simultaneously
- ✅ **Deep SORT Tracking** - Stable tracking IDs across frames
- ✅ **YOLOv8 Detection** - Lightning-fast object detection
- ✅ **Bounding Boxes** - Visual object localization
- ✅ **Confidence Scores** - Detection confidence percentages
- ✅ **Real-Time Analytics** - Live FPS, object counts, and statistics
- ✅ **Tracking Table** - Detailed tracking information display
- ✅ **RESTful API** - Clean HTTP API for all operations
- ✅ **Responsive UI** - Modern, adaptive dashboard
- ✅ **Dark Theme** - Futuristic AI dashboard design

---

## 🛠 Tech Stack

### Frontend
- **React 18** - UI framework
- **Vite** - Lightning-fast build tool
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client
- **React Icons** - Icon library
- **Modern ES6+** - Latest JavaScript

### Backend
- **Python 3.8+** - Programming language
- **FastAPI** - High-performance web framework
- **Uvicorn** - ASGI server
- **OpenCV (cv2)** - Computer vision library
- **YOLOv8 (Ultralytics)** - Object detection model
- **Deep SORT** - Multi-object tracking
- **PyTorch** - Deep learning framework
- **NumPy** - Numerical computing

### AI/CV Stack
- **YOLOv8n** - Nano model for fast inference
- **Deep SORT** - Hungarian algorithm-based tracking
- **OpenCV** - Video capture and processing

---

## 📁 Project Structure

```
project/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── HeroSection.jsx
│   │   │   ├── LiveDetectionPanel.jsx
│   │   │   ├── AnalyticsCards.jsx
│   │   │   ├── TrackingTable.jsx
│   │   │   ├── SettingsPanel.jsx
│   │   │   └── Footer.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── tsconfig.json
│   └── .gitignore
│
├── backend/
│   ├── app.py              # Main FastAPI application
│   ├── detector.py         # YOLOv8 detector logic
│   ├── tracker.py          # Deep SORT tracker logic
│   ├── requirements.txt    # Python dependencies
│   ├── models/             # Model storage directory
│   └── .gitignore
│
└── README.md
```

---

## 📦 Prerequisites

- **Python 3.8+** (for backend)
- **Node.js 18+** (for frontend)
- **npm or yarn** (package manager)
- **Git** (version control)
- **Webcam or video file** (for detection)
- **4GB+ RAM** (recommended)
- **GPU support** (optional, for faster inference)

---

## 🚀 Installation

### Step 1: Clone or Download the Project

```bash
cd "C:\Users\Harsha Vardhan\Documents\CodeAlpha_internprojs\Object Detection Tracking"
```

### Step 2: Backend Setup

#### 2.1 Create Virtual Environment (Windows)

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
```

#### 2.2 Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI & Uvicorn
- OpenCV
- YOLOv8 (Ultralytics)
- Deep SORT
- PyTorch
- NumPy
- And other dependencies

**Note**: First time installation may take 5-10 minutes as PyTorch and YOLOv8 models are downloaded.

### Step 3: Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Or with yarn
yarn install
```

---

## ⚡ Quick Start

### Terminal 1: Start Backend Server

```powershell
cd backend
venv\Scripts\activate
python app.py
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

The backend will be available at: `http://localhost:8000`

### Terminal 2: Start Frontend Development Server

```powershell
cd frontend
npm run dev
```

Expected output:
```
  VITE v5.0.0  ready in 234 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

### Terminal 3: Access the Application

Open your browser and navigate to: `http://localhost:5173`

---

## 🔌 API Endpoints

### Health Check
```
GET /health
```
Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": 1234567890.123
}
```

### Root Endpoint
```
GET /
```
Get API information and available endpoints.

### Start Camera
```
POST /start_camera
```
Start webcam capture and real-time detection.

**Response:**
```json
{
  "status": "started",
  "message": "Camera started successfully"
}
```

### Stop Camera
```
POST /stop_camera
```
Stop webcam capture.

**Response:**
```json
{
  "status": "stopped",
  "message": "Camera stopped successfully"
}
```

### Video Feed Stream
```
GET /video_feed
```
Stream real-time processed video feed (MJPEG format).

**Usage:**
```html
<img src="http://localhost:8000/video_feed" />
```

### Get Statistics
```
GET /stats
```
Get current detection statistics.

**Response:**
```json
{
  "fps": 28.5,
  "total_objects": 3,
  "object_counts": {
    "person": 2,
    "car": 1
  },
  "tracked_objects": [
    {
      "id": 1,
      "class": "person",
      "confidence": 0.95,
      "bbox": [100, 150, 250, 500]
    }
  ],
  "camera_status": "running"
}
```

### Upload Video
```
POST /upload_video
Content-Type: multipart/form-data

File: video.mp4
```

Process a video file for detection and tracking.

**Response:**
```json
{
  "status": "processed",
  "filename": "video.mp4",
  "total_frames": 100,
  "frames_data": [...]
}
```

---

## ⚙️ Configuration

### Backend Configuration

Edit `backend/app.py` to customize:

```python
# Model configuration
detector = ObjectDetector(
    model_name="yolov8n.pt",  # Options: yolov8n, yolov8s, yolov8m, yolov8l, yolov8x
    conf_threshold=0.5        # Confidence threshold (0-1)
)

# Tracker configuration
tracker = ObjectTracker()
# Edit tracker initialization for custom parameters
```

### Frontend Configuration

Edit `frontend/src/App.jsx` for API configuration:

```javascript
const API_URL = 'http://localhost:8000'
const STATS_UPDATE_INTERVAL = 500 // milliseconds
```

### Video Capture Settings

Modify in `backend/app.py`:

```python
cap = cv2.VideoCapture(0)  # 0 for default webcam
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
```

---

## 📖 Usage

### 1. **Start Real-Time Detection**

1. Open the dashboard at `http://localhost:5173`
2. Click **"Start Camera"** button
3. Live webcam feed will appear with:
   - Bounding boxes around detected objects
   - Tracking IDs (e.g., "ID:1 person")
   - Confidence scores
   - FPS counter

### 2. **View Analytics**

- **FPS**: Current frames per second
- **Total Objects**: Number of detected and tracked objects
- **Persons**: Count of person detections
- **Vehicles**: Count of vehicle detections (cars, trucks, buses)

### 3. **Tracking Table**

View detailed information about tracked objects:
- Unique tracking ID
- Object class
- Confidence percentage
- Position (X, Y coordinates)
- Status (Active/Inactive)

### 4. **Adjust Settings**

Fine-tune detection parameters:
- **Confidence Threshold**: Minimum confidence for detections (0-100%)
- **Max Tracking Age**: Maximum frames to keep unmatched tracks
- **Min Tracking Hits**: Minimum hits to confirm a track

### 5. **Upload Video**

Process video files (feature in API, can be added to UI):

```bash
curl -X POST -F "file=@video.mp4" http://localhost:8000/upload_video
```

---

## 🐛 Troubleshooting

### Issue: Camera Not Starting

**Solution:**
1. Check if another application is using the webcam
2. Grant camera permissions to Python/browser
3. Try restarting the backend server

### Issue: Slow Performance / Low FPS

**Solution:**
1. Use smaller YOLOv8 model: `yolov8n.pt` (default)
2. Reduce video resolution in `app.py`
3. Close other applications
4. Use GPU if available (CUDA support)

### Issue: Port Already in Use

**Solution:**
```bash
# Change backend port in app.py
uvicorn.run(app, host="0.0.0.0", port=8001)

# Change frontend port in vite.config.js
server: {
  port: 5174
}
```

### Issue: Module Not Found Errors

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Or for frontend
npm install --legacy-peer-deps
```

### Issue: CUDA/GPU Not Working

**Solution:**
1. Install CUDA Toolkit from NVIDIA
2. Install cuDNN
3. Reinstall PyTorch with CUDA support:
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

### Issue: Memory Issues

**Solution:**
1. Reduce frame size in `app.py`:
   ```python
   frame = cv2.resize(frame, (320, 240))
   ```
2. Limit video frames in `/upload_video`
3. Increase system RAM or use cloud GPU

---

## 📊 Model Information

### YOLOv8 Models

| Model | Size | Speed | mAP |
|-------|------|-------|-----|
| YOLOv8n | 3.2 MB | 80ms | 37.3 |
| YOLOv8s | 11 MB | 100ms | 44.9 |
| YOLOv8m | 26 MB | 234ms | 50.2 |
| YOLOv8l | 52 MB | 375ms | 52.9 |
| YOLOv8x | 97 MB | 479ms | 53.9 |

**Default**: YOLOv8n (fast, lightweight)

### Supported Classes

The YOLOv8 model detects 80 COCO dataset classes including:
- person, bicycle, car, motorbike, airplane, bus, train, truck
- boat, traffic light, fire hydrant, stop sign, parking meter
- dog, cat, bird, horse, and many more...

---

## 🎨 UI Features

### Design System

- **Color Scheme**:
  - Primary: Neon Blue (#00D9FF)
  - Secondary: Neon Purple (#BC00D9)
  - Background: Dark (#0a0e27)
  - Cards: Dark Card (#1a1f3a)

- **Effects**:
  - Glassmorphism cards
  - Neon glow effects
  - Smooth animations
  - Responsive design

### Components

1. **Navbar** - Navigation and branding
2. **Hero Section** - Welcome message
3. **Analytics Cards** - Real-time statistics
4. **Live Detection Panel** - Video feed and controls
5. **Tracking Table** - Object details
6. **Settings Panel** - Parameter adjustment
7. **Footer** - Links and information

---

## 📝 Code Examples

### Detect Objects in Python

```python
from detector import ObjectDetector

# Initialize detector
detector = ObjectDetector(model_name="yolov8n.pt", conf_threshold=0.5)

# Detect objects
import cv2
frame = cv2.imread("image.jpg")
detections = detector.detect(frame)

# Draw detections
frame = detector.draw_detections(frame, detections)
cv2.imshow("Detections", frame)
cv2.waitKey(0)
```

### Track Objects

```python
from tracker import ObjectTracker

# Initialize tracker
tracker = ObjectTracker()

# Update tracks
tracked_objects = tracker.update(detections, frame)

# Draw tracks
frame = tracker.draw_tracks(frame, tracked_objects)
```

### Use API from React

```javascript
import axios from 'axios'

// Start camera
const response = await axios.post('http://localhost:8000/start_camera')

// Get stats
const stats = await axios.get('http://localhost:8000/stats')
console.log(stats.data)

// Stop camera
await axios.post('http://localhost:8000/stop_camera')
```

---

## 🌐 Deployment

### Deploy Backend

**Using Docker:**
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]
```

### Deploy Frontend

**Build for production:**
```bash
npm run build
npm run preview
```

Deploy `dist/` folder to hosting service (Vercel, Netlify, etc.)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **Ultralytics** for YOLOv8
- **DeepSort** community
- **React** and **FastAPI** communities
- **OpenCV** contributors

---

## 📧 Support

For issues, questions, or suggestions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review API documentation
3. Check existing issues on GitHub
4. Create a new issue with detailed information

---

## 🚀 Future Enhancements

- [ ] GPU acceleration (CUDA)
- [ ] Multi-camera support
- [ ] Custom model training
- [ ] Database storage for tracking history
- [ ] Real-time alerting
- [ ] Video export functionality
- [ ] Advanced analytics dashboard
- [ ] Mobile app support
- [ ] Cloud deployment ready
- [ ] Performance optimization

---

**Made with ❤️ by CodeAlpha**

Last Updated: 2024
