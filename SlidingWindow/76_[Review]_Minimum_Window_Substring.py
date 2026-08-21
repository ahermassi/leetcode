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
    """
    Pattern: Variable-Size Sliding Window — Minimum Valid Window
             + Explicit Frequency Matching.

    Start from the same first principles as v1:

        We need the smallest substring of s that contains every character
        required by t, including duplicate occurrences.

    For example, if:

        t = "AABC"

    then a valid window must contain at least:

        A -> 2
        B -> 1
        C -> 1

    This gives us the Minimum Valid Window template:

        1. Expand right until the current window satisfies every requirement.
        2. Once valid, record the current window.
        3. Keep shrinking left while the window remains valid, because we want
           the smallest possible valid window.
        4. Once shrinking makes the window invalid, resume expanding right.

    This is the same template as v1. The difference is how we represent the
    relationship between t and the current window.

    ----------------------------------------------------------------------
    State representation
    ----------------------------------------------------------------------

    v1 mutates `counter` itself into a deficit/surplus map.

    v2 keeps the two states separate:

        `counter` = frequencies required by t
        `window`  = frequencies currently present in s[left:right+1]

    We do not need every character count in the two maps to be exactly equal.
    A window is valid as long as it contains AT LEAST the required number of
    each character.

    For example, if t requires:

        A -> 2

    then all of these are sufficient:

        window['A'] = 2
        window['A'] = 3
        window['A'] = 4

    So we need to know when each distinct character requirement becomes fully
    satisfied.

    `needed` is the number of DISTINCT character requirements in t:

        needed = len(counter)

    If:

        t = "AABC"

    then:

        needed = 3

    because we need to fully satisfy the requirements for A, B, and C.

    `matched_characters` counts how many of those distinct requirements are
    currently satisfied.

    ----------------------------------------------------------------------
    Expanding right
    ----------------------------------------------------------------------

    When right_char enters:

        window[right_char] += 1

    If its frequency becomes exactly the required frequency:

        window[right_char] == counter[right_char]

    then that character's entire requirement has just become satisfied, so:

        matched_characters += 1

    We check equality rather than >= because once the requirement has already
    been satisfied, additional surplus copies should not increase
    `matched_characters` again.

    Example:

        counter['A'] = 2

        first A:
            window['A'] = 1
            requirement not yet satisfied

        second A:
            window['A'] = 2
            requirement just became satisfied
            matched_characters += 1

        third A:
            window['A'] = 3
            still satisfied, but do not increment again

    ----------------------------------------------------------------------
    Window validity and shrinking
    ----------------------------------------------------------------------

    The current window is valid when:

        matched_characters == needed

    At that point, every distinct character from t appears with at least its
    required frequency.

    Because this is a Minimum Valid Window problem, once the window becomes
    valid we shrink from the left as aggressively as possible.

    Before each shrink, record the current window if it is the smallest valid
    window seen so far.

    When left_char leaves:

        window[left_char] -= 1

    If its frequency falls below what t requires:

        window[left_char] < counter[left_char]

    then that character's requirement is no longer satisfied, so:

        matched_characters -= 1

    The window becomes invalid, the shrinking loop stops, and right resumes
    expanding.

    ----------------------------------------------------------------------
    Progression from v1
    ----------------------------------------------------------------------

    Both solutions use the same template and validity idea:

        expand right
        -> while VALID:
               record answer
               shrink left while valid
        -> once INVALID:
               resume expanding right

    They differ only in state representation:

        v1:
            one mutable deficit/surplus counter

        v2:
            target frequency map + explicit current-window frequency map

    v2 is more explicit: `counter` always means "what t requires" and `window`
    always means "what the current window contains".

    Reusable idea:

        When validity depends on satisfying multiple frequency requirements,
        track how many DISTINCT requirements are currently fully satisfied
        rather than comparing entire frequency maps after every change.

    Each pointer moves only forward, so every character enters and leaves the
    window at most once.

    Time complexity: O(N + M), where N = len(s) and M = len(t).
    Space complexity: O(N + M) in the general case because the maps may contain
                      characters from s and t; O(1) if the character alphabet
                      is fixed and bounded.
    """
    if len(t) > len(s):
        return ""
    n = len(s)
    counter, window = Counter(t), defaultdict(int)
    needed = len(counter)
    matched_characters = 0
    min_left = 0
    min_length = float("inf")
    left = right = 0
    while right < n:
        right_char = s[right]

        window[right_char] += 1

        # This distinct character requirement has just become fully satisfied.
        if window[right_char] == counter[right_char]:
            matched_characters += 1

        # Minimum Valid Window template:
        # once valid, shrink as aggressively as possible.
        while matched_characters == needed:
            window_length = right - left + 1

            if window_length < min_length:
                min_left = left
                min_length = window_length

            left_char = s[left]
            window[left_char] -= 1
            # This character's required frequency is no longer satisfied.
            if window[left_char] < counter[left_char]:
                matched_characters -= 1

            left += 1

        right += 1

    if min_length == float("inf"):
        return ""
    return s[min_left:min_left + min_length]


class Test(unittest.TestCase):
    data = [('ADOBECODEBANC', 'ABC', 'BANC')]

    def test_min_window(self):
        for test_s, test_t, result in self.data:
            self.assertEqual(result, min_window_v1(test_s, test_t))
            self.assertEqual(result, min_window_v2(test_s, test_t))


if __name__ == '__main__':
    unittest.main()
