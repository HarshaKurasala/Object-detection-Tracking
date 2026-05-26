"""DeepSORT Object Tracker"""
import cv2
from deep_sort_realtime.deepsort_tracker import DeepSort

class ObjectTracker:
    # Constructor to initialize DeepSORT multi-object tracker
    # Parameters: max_age - maximum frames to keep track before removal (default 30)
    #            n_init - number of detections needed to confirm track (default 1)
    def __init__(self, max_age=30, n_init=1):
        self.tracker = DeepSort(max_age=max_age, n_init=n_init)
        
    # Updates tracker with new detections from current frame
    # Performs data association and generates persistent track IDs across frames
    # Parameters: detections - list of detection dictionaries from detector
    #            frame - current video frame for deep feature extraction
    # Returns: list of confirmed track dictionaries with IDs and trajectories
    def update(self, detections, frame):
        try:
            if not detections:
                return []
            
            ds_detections = []
            for d in detections:
                try:
                    x1, y1, x2, y2 = d["x1"], d["y1"], d["x2"], d["y2"]
                    w = x2 - x1
                    h = y2 - y1
                    conf = d["conf"]
                    label = d.get("label", "unknown")
                    
                    ds_detections.append(([x1, y1, w, h], conf, label))
                except Exception as e:
                    print(f"[ERROR] Processing detection: {e}")
                    continue
            
            if not ds_detections:
                return []
            
            raw_tracks = self.tracker.update_tracks(ds_detections, frame=frame)
            tracks = []
            
            for track in raw_tracks:
                try:
                    if not track.is_confirmed():
                        continue
                    
                    tid = int(track.track_id)
                    ltrb = list(map(int, track.to_ltrb()))
                    label = track.det_class if hasattr(track, "det_class") and track.det_class else "unknown"
                    conf = track.det_conf if hasattr(track, "det_conf") else 0.0
                    
                    tracks.append({
                        "tid": tid,
                        "box": ltrb,
                        "label": label,
                        "conf": conf
                    })
                except Exception as e:
                    print(f"[ERROR] Processing track: {e}")
                    continue
            
            return tracks
        except Exception as e:
            print(f"[ERROR] Tracker update failed: {e}")
            return []
    
    # Draws tracked object bounding boxes with persistent track IDs on frame
    # Parameters: frame - input image to draw on
    #            tracks - list of track dictionaries from update() method
    # Returns: annotated frame with tracked boxes labeled with IDs
    def draw_tracks(self, frame, tracks):
        try:
            if not tracks:
                return frame
            
            for track in tracks:
                try:
                    x1, y1, x2, y2 = track["box"]
                    color = self._get_color(track["tid"])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    
                    label = f"ID:{track['tid']} {track['label']}"
                    self._put_label(frame, label, x1, y1, color)
                except Exception as e:
                    print(f"[ERROR] Drawing track: {e}")
                    continue
            
            return frame
        except Exception as e:
            print(f"[ERROR] draw_tracks failed: {e}")
            return frame
    
    # Helper method to assign consistent colors to different track IDs
    # Parameter: tid - track identifier
    # Returns: BGR color tuple (B, G, R) for consistent visualization across frames
    def _get_color(self, tid):
        colors = [
            (255, 56, 56), (255, 157, 51), (255, 225, 51), (99, 226, 87),
            (45, 211, 153), (56, 185, 255), (69, 83, 255), (209, 34, 255),
            (255, 72, 186), (160, 237, 87), (71, 193, 193), (255, 142, 203)
        ]
        return colors[int(tid) % len(colors)]
    
    # Helper method to draw text labels on frames with background rectangle
    # Parameters: frame - image to draw on
    #            text - label text to display (track ID and class name)
    #            x, y - position for label placement
    #            color - BGR color tuple for the rectangle background
    def _put_label(self, frame, text, x, y, color):
        try:
            (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            y0 = max(y, th + 10)
            cv2.rectangle(frame, (x, y0 - th - 6), (x + tw + 4, y0), color, -1)
            cv2.putText(frame, text, (x + 2, y0 - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        except Exception as e:
            print(f"[ERROR] _put_label failed: {e}")
