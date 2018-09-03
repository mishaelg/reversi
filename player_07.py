from abstractplayer import AbstractPlayer
from rules import Rules
import copy
from disk import Disk
import math
from datetime import datetime
from datetime import timedelta
import random

class Player07(AbstractPlayer):
    def __init__(self, color, time_per_turn=5, game=None):
        super().__init__(color, time_per_turn)
        self.game = game

    def get_move(self, board, possible_moves):
        if self.game.all_moves == '':  # first of the game, doesn't matter what you pick
            return random.choice(list(possible_moves.keys()))
        try:
            return self.game.opening_book[self.game.all_moves]
        except KeyError:
            self.current_time = datetime.now()
            self.had_time = True
            depth = int(math.log(self.time_per_turn, 2))  # adaptive start depth, based on how much time was given on start
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
                temp_val = self.minimax(depth, temp_board, False, -math.inf, math.inf)  # the value of the heuristics
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

    def minimax(self, depth, board, maximizing_player, alpha, beta):
        """
        :param depth: depth of the recursion
        :param board: the node
        :param maximizing_player: True if the maximizing player turn to play, False else
        :return: the node(Board) with the highest heuristic value
        """
        if depth == 0:
            return self.heuristic_score(board)
        if self.game.rules.check_win(board, self.color if maximizing_player else Disk(3 - self.color.value)):# terminal node, either the board is full or both players are out of moves
            if self.game.rules.find_winner(board, board.board_size()) == self.color:  # if the player won, this is the optimum move
                return math.inf
            else:  # playing to win baby!
                return -math.inf
        if self.time_per_turn - (datetime.now() - self.current_time).seconds < 0.01 * self.time_per_turn:
            self.had_time = False
            return
        if maximizing_player:
            max_val = -math.inf
            possible_moves = self.game.rules.get_move_list(board, self.color)  # gets all the moves
            if len(possible_moves) == 0:
                return self.minimax(depth - 1, board, False, alpha, beta)
            moves = list(possible_moves.keys())  # all the possible moves by list
            for move in moves:
                temp_board = copy.deepcopy(board)
                self.game.rules.update_board(temp_board, move, possible_moves, self.color)
                checker = self.minimax(depth-1, temp_board, False, alpha, beta)
                if not self.had_time:
                    return  # if he didn't have time, collapse the recursion
                max_val = max(max_val, checker)
                alpha = max(max_val, alpha)
                if alpha > beta:
                    break
            return max_val
        else:  # now its the minimizing player's turn
            min_val = math.inf
            possible_moves = self.game.rules.get_move_list(board, Disk(3-self.color.value))  # gets all the moves
            if len(possible_moves) == 0:
                return self.minimax(depth - 1, board, True, alpha, beta)
            moves = list(possible_moves.keys())  # all the possible moves by list
            for move in moves:
                temp_board = copy.deepcopy(board)
                self.game.rules.update_board(temp_board, move, possible_moves, Disk(3-self.color.value))
                checker = self.minimax(depth - 1, temp_board, True, alpha, beta)
                if not self.had_time:
                    return  # if he didn't have time, collapse the recursion
                min_val = min(min_val, checker)
                beta = min(min_val, beta)
                if alpha > beta:
                    break
            return min_val

    def heuristic_score(self, board):  # the heuristic score of each node
        score = 0
        new_mat = self.weighted_mat
        ## if we already have disk in the corner- now the squares near the corner worth a lot more
        if board.get_board_value(0, 0) == self.color:
            new_mat[0][1] = 1
            new_mat[1][0] = 1
            new_mat[1][1] = 1
        if board.get_board_value(7, 7) == self.color:
            new_mat[6][7] = 1
            new_mat[7][6] = 1
            new_mat[6][6] = 1
        if board.get_board_value(0, 7) == self.color:
            new_mat[1][7] = 1
            new_mat[0][6] = 1
            new_mat[1][6] = 1
        if board.get_board_value(7, 0) == self.color:
            new_mat[6][1] = 1
            new_mat[7][1] = 1
            new_mat[6][1] = 1
        for i in range(board.board_size()):
            for j in range(board.board_size()):  # running through all the board
                if board.get_board_value(i, j) == self.color:
                    score += new_mat[i][j]
                elif board.get_board_value(i, j) == Disk.NONE:
                    pass
                else:
                    score -= new_mat[i][j]
        return score