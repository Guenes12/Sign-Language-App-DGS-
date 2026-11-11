#### Technische Dokumentation – Flutter-Frontend der Sign-Language-App

&#x09;	Projekt: Sign-Language-App(DGS)

&#x09;				Autor: Semanur 

 
Das Flutter-Frontend bildet die mobile Benutzeroberfläche der Sign-App. Die Anwendung ermöglicht es, Gebärdensprachaufnahmen über die Smartphone-Kamera aufzunehmen und zur automatisierten Verarbeitung an einen Python-Server zu übertragen.
 
Der Server analysiert das aufgenommene Video und liefert das erkannte Ergebnis zusammen mit einem Konfidenzwert zurück. Das Flutter-Frontend stellt diese Informationen anschließend übersichtlich dar. Zusätzlich besteht die Möglichkeit, das erkannte Ergebnis über eine Text-to-Speech-Funktion ausgeben zu lassen.
 
Der Schwerpunkt des Frontends liegt auf der intuitiven Bedienung der Anwendung, der Steuerung des Aufnahmeprozesses, der stabilen Kommunikation mit dem Server und der visuellen sowie auditiven Darstellung des Übersetzungsergebnisses.
 
 
1. Projektstruktur
 
Das Flutter-Projekt ist funktional strukturiert. Die einzelnen Bereiche befinden sich in thematisch getrennten Verzeichnissen:
 
* Home: Startseite und Einstieg in die Anwendung
* Onboarding: Interaktive Anleitung zur Bedienung der App
* Recording: Aufnahme, Verarbeitung und Anzeige der Übersetzung
* Config: Zentrale Anwendungskonfiguration
* Utils: Wiederverwendbare Hilfsfunktionen
* Test: Automatisierte Unit- und Widget-Tests
 
Das Recording-Feature enthält zusätzlich eigene Unterbereiche für Datenmodelle und technische Services.
 
Diese Struktur ermöglicht eine klare Trennung der Verantwortlichkeiten (Separation of Concerns) und erleichtert die Wartung und Erweiterbarkeit des Projekts.
 
 
2. Einstiegspunkt der Anwendung
 
Die Datei main.dart bildet den Einstiegspunkt der Flutter-Anwendung.
 
Ihre Aufgabe besteht darin, die Flutter-Engine zu initialisieren und die Anwendung zu starten. Die eigentliche Basiskonfiguration befindet sich in app.dart.
 
Dadurch bleibt der Einstiegspunkt bewusst schlank und enthält keine fachliche Anwendungslogik.
 
 
3. Anwendungskonfiguration
 
Die grundlegende Flutter-Anwendung wird in app.dart definiert.
 
Dort wird unter anderem das MaterialApp eingerichtet und festgelegt, welche Ansicht beim Start der Anwendung angezeigt wird.
 
Die Anwendung beginnt mit dem Onboarding-Bereich. Von dort aus kann der Benutzer zur eigentlichen Startseite und anschließend zur Übersetzungsfunktion gelangen.
 
 
4. Zentrale Serverkonfiguration
 
Die Netzwerkadresse des Python-Servers wird zentral in der Datei app_config.dart hinterlegt:
static const String serverIp = '<IP-ADRESSE_DES_RECHNERS>';
 
Der ApiService verwendet diese Konfiguration für die Kommunikation mit dem Server. Dadurch befindet sich die Serveradresse nicht mehrfach im Quellcode.
 
Diese Lösung erleichtert insbesondere die Anpassung der Anwendung an unterschiedliche Entwicklungsumgebungen, beispielsweise wenn sich die IP-Adresse im lokalen WLAN oder der Port des Python-Servers ändert.
 
 
5. Startseite
 
Der HomeScreen stellt den zentralen Einstiegspunkt für die Benutzerinteraktion dar.
 
Auf der Startseite werden das Logo beziehungsweise Symbol der Anwendung, eine kurze Beschreibung und zwei zentrale Funktionen dargestellt:
* Öffnen der Anleitung
* Starten der Übersetzungsfunktion
 
