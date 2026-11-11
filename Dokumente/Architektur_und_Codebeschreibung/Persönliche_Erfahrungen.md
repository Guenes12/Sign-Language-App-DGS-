#### &#x09;Dokumentation der Entwicklung der Sign-Language-App



&#x09;	Projekt: Sign-Language-App(DGS)

&#x09;				Autor: Semanur 




Dieses Dokument fasst die praktischen Erfahrungen, die aufgetretenen Herausforderungen und die gefundenen Lösungsansätze zusammen, die während der Entwicklung des Gebärdensprach-Übersetzungsmodells auf Basis eines Long Short-Term Memory (LSTM)-Netzwerks gesammelt wurden. Das Ziel bestand darin, ein Modell zu trainieren, das Gebärden aus Videomaterial erkennen und übersetzen kann. Dabei zeigte sich, dass nicht nur die Datenerfassung und das Training, sondern auch die sorgfältige Evaluierung mit unabhängigen Testdaten, die zugrundeliegende Datenverarbeitungsarchitektur sowie eine klare Benutzerführung entscheidend für den Erfolg sind.


1. Datenerfassung und -aufbereitung: Die Basis für ein erfolgreiches Training

Die Qualität und Quantität der Trainingsdaten sind entscheidend für die Leistungsfähigkeit jedes maschinellen Lernmodells. Im Rahmen dieses Projekts stellte die Erstellung eines geeigneten Datensatzes eine der größten Herausforderungen dar.


1.1. Anfängliche Annahmen und erste Hürden:

Zu Beginn stand die Annahme im Raum, dass für die Erkennung einfacher Gebärden wie „Ja“ und „Nein“, für die man nur eine Hand für die Gebärde braucht, eine fokussierte Videoaufnahme der Hand komplett ausreichen würde, um das Modell zu trainieren.

Problemstellung: Es stellte sich jedoch heraus, dass die für die Feature-Extraktion verwendete mediapipe-Bibliothek eine umfassendere Sicht auf die gebärdende Person benötigt. Um eine präzise und konsistente Extraktion der relevanten Gelenkpunkte und Körperhaltungen zu gewährleisten, musste man den gesamten Oberkörper und den Kopf der Person im Video sehen. Eine eingeschränkte Perspektive führte zu unzureichenden oder fehlerhaften Extraktionen, was das Modelltraining erheblich erschwerte.


1.2. Herausforderungen bei der Datensatz-Erweiterung und -Diversifizierung:

Um genügend Trainingsmaterial für jede Gebärde generieren zu können, wurden verschiedene Ansätze verfolgt, die jeweils eigene Schwierigkeiten mit sich brachten.

- Ansatz A: Manuelle Videoaufnahme und automatisierte Manipulation mittels ffmpeg und Batch-Dateien
  -  Ziel: Eigene Videos unter kontrollierten Bedingungen aufnehmen und diese anschließend automatisiert manipulieren, um den Datensatz zu erweitern und zu diversifizieren.
  - Umsetzung (erste Phase): Zunächst wurden Videos manuell aufgenommen. Um den Datensatz zu erweitern, wurde eine Batch-Datei mit ffmpeg genutzt, um aus diesen Originalvideos modifizierte Versionen zu erstellen. In dieser frühen Phase wurden auch Varianten mit künstlich hinzugefügtem Rauschen erzeugt.
  - Problemstellung der ersten Phase:
    - Rauschen: Das künstlich hinzugefügte Rauschen, obwohl zur Erhöhung der Robustheit gedacht, verschlechterte die Qualität der mediapipe-Extraktion ziemlich drastisch. Die Algorithmen hatten Schwierigkeiten, in verrauschten Bildern präzise Gelenkpunkte zu identifizieren, was zu fehlerhaften Features und einem ineffektiven Training führte.
    - Geringe Diversität: Obwohl die Videos modifiziert wurden, basierten sie alle auf einem einzigen Ausgangsvideo, was die tatsächliche Varianz im Datensatz nur begrenzt erhöhte und das Modell anfällig für Overfitting auf spezifische Ausgangsbedingungen machte.
  - Umsetzung (verbesserte Phase): Basierend auf diesen Erkenntnissen wurde die Batch-Datei angepasst. Anstatt Rauschen hinzuzufügen, lag der Fokus auf realistischeren Variationen wie leichten Änderungen der Lichtverhältnisse, subtilen Schattenwürfen und geringfügigen Beschnitten. Dies ermöglichte es, die Diversität zu erhöhen, ohne die Qualität der Feature-Extraktion zu beeinträchtigen.

