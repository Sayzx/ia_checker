import random

class CheckersAI:
    def get_best_move(self, board):
        """Renvoie un coup valide basé sur les mouvements possibles"""
        valid_moves = []

        # Cherche tous les pions noirs et leurs mouvements possibles
        for row in range(8):
            for col in range(8):
                if board.board[row][col] == 'N' or board.board[row][col] == 'ND':  # Pions noirs ou dames noires
                    moves = board.get_valid_moves(row, col)
                    for move in moves:
                        valid_moves.append(((row, col), move))

        if not valid_moves:
            return None  # Aucun mouvement possible

        return random.choice(valid_moves)  # Choisir un mouvement aléatoire