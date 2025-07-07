# preprocessing.py

import pandas as pd
import numpy as np

def load_and_preprocess_data(csv_path):
    """
    Charge le fichier CSV et encode le board
    X = 1, O = -1, vide = 0
    Labels (1-9) transformés en 0-8
    """

    df = pd.read_csv(csv_path)

    boards = []
    moves = []

    for index, row in df.iterrows():
        board_str = row["board"]
        move = int(row["decision"])

        encoded_board = []
        for c in board_str:
            if c == 'X':
                encoded_board.append(1)
            elif c == 'O':
                encoded_board.append(-1)
            else:
                encoded_board.append(0)

        boards.append(encoded_board)
        moves.append(move - 1)  # on décale car softmax attend 0..8

    X = np.array(boards)
    y = np.array(moves)

    return X, y
