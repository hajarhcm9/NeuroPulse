import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import os

# Chemins adaptés à votre architecture
DATA_PATH = '../data/epilepsy_dataset_5000.csv'
MODELS_PATH = '../models/'

# 1. Charger les données
print("Chargement des données...")
df = pd.read_csv(DATA_PATH)

# 2. Définir les caractéristiques (features) pour chaque patient
features_p1 = ['eda_ratio', 'eda_us', 'temp_delta'] # Patient 1 (EDA)
features_p2 = ['bpm_ratio', 'bpm', 'temp_delta']    # Patient 2 (BPM)
target = 'risk_level'

# 3. Fonction d'entraînement
def train_patient_model(df_patient, features, patient_name, model_filename):
    print(f"\n--- Entraînement du modèle pour {patient_name} ---")
    
    train_data = df_patient[df_patient['split'] == 'train']
    test_data = df_patient[df_patient['split'] == 'test']
    
    X_train = train_data[features]
    y_train = train_data[target]
    X_test = test_data[features]
    y_test = test_data[target]
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    print(classification_report(y_test, predictions, zero_division=0))
    
    # Sauvegarder dans le dossier models/
    save_path = os.path.join(MODELS_PATH, model_filename)
    joblib.dump(model, save_path)
    print(f"✅ Modèle sauvegardé sous '{save_path}'")
    
    return model

# 4. Exécuter l'entraînement pour le Patient 1
df_p1 = df[df['patient_id'] == 'P001'].copy()
if not df_p1.empty:
    train_patient_model(df_p1, features_p1, "Patient 1 (EDA Dominant)", "model_patient_1_eda.pkl")

# 5. Exécuter l'entraînement pour le Patient 2 (Décommentez quand vous aurez P002)
"""
df_p2 = df[df['patient_id'] == 'P002'].copy()
if not df_p2.empty:
    train_patient_model(df_p2, features_p2, "Patient 2 (BPM Dominant)", "model_patient_2_bpm.pkl")
"""