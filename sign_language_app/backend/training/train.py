import json
import zipfile
from pathlib import Path
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from tensorflow.keras.models import load_model
 
from app.config import (
    MODEL_DIR,
    BATCH_SIZE,
    LEARNING_RATE,
    TEST_SIZE,
    VALIDATION_SPLIT,
    TARGET_FRAMES,
    FEATURES_PER_FRAME,
    MAX_EPOCHS,
    PATIENCE_EARLY_STOPPING,
    PATIENCE_REDUCE_LR
)
from training.data_loader import DataLoader
from training.model_builder import build_model
 
def main():
    model_dir = Path(MODEL_DIR)
    model_dir.mkdir(parents=True, exist_ok=True)
    model_path = model_dir / "gesture_model.keras"
 
    print("=" * 70)
    print("STARTE MODELL-TRAINING (7 Klassen mit Invarianten Gesten-Metriken)")
    print("=" * 70)
 
    # 1. Daten und Klassen laden
    loader = DataLoader()
    X, y, class_names = loader.load()
 
    print(f"Datensatz: {len(X)} Sequenzen geladen.")
    print(f"Klassen ({len(class_names)}): {class_names}")
 
    # 2. Stratified Train/Test Split (80% Train, 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=42,
        stratify=y,
    )
    print(f"Aufteilung: {len(X_train)} Training, {len(X_test)} Test")
 
    # 3. Modell bauen
    print("\nInitialisiere Modell mit invarianten Gestenmerkmalen...")
    model = build_model(
        input_shape=(TARGET_FRAMES, FEATURES_PER_FRAME),
        train_data=X_train,
        class_names=class_names,
    )
 
    model.compile(
        optimizer=Adam(learning_rate=LEARNING_RATE),
        loss=SparseCategoricalCrossentropy(),
        metrics=["accuracy"],
    )
 
    # 4. Callbacks: Early Stopping (15 Epochen) & dynamische Lernraten-Anpassung
    callbacks = [
        EarlyStopping(
            monitor="val_loss",
            patience=PATIENCE_EARLY_STOPPING,
            restore_best_weights=True,
            verbose=1,
        ),
        ModelCheckpoint(
            str(model_path),
            monitor="val_loss",
            save_best_only=True,
            verbose=1,
        ),
        ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=PATIENCE_REDUCE_LR,
            min_lr=1e-6,
            verbose=1,
        ),
    ]
 
    print(f"\nBeginne Training (Max: {MAX_EPOCHS} Epochen, Early-Stopping Geduld: {PATIENCE_EARLY_STOPPING})...")
    model.fit(
        X_train,
        y_train,
        validation_split=VALIDATION_SPLIT,
        epochs=MAX_EPOCHS,
        batch_size=BATCH_SIZE,
        shuffle=True,
        callbacks=callbacks,
    )
 
    # 5. Bestes Modell nachladen
    print("\nLade das beste Modell vom Checkpoint nach...")
    best_model = load_model(str(model_path), safe_mode=False)
 
    # 6. Klassenliste direkt in das .keras Zip-Paket schreiben
    with zipfile.ZipFile(str(model_path), mode="a") as z:
        z.writestr("classes.json", json.dumps(class_names, ensure_ascii=False, indent=2))
 
    # 7. Finale Evaluation mit ungesehenem Test-Split
    test_loss, test_accuracy = best_model.evaluate(X_test, y_test, verbose=0)
 
    print()
    print("=" * 70)
    print("TRAINING ERFOLGREICH BEENDET")
    print(f"Datei gesichert:     {model_path}")
    print(f"Klassen im Modell:   {class_names}")
    print(f"Final Test Loss:     {test_loss:.4f}")
    print(f"Final Test Accuracy: {test_accuracy * 100:.2f}%")
    print("=" * 70)
 
 
if __name__ == "__main__":
    main()