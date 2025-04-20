import random
import pandas as pd
import os

class CheckersAI:
    def __init__(self, history_file="data/game_history.csv"):
        self.history_file = history_file
        self.history_data = self.load_history()

    def load_history(self):
        if not os.path.exists(self.history_file):
            return None

        try:
            df = pd.read_csv(self.history_file, encoding='utf-8-sig')
        except Exception as e:
            print(f"❌ Erreur de lecture du fichier CSV : {e}")
            return None

        df.columns = df.columns.str.strip().str.lower()
        expected = {"turn", "start", "end", "player", "captured piece"}

        if not expected.issubset(set(df.columns)):
            print("❌ Colonnes manquantes :", expected - set(df.columns))
            return None

        return df

    def evaluate_moves(self, board, player, valid_moves):
        move_scores = {(start, end): 0 for start, end in valid_moves}

        for start, end in valid_moves:
            score = 0

            # Stratégie : aller vers le centre
            if 2 <= end[0] <= 5 and 2 <= end[1] <= 5:
                score += 2

            # Stratégie : capture
            if hasattr(board, 'is_capture_move') and board.is_capture_move(start, end):
                score += 10

            # Stratégie : promotion
            if player == "N" and end[0] == 0:
                score += 5
            elif player == "B" and end[0] == 7:
                score += 5

            # Éviter les bords
            if end[1] in [0, 7]:
                score -= 1

            # Analyse de l'historique
            if self.history_data is not None:
                filtered = self.history_data[
                    (self.history_data["start"] == str(start)) &
                    (self.history_data["end"] == str(end)) &
                    (self.history_data["player"] == player)
                ]

                wins = 0
                total = 0
                current_winner = None

                for _, row in filtered.iterrows():
                    turn = row["turn"]
                    if isinstance(turn, str) and "résultat" in turn.lower():
                        current_winner = str(row["captured piece"]).strip()
                    elif str(turn).isdigit():
                        if current_winner:
                            if (player == "N" and current_winner == "IA") or (player == "B" and current_winner == "Joueur"):
                                wins += 1
                            total += 1

                if total > 0:
                    score += (wins / total) * 5  # pondération max +5

            move_scores[(start, end)] = score

        return move_scores

    def get_best_move(self, board, player="N"):
        """
        Determines the best move for the given player on the current board.
        This function identifies all valid moves available for the player, evaluates each move
        using the evaluate_moves method, and selects one of the moves with the highest score.
        If multiple moves have the same highest score, one is chosen randomly.
        Args:
            board: The game board object containing the current state of the game.
            player (str, optional): The player identifier ('N' for black by default).
        Returns:
            tuple or None: A tuple containing the source position ((row, col)) and the 
            destination position, representing the best move. Returns None if no valid 
            moves are available.
        """
        valid_moves = []

        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]
                if piece and piece[0] == player:
                    moves = board.get_valid_moves(row, col)
                    for move in moves:
                        valid_moves.append(((row, col), move))

        if not valid_moves:
            return None

        scored_moves = self.evaluate_moves(board, player, valid_moves)
        max_score = max(scored_moves.values())
        best_moves = [move for move, score in scored_moves.items() if score == max_score]
        return random.choice(best_moves)