- Ansatz B: Manuelle Videoaufnahme mit einfachen Mitteln (anfängliche Herausforderungen)
  - Ziel: Eigene Videos unter kontrollierteren, aber einfachen Bedingungen aufzunehmen, um die Qualität der Features zu verbessern und eine bessere Basis für die Augmentierung zu schaffen.
  - Umsetzung: Es wurde versucht, die Videos aufzunehmen, indem das Smartphone auf das Bett abgelegt wurde.
  - Problemstellung:
    - Perspektive: Die improvisierte Kamerapositionierung führte jedoch oft zu suboptimalen Perspektiven. Eine ungünstige Perspektive kann die Sichtbarkeit wichtiger Körperteile einschränken und die mediapipe-Extraktion beeinträchtigen, selbst wenn der gesamte Oberkörper theoretisch sichtbar ist. Dies erschwerte ebenfalls ein effektives Training des Modells.

- Ansatz C: Diversifizierung durch unterschiedliche Aufnahmegeräte
  - Problemstellung: Anfänglich wurden die Trainingsvideos hauptsächlich mit einem iPhone aufgenommen, während die App auf einem Samsung-Smartphone getestet wurde. Dies führte zu einer suboptimalen Unterscheidung bei der Erkennung von Gebärden wie „Ja“ und „Nein“, da das Modell möglicherweise auf gerätespezifische Bildeigenschaften trainiert war.
  - Lösungsansatz: Um die Generalisierungsfähigkeit des Modells zu verbessern, wurden zusätzlich pro Wort je 8 Trainingsvideos mit dem Samsung-Smartphone aufgenommen. Diese Videos wurden dann ebenfalls mit der angepassten Batch-Datei extrahiert und dem Datensatz hinzugefügt. Bei diesen Aufnahmen wurde bewusst darauf geachtet, sowohl Szenarien mit gut sichtbarem Oberkörper und Gesicht als auch solche mit leichten Abschnitten zu integrieren, um das Modell robuster gegenüber unterschiedlichen Bildausschnitten zu machen.
  - Vorteile: Das Modell lernt, Gebärden unabhängig von den spezifischen Kameraeigenschaften eines Geräts zu erkennen, was die Anwendbarkeit in der Praxis erheblich verbessert.



2. Architekturänderungen, effizientes Datenmanagement und Benutzerführung

Im Laufe des Projekts wurde die Architektur der Datenverarbeitung angepasst, um die Effizienz zu steigern, den Datenschutz zu gewährleisten und die Weitergabe des Codes zu erleichtern. Zudem wurde die Benutzerführung optimiert, um die Qualität der Datenaufnahme zu verbessern.


2.1. Umstellung der Datenverarbeitung für Trainingsdaten:

Anfangs wurden die aufgenommenen Videos direkt und dauerhaft gespeichert. Dies führte zu großen Datenmengen und potenziellen Problemen bei der Weitergabe des Codes, da die Rohvideos  persönliche Informationen enthalten.
- Lösungsansatz: Die Architektur wurde so umgestellt, dass die Videos für das Training zuerst von mediapipe extrahiert und dann als .npy-Dateien gespeichert werden.
- Vorteile:
  - Effizienz: Die Feature-Extraktion muss nur einmal durchgeführt werden. Das Modell kann dann direkt mit den vorbereiteten .npy-Dateien trainiert werden, was den Trainingsprozess beschleunigt.
  - Datenschutz: Die Rohvideos müssen nicht dauerhaft gespeichert oder weitergegeben werden. Nur die anonymisierten Gelenkpunkt-Daten (.npy-Dateien) sind für das Training relevant.
  - Code-Weitergabe: Wenn der Code weitergegeben werden soll, müssen nicht die sensiblen Videodateien mitgeliefert werden, sondern nur die wesentlich kleineren und unkritischeren .npy-Dateien.


