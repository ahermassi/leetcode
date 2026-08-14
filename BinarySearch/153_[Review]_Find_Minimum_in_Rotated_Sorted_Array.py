""" Suppose an array sorted in ascending order is rotated at some pivot unknown to you beforehand.
(i.e.,  [0,1,2,4,5,6,7] might become  [4,5,6,7,0,1,2]).
Find the minimum element.
You may assume no duplicate exists in the array. """

import unittest2 as unittest

# v1: FIND the dip explicitly
#     → while left <= right
#     → inspect mid
#
# v2: CONVERGE onto the minimum
#     → while left < right
#     → [left, right] always contains answer
#     → stop when one candidate remains

# Check out this article for a good illustration: https://leetcode.com/articles/find-minimum-in-rotated-sorted-array/
def find_min_v1(nums):
    """ Explicitly find the rotation point.

        In a rotated sorted array such as:

            [4, 5, 6, 7, 0, 1, 2]
                         ^
                       minimum

        the minimum is the value immediately after the "drop" from the high-valued sorted section to the low-valued
        sorted section.

        At each iteration:

        1. Check whether mid is directly next to that drop.
           - nums[mid] > nums[mid + 1]  -> nums[mid + 1] is the minimum
           - nums[mid] < nums[mid - 1]  -> nums[mid] is the minimum

        2. Otherwise, determine which direction contains the rotation:
           - nums[mid] >= nums[left]:
               mid is in the left/high sorted section, so the minimum
               must be strictly to the right of mid.

           - nums[mid] < nums[left]:
               mid is in the right/low section, so the minimum must
               be somewhere to the left.

        This uses `while left <= right` because we are actively inspecting mid to see whether it is at the rotation
        point.

    Time complexity: O(logN)
    Space complexity: O(1)
    """
    if len(nums) == 1 or nums[0] < nums[-1]:
        # Already sorted, so the first element is the minimum.
        return nums[0]

    left, right = 0, len(nums) - 1

    while left <= right:
        mid = (left + right) // 2

        if nums[mid + 1] < nums[mid]:
            # The drop occurs immediately after mid.
            return nums[mid + 1]

        if nums[mid] < nums[mid - 1]:
            # The drop occurs immediately before mid, so mid is the minimum.
            return nums[mid]

        if nums[mid] >= nums[left]:
            # mid is in the high-valued sorted section.
            # We already proved mid is not the minimum, so discard it.
            left = mid + 1
        else:
            # mid is in the low-valued section.
            # We already proved mid is not the minimum, so search strictly left.
            right = mid - 1


# Video explanation: https://youtu.be/nIVW4P8b1VA
def find_min_v2(nums):
    """ Binary-search the boundary between the high and low sections.

        Example:

            [4, 5, 6, 7, 0, 1, 2]
            high section | low section
                         ^
                      minimum

        Invariant:
            The minimum is always somewhere inside [left, right].

        Compare nums[mid] with nums[right]:

        1. nums[mid] > nums[right]

            Example:
                [4, 5, 6, 7, 0, 1, 2]
                          M        R
                7 > 2

            mid is still in the high-valued section, so the drop/minimum must be strictly to the right of mid.
            mid cannot be the minimum, so:
                left = mid + 1

        2. nums[mid] < nums[right]

            Example:
                [6, 7, 0, 1, 2, 3, 4]
                       M           R
                1 < 4

            mid is in the low/sorted section. The minimum is therefore at mid or somewhere to its left.
            mid might itself be the minimum, so we must keep it:
                right = mid

        Why `while left < right`?

            This is a candidate-convergence / boundary search.

            [left, right] always contains the minimum, and we keep shrinking that interval until exactly ONE candidate
            remains.

            When:
                left == right

            that single index must be the minimum, so the loop stops.

        Alternative F/T visualization using the ORIGINAL last element:

            nums = [3, 4, 5, 1, 2]

            predicate: nums[i] <= nums[right]

                      [F, F, F, T, T]
                                ^
                             first T

            The first T is the minimum.

    Time complexity: O(logN)
    Space complexity: O(1)
    """
    left, right = 0, len(nums) - 1

    # Keep shrinking [left, right] while more than one candidate remains.
    while left < right:
        mid = (left + right) // 2

        if nums[mid] > nums[right]:
            # The minimum is strictly to the right of mid. mid cannot be the answer, so discard it.
            left = mid + 1
        else:
            # The minimum is at mid or somewhere to its left. mid may still be the answer, so keep it.
            right = mid

    # left == right: exactly one candidate remains.
    return nums[right]


class Test(unittest.TestCase):
    data = [([3, 4, 5, 1, 2], 1), ([4, 5, 6, 7, 0, 1, 2], 0)]

    def test_find_min(self):
        for test_nums, result in self.data:
            self.assertEqual(result, find_min_v1(test_nums))
            self.assertEqual(result, find_min_v2(test_nums))


if __name__ == '__main__':
    unittest.main()
