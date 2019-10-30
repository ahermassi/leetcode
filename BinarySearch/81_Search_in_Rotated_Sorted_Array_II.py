""" Suppose an array sorted in ascending order is rotated at some pivot unknown to you beforehand.
(i.e., [0,0,1,2,2,5,6] might become [2,5,6,0,0,1,2]).
You are given a target value to search. If found in the array return true, otherwise return false.
This is a follow up problem to Search in Rotated Sorted Array, where nums may contain duplicates. """

import unittest2 as unittest


def search(nums, target):
    """ The idea is the same as the previous one without duplicates, 33- Search in Rotated Sorted Array.
        The idea is that when rotating the array, there must be one half of the array that is still in sorted order.
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
        The only difference is that due to the existence of duplicates, we can have nums[left] == nums[mid] and in that
        case, the first half could be out of order (i.e. NOT in the ascending order, e.g. [3 1 2 3 3 3 3]) and we have
        to deal this case separately. In this case, we move the left pointer forward until it's no longer equal to mid
        value. Mid is a floor of (left + right)/2, so it can be equal to 'left'. We want to make sure that the equal
        sign in condition nums[left] <= nums[mid] only happens when left = mid, so we have to remove the duplicates for
        the left. However for the right, it's not necessary, and it can make the calculation slower. For example,
        find 2 in [0, 1, 2, 3, 3, 3, 3, 3, 3, 3]; all the 3s can be skipped in a O(logN) manner if we don't do
        right -=1, but we you do, it result in O(N).
    Time complexity: O(logN) best case, O(N) worst case
    Space complexity: O(1)
    """
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return True
        while nums[left] == nums[mid] and left != mid:
            left += 1
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return False


class Test(unittest.TestCase):
    data = [
        ([2, 5, 6, 0, 0, 1, 2], 0, True),
        ([2, 5, 6, 0, 0, 1, 2], 3, False)
    ]

    def test_search(self):
        for test_array, test_target, result in self.data:
            self.assertEqual(result, search(test_array, test_target))


if __name__ == '__main__':
    unittest.main()