2.2. Temporäre Verarbeitung von Live- und Testvideos:

Ähnlich wie bei den Trainingsdaten wurde auch der Umgang mit Videos, die live über das Smartphone aufgenommen oder für Testzwecke verwendet werden, optimiert.
- Lösungsansatz: Videos, die über das Smartphone aufgenommen werden, werden jetzt nur temporär gespeichert. Dasselbe gilt für Testvideos. Sie werden direkt von mediapipe extrahiert, die extrahierten Features werden dann dem Modell zur Übersetzung übergeben, und die Originalvideos können anschließend gelöscht werden.
- Vorteile: Minimierung des Speicherbedarfs und weitere Verbesserung des Datenschutzes, da keine unnötigen Videodateien auf dem System verbleiben.


2.3. Integration einer Anleitung in die App (Flutter):

Anfangs fehlte eine direkte Erklärung innerhalb der App zur Bedienung der Videoaufnahme. Dies könnte zu Unsicherheiten beim ersten Start führen.
- Lösungsansatz: Um den Benutzer bei den ersten Schritten zu begleiten, wurde eine kompakte Anleitung direkt in die Flutter-App integriert. Diese Anleitung führt durch die grundlegende Bedienung der App und erklärt, wie die Aufnahme gestartet und beendet wird, wie zwischen Front- und Rückkamera gewechselt werden kann und wie das Übersetzungsergebnis angezeigt wird.
- Vorteile:
  - Erhöhte Benutzerfreundlichkeit: Die Anleitung führt Schritt für Schritt durch die Bedienung und reduziert anfängliche Unsicherheiten bei der Nutzung der App.
  - Klare Abläufe: Der Benutzer weiß direkt, wie die Aufnahme über den Button gesteuert wird und wo das Ergebnis erscheint.


2.4. Herausforderungen bei der Bibliothekskompatibilität:

Während der Entwicklung traten wiederkehrende Probleme mit der Kompatibilität der verwendeten Python-Bibliotheken auf.
- Problemstellung: Ein einfaches pip install führte oft zu Versionen, die nicht miteinander harmonisierten oder unerwartete Fehler verursachten. Insbesondere die Interaktion zwischen TensorFlow, Keras, Mediapipe und anderen Abhängigkeiten erforderte spezifische Versionen, um eine stabile und funktionierende Entwicklungsumgebung zu gewährleisten.
- Lösungsansatz: Die passenden Versionen der Bibliotheken mussten manuell recherchiert und installiert werden, um Konflikte zu vermeiden. Dies beinhaltete oft das Erstellen einer virtuellen Umgebung und das schrittweise Testen verschiedener Versionskombinationen, bis eine stabile Konfiguration gefunden wurde.
- Erkenntnis: Die genaue Spezifikation und Verwaltung von Bibliotheksversionen (z. B. mittels requirements.txt) ist für die Reproduzierbarkeit und Stabilität des Projekts unerlässlich und sollte von Anfang an berücksichtigt werden.



3. Chronologische Problemlösung: Von der Skalierung über die Lagekorrektur bis zur Fingerabstandsanalyse

