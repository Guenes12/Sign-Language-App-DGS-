# Lastenheft (Anforderungskatalog aus Anwendersicht)



1. **Zielsetzung des Projekts**

• 1.1 Projektname: Gebärdensprachen-Erkennungs-App (Arbeitstitel)

• 1.2 Vision: Eine mobile Anwendung zu entwickeln, die es Nutzern ermöglicht, Gebärdensprache über die Handykamera aufzunehmen und in Text zu transkribieren, um die Kommunikation zu erleichtern 	      und die Inklusion zu fördern.

• 1.3 Projektziel (MVP): Eine funktionierende mobile Anwendung zu erstellen, die in der Lage ist, 20 spezifische Gebärden (Wörter) über die Handykamera zu erkennen und diese in Text umzuwandeln.



**2. Anwendungsbereich und Zielgruppe**

• 2.1 Anwendungsbereich:

 	o Erkennung von Gebärdensprache in Echtzeit (oder nahezu Echtzeit) über die Smartphone-Kamera.

 	o Unterstützung beim Erlernen von Gebärdensprache.

 	o Erleichterung der Kommunikation zwischen Gehörlosen/Hörgeschädigten und Hörenden.

• 2.2 Zielgruppe:

 	o Personen, die Gebärdensprache lernen möchten.

 	o Gehörlose oder hörgeschädigte Personen, die ihre Gebärden in Text umwandeln möchten.

 	o Hörende Personen, die mit Gebärdensprache kommunizieren möchten.

 	o Pädagogen und Lehrende im Bereich Gebärdensprache.



**3. Funktionale Anforderungen (Was die App können soll)**

• 3.1 Gebärdenaufnahme (Prio: Sehr Hoch)

 	o Die App muss in der Lage sein, Videos von Gebärden über die integrierte Smartphone-Kamera aufzunehmen.

 	o Die Aufnahme muss manuell durch den Nutzer gestartet und gestoppt werden können.

 	o Die App soll visuelles Feedback während der Aufnahme geben (z.B. "Aufnahme läuft").

• 3.2 Gebärdenanalyse und -erkennung (Prio: Sehr Hoch)

 	o Die App muss die aufgenommenen Gebärdenvideos analysieren können.

 	o Die App muss in der Lage sein, die 20 trainierten Gebärden (Wörter) zu erkennen.

 	o Nach der Erkennung soll das erkannte Wort als Text angezeigt werden.

 	o Die Erkennung soll möglichst schnell erfolgen (nahezu Echtzeit oder innerhalb weniger Sekunden nach 	 	 	Aufnahmeende).

• 3.3 Anzeige der Erkennungsergebnisse (Prio: Hoch)

 	o Das erkannte Wort soll klar und deutlich auf dem Bildschirm angezeigt werden.

 	o Bei Unsicherheit der Erkennung soll die App dies anzeigen können (z.B. "Erkennung unsicher" oder Top-3-	Ergebnisse).

• 3.4 Benutzerfreundliche Oberfläche (Prio: Hoch)

 	o Die Benutzeroberfläche soll intuitiv sein – Buttons sollen groß genug und beschriftet sein.

 	o Klare Anweisungen zur Nutzung der Kamera und zur Gebärdenaufnahme.

• 3.5 Datenverwaltung der Trainingsvideos (Intern, Prio: Mittel)

 	o Die App soll die Möglichkeit bieten, die 20 Referenzvideos (für das Training) intern zu verwalten. (Dies ist 	eher eine Entwickleranforderung, aber wichtig für die spätere Wartung).



**4. Nicht-funktionale Anforderungen (Wie die App sein soll)**

• 4.1 Performance (Prio: Hoch)

 	o Die App soll flüssig und reaktionsschnell laufen.

 	o Die Erkennungszeit pro Gebärde soll minimal sein.

• 4.2 Zuverlässigkeit (Prio: Hoch)

 	o Die Gebärdenerkennung soll eine hohe Trefferquote für die trainierten Gebärden aufweisen.

 	o Die App soll stabil laufen und nicht abstürzen.

• 4.3 Benutzerfreundlichkeit (Prio: Hoch)

 	o Einfache und intuitive Bedienung (Anweisungen sollen klar und verständlich sein).

 	o Klares Design.

• 4.4 Skalierbarkeit (Prio: Mittel)

 	o Die Architektur der App und des neuronalen Netzes sollte so gewählt werden, dass später weitere Gebärden und Funktionen hinzugefügt werden können.

• 4.5 Sicherheit (Prio: Gering für MVP, aber wichtig für Zukunft)

 	o Datenschutz: Aufgenommene Videos werden nur lokal verarbeitet und nicht ohne explizite Zustimmung des Nutzers hochgeladen oder geteilt.

