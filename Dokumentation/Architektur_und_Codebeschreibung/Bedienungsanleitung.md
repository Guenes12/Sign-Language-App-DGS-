#### &#x09;Bedienungs- und Entwickleranleitung der Sign-Language-App



&#x09;	Projekt: Sign-Language-App(DGS)





Dieses Dokument beschreibt die Inbetriebnahme, den Trainingszyklus sowie die Diagnosewerkzeuge des Systems zur Erkennung der Deutschen Gebärdensprache. Das System besteht aus zwei Komponenten:
- Frontend (Mobile Applikation in Flutter): Videoaufnahme und Visualisierung der Ergebnisse.
- Backend (REST-API in FastAPI/TensorFlow): Merkmalsextraktion mit MediaPipe und Klassifikation mittels Bidirectional LSTM und invarianter Merkmalsschicht.
 
 
1. Systemvoraussetzungen
 
Für den Betrieb und Test des Gesamtsystems werden folgende Umgebungen benötigt:
- Server-Umgebung (Backend):
    - Betriebssystem: Windows 10/11, macOS oder Linux (Ubuntu 22.04 LTS empfohlen)
    - Python-Version: Python 3.10 oder 3.11
    - Installierte Kernbibliotheken: FastAPI, Uvicorn, TensorFlow / Keras 3, OpenCV (Headless), MediaPipe, NumPy, Scikit-Learn
    - Hardware-Empfehlung: Mindestens 8 GB Arbeitsspeicher und ein Multi-Core-Prozessor zur flüssigen Extraktion der Landmark-Punkte
- Client-Umgebung (Frontend):
    - Flutter SDK (Version 3.19 oder höher) und Dart SDK
    - Physisches Smartphone (Android ab Version 8.0 oder iOS ab Version 13) mit integrierter Kamera oder ein konfigurierter Emulator mit aktivierter Kamera-Emulation
    - Aktive Netzwerkverbindung (WLAN) zwischen Smartphone und Server
 
 

2. Inbetriebnahme des Gesamtsystems
 
2.1 Vorbereitung des mobilen Endgeräts
 
Für die Ausführung der Flutter-Applikation auf einem physischen Android-Endgerät über eine USB-Kabelverbindung sind folgende Schritte erforderlich:
- Entwickleroptionen freischalten: Unter Einstellungen > Über das Telefon siebenmal auf den Eintrag Build-Nummer tippen, bis die Meldung erscheint, dass die Entwickleroptionen aktiv sind.
- USB-Debugging autorisieren: In den Entwickleroptionen den Menüpunkt USB-Debugging aktivieren. Nach dem Verbinden mit dem Rechner die Autorisierungsanfrage des Rechners dauerhaft bestätigen.
- Netzwerk-Konfiguration (IP-Adresse hinterlegen):
    - Rechner und Mobiltelefon müssen sich im selben lokalen Netzwerk (WLAN) befinden.
    - Die IPv4-Adresse des Rechners ermitteln (z. B. über den Befehl ipconfig unter Windows).
    - In der Konfigurationsdatei der mobilen Applikation (frontend/lib/config/app_config.dart) die ermittelte IP-Adresse eintragen:
      static const String serverIp = '<IP-ADRESSE_DES_RECHNERS>';
 
 
2.2 Starten des Backend-Servers
 
Das Backend stellt die REST-Schnittstelle über den Server Uvicorn bereit. Der Host 0.0.0.0 stellt sicher, dass der Dienst über alle Netzwerkschnittstellen erreichbar ist.
- Arbeitsverzeichnis: backend
- Ausführungsbefehl: uvicorn app.main:app --host 0.0.0.0 --port 8000
 
Nach dem Start ist der Server unter Port 8000 aktiv. Die interaktive API-Dokumentation (Swagger UI) kann im Browser unter http://localhost:8000/docs aufgerufen werden.
 
 
2.3 Starten der mobilen Applikation
 
Sobald der Backend-Server läuft, wird die mobile Anwendung kompiliert und auf das verbundene Mobiltelefon übertragen:
- Arbeitsverzeichnis: frontend
- Ausführungsbefehl: flutter run
 
 

3. Trainingszyklus und Modellerstellung
 
Die Pipeline trennt die rechenintensive Merkmalsextraktion strikt vom eigentlichen Modelltraining. Dies gewährleistet deterministische Datengrundlagen und ermöglicht iterative Modellarchitektur-Iterationen ohne wiederholtes Video-Decoding.
 
