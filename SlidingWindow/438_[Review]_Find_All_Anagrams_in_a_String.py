""" Given a string s and a non-empty string p, find all the start indices of p's anagrams in s.
String consists of lowercase English letters only and the length of both strings s and p will not be larger than
20,100.
The order of output does not matter. """

from collections import Counter
import unittest2 as unittest


def find_anagrams_v1(s, p):
    """
    Pattern: Fixed-Size Sliding Window + Frequency Matching.

    Start from the definition of an anagram:

        Two strings are anagrams iff they contain exactly the same characters
        with exactly the same frequencies.

    Therefore, character order inside a candidate substring does not matter.
    What matters is whether its frequency map matches the frequency map of `p`.

    An anagram of `p` must also have exactly len(p) characters, which gives us
    a fixed-size sliding window:

        window_size = len(p)

    So the problem becomes:

        For every contiguous window of size len(p) in `s`,
        does its frequency map equal Counter(p)?

    This is the same Fixed-Size Sliding Window + Frequency Matching pattern
    used in LC 567.

    The difference in the problem objective is:

        LC 567:
            return True as soon as one matching window is found

        LC 438:
            collect the starting index of every matching window

    This implementation uses the following fixed-window lifecycle:

        preload len(p) - 1 characters
        -> add right, completing a window of size len(p)
        -> evaluate the complete window
        -> remove left, returning to size len(p) - 1
        -> advance and repeat

    `p_counter` stores the required frequencies from `p`.
    `window` stores the frequencies represented by the current sliding window.

    When:

        window == p_counter

    the current substring is an anagram of `p`, so we append its left boundary.

    After evaluating the window, the leftmost character is removed from the
    frequency map so the next iteration can slide the window one position
    to the right without rebuilding its state from scratch.

    Pattern connection:

        anagram preserves length
            -> only windows of len(p) matter
            -> Fixed-Size Sliding Window

        anagram ignores order but preserves frequencies
            -> Frequency Matching

    Each character enters and leaves the window once.

    Time complexity: O(N), where N = len(s).
          Counter comparison is O(26) = O(1) because the strings contain only
          lowercase English letters.
    Space complexity: O(26) = O(1)
    """
    if len(p) > len(s):
        return []
    n, m = len(s), len(p)
    p_counter, window = Counter(p), Counter(s[:m - 1])
    res = []
    left, right = 0, m - 1
    while right < n:
        left_char, right_char = s[left], s[right]

        # Complete the current size-m window.
        window[right_char] += 1

        if window == p_counter:
            res.append(left)

        # Return the window to size m - 1 before the next iteration.
        window[left_char] -= 1
        if window[left_char] == 0:
            del window[left_char]

        left += 1
        right += 1

    return res

def find_anagrams_v2(s, p):
    """
    Pattern: Fixed-Size Sliding Window + Incremental Frequency Matching.

    Start from the same first principles as v1:

        - An anagram of p must have exactly len(p) characters.
        - Therefore, only fixed-size windows of len(p) in s matter.
        - Two strings are anagrams iff every character has exactly the same
          frequency in both strings.

    v1 maintains:
        `counter` = frequencies required by p
        `window`  = frequencies in the current window

    and evaluates every complete window by comparing:

        window == counter

    This solution asks:

        When the window slides by one position, how much of the frequency
        state actually changes?

    Only two character counts change:
        - s[right] enters the window
        - s[left] leaves the window

    Equality of the two frequency maps can be viewed as 26 independent
    conditions:

        window['a'] == counter['a']
        window['b'] == counter['b']
        ...
        window['z'] == counter['z']

    Instead of checking all 26 conditions after every slide, `matches` stores
    how many of those equalities are currently true.

    This implementation uses the Fixed-Size Sliding Window lifecycle:

        preload len(p) - 1 characters
        -> add right, completing a size-len(p) window
        -> update `matches` for right_char
        -> evaluate the complete window
        -> remove left, returning to size len(p) - 1
        -> update `matches` for left_char
        -> advance and repeat

    Because each affected frequency changes by exactly 1, a character's match
    status can only change when it crosses the required frequency.

    When right_char enters:

        window[right_char] += 1

        - If the new count equals counter[right_char], it just became a match,
          so increment `matches`.

        - If the new count equals counter[right_char] + 1, it must have matched
          immediately before the increment. We moved one above the required
          count, so decrement `matches`.

    When left_char leaves:

        window[left_char] -= 1

        - If the new count equals counter[left_char], it just became a match,
          so increment `matches`.

        - If the new count equals counter[left_char] - 1, it must have matched
          immediately before the decrement. We moved one below the required
          count, so decrement `matches`.

    Any other count change leaves that character mismatched both before and
    after, so `matches` does not change.

    Therefore:

        matches == 26

    means every character frequency matches, so the current fixed-size window
    is an anagram of p. Unlike LC 567, where we can return immediately, this
    problem requires every match, so we append the current left boundary.

    Progression from v1:

        v1:
            maintain the window frequencies
            -> compare the entire frequency state

        v2:
            maintain the same frequencies
            -> maintain the result of that comparison incrementally

    Reusable idea:

        When an operation changes only a small part of the state, avoid
        recomputing a global predicate from scratch if the predicate itself can
        be updated using only those local changes.

    Time complexity: O(N), where N = len(s). Initializing the counters and
                     matches is bounded by len(p) + 26, and every character in
                     s is processed at most once as it enters and leaves the
                     fixed-size window.
    Space complexity: O(1), since the frequency maps contain at most 26
                      lowercase English letters.
    """
    if len(p) > len(s):
        return []
    n, m = len(s), len(p)
    counter, window = Counter(p), Counter(s[:m - 1])
    matches = 0
    for i in range(26):
        char = chr(ord('a') + i)
        if window[char] == counter[char]:
            matches += 1
    res = []
    left, right = 0, m - 1
    while right < n:
        left_char, right_char = s[left], s[right]

        # Complete the current fixed-size window.
        window[right_char] += 1

        if window[right_char] == counter[right_char]:
            matches += 1
        elif window[right_char] == counter[right_char] + 1:
            matches -= 1

        # Evaluate while the window contains exactly len(p) characters.
        if matches == 26:
            res.append(left)

        # Return the window to size len(p) - 1 for the next iteration.
        window[left_char] -= 1

        if window[left_char] == counter[left_char]:
            matches += 1
        elif window[left_char] == counter[left_char] - 1:
            matches -= 1

        left += 1
        right += 1

    return res


