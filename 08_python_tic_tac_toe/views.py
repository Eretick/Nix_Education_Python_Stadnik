import sys
from tkinter import Tk, Button, Label, Radiobutton, Frame, messagebox, StringVar, IntVar, Entry
from enum import Enum
import tkinter
from settings import WINNERS_FILE, P1_SYMBOL, P2_SYMBOL
MENU_OPTIONS = ["Начать", "Против", "История", "Выход"]


def winners():
    with open(WINNERS_FILE, "r", encoding="utf-8") as file:
        text = file.read()
        if text != "":
            return text
        return "Здесь пока нет истории. Начните новую игру!"

class ConsoleUI:
    cells = range(1, 10)
    def __init__(self, controller):
        self.controller = controller
        self.versus = False

    @staticmethod
    def print(message="", title=""):
        if title != "":
            print(title)
        print(message)
    
    @staticmethod
    def input(message=""):
        return input(message).lower()
    
    def input_move(self, user_info=""):
        """ Only for set a move text to GUI label. 
        The name is equal to input func in Console UI """
        self.controller.next_move(int(input(user_info)[0]))

    def show_menu(self):
        self.print("---------Начать--------")
        self.print("---Друг против друга---")
        self.print("-----История побед-----")
        self.print("---------Выход---------")
        self.print("Выберите один из вариантов: начать/против/история/выход")

    def menu_check(self, option):
        if option == MENU_OPTIONS[0].lower():
            self.versus = False
            self.controller.game.prepare_new_game(self.versus)
            self.controller.start(self.versus)
        elif option == MENU_OPTIONS[1].lower():
            self.versus = True
            self.controller.game.prepare_new_game(versus=self.versus)
            self.controller.start(self.versus)
        elif option == MENU_OPTIONS[2].lower():
            self.controller.history()
        elif option == MENU_OPTIONS[3].lower():
            self.controller.__exit()
        else:
            print("Неверный ввод!")

    def show_history(self):
        self.print(winners())

    @staticmethod
    def ask_names(versus):
        name1 = input("Игрок 1, введите имя: ")
        name2 = "Computer"
        if versus is True:
            name2 = input("Игрок 2, введите имя: ")
        return name1, name2

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
    
    def sync_grid(self, cells: list):
        self.cells = cells

    def show(self):
        print(self.image)
    
    def exit(self):
        self.input("Выход из игры. Нажмите любую клавишу...")

    def reset_grid(self):
        self.cells = range(1, 10)
    
    