• 4.6 Kompatibilität (Prio: Hoch)

 	o Die App soll auf gängigen Android- und iOS-Smartphones lauffähig sein.

• 4.7 Wartbarkeit (Prio: Mittel)

 	o Der Code soll gut strukturiert und kommentiert sein, um zukünftige Erweiterungen und Fehlerbehebungen zu erleichtern.

 

**5. Technische Rahmenbedingungen**

• 5.1 Entwicklungsumgebung: Flutter (Dart).

• 5.2 Kamera-Zugriff: Nutzung der nativen Kamerafunktionen des Smartphones.

• 5.3 KI/ML-Framework: TensorFlow Lite (oder ähnliches, das auf mobilen Geräten läuft).

• 5.4 Datenformat der Videos: Gängige Videoformate, die von Smartphones unterstützt werden (z.B. MP4).





# Pflichtenheft (Realisierungskonzept aus Entwicklersicht)



1. **Architekturübersicht**

• 1.1 Client (Flutter App):

 	o Benutzeroberfläche (UI) für Kameraaufnahme und Ergebnisanzeige.

 	o Kameramodul für Videoaufnahme.

 	o Modul zur Vorverarbeitung der Videodaten.

 	o Integration des trainierten neuronalen Netzes (TensorFlow Lite Modell).

 	o Anzeigemodul für die Erkennungsergebnisse.

• 1.2 Backend (Optional, für MVP nicht zwingend): Für das MVP wird kein separates Backend benötigt, da die Erkennung lokal auf dem Gerät stattfindet. Später könnte ein Backend für Modell-Updates oder komplexere Analysen in Betracht gezogen werden.



**2. Detaillierte Beschreibung der Komponenten**

• 2.1 Benutzeroberfläche (Flutter UI)

 	o 2.1.1 Startbildschirm:

 		 Großer "Aufnahme starten"-Button.

 		 Anzeigebereich für das erkannte Wort.

 		 Optional: Statusanzeige (z.B. "Bereit zur Aufnahme").

 	o 2.1.2 Kameraansicht:

 		 Live-Vorschau der Kamera.

 		 Button zum Starten/Stoppen der Aufnahme.

 		 Visuelles Feedback während der Aufnahme (z.B. roter Rahmen, Text "Aufnahme läuft").

 	o 2.1.3 Ergebnisansicht:

 		 Große Textanzeige des erkannten Wortes.

 		 Optional: Konfidenzwert der Erkennung.

 		 Optional: Button zum erneuten Aufnehmen.

• 2.2 Kameramodul (Flutter camera package)

 	o Initialisierung der Kamera (Front- oder Rückkamera, je nach Präferenz – für Gebärden ist Frontkamera oft praktischer, da man sich selbst sieht).

 	o Konfiguration der Videoauflösung und Bildrate (fps) für optimale Erkennung bei vertretbarer Dateigröße.

 	o Starten und Stoppen der Videoaufnahme.

 	o Speichern des aufgenommenen Videos temporär auf dem Gerät.

• 2.3 Videovorverarbeitung

 	o 2.3.1 Frame-Extraktion: Extrahieren von Einzelbildern (Frames) aus dem aufgenommenen Video. Die Frequenz der Frame-Extraktion muss festgelegt werden (z.B. 5-10 Frames pro Sekunde).

 	o 2.3.2 Pose Estimation (Prio: Hoch)

 		 Verwendung eines vor-trainierten Modells zur Pose Estimation (z.B. MediaPipe Pose, OpenPose, MoveNet) um Schlüsselpunkte des Körpers (Hände, Arme, Kopf, Schultern) in jedem Frame 		zu erkennen.

 		 Extrahieren der Koordinaten dieser Schlüsselpunkte.

 	o 2.3.3 Normalisierung der Pose-Daten (Prio: Hoch)

 		 Normalisierung der Schlüsselpunkt-Koordinaten (z.B. relativ zur Körpermitte oder zur Größe des bounding box), um Variationen in der Größe und Position der Person im Bild 			auszugleichen.

 		 Optional: Glättung der Posen-Daten über die Zeit, um Rauschen zu reduzieren.

 	o 2.3.4 Sequenzbildung: Zusammenfassen der normalisierten Posen-Daten einer Gebärde zu einer Zeitreihe (Sequenz), die als Input für das neuronale Netz dient.

