# \*\*Roadmap für zukünftige Erweiterungen der Gebärdensprachen-Erkennung\*\*







Diese Roadmap ist in Prioritätsstufen unterteilt, um einen iterativen und sinnvollen Entwicklungspfad zu gewährleisten.







#### \\### \\\*\\\*Priorität 1: Unmittelbare Verbesserungen \\\& Benutzerfreundlichkeit (Nach MVP)\\\*\\\*





Diese Erweiterungen konzentrieren sich darauf, die Kernfunktionalität zu verbessern und die Benutzererfahrung nach dem erfolgreichen MVP zu optimieren.





**\\#### \\\*\\\*1.1 Erweiterung des Wortschatzes\\\*\\\***



\\\*   \\\*\\\*Beschreibung:\\\*\\\* Das Hinzufügen weiterer Einzelwörter zum Erkennungssystem. Dies ist der logische nächste Schritt nach dem MVP.



\\\*   \\\*\\\*Technische Schritte:\\\*\\\*

&nbsp;	  \\\*   \\\*\\\*Datensammlung:\\\*\\\* Erfassen von Trainingsvideos für jedes neue Wort (mindestens 5-10 pro Wort, idealerweise mehr).



&nbsp;	  \\\*   \\\*\\\*Datenverarbeitung:\\\*\\\* Extraktion und Normalisierung der Posen-Keypoints für die neuen Videos, wie bereits im MVP etabliert.



&nbsp;	  \\\*   \\\*\\\*Modelltraining:\\\*\\\* Retraining des bestehenden LSTM/GRU-Modells mit dem erweiterten Datensatz. Die `NUM\\\_CLASSES` im Output-Layer des Modells muss entsprechend angepasst werden.



&nbsp;         \\\*   \\\*\\\*Modellkonvertierung:\\\*\\\* Erneute Konvertierung des trainierten Modells in das `.tflite`-Format.

&nbsp;	  \\\*   \\\*\\\*App-Update:\\\*\\\* Aktualisierung der `labels`-Liste in der Flutter-App und Bereitstellung des neuen `.tflite`-Modells.



\\\*   \\\*\\\*Herausforderungen:\\\*\\\* Skalierung der Datenmenge, mögliche Verwechslungen zwischen ähnlichen Gebärden, längere Trainingszeiten.



\\\*   \\\*\\\*Vorteile:\\\*\\\* Erhöht den praktischen Nutzen der App erheblich.







**\\#### \\\*\\\*1.2 Sprachliche Ausgabe (Text-to-Speech)\\\*\\\***



\\\*   \\\*\\\*Beschreibung:\\\*\\\* Das erkannte Wort wird nicht nur als Text angezeigt, sondern auch vom Gerät vorgelesen.



\\\*   \\\*\\\*Technische Schritte:\\\*\\\*



&nbsp;	   \\\*   \\\*\\\*Flutter-Integration:\\\*\\\* Verwendung eines Flutter-Plugins für Text-to-Speech (z.B. `flutter\\\_tts`).

&nbsp;	   \\\*   \\\*\\\*Implementierung:\\\*\\\* Nach erfolgreicher Erkennung eines Wortes wird der Text an das TTS-Plugin übergeben und vorgelesen.



&nbsp;	   \\\*   \\\*\\\*Sprachauswahl:\\\*\\\* Optional: Möglichkeit zur Auswahl verschiedener Sprachen/Stimmen.



\\\*   \\\*\\\*Herausforderungen:\\\*\\\* Ggf. Latenz bei der Sprachausgabe, Verfügbarkeit von Stimmen auf verschiedenen Geräten.



\\\*   \\\*\\\*Vorteile:\\\*\\\* Verbessert die Zugänglichkeit und die Benutzererfahrung, besonders für Menschen mit Sehbehinderung oder Lernschwierigkeiten.







**\\#### \\\*\\\*1.3 Visuelles Feedback für die Gebärdenausführung\\\*\\\***



\\\*   \\\*\\\*Beschreibung:\\\*\\\* Während der Gebärdenausführung erhält der Benutzer visuelles Feedback, ob die Pose korrekt erkannt wird (z.B. durch Überlagerung der Keypoints oder farbliche Markierung).



\\\*   \\\*\\\*Technische Schritte:\\\*\\\*



&nbsp;	   \\\*   \\\*\\\*Echtzeit-Visualisierung:\\\*\\\* Überlagerung der von MediaPipe/ML Kit erkannten Keypoints auf dem Kamerabild in der Flutter-App.

&nbsp;	   \\\*   \\\*\\\*"Confidence"-Anzeige:\\\*\\\* Visuelle Indikatoren (z.B. Farbcodes, Fortschrittsbalken), die zeigen, wie sicher das Modell eine Gebärde erkennt.



\\\*   \\\*\\\*Herausforderungen:\\\*\\\* Performance (Echtzeit-Rendering), genaue Kalibrierung des Feedbacks.



