
import tkinter as tk
import pandas as pd
import ast
from board import Board
from gui import GUI

class ReplayGameWrapper:
    def __init__(self, root, moves):
        self.root = root
        self.moves = moves
        self.board = Board()
        self.canvas = None
        self.gui = GUI(root, self)
        self.current_index = 0
        self.game_over = False

        self.create_controls()
        self.update_status("Cliquez sur ▶️ pour rejouer la partie.")

    def create_controls(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=5)

        self.next_button = tk.Button(control_frame, text="▶️ Coup Suivant", command=self.replay_next_move)
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.auto_button = tk.Button(control_frame, text="⏩ Lecture Auto", command=self.start_auto_replay)
        self.auto_button.pack(side=tk.LEFT, padx=5)

    def update_status(self, message):
        self.gui.update_status(message)

    def replay_next_move(self):
        if self.current_index >= len(self.moves):
            self.update_status("🎉 Relecture terminée !")
            return

        move = self.moves.iloc[self.current_index]
        try:
            start = ast.literal_eval(move["Start"])
            end = ast.literal_eval(move["End"])
            player = move["Player"]
        except Exception as e:
            self.update_status(f"⚠️ Erreur parsing du coup {self.current_index}: {e}")
            return

        success, _ = self.board.move_piece(start, end)
        if not success:
            self.update_status(f"⚠️ Mouvement invalide : {player} {start} → {end}")
        else:
            self.gui.draw_board()
            self.gui.update_status(f"{player} : {start} → {end}")

        self.current_index += 1

    def start_auto_replay(self):
        if self.current_index < len(self.moves):
            self.replay_next_move()
            self.root.after(1000, self.start_auto_replay)
        else:
            self.update_status("🎉 Relecture automatique terminée !")

def replay_game_visual(csv_file="data/game_history.csv"):
    try:
        df = pd.read_csv(csv_file)

        result_indexes = df[df["Turn"] == "Résultat"].index.tolist()
        if not result_indexes:
            print("Aucune fin de partie trouvée.")
            return

        start_index = result_indexes[-2] + 1 if len(result_indexes) >= 2 else 0
        end_index = result_indexes[-1]

        df = df.iloc[start_index:end_index]
        df = df[df["Player"].isin(["B", "N"])].reset_index(drop=True)

        if df.empty:
            print("Aucune partie récente trouvée.")
            return

        root = tk.Tk()
        root.title("Rejouer une partie")
        app = ReplayGameWrapper(root, df)
        root.mainloop()

    except Exception as e:
        print("Erreur pendant la relecture :", e)
