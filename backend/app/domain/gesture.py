from dataclasses import dataclass

@dataclass(slots=True)
class Gesture:
   """
   Repräsentiert eine Gebärde.
   """
   label: str