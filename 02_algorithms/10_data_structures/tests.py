""" Tests for structures """
import pytest
from structures import LinkedList, Queue, Stack, HashTable, BinarySearchTree, Graph


@pytest.fixture
def linked_list():
    """ LinkedList test fixture """
    return LinkedList()


@pytest.fixture
def linked_list_filled(linked_list):
    """ LinkedList test fixture with some fixed data """
    values = [9, 2.4, 8]
    for value in values:
        linked_list.append(value)
    return linked_list


@pytest.fixture
def queue():
    """ Queue test fixture """
    return Queue()


@pytest.fixture
def stack_empty():
    """ Empty stack fixture """
    return Stack()


@pytest.fixture
def stack_filled(stack_empty):
    """ Stack with elements fixture """
    values = [1, 2, 3, 4.0, "string", None]
    stack = Stack()
    for value in values:
        stack.push(value)
    return stack


@pytest.fixture
def hash_table_empty():
    """ Fixture of empty hash table from structures.py"""
    return HashTable


@pytest.fixture
def binary_search():
    """ Fixture of binary search tree instance from structures.py """
    return BinarySearchTree()


@pytest.fixture
def graph():
    """ Fixture of Graph from structures.py """
    return Graph()


@pytest.mark.parametrize("value", [9,"f", 2.4])
def test_linked_append(linked_list, value):
    """ Test append function of LinkedList. Every item should be added after last item """
    first_len = len(linked_list)
    linked_list.append(value)
    second_len = len(linked_list)
    assert second_len > first_len, "length of list should be ancreased then before append!"
    # test correct multiple append
    linked_list.append(25)
    assert len(linked_list) > second_len, "length of list should increase after previous append!"
    assert linked_list.data[1] == 25, "Wrong item place after double append!"


@pytest.mark.parametrize("value", [9,"f", 2.4])
def test_linked_prepend(linked_list, value):
    """ Test prepend function of LinkedList. Every item should be added to beginning """
    first_len = len(linked_list)
    linked_list.prepend(value)
    second_len = len(linked_list)
    assert second_len > first_len, "length of list should be ancreased then before append!"
    # test correct multiple append
    linked_list.prepend(25)
    assert len(linked_list) > second_len, "length of list should increase after previous append!"
    assert linked_list.data[0] == 25, "Wrong item place after double append!"


def test_linked_lookup(linked_list_filled):
    """ Test lookup function from LinkedList """
    assert linked_list_filled.lookup(9) == 0, "Wrong found 1st item index."
    assert linked_list_filled.lookup("f") == -1, "Wrong not found item index."
    assert linked_list_filled.lookup(2.4) == 1, "Wrong found somethere inside item index."
    assert linked_list_filled.lookup(8) == len(linked_list_filled)-1, "Wrong found last item index."


@pytest.mark.parametrize("delete_values", [0, 5, 1, 2])
def test_linked_delete(linked_list_filled, delete_values):
    """ Test delete function from LinkedList """
    if delete_values in range(len(linked_list_filled.data)):
        length = len(linked_list_filled)
        linked_list_filled.delete(delete_values)
        assert len(linked_list_filled) < length, "List's len() must be decreased after removing element"
    else:
        with pytest.raises(IndexError):
            assert linked_list_filled.delete(delete_values), "Deleting of item with wrong index must raise IndexError!"


def test_queue_enqueue(queue):
    """ Test adding to queue end element function from Queue """
    first_len = len(queue)
    queue.enqueue(2)
    second_len = len(queue)
    assert second_len > first_len, "length of queue must increase after adding to queue!"


def test_queue_dequeue(queue):
    """ Test adding to queue end element function from Queue """
    queue.enqueue(2)
    first_len = len(queue)
    queue.dequeue()
    second_len = len(queue)
    assert second_len < first_len, "length of queue must decrease after adding to queue!"


@pytest.mark.parametrize("elements", [[1,2,3,4]])
def test_queue_peek(queue, elements):
    """ test Queue.peek() function  """
    for i in elements:
        queue.enqueue(i)
    assert queue.peek().value == elements[0], "Wrong 1st item element!"


def test_queue_empty_peek(queue):
    """ test Queue.peek() function from queue of queue is empty """
    assert queue.peek() is None, "First element for empty queue should be None!"


@pytest.mark.parametrize("value", [1, 2.0, 3, "string", None])
def test_stack_push(stack_empty, value):
    """ Test push function from Stack """
    first_len = len(stack_empty)
    stack_empty.push(value)
    second_len = len(stack_empty)
    assert second_len > first_len, "Stack length must increase after pushing a value!"


def test_stack_pop(stack_filled):
    """ Test pop function from Stack """
    first_len = len(stack_filled)
    stack_filled.pop()
    second_len = len(stack_filled)
    assert second_len < first_len, "Stack length must decrease after pop a value!"


