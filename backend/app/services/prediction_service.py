import zipfile
import json
from pathlib import Path
from typing import Dict, Any, List
import numpy as np
import tensorflow as tf
from app.config import MODEL_DIR, TARGET_FRAMES, FEATURES_PER_FRAME
import training.model_builder
 
 
class PredictionService:
 
    def __init__(self):
        model_path = Path(MODEL_DIR) / "gesture_model.keras"
        if not model_path.exists():
            raise FileNotFoundError(f"Modell nicht gefunden: {model_path}")
 
        # Modell laden
        self.model = tf.keras.models.load_model(str(model_path))
 
        # Klassen direkt aus der .keras-Datei extrahieren
        with zipfile.ZipFile(model_path, "r") as z:
            if "classes.json" in z.namelist():
                self.labels: List[str] = json.loads(z.read("classes.json").decode("utf-8"))
            else:
                raise ValueError("Keine Klassen-Metadaten im Modell gefunden.")
 
    def predict(self, sequence: np.ndarray) -> Dict[str, Any]:
        seq = np.asarray(sequence, dtype=np.float32)
 
        if seq.shape != (TARGET_FRAMES, FEATURES_PER_FRAME):
            raise ValueError(
                f"Falsche Feature-Shape: {seq.shape}. "
                f"Erwartet: ({TARGET_FRAMES}, {FEATURES_PER_FRAME})"
            )
 
        # Die Normalisierung ist als Layer direkt im Modell hinterlegt
        input_data = np.expand_dims(seq, axis=0)
        probabilities = self.model.predict(input_data, verbose=0)[0]
        predicted_idx = int(np.argmax(probabilities))
 
        return {
            "label": self.labels[predicted_idx],
            "confidence": float(probabilities[predicted_idx]),
            "probabilities": {
                label: float(probabilities[idx])
                for idx, label in enumerate(self.labels)
            },
        }