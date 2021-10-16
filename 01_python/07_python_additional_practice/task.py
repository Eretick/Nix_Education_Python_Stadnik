""" *ators practive """

def work_logger(func):
    """ simple func's state decorator """
    print(f"{func} is started...")
    def wrap(*args, **kwargs):
        func(*args, **kwargs)
        print(f"{func} is ended...")
    return wrap

def gen(words):
    """ Simple generator """
    for word in words:
        yield word


class Container:
    def __init__(self, data):
        self.data = data

    def __iter__(self):
        return MyIterator(self.data)


class MyIterator:
    """ Custom iterator class """
    def __init__(self, data):
        self.data = data
        self.len = len(data)
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < self.len:
            text = self.data[self.index]
            self.index = self.index + 1
            return text

        raise StopIteration


@work_logger
def test_func_1():
    """ Example for demonstrate decorator's work """
    print("Test functions working...")


class TempList(list):
    """ Custom context list-manager """
    def __init__(self, data: list):
        self.data = data
        super().__init__()

    def __enter__(self):
        return self.data

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.data.clear()


if __name__ == "__main__":
    print("Check1: decorator.")
    test_func_1()

    generator = gen(['word1', 'word2'])
    print("Generator", generator)
    print("Check2: generator in for loop.")
    for i in generator:
        print(i)

    print("Check3: generator with 2 next():")
    generator = gen(['word1', 'word2'])
    print(next(generator))
    print(next(generator))

    iterator = MyIterator(["word3", "word4"])
    print("Iterator", iterator)
    print("Check4: iterator in for loop.")
    for i in iterator:
        print(i)

    print("Check5: iterator with 2 next():")
    iterator = MyIterator(['word5', 'word6'])
    print(next(iterator))
    print(next(iterator))

    print("Check7: the same but with container.")
    c = Container(['word7', 'word8'])
    i = iter(c)
    print("Using next():", next(i), next(i))
    print("Using for:")
    i = iter(c)
    for word in i:
        print(word)

    print("Check6: Custom context manager.")
    temp_list = TempList(["word7", "word8", "word9"])
    print("Custom self-clear list:", type(temp_list))
    with temp_list as t:
        print("Looking on data while opened:")
        print(t)
    print("Looking on data after closing:", t)
