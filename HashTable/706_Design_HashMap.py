""" Design a HashMap without using any built-in hash table libraries.
All keys and values will be in the range of [0, 1000000].
The number of operations will be in the range of [1, 10000].
Please do not use the built-in HashMap library.
"""

import unittest2 as unittest


class ListNode:
    def __init__(self, key, value):
        self.pair = (key, value)
        self.next = None


class MyHashMap(object):
    """ Simple implementation of Hash with chaining. """

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.size = 10000
        self.hash_map = [None] * self.size

    def put(self, key, value):
        """
        value will always be non-negative.
        :type key: int
        :type value: int
        :rtype: None
        """
        index = key % self.size  # This is our hash function
        if not self.hash_map[index]:
            self.hash_map[index] = ListNode(key, value)
        else:
            cur = self.hash_map[index]  # Iterate over the linked list to find the key
            while cur:
                if cur.pair[0] == key:
                    cur.pair = (key, value)  # Update existing pair
                    return
                if cur.next:
                    cur = cur.next
                else:
                    break
            cur.next = ListNode(key, value)  # If not found, create a new pair (node)

    def get(self, key):
        """
        Returns the value to which the specified key is mapped, or -1 if this map contains no mapping for the key
        :type key: int
        :rtype: int
        """
        index = key % self.size
        cur = self.hash_map[index]
        while cur:
            if cur.pair[0] == key:
                return cur.pair[1]
            cur = cur.next
        return -1

    def remove(self, key):
        """
        Removes the mapping of the specified value key if this map contains a mapping for the key
        :type key: int
        :rtype: None
        """
        index = key % self.size
        cur = prev = self.hash_map[index]
        if not cur:
            return
        if cur.pair[0] == key:
            self.hash_map[index] = cur.next
        else:
            cur = cur.next
            while cur:
                if cur.pair[0] == key:
                    prev.next = cur.next
                cur, prev = cur.next, prev.next


class Test(unittest.TestCase):
    hash_map = MyHashMap()
    hash_map.put(1, 1)
    hash_map.put(2, 2)
    one = hash_map.get(1)
    three = hash_map.get(3)
    hash_map.put(2, 1)
    two = hash_map.get(2)
    hash_map.remove(2)
    new_two = hash_map.get(2)

    def test_hashmap(self):
        self.assertEqual(1, self.one)
        self.assertEqual(-1, self.three)
        self.assertEqual(1, self.two)
        self.assertEqual(-1, self.new_two)


if __name__ == '__main__':
    unittest.main()
