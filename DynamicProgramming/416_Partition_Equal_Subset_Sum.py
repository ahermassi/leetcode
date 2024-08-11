""" Given a non-empty array containing only positive integers, find if the array can be partitioned into two subsets
such that the sum of elements in both subsets is equal. """

import unittest2 as unittest


def can_partition_v1(nums):
    """ Brute force. BFS-like. Similar to 78- Subsets.

         The problem to find the subset with a sum equals a given target. Here target is half the total sum of numbers
         in the list. It must be noted that the total sum of an array must be even, only then we can divide it into 2
         equal subsets.

         Note that finding a subset with a sum equal to a given target is different from subarray sum equals k.
         A subarray is a contiguous sequence of array elements, whereas the subset could consist of any array elements
         regardless of the sequence, but each array element must belong to exactly one subset.

         Each number in the array can be picked or not picked to form the subset of array to have a target sum. Here we
         can scan through the array and store the sums of the subsets that include the current number and those that
         don't. We can use a set to store the sums to avoid duplicates.

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
    """ Top-Down Dynamic Programming.

         We have to find a subset in the array whose sum is equal to sum(nums) / 2. The brute force approach would be to
         generate all the possible subsets of the array and return true if we find a subset with the required sum.

         For a given array element x, there could be either of 2 possibilities:

            - x is included in subset sum. subset_sum = subset_sum + x
            - x is not included in subset sum, so we must take previous sum without x

        We can use DFS and recursively calculate the subset sum for each case and check if either of them is true.

    Time complexity: O(N * sum), where N is the number of elements in nums and sum is the sum of all elements in nums.
    In the worst case where there is no overlapping calculation, the maximum number of entries in the memo would be
    N * sum. For each entry, overall we could consider that it takes constant time, i.e. each invocation of dfs() at
    most emits one entry in the memo. The overall computation is proportional to the number of entries in memo.
    Space complexity: O(N + N * sum), space used by the call stack and memo
    """

    def dfs(index, remaining):
        if not remaining:
            return True
        if index == n:
            return False
        if (index, remaining) in memo:
            return memo[(index, remaining)]
        # Either take the current num or leave it
        memo[(index, remaining)] = dfs(index + 1, remaining - nums[index]) or dfs(index + 1, remaining)
        return memo[(index, remaining)]

    total = sum(nums)
    if total % 2 == 1:
        return False
    target = total // 2
    n, memo = len(nums), {}
    return dfs(0, target)


def can_partition_v3(nums):
    """ Top-Down Dynamic Programming with pruning.

        Similar to the previous solution but it prunes the search space by sorting the nums array.

    Time complexity: O(N * sum)
    Space complexity: O(N + N * sum), space used by the call stack and memo
    """

    def dfs(index, remaining):
        if not remaining:
            return True
        if index == n:
            return False
        # Early exit. Neither the current element nor its successors can contribute to the final subset as they are
        # greater than the remaining target
        if nums[index] > remaining:
            return False
        if (index, remaining) in memo:
            return memo[(index, remaining)]
        # Either take the current num or leave it
        memo[(index, remaining)] = dfs(index + 1, remaining - nums[index]) or dfs(index + 1, remaining)
        return memo[(index, remaining)]

    total = sum(nums)
    if total % 2 == 1:
        return False
    target = total // 2
    n, memo = len(nums), {}
    nums.sort()
    return dfs(0, target)


def can_partition_v4(nums):
    """ Bottom-Up Dynamic Programming.

         This problem is essentially about finding whether there are some numbers in a set that sum up to a specific
         value. In this case, the value is sum(nums) / 2.

         Actually, this is a 0/1 knapsack problem. For each number, we can either pick it or not pick it. Let's assume
         that:

                    dp[i][j] = whether sum j can be obtained from a subset of the first i numbers

         If we can find such subset of numbers from 0 to i whose sum is j, dp[i][j] is true, otherwise it is false.

         Base case: dp[0][0] = true (zero numbers sum up to 0 is true)

         Transition function: for each number, if we don't pick it, dp[i][j] = dp[i-1][j], which means if a subset of
         the first i-1 elements sum up to j, a subset of the first i elements also sums up to j just by not picking
         nums[i].
         If we pick nums[i], dp[i][j] = dp[i-1][j-nums[i]], which means that j is the sum of the current element nums[i]
         and the other remaining previous numbers. Thus, the transition function is:

                dp[i][j] = dp[i-1][j] OR (j >= nums[i] AND dp[i-1][j-nums[i]])

    Time complexity: O(N * sum/2)
    Space complexity: O(N * sum/2)
    """
    total = sum(nums)
    if total % 2 == 1:
        return False
    target, n = total // 2, len(nums)
    dp = [[False] * (target + 1) for _ in range(n)]
    dp[0][0] = True
    for i in range(1, n):
        for j in range(target + 1):
            if dp[i - 1][j] or j >= nums[i] and dp[i - 1][j - nums[i]]:
                dp[i][j] = True
    return dp[n - 1][target]


def can_partition_v5(nums):
    """ We can optimize in space. We used a two dimensional array to solve the problem, but we can also use a one
        dimensional array of size (target+1).
        Why iterate from 0 to (target + 1) in reverse order?
        dp[i][j] only depends on the previous row, so we can optimize the space by only using 2 rows instead of the
        matrix. Let's say array1 and array2. We can also see that the column indices of dp[i - 1][j - nums[i] and
        dp[i - 1][j] are <= j. The conclusion we can draw is: The elements of the previous row whose column index
        is > j (i.e. dp[i - 1][j + 1 : n - 1]) will not affect the update of dp[i][j] since we will not touch them:

                			  j
	            . . . . . . . . . . . .
	            . . . . . . . . . . . .
	            . . ? . . ? x x x x x x  We will not touch x for dp[i][j]
            i	. . . . . # . . . . . .  # dp[i][j]
	            . . . . . . . . . . . .
	            . . . . . . . . . . . .
	            . . . . . . . . . . . .
	            . . . . . . . . . . . .
	            . . . . . . . . . . . .

        Thus, if we merge array1 and array2 into a single array array, if we update array backwards, all dependencies
        are not touched!

                (n represents new value, i.e. updated)
	            . . ? . . ? n n n n n n n
                        #

        However, if we update forwards, dp[j - nums[i]] is updated overwritten, we cannot use it:

                (n represents new value, i.e. updated)
	            n n n n n ? . . . . . .  where another ? goes? Oops, it is overwritten, we lost it :(
                        #

    Time complexity: O(N * sum/2)
    Space complexity: O(sum/2)
    """
    total = sum(nums)
    if total % 2 == 1:
        return False
    target, n = total // 2, len(nums)
    dp = [False] * (target + 1)
    dp[0] = True
    for num in nums:
        # If we go from left to right, dp[j - num] has been updated during the current iteration and the status from
        # last iteration is lost
        for j in reversed(range(target + 1)):
            if j - num >= 0:
                dp[j] = dp[j] or dp[j - num]
    return dp[target]


class Test(unittest.TestCase):
    data = [([1, 5, 11, 5], True), ([1, 2, 3, 5], False)]

    def test_can_partition(self):
        for test_nums, result in self.data:
            self.assertEqual(result, can_partition_v1(test_nums))
            self.assertEqual(result, can_partition_v2(test_nums))
            self.assertEqual(result, can_partition_v3(test_nums))
            self.assertEqual(result, can_partition_v4(test_nums))
            self.assertEqual(result, can_partition_v5(test_nums))


if __name__ == '__main__':
    unittest.main()

