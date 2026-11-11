import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_tts/flutter_tts.dart';
import 'package:fronted/features/recording/models/translation_response.dart';
import 'package:fronted/features/recording/recording_controller.dart';
import 'package:fronted/features/recording/recording_screen.dart';
import 'package:fronted/features/recording/services/api_service.dart';
import 'package:fronted/features/recording/services/camera_service.dart';

class FakeCameraService extends CameraService {
 @override
 bool get isReady => true;
 @override
 Widget get preview => const ColoredBox(
       color: Colors.black,
       child: SizedBox.expand(),
     );
 @override
 Future<void> init() async {}
 @override
 Future<void> startRecording() async {}
 @override
 Future<XFile?> stopRecording() async {
   return XFile('test_video.mp4');
 }
 @override
 Future<void> switchCamera() async {}
 @override
 Future<void> dispose() async {}
}
class FakeApiService extends ApiService {
 @override
 Future<TranslationResponse?> sendVideo(XFile file) async {
   return TranslationResponse(
     label: 'Hallo',
     confidence: 0.95,
   );
 }
 @override
 void dispose() {}
}
class FakeFlutterTts extends FlutterTts {
 @override
 Future<dynamic> setLanguage(String language) async {}
 @override
 Future<dynamic> setSpeechRate(double rate) async {}
 @override
 Future<dynamic> speak(
   String text, {
   bool focus = false,
 }) async {}
 @override
 Future<dynamic> stop() async {}
}
void main() {
 TestWidgetsFlutterBinding.ensureInitialized();
 late RecordingController controller;
 setUp(() {
   controller = RecordingController(
     cameraService: FakeCameraService(),
     apiService: FakeApiService(),
     tts: FakeFlutterTts(),
   );
 });

 testWidgets('RecordingScreen zeigt den Titel SIGN-APP', (
   WidgetTester tester,
 ) async {
   await tester.pumpWidget(
     MaterialApp(
       home: RecordingScreen(
         controller: controller,
       ),
     ),
   );
   await tester.pump();
   expect(find.text('SIGN-APP'), findsOneWidget);
 });
 testWidgets('RecordingScreen zeigt den Aufnahme-Button', (
   WidgetTester tester,
 ) async {
   await tester.pumpWidget(
     MaterialApp(
       home: RecordingScreen(
         controller: controller,
       ),
     ),
   );
   await tester.pump();
   expect(find.byIcon(Icons.play_arrow), findsOneWidget);
 });
 testWidgets('RecordingScreen zeigt Kamerawechsel-Button', (
   WidgetTester tester,
 ) async {
   await tester.pumpWidget(
     MaterialApp(
       home: RecordingScreen(
         controller: controller,
       ),
     ),
   );
   await tester.pump();
   expect(find.byIcon(Icons.cameraswitch), findsOneWidget);
 });
 testWidgets('RecordingScreen zeigt Home-Button', (
   WidgetTester tester,
 ) async {
   await tester.pumpWidget(
     MaterialApp(
       home: RecordingScreen(
         controller: controller,
       ),
     ),
   );
   await tester.pump();
   expect(find.byIcon(Icons.home), findsOneWidget);
 });
 testWidgets('RecordingScreen zeigt Bereit Status', (
   WidgetTester tester,
 ) async {
   await tester.pumpWidget(
     MaterialApp(
       home: RecordingScreen(
         controller: controller,
       ),
     ),
   );
   await tester.pump();
   expect(find.text('Bereit'), findsOneWidget);
 });
 testWidgets('RecordingScreen startet Aufnahme beim Drücken des Buttons', (
   WidgetTester tester,
 ) async {
   await tester.pumpWidget(
     MaterialApp(
       home: RecordingScreen(
         controller: controller,
       ),
     ),
   );
   await tester.pump();
   await tester.tap(find.byIcon(Icons.play_arrow));
   await tester.pump();
   expect(controller.isRecording, true);
   expect(find.byIcon(Icons.stop), findsOneWidget);
 });
 testWidgets('RecordingScreen zeigt Übersetzung und Sicherheit', (
   WidgetTester tester,
 ) async {
   controller.translatedText = 'Hallo';
   controller.confidence = 0.95;
   await tester.pumpWidget(
     MaterialApp(
       home: RecordingScreen(
         controller: controller,
       ),
     ),
   );
   await tester.pump();
   expect(find.text('Hallo'), findsOneWidget);
   expect(find.text('Sicherheit: 95.0 %'), findsOneWidget);
   expect(find.text('Vorlesen'), findsOneWidget);
 });
}