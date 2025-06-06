class Board:
    def __init__(self):
        self.board = self.create_board()  # Plateau 8x8
        self.captured_black = 0           # Pions noirs capturés
        self.captured_white = 0           # Pions blancs capturés
        self.mandatory_jump_piece = None  # Pièce obligée de continuer une capture

    def create_board(self):
        # Création du plateau avec pièces blanches et noires
        board = [[None] * 8 for _ in range(8)]
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = 'N'  # Pions noirs en haut
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = 'B'  # Pions blancs en bas
        return board

    def has_any_capture(self, player_color):
        # Vérifie si le joueur a au moins une capture possible
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece[0] == player_color:
                    moves = self.get_valid_moves(row, col)
                    for move_row, move_col in moves:
                        if abs(move_row - row) == 2 or "D" in piece:
                            return True
        return False

    def move_piece(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        piece = self.board[start_row][start_col]

        if not self.is_valid_move(start, end):
            return False, False

        self.board[start_row][start_col] = None
        self.board[end_row][end_col] = piece

        # Si capture : retirer la pièce adverse sautée
        is_capture = abs(start_row - end_row) > 1
        if is_capture:
            dx = 1 if end_row > start_row else -1
            dy = 1 if end_col > start_col else -1
            r, c = start_row + dx, start_col + dy
            while (r != end_row and c != end_col):
                if self.board[r][c] and self.board[r][c][0] != piece[0]:
                    captured_piece = self.board[r][c]
                    if captured_piece[0] == 'N':
                        self.captured_black += 1
                    elif captured_piece[0] == 'B':
                        self.captured_white += 1
                    self.board[r][c] = None
                r += dx
                c += dy

        # Promotion en dame
        if (end_row == 0 and piece == 'B') or (end_row == 7 and piece == 'N'):
            self.board[end_row][end_col] = piece + 'D'

        # Vérifie s'il y a encore une capture possible
        if is_capture:
            further_captures = self.get_capture_moves(end_row, end_col)
            if further_captures:
                self.mandatory_jump_piece = (end_row, end_col)
                return True, True
            else:
                self.mandatory_jump_piece = None
        else:
            self.mandatory_jump_piece = None

        return True, False

    def is_valid_move(self, start, end):
        x1, y1 = start
        x2, y2 = end

        if not (0 <= x1 < 8 and 0 <= y1 < 8 and 0 <= x2 < 8 and 0 <= y2 < 8):
            return False

        piece = self.board[x1][y1]
        if not piece or self.board[x2][y2]:
            return False

        if self.mandatory_jump_piece and (x1, y1) != self.mandatory_jump_piece:
            return False

        if self.has_capture(piece[0]) and not self.is_capture_move(start, end):
            return False

        dx, dy = abs(x2 - x1), abs(y2 - y1)

        if 'D' in piece:
            if dx != dy:
                return False
            step_x = 1 if x2 > x1 else -1
            step_y = 1 if y2 > y1 else -1
            enemy_found = False
            r, c = x1 + step_x, y1 + step_y
            while r != x2 and c != y2:
                if self.board[r][c]:
                    if self.board[r][c][0] == piece[0]:
                        return False
                    elif not enemy_found:
                        enemy_found = True
                    else:
                        return False
                r += step_x
                c += step_y
            return True

        else:
            # Déplacement simple
            if dx == dy == 1:
                if (piece.startswith('B') and x2 < x1) or (piece.startswith('N') and x2 > x1):
                    return True
            # Capture diagonale
            if dx == dy == 2:
                mid_row, mid_col = (x1 + x2) // 2, (y1 + y2) // 2
                mid_piece = self.board[mid_row][mid_col]
                if mid_piece and mid_piece[0] != piece[0]:
                    if piece.startswith('B') and x2 < x1:
                        return True
                    if piece.startswith('N') and x2 > x1:
                        return True
            return False

    def is_capture_move(self, start, end):
        return abs(start[0] - end[0]) > 1 and abs(start[1] - end[1]) > 1

    def get_capture_moves(self, row, col):
        piece = self.board[row][col]
        if not piece:
            return []

        captures = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        if 'D' in piece:
            for dx, dy in directions:
                r, c = row + dx, col + dy
                while 0 <= r < 8 and 0 <= c < 8:
                    if self.board[r][c] and self.board[r][c][0] != piece[0]:
                        after_r, after_c = r + dx, c + dy
                        if 0 <= after_r < 8 and 0 <= after_c < 8 and self.board[after_r][after_c] is None:
                            captures.append((after_r, after_c))
                        break
                    elif self.board[r][c]:
                        break
                    r += dx
                    c += dy
        else:
            for dx, dy in directions:
                enemy_r, enemy_c = row + dx, col + dy
                land_r, land_c = row + 2 * dx, col + 2 * dy
                if 0 <= enemy_r < 8 and 0 <= enemy_c < 8 and 0 <= land_r < 8 and 0 <= land_c < 8:
                    target = self.board[enemy_r][enemy_c]
                    if target and target[0] != piece[0] and self.board[land_r][land_c] is None:
                        if piece == 'B' and dx == -1:
                            captures.append((land_r, land_c))
                        elif piece == 'N' and dx == 1:
                            captures.append((land_r, land_c))

        return captures

    def has_capture(self, player):
        # Y a-t-il une capture disponible pour ce joueur ?
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece[0] == player:
                    if self.get_capture_moves(row, col):
                        return True
        return False

    def has_valid_moves(self, player):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece[0] == player:
                    if self.get_valid_moves(row, col):
                        return True
        return False

    def get_valid_moves(self, row, col):
        piece = self.board[row][col]
        if not piece:
            return []

        player = piece[0]

        if self.mandatory_jump_piece and (row, col) != self.mandatory_jump_piece:
            return []

        capture_moves = self.get_capture_moves(row, col)
        if capture_moves:
            return capture_moves

        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        if 'D' in piece:
            for dx, dy in directions:
                for dist in range(1, 8):
                    new_row = row + dx * dist
                    new_col = col + dy * dist
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        if self.board[new_row][new_col] is None:
                            if not self.has_capture(player):
                                moves.append((new_row, new_col))
                        else:
                            break
                    else:
                        break
        else:
            if piece == 'B':
                directions = [(-1, -1), (-1, 1)]
            elif piece == 'N':
                directions = [(1, -1), (1, 1)]

            for dx, dy in directions:
                new_row = row + dx
                new_col = col + dy
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if self.board[new_row][new_col] is None:
                        if not self.has_capture(player):
                            moves.append((new_row, new_col))

                # Vérifie aussi les captures
                new_row = row + 2 * dx
                new_col = col + 2 * dy
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    mid_row = row + dx
                    mid_col = col + dy
                    mid_piece = self.board[mid_row][mid_col]
                    if mid_piece and mid_piece[0] != player and self.board[new_row][new_col] is None:
                        moves.append((new_row, new_col))

        return moves
