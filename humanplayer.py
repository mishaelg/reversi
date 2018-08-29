from abstractplayer import AbstractPlayer
from user_interface import UI


class HumanPlayer(AbstractPlayer):
    def __init__(self, color, time_per_turn=5, UI=None,rules=None):
        super().__init__(color, time_per_turn)
        self.UI = UI

    def get_move(self, board, possible_moves):
        self.UI.print_list(self.color, possible_moves)
        return self.UI.get_move(possible_moves)  # I keep this separated in order to make sure all is done in the UI



