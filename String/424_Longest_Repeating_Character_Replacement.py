""" Given a string s that consists of only uppercase English letters, you can perform at most k operations on that
string.
In one operation, you can choose any character of the string and change it to any other uppercase English character.
Find the length of the longest sub-string containing all repeating letters you can get after performing the above
operations. """

from collections import defaultdict
import unittest2 as unittest

# Video explanation: https://www.youtube.com/watch?v=gqXU1UyA8pk


def character_replacement(s, k):
    """ Idea: Since the number of allowed replacements (k) is limited, we want all the characters in a particular window
        to match the most frequent character in that window.
        If we want to replace the characters in a substring and make it into the longest repeating, then we definitely
        want to find the character with maximum frequency and then replace all the other characters by this one, hence
        in this way, we can minimize the number of replacements.
        Given this, we can apply the at-most-k-changes constraint and maintain a sliding window such that:
            (size of window - frequency of the most frequent letter in the window) <= k
        where max characters to replace = size of window - frequency of the most frequent letter in the window
        Each time we expand right, we include a new character in the window. If the max number of characters to replace
        in the current window is bigger than k, we get an invalid window, and so we decrease the window size from the
        left.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    n = len(s)
    left = right = max_frequency = res = 0
    counter = defaultdict(int)
    while right < n:
        c = s[right]
        counter[c] += 1
        max_frequency = max(max_frequency, counter[c])
        max_replacements = (right - left + 1) - max_frequency
        if max_replacements > k:
            counter[s[left]] -= 1
            left += 1
        else:
            res = max(res, right - left + 1)
        right += 1
    return res


class Test(unittest.TestCase):
    data = [('ABAB', 2, 4), ('AABABBA', 1, 4)]

    def test_character_replacement(self):
        for test_s, test_k, result in self.data:
            self.assertEqual(result, character_replacement(test_s, test_k))


if __name__ == '__main__':
    unittest.main()