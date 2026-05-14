"""Smart Guardian - EEG Model Training Pipeline with data augmentation and versioning."""

import os
import json
import shutil
import logging
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List

logger = logging.getLogger("smart-guardian")

MODELS_DIR = Path("models")
VERSIONS_DIR = Path("models/versions")
BONN_DIR = Path("ml/training/data")


class TrainingService:
    """EEG model training service with augmentation and versioning."""

    def __init__(self):
        self._is_training = False
        self._current_status: Dict[str, Any] = {
            "is_training": False,
            "current_epoch": 0,
            "total_epochs": 0,
            "loss": None,
            "accuracy": None,
            "val_loss": None,
            "val_accuracy": None,
        }
        self._training_thread: Optional[threading.Thread] = None

    @property
    def is_training(self) -> bool:
        return self._is_training

    def get_status(self) -> Dict[str, Any]:
        return dict(self._current_status)

    def list_versions(self) -> List[Dict[str, Any]]:
        """List all saved model versions."""
        versions = []
        if not VERSIONS_DIR.exists():
            return versions

        for vdir in sorted(VERSIONS_DIR.iterdir(), reverse=True):
            if vdir.is_dir():
                meta_file = vdir / "metadata.json"
                meta = {}
                if meta_file.exists():
                    with open(meta_file, "r") as f:
                        meta = json.load(f)
                versions.append({
                    "version": vdir.name,
                    "created_at": meta.get("created_at", "unknown"),
                    "accuracy": meta.get("accuracy"),
                    "loss": meta.get("loss"),
                    "is_active": self._is_active_version(vdir.name),
                })
        return versions

    def activate_version(self, version: str) -> bool:
        """Switch the active model to a previously trained version."""
        vdir = VERSIONS_DIR / version
        if not vdir.exists():
            return False

        model_file = vdir / "seizure_detector.h5"
        meta_file = vdir / "metadata.json"
        if not model_file.exists():
            return False

        shutil.copy2(str(model_file), str(MODELS_DIR / "seizure_detector.h5"))
        if meta_file.exists():
            shutil.copy2(str(meta_file), str(MODELS_DIR / "model_metadata.json"))

        from app.services.model_service import model_service
        model_service.load_model()
        logger.info("Activated model version: %s", version)
        return True

    def delete_version(self, version: str) -> bool:
        """Delete a saved model version."""
        if self._is_active_version(version):
            logger.warning("Cannot delete active version: %s", version)
            return False
        vdir = VERSIONS_DIR / version
        if not vdir.exists():
            return False
        shutil.rmtree(str(vdir))
        logger.info("Deleted model version: %s", version)
        return True

    def start_training(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Start training in a background thread."""
        if self._is_training:
            return {"error": "Training already in progress", "status": self.get_status()}

        self._is_training = True
        self._current_status = {
            "is_training": True,
            "current_epoch": 0,
            "total_epochs": config.get("epochs", 50),
            "loss": None,
            "accuracy": None,
            "val_loss": None,
            "val_accuracy": None,
        }

        self._training_thread = threading.Thread(
            target=self._train_model,
            args=(config,),
            daemon=True,
        )
        self._training_thread.start()
        return {"message": "Training started", "status": self.get_status()}

    def _train_model(self, config: Dict[str, Any]):
        """Internal training method running in background thread."""
        try:
            import tensorflow as tf
            import numpy as np
        except ImportError:
            self._is_training = False
            self._current_status["is_training"] = False
            logger.error("TensorFlow not available for training")
            return

        try:
            epochs = config.get("epochs", 50)
            batch_size = config.get("batch_size", 32)
            learning_rate = config.get("learning_rate", 0.001)
            use_augmentation = config.get("augmentation", True)
            noise_level = config.get("noise_level", 0.05)
            val_split = config.get("validation_split", 0.2)

            # 1) Load Bonn EEG dataset
            X, y = self._load_bonn_data()
            if X is None:
                logger.error("No training data found")
                self._is_training = False
                self._current_status["is_training"] = False
                return

            # 2) Data augmentation
            if use_augmentation:
                X_aug, y_aug = self._augment_data(X, y, noise_level)
                X = np.concatenate([X, X_aug], axis=0)
                y = np.concatenate([y, y_aug], axis=0)
                logger.info("Augmented dataset: %d samples", len(X))

            # 3) Normalize
            mean = float(np.mean(X))
            std = float(np.std(X))
            if std == 0:
                std = 1.0
            X = (X - mean) / std

            # 4) Split
            split_idx = int(len(X) * (1 - val_split))
            X_train, X_val = X[:split_idx], X[split_idx:]
            y_train, y_val = y[:split_idx], y[split_idx:]

            # 5) Build model
            model = self._build_model(learning_rate)

            # 6) Train with epoch callback
            class StatusCallback(tf.keras.callbacks.Callback):
                def __init__(self, service):
                    super().__init__()
                    self.service = service

                def on_epoch_end(self, epoch, logs=None):
                    logs = logs or {}
                    self.service._current_status.update({
                        "current_epoch": epoch + 1,
                        "total_epochs": epochs,
                        "loss": round(float(logs.get("loss", 0)), 4),
                        "accuracy": round(float(logs.get("accuracy", 0)), 4),
                        "val_loss": round(float(logs.get("val_loss", 0)), 4) if logs.get("val_loss") else None,
                        "val_accuracy": round(float(logs.get("val_accuracy", 0)), 4) if logs.get("val_accuracy") else None,
                    })

            history = model.fit(
                X_train, y_train,
                validation_data=(X_val, y_val),
                epochs=epochs,
                batch_size=batch_size,
                callbacks=[StatusCallback(self)],
                verbose=0,
            )

            # 7) Save new version
            final_loss = float(history.history["loss"][-1])
            final_acc = float(history.history["accuracy"][-1])
            final_val_loss = float(history.history.get("val_loss", [0])[-1])
            final_val_acc = float(history.history.get("val_accuracy", [0])[-1])

            version = "v" + datetime.now().strftime("%Y%m%d_%H%M%S")
            self._save_model_version(model, version, {
                "model_version": version,
                "created_at": datetime.now().isoformat(),
                "accuracy": round(final_acc, 4),
                "loss": round(final_loss, 4),
                "val_accuracy": round(final_val_acc, 4),
                "val_loss": round(final_val_loss, 4),
                "epochs": epochs,
                "batch_size": batch_size,
                "learning_rate": learning_rate,
                "augmentation": use_augmentation,
                "noise_level": noise_level,
                "training_samples": len(X_train),
                "validation_samples": len(X_val),
                "normalization": {"mean": round(mean, 4), "std": round(std, 4)},
            })

            # 8) Activate the new model
            self.activate_version(version)

            logger.info(
                "Training complete: %s acc=%.4f loss=%.4f",
                version, final_acc, final_loss,
            )

        except Exception as e:
            logger.error("Training failed: %s", e)
        finally:
            self._is_training = False
            self._current_status["is_training"] = False

    def _load_bonn_data(self):
        """Load Bonn EEG dataset from ml/training/data directory."""
        import numpy as np

        data_dir = BONN_DIR
        if not data_dir.exists():
            # Try to load from .npy files in models dir
            for npy_path in MODELS_DIR.glob("*.npy"):
                pass
            logger.warning("Bonn dataset not found at %s", data_dir)
            return None, None

        X_list = []
        y_list = []

        # Try loading .npy files (z: seizure, n: normal)
        for label, prefix in [(1, "z"), (0, "n"), (1, "s"), (0, "o")]:
            for npy_file in sorted(data_dir.glob(prefix + "*.npy")):
                try:
                    data = np.load(str(npy_file))
                    for segment in data:
                        if len(segment) >= 178:
                            X_list.append(segment[:178])
                            y_list.append(label)
                except Exception as e:
                    logger.warning("Failed to load %s: %s", npy_file, e)

        # Try CSV files as fallback
        if not X_list:
            for label, prefix in [(1, "z"), (0, "n"), (1, "s"), (0, "o")]:
                for csv_file in sorted(data_dir.glob(prefix + "*.csv")):
                    try:
                        data = np.loadtxt(str(csv_file), delimiter=",")
                        if data.ndim == 1:
                            if len(data) >= 178:
                                X_list.append(data[:178])
                                y_list.append(label)
                        else:
                            for row in data:
                                if len(row) >= 178:
                                    X_list.append(row[:178])
                                    y_list.append(label)
                    except Exception as e:
                        logger.warning("Failed to load %s: %s", csv_file, e)

        if not X_list:
            return None, None

        X = np.array(X_list, dtype=np.float32).reshape(-1, 178, 1)
        y = np.array(y_list, dtype=np.float32)
        logger.info("Loaded %d EEG segments", len(X))
        return X, y

    def _augment_data(self, X, y, noise_level: float):
        """Apply data augmentation: noise, time-shift, amplitude scaling."""
        import numpy as np

        X_aug = []
        y_aug = []

        for i in range(len(X)):
            sample = X[i].copy()

            # Gaussian noise
            noisy = sample + np.random.normal(0, noise_level, sample.shape).astype(np.float32)
            X_aug.append(noisy)
            y_aug.append(y[i])

            # Amplitude scaling (0.8x to 1.2x)
            scale = np.random.uniform(0.8, 1.2)
            scaled = (sample * scale).astype(np.float32)
            X_aug.append(scaled)
            y_aug.append(y[i])

            # Time shift (shift left or right by up to 10 samples)
            shift = np.random.randint(-10, 11)
            shifted = np.roll(sample, shift, axis=0).astype(np.float32)
            X_aug.append(shifted)
            y_aug.append(y[i])

        return np.array(X_aug, dtype=np.float32), np.array(y_aug, dtype=np.float32)

    def _build_model(self, learning_rate: float):
        """Build the Conv1D + BiLSTM + Dense model."""
        import tensorflow as tf

        model = tf.keras.Sequential([
            tf.keras.layers.Conv1D(32, 3, activation="relu", input_shape=(178, 1)),
            tf.keras.layers.Conv1D(64, 3, activation="relu"),
            tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=False)),
            tf.keras.layers.Dense(32, activation="relu"),
            tf.keras.layers.Dense(16, activation="relu"),
            tf.keras.layers.Dense(1, activation="sigmoid"),
        ])

        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
            loss="binary_crossentropy",
            metrics=["accuracy"],
        )
        return model

    def _save_model_version(self, model, version: str, metadata: Dict[str, Any]):
        """Save model and metadata to versions directory."""
        vdir = VERSIONS_DIR / version
        vdir.mkdir(parents=True, exist_ok=True)
        model.save(str(vdir / "seizure_detector.h5"))
        with open(str(vdir / "metadata.json"), "w") as f:
            json.dump(metadata, f, indent=2)
        logger.info("Model saved: %s", version)

    def _is_active_version(self, version: str) -> bool:
        """Check if a version is currently the active model."""
        meta_path = MODELS_DIR / "model_metadata.json"
        if not meta_path.exists():
            return False
        try:
            with open(str(meta_path), "r") as f:
                meta = json.load(f)
            return meta.get("model_version") == version
        except Exception:
            return False


training_service = TrainingService()