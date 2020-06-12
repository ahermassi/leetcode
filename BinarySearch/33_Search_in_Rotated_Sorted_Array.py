""" Suppose an array sorted in ascending order is rotated at some pivot unknown to you beforehand.
(i.e., [0,1,2,4,5,6,7] might become [4,5,6,7,0,1,2]).
You are given a target value to search. If found in the array return its index, otherwise return -1.
You may assume no duplicate exists in the array.
Your algorithm's runtime complexity must be in the order of O(log n). """

import unittest2 as unittest


def search(nums, target):
    """ The idea is that when rotating the array, there must be one half of the array that is still in sorted order.
        Perform standard binary search. Take an index in the middle as a pivot.
        If nums[mid] == target, the job is done, return mid.
        Now there could be two situations:
            1- Middle element is larger than the first element in the array, i.e. the part of array from the first
               element to the middle one is non-rotated.
               If the target is in that non-rotated part as well, go left: right = mid - 1.
               Otherwise, go right: left = mid + 1.
            2- Middle element is smaller than the first element of the array, i.e. the rotation index is somewhere
               between 0 and mid. That means that the part of array from the middle element to the last one is
               non-rotated.
               If target is in that non-rotated part as well, go right: left = mid + 1.
               Otherwise, go left: right = mid - 1.
        So we only need to be in the ordered half to determine whether the target value is in this area and which half
        is preserved.
        Formula: If a sorted array is shifted, if we take the middle, always one side will be sorted.
            1- Take the middle and compare with target, if matches return.
            2- If middle is bigger than left side, it means left is sorted.
                2a- If nums[left] <= target < nums[middle], search on left side: right = middle - 1
                2b- Left side is sorted, but target not in here, search on right side: left = middle + 1
            3- If middle is less than right side, it means right is sorted.
                3a- If nums[middle] < target <= nums[right], search on right side: left = middle + 1
                3b- Right side is sorted, but target not in here, search on left side: right = middle - 1
    Time complexity: O(logN)
    Space complexity: O(1)
    """
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[left] <= nums[mid]:  # It's <= instead of < because when there's only two elements, 'mid' and 'left'
            # point to exactly the same element. Then we have to include = to make sure it covers this case.
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

    def test_search(self):
        for test_array, test_target, result in self.data:
            self.assertEqual(result, search(test_array, test_target))


if __name__ == '__main__':
    unittest.main()
