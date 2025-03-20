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
            return False
        
        # Effectuer le déplacement
        self.board[start_row][start_col] = None
        self.board[end_row][end_col] = piece
        
        # Vérifier si c'est une capture
        is_capture = abs(start_row - end_row) > 1
        if is_capture:
            mid_row = (start_row + end_row) // 2
            mid_col = (start_col + end_col) // 2
            captured_piece = self.board[mid_row][mid_col]
            
            # Incrémenter les compteurs de capture
            if captured_piece and 'N' in captured_piece:
                self.captured_black += 1
            elif captured_piece and 'B' in captured_piece:
                self.captured_white += 1
                
            self.board[mid_row][mid_col] = None
        
        # Transformation en dame
        if (end_row == 0 and piece == 'B') or (end_row == 7 and piece == 'N'):
            self.board[end_row][end_col] = piece + 'D'
        
        # Vérifier s'il y a d'autres captures possibles pour ce pion
        if is_capture:
            further_captures = self.get_capture_moves(end_row, end_col)
            if further_captures:
                self.mandatory_jump_piece = (end_row, end_col)
                return True, True  # Mouvement réussi, capture multiple possible
            else:
                self.mandatory_jump_piece = None
        else:
            self.mandatory_jump_piece = None
            
        return True, False  # Mouvement réussi, pas de capture multiple

    def is_valid_move(self, start, end):
        """Vérifie si un mouvement est valide"""
        x1, y1 = start
        x2, y2 = end
        
        # Vérifier que les coordonnées sont dans les limites
        if not (0 <= x1 < 8 and 0 <= y1 < 8 and 0 <= x2 < 8 and 0 <= y2 < 8):
            return False
            
        piece = self.board[x1][y1]
        if not piece or self.board[x2][y2]:  # Case de départ vide ou case d'arrivée occupée
            return False
            
        # Si une capture multiple est obligatoire, seule la pièce concernée peut jouer
        if self.mandatory_jump_piece and (x1, y1) != self.mandatory_jump_piece:
            return False
            
        dx, dy = abs(x2 - x1), abs(y2 - y1)
        
        # Vérifier si on doit faire une prise obligatoire
        if not self.mandatory_jump_piece:
            must_capture = self.has_capture(piece[0])
            if must_capture and (dx != 2 or dy != 2):
                return False
        
        # Mouvement pour les dames
        if 'D' in piece:
            if dx == dy:  # Déplacement diagonal
                step_x = 1 if x2 > x1 else -1
                step_y = 1 if y2 > y1 else -1
                
                # Vérifie si c'est une capture
                if dx > 1:
                    capture_count = 0
                    enemy_positions = []
                    
                    for i in range(1, dx):
                        check_x, check_y = x1 + i * step_x, y1 + i * step_y
                        if self.board[check_x][check_y]:
                            if self.board[check_x][check_y][0] == piece[0]:  # Même couleur
                                return False
                            else:
                                capture_count += 1
                                enemy_positions.append((check_x, check_y))
                    
                    # Une dame ne peut sauter qu'un seul pion à la fois
                    if capture_count > 1:
                        return False
                    elif capture_count == 1:
                        # Vérifie qu'il n'y a pas d'autre pion après celui capturé
                        enemy_x, enemy_y = enemy_positions[0]
                        between_x1_enemy = abs(enemy_x - x1)
                        for i in range(between_x1_enemy + 1, dx):
                            if self.board[x1 + i * step_x][y1 + i * step_y]:
                                return False
                                
                return True
                
        # Mouvement pour les pions normaux
        else:
            if dx == dy == 1:  # Déplacement simple
                if piece == 'B' and x2 > x1:  # Les pions blancs ne peuvent avancer que vers le haut
                    return False
                if piece == 'N' and x2 < x1:  # Les pions noirs ne peuvent avancer que vers le bas
                    return False
                return True
                
            if dx == dy == 2:  # Capture
                mid_row, mid_col = (x1 + x2) // 2, (y1 + y2) // 2
                mid_piece = self.board[mid_row][mid_col]
                if mid_piece and mid_piece[0] != piece[0]:
                    return True
                    
        return False

    def get_valid_moves(self, row, col):
        """Retourne tous les mouvements valides pour une pièce donnée"""
        piece = self.board[row][col]
        if not piece:
            return []
            
        # Si capture multiple obligatoire, seule cette pièce peut jouer
        if self.mandatory_jump_piece and (row, col) != self.mandatory_jump_piece:
            return []
            
        # Vérifier s'il existe des prises obligatoires sur le plateau
        must_capture = False
        if not self.mandatory_jump_piece:
            must_capture = self.has_capture(piece[0])
            
        moves = []
        
        # Si on doit capturer, ne retourne que les mouvements de capture
        if must_capture:
            return self.get_capture_moves(row, col)
            
        # Mouvement pour les dames
        if 'D' in piece:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dx, dy in directions:
                for distance in range(1, 8):
                    new_row, new_col = row + dx * distance, col + dy * distance
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        if not self.board[new_row][new_col]:  # Case vide
                            moves.append((new_row, new_col))
                        else:  # Case occupée, on s'arrête
                            break
                    else:  # Hors du plateau
                        break
        # Mouvement pour les pions normaux
        else:
            directions = [(-1, -1), (-1, 1)] if piece == 'B' else [(1, -1), (1, 1)]
            for dx, dy in directions:
                new_row, new_col = row + dx, col + dy
                if 0 <= new_row < 8 and 0 <= new_col < 8 and not self.board[new_row][new_col]:
                    moves.append((new_row, new_col))
                    
        return moves

    def get_capture_moves(self, row, col):
        """Retourne les mouvements de capture possibles pour une pièce"""
        piece = self.board[row][col]
        if not piece:
            return []
            
        captures = []
        
        # Pour les dames
        if 'D' in piece:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dx, dy in directions:
                for distance in range(1, 7):
                    check_row, check_col = row + dx * distance, col + dy * distance
                    if 0 <= check_row < 8 and 0 <= check_col < 8:
                        if self.board[check_row][check_col]:
                            if self.board[check_row][check_col][0] != piece[0]:  # Pion adverse
                                target_row, target_col = check_row + dx, col + dy * (distance + 1)
                                if 0 <= target_row < 8 and 0 <= target_col < 8 and not self.board[target_row][target_col]:
                                    captures.append((target_row, target_col))
                            break  # Arrêt à la première pièce rencontrée
                    else:
                        break
        # Pour les pions normaux
        else:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dx, dy in directions:
                # Si c'est un pion blanc, il ne peut se déplacer que vers le haut
                if piece == 'B' and dx > 0:
                    continue
                # Si c'est un pion noir, il ne peut se déplacer que vers le bas
                if piece == 'N' and dx < 0:
                    continue
                    
                mid_row, mid_col = row + dx, col + dy
                if 0 <= mid_row < 8 and 0 <= mid_col < 8:
                    mid_piece = self.board[mid_row][mid_col]
                    if mid_piece and mid_piece[0] != piece[0]:  # Pion adverse
                        end_row, end_col = mid_row + dx, mid_col + dy
                        if 0 <= end_row < 8 and 0 <= end_col < 8 and not self.board[end_row][end_col]:
                            captures.append((end_row, end_col))
                            
        return captures

    def has_capture(self, player):
        """Vérifie s'il y a des captures possibles pour un joueur"""
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece[0] == player:
                    if self.get_capture_moves(row, col):
                        return True
        return False

    def has_valid_moves(self, player):
        """Vérifie si un joueur a encore des mouvements possibles"""
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece[0] == player:
                    if self.get_valid_moves(row, col) or self.get_capture_moves(row, col):
                        return True
        return False