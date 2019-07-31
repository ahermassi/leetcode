""" Write an algorithm to determine if a number is "happy".
A happy number is a number defined by the following process: Starting with any positive integer, replace the number by
the sum of the squares of its digits, and repeat the process until the number equals 1 (where it will stay), or it
loops endlessly in a cycle which does not include 1. Those numbers for which this process ends in 1 are happy numbers.
"""

import unittest2 as unittest


def is_happy(n):
    """ Keep a 'seen' set to record the numbers already visited in the process. Calculate the sum of squares of digits
        of the number until 1 is reached or result of calculation seen before.
    Time complexity: O(N) where N is the number of n digits
    Space complexity: O(N) ?
    """
    seen = set()
    while n != 1:
        n = sum([int(d) ** 2 for d in str(n)])
        if n in seen:
            return False
        seen.add(n)
    return True


class Test(unittest.TestCase):

    def test_is_happy(self):
        self.assertTrue(is_happy(19))


if __name__ == '__main__':
    unittest.main()