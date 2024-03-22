""" Given an array of non-negative integers nums, you are initially positioned at the first index of the array.

Each element in the array represents your maximum jump length at that position.

Your goal is to reach the last index in the minimum number of jumps.

You can assume that you can always reach the last index. """


def jump_v1(nums):
    """" Bottom-Up Dynamic Programming.

         Let dp[i] be the minimum number of jumps needed to reach the last index if we're positioned at index i.

         We start from the last index. We need 0 jumps from that position to reach the end. We express this as
         dp[n-1] = 0. Then, iteratively, solve for each previous index until the 0th index.

         For each index, we explore all the possible jump sizes available to us.

    Time complexity: O(N^2)
    Space complexity: O(N)
    """
    n = len(nums)
    dp = [float('inf')] * n
    dp[n - 1] = 0
    for i in reversed(range(n - 1)):
        # The maximum index we can jump to starting at index i. min() is used to avoid going out of bounds.
        farthest_reachable_index = min(i + nums[i], n - 1)
        for j in range(i, farthest_reachable_index + 1):
            # Jump to j and take it from there
            dp[i] = min(dp[i], dp[j] + 1)
    return dp[0]


# Video explanation: https://www.youtube.com/watch?v=dJ7sWiOoK7g
def jump_v2(nums):
    """  Imagine that we are at index i in the array. The element in the current position defines the maximum distance
          that we can jump. Therefore, our next step will fall somewhere in the range [start, end], where start is the
          next index (i + 1) and end is (i + nums[i]). Then the question is, where to jump?

          If we greedily jump as far as we can, we may end up at an index with small jump power.
          If we choose to jump only 1 step, we may have a strong jump power for the next jump.

          Let's think about it in the following way. The next move will fall somewhere between [start, end], and to find
          the minimum number of jumps to reach the end of the array, we must determine which index will take us the
          farthest in the next jump.

         As we can notice, we are using a greedy approach: always jump to the index that will take us the farthest.

         The idea is to maintain two pointers 'start' and 'end', initially set to 0, such as indices between 0 and
         nums[0] are the ones we can reach by making only 1 jump from the first index.

         Next, we want to find the indices we can reach making 2 jumps, so new 'start' is set to (end + 1) and new 'end'
         is set to the farthest index we can reach by making 2 jumps, which is:

                    end = max(i + nums[i] for i in range(start, end + 1)

        Why do we set start = end + 1?
        Suppose the starting indices of jump 0 are in the range [0, 2]. When looking for the starting indices of the
        next jump, do we still consider the range [0, 2]? The answer is NO! We want to reach the ending position by
        using the least number of jumps possible, so there is no reason in reaching an index in the same range with
        more jumps. Therefore, we shall take a greedy approach that tries to reach each index using the least number of
        jumps and ignore updates that result in more jumps.

         Back to the example, even if we can move to [0, 2] in jump 1, we would not consider doing so since we already
         covered that range with jump 0. If, for instance, nums[1] = 3, the valid range of reachable indices for jump 1
         is [3, 4] instead of [0, 4].

        This problem has a nice BFS structure. Let's illustrate it using the example nums = [2, 3, 1, 1, 4].

        We are initially at position 0. Then we can move at most nums[0] steps from there. So, after one move, we may
        reach nums[1] = 3 or nums[2] = 1. These positions are reachable in 1 move. From there, we can further move to
        nums[3] = 1 and nums[4] = 4. Now we can see that the target nums[4] = 4 is reachable in 2 moves.

        Putting these into code, we keep two pointers 'start' and 'end' that represent the current range of reachable
        indices with the minimal number of jumps possible so far. Each time we make a jump, update 'start' to end+1 and
        'end' to be the farthest index that can be reached in 1 jump from the current range [start, end].

    Time complexity: O(N), we visit each element in the array only once
    Space complexity: O(1)
    """
    n, jumps = len(nums), 0
    start = end = 0
    while end < n - 1:
        farthest_reachable_index = 0
        for i in range(start, end + 1):
            farthest_reachable_index = max(farthest_reachable_index, i + nums[i])
        # Once we have finished iterating over the range of the current jump (we reach 'end'), the next step
        # is to continue iterating over the reachable indices that are beyond farthest_reachable_index, which are
        # represented by the range [end + 1, farthest_reachable_index]
        start, end = end + 1, farthest_reachable_index
        jumps += 1
    return jumps


# Video explanation: https://www.youtube.com/watch?v=vBdo7wtwlXs
def jump_v3(nums):
    """ This solution uses the same concept of the previous algorithm but with a twist.

         Suppose the range of the current jump is [cur_jump_start, cur_jump_end], farthest_reachable_index is the
         farthest position that all indices in [cur_jump_start, cur_jump_end] can reach. Once the current index reaches
         cur_jump_end, then trigger another jump by setting cur_jump_end to farthest_reachable_index, then repeat the
         steps above.

         Note that we exclude the last element from the iteration because as soon as we reach the last element, we do
         not need to jump any further.

         This is an implicit BFS solution. i == cur_jump_end means we visited all the nodes in the current level.
         Incrementing 'jumps' is like incrementing the level we are at. cur_jump_end = farthest_reachable_index is like
         getting the queue size (level size) for the next level we are traversing.

        The idea is pretty intuitive. Think of each of the indices as missile bases, each having a max range defined by
        the value at that index. Now say, for example, we can reach 100 miles from base 0. If the target is in that
        range, then it's just a direct hop. If not, we start our search for better launchers moving forward.

        We discover that base 1 gives better coverage i.e. > 100 miles, so we may simply move to that base.
        This counts as an extra hop. However, that this is not necessarily the best choice. Within the range of this
        launcher (at base 0), there could be other bases providing better coverage. Our job is to iterate through and
        choose the launcher that improves our current range and reaches the target first.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    n, jumps = len(nums), 0
    cur_jump_end = farthest_reachable_index = 0  # cur_jump_end marks the end of the range that we can jump to
    for i in range(n - 1):
        # Extend current coverage/reach as far as possible
        farthest_reachable_index = max(farthest_reachable_index, i + nums[i])
        if i == cur_jump_end:
            # If we have come to the end of the current jump's reach, we need to make another jump
            cur_jump_end = farthest_reachable_index
            jumps += 1
            # Check if we reached the end of the array already (optional)
            # if cur_jump_end >= n - 1:
            #     return jumps
    return jumps
