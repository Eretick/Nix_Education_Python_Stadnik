""" This is a main entry point """
import sys
from controllers import TicTacToe

def choice():
    print("""Какую версию игры запустить?
    1 - Консольная игра
    2 - С графическим интерфейсом""")
    return input("Ваш выбор: ")


if __name__ == "__main__":
    option = choice()
    if option == "1":
        game = TicTacToe(mode="console")
        game.show_menu()
    elif option == "2":
        game = TicTacToe(mode="graphic")
        game.show_menu()
        game.ui.mainloop()
    else:
        input("Неверный ввод!")
        sys.exit()

