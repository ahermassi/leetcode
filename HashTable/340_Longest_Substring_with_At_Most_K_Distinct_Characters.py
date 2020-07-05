""" Given a string, find the length of the longest substring T that contains at most k distinct characters. """

from collections import defaultdict
import unittest2 as unittest


def length_of_longest_substring_k_distinct_v1(s, k):
    """ Similar to 159- Longest Substring with At Most Two Distinct characters.
    Time complexity: O(N), for the best case when input string contains no more than k distinct characters, O(N * k)
    for the worst case when the input string contains N distinct characters. In that case, at each step we use O(k)
    time to find a minimum value in the hash map with k elements.
    Space complexity: O(k)
    """
    last_occ_index, start, res = {}, 0, 0
    for i, c in enumerate(s):
        last_occ_index[c] = i
        if len(last_occ_index) > k:
            removal_index = min(last_occ_index.values())
            del last_occ_index[s[removal_index]]
            start = removal_index + 1
        res = max(res, i - start + 1)
    return res


def length_of_longest_substring_k_distinct_v2(s, k):
    """ We can achieve linear time complexity by storing the frequency of each character instead of its rightmost index.
        Run a sliding window across the string, using a hash map to track the characters present and the occurrence
        count of each. If the sliding window includes a character that brings the distinct char count above k, then
        close the window until the distinct char count is back to k. At each step, compute whether the window size is
        bigger than the current max.
    Time complexity: O(N)
    Space complexity: O(1), at most 256 characters can be stored in the frequency map
    """
    counter = defaultdict(int)
    left, right, distinct, n, res = 0, 0, 0, len(s), 0
    while right < n:
        if counter[s[right]] == 0:
            distinct += 1
        counter[s[right]] += 1
        while distinct > k:
            counter[s[left]] -= 1
            if counter[s[left]] == 0:
                distinct -= 1
            left += 1
        res = max(res, right - left + 1)
        right += 1
    return res


class Test(unittest.TestCase):
    data = [('eceba', 2, 3), ('aa', 1, 2)]

    def test_length_of_longest_substring_k_distinct(self):
        for test_s, test_k, result in self.data:
            self.assertEqual(result, length_of_longest_substring_k_distinct_v1(test_s, test_k))
            self.assertEqual(result, length_of_longest_substring_k_distinct_v2(test_s, test_k))


if __name__ == '__main__':
    unittest.main()
