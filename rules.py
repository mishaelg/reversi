from board import Board
from disk import Disk


class Rules:
    def start_board(self, board):
        n = board.board_size()
        board.set_board(n//2 - 1, n // 2 - 1, Disk.LIGHT)
        board.set_board(n // 2, n // 2, Disk.LIGHT)
        board.set_board(n // 2, n // 2-1, Disk.DARK)
        board.set_board(n // 2-1, n // 2, Disk.DARK)

    def update_board(self, board, move, moves, player):
        for direction in moves[move]:
            i, j = direction
            row, col = move
            board.set_board(row, col, player)
            jump_i = i - row
            jump_j = j - col
            while True:
                if board.out_of_bound(i, j) or board.get_board_value(i, j) == player:
                    return
                board.set_board(i, j, player)
                i += jump_i
                j += jump_j


    def get_move_list(self, board, player):
        """

        :param board:
        :param player:
        :return: A dictionary containing possible moves as keys, and where they came from as values
        """
        moves = {}
        for i in range(board.board_size()):  # looping through all the squares
            for j in range(board.board_size()):
                if board.get_board_value(i, j).value == 3 - player.value:  # this square contains enemy player's disk
                    for candidate_spot in self.find_vacant_spots(i, j, board):
                        row, col = candidate_spot
                        if self.is_valid_move(i, j, row, col, board, player):
                            try:
                                moves[(row, col)].append((i, j))
                            except KeyError:
                                moves[(row, col)] = [(i, j)]
        return moves

    def is_valid_move(self, i, j, row, col, board, player):
        jump_i = i - row
        jump_j = j - col
        while True:
            i += jump_i
            j += jump_j
            if board.out_of_bound(i, j):
                return False
            if board.get_board_value(i, j) == player: # found the player disk on the opposite side
                return True

    def find_vacant_spots(self, i, j, board):
        """
        :param i: row
        :param j: column
        :param board: the board
        :return: list of all vacant squares around given location
        """
        vacant_squares = []
        for row in range(i-1, i+2):
            for col in range(j-1, j+2):
                if board.out_of_bound(row, col):
                    continue
                if board.get_board_value(row, col) == Disk.NONE:  # found the vacant spot
                    vacant_squares.append((row, col))
        return vacant_squares

    def check_win(self, board, player):
        return board.board_is_full() or (len(self.get_move_list(board, player)) == 0 and len(self.get_move_list(board, Disk(3 - player.value))) == 0)

    def find_winner(self, board, n):
        dark_counter, white_counter = self.count_pieces(board, n)
        if dark_counter > white_counter:
            return Disk.DARK
        elif dark_counter < white_counter:
            return Disk.LIGHT
        else:
            return Disk.NONE


    def count_pieces(self, board, n):
        dark_counter = 0
        white_counter = 0
        for i in range(n):
            for j in range(n):
                if board.get_board_value(i, j) == Disk.DARK:
                    dark_counter += 1
                elif board.get_board_value(i, j) == Disk.LIGHT:
                    white_counter += 1
        return dark_counter, white_counter