Die Navigation zwischen den Bereichen erfolgt deklarativ über das Flutter-Routing. Die Startseite selbst enthält keine komplexe Zustandslogik und ist deshalb ressourcenschonend als zustandsloses Widget (StatelessWidget) umgesetzt.
 
 
6. Onboarding
 
Der OnboardingScreen dient als interaktive Anleitung für neue Benutzer.
 
Die Anleitung besteht aus mehreren Seiten. Jede Seite erklärt einen bestimmten Bestandteil der Anwendung, wie beispielsweise:
* Starten einer Aufnahme
* Wechsel der Kamera (Front- und Rückkamera)
* Maximale Aufnahmedauer (10 Sekunden)
* Verarbeitung durch das KI-System im Backend
* Anzeige des Übersetzungsergebnisses und Konfidenzwerts
* Sprachausgabe (Text-to-Speech)
* Rückkehr zur Startseite
 
Die einzelnen Seiten werden über ein PageView dargestellt. Ein PageController ermöglicht das lineare Durchblättern. Zusätzlich wird der aktuelle Fortschritt über Indikatoren visualisiert. Der Benutzer kann die Anleitung schrittweise durchlaufen oder direkt überspringen.
 
 
7. RecordingScreen
 
Der RecordingScreen bildet den zentralen Funktionsbereich der Anwendung.
 
Hier werden sämtliche für die Übersetzung erforderlichen Bedienelemente zusammengeführt:
* Live-Kameravorschau
* Kamerawechsel-Schaltfläche
* Aufnahme- und Stopp-Button
* Fortschrittsanzeige und Zeiterfassung
* Statusinformationen (Bereit, Aufnahme läuft, Verarbeitung...)
* Anzeige des Übersetzungsergebnisses mit Konfidenzwert
* Vorlesefunktion (Audioausgabe)
* Navigation zurück zur Startseite
 
Die Benutzeroberfläche übernimmt dabei strikt die passive Darstellung des aktuellen Systemzustands. Die Steuerung erfolgt vollständig durch den RecordingController.
 
 
8. RecordingController
 
Der RecordingController stellt die zentrale Steuerung des Aufnahme- und Übersetzungsprozesses dar.
 
Er basiert auf ChangeNotifier und verwaltet den reaktiven Zustand des Recording-Bereichs. Zu seinen Aufgaben gehören:
* Initialisierung der Kamera-Hardware
* Starten und Beenden einer Videoaufnahme
* Verwaltung der Aufnahmedauer und Begrenzung auf maximal zehn Sekunden
* Fortlaufende Aktualisierung des Aufnahmefortschritts
* Übergabe der Videodatei an den ApiService
* Entgegennahme und Aufbereitung der Serverantwort
* Verwaltung von Lade-, Erfolgs- und Fehlerzuständen
* Wechsel der Kameraquelle
* Ansteuerung der Sprachausgabe
 
Bei Zustandsänderungen benachrichtigt der Controller die UI über notifyListeners(), woraufhin der RecordingScreen seine Darstellung gezielt neu aufbaut.
 
 
9. Zustandsverwaltung
 
Der Controller modelliert den gesamten Aufnahme- und Übersetzungszyklus über eindeutige Zustandsvariablen:
* Bereitschaft der Kamera
* Status der aktiven Aufnahme
* Vergangene Aufnahmezeit in Sekunden
* Relativer Fortschrittsbalken (0.0 bis 1.0)
* Ladeindikator während der Netzwerk- und Inferenzzeit
* Benutzerfreundliche Statusmeldungen
* Erkanntes Gestenlabel und prozentualer Konfidenzwert
 
Nach Abschluss einer Übersetzung oder bei Abbruch werden flüchtige Zustände sauber zurückgesetzt.
 
 
10. Begrenzung der Aufnahmezeit
 
Die maximale Aufnahmedauer ist auf exakt zehn Sekunden begrenzt.
 
Während der Aufnahme registriert ein periodischer Timer das Verstreichen der Zeit. Erreicht der Timer die Obergrenze von zehn Sekunden, stoppt der Controller die Aufnahme automatisch und leitet die Übertragung ein. Alternativ kann der Benutzer die Aufnahme jederzeit vorzeitig über den Stopp-Button beenden.
 
 
11. CameraService
 
