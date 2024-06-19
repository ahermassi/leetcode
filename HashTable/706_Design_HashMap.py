""" Design a HashMap without using any built-in hash table libraries. All keys and values will be in the range of
[0, 1000000]. The number of operations will be in the range of [1, 10000].
Please do not use the built-in HashMap library.
"""

import unittest2 as unittest


class ListNode:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.next = None


# Video explanation: https://youtu.be/cNWsgbKwwoU
class MyHashMap(object):
    """ Simple implementation of hash with chaining.

        There are two main issues that we should tackle, in order to design an efficient hash map data structure:

            1- Hash function design: the purpose of hash function is to map a key value to an address in the storage
                 space. For a good hash function, it should map different keys evenly across the storage space, so that
                 we don't end up with the majority of the keys concentrated in a few spaces.

            2- Collision handling: essentially the hash function reduces the vast key space into a limited address
                 space. As a result, there could be the case where two different keys are mapped to the same address,
                 which is what we call 'collision'. Since the collision is inevitable, it is important that we have a
                 strategy to handle it.

        We could adopt the modulo operator as the hash function, since the key's value is of integer type. It's easy
        enough to mimic a key lookup if the keys themselves are integers that are constrained enough to act as their own
        indexes. But what if they're not? Or what if they're some other data type, like strings? In this case, we can
        use a hashing function to convert the key into an integer within the bounds of our hashmap array's index range.

        We organize the storage space as an array where each element is indexed with the output value of the hash
        function. In case of collision, where two different keys are mapped to the same address, we use a bucket to hold
        all the values. The bucket is a container that holds all the values that are assigned by the hash function to
        the same index. We can make each of the hashmap array's elements a linked list. This will allow us to treat them
        like a simple stack.

        Since navigating a linked list will drop our lookup time past O(1), the goal of a good hashing function is to
        randomize the keys' hashes enough to limit collisions as much as possible for a given hashmap array size, thus
        keeping down the average lookup time complexity.

        This localization process can be done in two steps:

            1- For a given key value, first apply the hash function to generate a hash key, which corresponds to the
              address in the main storage. With this hash key, we would find the bucket where the value should be
              stored.

            2- Now that we found the bucket, we simply iterate through the bucket to check if the desired key exists.

    Time complexity: O(N/k), where N is the number of all possible keys and k is the number of predefined buckets in the
    hashmap, which is 10000 in our case. In the worst case we need to iterate through an entire bucket to find the
    desired key.
    Space complexity: O(k + M), where k is the number of predefined buckets in the hashmap and M is the number of
    unique keys that have been inserted into the hashmap.
    """

    def __init__(self):
        self.size = 10000
        self.mapStorage = [None] * self.size

    def put(self, key, value):
        index = key % self.size
        cur = self.mapStorage[index]
        if not cur:
            # First entry at this index
            self.mapStorage[index] = ListNode(key, value)
        else:
            pre = None
            while cur and cur.key != key:
                pre, cur = cur, cur.next
            if not cur:
                # We're here because no node corresponds to the desired key, so we add a node to the tail of the list
                pre.next = ListNode(key, value)
            else:
                # We're here because the current node has the key we're searching for, so we update the node's value
                cur.val = value

    def get(self, key):
        """ We hash() the key, access the corresponding bucket in the hashmap array (data), and navigate through the
             linked list (if necessary) and return the correct value, or -1 if the key is not found.
        """
        index = key % self.size
        cur = self.mapStorage[index]
        while cur:
            if cur.key == key:
                return cur.val
            cur = cur.next
        return -1

    def remove(self, key):
        """ Removes the mapping of the specified value key if the map contains a mapping for the key """
        index = key % self.size
        cur = self.mapStorage[index]
        if not cur:
            return
        if cur.key == key:
            # The key to remove corresponds to the head of the list
            self.mapStorage[index] = cur.next
            return
        pre = None
        while cur and cur.key != key:
            pre, cur = cur, cur.next
        if cur:
            # We're here because the current node has the key we want to remove
            pre.next = cur.next


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
