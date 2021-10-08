""" Console Tic-tac-toe """
import datetime
import logging
import random
import sys

from players import Player, Computer
from grid import Grid

WINNERS_FILE = "winners.log"

# file logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("winners_logger")
log_handler = logging.FileHandler(f"{WINNERS_FILE}", encoding='utf-8')
log_handler.setLevel(logging.DEBUG)
logger.addHandler(log_handler)


class Game:
    """ Main game class """
    all_points = list(range(1, 10))
    current_player = None
    win_comb = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7],
                [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
    marked_cells = []

    def __init__(self):
        # objects defined later
        self.grid = None
        self.player1 = None
        self.player2 = None

    def start(self, versus=False):
        # begin new game
        self.new_game(versus)

    def new_game(self, versus):
        """ Game reset func """
        self.grid = Grid()
        self.all_points = list(range(1, 10))
        self.__create_players(versus)
        self.marked_cells.clear()
        self.main()

    def revenge(self):
        """ Continue playing with the same players """
        self.grid = Grid()
        self.all_points = list(range(1, 10))
        self.player1.marked_cells.clear()
        self.player2.marked_cells.clear()
        self.marked_cells.clear()
        self.main()

    def __create_players(self, versus):
        """ Functions for recreating players every game.
        Depends on bool versus mode (user/user or user/AI) """
        print("Игрок 1:")
        self.player1 = Player(self.__set_player_name())
        self.player1.marked_cells.clear()
        if versus is True:
            print("Игрок 2:")
            self.player2 = Player(self.__set_player_name())
            self.player2.marked_cells.clear()
        else:
            self.player2 = Computer("Computer")
            self.player2.all_points = list(self.all_points)

    def show_menu(self):
        """ Main menu """
        print("---------Начать--------")
        print("---Друг против друга---")
        print("-----История побед-----")
        print("---------Выход---------")
        print("Выберите один из тов: начать/против/история/выход")
        self.__menu_check()

    @staticmethod
    def __choice():
        """ Internal shortcart for user input """
        return input("Введите свой выбор:")

    @staticmethod
    def __set_player_name():
        """ Player setup """
        name = input("Введите свое имя: ")
        return name

    @staticmethod
    def __compare(var, template):
        """ Simple comparing internal shortcut. Returns True if var==template. """
        return var.lower() == template.lower()

    def __menu_check(self):
        """ Menu choice """
        choice = self.__choice()
        if self.__compare(choice, "Начать"):
            self.start()
        if self.__compare(choice, "Против"):
            self.start(versus=True)
        elif self.__compare(choice, "История"):
            self.history()
        elif self.__compare(choice, "Выход"):
            self._exit()

    def main(self, versus=False):
        """ Main game loop """
        self.current_player = self.__choose_first_player()
        print(self.grid.check_filled())
        while not self.grid.check_filled():
            winner = self.check_win()
            if winner:
                print(f"Победил игрок {winner.name}!")
                self._log_results(winner)
                break
            if isinstance(self.current_player, Player):
                self.show_status()
            self._next_move()
            self.__change_player()
        print("Игра окончена!")
        if not winner:
            print("Ничья!")
        print("Реванш? (да/нет)")
        choice = self.__compare(self.__choice(), "да")
        if choice:
            self.revenge()
        print("Выйти в меню? (да/нет)")
        choice = self.__compare(self.__choice(), "да")
        if choice:
            self.show_menu()
        self._exit()

    def __choose_first_player(self):
        """ Choose randomly player to make first move """
        choice = random.randint(1, 2)
        if choice == 1:
            self.player1.symbol = "X"
            self.player2.symbol = "O"
            return self.player1
        self.player1.symbol = "O"
        self.player2.symbol = "X"
        return self.player2

    @staticmethod
    def _log_results(winner):
        """ Creating winner logs to WINNERS_FILE document """
        if isinstance(winner, Player):
            date = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            # logger.debug(f"{date} - победил {winner.name}")
            logger.debug("%s - победил %s", date, winner.name)

    def _next_move(self):
        """ Main game players moves logic """
        move = self.current_player.move()
        if move in self.all_points and move not in self.marked_cells:
            self.current_player.marked_cells.append(move)
            self.grid.fill(move, self.current_player.symbol)
            self.marked_cells.append(move)
        else:
            if isinstance(self.current_player, Player):
                print(f"Нельзя походить в ячейку {move}.")
            self._next_move()

    def __change_player(self):
        """ Change player's move turn """
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    @staticmethod
    def _exit():
        """ Just user-friendly console exit """
        input("Выход из игры. Нажмите любую клавишу...")
        sys.exit()

    def history(self):
        """ Showing all players wins history """
        print("История побед/поражений:")
        with open(WINNERS_FILE, "r", encoding="utf-8") as file:
            text = file.read()
            if text != "":
                print(text)
            else:
                print("Здесь пока нет истории. Начните новую игру!")
                self.show_menu()

    def show_status(self):
        """ Showing current grid state """
        self.grid.show()

    def check_win(self):
        """ Check did player maked a line """
        for part in self.win_comb:
            part = set(part)
            if part.issubset(set(self.player1.marked_cells)):
                print(self.player1.marked_cells)
                return self.player1
            if part.issubset(set(self.player2.marked_cells)):
                print(self.player2.marked_cells)
                return self.player2
        return False
