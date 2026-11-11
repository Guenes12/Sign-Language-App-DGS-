#### Technische Dokumentation – Python-FastAPI-Backend der Sign-Language-App

&#x09;	Projekt: Sign-Language-App(DGS)

&#x09;				Autor: Semanur 

 
Das Python-Backend bildet die zentrale Verarbeitungs- und Inferenzkomponente der Sign-Language-App. Seine Hauptaufgabe besteht darin, über die Smartphone-Kamera aufgenommene Gebärdensprachvideos entgegenzunehmen, eine mehrstufige Merkmalsextraktion und geometrische Normierung durchzuführen und das Bewegungsmuster mittels eines tiefen neuronalen Netzes zu klassifizieren.
 
Als Ergebnis liefert das Backend die erkannte Gebärde sowie den zugehörigen Konfidenzwert im schlanken JSON-Format an das mobile Endgerät zurück.
 
Der Schwerpunkt des Backends liegt auf der asynchronen Bereitstellung der HTTP-Schnittstelle, der robusten Lagekorrektur variabler Videoquellen, der skelettbasierten Landmark-Extraktion mittels MediaPipe Holistic sowie der Inferenz über eine mathematisch translations- und skaleninvariante Netzarchitektur (Bi-LSTM).
 
 
1. Projektstruktur
 
Das Backend ist modular nach funktionalen Schichten und Verantwortlichkeiten strukturiert:
 
* app/: Kern der Produktivanwendung (REST-API, Schnittstellenrouten, Domänenmodelle, Dienste und globale Konfiguration).
* training/: Trainingspipeline, bestehend aus der Rohdaten-Vorverarbeitung (preprocessing/), dem Datenlader (data_loader.py), dem Label-Encoder (label_encoder.py), der Modellarchitektur (model_builder.py) und den Trainingsskripten.
* tests/: Automatisierte Softwaretests, aufgeteilt in isolierte Unit-Tests (unit/) und physikalische Merkmals- sowie Lage- und Fehlerursachenanalysen (analysis/).
* trained_models/: Persistierung trainierter Modellgewichte und Klassenmetadaten (gesture_model.keras).
* dataset/ & features/: Datenhaltung für rohe Klassen-Trainingsvideos und serialisierte NumPy-Merkmalsmatrizen (.npy).
 
Diese Struktur trennt den operativen API-Dienst strikt vom Trainingszyklus und den mathematischen Analysewerkzeugen.
 
 
2. Einstiegspunkt der Anwendung
 
Die Datei app/main.py bildet den Einstiegspunkt des FastAPI-Backends.
 
Ihre Aufgabe besteht darin, die FastAPI-Anwendungsinstanz zu initialisieren, grundlegende Status- und Health-Check-Routen bereitzustellen (@app.get("/") -> {"status": "running"}) und die thematischen Router für Vorhersagen einzubinden.
 
Zur reibungslosen Kommunikation mit mobilen Endgeräten im lokalen Netzwerk ist zudem eine CORS-Middleware (Cross-Origin Resource Sharing) eingerichtet. Dadurch bleibt der zentrale Einstiegspunkt übersichtlich und frei von schwerer Merkmalsextraktions- oder Modelllogik.
 
 
3. Zentrale Konfiguration
 
Sämtliche globalen Hyperparameter, Dateipfade und mathematischen Dimensionen werden zentral in app/config.py verwaltet.
 
Dazu gehören:
* Pfaddefinitionen: Basisverzeichnisse für Datensätze (dataset/), vorberechnete Merkmale (features/), temporäre Dateien und gespeicherte Modelle (trained_models/).
* Sequenzparameter: Ziel-Framelänge (TARGET_FRAMES = 90).
* Dimensionen: Handmerkmale (63), Posemerkmale (21) und Gesichtsmerkmale (21), woraus sich die Eingabebreite von exakt 105 Rohmerkmalen pro Zeitschritt ergibt (FEATURES_PER_FRAME = 105). Die anschließende Invarianzschicht expandiert diese auf 159 Merkmale (INV_FEATURE_DIM = 159).
* Hyperparameter des Trainings: Maximale Epochen (150), Batch-Größe (8), Lernrate (0.001) und Abbruchkriterien für das Training.
 
