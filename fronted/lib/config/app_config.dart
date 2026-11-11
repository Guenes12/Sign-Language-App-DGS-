class AppConfig {
 AppConfig._();
 // ============================================================
 // Python server configuration
 // Change the IP address here when the server runs on another
 // device or network.
 // ============================================================
 static const String serverIp = '';
 static const int serverPort = 8000;
 static String get predictionUrl =>
     'http://$serverIp:$serverPort/predict';
}