Nachdem das Grundmodell für die drei ursprünglichen Basisgebärden („ja“, „nein“, „keineAhnung“) funktionierte, bestand der nächste Schritt darin, das Vokabular auf 7 alltagsrelevante Klassen zu erweitern („ja“, „nein“, „keineAhnung“, „essen“, „danke“, „Angst“, „not“).
Hierbei stellte sich die Frage, warum die Erkennung bei den ersten drei Wörtern zunächst funktionierte, bei der Erweiterung auf sieben Wörter jedoch gravierende Fehler auftraten:
Bei den ersten drei Gebärden („ja“, „nein“, „keineAhnung“) lagen die Handbewegungen räumlich und dynamisch noch sehr weit auseinander: „nein“ zeichnet sich durch eine klare horizontale Seitwärtsbewegung aus, „ja“ durch das Abknicken der Hand nach vorne, und „keineAhnung“ findet oben an der Schläfe bzw. Stirn statt. Durch diese deutlichen Zonenunterschiede konnte das Modell die drei Gesten anfangs noch trennen.
Mit den zusätzlichen Gebärden kamen jedoch Gesten hinzu, die sich in denselben Raumbereichen abspielen: Vor allem „essen“ (Handbewegung zum Mund) liegt räumlich extrem nah am Kopfbereich von „keineAhnung“. Ebenso bewegen sich „danke“ (vom Kinn nach vorne) und „Angst“ (vor der Brust) in eng benachbarten Zonen. Hierbei kam es zu massiven Verwechslungen, insbesondere wurde „keineAhnung“ dauerhaft als „essen“ vorhergesagt.
Die folgenden Abschnitte beschreiben die genaue zeitliche Abfolge der Schritte und Versuche zur Lösung dieses Problems:


3.1. Schritt 1: Systematische Reduktion der Klassenanzahl (7 → 6 → 5 → 4 Wörter)

- Hypothese: Die erste Vermutung war, dass das Modell schlichtweg mit der Anzahl von 7 Klassen überfordert war und die Entscheidungsgrenzen nicht mehr sauber trennen konnte.
- Durchführung: Um dies zu überprüfen, wurde der Datensatz schrittweise reduziert:
  Es wurde jeweils eine Gebärde entfernt und das Modell mit 6 Klassen trainiert.
  Da die Verwechslungen unverändert blieben, wurde weiter auf 5 Klassen und schließlich auf nur noch 4 Klassen reduziert.
- Erkenntnis: Auch bei nur 4 Klassen blieben die Fehlklassifikationen bestehen. Damit war empirisch belegt, dass die reine Wortanzahl nicht die Ursache des Problems war. Die Ursache lag tiefer im System.


3.2. Schritt 2: Lösungsversuch durch Erhöhung von Frames und Features (Gescheitert)

- Lösungsversuch: Bevor das Orientierungsproblem entdeckt wurde, wurde versucht, die Erkennung dadurch zu verbessern, dass die Anzahl der abgetasteten Frames sowie die extrahierten Features im Modell erhöht wurden (noch ohne den späteren Invarianz-Layer).
- Ergebnis: Dieser Versuch brachte keine Besserung und schlug fehl.
- Grund des Scheiterns: Wie sich kurz darauf herausstellte, lag das Problem nicht an einer zu geringen Datenmenge, sondern daran, dass die Videos im Hintergrund durch die OpenCV-Verarbeitung auf dem Kopf stehend verarbeitet wurden. Eine höhere Anzahl an Frames und Features lieferte bei invertierten Bildern lediglich noch mehr verkehrte Koordinaten.


3.3. Schritt 3: Das Diskrepanz-Rätsel zwischen Trainings- und Live-Videos (Metadaten-Flag vs. OpenCV-Matrix)

- Problemstellung: Bei den Tests mit der mobilen Flutter-App (bei der durchgehend dasselbe Smartphone genutzt wurde) blieben die Erkennungsergebnisse zunächst unbrauchbar. Dies erschien widersprüchlich, da die mit demselben Smartphone aufgenommenen Trainingsdaten im Offline-Training zuvor funktioniert hatten. Um der Ursache auf den Grund zu gehen, wurde das sofortige Löschen der empfangenen Live-Videos deaktiviert und die Dateien zur manuellen Sichtprüfung in einem temporären Ordner gespeichert.
Das Paradoxon bei der Sichtprüfung: Wurden die temporär gespeicherten Videodateien in einem normalen Mediaplayer geöffnet, wurden sie völlig aufrecht und normal abgespielt. Dennoch schlug die Vorhersage im Backend fehl.

