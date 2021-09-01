""" Given an array nums and a target value k, find the maximum length of a sub-array that sums to k. If there isn't one,
return 0 instead. """

import unittest2 as unittest


def max_sub_array_len(nums, k):
    """ How many possible sub-arrays are there in an array of size n? There is 1 sub-array with length n, 2 sub-arrays
        with length (n - 1), 3 sub-arrays with length (n - 2) and so on. This means there are n + (n - 1) + (n - 2) +
        ... + 2 + 1 = n * (n + 1) / 2 possible sub-arrays. This question has bounds of n <= 2 * 10^5, which means
        naively checking every possible sub-array could mean looking at over 20 billion sub-arrays. This is far too
        slow and we need a better solution.
        Similarly to 560- Subarray Sum Equals K, we use a hash map 'prefix_sum' to store the sum of all elements before
        index i as key, and i as value. For each i, we check not only the current sum but also (cur_sum - k) to see if
        there is a previous sum such that cur_sum - previous_sum = k.
        The idea is that if there is a number in the hash map where (cur_sum - k) equals to a number already in the
        map, there must be a contiguous section from that point to current index i where the sum of all items is k.
        The distance between these two points is the length of the sub array and is a candidate for our answer.
        Let's say we've iterated to index 5 (randomly chosen) and our sum from index 0 to 5 so far is 7, and k is 3.
        (cur_sum - k) in this case is 4. What prefix_sum[cur_sum - k] returns is the index where the sum of every
        element up to that index from index 0 is (cur_sum - k), or (7 - 4) == 3, in our example. Let's say that the
        index returned is 2. So knowing that at index 2 the total sum is 4, and at index 5 the total sum is 7, that
        means the elements between index 2 and index 5 incremented the total sum by 3, or k.
        If we run into a duplicate (which is possible because of negative numbers), we should not update the index in
        the hash map because we want the longest sub-array, so we want to keep the index as far to the left as
        possible. For example, if we had the input nums = [1, -1, 1, 3] and k = 4, then the longest sub-array would be
        the entire array. The prefix sum at each step would be [1, 0, 1, 4]. As we can see, we always want to pick the
        leftmost index to maximize length. Therefore, when we get to the third element and see that 1 already exists in
        the hash map, we should not replace the value with the current index.
        Note that we need to initialize the hash map to {0: -1} to account for the case when the prefix sum is equal
        to k. Take the example nums = [1, -1, 5, -2 , 3] and k = 3. When we use prefix_sum = {0: -1} at the start,
        then at i = 1, cur_sum = 0. When we reach i = 3, cur_sum = 3. cur_sum - k = 0 and
        i - prefix_sum[cur_sum - k] = 4 (which is the longest sub array length that totals k). If instead
        prefix_sum = {} at the start, prefix_sum[0] gets updated to i = 1 and at i = 3, i - prefix_sum[cur_sum - k] = 2.
    Time complexity: O(N)
    Space complexity: O(N), the hash map can potentially hold as many key-value pairs as there are numbers in nums. An
    example of this is when there are no negative numbers in the array.
    """
    prefix_sum, cur_sum, res = {0: -1}, 0, 0
    for i, num in enumerate(nums):
        cur_sum += num
        if cur_sum - k in prefix_sum:
            res = max(res, i - prefix_sum[cur_sum - k])
        if cur_sum not in prefix_sum:
            prefix_sum[cur_sum] = i
    return res


class Test(unittest.TestCase):
    data = [([1, -1, 5, -2, 3], 3, 4), ([-2, -1, 2, 1], 1, 2)]

    def test_max_sub_array_len(self):
        for test_nums, test_k, result in self.data:
            self.assertEqual(result, max_sub_array_len(test_nums, test_k))


if __name__ == '__main__':
    unittest.main()
