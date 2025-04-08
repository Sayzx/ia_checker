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
        self.replay_speed = 1000

        self.add_replay_controls()
        self.update_status("Cliquez sur ▶️ pour rejouer la partie.")

    def add_replay_controls(self):
        control_frame = tk.Frame(self.root, bg="#2b2b2b")
        control_frame.place(relx=0.99, rely=0.01, anchor="ne")

        button_style = {
            "font": ("Helvetica", 12), "bg": "#444", "fg": "white",
            "activebackground": "#666", "padx": 10, "pady": 5, "bd": 0, "relief": tk.FLAT
        }

        self.next_button = tk.Button(control_frame, text="▶️ Coup Suivant", command=self.replay_next_move, **button_style)
        self.next_button.pack(side=tk.TOP, pady=2)

        self.auto_button = tk.Button(control_frame, text="⏩ Lecture Auto", command=self.start_auto_replay, **button_style)
        self.auto_button.pack(side=tk.TOP, pady=2)

        tk.Label(control_frame, text="Vitesse", fg="white", bg="#2b2b2b", font=("Helvetica", 10)).pack(pady=(10, 0))
        self.speed_scale = tk.Scale(control_frame, from_=200, to=2000, resolution=100, orient=tk.HORIZONTAL,
                                    bg="#2b2b2b", fg="white", troughcolor="#555", highlightthickness=0,
                                    length=150, command=self.set_speed)
        self.speed_scale.set(self.replay_speed)
        self.speed_scale.pack()

    def set_speed(self, val):
        self.replay_speed = int(val)

    def update_status(self, message):
        self.gui.update_status(message)

    def replay_next_move(self):
        if self.current_index >= len(self.moves):
            self.update_status("🎉 Relecture terminée !")
            return

        move = self.moves.iloc[self.current_index]
        try:
            start = ast.literal_eval(str(move["start"]))
            end = ast.literal_eval(str(move["end"]))
            player = move["player"]
        except Exception as e:
            self.update_status(f"⚠️ Erreur parsing du coup {self.current_index}: {e}")
            return

        success, _ = self.board.move_piece(start, end)
        if not success:
            self.update_status(f"⚠️ Mouvement invalide : {player} {start} → {end}")
        else:
            self.gui.draw_board()
            self.gui.update_status(f"{player} : {start} → {end}")
            if hasattr(self.gui, 'append_history'):
                label = "Le joueur joue" if player == 'B' else "L'IA joue"
                self.gui.append_history(f"{label} : {start} -> {end}")

        self.current_index += 1

    def start_auto_replay(self):
        if self.current_index < len(self.moves):
            self.replay_next_move()
            self.root.after(self.replay_speed, self.start_auto_replay)
        else:
            self.update_status("🎉 Relecture automatique terminée !")

def select_game_to_replay(csv_file="data/game_history.csv"):
    try:
        df = pd.read_csv(csv_file)
        df.columns = df.columns.str.strip().str.lower()

        start_indices = df[df["turn"].str.contains("---debut-partie", na=False)].index.tolist()
        end_indices = df[df["turn"].str.contains("---fin-partie", na=False)].index.tolist()

        if not start_indices or not end_indices:
            print("Aucune partie trouvée.")
            return

        games = []
        for i, (start, end) in enumerate(zip(start_indices, end_indices), 1):
            game_data = df.iloc[start+1:end]  # skip start marker
            games.append((i, game_data))

        root = tk.Tk()
        root.title("Sélectionner une partie")
        root.geometry("400x300")

        tk.Label(root, text="Choisissez une partie à rejouer:", font=("Helvetica", 14)).pack(pady=10)
        listbox = tk.Listbox(root, font=("Courier", 12))
        listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        for i in range(len(games)):
            listbox.insert(tk.END, f"Partie {i+1}")

        def launch_replay():
            selection = listbox.curselection()
            if selection:
                game_index = selection[0]
                root.destroy()
                replay_root = tk.Tk()
                replay_root.attributes('-fullscreen', True)
                ReplayGameWrapper(replay_root, games[game_index][1])
                replay_root.mainloop()

        tk.Button(root, text="Rejouer la partie", command=launch_replay, font=("Helvetica", 12), bg="#444", fg="white").pack(pady=10)
        root.mainloop()

    except Exception as e:
        print("Erreur pendant la sélection/relecture de partie:", e)
