""" You have a pointer at index 0 in an array of size arrLen. At each step, you can move 1 position to the left,
1 position to the right in the array, or stay in the same place (The pointer should not be placed outside the array
at any time).

Given two integers steps and arrLen, return the number of ways such that your pointer still at index 0 after exactly
'steps' steps. Since the answer may be too large, return it modulo 109 + 7. """


def num_ways_v1(steps, arr_len):
    """ Top-Down Dynamic Programming.

        We can use a simple DFS/recursion to form the solution. We also use memoization to cache all our answers.

    Time complexity: O(3^steps) without memoization, O(steps^2) with memoization
    Space complexity: O(steps * arr_len), the space is the memo size which is the whole recursion tree size, not just
    the depth. To determine the size, there two dimensions we need to consider, steps and position/index.
    """

    def dfs(index, remaining_steps):
        if (index, remaining_steps) in memo:
            return memo[(index, remaining_steps)]
        if index < 0 or index >= arr_len or remaining_steps < 0:
            return 0
        if index == remaining_steps == 0:
            return 1
        res = dfs(index + 1, remaining_steps - 1) + dfs(index - 1, remaining_steps - 1) + \
              dfs(index, remaining_steps - 1)
        memo[(index, remaining_steps)] = res
        return res

    memo = {}
    return dfs(0, steps) % (10 ** 9 + 7)


def num_ways_v2(steps, arr_len):
    """ Bottom-Up Dynamic Programming.

        Let dp[step][index] be the number of ways to stay at index 'index' after exactly 'step' steps. From this state
        we can either:

        Stay. Then we consume one step and stay at the same position => dp[step - 1][index]
        Go right. Then we consume one step and go right              => dp[step - 1][index + 1]
        Go left. Then we consume one step and go left                => dp[step - 1][index - 1]

        Then our state can be calculated as:

                dp[step][index] = dp[step-1][index] + dp[step-1][index+1] + dp[step-1][index-1]

        The base case is when we want to stay at index 0 with exactly 0 steps to move. There is only 1 way which is to
        stay.

    Time complexity: O(steps * arr_len)
    Space complexity: O(steps * arr_len)
    """
    dp = [[0] * arr_len for _ in range(steps + 1)]
    dp[0][0] = 1
    for step in range(1, steps + 1):
        for index in range(arr_len):
            dp[step][index] = dp[step - 1][index]
            if index < arr_len - 1:
                dp[step][index] += dp[step - 1][index + 1]
            if index > 0:
                dp[step][index] += dp[step - 1][index - 1]
    return dp[steps][0] % (10 ** 9 + 7)


def num_ways_v3(steps, arr_len):
    """ Unfortunately, the previous solution TLEs.

        Notice that we can only go right as far as many steps we have. For example, for 500 steps, we can only go as
        far as the 500th position, doesn't matter if the arrLen is 99999999. So the array size can be larger than the
        number of steps. We can ignore array elements greater than (steps / 2), as we won't able to go back to the
        first element from there. If we travel 50 steps forward, we need 50 steps to go back to the first element.
        So, if we have 100 total steps, we can ignore elements 51 and later.

    Time complexity: O(steps * min(arr_len, steps))
    Space complexity: O(steps * min(arr_len, steps))
    """
    arr_len = min(arr_len, steps // 2 + 1)
    dp = [[0] * arr_len for _ in range(steps + 1)]
    dp[0][0] = 1
    for step in range(1, steps + 1):
        for index in range(arr_len):
            dp[step][index] = dp[step - 1][index]
            if index < arr_len - 1:
                dp[step][index] += dp[step - 1][index + 1]
            if index > 0:
                dp[step][index] += dp[step - 1][index - 1]
    return dp[steps][0] % (10 ** 9 + 7)


def num_ways_v4(steps, arr_len):
    """ Bottom-Up Dynamic Programming with space compression.

    Time complexity: O(steps * min(arr_len, steps))
    Space complexity: O(min(arr_len, steps)) if true recycling of arrays is used, but if implemented like below we'll
    be still allocating (steps + 1) times new array, making the space complexity O(steps * min(arr_len, steps))
    """
    arr_len = min(arr_len, steps // 2 + 1)
    prev_dp = [0] * arr_len
    prev_dp[0] = 1
    for step in range(1, steps + 1):
        cur_dp = [0] * arr_len
        for index in range(arr_len):
            cur_dp[index] = prev_dp[index]
            if index < arr_len - 1:
                cur_dp[index] += prev_dp[index + 1]
            if index > 0:
                cur_dp[index] += prev_dp[index - 1]
        # We could also create prev_dp and cur_dp before the loop and swap prev_dp and cur_dp after each loop.
        # This is true recycling.
        # prev_dp, cur_dp = cur_dp, pre_dp
        prev_dp = cur_dp
    return prev_dp[0] % (10 ** 9 + 7)

