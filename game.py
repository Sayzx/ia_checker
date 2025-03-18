import pandas as pd
import random
import os
from board import Board
from gui import GUI
from ia import CheckersAI  

class Game:
    def __init__(self, root):
        self.board = Board()
        self.gui = GUI(root, self)
        self.ai = CheckersAI() 
        self.current_player = "N"
        self.selected_piece = None
        self.moves_history = []
        self.load_game_from_excel("game_history.xlsx")

    def get_ai_move(self):
        return self.ai.get_best_move(self.board)
    
    def ai_turn(self):
        if self.current_player == "N":  # L'IA joue les pions noirs
            best_move = self.ai.get_best_move(self.board)
            if best_move is None:
                print("L'IA n'a pas trouvé de coup valide.")
                return

            start, end = best_move
            print(f"L'IA joue : {start} -> {end}")
            self.move_piece(start, end)

    
    
    def move_piece(self, start, end):
        """Effectue un mouvement de pion"""
        if not self.board.move_piece(start, end):
            return False

        # Change le joueur actif
        self.current_player = "B" if self.current_player == "N" else "N"
        print(f"Tour actuel : {self.current_player}")  # Log pour vérifier le tour
        self.moves_history.append((start, end))

        # Vérifie si la partie est terminée
        if not self.board.has_valid_moves(self.current_player):
            print(f"Le joueur {self.current_player} n'a plus de mouvements possibles. Partie terminée !")
            self.save_game_to_excel()
            self.gui.root.quit()  # Ferme la fenêtre de jeu

        self.gui.update_capture_count(self.board.captured_black, self.board.captured_white)
        self.gui.draw_board()  # Met à jour l'affichage du plateau

        # Si c'est au tour de l'IA, elle joue automatiquement
        if self.current_player == "N":
            print("C'est au tour de l'IA de jouer.")  # Log pour vérifier l'appel de l'IA
            self.gui.root.after(500, self.ai_turn)  # L'IA joue après un délai de 500ms

        return True

    def select_piece(self, start):
        self.selected_piece = start
        self.gui.highlight_possible_moves(start)

    def save_game_to_excel(self):
        game_data = []
        for move in self.moves_history:
            start, end = move
            game_data.append({
                "Start Position": start,
                "End Position": end,
                "Captured Black": self.board.captured_black,
                "Captured White": self.board.captured_white,
                "Current Player": self.current_player
            })

        df = pd.DataFrame(game_data)
        if not os.path.exists("game_history.xlsx"):
            df.to_excel("game_history.xlsx", index=False)
        else:
            with pd.ExcelWriter("game_history.xlsx", mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
                df.to_excel(writer, index=False, sheet_name=f"Game_{len(self.moves_history)}")

    def load_game_from_excel(self, file_name):
        """Charge une partie depuis un fichier Excel et rejoue les mouvements"""
        if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
            df = pd.read_excel(file_name)
            for index, row in df.iterrows():
                start = row['Start Position']
                end = row['End Position']
                self.move_piece(start, end)
                self.gui.update_capture_count(self.board.captured_black, self.board.captured_white)
                self.gui.draw_board()
        else:
            # Si le fichier est vide ou n'existe pas, initialise la partie et fait jouer l'IA
            print("Aucune partie précédente trouvée. L'IA commence à jouer.")
            self.ai_turn()