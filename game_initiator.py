from board import Board
from user_interface import UI
from disk import Disk
from rules import Rules
from players_list import PlayersList
from humanplayer import HumanPlayer
from simple_player import SimplePlayer
from randomplayer import RandomPlayer
from player_07 import Player07


class GameInitiator:
    def __init__(self):
        self.turns = 0
        self.rules = Rules()
        self.UI = UI()
        self.all_moves = ''
        self.opening_book = self.create_opening_book()

    def initiate_game(self):
        player_time = 5
        n, opt1, opt2 = self.UI.start_message()
        self.board = Board(n)
        self.rules.start_board(self.board)
        game_players = PlayersList(eval(opt1)(Disk.DARK, player_time, self))
        game_players.add_next(eval(opt2)(Disk.LIGHT, player_time, self))
        self.game_players = game_players
        self.play_game()

    def play_game(self):
        player = self.game_players.get_next()
        while True:
            player = self.game_players.get_next()
            moves_list = self.rules.get_move_list(self.board, player.color)
            self.UI.board_print(self.board)
            if len(moves_list) == 0:
                self.UI.print_stop_message(player)
                self.turns += 1
                if self.turns == 2:
                    winner = self.rules.find_winner(self.board, self.board.board_size())
                    self.UI.print_winners(winner)
                    return winner
                continue
            else:
                self.turns = 0
                move = player.get_move(self.board, moves_list)
                if type(move) is tuple: # this move is calculated
                    if player.color == Disk.DARK:
                        self.all_moves += '+' + chr(ord('a')+move[1]) + str(move[0] + 1)
                    else:
                        self.all_moves += '-' + chr(ord('a')+move[1]) + str(move[0] + 1)
                else:
                    self.all_moves += move
                if type(move) is not tuple:
                    move = (int(move[2]) - 1, ord(move[1]) - ord('a'))
                self.rules.update_board(self.board, move, moves_list, player.color)
                self.UI.print_gap(self.board)

    def create_opening_book(self):
        """

        :return: a dictionary, each key is a set of move, its value is the optimal next move
        """
        f = open('xxx.gam')
        opening_book = {}
        for line in f:
            counter = 3
            while line[counter + 6] != ':':
                new_move = line[0:counter]
                if new_move not in opening_book:
                    opening_book[new_move] = line[counter:counter + 3]
                counter += 3
        f.close()
        return opening_book

