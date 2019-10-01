""" Given an array of integers nums sorted in ascending order, find the starting and ending position of a given target
value.
Your algorithm's runtime complexity must be in the order of O(log n).
If the target is not found in the array, return [-1, -1]. """

import unittest2 as unittest


def search_range_v1(nums, target):
    """ Modified binary search done twice to find both left and right positions. The tricky part is handling left and
        right pointers when a match is found.
    Time complexity: O(logN)
    Space complexity: O(1)
    """
    def binary_search_left(nums, target):
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if target > nums[mid]:
                left = mid + 1
            else:
                right = mid - 1
        return left

    def binary_search_right(nums, target):
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if target >= nums[mid]:
                left = mid + 1
            else:
                right = mid - 1
        return right

    left, right = binary_search_left(nums, target), binary_search_right(nums, target)
    return [left, right] if left <= right else [-1, -1]


class Test(unittest.TestCase):
    data = [([5, 7, 7, 8, 8, 10], 8, [3, 4]), ([5, 7, 7, 8, 8, 10], 6, [-1, -1])]

    def test_can_finish(self):
        for test_array, test_target, result in self.data:
            self.assertEqual(result, search_range_v1(test_array, test_target))


if __name__ == '__main__':
    unittest.main()
