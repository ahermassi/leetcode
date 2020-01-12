""" Given an unsorted array of integers, find the length of longest increasing subsequence. """

import unittest as unittest


# Watch: https://www.youtube.com/watch?v=fV-TF4OvZpk

def length_of_lis_v1(nums):
    """ Let dp[i] be the length of the longest increasing sub-sequence ending at and including index i of the original
        nums array.
        Default answer is 1. A single item is neither increasing or decreasing.
        In order to find out dp[i], we need to try to append the current element nums[i] in every possible increasing
        sub-sequence upto the (i−1)th index(including the (i−1)th index), such that the new sequence formed by adding
        the current element is also an increasing sub-sequence. Therefore:
            dp[i] = max(dp[j] + 1 for 0 <= j < i)
        At the end, the maximum out of all the dp[i]'s determines the final result:
            LIS_length = max(dp[i] for 0 <= i < n)
        Example: nums = [-1, 3, 4, 5, 2, 8]
        At index 0 we always know that we can have a sub-sequence of length 1. In fact, at all positions the LIS can be
        at least length 1.
        We then look at index 1. We need to ask ourselves if the item at index 1 can lengthen the LIS found at index 0.
        We check if 3 is greater than or equal to -1... it is. Great. index 1 can be tacked on, but should we?
        dp[1] = 1, dp[0] = 1. It makes sense because if we tack 3 onto the LIS we found for the sub-problem of just
        [-1] then at index 1 we will also have a LIS. So what we basically do is build a table and ask ourselves these
        questions all along the way.
        Each cell represents the answer to the sub-problem asked against the sub-sequence from index 0 to index i
        (including the element at index i).
    Time complexity: O(N^2)
    Space complexity: O(N)
    """
    if not nums:
        return 0
    n = len(nums)
    dp, max_len = [1] * n, 1
    for i in range(1, n):
        # We aim to see if we can append the item at nums[i] to extend the Longest Increasing Sub-sequence achieved
        # from index 0...j. We want to solve for dp[i] if the value at i is greater than the value at j
        for j in range(i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + 1)  # The value of dp[j] is the length of the LIS from 0...j, we conceptually
                # 'append' this item to that LIS by adding 1 to that sub-problem answer, yielding a potentially new
                # answer for LIS[0..i]
        max_len = max(max_len, dp[i])  # We now have an answer for LIS[0...i]. Compete it against the best LIS length
        # found so far.
    return max_len


def length_of_LIS_v2(nums):
    """ This approach is known as Patience Sorting.
        We try to build increasing_subsequence where elements are sorted increasingly. We iterate over nums array. If
        the current element in greater than the largest (last) element in increasing_subsequence, we simply append it.
        Otherwise, we determine the insertion index of the current element in increasing_subsequence if we were to keep
        increasing_subsequence sorted, using binary search. We eventually end up with a list of elements sorted
        increasingly whose length is the length of (one of) longest increasing subsequence in nums.
        For an explanation:
        https://leetcode.com/problems/longest-increasing-subsequence/discuss/74824/JavaPython-Binary-search-O(nlogn)-time-with-explanation
    Time complexity: O(N logN), binary search takes logN time and it is called N times
    Space complexity: O(N)
    """
    increasing_subsequence = [0] * len(nums)
    size = 0
    for x in nums:
        # Binary search
        left, right = 0, size
        while left != right:
            mid = (left + right) // 2
            if increasing_subsequence[mid] < x:
                left = mid + 1
            else:
                right = mid
        increasing_subsequence[left] = x
        size = max(left + 1, size)
    return size


class Test(unittest.TestCase):
    data = [([10, 9, 2, 5, 3, 7, 101, 18], 4)]

    def test_length_of_LIS(self):
        for test_array, result in self.data:
            self.assertEqual(result, length_of_LIS_v1(test_array))
            self.assertEqual(result, length_of_LIS_v2(test_array))


if __name__ == '__main__':
    unittest.main()
