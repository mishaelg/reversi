from abstractplayer import AbstractPlayer
from rules import Rules
import copy
from disk import Disk
import math
from datetime import datetime
from datetime import timedelta

class Player07(AbstractPlayer):
    def __init__(self, color, time_per_turn=5, UI=None, rules=None):
        super().__init__(color, time_per_turn)
        self.rules = rules
        self.UI = UI

    def get_move(self, board, possible_moves):
        self.current_time = datetime.now()
        self.had_time = True
        depth = int(math.log(self.time_per_turn, 2)) #adaptive start depth, based on how much time was given on start
        node_counter = 0
        if not hasattr(self, 'weighted_mat'):
            self.weighted_mat = self.rules.create_weight_mat(board.board_size())  # if the player doesnt have a weighted list already, create one (save calculation time later)
        max_val = -math.inf
        moves = list(possible_moves.keys())  # all the possible moves by list
        while True:  # running through the first level of nodes, with increasing depth until there is no more time
            temp_board = copy.deepcopy(board)
            self.rules.update_board(temp_board, moves[node_counter], possible_moves, self.color)
            if self.rules.check_win(temp_board, Disk(3-self.color.value)) and self.rules.find_winner(temp_board, temp_board.board_size()) == self.color:  # if after the update the other player has no moves, and i won
                    return moves[node_counter]  # this is winning condition, therefore i should pick that
                temp_val = self.minimax(3, temp_board, False)  # the value of the heuristics
                if temp_val > max_val:
                    max_val = temp_val
                    max_index = i
        return moves[max_index]

    def minimax(self, depth, board, maximizing_player):
        """
        :param depth: depth of the recursion
        :param board: the node
        :param maximizing_player: True if the maximizing player turn to play, False else
        :return: the node(Board) with the highest heuristic value
        """
        if depth == 0 or self.rules.check_win(board, self.color if maximizing_player else Disk(3 - self.color.value)):  # terminal node, either the board is full or both players are out of moves
            return self.heuristic_score(board)
        if self.time_per_turn - (datetime.now - self.current_time).second < 0.2:
            self.had_time = False
            return
        if maximizing_player:
            max_val = -math.inf
            possible_moves = self.rules.get_move_list(board, self.color)  # gets all the moves
            if len(possible_moves) == 0:
                return self.minimax(depth - 1, board, False)
            moves = list(possible_moves.keys())  # all the possible moves by list
            for move in moves:
                temp_board = copy.deepcopy(board)
                self.rules.update_board(temp_board, move, possible_moves, self.color)
                max_val = max(max_val, self.minimax(depth-1, temp_board, False))
                if not self.had_time:
                    return  # if he didn't have time, collapse the recursion
            return max_val
        else:  # now its the minimizing player's turn
            min_val = math.inf
            possible_moves = self.rules.get_move_list(board, Disk(3-self.color.value))  # gets all the moves
            if len(possible_moves) == 0:
                return self.minimax(depth - 1, board, True)
            moves = list(possible_moves.keys())  # all the possible moves by list
            for move in moves:
                temp_board = copy.deepcopy(board)
                self.rules.update_board(temp_board, move, possible_moves, Disk(3-self.color.value))
                min_val = min(min_val, self.minimax(depth - 1, temp_board, True))
                if not self.had_time:
                    return  # if he didn't have time, collapse the recursion
            return min_val

    def heuristic_score(self, board):  # the heuristic score of each node
        score = 0
        for i in range(board.board_size()):
            for j in range(board.board_size()):  # running through all the board
                if board.get_board_value(i, j) == self.color:
                    score += self.weighted_mat[i][j]
                elif board.get_board_value(i, j) == Disk.NONE:
                    pass
                else:
                    score -= self.weighted_mat[i][j]
        return score