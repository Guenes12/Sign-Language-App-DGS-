#### Checkliste für die Sign-Language-App

&#x09;	Projekt: Sign-Language-App(DGS)





Projektziel
Entwicklung eines mobilen Prototyps zur Erkennung ausgewählter Gebärden.

Die Gebärden werden über die Smartphone-Kamera aufgenommen, mittels MediaPipe in Landmark-Daten überführt und anschließend durch ein selbst trainiertes neuronales Klassifikationsmodell erkannt.


⸻

Phase 0: Flutter UI & Architekturgrundlage
✔ Flutter-Projekt initial erstellt

✔ Grundlegende App-Struktur aufgebaut:

Screens

Services

Controller

Models

Utilities

✔ HomeScreen implementiert

✔ OnboardingScreen implementiert

✔ RecordingScreen implementiert

✔ CameraService zur Steuerung der Smartphone-Kamera implementiert

✔ RecordingController zur Steuerung der Aufnahme- und Anwendungslogik implementiert

✔ Kamerawechsel zwischen Front- und Rückkamera implementiert

✔ Statusanzeige implementiert

✔ Aufnahme-Timer implementiert

✔ Fortschrittsanzeige implementiert

✔ maximale Aufnahmezeit auf 10 Sekunden begrenzt

✔ Möglichkeit zum manuellen Beenden der Aufnahme implementiert
Ziel: Aufbau einer funktionsfähigen mobilen Benutzeroberfläche unabhängig von der KI.


⸻

Phase 1: Flutter-Funktionstests
✔ Grundlegende Funktionalität der Flutter-Anwendung getestet

✔ Navigation zwischen Home, Anleitung und Aufnahme getestet

✔ Kamerainitialisierung getestet

✔ Start und Stopp der Aufnahme getestet

✔ Kamerawechsel getestet

✔ Timer und Fortschrittsanzeige getestet

✔ UI-Zustände während der Aufnahme überprüft

✔ Erweiterte automatisierte Unit- und Integrationstests
Ziel: Sicherstellen, dass die mobile Anwendung unabhängig von der KI-Komponente stabil funktioniert.


⸻

Phase 2: Datenerhebung für das eigene KI-Modell
✔ Definition der zu erkennenden Gebärden

Aktuell verwendete Klassen:

ja

nein

keine Ahnung

essen

Not

Angst

danke

✔ Aufbau eines eigenen Datensatzes

✔ Aufnahme von ca. 250 Videos pro Klasse

✔ Insgesamt ca. 1.750 Videos

✔ Verwendung eines Smartphones zur Datenerhebung

✔ Standardisierung der Aufnahmebedingungen

✔ Speicherung der Videos nach Klassen

✔ Überprüfung der Datenqualität


✔  Untersuchung von Variationen hinsichtlich:

Personen

Beleuchtung

Kameraposition

Hintergrund

Entfernung zur Kamera

Bewegungsgeschwindigkeit
Ziel: Erstellung eines geeigneten Datensatzes für das Training eines eigenen Klassifikationsmodells.


⸻

Phase 3: MediaPipe Feature Extraction
✔ Integration von MediaPipe Holistic

✔ Verarbeitung der einzelnen Videoframes

✔ Extraktion der Pose-Landmarks

✔ Extraktion der linken Hand-Landmarks

✔ Extraktion der rechten Hand-Landmarks

✔ Umgang mit nicht erkannten Landmarks implementiert

✔ Erzeugung eines Feature-Vektors pro Frame

✔ Standardisierung der Sequenzlänge

✔ Verwendung von 45 Frames pro Video

✔ Verwendung von 75 Landmark-Punkten × 3 Koordinaten

→ 225 Features pro Frame

Damit entsteht für jedes Video ein Tensor der Form:  (45, 225)

Ziel: Transformation der Rohvideos in strukturierte numerische Eingabedaten für das neuronale Netz.

