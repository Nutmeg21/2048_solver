import math

class Solver:
    def __init__(self):
        self.SCORING_MATRICES = [
        # Top Left Horizontal
        [
            [15, 14, 13, 12],
            [8,  9,  10, 11],
            [7,  6,  5,  4],
            [0,  1,  2,  3]
        ],

        # Top Right Horizontal
        [
            [12, 13, 14, 15],
            [11, 10, 9,  8],
            [4,  5,  6,  7],
            [3,  2,  1,  0]
        ],

        # Bottom Left Horizontal
        [
            [0,  1,  2,  3],
            [7,  6,  5,  4],
            [8,  9,  10, 11],
            [15, 14, 13, 12]
        ],
       
        # Bottom Right Horizontal
        [
            [3,  2,  1,  0],
            [4,  5,  6,  7],
            [11, 10, 9,  8],
            [12, 13, 14, 15]
        ],

        # Top Left Vertical
        [
            [15, 8,  7,  0],
            [14, 9,  6,  1],
            [13, 10, 5,  2],
            [12, 11, 4,  3]
        ],

        # Top Right Vertical
        [
            [0,  7,  8,  15],
            [1,  6,  9,  14],
            [2,  5,  10, 13],
            [3,  4,  11, 12]
        ],

        # Bottom Left Vertical
        [
            [12, 11, 4,  3],
            [13, 10, 5,  2],
            [14, 9,  6,  1],
            [15, 8,  7,  0]
        ],
       
        # Bottom Right Vertical
        [
            [3,  4,  11, 12],
            [2,  5,  10, 13],
            [1,  6,  9,  14],
            [0,  7,  8,  15]
        ],
        ]

        self.SCORING_MATRICES_2 = [
        # Top Left
        [
            [15, 12, 9,  6],
            [12, 9,  6,  3],
            [9,  6,  3,  2],
            [6,  3,  2,  1]
        ],

        # Top Right
        [
            [6,  9,  12, 15],
            [3,  6,  9,  12],
            [2,  3,  6,  9],
            [1,  2,  3,  6]
        ],

        # Bottom Left
        [
            [6,  3,  2,  1],
            [9,  6,  3,  2],
            [12, 9,  6,  3],
            [15, 12, 9,  6]
        ],
       
        # Bottom Right
        [
            [1,  2,  3,  6],
            [2,  3,  6,  9],
            [3,  6,  9,  12],
            [6,  9,  12, 15]
        ]
        ]

        self.WEIGHT_MATRIX_CORNER = [
            [6, 3, 3, 6],
            [3, 2, 2, 3],
            [3, 2, 2, 3],
            [6, 3, 3, 6]
        ]

        self.MOVES = ["up", "down", "left", "right"]

    def get_best_move(self, board):
        best_score = -float('inf')
        best_move = None
        for move in self.MOVES:
            new_board = self.simulate_move(board, move)
            # If nothing changes
            if new_board == board:
                continue
            # Set depth here (depth = 3 for optimal balance between speed and accuracy)
            score = self.expectimax(new_board, depth=5, turn="COMPUTER")
            if score > best_score:
                best_score = score
                best_move = move
        print(best_score)
        return best_move
    
    def expectimax(self, board, depth, turn):
        if depth == 0:
            return self.heuristic_score(board)
        else:
            if turn == "PLAYER":
                max_score = -float('inf')
                
                for move in self.MOVES:
                    new_board = self.simulate_move(board, move)
                    # If nothing changes
                    if new_board == board:
                        continue

                    score = self.expectimax(new_board, depth - 1, "COMPUTER")
                    if score > max_score:
                        max_score = score
                return max_score
                     
            elif turn == "COMPUTER":
                total_score = 0
                empty_cells = self.get_empty_cells(board)            

                # Optimization: If too many empty cells, tree is too big. 
                # Only check the first few to save speed (optional)
                if len(empty_cells) > 6:
                    empty_cells = empty_cells[:6]

                # Game Over
                if not empty_cells:
                    return self.heuristic_score(board)
                
                for (r, c) in empty_cells:
                    # Spawns a 2 (90% chance)
                    new_board_with_2 = [row[:] for row in board]
                    new_board_with_2[r][c] = 2
                    score_2 = self.expectimax(new_board_with_2, depth - 1, "PLAYER")
                    total_score += 0.9 * score_2

                    # Spawns a 4 (10% chance)
                    new_board_with_4 = [row[:] for row in board]
                    new_board_with_4[r][c] = 4
                    score_4 = self.expectimax(new_board_with_4, depth - 1, "PLAYER")
                    total_score += 0.1 * score_4

                # Return average score
                return total_score / len(empty_cells)
    
    def heuristic_score(self, board):
        snakeness = self.snake_score(board)
        snakeness_mult = 4
        empty_tile = len(self.get_empty_cells(board))
        empty_tile_mult = 50
        corner_bonus = self.corner_score(board)
        corner_bonus_mult = 2
        smoothness = self.smoothness(board)
        smoothness_mult = 1.3
        score = (snakeness * snakeness_mult) + (empty_tile * empty_tile_mult) + (smoothness * smoothness_mult)
        return score    

    def simulate_move(self, board, direction):
        """
        Returns a NEW board state after moving in the given direction.
        """
        # 1. Create a Deep Copy
        # Using list comprehension is faster than deepcopy library for simple 2D lists
        temp_board = [row[:] for row in board]

        if direction == 'left':
            # Logic: Just apply merge on every row
            temp_board = [self.merge_left(row) for row in temp_board]

        elif direction == 'right':
            # Logic: Reverse -> Merge Left -> Reverse Back
            # [2, 0, 0, 0] -> [0, 0, 0, 2] -> Merge -> [2, 0, 0, 0]
            temp_board = self.reverse(temp_board)
            temp_board = [self.merge_left(row) for row in temp_board]
            temp_board = self.reverse(temp_board)

        elif direction == 'up':
            # Logic: Transpose -> Merge Left -> Transpose Back
            # Columns become rows. Moving "Left" on a transposed board is "Up".
            temp_board = self.transpose(temp_board)
            temp_board = [self.merge_left(row) for row in temp_board]
            temp_board = self.transpose(temp_board)

        elif direction == 'down':
            # Logic: Transpose -> Reverse -> Merge Left -> Reverse -> Transpose
            # 1. Turn columns into rows (Transpose)
            # 2. Flip them (Reverse) so the "Bottom" is now on the "Left"
            temp_board = self.transpose(temp_board)
            temp_board = self.reverse(temp_board)
            temp_board = [self.merge_left(row) for row in temp_board]
            temp_board = self.reverse(temp_board)
            temp_board = self.transpose(temp_board)

        return temp_board
    
    def transpose(self, board):
        """Swaps rows and columns (Rotates the board diagonal)."""
        # zip(*board) unzips the rows and pairs them by index
        return [list(row) for row in zip(*board)]

    def reverse(self, board):
        """Reverses the order of elements in every row (Mirror image)."""
        return [row[::-1] for row in board]
    
    def merge_left(self, row):
        """
        The core logic: Slides a single row to the left and merges.
        Input:  [2, 2, 0, 4]
        Output: [4, 4, 0, 0]
        """
        # 1. Compress (remove 0s)
        new_row = [i for i in row if i != 0]
        
        # 2. Merge
        for i in range(len(new_row) - 1):
            # If current equals next, and current hasn't been merged (value check)
            if new_row[i] == new_row[i+1]:
                new_row[i] *= 2
                new_row[i+1] = 0 # Mark as empty so it doesn't merge again
        
        # 3. Compress again (remove the new 0s created by merging)
        new_row = [i for i in new_row if i != 0]
        
        # 4. Pad with 0s to maintain length of 4
        return new_row + [0] * (4 - len(new_row))
        
    def get_empty_cells(self, board):
        empty_cells = []
        for r in range(4):
            for c in range(4):
                if board[r][c] == 0:
                    empty_cells.append((r, c))
        return empty_cells
    
    def snake_score(self, board):
        highest_score = 0
        for i in range(4):
            score = 0
            for r in range(4):
                for c in range(4):
                    if board[r][c] > 0:
                        score += (board[r][c]) * self.SCORING_MATRICES[i][r][c]
            if score > highest_score:
                highest_score = score
        return highest_score
    
    def corner_score(self, board):
        score = 0
        for r in range(4):
            for c in range(4):
                if board[r][c] > 0:
                    score += math.log2(board[r][c]) * self.WEIGHT_MATRIX_CORNER[r][c]
        return score
    
    def smoothness(self, board):
        # Penalizes large jumps in value between tiles
        smoothness = 0
        for r in range(4):
            for c in range(4):
                value = 0
                if board[r][c] > 0:
                    value = math.log2(board[r][c])
                
                # Check right neighbour
                if c < 3 and board[r][c + 1] > 0:
                    neighbour_value = math.log2(board[r][c + 1])
                    smoothness -= abs(neighbour_value - value)

                # Check down neighbour
                if r < 3 and board[r + 1][c] > 0:
                    neighbour_value = math.log2(board[r + 1][c])
                    smoothness -= abs(neighbour_value - value)
        return smoothness