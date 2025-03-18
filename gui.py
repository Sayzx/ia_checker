import tkinter as tk

class GUI:
    def __init__(self, root, game):
        self.game = game
        self.root = root
        self.root.title("Dames")
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()

        self.board = self.game.board
        self.selected_piece = None
        self.draw_board()

        self.canvas.bind("<Button-1>", self.on_click)

    def draw_board(self):
        """Dessine le plateau de jeu avec des couleurs marron et beige"""
        self.canvas.delete("all")
        for row in range(8):
            for col in range(8):
                x1 = col * 50
                y1 = row * 50
                x2 = x1 + 50
                y2 = y1 + 50
                color = "beige" if (row + col) % 2 == 0 else "maroon"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

                piece = self.board.board[row][col]
                if piece:
                    self.draw_piece(row, col, piece)

    def draw_piece(self, row, col, piece):
        """Dessine un pion noir ou blanc, ou une dame"""
        x1 = col * 50 + 10
        y1 = row * 50 + 10
        x2 = x1 + 30
        y2 = y1 + 30
        if piece == 'N':
            color = "black"
        elif piece == 'B':
            color = "white"
        elif piece == 'ND':
            color = "black"
            self.canvas.create_text(x1 + 15, y1 + 15, text="D", fill="white", font=("Arial", 12))
        elif piece == 'BD':
            color = "white"
            self.canvas.create_text(x1 + 15, y1 + 15, text="D", fill="black", font=("Arial", 12))
        self.canvas.create_oval(x1, y1, x2, y2, fill=color)

    def highlight_possible_moves(self, start):
        """Met en surbrillance les cases où un pion peut se déplacer"""
        row, col = start
        valid_moves = self.board.get_valid_moves(row, col)
        for move in valid_moves:
            x1 = move[1] * 50 + 10
            y1 = move[0] * 50 + 10
            x2 = x1 + 30
            y2 = y1 + 30
            self.canvas.create_oval(x1, y1, x2, y2, outline="green", width=3)

    def on_click(self, event):
        """Gère le clic sur une case"""
        if self.game.current_player != "B":  # Vérifie que c'est au tour du joueur
            print("Ce n'est pas votre tour !")
            return

        col = event.x // 50
        row = event.y // 50
        piece = self.board.board[row][col]

        if self.selected_piece:  # Si un pion est sélectionné, essaye de le déplacer
            if self.game.move_piece(self.selected_piece, (row, col)):  # Appelle Game.move_piece
                self.selected_piece = None  # Désélectionne le pion
                self.draw_board()  # Met à jour l'affichage du plateau
            else:
                self.selected_piece = None  # Annule la sélection si le mouvement est invalide
                self.draw_board()  # Met à jour l'affichage du plateau
        elif piece == 'B':  # Seuls les pions blancs peuvent être sélectionnés
            self.selected_piece = (row, col)
            self.highlight_possible_moves(self.selected_piece)  # Affiche les mouvements possibles
    def update_capture_count(self, captured_black, captured_white):
        """Mise à jour du compteur de pions capturés"""
        self.root.title(f"Dames - Noirs capturés: {captured_black}, Blancs capturés: {captured_white}")