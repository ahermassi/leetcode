""" Given two strings s1 and s2, write a function to return true if s2 contains the permutation of s1. In other words,
one of the first string's permutations is the substring of the second string. """
import string
from collections import Counter, defaultdict
import unittest2 as unittest


def check_inclusion_v1(s1, s2):
    """ One string is a permutation of another string only if both of them contain the same characters with the
         same number of occurrences.

         We can consider every possible substring in the longer string s2 of the same length as that of s1 and check the
         occurrences of characters appearing in the two. If the frequencies of all letters match exactly, then s1's
         permutation can be a substring of s2.

         We make use of a hashmap 'counter' which stores the number of occurrences of all the characters in the shorter
         string s1. Then, we consider every possible substring of s2 of the same length as that of s1 and construct its
         corresponding frequency map as well.

         Instead of generating the hashmap afresh for every window in s2, we just need to maintain a sliding window of
         the same length as s1 and move it from the beginning to the end of s2.

         When a character enters the window, we increment that character's count. When a character is dropped from the
         window, we decrement that character's count. We maintain a valid window by decrementing the count of the
         character at index (i - len(s1)). After, we only need to check if the two frequency maps are equal.

         Thus, the substrings considered can be viewed as a window of length as that of s1 iterating over s2.

    Time complexity: O(N + M), where N is the length of s1 and M is the length of s2. We could argue that comparing the
    frequency maps is O(1) since they contain at most 26 key-value pairs, which results in an O(N + M) time complexity.
    Space complexity: O(1)
    """
    if len(s1) > len(s2):
        return False
    n, m = len(s1), len(s2)
    counter, window = defaultdict(int), defaultdict(int)
    for i in range(n):
        counter[s1[i]] += 1
        window[s2[i]] += 1
    if counter == window:
        return True
    for i in range(n, m):
        window[s2[i]] += 1
        window[s2[i - n]] -= 1
        if window[s2[i - n]] == 0:
            del window[s2[i - n]]
        if window == counter:
            return True
    return False


# Video explanation: https://youtu.be/UbyhOgBN834
def check_inclusion_v2(s1, s2):
    """ The previous approach can be optimized. Instead of comparing all the elements of the hashmaps for every updated
         frequency map of every window of s2, we keep track of the number of characters which were already matching in
         the previous window and only update the count of matching elements when we shift the window towards the right.

         We maintain a 'matches' variable which stores the number of characters that have the same frequency of
         occurrence in s1, and the current window in s2. When we slide the window:

            - If the exclusion of the leftmost character and the inclusion of the new character lead to a new frequency
               match for any of the characters, we increment 'matches'.

            - Otherwise, we keep 'matches' intact.

        However, if a character whose frequency was the same earlier (prior to addition or removal) is included, it
        could lead to a frequency mismatch which is taken into account by decrementing 'matches'.

        If after sliding the window 'matches' evaluates to 26, it means all the characters match in frequency.

    Time complexity: O(N + M)
    Space complexity: O(1)
    """
    if len(s1) > len(s2):
        return False
    n, m = len(s1), len(s2)
    s1_counter, s2_counter = defaultdict(int), defaultdict(int)
    for i in range(n):
        s1_counter[s1[i]] += 1
        s2_counter[s2[i]] += 1
    matches = 0
    for i in range(26):
        if s1_counter[chr(i + ord('a'))] == s2_counter[chr(i + ord('a'))]:
            matches += 1
    if matches == 26:
        return True
    for i in range(n, m):
        cur_char, leftmost_char = s2[i], s2[i-n]
        s2_counter[cur_char] += 1  # Expand the window
        if s1_counter[cur_char] == s2_counter[cur_char]:
            matches += 1
        # If the addition of the current character disrupts an earlier match
        elif s2_counter[cur_char] == s1_counter[cur_char] + 1:
            matches -= 1
        s2_counter[leftmost_char] -= 1  # Shrink the window
        if s1_counter[leftmost_char] == s2_counter[leftmost_char]:
            matches += 1
        # If the removal of the current character disrupts an earlier match
        elif s1_counter[leftmost_char] == s2_counter[leftmost_char] + 1:
            matches -= 1
        if matches == 26:
            return True
    return False


def check_inclusion_v3(s1, s2):
    """ Same as 438- Find All Anagrams in a String. No hashmap comparison is needed.

         Find the frequency of characters in s1 using 'counter' hashmap, two variables 'left' and 'right' represent
         the left and right boundaries of the sliding window, and a variable 'matches' represents the number of
         characters in s1 that matched in the sliding window so far.

         If the rightmost (current) character is already in the hashmap, indicating that the character appears in s1,
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
    left, right, matches = 0, 0, 0
    while right < m:
        cur_char = s2[right]
        if counter[cur_char] > 0:  # The current character is in s1
            matches += 1  # One more character is matched
        # Decrement the count of current character in all cases, so when it is not part of s1 it gets a negative
        # count in the map.
        counter[cur_char] -= 1
        if matches == n:
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
