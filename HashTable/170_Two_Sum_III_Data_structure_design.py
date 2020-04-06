""" Design and implement a TwoSum class. It should support the following operations: add and find.
add - Add the number to an internal data structure.
find - Find if there exists any pair of numbers which sum is equal to the value. """

from collections import defaultdict
import unittest2 as unittest


class TwoSum:
    """ We can employ a hash table to index each number. Given a desired sum value S, for each number a, we just need
        to verify if there exists a complement number (S - a) in the table.
        For the add(number) function, we build a frequency hash map with the number as key and the frequency of the
        number as the value.
        For the find(value) function, we iterate through the hashtable over the keys. For each key 'number', we check
        if there exists a complement (value - number) in the table. If so, we could terminate the loop and return the
        result. In a particular case, where the number and its complement are equal, we then need to check if there
        exists at least two copies of the number in the table.
    Time complexity: O(1) for add(number), O(N) for find(value) where N is the total number of unique numbers
    Space complexity: O(N), where N is the total number of unique numbers that we will see during the usage of the data
    structure
    """

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.numbers = defaultdict(int)

    def add(self, number: int) -> None:
        """
        Add the number to an internal data structure..
        """
        self.numbers[number] += 1

    def find(self, value: int) -> bool:
        """
        Find if there exists any pair of numbers which sum is equal to the value.
        """
        numbers = self.numbers
        for number, count in numbers.items():
            complement = value - number
            if complement in numbers and (complement != number or count > 1):
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