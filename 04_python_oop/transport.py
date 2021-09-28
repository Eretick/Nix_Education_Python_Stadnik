# Transport tasks
import time
from abc import ABC, abstractmethod

class Transport(ABC):
    is_moving = False
    color = 'black'
    """
    Attributes:
        Base class for all transprots.\n
        :manufacturer=str - current product's creator (company name)
        :model=str - current product's model
        :number=int - serial number (if exists). Additional argument
        :owner=str - current product's owner (if exists)
        :color=str - current product's color
    """
    def __init__(self, manufacturer=None, model=None, number=None, owner=None, color=None):
        self.manufacturer = manufacturer
        self.model = model
        self.number = number
        self.owner = owner

    @property
    def full_name(self):
        return f"{self.manufacturer} {self.model}"

    @abstractmethod
    def move(self, distance):
        self.is_moving = True
        print(f"Moving {distance} meters")

    @abstractmethod
    def stop(self):
        self.is_moving = False

    def __str__(self):
        mess = f'''This is a {self.__class__} made by {self.manufacturer} with {self.color} color.
Model: {self.model}.
The owner is: {self.owner}.'''
        return  mess


class Engine:
    """ Engine class for Car-like transports """
    _fuel_level = 100

    @property
    def fuel(self):
        return self._fuel_level

    def spend_fuel(self, km):
        if self.fuel > 0:
            self._fuel_level -= km

    def charge(self):
        if self.fuel < 100:
            self._fuel_level += 1

    def __round__(self, n=2):
        return round(self._fuel_level, n)

    def __int__(self):
        return int(self._fuel_level)

class Car(Transport, Engine):
    """ Basic class for all cars"""
    def __init__(self, manufacturer, model, number=None, owner=None, color=None):
        super().__init__(manufacturer, model, number=number, owner=owner, color=color)

    def __eq__(self, other):
        if type(other) == self.__class__:
            if self.fuel == other.fuel:
                return True
        return False

    def __gt__(self, other):
        if type(other) == self.__class__:
            if self.fuel > other.fuel:
                return True
        return False

    def __lt__(self, other):
        if type(other) == self.__class__:
            if self.fuel < other.fuel:
                return True
        return False

    def __ge__(self, other):
        if type(other) == self.__class__:
            if self.fuel >= other.fuel:
                return True
        return False

    def __le__(self, other):
        if type(other) == self.__class__:
            if self.fuel <= other.fuel:
                return True
        return False

    def move(self, km=1):
        """ Moving considering engine fuel level"""
        if km >= 0:
            self.is_moving = self.check_fuel(km)
            if self.is_moving:
                self.spend_fuel(km)
                print(f"Left {self.fuel} after driving {km} km.")
            else:
                print("Can't move.")
        else:
            print("You can't move in past, LOL. Move distance must be a positive.")

    def stop(self):
        self.is_moving = False

    def check_fuel(self, km=1):
        if self.fuel - km >= 0:
            return True
        return False


class Skate(Transport):
    """ Typical teenage skate implementation """
    types = ["shortboard", "longboard", "pennieboard"]

    def __init__(self, manufacturer=None, model=None, number=None, owner=None, color=None, type=types[0]):
        super().__init__(manufacturer, model, number=number, owner=owner, color=color)
        self.type = type

    def move(self, distance=1):
        print("The skate is moving...")
        time.sleep(distance)
        self.stop()

    def stop(self):
        print("The skate is stopped")


class Train(Transport, Engine):
    places = 100
    _passengers = 0
    _free_places = 100

    def __init__(self, free_places=_free_places, *args, **kwargs):
        super().__init__()
        self._free_places = free_places

    @property
    def passengers(self):
        self._passengers = self.places - self.free_places
        return self._passengers

    @property
    def free_places(self):
        return self._free_places

    def add_passenger(self, passangers=1):
        if self.free_places > 0:
            if self._free_places - passangers > 0:
                self._free_places -= passangers
            else:
                self._free_places = 0
        else:
            print("No more free places!")

    def delete_passenger(self, passangers=1):
        if self.passengers > 0:
            if self._free_places + passangers < self.places:
                self._free_places += passangers
            else:
                self._free_places = self.places
        else:
            print("No more passengers for removing!")

    def move(self):
        print("The train is moving.")
        print("Chuh-chuh, chuh-chuh")

    def stop(self):
        print("The train is stopped.")


class Escalator(Transport, Engine):
    move_modes = ['up', 'down']
    mode = move_modes[0]

    def __str__(self):
        return f"""Escalator {'' if self.owner is None else "in "+ self.owner} is moving {self.mode}."""

    def switch_mode(self, mode=None):
        if mode is None:
            if self.mode == self.move_modes[0]:
                self.mode = self.move_modes[1]
            else:
                self.mode = self.move_modes[0]

    def move(self):
        self.is_moving = True

    def stop(self):
        self.is_moving = False


if __name__ == "__main__":
    car1 = Car("Audi", "A4", color="red")
    car2 = Car("Nissan", "Altima", color="red")
    print("Info about car:")
    print(car1)
    print("Cars with the same fuel level:", car1 == car2)
    print("Car-2:")
    car1.move(1.5)
    print("Cars with the same fuel level:", car1 == car2)
    print("Car1 has less fuel then Car2:", car1 < car2)

    print("Info about skate:")
    skate = Skate("Profi", "MS 0354-2", color='space')
    print(skate.full_name)
    skate.move()

    esclalator1 = Escalator()
    print(esclalator1)
    esclalator2 = Escalator(owner="AТБ")
    esclalator2.switch_mode()
    print(esclalator2)

    train = Train(free_places=1)
    print("Passengers in train:", train.passengers)
    print("Addede 1 more:")
    train.add_passenger()
    print(train.passengers)
    print("Add 1 more:")
    train.add_passenger()
    print(train.passengers)
    print("Passengers in train:", train.passengers)
    print("Getting out 1 passanger:")
    train.delete_passenger()
    print(train.passengers)
    train.move()
    print(round(car1))