import tkinter as tk
from tkinter import messagebox

class GUI:
    def __init__(self, root, game):
        self.game = game
        self.root = root
        self.root.title("Jeu de Dames")
        
        # Frame principale
        main_frame = tk.Frame(root)
        main_frame.pack(padx=10, pady=10)
        
        # Canvas pour le plateau
        self.canvas = tk.Canvas(main_frame, width=400, height=400, bg="lightgray")
        self.canvas.pack()
        
        # Frame pour le statut
        status_frame = tk.Frame(root)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Label pour afficher les messages de statut
        self.status_label = tk.Label(status_frame, text="Bienvenue au jeu de dames!", 
                                    font=("Arial", 12), bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X)
        
        # Frame pour les boutons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        
        # Boutons
        tk.Button(button_frame, text="Nouvelle Partie", command=self.new_game).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Abandonner", command=self.resign_game).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Quitter", command=root.quit).pack(side=tk.LEFT, padx=5)
        
        self.board = self.game.board
        self.selected_piece = None
        
        self.canvas.bind("<Button-1>", self.on_click)
        
        # Dessiner le plateau initial
        self.draw_board()

    def draw_board(self):
        """Dessine le plateau de jeu avec les pièces"""
        self.canvas.delete("all")
        
        # Dessiner les cases
        for row in range(8):
            for col in range(8):
                x1 = col * 50
                y1 = row * 50
                x2 = x1 + 50
                y2 = y1 + 50
                
                # Couleurs alternées
                color = "beige" if (row + col) % 2 == 0 else "saddlebrown"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                
                # Dessiner les pièces
                piece = self.board.board[row][col]
                if piece:
                    self.draw_piece(row, col, piece)
                    
        # Optionally highlight the mandatory jump piece
        if self.board.mandatory_jump_piece:
            row, col = self.board.mandatory_jump_piece
            x1 = col * 50
            y1 = row * 50
            x2 = x1 + 50
            y2 = y1 + 50
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="orange", width=3)

    def draw_piece(self, row, col, piece):
        """Dessine une pièce sur le plateau"""
        x_center = col * 50 + 25
        y_center = row * 50 + 25
        radius = 20
        
        color = "black" if piece[0] == 'N' else "white"
        outline_color = "white" if piece[0] == 'N' else "black"
        
        # Dessiner le pion
        self.canvas.create_oval(
            x_center - radius, y_center - radius,
            x_center + radius, y_center + radius,
            fill=color, outline=outline_color, width=2
        )
        
        # Si c'est une dame, ajouter une couronne
        self.canvas.create_text(
            x_center, y_center,
            text="♛", font=("Arial", 24),
            fill="gold" if piece[0] == 'N' else "yellow"
        )

    def highlight_possible_moves(self, row, col):
        """Met en évidence les mouvements possibles"""
        valid_moves = self.board.get_valid_moves(row, col)
        
        for move_row, move_col in valid_moves:
            x_center = move_col * 50 + 25
            y_center = move_row * 50 + 25
            
            # Cercle vert pour indiquer les cases disponibles
            self.canvas.create_oval(
                x_center - 15, y_center - 15,
                x_center + 15, y_center + 15,
                outline="lime", width=3, tags="highlight"
            )

    def on_click(self, event):
        """Gère les clics sur le plateau"""
        if self.game.game_over:
            return
            
        # Convertir les coordonnées du clic en indices de case
        col = event.x // 50
        row = event.y // 50
        
        # Gérer le clic
        self.game.handle_click(row, col)

    def update_status(self, message):
        """Met à jour le message de statut"""
        self.status_label.config(text=message)

    def update_capture_count(self, captured_black, captured_white):
        """Met à jour le compteur de pièces capturées"""
        self.root.title(f"Dames - Noirs capturés: {captured_black}, Blancs capturés: {captured_white}")

    def new_game(self):
        """Démarre une nouvelle partie"""
        if messagebox.askyesno("Nouvelle partie", "Voulez-vous vraiment commencer une nouvelle partie?"):
            # Réinitialiser le jeu
            self.game.board = Board()
            self.game.current_player = "B"
            self.game.selected_piece = None
            self.game.moves_history = []
            self.game.game_over = False
            self.game.setup_new_game()
            self.draw_board()

    def resign_game(self):
        """Abandonner la partie"""
        if not self.game.game_over:
            if messagebox.askyesno("Abandonner", "Voulez-vous vraiment abandonner cette partie?"):
                self.game.game_over = True
                self.game.update_status_message("Vous avez abandonné. L'IA gagne!")
                self.game.end_game()