Die zentrale Hinterlegung garantiert, dass Trainingspipeline, REST-API und Analyseskripte stets auf identischen Annahmen operieren.
 
 
4. Domänenmodelle
 
Die Fachlichkeit der Vorhersage wird im Paket app/domain/ über kompakte Datenklassen (dataclasses mit slots=True) abgebildet:
 
* Gesture (app/domain/gesture.py): Repräsentiert eine Gebärde anhand ihres Textbezeichners (label).
* PredictionResult (app/domain/prediction_result.py): Kapselt das Klassifikationsergebnis bestehend aus label und confidence und stellt eine Hilfsmethode to_dict() bereit, die den Konfidenzwert gerundet zur JSON-Serialisierung formatiert:
  {"label": self.label, "confidence": round(self.confidence, 4)}
 
Diese Kapselung entkoppelt die interne Modellvorhersage sauber von externen Transportformaten.
 
 
5. REST-API und Routing
 
Der Vorhersage-Endpunkt wird in app/api/prediction.py über einen FastAPI-APIRouter bereitgestellt.
 
Die Route @router.post("/predict") nimmt eingehende Videodateien als UploadFile über das HTTP-Multipart-Verfahren entgegen.
 
Zur Entkopplung des asynchronen Netzwerk-Streams von OpenCV speichert der Router den Dateiinhalt zunächst in einer systemspezifischen temporären Datei (tempfile.NamedTemporaryFile). Anschließend wird die Sequenz über die Vorverarbeitungspipeline verarbeitet und an den Vorhersagedienst übergeben.
 
 
6. Sichere Dateibereinigung
 
Da Videodateien beträchtlichen Speicherplatz beanspruchen können, ist die temporäre Dateiverwaltung in einem try-finally-Block gekapselt.
 
Unabhängig davon, ob die Merkmalsextraktion erfolgreich verläuft oder durch eine beschädigte Videodatei eine Ausnahme auslöst, stellt die finally-Klausel sicher, dass die temporäre Datei (os.remove(temp_path)) nach Abschluss des Aufrufs rückstandslos gelöscht wird.
 
 
7. PredictionService und Service-Schicht
 
Die Fachlogik zur Ausführung von Vorverarbeitung und Klassifikation ist in app/services/ gebündelt:
 
* PredictionService (app/services/prediction_service.py):
  Lädt das neuronale Netz aus trained_models/gesture_model.keras. Eine Besonderheit liegt im Auslesen der Klassenbezeichner: Diese werden direkt aus dem ZIP-Archiv der .keras-Datei entnommen (classes.json). Dadurch wird garantiert, dass die Reihenfolge der Modell-Ausgabeneuronen exakt zu den Textlabels passt. Die Methode predict(sequence) validiert die Eingabedimension, fügt die Batch-Dimension hinzu ((1, 90, 105)), führt den Vorwärtspass durch und gibt ein PredictionResult zurück.
 
* MediaPipeService (app/services/mediapipe_service.py):
  Fungiert als handlicher Service-Wrapper um die PreprocessingPipeline und stellt eine einfache Schnittstelle process_video(video_path) für übergeordnete Module bereit.
 
* ModelService (app/services/model_service.py):
  Kapselt das reine Laden des TensorFlow-Keras-Modells und führt die mathematische Tensor-Inferenz durch.
 
 
8. Vorverarbeitungs-Pipeline (PreprocessingPipeline)
 
Die Klasse PreprocessingPipeline (training/preprocessing/pipeline.py) koordiniert die Transformation eines rohen Videos in ein bereinigtes NumPy-Array der Dimension (90, 105).
 
Sie fungiert als Fassade über fünf sequenziell geschaltete Spezialkomponenten:
1. VideoLoader
2. VideoOrientationCorrector
3. FrameSampler
4. MediaPipeExtractor
5. LandmarkNormalizer
 
Entspricht das extrahierte Array am Ende nicht exakt der Zielform (90, 105), bricht die Pipeline mit einem definierten ValueError ab.
 
 
9. Frame-Dekodierung (VideoLoader)
 
