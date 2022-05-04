""" Suppose an array sorted in ascending order is rotated at some pivot unknown to you beforehand.
(i.e., [0,1,2,4,5,6,7] might become [4,5,6,7,0,1,2]).
You are given a target value to search. If found in the array return its index, otherwise return -1.
You may assume no duplicate exists in the array.
Your algorithm's runtime complexity must be in the order of O(log n). """

import unittest2 as unittest

# Video explanation: https://www.youtube.com/watch?v=U8XENwh8Oy8


def search(nums, target):
    """ We have an ascending array, which is rotated at some pivot. Let's call the rotation the Inflection Point. (IP)
        One characteristic the inflection point holds is:
                arr[IP] > arr[IP + 1] and arr[IP] > arr[IP - 1]
        So if we had an array like: [7, 8, 9, 0, 1, 2, 3, 4] the inflection point, IP would be the number 9.

         One thing we notice is that values until the IP are ascending, and values from IP + 1 until the end of the
         array are also ascending (binary search, wink, wink). Also, the values in [0, IP] are always bigger than those
         in [IP + 1, n].

         The idea is that when rotating the array, there must be one half of the array that is still in sorted order.
         Perform standard binary search. Take an index in the middle as a pivot.

        If nums[mid] == target, the job is done, return mid.

        Now there could be two situations:

            1- Middle element is larger than the first element in the array, i.e. the part of array from the leftmost
                 element to the middle one is non-rotated.
                 If the target is located in that non-rotated part as well, go left: right = mid - 1.
                 Otherwise, go right: left = mid + 1.

            2- Middle element is smaller than the first element of the array, i.e. the rotation index is somewhere
                 between left and mid. That means that the part of array from the middle element to the rightmost one is
                 non-rotated.
                 If target is in that non-rotated part as well, go right: left = mid + 1.
                 Otherwise, go left: right = mid - 1.

        So we only need to be in the ordered, non-rotated half to determine whether the target value is in this area
        and which half is preserved.

        Formula: If a sorted array is shifted, and we examine the middle element, always one side will be sorted.

            1- Take the middle and compare with target, if matches return.

            2- If middle is bigger than left side, it means the subarray from left to mid is sorted/non-rotated.
                2a- If nums[left] <= target < nums[middle], search on left side: right = mid - 1
                2b- Left side is sorted, but target not in there, search on right side: left = mid + 1

            3- If middle is less than left side, it means the subarray from mid to right is sorted/non-rotated.
                3a- If nums[middle] < target <= nums[right], search on right side: left = mid + 1
                3b- Right side is sorted, but target not in there, search on left side: right = mid - 1

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
