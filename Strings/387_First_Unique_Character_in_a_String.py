""" Given a string, find the first non-repeating character in it and return it's index. If it doesn't exist,
return -1. """

import unittest2 as unittest


def first_uniq_char(s):
    """ The idea is to go through the string and save in a hash map the number of times each character appears in the
    string. And then we go through the string the second time, this time we use the hash map as a reference to check
    if a character is unique or not.
    Time complexity: O(N)
    Space complexity: O(1), if English alphabet is assumed the algorithm is iterating over a constant (26) number of
    bins as keys for hashmap.
    """
    chars = {}
    for i, ch in enumerate(s):
        try:
            chars[ch] += 1
        except KeyError:
            chars[ch] = 1
    for i, ch in enumerate(s):
        if chars[ch] == 1:
            return i
    return -1


class Test(unittest.TestCase):
    data = [('leetcode', 0),
            ('loveleetcode', 2)
            ]

    def test_first_uniq_char(self):
        for test_string, result in self.data:
            self.assertEqual(result, first_uniq_char(test_string))


if __name__ == '__main__':
    unittest.main()

