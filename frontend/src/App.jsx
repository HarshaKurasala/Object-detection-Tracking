import { useState, useEffect } from 'react'
import axios from 'axios'
import { FaVideo, FaStop, FaUpload, FaImage, FaExpand, FaCompress, FaTrash, FaTimes } from 'react-icons/fa'
import './App.css'

const API_URL = 'http://localhost:8000'

// Internationalization (i18n) translations
const translations = {
  en: {
    // Tabs
    webcamDetection: 'Webcam Detection',
    imageDetection: 'Image Detection',
    videoTracking: 'Video Tracking',
    // Webcam
    liveFeed: 'Live Feed',
    startCamera: 'Start Camera',
    stopCamera: 'Stop Camera',
    liveStatistics: 'Live Statistics',
    fps: 'FPS',
    totalObjects: 'Total Objects',
    persons: 'Persons',
    vehicles: 'Vehicles',
    trackedObjects: 'Tracked Objects',
    noObjectsTracked: 'No objects tracked',
    // Image
    inputImage: 'Input image',
    detectionOutput: 'Detection output',
    runDetection: 'Run Detection',
    processing: 'Processing...',
    clickToUploadImage: 'Click to upload image',
    detectionResultWillAppearHere: 'Detection result will appear here',
    // Video
    inputVideo: 'Input video',
    trackedOutput: 'Tracked output',
    runTracking: 'Run Tracking',
    clickToUploadVideo: 'Click to upload video',
    trackingResultWillAppearHere: 'Tracking result will appear here',
    // Parameters
    detectionParameters: 'Detection parameters',
    confidenceThreshold: 'Confidence threshold',
    lowerDetectMore: 'Lower = detect more objects | higher = fewer false positives',
    showLabelsScores: 'Show labels & scores',
    // Footer
    detectableClasses: 'Detectable classes — 80 COCO categories',
    // Messages
    uploadImageAndClickRun: 'Upload an image and click Run detection to start.',
    imageLoaded: 'Image loaded. Click Run detection.',
    uploadVideoAndClickRun: 'Upload a video and click Run tracking to start.',
    videoLoaded: 'Video loaded. Click Run tracking.',
    processingVideo: 'Processing video... This may take a while.',
    detectionComplete: '✅ Detection complete!',
    videoTrackingComplete: '✅ Video tracking complete!',
    detectionFailed: '❌ Detection failed: ',
    videoProcessingFailed: '❌ Video processing failed: ',
    pleaseUploadImage: '⚠️ Please upload an image.',
    pleaseUploadVideo: '⚠️ Please upload a video.',
    cameraOffline: 'Camera Offline',
  }
}

const t = (key) => translations.en[key] || key

