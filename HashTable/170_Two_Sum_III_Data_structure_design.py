""" Design and implement a TwoSum class. It should support the following operations: add and find.
add - Add the number to an internal data structure.
find - Find if there exists any pair of numbers which sum is equal to the value. """

import unittest2 as unittest


class TwoSum(object):

    """ Good old hash table techniques. """

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.numbers = {}

    def add(self, number):
        """
        Add the number to an internal data structure..
        :type number: int
        :rtype: None
        """
        try:
            self.numbers[number] += 1
        except KeyError:
            self.numbers[number] = 1

    def find(self, value):
        """
        Find if there exists any pair of numbers which sum is equal to the value.
        :type value: int
        :rtype: bool
        """
        for i in self.numbers:
            # If the complement of i is found, it should be either not equal to i or that i was added more than once
            if value - i in self.numbers and (value - i != i or self.numbers[i] > 1):
                return True
        return False


class Test(unittest.TestCase):
    two_sum = TwoSum()
    two_sum.add(1)
    two_sum.add(3)
    two_sum.add(5)

    def test_two_sum(self):
        self.assertTrue(self.two_sum.find(4))
        self.assertFalse(self.two_sum.find(7))


if __name__ == '__main__':
    unittest.main()