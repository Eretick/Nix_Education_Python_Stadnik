""" Implementation of binary sorting algorithm  """


def binary_search(data: list, search_item):
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

    # check if item in search list range to avoid extra calculation
    if search_item > data[max_index-1]:
        return -1
    elif search_item < data[0]:
        return -1
    # main search algorithm
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

def quick_sort(data:list):
    """ Implementation of quick sort algorhitm
     :data - list of unsorted values
     """
    if len(data) > 0:
        last_index = len(data)-1
        last_item = data[len(data)-1]
        new_data = data[:last_index]
        data_left = []
        data_right = []
        for i in range(len(new_data)):
            if new_data[i] < last_item:
                data_left.append(new_data[i])
            elif new_data[i] >= last_item:
                data_right.append(new_data[i])

        left_sorted = []
        for i in range(len(data_left)-1):
            if data_left[i+1] > data_left[i]:
                left_sorted.append(True)
        right_sorted = []
        for i in range(len(data_right)-1):
            if data_right[i+1] > data_right[i]:
                right_sorted.append(True)

        if len(left_sorted) != len(data_left):
            data_left = quick_sort(data_left)
        if len(right_sorted) != len(data_right):
            data_right = quick_sort(data_right)
        result = data_left + [last_item]+ data_right
        return result

def my_factorial(number):
    """ Recursive factorial implementation """
    if number < 0:
        raise ValueError("Factorial can be only numbers > 0!")
    elif number == 0:
        return 1
    elif number == 1:
        return number
    return number * my_factorial(number-1)