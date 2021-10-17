""" Implementation of binary sorting algorithm  """


def binary(data: list, search_item):
    """ Function for creating sorted list by binary search
    :list - list of sorted data
    :returns index of element
    """
    # Check if list is sorted
    if data != sorted(data):
        raise ValueError("List must be sorted!")

    index = -1  # index of found element. Default -1 (not found)

    max_index = len(data)
    data_copy = data.copy()
    cur_start = 0
    cur_end = max_index
    for i in range(len(data)):
        mid_index = len(data_copy)//2
        mid_item = data_copy[mid_index]
        if mid_item == search_item:
            index = mid_index+cur_start
            break
        elif mid_item > search_item:
            cur_end -= mid_index
            data_copy = data[cur_start:cur_end]
        elif mid_item < search_item:
            cur_start += mid_index
            data_copy = data[cur_start:cur_end]
    return index
