""" The chess knight has a unique movement, it may move two squares vertically and one square horizontally, or two
squares horizontally and one square vertically (with both forming the shape of an L).

We have a chess knight and a phone pad as shown below, the knight can only stand on a numeric cell.

Given an integer n, return how many distinct phone numbers of length n we can dial.
You are allowed to place the knight on any numeric cell initially and then you should perform n - 1 jumps to dial a
number of length n. All jumps should be valid knight jumps.

As the answer may be very large, return the answer modulo 109 + 7. """


# Great walkthrough of all the possible solutions:
# https://medium.com/hackernoon/google-interview-questions-deconstructed-the-knights-dialer-f780d516f029

def knight_dialer_v1(n):
    """ How can we count phone numbers without generating them? It can be done, but not without an additional insight.
        Notice how the count of numbers that can be generated from a given starting position in N hops is equal to the
        sum of the counts of hops that can be generated starting from each of its neighbors in (N - 1) hops.
        Stated mathematically as a recurrence relation, it looks like this:

            T(P, N) =         Σ           T(p, N-1)
                      {p ∈ neighbors(P)}

            where P is a starting position

        This is intuitively obvious when we consider what happens with one hop: 6, for instance, has 3 neighbors
        (1, 7, and 0) and in zero hops we can reach one number for each, so we can only dial three numbers starting
        from 6.
    Time complexity: O(2^N), every call to dfs() recursively calls dfs() at least twice, because each key has at least
    two neighbors. Since we recurse a number of times equal to the desired number of hops, and the number of calls to
    dfs() at least doubles with each call, we’re left with a runtime complexity of at least exponential time.
    Space complexity: O(N)
    """

    def dfs(i, j, remaining_hops):
        # dfs(i, j, x) returns the number of phone numbers we can dial starting from cell (i,j) with x hops
        if not 0 <= i < 4 or not 0 <= j < 3 or (i == 3 and j != 1):
            # The last condition guarantees that we don't land on a non-numeric cell ('*' or '#')
            return 0
        if remaining_hops == 1:  # The cell we're standing at counts for the last remaining hop to make
            return 1
        res = 0
        for x, y in directions:
            res += dfs(i + x, j + y, remaining_hops - 1)
        return res

    directions = [(-1, 2), (-2, 1), (-1, -2), (-2, -1), (1, 2), (2, 1), (1, -2), (2, -1)]
    res = 0
    for i in range(4):
        for j in range(3):
            res += dfs(i, j, n)
    return res % (10 ** 9 + 7)


def knight_dialer_v2(n):
    """" This is same as previous solution, but it uses a hash map to compute the keys to which we can hop from a
        given position, also known as the neighbors.
    Time complexity: O(2^N)
    Space complexity: O(N)
    """

    def dfs(cell, remaining_hops):
        if remaining_hops == 1:
            return 1
        res = 0
        for neighbor in next_hop[cell]:
            res += dfs(neighbor, remaining_hops - 1)
        return res

    next_hop = {0: (4, 6), 1: (6, 8), 2: (7, 9), 3: (4, 8), 4: (0, 3, 9), 5: (), 6: (0, 1, 7), 7: (2, 6), 8: (1, 3),
                9: (2, 4)}
    res = 0
    for i in range(10):
        res += dfs(i, n)
    return res % (10 ** 9 + 7)


def knight_dialer_v3(n):
    """ Can we do better? The crucial insight here is that many function calls repeat, each time returning the same
        value. After we compute their result once there’s no need to recompute them. We can use memoization, which
        basically means we record results of function calls we’ve seen before and use those instead of redoing the work.
    Time complexity: O(N), each function call’s result is stored in the cache, and it’s inserted there exactly once.
    This allows us to re-frame the question as “how does the size of the cache grow with the size of the input?” Given
    that the cache is keyed by position and number of hops, and there are exactly 10 positions, we can conclude that
    the cache grows in direct proportion to the number of requested hops. This follows from the pigeonhole principle:
    Once we have an entry in the cache for every combination of position and jump count, all calls will hit the cache
    rather than result in a new function call.
    Space complexity: O(N)
    """

    def dfs(cell, remaining_hops):
        if (cell, remaining_hops) in cache:
            return cache[(cell, remaining_hops)]
        if remaining_hops == 1:
            return 1
        res = 0
        for neighbor in next_hop[cell]:
            res += dfs(neighbor, remaining_hops - 1)
        cache[(cell, remaining_hops)] = res
        return res

    next_hop = {0: (4, 6), 1: (6, 8), 2: (7, 9), 3: (4, 8), 4: (0, 3, 9), 5: (), 6: (0, 1, 7), 7: (2, 6), 8: (1, 3),
                9: (2, 4)}
    cache = {}
    res = 0
    for i in range(10):
        res += dfs(i, n)
    return res % (10 ** 9 + 7)


def knight_dialer_v4(n):
    """ Bottom-up Dynamic Programming.
        The minor limitation of the recursive memoizing solution is clear when we look at the recurrence relation:

             T(P, N) =         Σ           T(p, N-1)
                      {p ∈ neighbors(P)}

            where P is a starting position

        Notice that the results for N hops depend only on the results for calls with (N - 1) hops. Meanwhile, the cache
        contains entries for every (nonzero) number of hops. Also notice that the code starts with the largest number
        of hops and recurses directly down to the smallest. If we imagine the entire function call graph as a sort of
        virtual tree, we’ll quickly see we’re performing a depth-first traversal.
        Can we perform a breadth-first traversal instead, where we start at the top and “visit” function calls for
        (N - 1) hops only after we’ve visited those for N hops? Sadly, no. The values of function calls with nonzero
        hops absolutely require the values from smaller hop counts, so we won’t get any results until we reach the
        1-hop layer and start returning numbers rather than additional function calls
        We can, however, reverse the order: Visit layers with N hops only after we’ve visited layers with (N - 1)
        hops. We know that the values of 1-hop function calls are always equal to 1 (the base case). We also know how
        to combine (N - 1) hop values to get N hop values, using the recurrence relation. We can start with a base case
        of 1 hop and induce all values greater than 1.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    next_hop = {0: (4, 6), 1: (6, 8), 2: (7, 9), 3: (4, 8), 4: (0, 3, 9), 5: (), 6: (0, 1, 7), 7: (2, 6), 8: (1, 3),
                9: (2, 4)}
    cur_counts = [1] * 10  # cur_counts[i] is the number of phone number we can dial starting from position (digit) i
    # at the current iteration
    for _ in range(n - 1):  # The phone number needs to have a length n (n hops)
        next_counts = [0] * 10
        for cell in range(10):
            for neighbor in next_hop[cell]:
                next_counts[cell] += cur_counts[neighbor]  # This is the recurrence relation
        cur_counts = next_counts
    return sum(cur_counts) % (10 ** 9 + 7)
