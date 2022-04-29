""" Design and implement a data structure for Least Recently Used (LRU) cache. It should support the following
operations: get and put.
get(key) - Get the value (will always be positive) of the key if the key exists in the cache, otherwise return -1.
put(key, value) - Set or insert the value if the key is not already present. When the cache reached its capacity, it
should invalidate the least recently used item before inserting a new item.
The cache is initialized with a positive capacity. """

from collections import OrderedDict
import unittest2 as unittest


# Watch: https://www.youtube.com/watch?v=S6IfqDXWa10

class Node:
    def __init__(self, key, val):
        self.key = key  # We have to store the key because we need to know a key when we remove a node from the map.
        # Otherwise, for each remove operation we would need to scan the entire Map
        self.val = val
        self.next = None
        self.prev = None


class LRUCacheV1(object):
    """ The problem can be solved with a hash map that keeps track of the keys and its values in the doubly-linked list.
        That results in O(1) time for put and get operations and allows to remove the first added node in O(1) time as
        well.

        One advantage of doubly-linked list is that the node can remove itself without other reference. In addition, it
        takes constant time to add and remove nodes from the head or tail.

        In a singly-linked list, we would also need a reference to the node before the one we want to remove.
        Therefore, if we were using a singly-linked list, we wouldn't be able to remove nodes we retrieved from the
        hash map in O(1) time because we don't have a reference to the one before them. By using a doubly-linked list,
        we can retrieve node from the hash map in O(1) and then remove the node itself from the list in O(1), giving
        the entire operation an O(1) running time.

        One particularity about the doubly-linked list implemented here is that there are dummy head and dummy tail to
        mark the boundary, so that we don't need to check the null node during the update.

        Rules:
            1- Always add new node AFTER the dummy head: this is the most recently used
            2- As a result of the previous rule, the LRU node is always the one right BEFORE the dummy tail

        put :
            - If the key is already in the cache, we remove the key node and re-insert it after the head with the
               new value.
            - If the key is not in cache, we insert the new key node after the head. If the cache becomes full, we
               delete the node before the tail to make room for the new node.

        get:
            - Remove the node
            - Re-insert the node after the head
            - Return the value of the node

    Time complexity: O(1)
    Space complexity: O(N)
    """

    def __init__(self, capacity):
        self.nodes = {}  # (Node.key: Node) pairs
        self.capacity = capacity
        self.size = 0
        # Dummy head and tail nodes to avoid empty states. The tail is the pseudo node that marks the boundary of the
        # tail, same as that the head node is a pseudo node that marks the head. The doubly-linked list can be
        # represented as head (pseudo) <--> head <--> ....tail <--> tail (pseudo).
        # By adding two pseudo nodes to mark the boundaries, we could reduce the boundary checking code such as
        # if (head != null), making the code more concise and also more efficient.
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key):
        if key not in self.nodes:
            return -1
        node = self.nodes[key]
        self.remove(key)  # The node is now most recently accessed, so remove it ..
        self.add(key, node.val)  # and place it right before the dummy tail
        return node.val

    def put(self, key, value):
        if key in self.nodes:  # If the key already exists, then this is essentially an update
            self.remove(key)  # The node is now most recently accessed, so remove it
        self.add(key, value)
        if self.size > self.capacity:
            lru = self.head.next
            self.remove(lru)

    def remove(self, key):
        node = self.nodes[key]
        node.prev.next = node.next
        node.next.prev = node.prev
        del self.nodes[key]
        self.size -= 1

    def add(self, key, value):
        node = Node(key, value)
        node.next = self.head.next
        node.prev = self.head
        node.next.prev = node
        self.head.next = node
        self.nodes[key] = node
        self.size += 1
        if self.size > self.capacity:  # If max capacity reached, delete the LRU node: the one before the dummy tail
            lru = self.tail.prev
            self.remove(lru.key)


class LRUCacheV2(object):
    """ We're asked to implement the structure which provides the following operations in O(1) time:

            Get the key / Check if the key exists
            Put the key
            Delete the first added key

        The first two operations in O(1) time are provided by the standard hash map, and the last one by linked list.

        We can maintain a separate queue of keys. In the hash table, we store for each key a reference to its location
        in the queue. Each time an item is looked up and is found in the hash table, it is moved to the front of the
        queue. (This requires us to use a linked list implementation of the queue, so that items in the middle of the
        queue can be moved to the head). When the length of the queue exceeds the capacity, when a new element is added
        to the cache, the item at the tail of the queue is deleted from the cache, i.e., from the queue and the hash
        table.

        There is a structure called Ordered Dictionary which combines behind the scenes both hash map and linked list.
        In Python, this structure is called OrderedDict.

        Things to keep in mind:

        - put: Whenever we are putting a key-value pair in, we have to check whether the key already exists.
            - If it exists, we get that key-value pair, update the value and put that pair at the end of the cache.
            - If the key does not exist, we check whether the cache size is already at limit.
                - If the cache size is at limit, pop the key-value pair at the beginning of the cache and push the
                  new key-value pair at the end of the cache.
                - If the cache is still below size limit, simply push the new key-value pair at the end of the cache.

        - get: Whenever we are getting the value of the key, check whether the key exists in the cache.
            - If it exists, put that key-value pair at the end of the cache and return the value.
            - If it does not exist, return -1.
    """

    def __init__(self, capacity):
        self.nodes = OrderedDict()
        self.capacity = capacity
        self.size = 0

    def get(self, key):
        """ When an element is accessed, that makes it a recently used element, so we need to pop and place it again.
        """
        if key not in self.nodes:
            return -1
        val = self.nodes.pop(key)  # Remove the element ..
        self.nodes[key] = val  # and put it back to produce a new order in the dict
        return val

    def put(self, key, value):
        if key in self.nodes:  # If key already exists, then this is essentially an update
            self.nodes.pop(key)
        elif self.size == self.capacity:  # Max capacity reached
            self.nodes.popitem(last=False)  # The popitem() method for ordered dictionaries returns and removes a
            # (key, value) pair. The pairs are returned in a LIFO order if last=true and FIFO order if last=false.
            # Here, last=False means the first element in (least recently used) will be popped.
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
