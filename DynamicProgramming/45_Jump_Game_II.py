""" Given an array of non-negative integers nums, you are initially positioned at the first index of the array.

Each element in the array represents your maximum jump length at that position.

Your goal is to reach the last index in the minimum number of jumps.

You can assume that you can always reach the last index. """


def jump_v1(nums):
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


# Video explanation: https://www.youtube.com/watch?v=dJ7sWiOoK7g


def jump_v2(nums):
    """  Imagine that we are at index i in the array. The element in the current position defines the maximum distance
         that we can jump. Therefore, our next step will fall somewhere in the range [start, end], where start is the
         place right next to us and end is (i + nums[i]). Then the question is, where to jump?

         If we greedily jump as far as we can, we may end up in a place with small jump power.
         If we choose to only jump 1, we may have a strong jump power for the next jump.

         Let's think about it in the following way. Our next move will fall somewhere between [start, end], and to find
         the minimum number of jumps to reach the end of the array, we must determine which place will take us the
         farthest in the next jump.

         As you may notice, we are using a greedy approach: Always jump to the place that will take us the farthest.

         The idea is to maintain two pointers 'start' and 'end', initially set to 0. So points between 0 and nums[0] are
         the ones we can reach by using just 1 jump.

         Next, we want to find points we can reach using 2 jumps, so our new 'start' will be set equal to (end + 1),
         and our new 'end' will be set equal to the farthest point we can reach by two jumps. which is:

                    end = max(i + nums[i] for i in range(start, end + 1)

        This problem has a nice BFS structure.

        Let's illustrate it using the example nums = [2, 3, 1, 1, 4] in the problem statement.

        We are initially at position 0. Then we can move at most nums[0] steps from it. So, after one move, we may reach
        nums[1] = 3 or nums[2] = 1. So these nodes are reachable in 1 move. From these nodes, we can further move to
        nums[3] = 1 and nums[4] = 4. Now we can see that the target nums[4] = 4 is reachable in 2 moves.

        Putting these into code, we keep two pointers 'start' and 'end' that record the current range of the starting
        nodes. Each time after we make a move, update 'start' to be (end + 1) and 'end' to be the farthest index that
        can be reached in 1 move from the current [start, end].

    Time complexity: O(N), we visit each element in the array only once
    Space complexity: O(1)
    """
    n, jumps = len(nums), 0
    start = end = 0
    while end < n - 1:
        farthest_reach = 0
        for i in range(start, end + 1):
            farthest_reach = max(farthest_reach, i + nums[i])
        start, end = end + 1, farthest_reach
        jumps += 1
    return jumps
