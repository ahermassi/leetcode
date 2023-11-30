""" You are climbing a stair case. It takes n steps to reach to the top.
Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top? """


# Video explanation for all solutions: https://youtu.be/Y0lT9Fck7qI

def climb_stairs_v1(n):
    """ Brute force recursive solution. TLE.

        To calculate the number of ways to climb the stairs, we can observe that when we are on the nth stair, we have
        two options:

            - Either we climbed one stair from the (n-1)th stair, or
            - We climbed two stairs from the (n-2)th stair

        By leveraging this observation, we can break down the problem into smaller sub-problems and apply the concept of
        the Fibonacci series.

        The base cases are:

            - n=1: There's only 1 way to climb a singular step - just climb that step! We couldn't possibly take 2
               steps in this situation, because then we'd be climbing more steps than there are to climb.

            - n=2: We can either climb the 2 steps by taking 2 steps, or climb 1 step twice, for a total of 2 ways to
               climb.

        The number of ways to reach step n depends on the number of ways to get to (n-1)th step and the number of ways
        to get to (n-2)th step n−2n - 2n−2. Since both of the above possibilities are valid choices, the number of ways
        to get to n is going to be their sum.

        Why sum?

        Think about what happens on the nth step. We can get to it either from (n-1)th step, or from (n-2)th step.
        Say there are x distinct ways to get to (n-1)th step, and y distinct ways to get to (n-2)th step.

        For (n-1), to get to n we just need to add 1 to the end of each of those x paths that lead here. That does not
        change the number of those paths in which we're interested -- it just makes them all acquire a 'tail' of 1.

        For (n-2), to get to n we will need to add 2 to each of the y paths that lead there. That also doesn't change
        the number of the paths that lead to it, just makes them all acquire a 'tail' of 2.

        What actually happens at the step of n, is we're adding up those two groups of possible ways to get to n.

    Time complexity: O(2^n), we have n levels and at each level we can make 2 choices, O(b^d)
    Space complexity: O(n)
    """
    if n <= 2:
        return n
    return climb_stairs_v1(n-1) + climb_stairs_v1(n-2)


def climb_stairs_v2(n):
    """ Top down DP + memoization

         In the previous approach, we are redundantly calculating the result for every step. Let's think about
         calculating the ways to climb 6 stairs, climbStairs(6).

                                                    climbStairs(6)
									            /                          \
								            cS(5)       +                 cS(4)
					                        /    \                          /    \
			                            cS(4)   +   cS(3)            cS(3) + cS(2)
						                /  \           /   \              /   \
				                  cS(3) + cS(2) cS(2) + cS(1)  cS(2) + cS(1)
					              /  \
			                  cS(2) + cS(1)

        As we can see from the recursion tree above, we are calculating climbStairs(4) and climbStairs(3) multiple
        times. Specifically, climbStairs(4) is being recalculated twice, while climbStairs(3) is being recalculated
        3 times. If we think about what happens for larger values of n, we can see that we are recalculating a lot of
        values.

        What if instead of recomputing each value of climbStairs, we made sure to save the unique values, trading space
        for time? That's what a top-down dynamic programming approach called memoization is. We make use of a
        dictionary memo in which we store the values of climbStairs that we have computed, and if we ever have to
        compute that value again we just check memo in (average) O(1) time instead of doing the work all over again.

         In this way, we are pruning recursion tree with the help of memo map and educing the size of recursion tree
         down to n.

         This top-down paradigm works well when we approach the problem from the top of the stairs (the last step we
         needed to climb, n) down.

    Time complexity: O(n), there are n distinct sub-problems to solve, each requiring only O(1) amount of work of
    getting the values of smaller sub-problems from memo and adding them together.
    Space complexity: O(n)
    """

    def climb(n):
        if n not in memo:
            memo[n] = climb(n-1) + climb(n-2)
        return memo[n]

    memo = {1: 1, 2: 2}  # Base cases
    return climb(n)


def climb_stairs_v3(n):
    """ As we can see, this problem can be broken into sub-problems, and it contains the optimal substructure property
        i.e. its optimal solution can be constructed efficiently from optimal solutions of its sub-problems. We can use
        dynamic programming to solve the problem.
        We can reach ith step in one of the two ways:
            1- Taking a single step from (i−1)th step
            2- Taking a step of 2 from (i-2)th step
        Let dp[i] denote the number of ways to reach ith step if we can take 1 or 2 steps:
            dp[i] = dp[i-1] + dp[i-2]
    Time complexity: O(n)
    Space complexity: O(n)
    """
    dp = [0] * (n + 1)  # We create an array of size (n + 1) so we can just return dp[n] at the end instead of fumbling
    # with dp[n-1]
    dp[0] = dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]


def climb_stairs_v4(n):
    """ No need to store every middle result. We notice that this is just the Fibonacci series. We can just use local
        variables to keep track of the items 1 step and 2 steps behind where we stand.
    Time complexity: O(n)
    Space complexity: O(1)
    """
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a



