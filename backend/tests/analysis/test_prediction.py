from pathlib import Path
from app.config import TEST_VIDEOS
from app.services.prediction_service import PredictionService
from training.preprocessing.pipeline import PreprocessingPipeline
 
# Konfiguration des zu testenden Videos
# Falls keine Unterordner genutzt werden, einfach Dateiname anpassen:
VIDEO_PATH = TEST_VIDEOS / "nein" / "front (1).mp4"
# Fallback, falls Datei direkt in testvideos/ liegt:
if not VIDEO_PATH.exists():
    VIDEO_PATH = TEST_VIDEOS / "front (1).mp4"
 
 
def main():
    if not VIDEO_PATH.exists():
        print(f"❌ Testvideo nicht gefunden: {VIDEO_PATH}")
        print(f"Bitte lege ein Video unter {TEST_VIDEOS} ab.")
        return
 
    print("=" * 60)
    print(f"TESTE EINZELNES VIDEO: {VIDEO_PATH.name}")
    print("=" * 60)
 
    # 1. Vorverarbeitung (Orientierung, Frame-Sampling, MediaPipe)
    pipeline = PreprocessingPipeline()
    try:
        print("1. Extrahiere Features aus Video...")
        sequence = pipeline.process_video(str(VIDEO_PATH))
        print(f"   -> Feature-Shape erfolgreich: {sequence.shape}")
 
        # 2. Inferenz über PredictionService
        print("2. Führe Modell-Klassifikation durch...")
        service = PredictionService()
        result = service.predict(sequence)
 
        # 3. Ausgabe
        print("\nERGEBNIS:")
        print(f"Vorhergesagte Gebärde: {result['label']}")
        print(f"Konfidenz:             {result['confidence']:.2%}")
        print("\nWahrscheinlichkeitsverteilung aller Klassen:")
        for label, prob in result["probabilities"].items():
            bar = "█" * int(prob * 30)
            print(f"  {label:15s}: {prob*100:5.2f}% {bar}")
 
    finally:
        pipeline.close()
 
 
if __name__ == "__main__":
    main()