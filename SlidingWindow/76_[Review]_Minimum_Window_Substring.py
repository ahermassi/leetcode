""" Given a string S and a string T, find the minimum window in S which will contain all the characters in T in
complexity O(n). """

from collections import Counter, defaultdict
import unittest2 as unittest


# Video explanation: https://youtu.be/eS6PZLjoaq8
def min_window_v1(s, t):
    """
    Pattern: Variable-Size Sliding Window — Minimum Valid Window
             + Frequency Deficit Counter.

    Start from the problem itself:

        We need the smallest substring of s that contains every character
        required by t, including duplicate occurrences.

    For example, if:

        t = "AABC"

    then a valid window must contain:
        2 A's, 1 B, and 1 C.

    This gives us a Variable-Size Sliding Window — Minimum Valid Window:

        1. Expand right until the window becomes valid.
        2. Once valid, record the current window.
        3. Keep shrinking from the left while the window remains valid,
           because we want the smallest possible valid window.
        4. Once shrinking makes the window invalid, resume expanding right.

    This is the same minimum-valid-window template as LC 209:

        LC 209:
            valid when window_sum >= target

        LC 76:
            valid when every required character frequency from t is satisfied

    ----------------------------------------------------------------------
    Window state: Frequency Deficit Counter
    ----------------------------------------------------------------------

    `counter` initially stores how many copies of each character are required
    by t.

    As right expands, we decrement the count of every character that enters
    the window:

        counter[right_char] -= 1

    This turns `counter` into a deficit/surplus map:

        counter[c] > 0  -> still missing copies of c
        counter[c] == 0 -> the required frequency of c is exactly satisfied
        counter[c] < 0  -> the window contains surplus copies of c

    `matched_characters` does NOT count individual matched occurrences.
    It counts how many DISTINCT character requirements from t are currently
    fully satisfied.

    `needed` is therefore:

        needed = number of distinct characters in t

    When right_char enters, we first decrement its counter:

        counter[right_char] -= 1

    If the count becomes exactly 0:

        counter[right_char] == 0

    then we have just collected enough copies of that character to fully
    satisfy its requirement, so:

        matched_characters += 1

    Example:

        t = "AABC"

        counter['A'] starts at 2.

        first A:
            2 -> 1
            A is still missing one copy

        second A:
            1 -> 0
            A's requirement is now fully satisfied
            matched_characters += 1

    ----------------------------------------------------------------------
    Window validity
    ----------------------------------------------------------------------

    The window is valid when every distinct character requirement is fully
    satisfied:

        matched_characters == needed

    Once this happens, we enter the shrinking phase of the Minimum Valid
    Window template.

    Before each shrink, the current window is valid, so we compare its length
    against the smallest valid window found so far.

    When left_char leaves, we undo its contribution:

        counter[left_char] += 1

    If the count becomes positive:

        counter[left_char] > 0

    then we just went from having enough copies of that character to being
    short one copy again. Its requirement is no longer satisfied, so:

        matched_characters -= 1

    The window is now invalid, the shrinking loop stops, and right resumes
    expanding.

    ----------------------------------------------------------------------
    Pattern connection
    ----------------------------------------------------------------------

    Minimum Valid Window template:

        expand right
        -> while VALID:
               record answer
               shrink left while still valid
        -> once INVALID:
               resume expanding right

    Frequency deficit representation:

        positive -> still missing
        zero     -> requirement satisfied
        negative -> surplus

    This also connects to the frequency-deficit ideas used in LC 567 and
    LC 438, but the meaning of the matching variable is different here:

        LC 76:
            matched_characters = number of DISTINCT character requirements
                                 whose required frequencies are satisfied

        needed:
            number of distinct required characters

    Each pointer moves only forward, so every character enters and leaves the
    window at most once.

    Time complexity: O(N + M), where N = len(s) and M = len(t).
    Space complexity: O(M) in the general case for the frequency map;
                      O(1) if the character alphabet is fixed and bounded.
    """
    if len(t) > len(s):
        return ""
    n = len(s)
    counter = Counter(t)
    matched_characters = 0
    needed = len(counter)
    min_left = 0
    min_length = float("inf")
    left = right = 0
    while right < n:
        right_char = s[right]

        # Consume this occurrence in the deficit/surplus counter.
        counter[right_char] -= 1

        # Reaching zero means this character's required frequency has just
        # become fully satisfied.
        if counter[right_char] == 0:
            matched_characters += 1

        # Minimum Valid Window template:
        # once valid, shrink as aggressively as possible.
        while matched_characters == needed:
            window_length = right - left + 1
            if window_length < min_length:
                min_left = left
                min_length = window_length

            left_char = s[left]

            # Undo the contribution of the character leaving the window.
            counter[left_char] += 1

            # Positive again means this character's frequency requirement
            # is no longer satisfied.
            if counter[left_char] > 0:
                matched_characters -= 1

            left += 1

        right += 1

    if min_length == float("inf"):
        return ""
    return s[min_left:min_left + min_length]


# Video explanation: https://youtu.be/jSto0O4AJbM
def min_window_v2(s, t):
    """ We can also use a second hashmap to represent the current sliding window in s.

    Time complexity: O(N+ M)
    Space complexity: O(N + M)
    """
    n = len(s)
    counter = Counter(t)
    window = defaultdict(int)  # Keeps a count of all the characters in the current window
    # Note that, unlike the previous algorithm, characters_to_match is initialized to the length of the counter not t.
    # characters_to_match is how many UNIQUE characters in t should be present in the current window in its desired
    # frequency for the window to be valid. e.g. if t = "AABC" then the window must have two A's, one B and one C.
    # Thus, characters_to_match is equal to 3.
    characters_to_match = len(counter)
    matched_characters = 0
    res, min_len = '', float('inf')
    left = right = 0
    while right < n:
        cur_char = s[right]
        window[cur_char] += 1
        if window[cur_char] == counter[cur_char]:
            # If the frequency of the current added character equals the desired count in t, then we have just matched
            # ALL THE OCCURRENCES of one more character
            matched_characters += 1
        # Try to contract the window until it ceases to be desirable/valid
        while matched_characters == characters_to_match:
            window_length = right - left + 1
            if window_length < min_len:  # Take note of the smallest valid window seen so far
                min_len, res = window_length, s[left:right + 1]
            window[s[left]] -= 1
            if window[s[left]] < counter[s[left]]:
                matched_characters -= 1
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
