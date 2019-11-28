""" Given a string s and a non-empty string p, find all the start indices of p's anagrams in s.
Strings consists of lowercase English letters only and the length of both strings s and p will not be larger than
20,100.
The order of output does not matter. """

from collections import Counter
import unittest2 as unittest


def find_anagrams(s, p):
    """ Maintain a window of len(p) in s, and slide to right until finish.
    Time complexity: O(N), the comparison of the two hash maps is still O(1) because every hash map can hold at most
    26 characters.
    Space complexity: O(26) = O(1)
    """
    n, m = len(s), len(p)
    p_counter = Counter(p)
    window_counter = Counter(s[:m - 1])  # Initially, the window is of size len(p) - 1
    ans = []
    for i in range(m - 1, n):
        window_counter[s[i]] += 1  # Add character to have a window of size len(p)
        if window_counter == p_counter:
            ans.append(i - m + 1)  # Append the starting index
        window_counter[s[i - m + 1]] -= 1  # Decrease count of oldest char in window. This is how the window 'slides'
        if window_counter[s[i - m + 1]] == 0:
            del window_counter[s[i - m + 1]]  # Remove the character if its count is zero
    return ans


class Test(unittest.TestCase):
    data = [('cbaebabacd', 'abc', [0, 6]), ('abab', 'ab', [0, 1, 2])]

    def test_find_anagrams(self):
        for test_string, test_pattern, result in self.data:
            self.assertEqual(result, find_anagrams(test_string, test_pattern))


if __name__ == '__main__':
    unittest.main()
