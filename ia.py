import random
import pandas as pd
import os

class CheckersAI:
    def __init__(self, stats_file="data/games_stats.csv"):
        self.stats_file = stats_file
        self.popular_moves = self.load_move_stats()

    def load_move_stats(self):
        if not os.path.exists(self.stats_file):
            return {}

        try:
            df = pd.read_csv(self.stats_file)
            if "move" in df.columns:
                return df["move"].value_counts().to_dict()
        except:
            pass

        return {}

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
            score = self.popular_moves.get(move_str, 0)
            scored_moves.append(((start, end), score))

        scored_moves.sort(key=lambda x: -x[1])
        top_moves = scored_moves[:3] if len(scored_moves) >= 3 else scored_moves
        return random.choice([move for move, score in top_moves])
