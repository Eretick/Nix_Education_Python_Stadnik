""" This is models implementations for MVC pattern """
import random
from abc import ABC, abstractmethod
from settings import WIN_COMBS


class Player(ABC):
    """ Basic player class"""

    def __init__(self, name=""):
        self._name = name
        # all possible cells numbers for moving. Assigned from Game.__create_players()
        self.all_points = []
        self.marked_cells = []
        self.symbol = ""

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

    def set_name(self, name: str):
        """ Method sets name to player instance.
         Argument:
            - name: str
         """
        if isinstance(name, str):
            self._name = name
        else:
            raise TypeError("Player's name must be string only!")

    def remove_from_all(self, move):
        """ Remove maked move from all available moves """
        if move in self.all_points:
            self.all_points.remove(move)


class Person(Player):
    """ Player's model based on abstract Player class """

    def move(self, option):
        """ Simple player's move function. Returns the 1st symbol in case of mistyping"""
        return int(option)


class Computer(Player):
    """ AI's model based on abstract Player class """

    def __init__(self, name):
        super().__init__(name)
        self.marked_cells = []  # convert inherited class variable marked_cells to instance variable

    def __is_free(self):
        """ Internal algoritm of finding free cell.
        Outdated after adding MINIMAX algorythm. Keep cause of "out of nostalgic feelings" :D
        """
        return random.choice(self.all_points)

    def move(self):
        """ Computer tries to move in free cell. If cell is busy, it tries again. """
        move = self.__is_free()
        if move not in self.marked_cells:
            return move
        self.move()
        return None


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

    def check_filled(self, tactics=None):
        """ Returns False if Grid has a cell for move.  """
        if tactics is None:
            cells = self.cells
        else:
            cells = tactics["grid"]
        return not any(list(str(x).isdigit() for x in cells))

    def fill(self, cell_number, symbol):
        """ Marking the cell by player's symbol """
        self.cells[cell_number-1] = symbol

    def reset_cells(self):
        """ Reset cells grid's model cells to default state.  """
        self.cells = list(range(1, 10))


class Game:
    """ Game model """

    marked_cells = []
    all_points = list(range(1, 10))
    current_player = None

    def __init__(self, mode="console"):
        self.mode = mode
        self.player1 = None
        self.player2 = None

    def create_players(self, versus):
        """ Functions for recreating players every game.
        Depends on bool versus mode (user/user or user/AI) """
        self.player1 = Person()
        self.player1.all_points = self.all_points
        self.player1.marked_cells.clear()
        if versus is True:
            self.player2 = Person()
            self.player2.all_points = self.all_points
            self.player2.marked_cells.clear()
        else:
            self.player2 = Computer("Computer")
            self.player2.all_points = list(self.all_points)

    def prepare_new_game(self, versus=False):
        """ Game reset func """
        self.all_points = list(range(1, 10))
        self.create_players(versus)
        self.marked_cells.clear()

    @staticmethod
    def set_player_name(player: Person, name: str):
        """ Person setup """
        player.set_name(name)

    def choose_first_player(self):
        """ Choose randomly player to make first move """
        choice = random.randint(1, 2)
        if choice == 1:
            self.player1.symbol = "X"
            self.player2.symbol = "O"
            return self.player1
        self.player1.symbol = "O"
        self.player2.symbol = "X"
        return self.player2

    def revenge(self):
        """ Continue playing with the same players """
        self.all_points = list(range(1, 10))
        self.player1.marked_cells.clear()
        self.player2.marked_cells.clear()
        self.marked_cells.clear()

    def check_win(self, tactics: dict = None):
        """ Check did player maked a line """
        for part in WIN_COMBS:
            part = set(part)
            if tactics is None:
                if part.issubset(set(self.player1.marked_cells)):
                    return self.player1
                if part.issubset(set(self.player2.marked_cells)):
                    return self.player2
            else:
                if isinstance(tactics, dict):
                    grid = tactics["grid"]
                    player = tactics["player"]
                    grid_part = [grid[i-1] for i in part]
                    if all(player.symbol == i for i in grid_part):
                        return player
                else:
                    raise TypeError("tactics argument must be a dict!")
        return False
