from disk import Disk


class Board:
    def __init__(self, n):
        self.n = n
        self.mat = [[Disk.NONE for i in range(n)] for j in range(n)]

    def set_board(self, x, y, disk):
        self.mat[x][y] = disk

    def board_size(self):
        return self.n

    def get_board_value(self, i, j):
        return self.mat[i][j]

    def board_is_full(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.mat[i][j] == Disk.NONE:
                    return False
        return True

    def out_of_bound(self, row, col):
        """
        check if the given indexes are out of bound of the matrix
        """
        return row > self.board_size() - 1 or row < 0 or col > self.board_size() - 1 or col < 0





