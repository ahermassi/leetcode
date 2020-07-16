""" Given an unsorted integer array, find the smallest missing positive integer. """

import unittest2 as unittest


# Video explanation: https://www.youtube.com/watch?v=9SnkdYXNIzM


def first_missing_positive_v1(nums):
    """ The basic idea is that we have an array with n elements. The first missing positive integer must be in the
        range [1..n]. This is the crucial observation we use to deduce the algorithm. This means that the range of
        possible answers is [1..n] if an integer is missing, and if an integer is not missing then the answer is n+1.
        If there is no missing integer, this means that the array has all number from 1 to n. This must mean that the
        array is full. Why? Because in the range [1..n] there are exactly n numbers, and if we place n numbers in an
        array of length n, the array is by definition full. In this case, the solution is to return n+1 which is the
        first missing positive integer.
        Then, the algorithm becomes:
            1- Ignore all numbers <= 0 and > n since they are outside the range of possible answers
            2- For every remaining cell that contains a positive integer X, we can use the negative of the number
               stored at index (X - 1) as a flag to mark that X was previously found
            3- Find the first cell not marked, that is the first missing positive integer. If we did not find an
               unmarked cell, there was no missing integer, so return n+1.
        In very simple words: Once all numbers are made positive, if any number is found in range [1,n] then attach a
        negative sign to the corresponding index. So for 1, 0th element becomes negative, etc.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    n = len(nums)
    for i, num in enumerate(nums):
        if num <= 0 or num > n:  # Mark numbers <= 0 and > n with a special marker number (n+1)
            nums[i] = n + 1
    # Note: All numbers in the array are now positive and in the range 1..n+1. Therefore, they can be used as indices
    for num in nums:
        num = abs(num)
        if num == n + 1:
            continue
        index = num - 1
        if nums[index] > 0:  # Prevent double negative operations
            nums[index] *= -1  # Mark each number appearing in the array by negating the value appearing at the index
            # pointed at by index - 1
    for i, num in enumerate(nums):  # Find the first cell which isn't negative (doesn't appear in the array)
        if num > 0:
            return i + 1
    return n + 1


class Test(unittest.TestCase):
    data = [([1, 2, 0], 3), ([3, 4, -1, 1], 2), ([7, 8, 9, 11, 12], 1)]

    def test_first_missing_positive(self):
        for test_nums, result in self.data:
            self.assertEqual(result, first_missing_positive_v1(test_nums))


if __name__ == '__main__':
    unittest.main()
