"""Smart Guardian - Synthetic EEG Data Generator

Generates realistic synthetic EEG data for training the seizure detection model.
Uses signal processing techniques to simulate normal and seizure EEG patterns.

In production, replace with real EEG datasets like:
- CHB-MIT Scalp EEG Database
- Bonn University EEG Database
- TUH EEG Seizure Corpus
"""

import numpy as np
import os
from typing import Tuple


def generate_normal_eeg(
    num_samples: int,
    sequence_length: int = 178,
    num_channels: int = 1,
    sampling_rate: int = 256,
) -> np.ndarray:
    """Generate synthetic normal (non-seizure) EEG signals.

    Normal EEG is characterized by:
    - Alpha waves (8-13 Hz) dominant in relaxed states
    - Beta waves (13-30 Hz) in active states
    - Low amplitude, rhythmic patterns
    - Random noise floor
    """
    data = np.zeros((num_samples, sequence_length, num_channels))
    t = np.linspace(0, sequence_length / sampling_rate, sequence_length)

    for i in range(num_samples):
        for ch in range(num_channels):
            # Alpha wave (8-13 Hz) - dominant rhythm
            alpha_freq = np.random.uniform(8, 13)
            alpha_amp = np.random.uniform(20, 50)
            alpha = alpha_amp * np.sin(2 * np.pi * alpha_freq * t)

            # Beta wave (13-30 Hz) - lower amplitude
            beta_freq = np.random.uniform(13, 30)
            beta_amp = np.random.uniform(5, 15)
            beta = beta_amp * np.sin(2 * np.pi * beta_freq * t + np.random.uniform(0, 2 * np.pi))

            # Theta wave (4-8 Hz) - occasional
            theta_freq = np.random.uniform(4, 8)
            theta_amp = np.random.uniform(0, 15)
            theta = theta_amp * np.sin(2 * np.pi * theta_freq * t + np.random.uniform(0, 2 * np.pi))

            # Background noise
            noise = np.random.normal(0, 5, sequence_length)

            # Amplitude modulation
            modulation = 1 + 0.3 * np.sin(2 * np.pi * np.random.uniform(0.5, 2) * t)
            signal = (alpha + beta + theta + noise) * modulation
            data[i, :, ch] = signal

    return data


def generate_seizure_eeg(
    num_samples: int,
    sequence_length: int = 178,
    num_channels: int = 1,
    sampling_rate: int = 256,
) -> np.ndarray:
    """Generate synthetic seizure EEG signals.

    Seizure EEG is characterized by:
    - High amplitude spike-and-wave discharges
    - Rhythmic sharp transients (3-6 Hz)
    - Sudden onset with progressive evolution
    - Significantly higher power than background
    """
    data = np.zeros((num_samples, sequence_length, num_channels))
    t = np.linspace(0, sequence_length / sampling_rate, sequence_length)

    for i in range(num_samples):
        for ch in range(num_channels):
            # Spike-and-wave pattern
            spike_freq = np.random.uniform(2, 6)
            spike_amp = np.random.uniform(100, 300)
            spike = spike_amp * np.abs(np.sin(2 * np.pi * spike_freq * t))

            # Sharp wave component
            sharp_freq = np.random.uniform(10, 25)
            sharp_amp = np.random.uniform(50, 150)
            sharp = sharp_amp * np.sin(2 * np.pi * sharp_freq * t)

            # Onset envelope
            onset = int(sequence_length * np.random.uniform(0.1, 0.3))
            envelope = np.zeros(sequence_length)
            for j in range(onset, sequence_length):
                progress = (j - onset) / (sequence_length - onset)
                envelope[j] = min(1.0, progress * 2)

            # High-frequency burst
            burst_freq = np.random.uniform(15, 40)
            burst = np.random.uniform(30, 80) * np.sin(2 * np.pi * burst_freq * t)
            noise = np.random.normal(0, 10, sequence_length)

            signal = (spike + sharp) * envelope + burst * envelope * 0.5 + noise
            data[i, :, ch] = signal

    return data


def generate_dataset(
    num_normal: int = 2000,
    num_seizure: int = 2000,
    sequence_length: int = 178,
    num_channels: int = 1,
    test_split: float = 0.2,
    val_split: float = 0.1,
    seed: int = 42,
) -> Tuple[dict, dict, dict]:
    """Generate complete training/validation/test datasets."""
    np.random.seed(seed)

    normal_data = generate_normal_eeg(num_normal, sequence_length, num_channels)
    seizure_data = generate_seizure_eeg(num_seizure, sequence_length, num_channels)

    normal_labels = np.zeros(num_normal)
    seizure_labels = np.ones(num_seizure)

    X = np.concatenate([normal_data, seizure_data], axis=0)
    y = np.concatenate([normal_labels, seizure_labels], axis=0)

    indices = np.random.permutation(len(X))
    X = X[indices]
    y = y[indices]

    test_size = int(len(X) * test_split)
    X_test, y_test = X[:test_size], y[:test_size]
    X_remain, y_remain = X[test_size:], y[test_size:]

    val_size = int(len(X_remain) * val_split)
    X_val, y_val = X_remain[:val_size], y_remain[:val_size]
    X_train, y_train = X_remain[val_size:], y_remain[val_size:]

    print(f"Dataset generated:")
    print(f"  Train: {X_train.shape[0]} samples")
    print(f"  Val:   {X_val.shape[0]} samples")
    print(f"  Test:  {X_test.shape[0]} samples")
    print(f"  Input shape: {X_train.shape[1:]}")
    print(f"  Seizure ratio: {y_train.mean():.2%}")

    train = {"x": X_train, "y": y_train}
    val = {"x": X_val, "y": y_val}
    test = {"x": X_test, "y": y_test}

    return train, val, test


def save_dataset(train, val, test, output_dir="ml/data"):
    """Save datasets to numpy compressed file."""
    os.makedirs(output_dir, exist_ok=True)
    np.savez_compressed(
        os.path.join(output_dir, "eeg_dataset.npz"),
        x_train=train["x"], y_train=train["y"],
        x_val=val["x"], y_val=val["y"],
        x_test=test["x"], y_test=test["y"],
    )
    print(f"Dataset saved to {output_dir}/eeg_dataset.npz")


def load_dataset(path="ml/data/eeg_dataset.npz"):
    """Load datasets from numpy file."""
    data = np.load(path)
    train = {"x": data["x_train"], "y": data["y_train"]}
    val = {"x": data["x_val"], "y": data["y_val"]}
    test = {"x": data["x_test"], "y": data["y_test"]}
    print(f"Dataset loaded from {path}")
    return train, val, test


if __name__ == "__main__":
    train, val, test = generate_dataset()
    save_dataset(train, val, test)
