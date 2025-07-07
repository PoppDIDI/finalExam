# train_model.py

from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
from preprocessing import load_and_preprocess_data

def build_model():
    """
    Modèle MLP pour Tic Tac Toe
    Entrée 9 cases
    Sortie 9 probabilités (softmax)
    """
    model = keras.Sequential([
        layers.Dense(64, activation="relu", input_shape=(9,)),
        layers.Dense(32, activation="relu"),
        layers.Dense(9, activation="softmax")
    ])

    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model

if __name__ == "__main__":
    # Charger le dataset
    X, y = load_and_preprocess_data("../data/tic_tac_toe_records_minimax.csv")

    # Découper en train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Construire le modèle
    model = build_model()

    # Entraîner
    model.fit(
        X_train, y_train,
        epochs=20,
        batch_size=32,
        validation_data=(X_test, y_test)
    )

    # Sauvegarder
    model.save("../models/mlp_tictactoe.h5")

    print("Modèle sauvegardé dans models/mlp_tictactoe.h5")
