from abstractplayer import AbstractPlayer
from rules import Rules
import copy
from disk import Disk
import math


class Player07(AbstractPlayer):
    def __init__(self, color, time_per_turn=5, UI=None, rules=None):
        super().__init__(color, time_per_turn)
        self.rules = rules
        self.UI = UI

    def get_move(self, board, possible_moves):
        max_val = -math.inf
        moves = list(possible_moves.keys())  # all the possible moves by list
        for i, move in enumerate(moves):  # possible moves
            temp_board = copy.deepcopy(board)
            self.rules.update_board(temp_board, move, possible_moves, self.color)
            if len(self.rules.get_move_list(temp_board, Disk(3 - self.color.value))) == 0:  # if after the update the other player has no moves
                if len(self.rules.get_move_list(temp_board, self.color)) == 0:  # see if this player has no moves also
                    return moves[i]  # this is winning condition, therefore i should pick that
            temp_val = self.minimax(2, temp_board, self.color)  # the value of the herustics

            if temp_val > max_val:
                max_val = temp_val
                max_index = i
        return moves[max_index]

    def minimax(self, depth, board, maximizing_player):
        """
        :param depth: depth of the recursion
        :param board: the node
        :param maximizing_player: True if the maxizmazing player turn to play, False else
        :return: the node(Board) with the highest heuristic value
        """
        if depth == 0 or self.rules.check_win(board, self.color if maximazing_player else Disk(3 - self.color.value)):
            return self.heuristic_score(board)
        if maximazing_player:
            max_val = -math.inf
            possible_moves = self.rules.get_move_list(board, self.color) #gets all the moves
            if len(possible_moves) == 0:
                return self.minimax(depth - 1, board, False)
            moves = list(possible_moves.keys())  # all the possible moves by list
            for move in moves:
                temp_board = copy.deepcopy(board)
                self.rules.update_board(temp_board, move, possible_moves, self.color)
                new_val = self.minimax(depth-1, temp_board, False)
                if new_val > max_val:
                    max_val = new_val
            return max_val
        else:
            min_val = math.inf
            possible_moves = self.rules.get_move_list(board, Disk(3-self.color.value))  # gets all the moves
            if len(possible_moves) == 0:
                return self.minimax(depth - 1, board, True)
            moves = list(possible_moves.keys())  # all the possible moves by list
            for move in moves:
                temp_board = copy.deepcopy(board)
                self.rules.update_board(temp_board, move, possible_moves, Disk(3-self.color.value))
                new_val = self.minimax(depth - 1, temp_board, True)
                if new_val < min_val:
                    min_val = new_val
            return min_val

    def heuristic_score(self, board):
        dark_count, white_count = self.rules.count_pieces(board, board.board_size())
        if self.color == Disk.DARK:
            return dark_count - white_count
        else:
            return white_count - dark_count