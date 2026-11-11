#### Entwicklung einer KI-gestützten App zur Echtzeit-Übersetzung von Gebärdensprache in Text unter Verwendung von MediaPipe und Sign-Whisper-German





###### Bereich 1: Computer Vision \& Sensorik

###### Titel: „Echtzeit-Feature-Extraktion und Normalisierung von Gebärden-Landmarks mittels MediaPipe“



**Kernaufgaben:**

* Input-Pipeline: Implementierung des Video-Streamings und Frame-Processing mittels OpenCV.
* Landmark-Detection: Konfiguration der MediaPipe Holistic-Pipeline zur stabilen Erfassung von Händen, Pose (Oberkörper) und Gesicht.
* Data Preprocessing: Entwicklung mathematischer Algorithmen zur Normalisierung (Skalierung der Koordinaten unabhängig von der Kameraposition) und Rauschunterdrückung (Smoothing der Zitterbewegungen).
* Sequenzmanagement: Aufbau eines Buffers, der die Frames sammelt (z. B. 30 FPS) und für das Modell als konsistenter Tensor bereitstellt.
* Frontend \& UI: Design der Benutzeroberfläche (Kamera-Preview, Overlay der Keypoints, Anzeige des übersetzten Textes).









###### Bereich 2: Deep Learning \& NLP

###### Titel: „Integration und Optimierung eines Transformer-basierten Modells zur sequentiellen Gebärden-Text-Übersetzung“



**Kernaufgaben:**

* Modell-Architektur: Einbindung von Sign-Whisper-German (Hugging Face Transformers).
* Inferenz-Logik: Entwicklung der Logik zur Verarbeitung der Sequenzen (Sliding Window Ansatz), damit die Übersetzung während des Gebärdens flüssig erscheint.
* NLP-Postprocessing: Implementierung des Tokenizers und Dekoders, um die numerischen Vorhersagen in grammatikalisch korrekte deutsche Sätze zu wandeln.
* Performance-Optimierung: Untersuchung von Quantisierung (z. B. INT8) oder Modellschnitt (Pruning), um die Latenz der Übersetzung zu minimieren.
* Evaluation: Messung der Übersetzungsgenauigkeit (z.B. BLEU-Score oder Word Error Rate) basierend auf Testsequenzen.

