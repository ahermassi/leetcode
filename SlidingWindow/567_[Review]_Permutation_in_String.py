""" Given two strings s1 and s2, write a function to return true if s2 contains the permutation of s1. In other words,
one of the first string's permutations is the substring of the second string. """
import string
from collections import Counter, defaultdict
import unittest2 as unittest


def check_inclusion_v1(s1, s2):
    """ Pattern: Fixed-Size Sliding Window + Frequency Matching.

        Start from the definition of a permutation:

            Two strings are permutations of each other iff they contain exactly the
            same characters with exactly the same frequencies.

        Therefore, we do not care about the order of characters inside a candidate
        substring of s2. We only care about its character-frequency map.

        A permutation of s1 must also have exactly len(s1) characters. That immediately
        gives us a fixed-size sliding window:

            window_size = len(s1)

        So instead of examining arbitrary substrings of s2, we only need to examine
        every contiguous window of exactly that size and ask:

            frequencies(window) == frequencies(s1) ?

        This maps directly to the Fixed-Size Sliding Window template:

            1. Build the state for the first window of size n.
            2. Move the window one position to the right:
                   - add the new right character
                   - remove the old left character
            3. Evaluate the newly formed window.
            4. Repeat until every size-n window has been checked.

        Here, the window state is a frequency map.

        `counter` stores the required frequencies from s1.
        `window` stores the frequencies in the current substring of s2.

        When the window slides:
            - s2[right] enters, so increment its count
            - s2[left] leaves, so decrement its count
            - if that count reaches 0, remove the key so the map represents only
              characters actually present in the current window

        If `window == counter`, the current substring contains exactly the same
        multiset of characters as s1, so it must be a permutation of s1.

        The key pattern connection is:

            permutation preserves length
                -> only windows of len(s1) matter
                -> fixed-size sliding window

            permutation ignores order but preserves counts
                -> frequency map is the necessary window state

        Instead of rebuilding a frequency map for every substring from scratch, the
        sliding window updates the existing state in O(1) work as characters enter and
        leave.

    Time complexity: O(N + M), where N is the length of s1 and M is the length of s2. We could argue that comparing the
    frequency maps is O(1) since they contain at most 26 key-value pairs, which results in an O(N + M) time complexity.
    Space complexity: O(1)
    """
    if len(s1) > len(s2):
        return False
    n, m = len(s1), len(s2)
    counter, window = Counter(s1), Counter(s2[:n])
    if window == counter:
        return True
    left, right = 0, n
    while right < m:
        window[s2[right]] += 1
        window[s2[left]] -= 1
        if window[s2[left]] == 0:
            del window[s2[left]]
        if window == counter:
            return True
        left += 1
        right += 1
    return False


# Video explanation: https://youtu.be/UbyhOgBN834
def check_inclusion_v2(s1, s2):
    """ The previous approach can be optimized. Instead of comparing all the elements of the hashmaps for every updated
         frequency map of every window in s2, we keep track of the number of characters that already matched in the
         previous window and only update the count of those characters when we slide the window.

         We maintain a 'matches' variable which stores the number of characters that have the same number of occurrences
         in both s1 and the current window in s2. When we slide the window:

            - If the exclusion of the leftmost character and the inclusion of the current character lead to a new
               match in occurrences for any of the characters, we increment 'matches'.

            - Otherwise, if a character whose frequency was the same earlier (prior to addition or removal) is included,
               it could lead to a frequency mismatch which is taken into account by decrementing 'matches'.

            - Otherwise, we keep 'matches' intact.

        If after sliding the window 'matches' evaluates to 26, it means all the characters match in frequency.

    Time complexity: O(N + M)
    Space complexity: O(1)
    """
    if len(s1) > len(s2):
        return False
    n, m = len(s1), len(s2)
    counter, window = Counter(s1), Counter(s2[:n])
    matches = 0
    for i in range(26):
        if window[chr(i + ord('a'))] == counter[chr(i + ord('a'))]:
            matches += 1
    if matches == 26:
        return True
    left, right = 0, n
    while right < m:
        cur_char, leftmost_char = s2[right], s2[left]
        window[cur_char] += 1  # Expand the window
        if window[cur_char] == counter[cur_char]:
            matches += 1
        elif window[cur_char] == counter[cur_char] + 1:
            # If the addition of the current character disrupts an earlier match
            matches -= 1
        window[leftmost_char] -= 1  # Shrink the window
        if window[leftmost_char] == counter[leftmost_char]:
            matches += 1
        elif window[leftmost_char] == counter[leftmost_char] - 1:
            # If the removal of the current character disrupts an earlier match
            matches -= 1
        if matches == 26:
            return True
        left += 1
        right += 1
    return False


def check_inclusion_v3(s1, s2):
    """ Same as 438- Find All Anagrams in a String. No hashmap comparison is needed.

         Find the frequency of characters in s1 using 'counter' hashmap, two variables 'left' and 'right' represent
         the left and right boundaries of the sliding window, and a variable 'matches' represents the number of
         characters in s1 that matched in the sliding window so far.

         If the rightmost (current) character is already in the hashmap, indicating that the character exists in s1,
         then 'matches' is incremented, and the count of the current character in the hashmap is also decremented in all
         cases.

         If at any point in time 'matches' becomes equal to s2's length, it means that all the characters in s1 were
         matched in the current window, so we return true.

         If the window size (right - left + 1) is equal to the length of s1, it means that the leftmost character should
         be removed from the window. If after removal (corresponding count in the frequency map is incremented by 1)
         the count of the leftmost character is greater than 0, it means that the character exists in s1. Why?
         Because each character count is decremented in all cases, and if it is not a character of s1, then the
         character's count in the hashmap should be 0, and it would become -1 after decrementing, so that way we know
         whether the character exists in s1. So if the leftmost character we removed exists in s1, 'matches' is
         decremented.

    Time complexity: O(N + M)
    Space complexity: O(1)
    """
    n, m = len(s1), len(s2)
    counter = Counter(s1)
    matches, needed = 0, n
    left = right = 0
    while right < m:
        cur_char = s2[right]
        if counter[cur_char] > 0:  # The current character is in s1
            matches += 1  # One more character is matched
        # Decrement the count of current character in all cases, so when it is not part of s1 it gets a negative
        # count in the map.
        counter[cur_char] -= 1
        if matches == needed:
            return True
        if right - left + 1 == n:  # Current window size is equal to s1's length
            counter[s2[left]] += 1  # Exclude the leftmost character
            if counter[s2[left]] > 0:
                # If the discarded character was part of s1, then it would have an entry equal to 0 at least, and if
                # it's the case it would be > 0 after being incremented
                matches -= 1
            left += 1
        right += 1
    return False


class Test(unittest.TestCase):
    data = [('ab', 'eidbaooo', True), ('ab', 'eidboaoo', False)]

    def test_check_inclusion(self):
        for test_s1, test_s2, result in self.data:
            self.assertEqual(result, check_inclusion_v1(test_s1, test_s2))
            self.assertEqual(result, check_inclusion_v2(test_s1, test_s2))
            self.assertEqual(result, check_inclusion_v3(test_s1, test_s2))


if __name__ == '__main__':
    unittest.main()
