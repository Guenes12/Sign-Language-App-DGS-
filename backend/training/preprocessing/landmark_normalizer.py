import numpy as np
from app.config import MIN_SHOULDER_WIDTH, MAX_ABS_FEATURE, FEATURES_PER_FRAME
 
 
class LandmarkNormalizer:
    """Zentriert auf den Körper und skaliert invariant gegenüber Kameraabstand."""
 
    def normalize(self, sequence: np.ndarray) -> np.ndarray:
        seq = np.asarray(sequence, dtype=np.float32)
        if seq.ndim != 2 or seq.shape[1] != FEATURES_PER_FRAME:
            raise ValueError(f"Erwarte Shape (T, {FEATURES_PER_FRAME}), erhalten: {seq.shape}")
 
        # Reshape: Hand (21,3), Pose (7,3), Face (7,3)
        hand = seq[:, 0:63].reshape(-1, 21, 3)
        pose = seq[:, 63:84].reshape(-1, 7, 3)
        face = seq[:, 84:105].reshape(-1, 7, 3)
 
        # Zeitliche Interpolation von Ausfällen
        hand = self._interpolate_landmarks(hand)
        pose = self._interpolate_landmarks(pose)
        face = self._interpolate_landmarks(face)
 
        # Schultern aus Pose (Index 1 = Left, Index 2 = Right)
        left_shoulder = pose[:, 1]
        right_shoulder = pose[:, 2]
 
        shoulder_center = (left_shoulder + right_shoulder) / 2.0
        shoulder_widths = np.linalg.norm(left_shoulder - right_shoulder, axis=1)
 
        valid_widths = shoulder_widths[np.isfinite(shoulder_widths) & (shoulder_widths > 0)]
        shoulder_width = float(np.median(valid_widths)) if len(valid_widths) > 0 else 0.2
        shoulder_width = max(shoulder_width, MIN_SHOULDER_WIDTH)
 
        # Zentrierung und Skalierung
        hand_norm = (hand - shoulder_center[:, None, :]) / shoulder_width
        pose_norm = (pose - shoulder_center[:, None, :]) / shoulder_width
        face_norm = (face - shoulder_center[:, None, :]) / shoulder_width
 
        normalized = np.concatenate([
            hand_norm.reshape(-1, 63),
            pose_norm.reshape(-1, 21),
            face_norm.reshape(-1, 21),
        ], axis=1)
 
        # Extremwert-Schutz
        normalized = np.nan_to_num(normalized, nan=0.0, posinf=MAX_ABS_FEATURE, neginf=-MAX_ABS_FEATURE)
        return np.clip(normalized, -MAX_ABS_FEATURE, MAX_ABS_FEATURE).astype(np.float32)
 
    @staticmethod
    def _interpolate_landmarks(data: np.ndarray) -> np.ndarray:
        res = data.copy()
        t_indices = np.arange(data.shape[0])
 
        for lm in range(data.shape[1]):
            for coord in range(3):
                v = data[:, lm, coord]
                valid = np.isfinite(v)
                cnt = np.sum(valid)
                if cnt == 0:
                    res[:, lm, coord] = 0.0
                elif cnt == 1:
                    res[:, lm, coord] = v[valid][0]
                else:
                    res[:, lm, coord] = np.interp(t_indices, t_indices[valid], v[valid])
        return res