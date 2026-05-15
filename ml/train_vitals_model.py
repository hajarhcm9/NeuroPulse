import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import json
import os

print("Chargement des données...")
df = pd.read_csv('data/epilepsy_dataset_5000.csv')

# 1. Préparation des données
# On garde uniquement les colonnes numériques utiles
features_to_keep = ['age', 'baseline_eda', 'baseline_bpm', 'baseline_temp', 
                    'eda_us', 'bpm', 'temp_c']

# La cible à prédire
target = 'alert'

# Remplacer les valeurs manquantes par 0
df = df[features_to_keep + [target]].fillna(0)

X = df[features_to_keep].values
y = df[target].values

print(f"Données prêtes : {X.shape[0]} échantillons, {X.shape[1]} features")

# 2. Division Entraînement / Test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Normalisation (très important)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Sauvegarder les paramètres de normalisation
mean_values = scaler.mean_.tolist()
scale_values = scaler.scale_.tolist()

# 4. Création du modèle Dense (adapté aux 11 features)
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(X.shape[1],)),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

print("\nDébut de l'entraînement...")
# 5. Entraînement
model.fit(X_train, y_train, epochs=15, batch_size=32, validation_data=(X_test, y_test), verbose=1)

# 6. Évaluation
loss, acc = model.evaluate(X_test, y_test, verbose=0)
print(f"\n✅ Précision sur les données de test : {acc*100:.2f}%")

# 7. Sauvegarde du modèle et des paramètres
model.save('models/seizure_detector.h5') # On écrase l'ancien modèle
with open('models/model_metadata.json', 'w') as f:
    json.dump({'features': features_to_keep, 'mean': mean_values, 'std': scale_values}, f)

print("Modèle et métadonnées sauvegardés dans ml/models/ !")