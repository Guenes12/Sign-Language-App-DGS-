#### &#x09;		Checkliste



&#x09;	Gebärdensprach-Erkennung (MVP – iterative Entwicklung mit Teststrategie)







#### Phase 0: Flutter UI \& Architekturgrundlage



✔ Flutter Projekt initial erstellt



✔ Grundlegende App-Struktur aufgebaut (Screens, Services, Controller)



✔ RecordingScreen mit Kamera-UI implementiert



✔ CameraService zur Videoaufnahme implementiert



✔ RecordingController zur Steuerung der App-Logik erstellt



✔ Statusanzeige, Timer und Progress-Bar implementiert



✔ Aufnahmezeitbegrenzung (max. 30 Sekunden) integriert







#### Phase 1: Flutter Unit Testing (Frontend Validierung)



✔ Unit Tests für Flutter-Komponenten erstellt



✔ Validierung der UI-Zustände ohne Backend



✔ Test der Kamera-Service Logik 



👉 Ziel dieser Phase: Sicherstellen, dass die mobile Anwendung isoliert korrekt funktioniert







#### Phase 2: Videoaufnahme \& lokale Funktionstests



✔ Kameraaufnahme (Start/Stop Recording) implementiert



✔ Speicherung von Videos als temporäre Datei



✔ Kamerawechsel (Front/Back) implementiert



✔ UI Feedback (Timer, Recording Status) validiert



✔ App läuft vollständig ohne KI







#### Phase 3: Backend (FastAPI) Aufbau



✔ FastAPI Server initialisiert



✔ /translate Endpoint erstellt



✔ Video Upload implementiert



✔ temporäre Speicherung von Videos im Backend



✔ Server gibt Testantwort zurück







#### Phase 4: Flutter ↔ Backend Integration (ohne KI)



✔ API Service in Flutter implementiert



✔ Verbindung Flutter → FastAPI hergestellt



✔ Video erfolgreich an Server übertragen



✔ Server bestätigt Empfang der Daten



✔ Rückgabe eines Test-Strings in der App angezeigt



✔ End-to-End Kommunikation stabil getestet



👉 WICHTIGER MEILENSTEIN: Erste vollständige Systemintegration ohne KI-Modell







#### Phase 5: MediaPipe Integration (Backend)



✔ MediaPipe Holistic im Backend integriert



✔ Extraktion von Hand- und Pose-Landmarks implementiert



✔ Frame-basierte Videoverarbeitung umgesetzt



✔ Feature-Vektoren pro Frame generiert



✔ Sequenzbildung aus Videodaten implementiert



✔ Standardisierung der Input-Datenstruktur (Tensor-Format)







#### Phase 6: KI-Modell Integration



✔ Integration eines vortrainierten Modells von Hugging Face



✔ Inferenzpipeline aufgebaut:



Feature Tensor → Modell → Textausgabe



✔ Tokenizer / Processor integriert



✔ JSON Response mit Textausgabe implementiert



✔ Verbindung KI → API → Flutter hergestellt







#### Phase 7: Gesamtsystemintegration (End-to-End)



✔ vollständige Pipeline getestet: Flutter → Video → FastAPI → MediaPipe → KI → Response → Flutter



✔ stabile Kommunikation zwischen allen Komponenten



✔ Fehlerfälle getestet:



* Server nicht erreichbar



* ungültige Videos



* leere Frames



✔ Latenz und Stabilität überprüft







#### Phase 8: Systemtests \& Validierung



✔ End-to-End Tests durchgeführt



✔ Flutter Unit Tests erfolgreich abgeschlossen



✔ Backend-Kommunikation validiert



✔ MediaPipe Feature Extraktion geprüft



✔ KI-Modell Ausgabe getestet



✔ Performance als MVP-tauglich bewertet



✔ 30-Sekunden Limit erfolgreich verifiziert







#### Phase 9: Architekturfinalisierung \& Erweiterbarkeit



✔ klare Trennung zwischen:



* UI (Flutter)



* Backend (FastAPI)



* KI (Transformer Modell)



✔ Vorbereitung für Cloud Deployment



✔ spätere On-Device KI möglich (optional)



✔ modulare Erweiterbarkeit sichergestellt



&#x20;

