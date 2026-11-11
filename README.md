# Sign-Language-App(DGS)

Die **SignLanguageApp** ist ein mobiles Assistenzsystem zur videobasierten Erkennung von Gebärden der Deutschen Gebärdensprache (DGS), das im Rahmen einer Bachelorarbeit entwickelt wurde. 

Das System verbindet eine benutzerfreundliche Smartphone-Oberfläche mit einer intelligenten Bildverarbeitungs- und Deep-Learning-Pipeline. Über die Handykamera aufgenommene Gebärden werden dabei nicht als schwere Rohvideos verarbeitet, sondern mithilfe von *MediaPipe Holistic* auf wesentliche Körperpunkte reduziert und anschließend durch ein zeitbasiertes, bidirektionales LSTM-Netzwerk präzise klassifiziert.

> **Hinweis zum Projekt:** Bei der Anwendung handelt es sich um einen experimentellen wissenschaftlichen Prototyp zur Evaluierung mobiler Erkennungsmethoden, nicht um ein zertifiziertes medizinisches oder kommerzielles Übersetzungsprodukt.

<!-- Zwei Screenshots nebeneinander: Startseite & Aufnahme/Ergebnis --><p align="center">  <img src="Dokumentation/screenshots/startseite.png" width="280" alt="Startseite der App" style="margin-right: 20px;">  <img src="Dokumentation/screenshots/aufnahme.png" width="280" alt="Aufnahme und Ergebnisanzeige"></p><p align="center">  <em>Abbildung: Startseite (links) und Aufnahme-/Ergebnisanzeige (rechts) der mobilen Anwendung.</em></p>

## Motivation

Die Verständigung zwischen gehörlosen und hörenden Menschen scheitert im Alltag häufig an Sprachbarrieren, wenn keine Gebärdensprachdolmetscher anwesend sind. Während automatische Übersetzungssysteme für Lautsprache weit verbreitet sind, gibt es für die Deutsche Gebärdensprache bisher nur wenige frei zugängliche, mobile Lösungen.


Dieses Projekt untersucht einen modularen Ansatz auf Basis von Deep-Learning- und Computer-Vision-Methoden, um eine solche Erkennung auf mobilen Endgeräten zu realisieren:
- Statt schwerer End-to-End-Videomodelle werden die Videodaten über Pose-Estimation auf anatomische Skelettkoordinaten reduziert.
- Geometrische und kinematische Invarianten (Zentrierung auf die Schultern, Skalierungsnormierung, relative Geschwindigkeiten und Abstände zum Gesicht) machen das Modell unabhängig von Körpergröße, Kameraabstand und -orientierung.
- Ein zeitbasiertes Bidirektionales LSTM klassifiziert die dynamischen Bewegungsmuster bei geringem Rechenaufwand.


Die genaue Architektur des Backends ist in [Dokumentation\Architektur_und_Codebeschreibung\Backend_Codebeschreibung.md]Dokumentation\Architektur_und_Codebeschreibung\Backend_Codebeschreibung.md dokumentiert, die mobile Benutzeroberfläche in [Dokumentation\Architektur_und_Codebeschreibung\Fronted_Codebeschreibung.md]Dokumentation\Architektur_und_Codebeschreibung\Fronted_Codebeschreibung.md.


---


## Systemüberblick

Der Benutzer zeichnet eine Gebärde mit der mobilen Flutter-App auf. Die Aufnahme wird über eine HTTP-Multipart-Schnittstelle an das FastAPI-Backend übertragen. Das Backend führt eine mehrstufige Vorverarbeitung und Merkmalsextraktion durch, übergibt die bereinigte Merkmalsmatrix an das neuronale Netz und sendet die erkannte Gebärde zusammen mit einem Konfidenzwert an das Smartphone zurück.

```text
[ Benutzer / Smartphone ]        
    │  (Zeichnet Gebärde auf)        
    ▼
[ Flutter-Frontend ]        
    │  POST /predict (HTTP-Multipart-Upload)        
    ▼
[ FastAPI-Backend ]        
    ├── 1. Frame-Dekodierung & Orientierungskorrektur (OpenCV)        
    ├── 2. Temporale Abtastung (Normierung auf 90 Zeitschritte)        
    ├── 3. Skelettextraktion (MediaPipe Holistic -> 105 Rohmerkmale)        
    ├── 4. Invarianzschicht (159 biomechanische Kennzahlen)        
    └── 5. Deep-Learning-Klassifikation (Bi-LSTM + Peak-Pooling)        
    │        
    ▼  
    JSON-Antwort: {"label": "danke", "confidence": 0.9852}                      (""beispielhaft dargestellt"")
[ Benutzeroberfläche (Ergebnisanzeige) ]
```

---

## Was das System kann

### Aufnahme & Mobile Benutzeroberfläche

