import time
from abc import ABC

SOLD_PERCENT = 0.05


class CustomWarning(Warning):
    pass


class Product:
    def __init__(self, name: str, price: float, need_cook: bool = False, sale: float = 0.0, order_id: int = None):
        self._cooked = False
        self._base_price = price
        self.name = name
        self._need_cook = need_cook
        self.order_id = order_id
        self.sale = sale

    @property
    def price(self):
        """ Read-only property. Returns final price, including the sale. """
        if self.sale > 0:
            price = self._base_price * (self._base_price * self.sale)
        else:
            price = self._base_price
        return price

    def get_need_cook_status(self):
        """ Method to find out does the product needs to be sent at Kitchen """
        return self._need_cook

    def set_need_cook_status(self, status: bool):
        """ Method for mark product as cooked.
         Argument:
            - status:bool - status to set"""
        self._need_cook = status

    def set_order_id(self, order_id:int):
        if isinstance(order_id, int):
            self.order_id = order_id
        else:
            TypeError("ID must be an integer!")


class Order:
    pass


class Menu:
    """ Main menu class with all products"""
    __products = []

    @property
    def products(self):
        return self.__products

    def add_to_menu(self, products:Product or list):
        def add(product):
            """ Simple internal function for avoid duplicates"""
            if product not in self.products:
                self.__products.append(product)
            else:
                raise UserWarning("This product already exists!")

        if isinstance(products, Product):
            add(products)
        elif isinstance(products, list):
            for item in products:
                if isinstance(item, Product):
                    add(item)
                else:
                    raise TypeError("Can't add not Products to menu!")
        else:
            raise TypeError("Menu must consist a product or products list!")

    def remove_from_menu(self, product):
        if isinstance(product, Product):
            if product in self.__products:
                self.__products.remove(product)
        else:
            raise TypeError("Argument must be a Product type!")


class Person(ABC):
    """ Base abstract Person class """
    def __init__(self, name, phone=None):
        self.name = name
        self.phone = None

    def __str__(self):
        return f"{self.name} with phone number: {self.phone}"

    def info(self):
        """ Method returns a dict with keys 'full_name' and 'phone' """
        return {"full_name": self.name, "phone": self.phone}


class Customer(Person):
    """ Customer class """
    def __init__(self, name, phone=None):
        super().__init__(name, phone)
        self.__bonuses = 0
        self.orders = []

    def create_order(self, products: list):
        """ Creating order (argument type: Order) from products got from menu """
        pass

    def delete_order(self, order):
        """ Cancel order (argument type:Order) """
        if order in self.orders:
            self.orders.remove(order)
            return True
        return False

    def cancel_order(self, order):
        """ Cancel order (argument type:Order) """
        if self.delete_order():
            # some additional cancel stuff goes here
            pass

    def edit_order(self, order, **kwargs):
        pass

    def purchase_order(self, order):
        """ Customer's purchase method  """
        # some additional stuff here
        # then
        if order in self.orders:
            self.delete_order(order)
            self.increase_bonus()

    def increase_bonus(self, value: int or float):
        """ Method accept int or float argument of final numeric value (not percent)  to increase bonuses """
        if isinstance(value, float) or isinstance(value, int):
            self.__bonuses += value

    def decrease_bonus(self, value: int or float):
        """ Method accept int or float argument of final numeric value (not percent)  to increase bonuses """
        if isinstance(value, float) or isinstance(value, int):
            if self.__bonuses - value >= 0:
                self.__bonuses -= value
            else:
                self.__bonuses = 0


