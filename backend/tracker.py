"""DeepSORT Object Tracker"""
import cv2
from deep_sort_realtime.deepsort_tracker import DeepSort

class ObjectTracker:
    def __init__(self, max_age=30, n_init=1):
        self.tracker = DeepSort(max_age=max_age, n_init=n_init)
        
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
    
    def _get_color(self, tid):
        colors = [
            (255, 56, 56), (255, 157, 51), (255, 225, 51), (99, 226, 87),
            (45, 211, 153), (56, 185, 255), (69, 83, 255), (209, 34, 255),
            (255, 72, 186), (160, 237, 87), (71, 193, 193), (255, 142, 203)
        ]
        return colors[int(tid) % len(colors)]
    
    def _put_label(self, frame, text, x, y, color):
        try:
            (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            y0 = max(y, th + 10)
            cv2.rectangle(frame, (x, y0 - th - 6), (x + tw + 4, y0), color, -1)
            cv2.putText(frame, text, (x + 2, y0 - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        except Exception as e:
            print(f"[ERROR] _put_label failed: {e}")
