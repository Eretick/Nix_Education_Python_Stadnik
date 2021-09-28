import random
import re

class MultipleSentencesError(UserWarning):
    pass


class Sentence:
    def __init__(self, string):
        self.string = string
        self.splitters = (".", "!", "?", "...")
        self.re_splitters = f'[{",".join(self.splitters)}]'
        if not isinstance(self.string, str):
            raise TypeError('The Sentence class can work only with string!')
        self._chars = 0
        self.sentence = self.get_sentence()

    def __repr__(self):
        return f'<Sentence(words={self.words}, other_chars=self.chars)>'

    def __check_full_sentence(self):
        if not self.string.endswith(self.splitters):
            raise ValueError("The sentence must be finished!")

    def get_sentence(self):
        self.__check_full_sentence()
        # deleting empty strings after multiple splits
        sentence = [i for i in re.split(self.re_splitters, self.string) if i != '']
        if len(sentence) > 1:
            raise MultipleSentencesError("Must be only one sentence")
        return sentence[0].split()

    def _words(self):
        lenght = len(self.sentence)
        return SentenceIterator(self.sentence)

    @property
    def words(self):
        words_list = [i for i in iter(self._words())]
        return words_list


class SentenceIterator:
    def __init__(self, sentence:list, lenght=None):
        self.sentence = sentence
        self._min = 0
        self._max = len(sentence)
        self._remains = lenght if lenght != None else self._max

    def __next__(self):
        return self.gen_item()

    def __iter__(self):
        return self

    def gen_item(self):
        if self._remains > 0:
            self._remains -= 1
            return self.sentence[self._max-self._remains-1]
        raise StopIteration



if __name__ == "__main__":
    # unfinished sentence
    #s = Sentence("Первое предложение")
    # user exception
    #s = Sentence("Первое предложение. Второе предложение. Третье! Четвертое!")
    # normal sentence
    s = Sentence("Первое предложение.")
    print("Check1:")
    for i in iter(s._words()):
        print(i)
    print("Check2 (first word):")
    print(next(s._words()))

    print("Words property check:", s.words)


