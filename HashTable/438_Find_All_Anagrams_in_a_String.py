""" Given a string s and a non-empty string p, find all the start indices of p's anagrams in s.
String consists of lowercase English letters only and the length of both strings s and p will not be larger than
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
    """ A different sliding window approach. No hash map comparison is involved.
        Find the frequency of characters in the string p using 'counter' hash map, two variables 'left' and 'right' to
        represent the left and right boundaries of the sliding window, and a variable 'need' to represent the number
        of characters in the string p that need to be matched.
        If the character on the right boundary is already in the hash table, indicating that the character appears in
        p, then 'need' is decremented by 1, and then the entry of the current character in the hash table is also
        decremented by 1 anyways. If 'need' is reduced to 0 at this time, it means that the characters in p are
        matched in the current window, and the left boundary is added to the result 'res'.
        If the window size (right - left + 1) is equal to the length of p, it means that the leftmost character should
        be removed from the window. If after removal (corresponding entry in the frequency map is incremented by 1)
        the count of the left character is greater than 0, it means that the character is a character in p. Why ?
        Well, because each character is decremented by 1 above, and if it is not a character in p, then the character's
        frequency in the hash table should be 0, and it will be -1 after decrementing by 1, so that we know whether
        the character belongs to p. So if the leftmost character we removed belongs to p, 'need' is incremented by 1.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    n, m = len(s), len(p)
    counter = Counter(p)
    left, right, need, res = 0, 0, len(p), []
    while right < n:
        cur_char = s[right]
        if counter[cur_char] > 0:  # The current character is in p
            need -= 1  # One less character is needed
        counter[cur_char] -= 1  # Decrement the count of current character anyway, so when it is not part of p it gets
        # a negative entry in the map
        if need == 0:
            res.append(left)
        if right - left + 1 == m:  # Current window size is equal to p length
            counter[s[left]] += 1  # Discard the leftmost character
            if counter[s[left]] > 0:  # If the discarded character was part of p, then it would have an entry equal to
                # 0 at least, and if it's the case it would be > 0 after being incremented
                need += 1
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