Der CameraService kapselt den plattformspezifischen Zugriff auf das offizielle Flutter-Kamera-Plugin.
 
Seine Aufgaben umfassen:
* Abfragen der hardwareseitig verfügbaren Kameras
* Initialisieren des CameraControllers mit gewünschter Auflösung
* Bereitstellen des Vorschau-Streams für die UI
* Starten und Stoppen der Videodatei-Aufzeichnung
* Wechsel zwischen Front- und Hauptkamera
* Geordnete Freigabe der Kameraressourcen (dispose)
 
Durch diese Abstraktion bleibt der RecordingController frei von systemspezifischen Implementierungsdetails des Kamera-Treibers.
 
 
12. Kameravorschau
 
Die Vorschau wird über den CameraService initialisiert und als nativer Widget-Stream im RecordingScreen eingebunden.
 
Solange die Initialisierung der Hardware andauert, zeigt die Oberfläche einen Ladeindikator. Schlägt der Zugriff fehl (z. B. durch verweigerte Betriebssystem-Berechtigungen), fängt der Service dies ab und setzt eine verständliche Fehlermeldung.
 
 
13. Wechsel der Kamera
 
Sofern das Endgerät über mehrere Linsen verfügt, ermöglicht der CameraService ein Umschalten zwischen Front- und Rückkamera.
 
Der Service verwaltet den aktiven Kameraindex, gibt die aktuell laufende Instanz sauber frei und initialisiert den Sensor der gewählten Gegenkamera. Um Dateninkonsistenzen zu verhindern, ist der Kamerawechsel während einer laufenden Videoaufzeichnung softwareseitig gesperrt.
 
 
14. ApiService
 
Der ApiService ist für die Netzwerkkommunikation zwischen der mobilen Flutter-App und dem FastAPI-Server verantwortlich.
 
Nach Beendigung der Aufnahme empfängt der Service die Videodatei (als XFile bzw. temporäre Datei). Er baut eine HTTP-POST-Anfrage an den Endpunkt /predict auf und überträgt das Video als multipart/form-data unter dem Feldnamen file.
 
Nach erfolgreicher Inferenz nimmt der Service die JSON-Antwort entgegen, validiert diese und wandelt sie in ein typisiertes Datenmodell um.
 
 
15. Verarbeitung der Serverantwort
 
Die Antwort des Servers wird nur bei einem HTTP-Statuscode von 200 OK als gültig interpretiert.
 
Der empfangene JSON-Body wird geparst und in ein TranslationResponse-Objekt überführt. Tritt ein Verbindungsabbruch auf oder antwortet der Server mit einem Fehlercode (z. B. 400 oder 500), fängt der ApiService die Ausnahme ab und signalisiert dem Controller das Fehlschlagen, woraufhin dieser eine entsprechende Statusmeldung ausgibt.
 
 
16. TranslationResponse
 
Das Datenmodell TranslationResponse strukturiert die Serverantwort im Frontend:
* label: Der Klassenbezeichner der erkannten Gebärde (z. B. "danke")
* confidence: Der berechnete Konfidenzwert als Gleitkommazahl (0.0 bis 1.0)
* probabilities: Optional die Wahrscheinlichkeitsverteilung über alle Klassen 
 
Durch dieses Modell bleibt der gesamte Controller- und UI-Code strikt typisiert und unabhängig vom Roh-JSON-Format.
 
 
17. Verarbeitung des Übersetzungsergebnisses
 
Sobald der ApiService ein gültiges TranslationResponse-Objekt liefert, übernimmt der Controller das Ergebnis:
* Das Label wird als Text auf der Benutzeroberfläche präsentiert.
* Der Konfidenzwert wird zur besseren Verständlichkeit in eine prozentuale Angabe formatiert (z. B. 98.5 %).
 
Die App führt dabei selbst keine mathematische Bewertung durch, sondern spiegelt objektiv das Klassifikationsergebnis des Python-Backends wider.
 
 
18. Text-to-Speech
 
Die Sprachausgabe wird über das Plugin flutter_tts realisiert.
 
