""" Given an array of integers, return indices of the two numbers such that they add up to a specific target.
You may assume that each input would have exactly one solution, and you may not use the same element twice. """

import unittest2 as unittest


def two_sum_v1(nums, target):
    """ Brute force approach. Not the best performance.
         Loop through each element x and find if there is another value that equals to (target - x)

    Time complexity: O(N^2)
    Space complexity: O(1)
    """
    n = len(nums)
    for i in range(n):
        s = nums[i]
        for j in range(i + 1, n):
            if s + nums[j] == target:
                return [i, j]


def two_sum_v2(nums, target):
    """ Using a hash table and 2 passes, trading space for time complexity.
        In the first iteration, we add each element's value and its index to the table. Then, in the second iteration,
        we check if each element's complement (target - nums[i]) exists in the table.
        Beware that the complement must not be nums[i] itself.

    Time complexity: O(N), for 2 hash table passes
    Space complexity: O(N)
    """
    indices = {}
    for i, num in enumerate(nums):
        indices[num] = i # Add each element value and its index to the table
    for i, num in enumerate(nums):
        complement = target - nums[i]
        if complement in indices and indices[complement] != i:  # The complement (target - num) found in O(1) lookup
            return [i, indices[complement]]


def two_sum_v3(nums, target):
    """ We can do it in one pass. While we iterate and insert elements into the hash map, we also look back to check
         if current element's complement already exists in the hash map. If it exists, we have found a solution and
         return immediately.

    Time complexity: O(N), for one hash table pass
    Space complexity: O(N)
    """
    indices = {}
    for i, num in enumerate(nums):
        if target - num in indices:
            return [indices[target - num], i]
        indices[num] = i


class Test(unittest.TestCase):
    data = ([2, 7, 11, 15], 9)

    def test_two_sum(self):
        self.assertEqual([0, 1], two_sum_v1(self.data[0], self.data[1]))
        self.assertEqual([0, 1], two_sum_v2(self.data[0], self.data[1]))
        self.assertEqual([0, 1], two_sum_v3(self.data[0], self.data[1]))


if __name__ == '__main__':
    unittest.main()