Der VideoLoader (training/preprocessing/video_loader.py) abstrahiert den Zugriff auf OpenCV (cv2.VideoCapture).
 
Er öffnet den übergebenen Dateipfad, überprüft die Lesbarkeit des Containers und liest die Einzelbilder fortlaufend in eine Liste von BGR-NumPy-Arrays ein. Nach dem Einlesen wird der Hardware-Handle im finally-Block sofort freigegeben.
 
 
10. Automatische Orientierungskorrektur
 
Smartphones zeichnen Videos je nach Haltung mit internen Rotations-Metadaten auf, was bei standardmäßigem Auslesen zu um 90° oder 180° verdrehten Frames führen kann.
 
Der VideoOrientationCorrector (training/preprocessing/video_orientation_corrector.py) behebt dieses Problem algorithmisch:
* Anhand einer Stichprobe von Einzelbildern wird über MediaPipe Pose die anatomische Lage evaluiert.
* Zur Bewertung wird ein Güte-Score herangezogen: Die Schulterlinie muss horizontal verlaufen (dy -> 0) und die Nase zwingend oberhalb des Schulterzentrums liegen (y_Nase < y_Schulter). Liegt der Kopf unten, wird ein hoher Strafwert vergeben.
* Aus den Kandidaten 0°, 90°, 180° und 270° wird die Rotation mit dem minimalen Median-Fehlerscore gewählt und über cv2.rotate auf alle Frames angewendet.
 
 
11. Temporales Resampling (FrameSampler)
 
Die Dauer und Bildrate von Gebärdenaufnahmen variiert in der Praxis.
 
Der FrameSampler (training/preprocessing/frame_sampler.py) normalisiert jede beliebige Videolänge auf exakt T = 90 Zeitschritte. Über np.linspace(0, len(frames) - 1, TARGET_FRAMES, dtype=int) wird eine gleichmäßige lineare Abtastung über den gesamten Zeitverlauf durchgeführt.
 
Kurze Videos werden dadurch zeitlich gedehnt, lange Videos ohne Informationsverlust des Gesamtverlaufs gestaucht.
 
 
12. Skelett- und Merkmalsextraktion (MediaPipeExtractor)
 
Der MediaPipeExtractor (training/preprocessing/mediapipe_extractor.py) nutzt MediaPipe Holistic im Tracking-Modus (smooth_landmarks=True):
 
* Dominante Hand (63 Merkmale): In Gebärdensprachen führt häufig eine Hand die primäre Bedeutung. Das Skript zählt die Detektionshäufigkeit beider Hände über das Video und wählt die dominant sichtbare Hand aus (21 Gelenke mal 3 Raumachsen = 63 Dimensionen).
* Oberkörper-Pose (21 Merkmale): Extraktion von 7 anatomischen Schlüsselpunkten (Nase, linke/rechte Schulter, Ohren und Hüften).
* Gesichtskonturen (21 Merkmale): Extraktion von 7 Indizes der Lippen- und Nasengeometrie zur Unterscheidung von Mundgesten.
 
Die Merkmale werden pro Frame zu einem Vektor mit 105 Gleitkommawerten konkateniert.
 
 
13. Geometrische Normalisierung (LandmarkNormalizer)
 
Der LandmarkNormalizer (training/preprocessing/landmark_normalizer.py) macht die extrahierten Koordinaten unabhängig von Personengröße und Kameraabstand:
 
* Ausfallkompensation: Tracking-Lücken (NaN-Werte) werden über die Zeitachse per linearer 1D-Interpolation rekonstruiert.
* Translationsinvarianz: Der Mittelpunkt zwischen linker und rechter Schulter wird berechnet. Alle Koordinaten (Hand, Pose, Gesicht) werden auf dieses Schulterzentrum bezogen.
* Skalierungsinvarianz: Die Distanz zwischen den beiden Schultern wird ermittelt. Alle zentrierten Koordinaten werden durch die mediane Schulterbreite der Sequenz dividiert.
* Extremwert-Clamping: Zur numerischen Stabilisierung des neuronalen Netzes werden Ausreißer auf den Bereich [-5.0, 5.0] begrenzt.
 
 
14. Biomechanische Invarianzschicht (InvariantFeatureLayer)
 
