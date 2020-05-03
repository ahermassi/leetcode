""" Given a 32-bit signed integer, reverse the digits of the integer. Note: Assume we are dealing with an environment
which could only store integers within the 32-bit signed integer range: [−231,  231 − 1]. For the purpose of this
problem, assume that your function returns 0 when the reversed integer overflows. """

import unittest2 as unittest


def reverse_v1(x):
    """" Same as in 9-Palindrome Number problem, reverse the integer using division operations. Pay attention to
         overflow cases (although INT doesn't overflow in Python, test had to be done to pass Leetcode's OJ).
    Time complexity: O(log10 x)
    Space complexity: O(1)
    """
    sign = [1, -1][x < 0]  # COOL trick to get the sign of x. [1,-1] is a list which has two elements, [x<0] works as
    # an index, when false it evaluates to 0 , when true to 1.
    rev, p = 0, abs(x)
    while p:
        rev = rev * 10 + p % 10
        p = p // 10
    return sign * rev if pow(-2, 31) <= rev <= pow(2, 31) else 0


def reverse_v2(x):
    """ This solution converts the integer to a string and then it reverses it.
    Time complexity: O(N) for string reversal
    Space complexity: O(N) for string allocation
    """
    sign = [1, -1][x < 0]
    res = sign * int(str(abs(x))[::-1])
    return res if pow(-2, 31) <= res <= pow(2, 31) else 0


class Test(unittest.TestCase):
    data = [(123, 321), (-123, -321), (120, 21)]

    def test_reverse(self):
        for test_number, result in self.data:
            self.assertEqual(result, reverse_v1(test_number))
            self.assertEqual(result, reverse_v2(test_number))


if __name__ == '__main__':
    unittest.main()
