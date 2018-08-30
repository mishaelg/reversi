from abstractplayer import AbstractPlayer
from user_interface import UI


class HumanPlayer(AbstractPlayer):
    def __init__(self, color, time_per_turn=5, game=None):
        super().__init__(color, time_per_turn)
        self.game = game

    def get_move(self, board, possible_moves):
        self.game.UI.print_list(self.color, possible_moves)
        return self.game.UI.get_move(possible_moves)  # I keep this separated in order to make sure all is done in the UI



