""" You are given a list of non-negative integers, a1, a2, ..., an, and a target, S. Now you have 2 symbols + and -.
For each integer, you should choose one from + and - as its new symbol.
Find out how many ways to assign symbols to make sum of integers equal to target S. """

from collections import defaultdict
import unittest2 as unittest


def find_target_sum_ways_v1(nums, target):
    """ Brute force. TLE

         The brute force approach is based on recursion. We need to try to put both the + and - symbols at every
         location in the given nums array and find out the assignments which lead to the required result 'target'.

         For this, we make use of a recursive function dfs(index, cur_sum), which constructs the assignments leading to
         the target sum, starting from the current index, provided the sum of elements up to index-1 is cur_sum.
         This function appends a + sign then a - sign to the element at the current index and calls itself with the
         updated cur_sum as cur_sum+nums[index] and cur_sum-nums[index], respectively, along with the updated current
         index as index+1.

         Whenever we reach the end of the array, we compare the sum obtained with the target. If they are equal, we
         increment the count value to be returned.

         Thus, the call dfs(0, 0) constructs all the possible assignments.

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


# Video explanation: https://youtu.be/g0npyaQtAQM
def find_target_sum_ways_v2(nums, target):
    """ Top-Down Dynamic Programming.

         In the last implementation, we can observe that a lot of redundant function calls were made with the same
         values of current index cumulative sum, since the same values could be obtained through multiple paths in the
         recursion tree.

         In order to remove this redundancy, we make use of memoization to store the results which have been calculated
         earlier. Thus, for every call to dfs(index, cur_sum), we store the result obtained in memo[(index, cur_sum)].
         By making use of memoization, we can prune the search space.

    Time complexity: O(N * L), where L = (largest sum that can be obtained - smallest sum that can be obtained). For
    example, for nums = [1, 2, 3], the largest sum that can be obtained is 1 + 2 + 3 = 6, and the smallest sum is
    -1 - 2 - 3 = -6, so L= 6- (-6) = 12. In other words, L is in the range [-sum(nums), sum(nums)].
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
    """ Bottom-Up Dynamic programming.

         The idea behind this approach is as follows. Suppose we can find out the number of expressions that evaluate to
         S up to index i in the given nums array. The total number of expressions is given by, say, T.

         Now, we can deduce that the number of times the sum S+nums[i] can be obtained is T. Similarly, the number of
         times the sum S+nums[i] can be obtained is also T.

         Thus, if we know all the sums S_j which are possible up to the jth index by using various assignments, along
         with the corresponding count of assignments T_j, leading to the same sum, we can determine all the sums
         possible up to the (j+1)th index along with the corresponding count of assignments leading to the new sums.

         This is a classic knapsack problem. In knapsack, we decide whether to choose an element or not. In this
         problem, we decide whether we add an element or its negation.

         Let dp[i][j] be the number of assignments which can lead to a sum of j up to index i. We can observe that:

            dp[i][j] = dp[i - 1][j - nums[i]] + dp[i - 1][j + nums[i]]

        !!! IMPORTANT !!!

        Notice that the dp's j range is [-sum, sum], where 'sum' is the sum of all elements in the array. -sum and +sum
        are the lower bound and upper bound, respectively, of the sum of different assignments of - and + signs
        corresponding to all elements multiplied by -1 and +1, respectively. Therefore, we need to add an offset of
        sum to the j indices (column number) to map all the sums obtained to a positive range. This way, j moves from
        range [-sum(nums), sum(nums)] to the range [0, 2 * sum(nums)] .

    Time complexity: O(N * L), where L = largest sum that can be obtained - smallest sum that can be obtained = 2 * sum
    Space complexity: O(N * L)
    """
    n, nums_sum = len(nums), sum(nums)
    if not -nums_sum <= target <= nums_sum:
        return 0
    # The possible range of sums of different combinations is [0, 2 * nums_sum]
    dp = [[0] * (2 * nums_sum + 1) for _ in range(n)]
    # Without the offset, this is dp[0][nums[0]] = 1: there is only 1 way to get a sum of nums[0] using only the 0th
    # element of nums
    dp[0][nums[0] + nums_sum] = 1
    # If nums[0] == 0, then we have 2 ways (+0 and -0) of getting a sum of zero
    dp[0][-nums[0] + nums_sum] += 1
    for i in range(1, n):
        for j in range(2 * nums_sum + 1):
            plus = minus = 0
            # If (j - nums[i]) or (j + nums[i]) is in a valid range, we can use dp[i - 1] to calculate the next state
            if j - nums[i] >= 0:
                minus = dp[i - 1][j - nums[i]]
            if j + nums[i] < 2 * nums_sum + 1:
                plus = dp[i - 1][j + nums[i]]
            dp[i][j] = plus + minus
    # Without the offset, this would be dp[n-1][target]: how many way to get target using the first n-1 elements, i.e.
    # the entire array
    return dp[n - 1][target + nums_sum]


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


def find_target_sum_ways_v5(nums, target):
    """ We can use a dictionary to store all possible sums using all the numbers with +/- signs and return the number
        of ways the target sum can be obtained. It is a special implementation of level-order BFS, where each element
        in nums is one level.
    Time complexity: O(2^N), since we are trying + and - for every element in the array
    Space complexity: O(L), where L = largest sum that can be created - smallest sum that can be created
    """
    counter = {0: 1}  # At first, we have one way with sum = 0. Before we assign + or - to the first element, sum = 0.
    for num in nums:
        next_counter = defaultdict(int)
        for sum, count in counter.items():
            next_counter[sum + num] += count
            next_counter[sum - num] += count
        counter = next_counter
    return counter[target]


class Test(unittest.TestCase):
    data = [([1, 1, 1, 1, 1], 3, 5)]

    def test_find_target_sum_ways(self):
        for test_nums, test_s, result in self.data:
            self.assertEqual(result, find_target_sum_ways_v1(test_nums, test_s))
            self.assertEqual(result, find_target_sum_ways_v2(test_nums, test_s))
            self.assertEqual(result, find_target_sum_ways_v3(test_nums, test_s))
            self.assertEqual(result, find_target_sum_ways_v4(test_nums, test_s))
            self.assertEqual(result, find_target_sum_ways_v5(test_nums, test_s))


if __name__ == '__main__':
    unittest.main()
