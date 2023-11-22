""" Suppose an array sorted in ascending order is rotated at some pivot unknown to you beforehand.
(i.e., [0,1,2,4,5,6,7] might become [4,5,6,7,0,1,2]).
You are given a target value to search. If found in the array return its index, otherwise return -1.
You may assume no duplicate exists in the array.
Your algorithm's runtime complexity must be in the order of O(log n). """

import unittest2 as unittest

# Video explanation: https://www.youtube.com/watch?v=U8XENwh8Oy8


def search_v1(nums, target):
    """ Let's take a step back and consider a regular binary search. Why are we able to confidently discard half of the
         array after comparing target with the middle value nums[mid]? The reason is that both halves of the array are
         sorted. Hence, if target is less than the middle value, it's assured to be smaller than every value in the
         right half. If target is larger than the middle value, it's guaranteed to be larger than every value in the
         left half. Therefore, we can safely discard one half of nums in either case.

         However, a rotated sorted array may not possess this characteristic – we can't determine whether target is
         definitively not in the array just by comparing boundary values.

        We have an ascending array, which is rotated at some pivot. Let's call the index where the rotation occurs the
        Inflection Point (IP).
        One characteristic the inflection point holds is:

                arr[IP] > arr[IP + 1] and arr[IP] > arr[IP - 1]

        So if we had an array like: [7, 8, 9, 0, 1, 2, 3, 4] the inflection point, IP would be the number 9.

         One thing we notice is that values until the IP are ascending, and values from IP + 1 until the end of the
         array are also ascending (binary search, wink, wink). Also, the values in [0, IP] are always bigger than those
         in [IP + 1, n].

         Although the array is rotated, it retains some properties of sorted arrays that we can leverage. Specifically,
         one half of the array (either the left or the right) will always be sorted. This means we can still apply
         binary search by determining which half of our array is sorted and whether the target lies within it.

         It is straightforward to determine if a sorted array nums[left ~ right] could possibly contain target. We can
         simply compare target with the two boundary values nums[left] and nums[right].
         If nums[left] <= target <= nums[right], then nums[left ~ right] might contain target, which needs to be
         verified by binary search, so we continue with this subarray.
        Otherwise, target is guaranteed to not be in nums[left ~ right], and there is no need to search over this array,
        so we continue with the other subarray.

         Perform standard binary search. Take an index in the middle as a pivot.
         If nums[mid] == target, the job is done, return mid.
         Otherwise, there could be two situations:

            1- Middle element is greater than the leftmost element in the array, i.e. the part of array from the leftmost
                 element to the middle one, nums[left ~ mid], is sorted/non-rotated. In a normally sorted array, if the
                 start is less than or equal to the midpoint, it means all elements till the midpoint are in the correct
                 increasing order.

                 If the target lies within this sorted left half:
                        nums[left] <= target < nums[mid]
                 it suggests that the sorted left half might include target while the other half does not contain
                 target. Consequently, we focus on the left half for further search: right = mid - 1.

                 Otherwise, the left half is guaranteed not to contain target, and we will move on to the right half:
                 left = mid + 1.

            2- Middle element is smaller than the leftmost element of the array, which implies that the rotation index
                 is somewhere between left and mid. That means that the part of array from the middle element to the
                 rightmost one, nums[mid ~ right], is sorted/non-rotated.

                 If the target lies within this sorted right half:
                        nums[mid] < target <= nums[right]
                 it suggests that the sorted right half might include target, so go right: left = mid + 1.

                 Otherwise, the right half is guaranteed not to contain target, and we will move on to the left half:
                 right = mid - 1.

        The beauty of this approach lies in its ability to determine with certainty which half of the array to look in,
        even though the array is rotated. By checking which half of the array is sorted and then using the sorted
        property to determine if the target lies in that half, we can effectively eliminate half of the array from
        consideration at each step

    Time complexity: O(logN)
    Space complexity: O(1)
    """
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] >= nums[left]:
            # It's <= instead of < because when there's only two elements, 'mid' and 'left' point to exactly the same
            # element. Then we have to include = to make sure it covers this case.
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


def search_v2(nums, target):
    """ This is the exact same solution. However, it looks like when the range inclusion checks are more explicit the
        intuition is much clearer.
    Time complexity: O(logN)
    Space complexity: O(1)
    """
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[left] <= nums[mid]:
            # target is greater than mid element, and we know that the subarray from left to mid is
            # sorted/non-rotated, so go right because a smaller value can't exist to the left
            # OR
            # target is smaller than leftmost element, and we know that the subarray from left to mid is
            # sorted/non-rotated in INCREASING ORDER, so go right because a smaller value can't exist to the left
            if target > nums[mid] or target < nums[left]:
                left = mid + 1
            else:
                right = mid - 1
        else:
            # target is smaller than mid element, and we know that the subarray from mid to right is
            # sorted/non-rotated, so go left because a smaller value can't exist to the right
            # OR
            # target is greater than rightmost element, and we know that the subarray from mid to right is
            # sorted/non-rotated in INCREASING ORDER, so go left because a larger value can't exist to the right
            if target < nums[mid] or target > nums[right]:
                right = mid - 1
            else:
                left = mid + 1
    return -1


class Test(unittest.TestCase):
    data = [
        ([4, 5, 6, 7, 0, 1, 2], 0, 4),
        ([4, 5, 6, 7, 0, 1, 2], 3, -1)
    ]

    def test_search(self):
        for test_array, test_target, result in self.data:
            self.assertEqual(result, search_v1(test_array, test_target))
            self.assertEqual(result, search_v2(test_array, test_target))


if __name__ == '__main__':
    unittest.main()
