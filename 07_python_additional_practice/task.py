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

@work_logger
def test_func_1():
    print("Test functions working...")

if __name__ == "__main__":
    print("Check1: decorator.")
    test_func_1()
    print("Check2: generator in for loop.")
    for i in gen(['word1', 'word2']):
        print(i)
