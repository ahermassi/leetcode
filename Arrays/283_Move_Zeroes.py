""" Given an array nums, write a function to move all 0's to the end of it while maintaining the relative order of
the non-zero elements.
You must do this in-place without making a copy of the array. """

import unittest2 as unittest


# Pattern applied: use 2 pointers and maintain an invariant between the pointers

def move_zeroes_v1(nums):
    """ This is a 2 pointer approach. The fast pointer which is denoted by variable i does the job of processing new
        elements. If the newly found element is not a zero, we record it just after the last found non-zero element.
        The position of last found non-zero element is denoted by the 'non_zero_index' variable.
        The code will maintain the following invariants:
            1- All elements before 'non_zero_index' are non-zeroes
            2- All elements between 'non_zero_index' and i are zeroes
            3- All elements after i are undecided (yet)
        Therefore, when we encounter a non-zero element, we need to swap elements pointed by i and 'non_zero_index',
        then advance both pointers. If it's a zero element, we just advance i pointer.
    Time complexity: O(N), the total number of operations is optimal. The total operations (array writes) that code
    does is number of non-zero elements.
    Space complexity: O(1)
    """
    non_zero_index = 0
    for i, num in enumerate(nums):
        if num:
            nums[i], nums[non_zero_index] = nums[non_zero_index], nums[i]
            non_zero_index += 1


def move_zeroes_v2(nums):
    """ The same as above. However, as we keep finding new non-zero elements, we just overwrite them at the
        'non_zero_index'. After i index reaches the end of array, we now know that all the non-zero elements have been
        moved to the beginning of the array in their original order. Now comes the time to fulfill the other
        requirement: Moving all 0's to the end. We now simply need to fill all the indexes after 'non_zero_index'
        with 0.
    Time complexity: O(N), however, the total number of operations is sub-optimal. The total operations (array writes)
    that the algorithm does is N.
    Space complexity: O(1)
    """
    n, non_zero_index = len(nums), 0
    for i, num in enumerate(nums):
        if num:  # If the current element is not 0, then we need to append it just in front of last non 0 we found.
            nums[non_zero_index] = num
            non_zero_index += 1
    for i in range(non_zero_index, n):  # After we have finished processing new elements, all the non-zero elements
        # are already at beginning of array. We just need to fill remaining array with 0's.
        nums[i] = 0


def move_zeroes_v3(nums):
    """ Using built-in sort() elegantly. Note that Timsort might introduce temporary arrays making it out-of-place
    Time complexity: O(N logN)
    Space complexity: O(N)
    """
    nums.sort(key=lambda x: 1 if x == 0 else 0)


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
