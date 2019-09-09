""" Given an array nums of n integers and an integer target, are there elements a, b, c, and d in nums such that
a + b + c + d = target? Find all unique quadruplets in the array which gives the sum of target.

Note:
The solution set must not contain duplicate quadruplets. """

import unittest2 as unittest

from collections import defaultdict


def four_sum(nums, target):
    """ This is essentially 2sum + 2sum. Save every sum of 2 different elements in nums in a hash map along with
        corresponding indices. After that, for every sum s, check if target - s is in the hash map. Be careful not no
        add duplicate elements to the final result.
    Time complexity: O(N ** 3)
    Space complexity: O(N ** 2)
    """
    ans = set()  # Use a set to avoid duplicates
    d = defaultdict(list)
    for i in range(len(nums) - 1):
        for j in range(i + 1, len(nums)):
            s = nums[i] + nums[j]
            d[s].append((i, j))
    for key in d:
        if target - key in d:
            list1, list2 = d[key], d[target - key]
            for (i, j) in list1:
                for (k, l) in list2:
                    if i != k and i != l and j != k and j != l:
                        temp = sorted([nums[i], nums[j], nums[k], nums[l]])
                        ans.add(tuple(temp))
    return list(list(v) for v in ans)


class Test(unittest.TestCase):
    data = [1, 0, -1, 0, -2, 2]
    target = 0
    result = [
        [-1, 0, 0, 1],
        [-2, -1, 1, 2],
        [-2, 0, 0, 2]
    ]

    def test_four_sum(self):
        self.assertEqual(self.result, four_sum(self.data, self.target))


if __name__ == '__main__':
    unittest.main()