def find_anagrams_v3(s, p):
    """
    Pattern: Fixed-Size Sliding Window + Deficit Counter.

    Start from the same first principles as v1 and v2:

        - An anagram of p must have exactly len(p) characters.
        - Therefore, only fixed-size windows of len(p) in s matter.
        - A window is an anagram iff it contains exactly the character
          frequencies required by p.

    The previous solutions represent the window state differently:

        v1:
            Keep `counter` for p and a separate `window` frequency map.
            Compare the two maps for every complete window.

        v2:
            Keep both maps, but maintain the result of that comparison
            incrementally with `matches`.

        v3:
            Remove the separate window map entirely and mutate `counter`
            into a deficit/surplus map for the current window.

    Initially:

        counter[c] = number of copies of c required by p

    As characters enter the window, we decrement their counts:

        counter[c] > 0  -> still missing copies of c
        counter[c] == 0 -> exactly enough copies of c have been seen
        counter[c] < 0  -> the current window contains surplus copies of c

    `matched_chars` counts how many individual character occurrences required
    by p are currently satisfied.

    When right_char enters:

        if counter[right_char] > 0:
            matched_chars += 1

        counter[right_char] -= 1

    If counter[right_char] was positive before the decrement, we still needed
    that occurrence, so it satisfies one requirement from p.

    When:

        matched_chars == len(p)

    every required character occurrence has been satisfied.

    Because the sliding window is bounded to len(p) characters, satisfying all
    len(p) required occurrences means the current window must be an anagram of
    p. We therefore append its left boundary to the result.

    When the window reaches size len(p), the leftmost character must leave
    before the next iteration:

        counter[left_char] += 1

    If the count becomes positive afterward, the new window is now missing one
    required copy of that character, so:

        matched_chars -= 1

    If the count remains zero or negative, the removed occurrence was surplus
    and was not contributing to `matched_chars`.

    This is still the Fixed-Size Sliding Window template:

        expand right
        -> update the window state
        -> evaluate the complete size-len(p) window
        -> remove left
        -> continue

    The progression across the three solutions is:

        v1: compare complete frequency state
        v2: maintain the comparison result incrementally
        v3: encode target vs. current window directly as deficits and surpluses

    This is also the same deficit-counter representation used in LC 567 v3.
    The only difference is the problem's output:

        LC 567: return True when a matching window is found
        LC 438: append the left boundary of every matching window

    Reusable idea:

        A target frequency map can sometimes be transformed into a balance or
        deficit map:

            positive -> still needed
            zero     -> satisfied
            negative -> surplus

    Time complexity: O(N), where N = len(s).
    Space complexity: O(1), since the counter contains at most 26 lowercase
                      English letters.
    """
    if len(p) > len(s):
        return []
    n, m = len(p), len(s)
    counter = Counter(p)
    matched_chars = 0
    res = []
    left = right = 0
    while right < m:
        right_char = s[right]

        # This character satisfies one still-unmet requirement from p.
        if counter[right_char] > 0:
            matched_chars += 1

        # Consume this occurrence. A negative value means we have surplus
        # copies of this character in the current window.
        counter[right_char] -= 1

        # All characters required by p are satisfied, so the current
        # size-n window is an anagram.
        if matched_chars == n:
            res.append(left)

        # Keep the window bounded to size n.
        if right - left + 1 == n:
            left_char = s[left]

            # Undo the contribution of the character leaving the window.
            counter[left_char] += 1

            # Positive again means the new window is missing one required copy.
            if counter[left_char] > 0:
                matched_chars -= 1

            left += 1

        right += 1

    return res


class Test(unittest.TestCase):
    data = [('cbaebabacd', 'abc', [0, 6]), ('abab', 'ab', [0, 1, 2])]

    def test_find_anagrams(self):
        for test_string, test_pattern, result in self.data:
            self.assertEqual(result, find_anagrams_v1(test_string, test_pattern))
            self.assertEqual(result, find_anagrams_v2(test_string, test_pattern))
            self.assertEqual(result, find_anagrams_v3(test_string, test_pattern))


if __name__ == '__main__':
    unittest.main()
