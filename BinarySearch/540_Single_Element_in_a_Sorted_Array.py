""" You are given a sorted array consisting of only integers where every element appears exactly twice, except for one
element which appears exactly once. Find this single element that appears only once. """

import unittest2 as unittest


def single_non_duplicate_v1(nums):
    """ Let's start with two simple observations.
        Example 1: An array with length 2*4 + 1
        left = 0, right = 8, mid = 4 (even)
        If the single element X is on the left hand side, nums[mid] == nums[mid-1]: [1, 1, X, 2, 2(mid), 3, 3, 4, 4]
        If the single element X is on the right hand side, nums[mid] == nums[mid+1]: [1, 1, 2, 2, 3(mid), 3, X, 4, 4]
        Example 2: An array with length 2*3 + 1
        left = 0, right = 6, mid = 3 (odd)
        If the single element X is on the left hand side, nums[mid] == nums[mid+1]: [1, 1, X, 2(mid), 2, 3, 3]
        If the single element X is on the right hand side, nums[mid] == nums[mid-1]: [1, 1, 2, 2(mid), 3, 3, X]
        We start by setting 'left' and 'right' to be the lowest and highest index (inclusive) of the array, and then
        iteratively halve the array until we find the single element or until there is only one element left.
        On each loop iteration, we find 'mid', and determine the odd/evenness of the sides. By then looking at which
        half the middle element's PARTNER is in, we can 'left' and 'right' to cover the part of the array we now know
        the single element must be in.
        The trick that is required to be able to solve the problem is:
            The pairs which are on the left of the single element will have the first element in an even index. All the
            pairs which are on the right side of the single element will have the first element at an odd index.
        Use this fact to decide whether to go to the left side of the array or to the right side.
    Time complexity: O(logN)
    Space complexity: O(1)
    """
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] != nums[mid - 1] and nums[mid] != nums[mid + 1]:
            return nums[mid]
        if mid % 2 == 0:  # 'mid' is at an even index, then duplicate partner should be to the right if the single
            # element didn't occur in the left half (until now)
            if nums[mid] == nums[mid + 1]:
                left = mid + 2  # Skip the duplicate
            else:
                right = mid - 1
        else:  # 'mid' is at an odd index, then duplicate should be to the left if the single element didn't occur in
            # the left half (until now)
            if nums[mid] == nums[mid - 1]:
                left = mid + 1
            else:
                right = mid - 2  # Skip the duplicate
    return nums[left]


def single_non_duplicate_v2(nums):
    """ The single element is at the first even index not followed by its pair. After the single element, the pattern
        changes to being odd indices followed by their pair. This means that the single element (an even index) and all
        elements after it are even indices not followed by their pair. Therefore, given any even index in the array,
        we can easily determine whether the single element is to the left or to the right.
        We need to make sure our 'mid' index is even. We can do this by dividing 'left' and 'right' in the usual way,
        but then decrementing it by 1 if it is odd.
        Then we check whether or not the 'mid' index is the same as the one after it.
        If it is, then we know that 'mid' is not the single element, and that the single element must be at an even
        index after 'mid'. Therefore, we set left = mid + 2.
        If it is not, then we know that the single element is at some index before 'mid'. Therefore, we set
        right = mid - 1
    Time complexity: O(logN)
    Space complexity: O(1)
    """
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if mid % 2 == 1:  # We want the first element of the middle pair, which should be at an even index if the left
            # part is sorted.
            # Example: Index: 0 1 2 3 4 5 6
            #          Array: 1 1 3 3 4 8 8
            #                     ^
            mid -= 1
        if nums[mid] == nums[mid + 1]:  # We found a pair. The single element must be on the right.
            # Example: |1 1 3 3 5 6 6|
            # Next:     1 1 3 3|5 6 6|
            left = mid + 2
        else:  # We didn't find a pair. The single element must be on the left.
            # Example: |0 1 1 3 3 6 6|
            # Next:    |0 1 1|3 3 6 6
            right = mid - 1
    return nums[left]


class Test(unittest.TestCase):
    data = [([1, 1, 2, 3, 3, 4, 4, 8, 8], 2), ([3, 3, 7, 7, 10, 11, 11], 10)]

    def test_single_non_duplicate(self):
        for test_nums, result in self.data:
            self.assertEqual(result, single_non_duplicate_v1(test_nums))
            self.assertEqual(result, single_non_duplicate_v2(test_nums))


if __name__ == '__main__':
    unittest.main()
