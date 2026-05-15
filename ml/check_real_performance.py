import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
import json

print("Chargement des données et du modèle...")
df = pd.read_csv('data/epilepsy_dataset_5000.csv')

with open('models/model_metadata.json', 'r') as f:
    meta = json.load(f)

features = meta['features']
mean = np.array(meta['mean'])
std = np.array(meta['std'])

X = df[features].fillna(0).values
y_true = df['alert'].values

# Normalisation
X_norm = (X - mean) / std

# Charger le modèle et prédire
model = tf.keras.models.load_model('models/seizure_detector.h5')
y_pred_prob = model.predict(X_norm, verbose=0)
y_pred = (y_pred_prob > 0.5).astype(int).flatten()

# Afficher le vrai rapport
print("\n" + "="*50)
print("RAPPORT DE CLASSIFICATION (LES VRAIS SCORES)")
print("="*50)
print(classification_report(y_true, y_pred, target_names=["Pas d'alerte (0)", "Alerte Crise (1)"]))

print("\n" + "="*50)
print("MATRICE DE CONFUSION")
print("="*50)
cm = confusion_matrix(y_true, y_pred)
print(f"Vrais Négatifs (0 bien prédit) : {cm[0][0]}")
print(f"Faux Positifs (0 prédit comme 1): {cm[0][1]}")
print(f"Faux Négatifs (1 prédit comme 0): {cm[1][0]} ⚠️ (Crises ratées !)")
print(f"Vrais Positifs (1 bien prédit)  : {cm[1][1]} ✅ (Crises détectées !)")