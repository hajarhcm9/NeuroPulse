import os
import json
import numpy as np
import tensorflow as tf

class Predictor:
    def __init__(self):
        base_dir = os.path.dirname(__file__)
        self.model_path = os.path.join(base_dir, 'models', 'seizure_detector.h5')
        self.metadata_path = os.path.join(base_dir, 'models', 'model_metadata.json')
        
        self.model = None
        self.mean = 0
        self.std = 1
        self.features = []
        
        self.load_model()

    def load_model(self):
        if os.path.exists(self.model_path):
            self.model = tf.keras.models.load_model(self.model_path)
            print("✅ Modèle chargé avec succès !")
            
        if os.path.exists(self.metadata_path):
            with open(self.metadata_path, 'r') as f:
                metadata = json.load(f)
                self.mean = np.array(metadata['mean'])
                self.std = np.array(metadata['std'])
                self.features = metadata['features']
            print(f"✅ Normalisation chargée pour les features : {self.features}")

    def predict(self, input_data):
        if self.model is None:
            return "Erreur : Modèle non chargé."
        
        data = np.array(input_data)
        data = (data - self.mean) / self.std
        probabilite = self.model.predict(data.reshape(1, -1), verbose=0)[0][0]
        classe = 1 if probabilite > 0.5 else 0
        
        return {"probabilite_alerte": float(probabilite), "classe_predite": classe}

if __name__ == "__main__":
    p = Predictor()
    # Faux test avec 11 valeurs (age, eda, bpm, etc.)
    resultat = p.predict([25, 1.5, 80, 36.5, 2.1, 95, 37.1, 1.4, 1.2, 0.6, 50])
    print(resultat)