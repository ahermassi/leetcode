""" Given an unsorted array of integers, find the length of the longest increasing subsequence. """

import unittest as unittest


# Video explanation: https://www.youtube.com/watch?v=fV-TF4OvZpk
# Video explanation: https://youtu.be/cjWnW0hdF1Y
def length_of_lis_v1(nums):
    """ Let dp[i] be the length of the longest increasing subsequence that ends with the ith element, or nums[:i].

         The default answer is 1. Every element on its own is technically an increasing subsequence.

         We need a way to transition between states, such as dp[5] and dp[7]. Let's say we know dp[0], dp[1], and dp[2].
         How can we find dp[3] given this information? Well, since dp[2] represents the length of the longest increasing
         subsequence that ends with nums[2], if nums[3] > nums[2], then we can simply take the subsequence ending at =2
         and append nums[3] to it, increasing the length by 1. The same can be said for nums[0] and nums[1] if nums[3]
         is larger. Of course, we should try to maximize dp[3], so we need to check all 3. Formally, the recurrence
         relation is:

                    dp[i] = max(dp[j] + 1) for all j < i, where nums[j] < nums[i]

         At the end, the maximum out of all the dp[i]'s determines the final result.

        Example: nums = [-1, 3, 4, 5, 2, 8]
        At index 0 we always know that we can have a sub-sequence of length 1. In fact, at all positions the LIS can be
        at least length 1.
        We then look at index 1. We need to ask ourselves if the item at index 1 can lengthen the LIS found at index 0.
        We check if 3 is greater than -1... it is. Great. Index 1 can be tacked on, but should we?
        dp[1] = 1, dp[0] = 1. It makes sense because if we tack 3 onto the LIS we found for the sub-problem of just
        [-1], then at index 1 we will also have a LIS. So what we basically do is build a table and ask ourselves these
        questions all along the way.
        Each cell represents the answer to the sub-problem asked against the sub-sequence from index 0 to index i
        (including the element at index i).
    Time complexity: O(N^2)
    Space complexity: O(N)
    """
    n = len(nums)
    dp, max_len = [1] * n, 1
    for i in range(n):
        # We want to check if we can append the item at nums[i] to extend the Longest Increasing Subsequence built
        # from index j=0...i-1. We want to solve for dp[i] if the value at i is greater than the value at j
        for j in range(i):
            if nums[i] > nums[j]:
                # The value of dp[j] is the length of the LIS from 0...j, we conceptually 'append' the current element
                # to this LIS by adding 1 to that sub-problem answer, yielding a potentially new answer for LIS[0..i]
                dp[i] = max(dp[i], dp[j] + 1)
        max_len = max(max_len, dp[i])  # We have an answer for LIS[0...i]. Compare it with the best LIS length so far.
    return max_len


def length_of_lis_v2(nums):
    """ This approach is known as Patience Sorting.
        We try to build 'increasing_sub_sequence' where elements are sorted increasingly.
        We iterate over nums array. If the current element is greater than the largest (last) element in
        'increasing_sub_sequence', we simply append it. Otherwise, we determine the insertion index of the current
        element in 'increasing_sub_sequence' if we were to keep it sorted, using binary search. We eventually end up
        with a list of elements sorted increasingly whose length is the length of (one of) LIS in nums.
        Note: 'increasing_sub_sequence' array does not result in longest increasing sub-sequence, but length of
        'increasing_sub_sequence' array will give the length of LIS.
        Why is this correct ?
        When we replace increasing_sub_sequence[i] with current num, we don't change the length of answer, but we
        change the potential best candidate. Replacing increasing_sub_sequence[i] with the first element that is
        smaller than or equal to it increases our chance of extending the array because increasing_sub_sequence[i] is
        smaller than that element.
        So the main idea is:
            Use binary search to extend increasing sequence with larger numbers, or minimize existing values with
            smaller ones, so we can use larger numbers to extend it.
        Try to make each position's number as small as possible. The actual sequence only changes when we append a
        number, otherwise it's just a 'virtual change', meaning we don't change the current sequence, but we try to
        make each number small so we'll have a larger chance to append more numbers.
        For more details:
        https://leetcode.com/problems/longest-increasing-subsequence/discuss/74824/JavaPython-Binary-search-O(nlogn)-time-with-explanation
        Example: nums = [0, 8, 4, 12, 2]
        i = 0, increasing_sub_sequence = [0]
        i = 1, increasing_sub_sequence = [0, 8]
        i = 2, increasing_sub_sequence = [0, 4]
        i = 3, increasing_sub_sequence = [0, 4, 12]
        i = 4, increasing_sub_sequence = [0 , 2, 12] which is not the longest increasing sub-sequence, but its length
        is the length of LIS.
    Time complexity: O(N logN), binary search takes logN time and it is called N times
    Space complexity: O(N)
    """

    def find_insertion_index(val):
        left, right = 0, len(increasing_subsequence) - 1
        while left <= right:
            mid = (left + right) // 2
            if increasing_subsequence[mid] == val:
                return mid
            if increasing_subsequence[mid] < val:
                left = mid + 1
            else:
                right = mid - 1
        return left

    increasing_subsequence = []
    for num in nums:
        index = find_insertion_index(num)
        if index == len(increasing_subsequence):
            increasing_subsequence.append(num)
        else:
            increasing_subsequence[index] = num
    return len(increasing_subsequence)


class Test(unittest.TestCase):
    data = [([10, 9, 2, 5, 3, 7, 101, 18], 4)]

    def test_length_of_LIS(self):
        for test_array, result in self.data:
            self.assertEqual(result, length_of_lis_v1(test_array))
            self.assertEqual(result, length_of_lis_v2(test_array))


if __name__ == '__main__':
    unittest.main()
