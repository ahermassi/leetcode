""" Write a function that reverses a string. The input string is given as an array of characters char[].
Do not allocate extra space for another array, you must do this by modifying the input array in-place with O(1) extra
memory. """

import unittest2 as unittest


def reverse_string(s):
    """
    Time complexity: O(N)
    Space complexity: O(1)
    """
    s = list(s)
    i, j = 0, len(s) - 1
    while i <= j:
        s[i], s[j] = s[j], s[i]
        i += 1
        j -= 1
    return ''.join(s)


class Test(unittest.TestCase):
    data = [('Hello', 'olleH'), ('leetcode', 'edocteel')]

    def test_roman_to_int(self):
        for test_string, result in self.data:
            self.assertEqual(result, reverse_string(test_string))


if __name__ == '__main__':
    unittest.main()