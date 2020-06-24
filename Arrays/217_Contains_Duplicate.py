""" Given an array of integers, find if the array contains any duplicates.
Your function should return true if any value appears at least twice in the array, and it should return false if every
element is distinct. """

from collections import defaultdict
import unittest2 as unittest


def contains_duplicate_v1(nums):
    """ The good old hash set in action. This solution performs an optimal number of operations because it can exit
        early when the first 2 array elements are equal.
    Time complexity: O(N), where N is the length of array
    Space complexity: O(N)
    """
    values = set()
    for num in nums:
        if num in values:
            return True
        values.add(num)
    return False


def contains_duplicate_v2(nums):
    """ If there are any duplicate integers, they will be consecutive after sorting.
        The implementation here modifies the original array by sorting it. In general, it is not a good practice to
        modify the input unless it is clear to the caller that the input will be modified. We may make a copy of nums
        and operate on the copy instead.
    Time complexity: O(N logN), for sorting
    Space complexity: O(N)
    """
    nums.sort()
    n = len(nums)
    for i in range(n - 1):
        if nums[i] == nums[i + 1]:
            return True
    return False


class Test(unittest.TestCase):
    data = [([1, 2, 3, 1], True), ([1, 2, 3, 4], False), ([1, 1, 1, 3, 3, 4, 3, 2, 4, 2], True)]

    def test_contains_duplicate(self):
        for test_nums, result in self.data:
            self.assertEqual(result, contains_duplicate_v1(test_nums))
            self.assertEqual(result, contains_duplicate_v2(test_nums))


if __name__ == '__main__':
    unittest.main()
