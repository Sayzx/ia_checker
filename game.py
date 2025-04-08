import pandas as pd
import random
import os
from board import Board
from gui import GUI
from ia import CheckersAI
from stats import GameStats
from datetime import datetime

class Game:
    def __init__(self, root):
        self.board = Board()
        self.gui = GUI(root, self) 
        self.ai = CheckersAI()
        self.current_player = "B" 
        self.selected_piece = None
        self.moves_history = []
        self.stats = GameStats()
        self.game_over = False

        self.setup_new_game()
        
    def setup_new_game(self):
        self.update_status_message(f"À votre tour de jouer (blanc)")
        
    def update_status_message(self, message):
        if self.gui:
            self.gui.update_status(message)
            
    def get_ai_move(self):
        return self.ai.get_best_move(self.board)
    
    def ai_turn(self):
        if self.current_player != "N":  
            return

        self.update_status_message("L'IA réfléchit...")
        self.gui.root.update()  
        best_move = self.ai.get_best_move(self.board)
        if best_move is None:
            self.game_over = True
            self.update_status_message("Partie terminée! Vous avez gagné!")
            self.end_game() 
            return

        start, end = best_move
        print(f"L'IA joue : {start} -> {end}")
        self.gui.append_history(f"L'IA joue : {start} -> {end}")


        success, multiple_capture = self.move_piece(start, end)

        self.moves_history.append((start, end))
        self.stats.record_move("N", f"{start}->{end}")

        self.gui.draw_board()
        self.gui.update_capture_count(self.board.captured_black, self.board.captured_white)

        if multiple_capture:
            self.ai_turn()  
        else:
            if self.board.has_valid_moves("B"):
                self.current_player = "B"
                self.update_status_message("À votre tour de jouer (blanc)")
            else:
                self.game_over = True
                self.update_status_message("Partie terminée! L'IA a gagné!")
                self.end_game()

    def move_piece(self, start, end):
        try:
            success, multiple_capture = self.board.move_piece(start, end)

            if success:
                if not multiple_capture:
                    self.current_player = "B" if self.current_player == "N" else "N"
                return success, multiple_capture

            return False, False
        except Exception as e:
            self.update_status_message(f"Erreur lors du déplacement : {e}")
            return False, False

    def select_piece(self, row, col):
        piece = self.board.board[row][col]
        if piece and piece[0] == self.current_player:
            self.selected_piece = (row, col)
            self.gui.highlight_possible_moves(row, col)
            return True
        return False
        
    def handle_click(self, row, col):
        if self.game_over:
            return

        if self.current_player != "B": 
            self.update_status_message("Ce n'est pas votre tour!")
            return

        piece = self.board.board[row][col]

        if self.selected_piece:
            start_row, start_col = self.selected_piece
            

            if (row, col) == (start_row, start_col):
                self.selected_piece = None
                self.gui.draw_board()
                self.update_status_message("Pièce désélectionnée.")
                return

            success, multiple_capture = self.move_piece(self.selected_piece, (row, col))

            if success:
                self.moves_history.append((self.selected_piece, (row, col)))
                self.stats.record_move("B", f"{self.selected_piece}->{(row, col)}")
                print(f"Le joueur joue : {self.selected_piece} -> {(row, col)}")
                self.gui.append_history(f"Le joueur joue : {self.selected_piece} -> {(row, col)}")

                self.gui.draw_board()
                self.gui.update_capture_count(self.board.captured_black, self.board.captured_white)

                if multiple_capture:
                    self.selected_piece = (row, col)

                    # Vérifie s'il reste des captures à faire depuis la nouvelle position
                    valid_moves = self.board.get_valid_moves(row, col)
                    has_additional_capture = False

                    for move_row, move_col in valid_moves:
                        # On vérifie que c'est une capture (différence de 2 cases en diagonale)
                        if abs(move_row - row) == 2 and abs(move_col - col) == 2:
                            has_additional_capture = True
                            break

                    if has_additional_capture:
                        self.gui.highlight_possible_moves(row, col)
                        self.update_status_message("Capture multiple possible!")
                    else:
                        self.selected_piece = None
                        self.update_status_message("Au tour de l'IA...")
                        self.gui.root.after(500, self.ai_turn)

                else:
                    self.selected_piece = None
                    self.update_status_message("Au tour de l'IA...")
                    self.gui.root.after(500, self.ai_turn)  
            else:
                self.gui.draw_board()
                self.gui.highlight_possible_moves(start_row, start_col) 
                self.update_status_message("Mouvement invalide!")

        elif piece and piece[0] == "B":
            if self.board.mandatory_jump_piece and (row, col) != self.board.mandatory_jump_piece:
                self.update_status_message("Vous devez continuer la capture avec la pièce qui vient de capturer!")
                return

            self.select_piece(row, col)
            # mettre cette piece en jaune 
            self.gui.highlight_selected_piece(row, col) 
            self.update_status_message("Clique sur un rond vert")

    def end_game(self):
        if not self.game_over:
            self.game_over = True
            
        if not self.board.has_valid_moves("N"):
            self.update_status_message("Partie terminée! Vous avez gagné!")
        elif not self.board.has_valid_moves("B"):
            self.update_status_message("Partie terminée! L'IA a gagné!")
        else:
            self.update_status_message("Partie terminée!")
        print("Partie terminée!")
        self.stats.save_game()
        print("Sauvegarde de la partie.")
        self.save_game_to_csv()
            

    def save_game_to_csv(self):
        game_data = []

        os.makedirs("data", exist_ok=True)
        csv_path = "data/game_history.csv"

        game_id = 1
        if os.path.exists(csv_path):
            try:
                with open(csv_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    game_id = sum(1 for line in lines if line.strip().startswith("---debut-partie")) + 1
            except Exception as e:
                print(f"Erreur lors de la lecture brute du fichier : {e}")

        game_data.append({
            "Turn": f"---debut-partie{game_id}---",
            "Player": "", "Start": "", "End": "", "Captured Piece": ""
        })

        for i, move in enumerate(self.moves_history):
            start, end = move
            player = "B" if i % 2 == 0 else "N"
            captured_piece = None

            if abs(start[0] - end[0]) > 1:
                mid_row = (start[0] + end[0]) // 2
                mid_col = (start[1] + end[1]) // 2
                captured_piece = self.board.board[mid_row][mid_col]

            game_data.append({
                "Turn": i + 1,
                "Player": player,
                "Start": str(start),
                "End": str(end),
                "Captured Piece": str(captured_piece)
            })

        winner = "IA" if not self.board.has_valid_moves("B") else "Joueur"

        game_data.append({
            "Turn": "Résultat",
            "Player": "",
            "Start": "",
            "End": "",
            "Captured Piece": winner
        })

        game_data.append({
            "Turn": f"---fin-partie{game_id}---",
            "Player": "", "Start": "", "End": "", "Captured Piece": ""
        })

        df = pd.DataFrame(game_data)

        try:
            if os.path.exists(csv_path):
                df.to_csv(csv_path, mode='a', header=False, index=False)
                print(f"Données ajoutées (partie {game_id}).")
            else:
                df.to_csv(csv_path, index=False)
                print(f"Nouveau fichier créé (partie {game_id}).")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du CSV : {e}")


            