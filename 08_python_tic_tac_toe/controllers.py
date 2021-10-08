""" Console Tic-tac-toe """
import datetime
import logging
import random
import sys
from models import Person, Computer
from views import ConsoleUI, GraphicUI
from settings import *


class Game:
    """ Main game class """
    all_points = list(range(1, 10))
    current_player = None
    marked_cells = []

    def __init__(self, mode="console"):
        """
        :param mode: game mode, "console" or "graphic". Defines an user interface type.
            default -> "console"
        """
        # objects defined later
        self.menu_options = ["Начать", "Против", "История", "Выхода"]
        self.player1 = None
        self.player2 = None
        self.mode = mode
        if self.mode == "console":
            self.ui = ConsoleUI()
        else:
            self.ui = GraphicUI()


    def start(self, versus=False):
        """ New game entry point """
        self.new_game(versus=versus)

    def new_game(self, versus=False):
        """ Game reset func """
        self.ui = ConsoleUI()
        self.all_points = list(range(1, 10))
        self.__create_players(versus)
        self.marked_cells.clear()
        self.main()

    def revenge(self):
        """ Continue playing with the same players """
        self.ui = ConsoleUI()
        self.all_points = list(range(1, 10))
        self.player1.marked_cells.clear()
        self.player2.marked_cells.clear()
        self.marked_cells.clear()
        self.main()

    def __create_players(self, versus):
        """ Functions for recreating players every game.
        Depends on bool versus mode (user/user or user/AI) """
        self.ui.print("Игрок 1:")
        self.player1 = Person(self.__set_player_name())
        self.player1.marked_cells.clear()
        if versus is True:
            self.ui.print("Игрок 2:")
            self.player2 = Person(self.__set_player_name())
            self.player2.marked_cells.clear()
        else:
            self.player2 = Computer("Computer")
            self.player2.all_points = list(self.all_points)

    def show_menu(self):
        """ Main menu """
        self.ui.show_menu()
        if self.mode == "console":
            self.menu_check(self.ui.menu_check())

    def menu_check(self, option):
        if option == self.menu_options[0].lower():
            self.new_game()
        if option == self.menu_options[1].lower():
            self.new_game(versus=True)
        elif option == self.menu_options[2].lower():
            self.history()
        elif option == self.menu_options[3].lower():
            self._exit()
        else:
            logging.debug("No match")

    def __set_player_name(self):
        """ Person setup """
        name = self.ui.input("Введите свое имя: ")
        return name

    @staticmethod
    def __compare(var, template):
        """ Simple comparing internal shortcut. Returns True if var==template. """
        return var.lower() == template.lower()

    def main(self, versus=False):
        """ Main game loop """
        self.current_player = self.__choose_first_player()
        while not self.ui.grid.check_filled():
            winner = self.check_win()
            if winner:
                self.ui.print(f"Победил игрок {winner.name}!")
                self._log_results(winner)
                break
            if isinstance(self.current_player, Person):
                self.show_status()
            self._next_move()
            self.__change_player()
        self.ui.print("Игра окончена!")
        if not winner:
            self.ui.print("Ничья!")
        self.ui.print("Реванш? (да/нет)")
        choice = self.__compare(self.ui.choice(), "да")
        if choice:
            self.revenge()
        self.ui.print("Выйти в меню? (да/нет)")
        choice = self.__compare(self.ui.choice(), "да")
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
        if isinstance(winner, Person):
            date = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            # logger.debug(f"{date} - победил {winner.name}")
            logger.debug("%s - победил %s", date, winner.name)

    def _next_move(self):
        """ Main game players moves logic """
        if isinstance(self.current_player, Person):
            point = self.ui.input(f"Ход игрока {self.current_player.name} (номер ячейки):")[0]
            move = int(self.current_player.move(point))
        elif isinstance(self.current_player, Computer):
            move = self.current_player.move()
        if move in self.all_points and move not in self.marked_cells:
            self.current_player.add_marked(move)
            self.ui.grid.fill(move, self.current_player.symbol)
            self.marked_cells.append(move)
        else:
            if isinstance(self.current_player, Person):
                self.ui.print(f"Нельзя походить в ячейку {move}.")
            self._next_move()

    def __change_player(self):
        """ Change player's move turn """
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def _exit(self):
        """ Just user-friendly console exit """
        self.ui.exit()
        sys.exit()

    def history(self):
        """ Showing all players wins history """
        self.ui.print("История побед/поражений:")
        self.ui.show_history()
        if self.mode == "console":
            self.show_menu()

    def show_status(self):
        """ Showing current grid state """
        self.ui.grid.show()

    def check_win(self):
        """ Check did player maked a line """
        for part in WIN_COMBS:
            part = set(part)
            if part.issubset(set(self.player1.marked_cells)):
                return self.player1
            if part.issubset(set(self.player2.marked_cells)):
                return self.player2
        return False

