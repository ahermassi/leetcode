""" You are climbing a stair case. It takes n steps to reach to the top.
Each time you can either climb k steps. In how many distinct ways can you climb to the top ? """


def number_of_ways_to_top(n, k) -> int:
    """ Pretty straightforward, generalizing the climbing stairs problem.
        Example: n = 4, k = 2
        dp(4) = dp(4- 2) + dp(4- 1).
        Recursing, dp(4-2) = dp(4-2-2) + dp(4-2-1).
        Both dp(0) and dp(1) are base-cases, with a value of 1, so dp(4-2) = 2.
        Continuing with dp(4-1), dp(4-1) = dp(4-1-2) + dp(4-1-1). The first term is a base case, with a value of 1.
        The second term has already been computed; its value is 2. Therefore, dp(4-1) = 3, and dp(4)= 3 + 2 = 5.
    Time complexity: O(nk)
    Space complexity: O(n)
    """
    dp = [0] * (n + 1)
    dp[0] = dp[1] = 1
    for i in range(2, n+1):
        for j in range(i-k, i):
            dp[i] += dp[j]
    return dp[n]