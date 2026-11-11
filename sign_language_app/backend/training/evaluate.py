import json
from pathlib import Path
import zipfile
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import tensorflow as tf
from app.config import MODEL_DIR, TEST_SIZE
import training.model_builder  # noqa: F401 - registers InvariantFeatureLayer
from training.data_loader import DataLoader
 
MODEL_PATH = Path(MODEL_DIR) / "gesture_model.keras"
 
 
def load_classes_from_model(model_path: Path):
    with zipfile.ZipFile(model_path, "r") as z:
        if "classes.json" in z.namelist():
            return json.loads(z.read("classes.json").decode("utf-8"))
    raise ValueError("Keine 'classes.json' im Modell gefunden.")
 
 
def analyze_sample_biomechanics(x_sample: np.ndarray) -> dict:
    """Extrahiert Schlüsselmetriken für die Fehlerursachenanalyse."""
    # Landmarken: Hand Tip 8 (24:27), Nase (63:66), Mund (93:96)
    tip = x_sample[:, 24:27]
    nose = x_sample[:, 63:66]
    mouth = x_sample[:, 93:96]
 
    # Höhe: Fingerspitze Y minus Nase Y (negativ = über Nase/Stirn, positiv = unter Nase/Mund)
    rel_y = tip[:, 1] - nose[:, 1]
    min_rel_y = np.min(rel_y)  # Höchster Punkt der Hand relative zur Nase
 
    dist_mouth = np.linalg.norm(tip - mouth, axis=-1)
    min_dist_mouth = np.min(dist_mouth)
 
    dist_nose = np.linalg.norm(tip - nose, axis=-1)
    min_dist_nose = np.min(dist_nose)
 
    # Pinch (Daumen-Zeigefinger-Abstand): Daumen 4 (12:15), Zeige 8 (24:27)
    thumb = x_sample[:, 12:15]
    pinch = np.linalg.norm(tip - thumb, axis=-1)
    mean_pinch = np.mean(pinch)
 
    return {
        "min_rel_y": float(min_rel_y),
        "min_dist_mouth": float(min_dist_mouth),
        "min_dist_nose": float(min_dist_nose),
        "mean_pinch": float(mean_pinch),
    }
 
 
def main():
    print("\n" + "=" * 70)
    print("MODELL EVALUATION & FEHLER-DIAGNOSE")
    print("=" * 70)
 
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Modell nicht gefunden: {MODEL_PATH}")
 
    loader = DataLoader()
    X, y, class_names_dataset = loader.load()
    classes = load_classes_from_model(MODEL_PATH)
    model = tf.keras.models.load_model(str(MODEL_PATH), safe_mode=False)
 
    print(f"Modell geladen mit Klassen ({len(classes)}): {classes}")
 
    # Indizes mit-splitten, um Samples zuzuordnen
    indices = np.arange(len(X))
    _, X_test, _, y_test, _, idx_test = train_test_split(
        X,
        y,
        indices,
        test_size=TEST_SIZE,
        random_state=42,
        stratify=y,
    )
 
    print(f"Evaluiere auf {len(X_test)} Test-Sequenzen...")
 
    predictions = model.predict(X_test, verbose=0)
    y_pred = np.argmax(predictions, axis=1)
 
    # 1. Classification Report
    print("\n" + "-" * 70)
    print("CLASSIFICATION REPORT (Precision, Recall, F1-Score)")
    print("-" * 70)
    print(
        classification_report(y_test, y_pred, target_names=classes, digits=4)
    )
 
    # 2. Confusion Matrix
    print("-" * 70)
    print("CONFUSION MATRIX")
    print("-" * 70)
    cm = confusion_matrix(y_test, y_pred)
    header = f"{'Erwartet / Erkannt':<20}" + "".join(
        [f"{c:>12}" for c in classes]
    )
    print(header)
    print("-" * len(header))
    for idx, row in enumerate(cm):
        row_str = f"{classes[idx]:<20}" + "".join(
            [f"{val:>12d}" for val in row]
        )
        print(row_str)
    print("=" * 70)
 
    # 3. Detaillierte Fehleranalyse aller Fehlklassifikationen
    misclassified = np.where(y_test != y_pred)[0]
    print(
        f"\nGEFUNDENE FEHLKLASSIFIKATIONEN: {len(misclassified)} von {len(X_test)}"
    )
    print("=" * 70)
 
    for i, idx in enumerate(misclassified, 1):
        true_cls = classes[y_test[idx]]
        pred_cls = classes[y_pred[idx]]
        probs = predictions[idx]
        metrics = analyze_sample_biomechanics(X_test[idx])
 
        # Top 3 Vorhersagen
        top3_idx = np.argsort(probs)[::-1][:3]
        top3_str = ", ".join(
            [f"{classes[k]}: {probs[k]*100:.1f}%" for k in top3_idx]
        )
 
        print(f"[{i}] Test-Index: #{idx_test[idx]} | Erwartet: '{true_cls}' ➡️ Erkannt: '{pred_cls}'")
        print(f"    Wahrscheinlichkeiten: {top3_str}")
        print(
            f"    Biomechanik: Hand-Nase Y-Diff: {metrics['min_rel_y']:+.3f} "
            f"({'Über Nase/Stirn' if metrics['min_rel_y'] < 0 else 'Unter Nase/Mund'}), "
            f"Distanz Mund: {metrics['min_dist_mouth']:.3f}, "
            f"Distanz Nase: {metrics['min_dist_nose']:.3f}, "
            f"Pinch: {metrics['mean_pinch']:.3f}"
        )
        print("-" * 70)
 
 
if __name__ == "__main__":
    main()