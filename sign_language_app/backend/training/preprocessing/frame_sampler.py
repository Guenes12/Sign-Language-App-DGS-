import numpy as np
from app.config import TARGET_FRAMES

class FrameSampler:
   def sample(self, frames: list) -> list:
       if len(frames) == 0:
           raise ValueError(
               "Video enthält keine Frames."
           )
       indices = np.linspace(
           0,
           len(frames) - 1,
           TARGET_FRAMES,
           dtype=int
       )
       sampled_frames = [
           frames[index]
           for index in indices
       ]
       return sampled_frames