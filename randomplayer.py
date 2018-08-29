from abstractplayer import AbstractPlayer
import random


class RandomPlayer(AbstractPlayer):
    def __init__(self, color, time=5, rules=None, UI=None):
        super().__init__(color, time)

    def get_move(self, board, possible_moves):
        """
        select a possible move in random
        """
        return random.choice(list(possible_moves.keys()))  # randomly selects a key from possible moves