Nach einer erfolgreichen Erkennung kann der Benutzer die Audio-Ausgabe über die Schaltfläche „Vorlesen“ aktivieren. Der Controller konfiguriert das TTS-Modul auf die deutsche Sprachausgabe (de-DE) mit moderater Sprechgeschwindigkeit. Die Audio-Wiedergabe ist nur aktivierbar, wenn ein valides Übersetzungsergebnis vorliegt.
 
 
19. Fortschritts- und Statusanzeige
 
Während der Videoaufzeichnung informiert ein dynamischer Fortschrittsbalken über die verstrichene Zeit im Verhältnis zum Zehn-Sekunden-Limit. Die Farbe des Balkens wechselt mit fortschreitender Zeit, ergänzt durch einen pulsierenden roten Aufnahmeindikator.
 
Außerhalb der Aufnahme signalisieren prägnante Statustexte den Bereitschaftszustand oder den laufenden Inferenzprozess.
 
 
20. Fehlerbehandlung
 
Die Anwendung verfügt über ein mehrstufiges Fehlerbehandlungskonzept:
* Hardwarefehler: Fehlende Kameraberechtigungen oder Initialisierungsfehler werden abgefangen.
* Dateifehler: Beschädigte oder leere Videoaufnahmen werden vor dem Upload erkannt.
* Netzwerkfehler: Timeouts oder Serverausfälle führen nicht zum Absturz der App, sondern zu aussagekräftigen Hinweistexten ("Server nicht erreichbar").
 
 
21. Zentrale Zeitformatierung
 
Die Formatierung von Zeiteinheiten ist in ein separates Utility-Modul (time_formatter.dart) ausgelagert.
 
Die Funktion rechnet verstrichene Sekunden in das benutzerfreundliche Format MM:SS um. Diese Auslagerung verhindert Codeduplizierung und ermöglicht isolierte Unit-Tests der Datums- und Zeitlogik.
 
 
22. Dependency Injection
 
Zur Steigerung der Testbarkeit unterstützt der RecordingController die Injektion seiner Kernabhängigkeiten über den Konstruktor:
* CameraService
* ApiService
* FlutterTts
 
Im regulären Produktivbetrieb werden die Standard-Singletons instanziiert, während automatisierte Tests kontrollierte Mocks bzw. Fakes übergeben können.
 
 
23. Testkonzept
 
Die Frontend-Qualitätssicherung stützt sich auf zwei Säulen:
* Unit-Tests: Überprüfen die reine Geschäftslogik des RecordingControllers, des ApiServices sowie der Formatierungsfunktionen ohne UI-Abhängigkeit.
* Widget-Tests: Validieren das visuelle Verhalten, die Navigationsschritte und das korrekte Reagieren der Benutzeroberfläche auf Controller-Zustände.
 
 
24. Tests des ApiService
 
Der ApiService wird unter Zuhilfenahme eines gemockten HTTP-Clients isoliert getestet.
 
Geprüfte Szenarien:
* Korrekte Extraktion von label und confidence bei HTTP 200
* Fehlerbehandlung bei HTTP-Status 500 oder 404
* Verhalten bei fehlerhaftem oder leerem JSON-Body
* Korrekter Aufbau des Multipart-Dateiuploads
 
 
25. Tests des RecordingController
 
Mithilfe simulierter Services lässt sich das Verhalten des Controllers deterministisch prüfen:
* Starten und automatisches Stoppen nach zehn Sekunden
* Zustandswechsel bei erfolgreicher Serverantwort
* Setzen definierter Fehlermeldungen bei Netzwerkunterbrechung
* Deaktivierung von Interaktionselementen während der Verarbeitung
 
 
26. Widget-Tests des HomeScreen
 
Die Startseite wird daraufhin geprüft, ob alle initialen Komponenten (Logo, Beschreibungstext, Aktionsbuttons) fehlerfrei gerendert werden und die Routen-Navigation zum Onboarding bzw. zum Recording-Bereich korrekt ausgelöst wird.
 
 
27. Widget-Tests des Onboarding
 
