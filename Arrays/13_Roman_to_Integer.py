""" Given a roman numeral, convert it to an integer.  """

import unittest2 as unittest


def roman_to_int_v1(s):
    """ Most intuitive approach.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    roman = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    sum = 0
    i = 0
    while i < len(s):
        c = s[i]
        if i + 1 < len(s) and (c == 'I' and s[i + 1] in {'V', 'X'} or
                               c == 'X' and s[i + 1] in {'L', 'C'} or
                               c == 'C' and s[i + 1] in {'D', 'M'}):
                sum = sum + roman[s[i + 1]] - roman[c]
                i += 2
        else:
            sum += roman[c]
            i += 1
    return sum


def roman_to_int_v2(s):
    """ If one letter is less than its latter one, this letter is subtracted.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    roman = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    sum = 0
    for i in range(len(s)):
        c = s[i]
        next = s[i + 1: i + 2]
        if next and roman[next] > roman[c]:
            sum -= roman[c]
        else:
            sum += roman[c]
    return sum


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
            self.assertEqual(result, roman_to_int_v1(test_string))
            self.assertEqual(result, roman_to_int_v2(test_string))


if __name__ == '__main__':
    unittest.main()
