""" Given two strings s and t, return true if s is a subsequence of t, or false otherwise.

A subsequence of a string is a new string that is formed from the original string by deleting some (can be none) of the
characters without disturbing the relative positions of the remaining characters. (i.e., "ace" is a subsequence of
"abcde" while "aec" is not). """

from collections import defaultdict
import unittest2 as unittest


# Video explanation: https://youtu.be/99RVfqklbCE
def is_subsequence(s, t):
    """ We iterate through the source and target strings, respectively with a pointer. Each pointer marks a position
         that we progress on the matching of the characters.

         We designate two pointers for iteration, with j pointer referring to the source string and i to the target
         string. We move the pointers accordingly on the following two cases:

            - If source[j] == target[i]: we found a match. Hence, we move both pointers one step forward.
            - If source[j] != target[i]: no match is found. We then move only i pointer on the target string.

        The iteration would terminate when either of the pointers exceeds its boundary.

        At the end of the iteration, the result solely depends on the fact that whether we have consumed all the
        characters in the source string. If so, we have found a suitable match for each character in the source string.
        Therefore, the source string is a subsequence of the target string.

    Time complexity: O(M), where M is the length of the target string. At each iteration, we would consume one character
    from the target string and optionally one character from the source string. Iterations end when either of the
    strings becomes empty. In the worst case, we would have to scan the entire target string.
    Space complexity: O(1), the counter can hold at most 26 characters (or 128 characters)
    """
    n, m = len(t), len(s)
    i = j = 0
    while i < n and j < m:
        if t[i] == s[j]:
            j += 1
        i += 1
    return j == m


class Test(unittest.TestCase):
    data = [('abc', 'ahbgdc', True), ('axc', 'ahbgdc', False)]

    def test_can_construct(self):
        for s, t, result in self.data:
            self.assertEqual(result, is_subsequence(s, t))


if __name__ == '__main__':
    unittest.main()