Das Flutter-Frontend stellt eine zielgerichtete Benutzeroberfläche bereit:
- **Kameravorschau in Echtzeit:** Hilft bei der korrekten Positionierung von Händen, Oberkörper und Gesicht im Bildausschnitt.
- **Aufnahmesteuerung mit Timer:** Unterstützt die gezielte Aufnahme einzelner Gebärden mit visuellem Countdown und definierter Aufnahmedauer.
- **Direkte Ergebnisanzeige:** Präsentiert das erkannte Wort und die zugehörige statistische Konfidenz unmittelbar nach Eingang der Serverantwort.


### Unterstützte Gebärden (Klassen)
Der aktuelle Modellstand (gesture_model.keras) wurde auf 7 isolierte Gebärden der Deutschen Gebärdensprache trainiert und evaluiert:
- Angst
- danke
- essen
- ja
- keineAhnung
- nein
- not


### Automatische Bildkorrektur & zeitliche Normierung
Smartphones speichern Videos je nach Haltung oft mit abweichenden Rotationswinkeln ab:
- **Anatomische Lagekorrektur:** Das Backend prüft Stichprobenbilder über MediaPipe Pose auf die Lage der Schulterlinie und Kopfposition. Verdrehte Videos (0°, 90°, 180°, 270°) werden vor der Merkmalsextraktion automatisch aufrecht gedreht.
- **Gleichmäßige Zeittaktung:** Unabhängig davon, wie schnell oder langsam eine Gebärde ausgeführt wurde, tastet das System die Videosequenz linear auf exakt 90 Frames ab.

### Merkmalsextraktion & Invarianz
Um Bildrauschen und Hintergrundinformationen zu eliminieren, wird das Video auf wesentliche Landmark-Koordinaten verdichtet:
- **MediaPipe Holistic:** Extrahiert 21 Handgelenke (der dominanten Hand), 7 Oberkörperpunkte sowie 7 Punkte der Mund- und Gesichtskontur (105 Rohmerkmale pro Zeitschritt).
- **Geometrische Normalisierung:** Alle Punkte werden auf den Mittelpunkt zwischen linker und rechter Schulter zentriert und durch die Schulterbreite skaliert.
- **Biomechanische Invarianzschicht:** Ein maßgeschneiderter Keras-Layer berechnet 159 Merkmale (relative Fingerabstände, lokale Handformen, Richtungsgeschwindigkeiten und vertikale Ebenen).

### Klassifikation & Modellverwaltung
Die Sequenzklassifikation erfolgt über ein spezialisiertes neuronales Netzwerk:
- **Bidirektionale LSTMs:** Zwei gestapelte Bi-LSTM-Schichten erfassen den zeitlichen Kontext sowohl vorwärts als auch rückwärts.
- **Peak-Aware Temporal Pooling:** Kombiniert Global-Max-Pooling (zur Erfassung des prägnantesten Bewegungshöhepunkts) mit Global-Average-Pooling (Kontextinformation).- **Integrierte Metadaten:** Die Datei gesture_model.keras bündelt Modellarchitektur, trainierte Gewichte und das Klassenmapping (classes.json) in einem versionssicheren Archiv.

---

## Dokumentation & Spezifikation

Alle begleitenden Artefakte, Softwarediagramme, Spezifikationen und Prüfberichte der Bachelorarbeit sind zentral im Verzeichnis [`Dokumentation/`](Dokumentation/) hinterlegt:

| Kategorie | Dokument / Artefakt | Beschreibung | Direktlink |
| :--- | :--- | :--- | :--- |
| **Anforderungsanalyse** | **Lastenheft & Pflichtenheft** | Fachliche Anforderungen, Systemgrenzen & Kriterienkatalog | [Lastenheft.md](Dokumentation/Technischen_Anforderungen/Technischen_Dokumente/Lastenheft.md) und  [Pflichtenheft.md](Dokumentation/Technischen_Anforderungen/Technischen_Dokumente/Pflichtenheft.md)|
| **Qualitätssicherung** | **Checkliste & Abnahmetests** | Prüfprotokoll für Systemfunktionalität, Kameraschnittstelle & API | [Checkliste.md](Dokumentation/Technischen_Anforderungen/Technischen_Dokumente/Checkliste.md) |
| **Software-Architektur** | **Klassendiagramm Backend** | Domänenmodelle, Vorverarbeitungs-Pipelines & Inferenz-Dienste | [Klassendiagramm_backend.png](Dokumentation/Diagramme/Diagramme/Klassendiagramm_backend.png) |
| **Software-Architektur** | **Klassendiagramm Frontend** | Flutter-Controller, Service-Layer & UI-Zustandsverwaltung | [Klassendiagramm_frontend.png](Dokumentation/Diagramme/Diagramme/Klassendiagramm_frontend.png) |
| **Dynamik & Verhalten** | **Zustandsdiagramm** | Endlicher Automat der mobilen Aufnahme (`idle`, `recording`, `evaluating`) | [Zustandsdiagramm.png](Dokumentation/Diagramme/Diagramme/Zustandsdiagramm.png) |
| **Prozessablauf** | **Aktivitäts- / Sequenzdiagramm** | End-to-End-Datenfluss: Videoaufnahme $\rightarrow$ Normalisierung $\rightarrow$ Inferenz | [Sequenzdiagramm.png](Dokumentation/Diagramme/Diagramme/Sequenzdiagramm.png) |
| **Inbetriebnahme** | **Deployment- & Installationsleitfaden** | Anleitung für Backend-Deployment, Netzwerkkonfiguration & APK-Build | [Deployment(kompakt).png](Dokumentation/Diagramme/Diagramme/Deployment(kompakt).png) und [Deployment(detailliert).png](Dokumentation/Diagramme/Diagramme/Deployment(detailliert).png)|
| **Bedienung** | **Bedienungsanleitung** | Schritt-für-Schritt-Anleitung zur Nutzung der Anwendung | [Bedienungsanleitung.md](Dokumentation/Architektur_und_Codebeschreibung/Bedienungsanleitung.md) |
| **Code-Dokumentation** | **Backend Technische Doku** | Vollständige Modulübersicht aller 28 Python-Dateien | [Backend_Codebeschreibung.md](Dokumentation/Architektur_und_Codebeschreibung/Backend_Codebeschreibung.md) |
| **Code-Dokumentation** | **Frontend Technische Doku** | Vollständige Modulübersicht aller 11 Dart-Dateien | [Fronted_Codebeschreibung.md](Dokumentation/Architektur_und_Codebeschreibung/Fronted_Codebeschreibung.md) |

