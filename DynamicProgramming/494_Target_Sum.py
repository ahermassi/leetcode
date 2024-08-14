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
    """ Note that for the evaluation of the current row of dp, only the values of the last row are needed. Thus, we can
         save some space by using a 1D dp array instead.

         The only change we need to make is that we have to create an array next of the same size as dp so that we can
         update it while scanning through dp since it is not safe to mutate dp when the iteration is in progress. After
         the iteration is completed, we set dp equal to next and create a new empty array next before the next iteration
         starts, and so on.

    Time complexity: O(N * L)
    Space complexity: O(L)
    """
    n, nums_sum = len(nums), sum(nums)
    if not -nums_sum <= target <= nums_sum:
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
    """ BFS. Similar to 78- Subsets.

         We can use a hashmap to store all the possible sums using all the numbers with +/- signs and return the number
         of ways the target sum can be obtained. It is a special implementation of BFS, where each element in nums is
         one level.

    Time complexity: O(2^N), since we are trying + and - for every element in the array
    Space complexity: O(L), where L = largest sum that can be obtained - smallest sum that can be obtained = 2 * sum
    """
    # At the beginning, we there is only one way to get sum=0. Before we assign + or - to the first element, sum=0.
    counter = {0: 1}
    for num in nums:
        next_counter = defaultdict(int)
        for sum, count in counter.items():
            next_counter[sum + num] += count
            next_counter[sum - num] += count
        counter = next_counter
    return counter[target]


def find_target_sum_ways_v6(nums, target):
    """ Bottom-Up Dynamic Programming. Similar to 416- Partition Equal Subset Sum.

         Let's say we have nums = [1,1,1,1,1] and target = 1. We need to add + or - signs in front of the integers.
         e.g +1 +1 +1 -1 -1 = 1.
         Essentially, what we are doing is that we are just splitting the numbers into TWO SUBSETS, one with all
         positive numbers and the other with all negative numbers:

         (1 , 1 , 1) => with positive signs
         (1 , 1) => with negative signs

         We are then calculating the difference of the sum of these two sets and comparing it with the target:
         (1 , 1 , 1) => sum = 3
         (1 , 1) => sum = 2
         diff = 3-2 = 1 = target

         So we just need to find all such pairs of subsets whose sum difference is equal to the target.
         Consider S1 and S2 to be one such pair, then the following equations hold:

                    S1 - S2 = target
                    S1 + S2 = sum of all the elements

        By simplifying the 2 equations we get:

                    2* S1 = target + sum of all the elements
                    S1 = (target + sum of all the elements) / 2

        So, this problem now reduces to finding the count of subsets that have a sum equal to S1.

        Actually, this is a 0/1 knapsack problem. For each number, we can either pick it or not pick it. Let's assume
         that:

                    dp[i][j] = number of subsets up to and including index i that sum up to j

         Base case 1: dp[0][nums[0]] = 1; the first number is a subset that sums up to the first number's value
         Base case2: dp[i][0] = 1 for all 0 <= i < n; we can form subsets whose sum is 0 up to each index by not
         including any number.

         Transition function: for each number, if we don't pick it, dp[i][j] = dp[i-1][j], which means if a subset of
         the first i-1 elements sum up to j, a subset of the first i elements also sums up to j just by not picking
         nums[i].
         If we pick nums[i], dp[i][j] = dp[i-1][j-nums[i]], which means that j is the sum of the current element nums[i]
         and the other remaining previous numbers. Thus, the transition function is:

                dp[i][j] = dp[i-1][j] + (dp[i-1][j-nums[i]] IF j >= nums[i])

    Time complexity: O(N * (target + sum))
    Space complexity: O(N * (target + sum))
    """
    n = len(nums)
    nums_sum = sum(nums)
    if not -nums_sum <= target <= nums_sum or (nums_sum + target) % 2:
        return 0
    target = (target + nums_sum) // 2
    dp = [[0] * (target + 1) for _ in range(n)]
    # dp[i][j] = number of subsets up to and including index i that sum up to j
    if nums[0] < target + 1:
        dp[0][nums[0]] = 1
    for i in range(n):
        # ATTENTION: it's += instead of =. If nums[0] == 0, then we have to consider two choices : include this 0 to
        # form a subset with sum 0, or exclude this 0 to form a subset with sum 0. dp[0][nums[0]] = dp[0][0] already
        # accounted the first choice in the previous initialization.
        dp[i][0] += 1
    for i in range(1, n):
        for j in range(target + 1):
            dp[i][j] = dp[i - 1][j]
            if j >= nums[i]:
                dp[i][j] += dp[i - 1][j - nums[i]]
    return dp[n - 1][target]


class Test(unittest.TestCase):
    data = [([1, 1, 1, 1, 1], 3, 5)]

    def test_find_target_sum_ways(self):
        for test_nums, test_s, result in self.data:
            self.assertEqual(result, find_target_sum_ways_v1(test_nums, test_s))
            self.assertEqual(result, find_target_sum_ways_v2(test_nums, test_s))
            self.assertEqual(result, find_target_sum_ways_v3(test_nums, test_s))
            self.assertEqual(result, find_target_sum_ways_v4(test_nums, test_s))
            self.assertEqual(result, find_target_sum_ways_v5(test_nums, test_s))
            self.assertEqual(result, find_target_sum_ways_v6(test_nums, test_s))


if __name__ == '__main__':
    unittest.main()
