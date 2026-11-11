import numpy as np
import tensorflow as tf


class ModelService:

    def __init__(self):

        self.model = tf.keras.models.load_model(

            "trained_models/gesture_model.keras"

        )

    def predict(self, sequence):

        input_data = np.expand_dims(sequence, axis=0)

        predictions = self.model.predict(

            input_data,

            verbose=0

        )

        probabilities = predictions[0]

        class_id = int(np.argmax(probabilities))

        confidence = float(

            probabilities[class_id]

        )

        return class_id, confidence
 