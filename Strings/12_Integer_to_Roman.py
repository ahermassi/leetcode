""" Given an integer, convert it to a roman numeral. """

import unittest2 as unittest


def int_to_roman(num):
    """ More concise but tricky solution. Because we construct the roman numeral largest to smallest from left to right,
        we use a decreasingly ordered mapping from decimals to roman symbols. We keep dividing the original number by
        the largest possible decimal and convert the division result to the corresponding roman symbol which we append
        to the final string, get the modulo and re-iterate.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    numerals = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    romans = ['M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I']
    res = ''
    for numeral, roman in zip(numerals, romans):
        res += (num // numeral) * roman
        num = num % numeral
    return res


class Test(unittest.TestCase):
    data = [
        (3, 'III'),
        (4, 'IV'),
        (9, 'IX'),
        (58, 'LVIII'),
        (1994, 'MCMXCIV')
    ]

    def test_int_to_roman(self):
        for test_int, result in self.data:
            self.assertEqual(result, int_to_roman(test_int))


if __name__ == '__main__':
    unittest.main()

