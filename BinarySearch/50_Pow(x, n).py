""" Implement pow(x, n), which calculates x raised to the power n (xn). """

import unittest2 as unittest


def my_pow_v1(x, n):
    """ Assuming we have got the result of (x^n), how can we get (x^2n) ? Obviously, we do not need to multiply x
        for another n times. Using the formula (x^n)^2 = x^2n, we can get (x^2n) at the cost of only one computation.
        Using this optimization, we can reduce the time complexity of our algorithm.
        If n is even, x^2n = x^n * x^n
        If n is odd, x^2n = x * x^n * x^n
        This approach can be easily implemented using recursion. We call this method 'Fast Power', because we only need
        at most O(logn) computations to get (x^n).
        Example: x = 5, n = 100
        x^100 = x^50 * x^50 = x^(50*2)
        x^50 = x^25 * x^25 = x^(25*2)
        x^25 = x * x^12 * x^12 = x * x^(12*2)
        x^12 = x^6 * x^6 = x^(6*2)
        x^6 = x^3 * x^3 = x^(3*2)
        x^3 = x * x^1 * x^1 = x * x^(1*2)
        x^1 = x * x^0 * x^0 = x * x^(0*2)
        x^0 = 1: base case
        So we went from calculating x^100 to: 100 -> 50 -> 25 -> 12 -> 6 -> 3 -> 1 -> 0, giving logn time complexity.
    Time complexity: O(logn), each time we apply the formula (x ^ n) ^ 2 = x ^ {2 * n}, n is reduced by half. Thus we
    need at most O(logn) computations to get the result
    Space complexity: O(logn)
    """

    def get_power(x, n):
        if n == 0:
            return 1
        half = get_power(x, n // 2)
        if n % 2 == 0:
            return half * half
        return x * half * half

    if n < 0:
        x, n = 1/x, -n
    return get_power(x, n)


def my_pow_v2(x, n):
    """ Iterative Fast Power.
        Example: x = 2, n = 10
                          res           = 1,    x = 2,   n = 10
        n % 2 == 1 ? No;  res           = 1,    x = 4,   n = 5
        n % 2 == 1 ? Yes; res = 1 * 4   = 4,    x = 16,  n = 2
        n % 2 == 0 ? No;  res           = 4,    x = 256, n = 1
        n % 2 == 1 ? Yes; res = 4 * 256 = 1024, x = - ,  n = 0
    Time complexity: O(logn)
    Space complexity: O(1)
    """
    if n < 0:
        x, n = 1 / x, -n
    res = 1
    while n:
        if n % 2 == 1:
            res *= x
        x *= x
        n //= 2
    return res


class Test(unittest.TestCase):
    data = [(2.00000, 10, 1024.00000), (2.10000, 3, 9.261000000000001), (2.00000, -2, 0.25000)]

    def test_my_pow(self):
        for test_x, test_n, result in self.data:
            self.assertEqual(result, my_pow_v1(test_x, test_n))


if __name__ == '__main__':
    unittest.main()
