
from game_initiator import GameInitiator
from board import Board
from players_list import PlayersList
from disk import Disk
from player_07 import Player07
from humanplayer import HumanPlayer
from simple_player import SimplePlayer
from randomplayer import RandomPlayer



def calc_wins():
    """
    calculates how many time each player won in 100 matches
    """

    dark_wins = 0
    white_wins = 0
    ties = 0
    for i in range(10):
        game = GameInitiator()
        player_time = 10
        game.__setattr__("board", Board(8))
        game.rules.start_board(game.board)
        opt1 = "Player07"
        opt2 = "RandomPlayer"
        game_players = PlayersList(eval(opt1)(Disk.DARK, player_time, game))
        game_players.add_next(eval(opt2)(Disk.LIGHT, player_time, game))
        game.__setattr__("game_players", game_players)
        winner = game.play_game()
        if winner == Disk.DARK:
            dark_wins += 1
        elif winner == Disk.LIGHT:
            white_wins += 1
        else:
            ties += 1
    print(f"x has won {dark_wins}")
    print(f"o has won {white_wins}")
    print(f"{ties} games has been tied")


calc_wins()

