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

        self.MOVES = ["up", "down", "left", "right"]

        self.transposition_table = {}

    def get_best_move(self, board):
        best_score = -float('inf')
        best_move = None

        # Memory management
        if len(self.transposition_table) > 50000:
            self.transposition_table = {}

        # Dynamic depth
        empty_count = len(self.get_empty_cells(board))
        if empty_count <= 4:
            depth = 6
        elif empty_count <= 8:
            depth = 5
        else:
            depth = 4

        for move in self.MOVES:
            new_board = self.simulate_move(board, move)
            # If nothing changes
            if new_board == board:
                continue
                
            score = self.expectimax(new_board, depth, turn="COMPUTER")
            if score > best_score:
                best_score = score
                best_move = move
        # print(best_score)
        return best_move
    
    def expectimax(self, board, depth, turn):
        if depth == 0:
            return self.heuristic_score(board)
        
        # Convert board to hashable key
        board_tuple = tuple(tuple(row) for row in board)
        
        # Check if this state exists in memory
        if board_tuple in self.transposition_table:
            entry = self.transposition_table[board_tuple]
            
            # Determine if we have enough depth in this tree
            # if depth too shallow, then we recalculate it
            if entry['depth'] >= depth: 
                return entry['score']


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
            # Only check the first few to save speed
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

            # Saves board depth and score so it doesn't have calculate this tree again
            self.transposition_table[board_tuple] = {'depth': depth, 'score': total_score}

            # Return average score
            return total_score / len(empty_cells)

    def heuristic_score(self, board):
        snakeness = self.snake_score(board)
        snakeness_mult = 4
        empty_tile = len(self.get_empty_cells(board))
        empty_tile_mult = 50
        smoothness = self.smoothness(board)
        smoothness_mult = 1.3
        score = (snakeness * snakeness_mult) + (empty_tile * empty_tile_mult) + (smoothness * smoothness_mult)
        return score    

    def simulate_move(self, board, direction):
        """
        Returns a NEW board state after moving in the given direction.
        """
        # Create deep copy using list
        temp_board = [row[:] for row in board]

        # Only merge left is programmed
        # For other directions, rotate the board then merge left again
        if direction == 'left':
            temp_board = [self.merge_left(row) for row in temp_board]

        elif direction == 'right':
            temp_board = self.reverse(temp_board)
            temp_board = [self.merge_left(row) for row in temp_board]
            temp_board = self.reverse(temp_board)

        elif direction == 'up':
            temp_board = self.transpose(temp_board)
            temp_board = [self.merge_left(row) for row in temp_board]
            temp_board = self.transpose(temp_board)

        elif direction == 'down':
            temp_board = self.transpose(temp_board)
            temp_board = self.reverse(temp_board)
            temp_board = [self.merge_left(row) for row in temp_board]
            temp_board = self.reverse(temp_board)
            temp_board = self.transpose(temp_board)

        return temp_board
    
    def transpose(self, board):
        """Swaps rows and columns (Rotates the board diagonal)."""
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
        # Compress (remove 0s)
        new_row = [i for i in row if i != 0]
        
        # Merge
        for i in range(len(new_row) - 1):
            # If current equals next, and current hasn't been merged (value check)
            if new_row[i] == new_row[i+1]:
                new_row[i] *= 2
                new_row[i+1] = 0 # Mark as empty so it doesn't merge again
        
        # Compress again by removing the new 0s created by merging
        new_row = [i for i in new_row if i != 0]
        
        # Pad with 0s to maintain length of 4
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
