from abstractplayer import AbstractPlayer
from rules import Rules
import copy
from disk import Disk
import math


class SimplePlayer(AbstractPlayer):
    def __init__(self, color, time_per_turn=5, UI=None, rules=None):
        super().__init__(color, time_per_turn)
        self.rules = rules
        self.UI = UI

    def get_move(self, board, possible_moves):
        max_val = -math.inf
        moves = list(possible_moves.keys()) # all the possible moves by list
        for i, move in enumerate(moves):  # possible moves
            temp_board = copy.deepcopy(board)
            self.rules.update_board(temp_board, move, possible_moves, self.color)
            if len(self.rules.get_move_list(temp_board, Disk(3 - self.color.value))) == 0:  # if after the update the other player has no moves
                if len(self.rules.get_move_list(temp_board, self.color)) == 0:  # see if this player has no moves also
                    return moves[i]  # this is winning condition, therefore i should pick that
            temp_val = self.find_score(temp_board) # the score for each node
            if temp_val > max_val:
                max_val = temp_val
                max_index = i
        return moves[max_index]

    def find_score(self, board):
        dark_count, white_count = self.rules.count_pieces(board, board.board_size())
        if self.color == Disk.DARK:
            return dark_count - white_count
        else:
            return white_count - dark_count