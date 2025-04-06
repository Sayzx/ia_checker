class Board:
    def __init__(self):
        """Initialise un plateau de dames avec les pions placés correctement"""
        self.board = self.create_board()
        self.captured_black = 0
        self.captured_white = 0
        self.mandatory_jump_piece = None  # Pion qui doit continuer une capture multiple

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
        """Déplace un pion et gère les captures"""
        start_row, start_col = start
        end_row, end_col = end
        piece = self.board[start_row][start_col]
        
        # Vérifier si le mouvement est valide
        if not self.is_valid_move(start, end):
            return False, False 
        
        self.board[start_row][start_col] = None
        self.board[end_row][end_col] = piece
        
        is_capture = abs(start_row - end_row) > 1
        if is_capture:
            mid_row = (start_row + end_row) // 2
            mid_col = (start_col + end_col) // 2
            captured_piece = self.board[mid_row][mid_col]
            
            if captured_piece and 'N' in captured_piece:
                self.captured_black += 1
            elif captured_piece and 'B' in captured_piece:
                self.captured_white += 1
                
            self.board[mid_row][mid_col] = None
        
        if (end_row == 0 and piece == 'B') or (end_row == 7 and piece == 'N'):
            self.board[end_row][end_col] = piece + 'D'
        
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

        dx, dy = abs(x2 - x1), abs(y2 - y1)

        if 'D' in piece:  # Dame
            if dx == dy:  # Déplacement diagonal
                step_x = 1 if x2 > x1 else -1
                step_y = 1 if y2 > y1 else -1
                for i in range(1, dx):
                    check_x, check_y = x1 + i * step_x, y1 + i * step_y
                    if self.board[check_x][check_y]:
                        if self.board[check_x][check_y][0] == piece[0]:  # Obstacle de même couleur
                            return False
                return True
            return False

        else:  # Pion normal
            if dx == dy == 1:  # Déplacement simple
                return True
            if dx == dy == 2:  # Capture
                mid_row, mid_col = (x1 + x2) // 2, (y1 + y2) // 2
                mid_piece = self.board[mid_row][mid_col]
                if mid_piece and mid_piece[0] != piece[0]:  # Vérifie qu'il y a une pièce ennemie à capturer
                    return True

        return False


    def get_valid_moves(self, row, col):
        piece = self.board[row][col]
        if not piece:
            return []
            
        # Si un pion est forcé de capturer, limiter les mouvements à ce pion
        if self.mandatory_jump_piece and (row, col) != self.mandatory_jump_piece:
            return []
            
        moves = []
        capture_moves = self.get_capture_moves(row, col)
        
        if capture_moves:
            return capture_moves  # Priorité aux captures
        
        # Si aucune capture n'est obligatoire, calcule les mouvements normaux
        if 'D' in piece:  # Dame
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dx, dy in directions:
                for distance in range(1, 8):
                    new_row, new_col = row + dx * distance, col + dy * distance
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        if not self.board[new_row][new_col]: 
                            moves.append((new_row, new_col))
                        else:
                            if self.board[new_row][new_col][0] != piece[0]:  # Pièce ennemie
                                target_row, target_col = new_row + dx, new_col + dy
                                if 0 <= target_row < 8 and 0 <= target_col < 8 and not self.board[target_row][target_col]:
                                    moves.append((target_row, target_col))
                            break
                    else:
                        break
        else:  # Pion normal
            directions = [(-1, -1), (-1, 1)] if piece == 'B' else [(1, -1), (1, 1)]
            for dx, dy in directions:
                new_row, new_col = row + dx, col + dy
                if 0 <= new_row < 8 and 0 <= new_col < 8 and not self.board[new_row][new_col]:
                    moves.append((new_row, new_col))
                    
        return moves

    
    def get_capture_moves(self, row, col):
        piece = self.board[row][col]
        if not piece:
            return []

        captures = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        if 'D' in piece:  # Dame capture à distance (fixé)
            for dx, dy in directions:
                r, c = row + dx, col + dy
                while 0 <= r < 8 and 0 <= c < 8:
                    target = self.board[r][c]
                    if target and target[0] != piece[0]:
                        after_r, after_c = r + dx, c + dy
                        if (0 <= after_r < 8 and 0 <= after_c < 8 and
                            self.board[after_r][after_c] is None):
                            captures.append((after_r, after_c))
                        break  # on stoppe après la pièce ennemie
                    elif target:
                        break  # pièce alliée, on bloque
                    r += dx
                    c += dy
        else:  # Pion capture
            deltas = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dx, dy in deltas:
                enemy_r, enemy_c = row + dx, col + dy
                land_r, land_c = row + 2*dx, col + 2*dy
                if (0 <= enemy_r < 8 and 0 <= enemy_c < 8 and
                    0 <= land_r < 8 and 0 <= land_c < 8):
                    target = self.board[enemy_r][enemy_c]
                    if target and target[0] != piece[0] and self.board[land_r][land_c] is None:
                        captures.append((land_r, land_c))

        return captures


    def has_capture(self, player):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece[0] == player:
                    if self.get_capture_moves(row, col):
                        return True
        return False

    def has_valid_moves(self, player):
        print(f"Coup possible pour le joueur {player}:")
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece[0] == player:
                    valid_moves = self.get_valid_moves(row, col)
                    if valid_moves:  # Vérifie les mouvements normaux
                        print(f"  Pièce à ({row}, {col}) peut se déplacer vers : {valid_moves}")
                        return True
                    capture_moves = self.get_capture_moves(row, col)
                    if capture_moves:  # Vérifie les captures
                        print(f"  Pièce à ({row}, {col}) peut capturer vers : {capture_moves}")
                        return True
        return False