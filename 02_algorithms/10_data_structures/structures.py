""" Task Data Structures - practice """
import logging
# uncomment logging setup line to view debug messages (BinarySearch etc)
logging.basicConfig(level=logging.DEBUG)


def get_hash(key, size):
    """ Generating hash code function

     :argument: item: HashItem. Function used item.key for generating hash.

     :return: index of HashItem element place
    """
    summ = 0
    for i in str(key):
        summ += ord(i)
    index = summ % size
    return index


class ListNode:
    """ Basic element of linked list """
    def __init__(self, value):
        self.value = value
        self.__next = None
        self.__prev = None

    def has_next(self):
        """ Check if node has link to next element.
         Returns True or False
         """
        if self.__next is None or isinstance(self.next, TailNode):
            return False
        return True

    def has_prev(self):
        """ Check if node has link to next element.
         Returns True or False
         """
        if self.__prev is None:
            return False
        return True

    @property
    def next(self):
        """ Read-only property, the next element (if exists, otherwise None) """
        return self.__next

    @property
    def prev(self):
        """ Read-only property, the next element (if exists, otherwise None) """
        return self.__prev

    def set_next(self, next_node, keep_next=True):
        """ Add link to next node """
        #logging.debug([self, next_node, next_node.value, next_node.prev])
        if type(next_node) in [ListNode, BSNode, TailNode, GraphNode] or next_node is None:
            self.__next = next_node
        else:
            raise TypeError("Node must be a None or ListNode type!")

    def set_prev(self, prev_node):
        """ Add link to next node """
        if isinstance(prev_node, ListNode) or prev_node is None:
            if not self.has_prev():
                self.remove_prev()
            self.__prev = prev_node
        else:
            raise TypeError("Node must be a None or ListNode type!")

    def remove_next(self):
        """ Remove link to next node """
        #del self.__next
        self.__next = None

    def remove_prev(self):
        """ Remove link to next node """
        #del self.__prev
        self.__prev = None

    def set_value(self, value):
        """ Change Node value """
        self.value = value


class TopNode(ListNode):
    """ The first non-interactive node after all list values. The head of a list. """
    def __init__(self):
        super().__init__(None)

    def has_prev(self):
        # blocking unwanted methods for this class
        raise AttributeError("'TailNode' object has no attribute 'has_next'")

    @property
    def prev(self):
        # blocking unwanted methods for this class
        raise AttributeError("'TopNode' object has no attribute 'prev'")

    def set_prev(self, prev_node):
        # blocking unwanted methods for this class
        raise AttributeError("'TopNode' object has no attribute 'set_prev'")

    def remove_prev(self):
        # blocking unwanted methods for this class
        raise AttributeError("'TopNode' object has no attribute 'remove_prev'")

    def set_value(self, value):
        # blocking unwanted methods for this class
        raise AttributeError("'TopNode' object has no attribute 'set_value'")


class TailNode(ListNode):
    """ Last non-interactive node after all list values. The tail of list. """
    def __init__(self):
        super().__init__(None)

    def has_next(self):
        # blocking unwanted methods for this class
        raise AttributeError("'TailNode' object has no attribute 'has_next'")

    @property
    def next(self):
        # blocking unwanted methods for this class
        raise AttributeError("'TailNode' object has no attribute 'next'")

    def set_next(self, next_node):
        # blocking unwanted methods for this class
        raise AttributeError("'TailNode' object has no attribute 'set_next'")

    def remove_next(self):
        # blocking unwanted methods for this class
        raise AttributeError("'TailNode' object has no attribute 'remove_next'")

    def set_value(self, value):
        # blocking unwanted methods for this class
        raise AttributeError("'TailNode' object has no attribute 'set_value'")


class BSNode:
    """ Node class for Binary Search Tree """
    def __init__(self, value):
        self.value = value
        self.left_node = None
        self.right_node = None
        self.__prev = None

    @property
    def previous(self):
        return self.__prev

    def set_left(self, node):
        """ Set node argument to left subtree of current BSNode instance """
        if isinstance(node, BSNode) or node is None:
            self.left_node = node
            if node is not None:
                node.set_previous(self)
        else:
            raise TypeError("Can set only BSNode instance!")

    def set_right(self, node):
        """ Set node argument to right subtree of current BSNode instance """
        if isinstance(node, BSNode) or node is None:
            self.right_node = node
            if node is not None:
                node.set_previous(self)
        else:
            raise TypeError("Can set only BSNode instance!")

    def has_left(self):
        """ Check if current Node has left child node """
        if self.left_node is None:
            return False
        return True

    def has_right(self):
        """ Check if current Node has right child node """
        if self.right_node is None:
            return False
        return True

    def set_previous(self, node):
        """ Method for making link to parent node  """
        self.__prev = node


