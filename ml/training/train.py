"""Smart Guardian - Training Pipeline

Complete training pipeline for the seizure detection model.
Generates data, builds model, trains, evaluates, and exports.
"""

import os
import sys
import json
import numpy as np
import tensorflow as tf
from datetime import datetime
from tensorflow import keras
from generate_data import generate_dataset, save_dataset
from model import build_seizure_detector


def normalize_data(X_train, X_val, X_test):
    """Z-score normalization using training statistics."""
    mean = X_train.mean()
    std = X_train.std()
    if std == 0:
        std = 1.0
    X_train = (X_train - mean) / std
    X_val = (X_val - mean) / std
    X_test = (X_test - mean) / std
    return X_train, X_val, X_test, mean, std


def train_model(
    epochs: int = 50,
    batch_size: int = 32,
    sequence_length: int = 178,
    num_channels: int = 1,
    lstm_units: int = 64,
    dropout_rate: float = 0.3,
    learning_rate: float = 0.001,
    num_normal: int = 2000,
    num_seizure: int = 2000,
    output_dir: str = "ml/models",
):
    """Full training pipeline."""
    print("=" * 60)
    print("Smart Guardian - Seizure Detection Model Training")
    print("=" * 60)
    print(f"TensorFlow version: {tf.__version__}")
    print(f"GPU available: {len(tf.config.list_physical_devices('GPU')) > 0}")
    print()

    # Step 1: Generate dataset
    print("[1/5] Generating dataset...")
    train_data, val_data, test_data = generate_dataset(
        num_normal=num_normal,
        num_seizure=num_seizure,
        sequence_length=sequence_length,
        num_channels=num_channels,
    )
    save_dataset(train_data, val_data, test_data)
    print()

    # Step 2: Normalize
    print("[2/5] Normalizing data...")
    X_train, X_val, X_test, mean, std = normalize_data(
        train_data["x"], val_data["x"], test_data["x"]
    )
    y_train = train_data["y"]
    y_val = val_data["y"]
    y_test = test_data["y"]
    print(f"  Normalization: mean={mean:.4f}, std={std:.4f}")
    print()

    # Step 3: Build model
    print("[3/5] Building model...")
    model = build_seizure_detector(
        sequence_length=sequence_length,
        num_channels=num_channels,
        lstm_units=lstm_units,
        dropout_rate=dropout_rate,
        learning_rate=learning_rate,
    )
    model.summary()
    print()

    # Step 4: Train
    print("[4/5] Training model...")
    callbacks = [
        keras.callbacks.EarlyStopping(
            monitor="val_auc",
            patience=10,
            mode="max",
            restore_best_weights=True,
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=5,
            min_lr=1e-6,
        ),
        keras.callbacks.ModelCheckpoint(
            filepath=os.path.join(output_dir, "best_model.keras"),
            monitor="val_auc",
            mode="max",
            save_best_only=True,
        ),
    ]

    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=epochs,
        batch_size=batch_size,
        callbacks=callbacks,
        verbose=1,
    )
    print()

    # Step 5: Evaluate
    print("[5/5] Evaluating model...")
    results = model.evaluate(X_test, y_test, verbose=0)
    metrics = dict(zip(model.metrics_names, results))
    for name, value in metrics.items():
        print(f"  {name}: {value:.4f}")
    print()

    # Export model
    os.makedirs(output_dir, exist_ok=True)
    model_path = os.path.join(output_dir, "seizure_detector.h5")
    model.save(model_path)
    print(f"Model saved to {model_path}")

    # Save normalization params and metadata
    metadata = {
        "model_version": "1.0.0",
        "trained_at": datetime.now().isoformat(),
        "sequence_length": sequence_length,
        "num_channels": num_channels,
        "input_shape": [sequence_length, num_channels],
        "normalization": {"mean": float(mean), "std": float(std)},
        "metrics": {k: float(v) for k, v in metrics.items()},
        "training_params": {
            "epochs": epochs,
            "batch_size": batch_size,
            "lstm_units": lstm_units,
            "dropout_rate": dropout_rate,
            "learning_rate": learning_rate,
            "num_samples": num_normal + num_seizure,
        },
    }
    meta_path = os.path.join(output_dir, "model_metadata.json")
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"Metadata saved to {meta_path}")
    print()
    print("=" * 60)
    print("Training complete!")
    print("=" * 60)

    return model, history, metrics


if __name__ == "__main__":
    model, history, metrics = train_model(epochs=50)
