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
        self._words_count = 0

    def __repr__(self):
        return f'<Sentence(words={len(self.words)}, other_chars={self.other_chars})>'

    def __check_full_sentence(self):
        """ Internal method for check if sentence is complete.
         Raise ValueError if not."""
        if not self.string.endswith(SPLITTERS):
            raise ValueError("The sentence must be finished!")

    def __get_sentence(self):
        """ Method checks if the sentence is full and it's only one. """
        self.__check_full_sentence()
        # deleting empty strings after multiple splits
        sentence_list = [i.strip() for i in re.split(self.__re_splitters, self.string) if i != '']
        if len(sentence_list) > 1:
            raise MultipleSentencesError("Must be only one sentence")
        first_sentence = sentence_list[0]
        # Adding to first sentence clipped ending symbol
        return first_sentence + self.string[len(first_sentence)]

    def _words(self):
        """ Internal method for words property """
        return SentenceIterator(self.__get_sentence())

    @property
    def words(self):
        """ Getting words from iterator """
        iterator = iter(self._words())
        words_list = []
        for i in iterator:
            words_list.append(i)
        return words_list

    @property
    def other_chars(self):
        """ Property function which returns non-letters chars in sentence. """
        # return list(set(self.__other_chars))
        return self._words().get_symbols()

    def __getitem__(self, item):
        """ Support indexes """
        return self.words[item]


class SentenceIterator:
    """ Iterator for Sentence class"""

    def __init__(self, sentence: str):
        self.sentence = sentence  # original sentence
        self.__word_symbol = "w"
        self.__sign_symbol = "s"
        self.__scheme = ""
        self.__create_scheme()  # schematic view of sentence
        self.__words_indexes = []  # list of indexes of every word
        self.__chars_indexes = []  # list of indexes of not-word chars
        self.other_chars = []  # list of non-text-symbol chars
        self._min = 0
        self.__words_count = self.__count_words()
        self._remains = self.__words_count

    def __count_words(self):
        """ Internal method, uses created schema to find and save to all words indexes.
        Return words count """
        self.__get_indexes()
        return len(self.__words_indexes)

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
        for index, _ in enumerate(self.__scheme):
            # filling symbols index list
            if self.__scheme[index] == self.__sign_symbol:
                self.__chars_indexes.append(self.__scheme[index])
            # filling words index list
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
                    if self.__scheme[index] == self.__word_symbol and index == len(self.__scheme):
                        word_end = index
                        indexes.append([word_start, word_end])
        self.__words_indexes = indexes

    def __get_word(self, index_start, index_end):
        """ Getting a word from prepared scheme by indexes """
        if len(self.__words_indexes) == 0:
            self.__get_indexes()
        return self.sentence[index_start:index_end+1]

    @property
    def words_count(self):
        """ Read-only property, returns words count in sentence. """
        return self.__count_words()

    def get_symbols(self):
        """ Func returns all used symbols in sentence """
        symbols = [self.sentence[i] for i in range(len(self.__scheme)) if self.__scheme[i] == self.__sign_symbol]
        return list(set(symbols))



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
