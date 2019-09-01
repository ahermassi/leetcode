""" Implement strStr().
Return the index of the first occurrence of needle in haystack, or -1 if needle is not part of haystack. """

import unittest2 as unittest


def str_str(haystack, needle):
    """ Standard search. Linearly scan haystack. Pay attention to the boundaries of the search range: 0 .. n - m + 1, as
    it is useless to go beyond haystack[n - m] considering needle's size is m.
    Time complexity: O(N * M) where N is the length of haystack and M is the length of needle
    Space complexity: O(1)
    """
    if not needle:
        return 0
    n, m = len(haystack), len(needle)
    for i in range(n - m + 1):
        c = haystack[i]
        if c == needle[0] and haystack[i: i + m] == needle:
            return i
    return -1


class Test(unittest.TestCase):
    data = [('hello', 'll', 2), ('aaaaa', 'bba', -1)]

    def test_str_str(self):
        for test_haystack, test_needle, result in self.data:
            self.assertEqual(result, str_str(test_haystack, test_needle))


if __name__ == '__main__':
    unittest.main()