⸻
Phase 4: Aufbau des eigenen KI-Modells

✔ Definition eines eigenen neuronalen Klassifikationsmodells

✔ Verwendung eines sequenzbasierten Modells zur Verarbeitung der 45 Frames

✔ Integration einer LSTM-basierten Architektur

✔ Anpassung der Ausgabe an die Anzahl der Gebärdenklassen

✔ Verwendung von 7 Klassen

✔ Training des Modells mit dem eigenen Datensatz

✔ Aufteilung der Daten in Trainings- und Validierungs-/Testdaten

✔ Verwendung von Early Stopping

✔ Speicherung des besten Modellzustands
Aktueller Trainingsstand:

ca. 99 % Training Accuracy

ca. 96 % Validation Accuracy

Loss ca. 0,04

Ziel: Entwicklung eines eigenen Modells zur Klassifikation der definierten Gebärden.


⸻

Phase 5: Modellvalidierung
✔ Erstellung eines Classification Reports

✔ Berechnung von:

Precision

Recall

F1-Score

Accuracy

✔ Erstellung einer Confusion Matrix

✔ Analyse der Klassifikationsleistung pro Gebärde

✔ Identifikation problematischer Klassen

✔ Untersuchung von Fehlklassifikationen


Ziel: Nicht nur die Trainingsgenauigkeit, sondern insbesondere die Fähigkeit des Modells zur Generalisierung auf neue Aufnahmen bewerten.


⸻

Phase 6: Konfidenz- und Unsicherheitsbehandlung
✔ Wahrscheinlichkeitsausgabe des Modells implementiert

✔ Ermittlung der vorhergesagten Klasse über die höchste Wahrscheinlichkeit

✔ Konfidenzwert aus der Modellwahrscheinlichkeit bestimmt

✔ Schwellenwert für unsichere Vorhersagen eingeführt


Wichtig: Die Konfidenz wird dabei als Modellwahrscheinlichkeit interpretiert und nicht automatisch als statistisch kalibrierte Wahrscheinlichkeit.
Ziel: Verhindern, dass beliebige Bewegungen zwangsläufig als eine der bekannten Gebärden ausgegeben werden.

⸻
Phase 7: FastAPI-Integration als Entwicklungs- und Testsystem

✔ FastAPI-Server implementiert

✔ Video-Upload vom Flutter-Frontend implementiert

✔ Verarbeitung des Videos auf dem Server

✔ MediaPipe Feature Extraction auf dem Server

✔ Übergabe der Features an das eigene KI-Modell

✔ Klassifikation des Videos

✔ Rückgabe von: Label und Confidence

✔ Flutter zeigt das Klassifikationsergebnis an
Ziel: Zunächst eine funktionierende Referenzpipeline schaffen, um das selbst trainierte Modell unabhängig von der mobilen On-Device-Inferenz testen zu können.

⸻
Phase 8: Systemtests & wissenschaftliche Evaluation

✔  Test mit bekannten Datensatz-Videos

✔  Test mit unbekannten Aufnahmen

✔  Test mit verschiedenen Personen

✔ Test mit Front- und Rückkamera

✔  Test unter unterschiedlichen Lichtbedingungen

✔  Test mit unterschiedlichen Hintergründen

✔  Untersuchung der Fehlklassifikationen

✔  Untersuchung der Konfidenzwerte

⸻
Phase 9: Vokabular-Erweiterung, Fehlerdiagnose & Modelloptimierung

✔ Erweiterung des Datensatzes auf 7 Gebärdenklassen:
    - Ergänzung der 3 Basiswörter (ja, nein, keineAhnung) um 4 alltagsrelevante Klassen (essen, danke, Angst, not)
    - Aufnahme und strukturierte Vorbereitung der neuen Videosequenzen

✔ Fehleranalyse & -behebung 
    
✔ wiederholter Systemtests (erneutes Abarbeiten von Phase 8)
