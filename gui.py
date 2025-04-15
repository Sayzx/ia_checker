import tkinter as tk
from tkinter import messagebox
from board import Board

class GUI:
    def __init__(self, root, game, restart_callback=None):
        self.game = game
        self.root = root
        self.restart_callback = restart_callback
        self.root.title("Jeu de Dames")
        self.root.attributes('-fullscreen', True)

        self.cell_size = 100
        board_size = self.cell_size * 8

        # Frame principale
        main_frame = tk.Frame(root, bg="#2b2b2b")
        main_frame.pack(padx=20, pady=20, side=tk.TOP)

        # Canvas pour le plateau
        self.canvas = tk.Canvas(main_frame, width=board_size, height=board_size, bg="lightgray", highlightthickness=0)
        self.canvas.grid(row=0, column=0, padx=20)

        # Frame droite pour status + boutons + historique
        side_frame = tk.Frame(main_frame, bg="#2b2b2b", width=400)
        side_frame.grid(row=0, column=1, sticky="ns")
        side_frame.grid_propagate(False)

        self.status_label = tk.Label(
            side_frame, text="Bienvenue au jeu de dames !",
            font=("Helvetica", 18), fg="white", bg="#2b2b2b", anchor=tk.W, wraplength=380, justify=tk.LEFT, height=4
        )
        self.status_label.pack(fill=tk.X, pady=10, padx=10)

        button_style = {"font": ("Helvetica", 16), "bg": "#444", "fg": "white",
                        "activebackground": "#666", "padx": 20, "pady": 10, "bd": 0, "relief": tk.FLAT}

        tk.Button(side_frame, text="Nouvelle Partie", command=self.new_game, **button_style).pack(pady=10, fill=tk.X, padx=10)
        tk.Button(side_frame, text="Abandonner", command=self.resign_game, **button_style).pack(pady=10, fill=tk.X, padx=10)
        tk.Button(side_frame, text="Quitter", command=root.quit, **button_style).pack(pady=10, fill=tk.X, padx=10)

        # Zone historique des coups
        self.history_label = tk.Label(side_frame, text="Historique des coups:", font=("Helvetica", 14), fg="white", bg="#2b2b2b")
        self.history_label.pack(pady=(20, 0), padx=10, anchor="w")

        self.history_text = tk.Text(side_frame, height=15, width=45, font=("Courier", 12), bg="#1e1e1e", fg="white", wrap=tk.WORD)
        self.history_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        self.history_text.config(state=tk.DISABLED)

        self.board = self.game.board
        self.selected_piece = None
        self.canvas.bind("<Button-1>", self.on_click)
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(8):
            for col in range(8):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                color = "#FFCE9E" if (row + col) % 2 == 0 else "#D18B47"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

                piece = self.board.board[row][col]
                if piece:
                    self.draw_piece(row, col, piece)

        if self.board.mandatory_jump_piece:
            row, col = self.board.mandatory_jump_piece
            x1 = col * self.cell_size
            y1 = row * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="orange", width=4)

    def draw_piece(self, row, col, piece):
        x_center = col * self.cell_size + self.cell_size // 2
        y_center = row * self.cell_size + self.cell_size // 2
        radius = self.cell_size // 2 - 10

        color = "black" if piece[0] == 'N' else "white"
        outline_color = "white" if piece[0] == 'N' else "black"

        self.canvas.create_oval(
            x_center - radius, y_center - radius,
            x_center + radius, y_center + radius,
            fill=color, outline=outline_color, width=4
        )

        if "D" in piece:
            self.canvas.create_text(
                x_center, y_center,
                text="♛", font=("Arial", 32),
                fill="gold" if piece[0] == 'N' else "darkgoldenrod"
            )

    def highlight_selected_piece(self, row, col):
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="blue", width=4)

    def highlight_possible_moves(self, row, col):
        self.canvas.delete("highlight")
        piece = self.board.board[row][col]
        if not piece:
            return

        valid_moves = self.board.get_valid_moves(row, col)
        filtered_moves = [
            (r, c) for (r, c) in valid_moves
            if self.board.is_valid_move((row, col), (r, c))
        ]

        for move_row, move_col in filtered_moves:
            x_center = move_col * self.cell_size + self.cell_size // 2
            y_center = move_row * self.cell_size + self.cell_size // 2
            self.canvas.create_oval(
                x_center - 20, y_center - 20,
                x_center + 20, y_center + 20,
                outline="lime", width=3, tags="highlight"
            )

    def on_click(self, event):
        if self.game.game_over:
            return
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        self.game.handle_click(row, col)

    def update_status(self, message):
        self.status_label.config(text=message)

    def append_history(self, move_description):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.insert(tk.END, move_description + "\n")
        self.history_text.yview(tk.END)
        self.history_text.config(state=tk.DISABLED)

    def update_capture_count(self, captured_black, captured_white):
        self.root.title(f"Dames - Noirs capturés: {captured_black}, Blancs capturés: {captured_white}")

    def new_game(self):
        if messagebox.askyesno("Nouvelle partie", "Voulez-vous vraiment recommencer ?"):
            if self.restart_callback:
                self.root.destroy()
                self.restart_callback()


    def resign_game(self):
        if not self.game.game_over:
            if messagebox.askyesno("Abandonner", "Êtes-vous sûr de vouloir abandonner ?"):
                self.game.game_over = True
                self.game.update_status_message("Vous avez abandonné. L'IA gagne!")
                self.game.end_game()
