from math import inf
import time
import random as rnd


class MinMax:
    def __init__(self):
        self.maximazing = +1
        self.minimazing = -1
        self.board = [[-1, 1, 0], [0, 0, 0], [0, 0, 0]]

    def solve(self, board, depth, player):
        """MinMax core algorithm."""
        print(board[0], board[1], board[2], sep="\n", end="\n===\n")
        time.sleep(1)

        if self.game_over(board):
            return self.value(board)

        if player == self.maximazing:
            best_val = -inf
            for cell in self.cells_left(board):
                x, y = cell
                board[x][y] = player
                value = self.solve(board, depth + 1, player * -1)
                best_val = max(best_val, value)
            return best_val
        else:
            best_val = +inf
            for cell in self.cells_left(board):
                x, y = cell
                board[x][y] = player
                value = self.solve(board, depth + 1, player * -1)
                best_val = min(best_val, value)
            return best_val

    def value(self, board):
        if self.won(board, self.maximazing):
            return +10
        elif self.won(board, self.minimazing):
            return -10
        else:
            return 0

    def game_over(self, board):
        if self.won(board, self.minimazing) or self.won(board, self.maximazing):
            return True
        return False

    def won(self, board, player):
        win_boards = [
            [board[0][0], board[0][1], board[0][2]],
            [board[1][0], board[1][1], board[1][2]],
            [board[2][0], board[2][1], board[2][2]],
            [board[0][0], board[1][0], board[2][0]],
            [board[0][1], board[1][1], board[2][1]],
            [board[0][2], board[1][2], board[2][2]],
            [board[0][0], board[1][1], board[2][2]],
            [board[2][0], board[1][1], board[0][2]],
        ]

        if 3 * [player] in win_boards:
            return True
        return False

    def cells_left(self, board):
        """Returns a list of cordinates of empty cells."""
        cells = list()
        for x, row in enumerate(board):
            for y, cell in enumerate(row):
                if cell == 0:
                    cells.append([x, y])
        return cells

    def get_computer_move(self):

        depth = len(self.cells_left(self.board))
        if depth == 0 or self.game_over(self.board):
            return

        if depth == 9:
            x = rnd.choice([0, 1, 2])
            y = rnd.choice([0, 1, 2])
        else:
            move = self.solve(self.board, depth, self.maximazing)
            x, y = move[0], move[1]
        self.board[x][y] = self.maximazing
        print(self.board[0], self.board[1], self.board[2], sep="\n")

    def insert_human_move(self, x, y):
        self.board[x][y] = self.minimazing
        print(self.board[0], self.board[1], self.board[2], sep="\n")


n = MinMax()
print(n.solve(n.board, 0, 1))


# if maximazing_player == self.maximazing:
#     best = [-1, -1, -inf]
# else:
#     best = [-1, -1, +inf]

# if depth == 0 or self.game_over(board):
#     score = self.value(board)
#     return [-1, -1, score]

# for cell in self.cells_left(board):
#     x, y = cell[0], cell[1]
#     board[x][y] = maximazing_player
#     score = self.solve(board, depth - 1, maximazing_player * -1)
#     board[x][y] = 0
#     score[0], score[1] = x, y

# if maximazing_player == self.maximazing:
#     if score[2] > best[2]:
#         best = score  # max value
# else:
#     if score[2] < best[2]:
#         best = score  # min value

# return best
