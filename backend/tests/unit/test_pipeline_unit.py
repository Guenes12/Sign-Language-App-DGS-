import numpy as np
import pytest
from app.config import TARGET_FRAMES
from training.preprocessing.frame_sampler import FrameSampler
from training.preprocessing.landmark_normalizer import LandmarkNormalizer
 
 
def test_frame_sampler_sampling_length():
    """Prüft, ob der FrameSampler jede Videolänge auf exakt TARGET_FRAMES skaliert."""
    sampler = FrameSampler()
    # Simuliere ein kurzes Video mit 30 Frames und ein langes mit 150 Frames
    short_video = [np.zeros((10, 10, 3)) for _ in range(30)]
    long_video = [np.zeros((10, 10, 3)) for _ in range(150)]
 
    assert len(sampler.sample(short_video)) == TARGET_FRAMES
    assert len(sampler.sample(long_video)) == TARGET_FRAMES
 
 
def test_landmark_normalizer_shape_validation():
    """Prüft, ob der Normalizer ungültige Tensoren sauber abweist."""
    normalizer = LandmarkNormalizer()
    invalid_tensor = np.zeros((TARGET_FRAMES, 50))  # 50 != 105
 
    with pytest.raises(ValueError):
        normalizer.normalize(invalid_tensor)