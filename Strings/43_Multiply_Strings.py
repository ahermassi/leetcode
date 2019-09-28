""" Given two non-negative integers num1 and num2 represented as strings, return the product of num1 and num2,
also represented as a string. """

import unittest2 as unittest


def multiply_v1(num1, num2):
    """ Multiply each digit of num1 by num2. Sum the partial results. Exactly as humans do.
    Time complexity: O(N * M) where N is the length of num1 and M is the length of num2
    Space complexity: O(N + M)
    """
    res = []
    for c in num1[::-1]:
        s, carry, factor, acc = 0, 0, 1, 0
        for d in num2[::-1]:
            s = int(c) * int(d) + carry
            acc += (s % 10) * factor
            carry = s // 10
            factor *= 10
        if carry:
            acc += carry * factor
        res.append(acc)
    factor, ans = 1, 0
    for i in res:
        ans += i * factor
        factor *= 10
    return str(ans)


class Test(unittest.TestCase):
    data = [('2', '3', '6'), ('123', '456', '56088')]

    def test_multiply(self):
        for test_num1, test_num2, result in self.data:
            self.assertEqual(result, multiply_v1(test_num1, test_num2))


if __name__ == '__main__':
    unittest.main()
