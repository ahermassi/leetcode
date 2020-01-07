""" Given an array of integers nums sorted in ascending order, find the starting and ending position of a given target
value.
Your algorithm's runtime complexity must be in the order of O(log n).
If the target is not found in the array, return [-1, -1]. """

import unittest2 as unittest


def search_range(nums, target):
    """ Modified binary search executed twice to find both left and right positions. The tricky part is handling left
        and right pointers when a match is found.
        Example:
                0  1  2  3  4  5  6  7  8  9  10 11 12
        nums = [1, 2, 2, 3, 4, 4, 5, 5, 5, 6, 7, 9, 9], target = 5

        left = 0, right = 12, mid = 6: notice here that nums[mid] == target. However, right = mid - 1. By doing that
        and narrowing down the search range, we're essentially locating the first element LESS than target, similar to
        bisect_left. When 'left' steps over 'right', nums[left] is the first occurrence of target.
        left = 0, right = 5, mid = 2
        left = 3, right = 5, mid = 4
        left = 5, right = 5, mid = 5
        left = 6, right = 5 -> return left = 6

        left = 0, right = 12, mid = 6: notice here that nums[mid] == target. However, left = mid + 1. By doing that
        and narrowing down the search range, we're essentially locating the first element GREATER than target, similar
        to bisect_right. When 'right' steps over 'left', nums[right] is the first occurrence of target.
        left = 7, right = 12, mid = 9
        left = 7, right = 8, mid = 7
        left = 8, right = 8, mid = 8
        left = 9, right = 8 -> return right = 8

    Time complexity: O(logN)
    Space complexity: O(1)
    """
    def binary_search_left():
        left, right = 0, len(nums) - 1
        while left < right:
            mid = (left + right) // 2
            if target > nums[mid]:
                left = mid + 1
            else:
                right = mid - 1
        return left

    def binary_search_right():
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        return right

    left, right = binary_search_left(), binary_search_right()
    return [left, right] if left <= right else [-1, -1]


class Test(unittest.TestCase):
    data = [([5, 7, 7, 8, 8, 10], 8, [3, 4]), ([5, 7, 7, 8, 8, 10], 6, [-1, -1])]

    def test_search_range(self):
        for test_array, test_target, result in self.data:
            self.assertEqual(result, search_range(test_array, test_target))


if __name__ == '__main__':
    unittest.main()
