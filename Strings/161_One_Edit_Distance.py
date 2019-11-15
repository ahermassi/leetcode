""" Given two strings s and t, determine if they are both one edit distance apart.
Note:
There are 3 possibilities to satisfy one edit distance apart:
Insert a character into s to get t
Delete a character from s to get t
Replace a character of s to get t """

import unittest2 as unittest


def is_one_edit_distance(s, t):
    """ Let's assume that s is always shorter or the same length as t. If not, we could always call
        is_one_edit_distance(t, s) to inverse the string order.
        If there is a different character so that s[i] != t[i]:
            1- If the strings are of the same length, ALL next characters should be equal to keep one edit away
               distance. To verify it, we compare the substrings of s and t both starting from the (i+1)th character.
               Example: s = '1203', t = '1213'; mismatch at s[2] and t[2]. Since s and t have the same length, s[3:]
               and t[3:] should be equal.
            2- If t is one character longer than s, the additional character t[i] should be the only difference between
               both strings. To verify it, we compare a substring of s starting from the ith character and a substring
               of t starting from the (i+1)th character.
               Example: s = 'abcd', t = 'abecd'; mismatch at s[2] and t[2]. Since t is 1 character longer than s,
               s[2:] and t[3:] should be equal.
    Time complexity: O(N), where N is a number of characters in the longest string.
    Space complexity: O(N) (string slicing)
    """
    if s == t:
        return False
    i, n, m = 0, len(s), len(t)
    if n > m:  # Force s no longer than t
        return is_one_edit_distance(t, s)
    if m - n > 1:  # The strings are NOT one edit away distance if the length difference is more than 1.
        return False
    while i < n and s[i] == t[i]:
        i += 1
    if n == m:
        return s[i + 1:] == t[i + 1:]
    return s[i:] == t[i + 1:]


class Test(unittest.TestCase):
    data = [('ab', 'acb', True), ('cab', 'ad', False), ('1203', '1213', True)]

    def test_is_one_edit_distance(self):
        for test_s, test_t, result in self.data:
            self.assertEqual(result, is_one_edit_distance(test_s, test_t))


if __name__ == '__main__':
    unittest.main()

