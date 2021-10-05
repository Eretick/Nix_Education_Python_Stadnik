""" Players module """
import random


class Player:
    """ Basic player class"""


    def __init__(self, name):
        self._name = name
        # all possible cells numbers for moving. Assigned from Game.__create_players()
        self.all_points = []
        self.marked_cells = []

    def move(self):
        """ Simple player's move function. Returns the 1st symbol in case of mistyping"""
        return int(input(f"Ход игрока {self.name} (номер ячейки):")[0])

    @property
    def name(self):
        """ Player's name """
        return self._name


class Computer(Player):
    """ AI class based on Player """
    GOOD_POINTS = [1, 3, 7, 9, 5]

    def __init__(self, name):
        super().__init__(name)
        self.marked_cells = []  # convert inherited class variable marked_cells to instance variable

    def __is_free(self, point):
        """ Finding free cell internal algoritm  """
        return random.choice(self.all_points)

    def move(self):
        """ Computer tries to move in free cell. If cell is busy, it tries again. """
        move = self.__is_free(random.choice(self.all_points))
        if move not in self.marked_cells:
            return move
        self.move()
        return None
