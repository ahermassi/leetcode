""" Design and implement a data structure for Least Recently Used (LRU) cache. It should support the following
operations: get and put.
get(key) - Get the value (will always be positive) of the key if the key exists in the cache, otherwise return -1.
put(key, value) - Set or insert the value if the key is not already present. When the cache reached its capacity, it
should invalidate the least recently used item before inserting a new item.
The cache is initialized with a positive capacity. """

from collections import OrderedDict
import unittest2 as unittest


class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.next = None
        self.pre = None


class LRUCacheV1(object):
    """ The problem can be solved with a hash map that keeps track of the keys and its values in the doubly linked list.
        That results in O(1) time for put and get operations and allows to remove the first added node in O(1) time as
        well.
        One advantage of doubly linked list is that the node can remove itself without other reference. In addition, it
        takes constant time to add and remove nodes from the head or tail.
        One particularity about the doubly linked list implemented here is that there are dummy head and dummy tail to
        mark the boundary, so that we don't need to check the null node during the update.
        Rules:
            1- Always add new node BEFORE the tail: this is the most recently used
            2- As a result of previous rule, the LRU node is always the one right AFTER the head
    """

    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.nodes = {}  # (key: node) pairs
        self.capacity = capacity
        self.size = 0
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.pre = self.head

    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        if key not in self.nodes:
            return -1
        node = self.nodes[key]
        self.remove(node)  # The node is now most recently accessed, so remove it ..
        self.add(node)  # and place it right before the tail
        return node.val

    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: None
        """
        if key in self.nodes:  # If key already exists, then this is essentially an update
            self.remove(self.nodes[key])  # The node is now most recently accessed, so remove it
        node = Node(key, value)
        self.add(node)
        if self.size > self.capacity:  # If max capacity reached, delete the LRU node: the one after the head
            lru = self.head.next
            self.remove(lru)

    def remove(self, node):
        node.pre.next = node.next
        node.next.pre = node.pre
        del self.nodes[node.key]
        self.size -= 1

    def add(self, node):
        tail = self.tail
        p = tail.pre
        p.next = node
        node.pre = p
        tail.pre = node
        node.next = tail
        self.nodes[node.key] = node
        self.size += 1


class LRUCacheV2(object):
    """ We're asked to implement the structure which provides the following operations in O(1) time :
            Get the key / Check if the key exists
            Put the key
            Delete the first added key
        The first two operations in O(1) time are provided by the standard hash map, and the last one - by linked list.
        There is a structure called ordered dictionary which combines behind both hash map and linked list. In Python,
        this structure is called OrderedDict

    """

    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.nodes = OrderedDict()
        self.capacity = capacity
        self.size = 0

    def get(self, key):
        """ When an element is accessed, that makes it a recently used element, so we need to pop and place it again.
        :type key: int
        :rtype: int
        """
        if key not in self.nodes:
            return -1
        val = self.nodes[key]
        self.nodes.pop(key)  # Remove the element ..
        self.nodes[key] = val  # and put it back to produce a new order in the dict
        return val

    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: None
        """
        if key in self.nodes:  # If key already exists, then this is essentially an update
            self.nodes.pop(key)
        elif self.size == self.capacity:  # Max capacity reached
            self.nodes.popitem(last=False)  # The popitem() method for ordered dictionaries returns and removes a
            # (key, value) pair. The pairs are returned in LIFO order if last=true and FIFO order if last=false.
            # Here, last=False which means the first element in (least recently used) will be popped.
        self.nodes[key] = value
        self.size += 1


class Test(unittest.TestCase):
    cache = LRUCacheV1(2)
    cache.put(1, 1)
    cache.put(2, 2)
    val1 = cache.get(1)
    cache.put(3, 3)
    val2 = cache.get(2)
    cache.put(4, 4)
    val3 = cache.get(1)
    val4 = cache.get(3)
    val5 = cache.get(4)

    def test_LRUCache(self):
        self.assertEqual(1, self.val1)
        self.assertEqual(-1, self.val2)
        self.assertEqual(-1, self.val3)
        self.assertEqual(3, self.val4)
        self.assertEqual(4, self.val5)


if __name__ == '__main__':
    unittest.main()