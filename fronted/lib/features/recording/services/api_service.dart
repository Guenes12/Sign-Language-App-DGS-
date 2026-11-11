import 'dart:convert';
import 'package:camera/camera.dart';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import '../../../config/app_config.dart';
import '../models/translation_response.dart';

class ApiService {
 final http.Client client;
 ApiService({http.Client? client})
     : client = client ?? http.Client();
 Future<TranslationResponse?> sendVideo(XFile file) async {
   try {
     final request = http.MultipartRequest(
       'POST',
       Uri.parse(AppConfig.predictionUrl),
     );
     request.files.add(
       await http.MultipartFile.fromPath(
         'file',
         file.path,
       ),
     );
     debugPrint('POST ${AppConfig.predictionUrl}');
     debugPrint('Video: ${file.path}');
     final response = await client.send(request);
     final body = await response.stream.bytesToString();
     debugPrint('HTTP Status: ${response.statusCode}');
     debugPrint('Server Response: $body');
     if (response.statusCode != 200) {
       return null;
     }
     final json = jsonDecode(body) as Map<String, dynamic>;
     return TranslationResponse.fromJson(json);
   } catch (e) {
     debugPrint('API FEHLER: $e');
     return null;
   }
 }
 void dispose() {
   client.close();
 }
}