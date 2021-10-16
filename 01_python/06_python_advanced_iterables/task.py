""" Python iterator task """
import re

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
        self.splitters = (".", "!", "?", "...")
        self.__re_splitters = f'[{"".join(self.splitters)}]'
        if not isinstance(self.string, str):
            raise TypeError('The Sentence class can work only with string!')
        self.words_splitters = [',', '\'', '\"', ";", ":", "-", " "]
        self.__other_chars = []
        self._words_count = 0
        self.__sentence = ""

    def __repr__(self):
        return f'<Sentence(words={len(self.words)}, other_chars={self.__get_symbols()})>'

    def __check_full_sentence(self):
        if not self.string.endswith(self.splitters):
            raise ValueError("The sentence must be finished!")

    def __get_sentence(self):
        self.__check_full_sentence()
        # deleting empty strings after multiple splits
        sentence = [i.strip() for i in re.split(self.__re_splitters, self.string) if i != '']
        if len(sentence) > 1:
            raise MultipleSentencesError("Must be only one sentence")
        return sentence[0]

    def __sentence_to_list(self):
        self.__get_symbols(replace=True)
        return self.__sentence.split()

    def _words(self):
        return SentenceIterator(self.__sentence_to_list())

    @property
    def words(self):
        """ Getting words from iterator """
        words_list = list(iter(self._words()))
        self._words_count = len(words_list)
        return words_list

    @property
    def other_chars(self):
        """ Property function which returns non-letters chars in sentence. """
        return list(set(self.__other_chars))

    def __get_symbols(self, replace=False):
        """ Internal method for finding all non-letters chars in sentence.
        If replace=True, removes all chars from sentence for correct words splitting.
        No need to use from outside.
        """
        counter = 0
        self.__sentence = self.__get_sentence()
        self.__other_chars.clear()
        for symbol in self.__sentence:
            if symbol in self.words_splitters:
                counter += 1
                self.__other_chars.append(symbol)
                if replace:
                    self.__sentence = self.__sentence.replace(symbol, " ")
        return counter

    def __getitem__(self, item):
        """ Support indexes """
        return self.words[item]


class SentenceIterator:
    """ Iterator for Sentence class"""
    def __init__(self, sentence:list, lenght=None):
        self.sentence = sentence
        self._min = 0
        self._max = len(sentence)
        self._remains = lenght if lenght is not None else self._max

    def __next__(self):
        """ The main iterator logic """
        if self._remains > 0:
            self._remains -= 1
            return self.sentence[self._max - self._remains - 1]
        raise StopIteration

    def __iter__(self):
        return self


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
