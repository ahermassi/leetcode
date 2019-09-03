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
        is O(n).
        For this reason, we use a dictionary to just keep track of the index of the added elements, so when we remove
        them, we copy the last one into it. An array/list holds the inserted values.
        This way, we achieve average O(1) for insert, remove, and getRandom.
    """

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.indexes = {}
        self.nums = []

    def insert(self, val):
        """
        Inserts a value to the set. Returns true if the set did not already contain the specified element.
        :type val: int
        :rtype: bool
        """
        if val in self.indexes:
            return False
        self.nums.append(val)
        self.indexes[val] = len(self.nums) - 1  # Insert value along with its index in nums list
        return True

    def remove(self, val):
        """
        Removes a value from the set. Returns true if the set contained the specified element.
        :type val: int
        :rtype: bool
        """
        if val not in self.indexes:
            return False
        index = self.indexes[val]  # Get val index in list
        last = self.nums[-1]  # Get the last added element
        self.nums[index] = last  # Overwrite val index with last element
        self.nums.pop()  # Get rid of the last element from it's original spot. It now has a new home elsewhere
        self.indexes[last] = index  # Update the last element's index to its new spot
        del self.indexes[val]  # Delete value along with its index from the dictionary
        return True

    def getRandom(self):
        """
        Get a random element from the set.
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

    def test_level_order(self):
        self.assertTrue(self.param_1)
        self.assertFalse(self.param_2)
        self.assertTrue(self.param_4)
        self.assertTrue(self.param_5)
        self.assertEqual(2, self.param_6)


if __name__ == '__main__':
    unittest.main()