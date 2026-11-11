from dataclasses import dataclass

@dataclass(slots=True)
class PredictionResult:
   """
   Ergebnis einer Vorhersage.
   """
   label: str
   confidence: float
   def to_dict(self):
       return {
           "label": self.label,
           "confidence": round(self.confidence, 4)
       }