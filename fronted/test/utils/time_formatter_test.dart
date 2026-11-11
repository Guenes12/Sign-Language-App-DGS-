import 'package:flutter_test/flutter_test.dart';
import '../../lib/utils/time_formatter.dart';
void main() {
 group('formatTime', () {
   test('formats zero seconds', () {
     expect(formatTime(0), '00:00');
   });
   test('formats seconds below one minute', () {
     expect(formatTime(5), '00:05');
     expect(formatTime(59), '00:59');
   });
   test('formats exactly one minute', () {
     expect(formatTime(60), '01:00');
   });
   test('formats minutes and seconds', () {
     expect(formatTime(65), '01:05');
   });
   test('formats ten minutes', () {
     expect(formatTime(600), '10:00');
   });
 });
}