Der InvariantFeatureLayer (training/model_builder.py) ist ein benutzerdefinierter Keras-Layer (tf.keras.layers.Layer), der als erste Stufe im neuronalen Netz sitzt. Er transformiert die 105 normalisierten Koordinaten in 159 rotations-, lage- und geschwindigkeitsinvariante Kennzahlen:
 
1. Lokale Handform (63 Dims): Alle 21 Handpunkte werden relativ zum Handgelenk berechnet.
2. Differenzielle Kinematik (63 Dims): Temporale Geschwindigkeitsdifferenz (dx, dy, dz) von Frame t zu Frame t-1.
3. Morphologische Fingermetriken (14 Dims): Fingerstreckungsverhältnisse, Knospenhand-Score, Daumen-Zeigefinger-Pinch-Distanz und Zeigefinger-Isolation.
4. Körper- und Gesichtsrelationen (13 Dims): 3D-Vektoren und euklidische Distanzen zwischen Fingerspitze und Mund bzw. Nase sowie vertikale Ebenen (Stirn vs. Mund).
5. Kinematische Richtungsmerkmale (6 Dims): Horizontale Dominanz (dx / (dx + dy)), normierter 3D-Richtungseinheitsvektor und Tiefengeschwindigkeit (dz).
 
 
15. Modellarchitektur (PeakAwareDGSModel)
 
Das neuronale Netzwerk (training/model_builder.py) verarbeitet die invarianten Merkmale über eine spezialisierte Architektur:
 
* BatchNormalization: Stabilisierung der Merkmalsverteilungen am Netzeingang.
* Gestapelte Bidirektionale LSTMs:
    * Bidirectional(LSTM(64, return_sequences=True, dropout=0.2))
    * Bidirectional(LSTM(48, return_sequences=True, dropout=0.2))
* Peak-Aware Temporal Pooling: Anstelle eines einfachen letzten Zustands fusioniert das Modell eine GlobalMaxPooling1D-Schicht (erfasst den prägnantesten Bewegungshöhepunkt der Gebärde) und eine GlobalAveragePooling1D-Schicht (erfasst den Kontext) per Konkatenation.
* Dense-Klassifikationskopf: Vollvernetzte Schicht mit 64 Einheiten (ReLU), Batch-Normalisierung, Dropout (0.3) und eine 7-Klassen-Softmax-Schicht.
 
 
16. Klassen-Kodierung (LabelEncoder)
 
Das Modul training/label_encoder.py übernimmt die saubere Verwaltung der Textlabels und ihrer numerischen Indizes:
* Wandelt Klassennamen in Integer-Indizes für das Training um und decodiert sie für die Vorhersage zurück.
* Stellt sicher, dass das Mapping konsistent über JSON-Dateien gespeichert und geladen werden kann.
 
 
17. Feature-Generierung (Offline-Vorverarbeitung)
 
Das Skript training/feature_generator.py entkoppelt die zeitaufwendige Video-Vorverarbeitung vom Modelltraining.
 
Es iteriert durch alle Unterordner in dataset/, führt für jedes Video die PreprocessingPipeline aus, prüft das Ergebnis auf endliche Werte (np.isfinite) und speichert die Matrizen als .npy-Dateien im Ordner features/<Klasse>/ ab.
 
Ein analoges Skript (training/feature_generator_testvideos.py) bereitet separate Testvideos für schnelle Massendiagnosen vor.
 
 
18. Datenlader (DataLoader)
 
Die Klasse DataLoader (training/data_loader.py) liest vorberechnete Features zur Trainingszeit ein.
 
Die Klassen werden dynamisch aus den Unterordnern des Verzeichnisses features/ erkannt. Das Skript lädt alle validen .npy-Dateien, filtert beschädigte Datensätze heraus und gibt die Featurematrix X als float32-Array, den Labelvektor y als int32-Array sowie die sortierte Klassenliste zurück.
 
 
19. Trainingsprozedur und Callbacks
 
Das Training wird über training/train.py gesteuert:
 
