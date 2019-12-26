""" You are climbing a stair case. It takes n steps to reach to the top.
Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top? """


def climb_stairs_v1(n):
    """ This is the classic/intuitive recursive solution. However, it returns TLE.
        To reach nth step, what could have been our previous steps? Either (n-1) or (n-2)
    Time complexity: O(2^n), we have n levels and at each level we can make 2 choices, O(b^d)
    Space complexity: O(n)
    """
    if n <= 2:
        return n
    return climb_stairs_v1(n-1) + climb_stairs_v1(n-2)


def climb_stairs_v2(n):
    """ Top down + memoization
        Here are the steps to get the solution incrementally:
        Base cases:
            if n == 1, then there is only one NEW way to climb the stair.
            if n == 2, then there are two NEW ways to climb the stairs.
        The key intuition to solve the problem is that given a number of stairs n, if we know the number of ways to get
        to the points [n-1] and [n-2] respectively, denoted as n1 and n2 , then the total ways to get to the point [n]
        is n1 + n2. Because from the [n-1] point, we can take one single step to reach [n]. And from the [n-2] point,
        we could take two steps to get there.
        Now given the above intuition, one can construct an array where each node stores the solution for each number
        n. Or if we look at it closer, it is clear that this is basically a fibonacci number, with the starting numbers
        as 1 and 2, instead of 1 and 1.
    Time complexity: O(n)
    Space complexity: O(n)
    """

    def climb(n):
        if n in memo:
            return memo[n]
        res = climb(n - 1) + climb(n - 2)
        memo[n] = res
        return res

    memo = {0: 0, 1: 1, 2: 2}  # Base cases
    return climb(n)


def climb_stairs_v4(n):
    """ DP is all about caching the answers to previous work and using it in current work.
        dp[n] denotes the number of ways to climb n steps if we can take 1 or 2 steps.
        dp[n] = dp[n - 1] + dp[n - 2]
    Time complexity: O(n)
    Space complexity: O(n)
    """
    dp = [None] * (n + 1)
    dp[0] = dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[-1]


def climb_stairs_v5(n):
    """ No need to store every middle result. We notice that this is just the Fibonacci series. We can just use local
        variables to keep track of the items 1 and 2 behind where we stand.
    Time complexity: O(n)
    Space complexity: O(1)
    """
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a