- Die technische Ursachenanalyse:
  - Warum die Trainingsdaten funktionierten: Die Trainingsvideos wurden vor der Extraktion über FFmpeg-Skripte verarbeitet (z. B. für Zuschnitte und Augmentierung). FFmpeg wertet das interne MP4-Orientierungs-Flag des Smartphones standardmäßig aus und dreht die Rohpixel beim Enkodieren physisch fest um. MediaPipe erhielt folglich stets physisch aufrechte Pixel-Matrizen.
  - Warum die Live-Videos aus Flutter fehlschlugen: Das Kamera-Plugin von Flutter streamt die Rohdaten des Kamerasensors direkt in den MP4-Container. Viele Smartphone-Sensoren zeichnen das Bild hardwareseitig jedoch um 180° gedreht auf und hinterlegen die Drehung lediglich als logisches Metadaten-Tag (rotate=180) im Datei-Header. Mediaplayer lesen dieses Tag aus und zeigen das Video aufrecht an. Wird das Video im Backend jedoch über OpenCV (cv2.VideoCapture) Bild für Bild eingelesen, ignoriert OpenCV diese Metadaten standardmäßig und liest stur das ungedrehte Roh-Pixel-Array ein.
  - Die Auswirkung auf MediaPipe: Während die Trainingsdaten aufrecht waren, stand die Person in den Live-Streams für MediaPipe buchstäblich kopfüber (Nase unten, Hände oben). Während dies bei den drei ursprünglichen Gesten noch nicht die volle Zerstörung der Klassifikation bedeutete, kollabierte die Erkennung bei Gesten mit feinen Körperbezugspunkten vollständig.
  - Die nachhaltige Lösung: Im Backend wurde ein automatisches Orientierungsmodul (VideoOrientationCorrector) vorgeschaltet. Anhand der Landmark-Koordinaten der ersten Frames prüft das Modul anatomisch, ob der Y-Wert der Nase unterhalb der Schultern oder Hüfte liegt (Y=0 ist der obere Bildrand). Ist das der Fall, wendet OpenCV vor der Feature-Extraktion automatisch eine 180°-Rotation (cv2.ROTATE_180) an.
  - Erster großer Zwischenerfolg: Sobald die Live-Videos garantiert denselben physisch aufrechten Zustand aufwiesen wie die Trainingsdaten, stieg die Erkennungsgenauigkeit des Modells schlagartig auf rund 60 %. Das Grundgerüst funktionierte nun, allerdings reichte die Trennschärfe für ähnliche Handbewegungen noch nicht aus.

3.4. Schritt 4: Detaillierte Modellierung der Fingerabstände

Um die verbleibenden Verwechslungen bei den 60 % (insbesondere zwischen „keineAhnung“ und „essen“) zu lösen, wurde intensiv an der exakten Differenzierung der Hand- und Fingerkonfigurationen gearbeitet:
  - Problemstellung: Zuvor wurden primär grobe Handgelenkpunkte betrachtet. Da sich bei beiden Gesten die Hand im oberen Kopf- bzw. Gesichtsbereich befindet, reichten die Handgelenkkoordinaten nicht aus. Dem Modell fehlte die Information darüber, wie die Finger geformt sind und wo sich die Fingerspitzen relativ zum Gesicht befinden.
  - Intensive Arbeit an den Fingerabständen: In mehreren Schritten wurde die Extraktion auf alle 21 Fingergelenke pro Hand erweitert und ein geometrisches Abstandsmodell erarbeitet:
    - Relative Fingerabstände (Handform): Berechnung der euklidischen Distanzen der Fingerspitzen zueinander (z. B. Daumen zu Zeigefinger) sowie zur Handwurzel. Dadurch konnte das Modell mathematisch exakt zwischen einer flachen Hand, einer Faust oder einer Zangenform unterscheiden.
    - Fingerspitzen-zu-Gesicht-Distanzen: Berechnung der kontinuierlichen Vektoren von den Fingerspitzen direkt zum Mundzentrum und zur Nase.
  - Ergebnis: Nähert sich die Fingerspitze dem Mund bis auf wenige Zentimeter an, erkennt das Modell zweifelsfrei die Geste „essen“. Verbleibt die Hand an der Stirn/Schläfe, ohne Mundannäherung, wird verlässlich „keineAhnung“ klassifiziert.


