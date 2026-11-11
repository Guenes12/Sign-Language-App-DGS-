import 'package:camera/camera.dart';
import 'package:flutter/material.dart';

class CameraService {
 CameraController? _controller;
 List<CameraDescription> _cameras = [];
 int _cameraIndex = 0;
 bool get isReady =>
     _controller != null && _controller!.value.isInitialized;
 Widget get preview {
   if (!isReady) {
     return const Center(
       child: CircularProgressIndicator(),
     );
   }
   return CameraPreview(_controller!);
 }
 Future<void> init() async {
   _cameras = await availableCameras();
   if (_cameras.isEmpty) {
     throw Exception('Keine Kamera gefunden.');
   }
   await _initializeCurrentCamera();
 }
 Future<void> _initializeCurrentCamera() async {
   final controller = CameraController(
     _cameras[_cameraIndex],
     ResolutionPreset.medium,
   );
   await controller.initialize();
   _controller = controller;
 }
 Future<void> startRecording() async {
   if (!isReady) {
     throw Exception('Kamera ist nicht initialisiert.');
   }
   if (_controller!.value.isRecordingVideo) {
     return;
   }
   await _controller!.startVideoRecording();
 }
 Future<XFile?> stopRecording() async {
   if (!isReady) {
     return null;
   }
   if (!_controller!.value.isRecordingVideo) {
     return null;
   }
   return _controller!.stopVideoRecording();
 }
 Future<void> switchCamera() async {
   if (_cameras.length < 2) {
     return;
   }
   _cameraIndex = (_cameraIndex + 1) % _cameras.length;
   await _controller?.dispose();
   await _initializeCurrentCamera();
 }
 Future<void> dispose() async {
   await _controller?.dispose();
   _controller = null;
 }
}
