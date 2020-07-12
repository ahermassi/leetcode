""" Given a string S and a string T, find the minimum window in S which will contain all the characters in T in
complexity O(n). """

from collections import Counter
import unittest2 as unittest


def min_window(s, t):
    """ The logic is similar to 438- Find All Anagrams in a String.
        We can use a simple sliding window approach to solve this problem. The solution is pretty intuitive. We keep
        expanding the window by moving the right pointer. When the window has all the desired characters, we contract
        (if possible) and save the smallest window till now. The answer is the smallest desirable window.
            1- We start with two pointers, 'left' and 'right', initially pointing to the first element of the string S.
            2- We use the 'right' pointer to expand the window until we get a desirable window i.e. a window that
               contains all of the characters of T.
            3- Once we have a window with all the characters, we can move the 'left' pointer ahead one by one. If the
               window is still a desirable one we keep on updating the minimum window size.
            4- If the window is not desirable any more, we repeat step 2 onwards.
        To check if a window is valid, we use a map 'unmatched_t_chars' to store (char, count) for chars in T. We also
        use a counter 'needed' for the number of chars of T to be found in S.
        The key part is unmatched_t_chars[s[right]] -= 1: We decrease the count for each char in S. If it does not
        exist in t, the count will be negative. When contracting the window, make sure that the active window always
        contains all letters in T. In this case, every time the window is expanded, only the new char is checked.
    Time complexity: O(N + M)
    Space complexity: O(N + M)
    """
    unmatched_t_chars = Counter(t)
    needed = len(t)
    n, left, right = len(s), 0, 0
    min_left, min_length = 0, float('inf')
    while right < n:
        c = s[right]
        unmatched_t_chars[c] -= 1  # Decrease the count for the current character. If the letter is not in T, the count
        # becomes negative
        if unmatched_t_chars[c] >= 0:  # If the character exists in T, decrease the counter of needed characters
            needed -= 1
        while needed == 0:  # When we find a valid window, move 'left' to find a smaller window
            cur_length = right - left + 1
            if cur_length < min_length:
                min_left, min_length = left, cur_length  # Note the new left edge of the minimum window
            unmatched_t_chars[s[left]] += 1
            if unmatched_t_chars[s[left]] > 0:  # If the discarded character was part of T, then it would have an entry
                # equal to 0 AT LEAST, and if it's the case it would be > 0 after being incremented
                needed += 1
            left += 1
        right += 1
    return s[min_left:min_left + min_length] if min_length != float('inf') else ''


class Test(unittest.TestCase):
    data = [('ADOBECODEBANC', 'ABC', 'BANC')]

    def test_min_window(self):
        for test_s, test_t, result in self.data:
            self.assertEqual(result, min_window(test_s, test_t))


if __name__ == '__main__':
    unittest.main()
