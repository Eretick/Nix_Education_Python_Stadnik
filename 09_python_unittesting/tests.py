import pytest
import to_test


@pytest.mark.parametrize("test_input", [1, 2.0, 'abc'])
def test_type_error(test_input):
   assert to_test.even_odd(test_input)


def test_sum_all():
   assert to_test.sum_all(1, 2, 3) == 6, "Wrong sum algorithm"
   assert to_test.sum_all(1, 2.0, 2.5) == 5.5, "Only integers"
   assert to_test.sum_all('1', '2')  # не получилось сделать кастомное уведомление


def test_time():
    assert to_test.time_of_day() in ["morning", "afternoon", "night"], "Not all branches are returns value"
    assert isinstance(to_test.time_of_day(), str), "Must return a string!"

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
    create_product.subtract_quantity(20)
    assert create_product.quantity >= 0, "You can't subtract more products then available"
    assert abs(qual1) > abs(create_product.quantity), \
        "The subtract number must be positive!"


@pytest.mark.parametrize("test_input", [5, 0, -5])
def test_products_add_quantity(create_product, test_input):
    qual1 = create_product.quantity
    create_product.add_quantity(20)
    assert create_product.quantity > qual1, "The add number must be positive!"
    assert create_product.quantity < 0, "You can't subtract more products then available"


@pytest.mark.parametrize("test_input", [40, 20.5, -5, '34'])
def test_product_change_price(create_product, test_input):
    assert isinstance(test_input, int) or isinstance(test_input, float), \
        f"Argument must be a number, not a {type(test_input)}"
    create_product.change_price(test_input)
    assert create_product.price > 0, "The price can't be less then zero!"




