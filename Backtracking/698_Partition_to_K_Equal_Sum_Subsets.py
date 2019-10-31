""" Given an array of integers nums and a positive integer k, find whether it's possible to divide this array into k
non-empty subsets whose sums are all equal. """

import unittest2 as unittest


def can_partition_k_subsets_v1(nums, k):
    """ Assume sum is the sum of nums[] . The DFS/backtracking process is to find a subset of nums[] which sum equals
        to target = sum/k. We use an array visited[] to record which element in nums[] is used. Each time when we get a
        cur_sum = target, we will start from position 0 in nums[] to look up the elements that are not used yet and
        find another cur_sum = target. We exhaustively try all the possible combinations.
    """
    def helper(index, k, cur_sum, target):
        if k == 1:
            return True
        if cur_sum == target:
            return helper(0, k - 1, 0, target)  # A subset has been already formed, so decrement k and start over
        for i in range(index, n):
            if not visited[i] and cur_sum + nums[i] <= target:
                visited[i] = True
                if helper(i + 1, k, cur_sum + nums[i], target):  # Can we augment the current subset to get to target ?
                    return True
                visited[i] = False  # This is where we backtrack and drop the previous choice of nums[i]
        return False

    total = sum(nums)
    if total % k != 0:
        return False
    target = total // k
    visited, n = [False for _ in range(len(nums))], len(nums)
    return helper(0, k, 0, target)


class Test(unittest.TestCase):
    data = [([4, 3, 2, 3, 5, 2, 1], 4, True)]

    def test_can_partition_k_subsets(self):
        for test_nums, test_k, result in self.data:
            self.assertEqual(result, can_partition_k_subsets_v1(test_nums, test_k))


if __name__ == '__main__':
    unittest.main()