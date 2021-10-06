""" Game models """
import random
from abc import ABC, abstractmethod


class Player(ABC):
    """ Basic player class"""

    def __init__(self, name):
        self._name = name
        # all possible cells numbers for moving. Assigned from Game.__create_players()
        self.all_points = []
        self.marked_cells = []

    @abstractmethod
    def move(self):
        """ Players abstract move method, needs to be recreated in inherit classes """

    @property
    def name(self):
        """ Player's name """
        return self._name

    def add_marked(self, move):
        """ Filling list of confirmed players moves """
        self.marked_cells.append(move)

class Person(Player):
    def move(self, option):
        """ Simple player's move function. Returns the 1st symbol in case of mistyping"""
        return option


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


class ConsoleGrid:
    """ Game field class"""

    def __init__(self):
        self.filled = False
        self.cells = list(range(1, 10))
        self.all_points = []

    def __getitem__(self, item):
        """ Adding getting by index to Grid object """
        return self.cells[item]

    def __setitem__(self, key, value):
        """ Adding getting by index to Grid object """
        self.cells[key] = value

    @property
    def image(self):
        """ Console game grid autoupdated image"""
        return f'''
     ___________
    |   |   |   |
    | {self.cells[0]} | {self.cells[1]} | {self.cells[2]} |
    |___|___|___|
    |   |   |   |
    | {self.cells[3]} | {self.cells[4]} | {self.cells[5]} |
    |___|___|___|
    |   |   |   |
    | {self.cells[6]} | {self.cells[7]} | {self.cells[8]} |
    |___|___|___|
    '''

    def show(self):
        """ Viewing grid image """
        self.filled = self.check_filled()
        print(self.image)

    def check_filled(self):
        """ Returns False if Grid has a cell for move.  """
        return not any(list(str(x).isdigit() for x in self.cells))

    def fill(self, cell_number, symbol):
        """ Marking the cell by player's symbol """
        self.cells[cell_number-1] = symbol

class GraphicGrid:
    pass