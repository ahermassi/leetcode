""" Suppose an array sorted in ascending order is rotated at some pivot unknown to you beforehand.
(i.e., [0,0,1,2,2,5,6] might become [2,5,6,0,0,1,2]).
You are given a target value to search. If found in the array return true, otherwise return false.
This is a follow up problem to Search in Rotated Sorted Array, where nums may contain duplicates. """

import unittest2 as unittest


def search(nums, target):
    """ The idea is the same as the previous problem without duplicates, 33- Search in Rotated Sorted Array.
        When rotating the array, there must be one half of the array that is still in sorted order.
        Perform standard binary search. Take an index in the middle mid as a pivot.
        If nums[mid] == target, the job is done, return mid.
        Now there could be two situations:
            1- Middle element is larger than the first element in the array, i.e. the part of array from the first
               element to mid is non-rotated.
               If the target is in that non-rotated part as well, go left: right = mid - 1.
               Otherwise, go right: left = mid + 1.
            2- Middle element is smaller than the first element of the array, i.e. the rotation index is somewhere
               between 0 and mid. That means that the part of array from the middle element to the last one is
               non-rotated.
               If target is in that non-rotated part as well, go right: left = mid + 1.
               Otherwise, go left: right = mid - 1.
        The only difference is that, due to the existence of duplicates, we can have nums[left] == nums[mid]. In that
        case, the first half could be out of order (i.e. NOT in the ascending order, e.g. [3, 1, 2, 3, 3, 3, 3]), and
        we have to deal this case separately. mid is a floor of (left + right)/2, so it can be equal to left. We want
        to make sure that the equal sign in the condition nums[left] <= nums[mid] only happens when left == mid, so we
        have to remove the duplicates from the left.
        Consider this sorted array [1, 1, 1, 1, 1, 1,5], which is rotated to [1, 1, 5, 1, 1, 1, 1].
        Assume left = 0, mid = 3, target = 5. Therefore, the condition A[left] == A[mid] holds true, which leaves us
        with only two possibilities:
            1- All numbers between A[left] and A[mid] are all 1's.
            2- Different numbers (including our target) may exist between A[left] and A[mid].
        As we cannot determine which of the above is true, the best we can do is to move left one step forward and
        repeat the process again.
    Time complexity: O(logN) best case, O(N) worst case
    Space complexity: O(1)
    """
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return True
        if nums[left] < nums[mid]:  # Left half is sorted
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        elif nums[left] > nums[mid]:  # Right half is sorted
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
        else:  # nums[left] == nums[mid]
            left += 1
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
