"""Smart Guardian - Seizure Detection LSTM Model Architecture

Architecture: Conv1D + Bidirectional LSTM + Dense
Input: (batch, 178, 1) - EEG time series
Output: (batch, 1) - seizure probability [0, 1]
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


def build_seizure_detector(
    sequence_length: int = 178,
    num_channels: int = 1,
    lstm_units: int = 64,
    dropout_rate: float = 0.3,
    learning_rate: float = 0.001,
) -> keras.Model:
    """Build the seizure detection LSTM model.

    Architecture:
    1. Conv1D layers - local pattern extraction (spike detection)
    2. BatchNorm - normalize activations
    3. Bidirectional LSTM - temporal pattern recognition
    4. Dense layers - classification
    5. Sigmoid output - seizure probability
    """
    inputs = keras.Input(shape=(sequence_length, num_channels))

    # Conv1D for local feature extraction
    x = layers.Conv1D(filters=32, kernel_size=5, activation="relu", padding="same")(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.SpatialDropout1D(dropout_rate)(x)

    # Second Conv1D for deeper feature extraction
    x = layers.Conv1D(filters=64, kernel_size=3, activation="relu", padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.SpatialDropout1D(dropout_rate)(x)

    # Bidirectional LSTM for temporal patterns
    x = layers.Bidirectional(
        layers.LSTM(lstm_units, return_sequences=False)
    )(x)
    x = layers.Dropout(dropout_rate)(x)

    # Dense classification layers
    x = layers.Dense(32, activation="relu")(x)
    x = layers.Dropout(dropout_rate)(x)
    x = layers.Dense(16, activation="relu")(x)
    x = layers.Dropout(0.2)(x)

    # Output: seizure probability
    outputs = layers.Dense(1, activation="sigmoid")(x)

    model = keras.Model(inputs=inputs, outputs=outputs)

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
        loss="binary_crossentropy",
        metrics=[
            "accuracy",
            keras.metrics.Precision(name="precision"),
            keras.metrics.Recall(name="recall"),
            keras.metrics.AUC(name="auc"),
        ],
    )

    return model


if __name__ == "__main__":
    model = build_seizure_detector()
    model.summary()
