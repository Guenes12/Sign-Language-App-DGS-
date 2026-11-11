from typing import List, Optional
import cv2
import mediapipe as mp
import numpy as np
from app.config import FEATURES_PER_FRAME
 
 
class MediaPipeExtractor:
    """Extrahiert 63 Hand- + 21 Pose- + 21 Face-Features = 105 Dimensionen."""
 
    POSE_INDICES = [
        mp.solutions.pose.PoseLandmark.NOSE,
        mp.solutions.pose.PoseLandmark.LEFT_SHOULDER,
        mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER,
        mp.solutions.pose.PoseLandmark.LEFT_EAR,
        mp.solutions.pose.PoseLandmark.RIGHT_EAR,
        mp.solutions.pose.PoseLandmark.LEFT_HIP,
        mp.solutions.pose.PoseLandmark.RIGHT_HIP,
    ]
 
    FACE_INDICES = [1, 61, 291, 13, 14, 78, 308]
 
    def __init__(self, min_detection_confidence: float = 0.6, min_tracking_confidence: float = 0.6):
        self.mp_holistic = mp.solutions.holistic
        self.holistic = self.mp_holistic.Holistic(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            refine_face_landmarks=True,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )
 
    def _landmarks_to_array(self, landmarks) -> Optional[np.ndarray]:
        if landmarks is None:
            return None
        return np.array([[lm.x, lm.y, lm.z] for lm in landmarks.landmark], dtype=np.float32)
 
    def _extract_hand(self, result, hand_type: str) -> np.ndarray:
        lms = result.right_hand_landmarks if hand_type == "right" else result.left_hand_landmarks
        arr = self._landmarks_to_array(lms)
        return arr if arr is not None else np.full((21, 3), np.nan, dtype=np.float32)
 
    def _determine_dominant_hand(self, results) -> str:
        right_cnt = sum(1 for r in results if r.right_hand_landmarks is not None)
        left_cnt = sum(1 for r in results if r.left_hand_landmarks is not None)
        return "right" if right_cnt >= left_cnt else "left"
 
    def _extract_pose(self, result) -> np.ndarray:
        arr = self._landmarks_to_array(result.pose_landmarks)
        if arr is None:
            return np.full((7, 3), np.nan, dtype=np.float32)
        return arr[[idx.value for idx in self.POSE_INDICES]]
 
    def _extract_face(self, result) -> np.ndarray:
        arr = self._landmarks_to_array(result.face_landmarks)
        if arr is None:
            return np.full((7, 3), np.nan, dtype=np.float32)
        return arr[self.FACE_INDICES]
 
    def extract(self, frames: List[np.ndarray]) -> np.ndarray:
        if not frames:
            raise ValueError("Keine Frames zum Extrahieren vorhanden.")
 
        results = []
        for frame in frames:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb.flags.writeable = False
            results.append(self.holistic.process(rgb))
 
        dominant_hand = self._determine_dominant_hand(results)
        sequence = []
 
        for r in results:
            hand = self._extract_hand(r, dominant_hand)
            pose = self._extract_pose(r)
            face = self._extract_face(r)
 
            # Zusammenfügen: 63 + 21 + 21 = 105
            frame_vec = np.concatenate([
                hand.reshape(-1),
                pose.reshape(-1),
                face.reshape(-1),
            ])
            sequence.append(frame_vec)
 
        out = np.asarray(sequence, dtype=np.float32)
        if out.shape[1] != FEATURES_PER_FRAME:
            raise ValueError(f"Falsche Featurebreite: {out.shape[1]}, erwartet: {FEATURES_PER_FRAME}")
 
        return out
 
    def close(self):
        if self.holistic is not None:
            self.holistic.close()
            self.holistic = None