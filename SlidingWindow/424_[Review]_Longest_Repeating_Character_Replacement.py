""" Given a string s that consists of only uppercase English letters, you can perform at most k operations on that
string.
In one operation, you can choose any character of the string and change it to any other uppercase English character.
Find the length of the longest sub-string containing all repeating letters you can get after performing the above
operations. """

from collections import defaultdict
import unittest2 as unittest

# Video explanation: https://www.youtube.com/watch?v=gqXU1UyA8pk
def character_replacement_v1(s, k):
    """ Pattern: Variable-Size Sliding Window — Longest Valid Window.

        For any candidate window, we are allowed to replace at most k characters so
        that the entire window contains the same character.

        Suppose we decide that the final repeated character will be X.

        Every X already in the window can stay as-is. Every character that is not X
        must be replaced. Therefore:

            replacements_needed_for_X = window_size - frequency(X)

        To minimize the number of replacements, we should choose as X whichever
        character already appears most frequently in the window.

        Therefore:

            minimum replacements needed = window_size - max_frequency

        where `max_frequency` is the frequency of the most common character in the
        current window.

        This gives the window invariant:

            window_size - max_frequency <= k

        Now the problem fits the Longest Valid Window template:

            1. Expand right and update the character frequencies.
            2. If the window requires more than k replacements, shrink left until
               the invariant is restored.
            3. Once valid, update the maximum window length.

        In this first-principles version, we recompute the ACTUAL maximum frequency of
        the current window when checking validity. Therefore, after the shrinking loop,
        s[left:right+1] is guaranteed to be a genuinely valid window.

        Each pointer moves only forward.

    Time complexity: O(N), we access each index of the string at most two times, when it is added to and/or removed from
    the sliding window.
    Space complexity: O(1), the maximum number of keys in the map equals the number of unique characters in the string,
    which is the size of English alphabet.
    """
    n, res = len(s), 0
    counter = defaultdict(int)
    left = right = 0
    while right < n:
        counter[s[right]] += 1
        while right - left + 1 - max(counter.values()) > k:
            counter[s[left]] -= 1
            left += 1
        res = max(res, right - left + 1)
        right += 1
    return res


def character_replacement_v2(s, k):
    """ Same idea but we keep shrinking the window from the left AS LONG AS the max number of character replacements
        exceeds k.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    n = len(s)
    left = right = max_frequency = res = 0
    counter = defaultdict(int)
    while right < n:
        counter[s[right]] += 1
        max_frequency = max(max_frequency, counter[s[right]])
        while right - left + 1 - max_frequency > k:
            counter[s[left]] -= 1
            left += 1
        res = max(res, right - left + 1)
        right += 1
    return res


class Test(unittest.TestCase):
    data = [('ABAB', 2, 4), ('AABABBA', 1, 4)]

    def test_character_replacement(self):
        for test_s, test_k, result in self.data:
            self.assertEqual(result, character_replacement_v1(test_s, test_k))
            self.assertEqual(result, character_replacement_v2(test_s, test_k))


if __name__ == '__main__':
    unittest.main()