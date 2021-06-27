""" Given a string, find the length of the longest substring T that contains at most k distinct characters. """

from collections import defaultdict
import unittest2 as unittest


def length_of_longest_substring_k_distinct_v1(s, k):
    """ Similar to 159- Longest Substring with At Most Two Distinct characters.
        To solve the problem in one pass, let's use sliding window approach with two set pointers left and right
        serving as the window boundaries.
        The idea is to set both pointers in the position 0 and then move right pointer to the right while the window
        contains not more than two distinct characters. If at some point we've got 3 distinct characters, let's move
        left pointer to keep not more than 2 distinct characters in the window.
        Basically that's the algorithm : to move sliding window along the string, to keep not more than 2 distinct
        characters in the window, and to update max substring length at each step.
        Let's use for this purpose a hash map containing all characters in the sliding window as keys and their
        rightmost positions as values. At each moment, this hash map could contain not more than 3 elements.
        The key is to store the last occurrence of each character as the value in the hash map. This way, whenever the
        size of the hash map exceeds 2, we can traverse through the map to find the character with the smallest
        rightmost index and remove that character from our map. Since the range of characters is constrained, we should
        be able to find this character in constant time.
        This solution is well suited for the case of a super long string, as memory may not be large enough to load the
        entire string, so we'll treat it as a string stream. This algorithm stores each char's rightmost position, and
        every time we want to drop one char from current window, we can simply drop the char with smallest(leftmost)
        rightmost position.
    Time complexity: O(N), for the best case when input string contains no more than k distinct characters, O(N * k)
    for the worst case when the input string contains N distinct characters. In that case, at each step we use O(k)
    time to find a minimum value in the hash map with k elements. However, the hash map will have at most 256
    characters (or whatever the alphabet size used for constructing the string is - 256 for an ASCII string). Since
    there is a fixed number of characters, therefore there is a fixed number of key-value pairs in the map. Finding
    min with fixed number of characters will be 256 ops in the worst case which is as good as O(1). So overall time
    complexity of this solution should be O(N) just due to the outermost loop
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
