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
        self.my_rules = Rules()
        self.UI = UI()

    def initiate_game(self):
        player_time = 5
        n, opt1, opt2 = self.UI.start_message()
        self.board = Board(n)
        self.my_rules.start_board(self.board)
        game_players = PlayersList(eval(opt1)(Disk.DARK, player_time, self.UI, self.my_rules))
        game_players.add_next(eval(opt2)(Disk.LIGHT, player_time, self.UI, self.my_rules))
        self.game_players = game_players
        self.play_game()

    def play_game(self):
        player = self.game_players.get_next()
        while True:
            player = self.game_players.get_next()
            moves_list = self.my_rules.get_move_list(self.board, player.color)
            self.UI.board_print(self.board)
            if len(moves_list) == 0:
                self.UI.print_stop_message(player)
                self.turns += 1
                if self.turns == 2:
                    winner = self.my_rules.find_winner(self.board, self.board.board_size())
                    self.UI.print_winners(winner)
                    return winner
                    break
                continue
            else:
                self.turns = 0
                move = player.get_move(self.board, moves_list)
                self.my_rules.update_board(self.board, move, moves_list, player.color)
                self.UI.print_gap(self.board)

