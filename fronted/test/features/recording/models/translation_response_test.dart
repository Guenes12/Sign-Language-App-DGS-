import 'package:flutter_test/flutter_test.dart';
import '../../../../lib/features/recording/models/translation_response.dart';
void main() {
 group('TranslationResponse.fromJson', () {
   test('creates response from valid JSON', () {
     final response = TranslationResponse.fromJson({
       'label': 'Hallo',
       'confidence': 0.95,
     });
     expect(response.label, 'Hallo');
     expect(response.confidence, 0.95);
   });
   test('converts integer confidence to double', () {
     final response = TranslationResponse.fromJson({
       'label': 'Danke',
       'confidence': 1,
     });
     expect(response.label, 'Danke');
     expect(response.confidence, 1.0);
   });
   test('uses default values for missing fields', () {
     final response = TranslationResponse.fromJson({});
     expect(response.label, '');
     expect(response.confidence, 0.0);
   });
 });
}
