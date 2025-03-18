class Board:
    def __init__(self):
        """Initialise un plateau de dames avec les pions placés correctement"""
        self.board = self.create_board()
        self.captured_black = 0
        self.captured_white = 0

    def create_board(self):
        """Crée un plateau de 8x8 avec les pions noirs et blancs"""
        board = [[None] * 8 for _ in range(8)]
        for row in range(3):  # Pions noirs
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = 'N'
        for row in range(5, 8):  # Pions blancs
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = 'B'
        return board

    def move_piece(self, start, end):
        """Effectue un mouvement de pion"""
        start_row, start_col = start
        end_row, end_col = end

        # Vérifie si le mouvement est valide
        if not self.is_valid_move(start, end):
            return False

        # Effectue le déplacement
        piece = self.board[start_row][start_col]
        self.board[start_row][start_col] = None
        self.board[end_row][end_col] = piece

        # Vérifie si c'est une capture
        if abs(start_row - end_row) == 2:  # Mouvement de 2 cases (capture)
            mid_row = (start_row + end_row) // 2
            mid_col = (start_col + end_col) // 2
            captured_piece = self.board[mid_row][mid_col]
            self.board[mid_row][mid_col] = None  # Supprime le pion capturé

            # Met à jour le compteur de captures
            if captured_piece == 'N' or captured_piece == 'ND':
                self.captured_black += 1
            elif captured_piece == 'B' or captured_piece == 'BD':
                self.captured_white += 1

        # Transformation en dame
        if end_row == 0 and piece == 'B':  # Pion blanc atteint la dernière ligne
            self.board[end_row][end_col] = 'BD'  # BD = Dame blanche
        elif end_row == 7 and piece == 'N':  # Pion noir atteint la dernière ligne
            self.board[end_row][end_col] = 'ND'  # ND = Dame noire

        return True
        return True

    def is_valid_move(self, start, end):
        """Vérifie si un mouvement est valide"""
        x1, y1 = start
        x2, y2 = end
        piece = self.board[x1][y1]
        if piece and not self.board[x2][y2]:
            dx, dy = abs(x2 - x1), abs(y2 - y1)
            if dx == dy == 1:  # Déplacement simple
                if piece == 'B' and x2 > x1:  # Les pions blancs ne peuvent avancer que vers le haut
                    return False
                if piece == 'N' and x2 < x1:  # Les pions noirs ne peuvent avancer que vers le bas
                    return False
                return True
            if dx == dy == 2:  # Capture
                mid_row, mid_col = (x1 + x2) // 2, (y1 + y2) // 2
                if self.board[mid_row][mid_col] and self.board[mid_row][mid_col] != piece:
                    return True
        return False

    def get_valid_moves(self, row, col):
        """Renvoie les mouvements valides pour un pion donné, y compris les captures"""
        piece = self.board[row][col]
        if not piece:
            return []

        direction = -1 if piece == 'B' else 1  # Blancs montent, Noirs descendent
        moves = []

        # Vérifie les déplacements simples
        for dx in [-1, 1]:
            new_row, new_col = row + direction, col + dx
            if 0 <= new_row < 8 and 0 <= new_col < 8 and self.board[new_row][new_col] is None:
                moves.append((new_row, new_col))  # Case vide => mouvement possible

        # Vérifie les captures
        for dx in [-1, 1]:
            mid_row, mid_col = row + direction, col + dx
            new_row, new_col = row + 2 * direction, col + 2 * dx
            if (
                0 <= new_row < 8 and 0 <= new_col < 8 and
                self.board[mid_row][mid_col] is not None and
                self.board[mid_row][mid_col] != piece and
                self.board[new_row][new_col] is None
            ):
                moves.append((new_row, new_col))  # Capture possible

        return moves

    def has_valid_moves(self, player):
        """Vérifie si un joueur a encore des mouvements possibles"""
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and (piece == player or piece == player + 'D'):  # Pion ou dame
                    if self.get_valid_moves(row, col):
                        return True
        return False