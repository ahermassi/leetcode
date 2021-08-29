""" Given a non-empty array containing only positive integers, find if the array can be partitioned into two subsets
such that the sum of elements in both subsets is equal. """

import unittest2 as unittest


def can_partition_v1(nums):
    """ Brute force.
        Each number in the array can be picked or not picked to form the subset of array to have a target sum. Here we
        can scan through the array and store the sums of the subsets that include or not include the current number.
        We can use a set to store the sums to avoid duplicates.
        Example: nums = [2, 8, 3, 1], target = 14 / 2 = 7, sums = {0}
        num = 2, sums = {0, 0+2} = {0, 2}
        num = 8, sums = {0, 2, 0+8, 2+8} = {0, 2} (0+8 and 2+8 were omitted as they exceed target)
        num = 3, sums = {0, 2, 0+3, 2+3} = {0, 2, 3, 5}
        nums = 1, sums = {0, 2, 3, 5, 0+1, 2+1, 3+1, 5+1} = {0, 2, 3, 5, 1, 4, 6}
        --> target = 7 doesn't exist in sums, so the partitioning is not possible.
    Time complexity: O(N * sum/2)
    Space complexity: O(N * sum/2)
    """
    total = sum(nums)
    if total % 2 == 1:
        return False
    target = total // 2
    sums = {0}
    for num in nums:
        sums_with_num = []
        for s in sums:
            if num + s == target:
                return True
            if num + s < target:
                sums_with_num.append(num + s)
        sums.update(sums_with_num)
    return False


def can_partition_v2(nums):
    """ DFS + Memoization.
        We have to find a subset in the array whose smu is equal to sum(nums) / 2. The brute force approach would be to
        generate all the possible subsets of the array and return true if we find a subset with the required sum.
    Time complexity: O(2^N), the recursive call takes the form of a binary tree where there are 2 possibilities for
    every array element and the maximum depth of the tree could be N.
    Space complexity: O(N), space be used by the recursion stack
    """

    def dfs(index, remaining):
        if not remaining:
            return True
        if index == n:
            return False
        if (index, remaining) not in cache:
            # Either take the current num or leave it
            cache[(index, remaining)] = dfs(index + 1, remaining - nums[index]) or dfs(index + 1, remaining)
            return cache[(index, remaining)]
        return False

    total = sum(nums)
    if total % 2 == 1:
        return False
    target = total // 2
    n, cache = len(nums), {}
    return dfs(0, target)


def can_partition_v3(nums):
    """ This problem is essentially finding whether there are some numbers in a set which sum to a specific value. In
        this problem, the value is sum/2.
        Actually, this is a 0/1 knapsack problem. For each number, we can pick it or not. Let us assume that:
            dp[i][j] = whether the specific sum j can be gotten from some of the first i numbers
        If we can find such a series of numbers from 0..i whose sum is j, dp[i][j] is true, otherwise it is false.
        Base case:
            dp[0][0] = true (zero numbers consist of sum 0 is true)
        Transition function: For each number, if we don't pick it, dp[i][j] = dp[i-1][j], which means if some of the
        first (i - 1) elements has made it to j, dp[i][j] would also make it to j (we can just ignore nums[i]).
        If we pick nums[i], dp[i][j] = dp[i-1][j-nums[i]], which means that j is composed of the current value nums[i]
        and the remaining composed of other previous numbers. Thus, the transition function is:
            dp[i][j] = dp[i-1][j] OR dp[i-1][j-nums[i]]
    Time complexity: O(N * sum/2)
    Space complexity: O(N * sum/2)
    """
    total = sum(nums)
    if total % 2 == 1:
        return False
    target, n = total // 2, len(nums)
    dp = [[False for _ in range(target + 1)] for _ in range(n)]
    dp[0][0] = True
    for i in range(1, n):
        dp[i][0] = True
    for i in range(1, n):
        for j in range(1, target + 1):
            if j < nums[i]:
                dp[i][j] = dp[i - 1][j]
            else:
                dp[i][j] = dp[i - 1][j] or dp[i - 1][j - nums[i]]
    return dp[n - 1][target]


def can_partition_v4(nums):
    """ We can optimize in space. We used a two dimensional array to solve the problem, but we can also use a one
        dimensional array of size (target+1).
    Time complexity: O(N * sum/2)
    Space complexity: O(sum/2)
    """
    total = sum(nums)
    if total % 2 == 1:
        return False
    target, n = total // 2, len(nums)
    dp = [False for _ in range(target + 1)]
    dp[0] = True
    for i in range(1, n):
        for j in range(1, target + 1):
            if j >= nums[i]:
                dp[j] = dp[j - 1] or dp[j - nums[i]]
    return dp[target]


class Test(unittest.TestCase):
    data = [([1, 5, 11, 5], True), ([1, 2, 3, 5], False)]

    def test_can_partition(self):
        for test_nums, result in self.data:
            self.assertEqual(result, can_partition_v1(test_nums))
            self.assertEqual(result, can_partition_v2(test_nums))
            self.assertEqual(result, can_partition_v3(test_nums))
            self.assertEqual(result, can_partition_v4(test_nums))


if __name__ == '__main__':
    unittest.main()

