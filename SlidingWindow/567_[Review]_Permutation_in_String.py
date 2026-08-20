""" Given two strings s1 and s2, write a function to return true if s2 contains the permutation of s1. In other words,
one of the first string's permutations is the substring of the second string. """
import string
from collections import Counter, defaultdict
import unittest2 as unittest


def check_inclusion_v1(s1, s2):
    """ Pattern: Fixed-Size Sliding Window + Frequency Matching.

        Start from the definition of a permutation:

            Two strings are permutations iff they contain exactly the same
            characters with exactly the same frequencies.

        Therefore, character order does not matter. For every candidate substring
        of s2, we only care about its frequency map.

        A permutation of s1 must also have exactly len(s1) characters, which gives
        us a fixed-size sliding window:

            window_size = len(s1)

        So the problem becomes:

            For every contiguous window of size len(s1) in s2,
            does its frequency map equal the frequency map of s1?

        Fixed-Size Sliding Window template used here:

            1. Preload the window with the first n - 1 elements.
            2. Add s2[right], completing a window of exactly size n.
            3. Evaluate the complete window.
            4. Remove s2[left], returning the window to size n - 1.
            5. Advance both boundaries and repeat.

        This gives every iteration the same lifecycle:

            size n - 1
                -> add right
            size n
                -> evaluate
                -> remove left
            size n - 1
                -> repeat

        Window state:
            `counter` = frequencies required by s1
            `window`  = frequencies currently represented by the sliding window

        When `window == counter`, the current size-n substring contains exactly the
        same multiset of characters as s1, so it is a permutation.

        When the leftmost character leaves, its count is decremented. If the count
        reaches 0, we remove the key so `window` contains only characters actually
        present in the current window.

        Pattern connection:

            permutation preserves length
                -> only windows of len(s1) matter
                -> Fixed-Size Sliding Window

            permutation ignores order but preserves frequencies
                -> Frequency Matching

        Instead of rebuilding a frequency map for every candidate substring, we
        update the existing window state as one character enters and one leaves.

    Time complexity: O(N + M), where N = len(s1) and M = len(s2). Counter comparison is O(26) = O(1) because there are only 26
    lowercase English letters.
    Space complexity: O(26) = O(1)
    """
    if len(s1) > len(s2):
        return False
    n, m = len(s1), len(s2)
    counter, window = Counter(s1), Counter(s2[:n - 1])
    left, right = 0, n - 1
    while right < m:
        left_char, right_char = s2[left], s2[right]

        # Complete the current fixed-size window.
        window[right_char] += 1

        if window == counter:
            return True

        # Remove the leftmost character so the window is back to size n - 1
        # before the next iteration.
        window[left_char] -= 1

        if window[left_char] == 0:
            del window[left_char]

        left += 1
        right += 1

    return False


# Video explanation: https://youtu.be/UbyhOgBN834
def check_inclusion_v2(s1, s2):
    """ Pattern: Fixed-Size Sliding Window + Incremental Frequency Matching.

        Start from the same first principles as v1:

            - A permutation of s1 must have exactly len(s1) characters.
            - Therefore, only fixed-size windows of len(s1) in s2 matter.
            - Two strings are permutations iff every character has exactly the
              same frequency in both strings.

        v1 maintains:
            `counter` = frequencies required by s1
            `window`  = frequencies in the current window

        and evaluates each candidate by comparing the entire frequency state:

            window == counter

        This solution asks:

            When the window changes, do we really need to compare all 26
            character frequencies again?

        No. Each sliding-window step changes only two character counts:
            - right_char enters
            - left_char leaves

        We can view equality between the two frequency maps as 26 independent
        conditions:

            window['a'] == counter['a']
            window['b'] == counter['b']
            ...
            window['z'] == counter['z']

        `matches` stores how many of those 26 equalities are currently true.

        Fixed-Size Sliding Window template used here:

            1. Preload the first n - 1 elements.
            2. Add s2[right], completing a window of exactly size n.
            3. Incrementally update `matches` for right_char.
            4. Evaluate the complete window.
            5. Remove s2[left], returning the window to size n - 1.
            6. Incrementally update `matches` for left_char.
            7. Advance both boundaries and repeat.

        Because every count changes by exactly 1, a character's match status can
        change only when it crosses the required frequency.

        When right_char enters:

            window[right_char] += 1

            - If the new count equals counter[right_char], it just became a match:
                  matches += 1

            - If the new count equals counter[right_char] + 1, it must have been
              matching immediately before the increment, so the new character
              destroyed that match:
                  matches -= 1

        When left_char leaves:

            window[left_char] -= 1

            - If the new count equals counter[left_char], it just became a match:
                  matches += 1

            - If the new count equals counter[left_char] - 1, it must have been
              matching immediately before the decrement, so removing the character
              destroyed that match:
                  matches -= 1

        Any other change leaves that character mismatched both before and after.

        Therefore:

            matches == 26

        means all 26 character frequencies match, so the current size-n window is
        a permutation of s1.

        The progression from v1 is:

            v1:
                maintain the window state
                -> compare the entire state

            v2:
                maintain the same window state
                -> maintain the comparison result incrementally

        General reusable idea:

            If an operation changes only a small part of some state, avoid
            recomputing a global predicate from scratch when the predicate itself
            can be updated from those local changes.

    Time complexity: O(N + M)
    Space complexity: O(1), since there are only 26 lowercase English letters.
    """
    if len(s1) > len(s2):
        return False
    n, m = len(s1), len(s2)
    counter, window = Counter(s1), Counter(s2[:n - 1])
    matches = 0
    # `window` currently contains n - 1 characters, so initialize matches
    # against that exact state.
    for i in range(26):
        char = chr(ord('a') + i)
        if window[char] == counter[char]:
            matches += 1
    left, right = 0, n - 1
    while right < m:
        left_char, right_char = s2[left], s2[right]

        # Complete the size-n window.
        window[right_char] += 1
        if window[right_char] == counter[right_char]:
            matches += 1
        elif window[right_char] == counter[right_char] + 1:
            matches -= 1

        # Evaluate while the window contains exactly n characters.
        if matches == 26:
            return True

        # Return the window to size n - 1 for the next iteration.
        window[left_char] -= 1
        if window[left_char] == counter[left_char]:
            matches += 1
        elif window[left_char] == counter[left_char] - 1:
            matches -= 1

        left += 1
        right += 1

    return False


