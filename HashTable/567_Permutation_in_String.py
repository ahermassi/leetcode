""" Given two strings s1 and s2, write a function to return true if s2 contains the permutation of s1. In other words,
one of the first string's permutations is the substring of the second string. """
import string
from collections import Counter, defaultdict
import unittest2 as unittest


def check_inclusion_v1(s1, s2):
    """ One string will be a permutation of another string only if both of them contain the same characters with the
        same frequency. We can consider every possible substring in the long string s2 of the same length as that of s1
        and check the frequency of occurrence of the characters appearing in the two. If the frequencies of every
        letter match exactly, then only s1's permutation can be a substring of s2.
        We make use of a hash map 'counter' which stores the frequency of occurrence of all the characters in the short
        string s1. We consider every possible substring of s2 of the same length as that of s1, find its corresponding
        frequency map as well. But instead of generating the hash map afresh for every window considered in s2,
        we just need to maintain a sliding window with length of s1, move from beginning to the end of s2.
        When a character moves in from right of the window, we add 1 to that character count.
        When a character moves out from left of the window, we subtract 1 from that character count from the map.
        We can maintain the window by deleting the value of s2[i - len(s1)]. After, we only need to check if the two
        frequency maps are equal.
    Time complexity: O(N + N * M) ~= O(N * M), where N is the length of string s1 and M is the length of string s2.
    We could argue that comparing the frequency maps is O(1) since they contain at most 26 key-value pairs, which
    results in an O(N + M) time complexity
    Space complexity: O(1)
    """
    if len(s1) > len(s2):
        return False
    n, m = len(s1), len(s2)
    counter, window = Counter(s1), Counter(s2[:n])
    if window == counter:
        return True
    for i in range(n, m):
        window[s2[i]] += 1
        window[s2[i - n]] -= 1
        if window[s2[i - n]] == 0:
            del window[s2[i - n]]
        if window == counter:
            return True
    return False


def check_inclusion_v2(s1, s2):
    """ The previous approach can be optimized. Instead of comparing all the elements of the hashmaps for every
        updated map corresponding to every window of s2 considered, we keep track of the number of characters
        which were already matching in the previous window and update just the count of matching characters when
        we slide the current window.
        We maintain a 'matches' variable which stores the number of characters that have the same occurrence frequency
        in s1 and the current window in s2. When we slide the window, if the deduction of the leftmost character and the
        addition of the new character leads to a new frequency match for any of the characters, we increment 'matches'
        by 1. Otherwise, we keep 'matches' intact. However, if a character whose frequency was the same earlier
        (prior to addition or removal) is added, it now leads to a frequency mismatch which is taken into account by
        decrementing 'matches'. If, after sliding the window 'matches' evaluates to 26, it means all the characters
        match in frequency totally. So, we return a True in that case immediately.
    Time complexity: O(N + M)
    Space complexity: O(1)
    """
    n, m = len(s1), len(s2)
    s1_counter, s2_counter = Counter(s1), Counter(s2[:n])
    matches = 0
    for c in string.ascii_lowercase:
        if s1_counter[c] == s2_counter[c]:
            matches += 1
    if matches == 26:
        return True
    for i in range(n, m):
        cur_char, prev_char = s2[i], s2[i-n]

        s2_counter[cur_char] += 1  # Expand the window
        if s1_counter[cur_char] == s2_counter[cur_char]:
            matches += 1
        # If the addition of the current character disrupts an earlier match
        elif s1_counter[cur_char] == s2_counter[cur_char] - 1:
            matches -= 1

        s2_counter[prev_char] -= 1  # Shrink the window
        if s1_counter[prev_char] == s2_counter[prev_char]:
            matches += 1
        # If the removal of the current character disrupts an earlier match
        elif s1_counter[prev_char] == s2_counter[prev_char] + 1:
            matches -= 1

        if matches == 26:
            return True
    return False


def check_inclusion_v3(s1, s2):
    """ Same solution as 438- Find All Anagrams in a String. No hash map comparison is involved.
        Find the frequency of characters in the string s1 using 'counter' hash map, two variables 'left' and 'right' to
        represent the left and right boundaries of the sliding window, and a variable 'matches' to represent the number
        of characters in the string s1 that we matched in the sliding window so far.
        If the character on the right boundary is already in the hash table, indicating that the character appears in
        s1, then 'need' is incremented by 1, and then the entry of the current character in the hash table is also
        decremented by 1 anyway. If 'need' is equal to s2's length at any time, it means that the characters in s1 are
        matched in the current window, so we return true.
        If the window size (right - left + 1) is equal to the length of s1, it means that the leftmost character should
        be removed from the window. If after removal (corresponding entry in the frequency map is incremented by 1)
        the count of the left character is greater than 0, it means that the character exists in s1. Why ?
        Well, because each character is decremented by 1 above, and if it is not a character in s1, then the character's
        frequency in the hash table should be 0, and it will be -1 after decrementing by 1, so that we know whether
        the character exists in s1. So if the leftmost character we removed exists in s1, 'need' is decremented by 1.
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
        counter[cur_char] -= 1  # Decrement the count of current character anyway, so when it is not part of s1 it gets
        # a negative entry in the map
        if matches == n:
            return True
        if right - left + 1 == n:  # Current window size is equal to s1's length
            counter[s2[left]] += 1  # Discard the leftmost character
            if counter[s2[left]] > 0:  # If the discarded character was part of s1, then it would have an entry equal to
                # 0 at least, and if it's the case it would be > 0 after being incremented
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
