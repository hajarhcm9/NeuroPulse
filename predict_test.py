import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model

# 1. Charger le cerveau que tu as créé
model = load_model('models/epilepsy_model.h5')

def predict_status(signal_value):
    # On prépare la donnée (elle doit être en 2D pour le modèle)
    data = np.array([[signal_value]])
    
    # Faire la prédiction
    prediction = model.predict(data, verbose=0)
    
    # Si la probabilité est > 0.5, c'est une crise
    if prediction[0][0] > 0.5:
        return "⚠️ ALERTE : Crise détectée !"
    else:
        return "✅ État : Normal"

# Test avec une valeur au hasard
print(predict_status(45.0))