* Stratifizierte Aufteilung: Ein train_test_split (80 % Training, 20 % Test) teilt die Daten unter Beibehaltung der Klassenverhältnisse auf.
* Optimierung: Das Netz minimiert den SparseCategoricalCrossentropy-Verlust über den Adam-Optimierer (Lernrate = 0.001).
* Überwachung (Callbacks):
    * EarlyStopping: Bricht nach Stagnation des Validierungsverlusts ab und stellt den besten Gewichtszustand wieder her.
    * ModelCheckpoint: Speichert kontinuierlich das Modell mit dem besten val_loss.
    * ReduceLROnPlateau: Halbiert die Lernrate, wenn der Validierungsverlust über mehrere Epochen stagniert.
 
 
20. Modellpersistierung und Metadaten-Packaging
 
Nach Abschluss des Trainings lädt train.py den besten Checkpoint und öffnet das Keras-Container-Archiv (gesture_model.keras) im Zip-Append-Modus.
 
Die alphabetisch geordnete Liste der Klassenbezeichner wird als classes.json direkt in das Wurzelverzeichnis des .keras-Zip-Pakets geschrieben. Dadurch bilden Modellarchitektur, trainierte Gewichte und Klassenmapping eine untrennbare, versionskonsistente Einheit.
 
 
21. Statistische Gesamtevaluierung
 
Das Evaluierungsmodul training/evaluate.py überprüft das trainierte Modell auf dem ungesehenen Testsplit:
 
* Berechnet die Gesamtgenauigkeit (Test Accuracy) und den Test Loss.
* Erzeugt einen wissenschaftlichen Klassifikationsbericht mit Präzision (Precision), Sensitivität (Recall) und F1-Score pro Gebärde.
* Erstellt eine Konfusionsmatrix zur Identifikation systematischer Verwechslungen zwischen Gestenklassen.
 
 
22. End-to-End Einzeltest (test_prediction.py)
 
Das Skript tests/analysis/test_prediction.py ermöglicht die schnelle Überprüfung einzelner Videodateien:
* Lädt ein konkretes Testvideo direkt von der Festplatte.
* Schickt es durch die PreprocessingPipeline und den PredictionService.
* Gibt das ermittelte Label sowie den Konfidenzwert direkt im Terminal aus – ideal zur schnellen manuellen Verifikation neuer Aufnahmen.
 
 
23. Empirische Lageanalyse (test_video_orientation.py)
 
Das Analysetool tests/analysis/test_video_orientation.py dient der detaillierten Untersuchung von Ausrichtungsproblemen:
* Es analysiert reale Testvideos hinsichtlich Schulterneigung und relativer Kopfposition.
* Ermittelt für jede Aufnahme den exakten Drehwinkel (0°, 90°, 180° oder 270°) und überprüft die Zuverlässigkeit der automatischen Lagekorrektur.
 
 
24. Validierung der Ausrichtungskorrektur (test_video_orientation_correction.py)
 
Das Begleitskript tests/analysis/test_video_orientation_correction.py prüft die tatsächliche Frame-Rotation:
* Es wendet den VideoOrientationCorrector auf Testvideos an und kontrolliert, ob die rotierten Frames anatomisch korrekt ausgerichtet (Schultern waagerecht, Kopf oben) ausgegeben werden.
 
 
25. Biomechanische Video-Massendiagnose
 
Das Diagnosewerkzeug tests/analysis/analyze_saved_testvideos.py dient der detaillierten Fehlerursachenanalyse bei Fehlklassifikationen:
 
* Es scannt testvideos/, extrahiert die Features in Echtzeit und gleicht die Modellvorhersage mit dem erwarteten Label ab.
* Bei Abweichungen berechnet das Skript biomechanische Indikatoren (Handhöhe bezogen auf die Nase, Pinch-Distanz zwischen Daumen und Zeigefinger, Bewegungsrichtung X/Y) und generiert automatische Erklärungen (z. B. ob eine Gebärde versehentlich auf Stirnhöhe statt vor der Brust ausgeführt wurde).
 
 
26. Hochperformante Merkmalsdiagnose
 
Für schnelle Regressionstests liest tests/analysis/analyze_saved_testfeatures.py direkt vorberechnete .npy-Dateien aus testvideos_features/ ein.
 