class Seller(Person):
    """ Hall administrator class. Works with orders. """
    def __init__(self, salary, name, phone=None):
        super().__init__(name, phone)
        self._salary = salary  # basic salary
        self.sold_price = 0
        self._bonuses = 0.0

    def __increase_bonuses(self, sold_price):
        """ Method for increase seller's bonuses.
         Argument:
            - sold_price: int or float. Price of sold product order.
         """
        if isinstance(sold_price, int) or isinstance(sold_price, float):
            self._bonuses += sold_price * SOLD_PERCENT
        else:
            raise TypeError("The bonuses aeg must be an integer or float!")

    def __decrease_bonuses(self, bonuses):
        """ Method for decrease seller's bonuses.
        For example, after adding it to salary
         Argument:
            - bonuses: int or float. How much bonuses decrease.
         """
        if isinstance(bonuses, int) or isinstance(bonuses, float):
            if self._bonuses - bonuses > 0:
                self._bonuses -= self._bonuses - bonuses
            else:
                self._bonuses = 0
        else:
            raise TypeError("The bonuses aeg must be an integer or float!")

    @property
    def bonuses(self):
        """ Read-only property.
        Returns currency bonuses depends on sold price.  """
        if self.sold_price > 0:
            return self.sold_price * self._bonuses
        return self._bonuses

    @staticmethod
    def add_to_menu(product: Product):
        if isinstance(product, Product):
            Menu.add_to_menu(product)
        else:
            raise TypeError("Not a Product type!")

    @staticmethod
    def remove_from_menu(product: Product):
        if isinstance(product, Product):
            Menu.remove_product(product)
        else:
            raise TypeError("Not a Product type!")

    @staticmethod
    def edit_product(self, product: Product, **kwargs):
        """ Method for editing product's info.
        Arguments:
            - kwargs. Any named parameters.
            Parameter will be overwriten (if exists).
            """
        if isinstance(product):
            for a, k in kwargs:
                if a in product.__dict__:
                    product.__dict__[a] = k
        else:
            raise TypeError("Not a Product type!")

    @staticmethod
    def send_to_kitchen(product: Product):
        """ Sending some products from customer's order to kitchen  """
        if isinstance(product, Product):
            Kitchen.add_dish(product)
        else:
            raise TypeError("Not a Product type!")

    @staticmethod
    def create_delivery(self, order: Order):
        if isinstance(order, Order):
            Delivery.add_deliver(order)


class Cook:
    """ Cook class for Kitchen """
    def __init__(self, name, is_free=True):
        self.name = name
        self.__is_free = is_free

    def cook_dish(self, product: Product):
        """ Method for "cooking" product.
         In result changes the product status cooked to True
         """
        if self.is_free is True:
            if isinstance(product, Product):
                if product.get_need_cook_status() is True:
                    # simulate cooking
                    print(f"Product {product.name} is cooking...")
                    time.sleep(1)
                    print("Please wait...")
                    time.sleep(1)
                    product.set_need_cook_status(False)
                    print("Done!")
                else:
                    raise ValueError(f"No need to cook {product.name} or it already cooked.")
            else:
                raise TypeError("Can't cook not Product type!")
        else:
            raise CustomWarning("This cook is busy now!")

    @property
    def is_free(self):
        return self.__is_free

    def set_free(self, busy_mode: bool):
        """ Change cook.is_free status """
        if isinstance(busy_mode, bool):
            self.__is_free = busy_mode
        else:
            raise TypeError("Argument must be bool type!")


class Hall:
    """ One of important part of restaurant """
    def __init__(self, restaurant, max=0):
        self.max = max
        self.visitors = []
        self.seller = None
        if not isinstance(restaurant, Restaurant):
            raise TypeError("Wrong restaurant object in Hall")
        self.restaurant = restaurant
        self.__is_working = False

    @property
    def is_working(self):
        if self.__is_working is True and self.__can_work():
            return True
        return False

    def __can_work(self):
        """ Check if Hall can work.
        Depends on self.is_working property and restaurant.is_working"""
        if not self.restaurant is None:
            if self.restaurant.is_working:
                return True
        return False

    def begin_service(self):
        """ Open the Hall """
        self.__is_working = True

    def stop_service(self):
        """ Close the Hall """
        self.__is_working = False


