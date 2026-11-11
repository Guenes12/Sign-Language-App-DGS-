from pathlib import Path
from typing import List
import cv2
import numpy as np
 
 
class VideoLoader:
    """Lädt Videodateien einheitlich in eine Liste von BGR-Frames."""
 
    def load(self, video_path: str) -> List[np.ndarray]:
        path = Path(video_path)
        if not path.exists():
            raise FileNotFoundError(f"Videodatei existiert nicht: {video_path}")
 
        capture = cv2.VideoCapture(str(path))
        if not capture.isOpened():
            raise ValueError(f"Video konnte nicht geöffnet werden: {video_path}")
 
        frames: List[np.ndarray] = []
        try:
            while True:
                success, frame = capture.read()
                if not success or frame is None:
                    break
                frames.append(frame)
        finally:
            capture.release()
 
        if not frames:
            raise ValueError(f"Keine Frames aus {video_path} extrahiert.")
 
        return frames