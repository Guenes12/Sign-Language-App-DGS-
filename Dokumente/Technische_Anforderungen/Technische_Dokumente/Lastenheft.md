
#### Lastenheft für die Sign-Language-App

&#x09;	Projekt: Sign-Language-App(DGS)

&#x09;				Autor: Semanur 



##### 1\. Zielsetzung des Projekts



###### 1.1 Projektname



Gebärdensprach-Übersetzungs-App (Arbeitstitel)





###### 1.2 Vision



Ziel des Projekts ist die Entwicklung einer mobilen Anwendung zur automatisierten Übersetzung von Gebärdensprache in Text.



Die Anwendung soll die Kommunikation zwischen gehörlosen bzw. hörgeschädigten und hörenden Personen erleichtern und einen Beitrag zur digitalen Inklusion leisten.



Die Verarbeitung erfolgt über eine serverbasierte KI-Pipeline bestehend aus:

* Flutter Mobile App
* FastAPI Backend
* MediaPipe Pose-/Hand-Tracking
* Vortrainiertes Transformer-Modell von Hugging Face





###### 1.3 Projektziel (MVP)



Das Minimum Viable Product (MVP) erfüllt folgende Kernfunktionen:

* Aufnahme von Gebärdenvideos über ein Smartphone
* Übertragung an einen KI-Server
* Analyse der Gebärden mittels KI-Modell
* Rückgabe der erkannten Übersetzung als Text





##### 2\. Anwendungsbereich und Zielgruppe



###### 2.1 Anwendungsbereich



* Gebärdensprach-Erkennung über Smartphone-Kamera
* KI-gestützte Videoanalyse
* Unterstützung beim Lernen von Gebärdensprache
* Kommunikationshilfe im Alltag





###### 2.2 Zielgruppe



* Gehörlose und hörgeschädigte Personen
* Lernende der Gebärdensprache
* Lehrkräfte und Bildungseinrichtungen
* Hörende Personen zur barrierefreien Kommunikation





##### 3\. Funktionale Anforderungen



***ID	Funktion						Priorität***

01	Videoaufnahme über Smartphone-Kamera			Sehr Hoch

02	Start/Stop der Aufnahme durch Benutzer			Sehr Hoch

03	Visuelles Feedback während der Aufnahme			Hoch

04	Übertragung des Videos an den KI-Server			Sehr Hoch

05	Verarbeitung durch KI-Modell				Sehr Hoch

06	Rückgabe der Übersetzung als Text			Sehr Hoch

07	Anzeige der Übersetzung in der App			Sehr Hoch

08	Kamerawechsel (Front-/Backkamera)			Mittel

09	Stabile Client-Server-Kommunikation			Hoch







##### 4\. Nicht-funktionale Anforderungen



***ID	Anforderung						Priorität***

01	Schnelle Verarbeitung (wenige Sekunden Latenz)		Hoch

02	Hohe Systemstabilität					Hoch

03	Intuitive Benutzeroberfläche				Hoch

04	Modulare Architektur					Hoch

05	DSGVO-konforme temporäre Verarbeitung			Hoch

06	Erweiterbarkeit für neue Modelle/Funktionen		Mittel







##### 5\. Technische Rahmenbedingungen



***Bereich*			*Technologie***

Frontend		Flutter (Dart)

Backend			FastAPI (Python)

Computer Vision		MediaPipe Holistic

KI-Modell		Transformer (Hugging Face)

Kommunikation		REST API (HTTP/JSON)

Videoformat		MP4





##### 6\. Systemabgrenzung



Nicht Bestandteil des Systems sind:

* Permanente Videospeicherung
* Benutzerkonten oder Login-Systeme
* Echtzeit-Dauerübersetzung
* Offline On-Device KI-Inferenz (Mediapipe-Extraktion in der Offline-Version nicht wie gewollt umsetzbar)





##### 7\. Abnahmekriterien



Das System gilt als erfolgreich umgesetzt, wenn:

* Videos erfolgreich aufgenommen werden
* Videos an das Backend übertragen werden
* MediaPipe-Features extrahiert werden
* Das KI-Modell eine Textausgabe generiert
* Die Übersetzung in der App angezeigt wird
* Die Kommunikation stabil funktioniert





##### 8\. Use-Case-Szenario



* Benutzer öffnet die App
* Benutzer startet die Videoaufnahme
* Gebärden werden aufgenommen
* Video wird an den Server gesendet
* KI analysiert die Gebärden
* Text wird zurückgegeben
* Ergebnis wird angezeigt

