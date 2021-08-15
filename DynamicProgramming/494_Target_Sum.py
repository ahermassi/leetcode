""" You are given a list of non-negative integers, a1, a2, ..., an, and a target, S. Now you have 2 symbols + and -.
For each integer, you should choose one from + and - as its new symbol.
Find out how many ways to assign symbols to make sum of integers equal to target S. """

import unittest2 as unittest


def find_target_sum_ways_v1(nums, target):
    """ Brute force. TLE
        The brute force approach is based on recursion. We need to try to put both the + and - symbols at every
        location in the given nums array and find out the assignments which lead to the required result 'target'.
        For this, we make use of a recursive function dfs(index, cur_sum), which returns the assignments leading to the
        sum 'target', starting from index 'index' onwards, provided the sum of elements up to the (index -1)th element
        is 'cur_sum'. This function appends a + sign and a - sign both to the element at the current index and calls
        itself with the updated cur_sum as (cur_sum + nums[index]) and (cur_sum - nums[index]) respectively along with
        the updated current index as (index + 1). Whenever we reach the end of the array, we compare the sum obtained
        with 'target'. If they are equal, we increment the count value to be returned.
        Thus, the function call dfs(0, 0) returns the required number of assignments.
    Time complexity: O(2^N)
    Space complexity: O(N), the depth of recursion tree
    """

    def dfs(index, cur_sum):
        if index == n:
            res[0] += 1 if cur_sum == target else 0
            return
        dfs(index + 1, cur_sum + nums[index])
        dfs(index + 1, cur_sum - nums[index])

    n, res = len(nums), [0]
    dfs(0, 0)
    return res[0]


def find_target_sum_ways_v2(nums, target):
    """ It can be easily observed that in the last approach, a lot of redundant function calls could be made with the
        same value of 'index' as the current index and the same value of 'cur_sum' as the current sum, since the same
        values could be obtained through multiple paths in the recursion tree. In order to remove this redundancy,
        we make use of memoization as well to store the results which have been calculated earlier.
        Thus, for every call to dfs(index, cur_sum), we store the result obtained in memo[(index, cur_sum)]. By making
        use of memoization, we can prune the search space to a good extent.
    Time complexity: O(N * L), where L = (largest sum that can be created - smallest sum that can be created). For
    example, for input array [1, 2, 3], the largest sum that can be created from input is 1 + 2 + 3 = 6, and the
    smallest sum that can be created is -1 - 2 - 3 = -6, so L= 6- (-6) = 12
    Space complexity: O(N)
    """

    def dfs(index, cur_sum):
        if index == n:
            return 1 if cur_sum == target else 0
        if (index, cur_sum) in memo:
            return memo[(index, cur_sum)]
        plus = dfs(index + 1, cur_sum + nums[index])
        minus = dfs(index + 1, cur_sum - nums[index])
        memo[(index, cur_sum)] = plus + minus
        return memo[(index, cur_sum)]

    n, memo = len(nums), {}
    return dfs(0, 0)

# Nice read: https://leetcode.com/problems/target-sum/discuss/455024/DP-IS-EASY!-5-Steps-to-Think-Through-DP-Questions.


def find_target_sum_ways_v3(nums, target):
    """ Dynamic programming.
        The idea behind this approach is as follows. Suppose we can find out the number of times a particular sum, say
        sum_i, is possible up to a particular index, say i, in the given nums array, which is given by say count_i.
        Now, we can find out the number of times the sum (sum_i + nums[i]) can occur easily as count_i. Similarly, the
        number of times the sum (sum_i - nums[i]) occurs is also given by count_i.
        This is a classic knapsack problem. In knapsack, we decide whether we choose an element or not. In this
        question, we decide whether we add an element or its negation.
        Let dp[i][j] be the number of ways for the first i elements to reach a sum j. We can easily observe that:

            dp[i][j] = dp[i - 1][j - nums[i]] + dp[i - 1][j + nums[i]]

        Another part which is quite confusing is the return value. Notice that the dp's j range -sum --> 0 --> +sum,
        where 'sum' is the sum of all elements in the array. -sum and +sum are the lower bound and upper bound,
        respectively, of the sum of different assignments of - and + signs corresponding to all elements multiplied by
        -1 and +1, respectively. Therefore, to make j run starting from 0, we add an offset = sum(nums). This way, j is
        in the range [0, 2 * sum(nums)] instead of [-sum(nums), sum(nums)].
    Time complexity: O(N * L), where L = largest sum that can be created - smallest sum that can be created
    Space complexity: O(N * L)
    """
    n, nums_sum = len(nums), sum(nums)
    if nums_sum < target or -nums_sum > target:
        return 0
    # The possible range of sums of different combinations is [0, 2 * nums_sum]
    dp = [[0] * (2 * nums_sum + 1) for _ in range(n)]
    dp[0][nums[0] + nums_sum] = 1  # Without the offset, this is dp[0][nums[0]] = 1: There is only 1 way to get a sum of
    # nums[0] using only the 0th element of nums
    dp[0][-nums[0] + nums_sum] += 1  # If nums[0] == 0, then we have 2 ways (+0 and -0) of getting the zero sum
    for i in range(1, n):
        for j in range(2 * nums_sum + 1):
            plus = minus = 0
            # If (j - nums[i]) or (j + nums[i]) is in correct range, we can use dp[i - 1] to generate next state
            if j - nums[i] >= 0:
                minus = dp[i - 1][j - nums[i]]
            if j + nums[i] <= 2 * nums_sum:
                plus = dp[i - 1][j + nums[i]]
            dp[i][j] = plus + minus
    return dp[n - 1][target + nums_sum]  # Without the offset, this would be dp[n-1][target]: How many way to get
    # 'target' using the first (n-1) elements, or the entire array


def find_target_sum_ways_v4(nums, target):
    """ If we look closely at the last solution, we can observe that for the evaluation of the current row of dp,
        only the values of the last row of dp are needed. Thus, we can save some space by using a 1D dp array instead
        of a 2D dp array. The only difference that needs to be made is that now the same dp array will be updated for
        every row traversed.
    Time complexity: O(N * L)
    Space complexity: O(L)
    """
    n, nums_sum = len(nums), sum(nums)
    if nums_sum < target or -nums_sum > target:
        return 0
    cur = [0] * (2 * nums_sum + 1)
    cur[nums[0] + nums_sum] = 1
    cur[-nums[0] + nums_sum] += 1
    for i in range(1, n):
        next = [0] * (2 * nums_sum + 1)
        for j in range(2 * nums_sum + 1):
            if j - nums[i] >= 0:
                next[j] += cur[j - nums[i]]
            if j + nums[i] <= 2 * nums_sum:
                next[j] += cur[j + nums[i]]
        cur = next
    return cur[target + nums_sum]


class Test(unittest.TestCase):
    data = [([1, 1, 1, 1, 1], 3, 5)]

    def test_find_target_sum_ways(self):
        for test_nums, test_s, result in self.data:
            self.assertEqual(result, find_target_sum_ways_v1(test_nums, test_s))
            self.assertEqual(result, find_target_sum_ways_v2(test_nums, test_s))
            self.assertEqual(result, find_target_sum_ways_v3(test_nums, test_s))
            self.assertEqual(result, find_target_sum_ways_v4(test_nums, test_s))


if __name__ == '__main__':
    unittest.main()
