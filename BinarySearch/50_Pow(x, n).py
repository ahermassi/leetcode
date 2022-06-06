""" Implement pow(x, n), which calculates x raised to the power n (xn). """

import unittest2 as unittest


def my_pow_v1(x, n):
    """ Assuming we have got the result of (x^n), how can we get (x^2n) ? Obviously, we do not need to multiply x
        for another n times. Using the formula (x^n)^2 = x^2n, we can get (x^2n) at the cost of only one computation.

        Using this optimization, we can reduce the time complexity of our algorithm.

            - If n is even, x^2n = x^n * x^n

            - If n is odd, x^2n = x * x^n * x^n

        This approach can be easily implemented using recursion. We call this method 'Fast Power', because we only need
        at most O(log n) computations to get (x^n).

        Example: x = 5, n = 100
        x^100 = x^50 * x^50 = x^(50*2)
        x^50 = x^25 * x^25 = x^(25*2)
        x^25 = x * x^12 * x^12 = x * x^(12*2)
        x^12 = x^6 * x^6 = x^(6*2)
        x^6 = x^3 * x^3 = x^(3*2)
        x^3 = x * x^1 * x^1 = x * x^(1*2)
        x^1 = x * x^0 * x^0 = x * x^(0*2)
        x^0 = 1: base case
        So we went from calculating x^100 to: 100 -> 50 -> 25 -> 12 -> 6 -> 3 -> 1 -> 0, giving log n time complexity.

    Time complexity: O(log n), each time we apply the formula (x ^ n) ^ 2 = x ^ 2n, n is reduced by half. Thus we
    need at most O(log n) computations to get the result
    Space complexity: O(log n)
    """

    def get_power(x, n):
        if n == 0:
            return 1
        half_power = get_power(x, n // 2)
        if n % 2 == 0:
            return half_power * half_power
        return x * half_power * half_power

    if n < 0:
        x, n = 1/x, -n
    return get_power(x, n)


def my_pow_v2(x, n):
    """ Iterative Fast Power.
        We can use the binary representation of n to better understand the problem. Let the binary representation of n
        to be b_1, b_2, ..., b_k, from the Least Significant Bit (LSB) to the Most Significant Bit(MSB). For the ith
        bit, if b_i = 1, it means we need to multiply the result by x ^ {2 ^ i}.
        Using the formula (x ^ n) ^ 2 = x ^ {2 * n}, initially x ^ 1 = x, and for each i > 1, we can use the result
        of x ^ {2 ^ {i - 1}} to get x ^ {2 ^ i} in one step. After that, for every i that satisfies b_i = 1, we can
        multiply x ^ {2 ^ i} to the result.
        For example, let's say n = 9 = 2 ^ 3 + 2 ^ 0 = 1001 in binary. Then:
        x ^ 9 = x ^ (2 ^ 3 + 2 ^ 0) = x ^ (2 ^ 3) * x ^ (2 ^ 0)
        We can see that every time we encounter a 1 in the binary representation of n, we need to multiply the answer
        with x ^ (2 ^ i), where i is the ith bit of the exponent. Thus, we can keep a running total of repeatedly
        squaring x - (x, x ^ 2, x ^ 4, x ^ 8, etc) and multiply it by the answer when we see a 1 in the binary
        representation of n. In other words, for each bit that is right shifted, x becomes square of itself. And for
        each bit, the result is multiplied by x only if the bit is turned on.
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
        if n & 1 == 1:  # n & 1 gets the the value of the least significant bit of n.
            # n = 100101, n & 1 = 1  ;  n = 100100, n & 1 = 0
            res *= x
        x *= x
        n = n >> 1
        # Shifting by n bits to the right is equivalent to dividing by 2^n. So shifting by 1 bit to the right
        # is equivalent to dividing by 2.
        # Shifting by k bits to the right brings the kth bit to the rightmost index (k is 0-based). So shifting by
        # 1 bit to the right brings the bit at index 1 (next bit) to the rightmost index
    return res


class Test(unittest.TestCase):
    data = [(2.00000, 10, 1024.00000), (2.10000, 3, 9.261000000000001), (2.00000, -2, 0.25000)]

    def test_my_pow(self):
        for test_x, test_n, result in self.data:
            self.assertEqual(result, my_pow_v1(test_x, test_n))
            self.assertEqual(result, my_pow_v2(test_x, test_n))


if __name__ == '__main__':
    unittest.main()
