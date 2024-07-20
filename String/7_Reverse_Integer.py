""" Given a 32-bit signed integer, reverse the digits of the integer. Note: Assume we are dealing with an environment
which could only store integers within the 32-bit signed integer range: [−231,  231 − 1]. For the purpose of this
problem, assume that your function returns 0 when the reversed integer overflows. """

import unittest2 as unittest


# Video explanation: https://www.youtube.com/watch?v=HAgLH58IgJQ
def reverse_v1(x):
    """" We can build up the reverse integer one digit at a time. While doing so, we can check beforehand
          whether appending another digit would cause overflow.

          We want to repeatedly "pop" the last digit off of x and "push" it to the back of the rev. In the end, rev will
          be the reverse of the x.

          However, this approach is dangerous, because the statement rev * 10+last_digit can cause overflow.
          Luckily, it is easy to check beforehand whether this statement would cause an overflow.

    Time complexity: O(log10 x)
    Space complexity: O(1)
    """
    # COOL trick to get the sign of x. [1,-1] is a list which has two elements, [x<0] works as an index, when false
    # it evaluates to 0 , when true to 1.
    sign = [1, -1][x < 0]
    rev = 0
    num = abs(x)
    while num:
        last_digit = num % 10
        if rev > (pow(2, 31) - last_digit) // 10:
            # Check if adding the last digit won't make the reversed number too big and overflow. We have to reverse the
            # operations we intend to perform from the absolute limit of the system, to determine the highest value that
            # rev could hold BEFORE applying them, to not go past the boundary.
            # If we check rev > pow(2, 31) AFTER adding the last digit, we've already overflown and will get an error.
            # rev * 10 + last_digit > pow(2, 31)
            # --> rev * 10 > pow(2, 31) - list_digit
            # --> rev > (pow(2, 31) - list_digit) // 10
            return 0
        rev = rev * 10 + last_digit
        num = num // 10
    return sign * rev


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
