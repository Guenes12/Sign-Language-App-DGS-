import json
import zipfile
from pathlib import Path
import numpy as np
 
# Registriert den Custom-Layer bei Keras vor dem Laden
import training.model_builder 
from tensorflow.keras.models import load_model
from app.config import (

    MODEL_DIR,

    FEATURE_DIR,

    TEST_VIDEOS,

    TARGET_FRAMES,

    FEATURES_PER_FRAME,

)

from training.data_loader import DataLoader
from training.preprocessing.pipeline import PreprocessingPipeline
 
MODEL_PATH = Path(MODEL_DIR) / "gesture_model.keras"

VIDEO_EXTENSIONS = [".mp4", ".avi", ".mov", ".mkv", ".webm"]
 
 
def normalize_name(text: str) -> str:

    text = text.lower()

    return (

        text.replace("ä", "ae")

        .replace("ö", "oe")

        .replace("ü", "ue")

        .replace("ß", "ss")

    )
 
 
def load_model_classes(model_path: Path):

    try:

        with zipfile.ZipFile(model_path, "r") as z:

            if "classes.json" in z.namelist():

                return json.loads(z.read("classes.json").decode("utf-8"))

    except Exception:

        pass

    return DataLoader(FEATURE_DIR).get_class_names()
 
 
def expected_class_from_video(video_path: Path, classes):

    for parent in video_path.parents:

        p_name = normalize_name(parent.name)

        for cls in classes:

            if p_name == normalize_name(cls):

                return cls
 
    stem = normalize_name(video_path.stem)

    for cls in sorted(classes, key=lambda x: len(x), reverse=True):

        if normalize_name(cls) in stem:

            return cls

    return None
 
 
def extract_motion_diagnostics(sequence: np.ndarray):

    """

    Berechnet die physikalischen Bewegungsmerkmale aus der 90x105 Sequenz.

    """

    hand = sequence[:, :63]

    wrist_y = sequence[:, 1]

    nose_y = sequence[:, 64]

    # Handhöhe relativ zur Nase (Niedriger Wert = höher am Kopf)

    h2n_y = wrist_y - nose_y

    min_h2n_y = float(np.min(h2n_y))

    mean_h2n_y = float(np.mean(h2n_y))
 
    # Bewegung über die Zeit

    diff = np.diff(hand, axis=0)

    dx = float(np.sum(np.abs(diff[:, 0::3])))  # Horizontale Bewegung

    dy = float(np.sum(np.abs(diff[:, 1::3])))  # Vertikale Bewegung

    ratio_xy = dx / (dy + 1e-6)
 
    # Relative Position als Text

    if min_h2n_y < 0.20:

        position_desc = "Stirn / Schläfe (Kopfhöhe)"

    elif mean_h2n_y < 0.55:

        position_desc = "Mund / Kinnbereich"

    else:

        position_desc = "Brust / Bauchbereich"
 
    return {

        "min_h2n_y": min_h2n_y,

        "mean_h2n_y": mean_h2n_y,

        "position_desc": position_desc,

        "dx": dx,

        "dy": dy,

        "ratio_xy": ratio_xy,

    }
 
 
def main():

    print("\n" + "=" * 80)

    print("ERWEITERTE TESTVIDEO-DIAGNOSE (Clean Root-Cause Analysis)")

    print("=" * 80)
 
    if not MODEL_PATH.exists():

        raise FileNotFoundError(f"Modell nicht gefunden: {MODEL_PATH}")
 
    model = load_model(str(MODEL_PATH), safe_mode=False)

    classes = load_model_classes(MODEL_PATH)

    print(f"Modell geladen mit Klassen: {classes}")
 
    test_dir = Path(TEST_VIDEOS)

    video_files = sorted([p for p in test_dir.rglob("*") if p.is_file() and p.suffix.lower() in VIDEO_EXTENSIONS])

    print(f"Gefundene Testvideos: {len(video_files)}")
 
    pipeline = PreprocessingPipeline()

    total = 0

    correct = 0

    class_total = {cls: 0 for cls in classes}

    class_correct = {cls: 0 for cls in classes}
 
    try:

        for video_path in video_files:

            print("\n" + "-" * 80)

            print(f"VIDEO: {video_path.name}")

            print("-" * 80)
 
            expected_class = expected_class_from_video(video_path, classes)

            print(f"Erwartet:  {expected_class if expected_class else 'UNBEKANNT'}")
 
            try:

                feature_sequence = pipeline.process_video(str(video_path))
 
                # Vorhersage & Wahrscheinlichkeiten

                probabilities = model.predict(feature_sequence[np.newaxis, ...], verbose=0)[0]

                predicted_idx = int(np.argmax(probabilities))

                predicted_class = classes[predicted_idx]

                confidence = float(probabilities[predicted_idx])
 
                print(f"Erkannt:   {predicted_class} ({confidence:.2%})")
 
                # Ausgabe aller Klassen-Wahrscheinlichkeiten

                prob_str = " | ".join([f"{c}: {p*100:5.1f}%" for c, p in zip(classes, probabilities)])

                print(f"Scores:    [{prob_str}]")
 
                # Physikalische Bewegungsanalyse

                diag = extract_motion_diagnostics(feature_sequence)

                print(f"Position:  {diag['position_desc']} (Höhe Hand->Nase: {diag['mean_h2n_y']:.2f})")

                print(

                    f"Bewegung:  Horiz(dx)={diag['dx']:.1f} | Vert(dy)={diag['dy']:.1f} | "

                    f"X/Y-Ratio={diag['ratio_xy']:.2f} ({'Wedeln (X)' if diag['ratio_xy'] > 1.2 else 'Nicken (Y)'})"

                )
 
                if expected_class:

                    total += 1

                    class_total[expected_class] += 1

                    if predicted_class == expected_class:

                        correct += 1

                        class_correct[expected_class] += 1

                        print("Status:    ✅ RICHTIG")

                    else:

                        print(f"Status:    ❌ FALSCH (Erwartet: {expected_class} | Erkannt: {predicted_class})")

                        # Automatische Ursachenerklärung

                        if expected_class == "nein" and predicted_class == "ja":

                            print("💡 Ursache: Vertikale Bewegung war zu stark im Vergleich zum horizontalen Wedeln.")

                        elif expected_class == "nein" and predicted_class == "keineAhnung":

                            print("💡 Ursache: Hand war kurzzeitig zu hoch (an Stirnhöhe) orientiert.")

                        elif predicted_class == "essen":

                            print("💡 Ursache: Handform oder Höhe lag nahe am Mundbereich.")
 
            except Exception as e:

                print(f"[ERROR] {video_path.name}: {e}")
 
    finally:

        pipeline.close()
 
    print("\n" + "=" * 80)

    print("GESAMTERGEBNIS DER DIAGNOSE")

    print("=" * 80)

    if total > 0:

        print(f"Gesamtgenauigkeit: {correct}/{total} ({correct/total*100:.2f}%)")

        for cls in classes:

            t = class_total[cls]

            c = class_correct[cls]

            print(f"  {cls:15s}: {c:2d}/{t:2d} ({c/t*100 if t > 0 else 0:5.1f}%)")
 
 
if __name__ == "__main__":

    main()
 