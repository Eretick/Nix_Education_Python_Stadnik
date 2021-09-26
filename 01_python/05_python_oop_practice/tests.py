""" tests for restaurant.py """
import pytest
from restaurant import *


@pytest.fixture
def restaurant_only():
    """ Restaurant fixture for future tests"""
    work_time = {
        "Понедельник": "8:00-23:00",
        "Вторник": "8:00-23:00",
        "Среда": "8:00-23:00",
        "Четверг": "8:00-23:00",
        "Пятница": "8:00-23:00",
        "Суббота": "8:00-23:00",
        "Воскресенье": "Выходной",
    }
    restaurant = Restaurant("Снежинка", work_time, False)
    return restaurant


@pytest.fixture
def kitchen_only(restaurant_only):
    """ Kitchen fixture for future tests"""
    kitchen = Kitchen(restaurant_only)
    return kitchen


@pytest.fixture
def delivery_only(restaurant_only):
    """ Delivery fixture for future tests"""
    delivery = Delivery(restaurant_only)
    return delivery


@pytest.fixture
def hall_only(restaurant_only):
    """ Hall fixture for future tests"""
    hall = Hall(restaurant_only, max=50)
    return hall


@pytest.fixture
def restaurant_full(restaurant_only, hall_only, delivery_only, kitchen_only):
    restaurant = restaurant_only
    restaurant.set_kitchen(kitchen_only)
    restaurant.set_hall(hall_only)
    restaurant.set_delivery(delivery_only)
    return restaurant


@pytest.fixture
def menu():
    return Menu()


@pytest.fixture
def temp_product():
    return Product("Beer", 15.70)


@pytest.fixture
def product_for_cook():
    return Product("Pizza", 30.0, need_cook=True, order_id=0)


@pytest.fixture
def cook_not_busy():
    return Cook("James", is_free=True)


@pytest.fixture
def cook_busy():
    return Cook("Mary", is_free=False)


def test_kitchen(kitchen_only):
    assert kitchen_only


def test_hall(hall_only):
    assert hall_only


def test_delivery(delivery_only):
    assert delivery_only


def test_simple_restaurant(restaurant_only):
    """ Simple restaurant instance creating test """
    assert restaurant_only


def test_full_restaurant(restaurant_full):
    """ Simple restaurant instance creating test with correct Kitchen, Hall and Delivery """
    assert restaurant_full


def test_open_full(restaurant_full):
    restaurant_full.open()
    assert restaurant_full.is_working is True, "Error with opening of full setted up restaurant"


def test_open_no_setup(restaurant_only, hall_only, kitchen_only, delivery_only):
    """ Test Restaurant.__check_conditions decorator
    Test must be passed if functions with this decorator raised error
    cause of Hall, Delivery or Kitchen was not setted.
    """
    # Here checks not all variants, cause restaurant_only is not isolated
    # object. They were previously check and working alongside
    # but affects result if together.

    # no setups
    with pytest.raises(CustomWarning):
        restaurant_only.open()
        assert restaurant_only.is_working is False, "You need to setup Kitchen, Delivery and Hall"

    # only kitchen
    with pytest.raises(CustomWarning):
        restaurant_only.set_kitchen(kitchen_only)
        restaurant_only.open()
        assert restaurant_only.is_working is False, "You need to setup Kitchen, Delivery and Hall"

    # only delivery and kitchen
    with pytest.raises(CustomWarning):
        restaurant_only.set_delivery(delivery_only)
        restaurant_only.set_kitchen(kitchen_only)
        restaurant_only.open()
        assert restaurant_only.is_working is False, "You need to setup Kitchen, Delivery and Hall"


def test_product():
    args = ["Pizza", 27.50, True, 0.0, 0]
    p = Product(args[0], args[1], need_cook=args[2], sale=args[3], order_id=args[4])
    assert p.name == args[0]
    assert p.price == args[1] if p.sale == 0 else p._base_price * (p._base_price * p.sale)
    assert p.get_need_cook_status() == args[2]
    assert p.set_need_cook_status(not args[2]) != args[2]
    assert  p.order_id == args[4]
    assert p.set_order_id(args[4]+1) != args[4]


def test_menu(menu, temp_product):
    assert menu.products == [], "products list must be empty for new menu"
    menu.add_to_menu(temp_product)
    assert len(menu.products) == 1, "Must be only 1 product after adding 1 single product"
    menu.remove_from_menu(temp_product)
    assert len(menu.products) == 0, "Must be no products after removing the last one"

    # test raising exception if product already in menu
    with pytest.raises(UserWarning):
        menu.add_to_menu(temp_product)
        assert menu.add_to_menu(temp_product)


def test_cook_twice(cook_not_busy, product_for_cook):
    """ Test of cooking the same product twice.
    Test passed if second cooking of same product raise ValueError
    """

    cook_not_busy.cook_dish(product_for_cook)
    with pytest.raises(ValueError):
        cook_not_busy.cook_dish(product_for_cook)

def test_busy_cook(cook_busy, product_for_cook):
    """ Test of cooking by busy cook
    Test passed if busy cook raise a CustomWarning """
    with pytest.raises(CustomWarning):
        assert cook_busy.cook_dish(product_for_cook)


def test_cook_set_free(cook_busy, product_for_cook):
    """ Test of changing state of cook.
     Busy cook set to free and then tries to cook the dish.
     Cooking should be successful (product.get_need_cook_status should be False)"""
    cook_busy.set_free(True)
    # if product needs to be cooked
    assert product_for_cook.get_need_cook_status() is True
    cook_busy.cook_dish(product_for_cook)
    assert product_for_cook.get_need_cook_status() is False

