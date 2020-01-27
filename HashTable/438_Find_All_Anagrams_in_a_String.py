""" Given a string s and a non-empty string p, find all the start indices of p's anagrams in s.
Strings consists of lowercase English letters only and the length of both strings s and p will not be larger than
20,100.
The order of output does not matter. """

from collections import Counter
import unittest2 as unittest


def find_anagrams_v1(s, p):
    """ Maintain a window of len(p) in s, and slide to right until finish.
    Time complexity: O(N), the comparison of the two hash maps is still O(1) because every hash map can hold at most
    26 characters.
    Space complexity: O(26) = O(1)
    """
    n, m, res = len(s), len(p), []
    p_counter = Counter(p)
    window = Counter(s[:m - 1])  # Initially, the window is of size len(p) - 1
    for i in range(m - 1, n):
        window[s[i]] += 1  # Add character to have a window of size len(p)
        if window == p_counter:
            res.append(i - m + 1)  # Append the starting index, or left boundary, of the window
        window[s[i - m + 1]] -= 1  # Decrease the count of the oldest char in the window. This is how the window
        # 'slides' and shrinks (from left)
        if window[s[i - m + 1]] == 0:
            del window[s[i - m + 1]]  # Remove the character if its count is zero
    return res


def find_anagrams_v2(s, p):
    n, m = len(s), len(p)
    need = Counter(p)
    left, right, missing, res = 0, 0, len(p), []
    while right < n:
        if need[s[right]] > 0:
            missing -= 1
        need[s[right]] -= 1
        if missing == 0:
            res.append(left)
        if right - left == m - 1:
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1
            left += 1
        right += 1
    return res


class Test(unittest.TestCase):
    data = [('cbaebabacd', 'abc', [0, 6]), ('abab', 'ab', [0, 1, 2])]

    def test_find_anagrams(self):
        for test_string, test_pattern, result in self.data:
            self.assertEqual(result, find_anagrams_v1(test_string, test_pattern))
            self.assertEqual(result, find_anagrams_v2(test_string, test_pattern))


if __name__ == '__main__':
    unittest.main()
