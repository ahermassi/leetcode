""" Given a string S and a string T, find the minimum window in S which will contain all the characters in T in
complexity O(n). """

from collections import Counter, defaultdict
import unittest2 as unittest


def min_window_v1(s, t):
    """ Similar to 438- Find All Anagrams in a String.

        We can use a simple sliding window approach to solve this problem. Let us call a window desirable if it has all
        the characters from T.

        The solution is pretty intuitive: We keep expanding the window by moving the right pointer. When the window has
        all the desired characters, we contract (if possible) and save the smallest window till now. The answer is the
        smallest desirable window.

        We start with two pointers, 'left' and 'right', initially pointing to the first element of the string S.

        We use the 'right' pointer to expand the window until we get a desirable window i.e. a window that contains
        all the characters of T.

        Once we have a window with all the characters, we can move the 'left' pointer ahead one by one. If the window
        is still a desirable one, we keep on updating the minimum window size. If the window is not desirable anymore,
        we repeat step 2 onwards.

        To check if a window is valid/desirable, we use a map 'counter' to store (char, count) of characters
        in T (even though the map evolves to include characters in S but with a negative count). We also use a counter
        'matches' for the number of chars of T so far matched in S.
        The key part is counter[s[right]] -= 1: We decrease the count for EVERY character in S. If it does not
        exist in T, the count will be negative. When contracting the window, make sure that the active window always
        contains all letters in T. In this case, every time the window is expanded, only the new character is checked.

        The idea is we use a variable-length sliding window which is gradually applied across the string. We use two
        pointers 'left' and 'right' to mark the sliding window. We start by fixing the left pointer and moving the
        right pointer to the right. The way we determine the current window is a valid one is by checking if all the
        target characters have been found in the current window. If we are in a valid sliding window, we first make
        note of the sliding window of the most minimum length we have seen so far. Next we try to contract the sliding
        window by moving the left pointer. If the sliding window continues to be valid, we note the new minimum sliding
        window. If it becomes invalid (all characters of the target have been bypassed), we break out of the inner loop
        and go back to moving the right pointer.

        The idea is a general solution for substring (longest/shortest/non-duplicate, etc):

        Create a hash map tracking occurrences of any specific characters in the target substring.
        Use two pointers, left=0 and right=0, to track current width/distance/range of the active window.
        Create a counter tracking if current width/distance/range is a valid substring range.
        As long as the counter indicates it's a valid range, shrink/expand the window until range's validity
        changes (by altering counter accordingly), record the valid width and let it compare with the last value
        (using min()/max() accordingly).

    Time complexity: O(N + M), both pointers scan the string S once
    Space complexity: O(N + M)
    """
    n = len(s)
    counter = Counter(t)
    matches, needed = 0, len(t)  # Number of matched characters and of total characters to be matched, respectively
    left = right = 0
    min_left, min_length = 0, float('inf')  # min_left is the left boundary of the minimum window found so far
    while right < n:
        cur_char = s[right]
        if counter[cur_char] > 0:  # If the character exists in T, increase the counter of matched characters
            matches += 1
        counter[cur_char] -= 1  # Decrease the count for the current character in all cases. If the character is not
        # in T, the count becomes negative. Interestingly, the counter for non-target characters never gets positive
        # because the upper loop decrements and lower loop increments the same elements
        while matches == needed:  # When we find a valid window, move 'left' to contract and find a smaller window
            cur_length = right - left + 1
            if cur_length < min_length:
                min_left, min_length = left, cur_length  # Note the new left edge of the minimum window
            counter[s[left]] += 1  # Increase the count of the leftmost character in the window. We increase
            # this for all characters, but only the target elements have a chance to have positive counters.
            if counter[s[left]] > 0:  # If the discarded character was part of T, then it would have an entry
                # equal to 0 AT LEAST, and if it's the case it would be > 0 after being incremented. For every
                # character that is not in S, we do one increment and one decrement. So, it totals up to 0, which will
                # never pass the if condition.
                matches -= 1
            left += 1
        right += 1
    return s[min_left:min_left + min_length] if min_length != float('inf') else ''


def min_window_v2(s, t):
    """ If the previous algorithm looks confusing, we can also use a second hash map to represent the current
        sliding window.

    Time complexity: O(N+ M)
    Space complexity: O(N + M)
    """
    n = len(s)
    counter = Counter(t)
    window = defaultdict(int)  # Keeps a count of all the unique characters in the current window
    # 'matches' is used to keep track of how many UNIQUE characters in t are present in the current window
    # in its desired frequency. e.g. if t = "AABC" then the window must have two A's, one B and one C.
    # Thus 'matches'' would be equal to 3 when all these conditions are met. 'needed' is the number of UNIQUE
    # characters in t which need to be present in the desired window
    matches, needed = 0, len(counter)
    res = ''
    min_len = float('inf')
    left = right = 0
    while right < n:
        cur_char = s[right]
        window[cur_char] += 1
        if window[cur_char] == counter[cur_char]:
            # If the frequency of the current character added equals the desired count in t, then increment the
            # matches count by 1
            matches += 1
        # Try and contract the window till the point where it ceases to be desirable
        while matches == needed:
            cur_length = right - left + 1
            if cur_length < min_len:  # Save the smallest window until now
                min_len, res = cur_length, s[left:right + 1]
            window[s[left]] -= 1
            if s[left] in counter and window[s[left]] < counter[s[left]]:
                matches -= 1
            left += 1
        right += 1
    return res


class Test(unittest.TestCase):
    data = [('ADOBECODEBANC', 'ABC', 'BANC')]

    def test_min_window(self):
        for test_s, test_t, result in self.data:
            self.assertEqual(result, min_window_v1(test_s, test_t))
            self.assertEqual(result, min_window_v2(test_s, test_t))


if __name__ == '__main__':
    unittest.main()
