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
    return dfs(0, steps) % (pow(10, 9) + 7)
