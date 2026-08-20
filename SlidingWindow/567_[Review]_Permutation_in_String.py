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
    """ Pattern: Fixed-Size Sliding Window + Incremental Frequency Matching.

        Start from the same reasoning as the first solution:

            - A permutation of s1 must have exactly len(s1) characters.
            - Therefore, only fixed-size windows of len(s1) in s2 matter.
            - Two strings are permutations iff every character has the same
              frequency in both strings.

        The first solution maintains the frequency map for the current window and,
        after every slide, compares the entire window state against `counter`.

        This solution asks a further question:

            When the window slides by one position, how much of the frequency
            state actually changes?

        Only two characters can change:
            - s2[right] enters the window
            - s2[left] leaves the window

        Equality of the two frequency maps can be viewed as 26 independent
        conditions:

            window['a'] == counter['a']
            window['b'] == counter['b']
            ...
            window['z'] == counter['z']

        Instead of checking all 26 conditions after every slide, `matches` stores
        how many of them are currently true.

        Now consider what happens when one character's frequency changes.

        When `right_char` enters the window, its count increases by exactly 1:

            window[right_char] += 1

        Because the count changes by only 1, there are only two cases in which its
        match status can change:

            - If the new count equals counter[right_char], the character just went
              from mismatched to matched, so increment `matches`.

            - If the new count equals counter[right_char] + 1, then it must have
              matched immediately before the increment. We just moved one past the
              required count, so decrement `matches`.

        Similarly, when `left_char` leaves the window, its count decreases by
        exactly 1:

            window[left_char] -= 1

        Again, only two transitions matter:

            - If the new count equals counter[left_char], the character just became
              matched, so increment `matches`.

            - If the new count equals counter[left_char] - 1, then it matched before
              the decrement, and we just moved below the required count, so decrement
              `matches`.

        Any other change leaves that character mismatched both before and after, so
        `matches` remains unchanged.

        Therefore, when:

            matches == 26

        all 26 character frequencies match, so the current window is a permutation
        of s1.

        This is still the same Fixed-Size Sliding Window template:

            build first window
            -> add the new right element
            -> remove the old left element
            -> evaluate the updated window

        The optimization is in HOW we evaluate the window:

            v1: compare the whole frequency state after every slide

            v2: maintain the result of that comparison incrementally, updating only
                the characters whose frequencies actually changed

        General reusable idea:

            When a state changes locally, avoid recomputing a global predicate from
            scratch if the predicate itself can be updated from those local changes.

    Time complexity: O(N + M)
    Space complexity: O(1)
    """
    if len(s1) > len(s2):
        return False
    n, m = len(s1), len(s2)
    counter, window = Counter(s1), Counter(s2[:n])
    matches = 0
    for i in range(26):
        char = chr(ord('a') + i)
        if window[char] == counter[char]:
            matches += 1
    if matches == 26:
        return True
    left, right = 0, n
    while right < m:
        left_char, right_char = s2[left], s2[right]
        # right_char is about to change, so remove its old contribution
        # to `matches` before updating its frequency.
        if window[right_char] == counter[right_char]:
            matches -= 1
        window[right_char] += 1
        if window[right_char] == counter[right_char]:
            matches += 1
        # Same logic for the character leaving the window.
        if window[left_char] == counter[left_char]:
            matches -= 1
        window[left_char] -= 1
        if window[left_char] == counter[left_char]:
            matches += 1
        if matches == 26:
            return True
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