class Kitchen:
    """ One of important part of restaurant """
    __dishes = []

    def __init__(self, restaurant):
        self.cooked_dishes = []
        self.personal = []
        if not isinstance(restaurant, Restaurant):
            raise TypeError("Wrong restaurant object in Kitchen")
        self.restaurant = restaurant

    def send_to_cook(self, product):
        """ Method finds first free cook and set cook task to him """
        if isinstance(product, Product):
            for person in self.personal:
                print("Looking for free cook...")
                # in case if kitchen will have more positions in future
                if isinstance(person, Cook):
                    if person.is_free is True:
                        person.cook_dish(product)
                        print("Dish is preparing to cook...")
                        return True
            print("Sorry, all cooks are buy for now. The dish will stay in queue")
            return False
        else:
            raise TypeError("Kitchen works with Products only!")

    @property
    def dishes(self):
        """ Read-only property.
         Returns a list of all preparing dishes. """
        return self.__dishes

    def add_dish(self, product: Product):
        """ Method add Product to Kitchen dishes list. """
        self.__dishes.append(product)

    def remove_dish(self, product: Product):
        """ Method remove Product from Kitchen dishes list. """
        self.__dishes.remove(product)

    def add_cook(self, cook: Cook):
        self.personal.append(cook)

    def remove_cook(self, cook):
        """ Method remove Cook from Kitchen persona list.
        In case of dismissal etc.
        """
        if cook in self.personal:
            index = self.personal.remove(cook)


class Delivery:
    """ One of important part of restaurant """
    def __init__(self, restaurant):
        self.__orders_list = []
        self.delivery_loads = []
        self.restaurant = restaurant

    def add_deliver(self, order):
        pass

    def remove_deliver(self, deliver):
        pass

    def deliver(self):
        pass


class Restaurant:
    """ The main class """
    def __init__(self, name: str, work_time: dict, is_working: bool = False):
        """
        Restaurant constructor

        Arguments:
            - name: The name of restaurant
                type: str
            - work_time: Working shedule
                type: dict. Key is string with day name, value - string of working hours format "start - end"
            - is_working: Current work status.
                type: bool
        """
        self.name = name
        self.work_time = work_time
        self.__is_working = is_working
        self.delivery = None
        self.kitchen = None
        self.hall = None

    def __check_conditions(func):
        """ Decorator for checking full setting up of Restaurant
        Raise CustomWarning if Restaurant has no Delivery, Hall or Kitchen.
        If everything is setted up, calls passed function.
        """
        def wrapper(self, *arg, **kw):
            if isinstance(self.delivery, Delivery) and \
                    isinstance(self.kitchen, Kitchen) and\
                    isinstance(self.hall, Hall):
                result = func(self, *arg, **kw)
                return result
            else:
                raise CustomWarning("You has to setup delivery and kitchen for using Restaurant."
                                    "\nPlease, create Hall, Delivery and Kitchen instances and set them"
                                    "by methods .set_delivery(), .set_kitchen(), .set_hall().")
        return wrapper

    @property
    def is_working(self):
        """ Check availability of delivery and kitchen for opening """
        return self.__is_working

    def set_delivery(self, delivery: Delivery):
        """ Function for manual set Delivery to restaurant.
        Arguments:
            - delivery: Delivery instance """
        if isinstance(delivery, Delivery):
            self.delivery = delivery
        else:
            raise TypeError("The restaurant.set_delivery() argument must be a Delivery type!")

    def set_kitchen(self, kitchen: Kitchen):
        """ Function for manual set Kitchen to restaurant.
                Arguments:
                    - delivery: Kitchen instance """
        if isinstance(kitchen, Kitchen):
            self.kitchen = kitchen
        else:
            raise TypeError("The restaurant.set_kitchen() argument must be a Kitchen type!")

    def set_hall(self, hall: Hall):
        """ Function for manual set Kitchen to restaurant.
                Arguments:
                    - delivery: Kitchen instance """
        if isinstance(hall, Hall):
            self.hall = hall
        else:
            raise TypeError("The restaurant.set_hall() argument must be a Hall type!")

    @__check_conditions
    def open(self):
        """ Change restaurant status to open """
        self.__is_working = True

    def close(self):
        """ Change restaurant status to close """
        self.__is_working = False
