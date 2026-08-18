""" Given a string, find the length of the longest substring without repeating characters. """

from collections import defaultdict
import unittest2 as unittest

def length_of_longest_substring_v1(s):
    """ Pattern: Variable-Size Sliding Window — Longest Valid Window.

        General template:
            1. Expand the right boundary and add the new element to the window state.
            2. If the window becomes invalid, shrink from the left until the invariant
               is restored.
            3. Once the window is valid, update the maximum window length.

        For this problem, the invariant is:
            every character in s[left:right+1] appears at most once.

        We use a frequency map to represent the current window. When s[right] is added,
        its count may become greater than 1, which means the window now contains a
        duplicate and is invalid.

        Because the window was valid before adding s[right], the only character that
        can violate the invariant is s[right]. We therefore move left forward,
        decrementing character counts as they leave the window, until s[right] appears
        only once again.

        At that point the invariant has been restored, so the current window is a
        candidate for the longest valid substring.

        This is the direct implementation of the longest-valid-window template:
            expand -> invalid -> shrink until valid -> evaluate

        Each character enters the window once and leaves it at most once.

    Time complexity : O(N)
    Space complexity: O(N), or O(1) if the set of characters considered is the English alphabet O(26)
    """
    n, res = len(s), 0
    chars = defaultdict(int)
    left = right = 0
    while right < n:
        chars[s[right]] += 1
        while chars[s[right]] > 1:
            chars[s[left]] -= 1
            left += 1
        res = max(res, right - left + 1)
        right += 1
    return res

def length_of_longest_substring_v2(s):
    """ Pattern: Variable-Size Sliding Window — Longest Valid Window.

        This uses the same sliding-window template as the frequency-map solution:

            expand right
                -> if invalid, shrink left until valid
                -> evaluate the valid window

        The invariant is still:
            s[left:right+1] contains no duplicate characters.

        The previous solution uses a HashMap to store character frequencies. However,
        for this problem we only need to know whether a character is already present
        in the current window; its exact frequency is not necessary.

        Therefore, a HashSet is sufficient window state.

        Before adding s[right], if that character is already in the set, adding it
        would create a duplicate. We repeatedly remove s[left] from the set and move
        left forward until s[right] is no longer present.

        We can then add s[right], restoring the invariant, and update the maximum
        window length.

        So this is not a different algorithm from the HashMap version. It is the same
        longest-valid-window template with a simpler state representation:

            HashMap frequencies -> HashSet membership

        Each character is added to and removed from the set at most once.

    Time complexity: O(N)
    Space complexity: O(N), or O(1)
    """
    n = len(s)
    window = set()  # A hash set is used to keep track of the characters in the current sliding window
    res = left = right = 0
    while right < n:
        c = s[right]
        while c in window:
            window.remove(s[left])
            # Notice that only 'left' moves forward. This is running a while loop that keeps deleting characters at
            # 'left' index until we get rid of the duplicate character at 'right'.
            left += 1
        window.add(c)
        res = max(res, right - left + 1)
        right += 1
    return res

def length_of_longest_substring_v3(s):
    """ Pattern: Variable-Size Sliding Window — Longest Valid Window.

        The underlying invariant and template are unchanged:

            invariant:
                s[left:right+1] contains no duplicate characters

            template:
                expand right
                -> restore validity when a duplicate appears
                -> evaluate the valid window

        The previous solutions restore the invariant by moving left forward one
        character at a time until the duplicate leaves the window.

        This solution asks whether we can restore the same invariant more directly.

        Instead of storing frequencies or membership, the HashMap stores each
        character's most recent index.

        If s[right] was previously seen at index j and j is still inside the current
        window, then any window containing both j and right is invalid. Therefore,
        instead of shrinking one position at a time, we can jump left directly past
        that duplicate:

            left = j + 1

        Equivalently:

            left = max(left, last_seen[s[right]] + 1)

        The max is important because the previous occurrence may already lie outside
        the current window. The left boundary must never move backward.

        After moving left if necessary, the current window is valid again, so we update
        the maximum length and record right as the character's newest occurrence.

        This is an optimization of the same sliding-window pattern, not a separate
        pattern:

            v1: detect duplicates with frequencies and shrink one-by-one
            v2: detect duplicates with membership and shrink one-by-one
            v3: remember positions and jump directly to the new valid left boundary

        Example:

         index    0    1    2    3   4   5   6   7
         string    a    c    b    d   b   a   c   d
                   ^                  ^
                   |                  |
		          left              right

		 last_occurrence = {a : 0, c : 1, b : 2, d: 3}
		 # case 1: last_occurrence[b] = 2, current window is s[0:4],
		 #             b is in the current window, last_occurrence[b] = 2 > left = 0. Move left pointer to
		 #             last_occurrence[b] + 1 = 3
		 last_occurrence = {a : 0, c : 1, b : 4, d: 3}

         index    0    1    2    3   4   5   6   7
         string   a    c    b    d   b   a   c   d
						         ^   ^
					             |   |
				               left  right

         index    0    1    2    3   4   5   6   7
         string   a    c    b    d   b   a   c   d
					             ^       ^
					             |       |
				               left    right
		 # case 2: last_occurrence[a] = 0, which means 'a' is not in the current window s[3:5] , since
		 # last_occurrence[a] = 0 < left = 3. We can keep moving the right pointer.

	     Consider the input:  s = 'tmsmfdut'
	     When right = s.length()-1 = 7, left = 2 after we've encountered the first repeated 'm',
	     so the current window is defined by left=2, right=7, substring='smfdut' If we update
	     left = last_occurrence['t'] + 1, then 'left' will be equal to 1 because the previous occurrence
	     of 't' is at index 0, and this will give a wrong answer. For this reason, 'left' should not be set to
	     (last_occurrence[c] + 1) as this value is less than current value of left = 2, or in simple words
	     (last_occurrence_index[c] + 1) is outside the window defined by left=2 and right=7.
	     If we have a string  like 'abba', when we encounter the second 'a', we want to mark the start of the
	     duplicate-free string from index 2 (second occurrence of 'b') which is the last known index which
	     holds uniqueness assumption, not from (last_occurrence['a'] + 1) which is 1.

    Time complexity : O(N)
    Space complexity: O(N), or O(1) if the set of characters considered is the English alphabet O(26)
    """
    n, res = len(s), 0
    last_occurrence = {}
    left = right = 0
    while right < n:
        if s[right] in last_occurrence:
            # If this is a duplicate character, shrink the window past its last recorded occurrence
            left = max(left, last_occurrence[s[right]] + 1)
            # The variable 'left' is used to indicate the index of first character of this substring/window. If the
            # duplicate character's index is less than 'left' itself, this means the duplicate character in the hash
            # map is no longer available at this time and is already outside the current window.
        res = max(res, right - left + 1)
        last_occurrence[s[right]] = right
        right += 1
    return res


class Test(unittest.TestCase):
    data = [('abcabcbb', 3), ('bbbbb', 1), ('pwwkew', 3)]

    def test_length_of_longest_substring(self):
        for test_string, result in self.data:
            self.assertEqual(result, length_of_longest_substring_v1(test_string))
            self.assertEqual(result, length_of_longest_substring_v2(test_string))
            self.assertEqual(result, length_of_longest_substring_v3(test_string))


if __name__ == '__main__':
    unittest.main()
