import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_tts/flutter_tts.dart';
import '../../utils/time_formatter.dart';
import 'models/translation_response.dart';
import 'services/api_service.dart';
import 'services/camera_service.dart';

class RecordingController extends ChangeNotifier {
 final CameraService cameraService;
 final ApiService apiService;
 final FlutterTts tts;
 static const int maxSeconds = 10;
 Timer? _timer;
 int seconds = 0;
 double progress = 0.0;
 bool isRecording = false;
 bool blink = false;
 bool isLoading = false;
 String status = 'Bereit';
 String? translatedText;
 double? confidence;
 
 RecordingController({
   CameraService? cameraService,
   ApiService? apiService,
   FlutterTts? tts,
 })  : cameraService = cameraService ?? CameraService(),
       apiService = apiService ?? ApiService(),
       tts = tts ?? FlutterTts();
 bool get ready => cameraService.isReady;
 Widget get cameraPreview => cameraService.preview;
 String get formattedTime => formatTime(seconds);
 Future<void> init() async {
   try {
     await cameraService.init();
     status = 'Bereit';
     notifyListeners();
   } catch (e) {
     status = 'Kamera konnte nicht gestartet werden.';
     notifyListeners();
   }
 }
 Future<void> start() async {
   if (isRecording) {
     return;
   }
   try {
     await cameraService.startRecording();
     isRecording = true;
     status = 'Aufnahme läuft...';
     translatedText = null;
     confidence = null;
     seconds = 0;
     progress = 0.0;
     blink = false;
     notifyListeners();
     _startTimer();
   } catch (e) {
     status = 'Aufnahme konnte nicht gestartet werden.';
     notifyListeners();
   }
 }
 void _startTimer() {
   _timer?.cancel();
   _timer = Timer.periodic(
     const Duration(seconds: 1),
     (_) async {
       if (!isRecording) {
         return;
       }
       seconds++;
       blink = !blink;
       progress = seconds / maxSeconds;
       notifyListeners();
       if (seconds >= maxSeconds) {
         await stop();
       }
     },
   );
 }
 Future<void> stop() async {
   if (!isRecording) {
     return;
   }
   _timer?.cancel();
   _timer = null;
   status = 'Sende Daten...';
   isLoading = true;
   notifyListeners();
   try {
     final file = await cameraService.stopRecording();
     if (file == null) {
       status = 'Keine Aufnahme vorhanden.';
       return;
     }
     final result = await apiService.sendVideo(file);
     if (result == null) {
       translatedText = null;
       confidence = null;
       status = 'Serverfehler';
     } else {
       translatedText = result.label;
       confidence = result.confidence;
       status = 'Übersetzung erhalten';
     }
   } catch (e) {
     translatedText = null;
     confidence = null;
     status = 'Fehler bei der Verarbeitung.';
   } finally {
     isRecording = false;
     isLoading = false;
     blink = false;
     progress = 0.0;
     seconds = 0;
     notifyListeners();
   }
 }
 Future<void> switchCamera() async {
   if (isRecording) {
     return;
   }
   try {
     await cameraService.switchCamera();
     notifyListeners();
   } catch (e) {
     status = 'Kamera konnte nicht gewechselt werden.';
     notifyListeners();
   }
 }
 Future<void> speak() async {
   if (translatedText == null || translatedText!.isEmpty) {
     return;
   }
   await tts.setLanguage('de-DE');
   await tts.setSpeechRate(0.5);
   await tts.speak(translatedText!);
 }
 Color get progressColor {
   if (seconds < 5) {
     return Colors.green;
   }
   if (seconds < 7) {
     return Colors.orange;
   }
   return Colors.red;
 }
 @override
 void dispose() {
   _timer?.cancel();
   apiService.dispose();
   cameraService.dispose();
   tts.stop();
   super.dispose();
 }
}
