""" Implement pow(x, n), which calculates x raised to the power n (xn). """

import unittest2 as unittest


def my_pow_v1(x, n):
    """ Assuming we have got the result of x ^ n, how can we get x ^ 2n. Obviously we do not need to multiply x
        for another n times. Using the formula (x ^ n) ^ 2 = x ^ 2*n, we can get x ^ 2n at the cost of only one
        computation. Using this optimization, we can reduce the time complexity of our algorithm.
        If n is even, x ^ 2n = (x ^ n) * (x ^ n)
        If n is odd, x ^ 2n = x * (x ^ n) * (x ^ n)
        This approach can be easily implemented using recursion. We call this method "Fast Power", because we only need
        at most O(logn) computations to get x ^ n
    Time complexity: O(logn)
    Space complexity: O(logn)
    """

    def get_power(x, n):
        if n == 0:
            return 1
        half = get_power(x, n // 2)
        if n % 2 == 0:
            return half * half
        return x * half * half

    x = 1 / x if n < 0 else x
    n = -n if n < 0 else n
    return get_power(x, n)


class Test(unittest.TestCase):
    data = [(2.00000, 10, 1024.00000), (2.10000, 3, 9.261000000000001), (2.00000, -2, 0.25000)]

    def test_max_product(self):
        for test_x, test_n, result in self.data:
            self.assertEqual(result, my_pow_v1(test_x, test_n))


if __name__ == '__main__':
    unittest.main()