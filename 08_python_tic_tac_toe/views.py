""" View module for console version """
import sys

from models import ConsoleGrid, GraphicGrid
from tkinter import Tk, Button, Label, Radiobutton, Frame, messagebox
from settings import WINNERS_FILE

def winners():
    with open(WINNERS_FILE, "r", encoding="utf-8") as file:
        text = file.read()
        if text != "":
            return text
        return "Здесь пока нет истории. Начните новую игру!"

class ConsoleUI:
    """ Main class for interact with console UI """
    def __init__(self):
        self.pack = ConsoleGrid()

    def show_menu(self):
        self.print("---------Начать--------")
        self.print("---Друг против друга---")
        self.print("-----История побед-----")
        self.print("---------Выход---------")
        self.print("Выберите один из вариантов: начать/против/история/выход")

    def choice(self):
        """ Internal shortcart for user self.ui.input """
        choise = self.input("Введите свой выбор:")
        return choise

    def menu_check(self):
        """ Menu choice """
        option = self.choice().lower()
        return option

    def show_history(self):
        self.print(winners())


    @staticmethod
    def print(message):
        print(message)

    @staticmethod
    def input(user_info=""):
        return input(user_info)

    def exit(self):
        self.input("Выход из игры. Нажмите любую клавишу...")


class GraphicUI(Tk):
    """ Main class for interact with console UI """

    def __init__(self):
        super().__init__()
        self.title("Tic-tac-toe")
        self.geometry("+500+200")
        self.grid = GraphicGrid()
        self._setup()

    def _setup(self):
        # Frames
        self.main_frame = Frame(self)
        self.label_frame = Frame(self.main_frame)
        self.rowconfigure(0, weight=1)
        self.menu_frame = Frame(self.main_frame)
        self.game_frame = Frame(self.main_frame)
        self.rowconfigure(1, weight=3)
        self.status_frame = Frame(self.main_frame)
        self.rowconfigure(2, weight=1)

        self.columnconfigure(0, weight=4)

        # Main Label
        self.main_label = Label(self.label_frame, text="Крестики-Нолики", font="Arial 25")
        self.main_label.pack()

        # player modes
        ...

        # Menu
        self.new_game_btn = Button(self.main_frame, text="Новая игра", width=15, command=self.show_game)
        self.versus_btn = Button(self.main_frame, text="Против друга", width=15)
        self.log_btn = Button(self.main_frame, text="История побед", width=15, command=self.show_history)
        self.exit_btn = Button(self.main_frame, text="Выход", width=15, command=self.exit)

        # Frame packing
        self.main_frame.pack()
        self.label_frame.pack()

        self.new_game_btn.pack(pady=10)
        self.versus_btn.pack(pady=10)
        self.log_btn.pack(pady=10)
        self.exit_btn.pack(pady=10)

        # Status
        self.status_label = Label(self.status_frame, text="")
        self.status_label.pack()

        self.show_menu()
        self.show_status()

        self.mainloop()

    def print(self, message):
        pass

    def input(self, warning=""):
        pass

    def show_menu(self):
        #self._clear_window()
        #self.menu_frame.pack()
        self.set_status("Выберите один из вариантов")

    @staticmethod
    def __clear_frame(self, frame):
        frame.pack_remove()

    def _clear_window(self):
        #self.__clear_frame(self.main_frame)
        pass

    def show_game(self):
        #self._clear_window()
        self.game_frame.pack()
        pass

    def set_status(self, status: str):
        self.status_label["text"] = status

    def show_status(self):
        self.status_frame.pack()

    def menu_check(self):
        """ Menu choice """
        print("will be later")

    @staticmethod
    def show_history():
        text = winners()
        messagebox.showinfo("История побед", text)

    def exit(self):
        self.destroy()
        sys.exit()
