from pathlib import Path
import math
import cv2
import mediapipe as mp
import numpy as np
from training.preprocessing.video_loader import VideoLoader
from training.preprocessing.frame_sampler import FrameSampler
from training.preprocessing.mediapipe_extractor import MediaPipeExtractor
from training.preprocessing.landmark_normalizer import LandmarkNormalizer
from app.config import TEST_VIDEOS

VIDEO_FOLDER = TEST_VIDEOS

SUPPORTED_EXTENSIONS = {

    ".mp4",

    ".mov",

    ".avi",

    ".m4v",

}



def get_video_files():

    if not VIDEO_FOLDER.exists():

        raise FileNotFoundError(

            f"Videoordner nicht gefunden:\n"

            f"{VIDEO_FOLDER.resolve()}"

        )

    files = []

    for file in VIDEO_FOLDER.iterdir():

        if not file.is_file():

            continue

        if file.suffix.lower() in SUPPORTED_EXTENSIONS:

            files.append(file)

    return sorted(files)


def analyze_pose(

    frame,

    holistic

):

    """

    MediaPipe auf genau einem Frame ausführen

    und die Schulterausrichtung untersuchen.

    """

    rgb = cv2.cvtColor(

        frame,

        cv2.COLOR_BGR2RGB

    )

    result = holistic.process(rgb)

    if result.pose_landmarks is None:

        return {

            "success": False,

            "reason": "Keine Pose erkannt.",

        }

    landmarks = result.pose_landmarks.landmark

    nose = landmarks[

        mp.solutions.pose.PoseLandmark.NOSE.value

    ]

    left_shoulder = landmarks[

        mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value

    ]

    right_shoulder = landmarks[

        mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value

    ]

    # Schultervektor

    dx = (

        left_shoulder.x

        - right_shoulder.x

    )

    dy = (

        left_shoulder.y

        - right_shoulder.y

    )

    shoulder_distance = math.sqrt(

        dx * dx + dy * dy

    )

    # Winkel der Schulterlinie

    angle = math.degrees(

        math.atan2(dy, dx)

    )

    # Für die Diagnose:

    #

    # horizontal:

    # abs(dx) > abs(dy)

    #

    # vertikal:

    # abs(dy) > abs(dx)

    if abs(dx) > abs(dy):

        orientation = "HORIZONTAL"

    else:

        orientation = "VERTIKAL"

    return {

        "success": True,

        "nose_x": nose.x,

        "nose_y": nose.y,

        "left_shoulder_x": left_shoulder.x,

        "left_shoulder_y": left_shoulder.y,

        "right_shoulder_x": right_shoulder.x,

        "right_shoulder_y": right_shoulder.y,

        "dx": dx,

        "dy": dy,

        "distance": shoulder_distance,

        "angle": angle,

        "orientation": orientation,

    }


def print_pose_result(

    result

):

    if not result["success"]:

        print(

            "MediaPipe Pose: "

            f"{result['reason']}"

        )

        return

    print()

    print("MediaPipe Pose")

    print("------------------------------")

    print(

        "Nase: "

        f"x={result['nose_x']:.4f}, "

        f"y={result['nose_y']:.4f}"

    )

    print(

        "Linke Schulter: "

        f"x={result['left_shoulder_x']:.4f}, "

        f"y={result['left_shoulder_y']:.4f}"

    )

    print(

        "Rechte Schulter: "

        f"x={result['right_shoulder_x']:.4f}, "

        f"y={result['right_shoulder_y']:.4f}"

    )

    print(

        "Schulter dx: "

        f"{result['dx']:.4f}"

    )

    print(

        "Schulter dy: "

        f"{result['dy']:.4f}"

    )

    print(

        "Schulterwinkel: "

        f"{result['angle']:.2f}°"

    )

    print(

        "Schulterausrichtung: "

        f"{result['orientation']}"

    )