class GraphNode(ListNode):
    """ Node (vertex) for Graph based on ListNode class """
    def __init__(self, value, connection_node=None):
        super().__init__(value)
        # __next attribute is kept for correct LinkedList logic (graph vertext list).
        self.__next = None
        # list of all nodes connected with current node
        self.__connections = LinkedList()

    @property
    def connections(self):
        """ Method for view all connected nodes """
        temp_list = LinkedList()
        for index, list_node in enumerate(self.__connections):
            cur_value = list_node
            temp_list.append(GraphNode(cur_value))
        return  temp_list

    def add_connection(self, node):
        """ Keep links of nodes connected with.
        :argument
            - node - GraphNode instance with integer index value of GraphNode element in general Graph list
        """
        if isinstance(node, GraphNode):
            if node not in self.__connections:
                self.__connections.append(node)
        else:
            raise TypeError("GraphNode can be connected only with GraphNode instance!")

    def remove_connection(self, node_value):
        """ Remove link of passed connected node.
        :argument
            - node -  Integer index value of GraphNode element in general Graph list
        """
        if isinstance(node_value, int):
            print("dada: ", self.connections.data, node_value)
            for i, k in enumerate(self.__connections):
                if k == node_value:
                    self.__connections.delete(i)
        else:
            raise TypeError("Can't remove connection from non-GraphNode instance!")


class LinkedList:
    """ Linked List implementation """
    def __init__(self):
        self.head = TopNode()

    def __len__(self):
        """ len() function support """
        return len(self.data)

    def __getitem__(self, index):
        return self.find_last(last_index=index)

    def __setitem__(self, index, value):
        return self.find_last(last_index=index).set_value(value)

    def __contains__(self, node):
        if self.lookup(node.value) == -1:
            return False
        return True

    def __iter__(self):
        """ for loop support """
        self.__number = 0
        return self

    def __next__(self):
        """ for loop support """
        if self.__number < len(self.data):
            item = self.data[self.__number]
            self.__number += 1
            return item
        else:
            raise StopIteration

    @property
    def data(self):
        """ Function for display all data in LinkedList
        Could be out of rules, but I kept it for check correct list behaviour.
        Can be deleted in final version
        """
        temp = []
        if self.head.has_next() is False:
            return temp
        node = self.head
        while node.has_next() is True:
            if node.next.value is not None:
                temp.append(node.next.value)
            node = node.next
        return temp

    def find_last(self, last_index=None):
        """ Finding last element """
        node = self.head
        step = 0
        while node.has_next():
            # if need not last item, but with specified index
            if last_index is not None:
                if step == last_index:
                    return node
                step += 1
            # if just the last item
            if node.next.has_next() is False:
                return node.next
            else:
                node = node.next
        return node

    def prepend(self, value):
        """ Adding item to the start """
        if type(value) not in [GraphNode, ListNode]:
            node = ListNode(value)
        else:
            node = value
        if not self.head.has_next():
            self.head.set_next(node)
        else:
            node.set_next(self.head.next)
            self.head.set_next(node)

    def append(self, value):
        """ Adding item to the end """
        if type(value) not in [GraphNode, ListNode]:
            node = ListNode(value)
        else:
            node = value
        # checking first position, does list has items after top
        if self.head.has_next() is False:
            self.head.set_next(node)
        # if doesn't, look for the tail
        elif self.head.has_next() is True:
            last = self.find_last()
            last.set_next(node)

    def delete(self, node_index):
        """ Deleting from list by index
        Argument:
            - node_intex: int
        Returns None
        Raises:
            - IndexError of node_index is out of list range
            - TypeError if index is not int"""
        if isinstance(node_index, int):
            if node_index in range(len(self.data)):
                # do some shit here
                current_index = 0
                node = self.head
                prev_node = None
                while node is not None and node.has_next():
                    node = node.next
                    # check previous item to link it later with new next item
                    if current_index == node_index-1:
                        prev_node = node
                    elif current_index == node_index:
                        # additional check if node_index is 0
                        if node_index == 0:
                            prev_node = self.head
                        # if we need to link previous and next items
                        if node.has_next():
                            if node == self.head.next:
                                self.head.set_next(node.next)
                            else:
                                prev_node.set_next(node.next)
                        else:
                            prev_node.set_next(None)
                        # delete node by index after all
                        del node
                        break
                    current_index += 1
            else:
                raise IndexError("Index is out of LinkedList items range")
        else:
            raise TypeError("Index for element deletion must be int type!")

    def lookup(self, value):
        """ Looking for first item with passed value
        Arguments:
            - value: any value you want to find in list
        Returns:
            - index of first ListNode with passed value
            - returns index -1 if ListNode with passed value wasn't found
        """
        index = -1
        if self.head.next is None:
            return index
        node = self.head.next
        counter = 0
        if node.has_next():
            while node is not None and node.has_next():
                if node.value == value:
                    return counter
                if node.next.value == value:
                    return counter + 1
                node = node.next
                counter += 1
        return index


