import 'package:flutter/material.dart';
import '../home/home_screen.dart';
import 'recording_controller.dart';

class RecordingScreen extends StatefulWidget {

  const RecordingScreen({

    super.key,

    this.controller,

  });

  final RecordingController? controller;

  @override

  State<RecordingScreen> createState() => _RecordingScreenState();

}

class _RecordingScreenState extends State<RecordingScreen> {

  late final RecordingController controller;

  @override

  void initState() {

    super.initState();

    controller = widget.controller ?? RecordingController();

    controller.addListener(_onControllerChanged);

    controller.init();

  }

  void _onControllerChanged() {

    if (mounted) {

      setState(() {});

    }

  }

  @override

  void dispose() {

    controller.removeListener(_onControllerChanged);

    controller.dispose();

    super.dispose();

  }

  void _goHome() {

    Navigator.pushAndRemoveUntil(

      context,

      MaterialPageRoute(

        builder: (_) => const HomeScreen(),

      ),

      (route) => false,

    );

  }

  @override

  Widget build(BuildContext context) {

    if (!controller.ready) {

      return Scaffold(

        backgroundColor: Colors.black,

        body: Center(

          child: controller.status.contains('Fehler') ||

                  controller.status.contains('nicht')

              ? Text(

                  controller.status,

                  style: const TextStyle(

                    color: Colors.white,

                  ),

                )

              : const CircularProgressIndicator(),

        ),

      );

    }

    return Scaffold(

      backgroundColor: Colors.black,

      body: SafeArea(

        child: Column(

          children: [

            _buildHeader(),

            _buildCameraPreview(),

            _buildProgress(),

            _buildRecordingStatus(),

            _buildTranslationResult(),

            _buildRecordButton(),

          ],

        ),

      ),

    );

  }

  Widget _buildHeader() {

    return Padding(

      padding: const EdgeInsets.symmetric(

        horizontal: 20,

        vertical: 10,

      ),

      child: Stack(

        alignment: Alignment.center,

        children: [

          const Text(

            'SIGN-APP',

            style: TextStyle(

              color: Colors.white,

              fontSize: 24,

              fontWeight: FontWeight.bold,

            ),

          ),

          Align(

            alignment: Alignment.centerLeft,

            child: FloatingActionButton(

              heroTag: 'home',

              mini: true,

              backgroundColor: Colors.grey,

              onPressed: _goHome,

              child: const Icon(Icons.home),

            ),

          ),

          Align(

            alignment: Alignment.centerRight,

            child: FloatingActionButton(

              heroTag: 'switch',

              mini: true,

              backgroundColor: Colors.blue,

              onPressed: controller.isRecording

                  ? null

                  : controller.switchCamera,

              child: const Icon(Icons.cameraswitch),

            ),

          ),

        ],

      ),

    );

  }

  Widget _buildCameraPreview() {

    return Expanded(

      child: Padding(

        padding: const EdgeInsets.symmetric(

          horizontal: 15,

        ),

        child: ClipRRect(

          borderRadius: BorderRadius.circular(20),

          child: controller.cameraPreview,

        ),

      ),

    );

  }

  Widget _buildProgress() {

    return Padding(

      padding: const EdgeInsets.fromLTRB(

        20,

        20,

        20,

        0,

      ),

      child: LinearProgressIndicator(

        value: controller.progress,

        minHeight: 10,

        backgroundColor: Colors.grey,

        valueColor: AlwaysStoppedAnimation(

          controller.progressColor,

        ),

      ),

    );

  }

  Widget _buildRecordingStatus() {

    return Padding(

      padding: const EdgeInsets.symmetric(

        vertical: 20,

      ),

      child: controller.isRecording

          ? Row(

              mainAxisAlignment: MainAxisAlignment.center,

              children: [

                AnimatedOpacity(

                  opacity: controller.blink ? 1.0 : 0.2,

                  duration: const Duration(

                    milliseconds: 500,

                  ),

                  child: Container(

                    width: 16,

                    height: 16,

                    decoration: const BoxDecoration(

                      color: Colors.red,

                      shape: BoxShape.circle,

                    ),

                  ),

                ),

                const SizedBox(width: 10),

                Text(

                  controller.formattedTime,

                  style: const TextStyle(

                    color: Colors.white,

                    fontSize: 22,

                    fontWeight: FontWeight.bold,

                  ),

                ),

              ],

            )

          : Text(

              controller.status,

              style: const TextStyle(

                color: Colors.white,

                fontSize: 18,

              ),

            ),

    );

  }

  Widget _buildTranslationResult() {

    if (controller.translatedText == null) {

      return const SizedBox.shrink();

    }

    return Padding(

      padding: const EdgeInsets.all(20),

      child: Column(

        children: [

          Text(

            controller.translatedText!,

            textAlign: TextAlign.center,

            style: const TextStyle(

              color: Colors.white,

              fontSize: 32,

              fontWeight: FontWeight.bold,

            ),

          ),

          const SizedBox(height: 10),

          if (controller.confidence != null)

            Text(

              'Sicherheit: '

              '${(controller.confidence! * 100).toStringAsFixed(1)} %',

              style: const TextStyle(

                color: Colors.greenAccent,

                fontSize: 18,

              ),

            ),

          const SizedBox(height: 15),

          FloatingActionButton.extended(

            onPressed: controller.speak,

            backgroundColor: Colors.blue,

            icon: const Icon(Icons.volume_up),

            label: const Text('Vorlesen'),

          ),

        ],

      ),

    );

  }

  Widget _buildRecordButton() {

    return Padding(

      padding: const EdgeInsets.only(

        bottom: 30,

      ),

      child: FloatingActionButton(

        onPressed: controller.isLoading

            ? null

            : controller.isRecording

                ? controller.stop

                : controller.start,

        backgroundColor:

            controller.isRecording ? Colors.red : Colors.green,

        child: controller.isLoading

            ? const CircularProgressIndicator(

                color: Colors.white,

              )

            : Icon(

                controller.isRecording

                    ? Icons.stop

                    : Icons.play_arrow,

              ),

      ),

    );

  }

}
 