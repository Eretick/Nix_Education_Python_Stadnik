import os
import random
PREVS_TXT_NAME = 'prevs.txt'
WORDS_TXT_NAME = 'words.txt'


def check_prev_words_file():
    files = os.listdir(os.getcwd())
    if PREVS_TXT_NAME not in files:
        with open(PREVS_TXT_NAME, 'w', encoding='utf8') as f:
            f.write('')

class Menu:
    def __init__(self):
        print('Добро пожаловать в Виселицу!')
        print('(c) Stadnik Vladislav. Nix Solutions Python Course')
        print('\n', 'Доступные варианты:', '\n',
              '   --->Начать<---', '\n',
              '--->Прошлые слова<---', '\n',
              '   --->Выход<---')
        self.start()

    def start(self):
        choise = input('Введите свой выбор: ')
        if choise.lower() == "начать":
            Game().start()
        elif choise.lower() == 'прошлые слова':
            self.show_prevs()

    def show_prevs(self):
        try:
            with open(PREVS_TXT_NAME, encoding="utf8") as f:
                words = [i.rstrip('\n') for i in f.readlines()]
                if words != []:
                    print([word for word in words])
                else:
                    print('Слов пока нет. Начните игру =)')
        except FileNotFoundError:
            print("Предыдущие слова не найдены")
        except Exception as e:
            print(e)
        self.start()

class Image:
    current_mode = 0
    image0 = '''
        ____
        |  |
           |
           |
           |
        ___|_
    '''
    image1 = '''
        ____
        |  |
        O  |
           |
           |
        ___|_
    '''
    image2 = '''
        ____
        |  |
        O  |
        |  |
           |
        ___|_
    '''
    image3 = '''
        ____
        |  |
        O/ |
        |  |
           |
        ___|_
    '''
    image4 = '''
        ____
        |  |
       \O/ |
        |  |
           |
        ___|_
    '''
    image5 = '''
        ____
        |  |
       \O/ |
        |  |
       / \ |
        ___|_
    '''

    def __init__(self):
        self.modes = [0, 1, 2, 3, 4, 5]
        self.images = [self.image0, self.image1, self.image2, self.image3, self.image4, self.image5]
        self.current_mode = self.modes[0]
        self.current_image = self.images[0]

    def change_mode(self, mode=None):
        " Change image mode to next if no mode argument"
        if self.current_mode < len(self.modes):
            self.current_mode = self.current_mode + 1 if mode is None else mode
            self.next_image()

    def next_image(self):
        self.current_image = self.images[self.current_mode]

class Game:
    def __init__(self):
        self.image = Image()
        self.choosed_word = ''  # the word from txt file
        self.incorrect_letters = []

    def choose_word(self):
        ''' Reading the words.txt and choose random word'''
        words = []
        with open(WORDS_TXT_NAME, encoding="utf-8") as f:
            words = [i.rstrip('\n') for i in f.readlines()]
        self.choosed_word = random.choice(words).upper()

    def start(self):
        ''' The main game process'''
        self.choose_word()
        self.incorrect_letters.clear()
        self.current_word_status = ['_', '_', '_', '_', '_']
        self.correct_answers = 0
        self.tries_left = len(self.current_word_status)
        self.image.current_mode = self.image.modes[0]
        while self.tries_left > 0 and '_' in self.current_word_status:
            self.print_status()
            self.ask_word()
        else:
            if self.correct_answers != len(self.current_word_status):
                self.game_over()
            else:
                self.win()


    def word_status(self):
        ''' Used for printing unknown word as a string'''
        return ''.join(self.current_word_status)

    def print_status(self):
        ''' Current game status  '''
        print(self.image.current_image)
        print("Осталось попыток:", self.tries_left)
        print("Неугаданные буквы:", self.incorrect_letters)
        print("Слово для отгадывания: ", self.word_status())

    def ask_word(self):
        ''' User guess the letter'''
        letter = input("Открыть букву: ").upper()
        letter_count = 0
        for i in range(len(self.choosed_word)):
            if self.choosed_word[i] == letter:
                self.current_word_status[i] = letter
                letter_count += 1
                self.correct_answers += 1
        if letter_count == 0:
            self.tries_left -= 1
            self.image.change_mode()
            self.incorrect_letters.append(letter)

    def game_over(self):
        self.save_word()
        self.print_status()
        print("Загаданное слово было", self.choosed_word)
        print("Игра окончена. Ты убил его. Серийный игрок >_<")
        print("Попробовать еще раз и убить очередного бедолагу?")
        answer = input("Да/нет: ").lower()
        if answer == "да":
            self.start()
        else:
            Menu().start()

    def win(self):
        self.save_word()
        self.print_status()
        print("Ты победил!")
        print("Загаданное слово было", self.choosed_word)
        print("Попробовать еще раз?")
        answer = input("Да/нет: ").lower()
        if answer == "да":
            self.start()
        else:
            Menu().start()

    def save_word(self):
        ''' Save used word to prevs.txt'''
        check_prev_words_file()
        words = []
        with open(PREVS_TXT_NAME, encoding='utf8') as f:
            words = [i.rstrip('\n').lower() for i in f.readlines()]
            print(words)
        if self.choosed_word.lower() not in words:
            with open(PREVS_TXT_NAME, encoding='utf8', mode='a') as f:
                f.write(self.choosed_word+'\n')

if __name__ == "__main__":
    check_prev_words_file()
    Menu().start()
