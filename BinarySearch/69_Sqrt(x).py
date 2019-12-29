""" Compute and return the square root of x, where x is guaranteed to be a non-negative integer.
Since the return type is an integer, the decimal digits are truncated and only the integer part of the result is returned.
"""

import unittest2 as unittest


def my_sqrt(x):
    """ The value a we're supposed to compute could be defined as: a^2 <= x < (a + 1)^2
        For x ≥ 2, the square root is always smaller than or equal to x and larger than 0 : 1 < a < x/2
        Use binary search to find an approximation of the two integers that the sqrt falls between.
    Time complexity: O(log x)
    Space complexity: O(1)
    """
    if x <= 1:
        return x
    left, right = 1, x
    while left <= right:
        mid = (left + right) // 2
        if mid ** 2 <= x < (mid + 1) ** 2:
            return mid
        if mid ** 2 > x:
            right = mid - 1
        else:
            left = mid + 1


class Test(unittest.TestCase):
    data = [(4, 2), (8, 2)]

    def test_my_sqrt(self):
        for test_integer, result in self.data:
            self.assertEqual(result, my_sqrt(test_integer))


if __name__ == '__main__':
    unittest.main()