Für den Onboarding-Bereich wird getestet:
* Korrektes Rendern der initialen Anleitungskarte
* Weiterschalten der Seiten über Wischgesten und Vorwärts-Buttons
* Korrekte Aktualisierung der Seitenindikatoren
* Reibungslose Beendigung der Anleitung über die Überspringen-Funktion
 
 
28. Widget-Tests des RecordingScreen
 
Der RecordingScreen wird unter kontrollierten Testbedingungen ohne reale Kamera-Hardware gerendert. Über injizierte Mock-Controller wird verifiziert:
* Anzeige des Ladebalkens bei aktiver Verarbeitung
* Korrekte Darstellung des erkannten Labels und Konfidenzwerts
* Sichtbarkeit und Klickbarkeit des Vorlese-Buttons bei vorhandenem Ergebnis
 
 
29. Umgang mit Flutter-Plugins in Tests
 
Da Plugins wie camera und flutter_tts native Schnittstellen des Betriebssystems aufrufen, wird in den Testsuiten das TestWidgetsFlutterBinding initialisiert und native Plattform-Kanäle durch standardisierte Methoden-Mocks ersetzt. Dies verhindert Testabstürze durch fehlende native Gerätetreiber.
 
 
30. Ressourcenverwaltung
 
Um Speicherlecks (Memory Leaks) auf dem Smartphone zu vermeiden, implementiert der Recording-Bereich eine konsequente Freigabe:
* Der periodische Aufnahmetimer wird bei Verlassen des Screens invalidiert.
* Der Hardware-Kamerastream wird über cameraController.dispose() freigegeben.
* Laufende TTS-Audioausgaben werden gestoppt.
 
 
31. Ablauf einer Übersetzung
 
Der durchgängige Anwendungsfall gliedert sich in folgende Schritte:
1. Initialisierung: Beim Betreten des Screens wird die Kamera vorbereitet und die Vorschau gestartet.
2. Aufnahmestart: Der Benutzer betätigt den Aufnahme-Button; Timer und Fortschrittsanzeige starten.
3. Aufnahme: Die Gebärde wird vor der Kamera ausgeführt (maximal zehn Sekunden).
4. Aufnahmestopp: Der Benutzer stoppt manuell oder der Timer beendet die Aufnahme automatisch.
5. Upload: Der ApiService sendet das Video als Multipart-POST an das Python-Backend.
6. Inferenz: Das Backend führt Merkmalsextraktion und Modellklassifikation durch.
7. Antwort: Die App empfängt das JSON-Ergebnis mit Label und Konfidenz.
8. Visualisierung: Der RecordingScreen stellt das erkannte Wort und die Erkennungsgenauigkeit dar.
9. Vorlesen: Der Benutzer kann sich das Ergebnis über die TTS-Sprachausgabe akustisch vorlesen lassen.
 
 
32. Architektonische Einordnung
 
Die mobile Anwendung folgt einer klaren Schichtenarchitektur:
 
Komponente:           | Aufgabe:
HomeScreen            | Startseite und Anwendungsnavigation
OnboardingScreen      | Interaktive Schritt-für-Schritt-Bedienungsanleitung
RecordingScreen       | Benutzeroberfläche für Aufnahme und Ergebnisdarstellung
RecordingController   | Zustandssteuerung und Ablauflogik
CameraService         | Kapselung der Kamera-Hardwarefunktionen
ApiService            | REST-Kommunikation mit dem Python-Backend
TranslationResponse   | Typisiertes Datenmodell für die Klassifikationsantwort
AppConfig             | Zentrale Netzwerk- und Anwendungskonfiguration
time_formatter        | Wiederverwendbare Zeitformatierungslogik
 
 
33. Zusammenfassung
 
Das Flutter-Frontend der Sign-App zeichnet sich durch eine saubere funktionale Trennung zwischen Benutzeroberfläche, Steuerungslogik und technischen Diensten aus.
 
Durch die Kapselung hardwarenaher Funktionen in dedizierten Services und die strikte Typisierung der Netzwerkdatenmodelle bleibt die App stabil, performant und leicht wartbar. Die konsequente Unterstützung von Dependency Injection und automatisierten Unit- sowie Widget-Tests stellt eine hohe Softwarequalität sicher und bietet eine solide wissenschaftliche Basis für zukünftige funktionale Erweiterungen.