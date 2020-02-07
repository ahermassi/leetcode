""" Implement strStr().
Return the index of the first occurrence of needle in haystack, or -1 if needle is not part of haystack. """

import unittest2 as unittest


def str_str_v1(haystack, needle):
    """ Standard search. Linearly scan haystack. Pay attention to the boundaries of the search range: 0 .. n - m + 1,
        as it is useless to go beyond haystack[n - m] considering needle's size is m.
    Time complexity: O(N * M) where N is the length of haystack and M is the length of needle
    Space complexity: O(1)
    """
    if not needle:
        return 0
    n, m = len(haystack), len(needle)
    for i in range(n - m + 1):
        c = haystack[i]
        if c == needle[0] and haystack[i: i + m] == needle:
            return i
    return -1


def str_str_v2(haystack, needle):
    """ Rabin-Karp algorithm.
        The idea is simple: move along the string, generate hash of substring in the sliding window, and compare it
        with the reference hash of the needle string.
        The Rabin-Karp algorithm is very similar to the brute-force algorithm, but it does not require the second loop.
        Instead, it uses the concept of a 'fingerprint'. Specifically,let m be the length of needle. It computes hash
        codes of each substring whose length is m. These are the fingerprints. The key to efficiency is using an
        incremental hash function, such as a function with the property that the hash code of a string is an additive
        function of each individual character. Such a hash function is sometimes referred to as a rolling hash.
        A rolling hash (also known as recursive hashing or rolling checksum) is a hash function where the input is
        hashed in a window that moves through the input. For such a function, getting the hash code of a sliding window
        of characters is very fast for each shift.
        We could consider string 'abcd' -> [ord('a'), ord('b'), ord('c'), ord('d')] as a number in a numeral system
        with the base 26. Hence 'abcd' -> [ord('a'), ord('b'), ord('c'), ord('d')] could be hashed as:
            h = ord('a') * 26^3 + ord('b') * 26^2 + ord('c') * 26^1 + ord('d') * 26^0
        Now let's consider the slice 'abcd' -> 'bcde' (sliding window). For the arrays that means
        [ord('a'), ord('b'), ord('c'), ord('d')] -> [ord('b'), ord('c'), ord('d'), ord('e')]
            h = h * 26 - ord('a') * 26^4 + ord('e') * 26^0
        Now hash regeneration is perfect and fits in a constant time.
    Time complexity: O(N + M)
    Space complexity: O(1)
    """
    if not needle:
        return 0
    if len(needle) > len(haystack):
        return -1
    n, m = len(haystack), len(needle)
    base = 26
    needle_hash = rolling_hash = 0
    for i in range(m):  # Compute the hash of haystack[:m] and reference hash of needle[:m]
        needle_hash = needle_hash * base + ord(needle[i])
        rolling_hash = rolling_hash * base + ord(haystack[i])
    if needle_hash == rolling_hash:
        return 0
    for i in range(1, n - m + 1):  # Iterate over the start position of possible match
        # Compute rolling hash based on the previous hash value: multiply previous hash by base, subtract the leftmost
        # element of the window, and add the hash of the rightmost (new) element of the window
        rolling_hash = rolling_hash * base - ord(haystack[i - 1]) * pow(base, m) + ord(haystack[i + m - 1])
        if needle_hash == rolling_hash:
            return i
    return -1


# Check out: https://leetcode.com/problems/implement-strstr/discuss/12883/KMP-in-C%2B%2B-explanation-included

def str_str_v3(haystack, needle):
    """ KMP (Knuth–Morris–Pratt) algorithm.
        The key behind KMP is that it takes advantage of the successful character checks during an unsuccessful pattern
        comparison subroutine.
        We may have a series of many comparisons that succeed and then even if one fails at the end, we should not 
        repeat the comparison work done since we already saw that a series matched.
        What we will do is very similar to the naive algorithm, it is just that we save comparisons by tracking the
        longest proper prefixes of pattern that are also suffixes.
        The key is that every time we have a mismatch, we try our best to prevent going backwards in s and repeating
        comparisons.
        We will pre-process the pattern string and create an array that indicates the longest proper prefix which is 
        also suffix at each point in the pattern string.
        A proper prefix does not include the original string.
        For example, prefixes of 'ABC' are '', 'A', 'AB' and 'ABC'. Proper prefixes are '', 'A' and 'AB'.
        For example, suffixes of 'ABC' are, '', 'C', 'BC', and 'ABC'. Proper suffixes are '', 'C', and 'BC'.
        Why do we care about these ??
        We know all characters behind our mismatch character match. If we can find the length of the longest proper
        prefix that matches a suffix to that point, we can skip len(prefix) comparisons at the beginning.
        Example: text : 'ababdbaababa', pattern: 'ababa'
        We start matching text with pattern and test if the pattern could be in text, starting at position 0. 
        We compare text[0] with pattern[0] and that turns out to be a match. We do the same for text[1], text[2] and
        text[3]. When we want to match text[4] with pattern[4], we don't have a match (d != a). We then know that the
        pattern will not start at the first position. We could then start the matching all over again for position 1 
        but that is not efficient. We can use the table now.
        The error occurred at pattern[4], so we go to table[4] which is 2. That tells us that we can start matching at 
        the current position again with 2 already matched characters. Instead of having to start matching at position 1,
        we can start at our previous position (0) + table[4] (2) = 2. Indeed, If we look at text[2] and text[3], we see
        that it is equal to pattern[0] and pattern[1], respectively.
        The numbers in table tell us how many positions are already matched when an error occurs. In this case 2 
        characters of the next pattern were already matched. We can then immediately start matching for position 2 and 
        skip position 1 (as the pattern can not be found starting at position 1).
    Time complexity: O(len(p) + len(s)), we spend len(p) time to build the prefix-suffix table and we spend len(s) 
    time for the traversal on average.
    Space complexity: O(len(p)), our prefix-suffix table is going to be the length of the pattern string.
    """
    if not needle:
        return 0
    table = [0] * (len(needle) + 1)
    i, j = 0, -1
    table[0] = -1
    # Prepare roll-back table
    while i < len(needle):
        # Roll-back
        while j >= 0 and needle[i] != needle[j]:
            j = table[j]
        i, j = i + 1, j + 1
        table[i] = j
    i = j = 0
    while i < len(haystack):
        # Roll-back
        while j >= 0 and needle[j] != haystack[i]:
            j = table[j]
        i, j = i + 1, j + 1
        if j == len(needle):
            return i - len(needle)
    return -1


class Test(unittest.TestCase):
    data = [('hello', 'll', 2), ('aaaaa', 'bba', -1)]

    def test_str_str(self):
        for test_haystack, test_needle, result in self.data:
            self.assertEqual(result, str_str_v1(test_haystack, test_needle))
            self.assertEqual(result, str_str_v2(test_haystack, test_needle))


if __name__ == '__main__':
    unittest.main()