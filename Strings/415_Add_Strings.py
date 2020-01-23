""" Given two non-negative integers num1 and num2 represented as string, return the sum of num1 and num2.
You must not use any built-in BigInteger library or convert the inputs to integer directly.
"""

import unittest2 as unittest


def add_strings(num1, num2):
    """ The idea is to transform each input string to a list and start adding digits from right to left as in a normal
        mathematical addition. The trick is to use ord() function to find the numerical value of a string digit.
    Time complexity: O(max(N, M)), where N is the length of num1 and M is the length of num2
    Space complexity: O(max(N, M))
    """
    num1, num2 = list(num1), list(num2)
    carry, res = 0, []
    while num1 or num2 or carry:
        n1 = ord(num1.pop()) - ord('0') if num1 else 0
        n2 = ord(num2.pop()) - ord('0') if num2 else 0
        temp = n1 + n2 + carry
        res.append(temp % 10)
        carry = temp // 10
    return ''.join(str(i) for i in reversed(res))


class Test(unittest.TestCase):
    data = [('107', '15', '122'),
            ('9', '99', '108')
            ]

    def test_add_strings(self):
        for test_num1, test_num2, result in self.data:
            self.assertEqual(result, add_strings(test_num1, test_num2))


if __name__ == '__main__':
    unittest.main()
