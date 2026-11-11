class TranslationResponse {
 final String label;
 final double confidence;
 const TranslationResponse({
   required this.label,
   required this.confidence,
 });
 factory TranslationResponse.fromJson(Map<String, dynamic> json) {
   return TranslationResponse(
     label: json['label'] as String? ?? '',
     confidence: (json['confidence'] as num?)?.toDouble() ?? 0.0,
   );
 }
}
