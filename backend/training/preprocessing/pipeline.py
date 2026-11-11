import numpy as np
from app.config import TARGET_FRAMES, FEATURES_PER_FRAME
from training.preprocessing.video_loader import VideoLoader
from training.preprocessing.video_orientation_corrector import VideoOrientationCorrector
from training.preprocessing.frame_sampler import FrameSampler
from training.preprocessing.mediapipe_extractor import MediaPipeExtractor
from training.preprocessing.landmark_normalizer import LandmarkNormalizer
 
 
class PreprocessingPipeline:

    """Verarbeitet rohe Videodateien zu normalisierten (90, 105) Sequenzen."""
 
    def __init__(self):

        self.video_loader = VideoLoader()

        self.orientation_corrector = VideoOrientationCorrector()

        self.frame_sampler = FrameSampler()

        self.extractor = MediaPipeExtractor()

        self.normalizer = LandmarkNormalizer()
 
    def process_video(self, video_path: str) -> np.ndarray:

        frames = self.video_loader.load(video_path)

        frames, rotation = self.orientation_corrector.correct(frames)

        frames = self.frame_sampler.sample(frames)

        raw_landmarks = self.extractor.extract(frames)

        sequence = self.normalizer.normalize(raw_landmarks)
 
        if sequence.shape != (TARGET_FRAMES, FEATURES_PER_FRAME):

            raise ValueError(

                f"Unerwartete Feature-Form {sequence.shape}, "

                f"erwartet: ({TARGET_FRAMES}, {FEATURES_PER_FRAME})"

            )

        return sequence
 
    def close(self):

        self.orientation_corrector.close()

        self.extractor.close()
 