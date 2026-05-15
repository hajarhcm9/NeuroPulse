import pandas as pd
import os
from predictor import Predictor

df = pd.read_csv('data/epilepsy_dataset_5000.csv')
print("✅ Dataset chargée !")

p = Predictor()

# Prendre la première ligne
ligne = df.iloc[0]
vraie_alerte = ligne['alert']

# Extraire uniquement les 11 features dont le modèle a besoin
input_features = ligne[p.features].values.tolist()

# Prédiction
resultat = p.predict(input_features)

print(f"Vraie alerte (dataset) : {vraie_alerte}")
print(f"Résultat du modèle      : {resultat}")