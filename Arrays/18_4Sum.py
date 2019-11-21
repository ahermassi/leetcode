""" Given an array nums of n integers and an integer target, are there elements a, b, c, and d in nums such that
a + b + c + d = target? Find all unique quadruplets in the array which gives the sum of target.

Note:
The solution set must not contain duplicate quadruplets. """

import unittest2 as unittest

from collections import defaultdict


def four_sum_v1(nums, target):
    """ This is essentially 2sum + 2sum. Save every sum of 2 different elements in nums in a hash map along with
        corresponding indices. After that, for every sum s, check if (target - s) is in the hash map. Be careful not no
        add duplicate elements to the final result.
    Time complexity: O(N ** 3)
    Space complexity: O(N ** 2)
    """
    if len(nums) < 4:
        return None
    nums.sort()
    n, res, two_sums = len(nums), set(), defaultdict(list)
    for i in range(n - 1):
        for j in range(i + 1, n):
            two_sums[nums[i] + nums[j]].append((i, j))
    for s in two_sums:
        if target - s in two_sums:
            indices1, indices2 = two_sums[s], two_sums[target - s]
            for i, j in indices1:
                for k, l in indices2:
                    if i != k and i != l and j != k and j != l:  # We don't need numbers at the same position.
                        # Example: target = 6, and one of the 2sum is equal to 3 --> target - s = 3, and indices1 and
                        # indices2 would be the exact same list
                        res.add(tuple(sorted([nums[i], nums[j], nums[k], nums[l]])))
    return map(list, res)


class Test(unittest.TestCase):
    data = [1, 0, -1, 0, -2, 2]
    target = 0
    result = [
        [-1, 0, 0, 1],
        [-2, -1, 1, 2],
        [-2, 0, 0, 2]
    ]

    def test_four_sum(self):
        self.assertEqual(self.result, four_sum_v1(self.data, self.target))


if __name__ == '__main__':
    unittest.main()
