""" X is a good number if after rotating each digit individually by 180 degrees, we get a valid number that is
different from X.
Now given a positive number N, how many numbers X from 1 to N are good?
"""

import unittest2 as unittest


def rotated_digits_v1(n):
    """ If at least one of the digits is in {3, 4, 7} then the number is not good (these digits do not rotate).
        If at least one of the digits is in {2, 5, 6, 9} then the number is good (these digits rotate to different
        digits)
     Time complexity: O(N * L), where L is number of digits of the "longest" number
     Space complexity: O(1)
     """

    def is_good(num):
        good = False
        while num:
            digit = num % 10
            if digit in {3, 4, 7}:
                return False
            if digit in {2, 5, 6, 9}:
                good = True
            num /= 10
        return good

    count = 0
    for i in range(1, n + 1):
        if is_good(i):
            count += 1
    return count


def rotated_digits_v2(n):
    """ Same idea, simpler implementation but more space usage.
    Time complexity: O(N * L)
    Space complexity: O(L)
    """
    good = 0
    for i in range(1, n + 1):
        digits = str(i)
        if '3' in digits or '4' in digits or '7' in digits:
            continue
        if '2' in digits or '5' in digits or '6' in digits or '9' in digits:
            good += 1
    return good


class Test(unittest.TestCase):

    def test_rotated_digits(self):
        self.assertEqual(4, rotated_digits_v1(10))
        self.assertEqual(4, rotated_digits_v2(10))


if __name__ == '__main__':
    unittest.main()