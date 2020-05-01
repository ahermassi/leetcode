""" Find the length of the longest substring T of a given string (consists of lowercase letters only) such that every
character in T appears no less than k times. """

from collections import defaultdict
import unittest2 as unittest


def longest_substring_v1(s, k):
    """ The intuition behind this solution is the following:
            Characters that occur less than k times can't be part of the longest valid substring
        We recursively split the given string on characters that do not occur at least k times (since they cannot be
        part of the longest valid substring).
        If this substring is shorter than k, then no characters in it can be repeated k times, therefore this substring
        and all substrings that could be formed from it are invalid, therefore return 0.
        Otherwise, count the frequency of characters in this substring. For every character in the frequency map, if
        this character occurs fewer than k times in this substring, we know that this character cannot be part of the
        longest valid substring and that the current substring is not valid. Hence, we will 'split' this substring on
        this character wherever it occurs and check the substrings formed by that split.
        If we arrive at the last statement, it means that every character in this substring occurs at least k times,
        then this is a valid substring, so return this substring's length.
        So the basic idea is to use those character whose frequency is than k as a 'wall' and divide the string into
        two parts and run recursion on the two parts.
    Time complexity: (N^2)
    Space complexity: O(N)
    """

    def divide(left, right):
        if right - left + 1 < k:
            return 0
        counter = defaultdict(int)
        for i in range(left, right + 1):
            counter[s[i]] += 1
        for c, count in counter.items():
            if count < k:
                for i in range(left, right + 1):
                    if s[i] == c:
                        before = divide(left, i - 1)
                        after = divide(i + 1, right)
                        return max(before, after)
        return right - left + 1

    return divide(0, len(s) - 1)


class Test(unittest.TestCase):
    data = [('aaabb', 3, 3), ('ababbc', 2, 5)]

    def test_longest_substring(self):
        for test_s, test_k, result in self.data:
            self.assertEqual(result, longest_substring_v1(test_s, test_k))


if __name__ == '__main__':
    unittest.main()
