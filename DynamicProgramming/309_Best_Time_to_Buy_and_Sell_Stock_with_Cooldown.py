""" You are given an array prices where prices[i] is the price of a given stock on the ith day.

Find the maximum profit you can achieve. You may complete as many transactions as you like (i.e., buy one and sell one
share of the stock multiple times) with the following restriction: After you sell your stock, you cannot buy stock on
the next day (i.e., cooldown one day).

Note: You may not engage in multiple transactions simultaneously (i.e., you must sell the stock before you buy again).
"""


def max_profit_v1(prices):
    """ Bottom-Up Dynamic Programming with State Machine.

         Let us treat the problem as a game, and the trader as an agent in the game. The agent can take actions that lead
         to gain or lose of game points (i.e. profits). The goal of the game for the agent is to gain the maximal
         points.

         In addition, we will introduce a tool called state machine, which is a mathematical model of computation. The
         state machine coupled with the dynamic programming technique can help us solve the problem easily.

         The state machine consists of three states, which we define as follows:

            - state "held": in this state, the agent holds a stock that it bought at some point before.

            - state "sold": in this state, the agent has just sold a stock right before entering this state. And the
               agent holds no stock at hand.

            - state "reset": we can consider this state as the starting point, where the agent holds no stock and did
               not sell a stock before. More importantly, it is also the transient state before the held and sold. Due
               to the cooldown rule, after the sold state, the agent can not immediately acquire any stock, but is
               forced into the reset state. We can consider this state as a "reset" button for the cycles of buy and
               sell transactions.

        At any moment, the agent can only be in one state. The agent would transition to another state by performing
        some actions, namely:

            - action "sell": the agent sells a stock at the current moment. After this action, the agent would
               transition to the sold state.

            - action "buy": the agent acquires a stock at the current moment. After this action, the agent would
               transition to the held state.

            - action "rest": this is the action that the agent does no transaction, neither buy nor sell. For instance,
               while holding a stock at the held state, the agent might simply do nothing, and at the next moment the
               agent would remain in the held state.

        Now, we can assemble the above states and actions into a state machine (check the .img file) where each node
        represents a state, and each edge represents a transition between two states. On top of each edge, we indicate
        the action that triggers the transition. Notice that, in all states except the sold state, by doing nothing, we
        would remain in the same state, which is why there is a self-looped transition on these states.

        Now, how exactly does the state machine that we defined help to solve the problem?

        As we mentioned before, we model the problem as a game, and the trader as an agent in the game. And this is
        where the state machine comes into the picture. The behaviors and the states of the game agent can be modeled by
        the state machine.

        Given a list of stock prices (i.e. price[0...n]), the agent would walk through each price point one by one.
        At each point, the agent would be in one of three states (i.e. held, sold and reset) that we defined before. And
        at each point, the agent would take one of the three actions (i.e. buy, sell and rest), which then would lead to
        the next state at the next price point.

        Now, if we chain up each state at each price point, it would form a graph where each path that starts from the
        initial price point and ends at the last price point represents a combination of transactions that the agent
        could perform throughout the game. In each node of the graph, we also indicate the maximal profits that the
        agent has gained so far in each state of each step. And we highlight the path that generates the maximal profits
        (check the .img file).

                    In order to solve the problem, the goal is to find such a path in the graph that
                                                    maximizes the profits.

        In order to implement the above state machine, we could define three arrays (i.e. held[i], sold[i] and reset[i])
        which correspond to the three states that we defined before. Each element in each array represents the maximal
        profits that we could gain at the specific price point i with the specific state.

        For instance, the element sold[2] represents the maximal profits we gain if we sell the stock at the price point
        price[2].

        According to the state machine we defined before, we can then deduce the formulas to calculate the values for
        the state arrays, as follows (check the .img file):

                    sold[i]=hold[i−1] + price[i]
                    held[i]=max(held[i−1], reset[i−1] − price[i])
                    reset[i]=max(reset[i−1], sold[i−1])

        Here is how to interpret each formula:

            - sold[i]: the previous state of sold can only be held. Therefore, the maximal profits of this state is the
               maximal profits of the previous state plus the revenue by selling the stock at the current price.

            - held[i]: the previous state of held could also be held, i.e. one does no transaction. Or its previous
               state could be reset, from which state we can acquire a stock at the current price point.

            - reset[i]: the previous state of reset could either be reset or sold. Both transitions do not involve any
               transaction with the stock.

        Finally, the maximal profits that we can gain from this game would be max(sold[n], reset[n]), i.e. at the last
        price point, either we sell the stock or we simply do no transaction, to have the maximal profits. It makes no
        sense to acquire the stock at the last price point, which only leads to the reduction of profits.

        Summary:

        Think about what we can do on day i: either have one stock or don't have on day i. For each case, we have two
        options, making a total of 4 possible actions on day i:

            - We have 1 stock and sell it
            - We have 1 stock and do nothing
            - We have 0 stock and buy stock i
            - We have 0 stock and do nothing

        Now we want to maximize the total profit but don't know what action to take on day i, so we try all 4 actions on
        every day.
        One detail to emphasize is that the initial value on day 0 is important. We basically cannot take action 1, so
        the corresponding profits should be 0. We cannot take action 2 in practice, but we cannot set up the profit
        to 0 because that means we don't have a stock to sell on day 1. Therefore, the initial profit should be negative
        value of the first stock. Think of it as buying the stock on day -1 and doing nothing on day 0.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    n = len(prices)
    reset, held, sold = [0] * n, [0] * n, [0] * n
    held[0] = -prices[0]  # After buying, we have -prices[0] profit
    reset[0] = 0  # At the start, we don't have any stock if we just rest
    sold[0] = float('-inf')  # Buy and sell on the same day
    for i in range(1, n):
        reset[i] = max(reset[i-1], sold[i-1])
        held[i] = max(held[i-1], reset[i-1] - prices[i])
        sold[i] = held[i-1] + prices[i]
    return max(sold[n -1], reset[n -1])


def max_profit_v2(prices):
    """ Space-optimized Bottom-Up Dynamic Programming.

         We only need the intermediate values at exactly one step before the current step. As a result, rather than
         keeping all the values in the three arrays, we could use a sliding window of size 1 to calculate the value for
         max(sold[n], reset[n]).

    Time complexity: O(N)
    Space complexity: O(1)
    """
    n = len(prices)
    held = -prices[0]
    reset = 0
    sold = 0
    for i in range(1, n):
        sold, held, reset = held + prices[i], max(held, reset - prices[i]), max(reset, sold)
    return max(sold, reset)


def max_profit_v3(prices):
    """ Notice that reset[i] <= sold[i] is also true therefore reset[i] can be simplified:

            reset[i] = max(reset[i−1], sold[i−1])
            --> reset[i] = sold[i−1]

        Substitute this in held[i] we now have 2 functions instead of 3:

                sold[i] = hold[i−1] + price[i]
                held[i] = max(held[i−1], sold[i−2] − price[i])

        If we sell on the ith day, the maximum profit is held[i-1] + price, because we have to buy before we can sell.
        If we buy on the ith day, the maximum profit is sold[i-2] - price, because on the (i-1)th day we can only cool
        down. If we cool down on the ith day, the maximum profit is same as held[i-1] since we did not do anything on
        the ith day. So sold[i] is the larger one of (sold[i-2] - price, held[i-1])

        held[i] is the max profit up to day i with buy as last action. sold[i] is the max profit up to day i with sell
        as last action.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    held = -prices[0]
    sold = 0
    prev_sold = 0
    for price in prices:
        prev_held = held
        held = max(prev_sold - price, prev_held)
        prev_sold = sold
        sold = max(prev_held + price, prev_sold)
    return sold


# Video explanation: https://youtu.be/I7j0F7AHpb8
def max_profit_v4(prices):
    """ Top-Down Dynamic Programming.

         Every day, we have two choices : buy/sell the stock at hand OR ignore and move to the next one. Along with the
         current day, we also need to maintain a buy variable which tells us, if we want to perform a transaction today,
         what type of transaction is permitted (buy or sell).

    Time complexity: O(N)
    Space complexity: O(1)
    """

    def dfs(index, buy):
        if index >= n:
            return 0
        if (index, buy) in memo:
            return memo[(index, buy)]
        no_transaction = dfs(index + 1, buy)
        if buy:
            transact = -prices[index] + dfs(index + 1, False)
        else:
            transact = prices[index] + dfs(index + 2, True)
        memo[(index, buy)] = max(no_transaction, transact)
        return memo[(index, buy)]

    n, memo = len(prices), {}
    return dfs(0, True)

