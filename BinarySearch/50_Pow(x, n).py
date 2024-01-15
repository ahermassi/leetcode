""" Implement pow(x, n), which calculates x raised to the power n (xn). """

import unittest2 as unittest


# Video explanation: https://youtu.be/g9YQyYi4IQQ
def my_pow_v1(x, n):
    """ Recursive Fast Power.

         We know (x^n) means we multiply x with itself n-times. The most naive way to solve this problem is to simply
         multiply x n-times. This method of multiplying will lead to a linear time complexity and is not efficient.

         Assuming we have the result of (x^n), how can we get (x^2n) ? Obviously, we do not need to multiply x for
         another n times. Using the formula (x^n)^2 = x^2n, we can get (x^2n) at the cost of only one computation.

         Using this optimization, we can reduce the time complexity of the algorithm.

            - If n is even, x^2n = x^n * x^n

            - If n is odd, x^2n = x * x^n * x^n

        This approach can be easily implemented using recursion. We call this method 'Fast Power' or
        'Binary Exponentiation', because we only need at most O(log n) computations to get (x^n).

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

    Time complexity: O(log n), each time we apply the formula (x ^ n) ^ 2 = x ^ 2n, n is reduced by half. Thus, we
    need at most O(log n) computations to get the result
    Space complexity: O(log n), used by the recursive call stack
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
        be b_1, b_2, ..., b_k, from the Least Significant Bit (LSB) to the Most Significant Bit (MSB).

        For the ith bit, if b_i = 1 it means we need to multiply the result by x ^ 2i.

        Using the formula (x ^ n) ^ 2 = x ^ 2n, initially x ^ 1 = x, and for each i > 1, we can use the result
        of x ^ (2 ^ (i - 1)) to get x ^ 2i in one step. After that, for every i that satisfies b_i = 1, we can
        multiply x ^ (2 ^ i) to the result.

        For example, let's say n = 9 = 2 ^ 3 + 2 ^ 0 = 1001 in binary. Then:
        x ^ 9 = x ^ (2 ^ 3 + 2 ^ 0) = x ^ (2 ^ 3) * x ^ (2 ^ 0)

        We can see that every time we encounter a 1 in the binary representation of n, we need to multiply the answer
        by x ^ (2 ^ i), where i is the ith bit of the exponent. Thus, we can keep a running total of repeatedly
        squaring x - (x, x ^ 2, x ^ 4, x ^ 8, etc) and multiply it by the answer when we see a 1 in the binary
        representation of n.

        In other words, for each bit that is right shifted, x becomes square of itself. And for
        each bit, the result is multiplied by x only if the bit is turned on.

        Let's assume that n =13, so we can say pow(x, 13) == pow(x, 1) * pow(x, 4) * pow(x, 8).
        Looks familiar? We basically decomposed 13 in its binary digits (1101).
        Okay, then: why would we care? Because that is how a computer efficiently gets powers: at each step we multiply
        x by itself, so we will get x(^1), x^2, x^4, x^8, x^16 and so on.

        Starting to see the bits of the puzzle coming together now? We can decompose n as a binary number and then keep
        multiplying for x raised to some power of 2 value as we go along and - boom, the magic is done!

        Example: x = 2, n = 10
                                    res               = 1,          x = 2,      n = 10
        n % 2 == 1 ? No;  res               = 1,          x = 4,      n = 5
        n % 2 == 1 ? Yes; res = 1 * 4   = 4,          x = 16,    n = 2
        n % 2 == 0 ? No;  res               = 4,          x = 256,  n = 1
        n % 2 == 1 ? Yes; res = 4 * 256 = 1024,  x = - ,     n = 0

    Time complexity: O(log n)
    Space complexity: O(1)
    """
    if n < 0:
        x, n = 1 / x, -n
    res = 1
    while n:
        if n & 1 == 1:  # n & 1 gets the value of the least significant bit of n.
            # n = 100101, n & 1 = 1  ;  n = 100100, n & 1 = 0
            res *= x
        x *= x
        n /= 2
    return res


class Test(unittest.TestCase):
    data = [(2.00000, 10, 1024.00000), (2.10000, 3, 9.261000000000001), (2.00000, -2, 0.25000)]

    def test_my_pow(self):
        for test_x, test_n, result in self.data:
            self.assertEqual(result, my_pow_v1(test_x, test_n))
            self.assertEqual(result, my_pow_v2(test_x, test_n))


if __name__ == '__main__':
    unittest.main()
