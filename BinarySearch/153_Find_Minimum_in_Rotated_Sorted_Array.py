""" Suppose an array sorted in ascending order is rotated at some pivot unknown to you beforehand.
(i.e.,  [0,1,2,4,5,6,7] might become  [4,5,6,7,0,1,2]).
Find the minimum element.
You may assume no duplicate exists in the array. """

import unittest2 as unittest


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


class Test(unittest.TestCase):
    data = [([3, 4, 5, 1, 2], 1), ([4, 5, 6, 7, 0, 1, 2], 0)]

    def test_find_min(self):
        for test_nums, result in self.data:
            self.assertEqual(result, find_min_v1(test_nums))


if __name__ == '__main__':
    unittest.main()
