""" Design and implement a data structure for Least Recently Used (LRU) cache. It should support the following
operations: get and put.
get(key) - Get the value (will always be positive) of the key if the key exists in the cache, otherwise return -1.
put(key, value) - Set or insert the value if the key is not already present. When the cache reached its capacity, it
should invalidate the least recently used item before inserting a new item.
The cache is initialized with a positive capacity. """

from collections import OrderedDict
import unittest2 as unittest


# Video explanation: https://www.youtube.com/watch?v=S6IfqDXWa10
# Video explanation: https://youtu.be/7ABFKPK2hD4
class Node:
    def __init__(self, key, val):
        # We have to store the key because we need to know a key when we remove a node from the map. Otherwise, for each
        # remove operation we would need to scan the entire map.
        self.key = key
        self.val = val
        self.next = None
        self.prev = None


class LRUCacheV1(object):
    """ The description of the put method states that we are storing key-value pairs. This means the data structure is
         similar to a hashmap, which also stores key-value pairs.

         It's easy to add new key-value pairs or update existing ones using a hashmap. The thing that makes this problem
         tricky is that the hashmap has a limited capacity. When the hashmap exceeds this capacity, we cannot
         arbitrarily remove a key - we need to remove the least recently used one. After we remove it, we need to know
         what the second least recently used one was (as it will be the next one to be deleted).

         To keep the order in which keys have been used, we can implement a queue. The key at the front of the queue is
         the most recently used key, and the key at the back of the queue is least recently used key. When we insert a
         key for the first time, we put it in the front of the queue. When we use an existing key (with either get or
         put), we locate it in the queue and move it to the front. If the data structure exceeds capacity, we can
         reference the back of the queue to find the key that should be deleted.

         If we use an array/list to implement the queue, operations will cost O(N). This is because we will frequently
         be removing elements from arbitrary positions in the list, which costs O(N).

         We need a way to implement this queue such that the operations will run in O(1). We need a way to store data
         in an ordered manner such that elements can be removed from any position in constant time.

         A linked list is a great candidate for this task. Removing from arbitrary positions is one of the few things
         that a linked list does better than an array. In general, if we want to remove a node from the list, we need a
         pointer to the node before it. Because of this, we shall use a doubly linked list.

        The problem can be solved with a hashmap that keeps track of the keys and its values in the doubly-linked list.
        That results in O(1) time for put and get operations and allows to remove the first added node in O(1) time as
        well. As each node represents an element in the data structure, we can also store the key-value pair in each
        node.

        One advantage of doubly-linked list is that the node can remove itself without other reference. In addition, it
        takes constant time to add and remove nodes from the head or tail.

        In a singly-linked list, we would also need a reference to the node before the one we want to remove.
        Therefore, if we were using a singly-linked list, we wouldn't be able to remove a node we retrieved from the
        hashmap in O(1) time because we don't have a reference to the one before it. By using a doubly-linked list,
        we can retrieve a node from the hashmap in O(1) and then remove the node itself from the list in O(1), giving
        the entire operation an O(1) running time.

        One particularity about the doubly-linked list implemented here is that there are dummy head and dummy tail to
        mark the boundaries, so that we don't need to check the null node during the update. The "real" head will be
        head.next and the "real" tail will be tail.prev. These dummy nodes sit just "outside" of the linked list.
        What is the purpose? We never want head or tail to be null.

        It's true that we can remove a node from a doubly linked list at any position in O(1) - but only if we already
        have a reference to the node. Given a key, how can we find the node associated with it in O(1)?
        In the hashmap, instead of mapping each key to its value, let's have it map each key to its associated node.

        Rules:
            1- Always add a new node AFTER the dummy head: this is the most recently used
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
    Space complexity: O(capacity)
    """

    def __init__(self, capacity):
        self.nodes = {}  # (Node.key: Node) pairs
        self.capacity = capacity
        self.size = 0
        # Dummy head and tail nodes to avoid null states. The tail is the pseudo node that marks the boundary of the
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
        self.remove(node)  # The node is now most recently accessed, so remove it ..
        self.insert(node)  # and place it right after the dummy head
        return node.val

    def put(self, key, value):
        if key in self.nodes:  # If the key already exists, then this is essentially an update
            self.remove(self.nodes[key])  # The node is now most recently accessed, so remove it
        node = Node(key, value)
        self.insert(node)

    def insert(self, node):
        node.next = self.head.next
        node.prev = self.head
        node.next.prev = node
        self.head.next = node
        self.nodes[node.key] = node
        self.size += 1
        if self.size > self.capacity:
            # If max capacity reached, delete the LRU node: the one before the dummy tail
            lru = self.tail.prev
            self.remove(lru)

    def remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
        del self.nodes[node.key]
        self.size -= 1


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
