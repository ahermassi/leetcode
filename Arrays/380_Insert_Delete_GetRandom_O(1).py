""" Design a data structure that supports all following operations in average O(1) time.

insert(val): Inserts an item val to the set if not already present.
remove(val): Removes an item val from the set if present.
getRandom: Returns a random element from current set of elements. Each element must have the same probability of being
returned. """

import random
import unittest2 as unittest


class RandomizedSet(object):
    """ When we store everything in a dictionary, it's fine when we insert or remove.
        But if we want to achieve O(1) on getRandom(), it's impossible. We have to turn it into a list first, which
        is O(N). The idea of GetRandom is to choose a random index and then to retrieve an element with that index.
        There is no indexes in hash map, and hence to get true random value, we have first to convert hash map keys
        into a list, and that would take linear time.
        For this reason, we use a dictionary to just keep track of the index of the added elements, so when we remove
        them, we copy the last one into it. An array/list holds the inserted values.
        To delete a value at arbitrary index takes linear time. The solution here is to always delete the last value:
            - Swap the element to delete with the last one.
            - Pop the last element out.
        For that, we have to compute the index of each element in constant time, and hence we need a hash map which
        stores element -> its index dictionary.
        Both ways converge into the same combination of data structures:
            - Hash map element -> its index.
            - List of elements.
        This way, we achieve average O(1) for insert, remove, and getRandom.
    """

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.indices = {}
        self.nums = []

    def insert(self, val):
        """
        Inserts a value to the set. Returns true if the set did not already contain the specified element.
        :type val: int
        :rtype: bool
        """
        if val in self.indices:
            return False
        self.nums.append(val)
        self.indices[val] = len(self.nums) - 1  # Insert value along with its index in nums list
        return True

    def remove(self, val):
        """
        Removes a value from the set. Returns true if the set contained the specified element.
        Retrieve an index of element to delete from the hash map.
        Move the last element to the place of the element to delete, O(1) time.
        Pop the last element out, O(1) time.
        """
        if val not in self.indices:
            return False
        index = self.indices[val]  # Get val index in list
        last = self.nums[-1]  # Get the last added element
        self.nums[index] = last  # Overwrite val index with last element
        self.nums.pop()  # Get rid of the last element from its original spot. It now has a new home elsewhere.
        self.indices[last] = index  # Update the last element's index to its new spot
        del self.indices[val]  # Delete value along with its index from the dictionary
        return True

    def getRandom(self):
        """
        Get a random element from the set.
        GetRandom could be implemented in O(1) time with the help of standard random.choice in Python.
        :rtype: int
        """
        return random.choice(self.nums)


class Test(unittest.TestCase):
    randomized_set = RandomizedSet()
    param_1 = randomized_set.insert(1)
    param_2 = randomized_set.remove(2)
    param_3 = randomized_set.getRandom()
    param_4 = randomized_set.insert(2)
    param_5 = randomized_set.remove(1)
    param_6 = randomized_set.getRandom()

    def test_randomized_set(self):
        self.assertTrue(self.param_1)
        self.assertFalse(self.param_2)
        self.assertTrue(self.param_4)
        self.assertTrue(self.param_5)
        self.assertEqual(2, self.param_6)


if __name__ == '__main__':
    unittest.main()