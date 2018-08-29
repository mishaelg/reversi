class PlayersList:
    """
    creates a list of player in a cycle list
    """
    def __init__(self, head):
        head = PlayerNode(head)
        self.head = head
        self.current = head

    def get_current(self):
        """
        :return: current player
        """
        return self.current.player

    def add_next(self, player):
        player = PlayerNode(player)
        self.head.next = player
        player.next = self.head
        player.current = self.head.next

    def get_next(self):
        """
        :return:  set the current as next in list, return the next player
        """
        self.current = self.current.next
        return self.current.player


class PlayerNode:
    def __init__(self, player, next=None):
        self.player = player
        self.next = next

