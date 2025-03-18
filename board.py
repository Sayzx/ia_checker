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
        """Effectue un mouvement de pion ou de dame"""
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
        if abs(start_row - end_row) > 1:  # Capture
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
            print("Un pion blanc est devenu une dame !")  # Log pour débogage
            # changer le style de la piece avec une couronne
    
        elif end_row == 7 and piece == 'N':  # Pion noir atteint la dernière ligne
            self.board[end_row][end_col] = 'ND'  # ND = Dame noire
            print("Un pion noir est devenu une dame !")  # Log pour débogage

        return True

    def is_valid_move(self, start, end):
        """Vérifie si un mouvement est valide"""
        x1, y1 = start
        x2, y2 = end
        piece = self.board[x1][y1]
        if piece and not self.board[x2][y2]:
            dx, dy = abs(x2 - x1), abs(y2 - y1)

            # Mouvement pour les dames
            if piece in ['BD', 'ND']:
                if dx == dy:  # Déplacement en diagonale
                    step_x = 1 if x2 > x1 else -1
                    step_y = 1 if y2 > y1 else -1
                    for i in range(1, dx):  # Vérifie que toutes les cases intermédiaires sont vides
                        if self.board[x1 + i * step_x][y1 + i * step_y] is not None:
                            return False
                    return True

            # Mouvement pour les pions
            if dx == dy == 1:  # Déplacement simple
                if piece == 'B' and x2 > x1:  # Les pions blancs ne peuvent avancer que vers le haut
                    return False
                if piece == 'N' and x2 < x1:  # Les pions noirs ne peuvent avancer que vers le bas
                    return False
                return True
            if dx == dy == 2:  # Capture
                mid_row, mid_col = (x1 + x2) // 2, (y1 + y2) // 2
                if self.board[mid_row][mid_col] and self.board[mid_row][mid_col][0] != piece[0]:
                    return True
        return False

    def get_valid_moves(self, row, col):
        """Renvoie les mouvements valides pour un pion ou une dame"""
        piece = self.board[row][col]
        if not piece:
            return []

        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonales

        if piece in ['B', 'N']:  # Pions
            directions = [(-1, -1), (-1, 1)] if piece == 'B' else [(1, -1), (1, 1)]

        for dx, dy in directions:
            new_row, new_col = row + dx, col + dy
            if 0 <= new_row < 8 and 0 <= new_col < 8 and self.board[new_row][new_col] is None:
                moves.append((new_row, new_col))  # Déplacement simple

            # Vérifie les captures
            mid_row, mid_col = row + dx, col + dy
            new_row, new_col = row + 2 * dx, col + 2 * dy
            if (
                0 <= new_row < 8 and 0 <= new_col < 8 and
                self.board[mid_row][mid_col] and self.board[mid_row][mid_col][0] != piece[0] and
                self.board[new_row][new_col] is None
            ):
                moves.append((new_row, new_col))  # Capture

        # Mouvement multiple pour les dames
        if piece in ['BD', 'ND']:
            for dx, dy in directions:
                step = 1
                while True:
                    new_row, new_col = row + step * dx, col + step * dy
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        if self.board[new_row][new_col] is None:
                            moves.append((new_row, new_col))
                        elif self.board[new_row][new_col][0] != piece[0]:
                            # Capture possible
                            capture_row, capture_col = new_row + dx, new_col + dy
                            if 0 <= capture_row < 8 and 0 <= capture_col < 8 and self.board[capture_row][capture_col] is None:
                                moves.append((capture_row, capture_col))
                            break
                        else:
                            break
                    else:
                        break
                    step += 1

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