def check_inclusion_v3(s1, s2):
    """ Pattern: Fixed-Size Sliding Window + Deficit Counter.

        Start from the same first principles as v1 and v2:

            - A permutation of s1 must have exactly len(s1) characters.
            - Therefore, only fixed-size windows of len(s1) in s2 matter.
            - A window is a permutation iff it contains exactly the character
              frequencies required by s1.

        The previous solutions represent this state differently:

            v1:
                Keep `counter` for s1 and a separate `window` frequency map.
                Compare the two maps after every slide.

            v2:
                Keep both maps, but avoid comparing all frequencies by maintaining
                how many frequency equalities currently match.

        This solution goes one step further:

            Do we even need a separate frequency map for the window?

        Instead, we mutate `counter` itself so that it represents how many copies
        of each character are still needed by the CURRENT window.

        Initially:

            counter[c] means we still need that many copies of c if counter[c] > 0

        When s2[right] enters:

            - If counter[s2[right]] > 0, this occurrence satisfies one character
              that we still needed, so `matched_chars` increases.

            - We always decrement counter[s2[right]].

        This gives the counter a useful interpretation:

            counter[c] > 0  -> still missing copies of c
            counter[c] == 0 -> exactly enough copies of c have been seen
            counter[c] < 0  -> the window contains surplus copies of c

        When the fixed-size window slides and s2[left] leaves, we undo its effect:

            counter[s2[left]] += 1

        If that makes the count positive, the removed occurrence was one of the
        copies that had been satisfying s1's requirement. The new window is now
        missing that character again, so `matched_chars` decreases.

        Therefore:

            matched_chars == len(s1)

        means every required character occurrence from s1 has been satisfied.
        Since the window also has exactly len(s1) characters, it must be a
        permutation of s1.

        This is still the Fixed-Size Sliding Window template:

            expand right
            -> update window state
            -> evaluate the size-n window
            -> remove left
            -> continue

        The difference is only how we REPRESENT the state:

            v1: target frequencies + window frequencies
            v2: same maps + incremental equality summary
            v3: one mutable deficit/surplus counter

        Reusable idea:
            A target frequency map can sometimes be transformed into a balance
            or deficit map. Positive counts mean "still needed", zero means
            "satisfied", and negative counts mean "surplus".

    Time: O(N + M)
    Space: O(1), since there are only 26 lowercase English letters.
    """
    if len(s1) > len(s2):
        return False
    n, m = len(s1), len(s2)
    counter = Counter(s1)
    matched_chars = 0
    left = right = 0
    while right < m:
        right_char = s2[right]

        # This character satisfies one still-unmet requirement from s1.
        if counter[right_char] > 0:
            matched_chars += 1

        # Consume this occurrence. A negative value means we have surplus
        # copies of this character in the current window.
        counter[right_char] -= 1

        # Because the window cannot have len(s1) matched characters without
        # containing at least len(s1) total characters, this means the current
        # size-n window is a permutation.
        if matched_chars == n:
            return True

        # Keep the window bounded to size n.
        if right - left + 1 == n:
            left_char = s2[left]

            # Undo the contribution of the character leaving the window.
            counter[left_char] += 1

            # Positive again means the new window is missing one required copy.
            if counter[left_char] > 0:
                matched_chars -= 1

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
