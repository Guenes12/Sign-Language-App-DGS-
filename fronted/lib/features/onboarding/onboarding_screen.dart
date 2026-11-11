import 'package:flutter/material.dart';
import '../home/home_screen.dart';

class OnboardingScreen extends StatefulWidget {
 const OnboardingScreen({super.key});
 @override
 State<OnboardingScreen> createState() => _OnboardingScreenState();
}
class _OnboardingScreenState extends State<OnboardingScreen> {
 final PageController _controller = PageController();
 int step = 0;
 final pages = [
   (
     "Willkommen 👋",
     "Mit der Sign-App kannst du Gebärdensprache automatisch in Text übersetzen."
   ),
   (
     "Aufnahme starten 🎥",
     "Drücke den grünen Button, um die Aufnahme zu starten."
   ),
   (
     "Kamera wechseln 🔄",
     "Wechsle zwischen Front- und Rückkamera."
   ),
   (
     "Aufnahmedauer ⏱️",
     "Maximal 10 Sekunden Aufnahmezeit."
     "Die Aufnahme kann jederzeit mit dem Stopp-Button beendet werden"
   ),
   (
     "KI Verarbeitung 🤖",
     "Dein Video wird von der KI analysiert."
   ),
   (
     "Übersetzung 📄",
     "Der erkannte Text erscheint nach der Verarbeitung."
   ),
   (
     "Vorlesen 🔊",
     "Der Text kann als Audio ausgegeben werden."
   ),
   (
     "Home 🏠",
     "Du kannst jederzeit zur Startseite zurück."
   ),
   (
     "Bereit 🚀",
     "Jetzt kannst du die App nutzen!"
   ),
 ];
 bool get isLast => step == pages.length - 1;
 void next() {
   if (!isLast) {
     _controller.nextPage(
       duration: const Duration(milliseconds: 350),
       curve: Curves.easeInOut,
     );
   } else {
     _finish();
   }
 }
 void back() {
   if (step > 0) {
     _controller.previousPage(
       duration: const Duration(milliseconds: 350),
       curve: Curves.easeInOut,
     );
   }
 }
 void skip() => _finish();
 void _finish() {
   Navigator.pushReplacement(
     context,
     MaterialPageRoute(
       builder: (_) => const HomeScreen(),
     ),
   );
 }
 Widget buildPage(String title, String desc, Widget visual) {
   return Padding(
     padding: const EdgeInsets.all(30),
     child: Column(
       mainAxisAlignment: MainAxisAlignment.center,
       children: [
         Text(
           title,
           textAlign: TextAlign.center,
           style: const TextStyle(
             color: Colors.white,
             fontSize: 28,
             fontWeight: FontWeight.bold,
           ),
         ),
         const SizedBox(height: 20),
         Text(
           desc,
           textAlign: TextAlign.center,
           style: const TextStyle(
             color: Colors.grey,
             fontSize: 18,
           ),
         ),
         const SizedBox(height: 50),
         AnimatedSwitcher(
           duration: const Duration(milliseconds: 300),
           child: visual,
         ),
       ],
     ),
   );
 }
 Widget buildVisual(int index) {
   switch (index) {
     case 1:
       return FloatingActionButton(
         onPressed: () {},
         backgroundColor: Colors.green,
         child: const Icon(Icons.play_arrow),
       );
     case 2:
       return FloatingActionButton(
         onPressed: () {},
         backgroundColor: Colors.blue,
         child: const Icon(Icons.cameraswitch),
       );
     case 3:
       return Column(
         children: [
           const Text(
             "00:05",
             style: TextStyle(
               color: Colors.white,
               fontSize: 22,
               fontWeight: FontWeight.bold,
             ),
           ),
           const SizedBox(height: 10),
           LinearProgressIndicator(
             value: 0.5,
             minHeight: 10,
             backgroundColor: Colors.grey,
             valueColor: const AlwaysStoppedAnimation(Colors.green),
           ),
         ],
       );
     case 4:
       return const CircularProgressIndicator(color: Colors.blue);
     case 5:
       return Container(
         width: 260,
         padding: const EdgeInsets.all(16),
         decoration: BoxDecoration(
           color: Colors.grey.shade900,
           borderRadius: BorderRadius.circular(12),
         ),
         child: const Text(
           "Ja",
           textAlign: TextAlign.center,
           style: TextStyle(
             color: Colors.white,
             fontSize: 24,
             fontWeight: FontWeight.bold,
           ),
         ),
       );
     case 6:
       return FloatingActionButton.extended(
         onPressed: () {},
         icon: const Icon(Icons.volume_up),
         label: const Text("Vorlesen"),
       );
     case 7:
       return FloatingActionButton(
         onPressed: () {},
         backgroundColor: Colors.grey,
         child: const Icon(Icons.home),
       );
     case 8:
       return Column(
         children: const [
           Icon(Icons.check_circle, color: Colors.green, size: 80),
           SizedBox(height: 10),
           Text(
             "Alles bereit!",
             style: TextStyle(color: Colors.white, fontSize: 20),
           ),
         ],
       );
     default:
       return const Icon(
         Icons.waving_hand,
         color: Colors.white,
         size: 80,
       );
   }
 }
 @override
 Widget build(BuildContext context) {
   return Scaffold(
     backgroundColor: Colors.black,
     appBar: AppBar(
       backgroundColor: Colors.black,
       leading: step > 0
           ? IconButton(
               icon: const Icon(Icons.arrow_back, color: Colors.white),
               onPressed: back,
             )
           : null,
       actions: [
         TextButton(
           onPressed: skip,
           child: Text(
             isLast ? "Fertig" : "Überspringen",
             style: const TextStyle(
               color: Colors.white,
               fontWeight: FontWeight.bold,
             ),
           ),
         ),
       ],
     ),
     body: Column(
       children: [
         LinearProgressIndicator(
           value: (step + 1) / pages.length,
           backgroundColor: Colors.grey.shade800,
           valueColor: const AlwaysStoppedAnimation(Colors.blue),
         ),
         Expanded(
           child: PageView.builder(
             controller: _controller,
             itemCount: pages.length,
             onPageChanged: (index) {
               setState(() => step = index);
             },
             itemBuilder: (context, index) {
               final page = pages[index];
               return buildPage(
                 page.$1,
                 page.$2,
                 buildVisual(index),
               );
             },
           ),
         ),
         Padding(
           padding: const EdgeInsets.all(20),
           child: SizedBox(
             width: double.infinity,
             child: ElevatedButton(
               onPressed: next,
               child: Text(isLast ? "Fertig" : "Weiter"),
             ),
           ),
         ),
       ],
     ),
   );
 }
}
 
 