class Queue:
    """ Queue implementation """
    def __init__(self):
        self.head = TopNode()
        self.tail = TailNode()
        self.head.set_next(self.tail)

    def __len__(self):
        """ len() function support """
        return len(self.data)

    def __find_last(self, node: ListNode):
        """ Finding last element, before self.tail """
        node = self.head
        while node.has_next():
            if node.next.has_next() is False:
                return node.next
            else:
                node = node.next
        return node

    @property
    def data(self):
        """ Function for display all data in LinkedList
        Could be out of rules, but I kept it for check correct list behaviour.
        Can be deleted in final version
        """
        temp = []
        if self.head.has_next() is False:
            return temp
        node = self.head
        while node.has_next() is True:
            temp.append(node.next.value)
            node = node.next
        return temp

    def enqueue(self, value):
        """ Adding item to the end of queue """
        node = ListNode(value)
        # checking first position, does list has items after head
        if not isinstance(self.head.next, TailNode):
            last = self.__find_last(self.head)
            node.set_prev(last)
            last.set_next(node)
            node.set_next(self.tail)
            self.tail.set_prev(node)
        # if doesn't, look for the tail
        else:
            self.head.set_next(node)
            node.set_next(self.tail)
            self.tail.set_prev(node)

    def peek(self):
        """ Getting element from end queue.  """
        first = self.head.next
        if isinstance(first, TailNode):
            first = None
        return first

    def dequeue(self):
        """ Deleting last added element from queue  """
        last = self.__find_last(self.head)
        if  type(last) not in [TopNode, TailNode, None]:
            if last.prev is not None:
                last.prev.set_next(self.tail)
            else:
                self.head.set_next(self.tail)
            del last


class Stack:
    def __init__(self):
        self.head = TopNode()

    def __len__(self):
        """ len() function support """
        return len(self.data)

    @property
    def data(self):
        """ Function for display all data in LinkedList
        Could be out of rules, but I kept it for check correct list behaviour.
        Can be deleted in final version
        """
        temp = []
        if self.head.has_next() is False:
            return temp
        node = self.head
        while node.has_next() is True:
            temp.append(node.next.value)
            node = node.next
        return temp

    def push(self, value):
        """ Adding item to the end of queue """
        node = ListNode(value)
        # checking first position, does list has items after head
        if self.head.has_next():
            node.set_next(self.head.next)
            self.head.next.set_prev(node)
            self.head.set_next(node)
        # if doesn't, look for the tail
        else:
            self.head.set_next(node)

    def pop(self):
        """ Pop last added item """
        if self.head.has_next():
            first = self.head.next
            if first.has_next():
                self.head.set_next(first.next)
                first.next.set_prev(self.head)
            else:
                self.head.set_next(None)
            del first
        else:
            raise TypeError("No items left for pop!")

    def peek(self):
        """ Function for peek first added element to stack
        Returns: ListNode if list isn't empty, else None
        """
        node = self.head
        if self.head.has_next():
            while node.has_next():
                node = node.next
            return node
        else:
            return None


class HashItem:
    """ Element for HashTable  """
    def __init__(self, key, value, table_size):
        self.key = key
        self.value = value
        self.key_hashed = get_hash(self.key, table_size) - 1


