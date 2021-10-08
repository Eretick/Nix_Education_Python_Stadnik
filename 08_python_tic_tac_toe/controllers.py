""" Console Tic-tac-toe """
import datetime
import logging
import random
import sys
from models import Person, Computer, Game, Grid
from views import ConsoleUI, GraphicUI, MENU_OPTIONS
from settings import *


class TicTacToe:
    """ Main game controller class """

    def __init__(self, mode="console"):
        """
        :param mode: game mode, "console" or "graphic". Defines an user interface type.
            default -> "console"
        """
        # objects defined later
        self.game = Game(mode=mode)
        self.ui = self.__create_ui(self.game.mode)
        self.grid = Grid()

    def __create_ui(self, mode: str="console"):
        if mode == "console":
            self.ui = ConsoleUI()
        else:
            self.ui = GraphicUI()
        return self.ui

    def start(self, versus=False):
        """ New game entry point """
        self.__create_ui()
        self.game.prepare_new_game(versus=versus)
        self.game.set_player_name(self.game.player1, self.ui.ask_name())
        if versus is True:
            self.game.set_player_name(self.game.player2, self.ui.ask_name())
        self.main()

    def show_menu(self):
        """ Main menu """
        self.ui.show_menu()
        if self.game.mode == "console":
            self.menu_check(self.ui.menu_check())

    def menu_check(self, option):
        if option == MENU_OPTIONS[0].lower():
            self.game.prepare_new_game()
            self.start()
        elif option == MENU_OPTIONS[1].lower():
            self.game.prepare_new_game(versus=True)
            self.start(versus=True)
        elif option == MENU_OPTIONS[2].lower():
            self.history()
        elif option == MENU_OPTIONS[3].lower():
            self._exit()
        else:
            logging.debug("No match")

    @staticmethod
    def __compare(var, template):
        """ Simple comparing internal shortcut. Returns True if var==template. """
        return var.lower() == template.lower()

    def main(self, versus=False):
        """ Main game loop """
        self.game.current_player = self.game.choose_first_player()
        while not self.grid.check_filled():
            winner = self.game.check_win()
            if winner:
                self.ui.print(f"Победил игрок {winner.name}!")
                self._log_results(winner)
                break
            if isinstance(self.game.current_player, Person):
                self.show_status()
            self._next_move()
            self.__change_player()
        self.ui.print("Игра окончена!")
        if not winner:
            self.ui.print("Ничья!")
        self.ui.print("Реванш? (да/нет)")
        choice = self.__compare(self.ui.choice(), "да")
        if choice:
            self._revenge()
        self.ui.print("Выйти в меню? (да/нет)")
        choice = self.__compare(self.ui.choice(), "да")
        if choice:
            self.show_menu()
        self._exit()

    def _revenge(self):
        self.game.prepare_new_game(self.game.mode)
        self.grid.reset_cells()
        self.game.revenge()
        self.main()

    @staticmethod
    def _log_results(winner):
        """ Creating winner logs to WINNERS_FILE document """
        if isinstance(winner, Person):
            date = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            # logger.debug(f"{date} - победил {winner.name}")
            logger.debug("%s - победил %s", date, winner.name)

    def _next_move(self):
        """ Main game players moves logic """
        if isinstance(self.game.current_player, Person):
            point = self.ui.input(f"Ход игрока {self.game.current_player.name} (номер ячейки):")[0]
            move = int(self.game.current_player.move(point))
        elif isinstance(self.game.current_player, Computer):
            move = self.game.current_player.move()
        if move in self.game.all_points and move not in self.game.marked_cells:
            self.game.current_player.add_marked(move)
            self.grid.fill(move, self.game.current_player.symbol)
            self.game.marked_cells.append(move)
        else:
            if isinstance(self.game.current_player, Person):
                self.ui.print(f"Нельзя походить в ячейку {move}.")
            self._next_move()

    def __change_player(self):
        """ Change player's move turn """
        if self.game.current_player == self.game.player1:
            self.game.current_player = self.game.player2
        else:
            self.game.current_player = self.game.player1

    def _exit(self):
        """ Just user-friendly console exit """
        self.ui.exit()
        sys.exit()

    def history(self):
        """ Showing all players wins history """
        self.ui.print("История побед/поражений:")
        self.ui.show_history()
        if self.game.mode == "console":
            self.show_menu()

    def show_status(self):
        """ Showing current grid state """
        self.grid.show()



