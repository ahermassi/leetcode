""" Design a data structure that supports all following operations in average O(1) time.
insert(val): Inserts an item val to the set if not already present.
remove(val): Removes an item val from the set if present.
getRandom: Returns a random element from current set of elements. Each element must have the same probability of being
returned. """

import random
import unittest2 as unittest


# Video explanation: https://youtu.be/j4KwhBziOp
class RandomizedSet(object):
    """ Let's figure out how to implement such a structure. Starting from the Insert, we immediately have two good
         candidates with O(1) average insert time: hashmap (or hash set, the implementation is very similar), and array.

         Hashmap provides insert and delete in average constant time, but it has problems with get random.
         The idea of get random is to choose a random index and then retrieve an element with that index. There are no
         indexes in the hashmap, and hence to get a true random value, we have first to convert the hashmap keys to a
         list, which would take linear time. The solution here is to build a list of keys aside and use this list to
         compute get random in constant time.

        Arrays have indexes and could provide insert and get random in average constant time, but have problems with
        delete. Deleting a value at an arbitrary index takes linear time. The solution here is to always delete the
        last value:

            - Swap the element to delete with the last one
            - Pop the last element

        To do that, we have to compute the index of each element in constant time and hence we use a dictionary to
        keep track of the indices of the added elements.

        Both ways converge into the same combination of data structures:
            - Hash map element -> index
            - List of elements

        This way, we achieve average O(1) for insert, remove, and get random.
    """

    def __init__(self):
        self.indices = {}
        self.nums = []

    def insert(self, val):
        """ Inserts a value to the set. Returns true if the set did not already contain the specified element. """
        if val in self.indices:
            return False
        self.nums.append(val)
        self.indices[val] = len(self.nums) - 1  # Insert the value along with its index in nums list
        return True

    def remove(self, val):
        """ Removes a value from the set. Returns true if the set contained the specified element.
            Retrieve the index of element to delete from the hash map.
            Move the last element to the place of the element to delete, in O(1) time.
            Pop the last element, in O(1) time.
        """
        if val not in self.indices:
            return False
        # Essentially, we're going to move the last element in the list to the location of the element we want to
        # remove. This is a significantly more efficient operation than the obvious solution of removing the item and
        # shifting the values of every item iin the dictionary to match their new position in the list.
        index = self.indices[val]  # Get val index in the list
        last = self.nums[-1]  # Get the last added element
        self.nums[index] = last  # Overwrite val index with the last element
        self.nums.pop()  # Pop the last element. It now has a new home elsewhere.
        self.indices[last] = index  # Update the last element's index to its new spot
        del self.indices[val]  # Delete value along with its index from the dictionary
        return True

    def getRandom(self):
        """ Get a random element from the set.
            getRandom could be implemented in O(1) time with the help of standard random.choice in Python.
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