\\\*   \\\*\\\*Vorteile:\\\*\\\* Hilft dem Benutzer, die Gebärden korrekt auszuführen und verbessert die Erkennungsrate.







\\---







**\\### \\\*\\\*Priorität 2: Fortgeschrittene Erkennung \\\& Interaktion\\\*\\\***







Diese Erweiterungen gehen über die Einzelworterkennung hinaus und fügen komplexere Funktionen hinzu.







\\#### \\\*\\\*2.1 Erkennung von einfachen Sätzen/Phrasen\\\*\\\*



\\\*   \\\*\\\*Beschreibung:\\\*\\\* Das System kann eine Abfolge von Gebärden als zusammenhängenden Satz interpretieren.



\\\*   \\\*\\\*Technische Schritte:\\\*\\\*



&nbsp;	  \\\*   \\\*\\\*Modell-Anpassung:\\\*\\\* Statt Einzelworterkennung könnte ein sequenzielles Modell (z.B. ein Encoder-Decoder-Modell oder ein Hidden Markov Model (HMM) über den LSTM-Outputs) verwendet werden, das die Abfolge der Einzelworterkennungen 			interpretiert.



&nbsp;	  \\\*   \\\*\\\*Grammatik-Regeln:\\\*\\\* Integration einfacher Grammatikregeln für die Gebärdensprache, um die Satzbildung zu unterstützen.



&nbsp;	  \\\*   \\\*\\\*Kontextualisierung:\\\*\\\* Berücksichtigung des Kontextes benachbarter Gebärden.



&nbsp;	  \\\*   \\\*\\\*Datensammlung:\\\*\\\* Erfassen von Trainingsdaten für ganze Sätze.



\\\*   \\\*\\\*Herausforderungen:\\\*\\\* Deutlich komplexere Modellarchitektur, exponentiell ansteigender Datenbedarf, Ambiguität in der Gebärdensprache.



\\\*   \\\*\\\*Vorteile:\\\*\\\* Ermöglicht eine natürlichere Kommunikation und erhöht den Anwendungsbereich der App erheblich.







**\\#### \\\*\\\*2.2 Unterstützung mehrerer Benutzerprofile/Anpassung\\\*\\\***



\\\*   \\\*\\\*Beschreibung:\\\*\\\* Ermöglicht es verschiedenen Benutzern, die App zu nutzen, und passt die Erkennung an individuelle Gebärdenstile an.



\\\*   \\\*\\\*Technische Schritte:\\\*\\\*

&nbsp;	   \\\*   \\\*\\\*Benutzerverwaltung:\\\*\\\* Implementierung einer einfachen Benutzerverwaltung in der App.



&nbsp;	   \\\*   \\\*\\\*Modell-Personalisierung:\\\*\\\* Speichern benutzerspezifischer Modellgewichte oder Anpassung des Modells durch Transfer Learning mit benutzerspezifischen Daten.



&nbsp;	  \\\*   \\\*\\\*Cloud-Synchronisation:\\\*\\\* Optional: Speicherung von Benutzerdaten und Modellanpassungen in der Cloud.



\\\*   \\\*\\\*Herausforderungen:\\\*\\\* Datenschutz, Komplexität der Modellverwaltung, Rechenressourcen für personalisiertes Training.



\\\*   \\\*\\\*Vorteile:\\\*\\\* Erhöht die Genauigkeit für individuelle Benutzer und macht die App inklusiver.







**\\#### \\\*\\\*2.3 Feedback zur Gebärdenkorrektheit\\\*\\\***



\\\*   \\\*\\\*Beschreibung:\\\*\\\* Das System gibt dem Benutzer Feedback, ob eine Gebärde korrekt ausgeführt wurde, auch wenn sie nicht erkannt wurde. Dies könnte als Lernhilfe dienen.



\\\*   \\\*\\\*Technische Schritte:\\\*\\\*



&nbsp;	   \\\*   \\\*\\\*Referenzmodelle:\\\*\\\* Speicherung von Referenz-Posen-Sequenzen für jede Gebärde.



&nbsp;	   \\\*   \\\*\\\*Ähnlichkeitsmetriken:\\\*\\\* Vergleich der ausgeführten Gebärde mit den Referenzmodellen (z.B. Dynamic Time Warping (DTW) oder Cosinus-Ähnlichkeit).



&nbsp;	  \\\*   \\\*\\\*Visuelles Feedback:\\\*\\\* Hervorhebung von Abweichungen (z.B. "Hand zu tief", "Bewegung zu schnell").



\\\*   \\\*\\\*Herausforderungen:\\\*\\\* Definition von "korrekt", robuste Ähnlichkeitsmessung.



\\\*   \\\*\\\*Vorteile:\\\*\\\* Macht die App zu einem effektiven Lernwerkzeug für Gebärdensprache.









