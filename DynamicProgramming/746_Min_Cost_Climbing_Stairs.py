""" You are given an integer array cost where cost[i] is the cost of ith step on a staircase. Once you pay the cost, you
 can either climb one or two steps.

You can either start from the step with index 0, or the step with index 1.

Return the minimum cost to reach the top of the floor.
"""


def min_cost_climbing_stairs(cost):
    """ Bottom-Up Dynamic Programming

         Before we begin, let's clear up some confusion surrounding the problem statement. The "top of the floor" does
         not refer to the final index of costs. We actually need to "arrive" beyond the array's bounds. For example:
         cost = [10, 15, 20]

						                      __________
				                        ___ | Final step
                                  ___ | 20
                            ___ | 15
            _________ | 10
            First step

        Let's look at an example costs = [0,1,2,3,4,5]. Since we can take 1 or 2 steps at a time, we need to reach
        either step 4 or step 5 (0-indexed), and then pay the respective cost to reach the top. For this example, to
        reach step 4 optimally would cost 2 by taking path 0 --> 2 --> 4 (we're not counting the cost of step 4 yet
        since we are only talking about REACHING the step right now). To reach step 5 optimally would cost 4 by taking
        path 1 --> 3 --> 5.

        Now, imagine that before we started the problem, somebody came up to us and said "to optimally reach step 4
        costs 2 and to optimally reach step 5 costs 4." Well, then the problem is trivial - the answer is the minimum of
        {2 + cost[4] = 6, 4 + cost[5] = 9}. The only reason this was so easy was because we already knew the cost to
        reach steps 4 and 5.

        So how do we find the minimum cost to reach step 4 or step 5? Well, notice that it's the exact same problem,
        just with a smaller input. For example, finding the minimum cost to reach step 4 is like solving the original
        problem with input [0,1,2,3] (step 4 is the "top of the floor" now). To solve this sub-problem, we need to find
        the minimum cost to reach steps 2 and 3, which requires us to answer the original problem for inputs [0,1] and
        [0,1,2].

        This pattern is known as a recurrence relation, and in this case, the minimum cost to reach the ith step is:

                    minimumCost[i] = minimum cost of reaching the ith step starting from either step 0 or step 1
                    minimumCost[i] = min(minimumCost[i - 1] + cost[i - 1], minimumCost[i - 2] + cost[i - 2])

        We get the solution for the ith step by using solutions from earlier steps. So, when does the sequence
        terminate? For this question, the base cases are given in the problem description - we are allowed to start at
        either step 0 or step 1, so minimumCost[0] and minimumCost[1] are both 0.

            - Define an array dp, where dp[i] represents the minimum cost of reaching the ith step. The array should be
               one element longer than costs and start with all elements set to 0. The reason the array should contain
               one additional element is because we will treat the top floor as the step to reach.

            - Iterate over the array starting at the 2nd index. The problem statement says we are allowed to start at
               the 0th or 1st step, so we know the minimum cost to reach those steps is 0.

            - For each step, apply the recurrence relation - dp[i] = min(dp[i - 1] + cost[i - 1], dp[i - 2] + cost[i - 2]).
               As we populate dp, it becomes possible to solve future sub-problems. For example, before solving the 5th
               and 6th steps we are required to solve the 4th step.

            - At the end, return the final element of dp. Remember, we are treating this "step" as the top floor that we
               need to reach.


    Time complexity: O(N)
    Space complexity: O(N)
    """
    n = len(cost)
    dp = [0] * (n + 1)
    # Minimum cost of reaching step 0 and step 1 is 0
    for i in range(2, n + 1):
        # dp[i] = min(reach (i-1)th step and pay (i-1)th cost to take one step,
        #                   reach (i-2)th step and pay (i-2)th cost to take two steps)
        dp[i] = min(dp[i - 1] + cost[i - 1], dp[i - 2] + cost[i - 2])
    return dp[n]