class HashTable:
    """ Hash table class """
    def __init__(self, size):
        self.__size = size
        self.__array = LinkedList()
        self.__create_empty_array()

    def __create_empty_array(self):
        for i in range(self.__size):
            self.__array.append(HashItem("None", "None", self.__size))

    def __len__(self):
        """ len() function support """
        return  len(self.data)

    def __find(self, key):
        """ Internal method for finding an element by key.  """
        search_value = get_hash(key, self.__size)
        for item in self.__array.data:
            current_key = item.key
            if key == current_key:
                return item

    @property
    def data(self):
        """ Visual part for demonstrating hash table elements """
        nodes = []
        for i in range(len(self.__array)):
            item = self.__array[i]
            if isinstance(item.value, HashItem):
                if item.value.key != "None":
                    temp_item = item.value.key, item.value.value
                    nodes.append(temp_item)

        return nodes

    def insert(self, key, value=None):
        """ Insert element """
        item = HashItem(key=key, value=value, table_size=self.__size)
        index = get_hash(key, self.__size)
        index_item = self.__array[index]
        self.__array[index] = item

    def lookup(self, key):
        """ Get value of item by key.

         Argument: key - key string for looking value.

         Returns: value of item with key or None if not found.
         """
        item = self.__find(key)
        if item is None:
            return None
        return item.value

    def delete(self, key):
        """ Method for deleting item by a key """
        item = self.__find(key)
        if item is None:
            raise KeyError(f"No item with key '{key}'")
        index = item.key_hashed
        self.__array.delete(index)
        item = HashItem("None", "None", self.__size)
        self.__array.append(item)


class BinarySearchTree:
    """ Binary Search Tree implementation """
    def __init__(self):
        self.head = TopNode()

    @staticmethod
    def __compare(internal_node: BSNode, foreign_node: BSNode):
        """ Compairing nodes value """
        if isinstance(internal_node, BSNode) and isinstance(foreign_node, BSNode):
            if internal_node.value <= foreign_node.value:
                return "right"
            return "left"
        else:
            raise TypeError("You can't compaire not BSNode instances!")

    def is_empty(self):
        """ Check if tree has no nodes """
        if self.head.has_next() is False:
            return True
        return False

    @staticmethod
    def __find_final_left(self, begin_node:BSNode) -> BSNode:
        if isinstance(begin_node, BSNode):
            if begin_node.left_node is None:
                return begin_node
            else:
                node = begin_node
                while node.left_node is not None:
                    node = node.left_node
                return  node
        else:
            raise TypeError("begin_node argument must be BSNode type!")

    def __find_place(self, node) -> BSNode:
        """ Method for finding place to insert
         :argument node - BSNode instance you trying to insert
         :return final_node - BSNode instance of current tree which will be parent for passed node argument
         """
        start = self.head.next
        if start is None:
            return start

        while True:
            result = self.__compare(start, node)
            if result == "left":
                if start.left_node is None:
                    return start
                else:
                    start = start.left_node
            else:
                if start.right_node is None:
                    return start
                else:
                    start = start.right_node

    def insert(self, value):
        """ Insert method to put Binary Search node to correct place """
        node = BSNode(value)
        if self.is_empty():
            self.head.set_next(node)
            logging.debug(f"Set first value {node.value}")
        else:
            final_node = self.__find_place(node)
            side = self.__compare(final_node, node)
            if side == "left":
                final_node.set_left(node)
            else:
                final_node.set_right(node)
            # debug view message
            logging.debug(f"Set {node.value} as {side} in {final_node.value}")

    def lookup(self, value):
        """ Method finds a node with passed value.

         :argument value - value to search for

         :return value of BSNode if found, else None
         """
        node = BSNode(value)
        return self.__find_place(node)

    def delete(self, value):
        node = self.lookup(value)
        if node is None:
            raise ValueError(f"No item with value '{value}'")
        # find out which side of parent took current node
        parent_part = self.__compare(node.previous, node)

        # if current node has no right item
        if not node.has_right():
            if parent_part == "right":
                node.previous.set_right(node.left_node)
            else:
                node.previous.set_left(node.left_node)
        # if current node has only right item
        elif not node.has_left() and node.has_right():
            # and right child item has no left child item
            if not node.right_node.has_left():
                if parent_part == "right":
                    node.previous.set_right(node.right_node)
                else:
                    node.previous.set_left(node.right_node)
        # if current node has right child item and that right child item has his own left child item
        elif not node.has_left() and node.has_right():
            if node.right_node.has_left():
                if parent_part == "right":
                    last_left = self.__find_final_left(node)
                    node.previous.set_right(last_left)
                else:
                    last_left = self.__find_final_left(node)
                    node.previous.set_left(last_left)
        del node


