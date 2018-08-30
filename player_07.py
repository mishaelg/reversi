from abstractplayer import AbstractPlayer
from rules import Rules
import copy
from disk import Disk
import math
from datetime import datetime
from datetime import timedelta

class Player07(AbstractPlayer):
    def __init__(self, color, time_per_turn=5, game=None):
        super().__init__(color, time_per_turn)
        self.game = game

    def get_move(self, board, possible_moves):
        try:
            return self.game.opening_book[self.game.all_moves]
        except KeyError:
            self.current_time = datetime.now()
            self.had_time = True
            depth = int(math.log(self.time_per_turn, 2) + 1)  # adaptive start depth, based on how much time was given on start
            node_counter = 0
            if not hasattr(self, 'weighted_mat'):
                self.weighted_mat = self.game.rules.create_weight_mat(board.board_size())  # if the player doesnt have a weighted list already, create one (save calculation time later)
            max_val = -math.inf
            moves = list(possible_moves.keys())  # all the possible moves by list
            while True:  # running through the first level of nodes, with increasing depth until there is no more time
                temp_board = copy.deepcopy(board)
                self.game.rules.update_board(temp_board, moves[node_counter], possible_moves, self.color)
                if self.game.rules.check_win(temp_board, Disk(3-self.color.value)) and self.game.rules.find_winner(temp_board, temp_board.board_size()) == self.color:  # if after the update the other player has no moves, and i won
                        return moves[node_counter]  # this is winning condition, therefore i should pick that
                temp_val = self.minimax(depth, temp_board, False)  # the value of the heuristics
                if not self.had_time: # if time is about to ran out
                    if (datetime.now() - self.current_time).seconds > self.time_per_turn:
                        raise TimeoutError(f"Player {self.color} has lost because he ran out of time")  # if we ran out of time we lost
                    return moves[max_index]  # return the best move we found so far
                if temp_val > max_val:
                    max_val = temp_val
                    max_index = node_counter
                if node_counter == len(moves) - 1: # if we reached the final node, we go from the start again, with more depth
                    node_counter = 0
                    depth += 1
                else:
                    node_counter += 1

    def minimax(self, depth, board, maximizing_player):
        """
        :param depth: depth of the recursion
        :param board: the node
        :param maximizing_player: True if the maximizing player turn to play, False else
        :return: the node(Board) with the highest heuristic value
        """
        if depth == 0 or self.game.rules.check_win(board, self.color if maximizing_player else Disk(3 - self.color.value)):  # terminal node, either the board is full or both players are out of moves
            return self.heuristic_score(board)
        if self.time_per_turn - (datetime.now() - self.current_time).seconds < 0.001:
            self.had_time = False
            return
        if maximizing_player:
            max_val = -math.inf
            possible_moves = self.game.rules.get_move_list(board, self.color)  # gets all the moves
            if len(possible_moves) == 0:
                return self.minimax(depth - 1, board, False)
            moves = list(possible_moves.keys())  # all the possible moves by list
            for move in moves:
                temp_board = copy.deepcopy(board)
                self.game.rules.update_board(temp_board, move, possible_moves, self.color)
                checker = self.minimax(depth-1, temp_board, False)
                if not self.had_time:
                    return  # if he didn't have time, collapse the recursion
                max_val = max(max_val, checker)
            return max_val
        else:  # now its the minimizing player's turn
            min_val = math.inf
            possible_moves = self.game.rules.get_move_list(board, Disk(3-self.color.value))  # gets all the moves
            if len(possible_moves) == 0:
                return self.minimax(depth - 1, board, True)
            moves = list(possible_moves.keys())  # all the possible moves by list
            for move in moves:
                temp_board = copy.deepcopy(board)
                self.game.rules.update_board(temp_board, move, possible_moves, Disk(3-self.color.value))
                checker = self.minimax(depth - 1, temp_board, True)
                if not self.had_time:
                    return  # if he didn't have time, collapse the recursion
                min_val = min(min_val, checker)

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