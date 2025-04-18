# -*- coding: utf-8 -*-
"""Spotify Neural Network.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HGQaa1f2edrWFpRjUSL6likhgGSh3hH6
"""

from google.colab import files
uploaded = files.upload()

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import matplotlib.pyplot as plt

df = pd.read_csv('dataset.csv')
#genres = ["Acoustic", "Pop", "Rock", "Hip-Hop", "Jazz"]
#df['track_genre'] = df['track_genre'].str.lower()
#genres = [genre.lower() for genre in genres]
#df = df[df['track_genre'].isin(genres)]

if df.empty:
    print("Error: DataFrame is empty after filtering. Check if the specified genres exist in the dataset.")
else:
    features = ['danceability', 'energy', 'valence', 'tempo',
                'acousticness', 'instrumentalness', 'loudness',
                'speechiness', 'duration_ms']
    X = df[features]
    y = df['popularity']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    max_popularity = y.max()
    y_reflected = max_popularity - y
    y_transformed = np.log1p(y_reflected)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_transformed, test_size=0.2, random_state=42)


    model = Sequential([
        Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
        Dense(64, activation='relu'),
        Dense(32, activation='relu'),
        Dense(1)
    ])

    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

    history = model.fit(X_train, y_train, epochs=32, batch_size=32, validation_split=0.2)

    test_loss, test_mae = model.evaluate(X_test, y_test)
    print(f"Test MAE (in transformed space): {test_mae:.4f}")

    y_pred_transformed = model.predict(X_test)
    y_pred = max_popularity - np.expm1(y_pred_transformed)
    y_actual = max_popularity - np.expm1(y_test)

    # Training Loss Plot
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Val Loss')
    plt.legend()
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.title("Training History")
    plt.show()

    # Scatter Plot of Predicted vs Actual
    plt.figure(figsize=(8, 6))
    plt.scatter(y_actual, y_pred, alpha=0.5)
    plt.xlabel("Actual Popularity")
    plt.ylabel("Predicted Popularity")
    plt.title("Predicted vs Actual Popularity")
    plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--')
    plt.grid(True)
    plt.show()

    from sklearn.metrics import mean_absolute_error

test_loss, test_mae = model.evaluate(X_test, y_test)
print(f"Test Loss: {test_loss:.4f}")
print(f"Test MAE: {test_mae:.4f}")

def predict_song_popularity(model, scaler, max_popularity):
    print("Enter the song's features:")

    danceability = float(input("Danceability (0 - 1): "))
    energy = float(input("Energy (0 - 1): "))
    valence = float(input("Valence (0 - 1): "))
    tempo = float(input("Tempo (BPM): "))
    acousticness = float(input("Acousticness (0 - 1): "))
    instrumentalness = float(input("Instrumentalness (0 - 1): "))
    loudness = float(input("Loudness (dB): "))
    speechiness = float(input("Speechiness (0 - 1): "))
    duration_ms = float(input("Duration (ms): "))

    input_data = pd.DataFrame({
        'danceability': [danceability],
        'energy': [energy],
        'valence': [valence],
        'tempo': [tempo],
        'acousticness': [acousticness],
        'instrumentalness': [instrumentalness],
        'loudness': [loudness],
        'speechiness': [speechiness],
        'duration_ms': [duration_ms]
    })

    input_scaled = scaler.transform(input_data)

    predicted_transformed = model.predict(input_scaled)

    predicted_popularity = max_popularity - np.expm1(predicted_transformed)

    print(f"Predicted Popularity: {predicted_popularity[0][0]:.2f}")

predict_song_popularity(model, scaler, max_popularity)

import seaborn as sns
import matplotlib.pyplot as plt

features = ['danceability', 'energy', 'valence', 'tempo',
            'acousticness', 'instrumentalness', 'loudness',
            'speechiness', 'duration_ms', 'popularity']

corr_matrix = df[features].corr()

plt.figure(figsize=(10, 8))

sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True)

plt.title("Feature Correlation Heatmap")
plt.show()