""" Given an array of positive integers nums and a positive integer target, return the minimal length of a subarray
whose sum is greater than or equal to target. If there is no such subarray, return 0 instead. """

import unittest2 as unittest


# Refer to this thread for a summary of sliding windows techniques:
# https://leetcode.com/problems/minimum-window-substring/discuss/26808/Here-is-a-10-line-template-that-can-solve-most-'substring'-problems

# Video explanation: https://www.youtube.com/watch?v=aYqYMIqZx5s
def min_sub_array_len_v1(target, nums):
    """ Use 2 pointers, one for the start and another for the end of the current subarray (window) and make optimal
         moves as to keep the sum greater than or equal to 'target' as well as maintain the smallest subarray size
         possible.

        Initialize the left pointer 'left', the right pointer 'right', and the window sum 'cur_sum' to 0 .
        Iterate over nums array:

            - Add nums[right] to 'cur_sum'

            - While 'cur_sum' is greater than or equal to 'target':

                * Update res = min(res ,right - left + 1), where (right - left + 1) is the size of the current window
                * It means that the element pointed at by the leftmost index can safely be discarded, since the minimum
                   subarray starting with this index with sum ≥ target has been found
                * Subtract nums[left] from 'cur_sum' and increment 'left' to shrink the window

        Since the given array contains only positive integers, the subarray sum can only increase by including more
        elements. Therefore, we don't have to include more elements once the current subarray reached a large
        enough sum.

        The essential idea is if a subarray starts at 'left', then try to get the minimum length subarray by adding
        elements to it. Once the sum is over 'target', it means we just found the minimum subarray starting at 'left'.
        In this case, instead of moving 'left' forward one step, we can just discard any elements starting from leftmost
        element of the current minimum subarray until the sum becomes less than 'target'.

    Time complexity: O(N), each element can be visited at most twice, once by the right pointer and (at most) once by
    the left pointer.
    Space complexity: O(1)
    """
    n, res = len(nums), float('inf')
    left = right = cur_sum = 0
    while right < n:
        cur_sum += nums[right]
        while cur_sum >= target:
            res = min(res, right - left + 1)
            cur_sum -= nums[left]
            left += 1
        right += 1
    return res if res != float('inf') else 0


def min_sub_array_len_v2(target, nums):
    """ We cannot sort the input array as the current order actually matters. How do we get an ordered array then?

         Since all the numbers are positive, the cumulative sum must be strictly increasing. Then, a subarray sum can
        be expressed as the difference between two cumulative sums. Hence, given the start index of the cumulative sum
        subarray, the other end index can be searched using binary search.

    Time complexity: O(N logN), the time required is O(N) for iteration over the array and O(logN) for finding the
    subarray for each index using binary search
    Space complexity: O(1)
    """

    def find_left(left, right, cur_sum):
        while left <= right:
            mid = (left + right) // 2
            if cur_sum - prefix_sum[mid] >= target:
                # The sum between indices 'mid' and 'right' is >= target
                left = mid + 1
            else:
                right = mid - 1
        # This is the biggest index such as nums[left:right+1] has a sum >= target, thus a min length subarray
        return left

    n, res = len(nums), float('inf')
    prefix_sum = [0] * n
    prefix_sum[0] = nums[0]
    for i in range(1, n):
        prefix_sum[i] += prefix_sum[i - 1] + nums[i]  # Cumulative sum, resulting in a sorted nums array
    left = right = 0
    while right < n:
        if prefix_sum[right] >= target:
            # If cumulative sum up to index 'right' is >= target, then it should be the right end of a
            # subarray that satisfies the problem property. Use binary search to find its left end.
            left = find_left(left, right, prefix_sum[right])
            # Note that we don't initialize 'left' at each iteration. As 'right' keeps moving forward, the cumulative
            # sum keeps increasing, and 'left' is the largest index (guaranteeing a min length subarray) from previous
            # iterations, so it's a waste of time to initialize it
            res = min(res, right - left + 1)
        right += 1
    return res if res != float('inf') else 0


class Test(unittest.TestCase):
    data = [(7, [2, 3, 1, 2, 4, 3], 2)]

    def test_min_sub_array_len(self):
        for test_sum, test_nums, result in self.data:
            self.assertEqual(result, min_sub_array_len_v1(test_sum, test_nums))
            self.assertEqual(result, min_sub_array_len_v2(test_sum, test_nums))


if __name__ == '__main__':
    unittest.main()