3.5. Schritt 5: Der finale Durchbruch durch den InvariantFeatureLayer (159 Merkmale → 98 % Genauigkeit)

- Umsetzung: Die berechneten Fingerdistanzen, die relativen Abstände zu den Gesichts- und Schulterankern sowie die zeitlichen Geschwindigkeitsableitungen (Δx,Δy,Δz) wurden in einem Keras-eigenen InvariantFeatureLayer gebündelt. Dieser überführt die 105 normierten Eingangslandmarks in 159 deterministische, physikalische Merkmale.
- Finales Ergebnis: Durch diesen Schritt sprang die Erkennungsrate von den zuvor erreichten 60 % auf hervorragende 98,00 % Gesamtgenauigkeit über 350 unabhängige Testsequenzen. Sowohl „keineAhnung“ als auch „essen“ erreichten im finalen Testdatensatz einen perfekten Recall von 100 %.

4. Erkenntnisse und Empfehlungen für die Weiterentwicklung

Basierend auf den gesamten gesammelten Erfahrungen lassen sich folgende Kernempfehlungen für zukünftige Entwicklungen festhalten:
- Umfang des Trainingsdatensatzes: Es wurde festgestellt, dass 50 Videos pro Gebärde für ein robustes Training nicht ausreichen. Für eine zuverlässige Erkennung sind mindestens 150–200 Videos pro Gebärde anzustreben, um eine ausreichende Varianz und Generalisierungsfähigkeit des Modells zu gewährleisten.
- Begrenzung der Videolänge:
  - Für die App-Aufnahme: Um zu verhindern, dass der Benutzer die Aufnahme versehentlich zu lange laufen lässt und unnötig große Dateien entstehen, wurde die Videolänge bei der Aufnahme durch die App auf maximal 10 Sekunden begrenzt. Dies sorgt für eine effiziente Datenerfassung und eine bessere Benutzererfahrung.
  - Für Trainingsvideos: Es wurde zudem versucht, die Länge der Trainingsvideos auf maximal 7 Sekunden zu begrenzen. Diese Homogenisierung der Videolängen erleichtert es dem Modell, Muster und Ähnlichkeiten in den Gebärden effektiver zu erkennen und zu lernen.
  - Hochwertige und konsistente Datenerfassung priorisieren: Es ist entscheidend, Zeit in die Aufnahme von qualitativ hochwertigen Originalvideos zu investieren:
  - Vollständige Sichtbarkeit: Sicherstellen, dass der gesamte Oberkörper und der Kopf der gebärdenden Person stets gut sichtbar sind.
  - Optimale Perspektive: Eine Kameraposition wählen, die eine klare und unverzerrte Sicht auf die Gebärden ermöglicht. Ein Stativ oder eine feste Halterung kann hierbei sehr hilfreich sein.
  - Gleichmäßige Lichtverhältnisse: Starke Schatten oder Überbelichtung vermeiden, da dies die Feature-Extraktion negativ beeinflussen kann.
  - Vorsicht bei Datensatz-Augmentierung: Techniken zur Datensatz-Erweiterung (Augmentierung) können nützlich sein, sollten aber mit Bedacht eingesetzt werden:
    - Rauschen: Das Hinzufügen von Rauschen, das die Qualität der Feature-Extraktion beeinträchtigt, sollte vermieden werden.
    - Realistische Augmentierungen: Der Fokus sollte auf Augmentierungen liegen, die realistische Variationen der Gebärden widerspiegeln (z. B. leichte Positionsverschiebungen, geringfügige Größenänderungen, natürliche Helligkeitsanpassungen).
