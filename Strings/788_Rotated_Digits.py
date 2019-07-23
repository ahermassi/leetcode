""" X is a good number if after rotating each digit individually by 180 degrees, we get a valid number that is
different from X.
Now given a positive number N, how many numbers X from 1 to N are good?
"""

import unittest2 as unittest


def rotated_digits(N):
    """ If at least one of the digits is in {3, 4, 7} then the number is not good (these digits do not rotate)
     If at least one of the digits is in {2, 5, 6, 9} then the number is good (these digits rotate to different digits)
     Time complexity: O(N)
     Space complexity: O(1)
     """
    count = 0
    for i in range(1, N + 1):
        s = str(i)
        if all((d not in set('347') for d in s)) and any((d in set('2569') for d in s)):
            count += 1
    return count


class Test(unittest.TestCase):

    def test_rotated_digits(self):
        self.assertEqual(4, rotated_digits(10))


if __name__ == '__main__':
    unittest.main()