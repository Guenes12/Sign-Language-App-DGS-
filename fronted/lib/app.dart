import 'package:flutter/material.dart';
import 'features/onboarding/onboarding_screen.dart';

class SignApp extends StatelessWidget {
 const SignApp({super.key});
 @override
 Widget build(BuildContext context) {
   return MaterialApp(
     debugShowCheckedModeBanner: false,
     home: const OnboardingScreen(),
   );
 }
}