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


# Video explanation: https://www.youtube.com/watch?v=vBdo7wtwlXs


def jump_v3(nums):
    """ This solution uses the same concept of the previous algorithm but with a twist.

         Let's say the range of the current jump is [cur_jump_start, cur_jump_end], farthest_reach is the farthest point
         that all points in [cur_jump_start, cur_jump_end] can reach. Once the current index reaches cur_jump_end, then
         trigger another jump by setting the new cur_jump_end to farthest_reach, then repeat the steps above.

         Note that we exclude the last element from the iteration because as soon as we reach the last element, we do
         not need to jump any further.

         This is an implicit BFS solution. i == cur_jump_end means we visited all the nodes in the current level.
         Incrementing 'jumps' is like incrementing the level we are on. cur_jump_end = farthest_reach is like getting
         the queue size (level size) for the next level we are traversing.

        The idea is pretty intuitive. Think of each of the indices as missile bases, each having a max range defined by
        the value at that index. Now say, for example, we can reach 100 miles from base 0. If the target is in that
        range, then well and good, it's just a direct hop. If not, we start our search for better launchers moving
        forward.

        We discover that base 1 gives better coverage i.e. > 100 miles, so we may simply move to that base.
        This counts as an extra hop. However, that this is not necessarily the best choice. Within the range of this
        launcher (at base 0), there could be other bases providing better coverage. Our job is to iterate through and
        choose the launcher that improves our current range and reaches the target first.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    n, jumps = len(nums), 0
    cur_jump_end = farthest_reach = 0  # cur_jump_end marks the end of the range that we can jump to
    for i in range(n - 1):
        farthest_reach = max(farthest_reach, i + nums[i])  # Extend current coverage/reach as further as possible
        if i == cur_jump_end:  # If we have come to the end of the current jump, we need to make another jump
            cur_jump_end = farthest_reach
            jumps += 1
            # Check if we reached the end of the array already (optional)
            # if cur_jump_end >= n - 1:
            #     return jumps
    return jumps
