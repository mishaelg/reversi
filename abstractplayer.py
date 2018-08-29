from abc import ABC, abstractmethod
from disk import Disk


class AbstractPlayer(ABC):
    """Your player must inherit from this class, and your player class name must be 'PlayerXX' where XX is
    your computer number, like this: "class Player05(AbstractPlayer):"
    """

    def __init__(self, color, time_per_turn=5):
        """
        :param color: The color of the player, of type Disk
        :param time_per_turn: Allowed move calculation time per turn (in seconds)
        """
        self.color = color
        self.time_per_turn = time_per_turn

    @abstractmethod
    def get_move(self, board, possible_moves):
        """Chooses an action from the given actions

        :param board: The current board state. It is a matrix whose cells are of the enum type Disk.
        :param possible_moves: A list of possible moves. Each move is a tuple of coordinates (x, y).
        :return: The desired move in the list of possible moves (a tuple).
        """
        pass

    def __str__(self):
        if self.color == Disk.DARK:
            return 'X'
        return 'O'