class GraphicUI(Tk):
    """ Main class for interact with console UI """

    def __init__(self, controller):
        super().__init__()
        self.title("Tic-tac-toe")
        self.controller = controller
        self.background = "white"
        self["bg"] = self.background
        self._setup()

    def _setup(self):
        # ---------------------------------------Frames------------------------------------------------------------
        # Main menu screen
        self.main_frame = Frame(self, bg=self.background)
        self.label_frame = Frame(self.main_frame, bg=self.background)
        self.menu_frame = Frame(self.main_frame, bg=self.background)
        self.status_frame = Frame(self.main_frame, bg=self.background)
        # Players settings screen
        self.players_frame = Frame(self.main_frame, bg=self.background)
        # Game screen
        self.game_frame = Frame(self.main_frame, bg=self.background)

        # ---------------------------------------Widgets------------------------------------------------------------
        # Main Label
        self.main_label = Label(self.label_frame, text="Крестики-Нолики", font="Arial 25", bg=self.background)
        self.main_label.pack()

        # Menu
        self.setup_btn = Button(self.menu_frame, text="Новая игра", width=15, command=self.__show_versus_choice, bg=self.background)
        self.log_btn = Button(self.menu_frame, text="История побед", width=15, command=self.show_history, bg=self.background)
        self.exit_btn = Button(self.menu_frame, text="Выход", width=15, command=self.exit, bg=self.background)

        # Players
        self.__versus = IntVar()
        self.player_radio = Radiobutton(self.players_frame, text="Против игрока",
                                        variable=self.__versus, value=1, command=self.__lock_p2_settings, bg=self.background)
        self.cpu_radio = Radiobutton(self.players_frame, text="Против компьютера",
                                     variable=self.__versus, value=0, command=self.__lock_p2_settings, bg=self.background)
        self.player_radio.select()
        self.p1_lab = Label(self.players_frame, text="Имя игрока 1", bg=self.background)
        self.p2_lab = Label(self.players_frame, text="Имя игрока 2", bg=self.background)
        self.p1_entry = Entry(self.players_frame, width=17)
        self.p2_entry = Entry(self.players_frame, width=17)
        self.new_game_btn = Button(self.players_frame, text="Начать игру", command=self.show_game, bg=self.background)
        self.back_btn = Button(self.players_frame, text="Назад", command=self.show_menu, bg=self.background)

        # Game
        self._grid = GraphicGrid(self.controller.next_move, self.game_frame, bg=self.background)
        self._grid.grid(row=1, column=0)
        self.menu_btn = Button(self.game_frame, text="В меню", command=self.show_menu, bg=self.background)
        self.menu_btn.grid(row=2, column=0)

        # Frame packing
        self.main_frame.grid(padx=10, pady=10)
        self.label_frame.grid(row=0, column=0)
        self.status_frame.grid(row=1, column=0)
        self.menu_frame.grid(row=2, column=0)

        # Widgets packing
        self.setup_btn.pack(pady=10)
        self.log_btn.pack(pady=10)
        self.exit_btn.pack(pady=10)

        self.player_radio.grid(row=0, column=0)
        self.cpu_radio.grid(row=0, column=1)
        self.p1_lab.grid(row=1, column=0)
        self.p2_lab.grid(row=1, column=1)
        self.p1_entry.grid(row=2, column=0)
        self.p2_entry.grid(row=2, column=1)
        self.new_game_btn.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        self.back_btn.grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=5)


        # Status
        self.status_label = Label(self.status_frame, text="", bg=self.background)
        self.status_label.pack()

        self.__lock_start_button()
        self.show_menu()
        self.show_status()

    def __lock_p2_settings(self):
        if self.versus is False:
            self.p2_entry["state"] = "disabled"
        else:
            self.p2_entry["state"] = "normal"

    def __lock_start_button(self, *args):
        print(self.versus)
        if self.versus == True and (self.p1_entry.get() == "" or self.p2_entry.get() == ""):
            self.new_game_btn["state"] = "disabled"
        elif self.versus == False and self.p1_entry.get() == "":
            self.new_game_btn["state"] = "disabled"
        else:
            self.new_game_btn["state"] = "normal"

    def sync_grid(self, cells: list):
        self._grid.cells = cells
        self._grid.update_grid()

    def reset_grid(self):
        for cell in self._grid.buttons:
            cell.reset_state()
        self._grid.update_grid()

    def print(self, title="",  message=""):
        messagebox.showinfo(title, message)

    def ask_names(self, versus=None):
        name1 = self.p1_entry.get()
        name2 = "Computer"
        if self.versus is True:
            name2 = self.p2_entry.get()
        return name1, name2, self.versus

    def show_menu(self):
        self.__clear_frame(self.game_frame)
        self.__clear_frame(self.players_frame)
        self.menu_frame.grid()
        self.input("Выберите один из вариантов")

    @property
    def versus(self):
        return bool(self.__versus.get())

    @staticmethod
    def __clear_frame(frame):
        frame.grid_remove()

    def __show_versus_choice(self):
        self.__clear_frame(self.menu_frame)
        self.players_frame.grid()
        self.p1_entry.bind("<Key>", self.__lock_start_button)
        self.p2_entry.bind("<Key>", self.__lock_start_button)

    def show_game(self):
        self.controller.start(self.versus)
        self.__clear_frame(self.menu_frame)
        self.__clear_frame(self.players_frame)
        self.game_frame.grid()

    def input(self, status: str):
        self.status_label["text"] = status
    
    def input_move(self, status: str):
        self.status_label["text"] = status

    def show_status(self):
        self.status_frame.grid()

    @staticmethod
    def show_history():
        text = winners()
        messagebox.showinfo("История побед", text)

    def exit(self):
        self.destroy()
        sys.exit()


class Cell(Button):
    def __init__(self, callback, *args, **kwargs):
        super().__init__(*args, **kwargs, disabledforeground="white")
        self["width"] = 7
        self["height"] = 5
        self["relief"] = "solid"
        self.__state = "normal"
        self.config(command=lambda: callback(int(self["text"])))

    def set_text(self, value):
        self["text"] = value

    @property
    def text(self):
        return self["text"]

    @property
    def state(self):
        return self.__state

    def set_active(self, bool):
        if bool == False:
            self["bg"] = "gray"
            self.__state = tkinter.DISABLED
            
        else:
            self.__state = tkinter.NORMAL
            self["bg"] = "white"
        self["state"] = self.__state

    def reset_state(self):
        self.__state = tkinter.NORMAL
        self.set_active(self.__state)
        print("activated")


class GraphicGrid(Frame):
    cells = range(1,10)
    def __init__(self, callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buttons = []
        self.callback = callback
        self._create()

    def _create(self):
        number = 1
        for i in range(1, 4):
            for j in range(1, 4):
                cell = Cell(self.callback, self, text=number, bg=self["bg"])
                self.buttons.append(cell)
                cell.grid(row=i, column=j)
                number += 1

    def fill(self, cell, text):
        cell.set_text(text)

    def update_grid(self):
        for index in range(9):
            cell_sign = self.cells[index]
            cell_btn = self.buttons[index]
            self.fill(cell_btn, cell_sign)
            if cell_btn.text == P1_SYMBOL or cell_btn.text == P2_SYMBOL:
                cell_btn.set_active(False)