---


## Projekt- und Repository-Struktur

sign_app/
├── backend/                   # Python-FastAPI-Backend & Machine-Learning-Pipeline
│   ├── app/                   # API-Routen, Inferenz-Dienste & Konfiguration
│   ├── training/              # Vorverarbeitung, Datenlader & Modelltraining
│   ├── tests/                 # Automatisierte Unit-Tests & Diagnose-Skripte
│   ├── trained_models/        # Keras-Modell inkl. Klassen-Metadaten
│   └── requirements.txt       # Python-Paketabhängigkeiten
│├── frontend/                 # Mobiles Flutter-Frontend
│   ├── lib/                   # UI-Screens, Controller & API-Dienste
│   ├── test/                  # Automatisierte Unit- und Widget-Tests
│   └── pubspec.yaml           # Flutter-Projektkonfiguration
│├── Videos_vobereiten/        # Hilfsskript zur Datensatzaufnahme & Vorbereitung
├── Dokumentation/             # Ausführliche technische Dokumentationen & Anleitungen
└── README.md                  # Zentrale Projektübersicht


---

## Schnellstart (Installation & Ausführung)

### 1. Backend startenVoraussetzungen: 
Python 3.10 oder 3.11
1. In das Backend-Verzeichnis wechseln:   
    cd backend

2. Virtuelle Umgebung erstellen und aktivieren:   
    python -m venv venv   
- Unter Windows:     
    venv\Scripts\activate   
- Unter macOS/Linux:     
    source venv/bin/activate

3. Abhängigkeiten installieren:   
    pip install -r requirements.txt

4. Server starten:   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

Das Backend läuft anschließend unter http://localhost:8000. Die interaktive API-Dokumentation (Swagger UI) ist unter http://localhost:8000/docs abrufbar.

### 2. Frontend ausführen
Voraussetzungen: Installiertes Flutter-SDK
1. In das Frontend-Verzeichnis wechseln:   
    cd frontend

2. Abhängigkeiten herunterladen:   
    flutter pub get

3. Lokale Server-IP in lib/config/app_config.dart eintragen:   
    static const String baseUrl = 'http://<DEINE-LOKALE-IP>:8000';

4. Anwendung auf Smartphone oder Emulator starten:   
    flutter run

---

## Testausführung
Die logischen Komponenten und Datenstrukturen werden über automatisierte Tests abgesichert:
### Backend-Tests
Überprüft Sequenzdimensionen, Normalisierungslogik und Datenklassen:
- Befehl (ausgeführt im Ordner backend):  
    python -m pytest tests/unit/ -v

### Frontend-Tests
Prüft JSON-Deserialisierung, Zeitformatierung und Oberflächenelemente:
- Befehl (ausgeführt im Ordner frontend):  
    flutter test
    
---

## Haftungsausschluss (Disclaimer)
Diese Software ist ein experimenteller Prototyp, der im Rahmen einer Projektarbeit entwickelt wurde. Sie ist nicht für den Einsatz in sicherheitskritischen Bereichen, im Notfall oder als medizinisches Hilfsmittel geprüft oder zertifiziert. Die Erkennungsgenauigkeit hängt von Umgebungsbedingungen wie Beleuchtung, Kameraabstand und Bewegungsausführung ab.

---

## 
LizenzDieses Projekt wurde zu akademischen Zwecken erstellt.