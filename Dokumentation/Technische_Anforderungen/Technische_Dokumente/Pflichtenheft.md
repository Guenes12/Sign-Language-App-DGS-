#### Pflichtenheft für die Sign-Language-App


&#x09;	Projekt: Sign-Language-App(DGS)





##### 1\. Systemarchitektur



Das System basiert auf einer Client-Server-Architektur.





###### 1.1 Frontend (Flutter App)



Aufgaben des Frontends:

* Benutzeroberfläche
* Kameraaufnahme
* Anzeige der KI-Ergebnisse
* API-Kommunikation





###### 1.2 Backend (FastAPI Server)



Aufgaben des Backends:

* Videoempfang
* Feature-Extraktion
* KI-Inferenz
* Rückgabe der Ergebnisse





##### 2\. Systemkomponenten



###### 2.1 Flutter Frontend



Aufgaben:

* Steuerung der Kamera
* Videoaufnahme
* UI-Darstellung
* Kommunikation mit dem Backend





###### 2.2 Kameramodul



Funktionen:

* Nutzung des Flutter camera Packages
* Start/Stop der Aufnahme (Maximale Videolänge: 30s)
* Temporäre Speicherung der Videos





###### 2.3 API-Kommunikation



Funktionen:

* HTTP POST Request
* Upload des Videos
* Empfang der JSON-Response





###### 2.4 MediaPipe Feature Extraction



Funktionen:

* Nutzung von MediaPipe Holistic
* Extraktion von Hand- und Pose-Landmarks
* Umwandlung in numerische Sequenzen





###### 2.5 KI-Modell (Inference Layer)



Verwendete Technologie: Vortrainiertes Transformer-Modell von Hugging Face



Aufgaben:

* Verarbeitung der Feature-Sequenzen
* Sequenzanalyse
* Generierung einer Textausgabe





###### 2.6 Backend Pipeline



Ablauf:

* Video speichern
* MediaPipe-Analyse durchführen
* Feature-Tensor erzeugen
* KI-Modell aufrufen
* Text zurückgeben





###### 2.7 Ergebnisdarstellung



Funktionen:

* Rückgabe als JSON
* Anzeige im Flutter UI
* Dynamische UI-Aktualisierung





##### 3\. Schnittstellen



***Schnittstelle		Beschreibung***

Flutter → FastAPI	Video-Upload (HTTP POST)

FastAPI → MediaPipe	Feature Extraction

FastAPI → KI-Modell	Tensor Input

Backend → Flutter	JSON Response





##### 4\. Datenformate



***Datentyp	Format***

Video		MP4

API		JSON

Features	NumPy Tensor

Output		UTF-8 Text





##### 5\. Fehlerbehandlung



Ungültiges Video 	→ 	Fehlerresponse

Modell nicht geladen 	→ 	Serverfehler

Netzwerkfehler 		→ 	Retry möglich

Leere Frames 		→ 	Padding mit Nullen





##### 6\. Testkonzept



###### 6.1 Unit Tests



Feature Extraction

API-Methoden





###### 6.2 Integration Tests



Flutter ↔ Backend Kommunikation





###### 6.3 End-to-End Tests



Vollständige Pipeline





###### 6.4 Performance Tests



Latenzmessung der KI-Inferenz





##### 7\. Deployment



Phase		Beschreibung

Lokal		FastAPI auf Laptop

Test		Flutter + lokaler Server

Erweiterung	Cloud Deployment möglich





##### 8\. Risiken



* Netzwerkabhängigkeit
* Modell-Latenz
* Ungenaue Erkennung bei schlechter Beleuchtung
* Rechenlast des KI-Modells
* Datenschutz bei Videoübertragung

