import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model
import os

class EpilepsyPredictor:
    def __init__(self, model_path='models/epilepsy_model.h5'):
        """
        Initialise le prédicteur en chargeant le modèle entraîné.
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Modèle introuvable à l'adresse : {model_path}")
        
        self.model = load_model(model_path)
        print(f"✅ Modèle chargé avec succès depuis {model_path}")

    def predict(self, signal_value):
        """
        Prend une valeur de signal brute et retourne la probabilité de crise.
        """
        try:
            # 1. Préparation de la donnée (format 2D requis par le modèle)
            data = np.array([[float(signal_value)]])
            
            # 2. Prédiction
            prediction = self.model.predict(data, verbose=0)
            probability = float(prediction[0][0])
            
            # 3. Résultat structuré
            is_seizure = probability > 0.5
            return {
                "probability": round(probability, 4),
                "is_seizure": is_seizure,
                "status": "🚨 CRISE DETECTEE" if is_seizure else "✅ NORMAL"
            }
        except Exception as e:
            return {"error": str(e)}

# --- EXEMPLE D'UTILISATION POUR LE BACKEND ---
if __name__ == "__main__":
    predictor = EpilepsyPredictor()
    result = predictor.predict(40.0)
    print(f"Test de prédiction : {result}")