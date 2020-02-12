""" Compute and return the square root of x, where x is guaranteed to be a non-negative integer.
Since the return type is an integer, the decimal digits are truncated and only the integer part of the result is returned.
"""

import unittest2 as unittest


def my_sqrt(x):
    """ The value a we're supposed to compute could be defined as: a^2 <= x < (a + 1)^2
        Looking carefully at the problem, it should be clear that it is wasteful to take unit-sized increments.
        For example, a^2 < x, then no number smaller than a can be the result, and if a^2 > x, then no number greater
        than or equal to a can be the result.
        This ability to eliminate large sets of possibilities is suggestive of binary search. Specifically, we can
        maintain an interval consisting of values whose squares are unclassified with respect to x, i.e., might be less
        than or greater than x.
        We initialize the interval to [0, x]. We compare the square of mid = (left + right) // 2 with x, and use the
        elimination rule to update the interval.
        If mid^2 > x, we know all numbers greater than or equal to mid have a square greater than x, so we update the
        candidate interval to [left, mid - 1].
        If mid^2 <= x, we know all integers less than or equal to mid have a square less than or equal to x. Therefore,
        we update the interval to [mid + 1, right].
        The algorithm terminates when the interval is empty, in which case every number less than left has a square
        less than or equal to x, and left's square is greater than x, so the result is left - 1, or right.
        For example, if x = 21, we initialize the interval to [0, 21].
        Now mid = (0 + 21) // 2 = 10. Since 10^2 > 21, we update the interval to [0, 9].
        Now mid = (0 + 9) // 2 = 4. Since 4^2 < 21, we update the interval to [5, 9].
        Now mid = (5 + 9) // 2 = 7. Since 7^2 > 21, we update the interval to [5, 6].
        Now mid = (5 + 6) // 2 = 5. Since 5^2 > 21, we update the interval to [5, 4].
        Now the right endpoint is less than the left endpoint, i.e., the interval is empty, so the result is 5 - 1 = 4,
        which is the value returned.
    Time complexity: O(log x)
    Space complexity: O(1)
    """
    left, right = 0, x
    while left <= right:  # Everything before left has square <= x, everything after right has square > x
        mid = (left + right) // 2
        mid_squared = mid * mid
        if mid_squared > x:
            right = mid - 1
        else:
            left = mid + 1
    return right  # The loop is stopped when left > right, and at this moment right * right <= x < left * left


class Test(unittest.TestCase):
    data = [(4, 2), (8, 2)]

    def test_my_sqrt(self):
        for test_integer, result in self.data:
            self.assertEqual(result, my_sqrt(test_integer))


if __name__ == '__main__':
    unittest.main()
