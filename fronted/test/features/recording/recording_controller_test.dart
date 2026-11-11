import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_tts/flutter_tts.dart';
import 'package:fronted/features/recording/recording_controller.dart';
import 'package:fronted/features/recording/models/translation_response.dart';
import 'package:fronted/features/recording/services/api_service.dart';
import 'package:fronted/features/recording/services/camera_service.dart';
class FakeCameraService extends CameraService {
 bool recordingStarted = false;
 bool shouldFailStart = false;
 bool shouldReturnFile = true;
 @override
 bool get isReady => true;
 @override
 Widget get preview => const SizedBox();
 @override
 Future<void> init() async {}
 @override
 Future<void> startRecording() async {
   if (shouldFailStart) {
     throw Exception('Kamera konnte nicht gestartet werden.');
   }
   recordingStarted = true;
 }
 @override
 Future<XFile?> stopRecording() async {
   if (!recordingStarted) {
     return null;
   }
   recordingStarted = false;
   if (!shouldReturnFile) {
     return null;
   }
   return XFile('test_video.mp4');
 }
 @override
 Future<void> switchCamera() async {}
 @override
 Future<void> dispose() async {}
}
class FakeApiService extends ApiService {
 TranslationResponse? response;
 bool shouldThrow = false;
 bool videoReceived = false;
 FakeApiService({this.response});
 @override
 Future<TranslationResponse?> sendVideo(XFile file) async {
   videoReceived = true;
   if (shouldThrow) {
     throw Exception('Serverfehler');
   }
   return response;
 }
 @override
 void dispose() {}
}
class FakeFlutterTts extends FlutterTts {
 bool speakCalled = false;
 String? spokenText;
 @override
 Future<dynamic> setLanguage(String language) async {}
 @override
 Future<dynamic> setSpeechRate(double rate) async {}
 @override
 Future<dynamic> speak(String text, {bool focus = false}) async {
   speakCalled = true;
   spokenText = text;
 }
 @override
 Future<dynamic> stop() async {}
}
void main() {
 TestWidgetsFlutterBinding.ensureInitialized();
 late FakeCameraService cameraService;
 late FakeApiService apiService;
 late FakeFlutterTts tts;
 late RecordingController controller;
 setUp(() {
   cameraService = FakeCameraService();
   apiService = FakeApiService();
   tts = FakeFlutterTts();
   controller = RecordingController(
     cameraService: cameraService,
     apiService: apiService,
     tts: tts,
   );
 });
 tearDown(() {
   controller.dispose();
 });
 group('RecordingController', () {
   test('hat initial korrekte Werte', () {
     expect(controller.seconds, 0);
     expect(controller.progress, 0.0);
     expect(controller.isRecording, false);
     expect(controller.isLoading, false);
     expect(controller.status, 'Bereit');
     expect(controller.translatedText, isNull);
     expect(controller.confidence, isNull);
     expect(controller.formattedTime, '00:00');
   });
   test('start startet eine Aufnahme', () async {
     await controller.start();
     expect(cameraService.recordingStarted, true);
     expect(controller.isRecording, true);
     expect(controller.status, 'Aufnahme läuft...');
     expect(controller.seconds, 0);
     expect(controller.progress, 0.0);
   });
   test('start wird ignoriert, wenn bereits aufgenommen wird', () async {
     await controller.start();
     expect(controller.isRecording, true);
     await controller.start();
     expect(controller.isRecording, true);
     expect(cameraService.recordingStarted, true);
   });
   test('start behandelt einen Kamerafehler', () async {
     cameraService.shouldFailStart = true;
     await controller.start();
     expect(controller.isRecording, false);
     expect(
       controller.status,
       'Aufnahme konnte nicht gestartet werden.',
     );
   });
   test('stop verarbeitet eine erfolgreiche Übersetzung', () async {
     apiService.response = TranslationResponse(
       label: 'Hallo',
       confidence: 0.95,
     );
     await controller.start();
     await controller.stop();
     expect(controller.isRecording, false);
     expect(controller.isLoading, false);
     expect(controller.status, 'Übersetzung erhalten');
     expect(controller.translatedText, 'Hallo');
     expect(controller.confidence, 0.95);
     expect(apiService.videoReceived, true);
     expect(controller.seconds, 0);
     expect(controller.progress, 0.0);
   });
   test('stop behandelt einen Serverfehler', () async {
     apiService.response = null;
     await controller.start();
     await controller.stop();
     expect(controller.isRecording, false);
     expect(controller.isLoading, false);
     expect(controller.status, 'Serverfehler');
     expect(controller.translatedText, isNull);
     expect(controller.confidence, isNull);
   });
   test('stop behandelt eine fehlende Aufnahme', () async {
     cameraService.shouldReturnFile = false;
     await controller.start();
     await controller.stop();
     expect(controller.isRecording, false);
     expect(controller.isLoading, false);
     expect(controller.status, 'Keine Aufnahme vorhanden.');
     expect(controller.translatedText, isNull);
     expect(controller.confidence, isNull);
   });
   test('stop behandelt einen Fehler bei der Verarbeitung', () async {
     apiService.shouldThrow = true;
     await controller.start();
     await controller.stop();
     expect(controller.isRecording, false);
     expect(controller.isLoading, false);
     expect(
       controller.status,
       'Fehler bei der Verarbeitung.',
     );
     expect(controller.translatedText, isNull);
     expect(controller.confidence, isNull);
   });
   test('stop wird ignoriert, wenn keine Aufnahme läuft', () async {
     await controller.stop();
     expect(controller.isRecording, false);
     expect(controller.isLoading, false);
     expect(controller.status, 'Bereit');
   });
   test('speak spricht die Übersetzung aus', () async {
     apiService.response = TranslationResponse(
       label: 'Danke',
       confidence: 0.90,
     );
     await controller.start();
     await controller.stop();
     await controller.speak();
     expect(tts.speakCalled, true);
     expect(tts.spokenText, 'Danke');
   });
   test('speak macht nichts ohne Übersetzung', () async {
     await controller.speak();
     expect(tts.speakCalled, false);
     expect(tts.spokenText, isNull);
   });
   test('progressColor ist anfangs grün', () {
     expect(controller.progressColor, Colors.green);
   });
   test('progressColor wird bei 5 Sekunden orange', () {
     controller.seconds = 5;
     expect(controller.progressColor, Colors.orange);
   });
   test('progressColor wird ab 7 Sekunden rot', () {
     controller.seconds = 7;
     expect(controller.progressColor, Colors.red);
   });
   test('switchCamera wird während der Aufnahme ignoriert', () async {
     await controller.start();
     await controller.switchCamera();
     expect(controller.isRecording, true);
   });
 });
}