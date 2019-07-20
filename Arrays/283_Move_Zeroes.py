""" Given an array nums, write a function to move all 0's to the end of it while maintaining the relative order of
the non-zero elements.
You must do this in-place without making a copy of the array. """

import unittest2 as unittest


def move_zeroes_v1(nums):
    """ First thought. A run on [0,1,0,3,12] produces the following intermediate arrays:
     1 0 3 0 12
     1 3 0 12 0
     1 3 12 0 0
     Time complexity: O(Nk), where k is the number of 0s in the array
     Space complexity: O(1)
     """
    for _ in range(nums.count(0)):
        for i in range(len(nums) - 1):
            if nums[i] == 0:
                nums[i], nums[i + 1] = nums[i + 1], nums[i]
            i += 1


def move_zeroes_v2(nums):
    """
     Time complexity: O(N)
     Space complexity: O(1)
     """
    non_zero_index = 0
    for i in range(len(nums)):
        if nums[i] != 0:
            nums[i], nums[non_zero_index] = nums[non_zero_index], nums[i]
            non_zero_index += 1


def move_zeroes_v3(nums):
    """ Using built-in sort() elegantly. Note that Timsort might introduce temporary arrays making in not in-place
    Time complexity: O(N log N)
     Space complexity: O(1) (?)
    """
    nums.sort(key=lambda x: 1 if x == 0 else 1)


class Test(unittest.TestCase):
    data = [([0, 1, 0, 3, 12], [1, 3, 12, 0, 0]),
            ([0, 1], [1, 0]),
            ([1, 2, 3], [1, 2, 3])
            ]

    def test_move_zeroes(self):
        for test_array, result in self.data:
            move_zeroes_v1(test_array)
            self.assertEqual(result, test_array)
        for test_array, result in self.data:
            move_zeroes_v2(test_array)
            self.assertEqual(result, test_array)
        for test_array, result in self.data:
            move_zeroes_v3(test_array)
            self.assertEqual(result, test_array)


if __name__ == '__main__':
    unittest.main()
