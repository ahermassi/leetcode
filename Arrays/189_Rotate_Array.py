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
         its initial state (where n is the length of array). Thus, depending on the value of k, we either perform
         (k % n) rotations or do a straightforward slicing.

    Time complexity: O(N)
    Space complexity: O(N), for the slicing
    """
    if not k:
        return nums
    k = k % len(nums)
    nums[:] = nums[-k:] + nums[:-k]


def rotate_v2(nums, k):
    """ Use a stack to push the elements involved in rotation.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    k = k % len(nums)
    stack = []
    for _ in range(k):
        stack.append(nums.pop())
    nums[:] = stack[::-1] + nums


def rotate_v3(nums, k):
    """ The idea is the following:
        1- Reverse the first (n - k) elements
        2- Reverse the rest of the elements
        3- Reverse the entire array
        nums = "----->-->"; k =3
        result = "-->----->";

        reverse "----->" we can get "<------->"
        reverse "-->" we can get "<-----<--"
        reverse "<-----<--" we can get "-->----->"
    Time complexity: O(N)
    Space complexity: O(1)
    """
    def reverse(left, right):
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1

    if not k:
        return nums
    n = len(nums)
    k = k % n
    reverse(0, n-k-1)
    reverse(n-k, n-1)
    reverse(0, n-1)


class Test(unittest.TestCase):
    data = [([1, 2, 3, 4, 5, 6, 7], 3, [5, 6, 7, 1, 2, 3, 4]),
            ([-1, -100, 3, 99], 2, [3, 99, -1, -100]),
            ]

    def test_rotate(self):
        for test_array, k, result in self.data:
            rotate_v1(test_array, k)
            self.assertEqual(result, test_array)


if __name__ == '__main__':
    unittest.main()
