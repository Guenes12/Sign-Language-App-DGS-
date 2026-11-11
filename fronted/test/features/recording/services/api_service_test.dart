import 'dart:io';
import 'package:camera/camera.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'package:sign_app/features/recording/services/api_service.dart';
void main() {
 late Directory tempDirectory;
 late File testVideo;
 setUp(() async {
   tempDirectory = await Directory.systemTemp.createTemp(
     'sign_app_api_test',
   );
   testVideo = File('${tempDirectory.path}/test_video.mp4');
   await testVideo.writeAsBytes([
     0,
     1,
     2,
     3,
   ]);
 });
 tearDown(() async {
   if (await tempDirectory.exists()) {
     await tempDirectory.delete(recursive: true);
   }
 });
 group('ApiService', () {
   test('sendVideo verarbeitet eine erfolgreiche Serverantwort', () async {
     final client = MockClient((request) async {
       return http.Response(
         '{"label":"Hallo","confidence":0.95}',
         200,
         headers: {
           'content-type': 'application/json',
         },
       );
     });
     final apiService = ApiService(client: client);
     final result = await apiService.sendVideo(
       XFile(testVideo.path),
     );
     expect(result, isNotNull);
     expect(result!.label, 'Hallo');
     expect(result.confidence, 0.95);
     apiService.dispose();
   });
   test('sendVideo gibt null bei HTTP-Fehler zurück', () async {
     final client = MockClient((request) async {
       return http.Response(
         'Server Error',
         500,
       );
     });
     final apiService = ApiService(client: client);
     final result = await apiService.sendVideo(
       XFile(testVideo.path),
     );
     expect(result, isNull);
     apiService.dispose();
   });
   test('sendVideo gibt null bei ungültiger JSON-Antwort zurück', () async {
     final client = MockClient((request) async {
       return http.Response(
         'Das ist kein JSON',
         200,
       );
     });
     final apiService = ApiService(client: client);
     final result = await apiService.sendVideo(
       XFile(testVideo.path),
     );
     expect(result, isNull);
     apiService.dispose();
   });
   test('sendVideo sendet eine Datei an den Server', () async {
     bool requestReceived = false;
     final client = MockClient((request) async {
       requestReceived = true;
       return http.Response(
         '{"label":"Danke","confidence":0.87}',
         200,
       );
     });
     final apiService = ApiService(client: client);
     final result = await apiService.sendVideo(
       XFile(testVideo.path),
     );
     expect(requestReceived, true);
     expect(result, isNotNull);
     expect(result!.label, 'Danke');
     expect(result.confidence, 0.87);
     apiService.dispose();
   });
 });
}