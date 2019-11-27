""" Given a set of distinct integers, nums, return all possible subsets (the power set).
Note: The solution set must not contain duplicate subsets. """

import unittest2 as unittest


def subsets_v1(nums):
    """ While iterating through all numbers, for each new number, we can either pick it or not pick it.
            1- If pick, just add current number to every existing subset.
            2- If not pick, just leave all existing subsets as they are.
        We just combine both into our result.
        Here's an example to help understand the code:
        The set to iterate over/generate the power set for: input_set = [1, 2, 3]
        Subset initially only has the empty set (empty list), []
        In each iteration, concatenate each element/list in subset with the list[n], then extend the results into
        subset.
            subset = [[]]
            element -> subset list after each iteration
            num = 1 -> [[], [1]]
            num = 2 -> [[], [1], [2], [1, 2]]
            num = 3 -> [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]
    Time complexity: O(2^N)
    Space complexity: O(1)
    """
    res = [[]]
    for num in nums:
        res += [lst + [num] for lst in res]
    return res


def subsets_v2(nums):
    """ DFS recursively.
    Time complexity: O(2 ** N)
    Space complexity: O(N) for call stack
    """

    def dfs(index, path):
        res.append(path)
        for i in range(index, len(nums)):
            dfs(i + 1, path + [nums[i]])

    res = []
    dfs(0, [])
    return res


class Test(unittest.TestCase):
    data = [([1, 2, 3], [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]])]

    def test_subsets(self):
        for test_array, result in self.data:
            self.assertEqual(result, sorted(subsets_v1(test_array)))
            self.assertEqual(result, sorted(subsets_v2(test_array)))


if __name__ == '__main__':
    unittest.main()
