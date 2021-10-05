""" Grid module """

class Grid:
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
