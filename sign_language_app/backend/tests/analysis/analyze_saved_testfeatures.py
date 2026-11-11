import json
import zipfile
from pathlib import Path
import numpy as np
 
# Registriert den Custom-Layer vor dem Laden bei Keras
import training.model_builder  # noqa: F401
from tensorflow.keras.models import load_model
 
from app.config import (
    MODEL_DIR,
    FEATURE_DIR,
    TARGET_FRAMES,
    FEATURES_PER_FRAME,
)
from training.data_loader import DataLoader
 
MODEL_PATH = Path(MODEL_DIR) / "gesture_model.keras"
 
# Ordner der gespeicherten Testfeatures (Fallback-Suche falls abweichend benannt)
POSSIBLE_TEST_DIRS = [
    Path("testvideos_features"),
    Path("testvideos_features 4"),
    Path("test_features"),
]
 
 
def find_test_feature_dir() -> Path:
    for d in POSSIBLE_TEST_DIRS:
        if d.exists() and any(d.glob("**/*.npy")):
            return d
    return POSSIBLE_TEST_DIRS[0]
 
 
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
 
 
def expected_class_from_path(file_path: Path, classes):
    """
    Ermittelt die Zielklasse anhand des Ordnernamens oder Dateinamens.
    """
    for parent in file_path.parents:
        p_name = normalize_name(parent.name)
        for cls in classes:
            if p_name == normalize_name(cls):
                return cls
 
    stem = normalize_name(file_path.stem)
    for cls in sorted(classes, key=lambda x: len(x), reverse=True):
        if normalize_name(cls) in stem:
            return cls
    return None
 
 
def extract_motion_diagnostics(sequence: np.ndarray):
    """
    Physikalische Kennzahlen: Handhöhe, Bewegungsdynamik (X vs Y).
    """
    hand = sequence[:, :63]
    wrist_y = sequence[:, 1]
    nose_y = sequence[:, 64]
 
    h2n_y = wrist_y - nose_y
    min_h2n_y = float(np.min(h2n_y))
    mean_h2n_y = float(np.mean(h2n_y))
 
    diff = np.diff(hand, axis=0)
    dx = float(np.sum(np.abs(diff[:, 0::3])))
    dy = float(np.sum(np.abs(diff[:, 1::3])))
    ratio_xy = dx / (dy + 1e-6)
 
    # Fingerspitzen Pinch (Landmark 4 Daumen zu Landmark 8 Zeigefinger)
    thumb = hand[:, 12:15]
    index = hand[:, 24:27]
    pinch_dist = float(np.mean(np.linalg.norm(thumb - index, axis=-1)))
 
    if min_h2n_y < 0.20:
        position_desc = "Stirn / Schläfe (Kopfhöhe)"
    elif mean_h2n_y < 0.55:
        position_desc = "Mund / Kinnbereich"
    else:
        position_desc = "Brust / Bauchbereich"
 
    return {
        "mean_h2n_y": mean_h2n_y,
        "position_desc": position_desc,
        "dx": dx,
        "dy": dy,
        "ratio_xy": ratio_xy,
        "pinch_dist": pinch_dist,
    }
 
 
def main():
    print("\n" + "=" * 80)
    print("DIAGNOSE GESPEICHERTER TESTFEATURES (.npy)")
    print("=" * 80)
 
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Modell nicht gefunden: {MODEL_PATH}")
 
    model = load_model(str(MODEL_PATH), safe_mode=False)
    classes = load_model_classes(MODEL_PATH)
    print(f"Modell geladen mit Klassen ({len(classes)}): {classes}")
 
    feature_dir = find_test_feature_dir()
    print(f"Lese Testfeatures aus Verzeichnis: {feature_dir.resolve()}")
 
    npy_files = sorted(list(feature_dir.rglob("*.npy")))
    if not npy_files:
        print(f"❌ Keine .npy Dateien in {feature_dir} gefunden!")
        return
 
    print(f"Gefundene Feature-Dateien: {len(npy_files)}")
 
    total = 0
    correct = 0
    class_total = {cls: 0 for cls in classes}
    class_correct = {cls: 0 for cls in classes}
 
    for file_path in npy_files:
        expected_class = expected_class_from_path(file_path, classes)
 
        try:
            feature_sequence = np.load(file_path)
 
            if feature_sequence.shape != (TARGET_FRAMES, FEATURES_PER_FRAME):
                print(f"[WARN] Überspringe {file_path.name}: Shape {feature_sequence.shape} != (90, 105)")
                continue
 
            # Modell-Vorhersage
            probabilities = model.predict(feature_sequence[np.newaxis, ...], verbose=0)[0]
            predicted_idx = int(np.argmax(probabilities))
            predicted_class = classes[predicted_idx]
            confidence = float(probabilities[predicted_idx])
 
            print("\n" + "-" * 80)
            print(f"DATEI:     {file_path.name}")
            print(f"Erwartet:  {expected_class if expected_class else 'UNBEKANNT'}")
            print(f"Erkannt:   {predicted_class} ({confidence:.2%})")
 
            # Wahrscheinlichkeiten aller Klassen anzeigen
            prob_str = " | ".join([f"{c}: {p*100:5.1f}%" for c, p in zip(classes, probabilities)])
            print(f"Scores:    [{prob_str}]")
 
            # Diagnostik
            diag = extract_motion_diagnostics(feature_sequence)
            print(f"Position:  {diag['position_desc']} (Höhe Hand->Nase: {diag['mean_h2n_y']:.2f})")
            print(
                f"Bewegung:  Horiz(dx)={diag['dx']:.1f} | Vert(dy)={diag['dy']:.1f} | "
                f"X/Y-Ratio={diag['ratio_xy']:.2f} | Pinch={diag['pinch_dist']:.3f}"
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
                    # Ursachen-Erklärung
                    if expected_class == "essen" and predicted_class == "danke":
                        print("💡 Ursache: Handform war zu flach/offen anstelle geschlossener Knospen-Fingerspitzen.")
                    elif expected_class == "nein" and predicted_class == "ja":
                        print("💡 Ursache: Vertikales Nicken überwog gegenüber horizontalem Wedeln.")
                    elif expected_class == "nein" and predicted_class == "keineAhnung":
                        print("💡 Ursache: Hand wurde kurzzeitig zu hoch (an Stirnhöhe) geführt.")
 
        except Exception as e:
            print(f"[ERROR] {file_path.name}: {e}")
 
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