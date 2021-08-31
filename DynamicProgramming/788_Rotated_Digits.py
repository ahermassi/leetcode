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


def rotated_digits_v3(n):
    """ Dynamic Programming.
        The point is to reduce calculating the same sub problems. In brute force, if n = 112, we need to judge digit by
        digit for n = 1 to n = 112. However, the same pattern like 11 is actually re-calculated because we already
        processed n = 11 and know it's not a good number. In this solution, n = 112 is split into 2 sub-problems,
        x = 11 and y = 2, and since these two sub-problems have already been calculated, we can deduce the answer for
        n = 112.
        We use the following notations:
        dp[i] = 0, if i is an invalid number (so it's not good)
        dp[i] = 1, if i is a valid number but rotates to itself (so it's not good)
        dp[i] = 2, if i is a good number
    Time complexity: O(N)
    Space complexity: O(N)
    """
    dp = [0] * (n + 1)
    res = 0
    for i in range(n + 1):
        if i < 10:
            if i in {0, 1, 8}:
                dp[i] = 1
            elif i in {2, 5, 6, 9}:
                dp[i] = 2
                res += 1
        else:
            part_one, part_two = dp[i // 10], dp[i % 10]
            if part_one == part_two == 1:
                dp[i] = 1
            elif part_one * part_two in {2, 4}:  # Either or both of the two parts is/are equal to 2
                dp[i] = 2
                res += 1
    return res


class Test(unittest.TestCase):

    def test_rotated_digits(self):
        self.assertEqual(4, rotated_digits_v1(10))
        self.assertEqual(4, rotated_digits_v2(10))
        self.assertEqual(4, rotated_digits_v3(10))


if __name__ == '__main__':
    unittest.main()