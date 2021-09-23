# Transport tasks

class Transport:
    is_moving = False
    """ Base class for all transprots """
    def __init__(self, manufacturer, model, number=None, owner=None):
        self.manufacturer = manufacturer
        self.model = model
        self.number = number
        self.owner = owner

    def move(self):
        self.is_moving = True
        print("Moving")


if __name__ == "__main__":
    print(1)