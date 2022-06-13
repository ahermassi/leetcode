""" Given an array of non-negative integers nums, you are initially positioned at the first index of the array.

Each element in the array represents your maximum jump length at that position.

Your goal is to reach the last index in the minimum number of jumps.

You can assume that you can always reach the last index. """


def jump(nums):
    """" Bottom-Up Dynamic Programming.

         Let dp[i] be the minimum number of jumps required to reach the last index if we're positioned at index i.

         We start from the last index. We need 0 jumps from nums[n-1] to reach the end. We store this as dp[n - 1] = 0
         and then iteratively solve this for each previous index till the 0th index.

         For each index, we explore all the possible jump sizes available to us.

    Time complexity: O(N^2)
    Space complexity: O(N)
    """
    n = len(nums)
    dp = [float('inf')] * n
    dp[n - 1] = 0
    for i in reversed(range(n - 1)):
        max_index_to_jump = min(i + nums[i], n - 1)  # The maximum index we can jump to starting at index i
        for j in range(i + 1, max_index_to_jump + 1):
            dp[i] = min(dp[i], dp[j] + 1)  # Jump to j and take it from there. Add +1 to account for current jump to j.
    return dp[0]