import numpy as np


MAX_ITER = 120
POSSIBLE_VALUES = [2, 4]
ROTATION_MAP = {
    "L": 0,
    "U": 1,
    "R": 2,
    "D": 3
}
BOARD_DIM = 4


class Board(object):

    def __init__(self):
        self.board = np.zeros([BOARD_DIM, BOARD_DIM])
        self.add_number_in_board()

    @property
    def possible_moves(self):
        possible_moves = []
        for i in ROTATION_MAP.keys():
            if self.test_move(i):
                possible_moves.append(i)
        return possible_moves

    def add_number_in_board(self) :
        """Docstring"""
        count = 0
        value = 1
        rand_row = 0
        rand_col = 0

        while value > 0 and count < MAX_ITER:
            rand_row = np.random.randint(0, 3)
            rand_col = np.random.randint(0, 3)
            value = self.board[rand_row][rand_col]
            count += 1

        rand_value = np.random.choice(POSSIBLE_VALUES)
        self.board[rand_row][rand_col] = rand_value

    def do_move(self, move):
        self.rotate_board(move, 1)
        score = self.update_board()
        self.rotate_board(move, -1)
        return score

    def rotate_board(self, input_player, direction=1):
        self.board = np.rot90(
            m=self.board,
            k=ROTATION_MAP[input_player] * direction
        )

    def update_board(self):
        """Docstring"""
        total_score = 0
        for i in range(BOARD_DIM) :
            self.board[i], score = self.process_row(self.board[i])
            total_score += score
        return total_score

    def process_row(self, row):
        row, score = self.merge_cells(row)
        row = self.fill_zeros(row)
        return row, score


    def merge_cells(self, row):
        """Look to the right of the row if the first value
           encountered is the same as the current cell
        """
        score = 0
        for j in range(BOARD_DIM):
            # If the cell is empty, do nothing
            if row[j] == 0:
                continue
            k = 1
            while j+k < BOARD_DIM:
                if row[j] == row[j+k]:
                    score += np.log2([row[j]])[0] * row[j] * 2
                    row[j] *= 2
                    row[j+k] = 0
                    break
                elif row[j+k] != 0:
                    break
                k += 1

        return row, score

    def fill_zeros(self, row):
        """Move every cell non mergable"""
        for j in range(BOARD_DIM) :
            if row[j] != 0 :
                k = 1
                while j - k >= 0 :
                    if row[j-k] == 0 :
                        row[j-k] = row[j-k+1]
                        row[j-k+1] = 0
                    k += 1    
        return row

    def test_move(self, move):
        """Test that the move will change the board"""
        new_board = Board()
        new_board.board = np.copy(self.board)
        new_board.do_move(move)

        for i in range(BOARD_DIM) :
            for j in range(BOARD_DIM) :
                if self.board[i][j] != new_board.board[i][j]:
                    return True

        return False
