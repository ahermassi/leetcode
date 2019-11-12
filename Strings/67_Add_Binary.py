""" Given two binary strings, return their sum (also a binary string).
The input strings are both non-empty and contains only characters 1 or 0. """

import unittest2 as unittest


def add_binary(a, b):
    """ Check out 415_Add_Strings. Same logic.
    Time complexity: O(max(N, M)) where N is the length of a and M is the length of b
    Space complexity: O(max(N, M))
    """
    a, b = list(a), list(b)
    res, carry = [], 0
    while a or b:
        val1 = ord(a.pop()) - ord('0') if a else 0
        val2 = ord(b.pop()) - ord('0') if b else 0
        val = val1 + val2 + carry
        res.append(str(val % 2))
        carry = val // 2
    if carry:
        res.append(str(carry))
    return ''.join(res)[::-1]


class Test(unittest.TestCase):
    data = [('11', '1', '100'),
            ('1010', '1011', '10101')
            ]

    def test_add_binary(self):
        for test_num1, test_num2, result in self.data:
            self.assertEqual(result, add_binary(test_num1, test_num2))


if __name__ == '__main__':
    unittest.main()