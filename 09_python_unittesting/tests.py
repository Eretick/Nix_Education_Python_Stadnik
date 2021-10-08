from datetime import datetime

import pytest
import to_test


@pytest.mark.parametrize("test_input", [1, 2.0, 'abc'])
def test_type_error(test_input):
    assert to_test.even_odd(test_input)


def test_sum_all():
    assert to_test.sum_all(1, 2, 3) == 6, "Wrong sum algorithm"
    assert to_test.sum_all(1, 2.0, 2.5) == 5.5, "Only integers"
    assert to_test.sum_all('1', '2')  # не получилось сделать кастомное уведомление


@pytest.fixture()
def morning_time():
    return datetime(2021, 10, 10, hour=8)


@pytest.fixture()
def afternoon_time():
    return datetime(2021, 10, 10, hour=13)


@pytest.fixture()
def night_time():
    return datetime(2021, 10, 10, hour=2)


def test_time():
    assert to_test.time_of_day() in ["morning", "afternoon", "night"], "Not all branches are returns value"
    assert isinstance(to_test.time_of_day(), str), "Must return a string!"


def test_morning(morning_time):
    now = morning_time
    assert to_test.time_of_day() == "morning", "Wrong morning calculation"


def test_afternoon(afternoon_time):
    now = afternoon_time
    assert to_test.time_of_day() == "afternoon", "Wrong afternoon calculation"


def test_night(night_time):
    now = night_time
    assert to_test.time_of_day() == "night", "Wrong night calculation"


@pytest.fixture()
def create_product(price=10, quantity=15):
    return to_test.Product("Product", price=price, quantity=quantity)


@pytest.mark.parametrize("test_input", [10, 0, -5])
def test_product_price(create_product, test_input):
    create_product.price = test_input
    assert create_product.price >= 0, "Product's price can't be lower zero!"


@pytest.mark.parametrize("test_input", [10, 0, -5])
def test_product_quantity(create_product, test_input):
    assert create_product.quantity >= 0, "Product's quantity can't be lower zero!"


@pytest.mark.parametrize("test_input", [5, 0, -5])
def test_products_subtract(create_product, test_input):
    qual1 = create_product.quantity
    create_product.subtract_quantity(test_input)
    assert create_product.quantity >= 0, "You can't subtract more products then available"
    assert abs(qual1) >= abs(create_product.quantity), \
        "The subtract number must be positive!"


@pytest.mark.parametrize("test_input", [5, 0, -5])
def test_products_add_quantity(create_product, test_input):
    qual1 = create_product.quantity
    create_product.add_quantity(test_input)
    assert create_product.quantity >= qual1, "The add number must be positive!"
    assert create_product.quantity > 0, "You can't add with negative result"


@pytest.mark.parametrize("test_input", [40, 20.5, -5, '34'])
def test_product_change_price(create_product, test_input):
    assert isinstance(test_input, int) or isinstance(test_input, float), \
        f"Argument must be a number, not a {type(test_input)}"
    create_product.change_price(test_input)
    assert create_product.price >= 0, "The price can't be less then zero!"


@pytest.fixture()
def shop(price=10, quantity=15):
    products = [
                to_test.Product(title="Xiaomi Mi 10", price=17000, quantity=200),
                to_test.Product(title="Xiaomi Mi 10T Pro", price=19000, quantity=100),
                to_test.Product(title="Samsung J1", price=2000, quantity=50)
                ]
    return to_test.Shop(products=products)


@pytest.mark.parametrize("product", [["Mi 11 (label)",
                                     to_test.Product(title="Xiaomi Mi 10", price=17000, quantity=200),
                                     None]]
                         )
def test_shop_products_type(product):
    temp_shop = to_test.Shop(products=product)
    for product in temp_shop.products:
        assert isinstance(product, to_test.Product) or temp_shop.products == [], "Unsupported product type!"


def test_sell_product(shop):
    assert shop.sell_product("Xiaomi Mi 10", 100) is not None
    with pytest.raises(ValueError):
        shop.sell_product("Samsung J1", 300), "Must be warning about amount!"
    assert shop.sell_product(1, bool) is None, "Not found item should return None"





