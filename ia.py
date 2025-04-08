import random
import pandas as pd
import os

class CheckersAI:
    def __init__(self, history_file="data/game_history.csv"):
        self.history_file = history_file
        self.move_scores = self.analyze_history()

    def analyze_history(self):
        if not os.path.exists(self.history_file):
            return {}

        try:
            df = pd.read_csv(self.history_file, encoding='utf-8-sig') 
        except Exception as e:
            print(f"❌ Erreur de lecture du fichier CSV : {e}")
            return {}

        df.columns = df.columns.str.strip().str.lower()
        print("✅ Colonnes détectées :", df.columns.tolist()) 

        expected = {"turn", "start", "end", "player", "captured piece"}
        actual = set(df.columns)

        if not expected.issubset(actual):
            print("❌ Colonnes manquantes dans game_history.csv")
            print("Il manque :", expected - actual)
            return {}

        move_results = {}
        current_winner = None

        for _, row in df.iterrows():
            turn = row["turn"]

            if isinstance(turn, str) and turn.startswith("---debut-partie"):
                current_winner = None

            elif isinstance(turn, str) and "résultat" in turn.lower():
                current_winner = str(row["captured piece"]).strip()

            elif str(turn).isdigit():
                start = row["start"]
                end = row["end"]
                player = row["player"]
                move_key = f"{start}->{end}"

                if current_winner and player in ["B", "N"]:
                    win = (
                        1 if player == "N" and current_winner == "IA" else
                        1 if player == "B" and current_winner == "Joueur" else
                        0
                    )

                    if move_key not in move_results:
                        move_results[move_key] = [0, 0]

                    move_results[move_key][0] += win
                    move_results[move_key][1] += 1

        scored = {}
        for move, (wins, total) in move_results.items():
            scored[move] = wins / total if total > 0 else 0

        return scored

    def get_best_move(self, board, player="N"):
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

        scored_moves = []
        for start, end in valid_moves:
            move_str = f"{start}->{end}"
            score = self.move_scores.get(move_str, 0.5) 
            scored_moves.append(((start, end), score))

        scored_moves.sort(key=lambda x: -x[1])
        top_moves = scored_moves[:3] if len(scored_moves) >= 3 else scored_moves
        return random.choice([move for move, score in top_moves])
