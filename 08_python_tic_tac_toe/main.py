""" This is a main entry point """
import sys
from controllers import TicTacToe

def choice():
    print("""Which variant of game you want to play?
    1 - Console game.
    2 - Graphic game.""")
    return input("Your choice (number only): ")


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
        input("Wrong input!")
        sys.exit()

