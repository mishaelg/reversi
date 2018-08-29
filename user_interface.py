from disk import Disk
import re


class UI:
    def board_print(self, board):
        n = board.board_size()
        first_row = '  |'
        separator = '--+' + '---+' * n
        for i in range(n):
            first_row += ' ' + chr(ord('a') + i) + ' |'
        print(first_row)
        print(separator)
        for i in range(n):
            if i < 9:
                new_row = ' ' + str(i + 1) + '|'
            else:
                new_row = str(i + 1) + '|'
            for j in range(n):
                if board.get_board_value(i, j) == Disk.NONE:
                    new_row += "   " + "|"
                elif board.get_board_value(i, j) == Disk.DARK:
                    new_row += " x " + "|"
                else:
                    new_row += " o " + "|"
            print(new_row)
            print(separator)

    def print_list(self, player, moves_list):
        print(f"{'x' if player == Disk.DARK else 'o' } its your turn ")
        print("possible moves are: ", end='')
        for move in moves_list.keys():
            print(f"({move[0]+1}, {chr(ord('a') + move[1])}), ", end='')
        print("")

    def start_message(self):
        choice_list = ["HumanPlayer", "RandomPlayer", "SimplePlayer", "Player07"]
        print("Hello, welcome to reversi")
        while True:
            try:
                n = int(input("Enter the size of the board you would like to play: "))
                break
            except TypeError or ValueError:
                print("Enter a valid number pls")

        while True:
            print("Please enter what type of player is player 1: ", end='')
            for i, name in enumerate(choice_list[:-1]):
                print(f"{i}-{name}, ", end='')
            print(f"{i+1}-{choice_list[i+1]}", end='')
            try:
                opt1 = int(input(": "))
                if opt1 > -1 and opt1 < len(choice_list):
                    break
                else:
                    raise TypeError
            except TypeError:
                print("Enter a valid number")
        while True:
            try:
                opt2 = int(input("Enter type of player 2: "))
                if opt2 > -1 and opt2 < len(choice_list):
                    break
                else:
                    raise TypeError
            except TypeError:
                print("Enter a valid number")

        return n, choice_list[opt1], choice_list[opt2]

    @staticmethod
    def get_move(possible_moves):
            while True:
                new_move = input("Please choose enter 1 legal move: ")
                args = re.search(r"\A(\d+),\s*(\w)\Z", new_move)
                if args is None:
                    print("Please enter in a valid row,column format")
                    continue
                row, col = args.groups()
                row = int(row)
                row -= 1
                col = ord(col) - ord('a')
                if (row, col) not in possible_moves.keys():
                    print("Not a valid move! please choose one from the list")
                    continue

                return row, col

    def print_winners(self, winner):
        if winner == Disk.DARK:
            print("x player has won")
        elif winner == Disk.LIGHT:
            print("o player has won")
        elif winner == Disk.NONE:
            print("This is a tie")
        print("Thank you for playing, Goodbye")

    def print_stop_message(self, player):
        """ prints if there are no more possible moves"""
        print(f"Player {'x' if player.color == Disk.DARK else 'o'} has no possible moves.")

    def print_gap(self, board):
        """ just a spacer between two board prints"""
        print("")
        print("-" * board.board_size() * 4)
        print("")