class Graph:
    """ Unordered graph without node's weight """
    def __init__(self):
        self.vertex_list = LinkedList()

    def __len__(self):
        return len(self.vertexes)

    @property
    def vertexes(self):
        return self.vertex_list.data

    def is_empty(self):
        """ Check if graph has no vertexes """
        if len(self.vertex_list) == 0:
            return True
        return False

    def insert(self, value, connection_nodes: list = None):
        """ Add item to all items list
        :argument
            - connection_nodes - list of nodes values to connect with
        """
        node = GraphNode(value)
        if node not in self.vertex_list and node.value not in self.vertex_list.data:
            # insert value (add to main list)
            self.vertex_list.append(node)
            # set connections if passed
            if connection_nodes is not None:
                # if passed only 1 node as integer
                if isinstance(connection_nodes, int):
                    connection_nodes = [connection_nodes]
                # making connections
                for node_value in connection_nodes:
                    if self.vertex_list.lookup(node_value) != -1:
                        self.add_connection(node.value, node_value)
        else:
            raise ValueError(f"Vertex with value {value} is already added.")

    def delete(self, value):
        """ Method delete vertex and all connections.

         :argument value - GraphNode value to find and delete with all links inside connected nodes.

         """
        node = self.lookup(value)
        if node is not None:
            delete_index = self.vertex_list.lookup(value)
            # TODO: deleting connections if exists
            # remove all connections first
            connection_indexes = self.lookup(value).connections
            print(connection_indexes.data)
            # if node has connection
            if len(connection_indexes) > 0:
                # finding index of current deleted element in general list
                del_index = self.vertex_list.lookup(node.value)
                for node_index in connection_indexes.data:
                    # finding item from connections
                    # +1 is fix offset cause LinkedList starts from TopNode
                    connected_node = self.vertex_list[node_index+1]
                    # find index of deleted value and remove it
                    if connected_node is not None:
                        for i in connected_node.connections.data:
                            print("current:", i, connected_node.connections.data, del_index)
                            if node_index is not None:
                                if i == del_index:
                                    print("found", i)
                                    connected_node.remove_connection(delete_index)
                            else:
                                raise ValueError(f"Index {i} of {connected_node.value} not found")
                    else:
                        raise AttributeError(f"Connected node not found by index {node_index}")

            # finally deleting node from list
            self.vertex_list.delete(delete_index)
        else:
            raise ValueError(f"Vertex with value {value} does not exist.")

    def lookup(self, value) -> GraphNode:
        """ Method finds a vertex by passed value.

         :argument value - any value stored in GraphNode instance

         :returns GraphNode
         """
        index = self.vertex_list.lookup(value)
        print("graph search item index", index)
        if index == -1:
            return None
        return self.vertex_list.find_last(index+1)

    def add_connection(self, value_from,  value_to):
        """ Make vertex connected with another vertex passed by node argument.
         Must be used after inserting to graph list!
         :argument value_from - value stored in 1st Graph node

         :argument value_to - value stored in 2nd Graph node

         :exception  ValueError if one of nodes out of Graph list.
         """
        # Finding elements in Graph list and keep indexes to set as connection of vertex
        node_from = self.lookup(value_from)
        node_to = self.lookup(value_to)
        # if nodes was found
        if node_from is not None and node_to is not None:
            if node_from in self.vertex_list and node_to in self.vertex_list:
                print("hello")
                # set first node
                # Looking for their undexes in main graph list
                node_from_index = self.vertex_list.lookup(node_from.value)
                node_to_index = self.vertex_list.lookup(node_to.value)
                print(self.vertex_list.data, node_from.value, node_to.value, node_from_index, node_to_index)
                # Adding indexes to connections list of nodes
                index_node_to = GraphNode(node_to_index)
                index_node_from = GraphNode(node_from_index)
                node_to.add_connection(index_node_from)
                node_from.add_connection(index_node_to)
                #node_from.add_connection(node_to)
                #index = node_from.connections.lookup(node_to.next.value)
                #node_from.connections.delete(index)
                # # set second node
                # node_to.add_connection(node_from)
                # index = node_to.connections.lookup(node_from.next.value)
                # node_to.connections.delete(index)
            else:
                raise ValueError("One of nodes or both are not in Graph list!")
        else:
            raise TypeError("One of nodes is None in some reason!")


g = Graph()
print(g.vertexes)
# print(g.vertexes)
# g.insert(12)
# print(g.vertexes)
# g.insert(16)
# print(g.vertexes)
#
# #print("before connection", g.lookup(16).connections.data)
# g.add_connection(12, 16)
# #print("after connection before delete", g.lookup(16).connections.data)
# g.delete(12)
#print("after delete", g.lookup(16).connections.data)

# raise an error if exists
#g.insert(12)
#rint(g.vertex_list.data)

# g.add_connection(4, 12)
# print("found 4", g.lookup(4), g.lookup(4).connections.data)
# print("found 12", g.lookup(12), g.lookup(12).connections.data)
# print(g.vertexes)

# print('insert with connections')
# g.insert(88, connection_nodes=4)
# print(g.lookup(4).connections.data)
# print(g.lookup(88).connections.data)

