""" Given two integers dividend and divisor, divide two integers without using multiplication, division and mod
operator.
Return the count after dividing dividend by divisor.
The integer division should truncate toward zero. """

import unittest2 as unittest


def divide(dividend, divisor):
    """ The idea behind this problem is simple. The dividend consists of multi times of divisor:
        dividend = (a0 * divisor * 2^0) + (a1 * divisor * 2^1) + (a2 * divisor * 2^2) + ...
        What we need to compute is a0 ... aN.
        A naive method is to repeatedly subtract divisor from dividend, until there is none enough left. Then the count
        of subtractions will be the answer. Yet this takes linear time and is thus slow.
        A better method is to subtract divisor in a more efficient way. We can subtract 1 * divisor, 2 * divisor,
        4 * divisor, 8 * divisor... Now the subtracting process only takes log time.
        Since we only care about how many abs(divisor) needed for abs(dividend), we should convert both integers
        to positive first. Use of abs should be very careful, since dividend or divisor could be Integer.MIN_VALUE.
        Integer.MAX_VALUE = 2147483647
        Integer.MIN_VALUE = -2147483648
        --> abs(Integer.MIN_VALUE) will overflow
        Keep subtracting the new divisor 'subtract' from what remained of 'dividend' and then double 'subtract'
        (subtract += subtract). If dividend < subtract, start from the original divisor. Do this until
        dividend < divisor.
        For example, if we want to calculate (17/2): dividend = 17, divisor = 2
            res = 0
            17-2, res += 1; dividend(left) = 15, subtract = divisor = 2, count = 1
            15-4, res += 2; dividend(left) = 11, subtract = 4, count = 2
            11-8, res += 4; dividend(left) = 3, subtract = 8, count = 4
            dividend(left) = 3 < subtract = 16 -> Rewind: subtract = divisor = 2, count = 1, dividend = 3
            3-2, res += 1; dividend(left) = 1, subtract = 2, count = 1
            dividend(left) = 1 < subtract = 4 -> dividend(left) = 1 < divisor = 2
            -> res = 8,  return
    Time complexity: O(log divisor)
    Space complexity: O(1)
    """
    sign = [1, -1][(dividend < 0) ^ (divisor < 0)]
    dividend, divisor = abs(dividend), abs(divisor)
    res = 0
    while dividend >= divisor:
        subtract, count = divisor, 1  # 'count' meres how many 'subtract' is there in 1 'divisor'
        while dividend >= subtract:
            dividend -= subtract
            res += count  # In 1 'subtract' we count 1 'divisor', in 2 'subtract's we count 2 'divisor's, etc
            # Doubling down on 'subtract' leads to doubling down on 'count'. 'count' can be seen as a multiplication
            # factor among a0, a1,...aN
            subtract += subtract
            count += count
    res *= sign
    return min(max(res, -2147483648), 2147483647)


class Test(unittest.TestCase):
    data = [(10, 3, 3), (7, -3, -2)]

    def test_divide(self):
        for test_dividend, test_divisor, result in self.data:
            self.assertEqual(result, divide(test_dividend, test_divisor))


if __name__ == '__main__':
    unittest.main()