3.1 Merkmalsextraktion neuer Videos (Feature-Generierung)
 
Werden neue Trainingsvideos aufgenommen, müssen diese im Verzeichnis backend/dataset/<Klassenname>/ strukturiert abgelegt werden (unterstützte Formate: .mp4, .avi, .mov, .mkv). Das Skript führt die vollständige Vorverarbeitungskette aus und speichert die extrahierten Merkmalsmatrizen als komprimierte NumPy-Arrays (.npy) ab.
- Arbeitsverzeichnis: backend
- Ausführungsbefehl: python -m training.feature_generator
 
Technische Zwischenschritte der PreprocessingPipeline:
- Video-Laden (VideoLoader): Dekodieren der Videosequenz in standardisierte BGR-Frames mittels OpenCV.
- Orientierungskorrektur (VideoOrientationCorrector): Automatische Lageprüfung und Ausrichtung (Kandidaten: 0°, 90°, 180°, 270°). Über eine Pose-Analyse der Schulterachse und Kopfposition (Nase oberhalb Schulterzentrum) wird eine fehlerhafte Ausrichtung von Mobiltelefon-Aufnahmen korrigiert.
- Temporales Resampling (FrameSampler): Vereinheitlichung variabler Frame-Anzahlen auf eine feste Zeitachse von exakt T = 90 Frames per linearer zeitlicher Abtastung.
- Landmark-Extraktion (MediaPipeExtractor): Erkennung anatomischer Bezugspunkte mittels MediaPipe Holistic:
    - Dominante Hand: 21 Gelenkpunkte (Wrist, MCP-, PIP-, DIP-Gelenke und Fingerspitzen) mit je (X, Y, Z) = 63 Dimensionen. Die Bestimmung der dominanten Hand erfolgt dynamisch über die Erkennungshäufigkeit der rechten bzw. linken Hand.
    - Pose-Oberkörper: 7 Schlüsselpunkte (Nase, linke/rechte Schulter, linkes/rechtes Ohr, linke/rechte Hüfte) mit je (X, Y, Z) = 21 Dimensionen.
    - Gesichts-Landmarks: 7 markante Konturpunkte im Mund- und Nasenbereich mit je (X, Y, Z) = 21 Dimensionen.
    - Zusammensetzung pro Frame: 63 + 21 + 21 = 105 Dimensionen.
- Landmark-Normalisierung (LandmarkNormalizer):
    - Zeitliche lineare Interpolation zur Kompensation temporärer Tracking-Ausfälle.
    - Translationsinvarianz: Subtraktion des Schulterzentrums (Mittelpunkt aus linker und rechter Schulter) von allen Koordinaten.
    - Skalierungsinvarianz: Division aller zentrierten Koordinaten durch die robuste mediane Schulterbreite zur Eliminierung von Abstandsunterschieden zur Kamera.
- Ablage und Validierung: Die resultierenden Tensoren der Dimension (90, 105) werden unter backend/features/<Klassenname>/<Videoname>.npy persistiert.
 
 
3.2 Modelltraining und Modellpersistierung
 
Das Training liest die vorberechneten .npy-Dateien dynamisch ein, initialisiert die tiefe neuronale Architektur und trainiert das Modell end-to-end.
- Arbeitsverzeichnis: backend
- Ausführungsbefehl: python -m training.train
 
Ablauf und Trainingskonfiguration:
- Datenaggregation (DataLoader): Dynamisches Scannen des Feature-Verzeichnisses backend/features/, automatisches Einlesen der Klassen und Validierung auf Vollständigkeit (Ausschluss beschädigter oder unvollständiger Arrays).
- Datensatz-Aufteilung: Stratifizierter Train/Test-Split (80 % Training, 20 % Test) zur Wahrung identischer Klassenverteilungen. Vom Trainingsanteil werden zusätzlich 20 % als Validierungsmenge reserviert.
- Modellarchitektur (PeakAwareDGSModel):
    - InvariantFeatureLayer: Transformation der 105 Roh-Landmarks in 159 biomechanisch invariante Merkmale (63 lokale wrist-zentrierte Handform-Koordinaten, 63 differentielle Geschwindigkeitswerte, 14 morphologische Fingerkennzahlen inkl. Knospenhand-Score und Pinch-Ratio, 13 Gesichts- und Körperdistanzvektoren sowie 6 kinematische Richtungsparameter).
    - Rekurrente Verarbeitung: Zwei gestapelte Bidirectional-LSTM-Schichten (64 und 48 Einheiten) zur Erfassung vorwärts- und rückwärtsgerichteter zeitlicher Dynamiken.
    - Peak-Aware Temporal Pooling: Parallele Extraktion dominanter Gestenspitzen (GlobalMaxPooling1D) und globaler Ausführungskontexte (GlobalAveragePooling1D) mit anschließender Konkatenation.
    - Klassifikationskopf: Dense-Schicht (64 Einheiten, ReLU-Aktivierung), Batch-Normalisierung, Dropout (Rate: 0.3) und finale Softmax-Ausgabeschicht über alle 7 Klassen.