- Diversifizierung der Trainingsbedingungen: Um das Modell auch für andere Personen und unterschiedliche Umgebungen zu trainieren, hat sich gezeigt, dass eine Variation der Aufnahmebedingungen unerlässlich ist:
  - Anfangsphase (Basis-Training): Die ersten ca. 50 Videos pro Gebärde sollten idealerweise unter kontrollierten Bedingungen aufgenommen werden, z. B. mit einem einfachen Hintergrund und konstanter Beleuchtung. Dies hilft dem Modell, die Kernmerkmale der Gebärde sauber zu lernen.
  - Erweiterungsphase (Robustheitstraining): Danach sollte man bewusst die Kleidung, den Hintergrund und die Lichtverhältnisse variieren. Zusätzlich ist die Einbeziehung weiterer Personen (z. B. durch Aufnahmen von Familienmitgliedern) entscheidend, um zu verhindern, dass das Modell nur auf die Merkmale einer einzelnen Person spezialisiert ist.
- Unabhängige und vielfältige Testdaten: Eine zentrale Erkenntnis ist, dass Testvideos immer separat von den Trainingsvideos aufgenommen und variiert werden müssen. Es ist nicht zielführend, dieselben Videos oder nur leicht modifizierte Versionen der Trainingsdaten zum Testen zu verwenden. Für eine aussagekräftige Bewertung sollte man:
  - Neue Videos aufnehmen, die das Modell noch nie verarbeitet hat.
  - Variationen einbauen bezüglich Kleidung, Hintergründen, Lichtverhältnissen und Personen.
  - Tests durch Dritte einbeziehen, um objektives Feedback zur Benutzerfreundlichkeit und Generalisierung zu erhalten.
- Aussagekräftige Metriken zur Evaluierung: Um die Genauigkeit und Leistung des Modells objektiv zu bewerten, ist es unerlässlich, relevante Metriken wie Accuracy, Precision, Recall und F1-Score auszugeben und zu interpretieren. Ein reines „es funktioniert“ ist nicht ausreichend; die Zahlen geben Aufschluss darüber, wie gut das Modell tatsächlich ist und wo es noch Schwächen hat.
- Iterative Überprüfung der Feature-Extraktion: Eine regelmäßige Überprüfung der Qualität der mediapipe-Extraktionen auf den Trainings- und Testdaten ist essenziell. Die Visualisierung der extrahierten Punkte kann helfen, frühzeitig Probleme zu erkennen und die Datenerfassung oder Vorverarbeitung anzupassen.



Fazit
Die Entwicklung eines Gebärdensprach-Übersetzungsmodells ist ein komplexes Unterfangen, bei dem die Qualität und Quantität der Trainingsdaten, die Validität der Testdaten, eine durchdachte Datenverarbeitungsarchitektur, die effiziente Handhabung der Videolängen, eine klare Benutzerführung und die Beachtung von Bibliothekskompatibilitäten eine zentrale Rolle spielen.
Die anfänglichen Herausforderungen bei der Datenerfassung, der methodische Test über das schrittweise Reduzieren der Klassen (von 7 auf 6, 5 und 4 Wörter), der zunächst gescheiterte Versuch über die reine Erhöhung von Frames und Features, die Aufdeckung der Diskrepanz zwischen FFmpeg-Verarbeitung und OpenCV-Metadaten-Ignorierung sowie die anschließende serverseitige Lagekorrektur (VideoOrientationCorrector, Sprung auf ca. 60 %) und schließlich die detaillierte mathematische Modellierung der relativen Finger- und Mundabstände im InvariantFeatureLayer (Sprung auf 98,00 %) zeichnen einen Entwicklungsprozess nach. Das Projekt belegt, dass nicht blindes Ausprobieren oder das bloße Vergrößern neuronaler Netze, sondern physikalisch und geometrisch fundierte Vorverarbeitungsschritte der Schlüssel zu robuster Gebärdenspracherkennung sind.

&#x20;

