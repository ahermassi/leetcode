""" Implement atoi which converts a string to an integer.

The function first discards as many whitespace characters as necessary until the first non-whitespace character is
found. Then, starting from this character, takes an optional initial plus or minus sign followed by as many numerical
digits as possible, and interprets them as a numerical value. """

import unittest2 as unittest


def my_atoi(str):
    """ Pretty straightforward. Be careful handling the overflow towards the end.
    Time complexity: O(N) where N is the length of the string
    Space complexity: O(1)
    """
    neg, i, res, n = False, 0, 0, len(str)
    while i < n and str[i].isspace():  # Discard left whitespaces
        i += 1
    if i == n or (not str[i].isdigit() and str[i] not in '+-'):
        return 0
    # Handling pos/neg sign
    if str[i] == '-':
        neg = True
        i += 1
    elif str[i] == '+':
        i += 1
    while i < n and str[i].isdigit():  # Actual conversion to int
        res = res * 10 + (ord(str[i]) - ord('0'))  # ord() is faster than int()
        i += 1
    if neg:
        res = -res
    return min(max(res, -2147483648), 2147483647)  # Handling overflow. max(res, -2147483648) prevents from going
    # below Integer.MIN_VALUE; outer min() prevents from going beyond Integer.MAX_VALUE


class Test(unittest.TestCase):
    data = [('42', 42), ('   -42', -42), ('4193 with words', 4193), ('words and 987', 0), ('-91283472332', -2147483648)]

    def test_my_atoi(self):
        for test_string, result in self.data:
            self.assertEqual(result, my_atoi(test_string))


if __name__ == '__main__':
    unittest.main()