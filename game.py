import pandas as pd
import random
import os
from board import Board
from gui import GUI
from ia import CheckersAI
from stats import GameStats

class Game:
    def __init__(self, root):
        self.board = Board()
        self.gui = GUI(root, self)  # Initialisation correcte de l'objet GUI
        self.ai = CheckersAI()
        self.current_player = "B"  # Le joueur (blanc) commence
        self.selected_piece = None
        self.moves_history = []
        self.stats = GameStats()
        self.game_over = False

        # Initialiser la partie
        self.setup_new_game()
        
    def setup_new_game(self):
        """Configure une nouvelle partie"""
        self.update_status_message(f"À votre tour de jouer (blanc)")
        
    def update_status_message(self, message):
        """Met à jour le message de statut dans l'interface"""
        if self.gui:
            self.gui.update_status(message)
            
    def get_ai_move(self):
        """Obtient le meilleur coup de l'IA"""
        return self.ai.get_best_move(self.board)
    
    def ai_turn(self):
        """Fait jouer l'IA"""
        if self.current_player != "N":  # Vérifie que c'est bien le tour de l'IA
            return

        self.update_status_message("L'IA réfléchit...")
        self.gui.root.update()  # Mettre à jour l'interface

        best_move = self.ai.get_best_move(self.board)
        if best_move is None:
            self.game_over = True
            self.update_status_message("Partie terminée! Vous avez gagné!")
            return

        start, end = best_move
        print(f"L'IA joue : {start} -> {end}")

        success, multiple_capture = self.move_piece(start, end)

        # Ajouter le mouvement à l'historique
        self.moves_history.append((start, end))
        self.stats.record_move("N", f"{start}->{end}")

        # Mettre à jour l'affichage
        self.gui.draw_board()
        self.gui.update_capture_count(self.board.captured_black, self.board.captured_white)

        # Si capture multiple possible, continuer avec l'IA
        if multiple_capture:
            self.ai_turn()  # L'IA continue de jouer pour faire des captures multiples
        else:
            # Sinon, c'est au tour du joueur
            if self.board.has_valid_moves("B"):
                self.current_player = "B"  # Passe au joueur
                self.update_status_message("À votre tour de jouer (blanc)")
            else:
                self.game_over = True
                self.update_status_message("Partie terminée! L'IA a gagné!")
                self.end_game()

    def move_piece(self, start, end):
        """Déplace une pièce et gère les conséquences"""
        success, multiple_capture = self.board.move_piece(start, end)

        if success:
            if not multiple_capture:
                # Changer de joueur si pas de capture multiple
                self.current_player = "B" if self.current_player == "N" else "N"
            return success, multiple_capture

        return False, False

    def select_piece(self, row, col):
        """Sélectionne une pièce pour la déplacer"""
        piece = self.board.board[row][col]
        if piece and piece[0] == self.current_player:
            self.selected_piece = (row, col)
            self.gui.highlight_possible_moves(row, col)
            return True
        return False
        
    def handle_click(self, row, col):
        """Gère le clic du joueur sur le plateau"""
        if self.game_over:
            return

        if self.current_player != "B":  # Vérifie que c'est bien le tour du joueur
            self.update_status_message("Ce n'est pas votre tour!")
            return

        piece = self.board.board[row][col]

        # Si une pièce est déjà sélectionnée, essayer de la déplacer
        if self.selected_piece:
            start_row, start_col = self.selected_piece

            if (row, col) == (start_row, start_col):  # Désélectionner la pièce
                self.selected_piece = None
                self.gui.draw_board()
                return

            # Essayer de déplacer la pièce
            success, multiple_capture = self.move_piece(self.selected_piece, (row, col))

            if success:
                # Ajouter le mouvement à l'historique
                self.moves_history.append((self.selected_piece, (row, col)))
                self.stats.record_move("B", f"{self.selected_piece}->{(row, col)}")

                # Mettre à jour l'affichage
                self.gui.draw_board()
                self.gui.update_capture_count(self.board.captured_black, self.board.captured_white)

                if multiple_capture:
                    # Si capture multiple, le même joueur continue
                    self.selected_piece = (row, col)
                    self.gui.highlight_possible_moves(row, col)
                    self.update_status_message("Capture multiple possible!")
                else:
                    # Sinon, c'est au tour de l'IA
                    self.selected_piece = None
                    self.update_status_message("Au tour de l'IA...")
                    self.gui.root.after(500, self.ai_turn)  # Petite pause avant que l'IA joue
            else:
                # Mouvement invalide, garder la sélection
                self.gui.draw_board()
                self.gui.highlight_possible_moves(start_row, start_col)
                self.update_status_message("Mouvement invalide!")

        # Si aucune pièce n'est sélectionnée, essayer d'en sélectionner une
        elif piece and piece[0] == "B":
            # Vérifier si cette pièce peut être sélectionnée (capture obligatoire)
            if self.board.mandatory_jump_piece and (row, col) != self.board.mandatory_jump_piece:
                self.update_status_message("Vous devez continuer la capture avec la pièce qui vient de capturer!")
                return

            self.select_piece(row, col)
            self.update_status_message("Cliquez sur une case verte pour vous déplacer.")

    def end_game(self):
        """Termine la partie et sauvegarde les statistiques"""
        if not self.game_over:
            self.game_over = True
            
        # Vérifier qui a gagné
        if not self.board.has_valid_moves("N"):
            self.update_status_message("Partie terminée! Vous avez gagné!")
        elif not self.board.has_valid_moves("B"):
            self.update_status_message("Partie terminée! L'IA a gagné!")
        else:
            self.update_status_message("Partie terminée!")
            
        # Sauvegarder les statistiques
        self.stats.save_game()
        
        # Sauvegarder l'historique des coups
        self.save_game_to_excel()
            
    def save_game_to_excel(self):
        """Sauvegarde la partie dans un fichier Excel"""
        game_data = []
        
        for i, move in enumerate(self.moves_history):
            start, end = move
            player = "B" if i % 2 == 0 else "N"  # Joueur alterne
            
            game_data.append({
                "Turn": i + 1,
                "Player": player,
                "Start Row": start[0],
                "Start Col": start[1],
                "End Row": end[0],
                "End Col": end[1]
            })
            
        df = pd.DataFrame(game_data)
        
        # Créer le dossier data s'il n'existe pas
        if not os.path.exists("data"):
            os.makedirs("data")
            
        # Sauvegarder dans le fichier
        excel_path = "data/game_history.xlsx"
        
        # S'il existe déjà, ajouter une nouvelle feuille
        if os.path.exists(excel_path):
            with pd.ExcelWriter(excel_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                import datetime
                sheet_name = f"Game_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        else:
            df.to_excel(excel_path, sheet_name="Game_1", index=False)