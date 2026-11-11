import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:sign_app/features/home/home_screen.dart';

void main() {
 testWidgets('HomeScreen zeigt die Begrüßung', (
   WidgetTester tester,
 ) async {
   await tester.pumpWidget(
     const MaterialApp(
       home: HomeScreen(),
     ),
   );
   expect(
     find.text('Willkommen zur Sign-App'),
     findsOneWidget,
   );
 });
 testWidgets('HomeScreen zeigt die Beschreibung', (
   WidgetTester tester,
 ) async {
   await tester.pumpWidget(
     const MaterialApp(
       home: HomeScreen(),
     ),
   );
   expect(
     find.text(
       'Übersetze Gebärdensprache automatisch '
       'in verständlichen Text.',
     ),
     findsOneWidget,
   );
 });
 testWidgets('HomeScreen zeigt Anleitung und Übersetzungsbutton', (
   WidgetTester tester,
 ) async {
   await tester.pumpWidget(
     const MaterialApp(
       home: HomeScreen(),
     ),
   );
   expect(find.text('Anleitung'), findsOneWidget);
   expect(find.text('Zum Übersetzen'), findsOneWidget);
 });
 testWidgets('Anleitung öffnet OnboardingScreen', (
   WidgetTester tester,
 ) async {
   await tester.pumpWidget(
     const MaterialApp(
       home: HomeScreen(),
     ),
   );
   await tester.tap(find.text('Anleitung'));
   await tester.pumpAndSettle();
   expect(
     find.text('Willkommen 👋'),
     findsOneWidget,
   );
 });
}