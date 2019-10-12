""" Given two integers dividend and divisor, divide two integers without using multiplication, division and mod
operator.
Return the count after dividing dividend by divisor.
The integer division should truncate toward zero. """

import unittest2 as unittest


def divide(dividend, divisor):
    """ The idea behind this problem is simple, the dividend consists of multi times of divisor:
        dividend = divisor * (2 ^ 0) * a0 + divisor * (2 ^ 1) * a1 + divisor * (2 ^ 2) * a2 + ...
        What we need to compute is a0 ... aN.
        A naive method is to repeatedly subtract divisor from dividend, until there is none enough left. Then the count
        of subtractions will be the answer. Yet this takes linear time and is thus slow. A better method is to subtract
        divisor in a more efficient way. We can subtract divisor, 2divisor, 4divisor, 8*divisor... Now the subtracting
        process only takes log-time.
        Since we only care about the how many abs(divisor) needed for abs(dividend), we should covert both integers
        into to positive first. Use of abs should be very careful, since dividend or divisor could be Integer.MIN_VALUE.
        Integer.MAX_VALUE =  2147483647
        Integer.MIN_VALUE = -2147483648
        --> abs(Integer.MIN_VALUE) will overflow
        Keep subtracting the new divisor 'substract' from the remaining left and then doubling 'substract'
        (substract += substract). if left < substract, start from the original divisor. Do this until left < divisor.
        For example, if we want to calculate (17/2)
            ans = 0
            17-2 ,ans += 1; left = 15, substract = divisor = 2, count = 1
            15-4 ,ans += 2; left =11, substract = 4, count = 2
            11-8 ,ans += 4; left = 3, substract = 8, count = 4
            3-2 ,ans += 1; left = 1, dividend = 3 < substract = 16 --> Rewind: substract = divisor = 2, count = 1
            ans = 8: dividend = left = 1 < divisor = 2, return
    Time complexity: O(log divisor)
    Space complexity: O(1)
    """
    positive = ((dividend > 0) is (divisor > 0))
    dividend, divisor = abs(dividend), abs(divisor)
    ans = 0
    while dividend >= divisor:
        substract, count = divisor, 1
        while dividend >= substract:
            dividend -= substract
            ans += count
            substract += substract
            count += count
    if not positive:
        return max(-ans, -2147483648)  # Dealing with case ans > Integer.MAX_VALUE
    return min(ans, 2147483647)


class Test(unittest.TestCase):
    data = [(10, 3, 3), (7, -3, -2)]

    def test_divide(self):
        for test_dividend, test_divisor, result in self.data:
            self.assertEqual(result, divide(test_dividend, test_divisor))


if __name__ == '__main__':
    unittest.main()