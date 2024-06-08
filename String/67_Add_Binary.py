""" Given two binary strings, return their sum (also a binary string).
The input strings are both non-empty and contains only characters 1 or 0. """

import unittest2 as unittest


# Video explanation: https://youtu.be/keuWJ47xG8g
def add_binary(a, b):
    """ Similar to 415_Add_Strings.

         The idea is to start adding digits from right to left as in a normal mathematical addition. The trick is to use
         ord() function to find the numerical value of a string digit.

         That's a good old classical algorithm, and there is no conversion from binary string to decimal and back here.

    Time complexity: O(max(N, M)), where N is the length of a and M is the length of b
    Space complexity: O(max(N, M))
    """
    i, j = len(a) - 1, len(b) - 1
    res, carry = [], 0
    while i >= 0 or j >= 0 or carry:
        digit_a = ord(a[i]) - ord('0') if i >= 0 else 0
        digit_b = ord(b[j]) - ord('0') if j >= 0 else 0
        val = digit_a + digit_b + carry
        res.append(str(val % 2))
        carry = val // 2
        i -= 1
        j -= 1
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
