""" Suppose an array sorted in ascending order is rotated at some pivot unknown to you beforehand.
(i.e.,  [0,1,2,4,5,6,7] might become  [4,5,6,7,0,1,2]).
Find the minimum element.
You may assume no duplicate exists in the array. """

import unittest2 as unittest


# Check out this article for a good illustration: https://leetcode.com/articles/find-minimum-in-rotated-sorted-array/

def find_min_v1(nums):
    """ There is a point in the array at which we would notice a change. This is the point which would help us in this
        question. We call this the Inflection Point.
        In this modified version of binary search algorithm, we are looking for this point. We notice that:
            All the elements to the left of inflection point > first element of the array.
            All the elements to the right of inflection point < first element of the array.
        Find the mid element of the array.
        If mid element > first element of array this means that we need to look for the inflection point on the right
        of mid.
        If mid element < first element of array this that we need to look for the inflection point on the left of mid.
        We stop our search when we find the inflection point, when either of the two conditions is satisfied:
            nums[mid] > nums[mid + 1] Hence, mid+1 is the smallest.
            nums[mid - 1] > nums[mid] Hence, mid is the smallest.
    Time complexity: O(logN)
    Space complexity: O(1)
    """
    if len(nums) == 1:
        return nums[0]
    if nums[0] < nums[-1]:  # If the last element is greater than the first element, then there is no rotation.
        return nums[0]
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] > nums[mid + 1]:  # If the mid element is greater than its next element, then mid+1 element is
            # the smallest. This point would be the point of change from higher to lower values.
            return nums[mid + 1]
        if nums[mid] < nums[mid - 1]:  # If the mid element is less than its previous element, then mid element is
            # the smallest
            return nums[mid]
        if nums[0] < nums[mid]:  # If the mid element's value is greater than the 0th element, this means the smallest
            # value is still somewhere to the right as we are still dealing with a non-rotated half
            left = mid + 1
        else:  # If nums[0] is greater than the mid value, then this means the smallest value is somewhere to the left
            right = mid - 1


def find_min_v2(nums):
    """ The main idea for our checks is to converge the left and right bounds to the start of the pivot, or Inflection
        Point, and never disqualify the index for a possible minimum value.
    Time complexity: O(logN)
    Space complexity: O(1)
    """
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
            # If nums[mid] > nums[right], we know that the pivot/minimum value must have occurred somewhere to the
            # right of mid.
            # Example: [3,4,5,6,7,8,9,1,2]. In the first iteration, we start with mid index = 4, right index = 9.
            # If nums[mid] > nums[right], we know that at some point to the right of mid, the pivot must have occurred,
            # which is why the values wrapped around so that nums[right] is less then nums[mid].
            # We also know that the number at mid is greater than AT LEAST one number to the right, so we can use
            # mid + 1 and never consider mid again.
        else:
            right = mid
            # If nums[mid] <= nums[right], we know that the pivot was not encountered to the right of middle, because
            # that means the values would wrap around and become smaller (which is caught in the above if statement).
            # This leaves the possible pivot point to be at index <= mid.
            # Example: [8,9,1,2,3,4,5,6,7]. In the first iteration, we start with mid index = 4, right index = 9.
            # If nums[mid] <= nums[right], we know the numbers continued increasing to he right of mid, so they never
            # reached the pivot and wrapped around. Therefore, we know the pivot must be at index <= mid.
            # It is possible for the mid index to store a smaller value than at least one other index in the list (at
            # right), so we do not discard it by doing right = mid - 1. It still might have the minimum value.
    # At this point, left and right converge to a single index (for minimum value). Our if/else block forces the bounds
    # of left/right to shrink each iteration:
    # When left bound increases, it does not disqualify a value that could be smaller than something else (we know
    # nums[mid] > nums[right], so nums[right] wins and we ignore mid).
    # When right bound decreases, it also does not disqualify a value that could be smaller than something else (we
    # know nums[mid] <= nums[right], so nums[mid] wins and we keep it for now).
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