Da das ressourcenintensive Video-Dekodieren und die MediaPipe-Berechnung entfallen, liefert das Werkzeug dieselbe detaillierte biomechanische Kennzahlen- und Fehleranalyse für Hunderte Sequenzen in unter einer Sekunde.
 
 
27. Automatisierte Unit-Tests
 
In tests/unit/ sind zwei automatisierte Testmodule hinterlegt, die isolierte Kernfunktionen verifizieren:
 
* test_pipeline_unit.py:
  Prüft den FrameSampler (deterministische Skalierung von z. B. 30 oder 150 Frames auf exakt 90 Frames) sowie die Formvalidierung des LandmarkNormalizers (Abweisung von Arrays mit unpassender Featuredimension).
* test_domain_and_config:
  Stellt sicher, dass die globalen Dimensionen (TARGET_FRAMES = 90, FEATURES_PER_FRAME = 105, HAND_FEATURE_DIMS = 63) konsistent definiert sind und validiert die saubere Instanziierung sowie Serialisierung von PredictionResult.
 
 
28. Logging und Hilfsfunktionen
 
Das Modul app/utils.py stellt mit setup_logger() eine standardisierte Logging-Infrastruktur bereit.
 
Fehler bei unvollständigen Videodaten, abweichenden Array-Dimensionen oder nicht erreichbaren Dateien werden im Backend sauber abgefangen, mit aussagekräftigen Protokolleinträgen versehen und über standardisierte HTTP-Fehlercodes (z. B. 400 oder 500) an den Client kommuniziert.
 
 
29. Schnittstellenkontrakt zwischen Client und Server
 
Die Kommunikation zwischen Flutter-Frontend und FastAPI-Backend folgt einem schlanken, klar definierten Vertrag:
 
1. Anfrage: POST /predict, Multipart-Encoding mit dem Videodatenstrom unter dem Schlüssel file.
2. Erfolgsantwort (HTTP 200 JSON):
{
  "label": "danke",
  "confidence": 0.9852
}
3. Fehlerantwort: Standardisierte FastAPI-Fehlermeldung (detail) bei Verbindungsabbrüchen oder unleserlichen Medienformaten.
 
 
30. Architektonische Einordnung
 
Das Backend folgt dem bewährten Prinzip der Schichtenarchitektur (Separation of Concerns):
 
Komponente:           | Datei / Modul:                        | Hauptaufgabe:
API Layer             | app/main.py, app/api/prediction.py    | HTTP-Routing, Upload-Empfang und Lifecycle-Bereinigung
Service Layer         | app/services/                         | Kapselung von Vorverarbeitung und Modellinferenz
Preprocessing         | training/preprocessing/pipeline.py    | Video-Dekodierung, Drehungskorrektur, Abtastung & Normalisierung
Feature Extraction    | mediapipe_extractor.py, model_builder | Extraktion von 105 Landmarks & Transformation in 159 Invarianten
Deep Learning         | gesture_model.keras                   | Zeitliche Klassifikation über gestapelte Bi-LSTMs und Peak-Pooling
Domain Models         | app/domain/                           | Typisierte Datenstrukturen (PredictionResult, Gesture)
Diagnostics & Tests   | tests/, training/evaluate.py          | Unit-Tests, Güteprüfung und physikalische Ursachenanalyse
 
 
31. Zusammenfassung
 
Das Python-Backend der Sign-Language-App kombiniert eine schlanke, asynchrone REST-Schnittstelle mit einer robusten Vorverarbeitungs- und Deep-Learning-Pipeline.
 
Durch die zweistufige Merkmalsextraktion – MediaPipe Holistic zur skelettbasierten Reduktion und der InvariantFeatureLayer zur mathematischen Normierung von Handgeometrie, Geschwindigkeiten und Körperrelationen – wird eine hohe Erkennungsgenauigkeit bei minimalem Trainingsaufwand erreicht.
 
Die konsequente Entkopplung von Offline-Featuregenerierung, Modelltraining, REST-Bereitstellung und Diagnosewerkzeugen gewährleistet wissenschaftliche Nachvollziehbarkeit, hohe Ausführungsgeschwindigkeit und einfache Erweiterbarkeit um weitere Gebärdenklassen.

