""" Suppose an array sorted in ascending order is rotated at some pivot unknown to you beforehand.
(i.e., [0,1,2,4,5,6,7] might become [4,5,6,7,0,1,2]).
You are given a target value to search. If found in the array return its index, otherwise return -1.
You may assume no duplicate exists in the array.
Your algorithm's runtime complexity must be in the order of O(log n). """

import unittest2 as unittest


def search(nums, target):
    """ The idea is that when rotating the array, there must be one half of the array that is still in sorted order.
        Perform standard binary search. Take an index in the middle mid as a pivot.
        If nums[mid] == target, the job is done, return mid.
        Now there could be two situations:
            1- Pivot element is larger than the first element in the array, i.e. the part of array from the first
               element to the pivot one is non-rotated.
               If the target is in that non-rotated part as well: go left: end = mid - 1.
               Otherwise: go right: start = mid + 1.
            2- Pivot element is smaller than the first element of the array, i.e. the rotation index is somewhere
               between 0 and mid. That means that the part of array from the pivot element to the last one is
               non-rotated.
               If target is in that non-rotated part as well: go right: start = mid + 1.
               Otherwise: go left: end = mid - 1.
    """
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[left] <= nums[mid]:  # It's <= instead of < because when there's only two elements, the mid and low
            # point to exactly the same element. Then we have to include = to make sure it covers this situation.
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1


class Test(unittest.TestCase):
    data = [
        ([4, 5, 6, 7, 0, 1, 2], 0, 4),
        ([4, 5, 6, 7, 0, 1, 2], 3, -1)
    ]

    def test_two_sum(self):
        for test_array, test_target, result in self.data:
            self.assertEqual(result, search(test_array, test_target))


if __name__ == '__main__':
    unittest.main()
