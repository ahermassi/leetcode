""" Compute and return the square root of x, where x is guaranteed to be a non-negative integer.
Since the return type is an integer, the decimal digits are truncated and only the integer part of the result is returned.
"""

import unittest2 as unittest


# Video explanation: https://youtu.be/zdMhGxRWutQ
def my_sqrt(x):
    """ The value a that we're supposed to compute could be defined as:

                    a^2 <= x < (a + 1)^2

         Looking carefully at the problem, it should be clear that it is wasteful to take unit-sized increments.
         For example, if a^2 < x, then no number smaller than a can be the result. If a^2 > x, then no number greater
         than or equal to a can be the result.

        This ability to eliminate large sets of possibilities is suggestive of binary search. Specifically, we can
        maintain an interval consisting of values whose squares are unclassified with respect to x, i.e., might be less
        than or greater than x.

            - Initialize the interval to [0, x].

            - Compare the square of mid = (left + right) // 2 to x, and use the elimination rule to update the interval.

            - If mid^2 > x, we know that all numbers greater than or equal to mid have a square greater than x, so we
               update the candidates' interval to [left, mid - 1].

            - If mid^2 < x, we know that all integers less than or equal to mid have a square less than or equal to x.
               Therefore, we update the interval to [mid + 1, right].

        The algorithm terminates when left steps over right (or right steps over left), i.e. left == right+1, in which
        case every number less than left has a square less than x, and left's square is greater than x because
        left == right+1 , so the square root is left-1, or right.

        Why return right, or left-1?

        'mid' is returned whenever the square root of x is an integer. Otherwise, the square root of x has a remainder.
        In the latter case, the while loop terminates when left > right, at which point left will be the smallest
        integer greater than the square root of x (the ceiling) and right will be less than the square root of x (the
        floor). The solution requires truncation, so we return right as it is the floor.
        'right' is the largest integer value whose square is less than x, which is the closest possible approximation to
        the integer square root.

        !! IMPORTANT!!
        The algorithm tries to find the largest value of mid whose square is less than x IF x is not a perfect square.

        For example, if x = 21, we initialize the interval to [0, 21].
        mid = (0 + 21) // 2 = 10. Since 10^2 > 21, we update the interval to [0, 9].
        mid = (0 + 9) // 2 = 4. Since 4^2 < 21, we update the interval to [5, 9].
        mid = (5 + 9) // 2 = 7. Since 7^2 > 21, we update the interval to [5, 6].
        mid = (5 + 6) // 2 = 5. Since 5^2 > 21, we update the interval to [5, 4].
        Now the right endpoint is less than the left endpoint, i.e., the interval is empty, so the result is 5 - 1 = 4.

    Time complexity: O(log x)
    Space complexity: O(1)
    """
    left, right = 0, x
    while left <= right:
        # The algorithm's invariant: every number < 'left' has square < x, and every number > 'right' has square > x
        mid = (left + right) // 2
        mid_squared = mid * mid
        if mid_squared == x:
            return mid
        if mid_squared < x:
            left = mid + 1
        else:
            right = mid - 1
    # No exact integer square root is found within the range, i.e. the true square root is a floating point value
    # between 'left' and 'right', and we want to round it down to the smaller number out of the 2.
    # The loop exits when left > right, and at this moment right^2 < x < left^2
    return right


class Test(unittest.TestCase):
    data = [(4, 2), (8, 2)]

    def test_my_sqrt(self):
        for test_integer, result in self.data:
            self.assertEqual(result, my_sqrt(test_integer))


if __name__ == '__main__':
    unittest.main()
