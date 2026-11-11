import 'package:flutter/material.dart';
import '../onboarding/onboarding_screen.dart';
import '../recording/recording_screen.dart';

class HomeScreen extends StatelessWidget {
 const HomeScreen({super.key});
 @override
 Widget build(BuildContext context) {
   return Scaffold(
     backgroundColor: Colors.black,
     body: SafeArea(
       child: Center(
         child: Padding(
           padding: const EdgeInsets.symmetric(horizontal: 30),
           child: Column(
             mainAxisAlignment: MainAxisAlignment.center,
             children: [
               const Icon(
                 Icons.sign_language,
                 color: Colors.blue,
                 size: 90,
               ),
               const SizedBox(height: 30),
               const Text(
                 'Willkommen zur Sign-App',
                 textAlign: TextAlign.center,
                 style: TextStyle(
                   color: Colors.white,
                   fontSize: 30,
                   fontWeight: FontWeight.bold,
                 ),
               ),
               const SizedBox(height: 15),
               const Text(
                 'Übersetze Gebärdensprache automatisch '
                 'in verständlichen Text.',
                 textAlign: TextAlign.center,
                 style: TextStyle(
                   color: Colors.grey,
                   fontSize: 18,
                 ),
               ),
               const SizedBox(height: 50),
               _buildButton(
                 context,
                 icon: Icons.menu_book,
                 label: 'Anleitung',
                 screen: const OnboardingScreen(),
               ),
               const SizedBox(height: 15),
               _buildButton(
                 context,
                 icon: Icons.translate,
                 label: 'Zum Übersetzen',
                 screen: const RecordingScreen(),
               ),
             ],
           ),
         ),
       ),
     ),
   );
 }
 Widget _buildButton(
   BuildContext context, {
   required IconData icon,
   required String label,
   required Widget screen,
 }) {
   return SizedBox(
     width: double.infinity,
     child: ElevatedButton.icon(
       icon: Icon(icon),
       label: Text(label),
       onPressed: () {
         Navigator.push(
           context,
           MaterialPageRoute(
             builder: (_) => screen,
           ),
         );
       },
     ),
   );
 }
}
 