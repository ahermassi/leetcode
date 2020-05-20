""" Given two strings s1 and s2, write a function to return true if s2 contains the permutation of s1. In other words,
one of the first string's permutations is the substring of the second string. """

from collections import Counter, defaultdict
import unittest2 as unittest


def check_inclusion_v1(s1, s2):
    """ One string will be a permutation of another string only if both of them contain the same charaters with the
        same frequency. We can consider every possible substring in the long string s2 of the same length as that of s1
        and check the frequency of occurrence of the characters appearing in the two. If the frequencies of every
        letter match exactly, then only s1's permutation can be a substring of s2.
        We make use of a hash map 'chars' which stores the frequency of occurrence of all the characters in the short
        string s1. We consider every possible substring of s2 of the same length as that of s1, find its corresponding
        hash map as well. Thus, the substrings considered can be viewed as a window of length as that of s1 iterating
        over s2. If the two hash maps obtained are identical for any such window, we can conclude that s1's permutation
        is a substring of s2, otherwise not.
    Time complexity: O(N + N * (M - N)) ~= O(N * M), where N is the length of string s1 and M is the length of string s2
    Space complexity: O(1), the hash map contains at most 26 key-value pairs
    """
    if len(s1) > len(s2):
        return False
    n, m = len(s1), len(s2)
    chars = Counter(s1)
    for i in range(m - n + 1):
        if s2[i] in chars and Counter(s2[i:i+n]) == chars:
            return True
    return False


def check_inclusion_v2(s1, s2):
    """ Instead of generating the hash map afresh for every window considered in s2, we just need to maintain a sliding
        window with length of s1, move from beginning to the end of s2. When a character moves in from right of the
        window, we subtract 1 from that character count from the map. When a character moves out from left of the
        window, we add 1 to that character count. We can maintain the window by deleting the value of s2[i - len(s1)]
        when it gets larger than len(s1). After, we only need to check if the two frequency maps are equal.
    Time complexity: O(N + N * M) ~= O(N * M), where N is the length of string s1 and M is the length of string s2.
    We could argue that comparing the frequency maps is O(1) since they contain at most 26 key-value pairs, which
    results in an O(N + M) time complexity
    Space complexity: O(1)
    """
    if len(s1) > len(s2):
        return False
    n, m = len(s1), len(s2)
    chars, window = Counter(s1), defaultdict(int)
    for i in range(m):
        window[s2[i]] += 1
        if i >= n:
            window[s2[i - n]] -= 1
            if window[s2[i - n]] == 0:
                del window[s2[i - n]]
        if window == chars:
            return True
    return False


class Test(unittest.TestCase):
    data = [('ab', 'eidbaooo', True), ('ab', 'eidboaoo', False)]

    def test_check_inclusion(self):
        for test_s1, test_s2, result in self.data:
            self.assertEqual(result, check_inclusion_v1(test_s1, test_s2))
            self.assertEqual(result, check_inclusion_v2(test_s1, test_s2))


if __name__ == '__main__':
    unittest.main()
