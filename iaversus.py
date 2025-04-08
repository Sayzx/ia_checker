import tkinter as tk
from game import Game
from ia import CheckersAI

class IAVersus:
    def __init__(self, root, speed_ms=500):
        self.root = root
        self.root.title("IA vs IA")
        self.root.attributes('-fullscreen', True)

        self.speed_ms = speed_ms
        self.game = Game(root)
        self.game.current_player = "B"  # Commence par IA blanche
        self.ai = CheckersAI()  # Utilisation directe

        self.add_controls()
        self.start_loop()

    def add_controls(self):
        control_frame = tk.Frame(self.root, bg="#2b2b2b")
        control_frame.place(relx=0.99, rely=0.01, anchor="ne")

        button_style = {
            "font": ("Helvetica", 12), "bg": "#444", "fg": "white",
            "activebackground": "#666", "padx": 10, "pady": 5, "bd": 0, "relief": tk.FLAT
        }

        tk.Label(control_frame, text="Vitesse", fg="white", bg="#2b2b2b", font=("Helvetica", 10)).pack(pady=(10, 0))
        self.speed_scale = tk.Scale(control_frame, from_=100, to=2000, resolution=100, orient=tk.HORIZONTAL,
                                    bg="#2b2b2b", fg="white", troughcolor="#555", highlightthickness=0,
                                    length=150, command=self.set_speed)
        self.speed_scale.set(self.speed_ms)
        self.speed_scale.pack()

        tk.Button(control_frame, text="Quitter", command=self.root.quit, **button_style).pack(pady=10)

    def set_speed(self, val):
        self.speed_ms = int(val)

    def start_loop(self):
        if self.game.game_over:
            self.game.end_game()
            return

        player = self.game.current_player

        if not self.game.board.has_valid_moves(player):
            self.game.update_status_message(f"IA {player} ne peut plus jouer.")
            self.game.end_game()
            return

        self.game.update_status_message(f"IA {player} réfléchit...")
        self.root.update()

        move = self.ai.get_best_move(self.game.board, player=player)
        if not move:
            self.game.end_game()
            return

        start, end = move
        print(f"IA {player} joue : {start} -> {end}")
        self.game.gui.append_history(f"IA {player} joue : {start} -> {end}")

        success, multiple_capture = self.game.move_piece(start, end)
        if success:
            self.game.moves_history.append((start, end))
            self.game.stats.record_move(player, f"{start}->{end}")
            self.game.gui.draw_board()
            self.game.gui.update_capture_count(self.game.board.captured_black, self.game.board.captured_white)

            if multiple_capture:
                self.root.after(self.speed_ms, self.start_loop)
                return

            self.game.current_player = "B" if player == "N" else "N"
            self.root.after(self.speed_ms, self.start_loop)
        else:
            self.game.end_game()


def start_ia_vs_ia():
    root = tk.Tk()
    app = IAVersus(root)
    root.mainloop()
