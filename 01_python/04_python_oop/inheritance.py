# simple class inheritance example

class Mammal:
    """ The main class for inherit to all mammal animals """
    max_age = 268  # самый долгоживущий, гренладский кит прожил 268 лет
    is_alive = True
    _age = 0
    speed = 100  # km/h. Just some default value

    @property
    def age(self):
        return self._age

    def grow(self, age=1):
        """" Increasing instance.age by age param. Default is 1. """
        if self.is_alive:
            self._age += age
        else:
            print("Sorry. Already dead.")

    def live(self, age=1):
        """ Simple life simulation. 1 call = 1 year. """
        if self.age <= self.max_age and self.age + age <= self.max_age:
            self.grow(age)
        else:
            self._age = self.max_age
            self.die()

    def die(self):
        """ The end of life. Used in live(). Can be called outside. """
        self.is_alive = False
        print(f"RIP {self.age} years old")


class Felidae(Mammal):
    """ Basic class for or cat-famaly animals """
    max_age = 38  # Кошка-рекордсмен Гиннеса

    def __init__(self, name=None, age=0, owner=None):
        self.name = name
        self._age = age
        self.owner = owner

class Cat(Felidae):
    """ What should I write here? Its a cat. My congratulations. """
    speed = 48

    @staticmethod
    def meow():
        print("MEEEAAAAAAAAAAAAAAAOOOOOOOW")

class Cheetah(Felidae):
    """ The same here. It's cheetah. Your Captain Obvious"""
    speed = 130


if __name__ == "__main__":
    cat = Cat()
    print("Name:", cat.name)
    print("Owner:", cat.owner)
    print("ALive:", cat.is_alive)
    print("Age:", cat.age)
    print("Maximum ages:", cat.max_age)
    cat.live()  # lived 1 year
    print("Age after 1 year:", cat.age)
    cat.live(5)  # lived 5 more years
    print("Age after 5 more years:", cat.age)
    print("Age after 50 years:")
    cat.live(50)
    print("Alive:", cat.is_alive)
    print("The cat says:")
    cat.meow()

    # Speed differences
    cheetah = Cheetah()
    print("Cat's speed:", cat.speed)
    print("Cheetah's speed:", cheetah.speed)






