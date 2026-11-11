from pathlib import Path
from typing import Tuple, List
import numpy as np
from app.config import FEATURE_DIR, TARGET_FRAMES, FEATURES_PER_FRAME
 
 
class DataLoader:
    """Lädt und validiert das Feature-Set dynamisch aus dem Dateisystem."""
 
    def __init__(self, feature_dir: Path = FEATURE_DIR):
        self.feature_dir = Path(feature_dir)
 
    def get_class_names(self) -> List[str]:
        """Gibt alle vorhandenen Klassenordner alphabetisch sortiert zurück."""
        if not self.feature_dir.exists():
            raise FileNotFoundError(f"Feature-Verzeichnis nicht gefunden: {self.feature_dir}")
 
        class_dirs = sorted([d.name for d in self.feature_dir.iterdir() if d.is_dir()])
        if not class_dirs:
            raise ValueError(f"Keine Klassenordner in {self.feature_dir} gefunden.")
        return class_dirs
 
    def load(self) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        class_names = self.get_class_names()
        X, y = [], []
 
        for class_idx, class_name in enumerate(class_names):
            class_dir = self.feature_dir / class_name
            files = sorted(class_dir.glob("*.npy"))
            for file in files:
                seq = np.load(file)
                if seq.shape != (TARGET_FRAMES, FEATURES_PER_FRAME):
                    continue
                if not np.isfinite(seq).all():
                    continue
                X.append(seq)
                y.append(class_idx)
 
        return np.asarray(X, dtype=np.float32), np.asarray(y, dtype=np.int32), class_names