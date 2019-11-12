""" Given a roman numeral, convert it to an integer.  """

import unittest2 as unittest


def roman_to_int(s):
    """ If one letter is less than its latter one, this letter is subtracted.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    roman_to_integer = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    res = 0
    for i in range(len(s) - 1):
        c, nxt = s[i], s[i + 1]
        if roman_to_integer[c] < roman_to_integer[nxt]:
            res -= roman_to_integer[c]
        else:
            res += roman_to_integer[c]
    res += roman_to_integer[s[-1]]  # Don't forget to add the last letter anyway as the loop stops at index len(s)-1
    return res


class Test(unittest.TestCase):
    data = [
        (3, 'III'),
        (4, 'IV'),
        (9, 'IX'),
        (58, 'LVIII'),
        (1994, 'MCMXCIV')
    ]

    def test_roman_to_int(self):
        for result, test_string in self.data:
            self.assertEqual(result, roman_to_int(test_string))
            self.assertEqual(result, roman_to_int(test_string))


if __name__ == '__main__':
    unittest.main()
