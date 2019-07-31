""" Given two strings s and t, determine if they are isomorphic.
Two strings are isomorphic if the characters in s can be replaced to get t.
All occurrences of a character must be replaced with another character while preserving the order of characters.
No two characters may map to the same character but a character may map to itself. """

from collections import defaultdict
import unittest2 as unittest


def is_isomorphic(s, t):
    """ Use two dictionaries d1 and d2. Every key/value pair in d1 is mapping a character in s to its corresponding
        character(s) in t. d2 is used for the exact opposite: to which character did a character in t map.
        When a character in t is found to map to more than one character in s OR a character in s maps to more than
        one character in t, the function returns False.
    Time complexity: O(N + M) where N is the length of s and t is the length of t
    Space complexity: O(N + M)
    """
    d1, d2 = defaultdict(set), {}
    for ch1, ch2 in zip(s, t):
        if ch2 in d2 and d2[ch2] != ch1:
            return False
        d1[ch1].add(ch2)
        d2[ch2] = ch1
    for v in d1.values():
        if len(v) > 1:
            return False
    return True


class Test(unittest.TestCase):
    data = [
        ('egg', 'add', True),
        ('foo', 'bar', False),
        ('paper', 'title', True)
        ]

    def test_is_isomorphic(self):
        for test_string1, test_string2, result in self.data:
            self.assertEqual(result, is_isomorphic(test_string1, test_string2))


if __name__ == '__main__':
    unittest.main()