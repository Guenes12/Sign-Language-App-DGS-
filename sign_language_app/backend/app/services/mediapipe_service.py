from training.preprocessing.pipeline import PreprocessingPipeline

class MediaPipeService:

    def __init__(self):

        self.pipeline = PreprocessingPipeline()

    def process_video(self, video_path):

        return self.pipeline.process_video(video_path)
 