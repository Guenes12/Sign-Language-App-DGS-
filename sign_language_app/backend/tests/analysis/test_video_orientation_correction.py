import os
import cv2
from training.preprocessing.video_loader import VideoLoader
from training.preprocessing.video_orientation_corrector import (

    VideoOrientationCorrector,

)
from app.config import TEST_VIDEOS
 
VIDEO_FOLDER = TEST_VIDEOS


def main():

    loader = VideoLoader()

    corrector = VideoOrientationCorrector()

    video_files = sorted(

        file_name

        for file_name in os.listdir(VIDEO_FOLDER)

        if file_name.lower().endswith(

            (".mp4", ".mov", ".avi", ".mkv")

        )

    )

    if not video_files:

        print(

            "Keine Videos gefunden."

        )

        return

    try:

        for file_name in video_files:

            video_path = os.path.join(

                VIDEO_FOLDER,

                file_name,

            )

            print()

            print("=" * 70)

            print(file_name)

            print("=" * 70)

            frames = loader.load(

                video_path

            )

            if not frames:

                print(

                    "Keine Frames geladen."

                )

                continue

            height, width = frames[0].shape[:2]

            print(

                f"Originalgröße: "

                f"{width} x {height}"

            )

            corrected_frames, rotation = (

                corrector.correct(frames)

            )

            corrected_height, corrected_width = (

                corrected_frames[0].shape[:2]

            )

            print(

                f"Korrigierte Größe: "

                f"{corrected_width} x "

                f"{corrected_height}"

            )

            print(

                f"Rotation: {rotation}°"

            )

            # Einige zusätzliche Informationen

            # über die korrigierten Frames.

            print(

                f"Frames: "

                f"{len(corrected_frames)}"

            )

            print(

                "Ergebnis: "

                "OK"

            )

    finally:

        corrector.close()


if __name__ == "__main__":

    main()
 