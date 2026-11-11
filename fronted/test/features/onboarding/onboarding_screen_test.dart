import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:fronted/features/home/home_screen.dart';
import 'package:fronted/features/onboarding/onboarding_screen.dart';

void main() {

  testWidgets('OnboardingScreen zeigt die erste Seite', (

    WidgetTester tester,

  ) async {

    await tester.pumpWidget(

      const MaterialApp(

        home: OnboardingScreen(),

      ),

    );

    expect(

      find.text('Willkommen 👋'),

      findsOneWidget,

    );

    expect(

      find.text(

        'Mit der Sign-App kannst du Gebärdensprache automatisch '

        'in Text übersetzen.',

      ),

      findsOneWidget,

    );

  });

  testWidgets('OnboardingScreen zeigt Weiter-Button', (

    WidgetTester tester,

  ) async {

    await tester.pumpWidget(

      const MaterialApp(

        home: OnboardingScreen(),

      ),

    );

    expect(

      find.text('Weiter'),

      findsOneWidget,

    );

  });

  testWidgets('OnboardingScreen zeigt Überspringen-Button', (

    WidgetTester tester,

  ) async {

    await tester.pumpWidget(

      const MaterialApp(

        home: OnboardingScreen(),

      ),

    );

    expect(

      find.text('Überspringen'),

      findsOneWidget,

    );

  });

  testWidgets('Weiter zeigt die nächste Seite', (

    WidgetTester tester,

  ) async {

    await tester.pumpWidget(

      const MaterialApp(

        home: OnboardingScreen(),

      ),

    );

    await tester.tap(find.text('Weiter'));

    await tester.pumpAndSettle();

    expect(

      find.text('Aufnahme starten 🎥'),

      findsOneWidget,

    );

  });

  testWidgets('Überspringen öffnet HomeScreen', (

    WidgetTester tester,

  ) async {

    await tester.pumpWidget(

      MaterialApp(

        home: const OnboardingScreen(),

        routes: {

          '/home': (_) => const HomeScreen(),

        },

      ),

    );

    await tester.tap(find.text('Überspringen'));

    await tester.pumpAndSettle();

    expect(

      find.byType(HomeScreen),

      findsOneWidget,

    );

  });

  testWidgets('Onboarding kann mehrere Seiten durchlaufen', (

    WidgetTester tester,

  ) async {

    await tester.pumpWidget(

      const MaterialApp(

        home: OnboardingScreen(),

      ),

    );

    for (int i = 0; i < 3; i++) {

      await tester.tap(find.text('Weiter'));

      await tester.pumpAndSettle();

    }

    expect(

      find.text('Aufnahmedauer ⏱️'),

      findsOneWidget,

    );

  });

}
 