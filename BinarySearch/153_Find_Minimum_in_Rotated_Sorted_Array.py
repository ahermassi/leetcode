""" Suppose an array sorted in ascending order is rotated at some pivot unknown to you beforehand.
(i.e.,  [0,1,2,4,5,6,7] might become  [4,5,6,7,0,1,2]).
Find the minimum element.
You may assume no duplicate exists in the array. """

import unittest2 as unittest


# Check out this article for a good illustration: https://leetcode.com/articles/find-minimum-in-rotated-sorted-array/

def find_min_v1(nums):
    """ There is a point in the array at which we would notice a change. This is the point which would help us in this
        question. We call this the Inflection Point.

        In this modified version of binary search algorithm, we are looking for this point.

        All the elements to the left of Inflection Point > first element of the array
        All the elements to the right of Inflection Point < first element of the array

        Find the middle element of the array.

            - If middle element > leftmost element of array, this means that left half is sorted/non-rotated, and we
               need to look for the Inflection Point on the right of mid.

            - If middle element < leftmost element of array, this that the left half is rotated (not completely sorted)
               and we need to look for the Inflection Point on the left of mid.

        We stop our search when we find the Inflection Point when either of the following two conditions is satisfied:

            - nums[mid] > nums[mid + 1] --> nums[mid + 1] is the smallest. This is because, in a sorted array, an
               element is always less than or equal to its successor

            - nums[mid] < nums[mid - 1] --> nums[mid] is the smallest. This is because, in a sorted array, an element is
               always greater than or equal to its predecessor.

        So, in all cases, we're looking for the point where the discrepancy occurs.

        The key observation is: regardless of where it occurs in the array, by definition the minimum value's left
        neighbor is the maximum value.

    Time complexity: O(logN)
    Space complexity: O(1)
    """
    if len(nums) == 1 or nums[0] < nums[-1]:  # If last element is greater than first element, there is no rotation.
        return nums[0]
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] > nums[mid + 1]:  # If the middle element is greater than its next element, then nums[mid + 1] is
            # the smallest. This point would be the point of change from higher to lower values.
            return nums[mid + 1]
        if nums[mid] < nums[mid - 1]:  # If the middle element is less than its previous element, then nums[mid] is
            # the smallest
            return nums[mid]
        if nums[left] < nums[mid]:  # If the middle element is greater than the leftmost element, this means the
            # smallest value is still somewhere to the right as we are still dealing with a sorted/non-rotated half
            left = mid + 1
        else:  # If nums[left] is greater than middle value, then this means the smallest value is somewhere to the left
            right = mid - 1


def find_min_v2(nums):
    """ The main idea for our checks is to converge the left and right bounds to the start of the pivot, or Inflection
         Point, and never disqualify the index for a possible minimum value.

         Remember that:

            - All the elements to the left of Inflection Point > leftmost element of the array
            - All the elements to the right of Inflection Point < rightmost element of the array

        Notice the numbers are divided into two sections: numbers larger than the rightmost element of the array and
        numbers smaller than it. The minimum element is at the boundary between the two sections.

        A better way to visualize thus algorithm is thinking that we apply a filter of "< rightmost element" to each
        value in the array, which conceptually produces a boolean array.
        For example, nums = [3,4,5,1,2] => filter( < rightmost element) => [F, F, F, F, T, T]

        Now the problem becomes finding the first T which can easily be solved using binary search.

        Binary search can work beyond sorted arrays, as long as there is a BINARY DECISION we can use to shrink the
        search range.

    Time complexity: O(logN)
    Space complexity: O(1)
    """
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
            # If nums[mid] > nums[right], we know that the discrepancy must have occurred somewhere to the right of mid.
            # mid can't be the minimum, so we can safely move left to mid + 1, which ensures the interval is always
            # shrinking.
            # Example: [3, 4, 5, 6, 7, 8, 9, 1, 2]. In the first iteration, we start with mid = 4, right = 9.
            # nums[mid] > nums[right], so we know that at some point to the right of mid, the pivot must have occurred.
            # We also know that the number at mid is greater than AT LEAST one number to the right, so we can use
            # mid + 1 and never consider mid again.
        else:
            right = mid
            # Example: [8,9,1,2,3,4,5,6,7]
            # In the first iteration, when we start with mid = 4, right = 9.
            # nums[mid] <= nums[right]; we know the numbers continued increasing to the right of mid, so
            # they never reached the pivot and wrapped around. Therefore, we know the pivot must be at index <= mid.
            # We also now know mid stores a smaller value than at least one other index in the list (to its right),
            # so we do not discard it by doing right = mid - 1. It still might have the minimum value.
            # Since we use round down for mid, and left < right, right would never be the same as mid. This situation
            # becomes very clear in the case of a two-element array (or just in general when the left and right pointers
            # are adjacent, .i.e. right = left + 1, in which case mid = left) Therefore, we can always make right = mid
            # while we don't have to worry the loop will not end, ensuring the interval is always shrinking.

    # At this point, left and right converge to a single index (for minimum value). Our if/else block forces the bounds
    # of left/right to shrink each iteration.
    # We shrink the left/right bounds to one value, without ever disqualifying a possible minimum
    return nums[left]


class Test(unittest.TestCase):
    data = [([3, 4, 5, 1, 2], 1), ([4, 5, 6, 7, 0, 1, 2], 0)]

    def test_find_min(self):
        for test_nums, result in self.data:
            self.assertEqual(result, find_min_v1(test_nums))
            self.assertEqual(result, find_min_v2(test_nums))


if __name__ == '__main__':
    unittest.main()
