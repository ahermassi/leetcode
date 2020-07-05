""" Given a string, find the length of the longest substring T that contains at most k distinct characters. """

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


class Test(unittest.TestCase):
    data = [('eceba', 2, 3), ('aa', 1, 2)]

    def test_length_of_longest_substring_k_distinct(self):
        for test_s, test_k, result in self.data:
            self.assertEqual(result, length_of_longest_substring_k_distinct_v1(test_s, test_k))


if __name__ == '__main__':
    unittest.main()
