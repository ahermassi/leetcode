""" Given two strings s and t, determine if they are isomorphic.
Two strings are isomorphic if the characters in s can be replaced to get t.
All occurrences of a character must be replaced with another character while preserving the order of characters.
No two characters may map to the same character but a character may map to itself. """

import unittest2 as unittest


def is_isomorphic(s, t):
    """ The idea is that we need to map a character to another one, for example, 'egg' and 'add', we need to construct
        the mapping 'e' -> 'a', 'a' -> 'e', 'g' -> 'd', and 'd' -> 'g'. When we encounter a character for the first
        time, we map it with the corresponding current character of the other string. If we encounter that character
        later, then we go and fetch the previous mapping and compare it to the current character of the other string.
        If they match, then fine. Otherwise, the strings can't be isomorphic.
    Time complexity: O(N + M), where N is the length of s and t is the length of t
    Space complexity: O(1), the hash maps can't store more than the size of the alphabet characters
    """
    s_chars, t_chars = {}, {}
    for c1, c2 in zip(s, t):
        if c1 not in s_chars and c2 not in t_chars:
            s_chars[c1] = c2
            t_chars[c2] = c1
        elif s_chars.get(c1, c2) != c2 or t_chars.get(c2, c1) != c1:  # We use a default value with .get() to avoid
            # returning False when both c1 and c2 are encountered for the first time
            return False
        # The previous block is equivalent to:
        # if (c1 in s_chars and s_chars[c1] != c2) or (c2 in t_chars and t_chars[c2] != c1):
        #     return False
        # s_chars[c1], t_chars[c2] = c2, c1
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