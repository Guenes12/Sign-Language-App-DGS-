import numpy as np
from pathlib import Path
from training.preprocessing.pipeline import (

    PreprocessingPipeline

)
from app.config import TARGET_FRAMES, FEATURES_PER_FRAME, DATASET_DIR, FEATURE_DIR
EXPECTED_SHAPE = (TARGET_FRAMES, FEATURES_PER_FRAME)
 
 
def generate_features(

    dataset_dir=DATASET_DIR,

    output_dir=FEATURE_DIR,

):
 
    dataset_dir = Path(

        dataset_dir

    )
 
    output_dir = Path(

        output_dir

    )
 
    if not dataset_dir.exists():

        raise ValueError(

            f"Dataset nicht gefunden: "

            f"{dataset_dir}"

        )
 
    pipeline = PreprocessingPipeline()
 
    try:
 
        class_dirs = sorted([

            path

            for path in dataset_dir.iterdir()

            if path.is_dir()

        ])
 
        if not class_dirs:

            raise ValueError(

                "Keine Klassen im Dataset gefunden."

            )
 
        for class_dir in class_dirs:
 
            class_name = class_dir.name
 
            videos = sorted([

                path

                for path in class_dir.iterdir()

                if path.is_file()

                and path.suffix.lower()

                in [".mp4", ".avi", ".mov", ".mkv"]

            ])
 
            if not videos:

                print(

                    f"Keine Videos in "

                    f"{class_name}"

                )

                continue
 
            class_output_dir = (

                output_dir / class_name

            )
 
            class_output_dir.mkdir(

                parents=True,

                exist_ok=True,

            )
 
            print()

            print(

                f"=== {class_name} ==="

            )
 
            for video_path in videos:
 
                output_path = (

                    class_output_dir

                    / f"{video_path.stem}.npy"

                )
 
                try:
 
                    print(

                        f"Verarbeite: "

                        f"{video_path.name}"

                    )
 
                    sequence = (

                        pipeline.process_video(

                            str(video_path)

                        )

                    )
 
                    if sequence.shape != EXPECTED_SHAPE:

                        raise ValueError(

                            f"Falsche Shape: "

                            f"{sequence.shape}"

                        )
 
                    if not np.isfinite(

                        sequence

                    ).all():

                        raise ValueError(

                            "Features enthalten "

                            "NaN oder Inf."

                        )
 
                    np.save(

                        output_path,

                        sequence,

                    )
 
                except Exception as error:
 
                    print(

                        f"❌ Fehler bei "

                        f"{video_path.name}: "

                        f"{error}"

                    )
 
    finally:
 
        pipeline.close()
 
 
if __name__ == "__main__":
 
    generate_features()
 