from typing import List, Tuple
import cv2
import mediapipe as mp
import numpy as np
 
 
class VideoOrientationCorrector:
    """Korrigiert Videodrehungen (0°, 90°, 180°, 270°)."""
 
    ROTATION_MAP = {
        0: None,
        90: cv2.ROTATE_90_CLOCKWISE,
        180: cv2.ROTATE_180,
        270: cv2.ROTATE_90_COUNTERCLOCKWISE,
        -90: cv2.ROTATE_90_COUNTERCLOCKWISE,
    }
 
    def __init__(self, sample_count: int = 5):
        self.sample_count = sample_count
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=True,
            model_complexity=1,
            smooth_landmarks=False,
            min_detection_confidence=0.4,
        )
 
    def _rotate_frame(self, frame: np.ndarray, angle: int) -> np.ndarray:
        flag = self.ROTATION_MAP.get(angle)
        return cv2.rotate(frame, flag) if flag is not None else frame
 
    def _evaluate_posture(self, frame: np.ndarray) -> float:
        """
        Gibt einen Gültigkeits-Score für eine Orientierung zurück.
        Niedrigerer Score = besser aufrecht.
        """
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.pose.process(rgb)
        if not result.pose_landmarks:
            return 999.0
 
        lm = result.pose_landmarks.landmark
        nose = lm[self.mp_pose.PoseLandmark.NOSE]
        left_sh = lm[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_sh = lm[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
 
        # Wenn Schultern oder Kopf unsichtbar sind
        if min(nose.visibility, left_sh.visibility, right_sh.visibility) < 0.4:
            return 999.0
 
        # Kriterium 1: Schulterlinie muss horizontal sein (dy -> 0)
        dx = abs(right_sh.x - left_sh.x)
        dy = abs(right_sh.y - left_sh.y)
        shoulder_angle = np.degrees(np.arctan2(dy, dx + 1e-6))
 
        # Kriterium 2: Nase muss OBERHALB des Schulterzentrums sein (y_nose < y_shoulder)
        shoulder_mid_y = (left_sh.y + right_sh.y) / 2.0
        head_penalty = 50.0 if nose.y > shoulder_mid_y else 0.0
 
        return float(shoulder_angle + head_penalty)
 
    def determine_rotation(self, frames: List[np.ndarray]) -> int:
        if not frames:
            return 0
 
        indices = np.linspace(0, len(frames) - 1, min(self.sample_count, len(frames)), dtype=int)
        candidates = [0, 90, 180, 270]
        candidate_scores = {deg: 0.0 for deg in candidates}
 
        for deg in candidates:
            frame_scores = []
            for idx in indices:
                rot_frame = self._rotate_frame(frames[idx], deg)
                frame_scores.append(self._evaluate_posture(rot_frame))
            candidate_scores[deg] = float(np.median(frame_scores))
 
        best_rotation = min(candidate_scores, key=candidate_scores.get)
        # Wenn gar keine Landmarks erkannt wurden, bleibe bei 0
        if candidate_scores[best_rotation] >= 900.0:
            return 0
 
        return best_rotation
 
    def correct(self, frames: List[np.ndarray]) -> Tuple[List[np.ndarray], int]:
        rotation = self.determine_rotation(frames)
        if rotation == 0:
            return frames, 0
 
        corrected = [self._rotate_frame(f, rotation) for f in frames]
        return corrected, rotation
 
    def close(self):
        if self.pose is not None:
            self.pose.close()
            self.pose = None