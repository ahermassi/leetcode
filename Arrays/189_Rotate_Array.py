""" Given an array, rotate the array to the right by k steps, where k is non-negative.
Input: [1,2,3,4,5,6,7] and k = 3
Output: [5,6,7,1,2,3,4]
Explanation:
rotate 1 steps to the right: [7,1,2,3,4,5,6]
rotate 2 steps to the right: [6,7,1,2,3,4,5]
rotate 3 steps to the right: [5,6,7,1,2,3,4]
"""

import unittest2 as unittest


def rotate_v1(nums, k):
    """ If the number of rotations is greater than the length of the array, every n rotations bring the array back to
        its initial state (where n is the length of array). Thus, depending on k, we either perform k % n rotations
        or do a straightforward slicing.
    Time complexity: O(k * N) == O(N)
    Space complexity: O(N) for the slicing
    """
    if not k:
        return nums
    if k >= len(nums):
        for _ in range(k % len(nums)):
            nums[:] = nums[-1] + nums[:-1]
    else:
        nums[:] = nums[-k:] + nums[:len(nums) - k]


def rotate_v2(nums, k):
    """ Use a stack to push the elements involved in rotation.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    stack, k, res = [], k % len(nums), []
    for _ in range(k):
        stack.append(nums.pop())
    while stack:
        res.append(stack.pop())
    nums[:] = res + nums


class Test(unittest.TestCase):
    data = [([1, 2, 3, 4, 5, 6, 7], 3, [5, 6, 7, 1, 2, 3, 4]),
            ([-1, -100, 3, 99], 2, [3, 99, -1, -100]),
            ]

    def test_valid_mountain_array(self):
        for test_array, k, result in self.data:
            rotate_v1(test_array, k)
            self.assertEqual(result, test_array)


if __name__ == '__main__':
    unittest.main()