function App() {
  const [activeTab, setActiveTab] = useState('webcam')
  const [cameraActive, setCameraActive] = useState(false)
  const [stats, setStats] = useState({ fps: 0, total_objects: 0, object_counts: {}, tracked_objects: [] })
  const [confThreshold, setConfThreshold] = useState(0.5)
  const [showLabels, setShowLabels] = useState(true)
  const [imageFile, setImageFile] = useState(null)
  const [imagePreview, setImagePreview] = useState(null)
  const [imageResult, setImageResult] = useState(null)
  const [imageMessage, setImageMessage] = useState('Upload an image and click Run detection to start.')
  const [videoFile, setVideoFile] = useState(null)
  const [videoResult, setVideoResult] = useState(null)
  const [videoMessage, setVideoMessage] = useState('Upload a video and click Run tracking to start.')
  const [processing, setProcessing] = useState(false)
  const [fullscreenImage, setFullscreenImage] = useState(false)
  const [fullscreenVideo, setFullscreenVideo] = useState(false)
  const [fullscreenImageInput, setFullscreenImageInput] = useState(false)
  const [fullscreenVideoInput, setFullscreenVideoInput] = useState(false)

  // Effect hook to fetch and update live statistics when camera is active
  // Polls the stats endpoint every 500ms to get FPS, object counts, and tracked objects
  useEffect(() => {
    const interval = setInterval(async () => {
      if (cameraActive) {
        try {
          const res = await axios.get(`${API_URL}/stats`)
          setStats(res.data)
        } catch (err) {
          console.error('Stats fetch error:', err.message)
        }
      }
    }, 500)
    return () => clearInterval(interval)
  }, [cameraActive])

  const startCamera = async () => {
    try {
      console.log('Starting camera...')
      const res = await axios.post(`${API_URL}/start_camera`)
      console.log('Camera response:', res.data)
      if (res.data.status === 'error') {
        alert('Camera Error: ' + res.data.message)
        return
      }
      setCameraActive(true)
    } catch (err) {
      console.error('Start camera error:', err)
      alert('Failed to start camera: ' + err.message)
    }
  }

  const stopCamera = async () => {
    try {
      console.log('Stopping camera...')
      await axios.post(`${API_URL}/stop_camera`)
      setCameraActive(false)
    } catch (err) {
      console.error('Stop camera error:', err)
    }
  }

  // Event handler for image file upload
  // Stores the uploaded file and creates preview URL
  // Updates UI message to indicate image is ready for detection
  const handleImageUpload = (e) => {
    const file = e.target.files[0]
    if (file) {
      console.log('Image selected:', file.name, file.size)
      setImageFile(file)
      setImagePreview(URL.createObjectURL(file))
      setImageResult(null)
      setImageMessage('Image loaded. Click Run detection.')
    }
  }

  // Async function to run object detection on uploaded image
  // Sends image to backend /detect_image endpoint with confidence threshold
  // Displays detected objects annotated with bounding boxes and confidence scores
  // Handles errors and shows appropriate status messages
  const runImageDetection = async () => {
    if (!imageFile) {
      setImageMessage('⚠️ Please upload an image.')
      return
    }
    setProcessing(true)
    setImageMessage('Processing...')
    const formData = new FormData()
    formData.append('file', imageFile)
    formData.append('threshold', confThreshold)
    formData.append('show_labels', showLabels)
    
    try {
      console.log('Sending image detection request...')
      const res = await axios.post(`${API_URL}/detect_image`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        responseType: 'blob'
      })
      console.log('Response received:', res.status, res.data.type)
      
      if (res.data.type && res.data.type.includes('image')) {
        const imageUrl = URL.createObjectURL(res.data)
        setImageResult(imageUrl)
        setImageMessage('✅ Detection complete!')
      } else {
        const text = await res.data.text()
        console.error('Error response:', text)
        setImageMessage('❌ ' + text)
      }
    } catch (err) {
      console.error('Image detection error:', err)
      setImageMessage('❌ Detection failed: ' + err.message)
    }
    setProcessing(false)
  }

  // Event handler for video file upload
  // Stores the uploaded video file
  // Updates UI message to indicate video is ready for tracking
  const handleVideoUpload = (e) => {
    const file = e.target.files[0]
    if (file) {
      console.log('Video selected:', file.name, file.size)
      setVideoFile(file)
      setVideoResult(null)
      setVideoMessage('Video loaded. Click Run tracking.')
    }
  }

  // Async function to run object tracking on uploaded video
  // Sends video to backend /process_video endpoint for frame-by-frame tracking
  // Displays tracked video with persistent object IDs across frames
  // Shows processing status and handles long-running video processing with timeout
  const runVideoTracking = async () => {
    if (!videoFile) {
      setVideoMessage('⚠️ Please upload a video.')
      return
    }
    setProcessing(true)
    setVideoMessage('Processing video... This may take a while.')
    const formData = new FormData()
    formData.append('file', videoFile)
    formData.append('threshold', confThreshold)
    formData.append('show_labels', showLabels)
    
    try {
      console.log('Sending video processing request...')
      const res = await axios.post(`${API_URL}/process_video`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        responseType: 'blob',
        timeout: 300000
      })
      console.log('Response received:', res.status, res.data.type)
      
      if (res.data.type && res.data.type.includes('video')) {
        const videoUrl = URL.createObjectURL(res.data)
        setVideoResult(videoUrl)
        setVideoMessage('✅ Video tracking complete!')
      } else {
        const text = await res.data.text()
        console.error('Error response:', text)
        setVideoMessage('❌ ' + text)
      }
    } catch (err) {
      console.error('Video tracking error:', err)
      setVideoMessage('❌ Video processing failed: ' + err.message)
    }
    setProcessing(false)
  }

  // Clears uploaded image and resets image detection state
  // Removes preview, result, and resets status message
  const removeImage = () => {
    setImageFile(null)
    setImagePreview(null)
    setImageResult(null)
    setImageMessage('Upload an image and click Run detection to start.')
  }

  // Clears uploaded video and resets video tracking state
  // Removes video file and result, resets status message
  const removeVideo = () => {
    setVideoFile(null)
    setVideoResult(null)
    setVideoMessage('Upload a video and click Run tracking to start.')
  }

  // Calculate person count from object statistics
  const personCount = Object.entries(stats.object_counts).filter(([k]) => k === 'person').reduce((a, [, v]) => a + v, 0)
  
  // Calculate vehicle count from object statistics (cars, trucks, buses, motorcycles)
  const vehicleCount = Object.entries(stats.object_counts).filter(([k]) => ['car', 'truck', 'bus', 'motorcycle'].includes(k)).reduce((a, [, v]) => a + v, 0)

  // Main App component render
  // Displays tabbed interface for webcam detection, image detection, and video tracking
  // Includes parameter controls and real-time statistics display
  return (
    <div className="app">
      {/* Hero Section */}
      <div className="vs-hero">
        <div className="vs-hero-row">
          <div className="vs-icon">🎯</div>
          <div>
            <h1 className="vs-htitle">Vision<span className="hl">Scan</span></h1>
            <span className="vs-hsub">real-time object detection &amp; tracking — yolov8 + deepsort</span>
            <div className="vs-badges">
              <span className="vs-b on">YOLOv8n</span>
              <span className="vs-b on">DeepSORT tracker</span>
              <span className="vs-b">80 COCO classes</span>
              <span className="vs-b">FastAPI + React</span>
              <span className="vs-b">MIT License</span>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div className="vs-stats">
        <div className="vs-sc">
          <div className="vs-sc-num">80</div>
          <div className="vs-sc-lbl">Object classes</div>
        </div>
        <div className="vs-sc">
          <div className="vs-sc-num">6<sub> MB</sub></div>
          <div className="vs-sc-lbl">Model size</div>
        </div>
        <div className="vs-sc">
          <div className="vs-sc-num">COCO</div>
          <div className="vs-sc-lbl">Training data</div>
        </div>
        <div className="vs-sc">
          <div className="vs-sc-num">YOLOv8<sub>n</sub></div>
          <div className="vs-sc-lbl">Architecture</div>
        </div>
      </div>

      {/* Parameters Section */}
      <div className="vs-pw">
        <div className="vs-pb">
          <span className="vs-pb-label">Detection parameters</span>
          <div className="vs-params-row">
            <div className="vs-param">
              <label>Confidence threshold</label>
              <div className="vs-param-info">Lower = detect more objects | higher = fewer false positives</div>
              <input
                type="range"
                min="0.1"
                max="0.95"
                step="0.05"
                value={confThreshold}
                onChange={(e) => setConfThreshold(parseFloat(e.target.value))}
              />
              <div className="vs-param-value">{confThreshold.toFixed(2)}</div>
            </div>
            <div className="vs-param-check">
              <label>
                <input
                  type="checkbox"
                  checked={showLabels}
                  onChange={(e) => setShowLabels(e.target.checked)}
                />
                <span>Show labels &amp; scores</span>
              </label>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs Section */}
      <div className="vs-tabs-container">
        <div className="vs-tab-nav">
          <button
            className={activeTab === 'webcam' ? 'selected' : ''}
            onClick={() => setActiveTab('webcam')}
          >
            Webcam Detection
          </button>
          <button
            className={activeTab === 'image' ? 'selected' : ''}
            onClick={() => setActiveTab('image')}
          >
            Image Detection
          </button>
          <button
            className={activeTab === 'video' ? 'selected' : ''}
            onClick={() => setActiveTab('video')}
          >
            Video Tracking
          </button>
        </div>

        <div className="vs-tab-content">
          {/* Webcam Tab */}
          {activeTab === 'webcam' && (
            <div className="vs-tab-item">
              <div className="vs-row">
                <div className="vs-col">
                  <div className="vs-block-label">Live Feed</div>
                  <div className="vs-video-box">
                    {cameraActive ? (
                      <img 
                        src={`${API_URL}/video_feed?t=${Date.now()}`} 
                        alt="Video Feed" 
                        className="vs-video-feed"
                        onError={(e) => {
                          console.error('Video feed error')
                          setTimeout(() => {
                            e.target.src = `${API_URL}/video_feed?t=${Date.now()}`
                          }, 1000)
                        }}
                      />
                    ) : (
                      <div className="vs-video-placeholder">
                        <FaVideo size={64} />
                        <p>Camera Offline</p>
                      </div>
                    )}
                  </div>
                  {!cameraActive ? (
                    <button onClick={startCamera} className="vs-btn vs-btn-primary">
                      <FaVideo /> Start Camera
                    </button>
                  ) : (
                    <button onClick={stopCamera} className="vs-btn vs-btn-stop">
                      <FaStop /> Stop Camera
                    </button>
                  )}
                </div>
                <div className="vs-col">
                  <div className="vs-block-label">Live Statistics</div>
                  <div className="vs-stats-panel">
                    <div className="vs-stat-item">
                      <div className="vs-stat-num">{stats.fps}</div>
                      <div className="vs-stat-txt">FPS</div>
                    </div>
                    <div className="vs-stat-item">
                      <div className="vs-stat-num">{stats.total_objects}</div>
                      <div className="vs-stat-txt">Total Objects</div>
                    </div>
                    <div className="vs-stat-item">
                      <div className="vs-stat-num">{personCount}</div>
                      <div className="vs-stat-txt">Persons</div>
                    </div>
                    <div className="vs-stat-item">
                      <div className="vs-stat-num">{vehicleCount}</div>
                      <div className="vs-stat-txt">Vehicles</div>
                    </div>
                  </div>
                  <div className="vs-block-label" style={{marginTop: '20px'}}>Tracked Objects</div>
                  <div className="vs-tracking-list">
                    {stats.tracked_objects?.length > 0 ? (
                      stats.tracked_objects.map((obj) => (
                        <div key={obj.tid} className="vs-track-item">
                          <span className="vs-track-id">ID:{obj.tid}</span>
                          <span className="vs-track-label">{obj.label}</span>
                        </div>
                      ))
                    ) : (
                      <div className="vs-empty">No objects tracked</div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Image Tab */}
          {activeTab === 'image' && (
            <div className="vs-tab-item">
              <div className="vs-row">
                <div className="vs-col">
                  <div className="vs-block-label-with-btn">
                    <span>{t('inputImage')}</span>
                    {imagePreview && (
                      <div className="vs-btn-group">
                        <button
                          className="vs-fullscreen-btn"
                          onClick={() => setFullscreenImageInput(!fullscreenImageInput)}
                          title={fullscreenImageInput ? 'Exit fullscreen' : 'Fullscreen'}
                        >
                          {fullscreenImageInput ? <FaCompress /> : <FaExpand />}
                        </button>
                        <button
                          className="vs-remove-btn"
                          onClick={removeImage}
                          title="Remove image"
                        >
                          <FaTrash />
                        </button>
                      </div>
                    )}
                  </div>
                  <div className={fullscreenImageInput ? "vs-upload-box-fullscreen" : "vs-upload-box"}>
                    {fullscreenImageInput && (
                      <button
                        className="vs-fullscreen-exit-btn"
                        onClick={() => setFullscreenImageInput(false)}
                        title="Close fullscreen"
                      >
                        <FaTimes />
                      </button>
                    )}
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleImageUpload}
                      id="image-upload"
                      style={{display: 'none'}}
                    />
                    <label htmlFor="image-upload" className="vs-upload-label">
                      {imagePreview ? (
                        <img src={imagePreview} alt="Preview" className="vs-preview-img" />
                      ) : (
                        <div className="vs-upload-placeholder">
                          <FaUpload size={48} />
                          <p>Click to upload image</p>
                        </div>
                      )}
                    </label>
                  </div>
                  <button
                    onClick={runImageDetection}
                    className="vs-btn vs-btn-primary"
                    disabled={processing}
                  >
                    <FaImage /> {processing ? 'Processing...' : 'Run Detection'}
                  </button>
                </div>
                <div className="vs-col">
                  <div className="vs-block-label-with-btn">
                    <span>{t('detectionOutput')}</span>
                    {imageResult && (
                      <button
                        className="vs-fullscreen-btn"
                        onClick={() => setFullscreenImage(!fullscreenImage)}
                        title={fullscreenImage ? 'Exit fullscreen' : 'Fullscreen'}
                      >
                        {fullscreenImage ? <FaCompress /> : <FaExpand />}
                      </button>
                    )}
                  </div>
                  <div className={fullscreenImage ? "vs-output-box-fullscreen" : "vs-output-box"}>
                    {fullscreenImage && (
                      <button
                        className="vs-fullscreen-exit-btn"
                        onClick={() => setFullscreenImage(false)}
                        title="Close fullscreen"
                      >
                        <FaTimes />
                      </button>
                    )}
                    {imageResult ? (
                      <img src={imageResult} alt="Result" className="vs-result-img" />
                    ) : (
                      <div className="vs-output-placeholder">
                        <p>Detection result will appear here</p>
                      </div>
                    )}
                  </div>
                  <div className="vs-out">{imageMessage}</div>
                </div>
              </div>
            </div>
          )}

          {/* Video Tab */}
          {activeTab === 'video' && (
            <div className="vs-tab-item">
              <div className="vs-row">
                <div className="vs-col">
                  <div className="vs-block-label-with-btn">
                    <span>{t('inputVideo')}</span>
                    {videoFile && (
                      <div className="vs-btn-group">
                        <button
                          className="vs-fullscreen-btn"
                          onClick={() => setFullscreenVideoInput(!fullscreenVideoInput)}
                          title={fullscreenVideoInput ? 'Exit fullscreen' : 'Fullscreen'}
                        >
                          {fullscreenVideoInput ? <FaCompress /> : <FaExpand />}
                        </button>
                        <button
                          className="vs-remove-btn"
                          onClick={removeVideo}
                          title="Remove video"
                        >
                          <FaTrash />
                        </button>
                      </div>
                    )}
                  </div>
                  <div className={fullscreenVideoInput ? "vs-upload-box-fullscreen" : "vs-upload-box"}>
                    {fullscreenVideoInput && (
                      <button
                        className="vs-fullscreen-exit-btn"
                        onClick={() => setFullscreenVideoInput(false)}
                        title="Close fullscreen"
                      >
                        <FaTimes />
                      </button>
                    )}
                    <input
                      type="file"
                      accept="video/*"
                      onChange={handleVideoUpload}
                      id="video-upload"
                      style={{display: 'none'}}
                    />
                    <label htmlFor="video-upload" className="vs-upload-label">
                      <div className="vs-upload-placeholder">
                        <FaUpload size={48} />
                        <p>Click to upload video</p>
                        {videoFile && <span className="vs-file-name">{videoFile.name}</span>}
                      </div>
                    </label>
                  </div>
                  <button
                    onClick={runVideoTracking}
                    className="vs-btn vs-btn-primary"
                    disabled={processing}
                  >
                    <FaVideo /> {processing ? 'Processing...' : 'Run Tracking'}
                  </button>
                </div>
                <div className="vs-col">
                  <div className="vs-block-label-with-btn">
                    <span>{t('trackedOutput')}</span>
                    {videoResult && (
                      <button
                        className="vs-fullscreen-btn"
                        onClick={() => setFullscreenVideo(!fullscreenVideo)}
                        title={fullscreenVideo ? 'Exit fullscreen' : 'Fullscreen'}
                      >
                        {fullscreenVideo ? <FaCompress /> : <FaExpand />}
                      </button>
                    )}
                  </div>
                  <div className={fullscreenVideo ? "vs-output-box-fullscreen" : "vs-output-box"}>
                    {fullscreenVideo && (
                      <button
                        className="vs-fullscreen-exit-btn"
                        onClick={() => setFullscreenVideo(false)}
                        title="Close fullscreen"
                      >
                        <FaTimes />
                      </button>
                    )}
                    {videoResult ? (
                      <video src={videoResult} controls className="vs-result-video" />
                    ) : (
                      <div className="vs-output-placeholder">
                        <p>Tracking result will appear here</p>
                      </div>
                    )}
                  </div>
                  <div className="vs-out">{videoMessage}</div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <div className="vs-foot">
        <div className="vs-foot-ttl">Detectable classes — 80 COCO categories</div>
        <div className="vs-tags">
          <span className="vs-tag">person</span><span className="vs-tag">car</span>
          <span className="vs-tag">truck</span><span className="vs-tag">bus</span>
          <span className="vs-tag">bicycle</span><span className="vs-tag">motorcycle</span>
          <span className="vs-tag">cat</span><span className="vs-tag">dog</span>
          <span className="vs-tag">horse</span><span className="vs-tag">cow</span>
          <span className="vs-tag">bird</span><span className="vs-tag">sheep</span>
          <span className="vs-tag">elephant</span><span className="vs-tag">bear</span>
          <span className="vs-tag">bottle</span><span className="vs-tag">cup</span>
          <span className="vs-tag">wine glass</span><span className="vs-tag">fork</span>
          <span className="vs-tag">knife</span><span className="vs-tag">bowl</span>
          <span className="vs-tag">banana</span><span className="vs-tag">apple</span>
          <span className="vs-tag">pizza</span><span className="vs-tag">chair</span>
          <span className="vs-tag">sofa</span><span className="vs-tag">laptop</span>
          <span className="vs-tag">phone</span><span className="vs-tag">tv</span>
          <span className="vs-tag">keyboard</span><span className="vs-tag">mouse</span>
          <span className="vs-tag">book</span><span className="vs-tag">clock</span>
          <span className="vs-tag">+ 50 more</span>
        </div>
      </div>
    </div>
  )
}

export default App