- Hyperparameter und Callbacks:
    - Optimizer: Adam (Adaptive Moment Estimation - adaptiver Gradientenabstiegs-Algorithmus) mit einer Lernrate von 0.001.
    - Batch-Größe: 8 Sequenzen.
    - Frühabstimmung (EarlyStopping): Obergrenze von 150 Epochen; bricht ab, wenn der Validierungsverlust über 30 Epochen nicht weiter sinkt, und stellt die Gewichte der besten Epoche wieder her.
    - Dynamische Lernratenreduktion (ReduceLROnPlateau): Halbiert die Lernrate (Faktor 0.5), falls der Validierungsverlust über 6 Epochen stagniert.
- Modellexport: Das Modell wird unter backend/trained_models/gesture_model.keras gesichert. Zur Vermeidung von Versions- und Label-Inkonsistenzen wird die Klassenzuordnungsliste (classes.json) direkt in das Keras-Zip-Archiv eingebettet.
 
 

4. Test-, Evaluierungs- und Diagnosewerkzeuge
 
Zur vollständigen Überprüfung des Gesamtsystems – von der Modulvalidierung über die statistische Modellgüte bis hin zur biomechanischen Fehlerursachenanalyse – stehen folgende Werkzeuge bereit:
 
4.1 System- und Einzeltests
 
4.1.1 Unit- und Pipeline-Tests (test_pipeline_unit.py)

- Zweck: Überprüft isoliert Kernkomponenten wie den FrameSampler (Skalierung beliebiger Frame-Längen auf exakt 90 Frames) sowie die Form- und Typenvalidierung des LandmarkNormalizers.
- Arbeitsverzeichnis: backend
- Ausführungsbefehl: python -m pytest tests/unit/test_pipeline_unit.py -v
- Ergebnis: Verifiziert die mathematische Integrität der Vorverarbeitungskomponenten.


4.1.2 Domain- und Konfigurations-Tests (test_domain_and_config.py)

