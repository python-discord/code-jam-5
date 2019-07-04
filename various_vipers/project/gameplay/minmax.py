from math import inf
import random as rnd


class MinMax:
    """Represents implementation of minmax algorithm with interface."""

    def __init__(self):
        self.human = -1
        self.computer = +1
        self.board = [[1, 0, 0], [0, 1, 0], [0, 1, 0]]

    def check(self):
        print(self.__is_game_over(self.board))

    def get_move(self):
        """Gets and inserts computer move."""
        board = self.board

        depth = len(self.__empty_cells(board))
        if depth == 0 or self.__is_game_over(board):
            return False

        if depth == 9:
            x = rnd.choice([0, 1, 2])
            y = rnd.choice([0, 1, 2])
        else:
            move = self.__run_algorithm(board, depth, self.computer)
            x, y = move[0], move[1]
        self.board[x][y] = +1

    def __run_algorithm(self, board: list, depth: int, player: int) -> list:
        """Recursion function which return the best row, col and score."""
        # print(self.board)

        if player == self.computer:
            best = [-1, -1, -inf]
        else:
            best = [-1, -1, +inf]

        if depth == 0 or self.__is_game_over(board):
            score = self.__evaluate_board(board)
            return [-1, -1, score]

        for cell in self.__empty_cells(board):
            x, y = cell[0], cell[1]
            board[x][y] = player

            score = self.__run_algorithm(board, depth - 1, -player)
            board[x][y] = 0

            score[0], score[1] = x, y

            if player == self.computer:
                if score[2] > best[2]:
                    best = score
            else:
                if score[2] < best[2]:
                    best = score
        return best

    def __check_win_positon(self, board: list, player: int) -> bool:
        """Checks if current board position is a win for given player."""
        states = list()  # a list for winning states

        # 3 horizontals, 3 verticals
        states.append([[cell for cell in row] for row in board])
        states.append([[board[cell][col] for cell in range(3)] for col in range(3)])

        # 2 diagonals
        states = [s for l in states for s in l]  # unpack inner lists
        states.append([board[cell][cell] for cell in range(3)])
        states.append([board[x][y] for x, y in zip(range(2, -1, -1), range(3))])

        if 3 * [player] in states:
            # player is met 3 times in the winning states
            return True
        return False

    def __evaluate_board(self, board: list) -> int:
        """Evaluates current board position."""
        if self.__check_win_positon(board, self.computer):
            score = +1
        elif self.__check_win_positon(board, self.human):
            score = -1
        else:
            score = 0
        return score

    def __empty_cells(self, board: list) -> list:
        """Returns position of the empty cells."""
        enm = enumerate
        return [[x, y] for x, row in enm(board) for y, cell in enm(row) if cell == 0]

    def __is_game_over(self, board: list) -> bool:
        """Returns if human or computer won."""
        return self.__check_win_positon(board, self.human) or self.__check_win_positon(
            board, self.computer
        )


a = MinMax()
# a.check()
a.get_move()
print(a.board)
