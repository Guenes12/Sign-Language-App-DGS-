import pytest
from app.config import TARGET_FRAMES, FEATURES_PER_FRAME, HAND_FEATURE_DIMS
from app.domain.gesture import Gesture
from app.domain.prediction_result import PredictionResult
 
 
def test_config_dimensions_consistency():
    """Stellt sicher, dass die Feature-Dimensionen mathematisch aufgehen."""
    assert TARGET_FRAMES == 90
    assert FEATURES_PER_FRAME == 105
    assert HAND_FEATURE_DIMS == 63
 
 
def test_prediction_result_creation():
    """Testet die Instanziierung des Vorhersageergebnisses."""
    res = PredictionResult(
        label="ja",
        confidence=0.97,
    )
    assert res.label == "ja"
    assert res.confidence == 0.97
    assert res.to_dict() == {"label": "ja", "confidence": 0.97}