- Zweck: Überprüft die mathematische Konsistenz der globalen Feature-Dimensionen (TARGET_FRAMES = 90, FEATURES_PER_FRAME = 105, `HAND_FEATURE_DIMS = 63) sowie die saubere Instanziierung der Domain-Klasse PredictionResult (label, confidence) und deren Serialisierung (to_dict()).
- Arbeitsverzeichnis: backend
- Ausführungsbefehl: python -m pytest tests/unit/test_domain_and_config.py -v
- Ergebnis: Garantiert, dass Datenmodelle und Hyperparameter-Konstanten systemweit konsistent definiert sind.


4.1.3 Gezielter Einzeltest eines Rohvideos (test_prediction.py)

- Dient der schnellen Überprüfung eines einzelnen Videos bei Unklarheiten in der Klassifikation.
- Das zu testende Video unter backend/testvideos/<Klassenname>/<Dateiname>.mp4 (oder direkt in backend/testvideos/) ablegen.
- In der Datei backend/tests/analysis/test_prediction.py den Pfad anpassen bzw. den voreingestellten Standardpfad nutzen.
- Arbeitsverzeichnis: backend
- Ausführungsbefehl: python -m tests.analysis.test_prediction               
- Ergebnis: Führt Vorverarbeitung und Klassifikation aus und gibt das erkannte Label, die Konfidenz sowie die Wahrscheinlichkeitsverteilung über alle Klassen aus.


4.2 Frontend-Tests (Flutter)

In Ergänzung zu den Backend-Prüfungen verfügt das Frontend über eigene automatisierte Tests, die die clientseitige Geschäftslogik und Benutzeroberfläche absichern.

4.2.1 Unit- und Modell-Tests
- Zweck: Überprüft die isolierte Logik der Hilfsklassen und Datenstrukturen:  
    - Validierung des TimeFormatter (korrekte Formatierung von Sekundenwerten in MM:SS).  
    - Validierung der TranslationResponse (fehlerfreies Deserialisieren der Backend-JSON-Antwort mit label und confidence).
    - Überprüfung der AppConfig auf die korrekte URL-Zusammensetzung (/predict).
- Arbeitsverzeichnis: frontend (Hauptverzeichnis der Flutter-App)
- Ausführungsbefehl: flutter test


4.3 Statistische Gesamtevaluierung des Modells (evaluate.py)
 
- Dieses Skript führt die wissenschaftliche Gesamtevaluierung des trainierten Keras-Modells auf dem disjunkten Testdatensatz durch.
- Arbeitsverzeichnis: backend
- Ausführungsbefehl: python -m training.evaluate           
- Ergebnis und Metriken:
    - Klassifikationsbericht: Ausgabe von Precision, Recall und F1-Score für jede der 7 Gebärdenklassen sowie der Gesamtmetriken (Macro und Weighted Average).
    - Gesamtgenauigkeit (Test Accuracy): Ausgabe der exakten Trefferquote über den Testsplit.
    - Konfusionsmatrix: Zeigt Verwechslungen zwischen Klassen zeilen- und spaltenweise auf.
 
 
4.4 Biomechanische Diagnosewerkzeuge für Testdaten
 
4.4.1 Systematische Massendiagnose von Rohvideos (analyze_saved_testvideos.py)

- Dieses Werkzeug validiert das trainierte Modell gegenüber einer Sammlung ungesehener Testvideos und führt eine detaillierte biomechanische Fehlerursachenanalyse durch.
- Arbeitsverzeichnis: backend
- Ausführungsbefehl: python -m tests.analysis.analyze_saved_testvideos
- Funktionsweise und Analyseablauf:
    - Automatische Iteration: Das Skript scannt den Ordner backend/testvideos/ nach Videodateien.
    - On-the-Fly-Extraktion: Jedes Video durchläuft in Echtzeit die PreprocessingPipeline (Drehungskorrektur, Frame-Sampling, MediaPipe-Holistic-Extraktion und Normalisierung).
    - Physikalische Merkmalsanalyse: Parallel zur Modellvorhersage berechnet das Skript biomechanische Kennzahlen:
        - Räumliche Position: Relativer vertikaler Abstand zwischen Handgelenk und Nase. Ermittelt, ob die Geste auf Stirnhöhe (keineAhnung), Mundhöhe (essen, danke) oder Brusthöhe (ja, nein, Angst, not) ausgeführt wurde.
        - Bewegungsvektoren: Aufteilung in horizontale Bewegungsanteile (Delta X) und vertikale Anteile (Delta Y). Ein hohes X/Y-Verhältnis kennzeichnet horizontales Wedeln (nein), ein niedriges Verhältnis vertikales Nicken/Handbewegen (ja).
        - Hand- und Fingermorphologie: Berechnung des Abstands zwischen Daumenspitze und Zeigefingerspitze (Pinch-Distanz) zur Unterscheidung von Knospenhand (essen) und flacher Hand (danke).
    - Ursachen-Diagnose bei Fehlklassifikation: Weicht das Ergebnis vom erwarteten Label ab, formuliert das Skript automatisch eine Hypothese (z. B. Handhaltung zu hoch oder flache Hand statt geschlossener Fingerspitzen).
    - Ergebnisstatistik: Ausgabe einer tabellarischen Trefferquote pro Gebärdenklasse sowie einer Gesamtauswertung.
 

4.4.2 Hochperformante Diagnose gespeicherter Merkmale (analyze_saved_testfeatures.py)

- Wurden die Merkmale der Testvideos bereits zuvor extrahiert (mittels python -m training.feature_generator_testvideos), vermeidet dieses Skript das zeitintensive Video-Decoding und die MediaPipe-Berechnung.
- Arbeitsverzeichnis: backend
- Ausführungsbefehl: python -m tests.analysis.analyze_saved_testfeatures
- Ergebnis: Liest direkt die vorberechneten .npy-Dateien aus backend/testvideos_features/ ein und liefert denselben ausführlichen Diagnose- und Kennzahlenbericht in unter einer Sekunde.
