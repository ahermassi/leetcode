""" Design and implement a data structure for Least Recently Used (LRU) cache. It should support the following
operations: get and put.
get(key) - Get the value (will always be positive) of the key if the key exists in the cache, otherwise return -1.
put(key, value) - Set or insert the value if the key is not already present. When the cache reached its capacity, it
should invalidate the least recently used item before inserting a new item.
The cache is initialized with a positive capacity. """

import unittest2 as unittest


class Node:
    def __init__(self, k, v):
        self.key = k
        self.val = v
        self.prev = None
        self.next = None


class LRUCacheV1(object):
    """ The problem can be solved with a hashmap that keeps track of the keys and its values in the double linked list.
        That results in O(1) time for put and get operations and allows to remove the first added node in O(1) time as
        well.
        One advantage of double linked list is that the node can remove itself without other reference. In addition, it
        takes constant time to add and remove nodes from the head or tail.
        One particularity about the double linked list implemented here is that there are dummy head and dummy tail to
        mark the boundary, so that we don't need to check the null node during the update.
        Rules:
            1- Always add new node BEFORE the tail
            2- As a result of previous rule, the LRU node is always the one right AFTER the head
    """

    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.capacity = capacity
        self.nodes = dict()  # (key: node) pairs
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        if key in self.nodes:
            node = self.nodes[key]
            val = node.val
            self.remove(node)  # The node is now most recently accessed, so remove it ..
            self.add(node)  # and place it right before the tail
            return val
        return -1

    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: None
        """
        if key in self.nodes:
            self.remove(self.nodes[key])  # The node is now most recently accessed, so remove it
        node = Node(key, value)
        self.add(node)
        self.nodes[key] = node
        if len(self.nodes) > self.capacity:  # If max capacity reached, delete the LRU node: the one after the head
            node = self.head.next
            self.remove(node)
            del self.nodes[node.key]

    def remove(self, node):
        p = node.prev
        n = node.next
        p.next = n
        n.prev = p

    def add(self, node):
        p = self.tail.prev
        p.next = node
        node.prev = p
        node.next = self.tail
        self.tail.prev = node


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