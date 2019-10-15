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


class Test(unittest.TestCase):
    data = [(7, [2, 3, 1, 2, 4, 3], 2)]

    def test_min_sub_array_len(self):
        for test_sum, test_nums, result in self.data:
            self.assertEqual(result, min_sub_array_len_v1(test_sum, test_nums))


if __name__ == '__main__':
    unittest.main()