def test_stack_pop_more(stack_filled):
    """ Test pop function from Stack in case pop more elements then available """
    # Pop trows an exception if try pop in empty stack
    with pytest.raises(TypeError):
        for i in range(len(stack_filled)+1):
            stack_filled.pop()


def test_hashtable_without_size(hash_table_empty):
    """ HashTable test for empty hash table. """
    with pytest.raises(TypeError):
        hash_table_empty(), "HashTable must have a size"


def test_hashtable_insert(hash_table_empty):
    """ HashTable insert test """
    table = hash_table_empty(5)
    len_1 = len(table)
    table.insert(5)
    len_2 = len(table)
    assert len_2 > len_1, "Table length must increase after insert value"
    assert table.data != [], "Hash table doesn't have a value or data view is broken!"


@pytest.mark.parametrize("values", [[["first",1], ["second",2]]])
def test_hashtable_lookup(hash_table_empty, values):
    """ HashTable lookup test """
    table = hash_table_empty(5)
    exist = [values[0][0], values[0][1]]
    no_exist = [values[1][0], values[1][1]]
    table.insert(exist[0], exist[1])
    assert table.lookup(exist[0]) == exist[1], "Not corret value after looking for existing value!"
    assert table.lookup(no_exist[0]) is None, "Value must be None then looking for not existing value!"


@pytest.mark.parametrize("values", [{"first":1, "second":2, "third":3, 14:None}])
def test_hashtable_delete(hash_table_empty, values):
    """ HashTable delete with correct values test """
    table = hash_table_empty(25)
    for i in values.items():
        table.insert(i[0], i[1])
    len_1 = len(table)
    key = list(values.keys())[0]
    table.delete(key)
    len_2 = len(table)
    assert len_2 <= len_1, "Table length must decrease after delete value"
    assert table.lookup(key) is None, "Value should be None cause of looking for deleted item "


def test_hashtable_delete_empty_or_not_existing(hash_table_empty):
    """ HashTable delete with uncorrect values test """
    # with empty HashTable
    table = hash_table_empty(20)
    with pytest.raises(KeyError):
        assert table.delete("any")
    table.insert("1", 1)
    # with not empty
    with pytest.raises(KeyError):
        assert table.delete("2")


@pytest.mark.parametrize("values", [1, "one"], [2, 2.0], ["state", "sweet"])
def binary_search_insert(binary_search, values):
    """ Binary Tree search testes """
    # Trying to find not added value
    assert binary_search.lookup(values[0]) is None, "Not found item must return None!"
    binary_search.insert(values[0], values[1])
    assert binary_search.lookup(values[0]) == values[1], "Wrong .lookup result"


@pytest.mark.parametrize("value", [1, "2.0", "text", [1, 2, 3]])
def test_graph_insert(graph, value):
    """ Simple graph insert node test """
    len_1 = len(graph)
    graph.insert(value)
    len_2 = len(graph)
    assert len_2 > len_1, "Graph length must increase after insert value!"


def test_graph_double_insert(graph):
    """ Graph must have no duplicates. Insert duplicate raise an error """
    graph.insert(1)
    with pytest.raises(ValueError):
        graph.insert(1), "Here must be an Exception cause of duplicate value"


@pytest.mark.parametrize("values", [[1, "2.0", "text", [1, 2, 3]]])
def test_graph_delete(graph, values):
    """ Simple graph delete node test """

    # delete existed value
    for value in values:
        graph.insert(value)
    len_1 = len(graph)
    graph.delete(values[1])
    len_2 = len(graph)
    assert len_2 < len_1, "Graph length must decrease after delete value!"

    # delete not existed node (also works with empty graph
    with pytest.raises(ValueError):
        graph.delete(123)


@pytest.mark.parametrize("values_list", [[1, 2]])
def test_graph_add_connection(graph, values_list):
    """ Connections tests """
    for i in values_list:
        graph.insert(i)
    # before connection list is empty
    assert len(graph.lookup(values_list[0]).connections.data) == 0 and \
           len(graph.lookup(values_list[1]).connections.data) == 0, "Must be no items in connections!"
    # adding connection
    graph.add_connection(values_list[0], values_list[1])
    # connection list items count  in both nodes should inscrease
    assert len(graph.lookup(values_list[0]).connections.data) > 0 and \
           len(graph.lookup(values_list[1]).connections.data) > 0, "Connections must be added!"


def test_graph_lookup(graph):
    """ Graph's lookup function """
    graph.insert(2)
    graph.insert(1)
    assert graph.lookup(1) is not None, "Inserted node must be found"
    assert graph.lookup("12") is None, "Not inserted node must be not found"
