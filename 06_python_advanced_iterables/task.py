""" Python iterator task """
import re

WORDS_SPLITTERS = [',', '\'', '\"', ";", ":", "-", " "]
SPLITTERS = (".", "!", "?", "...")

class MultipleSentencesError(UserWarning):
    """ Custom warning for Sentence class """


class Sentence:
    """ The main class for working with sentences
     Arguments:
     string - string to work with. Must be finished sentence (ends with ./?/!/... )

Errors:
     Raising a TypeError if string parametr is not str
     Raising a ValueError if sentence isn't finished
     Raising a MultipleSentencesError if string contains multiple sentences
     """
    def __init__(self, string):
        self.string = string
        self.__re_splitters = f'[{"".join(SPLITTERS)}]'
        if not isinstance(self.string, str):
            raise TypeError('The Sentence class can work only with string!')
        self.__other_chars = []
        self._words_count = 0

    def __repr__(self):
        return f'<Sentence(words={len(self.words)}, other_chars={self.__other_chars})>'

    def __check_full_sentence(self):
        """ Internal method for check if sentence is complete.
         Raise ValueError if not."""
        if not self.string.endswith(SPLITTERS):
            raise ValueError("The sentence must be finished!")

    def __get_sentence(self):
        """ Method checks if the sentence is full and it's only one. """
        self.__check_full_sentence()
        # deleting empty strings after multiple splits
        sentence = [i.strip() for i in re.split(self.__re_splitters, self.string) if i != '']
        if len(sentence) > 1:
            raise MultipleSentencesError("Must be only one sentence")
        return sentence[0]



    def _words(self):
        return SentenceIterator(self.__get_sentence())

    @property
    def words(self):
        """ Getting words from iterator """
        iterator = self._words()
        words_list = list(iter(iterator))
        return words_list

    @property
    def other_chars(self):
        """ Property function which returns non-letters chars in sentence. """
        # return list(set(self.__other_chars))
        return

    def __getitem__(self, item):
        """ Support indexes """
        return self.words[item]


class SentenceIterator:

    """ Iterator for Sentence class"""
    def __init__(self, sentence: str, lenght=None):
        self.sentence = sentence  # original sentence
        self.__sentence = ""  # internal variable to work with
        self.__word_symbol = "w"
        self.__sign_symbol = "s"
        self.__scheme = ""
        self.__create_scheme()  #  schematic view of sentence
        self.__words_indexes = []  # list of indexes of every word
        self.__chars_indexes = []  # list of indexes of not-word chars
        self.other_chars = []  # list of non-text-symbol chars
        self._min = 0
        self.__words_count = self.__count_words()
        self._sen_max = len(self.__sentence)
        self._remains = lenght if lenght is not None else self.__words_count

    def __count_words(self):
        """ Internal method, uses created schema to find and save to self.__indexes all words indexes.
        Return words count """
        self.__get_indexes()
        return len(self.__words_indexes)

    @property
    def words_count(self):
        return self.__count_words()

    def __next__(self):
        """ The main iterator logic """
        if self._remains > 0:
            index = self.words_count - self._remains
            self._remains -= 1
            return self.__get_word(*self.__words_indexes[index])
        raise StopIteration

    def __iter__(self):
        return self

    def __create_scheme(self):
        """ Create sign-scheme of sentence  """
        for symbol in self.sentence:
            if symbol not in SPLITTERS and symbol not in WORDS_SPLITTERS:
                self.__scheme += self.__word_symbol
            else:
                self.__scheme += self.__sign_symbol

    def __get_indexes(self):
        """ Algorithm for creating list of words limits indexes """

        indexes = []
        word_start = 0
        word_end = 0
        for index in range(len(self.__scheme)):
            # beginning of sentence scheme
            if index == 0:
                word_start = index
            # rest part
            elif index != 0 and index <= len(self.__scheme):
                # if new word begun
                if self.__scheme[index-1] == self.__sign_symbol and self.__scheme[index] == self.__word_symbol:
                    word_start = index
                # if word ends
                if self.__scheme[index - 1] == self.__word_symbol:
                    if self.__scheme[index] == self.__sign_symbol:
                        word_end = index-1
                        indexes.append([word_start, word_end])

        self.__words_indexes = indexes

    def __get_word(self, index_start, index_end):
        """ Getting a word from prepared scheme by indexes """
        if len(self.__words_indexes) == 0:
            self.__get_indexes()
        return self.sentence[index_start:index_end+1]





if __name__ == "__main__":
    # unfinished sentence
    #s = Sentence("Первое предложение")
    # user exception
    #s = Sentence("Первое предложение. Второе предложение. Третье! Четвертое!")
    # normal sentence
    s = Sentence("Девочка-припевочка, выходи гулять; Я иду на улицу - я иду искать!")
    help(s)
    print("Statistics:", repr(s))
    print("Check1: For loop:")
    for i in s:
        print(i)
    # Just hiding from pylint
    iterator = s._words()
    print("Check 1.2. _words method:", iterator)
    print("Check2: s._words() directly. First word:")
    print(next(iterator))
    print("Check3: Next word:")
    print(next(iterator))
    print(next(iterator))
    print("Check 4: Words property check:", s.words)
    print("Check 5: Non-words symbols:", s.other_chars)
    print("Check 6: Indexes. Third item:", s[2])
    print("Check 7: Range:", s[0:3])
    print("Check 8: Iter method:", iter(s))
