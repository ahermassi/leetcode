""" Given an array nums, write a function to move all 0's to the end of it while maintaining the relative order of
the non-zero elements.
You must do this in-place without making a copy of the array. """

import unittest2 as unittest


def move_zeroes_v1(nums):
    """ This is a 2 pointer approach. The fast pointer which is denoted by variable i does the job of processing new
        elements. If the newly found element is not a zero, we record it just after the last found non-zero element.
        The position of last found non-zero element is denoted by the 'non_zero_index' variable.
        The code will maintain the following invariants:
            1- All elements before 'non_zero_index' are non-zeroes.
            2- All elements between i and 'non_zero_index' are zeroes.
        Therefore, when we encounter a non-zero element, we need to swap elements pointed by i and 'non_zero_index',
        then advance both pointers. If it's a zero element, we just advance i pointer.

    Time complexity: O(N), the total number of operations are optimal. The total operations (array writes) that
    code does is number of non-zero elements.
    Space complexity: O(1)
    """
    non_zero_index = 0
    for i in range(len(nums)):
        if nums[i] != 0:
            nums[i], nums[non_zero_index] = nums[non_zero_index], nums[i]
            non_zero_index += 1


def move_zeroes_v2(nums):
    """ Using built-in sort() elegantly. Note that Timsort might introduce temporary arrays making it out-of-place
    Time complexity: O(N log N)
    Space complexity: O(N)
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


if __name__ == '__main__':
    unittest.main()
