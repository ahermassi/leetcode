""" Given an array of n positive integers and a positive integer s, find the minimal length of a contiguous sub array
of which the sum ≥ s. If there isn't one, return 0 instead. """

import unittest2 as unittest


# Refer to this thread for a summary of sliding windows techniques:
# https://leetcode.com/problems/minimum-window-substring/discuss/26808/Here-is-a-10-line-template-that-can-solve-most-'substring'-problems

def min_sub_array_len_v1(s, nums):
    """ Keep 2 pointers, one for the start and another for the end of the current sub array (window) and make optimal
        moves so as to keep the sum greater than s as well as maintain the lowest size possible.
        Initialize the left pointer 'left', the right pointer 'right', and the window sum 'cur_sum' to 0 .
        Iterate over nums array:
            - Add nums[right] to current 'cur_sum'
            - While 'cur_sum' is greater than or equal to s:
                * Update res = min(res ,right - left + 1), where (right - left + 1) is the size of current window
                * It means that the first index can safely be incremented, since the minimum sub array starting with
                  this index with sum ≥ s has been achieved
                * Subtract nums[left] from 'cur_sum' and increment 'left' to make the window smaller
        Since the given array contains only positive integers, the sub-array sum can only increase by including more
        elements. Therefore, we don't have to include more elements once the current sub-array already has a sum large
        enough.
        The essential idea is if a sub-array starts at 'left', then try to get min length sub-array by adding elements
        into it. Once the sum is over s, then it means we just found the min sub-array starting at 'left'. In this case,
        instead of moving forward 'left' one step, we can just subtract any elements starting from first element of the
        current min sub-array till the sum is less than s. Min length of sub-arrays starting at the updating 'left'
        index are updated during the subtraction.
    Time complexity: O(N), each element can be visited at most twice, once by the right pointer and (at most) once by
    the left pointer.
    Space complexity: O(1)
    """
    n, res = len(nums), float('inf')
    left = right = cur_sum = 0
    while right < n:
        cur_sum += nums[right]
        while cur_sum >= s:
            res = min(res, right - left + 1)
            cur_sum -= nums[left]
            left += 1
        right += 1
    return res if res != float('inf') else 0


def min_sub_array_len_v2(s, nums):
    """ We cannot sort the input array as the current order actually matters. How do we get an ordered array then?
        Since all elements are positive, the cumulative sum must be strictly increasing. Then, a sub-array sum can
        expressed as the difference between two cumulative sums. Hence, given a start index for the cumulative sum
        array, the other end index can be searched using binary search.
    Time complexity: O(N logN), the time required is O(N) for iteration over the array and O(logN) for finding the
    sub array for each index using binary search
    Space complexity: O(1)
    """

    def find_left(left, right, cur_sum):
        while left <= right:
            mid = (left + right) // 2
            if cur_sum - nums[mid] >= s:  # The sum between indices 'mid' and 'right' is >= s
                left = mid + 1
            else:
                right = mid - 1
        return left  # This is the largest index such as nums[left:right+1] has a sum >= s, thus a min length sub-array

    n, res = len(nums), float('inf')
    for i in range(1, n):
        nums[i] += nums[i - 1]  # Cumulative sum, resulting in a sorted nums array
    left = 0
    for right in range(n):
        if nums[right] >= s:  # If cumulative sum up to index 'right' is >= s, then it should be the right end of a
            # sub array that satisfies the problem property. Use binary search to find its left end.
            left = find_left(left, right, nums[right])  # Note that we don't initialize 'left' at each iteration.
            # As 'right' keeps moving forward, the cumulative sum keeps increasing, and 'left' is the largest index
            # (guaranteeing a min length sub array) from previous iterations, so it's a waste of time to initialize it
            res = min(res, right - left + 1)
    return res if res != float('inf') else 0


class Test(unittest.TestCase):
    data = [(7, [2, 3, 1, 2, 4, 3], 2)]

    def test_min_sub_array_len(self):
        for test_sum, test_nums, result in self.data:
            self.assertEqual(result, min_sub_array_len_v1(test_sum, test_nums))
            self.assertEqual(result, min_sub_array_len_v2(test_sum, test_nums))


if __name__ == '__main__':
    unittest.main()
