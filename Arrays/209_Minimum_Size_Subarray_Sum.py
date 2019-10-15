""" Given an array of n positive integers and a positive integer s, find the minimal length of a contiguous sub array of
which the sum ≥ s. If there isn't one, return 0 instead. """

import unittest2 as unittest


def min_sub_array_len_v1(s, nums):
    """ Keep 2 pointers, one for the start and another for the end of the current sub array (window) and make optimal
        moves so as to keep the sum greater than s as well as maintain the lowest size possible.
        Initialize left pointer 'window_left' to 0 and sum 'window_sum' to 0 .
        Initialize right pointer 'window_right' to -1 so as first move makes window_left == window_right (1-element
        window)
        Iterate over the nums:
            - Add nums[i] to sum
            - While sum is greater than or equal to s:
                * Update res = min(res ,right - left + 1), where (right - left + 1) is the size of current window
                * It means that the first index can safely be incremented, since, the minimum sub array starting with
                    this index with sum ≥ s has been achieved
                * Subtract nums[left] from sum and increment left to make the window smaller
    Time complexity: O(N), each element can be visited at most twice, once by the right pointer and (at most) once by
    the left pointer.
    Space complexity: O(1)
    """
    window_left = window_sum = 0
    window_right = -1
    res = float('inf')
    for num in nums:
        window_sum += num
        window_right += 1
        while window_sum >= s:
            res = min(res, window_right - window_left + 1)
            window_sum -= nums[window_left]
            window_left += 1
    return res if res != float('inf') else 0


def min_sub_array_len_v2(s, nums):
    """ Use nums[i] store the sum of nums from 0 to i, then nums is a sorted array, and then we can use binary search.
        Then, a sub array sum can expressed as the difference between two cumulative sum. Hence, given a start index
        for the cumulative sum array, the other end index can be searched using binary search.
    Time complexity: O(N logN), the time required is O(N) for iteration over the array and O(logN) for finding the
    sub array for each index using binary search.
    Space complexity: O(1)
    """

    def find_left(left, right, target):
        while left < right:
            mid = (left + right) // 2
            if target - nums[mid] >= s:
                left = mid + 1
            else:
                right = mid
        return left

    res = float('inf')
    for i in range(1, len(nums)):  # Cumulative sum, resulting in a sorted nums array
        nums[i] += nums[i - 1]
    left = 0
    for i, num in enumerate(nums):
        if num >= s:  # If cumulative sum up to this index i is greater than s, then i should be the right end of a
            # sub array that satisfies the problem property. Use binary search to find its left end.
            left = find_left(left, i, num)
            res = min(res, i - left + 1)
    return res if res != float('inf') else 0


class Test(unittest.TestCase):
    data = [(7, [2, 3, 1, 2, 4, 3], 2)]

    def test_min_sub_array_len(self):
        for test_sum, test_nums, result in self.data:
            self.assertEqual(result, min_sub_array_len_v1(test_sum, test_nums))
            self.assertEqual(result, min_sub_array_len_v2(test_sum, test_nums))


if __name__ == '__main__':
    unittest.main()
