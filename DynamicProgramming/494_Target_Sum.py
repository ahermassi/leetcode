""" You are given a list of non-negative integers, a1, a2, ..., an, and a target, S. Now you have 2 symbols + and -.
For each integer, you should choose one from + and - as its new symbol.
Find out how many ways to assign symbols to make sum of integers equal to target S. """

import unittest2 as unittest


def find_target_sum_ways_v1(nums, S):
    """ Brute force. TLE
        The brute force approach is based on recursion. We need to try to put both the + and - symbols at every
        location in the given nums array and find out the assignments which lead to the required result S.
        For this, we make use of a recursive function dfs(index, total), which returns the assignments leading to the
        sum S, starting from index 'index' onwards, provided the sum of elements upto the (index -1)th element is
        'total'. This function appends a + sign and a - sign both to the element at the current index and calls itself
        with the updated total as (total + nums[index]) and (total - nums[index]) respectively along with the updated
        current index as (index + 1). Whenever we reach the end of the array, we compare the sum obtained with S. If
        they are equal, we increment the count value to be returned.
        Thus, the function call dfs(0, 0) returns the required number of assignments.
    Time complexity: O(2^N)
    Space complexity: O(N), the depth of recursion tree
    """

    def dfs(index, total):
        if index == n:
            values[0] += 1 if total == S else 0
            return
        dfs(index + 1, total + nums[index])
        dfs(index + 1, total - nums[index])

    n, values = len(nums), [0]
    dfs(0, 0)
    return values[0]


def find_target_sum_ways_v2(nums, S):
    """ It can be easily observed that in the last approach, a lot of redundant function calls could be made with the
        same value of 'index' as the current index and the same value of 'total' as the current sum, since the same
        values could be obtained through multiple paths in the recursion tree. In order to remove this redundancy,
        we make use of memoization as well to store the results which have been calculated earlier.
        Thus, for every call to dfs(index, total), we store the result obtained in memo[(index, total)]. By making use
        of memoization, we can prune the search space to a good extent.
    Time complexity: O(N * L), where L = (largest sum that can be created - smallest sum that can be created). For
    example, for input array [1, 2, 3], the largest sum that can be created from input is 1 + 2 + 3 = 6, and the
    smallest sum that can be created is -1 - 2 - 3 = -6, so L= 6- (-6) = 12
    Space complexity: O(N)
    """

    def dfs(index, total):
        if index == n:
            return 1 if total == S else 0
        if (index, total) not in memo:
            plus = dfs(index + 1, total + nums[index])
            minus = dfs(index + 1, total - nums[index])
            memo[(index, total)] = plus + minus
        return memo[(index, total)]

    n, memo = len(nums), {}
    return dfs(0, 0)


class Test(unittest.TestCase):
    data = [([1, 1, 1, 1, 1], 3, 5)]

    def test_find_target_sum_ways(self):
        for test_nums, test_s, result in self.data:
            self.assertEqual(result, find_target_sum_ways_v1(test_nums, test_s))
            self.assertEqual(result, find_target_sum_ways_v2(test_nums, test_s))


if __name__ == '__main__':
    unittest.main()
