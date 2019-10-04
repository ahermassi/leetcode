""" Given an array nums containing n + 1 integers where each integer is between 1 and n (inclusive), prove that at
least one duplicate number must exist. Assume that there is only one duplicate number, find the duplicate one. """

import unittest2 as unittest


def find_duplicate_v1(nums):
    """ If the numbers are sorted, then any duplicate numbers will be adjacent in the sorted array.
    Time complexity: O(N logN)
    Space complexity: O(N)
    """
    nums.sort()
    for i in range(1, len(nums)):
        if nums[i] == nums[i - 1]:
            return nums[i]


def find_duplicate_v2(nums):
    """ If we store each element in a set as we iterate over the array, we can simply check each element as we iterate.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    seen = set()
    for num in nums:
        if num in seen:
            return num
        seen.add(num)


class Test(unittest.TestCase):
    data = [([1, 3, 4, 2, 2], 2), ([3, 1, 3, 4, 2], 3)]

    def test_find_duplicate(self):
        for test_array, result in self.data:
            self.assertEqual(result, find_duplicate_v1(test_array))
            self.assertEqual(result, find_duplicate_v2(test_array))


if __name__ == '__main__':
    unittest.main()
