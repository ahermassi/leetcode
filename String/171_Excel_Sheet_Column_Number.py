""" Given a column title as appear in an Excel sheet, return its corresponding column number.
For example:
    A -> 1
    B -> 2
    C -> 3
    ...
    Z -> 26
    AA -> 27
    AB -> 28
    ...
"""

import unittest2 as unittest


def title_to_number(s):
    """ Think of this problem as the same way we'd manually take a binary string and calculate its decimal value.
        Instead of being base 2, it is base 26.
        For every additional digit of the string, we multiply the value of the digit by 26^n where n is the number of
        digits it is away from the one's place. This is similar to how the number 254 could be broken down as:
        (2 x 10 x 10) + (5 x 10) + (4). The reason we use 26 instead of 10 is because 26 is our base.
        For s = 'BCM' the final solution would be (2 x 26 x 26) + (3 x 26) + (13)
        We could do this process iteratively. Start by looking at the first character 'B'. Add the int equivalent of
        'B' to the running sum and continue. Every time we look at the following character, we multiply our running sum
        by 26 before adding the next digit to signify we are changing places. Example below:
            'B' = 2
            'BC' = 2 * 26 + 3
            'BCM' = (2 * 26 + 3) * 26 + 13
    Time complexity: O(N), where N is the length of string
    Space complexity: O(1)
    """
    res = 0
    for c in s:
        res = res * 26 + ord(c) - ord('A') + 1
    return res


class Test(unittest.TestCase):
    data = [('A', 1), ('AB', 28), ('ZY', 701)]

    def test_title_to_number(self):
        for test_s, result in self.data:
            self.assertEqual(result, title_to_number(test_s))


if __name__ == '__main__':
    unittest.main()