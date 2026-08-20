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


def find_anagrams_v2(s, p):
    """ A different sliding window approach. No hash map comparison is involved.
        Find the frequency of characters in the string p using 'counter' hash map, two variables 'left' and 'right' to
        represent the left and right boundaries of the sliding window, and a variable 'need' to represent the number
        of characters in the string p that need to be matched.
        If the character on the right boundary is already in the hash table, indicating that the character appears in
        p, then 'need' is decremented by 1, and then the entry of the current character in the hash table is also
        decremented by 1 anyways. If 'need' is reduced to 0 at this time, it means that the characters in p are
        matched in the current window, and the left boundary is added to the result 'res'.
        If the window size (right - left + 1) is equal to the length of p, it means that the leftmost character should
        be removed from the window. If after removal (corresponding entry in the frequency map is incremented by 1)
        the count of the left character is greater than 0, it means that the character is a character in p. Why ?
        Well, because each character is decremented by 1 above, and if it is not a character in p, then the character's
        frequency in the hash table should be 0, and it will be -1 after decrementing by 1, so that we know whether
        the character belongs to p. So if the leftmost character we removed belongs to p, 'need' is incremented by 1.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    n, m = len(s), len(p)
    counter = Counter(p)
    left, right, need, res = 0, 0, len(p), []
    while right < n:
        cur_char = s[right]
        if counter[cur_char] > 0:  # The current character is in p
            need -= 1  # One less character is needed
        counter[cur_char] -= 1  # Decrement the count of current character anyway, so when it is not part of p it gets
        # a negative entry in the map
        if need == 0:
            res.append(left)
        if right - left + 1 == m:  # Current window size is equal to p length
            counter[s[left]] += 1  # Discard the leftmost character
            if counter[s[left]] > 0:  # If the discarded character was part of p, then it would have an entry equal to
                # 0 at least, and if it's the case it would be > 0 after being incremented
                need += 1
            left += 1
        right += 1
    return res


class Test(unittest.TestCase):
    data = [('cbaebabacd', 'abc', [0, 6]), ('abab', 'ab', [0, 1, 2])]

    def test_find_anagrams(self):
        for test_string, test_pattern, result in self.data:
            self.assertEqual(result, find_anagrams_v1(test_string, test_pattern))
            self.assertEqual(result, find_anagrams_v2(test_string, test_pattern))


if __name__ == '__main__':
    unittest.main()