def analyze_video(

    video_path,

    video_loader,

    frame_sampler,

    holistic

):

    print()

    print()

    print("============================================================")

    print("VIDEO")

    print("============================================================")

    print(video_path.name)

    print(

        f"Pfad: {video_path.resolve()}"

    )

    # --------------------------------------------------------

    # Video laden

    # --------------------------------------------------------

    frames = video_loader.load(

        str(video_path)

    )

    if not frames:

        print(

            "FEHLER: Keine Frames geladen."

        )

        return None

    # --------------------------------------------------------

    # Frame-Größe

    # --------------------------------------------------------

    first_frame = frames[0]

    height = first_frame.shape[0]

    width = first_frame.shape[1]

    print()

    print("Frame-Informationen")

    print("------------------------------")

    print(

        f"Breite: {width}"

    )

    print(

        f"Höhe: {height}"

    )

    print(

        f"Shape: {first_frame.shape}"

    )

    if height > width:

        print(

            "Pixel-Orientierung: HOCHFORMAT"

        )

    elif width > height:

        print(

            "Pixel-Orientierung: QUERFORMAT"

        )

    else:

        print(

            "Pixel-Orientierung: QUADRAT"

        )

    # --------------------------------------------------------

    # MediaPipe auf ersten Frame

    # --------------------------------------------------------

    print()

    print(

        "MediaPipe Analyse "

        "(erster Frame)"

    )

    pose_result = analyze_pose(

        first_frame,

        holistic

    )

    print_pose_result(

        pose_result

    )

    # --------------------------------------------------------

    # Zusätzlich mittleren Frame untersuchen

    # --------------------------------------------------------

    middle_index = len(frames) // 2

    middle_frame = frames[

        middle_index

    ]

    print()

    print(

        "MediaPipe Analyse "

        f"(mittlerer Frame #{middle_index})"

    )

    middle_pose_result = analyze_pose(

        middle_frame,

        holistic

    )

    print_pose_result(

        middle_pose_result

    )

    # --------------------------------------------------------

    # 90-Frame-Sampling

    # --------------------------------------------------------

    sampled_frames = frame_sampler.sample(

        frames

    )

    print()

    print(

        f"Frames nach Sampling: "

        f"{len(sampled_frames)}"

    )

    return {

        "video": video_path.name,

        "width": width,

        "height": height,

        "frame_count": len(frames),

        "first_orientation": (

            pose_result.get("orientation")

            if pose_result["success"]

            else "NICHT ERKANNT"

        ),

        "middle_orientation": (

            middle_pose_result.get("orientation")

            if middle_pose_result["success"]

            else "NICHT ERKANNT"

        ),

        "first_angle": (

            pose_result.get("angle")

            if pose_result["success"]

            else None

        ),

        "middle_angle": (

            middle_pose_result.get("angle")

            if middle_pose_result["success"]

            else None

        ),

    }


# ============================================================

# HAUPTPROGRAMM

# ============================================================

def main():

    print()

    print("============================================================")

    print("VIDEO ORIENTATION TEST")

    print("============================================================")

    print(

        f"Videoordner: "

        f"{VIDEO_FOLDER.resolve()}"

    )

    video_files = get_video_files()

    if not video_files:

        print()

        print(

            "Keine Videos gefunden."

        )

        print()

        print(

            "Lege deine Videos hier hinein:"

        )

        print(

            VIDEO_FOLDER.resolve()

        )

        return

    print()

    print(

        f"{len(video_files)} Video(s) gefunden:"

    )

    for file in video_files:

        print(

            f"  - {file.name}"

        )

    # --------------------------------------------------------

    # MediaPipe

    # --------------------------------------------------------

    mp_holistic = mp.solutions.holistic

    holistic = mp_holistic.Holistic(

        static_image_mode=False,

        model_complexity=1,

        smooth_landmarks=True,

        refine_face_landmarks=True,

        min_detection_confidence=0.6,

        min_tracking_confidence=0.6,

    )

    video_loader = VideoLoader()

    frame_sampler = FrameSampler()

    results = []

    try:

        for video_path in video_files:

            try:

                result = analyze_video(

                    video_path,

                    video_loader,

                    frame_sampler,

                    holistic,

                )

                if result is not None:

                    results.append(result)

            except Exception as error:

                print()

                print(

                    "FEHLER bei "

                    f"{video_path.name}:"

                )

                print(

                    repr(error)

                )

    finally:

        holistic.close()

    # --------------------------------------------------------

    # Zusammenfassung

    # --------------------------------------------------------

    print()

    print()

    print("============================================================")

    print("ZUSAMMENFASSUNG")

    print("============================================================")

    if not results:

        print(

            "Keine erfolgreichen Analysen."

        )

        return

    print()

    for result in results:

        print(

            f"{result['video']}"

        )

        print(

            f"  Auflösung: "

            f"{result['width']} x "

            f"{result['height']}"

        )

        print(

            f"  Frames: "

            f"{result['frame_count']}"

        )

        print(

            f"  Erster Frame: "

            f"{result['first_orientation']}"

        )

        print(

            f"  Mittlerer Frame: "

            f"{result['middle_orientation']}"

        )

        if result["first_angle"] is not None:

            print(

                f"  Winkel erster Frame: "

                f"{result['first_angle']:.2f}°"

            )

        if result["middle_angle"] is not None:

            print(

                f"  Winkel mittlerer Frame: "

                f"{result['middle_angle']:.2f}°"

            )

        print()

    print("============================================================")

    print("ENDE")

    print("============================================================")


if __name__ == "__main__":

    main()
 