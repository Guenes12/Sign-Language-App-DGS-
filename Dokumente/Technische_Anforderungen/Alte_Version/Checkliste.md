# Checkliste: Gebärdensprachen-Erkennung (MVP mit 2 Wörtern)

#### 

#### Phase 0: Projektinitialisierung \& Datensammlung

* Zwei spezifische Startwörter ausgewählt ("Ja" und "Nein").
* Mindestens 5-10 Videos pro Startwort aufgenommen (gute Qualität, verschiedene
* Blickwinkel/Variationen).
* Videos systematisch benannt und organisiert.
* Entscheidung für Pose Estimation Framework (MediaPipe Pose).
* Entscheidung für ML-Framework (TensorFlow/Keras).
* Entscheidung für Mobile Framework (Flutter).

#### 

#### Phase 1: Datenextraktion \& Vorverarbeitung (Python)

* Python-Umgebung eingerichtet (Python, mediapipe, opencv python, numpy, tensorflow, scikit-learn).
* Python-Skript zum Laden von Videos erstellt.
* Python-Skript zur Frame-Extraktion implementiert.
* Python-Skript zur Pose Estimation mit MediaPipe Pose implementiert.
* Extraktion der Schlüsselpunkt-Koordinaten implementiert.
* Normalisierung der Schlüsselpunkt-Koordinaten implementiert.
* Speicherung der normalisierten Posen-Sequenzen und Labels (z.B. NumPy-Arrays) implementiert.
* Visualisierung der extrahierten Schlüsselpunkte zur Validierung durchgeführt.
* 



#### Phase 2: Modelltraining \& Konvertierung (Python)

* Normalisierte Posen-Sequenzen und Labels geladen.
* Sequenzen auf einheitliche Länge gebracht (Padding/Trimming).
* Labels in One-Hot-Encoding umgewandelt.
* Daten in Trainings- und Validierungssets aufgeteilt.
* LSTM- (oder GRU-)Modell in TensorFlow/Keras definiert.
* Modell erfolgreich trainiert.
* Performance des Modells auf dem Validierungsset überprüft (hohe Genauigkeit erwartet).
* Trainiertes Modell in .tflite-Format konvertiert.
* Optimierungen (z.B. Quantisierung) beim Konvertieren angewendet.





#### Phase 3: Flutter App Entwicklung \& Integration

* Neues Flutter-Projekt erstellt.
* Notwendige Flutter-Pakete zur pubspec.yaml hinzugefügt (camera, path\_provider, tflite\_flutter, google\_ml\_kit\_pose\_detection).
* Kameravorschau in Flutter implementiert.
* Funktionalität zum Starten/Stoppen der Videoaufnahme in Flutter implementiert.
* Temporäre Speicherung des aufgenommenen Videos implementiert.
* Pose Estimation in Flutter implementiert (Live-Stream-Verarbeitung mit google\_ml\_kit\_pose\_detection oder ähnlichem).
* Gleiche Normalisierungslogik für Posen-Daten in Flutter implementiert wie in Python.
* .tflite-Modell in die Flutter-App geladen.
* TFLite-Inferenz mit den normalisierten Posen-Sequenzen in Flutter durchgeführt.
* Verarbeitung der Modell-Ausgabe (Wahrscheinlichkeiten) implementiert.
* Buttons und Statusanzeigen für die Benutzerführung implementiert.





#### Phase 4: Testen \& Iteration (MVP)

* End-to-End-Funktionstest mit neuen Aufnahmen der zwei Wörter erfolgreich durchgeführt.
* Alle identifizierten Fehler behoben.
* Erkennungsgenauigkeit für die zwei Wörter überprüft und als ausreichend befunden.
* Performance (Geschwindigkeit) der Erkennung als akzeptabel befunden.
* Optional: Dokumentation der Schritte und Erkenntnisse

