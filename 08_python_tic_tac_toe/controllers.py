""" Console Tic-tac-toe """
import datetime
import logging
import random
import sys
from models import Person, Computer, Game, Grid, Player
from settings import *
from views import GraphicUI,  ConsoleUI,MENU_OPTIONS

class TicTacToe:
    def __init__(self, mode="console") -> None:
        self.mode = mode
        self.grid = Grid()
        self.ui = self.__create_ui(self.mode)
        self.game = Game(mode=mode)

    def __create_ui(self, mode: str = "console"):
        if mode == "console":
            return ConsoleUI(self)
        return GraphicUI(self)

    def __show_status(self):
        """ Showing current grid state """
        if self.game.mode == "console":
            self.ui.show()

    def __sync_grid_gui(self):
        cells = self.grid.cells
        self.ui.sync_grid(cells)

    def __change_player(self):
        """ Change player's move turn """
        if self.game.current_player == self.game.player1:
            self.game.current_player = self.game.player2
        else:
            self.game.current_player = self.game.player1

    @staticmethod
    def __log_results(winner):
        """ Creating winner logs to WINNERS_FILE document """
        if isinstance(winner, Person):
            date = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            logger.debug("%s - победил %s", date, winner.name)

    def reset_game(self):
        self.grid.reset_cells()
        self.ui.reset_grid()
        self.game.prepare_new_game()
        self.__sync_grid_gui()

    def __exit(self):
        """ Just user-friendly console exit """
        self.ui.exit()
        sys.exit()

    def fill(self, move, symbol):
        self.grid.fill(move, symbol)
        self.__sync_grid_gui()

    def show_menu(self):
        self.ui.show_menu()
        if self.game.mode == "console":
            self.ui.menu_check(self.ui.input("Выберите один из вариантов меню: "))

    def start(self, versus=False):
        """ New game entry point """
        self.reset_game()
        self.game.prepare_new_game(versus=versus)
        names = self.ui.ask_names(versus)
        self.game.set_player_name(self.game.player1, names[0])
        if versus is True:
            self.game.set_player_name(self.game.player2, names[1])
        self.game.current_player = self.game.choose_first_player()
        print(self.game.current_player.name)
        self.main()

    def main(self):
        """ Main game loop """
        if not self.grid.check_filled():
            self.__show_status()
            self.ui.input_move(f"Ход игрока {self.game.current_player.name}")
            if isinstance(self.game.current_player, Person):
                pass
        else:
            self.ui.print("Игра окончена!")

    def check_win(self):
        winner = self.game.check_win()
        if winner:
            self.ui.print("Победа",f"Победил игрок {winner.name}!")
            self.__log_results(winner)
            if self.game.mode == "console":
                self.ui.print("Выйти в меню? (да/нет)")
                choice = self.ui.input()
                if choice == "да":
                    self.show_menu()
                    return
                else:
                    self.__exit()
            self.ui.show_menu()
            self.reset_game()
            return True
        elif self.grid.check_filled():
            self.ui.print(message=f"Ничья")
            self.ui.show_menu()
            self.reset_game()
            return True
        return False

    def next_move(self, move):
        print("p1:", self.game.player1.marked_cells)
        print("p2:", self.game.player2.marked_cells)
        print(self.game.marked_cells)

        if move in self.game.all_points and move not in self.game.marked_cells:
            self.game.marked_cells.append(move)
            self.game.current_player.add_marked(move)
            self.fill(move, self.game.current_player.symbol)

            winner = self.check_win()

            if not winner and self.game.mode == "console":
                self.ui.show()
        else:
            if isinstance(self.game.current_player, Person):
                if self.game.mode == "console":
                    self.next_move(move)

        self.__change_player()
        self.ui.input_move(f"Ход игрока {self.game.current_player.name}")
        if isinstance(self.game.current_player, Computer):
            comp_move = self.game.current_player.move()
            print(comp_move)
            self.next_move(comp_move)

        if self.game.mode == "console":
            self.main()

    def history(self):
        """ Showing all players wins history """
        self.ui.print("История побед/поражений:")
        self.ui.show_history()
        if self.game.mode == "console":
            self.show_menu()

