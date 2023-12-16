""" Given a string S and a string T, find the minimum window in S which will contain all the characters in T in
complexity O(n). """

from collections import Counter, defaultdict
import unittest2 as unittest


# Video explanation: https://youtu.be/eS6PZLjoaq8
def min_window_v1(s, t):
    """ Similar to 438- Find All Anagrams in a String.

        We can use a simple sliding window approach to solve this problem. Let us call a window desirable if it has all
        the characters from T.

        In any sliding window based problem we have two pointers. One right pointer whose job is to expand the current
        window and one left pointer whose job is to contract a given window. At any point in time, only one of these
        pointers moves and the other one remains fixed.

        The solution is pretty intuitive: We keep expanding the window by moving the right pointer. When the window has
        all the desired characters, we contract (if possible) and save the smallest window till now. The answer is the
        smallest desirable window seen so far.

            - We start with two pointers, 'left' and 'right', initially pointing to the first element of the string S.

            - We use the right pointer to expand the window until we get a desirable window i.e. a window that
               contains all the characters of T.

            - Once we have a window with all the characters, we can move the left pointer ahead one by one. If the
               window is still a desirable one, we keep on updating the minimum window size. If the window is not
               desirable anymore, we repeat step 2 onwards.

        To check if a window is valid/desirable, we use a map 'counter' to store (char, count) of characters
        in T (even though the map evolves to include characters in S but with a negative count). We also use a counter
        'matched_characters' for the number of chars of T so far matched in S.

        The key part is counter[cur_char] -= 1: We decrease the count of EVERY character in S. If it does not exist in
        T, the count will drop below zero. When contracting the window, we make sure that the active window always
        contains all the characters in T. In this case, every time the window expands, only the new character is
        checked.

        The idea is we use a variable-length sliding window which is gradually applied across the string. We use two
        pointers 'left' and 'right' to mark the sliding window. We start by fixing the left pointer and moving the
        right pointer to the right. The way we determine whether the current window is valid is by checking if all the
        target characters are present in the current window. If we are in a valid sliding window:

            - We first make note of the sliding window of the most minimum length we have seen so far.
            - Next, we try to contract the sliding window by moving the left pointer.
            - If the sliding window continues to be valid, we note the new minimum length.
            - If it becomes invalid (at least one character of the target string have been dropped), we break out of
               the inner loop and go back to expanding the window.

        The idea is a general solution for substring (longest/shortest/non-duplicate, etc):

            - Create a hash map tracking occurrences of any specific characters in the target substring.
            - Use two pointers, left=0 and right=0, to track current width/distance/range of the active window.
            - Create a counter tracking if current width/distance/range is a valid substring range.
            - As long as the counter indicates it's a valid range, shrink/expand the window until range's validity
               changes (by altering counter accordingly), record the valid width and let it compare with the last value
               (using min()/max() accordingly).

    Time complexity: O(N + M), both pointers scan the string s once
    Space complexity: O(N + M), or O(1)
    """
    n = len(s)
    counter = Counter(t)
    # characters_to_match is the total number of characters yet to be matched in the current window to be
    # desirable/valid
    characters_to_match = len(t)
    left = right = 0
    min_left, min_length = 0, float('inf')  # min_left is the left boundary of the minimum window found so far
    while right < n:
        cur_char = s[right]
        # Always decrement the counter of the current character. If the character is not in t, the counter drops below
        # zero. Interestingly, the counter for non-target characters never gets positive because the upper loop
        # decrements and lower loop increments the same elements
        counter[cur_char] -= 1
        if counter[cur_char] >= 0:
            # If the counter of the current character doesn't drop below zero, it means the character exists in t, so
            # decrement the counter of characters to match
            characters_to_match -= 1
        while characters_to_match == 0:
            # Try and contract the window till it ceases to be desirable/valid
            cur_length = right - left + 1
            if cur_length < min_length:
                min_left, min_length = left, cur_length  # Save the smallest window
            # Increment the counter of the leftmost character in the window. We increment this for all characters, but
            # only the target characters have a chance to have positive counters.
            counter[s[left]] += 1
            if counter[s[left]] > 0:
                # If the character we just discarded was part of t, then it would have a counter equal to 0 AT LEAST,
                # and if it's the case it would be > 0 after being incremented.
                # For every character that is not in s, we do one increment and one decrement. So, it totals up to 0,
                # which will never pass the if condition.
                characters_to_match += 1
            left += 1
        right += 1
    return s[min_left:min_left + min_length] if min_length != float('inf') else ''


# Video explanation: https://youtu.be/jSto0O4AJbM
def min_window_v2(s, t):
    """ If the previous algorithm looks confusing, we can also use a second hash map to represent the current
         sliding window in s.

    Time complexity: O(N+ M)
    Space complexity: O(N + M)
    """
    n = len(s)
    t_counter = Counter(t)
    window = defaultdict(int)  # Keeps a count of all the unique characters in the current window
    # 'characters_to_match' is how many UNIQUE characters in t should be present in the current window in its desired
    # frequency for the window to be valid. e.g. if t = "AABC" then the window must have two A's, one B and one C.
    # Thus 'characters_to_match'' would be equal to 0 when all these conditions are met.
    characters_to_match = len(t)
    res = ''
    min_len = float('inf')
    left = right = 0
    while right < n:
        cur_char = s[right]
        window[cur_char] += 1
        if window[cur_char] == t_counter[cur_char]:
            # If the frequency of the current character added equals the desired count in t, then decrement the
            # counter of characters to match
            characters_to_match -= 1
        # Try and contract the window till the point where it ceases to be desirable
        while characters_to_match == 0:
            cur_length = right - left + 1
            if cur_length < min_len:  # Save the smallest window seen so far
                min_len, res = cur_length, s[left:right + 1]
            window[s[left]] -= 1
            if s[left] in t_counter and window[s[left]] < t_counter[s[left]]:
                characters_to_match += 1
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
