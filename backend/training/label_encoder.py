import json
from pathlib import Path

class LabelEncoder:
   def __init__(self):
       self.classes = []
   def fit(self, class_names):
       self.classes = list(class_names)
   def encode(self, label):
       if label not in self.classes:
           raise ValueError(
               f"Unbekanntes Label: {label}"
           )
       return self.classes.index(label)
   def decode(self, index):
       if index < 0 or index >= len(self.classes):
           raise ValueError(
               f"Ungültiger Label-Index: {index}"
           )
       return self.classes[index]
   def save(self, path):
       path = Path(path)
       path.parent.mkdir(
           parents=True,
           exist_ok=True,
       )
       with open(
           path,
           "w",
           encoding="utf-8",
       ) as file:
           json.dump(
               self.classes,
               file,
               ensure_ascii=False,
               indent=2,
           )
   def load(self, path):
       path = Path(path)
       with open(
           path,
           "r",
           encoding="utf-8",
       ) as file:
           self.classes = json.load(file)
       return self.classes