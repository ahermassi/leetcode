""" You are climbing a stair case. It takes n steps to reach to the top.
Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top? """


def climb_stairs_v1(n):
    """ This is the classic/intuitive recursive solution. However, it returns TLE.
    Time complexity: O(2 ** n), size of recursion tree will be 2 ** n
    Space complexity: O(n)
    """
    if n == 1:
        return 1
    if n == 2:
        return 2
    return climb_stairs_v1(n - 1) + climb_stairs_v1(n - 2)


def climb_stairs_v2(n):
    """ Top down + memoization (list)
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
    Time complexity: O(N)
    Space complexity: O(N)
    """

    def climb(n):
        if n == 1 or n == 2:  # Base cases
            return n
        if memo[n]:
            return memo[n]
        else:
            res = climb(n - 1) + climb(n - 2)
            memo[n] = res
        return res

    memo = [None] * (n + 1)
    return climb(n)


def climb_stairs_v3(n):
    """ Top down + memoization (dictionary)
    Time complexity: O(N)
    Space complexity: O(N)
    """
    def climb(n):
        if n in memo:
            return memo[n]
        else:
            res = climb(n - 1) + climb(n - 2)
            memo[n] = res
        return res

    memo = {1: 1, 2: 2}  # Base cases
    return climb(n)





