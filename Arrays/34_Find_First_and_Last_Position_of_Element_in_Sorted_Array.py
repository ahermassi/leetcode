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


def search_range_v2(nums, target):
    """ Another version of two binary searches.
        Here, helper function 'search' is a simple binary search, telling us the first index where we could insert a
        number n into nums to keep it sorted (i.e first position). Thus, if nums contains target, we can find the first
        occurrence with search(target). We do that, and if target isn't actually there, then we return [-1, -1].
        Otherwise, we ask search(target + 1), which tells the first index where we could insert (target + 1), which of
        course is one index after the last index containing target, so all we have left to do is subtract 1.
    Time complexity: O(logN)
    Space complexity: O(1)
    """
    def search(target):
        left, right = 0, len(nums)
        while left < right:
            mid = (left + right) // 2
            if nums[mid] >= target:
                right = mid
            else:
                left = mid + 1
        return left

    left = search(target)
    return [left, search(target + 1) - 1] if target in nums[left:left + 1] else [-1, -1]


class Test(unittest.TestCase):
    data = [([5, 7, 7, 8, 8, 10], 8, [3, 4]), ([5, 7, 7, 8, 8, 10], 6, [-1, -1])]

    def test_can_finish(self):
        for test_array, test_target, result in self.data:
            self.assertEqual(result, search_range_v1(test_array, test_target))
            self.assertEqual(result, search_range_v2(test_array, test_target))


if __name__ == '__main__':
    unittest.main()