• 2.4 Neuronales Netz für Gebärdenerkennung (Prio: Sehr Hoch)

 	o 2.4.1 Modelltyp: Ein rekurrentes neuronales Netz (RNN) oder eine Transformer-Architektur ist für Zeitreihendaten wie Gebärden gut geeignet.

 		 Option 1 (Einfacher Start): Long Short-Term Memory (LSTM) oder Gated Recurrent Unit (GRU) Netz. 

 	o 2.4.2 Input-Layer: Nimmt die sequenziellen Posen-Daten (z.B. eine Liste von 2D- oder 3D-Koordinaten der Schlüsselpunkte pro Frame über eine bestimmte Zeitdauer) entgegen.

 	o 2.4.3 Hidden Layers: Eine oder mehrere LSTM/GRU-Schichten, gefolgt von Dense-Schichten.

 	o 2.4.4 Output-Layer: Eine Dense-Schicht mit Softmax-Aktivierung, die so viele Neuronen hat, wie es zu erkennende Gebärden (Wörter) gibt (in diesem Fall 20).

 	o 2.4.5 Training:

 		 Trainingsdaten: Die 20 Videos pro Wort. Wichtig ist, dass man pro Wort mehrere Aufnahmen hat, um Variationen abzudecken (z.B. 10-20 Aufnahmen pro Wort von verschiedenen Personen 		oder aus leicht unterschiedlichen Winkeln).

 		 Datenaugmentation: Techniken wie leichte Rotationen, Skalierungen, Verschiebungen oder Änderungen der Geschwindigkeit der Gebärden können angewendet werden, um die 				Trainingsdaten zu erweitern und das Modell robuster zu machen.

 		 Verlustfunktion: Categorical Cross-Entropy.

 		 Metriken: Accuracy, Precision, Recall, F1-Score.

 	o 2.4.6 Modellkonvertierung: Das trainierte Modell (z.B. in Keras/TensorFlow) muss in das TensorFlow Lite-Format konvertiert werden, damit es effizient auf mobilen Geräten ausgeführt 		werden kann.

• 2.5 Integration des TensorFlow Lite Modells (Flutter tflite\_flutter package)

 	o Laden des .tflite-Modells in die App.

 	o Ausführen von Inferenzen mit den vorverarbeiteten Gebärden-Sequenzen.

 	o Verarbeiten der Ausgaben des Modells (Wahrscheinlichkeiten für jedes Wort).

• 2.6 Ergebnisanzeige o Auswahl des Wortes mit der höchsten Wahrscheinlichkeit.

 	o Anzeige des Wortes auf der UI. o Optional: Implementierung einer "Schwellenwert"-Logik: Wenn die höchste Wahrscheinlichkeit unter einem 	bestimmten Wert liegt, wird "Unbekannte 	Gebärde" oder "Erkennung unsicher" angezeigt.



**3. Testkonzept**

• 3.1 Unit-Tests: Für einzelne Funktionen (z.B. Videovorverarbeitung, Modell-Inferenz).

• 3.2 Integrationstests: Testen des Zusammenspiels der Module (z.B. Kameraaufnahme -> Vorverarbeitung -> Erkennung).

• 3.3 End-to-End-Tests: Vollständiger Test des Workflows von der Aufnahme bis zur Anzeige des Ergebnisses.

• 3.4 Akzeptanztests: Überprüfung, ob die App die im Lastenheft definierten Anforderungen erfüllt, insbesondere die Erkennungsgenauigkeit der 20 Wörter.

• 3.5 Performance-Tests: Messung der Erkennungsgeschwindigkeit und des Ressourcenverbrauchs auf verschiedenen Geräten.



**4. Rollout-Plan (MVP)**

• 4.1 Interne Tests: Testen der App durch das Entwicklungsteam.

• 4.2 Alpha-Tests: Testen durch eine kleine Gruppe von ausgewählten Nutzern.

• 4.3 Beta-Tests (optional): Testen durch eine größere Gruppe von Early Adoptern.

• 4.4 Veröffentlichung: Deployment in den Google Play Store und Apple App Store (oder nur lokal für den Anfang).



**5. Offene Punkte und Risiken**

• 5.1 Datenqualität der Trainingsvideos: Die Qualität und Varianz der 20 Videos ist entscheidend für die Performance des Modells. Sind die Videos aus verschiedenen Blickwinkeln, mit unterschiedlichen Lichtverhältnissen, von verschiedenen Personen?

• 5.2 Komplexität der Gebärden: Manche Gebärden sind komplexer und schwerer zu unterscheiden als andere.

• 5.3 Rechenleistung auf mobilen Geräten: Pose Estimation und neuronale Netze können rechenintensiv sein. Optimierung ist hier wichtig.

• 5.4 Auswahl des Pose-Estimation-Modells: Welches Modell liefert die besten Ergebnisse für Gebärden und ist gleichzeitig performant genug für mobile Geräte?

• 5.5 Overfitting: Das Modell könnte zu stark auf die 20 Videos trainiert werden und bei neuen Aufnahmen schlecht performen. Datenaugmentation und Validierungsdaten sind hier wichtig.

