# gui.py

import tkinter as tk
from tkinter import messagebox
import numpy as np
import random
from tensorflow.keras.models import load_model
import os

class TicTacToeApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe - Humain vs IA")

        # gestion cross-platform maximisation
        try:
            self.window.state('zoomed')  # Windows
        except:
            try:
                self.window.attributes('-zoomed', True)  # Linux
            except:
                pass  # on ignore si aucune des deux ne marche

        self.window.configure(bg="#f0f0f0")

        self.main_frame = tk.Frame(self.window, bg="#f0f0f0")
        self.main_frame.pack(expand=True, fill='both')

        self.player_score = 0
        self.ai_score = 0
        self.draw_score = 0

        self.difficulty = "Facile"

        # chemin robuste vers le modèle
        current_dir = os.path.dirname(__file__)
        model_path = os.path.join(current_dir, "models/mlp_tictactoe.h5")
        self.model = load_model(model_path)

        self.show_welcome_screen()
        self.window.mainloop()

    def show_welcome_screen(self):
        self.clear_main_frame()

        label = tk.Label(
            self.main_frame, text="TIC TAC TOE",
            font=("Helvetica", 50, "bold"), bg="#f0f0f0", fg="#333333"
        )
        label.pack(pady=50)

        diff_label = tk.Label(
            self.main_frame, text="Choisissez la difficulté",
            font=("Helvetica", 22), bg="#f0f0f0", fg="#555555"
        )
        diff_label.pack(pady=20)

        button_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        button_frame.pack()

        for level in ["Facile", "Moyen", "Difficile"]:
            b = tk.Button(
                button_frame, text=level, font=("Helvetica", 18, "bold"),
                width=15, height=2,
                bg="#4CAF50", fg="white", activebackground="#45A049",
                relief="flat",
                command=lambda lvl=level: self.set_difficulty(lvl)
            )
            b.pack(pady=10)

    def set_difficulty(self, level):
        self.difficulty = level
        self.start_game()

    def start_game(self):
        self.clear_main_frame()

        self.current_player = "X"
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        grid_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        grid_frame.pack(expand=True)

        size = 200
        for i in range(3):
            grid_frame.rowconfigure(i, weight=1, minsize=size)
            grid_frame.columnconfigure(i, weight=1, minsize=size)

        for i in range(3):
            for j in range(3):
                b = tk.Button(
                    grid_frame, text="", font=("Helvetica", 50, "bold"),
                    width=3, height=1, bg="white", fg="#333333",
                    activebackground="#e0e0e0",
                    relief="groove",
                    command=lambda r=i, c=j: self.on_click(r, c)
                )
                b.grid(row=i, column=j, sticky="nsew", padx=10, pady=10)
                self.buttons[i][j] = b

        self.score_label = tk.Label(
            self.main_frame,
            text=self.get_score_text(),
            font=("Helvetica", 20, "bold"),
            bg="#f0f0f0", fg="#333333"
        )
        self.score_label.pack(pady=20)

        button_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        button_frame.pack(pady=10)

        replay_button = tk.Button(
            button_frame, text="Rejouer", font=("Helvetica", 16, "bold"),
            bg="#2196F3", fg="white", activebackground="#1976D2",
            width=12, height=1, relief="flat",
            command=self.start_game
        )
        replay_button.pack(side="left", padx=10)

        back_button = tk.Button(
            button_frame, text="Accueil", font=("Helvetica", 16, "bold"),
            bg="#9E9E9E", fg="white", activebackground="#757575",
            width=12, height=1, relief="flat",
            command=self.show_welcome_screen
        )
        back_button.pack(side="left", padx=10)

    def on_click(self, row, col):
        if self.buttons[row][col]["text"] == "":
            self.buttons[row][col]["text"] = "X"
            self.buttons[row][col]["fg"] = "#E91E63"

            if self.check_winner("X"):
                self.player_score += 1
                messagebox.showinfo("Fin", "Vous avez gagné !")
                self.start_game()
            elif self.is_draw():
                self.draw_score += 1
                messagebox.showinfo("Fin", "Match nul !")
                self.start_game()
            else:
                self.window.after(300, self.ai_move)

    # def ai_move(self):
    #     self.ai_predict()
    def ai_move(self):
        if self.difficulty == "Facile":
            self.ai_random()
        elif self.difficulty == "Moyen":
            # probabilité de jouer aléatoire
            if random.random() < 0.3:
                self.ai_random()
            else:
                self.ai_predict()
        else:  # Difficile
            self.ai_predict()

    def ai_predict(self):
        # encoder le plateau
        board_state = []
        for i in range(3):
            for j in range(3):
                text = self.buttons[i][j]["text"]
                if text == "X":
                    board_state.append(1)
                elif text == "O":
                    board_state.append(-1)
                else:
                    board_state.append(0)

        input_board = np.array(board_state).reshape(1, 9)

        # prédire
        prediction = self.model.predict(input_board, verbose=0)
        move = np.argmax(prediction)

        # traduire l'index en (row,col)
        row, col = divmod(move, 3)

        # vérifier si la case est libre
        if self.buttons[row][col]["text"] == "":
            self.buttons[row][col]["text"] = "O"
            self.buttons[row][col]["fg"] = "#3F51B5"
            if self.check_winner("O"):
                self.ai_score += 1
                messagebox.showinfo("Fin", "L'IA a gagné !")
                self.start_game()
            elif self.is_draw():
                self.draw_score += 1
                messagebox.showinfo("Fin", "Match nul !")
                self.start_game()
        else:
            # fallback aléatoire si le modèle propose une case déjà occupée
            self.ai_random()

    def ai_random(self):
        empty = [(i, j) for i in range(3) for j in range(3) if self.buttons[i][j]["text"] == ""]
        if empty:
            row, col = random.choice(empty)
            self.buttons[row][col]["text"] = "O"
            self.buttons[row][col]["fg"] = "#3F51B5"
            if self.check_winner("O"):
                self.ai_score += 1
                messagebox.showinfo("Fin", "L'IA a gagné !")
                self.start_game()
            elif self.is_draw():
                self.draw_score += 1
                messagebox.showinfo("Fin", "Match nul !")
                self.start_game()

    def check_winner(self, player):
        for i in range(3):
            if all(self.buttons[i][j]["text"] == player for j in range(3)):
                return True
            if all(self.buttons[j][i]["text"] == player for j in range(3)):
                return True
        if all(self.buttons[i][i]["text"] == player for i in range(3)):
            return True
        if all(self.buttons[i][2 - i]["text"] == player for i in range(3)):
            return True
        return False

    def is_draw(self):
        return all(self.buttons[i][j]["text"] != "" for i in range(3) for j in range(3))

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def get_score_text(self):
        return f"Score - Vous: {self.player_score} | IA: {self.ai_score} | Nuls: {self.draw_score}"

if __name__ == "__main__":
    TicTacToeApp()
