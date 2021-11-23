""" This is controller implementations for MVC pattern """
import datetime
import logging
import random
import sys
from models import Person, Computer, Game, Grid
from settings import *
from views import GraphicUI,  ConsoleUI
from math import inf as infinity, ceil

m_c = 0

class TicTacToe:
    """ The game controller class """
    def __init__(self, mode="console") -> None:
        self.__scores = {"user_symbol": -100,
                         "computer_symbol": 100,
                         "draw": 0}
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
            logger.debug("%s - %s has won", date, winner.name)

    def reset_game(self):
        """ Reset game models and view to origin state """
        self.grid.reset_cells()
        self.ui.reset_grid()
        self.game.prepare_new_game()
        self.__sync_grid_gui()

    def __exit(self):
        """ Quit method """
        self.ui.exit()
        sys.exit()

    def __computer_move(self):
        """ Move method for computer player using minimax algorithm """
        points = self.grid.cells.copy()
        depth = len([i for i in points if str(i).isdigit()])
        if depth == 9:
            move = random.randint(0, 10)
        else:
            move = self.call_minimax(points, depth)
            move = abs(3 * move[0] + move[1])
        return move

    def fill(self, move, symbol):
        """ Fill cell in grid model and sync it with view  """
        self.grid.fill(move, symbol)
        self.__sync_grid_gui()

    def show_menu(self):
        """ Method for show menu at start or after end game"""
        self.ui.show_menu()
        if self.game.mode == "console":
            self.ui.menu_check(self.ui.input("Choose 1 of menu options: "))

    def __current_player_move(self, move):
        """ Make player model know about change in  game """
        self.game.marked_cells.append(move)
        self.game.all_points.remove(move)
        self.game.current_player.add_marked(move)
        self.game.current_player.remove_from_all(move)

    def start(self, versus=False):
        """ New game entry point """
        self.reset_game()
        self.game.prepare_new_game(versus=versus)
        names = self.ui.ask_names(versus)
        self.game.set_player_name(self.game.player1, names[0])
        if versus is True:
            self.game.set_player_name(self.game.player2, names[1])
        self.game.current_player = self.game.choose_first_player()
        self.main()

    def main(self):
        """ Main game loop """
        if not self.grid.check_filled():
            self.__show_status()
            # The first move at game beginning, all next moves by self.next_move() called from ui
            if self.game.mode == "console":
                if isinstance(self.game.current_player, Person):
                    self.ui.input_move(f"Now {self.game.current_player.name} turn: ")
                else:
                    self.next_move()
        else:
            self.ui.print("Game over!")

    def check_win(self, tactics: dict = None):
        """ Check win method after every move """
        if tactics is None:
            winner = self.game.check_win()
            if winner:
                self.ui.print("Victory!", f"{winner.name} has won!")
                self.__log_results(winner)
                if self.game.mode == "console":
                    self.ui.print("Back to menu? (yes/no) - 'no' for exit.")
                    choice = self.ui.input()
                    if choice == "yes":
                        self.show_menu()
                        return
                    else:
                        self.__exit()
                self.ui.show_menu()
                self.reset_game()
                return True
            elif self.grid.check_filled():
                self.ui.print(message=f"Draw game!")
                if self.game.mode == "console":
                    self.ui.print("Back to menu? (yes/no) - 'no' for exit.")
                    choice = self.ui.input()
                    if choice == "yes":
                        self.show_menu()
                        return
                    else:
                        self.__exit()
                self.ui.show_menu()
                self.reset_game()
                return True
        else:
            winner = self.game.check_win(tactics)
        return winner

    def next_move(self, move=None):
        """ Main game logic.
        Argument:
            move: an integer (1-9) number what means cell number to fill. Need only for player.
            In case player - come from ui.
            In case AI - calculated by minimax algorithm so no need to pass it.
         """
        if isinstance(self.game.current_player, Computer):
            move = self.__computer_move()
            logging.debug(["comp 1st: ", move])
        # first check is input is correct
        if isinstance(move, int) and move in self.game.all_points:
            if move not in self.game.marked_cells and move not in self.game.current_player.marked_cells:
                self.__current_player_move(move)
                self.fill(move, self.game.current_player.symbol)
                winner = self.check_win()
                if not winner and self.game.mode == "console":
                    self.ui.show()
            else:
                if isinstance(self.game.current_player, Person):
                    if self.game.mode == "console":
                        self.next_move(move)
                else:
                    self.game.current_player.move()
        else:
            #  in case if we wrote wrong number in console
            self.ui.print(f"Wrong input '{move}'!")
            if self.game.mode == "console" and isinstance(self.game.current_player, Person):
                self.next_move(self.ui.input_move(f"Now {self.game.current_player.name} turn: "))
            elif isinstance(self.game.current_player, Computer):
                self.next_move()
            return
        self.__change_player()
        if isinstance(self.game.current_player, Computer):
            self.next_move()

        if self.game.mode == "console":
            self.main()

    def history(self):
        """ Showing all players wins history """
        self.ui.print("Winners history:")
        self.ui.show_history()
        if self.game.mode == "console":
            self.show_menu()

    def call_minimax(self, points, depth):
        """ Setup method for beginning AI move calculating """
        return self.__minimax(points, depth, self.game.current_player)

    def __minimax(self, points, depth, player):
        """ Minimax algorithm for computer """
        global m_c
        m_c += 1
        if isinstance(player, Computer):
            best = [-1, -1, -infinity]
            next_player = self.game.player1
        else:
            best = [-1, -1, +infinity]
            next_player = self.game.player2

        tactic = {"grid": points, "player": player}
        winner = self.check_win(tactics=tactic)
        if depth == 0 or winner is not False:
            if isinstance(winner, Person):
                score = 1
            elif isinstance(winner, Computer):
                score = -1
            else:
                score = 0
            return [-1, -1, score]

        for cell in points:
            if isinstance(cell, int) or cell.isdigit():
                number = points.index(cell)
                points[number] = player.symbol
                score = self.__minimax(points, depth - 1, next_player)
                points[number] = self.grid.cells[number]
                score[0] = ceil(cell//3)-1
                score[1] = cell - 3 * cell // 3
                if isinstance(player, Computer):
                    if score[2] > best[2]:
                        best = score  # max value
                else:
                    if score[2] < best[2]:
                        best = score  # min value
        #print("best:", best )
        return best