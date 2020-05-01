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


def longest_substring_v2(s, k):
    """ This problem prompts us to use the two pointer technique, however it's quite difficult to decide the conditions
        to expand and shrink the window.
        How do we explore all possible solutions (substrings that satisfy given constraints) ?
        Find all substrings which have i = 1 unique character(s) and each character in the substring repeats at least
        k times.
        Find all substrings which have i = 2 unique character(s) and each character in the substring repeats at least
        k times.
        ....
        Find all substrings which have i = 26 unique character(s) and each character in the substring repeats at least
        k times.
        At i = 26, we're done. Take max of all the above valid substrings (by tracking with 'res' variable). That'll be
        our answer.
        We count the number of current unique letters 'unique', and the number of letters that have a count of k or
        more 'no_less_than_k' using a sliding window.
        How do we expand the window ? If the number of unique letters is less than or equal to i, we need to add a
        letter, so we increment the right pointer, and add the count of the right letter by 1. If the count is equal
        to 1, we know this is a new letter so we increment 'unique', and if its frequency is equal to k we increment
        'no_less_than_k'. Note that we need to keep expanding the window if unique <= i (less than or EQUAL) because we
        can still have a chance at getting more letters when unique == i. For example, s = 'aaabb'; If we stop at the
        first 'a' because unique == i == 1, we won't ever get to 'aaa' which is the answer.
        How do we shrink the window ? If the number of unique letters is greater than i, we need to remove a letter,
        so we increment the left pointer, and decrease the count of the left letter by 1. If the count is equal to 0,
        we decrement the number of unique letters since all instances of this letter are gone, and if its frequency is
        equal to k before removal we also decrement 'no_less_than_k'.
        The window is a valid candidate if the number of unique letters is i and the number of letters whose frequency
        is k or more 'no_less_than_k' is also i. So we take the maximum of valid candidates.
    Time complexity: O(N), the maximum number of unique characters is bounded by 26, which means that O(N) time
    complexity holds
    Space complexity: O(1)
    """
    n, res = len(s), 0
    for i in range(1, 27):
        counter = defaultdict(int)
        unique = no_less_than_k = 0
        left = right = 0
        while right < n:
            if unique <= i:
                c = s[right]
                if counter[c] == 0:
                    unique += 1
                counter[c] += 1
                if counter[c] == k:
                    no_less_than_k += 1
                right += 1
            else:
                c = s[left]
                if counter[c] == k:
                    no_less_than_k -= 1
                counter[c] -= 1
                if counter[c] == 0:
                    unique -= 1
                left += 1
            if unique == no_less_than_k == i:
                res = max(res, right - left)
    return res


class Test(unittest.TestCase):
    data = [('aaabb', 3, 3), ('ababbc', 2, 5)]

    def test_longest_substring(self):
        for test_s, test_k, result in self.data:
            self.assertEqual(result, longest_substring_v1(test_s, test_k))
            self.assertEqual(result, longest_substring_v2(test_s, test_k))


if __name__ == '__main__':
    unittest.main()
